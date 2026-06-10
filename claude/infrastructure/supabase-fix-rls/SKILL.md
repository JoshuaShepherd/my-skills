---
name: supabase-fix-rls
description: Take an RLS finding from supabase-security-audit (or a free-form description of an RLS issue) and apply a reviewed fix via the Supabase MCP. Handles the four common patterns — RLS disabled, RLS enabled with no policies, overly permissive policies, missing tenant scope — plus a bonus path for excessive role grants. Every write is gated on explicit operator approval. Use when asked to "fix RLS on X", "lock down table Y", "harden the audit findings", or "remediate Supabase advisories".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__supabase__list_projects, mcp__supabase__get_project, mcp__supabase__list_tables, mcp__supabase__list_migrations, mcp__supabase__execute_sql, mcp__supabase__apply_migration, mcp__supabase__get_advisors, mcp__supabase__search_docs
---

Fix an RLS issue on Supabase: $ARGUMENTS

`$ARGUMENTS` may include any of:

- A finding pasted from the `supabase-security-audit` report (free-form OK)
- A table name (e.g. `corpus_bindings`) → diagnose then offer fixes
- An issue tag — `rls_disabled`, `no_policies`, `overly_permissive`, `missing_tenant_scope`, `anon_writes`, `excess_grants`
- `--project=<ref>` to target a non-default project
- `--dry-run` → produce the migration SQL but never call `apply_migration`
- `--apply` → still requires an explicit "apply" confirmation in chat; just signals intent
- `all` → walk every advisory of the relevant categories returned by `mcp__supabase__get_advisors`

Empty input ⇒ fetch advisories + ask the operator which finding to remediate first.

---

## Pairing

This skill is the **write companion** to `supabase-security-audit`. The audit identifies issues; this skill drafts and applies the fix. Always re-verify the finding here before fixing — audits get stale fast on a live DB.

If the operator pastes an audit report, treat it as a hint, not gospel. Re-run the diagnostic SQL in Phase 1 to confirm the issue still exists exactly as described.

---

## Hard rules (non-negotiable)

1. **Never** call `mcp__supabase__apply_migration` without an explicit operator "apply" / "yes, apply" / equivalent in the same conversation turn. A pasted finding is not approval to fix.
2. **Never** `DROP POLICY` without first showing the policy's full definition (`pg_policies.qual`, `with_check`, `roles`, `cmd`) and naming what replaces it.
3. **Never** disable RLS as part of a fix. If RLS is on and the policies are wrong, fix the policies — do not turn RLS off to "unbreak" a query.
4. **Never** target the wrong project. Phase 0 confirms the project ID before any Phase 5 write.
5. **Never** write the fix directly into `src/lib/database/schema.ts` — that file is auto-generated (per `CLAUDE.md`). Schema changes go through `mcp__supabase__apply_migration`, then the operator regenerates the Drizzle chain (Phase 8).
6. **Never** apply changes inside an SQL string that combines unrelated DDL — one logical fix per migration so rollback is precise.

---

## Project + MCP context

Source the project ref from `.env.local` / `.env.shared` / repo `CLAUDE.md`. Do **not** memorize. Default for Movemental production: `vhaiiiykcukrlyvwlgip`.

Tools used in this skill:

- `mcp__supabase__list_projects` / `get_project` — confirm the target before any write.
- `mcp__supabase__get_advisors` — pull current `security` advisories; many RLS findings show up here as `policy_exists_rls_disabled`, `rls_disabled_in_public`, etc.
- `mcp__supabase__list_tables` — confirm the table exists and inspect its FKs/columns when designing tenant-scoped policies.
- `mcp__supabase__execute_sql` — every diagnostic and verification query. Read-only by convention in this skill (only `SELECT`/`EXPLAIN`). Do **not** issue DDL through `execute_sql` — that path is for `apply_migration`.
- `mcp__supabase__apply_migration` — every write. One migration per logical fix.
- `mcp__supabase__search_docs` — when in doubt about RLS semantics (e.g. how `permissive` vs `restrictive` policies combine), prefer official docs over memory.

---

