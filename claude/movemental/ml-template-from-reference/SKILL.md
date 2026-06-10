---
name: ml-template-from-reference
description: Build an HTML/CSS/JS movement-leader template (home + content library + articles) whose visual design matches a provided reference image (or images) exactly. The movemental (alan-hirsch) navigation structure is fixed and consistent across leaders; everything else — color, type, layout, density, motifs — is extracted from the reference. The reference image(s) and an extracted style-spec are archived inside the template directory so future passes can re-consult them.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

Build a movement-leader HTML template whose visual design matches a reference image: $ARGUMENTS

`$ARGUMENTS` should include:
- One or more reference image paths (absolute, or under the project root)
- A leader name or template slug (e.g., "Brad Brisco" / `brad-brisco`)
- Optionally: path to a `*_RESEARCH_COLLATED.md` substrate for editorial copy
- Optionally: `--out <slug>` to override the default output directory name
- Optionally: `--primary-cta "Take the assessment"` to override the canonical CTA
- Empty → ask the user for the reference image(s) and leader name

## Output location

Generated artifacts land in [1-html/by-template-family/ml-templates/](1-html/by-template-family/ml-templates/), sibling to `alan-hirsch/`, `alan-books-static/`, and the other families documented in [1-html/README.md](1-html/README.md):

```
1-html/by-template-family/ml-templates/{slug}/
  _reference/
    {original-image-basename}.{ext}     # source reference(s) — copied, not moved
    style-spec.md                       # extracted design language, human-readable
    style-spec.json                     # same, machine-readable
    NOTES.md                            # provenance, known deviations, source URLs
  index.html                            # home
  library.html                          # content library
  articles.html                         # articles index
  css/
    tokens.css                          # extracted design tokens (CSS variables)
    base.css                            # reset, body typography, utilities
    components.css                      # nav, hero, cards, buttons, footer
    pages.css                           # page-specific composition
  js/main.js
  images/                               # placeholder hero/covers used by the template
```

The reference image(s) live inside the template directory permanently so future skills (audits, iterations, regenerations) can re-consult them without hunting through the user's filesystem.

## Process — four phases

### Phase 1 — Archive the reference

