---
name: vercel-deploy-audit
description: Audit a Vite+Express workspace for Vercel deployment issues — API connectivity, env vars, serverless bundling, CORS, symlinks, rewrites, and build config. Returns prioritized findings with fixes.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent
---

Run a comprehensive Vercel deployment audit for the current workspace: $ARGUMENTS

---

## Audit Protocol

Run ALL checks in order. For each check, inspect the relevant files, test live endpoints if a deployment URL is available, and record findings with severity ratings.

### Severity Levels
- **CRITICAL** — App is broken in production right now. API calls fail, pages don't load, auth doesn't work.
- **HIGH** — Will break under common conditions (specific routes, auth flows, cold starts).
- **MEDIUM** — Degraded behavior or fragile config that could break on next deploy.
- **LOW** — Best-practice violation, potential future issue.
- **INFO** — Observation worth noting.

---

## Check 1: Vercel Configuration (CRITICAL)

### 1a. vercel.json exists and is valid JSON

Read `vercel.json`. If missing, flag as **CRITICAL** — Vercel won't know how to route API calls.

### 1b. Rewrites configuration

Verify the rewrites array properly routes:
- `/api/*` requests to the serverless function entry point
- All non-API routes to `/index.html` (SPA catch-all)

**Common issues:**
- Missing API rewrite → API calls return 404 or the SPA HTML
- API rewrite destination doesn't match the actual serverless function path
- SPA catch-all regex accidentally captures `/api/` routes
- Regex ordering matters — API rewrite MUST come before the SPA catch-all

**Flag as CRITICAL if:** rewrites are missing, misordered, or the API destination doesn't match the serverless function file path.

### 1c. Functions configuration

Check `functions` key in vercel.json:
- The entry file (e.g., `api/index.ts`) must actually exist
- `includeFiles` must capture all server-side code the function imports
- Check for missing directories in `includeFiles` (e.g., `shared/`, `server/`, node_modules that need bundling)

**Flag as CRITICAL if:** entry file doesn't exist or `includeFiles` is missing critical directories.

### 1d. Build command and output directory

- `buildCommand` should match or be compatible with the package.json `build` script
- `outputDirectory` should match Vite's `build.outDir` (default: `dist`)

---

## Check 2: Serverless Function Entry Point (CRITICAL)

### 2a. API entry file structure

Read the serverless entry file (typically `api/index.ts`). Verify:
- It exports a default function with `(req: VercelRequest, res: VercelResponse)` signature
- It creates an Express app and passes `(req, res)` to it
- It does NOT call `app.listen()` (Vercel manages the server)
- It does NOT use `dotenv.config()` (Vercel injects env vars automatically; dotenv may fail or override)

**Flag as CRITICAL if:**
- No default export
- `app.listen()` is called (blocks the serverless function)
- Missing route registrations that exist in the dev server

### 2b. Route parity between dev server and serverless entry

Compare the dev server entry (e.g., `server/index.ts`) with the serverless entry (`api/index.ts`):
- All route registrations must be present in both
- Middleware order must be identical (especially auth middleware)
- CORS configuration must be present in the serverless entry

**Flag as HIGH if:** Routes or middleware differ between dev and prod entry points.

### 2c. CORS configuration

In the serverless entry, check the CORS setup:
- `cors()` with no origin restriction is fine for serverless (same-origin by default on Vercel)
- If `origin` is set to a specific URL (e.g., `http://localhost:3000`), it will block production requests

**Flag as CRITICAL if:** CORS origin is hardcoded to localhost in the serverless entry.

---

## Check 3: Environment Variables (CRITICAL)

### 3a. Catalog all required env vars

Scan the entire codebase for `process.env.VARIABLE_NAME` and `import.meta.env.VARIABLE_NAME` patterns. Build a complete list of:
- **Server-side vars** (used in `server/`, `api/`)
- **Client-side vars** (used in `src/`, must have `VITE_` prefix)

### 3b. Check for vars that will crash on missing

Search for patterns like:
- `if (!envVar) throw new Error(...)` — will crash the function
- `const x = process.env.VAR!` — will be undefined, may cause runtime errors
- Direct usage without fallback: `process.env.VAR.split(...)` — will throw TypeError

List every env var that causes a hard crash if missing. These MUST be set in Vercel.

### 3c. Required Vercel environment variables checklist

