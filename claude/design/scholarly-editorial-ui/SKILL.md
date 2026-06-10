---
name: scholarly-editorial-ui
description: >
  Front-end UI design expert for the alan-hirsch app's "Scholarly Editorial /
  Plum & Parchment" design system. Use when building or restyling any page,
  section, hero, card, nav, or component in this repo — to match the existing
  visual language. Anchors to src/app/globals.css tokens, tailwind.config.ts,
  and _docs/_build/design/SCHOLARLY_EDITORIAL.md. Keywords: plum, parchment,
  Newsreader, Manrope, scholarly, editorial, tonal surfaces, no-line rule,
  shadcn, Radix, motion/react, design tokens, theming.
---

# Scholarly Editorial UI (alan-hirsch)

Use this skill whenever you create or restyle front-end UI in this repo. You are
designing inside an **established, documented** design system — your job is
fidelity to it, not invention. Match the evidenced style; never introduce a new
look.

## North Star

**"The Modern Archivist" — a digital monograph.** Authoritative, curated,
intellectually warm. The palette is **Plum & Parchment**: plum is the *ink*,
parchment is the *paper*. Hierarchy comes from **intentional asymmetry** and
**tonal depth** (layered paper surfaces), not from boxes, borders, or loud color.

## Source of truth (read these, in order)

1. `src/app/globals.css` — **all design tokens** (HSL CSS vars) + the canonical
   utility-class API (`.typo-*`, `.btn-primary-gradient`, `.scholarly-glass`,
   `.signature-label`, `.ghost-border`, `.tonal-lift`, `.content-prose`).