1. Validate each reference image path with `Read` (it will surface the image so you can also begin Phase 2 inspection).
2. Create `1-html/by-template-family/ml-templates/{slug}/_reference/`.
3. Copy (NOT move) each reference image in with its original basename: `cp "{source}" "1-html/by-template-family/ml-templates/{slug}/_reference/{basename}"`.
4. Write `_reference/NOTES.md` capturing:
   - Original absolute path(s) of each reference, in order received
   - Date archived (today's date in YYYY-MM-DD)
   - Anything the user said about the reference ("match it exactly", "use the dominant warm tones", "this is the new Brisco style", etc.)
   - Any context that won't be obvious from the image alone (which leader, which page on the reference site this is from, etc.)

The user's original file is never touched.

### Phase 2 — Extract the design language

Follow [references/style-extraction-protocol.md](references/style-extraction-protocol.md) to systematically read each reference image. Fill out the template in [references/style-spec.template.md](references/style-spec.template.md), then write the result to `_reference/style-spec.md`. Mirror the same fields into `_reference/style-spec.json` (see [references/style-spec.example.json](references/style-spec.example.json) for the JSON shape).

The style spec captures:
- Color palette (semantic tokens, not just hex values)
- Typography (display + body family, observed weights, scale)
- Layout density & composition tendencies
- Decorative motifs (rules, frames, textures, grain, gradients)
- Imagery treatment (bleed / framed / masked, filters, mood)
- Hero pattern (which of the six canonical patterns the reference most resembles)
- Component vocabulary (button shape, card construction, dividers)
- Border-radius scale, shadow scale, motion implications

**Critical**: extract what the reference *actually shows*, not what's "on brand for movement leaders." If the reference is brutalist black-on-yellow, the template is brutalist black-on-yellow — not warm earth tones. If you find yourself reaching for movemental defaults instead of the image, stop and re-read the reference.

### Phase 3 — Scaffold the template

Follow [references/file-organization.md](references/file-organization.md) for the file layout, CSS architecture, and class-name contract. Each output page is built against a fixed spec:

| Page | Spec |
|------|------|
| Home (`index.html`) | [references/page-home-spec.md](references/page-home-spec.md) |
| Content Library (`library.html`) | [references/page-content-library-spec.md](references/page-content-library-spec.md) |
| Articles (`articles.html`) | [references/page-articles-spec.md](references/page-articles-spec.md) |

The navigation is **fixed** across all three pages — see [references/movemental-nav-spec.md](references/movemental-nav-spec.md). Only the visual styling of the nav (colors, typography, density, sticky behavior, search presence) adapts to the reference. The link set, semantics, mobile behavior, and login/CTA placement are canonical for the movement-leader template family.

CSS architecture (four files, in this load order):
1. `tokens.css` — `:root { --color-..., --font-..., --space-..., --radius-..., --shadow-... }` from Phase 2.
2. `base.css` — minimal reset, body typography, `.visually-hidden`, focus rings.
3. `components.css` — `.ml-nav`, `.ml-hero`, `.ml-card`, `.ml-button-*`, `.ml-footer`, etc. Must produce the class names listed in `file-organization.md`.
4. `pages.css` — page-specific composition (`.home-personas-grid`, `.library-grid`, `.articles-featured`).

JS is minimal: mobile nav drawer, sticky-on-scroll state, reveal animations only if the style spec's motion field is non-minimal. Vanilla, no framework, `defer` on the script tag.

### Phase 4 — Verify against the reference

Run through [references/verification-checklist.md](references/verification-checklist.md). If the user wants visual confirmation, hand off to `/verify` or `/run` to open the pages in a browser side-by-side with the saved reference. Record any drift in `_reference/NOTES.md` under a "Known deviations" section — don't silently smooth it over.

## What this skill is and is not

**Is**: a one-shot template scaffolder that produces a high-fidelity, design-matched HTML starting point.

**Is not**:
- A component library. Output is a template, not a reusable system.
- A content authoring skill. Copy is placeholder unless a substrate is provided — defer real copy to `/movemental-prose`, `/alan-voice`, or `/article-author`.
- A production React build. HTML/CSS/JS by deliberate design — portable, statically reviewable, convertible later via `/html-to-react-tailwind` if needed.
- A nav redesigner. The nav structure is canonical across all movement-leader templates; only styling adapts.

## Re-runs and iteration

If the output directory already exists:
- **Same reference, refined extraction** — overwrite `style-spec.md` / `style-spec.json`; preserve user edits to `_reference/NOTES.md`.
- **New reference image added** — copy it into `_reference/` alongside the existing one(s); update the spec; flag in `NOTES.md` which image is now the primary source of truth.
- **Style spec edited by hand** — treat the existing spec as authoritative and skip re-extraction unless the user explicitly says to overwrite.
- **Template HTML edited by hand** — never silently overwrite. Diff first, ask before clobbering.

## Hand-offs to other skills

| Next step | Skill |
|-----------|-------|
| Add real editorial copy | `/movemental-prose`, `/alan-voice`, `/article-author` |
| Audit the result | `/movemental-page-auditor` |
| Generate hero / cover art | `/asset-generate`, `/asset-hero-portrait`, `/asset-series` |
| Match a specific leader's brand guidelines | `/applying-brand-guidelines` |
| Convert HTML → React/Tailwind | `/html-to-react-tailwind` |
| Place the rendered template in a device mockup | `/asset-mockup` |

## Key rules

1. **The reference is the source of truth.** When torn between "what the reference shows" and "what feels movemental," follow the reference.
2. **Never move the reference image** — only copy it. The user's original stays where they put it.
3. **Nav structure is fixed; nav styling adapts.** Don't redesign the link set to match the reference.
4. **Three pages, every time.** Home, library, articles — even if one is sparse.
5. **No fabricated metadata.** Placeholder copy is acceptable and labeled (`Lorem-style placeholder until substrate is provided.`). Don't invent book titles, dates, authors, or quotes.
6. **One spec, two formats.** `style-spec.md` for humans, `style-spec.json` for downstream tools. They must agree.
7. **Class-name contract.** Every template ships the `.ml-*` class names listed in `file-organization.md` so downstream skills can target them.
