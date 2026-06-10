---
name: oatmeal-editorial-ui
description: >
  Front-end UI design expert for the movemental-html-template "Oatmeal" static
  marketing template. Use when building or restyling any HTML page, hero,
  section, card, nav, CTA band, or footer to match the existing visual language.
  Anchors to css/tokens.css (the token SSOT), css/components.css (ml-* primitives),
  the design-chain/design-chain.html charter, and _reference/style-spec.json.
  Keywords: oatmeal, cream paper, Playfair Display, Inter, pill CTA, surface
  tiers, hairlines, terminal period, ml- components, design chain, static HTML,
  reveal-on-scroll, data-theme oatmeal.
---

# Oatmeal Editorial UI (movemental-html-template)

Use this skill whenever you create or restyle pages in this static template.
You are working inside a documented "design chain" — match it faithfully and
never hardcode values.

## North Star

A **premium editorial marketing site** — warm cream paper, high-contrast serif
display, disciplined Inter UI chrome, and hierarchy built from **size and spacing
rather than loud color**. Depth comes from **surface tiers, not shadows**;
structure comes from **warm hairlines**, not boxes.

## Stack

**Static, framework-free, no build step.** Plain HTML + hand-authored CSS + one
vanilla JS file. No Tailwind/Bootstrap/Vite. Deployed to Vercel (`/` →
`movemental-home.html`).

**The design chain — load order is load-bearing.** Every marketing page is
`<html lang="en" class="oat-page" data-theme="oatmeal">` and loads, in order:

```html
<!-- Google Fonts: Playfair Display + Inter + Homemade Apple + IBM Plex Mono -->
<link rel="stylesheet" href="css/tokens.css" />      <!-- L1: tokens — the ONLY file with raw hex -->
<link rel="stylesheet" href="css/base.css" />        <!-- L2: reset, body type, .container, reduced-motion -->
<link rel="stylesheet" href="css/components.css" />  <!-- L3: ml-* primitives -->
<link rel="stylesheet" href="css/pages.css" />       <!-- L4–5: page namespaces home-*/mh-*/sf-*/pw-*/mp-*… -->
<script src="js/main.js" defer></script>             <!-- L6: nav, sticky, reveal, mega-menu -->
```

**Chain rule:** changes flow downward only. Never retrofit a one-off hex from a
page back into a token; never hardcode a color/size — always `var(--…)`.

## Source of truth (read these, in order)

1. `css/tokens.css` — **the token SSOT** (the only file with raw hex).
2. `css/components.css` — the `ml-*` primitive vocabulary.
3. `design-chain/design-chain.html` — the living style guide / charter (north star + 7 principles + live swatches & demos).
4. `_reference/style-spec.json` (+ `.md`) — machine-readable token/style twin, ideal for programmatic reference.
5. `_reference/PAGE-MANIFEST.md` — which pages are canonical (R0/R1) vs exemplar/draft.
6. Golden pages: `movemental-home.html`, `movemental-pricing.html`, `pathway-safety.html`, `field-guide-safety.html`.

## Color — tokens only (`css/tokens.css`)

Never hardcode hex in markup or page CSS — consume `var(--color-*)`.

| Token | Value | Role |
|---|---|---|
| `--color-bg` | `#FBFAF6` | Warm oatmeal page background |
| `--color-surface` | `#F8F6F1` | Tinted card/panel surface |
| `--color-surface-elevated` | `#FFFFFF` | White inner card layer |
| `--color-ink` | `#1A1A1A` | Primary text / near-black CTA fill |
| `--color-ink-muted` | `#5C5651` | Secondary text, captions, meta |
| `--color-accent` | `#1A1A1A` | Primary CTA fill (= ink) |
| `--color-accent-hover` | `#12356E` | Button hover (navy) |
| `--color-hero-dark` | `#0A0E1A` | Navy hero band |
| `--color-border` | `#E5DFD2` | Warm-tan hairline rules/dividers |
| `--color-on-hero` | cream `#E8ECF5` @ .78 | Text on dark hero (alpha ramp `-muted/-subtle/-faint…`) |

Audience accents `--color-blue/-deep/-soft`; status `--color-rating-yes/-partial/-no`.
Highlighter / blue-ballpoint / AI-dock tokens are **Paper Edition only**
(`data-theme="paper"`), not standard oatmeal chrome. Temperature warm, saturation muted.

## Typography

- **Display:** Playfair Display → `--font-display` — headlines, wordmarks, section titles, stat numerals, large quotes.
- **Body/UI:** Inter → `--font-body` — nav, eyebrows, meta, footer, buttons.
- **Hand:** Homemade Apple → `--font-hand` (Paper Edition marginalia only).
- **Mono:** IBM Plex Mono → `--font-mono` (Paper Edition only).

Defaults (`base.css`): all `h1–h6` → Playfair, weight 400, `--lh-tight` (1.05),
`--tr-tight` (-0.025em); body → Inter 400 / 16px / `--lh-normal` (1.5). Hero
headlines `clamp(2.5rem, 7vw, 5.25rem)`. Type scale `--fs-xs…--fs-6xl` (16px base).
Eyebrows: ALL-CAPS, tracked `--tr-eyebrow` (0.18em).

**Signature tic:** display headlines often end with a **terminal period**
("Is this for you?", "Pricing."). Headlines are sentence-case; ALL-CAPS only for
tiny tracked eyebrow chips and meta.

## Spacing, layout, radius, elevation, motion