2. `tailwind.config.ts` — token→utility mapping, type scale, radius, glow shadows, motion.
3. `_docs/_build/design/SCHOLARLY_EDITORIAL.md` — the written spec (palette, No-Line rule, elevation, do/don'ts).
4. Golden components: `src/components/pathways.tsx`, `src/components/navigation/PublicHeader.tsx`, `src/app/layout.tsx`.

> ⚠️ **Ignore the stale "Pastoral-Warm" docs.** `DESIGN_CHARTER.md`,
> `DESIGN_CHAIN.md`, design-folder `README.md`, `HERO_SECTION_GUIDELINES.md`, and
> their `layers/D0–D6` derivatives describe an **abandoned** theme (Amethyst/gold
> `#9460B8`/`#7A3596`, Montserrat + Inter, `--radius: 10px`). None of those values
> exist in `src/`. They are traps. The truth is `globals.css` + `SCHOLARLY_EDITORIAL.md`.

## Stack

Next.js 15 App Router (RSC) · Tailwind **v3.4** (JS config, HSL vars — *not* v4/OKLCH/`@theme`) ·
shadcn/ui "new-york" over Radix · `cn()` from `src/lib/utils.ts` · icons **only** via `<Icon>` from `@/components/ui/icon` (never import Lucide directly).

## Color — semantic tokens only (zero inline hex)

Use Tailwind semantic classes that resolve to `hsl(var(--x))`. Light theme:

| Role | Token / class | Value |
|---|---|---|
| Parchment canvas | `bg-background` | `#fbf9f4` |
| Ink (never pure black) | `text-foreground` | `#1b1c19` |
| Plum ink / primary | `bg-primary` / `text-primary` | `#37203b` |
| Deep plum container | `bg-accent` / `bg-primary-container` | `#4e3652` |
| Muted paper | `bg-muted` | `#ebe8e3` |
| Featured card fill | `bg-primary-fixed` | `#fad8fc` |
| Ghost border | `outline-variant` | `#cec3cc` |

**Tonal surface ladder** (use these to separate regions instead of borders):
`surface-bright` (#fefcf8, nav) → `surface` (#fbf9f4) → `surface-container-low`
(#f5f3ee) → `surface-container` (#f0eee9) → `surface-container-high` (#ebe8e3) →
`surface-container-highest` (#e4e2dd). Dark theme inverts the same ladder (`.dark`).

**Rules:** Never `text-black`/`bg-black`/raw hex in TSX. Don't saturate the
background with plum ("purple is the ink, not the paper"). Color is essentially a
plum-on-parchment duotone with restrained accents.

## Typography

- **Headings:** Newsreader (serif) → `font-heading` (dominant) or `font-serif` (both map to Newsreader). Loaded via next/font in `src/app/layout.tsx`.
- **Body/UI:** Manrope (sans) → `font-body` / default sans.
- **Mono:** JetBrains Mono → `font-mono`.
- **Canonical type API:** the `.typo-*` utility classes (`.typo-display`,
  `.typo-h1…h4`, `.typo-body`, `.typo-body-lg`, `.typo-small`, `.typo-label`).
  Prefer these over ad-hoc `text-[..]`. `.signature-label` = ALL-CAPS Manrope, 0.05em tracking, for eyebrows.
- Headings are tight (`line-height ~1.1`, `-0.02em` tracking) and use weight 700–800; body `line-height 1.65`. Never pure-black ink.

## Spacing, radius, elevation, motion

- **Radius:** `--radius: 0.5rem` (`rounded-lg`); buttons are pills (`rounded-full` / `rounded-button`); cards often `rounded-xl`. No hard 90° corners.
- **Layout:** sections `container mx-auto px-4 md:px-8`, vertical rhythm `py-16 md:py-24`; nav/content `max-w-7xl mx-auto`; reading column `max-w-measure` (~65ch). `.editorial-layout` for intentional asymmetry.
- **The No-Line rule:** **do not** use 1px solid borders or `<hr>` to separate
  sections. Transition between tonal surfaces (`surface` → `surface-container-low`) instead.
- **Elevation:** prefer plum-tinted ambient glow (`shadow-primary-glow`,
  `shadow-primary-glow-md/-lg`) and `.tonal-lift` over hard drop shadows. Avoid
  pure-black `rgba(0,0,0,…)` shadows. "If you can clearly see where the shadow ends, it's too dark."
- **Motion:** `motion/react` (the renamed framer-motion). Entrance pattern:
  `initial={{opacity:0,y:20}}` → `whileInView={{opacity:1,y:0}}`,
  `viewport={{once:true,margin:'-50px'}}`, stagger `delay: index*0.1`. CSS helpers
  `.fade-up`/`.card-hover`. Always honor `prefers-reduced-motion` (globals already zeroes durations).

## Component patterns

- Compose **shadcn primitives** from `src/components/ui/*` — **never edit them for
  styling**. Add tokens in `globals.css`/`tailwind.config.ts` or apply class
  overrides via `cn()`. (The bare shadcn defaults — `rounded-md` buttons,
  `rounded-xl` cards — are not themselves "the brand"; the editorial flavor lives
  in tokens + the `globals.css` utility classes.)
- **Card** (`pathways.tsx`): `group relative flex h-full flex-col rounded-xl
  overflow-hidden bg-card shadow-md hover:shadow-xl transition-all duration-300`,
  image top with `bg-gradient-to-t from-background/95 via-background/60 to-transparent`,
  `font-serif text-2xl` title, arrow reveal on hover.
- **Nav** (`PublicHeader.tsx`): `fixed` header gaining `glass-panel border-b
  border-border` when scrolled; links `font-bold uppercase tracking-widest
  hover:text-primary`, active in `text-primary` with an animated `bg-primary`
  underline (`w-0 group-hover:w-1/2`, `active ? w-full`).
- Layering discipline: **Tokens → Tailwind → Radix/shadcn → Domain components → Patterns → Pages**.

## Avoid (drift — do not copy)

- The Pastoral-Warm/Amethyst/Montserrat docs (see warning above).
- `src/components/_archive/*` (deprecated: footer.tsx, navbar.tsx, home-v2, simplified, scholar-profile-v2).
- Heavy `shadow-xl`/`shadow-2xl` and pure-black shadows — real drift vs. the plum-glow/tonal intent.
- `docs/html/*`, `public/html/*` — unrelated scraped vendor CSS.
- The generic `tailwind-design-system` skill (it targets Tailwind v4 / OKLCH / `@theme` — wrong for this v3 + HSL repo).
- Inline hex anywhere in `src/components` (verified clean — keep it that way).

## Workflow checklist

1. Identify the surface tier and tokens before writing markup.
2. Compose from `ui/*` primitives + `.typo-*`/utility classes; add overrides via `cn()`.
3. Separate regions with tonal surfaces, not lines.
4. Use plum-glow / tonal-lift elevation; pill buttons; 0.5rem corners.
5. Newsreader headings, Manrope body; icons via `<Icon>`.
6. Add `motion/react` entrance with reduced-motion respected.
7. Verify: no raw hex, no `_archive` imports, no stale-doc tokens, no 1px section dividers.
