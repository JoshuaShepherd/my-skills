---
name: supabase-add-tenant-user
description: Provision a new multi-tenant user on a Supabase-backed app with one auth user → one user_profiles row → one owned organization → one organization_memberships row. Tuned for the Movemental / alan-hirsch visual-editor schema (public.user_profiles, public.organizations, public.organization_memberships). Use whenever the user asks to "add a new user", "invite a creator", "onboard a tenant", or "add a member to an org".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__supabase__list_projects, mcp__supabase__execute_sql, mcp__supabase__apply_migration, mcp__supabase__list_tables
---

Add a new multi-tenant user: $ARGUMENTS

$ARGUMENTS can include any of:
- email (required)
- display name / full name
- role preference (`user` | `author` | `creator` | `editor` | `subscriber` | `admin`) — default `user`
- organization slug if joining an existing tenant (no new org created)
- membership role (`owner` | `admin` | `member`) — default `owner` if new org, `member` if joining
- Supabase project id / ref if not inferrable

---

## Operating principles

1. **Never grant `role = 'admin'` in `user_profiles` unless the user is explicitly the Movemental platform account.** Platform admin is reserved for the operator of the SaaS. Creators on the platform are `author` or `creator`, not `admin`.
2. **One auth user = one owned organization.** The `handle_new_user` trigger provisions a personal org automatically. Only bypass when joining an existing tenant.
3. **Never insert an `organization_memberships` row pointing to a non-existent org or user.** Verify both exist first.
4. **Never commit plaintext passwords to the repo.** Prefer magic-link invites (`supabase.auth.admin.inviteUserByEmail`) or passwordless OTP. If a password is required, print it once to the operator and do not persist.
5. **Always prefer the DB trigger over manual inserts.** `handle_new_user` is idempotent (`ON CONFLICT DO NOTHING` / existence checks) and will fill `user_profiles`, `organizations`, and `organization_memberships` automatically.

---

## Protocol

### Step 1 — Identify target project

Pick the Supabase project id for the app:
- Look in CLAUDE.md, `.env.shared`, or `.env.local` for `SUPABASE_PROJECT_ID` / `NEXT_PUBLIC_SUPABASE_URL`.
- If ambiguous, run `mcp__supabase__list_projects` and ask the operator.

For this repo (movemental-visual-editor):
- project id: `vhaiiiykcukrlyvwlgip`
- platform org slug: `movemental`
- platform org id: `928be32a-879a-407f-9bf4-4dfb17e5ea08`

### Step 2 — Confirm pre-reqs exist

Run once before acting (paste into the chat as a single SQL call):

```sql
-- Confirm schema is in the expected shape.
SELECT to_regclass('public.user_profiles')  AS user_profiles_exists,
       to_regclass('public.organizations')  AS organizations_exists,
       to_regclass('public.organization_memberships') AS memberships_exists;

-- Confirm the handle_new_user trigger exists.
SELECT tgname FROM pg_trigger
WHERE tgname = 'on_auth_user_created' AND tgrelid = 'auth.users'::regclass;
```

If any are missing, stop and tell the operator to run the
`auto_provision_user_organization` migration first.

### Step 3 — Classify the request

**A. New creator, new tenant.** Default case. Example:
> "Add brad@example.com as a new creator named Brad Example."

Action: create auth user; trigger auto-provisions org + owner membership.

**B. New member joining an existing tenant.** Example:
> "Add editor@foo.com as an editor on the alan-hirsch org."

Action: create auth user (trigger still provisions their own personal org;
that's fine — multi-tenant platforms often let humans have one personal org and
many org memberships). Then add an extra `organization_memberships` row
pointing to the target tenant.

**C. Platform admin (Movemental operator only).** Example:
> "Add ops@movemental.com as a platform admin."

Action: create auth user as (B) joining the `movemental` org as `owner`, then
`UPDATE public.user_profiles SET role = 'admin'` for that user. **Only do this
if the operator has confirmed the new admin should have cross-tenant access.**

### Step 4 — Create the auth user

Prefer the Supabase Auth admin API via the service role. The Service Role key
is in `~/Desktop/Dev/.env.shared` as `SUPABASE_SERVICE_ROLE_KEY`.

Options (in order of preference):

