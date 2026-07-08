---
name: stitch-token-bridge
description: >
  Phase B/02 of the Movemental tenant migration — map the Google Stitch black-and-white
  wireframe palette (the layout-proof grayscale) onto the tenant's production semantic
  design tokens, plus the typography and spacing bridge. Run ONCE after stitch-intake-audit
  and before any page conversion. Use when the user says "token bridge", "map the
  wireframe colors", "set up the design tokens for the stitch migration", or before
  stitch-page-port. Writes docs/build/notes/stitch-token-bridge.md and makes minimal,
  approved edits to globals.css / tailwind.config.ts. Tenant-agnostic: the production
  theme (e.g. Editorial Indigo / Atelier Amber) comes from TENANT_MANIFEST {{DESIGN_THEME}}.
  Prevents raw #111/#666 hex and wireframe fonts from leaking into production components.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Stitch token bridge

Wireframe colors are **layout proof only**. Production uses the tenant's semantic
tokens. This skill produces the mapping table every page conversion then follows, so
token extraction happens once — not per page.

Run once for the tenant in `$ARGUMENTS` (default: the current target repo).

## Read first

- `.stitch/designs/design-system.html` (or the embedded `tailwind.config` in any screen's `<head>`).
- `{{GLOBALS_CSS}}` (default `src/app/globals.css`) and `tailwind.config.ts`.
- `TENANT_MANIFEST.md` → `{{DESIGN_THEME}}`, `{{DESIGN_CHARTER}}`.
- The reference design charter if present (`{{REFERENCE_REPO}}/docs/internal/design/DESIGN_CHARTER.md`).

## Wireframe palette (Stitch — never ship as-is)

| Role | Wireframe hex | Purpose |
|------|---------------|---------|
| Page bg | `#FFFFFF` / `#F7F7F7` | Alternating sections |
| Text primary | `#111111` | Headlines, body |
| Text secondary | `#666666` | Meta, captions |
| Text tertiary | `#999999` | Labels |
| Border | `#E0E0E0` / `#CCCCCC` | Hairlines |
| Placeholder media | `#E8E8E8` | Image blocks |
| Primary button | `#111111` fill, white text | CTAs |

## Semantic mapping (production)

Map every Stitch color usage to a semantic token (these names are stable across tenants;
the *values* live in `globals.css` per `{{DESIGN_THEME}}`):

| Stitch intent | Tailwind / CSS variable |
|---------------|-------------------------|
| Page background | `bg-background` |
| Alt section | `bg-muted` |
| Primary text | `text-foreground` |
| Secondary text | `text-muted-foreground` |
| Borders | `border-border` |
| Primary CTA | `bg-primary text-primary-foreground` |
| Cards | `bg-card border-border` |
| Placeholder media | `bg-muted text-muted-foreground` |

## Typography bridge

| Wireframe | Tenant token |
|-----------|--------------|
| Serif headlines (Georgia) | `font-heading` — configure in `layout.tsx` via `next/font` |
| Sans body (system-ui) | `font-sans` |
| Mono routes/metadata | `font-mono` |

## Tasks

1. Extract the spacing rhythm from Stitch HTML (`py-16`, `max-w-1200`, 8px grid) and
   document it in `docs/internal/design/SPACING_NOTES.md` (create if missing).
2. Update `globals.css` **only** if the tenant tokens lack a required role (card, accent,
   popover). **Ask before changing existing values.**
3. Ensure `tailwind.config.ts` `fontFamily` extends to the `next/font` CSS variables.
4. Write the mapping to `docs/build/notes/stitch-token-bridge.md` — this is the
   contract `stitch-page-port` reads.

## Rules

- Do **not** add wireframe hex to `tailwind.config` as named colors.
- Do **not** re-extract tokens per page after this — every page uses this bridge.
- Dark mode: every token used in conversions must have a paired `.dark {}` value.

## Deliverables

- `docs/build/notes/stitch-token-bridge.md` (the mapping table).
- Minimal `globals.css` / `tailwind.config.ts` changes (approved).
- `pnpm typecheck` passes.

## Acceptance criteria

- [ ] Mapping doc exists
- [ ] No raw `#111` / `#666` patterns documented as allowed in component code
- [ ] Light + dark tokens cover card, muted, primary, border

Stop here — do not convert pages.

## Related skills

`stitch-intake-audit` · `stitch-page-port` · `design-chain` / `color-audit`
(token-violation audits) · `tenant-migration-playbook`
