---
name: supabase-security-audit
description: Audit a Supabase project for security issues -- RLS, auth config, role grants, storage, functions, and exposed secrets. Returns prioritized findings with fix recommendations.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__supabase__execute_sql, mcp__supabase__get_project, mcp__supabase__list_tables, mcp__supabase__search_docs
---

Run a comprehensive Supabase security audit: $ARGUMENTS

Default project ID comes from the project configuration or the user's request. If no project ID is provided, check project docs or config files for the Supabase project reference.

---

## Audit Protocol

Run all checks in order from most critical to least. For each check, execute the SQL query, analyze the result, and record the finding with a severity rating.

### Severity Levels
- **CRITICAL** -- Actively exploitable. Data can be read, modified, or deleted by unauthorized users right now.
- **HIGH** -- Significant exposure that becomes exploitable with minimal effort (e.g., public anon key + no RLS).
- **MEDIUM** -- Security gap that increases attack surface but requires additional conditions to exploit.
- **LOW** -- Best-practice violation that should be addressed but poses limited immediate risk.
- **INFO** -- Observation worth noting for awareness.

---

## Check 1: Row Level Security (CRITICAL)

**Why this matters:** Without RLS, Supabase's anon and authenticated roles have direct access to all data through the PostgREST API. The anon key is always exposed in browser code -- RLS is the only thing that protects your data from direct API access.

### 1a. Tables without RLS enabled

```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

**Findings format:** Count tables with `rowsecurity = false`. If ANY public table has RLS disabled, this is **CRITICAL**.

### 1b. Tables with RLS enabled but no policies

```sql
SELECT t.tablename
FROM pg_tables t
LEFT JOIN pg_policies p ON t.tablename = p.tablename AND p.schemaname = 'public'
WHERE t.schemaname = 'public'
  AND t.rowsecurity = true
  AND p.policyname IS NULL
ORDER BY t.tablename;
```

**Findings:** RLS enabled but no policies = all access denied (safe but broken). Flag as **MEDIUM** -- functional issue, not security.

### 1c. Overly permissive RLS policies

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

**Look for:**
- Policies with `qual = 'true'` (allows all rows) -- **HIGH** unless on intentionally public tables
- Policies granting access to `anon` role for INSERT/UPDATE/DELETE -- **HIGH** unless intentional
- Missing `with_check` on INSERT/UPDATE policies -- **MEDIUM**
- Policies that don't filter by `auth.uid()` on user-scoped tables -- **HIGH**

---

## Check 2: Role Grants (HIGH)

**Why this matters:** Even with RLS, if the `anon` or `authenticated` roles have excessive grants (TRUNCATE, DELETE on sensitive tables), a compromised or malicious client can do damage.

### 2a. Anon role privileges

```sql
SELECT table_name, privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
  AND grantee = 'anon'
ORDER BY table_name, privilege_type;
```

**Flag as HIGH if:**
- `anon` has INSERT, UPDATE, DELETE, or TRUNCATE on any table
- `anon` has SELECT on sensitive tables (user_profiles, payments, subscriptions, audit_logs, etc.)

### 2b. Authenticated role privileges

```sql
SELECT table_name, privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
  AND grantee = 'authenticated'
ORDER BY table_name, privilege_type;
```

**Flag as MEDIUM if:**
- `authenticated` has TRUNCATE on any table
- `authenticated` has DELETE on sensitive tables without RLS
- `authenticated` has full CRUD on admin-only tables

---

## Check 3: Authentication Configuration (HIGH)

### 3a. List all auth users

```sql
SELECT id, email, created_at, last_sign_in_at,
       raw_app_meta_data->>'provider' as provider,
       confirmed_at, is_anonymous
FROM auth.users
ORDER BY created_at DESC;
```

**Flag:** Unknown or unexpected users. Check if signup is open when it shouldn't be.

### 3b. Check for anonymous users

```sql
SELECT count(*) as anonymous_user_count
FROM auth.users
WHERE is_anonymous = true;
```

**Flag as MEDIUM if** anonymous auth is enabled and not intentional.

### 3c. Check auth flow state for signup method

```sql
SELECT authentication_method, count(*) as count
FROM auth.flow_state
GROUP BY authentication_method;
```

### 3d. Check the codebase for signup endpoints

Search the codebase for:
- `supabase.auth.signUp` calls
- Auth / signup pages or routes
- Any API routes that create auth users

**Recommend:** If signup should be restricted, either:
1. Disable email signup in Supabase Dashboard -> Authentication -> Providers
2. Add an invite-code gate in the signup form
3. Use Supabase's "Restrict email domains" setting

---

## Check 4: Storage Security (HIGH)

### 4a. Storage buckets

```sql
SELECT id, name, public, allowed_mime_types, file_size_limit
FROM storage.buckets;
```

**Flag as HIGH if:**
- Public buckets with no MIME type restrictions (allows arbitrary file uploads)
- No file size limits on public buckets
- Buckets that should be private are set to public

### 4b. Storage RLS policies

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'storage';
```

