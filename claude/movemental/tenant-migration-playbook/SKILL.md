---
name: tenant-migration-playbook
description: >
  Orchestrate the end-to-end migration of a Movemental thought-leader tenant —
  Google Stitch B&W wireframes → production React (L4/L5) → Supabase type-safety
  backend parity → tenant config alignment → validation. Use when onboarding or
  migrating any leader site under movement-leader-websites/ (e.g. michael-cooper,
  brad-brisco), when the user says "run the tenant migration", "migrate the stitch
  wireframes", "stitch playbook", "tenant onboarding pipeline", or references
  TENANT_MANIFEST.md / COMPONENT_CHECKLIST.md / MASTER_PLAYBOOK.md. This is the hub:
  it reads the manifest, scopes the slice, and dispatches to stitch-intake-audit,
  stitch-token-bridge, stitch-page-port, stitch-migration-validate,
  tenant-backend-parity, and tenant-structural-port. Tenant-agnostic — all
  tenant values come from the manifest, never hardcoded.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, TodoWrite
---

# Tenant migration playbook (orchestrator)

Drive a full Movemental tenant migration from Stitch wireframes to a production,
Supabase-backed tenant site. This skill is the **hub** — it never hardcodes a
tenant; it reads the manifest and delegates each phase to a discrete sub-skill.

Run it for: `$ARGUMENTS` — typically a phase/slice scope, e.g. `homepage`,
`content cluster`, `backend`, `full`, or a tenant slug to migrate.

This skill is **self-contained and portable** — the full tenant-agnostic process
(runbook, master playbook, route index, and the manifest / checklist templates) ships
inside this skill under `references/stitch-migration/`. It can bootstrap the process
into **any** project that doesn't have it yet.

## Step 0 — Locate or bootstrap the process docs

The process lives in the target repo at **`docs/build/stitch-migration/`** (older
repos may use `docs/build/prompts/stitch-migration/` — accept either; prefer the
former). Glob both before deciding it's missing.

**If the doc set already exists**, use it as-is.

**If it's missing** (a fresh project), scaffold it from this skill's bundled copy:

1. Copy `references/stitch-migration/*` → the target repo's
   `docs/build/stitch-migration/`. (Use the skill's own directory as the base — the
   bundle travels with the skill/plugin, so it works in any project.)
2. Fork the two templates in place:
   - `TENANT_MANIFEST.template.md` → `TENANT_MANIFEST.md`
   - `COMPONENT_CHECKLIST.template.md` → `COMPONENT_CHECKLIST.md`
3. Fill every `{{VAR}}` in `TENANT_MANIFEST.md` from the target tenant (slug, org id,
   design theme, reference repos, pathways, feature flags, leak grep patterns). If a
   value is unknown, ask the user — **never** invent a tenant value.

## Step 0.5 — Load the tenant contract (mandatory)

Read, in the target repo (under whichever `stitch-migration/` directory resolved above):

1. **`TENANT_MANIFEST.md`** — the source of every `{{VAR}}` (tenant slug, org id,
   design theme, reference repos, pathways, feature flags, leak grep patterns, branch
   naming). **Never** substitute a tenant value that isn't in the manifest.
2. **`MASTER_PLAYBOOK.md`** — phase pipeline.
3. **`COMPONENT_CHECKLIST.md`** — living route → status matrix.

If a value the prompts call `{{REFERENCE_REPO}}` / `{{STITCH_PROMPTS_HTML}}` resolves
to a sibling repo path, confirm the path exists before relying on it.

## Pipeline (delegate, don't reimplement)

```
Phase A  Stitch generation (human + Stitch — not automated here)
Phase B  Frontend: Stitch → React (00–10)
Phase C  Backend: type-safety + tenant parity (11–16)
Phase D  Optional structural code port from the reference repo
```

| Phase / step | Delegate to skill | Outcome |
|--------------|-------------------|---------|
| Charter + scope | *this skill* (Step 1) | Branch, scope, manifest read confirmed |
| 01 Intake + gap audit | `stitch-intake-audit` | Cached screens, screen↔route map, gap report |
| 02 Token bridge | `stitch-token-bridge` | Wireframe grayscale → tenant semantic tokens |
| 03–09 Chrome + page clusters | `stitch-page-port` | L4 sections + L5 pages per route cluster |
| 10 UI validation gate | `stitch-migration-validate` | Build/leak/token gates, checklist update |
| 11–16 Backend parity | `tenant-backend-parity` | Org identity, six-layer chain, config alignment |
| Deep code parity (optional) | `tenant-structural-port` | Course player / route normalization from reference |

