---
name: movemental-tenant-provision
description: Provision Movemental movement-leader tenants end-to-end on Supabase — runs Phase 0 prerequisite security/auth gates first, then per-leader identity → auth user → user_profile → owned org → owner membership. Targets the canonical author cohort (Alan Hirsch, Brad Brisco, Liz Rios, Rowland Smith, JR Woodward, Lucas Pulley, Jamie Roach) and the Movemental admin org. Use when asked to "wire up Movemental tenants", "onboard a movement leader", "provision the author orgs", or "run the tenant-wiring prompt".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__supabase__list_projects, mcp__supabase__get_project, mcp__supabase__list_tables, mcp__supabase__list_migrations, mcp__supabase__execute_sql, mcp__supabase__apply_migration, mcp__supabase__search_docs, mcp__supabase__get_advisors
---

Provision Movemental tenants from the canonical runbook: $ARGUMENTS

`$ARGUMENTS` may include:
- A leader name (e.g. `jamie-roach`) → run only that target
- `all` → walk every target in the cohort
- `prereqs` → run Phase 0 gates only and stop
- `verify` → run the read-only verification pass for every target
- `--env=staging|production` → which Supabase project to act in (default: production / `vhaiiiykcukrlyvwlgip`)

Empty input ⇒ Phase 0 gates, then ask the operator which target(s) to run.

---

## Source of truth

The authoritative runbook is `docs/movement_leader_research/tenant-wiring-prompt.md`. Re-read it on every invocation before acting — the doc evolves and per-target notes change. This skill **executes** that doc. Do not reinterpret or skip steps without the operator's explicit approval.

Per-leader research files live in `docs/movement_leader_research/<slug>.md` (create if missing — see Phase 1).

## Cohort

Canonical author tenants (one Supabase auth user → one `user_profiles` → one owned `organizations` row → one `owner` membership):

| Slug | Name | Status hint |
|---|---|---|
| `alan-hirsch` | Alan Hirsch | Existing — **dedupe first** |
| `brad-brisco` | Brad Brisco | Existing — **placeholder vs real** |
| `liz-rios` | Liz Rios | Greenfield |
| `rowland-smith` | Rowland Smith | Greenfield |
| `jr-woodward` | JR Woodward | Greenfield |
| `lucas-pulley` | Lucas Pulley | Greenfield |
| `jamie-roach` | Jamie Roach | Greenfield |
| `movemental` | Movemental admin | Platform admin role + org — needs product confirmation per account |

Slug rule: kebab-case of legal name unless the operator overrides. Verify uniqueness in `organizations.slug` before insert (the trigger appends `-1`/`-2` on collision — that is a smell, not a fix; reuse the existing slug if the leader already has an org).

---

## Project + MCP context

This repo points at one Supabase project per environment. Source these from `.env.local` / `.env.shared` — do **not** memorize:

- `SUPABASE_PROJECT_ID` (production default for this repo: `vhaiiiykcukrlyvwlgip`)
- `NEXT_PUBLIC_SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (server-only — never echo, never write to a tracked file)

Tools to use:
- `mcp__supabase__list_projects` / `get_project` — confirm you're aimed at the right project before any write.
- `mcp__supabase__execute_sql` — every read check in this skill. Safe to run repeatedly.
- `mcp__supabase__list_tables` / `list_migrations` — schema introspection before touching DDL.
- `mcp__supabase__get_advisors` — pull current security + performance advisories as part of Phase 0.
- `mcp__supabase__search_docs` — when in doubt about Auth behavior (PKCE, templates, rate limits) prefer official docs over memory.
- `mcp__supabase__apply_migration` — **only** if a reviewed migration is required (e.g. backfilling `account_owner_id`). Tenant provisioning itself does not need new tables.

The Supabase Auth admin endpoints (`/auth/v1/admin/...`) are reached via `Bash` + `curl` using `SUPABASE_SERVICE_ROLE_KEY`; the MCP does not currently expose admin user creation.

---

## Phase 0 — Prerequisite security / auth gates (run before ANY tenant work)

Tenants you create now inherit whatever auth posture the project has today. Don't onboard real humans onto a project that hasn't passed these gates. If a gate fails, **stop** and either fix it (with operator approval) or hand back to the operator with a precise diff of what's missing.

### 0.1 Schema + trigger gate (DB)

```sql
-- Required tables
SELECT to_regclass('public.user_profiles')          AS user_profiles_exists,
       to_regclass('public.organizations')          AS organizations_exists,
       to_regclass('public.organization_memberships') AS memberships_exists;

