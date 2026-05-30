# File organization — output template

## Directory layout

```
1-html/by-template-family/ml-templates/{slug}/
  _reference/
    {original-image-1}.{ext}        # copied from source, basename preserved
    {original-image-2}.{ext}        # if multiple references
    style-spec.md                   # extracted spec, human-readable
    style-spec.json                 # extracted spec, machine-readable
    NOTES.md                        # provenance, deviations, source URLs
  index.html
  library.html
  articles.html
  css/
    tokens.css                      # design tokens (CSS variables)
    base.css                        # reset, body typography, utilities
    components.css                  # nav, hero, cards, buttons, footer
    pages.css                       # home/library/articles composition
  js/
    main.js                         # nav toggle, sticky behavior, reveals
  images/
    hero-placeholder.webp           # or .jpg / .png matching the reference's format
    cover-placeholder-1.webp
    cover-placeholder-2.webp
    cover-placeholder-3.webp
    cover-placeholder-book.webp
```

## HTML conventions

Every page:

- `<!DOCTYPE html>` + `<html lang="en">`.
- Identical `<head>`:
  - `<meta charset="UTF-8">`
  - `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
  - `<title>{Page name} — {Leader Name}</title>` (page-specific title, leader stays the same)
  - Google Fonts preconnect + the single Google Fonts `<link>` for the families chosen in the style spec (no extras)
  - CSS load order: `tokens.css` → `base.css` → `components.css` → `pages.css`
  - `<script src="js/main.js" defer></script>`
- Identical `<header class="ml-nav">` markup at the top of `<body>`, with `aria-current="page"` set on the matching nav link.
- One `<main>` element per page.
- Identical `<footer class="ml-footer">` markup at the bottom of `<body>`.
- Section IDs match the spec (`personas`, `exploration`, `pathway`, `featured-book`, `latest-articles`, `newsletter`) so jump links from nav or hero CTAs resolve.

## CSS conventions

### `tokens.css` — extracted from the style spec

```css
:root {
  /* Color */
  --color-bg: #...;
  --color-surface: #...;
  --color-surface-elevated: #...;     /* omit if reference doesn't use elevation */
  --color-ink: #...;
  --color-ink-muted: #...;
  --color-accent: #...;
  --color-accent-2: #...;             /* omit if reference uses one accent */
  --color-border: #...;

  /* Typography */
  --font-display: '<chosen display>', '<fallback>', serif;
  --font-body:    '<chosen body>',    '<fallback>', sans-serif;
  --font-weight-display: 600;          /* whatever the reference shows */
  --font-weight-body: 400;
  --font-weight-body-strong: 600;

  /* Type scale (modular, anchored to reference's apparent base size) */
  --fs-xs:   0.75rem;
  --fs-sm:   0.875rem;
  --fs-base: 1rem;
  --fs-lg:   1.125rem;
  --fs-xl:   1.25rem;
  --fs-2xl:  1.5rem;
  --fs-3xl:  1.875rem;
  --fs-4xl:  2.5rem;
  --fs-5xl:  3.5rem;

  /* Line heights */
  --lh-tight:  1.1;
  --lh-snug:   1.3;
  --lh-normal: 1.5;
  --lh-loose:  1.7;

  /* Spacing — 8pt or 4pt depending on the reference's density */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-24: 6rem;

  /* Radius */
  --radius-sm:   2px;
  --radius-md:   6px;
  --radius-lg:   12px;
  --radius-pill: 999px;

  /* Shadow */
  --shadow-soft:    0 1px 2px rgba(0,0,0,0.04), 0 2px 8px rgba(0,0,0,0.06);
  --shadow-hard:    0 4px 0 rgba(0,0,0,1);     /* brutalist offset shadow only */
  --shadow-layered: 0 10px 30px rgba(0,0,0,0.08);

  /* Containers */
  --container-narrow:  42rem;
  --container-default: 64rem;
  --container-wide:    80rem;
}
```

Pare down whatever the reference doesn't actually use. If the reference uses one accent, ship one `--color-accent`. If there are no visible shadows, ship only `--shadow-soft` or omit shadows entirely. The token file is a **honest** capture of the reference, not a maximal palette.

### `base.css`

- Box-sizing reset (`*, *::before, *::after { box-sizing: border-box; }`).
- `body { font-family: var(--font-body); color: var(--color-ink); background: var(--color-bg); line-height: var(--lh-normal); }`.
- Heading defaults using `var(--font-display)`.
- `.visually-hidden` utility.
- `:focus-visible` ring at `2px solid var(--color-accent)` with `outline-offset: 2px`.
- Image defaults: `max-width: 100%; height: auto; display: block;`.
- Anchor defaults — color, hover treatment.
- `prefers-reduced-motion` block disables animations.

### `components.css` — class-name contract

The scaffold **must** produce these class names (downstream skills depend on them):

```
.ml-nav, .ml-nav-logo, .ml-nav-links, .ml-nav-actions, .ml-nav-toggle, .ml-nav-link-ghost
  + .ml-nav[data-sticky], .ml-nav.is-scrolled, .ml-nav-links a[aria-current="page"]

