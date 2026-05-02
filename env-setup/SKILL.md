---
name: env-setup
description: "Scaffold and validate environment variables for Next.js 15 or Vite + Express — Zod-validated env schema, .env.example with all required vars, runtime validation that fails fast on missing values, and a check:env script. Use when starting a new project or auditing env var hygiene."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up environment variable validation: $ARGUMENTS

$ARGUMENTS can include:
- "audit" — scan existing codebase for unvalidated env vars and fix
- "nextjs" or "vite" — framework hint (auto-detected)
- "full" — generate .env.example + Zod schema + check script (default)
- Empty — full setup, auto-detect framework

---

## Before Starting

1. Read `package.json` to detect framework and see existing scripts
2. Check if `src/lib/env.ts` already exists — update rather than overwrite
3. Read `.env.example` or `.env.local.example` if present
4. Grep for `process.env.` and `import.meta.env.` — find all usages to catalog vars
5. Read `src/lib/config/tenant.config.ts` for tenant-specific vars

---

## Architecture

```
src/lib/env.ts        ← Zod-validated env schema — single source of truth
.env.example          ← All vars with empty values + comments — committed to git
.env.local            ← Real values — in .gitignore, never committed
scripts/check-env.ts  ← CLI script: validates env before build/deploy
```

---

## Step 1 — Audit Existing Env Var Usage

Run these before writing anything new:

```bash
# Find all process.env usages
grep -rn "process\.env\." src/ --include="*.ts" --include="*.tsx" | grep -v ".test." | sort -u

# Find all import.meta.env usages (Vite)
grep -rn "import\.meta\.env\." src/ --include="*.ts" --include="*.tsx" | sort -u
```

Catalog every var found — this drives what goes in the schema.

---

## Step 2 — Zod Env Schema (Next.js 15)

Create or update `src/lib/env.ts`:

```typescript
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  /**
   * Server-side environment variables.
   * Available in Server Components, API Routes, and server actions.
   * NEVER accessible in the browser.
   */
  server: {
    // Database
    DATABASE_URL: z.string().url(),

    // Supabase (server-only)
    SUPABASE_SERVICE_ROLE_KEY: z.string().min(1).optional(),

    // Auth
    // (none needed — Supabase handles auth keys)

    // Tenant
    TENANT_ORG_ID: z.string().uuid(),

    // Email (Resend)
    RESEND_API_KEY: z.string().startsWith("re_").optional(),
    RESEND_FROM_EMAIL: z.string().email().optional(),
    RESEND_FROM_NAME: z.string().min(1).optional(),

    // Payments (Stripe)
    STRIPE_SECRET_KEY: z.string().startsWith("sk_").optional(),
    STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_").optional(),

    // Monitoring (Sentry)
    SENTRY_DSN: z.string().url().optional(),
    SENTRY_ORG: z.string().optional(),
    SENTRY_PROJECT: z.string().optional(),
    SENTRY_AUTH_TOKEN: z.string().optional(),

    // AI
    OPENAI_API_KEY: z.string().startsWith("sk-").optional(),
  },

  /**
   * Client-side environment variables.
   * Must be prefixed with NEXT_PUBLIC_.
   * These are bundled into the browser build — treat as public.
   */
  client: {
    NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
    NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
    NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),

    // Payments
    NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().startsWith("pk_").optional(),

    // Analytics
    NEXT_PUBLIC_GA4_MEASUREMENT_ID: z.string().optional(),
    NEXT_PUBLIC_POSTHOG_KEY: z.string().optional(),
    NEXT_PUBLIC_POSTHOG_HOST: z.string().url().optional(),
  },

  /**
   * Destructuring map — Next.js requires explicit mapping for process.env
   */
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
    TENANT_ORG_ID: process.env.TENANT_ORG_ID,
    RESEND_API_KEY: process.env.RESEND_API_KEY,
    RESEND_FROM_EMAIL: process.env.RESEND_FROM_EMAIL,
    RESEND_FROM_NAME: process.env.RESEND_FROM_NAME,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
    SENTRY_DSN: process.env.SENTRY_DSN,
    SENTRY_ORG: process.env.SENTRY_ORG,
    SENTRY_PROJECT: process.env.SENTRY_PROJECT,
    SENTRY_AUTH_TOKEN: process.env.SENTRY_AUTH_TOKEN,
    OPENAI_API_KEY: process.env.OPENAI_API_KEY,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
    NEXT_PUBLIC_GA4_MEASUREMENT_ID: process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID,
    NEXT_PUBLIC_POSTHOG_KEY: process.env.NEXT_PUBLIC_POSTHOG_KEY,
    NEXT_PUBLIC_POSTHOG_HOST: process.env.NEXT_PUBLIC_POSTHOG_HOST,
  },

  /**
   * Skip env validation in CI builds that don't need all vars.
   * Never skip in production.
   */
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
});
```