-- The auto-provision trigger (handle_new_user) must be present
SELECT tgname FROM pg_trigger
WHERE tgname = 'on_auth_user_created'
  AND tgrelid = 'auth.users'::regclass;

-- And the function it calls must exist as SECURITY DEFINER
SELECT proname, prosecdef
FROM pg_proc
WHERE proname = 'handle_new_user' AND pronamespace = 'public'::regnamespace;
```

Pass = three regclasses + one trigger row + one `prosecdef = true` row. Fail = stop; instruct the operator to apply the `auto_provision_user_organization` migration first.

### 0.2 RLS gate (DB)

```sql
-- All three tenant tables must have RLS on
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('user_profiles','organizations','organization_memberships');

-- Each must have at least one policy
SELECT tablename, count(*) AS policy_count
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('user_profiles','organizations','organization_memberships')
GROUP BY tablename;
```

Pass = `rowsecurity = true` for all three, and `policy_count >= 1` for each. Fail = run the `supabase-security-audit` skill before continuing.

### 0.3 Advisor gate (MCP)

Call `mcp__supabase__get_advisors` for both `security` and `performance`. Block on any **CRITICAL** or **HIGH** security finding that touches `auth.*`, `public.user_profiles`, `public.organizations`, or `public.organization_memberships`.

### 0.4 Auth dashboard gate (operator-confirmed checklist)

These cannot be safely set with ad-hoc SQL. Confirm with the operator (cite the runbook §3.1–§3.5). Each item is a yes/no:

- [ ] **Site URL** and **Redirect URLs** match the deployed app + local dev for every env you're touching.
- [ ] **Email confirmations** enabled in production.
- [ ] **Password policy:** minimum length ≥ 8, character classes, **leaked-password protection** enabled where the plan supports it.
- [ ] **Custom SMTP** configured (Resend / SES / etc.) — not the Supabase default sender — for production.
- [ ] **Rate limits** for sign-up, password reset, and OTP reviewed against expected SMTP capacity.
- [ ] **CAPTCHA** decision recorded (on / off / staged) and documented.
- [ ] **MFA (TOTP)** decision recorded for platform admin accounts.
- [ ] Operator has 2FA on Supabase org access; no shared Studio login for real authors.

If any item is "no" without an explicit deferral, run the `auth-setup` skill (or the appropriate Dashboard step) and re-check before moving on.

### 0.5 App-side security gate (codebase)

Run a quick scan to confirm baseline app hardening so the tenant doesn't get pwned via the surface around their account. Defer to the `security-setup` skill if any are missing:

- HTTP security headers / CSP set in `next.config.ts` (or `src/middleware.ts`).
- Rate limiting on auth-adjacent API routes (`/api/auth/*`, password reset, magic-link callback).
- Input validation on every server action / route handler that writes to `public.*`.
- `SUPABASE_SERVICE_ROLE_KEY` only referenced from server files (`src/app/**/route.ts`, server actions, scripts) — never from client code.
- Env flag `NEXT_PUBLIC_SHOW_ADMIN_TENANT_SWITCHER` set correctly for the target env (Movemental deploy = `"true"`; per-author single-tenant deploys = `"false"`).

### 0.6 Drift gate

```sql
-- Orgs missing an account_owner (legacy data) — fix before adding new tenants
SELECT id, slug, name, account_owner_id
FROM public.organizations
WHERE account_owner_id IS NULL
ORDER BY created_at;