## Phase 0 — Lock the project

```sql
-- via mcp__supabase__list_projects + get_project
```

Confirm the resolved project ref matches what the operator expects. If `--project` was passed, override the default and echo back: "Targeting project `<ref>` — proceed? (y/n)". Do not continue without confirmation when an override is in play.

Pull current advisories so the rest of the skill has fresh signal:

```
mcp__supabase__get_advisors { type: "security" }
```

Cross-reference any RLS-related advisory (`rls_disabled_in_public`, `policy_exists_rls_disabled`, `auth_users_exposed`, `security_definer_view`, `anonymous_users_can_*`) with the operator's $ARGUMENTS. If they conflict, ask.

---

## Phase 1 — Re-verify the finding

For each finding, run the matching diagnostic so the fix is grounded in current state, not a stale report.

### 1.1 RLS disabled on a public table

```sql
SELECT c.relname AS table_name, c.relrowsecurity AS rls_enabled
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relname = '{table}';
```

Pass-to-fix condition: `rls_enabled = false`. If `true`, the finding is stale — re-classify as 1.2 or 1.3 instead.

### 1.2 RLS enabled, no policies

```sql
SELECT t.tablename,
       (SELECT count(*) FROM pg_policies p
        WHERE p.schemaname = 'public' AND p.tablename = t.tablename) AS policy_count
FROM pg_tables t
WHERE t.schemaname = 'public' AND t.tablename = '{table}' AND t.rowsecurity = true;
```

Pass-to-fix condition: `policy_count = 0`. The table is in "default deny" — no row is reachable via PostgREST.

### 1.3 Overly permissive policy

```sql
SELECT policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = '{table}'
ORDER BY policyname;
```