Generate a complete checklist of env vars that must be configured in Vercel Dashboard → Settings → Environment Variables. Group by:

**Must be set (function crashes without these):**
- List all vars that throw or crash

**Should be set (features break without these):**
- List all vars used but with fallbacks

**Client-side (must be set at BUILD TIME):**
- List all `VITE_*` vars — these are baked into the JS bundle during `vite build`
- Check if vite.config.ts `define` block maps non-VITE_ vars to client-side vars (e.g., `SUPABASE_URL` → `VITE_SUPABASE_URL`)
- If so, note which vars the build actually reads

**Flag as CRITICAL if:** any crash-causing env var is identified. Remind user to verify these are set in Vercel Dashboard.

### 3d. dotenv usage in serverless context

Check if the serverless entry file (or files it imports) loads dotenv. On Vercel, env vars are injected by the platform — dotenv looking for `.env.local` will fail silently or interfere.

**Flag as MEDIUM if:** dotenv is loaded in the serverless code path.

---

## Check 4: Symlinks and Shared Code (CRITICAL for monorepos)

### 4a. Check for symlinks

```bash
find . -type l -not -path './node_modules/*' -not -path './.git/*' 2>/dev/null
```

### 4b. Verify symlink targets are included in function bundle

For each symlink found:
- Check if the symlink target directory is listed in `vercel.json` → `functions` → `includeFiles`
- Vercel's build may or may not follow symlinks depending on the builder version

**Flag as CRITICAL if:** Symlinked directories contain server-side code (schemas, shared types) but aren't in `includeFiles`. The serverless function will fail with "module not found" errors at runtime.

### 4c. Check for path aliases that won't resolve

Look at `tsconfig.json` / `tsconfig.server.json` for path aliases (e.g., `@/lib/*`):
- Vercel's Node.js runtime does NOT resolve TypeScript path aliases
- These must either be handled by the bundler or use relative imports in the serverless code

**Flag as HIGH if:** The serverless entry or its imports use TypeScript path aliases without a bundler to resolve them.

---

## Check 5: Module Resolution & Dependencies (HIGH)

### 5a. Check module type

Look at `package.json` → `"type"`. If `"module"`, the serverless function runs as ESM:
- `import` statements work
- `require()` does not work without createRequire
- `__dirname` / `__filename` are not available (need `import.meta.url`)

### 5b. Check for CommonJS/ESM mismatches

In the serverless entry and its imports, look for:
- `require()` calls in an ESM project
- `__dirname` usage in ESM context
- Dependencies that only ship CommonJS in an ESM project

**Flag as HIGH if:** module format mismatches are found.

### 5c. Check that server dependencies are in `dependencies` not `devDependencies`

Vercel installs `dependencies` but NOT `devDependencies` for serverless functions. Verify:
- `express`, `cors`, `jsonwebtoken`, `drizzle-orm`, `postgres`, `dotenv`, and any other server-side packages are in `dependencies`
- `@vercel/node` can be in `devDependencies` (Vercel provides it)

**Flag as CRITICAL if:** server runtime dependencies are in `devDependencies`.

---

## Check 6: Database Connectivity (HIGH)

### 6a. Connection string configuration

Check how the database connection is established:
- Is `DATABASE_URL` required? Will it crash without it?
- Is SSL configured? (Supabase requires `ssl: 'require'`)
- Is connection pooling configured appropriately for serverless? (low `max`, short `idle_timeout`, `prepare: false` for pgBouncer)

### 6b. Connection pooling for serverless

Serverless functions spin up/down frequently. Check for:
- Global connection caching (module-level variable) — good for warm invocations
- Connection pool size — should be low (1-5) for serverless
- `prepare: false` — required when using Supabase's connection pooler (pgBouncer)

**Flag as MEDIUM if:** pool size > 10 or prepare statements enabled with pooler.

### 6c. Correct connection string for serverless

Supabase offers two connection types:
- **Pooler (port 6543):** Use this for serverless (pgBouncer)
- **Direct (port 5432):** Use for migrations, NOT for serverless

Check if the `DATABASE_URL` pattern uses port 6543 (pooler) or 5432 (direct).

**Flag as HIGH if:** Direct connection (port 5432) is being used — will exhaust connections quickly in serverless.

---

## Check 7: Build & Bundle (MEDIUM)

