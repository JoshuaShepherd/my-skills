---
name: security-setup
description: "Harden a Next.js 15 or Vite + Express app for production — Content Security Policy headers, rate limiting (Upstash Redis), CORS policy, API input validation, secret scanning, and security checklist. Use before launching any project or when auditing security posture."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up security hardening: $ARGUMENTS

$ARGUMENTS can include:
- "audit" — scan codebase for security issues and report (no changes)
- "full" — CSP + rate limiting + CORS + validation hardening (default)
- "headers-only" — just HTTP security headers
- "rate-limiting" — just Upstash rate limiting
- Framework hint: "nextjs" or "vite" (auto-detected)
- Empty — full hardening, auto-detect framework

---

## Before Starting

1. Read `package.json` to detect framework
2. Read `src/middleware.ts` — add security headers there
3. Read `next.config.ts` — add HTTP headers config
4. Read `src/app/api/` — find API routes needing rate limiting
5. Check if `@upstash/ratelimit` or `@upstash/redis` is installed

---

## Architecture

### Next.js
```
next.config.ts         ← HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
src/middleware.ts      ← Rate limiting + auth check before route handling
src/lib/security/
  rate-limit.ts        ← Upstash rate limiter helpers
  validate-request.ts  ← Reusable API input validator
  csrf.ts              ← CSRF token helpers (if using forms)
```

### Vite + Express
```
server/middleware/
  security-headers.ts  ← helmet() + CSP config
  rate-limit.ts        ← express-rate-limit config
  cors.ts              ← CORS config
```

---

## Step 1 — HTTP Security Headers (Next.js)

Edit `next.config.ts` to add security headers:

```typescript
import type { NextConfig } from "next";

const securityHeaders = [
  // Prevent MIME type sniffing
  { key: "X-Content-Type-Options", value: "nosniff" },
  // Prevent clickjacking
  { key: "X-Frame-Options", value: "SAMEORIGIN" },
  // Enable HSTS (1 year, include subdomains)
  { key: "Strict-Transport-Security", value: "max-age=31536000; includeSubDomains" },
  // Referrer policy
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  // Permissions policy — disable features you don't use
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), payment=(self)",
  },
  // Content Security Policy
  // Start in report-only mode, then switch to enforcing
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com https://www.googletagmanager.com",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob: https://*.supabase.co https://*.supabase.in https://lh3.googleusercontent.com",
      "font-src 'self'",
      "connect-src 'self' https://*.supabase.co https://*.supabase.in wss://*.supabase.co https://api.stripe.com https://www.google-analytics.com",
      "frame-src https://js.stripe.com",
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self'",
      "upgrade-insecure-requests",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
```

**Tuning the CSP:** After deploy, check browser console for CSP violations and add the blocked origins to the appropriate directive. Never use `unsafe-eval` in production unless absolutely required (GSAP/canvas may need it — check first).

---

## Step 2 — Rate Limiting (Next.js Middleware)

Install:
```bash
pnpm add @upstash/ratelimit @upstash/redis
```

Add to `.env.local` and `.env.example`:
```bash
# Upstash Redis (upstash.com — free tier available)
UPSTASH_REDIS_REST_URL=https://...upstash.io
UPSTASH_REDIS_REST_TOKEN=...
```

Create `src/lib/security/rate-limit.ts`:

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

// Lazy initialization — only connects when first used
let redis: Redis | null = null;

function getRedis() {
  if (!redis) {
    redis = new Redis({
      url: process.env.UPSTASH_REDIS_REST_URL!,
      token: process.env.UPSTASH_REDIS_REST_TOKEN!,
    });
  }
  return redis;
}

// 10 requests per 10 seconds per IP — for API routes
export const apiRateLimit = new Ratelimit({
  redis: getRedis(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  analytics: true,
});

// 5 requests per minute — for auth routes (login, signup)
export const authRateLimit = new Ratelimit({
  redis: getRedis(),
  limiter: Ratelimit.slidingWindow(5, "60 s"),
  analytics: true,
});

// 3 requests per hour — for expensive AI routes
export const aiRateLimit = new Ratelimit({
  redis: getRedis(),
  limiter: Ratelimit.slidingWindow(3, "3600 s"),
  analytics: true,
});
```

Apply in middleware or API routes:

```typescript
// In an API route:
import { apiRateLimit } from "@/lib/security/rate-limit";
import { NextResponse } from "next/server";
import { headers } from "next/headers";

export async function POST(request: Request) {
  const headersList = await headers();
  const ip = headersList.get("x-forwarded-for") ?? "unknown";

  const { success, limit, remaining } = await apiRateLimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: "Too many requests" },
      {
        status: 429,
        headers: {
          "X-RateLimit-Limit": limit.toString(),
          "X-RateLimit-Remaining": remaining.toString(),
          "Retry-After": "10",
        },
      }
    );
  }

  // ... handler logic
}
```

**No Upstash?** For simpler projects without Redis, use in-memory rate limiting:

```bash
pnpm add rate-limiter-flexible
```

---

## Step 3 — API Input Validation Pattern

Create `src/lib/security/validate-request.ts`:

```typescript
import { NextResponse } from "next/server";
import type { ZodSchema } from "zod";