Flag policies where:
- `qual = 'true'` and `cmd IN ('SELECT', 'ALL')` and `roles` includes `anon` or `authenticated` (unless table is intentionally public — confirm with operator)
- `with_check IS NULL` on `INSERT` or `UPDATE` policies (can write rows the policy can't subsequently read)
- `qual` does not reference `auth.uid()` or `organization_id` on a tenant-scoped table

### 1.4 Missing tenant scope (multi-tenant tables)

A table is tenant-scoped if it has an `organization_id` column. Confirm:

```sql
SELECT column_name FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = '{table}' AND column_name = 'organization_id';
```

Then check whether existing policies actually filter by it:

```sql
SELECT policyname, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = '{table}'
  AND (qual NOT ILIKE '%organization_id%' OR with_check NOT ILIKE '%organization_id%');
```

Any row returned = a policy that touches a tenant table without an `organization_id` filter. Almost always a bug.

### 1.5 Anon writes

```sql
SELECT policyname, cmd, roles, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = '{table}'
  AND 'anon' = ANY(roles)
  AND cmd IN ('INSERT', 'UPDATE', 'DELETE', 'ALL');
```

Any row = anon role can write. Almost always wrong outside of explicitly-public capture forms (newsletter signups etc.) — confirm intent before fixing.

### 1.6 Helper functions present?

```sql
SELECT proname FROM pg_proc
WHERE pronamespace = 'public'::regnamespace
  AND proname IN ('is_member_of_org', 'is_movemental_staff');
```

If both exist, prefer the **Movemental-flavored** templates in §4. If they don't, use the **generic** templates that inline the membership EXISTS check.

---

## Phase 2 — Classify and pick a template

Match the verified finding to one of:

| Issue | Template (see §4) |
|---|---|
| RLS disabled | T1 — Enable RLS + add baseline policy |
| RLS enabled, no policies | T2 — Add minimal policy set (read for members, write for owners) |
| Overly permissive `SELECT` to `anon`/`authenticated` | T3 — Replace with scoped read |
| Missing tenant scope | T4 — Org-scoped policy via membership |
| Anon writes | T5 — Revoke anon writes, restrict to authenticated |
| `with_check` missing on INSERT/UPDATE | T6 — Add symmetric `with_check` |
| Excess role grants | T7 — Revoke excess grants from anon (Phase 6) |

If the finding doesn't match any of the above, **stop** and ask the operator to clarify rather than improvising a policy. RLS is one of the easiest places to introduce a silent privilege-escalation bug.

---

## Phase 3 — Draft the migration

Produce one migration per logical fix. Migration name should be descriptive and unique:

`fix_rls_<table>_<short_reason>` (e.g. `fix_rls_corpus_bindings_enable`, `fix_rls_agents_drop_anon_select`)

The migration body must:

1. Be idempotent where possible — guard with `IF EXISTS` / `IF NOT EXISTS`. RLS DDL like `ALTER TABLE … ENABLE ROW LEVEL SECURITY` is naturally idempotent.
2. Drop the bad policy by name **before** creating the replacement.
3. Use stable, descriptive policy names — `<verb>_<scope>_<table>` (e.g. `members_select_organizations`, `owners_update_organizations`).
4. Include a top-of-file comment naming the finding it remediates and the date.

Show the migration text to the operator inside a fenced ```sql block. Then **stop** and request approval.

---

## Phase 4 — Confirmation gate

Print a single, explicit prompt:

> "Apply migration `<name>` to project `<ref>`? This will run the SQL above. Reply `apply` to proceed, `dry-run` to skip, or paste an edit."

Acceptable approvals: `apply`, `yes apply`, `apply it`, `go`. Anything else = stop.

If the operator edits the SQL inline, re-print the new version and ask again. Never apply silently after an edit.

If `--dry-run` was passed in $ARGUMENTS, **skip Phase 5 entirely** and tell the operator the migration is ready to be applied later.

---

## Phase 5 — Apply

```
mcp__supabase__apply_migration {
  project_id: "<ref>",
  name: "fix_rls_<table>_<short_reason>",
  query: "<the SQL from Phase 3>"
}
```

Capture and report any error verbatim. **Do not** retry on error — investigate first. Common failure modes:

- `policy "x" for table "y" already exists` → the diagnostic in Phase 1 missed it; re-run §1.3 and update the migration to drop-then-create.
- `permission denied for table x` → the migration is being executed by a role without DDL privilege; confirm the MCP project ref and try once more.
- `function is_member_of_org(uuid) does not exist` → §1.6 was wrong about helper presence; switch to the generic template.

---

## Phase 6 — Verify

Re-run the Phase 1 diagnostic that originally identified the finding. The result must now be **empty / passing**. Then run a **negative-positive smoke** to make sure the policy actually filters:

```sql
-- Positive: a known member should see at least one row
SET LOCAL ROLE authenticated;
SET LOCAL "request.jwt.claims" TO '{"sub":"<known-member-uuid>"}';
SELECT count(*) FROM public.{table};
RESET ROLE;

-- Negative: an unknown user should see zero rows (or only public rows)
SET LOCAL ROLE authenticated;
SET LOCAL "request.jwt.claims" TO '{"sub":"00000000-0000-0000-0000-000000000000"}';
SELECT count(*) FROM public.{table};
RESET ROLE;
```

If the negative query returns rows that shouldn't be visible, **stop** and proceed to Phase 7 rollback. Do not leave a half-broken policy in place.

Also re-pull advisories:

```
mcp__supabase__get_advisors { type: "security" }
```

The advisory you fixed should be gone. If it isn't, Supabase's advisor is sometimes cached for a few minutes — note that and move on rather than chasing it.

---

## Phase 7 — Rollback (if Phase 6 fails)

Apply the inverse migration:

```sql
-- For T1 (enabled RLS) — leaving RLS on is safer than off, so prefer to fix-forward.
-- Only roll back to RLS-off if the operator explicitly demands it.

-- For T2/T3/T4/T5/T6 (added or replaced a policy) — drop the new policy and recreate the prior one verbatim.
DROP POLICY IF EXISTS "<new_policy>" ON public.{table};
-- (recreate prior policy from the snapshot in Phase 1.3)
```

Always show the rollback SQL and request approval before applying it (Phases 4–5 again).

---

## Phase 8 — Refresh the Drizzle chain

Per `CLAUDE.md`, `src/lib/database/schema.ts` is auto-generated from the live DB. RLS-only changes don't change column shapes, so the Drizzle chain often doesn't need regeneration. But if your fix involved adding/removing columns or constraints (rare for RLS, common for related grant fixes), tell the operator to:

```bash
pnpm exec tsx scripts/generate-schema.ts && pnpm db:check
pnpm validate:all
```

Never run those for the operator unless they ask — `validate:all` can be slow.

---

## Phase 9 — Document

Append a one-line entry to `docs/build/rls-fixes-log.md` (create it if missing):

```
- 2026-05-10 — fix_rls_corpus_bindings_enable — enabled RLS + added members_select policy. Finding source: supabase-security-audit 2026-05-09. Verified: positive=N, negative=0.
```

This isn't required by the protocol but it makes the next audit much faster and gives the operator a trail.

---

## §4 — Templates

All templates are parameterized on `{table}` and `{owner_column}` (the user-id column on the table — usually `user_id`, sometimes `account_owner_id` or `created_by`).

### T1 — Enable RLS + baseline policy

Use when RLS is disabled. Always pair the `ENABLE` with at least one policy so the table isn't immediately default-deny.

```sql
ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;

-- Default: members of the row's org can read. Adjust if the table is single-user-owned (T2 instead).
CREATE POLICY "members_select_{table}"
  ON public.{table} FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.organization_memberships m
      WHERE m.user_id = auth.uid()
        AND m.organization_id = {table}.organization_id
    )
  );
