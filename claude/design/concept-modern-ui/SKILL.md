---
name: concept-modern-ui
description: >
  Front-end UI design expert for movemental-ai's "Concept Modern" (warm
  editorial) design system. Use when building or restyling any marketing page,
  section, hero, card, nav, or component to match the existing visual language.
  Anchors to src/app/globals.css tokens, tailwind.config.ts, the editorial
  primitives in src/components/primitives/, and docs/design/DESIGN.md +
  MOTION.md + PATTERNS.md. Keywords: Concept Modern, cream paper, ink, duotone,
  Inter, Newsreader italic emphasis, pill CTA, hairlines, ghost-lift, Midnight
  bands, Section, Container, Display, Eyebrow, Reveal, Tailwind v4, shadcn.
---

# Concept Modern UI (movemental-ai)

Use this skill whenever you build or restyle front-end UI in this repo. You are
designing inside a richly documented, intentional system — match it faithfully.

## North Star

**Concept Modern — warm editorial.** *"Typography is the interface."* A
near-**duotone**: warm cream paper + near-black ink. Hierarchy comes from type
scale, tracking, italic-serif emphasis, hairlines, and **tonal "ghost-lift"
stacking** — never from drop shadows or decorative borders. **Midnight** bands
(`#141110`) mark authority moments.

## CRITICAL: scope to `src/`

There are **decoy duplicate trees**. Only `src/` is live (confirmed by
`tsconfig` `@/* → ./src/*`, `components.json`, tailwind globs).
- **Canonical:** `src/app/`, `src/components/`, `src/app/globals.css`.
- **IGNORE:** root `/app/`, root `/components/`, root `/app/globals.css` (stale HSL
  "Digital Curator" tokens like `--primary: 359 59% 50%`, scarlet/velvet-orchid).
- `docs/ai-studio/` is a separate sub-app.

## Source of truth (read these, in order)

1. `src/app/globals.css` — **token SSOT** (`@theme inline` + `:root`/`.dark` hex).
2. `docs/design/DESIGN.md` (master charter) + `MOTION.md` + `PATTERNS.md`.
3. `tailwind.config.ts` — fonts, fluid type scale, radii, motion, shadows.
   Header note: *"DESIGN.md is canonical — when this file and DESIGN.md disagree, DESIGN.md wins."*
4. Golden: `src/components/primitives/*`, `src/components/ui/button.tsx`, `src/app/(dashboard)/admin/design-tokens/page.tsx` (live token swatches).

> ⚠️ `CLAUDE.md`'s design section is **stale** (describes "Digital Curator",
> `#0053db` blue primary). Defer to `DESIGN.md`. Also: DESIGN.md says "Instrument
> Serif" but the **code loads Newsreader** — trust the code.

## Stack

Next.js 16 App Router (RSC) · React 19 · Tailwind **v4** (CSS-first `@theme`, no
HSL) · shadcn "radix-nova" over Radix · `cn()` from `src/lib/utils.ts` · Lucide icons.

## Color — semantic tokens only (raw hex in `:root` only)

Primary is **ink, not a brand color.** Use utilities, never raw hex/`bg-white`/`bg-black`/`bg-blue-600`.

| Role | Utility | Light hex |
|---|---|---|
| Paper base | `bg-background` | `#faf6ee` |
| Alt band / muted | `bg-section` / `bg-muted` | `#f2ece0` |
| Card | `bg-card` | `#ffffff` |
| Deepest paper / accent | `bg-surface-highest` / `bg-accent` | `#efe7d6` |
| Primary ink | `text-foreground` / `bg-primary` | `#19150f` |
| Primary dim (hover) | `bg-primary-dim` | `#000000` |
| Secondary ink | `text-muted-foreground` | `#6b6660` |
| Meta ink | `text-ink-soft` | `#7e786f` |
| Hairline | `border-border` | `#e6ddcb` |
| 0.5px rule | `border-rule` | `rgba(25,21,15,.14)` |
| **Midnight surface** | `bg-inverse-surface` | `#141110` |
| **On Midnight** | `text-inverse-foreground` | `#f4efe5` |

