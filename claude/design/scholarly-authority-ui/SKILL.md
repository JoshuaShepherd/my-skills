---
name: scholarly-authority-ui
description: >
  Front-end UI design expert for movemental-visual-editor-main's "Warm
  Scholarly Authority" dashboard design system. Use when building or restyling
  any dashboard page, content/course card, editor surface, list/detail view,
  shell chrome, or component to match the existing visual language. Anchors to
  src/app/globals.css (@theme tokens), the src/components/ui/* primitives, and
  golden pages like src/app/(dashboard)/content/page.tsx. Keywords: warm
  scholarly authority, cream paper, deep navy, amethyst sidebar, Newsreader,
  Inter, Manrope, Material Symbols, StatusChip, no-line rule, Tailwind v4,
  shadcn, Radix, design tokens, designer-dashboard.
---

# Warm Scholarly Authority UI (movemental-visual-editor-main)

Use this skill whenever you build or restyle front-end UI in this repo. Match the
established dashboard design language faithfully.

## North Star

**"Warm Scholarly Authority"** — a Next.js dashboard for `dashboard.movemental.ai`.
Warm cream paper surfaces, **deep-navy** primary, **amethyst** sidebar, serif
display headings over a crisp sans UI. Calm, editorial, token-driven. Structure
comes from background-tier shifts and hairlines (the **No-Line rule**), not boxes.

> Note: the legacy drag-and-drop "site builder" is **retired** (the
> `(dashboard)/site/[[...slug]]` route is a tombstone). There is **no Puck /
> Builder.io / Craft.js**. Composable rich content is authored via **TipTap**
> node-views in `src/components/article-editor/extensions/`. The "blocks" you
> design are dashboard pages, content/course cards, editor sections, and shell chrome.

## Source of truth (read these, in order)

1. `src/app/globals.css` — **the token bible** (`@theme` block, lines ~10–193). Every color/font resolves to a token here. There is **no `tailwind.config.*`**.
2. `.claude/skills/designer-dashboard/SKILL.md` — the most accurate prose rulebook (design chain, typography/color rules).
3. Golden pages/components:
   - `src/app/(dashboard)/content/page.tsx` — gold-standard list page.
   - `src/components/content-library/ContentLibraryItemViews.tsx` (`ContentItemCard`) — canonical card.
   - `src/components/ui/{button,card,status-chip}.tsx` — primitive contracts.
   - `src/app/(dashboard)/layout.tsx` + `src/components/shell/{AppSidebar,TopBar}.tsx` — chrome.

## Stack

Next.js 16 App Router · React 19 · Tailwind **v4** (CSS-first `@theme`, hex tokens,
**no config file, no dark-mode toggle**) · shadcn/Radix + CVA · `cn()` from
`src/lib/utils.ts` · icons: **Material Symbols Outlined** (ligature font) + **lucide-react** (both in use) · TipTap, Remotion, TanStack Query.

## Color — semantic tokens only (no raw hex / no raw Tailwind palette)

Every `--color-*` maps directly to `bg-*`/`text-*`/`border-*`. Add new colors by
extending `@theme`, never inline.

| Role | Utility | Hex |
|---|---|---|
| Page surface | `bg-surface` | `#fbf9f4` |
| Card / white layer | `bg-surface-container-lowest` / `bg-card` | `#ffffff` |
| Tier surfaces | `bg-surface-container-low/…/highest` | `#f5f3ee` → `#dad6cf` |
| Ink | `text-on-surface` / `text-foreground` | `#121311` |
| Primary (deep navy) | `bg-primary` | `#14006a` |
| Primary container | `bg-primary-container` | `#260b9e` |
| Tertiary (amethyst — sidebar) | `bg-tertiary-container` | `#37285e` |
| Serif title accent | `text-tertiary-container` | `#221148`/`#37285e` |
| Accent wash (selected) | `bg-accent` / `bg-surface-accent-wash` | `#f0edff` |
| Lilac CTA pair | `bg-lilac` / `text-on-lilac` | `#c9beff` / `#311c7e` |
| Hairline | `border-outline` / `border-outline-variant` | `#5f5668` / `#b5a8c4` |

Status: `success`/`warn`/`error` (+ `-container`/`-on-container`). **Scoped dark
namespaces** `ve-*` (video editor), `reader-*` (reader mode), `lucid-*` (recorder)
are **independent palettes** — never mix them into the cream dashboard. There is
**no global light/dark pair**.

## Typography

- **Body/UI:** Inter → `font-sans` (default; avoid `text-sm` as a default body size — use `text-base`).
- **Display/headings:** Newsreader → `font-serif`.
- **Labels/eyebrows/table headers/chrome:** Manrope → `font-display`.

Canonical roles (mirror the golden pages):
- **Page title:** `font-serif text-4xl md:text-5xl font-semibold tracking-tight text-tertiary-container`.
- **Section title:** `font-serif text-2xl–3xl font-semibold text-on-surface`.
- **Eyebrow/label:** `font-display text-[0.7rem] font-bold uppercase tracking-[0.2em] text-secondary-role` (or `text-on-surface-variant`).
- **Stats/numbers:** `font-serif … tabular-nums`.
- **Long-form prose:** `.content-prose` / `Prose` primitive — 17px, `lh 1.75`, serif headings, `max-width: var(--prose-max)` (65ch).

## Spacing, radius, elevation, motion

- **No `tailwind.config`** → Tailwind v4 stock spacing (4px) + default breakpoints.
- **Containers:** dashboard pages `mx-auto max-w-6xl px-6 py-10 md:px-10 md:py-12`; editors `max-w-5xl`–`6xl`; reading measure `65ch`.
- **Shell:** `(dashboard)/layout.tsx` = `flex h-dvh overflow-hidden bg-surface`, fixed **240px** amethyst sidebar (`bg-tertiary-container`), scroll on `<main>`. **TopBar** = `sticky top-0 h-14 z-50 bg-surface/80 backdrop-blur-md` frosted glass, **no bottom border**.
- **Radius (match live code):** `rounded-sm` for small controls/chips, `rounded-md` for buttons/cards/inputs (the `ui/*` primitives), **`rounded-xl` for larger feature cards/containers** (e.g. `rounded-t-xl` card media), `rounded-full` for avatars/pills. All are valid.
- **Shadows:** cards use `shadow-sm`; custom ambient shadows are **navy-tinted**, e.g. `shadow-[0_12px_28px_rgba(20,0,106,0.12)]` — not black. Hover = **border-tint shift** (`hover:border-primary-fixed-dim/40`), not lift.
- **Motion:** **no framer-motion/motion**. Tailwind utilities + Radix data-state +
  CSS transitions only. Canonical: `transition-colors` for hover/color,
  `transition-all duration-150/200` for menus, `animate-pulse` skeletons on
  `bg-surface-container-highest`, `animate-spin` spinners, `active:scale-95` press.

## Component patterns — compose `ui/*` primitives

- **Button** (`ui/button.tsx`, CVA, `rounded-md`, focus ring, `[&_svg]:size-4`): `default`/`primary` = `bg-primary text-primary-foreground shadow hover:bg-primary/90`; sizes `xs/sm/default/lg/icon`. (Primitives use `React.forwardRef` — match that.)
- **Card** (`ui/card.tsx`): `rounded-md border bg-card text-card-foreground shadow`; header/content `p-6`; `CardTitle` `font-semibold leading-none tracking-tight`.
- **StatusChip** (`ui/status-chip.tsx`) — the canonical status pattern; **use it instead of inline color maps**. `rounded-xs px-2 py-0.5 text-xs font-medium`, e.g. `draft → bg-secondary-container`, `published → bg-primary-fixed`. Prefer over generic `Badge` for state.
- **Canonical card recipe** (`ContentItemCard`): `Card className="flex h-full flex-col overflow-hidden border-outline/25 bg-card shadow-sm transition-colors hover:border-primary-fixed-dim/40"`; media `rounded-t-xl`; display eyebrow + `StatusChip` + `font-serif text-lg font-semibold text-tertiary-container line-clamp-2` title; ghost footer `border-t border-outline-variant/15 bg-surface-container-lowest/30`.
- **List page recipe** (`content/page.tsx`): serif page title + display eyebrow → filter tabs → search input → `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6` → skeleton loading → empty state. Token-only colors throughout.
- **Sidebar nav:** active item `bg-plum/30` with a `before:` left pill in `bg-primary-fixed`.

## Avoid (drift — do not copy)

- **`src/components/primitives/eyebrow.tsx` & `prose.tsx`** reference a non-existent vocabulary (`text-inverse-foreground`, `tracking-eyebrow`, "Instrument Serif", `--prose-max: 640px`, "DESIGN.md §5 Concept Modern"). **None of those tokens exist here.** Use the inline eyebrow pattern above instead.
- **The `design-chain-audit` skill's roundness/shadow ceilings are fiction** vs. the live code ("max `rounded-md`", "no `shadow-lg`", `max-w-7xl`). Match the live code: `rounded-xl` feature cards and `max-w-6xl` pages are correct.
- **Reference docs cited by skills don't exist** (`_docs/_build/_stitch/_design-system/DESIGN-CHAIN.md`, `tokens.md`, etc.). Real sources are `globals.css` + `designer-dashboard/SKILL.md` + golden components.
- **The generic `tailwind-design-system` skill** (oklch, dark mode, ref-as-prop) does **not** describe this repo — don't mine it for tokens.
- Raw Tailwind palette colors (`gray-`/`blue-`) — seen in `onboarding/` and admin roster, that's drift; use semantic tokens.
- `ve-*`/`reader-*`/`lucid-*` tokens outside their scoped surfaces.

## Workflow checklist

1. Open `globals.css` `@theme`; pick semantic tokens (extend `@theme` if a color is missing — never inline hex).
2. Compose from `ui/*` primitives; mirror `content/page.tsx` + `ContentItemCard`.
3. Serif `text-tertiary-container` titles, display uppercase eyebrows, Inter body.
4. Separate regions by surface tier, not borders (No-Line rule); navy-tinted ambient shadows + border-tint hover.
5. Use `StatusChip` for state; `transition-colors`/`animate-pulse` for motion (no framer-motion).
6. Verify: no raw hex/palette colors, no scoped `ve-*`/`reader-*` tokens, no copying the broken `eyebrow.tsx`/`prose.tsx` vocabulary, no aspirational audit-skill ceilings.