```

**Movemental flavor (when `is_member_of_org` exists):**

```sql
CREATE POLICY "members_select_{table}"
  ON public.{table} FOR SELECT
  TO authenticated
  USING (is_member_of_org({table}.organization_id));
```

### T2 — Owner-scoped CRUD

Use when the table has a single user-owner column (`user_id`, `created_by`).

```sql
ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;

CREATE POLICY "owner_select_{table}"
  ON public.{table} FOR SELECT TO authenticated
  USING (auth.uid() = {owner_column});

CREATE POLICY "owner_insert_{table}"
  ON public.{table} FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = {owner_column});

CREATE POLICY "owner_update_{table}"
  ON public.{table} FOR UPDATE TO authenticated
  USING (auth.uid() = {owner_column})
  WITH CHECK (auth.uid() = {owner_column});

CREATE POLICY "owner_delete_{table}"
  ON public.{table} FOR DELETE TO authenticated
  USING (auth.uid() = {owner_column});
```

### T3 — Replace overly permissive SELECT

Use when a `qual = true` policy is exposing data to anon/authenticated.

```sql
DROP POLICY IF EXISTS "{old_policy_name}" ON public.{table};

CREATE POLICY "members_select_{table}"
  ON public.{table} FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.organization_memberships m
      WHERE m.user_id = auth.uid()
        AND m.organization_id = {table}.organization_id
    )
  );
```

### T4 — Org-scoped CRUD (multi-tenant table)

Use when a tenant table needs full members-can-write, with optional staff override.

```sql
DROP POLICY IF EXISTS "{old_policy_name}" ON public.{table};  -- if replacing

CREATE POLICY "members_select_{table}"
  ON public.{table} FOR SELECT TO authenticated
  USING (is_member_of_org({table}.organization_id) OR is_movemental_staff());

CREATE POLICY "members_insert_{table}"
  ON public.{table} FOR INSERT TO authenticated
  WITH CHECK (is_member_of_org({table}.organization_id) OR is_movemental_staff());

CREATE POLICY "members_update_{table}"
  ON public.{table} FOR UPDATE TO authenticated
  USING (is_member_of_org({table}.organization_id) OR is_movemental_staff())
  WITH CHECK (is_member_of_org({table}.organization_id) OR is_movemental_staff());

CREATE POLICY "staff_delete_{table}"
  ON public.{table} FOR DELETE TO authenticated
  USING (is_movemental_staff());
```

If the helpers don't exist, inline the EXISTS as in T1.

### T5 — Revoke anon writes

Use when anon has INSERT/UPDATE/DELETE access and shouldn't.

```sql
DROP POLICY IF EXISTS "{anon_write_policy}" ON public.{table};

