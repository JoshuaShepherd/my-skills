---
name: movement-leader-platform-build
description: >
  Audits a movement-leader tenant against the master component checklist, writes a
  gap-remediation build prompt to docs/build/prompts/, then implements missing pages
  and components in the repo's existing design system with full type-safety compliance.
  Use when running the platform checklist, auditing component gaps, building remaining
  pages, platform build, master-component-checklist, or remediating missing shell/themes/
  library/formation routes. Run from any movement-leader repo root.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, TodoWrite
---

# Movement Leader Platform Build

End-to-end: **audit** → **build prompt** → **implement** → **validate**.

Run from the **tenant repo root** (`movement-leader-websites/{slug}/`, `alan-hirsch/`, or `brad-brisco/`).

Scope from `$ARGUMENTS`: optional `audit-only`, `build-only`, or `--zone {shell|home|themes|library|formation|about|chrome|footer}`.

## Read first (mandatory)

| Doc | Path |
|-----|------|
| Master checklist | `docs/build/checklists/components/master-component-checklist.md` |
| Design charter | `docs/design/README.md` + `docs/design/DESIGN_CHARTER.md` |
| Design layers | `docs/design/layers/L1_TOKENS.md` … `L5_PAGES.md` |
| Type safety | `docs/internal/type/TYPE_SAFETY.md` |
| Tenant config | `src/lib/config/tenant.config.ts` |
| Env contract | `src/lib/env.ts` |

If the master checklist is missing, stop.

## Phase 1 — Audit

Follow master checklist agent protocol steps 1–4. Copy master → `docs/build/checklists/components/{tenant}-audit-{YYYY-MM-DD}.md`. Inspect `src/app/**`, `src/components/**`, `tenant.config.ts`, hooks. Mark `[x]` / `[~]` / `[ ]` with paths. Summary at top: zone %, open **(R)** items, four load-bearing theme sections, identity assets.

Details: `references/reference.md` in this skill directory (or `.cursor/skills/movement-leader-platform-build/reference.md` when symlinked).

Stop if `audit-only`.

## Phase 2 — Build prompt

Write `docs/build/prompts/build-remaining-{tenant}-{YYYY-MM-DD}.md`:

- Every `[ ]` / `[~]` grouped by page, dependency order (shell → hubs → detail → enrichment)
- Build in repo design system; reuse L4; semantic tokens; no new visual language
- **(R)** gates; hook wiring for data sections
- Final validation: `pnpm typecheck`, `pnpm validate:all`, `pnpm build`

Template: see `references/reference.md#build-prompt-template`.

## Phase 3 — Build

Per build prompt, in dependency order. Design: tokens first, reuse L4, `tenantConfig` copy, server pages, Lucide. Type safety: hooks only for data, no invented types, fix bottom-up. Update audit checkboxes as items ship.

## Phase 4 — Validate

```bash
pnpm typecheck && pnpm validate:all && pnpm build
```

Fix bottom-up until clean.

## Phase 5 — Report

Audit path, % complete, build prompt path, zones built, remaining **(R)** gaps, validation pass/fail.

## Do not

- Edit the master checklist file
- Leave **(R)** routes on PlaceholderPage
- Skip validation after data changes
- Hardcode tenant or Movemental brand strings