-- Profiles whose id does NOT match an auth.users row (the invariant)
SELECT p.id, p.email, p.account_status
FROM public.user_profiles p
LEFT JOIN auth.users u ON u.id = p.id
WHERE u.id IS NULL;

-- Duplicate emails — should be zero
SELECT lower(email) AS e, count(*)
FROM public.user_profiles
GROUP BY 1
HAVING count(*) > 1;
```

Any non-empty result blocks tenant creation for the affected slugs until reconciled (see Phase 4 — Duplicate identity).

**Phase 0 exit criterion:** every gate green or explicitly deferred-with-reason in the operator log.

---

## Phase 1 — Per-leader identity verification

For each target slug in scope, do this before creating anything:

1. **Read research file** at `docs/movement_leader_research/<slug>.md`.
   - If missing: ask the operator for legal name, **primary work email**, any secondary emails to avoid, organization display name, and confirm slug. Write the file (no passwords, no PII beyond what's needed for ops). Commit before moving on so the next pass has provenance.

2. **Read the runbook's per-target note** in `docs/movement_leader_research/tenant-wiring-prompt.md` §5 for the slug. Honor any special-case warnings (Alan = dedupe, Brad = placeholder, Movemental = product clarification).

3. **DB lookup** — find every row that might be this person:

   ```sql
   -- Auth users by email variants
   SELECT id, email, email_confirmed_at, last_sign_in_at, created_at
   FROM auth.users
   WHERE lower(email) IN (lower(:primary_email), lower(:secondary_email_1), lower(:secondary_email_2))
   ORDER BY created_at;

   -- Profiles by email and by name
   SELECT id, email, display_name, first_name, last_name, role, account_status, created_at
   FROM public.user_profiles
   WHERE lower(email) IN (lower(:primary_email), lower(:secondary_email_1))
      OR display_name ILIKE :name_like
      OR (first_name ILIKE :first_like AND last_name ILIKE :last_like)
   ORDER BY created_at;

   -- Existing orgs whose slug or name suggests this leader
   SELECT id, slug, name, account_owner_id, organization_type, is_active, created_at
   FROM public.organizations
   WHERE slug = :slug OR name ILIKE :name_like
   ORDER BY created_at;
   ```

4. **Decide** one of:
   - **Greenfield** — no rows found. Proceed to Phase 2.
   - **Existing live identity** — single canonical row, healthy. Skip auth creation, jump to Phase 3 verification.
   - **Existing but broken** — `account_status = 'merged'`, missing `account_owner_id`, mis-pointed `id`, or two rows for one human. **Stop.** Run Phase 4 (duplicate identity) before any writes.

Record the decision in the operator log (env, slug, decision, evidence). No passwords, no PII beyond what is already in `docs/movement_leader_research/`.

---

## Phase 2 — Provision (greenfield path)

Per the existing `supabase-add-tenant-user` skill (see `~/.claude/skills/supabase-add-tenant-user/SKILL.md`), the `handle_new_user` trigger does the heavy lifting. Your job is:

1. **Confirm target project** with `mcp__supabase__list_projects`. Reject if it does not match `SUPABASE_PROJECT_ID` from the resolved env file.

2. **Create the auth user.** Prefer in this order — the operator's plan in §3.2 / §3.3 of the runbook decides which:

   - **Magic-link invite** (preferred for real humans):

     ```bash
     curl -sS -X POST \
       "$SUPABASE_URL/auth/v1/admin/generate_link" \
       -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
       -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
       -H "Content-Type: application/json" \
       -d '{
         "type": "invite",
         "email": "<canonical email>",
         "data": { "display_name": "<display name>" }
       }'
     ```

     Hand the returned `action_link` to the operator over a secure channel. Never paste it into the repo, the chat transcript that will be saved, or a ticket.

   - **Password reset** if the user already exists in `auth.users` but needs a fresh credential:

     ```bash
     curl -sS -X POST \
       "$SUPABASE_URL/auth/v1/admin/generate_link" \
       -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
       -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
       -H "Content-Type: application/json" \
       -d '{ "type": "recovery", "email": "<canonical email>" }'
     ```

   - **Direct create with temp password** — local/dev only. Print the password to the operator, do not persist, and require a forced reset on first login.

3. **Wait for the trigger.** Poll for the side-effects (do not insert by hand):

   ```sql
   SELECT
     up.id            AS profile_id,
     up.email,
     up.role          AS platform_role,
     up.account_status,
     o.id             AS org_id,
     o.slug           AS org_slug,
     o.account_owner_id,
     om.role          AS membership_role,
     om.status        AS membership_status
   FROM public.user_profiles up
   LEFT JOIN public.organizations o
          ON o.account_owner_id = up.id
   LEFT JOIN public.organization_memberships om
          ON om.user_id = up.id AND om.organization_id = o.id
   WHERE lower(up.email) = lower(:canonical_email);
   ```

   Expect: one row, `org_slug` populated and unique, `account_owner_id = profile_id`, `membership_role = 'owner'`, `membership_status = 'active'`. `platform_role` should be `author` (or `user`, depending on what the trigger sets) — **never** `admin` unless the leader is the Movemental case (Phase 5).

4. **Reconcile slug if needed.** If the trigger appended `-1`/`-2` to the slug and there is no real conflict, rename in a single statement (operator-approved):

   ```sql
   UPDATE public.organizations
   SET slug = :desired_slug, updated_at = now()
   WHERE id = :org_id
     AND NOT EXISTS (
       SELECT 1 FROM public.organizations
       WHERE slug = :desired_slug AND id <> :org_id
     );
   ```

5. **Promote `role` to `author` if the trigger left it as `user`** (and the runbook §5 calls for `author`):

   ```sql
   UPDATE public.user_profiles
   SET role = 'author', updated_at = now()
   WHERE id = :profile_id AND role = 'user';
   ```

   Allowed values today: `admin`, `author`, `creator`, `editor`, `subscriber`, `user`. Do not invent.

---

## Phase 3 — Verification (always run, including for existing-identity targets)

```sql
-- Per-target smoke test
SELECT
  up.email,
  up.role         AS platform_role,
  up.account_status,
  o.slug          AS owned_org_slug,
  o.account_owner_id = up.id AS owner_id_matches,
  om.role         AS membership_role,
  om.status       AS membership_status