type Result<T> = { ok: true; data: T } | { ok: false; response: NextResponse };

export async function validateBody<T>(
  request: Request,
  schema: ZodSchema<T>
): Promise<Result<T>> {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return {
      ok: false,
      response: NextResponse.json({ error: "Invalid JSON" }, { status: 400 }),
    };
  }

  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return {
      ok: false,
      response: NextResponse.json(
        { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
        { status: 422 }
      ),
    };
  }

  return { ok: true, data: parsed.data };
}
```

Usage in API routes:
```typescript
import { validateBody } from "@/lib/security/validate-request";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(1).max(1000),
});

export async function POST(request: Request) {
  const result = await validateBody(request, schema);
  if (!result.ok) return result.response;

  const { email, message } = result.data;
  // ... safe to use
}
```

---

## Step 4 — Security Audit Checklist

Run this checklist before every production deploy:

### Secrets
```bash
# Check for committed secrets
git log --all --full-history -- ".env*" | head -20
grep -rn "sk_live_\|sk_test_\|AKIA\|-----BEGIN" src/ --include="*.ts" | grep -v ".test."
# Should return nothing
```

### Exposed APIs
- [ ] All API routes check authentication before processing
- [ ] Mutation routes (POST/PUT/PATCH/DELETE) validate request body with Zod
- [ ] No `console.log(req)` calls in production code (leaks headers/auth tokens)
- [ ] Error responses don't include stack traces or internal details

### Dependencies
```bash
pnpm audit                     # Check for known vulnerabilities
pnpm outdated | head -20       # Check for outdated packages
```

### Headers
- [ ] `X-Content-Type-Options: nosniff` — present
- [ ] `X-Frame-Options: SAMEORIGIN` — present
- [ ] `Strict-Transport-Security` — present (HTTPS only)
- [ ] CSP header — present, `unsafe-eval` removed if possible

### Supabase
- [ ] RLS enabled on all tables with user data
- [ ] Service role key not in client code
- [ ] `anon` role only has SELECT on public data

---

## Step 5 — HTTP Security Headers (Vite + Express)

```bash
pnpm add helmet cors express-rate-limit
```

Create `server/middleware/security.ts`:

```typescript
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import type { Express } from "express";

export function applySecurityMiddleware(app: Express) {
  // Helmet sets secure HTTP headers
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'", "https://js.stripe.com"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https://*.supabase.co"],
        connectSrc: ["'self'", "https://*.supabase.co"],
        frameSrc: ["https://js.stripe.com"],
        objectSrc: ["'none'"],
      },
    },
    crossOriginEmbedderPolicy: false, // May break some CDN assets
  }));

  // CORS — restrict to your frontend domain
  app.use(cors({
    origin: process.env.APP_URL ?? "http://localhost:5173",
    credentials: true,
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  }));

  // Rate limiting
  app.use("/api", rateLimit({
    windowMs: 10 * 1000,
    max: 10,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: "Too many requests" },
  }));
}
```

---

## Verify

1. `pnpm typecheck` — no errors
2. Deploy to Vercel preview → check response headers in DevTools → Network
3. Verify CSP header is present and correct
4. `pnpm audit` — no critical vulnerabilities
5. Test rate limiting: send 11 requests in 10 seconds → 429 response on 11th

---

## Anti-Patterns

- NEVER disable CSP entirely — use `report-only` while tuning instead
- NEVER use `Access-Control-Allow-Origin: *` on routes that handle auth
- NEVER return detailed error messages (stack traces, DB errors) to clients
- NEVER skip input validation on mutation routes — assume all input is hostile
- NEVER store sensitive data in `localStorage` — use httpOnly cookies
