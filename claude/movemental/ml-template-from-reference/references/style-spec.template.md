# Style spec — {Leader Name / Template Slug}

**Generated from:** `_reference/{primary-image-basename}` ({+ N additional reference image(s)})
**Extracted on:** {YYYY-MM-DD}
**Extractor:** `ml-template-from-reference` skill

## First-impression sentence

> {One-sentence aesthetic description — the anchor for all later decisions.}

## Color

| Token | Value | Role | Notes |
|-------|-------|------|-------|
| `--color-bg` | `#......` | Page background | |
| `--color-surface` | `#......` | Card / panel surface | |
| `--color-surface-elevated` | `#......` | Hover / focus / nested surface | omit if unused |
| `--color-ink` | `#......` | Primary text | |
| `--color-ink-muted` | `#......` | Secondary text (captions, meta) | |
| `--color-accent` | `#......` | Primary accent / CTA | |
| `--color-accent-2` | `#......` | Secondary accent | omit if unused |
| `--color-border` | `#......` | Hairlines and dividers | |

**Temperature:** {warm / cool / neutral}
**Saturation:** {muted / balanced / vivid}

## Typography

| Slot | Family | Fallback chain | Weights used | Letterform notes |
|------|--------|----------------|--------------|------------------|
| Display | `{family}` | `{fallback chain}, serif/sans` | {e.g. 500, 700} | character: {serif / sans / slab / display} |
| Body | `{family}` | `{fallback chain}, sans-serif` | {e.g. 400, 600} | |
| Mono *(if used)* | `{family}` | `{fallback chain}, monospace` | | |

**Casing:** {title-case / sentence-case / ALL-CAPS headlines / mixed}
**Tracking — headlines:** {tight / normal / loose}
**Tracking — body:** {tight / normal / loose}
**Italics usage:** {emphasis / pull-quotes / none}

## Layout density

- **Whitespace ratio:** {sparse / balanced / dense}
- **Gutter width:** {narrow / generous}
- **Default column count:** {1 / 2 / 3 / 4}
- **Margin treatment:** {framed / full-bleed / mixed}

## Composition tendencies

- **Alignment:** {symmetric / asymmetric}
- **Grid behavior:** {strict-grid / overlap-allowed / break-grid}
- **Hierarchy mechanism:** {size / weight / color / spacing} contrast — usually {primary} + {secondary}
- **Flow:** {orthogonal / diagonal / mixed}

## Decorative motifs

{Bulleted list of every recurring graphic element. Use "none — relies on pure typography and spacing." if accurate.}

- {hairline rules / double rules / drop caps / badges / ornaments / grain / paper texture / dot pattern / blueprint grid / …}

## Imagery treatment

- **Bleed:** {full-bleed / framed / masked / cut-out}
- **Filter:** {none / warm-graded / desaturated / duotone / b&w}
- **Subjects:** {portrait / environmental / abstract / mixed}
- **Aspect ratios observed:** {16:9, 4:3, 3:4, 1:1}

## Hero pattern

**Selected:** `{bleed-overlay | split | portrait-dominant | art-bg-portrait-fg | text-only | editorial-stack}`

**Rationale:** {one sentence pulled from what the reference shows.}

## Component vocabulary

- **Button shape:** {rectangular / rounded / pill / square / underline-only}
- **Button fill:** {solid / outline / ghost / text}
- **Card construction:** {image-top / image-side / image-bg / borderless / heavy-border}
- **Divider style:** {none / hairline / double / ornamental}
- **Border-radius scale:** {sharp / 2–4px / 8–12px / 16–24px / fully-rounded}
- **Shadow scale:** {none / soft / hard / layered}

## Motion implications

**Energy:** {minimal / moderate / rich}

{One sentence on which moments matter — e.g., "moderate — only the hero gets a staggered reveal; chips and grids are static."}

## Web font loading

- **Display font URL:** `{Google Fonts URL or equivalent}`
- **Body font URL:** `{Google Fonts URL or equivalent}`
- **Total weight budget:** {< 100KB / < 200KB / other} — explicitly list every weight loaded.

## Open questions

{Bulleted list of anything unobservable from the reference and deferred to user input or to the next iteration. Honest gaps are better than guessed answers.}

- {…}
