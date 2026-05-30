---
name: oatmeal-template-audit
description: Audit and refine an HTML page in `1-html/by-template-family/ml-templates/oatmeal/` against the canonical Oatmeal template fingerprint — tokens, primitives, components, layout vocabulary, decorative motifs. Use whenever a new page is built in the oatmeal directory, when a page is being refined for template fidelity, or when the user says "make this look like the oatmeal template," "audit this against oatmeal," "is this on-brand for oatmeal," or "apply oatmeal styling." Complements `movemental-page-auditor` (which judges narrative/proof) and `page-audit` (which judges DESIGN.md compliance) — this skill judges **template fidelity only**.
---

# Oatmeal template audit

A focused audit pass that confirms a single page is built from the Oatmeal template's design language as documented in `_reference/style-spec.md` and embodied in `css/tokens.css`, `css/base.css`, `css/components.css`, and the canonical demo pages `index.html` / `library.html` / `articles.html`.

This skill does **not** judge content quality, narrative sequencing, or proof burden — only whether the page reads as Oatmeal-native at a glance and uses the template's primitives correctly.

---

## When this skill triggers

- "Audit this page against oatmeal"
- "Make this match the oatmeal template"
- "Is this on-brand for oatmeal?"
- "Apply oatmeal tokens / primitives / components / layouts"
- "Run the oatmeal audit across these pages"
- A new page lands in `1-html/by-template-family/ml-templates/oatmeal/` and the user wants it brought to template fidelity
- Refining a movemental-specific page (sandbox/skills/solutions/pricing/etc.) that was built quickly and may have drifted

Do **not** trigger for:
- Content/copy review (use `movemental-page-auditor` or `alan-voice`)
- React-component design questions (use `design-audit`)
- Pages in other template families (`tides`, `terminal`, etc.)

---

## The Oatmeal fingerprint

A page is "Oatmeal-native" when, looked at from across the room, you'd recognize it. The fingerprint has six load-bearing traits:

### 1. Palette discipline
- **Cream `#EFEADC` is the dominant page surface.** ~70% of vertical pixels.
- **Dark olive `#2D3A2A` is reserved for two roles only:** the hero bleed-overlay and the bottom CTA "midnight" band. Using it anywhere else dilutes its signal.
- **`#F6F2E8` is the inset tint** for cards-on-cream and tinted bands.
- **`#FFFFFF` appears for white surfaces ONLY on tinted sections** (not on the main cream).
- **`#0E0E0E` near-black is the only ink color.** `#6B6358` for muted ink.

Tokens: `--color-bg`, `--color-hero-dark`, `--color-surface`, `--color-surface-elevated`, `--color-ink`, `--color-ink-muted`, `--color-border`. Do not introduce new color values; if you find a hex literal in HTML that is not one of these tokens, that's a deviation.

### 2. Typography rules
- **Display = Fraunces**, body = Inter, no third face.
- **Sentence case** for both display and body. ALL-CAPS only for tiny eyebrow chips and stat labels.
- **Display headlines tend to end with a terminal period.** This is the single most identifiable Oatmeal tic. (`Pricing.` not `Pricing`; `Customer support that feels like a conversation.`)
- **Italics are rare.** Use the italic Fraunces variant sparingly — for one or two highlighted words inside a headline, or for an editorial pull quote. Do not italicize whole paragraphs or routine emphasis.
- **Tracking:** display is tight (`-0.02em`); body is normal; eyebrows use `0.18em` letterspacing.

### 3. Layout & rhythm
- Single container, `max-width: 72rem` (`var(--container-wide)`).
- **Section pad-block = `var(--space-20)`** (canonical) or `var(--space-16)` for tighter bands.
- Section dividers are **hairlines** (`1px solid var(--color-border)`), not heavy borders.
- Three-up grids are the default for content blocks on desktop; collapse to one column under 860px.
- **Generous whitespace.** Stat cards and section headers expect room around them.

### 4. Component vocabulary
Pages should reuse these existing primitives before introducing new ones:

| Pattern | Class | When to use |
|---|---|---|
| Sticky nav | `.ml-nav[data-sticky="true"]` | Every page |
| Buttons | `.ml-button .ml-button-primary` / `-secondary` / `-ghost` | All CTAs — always pill, always one of three variants |
| Hero (centered) | `.ml-hero--editorial-stack` or `.ml-hero--text-only` | Most pages |
| Hero (dark) | `.ml-hero--bleed-overlay` | Home/index pages only |
| Section header (centered) | `.ml-section-header > .ml-section-eyebrow + .ml-section-title + .ml-section-desc` | Default section intro |
| Card | `.ml-card .ml-card--persona / --portal / --library / --article` | Content tiles |
| Quote | `.ml-quote .ml-quote-text + .ml-quote-cite` | Cream-on-cream testimonials |
| Stat | `.ml-stats .ml-stat-number + .ml-stat-label + .ml-stat-desc` | Numerical proof |
| Q&A | `.ml-qa .ml-qa-item` (HTML `<details>`) | FAQ blocks |
| Endorsements | `.ml-endorsements .ml-endorsements-grid` | Logo strip |
| Footer | `.ml-footer .ml-footer-inner` | Every page |

Movemental sub-language extensions (kept consistent across the family):

| Pattern | Class prefix | Pages it lives on |
|---|---|---|
| Movemental home | `mh-*` | `movemental-home.html` |
| Safety flow shared | `sf-*` | safety pages, pathway pages |
| Field guide | `fg-*` | `field-guide-*.html`, pathway field guide blocks |
| SafeStart | `ss-*` | `about-safestart.html` |
| Five-Layer Read | `flr-*` | `pathway-safety.html` |
| Pathway shared | `pw-*` | `pathway-sandbox.html`, `pathway-skills.html`, `pathway-solutions.html` |
| Pricing | `mp-*` | `movemental-pricing.html` |

Use the existing prefix that matches the page's role. **Do not introduce new namespaces** for one-off variations.

### 5. Decorative motifs (use)
- Terminal period on display headlines
- Hairline rules between major sections
- Small tracked uppercase eyebrows — short phrases ("Why this work", "Movement Voices", "Pricing"), never sectioned with `§ 01 ·` or similar manuscript decorators
- Stat callouts (big serif numeral + tiny uppercase label)
- Italic em on one or two words in a headline for emphasis
- Optional cream-on-cream pull quote (`.ml-quote`) for testimonials

### 6. Decorative motifs (avoid)
- `§ NN ·` section numbering in eyebrows
- Dark olive used for testimonials, callouts, or feature blocks — it's reserved for hero + bottom CTA band
- Italic body paragraphs (one or two words is OK; whole sentences is a code smell)
- Inline `style="color: #..."` overrides — use a class
- Drop shadows or elevations beyond `translateY(-2px)` on hover
- Aggressive borders (`2px`, dashed for primary structure, etc.) — hairlines or nothing
- Tier badges, "Most popular" stickers, urgency pills
- Color used for hierarchy (Oatmeal uses size + spacing contrast, not color contrast)

---

## How to run the audit

For each target page:

### Pass 1 — Tokens
Grep the HTML and any inline `<style>` for:
- Hex color literals (`#XXX` or `#XXXXXX`) that are not one of the canonical seven (`#EFEADC`, `#F6F2E8`, `#FFFFFF`, `#0E0E0E`, `#6B6358`, `#2D3A2A`, `#E6DFD0`). One exception: `#9C4A2D` clay accent and `#5A8F3A` green / `#BC8C2F` amber are already established in `pages.css` for flow markers (rating chips, audience marker) — these are allowed.
- Font-family declarations that aren't `var(--font-display)` or `var(--font-body)`.
- Spacing in `px` where a `--space-*` token exists.

Findings → list deviations as `[line:col] non-token color #X used in <selector>`.

### Pass 2 — Display headlines
Find every `<h1>`, `<h2>`, `<h3>` rendered in `var(--font-display)`:
- Does it end with a period? (Standard Oatmeal trait.)
- Is it sentence case (not Title Case)?
- Is italic em used at most on 1–2 words?
- Length under 12 words for hero, under 16 for section heads?

### Pass 3 — Eyebrows
Find every section eyebrow (typically `.ml-section-eyebrow`, `.pw-kicker-eyebrow`, `.pw-hero-eyebrow`, `.mp-section-eyebrow`, etc.):
- Is it a short phrase, not a manuscript-style `§ 01 · ...` marker?
- ALL-CAPS, `letter-spacing: var(--tr-eyebrow)`, `color: var(--color-ink-muted)`?