.ml-hero, .ml-hero-media, .ml-hero-inner,
.ml-hero-eyebrow, .ml-hero-title, .ml-hero-tagline, .ml-hero-ctas
  + variants: .ml-hero--bleed-overlay, .ml-hero--split, .ml-hero--portrait-dominant,
              .ml-hero--art-bg-portrait-fg, .ml-hero--text-only, .ml-hero--editorial-stack,
              .ml-hero--compact

.ml-button, .ml-button-primary, .ml-button-secondary, .ml-button-ghost

.ml-card, .ml-card-media, .ml-card-body, .ml-card-meta, .ml-card-title, .ml-card-desc,
.ml-card-byline, .ml-card-cta, .ml-card-icon
  + variants: .ml-card--persona, .ml-card--portal, .ml-card--article,
              .ml-card--library, .ml-card--featured, .ml-card--featured-article

.ml-section, .ml-section-title, .ml-section-desc, .ml-section-header, .ml-section-more

.ml-quote, .ml-quote-text, .ml-quote-cite

.ml-filter-chips, .ml-filter-chips--topics, .ml-filter-chip, .ml-filter-chip.is-active

.ml-footer, .ml-footer-inner, .ml-footer-brand, .ml-footer-wordmark, .ml-footer-tagline,
.ml-footer-cols, .ml-footer-col, .ml-footer-bottom
```

This contract is what makes templates feel like a family across leaders. A downstream auditor or refactor should never have to guess class names.

### `pages.css`

Page-specific composition only. Reuse `.ml-card`, `.ml-section`, etc. from components. Define grid layouts:

```
.home-personas-grid, .home-portals-grid, .home-featured-book,
.home-pathway, .home-articles-strip, .home-newsletter-form

.library-grid, .library-featured, .library-featured-rail,
.library-pagination, .library-loadmore, .library-search

.articles-page, .articles-body, .articles-featured, .articles-grid,
.articles-sidebar, .articles-sidebar-block, .articles-sidebar-list
```

Page-specific styles never redefine `.ml-*` components — they only compose layouts around them.

## JS conventions

`js/main.js` only — no frameworks, no bundler, no build step. Handles:

1. **Mobile nav toggle** — `aria-expanded` flip + `.is-open` class on drawer.
2. **Sticky nav scroll state** — `.is-scrolled` toggle when `window.scrollY > 8`.
3. **Filter chips** — wire `.ml-filter-chip` clicks to toggle `[data-type]` / `[data-topic]` visibility on cards (only if the style spec's motion is ≥ `moderate`; otherwise leave chips visual-only).
4. **Reveal animations** — if motion is `moderate` or `rich`, use `IntersectionObserver` to add `.is-revealed` to `.ml-section` and `.ml-card` as they enter the viewport.

Wrap everything in an IIFE or use module syntax with `defer`. No globals.

```js
(() => {
  // 1. Mobile nav
  // 2. Sticky scroll
  // 3. Filter chips (conditional)
  // 4. Reveal observer (conditional)
})();
```

## Image placeholders

For the initial template, place placeholder images at these aspect ratios:

| Filename | Dimensions | Purpose |
|----------|-----------|---------|
| `hero-placeholder.{ext}` | 2400×1350 (16:9) — full-bleed; 1600×1200 (4:3) — split; 1200×1600 (3:4) — portrait-dominant | Home hero |
| `cover-placeholder-1.{ext}` | 1200×800 (3:2) | Theme portal / featured card |
| `cover-placeholder-2.{ext}` | 1200×800 (3:2) | Article card |
| `cover-placeholder-3.{ext}` | 1200×800 (3:2) | Theme portal |
| `cover-placeholder-book.{ext}` | 800×1200 (2:3) | Book cover |

A solid-color placeholder matching the reference's `--color-surface` is acceptable. Each placeholder is documented in `_reference/NOTES.md` so the next pass (`/asset-generate`, `/asset-series`) can replace them with generated art.

Image format follows the reference's apparent format — `.webp` for modern web references, `.jpg` for editorial references, `.png` for brutalist / flat-graphic references.

## Page `<title>` convention

```
{Page} — {Leader Name}
```

- `index.html` → `{Leader Name}` (no "Home —" prefix — the leader's name is the page)
- `library.html` → `Library — {Leader Name}`
- `articles.html` → `Articles — {Leader Name}`