For the per-screen HTML→React conversion mechanics inside `stitch-page-port`, the
underlying primitive is the existing **`stitch-react`** skill. Backend phases lean on
**`tenant-migrate`**, **`type-safety-chain`**, **`tenant-check`**, and **`validate`**.

## Step 1 — Charter and guardrails (run before any code)

Emit, before writing code:

1. Branch name from the manifest convention — `slice/Sxx-stitch-<topic>`,
   `slice/Sxx-backend-<topic>`, or `slice/Sxx-migration-<topic>`. Never commit to `main`.
2. Stitch screen id(s) / cached `.stitch/designs/` paths in scope.
3. Routes and layers touched, and which numbered prompts (01–16) the slice covers.
4. Blockers: missing Stitch screens, MCP auth, zero DB content for an enabled feature.

**Non-negotiables (enforce in every delegated phase):**

- Types flow downstream only: schema → zod → services → routes → hooks → UI.
  Never modify Drizzle schema for UI convenience.
- Never hand-edit generated `simplified/` files — fix the generator and rerun.
- No tenant strings in components; use `tenantConfig` / `useTenant()`.
- Don't restyle `src/components/ui/*`; fix L1 tokens or L4 section classes.
- Never add `"use client"` to `src/app/layout.tsx`.
- Archive existing `page.tsx` → `page-old.tsx` before replacing (stitch-react Archive Protocol).
- `pnpm` only. Never ship `dangerouslySetInnerHTML` dumps or raw wireframe hex (`#111`/`#666`).
- **Incomplete template policy:** if a Stitch screen omits a required section,
  *synthesize* it from the reference repo's structure + tenant tokens + manifest copy
  slots. Never leave IA holes; mark the row `PARTIAL` with a `Stitch gap:` note.

Wait for confirmation if a slice touches >12 new component files or needs new API routes.

## Step 2 — Sequence the slice

Use `TodoWrite` to track the slice. Typical orders:

- **New tenant, full run:** intake → token-bridge → page-port (chrome → home → clusters)
  → validate → backend-parity → validate. Structural-port only if validate flags
  hook/data gaps.
- **Single cluster (e.g. courses):** page-port (that cluster) → validate; add
  backend-parity if the cluster needs live data.
- **Backend-only slice:** backend-parity → validate.

Run phases as discrete delegated steps; after each, update `COMPONENT_CHECKLIST.md`
and `REFERENCE_PAGE_COMPARISON.md`. For large fan-out (many independent routes), each
route conversion can run as its own `stitch-page-port` invocation.

## Definition of "migration complete"

| Layer | Criterion |
|-------|-----------|
| IA | All in-scope routes match L5 section order + checklist |
| UI | No `PlaceholderPage`, no `dangerouslySetInnerHTML`, semantic tokens only |
| Types | `pnpm validate:all` green |
| Tenant | `pnpm verify:tenant-org` green; no source-tenant leaks in `src/` |
| Features | `features.*` matches org content counts in Supabase |
| Docs | `REFERENCE_PAGE_COMPARISON.md` + checklist updated |

## Related skills

`stitch-intake-audit` · `stitch-token-bridge` · `stitch-page-port` ·
`stitch-migration-validate` · `tenant-backend-parity` · `tenant-structural-port` ·
`stitch-react` · `tenant-migrate` · `tenant-check` · `type-safety-chain` · `validate`

## Install into another project (Claude plugin)

This skill and its six phase sub-skills ship as the **`movemental-tenant-migration`**
plugin, defined in `my-skills/.claude-plugin/marketplace.json`. To run the process in a
project that doesn't already have the skills:

```
/plugin marketplace add /home/josh/dev/01-Movemental-Core/my-skills
/plugin install movemental-tenant-migration
```

Then invoke `tenant-migration-playbook`; Step 0 bootstraps the process docs from the
bundled `references/stitch-migration/` into the target repo.

**External conversion primitives** (`stitch-react`, `tenant-migrate`) are not bundled —
they resolve from the manifest paths `{{STITCH_REACT_SKILL}}` / `{{TENANT_MIGRATE_SKILL}}`
(typically a sibling reference repo). Confirm those paths exist during Step 0.5.