Dark theme (`.dark`) inverts the ramp; the pill stays the brightest object (cream).
Status signals `status-go/caution/stop`, `pathway-accent` (#b8893a), citation
"Ledger" amber, and `safestart-*`/`sandbox-*`/`movemental-midnight` tokens are
**scoped** — the last group is for authenticated `/safestart`, `/sandboxlive`,
`/program` shells **only**, never marketing pages.

## Typography

- **Body/UI:** Inter → `font-sans` (weights 400/500).
- **Display + emphasis:** Newsreader (italic) → `font-serif`/`font-serif-display`/`font-headline`.
- **Headings use weight 500** — hierarchy via fluid scale + tracking, not heft.
- **Italic emphasis convention:** wrap stressed words in `<em>` *inside* a heading;
  the base layer auto-swaps to italic serif (weight 400, optical size bump). Don't
  hand-apply `font-serif italic` to whole headings; never use serif for multi-paragraph body.
- Type scale (fluid `clamp`, `tailwind.config.ts`): `display`, `h1…h4`, `body`
  (1.0625rem/1.55), `body-lg`, `small`, `label` (uppercase eyebrow, `tracking-eyebrow` 0.09em), `button`, `micro`.
- Base body 17px, `lh 1.55`, `font-feature-settings: "kern","liga","cv11"`.

## Spacing, radius, elevation, motion

- **Containers:** `--container-max 1200px`, `--container-narrow 740px`, `--prose-max 640px` — use the `Container` primitive (`max-w-(--container-*)`).
- **Section rhythm:** `--section-y-sm clamp(3rem,6vw,4.5rem)` default; `--section-y-lg clamp(5rem,10vw,8rem)` heroes/landmarks. Use the `Section` primitive.
- **Radius:** base `0.625rem`; `rounded-card` (14px) for cards/dialogs/hero images; **`rounded-pill` for ALL buttons/CTAs**.
- **Elevation:** minimal by doctrine. Only `shadow-ambient` (`0 24px 80px rgba(25,21,15,.12)`, dialogs), `shadow-hero-image`, `shadow-nav-scroll`. **No** arbitrary `shadow-md/lg`. Replace shadows with hairlines + tonal stacking.
- **Motion ("Calm Confidence"):** mostly CSS, not JS. Use the `<Reveal>` primitive
  (IntersectionObserver, fires once, full reduced-motion bail-out, optional 80ms
  stagger). Amplitude caps: reveal translateY ≤20px, card lift ≤-2px, hover scale
  ≤1.02. **Non-goals:** no parallax, particles, carousels, page-transition or 3D.
  `motion` v12 (`motion/react`) exists for bespoke cases; gsap only for `fragmentation-story`.

## Component patterns — compose the primitives

Build pages by composing **editorial primitives** (`src/components/primitives/`),
not raw divs: `Section` → `Container` → `Display`/`Eyebrow`/`Prose` +
`SurfaceCard`, `FeatureSplit`, `StatStrip`, `ArrowLink`, `PullQuote`,
`TestimonialRail`, `Timeline`, `LogoStrip`, `Reveal`.

- **Button** (`ui/button.tsx`, CVA): `default` = `rounded-pill bg-primary
  text-primary-foreground hover:-translate-y-px hover:bg-primary-dim`; `ghost` =
  pill + `border-border hover:border-foreground`; `primary-inverse` for Midnight
  bands. Arrow icons: `hover:[&_svg.arrow]:translate-x-[3px]`. Focus ring always.
- **Section**: variants → `bg-background|bg-section|bg-elevated|bg-inverse-surface`; Midnight sets `data-variant="midnight"`.
- **SurfaceCard**: tones `on-background` / `on-section` (`shadow-ambient`) / `midnight`; base `flex flex-col gap-3 rounded-xl p-6 sm:p-8`.
- **Display**: `font-sans font-medium tracking-display text-balance`.
- **Eyebrow**: `text-[0.78rem] font-medium uppercase tracking-eyebrow text-muted-foreground` + optional ink dot.
- For static-derived / studio components, the CSS-recipe `.btn-pill`/`.btn-pill--primary` in `recipes.css` is a legitimate mirror of `Button`.

## Avoid (drift — do not copy)

- The decoy `/app` & `/components` trees and stale `app/globals.css` HSL tokens; blue `#0053db` primary; the stale `CLAUDE.md` design section.
- "Instrument Serif" references (code uses Newsreader); the unused archived `editorial-stitch` palette (`_archive/2026-05-13/`).
- Raw hex / `bg-black` / `text-black` / `bg-blue-*` in TSX; decorative borders or `<hr>` between sections; new drop shadows beyond `shadow-ambient`.
- Arbitrary one-offs from `TopographicHero.tsx` (`text-[11px]`, direct `font-serif italic` h1) — prefer `Eyebrow`, `tracking-eyebrow`, `<em>` emphasis.
- `safestart-*`/`sandbox-*`/`pathway-accent` tokens on marketing routes.
- Shrinking type to fit, or hand-setting `class="dark"`.

## Workflow checklist

1. Confirm you're in `src/`; open `globals.css` + `DESIGN.md` for tokens/rules.
2. Compose `Section → Container → Display/Eyebrow/Prose/SurfaceCard/Button`.
3. Duotone palette via semantic tokens; ink-pill CTAs; weight-500 headings; `<em>` italic emphasis.
4. Separate regions with bands/hairlines + ghost-lift, not shadows/borders.
5. Wrap entrances in `<Reveal>`; respect amplitude caps + reduced motion.
6. Reach for Midnight bands for authority moments only.
7. Verify: no raw hex, no decoy-tree imports, no `bg-blue`, no shadow drift, no scoped product tokens on marketing.