### Pass 4 — Components
- Every CTA uses `.ml-button` with one of three variants? No bespoke buttons.
- Hero matches one of the canonical variants (`bleed-overlay`, `editorial-stack`, `text-only`, `compact`) OR is a documented movemental hero (`mh-hero`, `pw-hero`)?
- Cards reuse `.ml-card-*` or a `pw-output-card` / `sf-card` extension that uses the same vocabulary?
- Testimonials use cream-on-cream pattern (`.ml-quote` or `.pw-quote`), never dark olive?
- Footer is the canonical `.ml-footer .ml-footer-inner`?

### Pass 5 — Layout & rhythm
- Every major section is wrapped in `<div class="container">`?
- Section pad-block is `var(--space-16)` or `var(--space-20)`, not arbitrary px?
- Dividers between sections are hairlines (`1px solid var(--color-border)`)?
- Three-up grids collapse to single column under 860px?

### Pass 6 — Dark-olive discipline
- `var(--color-hero-dark)` (`#2D3A2A`) appears only in: hero bleed (`.ml-hero--bleed-overlay`, `.mh-hero`), bottom CTA band (`.mh-cta-band`, `.sf-midnight`), and as an accent on small markers (`.mh-mega-headline em`, `.sf-card-flag`, `.flr-chip[data-rating="yes"]`-related green isn't olive).
- It does NOT appear as the background of inline testimonials, feature cards, or quoting blocks.

---

## How to apply refinements

After listing deviations, apply them in this order:

1. **Add missing CSS classes to `css/pages.css`** rather than introducing inline `style="..."` overrides. New classes go in the appropriate prefix block (`pw-*`, `mp-*`).
2. **Strip `§ NN ·` from section eyebrows** — replace with the plain label that follows the marker.
3. **Add terminal periods** to display headlines (heroes, section heads, sidebar headings, closing titles) — but not to eyebrows, list items, or body paragraphs.
4. **Replace dark-olive testimonial blocks** with the cream-on-cream `.ml-quote` or `pw-quote` pattern.
5. **Refactor inline color overrides** into named modifier classes (`.pw-routing-card--active`, etc.).
6. **Verify Pass 6 dark-olive discipline** one more time before reporting done.

For each refined page, also check the cross-page chrome stays consistent:
- The nav mega-menu lists all four pathway pages and links them correctly with `is-active` on the current page.
- The `sf-stage-rail` shows the current stage as `.is-active` (a `<span>`, not a link) and other stages as links.
- The `sf-series-mast` shows volumes 01/02 as active/published, 03/04 as `.is-forthcoming`.
- The footer Pathway column has `aria-current="page"` on the current page.

---

## Output format

Return a short structured report:

```
# Oatmeal audit — <page>.html

## Deviations found
- [Pass 1: tokens] <description>
- [Pass 2: headlines] <description>
- ...

## Refinements applied
- <file>:<line> — <what changed>
- ...

## Residual
- <anything you flagged but didn't change, and why>
```

Keep it terse — this skill is run as part of a refinement cycle, not as a standalone deliverable.

---

## Canonical references

When in doubt, consult these in order:

1. `1-html/by-template-family/ml-templates/oatmeal/_reference/style-spec.md` — the formal extracted style spec
2. `1-html/by-template-family/ml-templates/oatmeal/_reference/NOTES.md` — adaptation decisions and known deviations
3. `1-html/by-template-family/ml-templates/oatmeal/css/tokens.css` — every token is the source of truth
4. `1-html/by-template-family/ml-templates/oatmeal/css/components.css` — primitive components
5. `1-html/by-template-family/ml-templates/oatmeal/index.html` — canonical home demo (Alan Hirsch exemplar)
6. `1-html/by-template-family/ml-templates/oatmeal/library.html`, `articles.html` — canonical library and article demos
7. `_reference/screencapture-tailwindcss-plus-kits-oatmeal-preview-*.png` — original kit screenshots for visual comparison

If a question can be answered from these references, it should be — don't speculate about Oatmeal canon when the source is sitting next to the page.