-- If a legitimate anon-capture flow exists (e.g. newsletter signup), recreate scoped:
CREATE POLICY "anon_insert_{table}_capture"
  ON public.{table} FOR INSERT TO anon
  WITH CHECK (
    -- Lock to a single safe pattern; e.g. only allow rows where status = 'pending' and
    -- no privileged columns are being set. Customize per table.
    status = 'pending'
  );
```

### T6 — Add symmetric `with_check`

Use when an INSERT or UPDATE policy has `qual` but no `with_check` — users can create rows that won't pass the SELECT filter (silent data loss to the writer, possible privilege escalation).

```sql
DROP POLICY IF EXISTS "{policy_name}" ON public.{table};

CREATE POLICY "{policy_name}"
  ON public.{table} FOR INSERT TO authenticated
  WITH CHECK ({same_predicate_as_qual});  -- mirror the SELECT condition
```

### T7 — Revoke excess grants from anon (see Phase 6 / fix-grants section)

```sql
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON public.{table} FROM anon;
-- Keep SELECT only if the table is intentionally public-readable.
REVOKE SELECT ON public.{table} FROM anon;  -- only if not public
```

Pair every grant revoke with a verification:

```sql
SELECT privilege_type FROM information_schema.table_privileges
WHERE table_schema = 'public' AND table_name = '{table}' AND grantee = 'anon';
```

Expected: empty (or `SELECT` only on intentionally-public tables).

---

## Bonus: fix-grants flow

If $ARGUMENTS includes `excess_grants` or the audit's Check 2 flagged the table, run T7 in Phase 3 instead of an RLS template. Same Phase 4 confirmation gate, same Phase 5 apply, same Phase 6 verification — but the diagnostic in Phase 1 is the `information_schema.table_privileges` query, not `pg_policies`.

Grants and policies are layered: revoking grants is a defense-in-depth move on top of correct RLS. If you have time, do both — RLS first (so the table isn't worse off mid-fix), then grants.

---

## Common pitfalls

- **`auth.uid()` is null in service-role contexts.** If a backend job uses the service role and you write `auth.uid() = user_id`, the job's queries will return zero rows. Service-role callers usually bypass RLS entirely (good). If they don't, the policy needs an explicit `OR current_setting('role') = 'service_role'` escape hatch — but adding that is a code-smell signal that the job should be using the service-role client instead.
- **`USING` filters reads, `WITH CHECK` filters writes.** UPDATE policies need both. INSERT only needs `WITH CHECK`. DELETE only needs `USING`. SELECT only needs `USING`. ALL needs both.
- **Permissive vs restrictive.** Default is permissive — multiple permissive policies are OR'd. Restrictive policies are AND'd on top. If you're stacking, document why.
- **`pg_policies.qual` is `text`, not SQL.** When matching policies in the diagnostic, treat the column as opaque text — don't try to parse it. Just check `ILIKE '%organization_id%'` style.
- **PostgREST exposes `auth.uid()` from the JWT `sub` claim.** Tests using `SET LOCAL "request.jwt.claims"` mimic this; tests using `SET LOCAL ROLE authenticated` without setting claims will see `auth.uid() = null`.
- **Realtime, Storage, and Functions all respect RLS.** Fixing a table's policies fixes all three surfaces at once.

---

## Output format (per finding handled)

```
## fix_rls_<table>_<reason>

**Finding:** <one line — what was wrong, severity from audit>
**Diagnostic re-verified:** <pass / stale / changed>
**Template applied:** <T#>
**Migration name:** <name>
**Migration SQL:**
\`\`\`sql
<the SQL>
\`\`\`
**Apply confirmation:** <operator response>
**Apply result:** <success / error verbatim>
**Verification:** positive=<N>, negative=<N>, advisor cleared=<yes/no>
**Rollback (if needed):** <SQL or "n/a">
**Drizzle refresh required:** <yes/no — if yes, command to run>
```

End the run with a single-line summary:

> Fixed N RLS findings across M tables. K skipped (operator declined apply). 0 left in failed-verification state.