- **Spacing:** 4pt grid, `--space-1`…`--space-32`. Section rhythm `.ml-section { padding-block: var(--space-20) }` (5rem).
- **Container:** `.container` = `max-width: 72rem`, centered, `padding-inline: clamp(1rem, 4vw, 3rem)`. Narrow 42rem / default 64rem / wide 72rem.
- **Grid:** strict CSS Grid (3-col content, 4-col persona, `1fr 2fr` footer, `3fr 9fr` kicker splits). Primary desktop→stack breakpoint **860px** (also 980/720/600/560/520/640).
- **Radius:** `--radius-chip 8px`, `--radius-input 12px`, `--radius-card / --radius-image 20px`, `--radius-pill 999px`. Buttons/inputs are pills; cards/images 20px.
- **Elevation — essentially no shadows by design.** Depth = surface tiers (`bg` → `surface` → `surface-elevated`). Cards lift on hover via `transform: translateY(-2px)` + border-tone shift, never box-shadow. (Only deliberate exceptions: the handbook book-cover and Paper Edition sheets.)
- **Hairlines:** section breaks are `1px solid var(--color-border)` (warm tan), never gray.
- **Motion:** no libraries. Transition tokens `--t-fast/-med/-slow` + `--ease`. `.reveal → .is-revealed` via IntersectionObserver (opacity + `translateY(12px)→0`); hero children stagger 0/80/160/240/320ms. Reduced motion fully honored (`base.css` + `main.js`).

## Component patterns — compose `ml-*` (and page namespaces)

Build from `css/components.css` primitives; never reinvent in inline styles.

- **Button** — `<a class="ml-button ml-button-primary">Label →</a>` (also `-secondary`, `-ghost`). Pill, near-black `--color-accent` fill / `--color-bg` text, hover → navy `--color-accent-hover` + `translateY(-1px)`; inverts to cream on dark bands.
- **Nav** — `<header class="ml-nav" data-sticky="true">` → `.container.ml-nav-inner` with `.ml-nav-logo` (Playfair wordmark), `.ml-nav-toggle` (pill, ≤860px), `.ml-nav-links`. Bottom hairline appears on scroll (`.is-scrolled`).
- **Hero** — `.ml-hero` with variants `--bleed-overlay` / `--editorial-stack` / `--compact` / `--text-only`. **One hero drama per page** (usually a navy `--color-hero-dark` band).
- **Section header** — `.ml-section-header` (`--left`) → `.ml-section-eyebrow` (uppercase) + `.ml-section-title` (Playfair, terminal period) + `.ml-section-desc`.
- **Card** — `<a class="ml-card ml-card--library">` → `.ml-card-media` + `.ml-card-body` (`.ml-card-meta` eyebrow, `.ml-card-title`, `.ml-card-desc`). `surface-elevated` fill, `1px solid var(--color-border)`, 20px radius, hover `translateY(-2px)`. Variants `--persona/--portal/--library/--article/--featured-article`.
- **Dark CTA band** — `.mh-cta-band` on `--color-hero-dark`: centered Playfair title, cream lede, inverted CTAs.
- **Footer** — `.ml-footer` (`1fr 2fr` brand/cols, tracked-uppercase column headings, `©` + `data-year`, legal nav, the `.ml-footer-chain` "Design chain" link on every page).
- Other primitives: `.ml-quote`, `.ml-filter-chip`, `.ml-endorsements` (grayscale logo strip), `.ml-stats`/`.ml-stat-number`, `.ml-qa` (native `<details>`, `+`→`×`).
- Page-specific composition lives in `pages.css` namespaces: `home-*`/`mh-*` (home), `sf-*`/`fg-*`/`ss-*`/`flr-*` (safety flow), `pw-*` (pathway), `mp-*` (pricing), `sf-midnight` (dark inner hero), `sf-prose` (editorial prose).

## The 7 charter principles (always)

1. Surface tiers, not shadows. 2. Typography is the hierarchy (+ optional terminal
period). 3. Pill CTAs, black fill, invert on dark. 4. One hero drama per page.
5. Framed imagery, 16–20px radius. 6. Hairline structure (`1px var(--color-border)`).
7. Movement-leader semantics.

## Avoid (drift — do not copy)

- **`index.html`, `library.html`, `articles.html`** — the Alan-Hirsch leader exemplar (Tier R3, "never Movemental marketing patterns"). Different semantics; not canonical Movemental pages.
- **`movemental-paper-draft-v1.html`** — local-only draft with off-palette hex (`--coffee` etc.) and 26 inline styles. Ignore entirely.
- **`site-map.html`** — internal tooling with its own inline `<style>` and off-palette tints. Not a style reference.
- **Heavy inline `style=` bodies** on some pathway/audience pages — treat as drift to migrate, prefer namespaced classes.
- Highlighter / blue-ballpoint / marginalia vocabulary outside `data-theme="paper"`.
- Gray dividers (use warm `--color-border`), box-shadows for depth (use surface tiers), and any hardcoded hex in page CSS/markup (resolve through tokens).

## Workflow checklist

1. Start every page as `class="oat-page" data-theme="oatmeal"` loading the 4 CSS + JS in order.
2. Compose only `ml-*` / page-namespace classes; **never** hardcode hex — use `var(--color-*)`.
3. Playfair display headlines (sentence case, optional terminal period) + Inter UI; eyebrows ALL-CAPS tracked.
4. Black pill CTAs that invert on navy bands; one hero drama per page; framed 20px imagery.
5. Separate regions with warm hairlines + surface tiers; depth via `translateY(-2px)` hover, not shadow.
6. 4pt spacing, 72rem `.container`, 860px primary breakpoint; `--t-*` transitions + `.reveal`.
7. Verify against `design-chain/design-chain.html` and `_reference/style-spec.json`; avoid the §drift pages.