**Flag as HIGH if:** No storage policies exist -- anyone can upload/download/delete files.

---

## Check 5: Functions & Security Definers (MEDIUM)

### 5a. SECURITY DEFINER functions

```sql
SELECT n.nspname as schema, p.proname as function_name, p.prosecdef as security_definer,
       pg_get_functiondef(p.oid) as definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
  AND p.prosecdef = true
ORDER BY p.proname;
```

**Why this matters:** SECURITY DEFINER functions execute with the privileges of the function owner (usually superuser), not the calling user. If a SECURITY DEFINER function doesn't properly validate its inputs, it can be exploited to bypass RLS.

**Flag as MEDIUM if:**
- Function doesn't validate `auth.uid()` before performing operations
- Function accepts user-provided table names or column names (SQL injection risk)
- Function modifies data without checking authorization

### 5b. Functions callable by anon

```sql
SELECT routine_name, routine_type
FROM information_schema.routine_privileges
WHERE grantee = 'anon'
  AND routine_schema = 'public';
```

---

## Check 6: Exposed Secrets (HIGH)

### 6a. Check codebase for hardcoded keys

Search the codebase for:
- Supabase service role key in client-side code (NEVER should be in `NEXT_PUBLIC_*` or `VITE_*`)
- Database connection strings in client code
- Any `.env` files committed to git

```bash
# Check for service role key exposure
grep -r "service_role" {{APP_ROOT}}/src/ --include="*.ts" --include="*.tsx" -l
grep -r "SUPABASE_SERVICE_ROLE" {{APP_ROOT}}/src/ --include="*.ts" --include="*.tsx" -l
```

```bash
# Check env validation -- adapt the path to where env config lives
grep -r "NEXT_PUBLIC_SUPABASE\|VITE_SUPABASE" {{APP_ROOT}}/src/ --include="*.ts" -l
```

**Flag as CRITICAL if:** Service role key appears in any `NEXT_PUBLIC_*` or `VITE_*` variable or client-side code.

### 6b. Check .gitignore

Verify `.env.local` and other secret files are in `.gitignore`.

---

## Check 7: API Route Security (MEDIUM)

### 7a. Unprotected API routes

Search for API routes that don't validate authentication:

```
{{APP_ROOT}}/src/app/api/ or {{APP_ROOT}}/server/ -- check for routes that don't call supabase.auth.getUser() or equivalent auth validation
```

**Flag as MEDIUM if:** API routes perform writes without auth checks.

### 7b. Webhook routes without signature verification

Check webhook routes for proper signature validation (e.g., Stripe webhook signature).

---

## Check 8: Realtime & Edge Functions (LOW)

### 8a. Realtime subscriptions

```sql
SELECT * FROM realtime.subscription LIMIT 10;
```

**Note:** Realtime respects RLS policies, so if RLS is disabled, realtime is also unprotected.

### 8b. Edge functions

List edge functions via the Supabase MCP if available and check for auth validation.

---

## Output Format

Present findings as a structured report:

```
# Supabase Security Audit Report
**Project:** {project_id}
**Date:** {date}
**Tables scanned:** {count}

## Summary
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
- LOW: {count}

## Findings

### [CRITICAL] {title}
**What:** {description}
**Impact:** {what can go wrong}
**Evidence:** {SQL result summary}
**Fix:** {specific remediation steps}

### [HIGH] {title}
...
```

## Remediation Priority

Always recommend fixes in this order:
1. Enable RLS on all tables (even if policies are permissive initially)
2. Revoke excessive grants from `anon` role
3. Restrict signup if not intended to be public
4. Add storage policies
5. Audit SECURITY DEFINER functions
6. Tighten RLS policies per-table
7. Add API route auth checks

## Common RLS Policy Templates

Provide these when recommending RLS fixes:

**User owns the row:**
```sql
CREATE POLICY "Users can view own data"
ON public.{{TABLE_NAME}} FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

**Org-scoped access (multi-tenant):**
```sql
CREATE POLICY "Org members can view"
ON public.{{TABLE_NAME}} FOR SELECT
TO authenticated
USING (organization_id = (
  SELECT organization_id FROM public.organization_memberships
  WHERE user_id = auth.uid()
  LIMIT 1
));
```

**Public read, authenticated write:**
```sql
CREATE POLICY "Anyone can read" ON public.{{TABLE_NAME}} FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Authenticated can insert" ON public.{{TABLE_NAME}} FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
```

**Admin only:**
```sql
CREATE POLICY "Admin only"
ON public.{{TABLE_NAME}} FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM public.organization_memberships
    WHERE user_id = auth.uid() AND role = 'admin'
  )
);
```