FROM public.user_profiles up
LEFT JOIN public.organizations o
       ON o.account_owner_id = up.id
LEFT JOIN public.organization_memberships om
       ON om.user_id = up.id AND om.organization_id = o.id
WHERE lower(up.email) = lower(:canonical_email);
```

Then the cohort-wide drift checks from Phase 0.6 again (orphan orgs, id mismatch, duplicate emails) — they should still be empty.

For each target, verify in the **app** (not just the DB):
- Sign-in with the magic link / new credential lands in the right tenant.
- Admin tenant switcher (if applicable) lists expected orgs.
- No console errors. Password reset round-trip works in staging with the same auth settings as production.

---

## Phase 4 — Duplicate identity / merged rows (Alan, Brad, anyone hitting "Existing but broken")

Per the runbook §6. Strict order:

1. **Inventory FKs** referencing the legacy `user_profiles.id`:

   ```sql
   SELECT 'organizations.account_owner_id' AS ref, count(*)
   FROM public.organizations WHERE account_owner_id = :legacy_id
   UNION ALL
   SELECT 'organization_memberships.user_id', count(*)
   FROM public.organization_memberships WHERE user_id = :legacy_id
   UNION ALL
   SELECT 'organization_memberships.invited_by', count(*)
   FROM public.organization_memberships WHERE invited_by = :legacy_id;
   -- extend with content tables (author_id, created_by, etc.) as the schema grows
   ```

2. **Decide canonical id** — the one matching the live `auth.users` row you're keeping.

3. **Reassign in a transaction** with operator approval. Prefer `mcp__supabase__apply_migration` over loose SQL so the change is reviewable and reversible.

4. **Soft-retire** the duplicate profile (`account_status = 'merged'`, internal note in the operator log). Do **not** delete from `auth.users` casually — understand the Auth Admin API + cascade rules first.

---

## Phase 5 — Movemental (admin) special case

Two orthogonal concerns the operator must split before you act:

- **(A) Platform admin role** — `user_profiles.role = 'admin'`. Grants cross-tenant access via `AdminTenantSwitcher`. Reserve for Movemental staff who actually need it. Each operator gets their own `auth.users` row — no shared logins, no shared inboxes.
- **(B) Movemental org membership** — membership in `organizations.slug = 'movemental'`. Owners vs members must be intentional and documented.

Order of operations for the Movemental case:

1. Confirm with product **which** humans get (A), which get (B), and which get both. Write it to the operator log before any UPDATE.
2. Run Phase 2 to provision each operator's auth user + personal owned org (every human still has one personal tenant).
3. Add membership to the Movemental org for the (B) folks:

   ```sql
   WITH usr AS (SELECT id FROM public.user_profiles WHERE lower(email) = lower(:email)),
        org AS (SELECT id FROM public.organizations WHERE slug = 'movemental')
   INSERT INTO public.organization_memberships
     (user_id, organization_id, role, status, joined_at, invited_by)
   SELECT usr.id, org.id, :membership_role, 'active', now(), NULL
   FROM usr, org
   WHERE NOT EXISTS (
     SELECT 1 FROM public.organization_memberships m
     WHERE m.user_id = usr.id AND m.organization_id = org.id
   );
   ```

4. Promote (A) folks to platform admin **only after operator sign-off**:

   ```sql
   UPDATE public.user_profiles
   SET role = 'admin', updated_at = now()
   WHERE lower(email) = lower(:email);
   ```

5. Sanity check the admin set:

   ```sql
   SELECT email, role
   FROM public.user_profiles
   WHERE role = 'admin'
   ORDER BY email;
   ```

---

## Hard rules (the runbook §0 carried forward)

1. **Never** paste passwords, service-role keys, or magic-link URLs into the repo, a ticket, or a chat that will be archived. Use a password manager and a one-time secure handoff.
2. **Never** call `mcp__supabase__apply_migration` or run destructive SQL in production without a second reviewer.
3. **Prefer** invite + user-set-password (or recovery link) over operator-set passwords for real humans.
4. **`public.user_profiles.id` MUST equal `auth.users.id`** for a given human. RLS, hooks, and `author_id` references all assume this. Any insert path that violates this invariant is a bug to escalate, not to work around.
5. **One human → one auth row.** Email variants, "+test" addresses, and shared inboxes for `auth.email` are discouraged.
6. **Service role key is server-only.** If you find it referenced in any `src/app/**/page.tsx`, `src/components/**`, or other client bundle, stop and treat it as a security incident.

---

## Done definition (per the runbook §8)

- [ ] All eight targets (seven authors + Movemental admin) have a documented state: exists / created / blocked (with reason).
- [ ] For each **active** author: auth confirms, profile `active`, org + owner membership, and successful login + reset tested.
- [ ] Auth Dashboard: URLs, SMTP, password policy, rate limits match product; MFA + CAPTCHA decisions recorded.
- [ ] No new duplicate identities; merge path followed where legacy data existed.
- [ ] Operator log complete (env, slug, decision, evidence) — no secrets, no PII beyond what is already in `docs/movement_leader_research/`.

---

## Reporting back

After every run, reply to the operator with:

1. Phase 0 gate status table (pass / fail / deferred per gate).
2. Per-target table: slug, decision (created / existing / blocked), uid, org_id, org_slug, membership_role, smoke-test result.
3. Any open follow-ups (e.g. "Liz Rios research file missing — provided template; need primary email").
4. The Supabase project id + env you acted in, and the timestamp.
5. **No** magic links, **no** passwords, **no** service-role tokens.
