---
name: tenant-backend-parity
description: >
  Phase C/11–16 of the Movemental tenant migration — bring a tenant's Supabase-backed
  data layer to parity with the reference repo so stitch-migrated UI can wire real data.
  Walks: 11 Supabase org & tenant identity audit (MCP), 12 six-layer type-safety chain
  port (Drizzle → Zod → Services → Routes → Hooks → UI) + validate:all, 13 services & API
  routes parity, 14 hooks layer parity, 15 tenant.config.ts ↔ DB feature alignment, 16
  backend validation & cutover. Use when the user says "port the backend", "type safety
  chain", "services/hooks parity", "align the tenant config with the database", "feature
  flags vs db", "verify tenant org", or finishes the stitch UI and needs live data.
  Tenant-agnostic: org id, project id, reference repo, and leak patterns come from
  TENANT_MANIFEST.md. Delegates to tenant-migrate, type-safety-chain, validate, tenant-check.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, TodoWrite, mcp__supabase__execute_sql, mcp__supabase__list_tables, mcp__supabase__get_project, mcp__supabase__list_projects, mcp__supabase__get_advisors, mcp__supabase__get_logs
---

# Tenant backend parity

Port the data layer and align tenant config so migrated UI runs on real data. Types flow
**downstream only**: `Drizzle schema → Zod → Services → API routes → Hooks → UI`.
Scope from `$ARGUMENTS` (e.g. `org-audit`, `type-chain`, `services`, `hooks`, `config`, `full`).

This skill orchestrates existing primitives — `tenant-migrate` (Supabase + config audit),
`type-safety-chain` (the six-layer generators/validators), `validate`, `tenant-check`.
Delegate to them; this skill sequences them for a tenant migration and enforces scoping.

## Read first

`TENANT_MANIFEST.md` → `{{TENANT_SLUG}}`, `{{TENANT_ORG_ID}}`, `{{SUPABASE_PROJECT_ID}}`,
`{{REFERENCE_REPO}}`, `{{SOURCE_TENANT_NAME}}`, `{{AI_ASSISTANT_LABEL}}`, `{{CONTENT_RESEARCH}}`,
`{{STORAGE_PREFIX}}`, feature-flag table, leak grep patterns. Plus `src/lib/config/tenant.config.ts`,
`tenant.schema.ts`, `.env.local.example`.

## 11 — Supabase org & tenant identity (tenant-migrate Phase 1)

Via Supabase MCP on project `{{SUPABASE_PROJECT_ID}}` (`public` schema):

1. **Org row:** `SELECT id, name, slug, description FROM organizations WHERE slug = '{{TENANT_SLUG}}';`
   Confirm `id == {{TENANT_ORG_ID}}`. If missing → **STOP and report**; never create an org without approval.
2. **Content counts** (scoped by `organization_id`): books, articles, courses, podcast_episodes,
   videos, pathways/themes. Report per type.
3. **Storage:** bucket `media-library`, prefix `{{STORAGE_PREFIX}}` — note whether the tenant folder has assets.
4. **AI/vector** (if `features.chat` will be on): org-scoped corpus tables; `OPENAI_VECTOR_STORE_ID` must be tenant-specific.
5. **Env alignment** + **middleware** (`src/middleware.ts` — no hardcoded source-tenant paths).

Deliverable: `docs/build/notes/supabase-org-audit-{{TENANT_SLUG}}-<date>.md` with PASS/FAIL per
check and warnings for any `features.* = true` that has zero content. Do **not** INSERT/UPDATE orgs.

## 12 — Type-safety chain port (delegate to `type-safety-chain`)

Inventory first (report only): diff `{{REFERENCE_REPO}}` vs target for `src/lib/db`, `scripts/`,
`src/hooks/simplified/`, `src/lib/services/`; compare `validate:`/`generate:`/`db:` package scripts.
Then on branch `slice/Sxx-backend-type-chain`: port missing generator scripts, run generators
(`pnpm generate:zod|services|routes|hooks`; `db:generate` only with human coordination), and validate:

```bash
pnpm validate:all   # or db:check / contracts:check / services:check / routes:check / hooks:check / ui:check
```

**Never** hand-edit `src/hooks/simplified/*` or generated zod — fix the generator and rerun.
Every service must filter by `organization_id` / `{{TENANT_ORG_ID}}`. Never modify Drizzle schema for UI.