1. **Magic-link invite** (no password):

   ```bash
   curl -sS -X POST \
     "$SUPABASE_URL/auth/v1/admin/generate_link" \
     -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
     -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "type": "invite",
       "email": "NEW_EMAIL",
       "data": { "display_name": "NEW_DISPLAY_NAME" }
     }'
   ```

2. **Create with a temporary password** (dev / local testing only):

   ```bash
   curl -sS -X POST \
     "$SUPABASE_URL/auth/v1/admin/users" \
     -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
     -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "NEW_EMAIL",
       "password": "TEMP_PASSWORD",
       "email_confirm": true,
       "user_metadata": { "display_name": "NEW_DISPLAY_NAME" }
     }'
   ```

After this succeeds, **the trigger creates `user_profiles`, `organizations`,
and `organization_memberships` automatically**. You do not need to insert them
by hand.

### Step 5 — (Case B only) Join an existing tenant

If the user should also be a member of another org, insert the membership:

```sql
WITH usr AS (
  SELECT id FROM public.user_profiles WHERE email = 'NEW_EMAIL'
),
org AS (
  SELECT id FROM public.organizations WHERE slug = 'TARGET_ORG_SLUG'
)
INSERT INTO public.organization_memberships
  (user_id, organization_id, role, status, joined_at, invited_by)
SELECT usr.id, org.id, 'MEMBERSHIP_ROLE', 'active', now(), NULL
FROM usr, org
WHERE NOT EXISTS (
  SELECT 1 FROM public.organization_memberships m
  WHERE m.user_id = usr.id AND m.organization_id = org.id
);
```

### Step 6 — (Case C only) Promote to platform admin

Only after the operator has confirmed. Only for the Movemental account.

```sql
UPDATE public.user_profiles
SET role = 'admin', updated_at = now()
WHERE email = 'NEW_EMAIL';
```

Verify no other email keeps `role = 'admin'` unintentionally:

```sql
SELECT email, role FROM public.user_profiles WHERE role = 'admin' ORDER BY email;
```

### Step 7 — Smoke-test the result

Always run after provisioning:

```sql
SELECT
  up.email,
  up.role                     AS platform_role,
  up.account_status,
  o.slug                      AS owned_org_slug,
  om.role                     AS membership_role,
  om.status                   AS membership_status
FROM public.user_profiles up
LEFT JOIN public.organizations o       ON o.account_owner_id = up.id
LEFT JOIN public.organization_memberships om
       ON om.user_id = up.id AND om.organization_id = o.id
WHERE up.email = 'NEW_EMAIL';
```

Expect exactly one row, with:
- `platform_role` ∈ {`user`, `author`, `editor`, `subscriber`, `creator`} (never `admin` unless Case C)
- `owned_org_slug` not null (except for Case B-only members of another org)
- `membership_role = 'owner'` for the owned org

If any field is `NULL` where it shouldn't be, inspect the trigger:
`SELECT pg_get_functiondef('public.handle_new_user'::regproc);`

### Step 8 — Report back

Reply to the operator with:
1. The user id (uuid) and email
2. The owned org slug + id (if new tenant)
3. Any extra memberships created
4. Whether the platform role is `admin` or not
5. A copy of the smoke-test result
6. The invite / magic link URL (if step 4 option 1)

---

## Gotchas seen in this codebase

- `user_profiles.role` is a free-text column (not an enum). Case-sensitive.
  Allowed values today: `admin`, `author`, `creator`, `editor`, `subscriber`,
  `user`. Do not invent new values.
- `organizations.slug` is globally unique. The trigger appends `-1`, `-2`, … on
  collision. If joining an existing tenant rather than creating one, pass the
  slug to Step 5.
- `organizations.account_owner_id` is nullable in the schema but the app (see
  `src/lib/tenant/resolve-owned-org.ts`) requires it set for the user to be
  able to save. The trigger now sets it; legacy rows may not — run:
  `UPDATE public.organizations SET account_owner_id = $uid WHERE id = $org`
  to fix.
- `NEXT_PUBLIC_SHOW_ADMIN_TENANT_SWITCHER="false"` in `.env.local` silently
  hides the tenant switcher even for admins. Set to `"true"` for the
  Movemental deploy.
- RLS: `public.user_profiles` and `public.organizations` have `user_select_own`
  policies keyed on `auth.uid()`. Inserts via the trigger run as
  `SECURITY DEFINER`, so they bypass RLS intentionally.
