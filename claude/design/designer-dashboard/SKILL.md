---
name: designer-dashboard
description: Apply the Stitch → tokens → primitives → components → layouts design chain to React/Tailwind dashboard UI for cohesive, on-brand surfaces. Use when building or refactoring dashboard routes, course/lesson editors, metadata pages, shell chrome, or running an agentic UI pass that must stay token-aligned.
---

**Cursor:** Read this skill whenever the user asks for dashboard design cohesion, a “design system” pass on `(dashboard)` routes, or work that should match Stitch-derived visuals without ad hoc styling.

## Project anchors

| Layer | Location | Rule |
|-------|----------|------|
| **Stitch / reference** | `_docs/_build/_stitch/` (e.g. `course-editor/`, `dashboard/`) | Source of layout hierarchy, section names, and *intent* — not a license to paste one-off hex into JSX. Map colors and type roles to tokens below. |
| **Tokens** | `src/app/globals.css` → `@theme { … }` | Single source of truth for color, font families, radii implied by utilities. **Do not** add new palette hex in components; extend `@theme` if a semantic is missing. |
| **Primitives** | `src/components/ui/*` (shadcn) | Buttons, inputs, cards, dialogs — compose these before bespoke divs. |
| **Components** | `src/components/` (domain: `shell/`, `course-editor/`, etc.) | Reusable patterns shared across routes; no raw business logic in leaf pages when a component already exists. |
| **Layouts / pages** | `src/app/(dashboard)/`, `src/components/shell/` | Route structure, sidebars, main scroll regions; page files orchestrate data + composition only. |

## Ordered chain (always apply in this direction)

When changing or creating UI, walk the chain **top → bottom**; never invert (e.g. do not pick a Tailwind arbitrary color then retrofit a token).

1. **Stitch / product intent** — Identify the screen’s job (e.g. metadata editing, settings, list/browse). Note hierarchy from reference HTML: page title → section titles → labels → values → actions.
2. **Tokens** — Choose semantic colors: `bg-surface`, `bg-card`, `text-on-surface`, `text-on-surface-variant`, `border-outline/*`, accents `primary`, `primary-fixed-dim`, `lilac` / `lilac-strong` for CTAs, `success` / `warn` for status. Fonts: `font-sans` (Inter) body, `font-serif` (Newsreader) display headings, `font-display` (Manrope) labels and chrome.
3. **Primitives** — Prefer `Button`, `Input`, `Card`, etc. from `src/components/ui/` when the pattern matches; align variants with tokens (default vs outline vs destructive).
4. **Components** — Extract repeated dashboard patterns (stat rows, form sections, floating save bars) into `src/components/` when the same structure appears twice.
5. **Layouts** — Respect dashboard shell: sidebar width, main padding, scroll ownership. Keep page-level grids consistent with sibling routes (e.g. `max-w-5xl` / `max-w-6xl`, `grid-cols-12 gap-8`).

## Typography rules (dashboard)

- **Page title:** `font-serif`, large (`text-4xl`–`text-5xl`), `font-bold` or `font-semibold`, `tracking-tight`. Avoid defaulting to italic unless Stitch explicitly uses it for *that* heading tier.
- **Section titles:** `font-serif text-2xl`–`text-3xl` `font-semibold` `text-on-surface`.
- **Labels (forms, metadata):** `font-display text-xs font-semibold uppercase tracking-wider text-on-surface-variant` (or `text-primary` when the label is the primary focus of the field, e.g. slug).
- **Body / inputs:** `font-sans text-base` for readable dashboard copy; avoid `text-sm` as the default for long prose.
- **Numbers / stats:** `font-serif` + `font-semibold` + `tabular-nums` where alignment matters.

## Color & surface rules

- Cards: `bg-card border border-outline/25 shadow-sm` (or equivalent) so surfaces separate from `bg-surface` without washed-out borders.
- Fields: visible `border-outline/25` + `focus:border-primary-fixed-dim` + `focus:ring-2 focus:ring-primary/15` rather than borderless grey boxes only.
- Status: semantic `success` / `warn` tokens for published vs draft-style badges — keep contrast with `success-container` / `on-success-container` where applicable.
- **Never** use raw hex/RGB in JSX for dashboard theme colors unless documenting a one-off asset (e.g. SVG data URL). Video editor (`ve-*`) tokens are scoped to the editor; do not mix into cream dashboard pages.

## Agentic workflow checklist

Before opening a PR or handing off:

- [ ] No new hardcoded palette colors in the touched files (grep for `#` and `rgb` in TSX).
- [ ] Labels and headings follow the typography rules above.
- [ ] Interactive elements have visible focus and hover states.
- [ ] Stitch reference (if any) was consulted for hierarchy; implementation uses repo tokens.
- [ ] Run or skim `.claude/skills/design-audit/SKILL.md` on the changed route for pattern, color, type, motion, and a11y.

## Related skills

- Full pass / audit: `.claude/skills/design-audit/SKILL.md`
- Tailwind v4 tokens & scale: `.claude/skills/tailwind-design-system/SKILL.md`
- Stitch loops and prompts: `.claude/skills/stitch-design/SKILL.md`, `.claude/skills/stitch-ui-design/SKILL.md`
- Token cleanup: `.claude/skills/tailwind-cleanup/SKILL.md`
