---
name: stitch-intake-audit
description: >
  Phase B/01 of the Movemental tenant migration — fetch and cache Google Stitch
  wireframe screens locally, map each screen to its Next.js route, inventory which
  routes are still PlaceholderPage scaffolds, and produce a section-level gap audit
  before any React conversion. Use when starting a stitch migration, when the user
  says "intake the stitch screens", "cache the wireframes", "gap audit", "screen to
  route map", or before running stitch-page-port. Writes
  docs/build/notes/stitch-screen-route-map.md and stitch-gap-audit-<date>.md.
  Tenant-agnostic: reads TENANT_MANIFEST.md for the Stitch project, prompt library,
  and route scope. Does NOT convert to React (that's stitch-page-port) and does NOT
  change tokens (that's stitch-token-bridge).
user-invocable: true
allowed-tools: Read, Write, Grep, Glob, Bash, Agent, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

# Stitch intake and gap audit

Ensure every in-scope route has a cached Stitch HTML + PNG mapped to the right route,
with a gap report against the component checklist — **before** any conversion.

Scope from `$ARGUMENTS` (a screen set, cluster, or "all"); default to the full project.

## Read first

From the target repo (values resolve via `TENANT_MANIFEST.md`):

- `docs/build/prompts/stitch-migration/TENANT_MANIFEST.md` — `{{STITCH_PROJECT_NAME}}`,
  `{{STITCH_PROMPTS_HTML}}`, route scope (in-scope / tenant-unique / excluded), legacy redirects.
- `docs/build/prompts/stitch-migration/STITCH_ROUTE_INDEX.md` — order ↔ route lookup.
- `docs/build/prompts/stitch-migration/COMPONENT_CHECKLIST.md` — required sections per route.
- The Stitch prompt library at `{{STITCH_PROMPTS_HTML}}` (the `PROMPTS[].text` entries define section order).

## A. Fetch and cache (stitch-react Phase 0)

Use the Stitch MCP (`stitch__list_projects` / `stitch__list_screens` / `stitch__get_screen`)
or ask the user for the project id. For each screen:

1. `get_screen` → `htmlCode.downloadUrl`, `screenshot.downloadUrl`.
2. Save to `.stitch/designs/{page-slug}.{html,png,meta.json}`.
3. Prefer `scripts/fetch-stitch.sh` if present; else `curl -L`.

Page-slug convention: lowercase, hyphenated from the screen title ("Homepage" → `homepage`).
The existing **`stitch-react`** skill (fetch-only mode) does exactly this — delegate to it
if available rather than re-implementing fetch logic.

## B. Build the screen ↔ route map

Create / update `docs/build/notes/stitch-screen-route-map.md`:

| Stitch order | Screen title | page-slug | Next route | Scaffold status |
|--------------|--------------|-----------|------------|-----------------|
| 1 | Global chrome | global-chrome | layout | MISSING / CACHED |
| 2 | Homepage | homepage | / | PlaceholderPage |

Scaffold status = grep `src/app` for `PlaceholderPage` on that route.

## C. Gap audit per route

For each mapped in-scope route, compare four signals:

1. Sections in the Stitch prompt (`{{STITCH_PROMPTS_HTML}}` → `PROMPTS[].text`).
2. Sections in `COMPONENT_CHECKLIST.md`.
3. Sections present in the cached HTML (grep `data-section` / heading structure).
4. Current React page (`PlaceholderPage` = 0% migrated).

Emit a gap table:

| Route | Required sections | In Stitch HTML | In React | Action |
|-------|-------------------|----------------|----------|--------|
| / | Hero, SocialProof, … | 7/8 | 0/8 | Convert + synthesize Newsletter |

## D. Diagnose fake migrations

```bash
rg 'dangerouslySetInnerHTML|const html =| class=' src -l
```

Any hits → flag for real-JSX conversion in `stitch-page-port`.

## Deliverables

1. `.stitch/designs/` populated (or a list of MISSING screens for a human to generate in Stitch).
2. `docs/build/notes/stitch-screen-route-map.md`.
3. `docs/build/notes/stitch-gap-audit-<date>.md` with a prioritized conversion order
   (Foundation/tokens → global chrome → home → pathways → content → courses → ai/chat/auth → utility/legal).

## Do not

- Convert to React (that's `stitch-page-port`).
- Change `globals.css` tokens (that's `stitch-token-bridge`).
- Port routes the manifest marks excluded (e.g. another tenant's unique route).

## Acceptance criteria

- [ ] Screen ↔ route map exists for every in-scope route
- [ ] Each route has CACHED or MISSING documented
- [ ] Gap audit lists section-level deltas with actions
- [ ] No React conversion started here

## Related skills

`stitch-react` (fetch primitive) · `stitch-token-bridge` · `stitch-page-port` ·
`tenant-migration-playbook`
