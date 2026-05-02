---
name: supabase-security-audit
description: Audit Supabase security — RLS policies, exposed secrets, API route auth, storage security, and role grants.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Bash
---

Run a comprehensive Supabase security audit for the project.

Target: $ARGUMENTS (optional — focus area like "rls", "secrets", "routes")

## Audit Checklist

### 1. Exposed Secrets (Critical)

Search the entire codebase for leaked credentials:

```
SUPABASE_SERVICE_ROLE_KEY
supabase.co (with inline keys)
anon key in client-side code (acceptable only if RLS is enforced)
```

Check:
- `.env` files are gitignored
- No secrets in client-side bundles (src/ should only use anon key)
- Server-side code uses service role key only in `server/` directory
- No secrets committed in git history

### 2. Row Level Security (RLS)

If SQL migrations or schema files exist, check:
- All tables have RLS enabled
- Policies exist for SELECT, INSERT, UPDATE, DELETE as appropriate
- No overly permissive policies (`USING (true)` without justification)
- Auth context is properly used (`auth.uid()`, `auth.role()`)

### 3. API Route Security

Audit all Express routes in `server/`:
- Authentication middleware on protected routes
- Input validation (Zod schemas) on all mutation endpoints
- No direct database access without auth checks
- Rate limiting on sensitive endpoints
- CORS configuration is restrictive

### 4. Client-Side Security

Check `src/` for:
- No direct Supabase client mutations that bypass the API server
- Sensitive operations go through Express API, not direct Supabase calls
- Auth tokens are handled securely (httpOnly cookies preferred over localStorage)

### 5. Storage Security

If Supabase Storage is used:
- Bucket policies restrict access appropriately
- No public buckets containing sensitive data
- Upload size limits enforced
- File type validation on uploads

### 6. Environment Configuration

Check:
- `.env.local` / `.env` are in `.gitignore`
- Server and client environment variables are properly separated
- No `SUPABASE_SERVICE_ROLE_KEY` accessible from client code

## Output Format

```
## Supabase Security Audit

### Critical (exploitable now)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|-------------|

### High (should fix before production)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|-------------|

### Medium (hardening)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|-------------|

### Passed Checks
- ...
```

Apply Critical fixes automatically. Report High and Medium for user review.
