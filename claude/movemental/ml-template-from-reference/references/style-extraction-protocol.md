# Style extraction protocol

A systematic protocol for reading a reference image and producing a style spec the template scaffold can consume. Run this protocol exactly once per reference set, before any HTML is written.

## Read the image in this order

### 1. First impression — one sentence

Before sampling pixels, write a single sentence describing the mood:

> "Warm scholarly editorial with generous whitespace and serif headlines."
> "Brutalist tabloid black-on-yellow with industrial sans-serif."
> "Soft pastel newsletter with hand-drawn ornaments."
> "Dense dark-mode utility portal with vivid accent and tight gutters."

This sentence anchors every later decision. If a later choice contradicts it, the choice is wrong, not the sentence.

### 2. Dominant colors (3–7)

Sample the largest contiguous color regions. Record each as a hex value plus a semantic role:

| Token | What to sample |
|-------|----------------|
| `--color-bg` | The page-level background — usually the largest area |
| `--color-surface` | Card / panel surfaces if distinct from `--color-bg` |
| `--color-surface-elevated` | Hover / focus / nested surfaces, if used |
| `--color-ink` | Primary body text color |
| `--color-ink-muted` | Secondary text (captions, meta) |
| `--color-accent` | The dominant accent — buttons, links, CTA |
| `--color-accent-2` | A second accent only if the reference clearly uses two |
| `--color-border` | Hairlines and dividers |

Do not extract more than two accent colors. If the reference visibly uses three, surface that to the user — it usually means the reference is multi-page and you're conflating contexts.

### 3. Color temperature and saturation

- Warm / cool / neutral — determines whether neutrals should be warm-gray or cool-gray.
- Muted / balanced / vivid — determines saturation budget across the palette.

### 4. Typography

Read the letterforms carefully — the `g`, `a`, `R`, and ampersand are the strongest tells.

- **Display family character**: serif / sans / slab / display / mono / hand-drawn. If you can identify the actual face, name it. Otherwise name two web-safe Google Fonts that hit the same character.
- **Body family character**: same drill.
- **Weights observed**: extract the actual weights, not a default scale. If the reference uses thin display + heavy body, capture that inversion — it's almost always intentional.
- **Tracking** observed (tight / normal / loose) on headlines and body separately.
- **Casing**: title case / sentence case / ALL CAPS headlines / mixed.
- **Italic usage**: does the reference use italics? For emphasis, or for pull quotes, or not at all?

### 5. Layout density

- Whitespace ratio: sparse / balanced / dense.
- Gutter widths: narrow / generous.
- Default column count: 1 / 2 / 3 / 4.
- Margin treatment: framed (content inside a clear margin) / full-bleed / mixed.

### 6. Composition tendencies

- Alignment: symmetric / asymmetric.
- Grid behavior: strict-grid / overlap-allowed / break-grid.
- Hierarchy mechanism: size contrast / weight contrast / color contrast / spacing contrast (often two of these in combination).
- Diagonal flow vs orthogonal.

### 7. Decorative motifs

List every recurring graphic element you see, however small:

- Hairline rules between sections
- Double rules / triple rules
- Drop caps
- Pull-quote ornaments
- Badges, ribbons, eyebrow chips
- Geometric shapes used as bullets
- Dot patterns
- Grain / noise overlay
- Paper texture
- Blueprint grid
- Hand-drawn ornaments

If none are visible, write "none — relies on pure typography and spacing." That is a valid extraction, not a gap.

### 8. Imagery treatment

- Bleed: full-bleed / framed / masked / cut-out.
- Filter: none / warm-graded / desaturated / duotone / monochrome.
- Aspect ratios observed.
- Subject treatment: portrait-centered / environmental / abstract / mixed.

### 9. Hero pattern

Pick the closest from the six canonical patterns:

| Pattern | Looks like |
|---------|-----------|
| `bleed-overlay` | Full-bleed image with text overlaid, often with gradient scrim |
| `split` | Image on one side, text on the other |
| `portrait-dominant` | Large portrait, minimal supporting text |
| `art-bg-portrait-fg` | Abstract art background with portrait foreground |
| `text-only` | Typographic hero, no imagery |
| `editorial-stack` | Headline above a single large image, text below |

This selection drives the home page's hero scaffold in Phase 3.

### 10. Component vocabulary

- Button shape: rectangular / rounded (2–6px) / pill / square (hard 0px) / underline-only.
- Button fill: solid / outline / ghost / text.
- Card construction: image-top / image-side / image-bg / borderless / heavy-border.
- Divider style: none / hairline / double / ornamental.
- Border-radius scale: sharp (0–2px) / small (4–6px) / medium (8–12px) / large (16–24px) / fully-rounded.
- Shadow scale: none / soft / hard (brutalist offset) / layered.

### 11. Motion implications

Motion is rarely visible in a static reference, but the design's *energy* implies it:

| Reference energy | Motion vocabulary |
|------------------|-------------------|
| Brutalist / monochrome / tabloid | None or hard cuts |
| Modern utility portal | Minimal — link hover states only |
| Editorial / magazine | Moderate — staggered reveal on load, subtle hover lifts |
| Soft / pastel / newsletter | Gentle — fades, easing curves, slow motion |
| Maximalist / animated brand | Rich — scroll-triggered, parallax, choreographed |

Encode as: `minimal | moderate | rich` + a one-sentence note on which moments matter (e.g., "moderate — only the hero gets a staggered reveal").

## Encode the spec

After reading, fill out [`style-spec.template.md`](style-spec.template.md) field-by-field, then write it to `_reference/style-spec.md`. Mirror the structured fields into `_reference/style-spec.json` (see [`style-spec.example.json`](style-spec.example.json)).

Every field must be defensible from the image. When a field genuinely cannot be inferred (e.g., the reference is a single hero screenshot with no card components), write `unobservable — defaulting to {neutral choice}` rather than guessing. Defaults must align with the first-impression sentence.

## Multiple references

If the user supplies multiple images:

| Case | Approach |
|------|----------|
| Variations on the same style | Average and note variance ranges in the spec |
| One "primary," others "secondary inspiration" | Lead with the primary; use secondaries only for fields the primary doesn't show |
| Conflicting styles | Surface the conflict to the user, ask which dominates — do **not** silently average a brutalist tabloid with a pastel newsletter |

When multiple images are kept, list them in `_reference/NOTES.md` in priority order.

## Defensive notes

- Don't sample colors from JPEG compression artifacts — sample from flat regions only.
- Don't assume a font is Inter just because it's sans-serif. Read the letterforms.
- A reference taken from an existing website doesn't license its fonts — pick web-safe equivalents (Google Fonts preferred) and disclose the substitution in `_reference/NOTES.md`.
- If the reference is a marketing screenshot at low resolution, mark color values as `±` approximate and note the resolution in `NOTES.md`.
- If the reference is a Figma/sketch export with a transparent canvas, infer the page background from the dominant surface color, not from the transparency.