Install: `pnpm add @t3-oss/env-nextjs`

---

## Step 3 — Zod Env Schema (Vite)

For Vite projects, use `@t3-oss/env-core` instead:

```typescript
import { createEnv } from "@t3-oss/env-core";
import { z } from "zod";

export const env = createEnv({
  clientPrefix: "VITE_",
  server: {
    DATABASE_URL: z.string().url(),
    STRIPE_SECRET_KEY: z.string().startsWith("sk_").optional(),
    // ... same pattern
  },
  client: {
    VITE_SUPABASE_URL: z.string().url(),
    VITE_SUPABASE_ANON_KEY: z.string().min(1),
    // ...
  },
  runtimeEnv: import.meta.env,
  skipValidation: import.meta.env.CI === "true",
});
```

Install: `pnpm add @t3-oss/env-core`

---

## Step 4 — .env.example

Create `.env.example` with every variable, empty values, and inline comments:

```bash
# =============================================================================
# REQUIRED — app will not start without these
# =============================================================================

# Database (Supabase connection string from Project Settings → Database → URI)
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Supabase (Project Settings → API)
NEXT_PUBLIC_SUPABASE_URL=https://[project-ref].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Tenant (your organization's UUID from the organizations table)
TENANT_ORG_ID=

# App URL (no trailing slash)
NEXT_PUBLIC_APP_URL=http://localhost:3000

# =============================================================================
# OPTIONAL — features degrade gracefully without these
# =============================================================================

# Supabase service role (server-only, for admin operations)
# SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Email (Resend — resend.com/api-keys)
# RESEND_API_KEY=re_...
# RESEND_FROM_EMAIL=hello@yourdomain.com
# RESEND_FROM_NAME=Your App

# Payments (Stripe — dashboard.stripe.com/apikeys)
# NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_...

# Analytics
# NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-...
# NEXT_PUBLIC_POSTHOG_KEY=phc_...
# NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com

# Error Monitoring (Sentry)
# SENTRY_DSN=https://...@sentry.io/...
# NEXT_PUBLIC_SENTRY_DSN= (same as above, for client-side)

# AI
# OPENAI_API_KEY=sk-...
```

---

## Step 5 — check:env Script

Create `scripts/check-env.ts`:

```typescript
#!/usr/bin/env tsx
/**
 * Validates all required environment variables are set.
 * Run before deploy: pnpm check:env
 */

import { z } from "zod";

const REQUIRED = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  TENANT_ORG_ID: z.string().uuid(),
});

const result = REQUIRED.safeParse(process.env);

if (!result.success) {
  console.error("❌ Missing or invalid environment variables:\n");
  result.error.errors.forEach((err) => {
    console.error(`  ${err.path.join(".")}: ${err.message}`);
  });
  console.error("\nSee .env.example for the full list of required variables.");
  process.exit(1);
}

console.log("✅ All required environment variables are set.");
```

Add to `package.json`:
```json
{
  "scripts": {
    "check:env": "tsx scripts/check-env.ts"
  }
}
```

Install: `pnpm add -D tsx`

---

## Step 6 — .gitignore Verification

Ensure these lines are in `.gitignore`:
```
.env
.env.local
.env.*.local
# But DO commit:
# .env.example ← intentionally not in .gitignore
```

---

## Step 7 — Import Pattern

Replace all raw `process.env.X` with `env.X` in the codebase:

```typescript
// Before (unvalidated, no type safety)
const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;

// After (Zod-validated, typed)
import { env } from "@/lib/env";
const url = env.NEXT_PUBLIC_SUPABASE_URL;
```

---

## Verify

1. `pnpm check:env` — passes with current `.env.local`
2. Remove a required var from `.env.local`, run `pnpm check:env` — should fail with clear error
3. `pnpm typecheck` — env.ts has no errors
4. `pnpm build` — build succeeds (or fails fast with clear env error if var is missing)

---

## Anti-Patterns

- NEVER commit `.env.local` or `.env` — only `.env.example`
- NEVER use `!` non-null assertions on `process.env.X` — use Zod schema instead
- NEVER put secrets in client-side vars (`NEXT_PUBLIC_` prefix)
- NEVER skip validation with `SKIP_ENV_VALIDATION=true` in production
- NEVER hardcode URLs or API keys in source files — always use env vars