### 7a. Vite build output

Check if `vite build` produces output compatible with Vercel:
- Output to `dist/` (or whatever `outputDirectory` says)
- `index.html` exists in output
- Assets are in `dist/assets/`

### 7b. Pre-build scripts

Check if `build:check` or similar pre-build scripts will block the Vercel build:
- Do they reference local files that won't exist in Vercel's build environment?
- Do they require env vars that might not be set during build?

### 7c. Node.js version compatibility

Check `package.json` → `engines.node` or `.nvmrc` or `vercel.json` → `functions.*.runtime`:
- Vercel defaults to Node 18.x
- If the project needs Node 20+, it must be specified

---

## Check 8: Live Deployment Verification (CRITICAL — if URL provided)

If a Vercel deployment URL is provided (or can be found via `vercel` CLI), test these endpoints:

### 8a. Health check
```
GET {url}/api/health
```
Expected: `{"status":"ok"}` with 200
- If 404: rewrites are broken
- If 500: serverless function is crashing (check env vars, module resolution)
- If HTML returned: SPA catch-all is intercepting API routes

### 8b. Check response headers
Look at response headers for clues:
- `x-vercel-cache`: present on static assets
- `x-vercel-id`: present on serverless function responses
- `content-type: text/html` on an API route = SPA catch-all is wrong

### 8c. Auth endpoint
```
POST {url}/api/auth/validate-invite
```
This should return a JSON response (even if error), NOT HTML.

### 8d. Protected endpoint without auth
```
GET {url}/api/courses
```
Expected: 401 with `{"error":"Missing authorization token"}`
- If HTML: rewrites broken
- If 500: function crash (env vars, DB connection)

---

## Check 9: CORS & Headers (MEDIUM)

### 9a. Verify CORS for cross-origin scenarios

If the frontend and API are on the same Vercel deployment (same domain), CORS is not needed. But check:
- Is `cors()` middleware applied in the serverless entry?
- Are credentials enabled if needed?
- Is the origin misconfigured for production?

### 9b. Response headers for security

Check for missing security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (if not using iframes)

**Flag as LOW** — nice to have but not causing the connection error.

---

## Check 10: Common Vercel + Express Pitfalls (HIGH)

### 10a. Express body parsing

Verify `express.json()` is called before routes. Without it, POST/PATCH/PUT bodies will be undefined.

### 10b. Request/Response passthrough

The Vercel handler must pass `(req, res)` directly to Express:
```typescript
export default function handler(req, res) {
  app(req, res);  // correct
}
```

Not:
```typescript
export default function handler(req, res) {
  app.handle(req, res);  // may work but non-standard
}
```

### 10c. Async handler issues

If the handler is async, unhandled promise rejections won't send a response — the function will time out.

### 10d. Cold start timeout

Vercel Hobby plan has a 10s execution limit (Pro: 60s). If DB connection + query exceeds this on cold start, the function times out.

**Flag as MEDIUM if:** hobby plan with complex cold-start initialization.

---

## Output Format

Present findings as a structured report:

```
# Vercel Deployment Audit Report
**Project:** {name from package.json}
**Date:** {date}
**Checks completed:** {count}

## Summary
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
- LOW: {count}

## Findings

### [CRITICAL] {title}
**What:** {description}
**Impact:** {what breaks}
**Evidence:** {file:line or test result}
**Fix:** {specific remediation steps with code}

### [HIGH] {title}
...
```

## Environment Variable Checklist

Always end the report with a complete env var checklist:

```
## Required Vercel Environment Variables

Set these in Vercel Dashboard → Project Settings → Environment Variables.
Make sure each variable is enabled for the correct environments (Production, Preview, Development).

### Server-side (Runtime)
- [ ] DATABASE_URL — PostgreSQL connection string (use pooler, port 6543)
- [ ] SUPABASE_JWT_SECRET — JWT verification key
- ...

### Client-side (Build-time)
- [ ] VITE_SUPABASE_URL — Supabase project URL
- ...
```

## Quick Fix Priority

Recommend fixes in this order:
1. Fix serverless function crashes (missing env vars, module errors)
2. Fix rewrites (API returning HTML)
3. Fix CORS (blocked requests)
4. Fix database connectivity (connection errors, timeouts)
5. Fix auth flow (token issues)
6. Address warnings and best practices
