---
name: vercel-audit
description: Audit Vercel deployment configuration for correctness and optimization — vercel.json, serverless functions, environment variables, headers, rewrites, and regions. Use before deploying or after config changes.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

Audit the Vercel deployment configuration for this Vite + Express SPA project. Check for correctness, security, and optimization opportunities.

Target: $ARGUMENTS (default: full audit)

## Pre-flight

1. Read `vercel.json`, `package.json`, `api/index.ts`, and `.env.local` (if exists).
2. Read `server/index.ts` to understand the Express handler shape.
3. Glob for any additional `api/**/*.ts` serverless entry points.

## Audit Checklist

### 1. SCHEMA & STRUCTURE
- [ ] `$schema` property present (`"https://openapi.vercel.sh/vercel.json"`) for IDE autocomplete
- [ ] No deprecated properties (`routes` → use `rewrites`/`redirects`/`headers` instead)
- [ ] No conflicting properties (e.g., `routes` mixed with `rewrites`)
- [ ] `framework` set to `"vite"` (matches actual build tool)
- [ ] `buildCommand` matches `package.json` build script or is omitted to use default
- [ ] `outputDirectory` matches Vite `build.outDir` (default: `"dist"`)

### 2. SERVERLESS FUNCTIONS
- [ ] `functions` config exists for each `api/*.ts` entry point
- [ ] `includeFiles` patterns are correct and complete — all runtime dependencies included
- [ ] `includeFiles` uses glob patterns (e.g., `"server/**"`) not comma-separated strings unless properly formatted
- [ ] `memory` configured appropriately (default 1024 MB; increase to 3008 for heavy AI/LLM work)
- [ ] `maxDuration` set if functions do long-running work (AI calls, DB queries); Pro plan max: 300s
- [ ] No unnecessary files in `includeFiles` (bloats cold start)
- [ ] `runtime` specified if non-default Node.js version needed
- [ ] Functions entry point (`api/index.ts`) exports a proper handler (req, res) or Web API Response

### 3. REWRITES & ROUTING
- [ ] SPA fallback rewrite exists: all non-API routes → `/index.html`
- [ ] API rewrite routes to correct serverless function: `/api/(.*)` → `/api/index.ts`
- [ ] SPA rewrite uses negative lookahead to exclude `/api/` paths: `/((?!api/).*)`
- [ ] Rewrite order is correct (specific routes before catch-all)
- [ ] No rewrite loops or conflicts between rules
- [ ] If `cleanUrls: true`, rewrites don't include `.html` extensions

### 4. HEADERS (Security & Caching)
- [ ] Security headers configured (recommended):
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY` or `SAMEORIGIN`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy` restricting unused APIs
- [ ] Static asset caching: `Cache-Control: public, max-age=31536000, immutable` for hashed assets (`/assets/*`)
- [ ] HTML caching: `Cache-Control: no-cache` for `index.html` (prevents stale SPA shells)
- [ ] API caching: appropriate `Cache-Control` or `s-maxage` for cacheable endpoints
- [ ] CORS headers if API is consumed cross-origin

### 5. ENVIRONMENT VARIABLES
- [ ] No secrets in `NEXT_PUBLIC_*` or `VITE_*` prefixed variables (these are client-exposed)
- [ ] `NEXT_PUBLIC_OPENAI_API_KEY` is a security risk — OpenAI keys must NEVER be client-exposed
- [ ] Database URLs (`DATABASE_URL`, `DIRECT_DATABASE_URL`) are server-only (no `VITE_`/`NEXT_PUBLIC_` prefix)
- [ ] Service role keys (`SUPABASE_SERVICE_ROLE_KEY`) are server-only
- [ ] Stripe secret keys (`STRIPE_SECRET_KEY`) are server-only
- [ ] `SENTRY_AUTH_TOKEN` is server-only (build-time only, not runtime)
- [ ] All required env vars for serverless functions are available in Vercel project settings
- [ ] No placeholder/dummy values for webhook secrets (e.g., `whsec_12345`)

### 6. REGIONS & PERFORMANCE
- [ ] `regions` configured to match data source location (Supabase `us-west-2` → `pdx1` or `sfo1`)
- [ ] Or using Fluid compute (`"fluid": true`) for automatic scaling (default for new projects since April 2025)
- [ ] `functionFailoverRegions` set for high-availability if needed
- [ ] Consider `trailingSlash: false` for clean URLs

### 7. BUILD OPTIMIZATION
- [ ] `buildCommand` runs type checking before build if desired (e.g., `npm run build:check && npm run build`)
- [ ] `installCommand` not set unless specific package manager behavior needed
- [ ] `ignoreCommand` considered for skipping unnecessary builds (e.g., docs-only changes)
- [ ] Source maps configured for error tracking (Sentry) but not publicly exposed

### 8. IMAGES (if applicable)
- [ ] `images` config set if using Vercel Image Optimization
- [ ] Allowed domains listed for remote images
- [ ] Format preferences set (`avif`, `webp`)

## Output Format

```
## Vercel Audit Report

### Score: X/8 dimensions passing

### Critical Issues
1. [DIMENSION] — [severity: CRITICAL/HIGH/MEDIUM/LOW] — description
   Current: `current value`
   Fix: specific fix with code

### Warnings
1. [DIMENSION] — description
   Recommendation: what to change

### Optimizations
1. [DIMENSION] — description
   Benefit: expected improvement

### Passing
- [DIMENSION] — what's configured correctly

### Recommended vercel.json
(Only if changes needed — show the complete corrected file)
```
