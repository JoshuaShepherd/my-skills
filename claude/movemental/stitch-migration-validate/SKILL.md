---
name: stitch-migration-validate
description: >
  Phase B/10 of the Movemental tenant migration — the UI validation gate run after a
  stitch-page-port slice (or after Prompts 03–09) and before merge. Runs build/lint/type
  checks, greps for the forbidden patterns (PlaceholderPage, dangerouslySetInnerHTML,
  raw wireframe hex), does a Stitch-PNG-vs-rendered visual spot check, updates
  COMPONENT_CHECKLIST.md and REFERENCE_PAGE_COMPARISON.md, and emits a conversion report.
  Use when the user says "validate the stitch slice", "run the UI gate", "check the
  migration before merge", "is this slice done", or finishes a page-port. Tenant-agnostic:
  leak grep patterns and route scope come from TENANT_MANIFEST.md. This is the UI gate;
  full backend validation lives in tenant-backend-parity.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Stitch migration validation gate

Gate a stitch UI slice before merge. Scope from `$ARGUMENTS` (the routes in the slice;
default to all converted routes).

## Read first

- `TENANT_MANIFEST.md` — content leak grep patterns, source-tenant names, route scope.
- `COMPONENT_CHECKLIST.md` and `REFERENCE_PAGE_COMPARISON.md`.
- The slice's gap audit `docs/build/notes/stitch-gap-audit-*.md`.

## Commands

```bash
pnpm typecheck
pnpm lint
pnpm build
rg 'PlaceholderPage' src/app
rg 'dangerouslySetInnerHTML' src
rg '#111111|#666666' src/components --glob '*.tsx'   # should be clean
```

`PlaceholderPage` is allowed only on routes the checklist explicitly defers; all three
greps should otherwise be clean on routes marked `BUILT`.

## Visual verification

For each converted route:
1. Compare `.stitch/designs/{slug}.png` with a `pnpm dev` screenshot (use the `verify` or
   browser-driver skill if a screenshot harness is available).
2. Confirm section order vs `COMPONENT_CHECKLIST.md`.
3. Light + dark mode spot check.

## Documentation updates

1. `COMPONENT_CHECKLIST.md` — set each route's Status (`SCAFFOLD` | `PARTIAL` | `BUILT` | `DEFERRED`).
2. `docs/internal/engineering/REFERENCE_PAGE_COMPARISON.md` — create/update rows.
3. Close resolved gaps in `docs/build/notes/stitch-gap-audit-*.md`.
4. Tick the relevant phase in the repo `README.md` migration checklist.

## Conversion report (per stitch-react Phase 8)

Emit markdown for the slice: screens converted · archived `page-old` files · new component
paths · token changes · hooks wired vs static stubs · issues flagged for `tenant-backend-parity`
or `tenant-structural-port`.

## PR checklist

- [ ] Branch `slice/Sxx-stitch-*`
- [ ] No hex colors in components
- [ ] `tenantConfig` for copy
- [ ] Feature flags respected
- [ ] No source-tenant content leaks (run `tenant-check` if available)
- [ ] CI green

## Slice "done" definition

1. All routes in scope are `BUILT` or `PARTIAL` with documented gaps.
2. No `PlaceholderPage` on those routes.
3. `pnpm build` passes.
4. Checklist + comparison doc updated.

## Handoff

If hooks/data are still missing after UI conversion, open a follow-up with
`tenant-backend-parity` (Prompts 11–16) or, for deep course/route parity,
`tenant-structural-port`.

Do not merge to `main` until this gate passes.

## Related skills

`stitch-page-port` · `tenant-check` · `verify` · `tenant-backend-parity` ·
`tenant-structural-port` · `tenant-migration-playbook`
