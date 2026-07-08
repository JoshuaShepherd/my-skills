---
name: stitch-page-port
description: >
  Phase B/03–09 of the Movemental tenant migration — the repeatable workhorse that
  converts a cached Google Stitch wireframe into production React for one route or one
  route cluster (global chrome, home/marketing, pathways, content library, courses, AI/
  chat/auth/account, utility/legal/tenant-unique). Replaces PlaceholderPage scaffolds
  with Server Component pages composing L4 section components, applies the token bridge,
  wires Layer-5 hooks when they exist, and SYNTHESIZES missing sections from the reference
  repo when a Stitch screen is incomplete. Use when the user says "port the homepage",
  "convert the courses pages", "build the content cluster from stitch", "migrate this
  route", or runs the playbook per-cluster. Underlying per-screen mechanic is the
  stitch-react skill. Tenant-agnostic: copy slots, pathways, and design come from
  TENANT_MANIFEST.md. See references/clusters.md for per-cluster section orders.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, mcp__stitch__get_screen
---

# Stitch page port

Convert a Stitch wireframe → production React for the route/cluster in `$ARGUMENTS`
(e.g. `homepage`, `pathways`, `content`, `courses`, `chrome`, `/contact`).

This skill is the orchestration + tenant-correctness layer around the existing
**`stitch-react`** skill (which does the raw HTML→React decomposition). Always prefer
delegating the mechanical conversion to `stitch-react`, then apply the rules here.

## Read first

- `TENANT_MANIFEST.md` — copy slots, pathways table, feature flags, `{{REFERENCE_REPO}}`,
  excluded/tenant-unique routes.
- `COMPONENT_CHECKLIST.md` — the row(s) for the route(s) in scope (required section order).
- `docs/build/notes/stitch-token-bridge.md` — the token mapping (from `stitch-token-bridge`).
- `docs/build/notes/stitch-screen-route-map.md` — cache paths (from `stitch-intake-audit`).
- `references/clusters.md` (in this skill) — section-order spec for the cluster in scope.
- The reference page + components: `{{REFERENCE_REPO}}/src/app/(public)/<route>` and `src/components/<area>/`.

## Per-route conversion procedure

1. **Visual audit** — read the cached HTML + PNG (`.stitch/designs/{slug}.html|png`).
2. **Read the reference** page and components for data-wiring patterns.
3. **Archive** the existing `page.tsx` → `page-old.tsx` (stitch-react Archive Protocol).
4. **Decompose** the Stitch HTML into L4 section components under `src/components/<area>/`.
   If a route needs >4 new sections, plan first and get approval.
5. **Apply the token bridge** — semantic tokens only; never wireframe hex.
6. **Wire data** — use Layer-5 hooks from `src/hooks/` if they exist; otherwise render
   static tenant placeholder copy from the manifest and **flag the route for
   `tenant-backend-parity`** (Prompts 13–14) before it can be marked `BUILT`.
7. **Compose the Server Component** `page.tsx` with feature gates at page level, e.g.
   `{tenantConfig.features.chat && <AILabTeaser />}`. Never add `"use client"` to a layout.
8. **Handle states** — loading / empty / error in client sections. Empty DB ⇒ empty state,
   never a removed section and never fake data.

## Incomplete-template synthesis (critical)

When the cached Stitch screen omits a section the checklist/L5 requires:

1. Read `STITCH_ROUTE_INDEX.md` + L5 page spec + `COMPONENT_CHECKLIST.md` for the required sections.
2. Implement the missing section in tenant design — spacing rhythm, shadcn primitives
   (Card, Button, Input, Tabs, Accordion), manifest copy slots.
3. If the section exists in `{{REFERENCE_REPO}}`, port its **structure** and re-skin with tenant tokens.
4. Mark the route `PARTIAL` in `REFERENCE_PAGE_COMPARISON.md` with note `Stitch gap: {section}`.
5. Never delete routes or reorder sections without documenting it.

## Global chrome (run before page clusters)

Chrome lives in `(public)/layout.tsx` only — exclude header/footer from individual page
conversions. Create `src/components/navigation/{site-header,site-footer,mobile-nav}.tsx`,
wire `tenantConfig.logo`, `tenantConfig.copyright`, feature-gate nav items
(`{features.courses && <CoursesLink/>}`), and use shadcn `NavigationMenu` + `Sheet` (mobile).
Server layout where possible; client only for mobile menu + theme toggle.

## Tenant correctness (every route)

- Tenant strings come from `tenantConfig` / research, never hardcoded — no source-tenant
  (reference) or wireframe-placeholder (Stitch) copy unless a feature is enabled.
- Pathway names, featured book, AI assistant label, podcast name → manifest tables.
- One `<h1>` per page. Section order matches the checklist exactly.

## Per route, finish with

`pnpm typecheck` → confirm section order → update `COMPONENT_CHECKLIST.md` row to
`BUILT` or `PARTIAL`. Emit a stitch-react conversion report (screens converted, archived
page-old files, new component paths, hooks wired vs static stubs, flagged gaps).

Full UI gate runs separately in **`stitch-migration-validate`**.

## Cluster specs

See `references/clusters.md` for the exact section order, route lists, and L4 component
paths for: global chrome · home/marketing · pathways · content library · courses ·
AI/chat/auth/account · utility/legal/tenant-unique.

## Related skills

`stitch-react` (conversion primitive) · `stitch-token-bridge` · `stitch-intake-audit` ·
`stitch-migration-validate` · `tenant-backend-parity` · `course-ux` · `new-page` ·
`tenant-migration-playbook`