## 13 — Services & API routes parity

`diff -rq {{REFERENCE_REPO}}/src/app/api <target>/src/app/api` (prioritize `api/custom`),
and `.../src/lib/services`. Port missing handlers; routes call **services**, not raw db.
Priority when courses enabled: `courses/[slug]/progress|access|discussions`, `assessments/**`;
plus `/api/search` and chat/agent routes when those features are on. Confirm `organization_id`
scoping; do **not** port source-tenant-only demo services. Verify `pnpm routes:check`, `pnpm services:check`.

## 14 — Hooks layer parity

`diff -rq {{REFERENCE_REPO}}/src/hooks/{simplified,custom} <target>/...`. Build the UI→hook
dependency map from `COMPONENT_CHECKLIST.md`. Generate simplified hooks via `pnpm generate:hooks`
(after services). Port priority custom hooks (`use-course-learn`, progress/enrollment, chat).
Hooks call API routes/services — never import Drizzle. After each hook ports, **wire the
corresponding stitch-migrated section** to use it instead of the static stub, and update the
checklist hook column. Zero DB rows ⇒ keep the hook wired, show empty state. Verify `pnpm hooks:check`.

## 15 — Tenant config & feature alignment (tenant-migrate Phases 2–5)

- **A — Flags vs DB:** for each `features.*` / `contentTypes.*.enabled`, compare to the Prompt-11
  counts. Count 0 ⇒ feature `false` or empty-state-only (no fake data).
- **B — Identity strings:** replace name/tagline/description/copyright/logo, hero/about/contact/
  newsletter, `chat.assistantLabel → {{AI_ASSISTANT_LABEL}}`, search placeholder, themes/pathways,
  affiliations, author profile — tenant values only.
- **C — Content slugs:** `contentTypes.courses.availableSlugs` and featured books from research, never source-tenant slugs.
- **D — Leak grep** (delegate to `tenant-check`): `rg '{{leak patterns}}' src --glob '!tenant.config.ts'`; fix violations.
- **E — Env example:** `TENANT_ORG_ID`, document `OPENAI_VECTOR_STORE_ID` (chat) and Stripe keys (checkout).

Deliverable: updated `tenant.config.ts` (tenant strings only — no unrelated refactors) +
`docs/build/notes/tenant-config-alignment-<date>.md`.

## 16 — Backend validation & cutover

```bash
pnpm validate:all && pnpm typecheck && pnpm lint && pnpm build
pnpm verify:tenant-org           # if defined
rg '{{SOURCE_TENANT_NAME}}|{{REFERENCE_SLUG}}' src --glob '!tenant.config.ts' -l
rg 'PlaceholderPage|dangerouslySetInnerHTML' src ; rg '#111111|#666666' src/components --glob '*.tsx'
```

Re-run content counts for `{{TENANT_ORG_ID}}` vs the Prompt-11 baseline. Update
`COMPONENT_CHECKLIST.md`, `REFERENCE_PAGE_COMPARISON.md`, L5 page docs, and README. Emit a
migration report: org PASS/FAIL · `validate:all` PASS/FAIL · routes BUILT N/M · features aligned ·
screens converted · APIs/hooks ported · archived page-old files · production blockers (content
seeding, Vercel env, Stripe/chat) · recommended follow-up slices.

**Human cutover** (flag, don't do): Vercel `TENANT_ORG_ID` env, Supabase auth redirects, Stripe
keys, `OPENAI_VECTOR_STORE_ID`, Sentry DSN, DNS/custom domain.

## Acceptance criteria

- [ ] Org row matches `{{TENANT_ORG_ID}}`; audit committed
- [ ] `pnpm validate:all` green (or failures documented with layer owner)
- [ ] No hand-edits in `simplified/`; services scope by `organization_id`
- [ ] Course APIs/hooks exist if `features.courses` true
- [ ] Every `features.* = true` has DB content or a documented staging plan
- [ ] Leak grep clean; `pnpm verify:tenant-org` passes

Do not merge to `main` until this passes or blockers are explicit product decisions.

## Related skills

`tenant-migrate` · `type-safety-chain` · `validate` · `tenant-check` ·
`tenant-structural-port` · `tenant-migration-playbook`
