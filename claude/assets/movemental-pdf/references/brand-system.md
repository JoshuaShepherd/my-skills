# Movemental Brand System

The visual identity for Movemental, LLC. The brand is defined by restraint: a single typeface family in a wide range of weights, a monochrome palette with one warm-gray panel tint, hairline rules, and generous whitespace. The wordmark logo (lowercase "movemental" with a spirograph rosette in place of the "o") sits on the cover and in the running header.

This document defines the tokens. The component library (`components.md`) shows how to combine them.

## Color tokens

The full palette as CSS variables. Use these names directly in skill-produced documents.

```css
:root {
  --ink:        #111111;  /* near-black body text and titles */
  --ink-soft:   #2a2a2a;  /* body prose — softer than pure black */
  --muted:      #6b6b6b;  /* labels, secondary text, footer chrome */
  --quiet:      #8a8a8a;  /* tertiary accents, the rosette gray */
  --rule:       #d8d8d8;  /* visible hairline rules */
  --rule-faint: #ececec;  /* nearly invisible separators */
  --bg-panel:   #f6f6f4;  /* warm-gray panel background */
  --bg-deep:    #efefec;  /* slightly darker panel — rarely used */
  --accent:     #8a8a8a;  /* same as --quiet, for bullet markers */
}
```

**Usage rules.**
- Body prose is `--ink-soft`, not pure black. Pure black is reserved for titles and emphasis.
- Tracked-caps labels (kickers, subheads, source lines) are `--muted` — never `--ink-soft` (too dark) or `--quiet` (too light).
- Hairlines under TOC entries, between citation items, etc. are `--rule-faint`. Hairlines that separate sections or sit under headings are `--rule`. Solid black rules are reserved for the cover and the top of `h2.section-title`.
- Brand panels (parties block, framework block, stat cards, stakes callout) are `--bg-panel` with a 2px solid `--ink` left rule. Never use a different background tint.

## Typography

The skill ships with Inter weights 100, 200, 300, 400, 500, 600, 700 (plus 300 and 400 italic). Inter is licensed under the SIL Open Font License and may be embedded freely.

```css
/* @font-face declarations — the starter template includes all of them */
@font-face { font-family: "Inter"; font-style: normal; font-weight: 100; src: url("fonts/inter-100.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 200; src: url("fonts/inter-200.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 300; src: url("fonts/inter-300.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 400; src: url("fonts/inter-400.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 500; src: url("fonts/inter-500.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 600; src: url("fonts/inter-600.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: normal; font-weight: 700; src: url("fonts/inter-700.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: italic;  font-weight: 300; src: url("fonts/inter-300-italic.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-style: italic;  font-weight: 400; src: url("fonts/inter-400-italic.woff2") format("woff2"); }
```

Always use `font-family: "Inter", "Helvetica Neue", Arial, sans-serif;` so the fallback stack is sane when fonts fail to load.

### Type scale

| Role | Family | Weight | Size | Line height | Color | Letter-spacing |
|---|---|---|---|---|---|---|
| Cover title (large) | Inter | 100 | 56–64pt | 1.0 | --ink | -0.025em |
| Cover title (continuation) | Inter | 200 | 56–64pt | 1.0 | --ink | -0.025em |
| Cover subtitle | Inter | 300 | 14–16pt | 1.35 | --ink-soft | normal |
| Section title (h2.section-title) | Inter | 200 | 26–32pt | 1.1 | --ink | -0.012em |
| Layer page title (h2.layer-title) | Inter | 200 | 26pt | 1.1 | --ink | -0.012em |
| Lede paragraph | Inter | 300 | 12pt | 1.5 | --ink-soft | normal |
| Subhead (h3.subhead) | Inter | 500 | 12pt | 1.4 | --ink | normal |
| Body prose | Inter | 400 | 10–10.5pt | 1.55–1.6 | --ink-soft | normal |
| Big statistic | Inter | 200 | 38–56pt | 1.0 | --ink | -0.02em |
| Tracked-caps kicker / label | Inter | 500 or 600 | 8–9pt | 1.4 | --muted | 0.18–0.26em |
| Footer / header chrome | Inter | 300 | 7.5pt | 1.0 | --muted | 0.18em (header right side) |
| Citation entry | Inter | 400 | 9pt | 1.45 | --ink-soft | normal |

**Letter-spacing rules.**
- Large display type gets negative tracking (-0.012em to -0.025em) so the wide gaps between thin letterforms tighten.
- Tracked-caps labels get positive tracking (0.18em minimum, 0.26em for the most spaced kickers). Always uppercase.
- Body prose is normal tracking. Never adjust.

## Page geometry

US Letter, 8.5 × 11 in.

**Cover.** Full bleed. The cover element sets its own padding (1.0in top, 1.0in sides, 0.9in bottom is typical). The render pass gives the cover 0in margins all around.

**Body.** Render pass margins:
- Top: 0.75in (reserves space for the running header)
- Bottom: 0.6in (reserves space for the footer)
- Left/right: 1.0in (gives body text a comfortable measure — about 70 characters per line at 10.5pt)

These margins are set on the `page.pdf()` call, not on the HTML `@page` rule. Do not also set `@page { margin: ... }` — it conflicts.

## The wordmark

The logo is a lowercase "movemental" wordmark in a thin geometric sans-serif. The "o" is replaced by a delicate gray spirograph rosette. The logo file (`assets/logo.png`) is 1498 × 478 px, RGB on transparent background.

**Where the wordmark appears.**
- On the cover, top-left, sized at 2.2–2.6in wide.
- In the running header of body pages, sized at 11pt high (about 0.4in wide).
- On the colophon page, centered, sized at 1.8in wide.

**Where the wordmark does not appear.**
- It does not appear on every page beyond the running header. Repetition cheapens the mark.
- It is not used as a background watermark. Movemental documents do not use watermarks.

**Color of the wordmark.** The PNG is monochrome. Do not tint it. Do not invert it.

## Voice in design

The brand voice is calm, considered, and confident. Visual choices should reinforce this:

- Hairlines under section titles, not heavy bars.
- Generous trailing whitespace at the end of section pages. Empty space is not a layout failure.
- One stat at a time gets large treatment. Crowding statistics shouts; spacing them makes each one land.
- Tables use horizontal rules only, never vertical lines or shaded headers. Cell padding is generous (10pt on each side).
- Bullets use a small filled circle in `--accent` or a hollow square checkbox in `--ink` (for "complete X contains" lists). Both are 4–7pt — small.

## What this brand is not

To stay on-brand, avoid:
- Bright accent colors. No blue links, no red emphasis, no green checkmarks.
- Drop shadows, gradients, rounded corners (greater than 0px), or any "soft UI" effect.
- Sans-serif typefaces other than Inter, including system Helvetica/Arial except as fallback.
- Icons or pictograms anywhere in the document body. The wordmark is the only graphic element.
- Centered body text. Body prose is always left-aligned. Centering is reserved for the colophon and the cover meta.
- All-caps body type. Tracked caps are for labels only, never paragraphs.
