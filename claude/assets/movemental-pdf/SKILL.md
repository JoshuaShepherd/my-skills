---
name: movemental-pdf
description: Produce branded Movemental PDFs (the Movemental, LLC visual identity used at movemental.ai — wordmark logo, Inter typography, monochrome palette with warm-gray accents, generous whitespace, brand panels and stat cards). Use this skill whenever the user asks for a Movemental-branded document, a Movemental Field Guide, a Movemental MOU or proposal, a Movemental report, whitepaper, or any PDF matching the movemental.ai aesthetic. Use it even when the user only says "make this look like our brand", "the way we did it last time", or "in our house style" if the context is Movemental, and any time the deliverable is a PDF for Joshua Shepherd or Movemental, LLC. The skill includes the logo, Inter web fonts, a component library (cover, section openers, brand panels, stat cards, comparison tables, layer pages, checklists, framework callouts, citations, colophon), and a two-pass Chromium render pipeline that produces print-ready PDFs with running header, page-numbered footer, and a suppressed-chrome cover page.
user-invocable: true
argument-hint: '<content-or-html-path>'
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Movemental PDF

A skill for producing branded PDFs in the Movemental visual identity. The output is a print-ready PDF rendered from HTML + CSS via headless Chromium (Playwright). The brand system is monochrome with one warm-gray panel tint, Inter typography (Thin/ExtraLight for display, Regular for body, Medium for tracked-caps labels), and a small library of composable components.

## Setup (one-time)

The render pipeline needs a few tools. Install them before the first render:

```bash
pip install playwright pypdf       # render.py: Chromium driver + PDF merge
python3 -m playwright install chromium   # the headless browser itself
pip install Pillow                 # contact_sheet.py only
```

`contact_sheet.py` also shells out to `pdftoppm` (from `poppler-utils`): `apt-get install poppler-utils` on Debian/Ubuntu, `brew install poppler` on macOS. `render.py` auto-installs `pypdf` on first use if it is missing, but Chromium must already be present — `playwright install chromium` is the one step that cannot self-heal.

The bundled Inter fonts and `logo.png` ship with the skill under `assets/`; you do not install those. `render.py` stages them next to your HTML automatically (see Rendering).

## When this skill applies

Trigger whenever any of the following are true:
- The user is Joshua Shepherd or anyone at Movemental, LLC and asks for a PDF document.
- The user references "our brand", "house style", "the movemental.ai look", "field guide style", or the previous PDFs produced under this skill.
- The deliverable is a Movemental Field Guide, MOU, proposal, whitepaper, report, one-pager, or board packet.
- The user asks to "redesign" or "rebrand" a document into the Movemental style.

If the user wants a Word document (.docx) instead of a PDF, this skill still applies — use it to design the layout in HTML, render to PDF, and only fall back to docx if the user explicitly insists on an editable Word file.

## Workflow

1. **Read the brand system reference** at `references/brand-system.md`. This defines the tokens (colors, fonts, spacing), the type scale, and the rules for when to use each weight. Read it before writing any HTML.
2. **Read the component library** at `references/components.md`. This is the catalog of reusable building blocks — cover, section opener, brand panel, stat card, layer page, checklist, framework block, comparison table, citations list, colophon — with copy-paste HTML for each.
3. **Start from the starter template** at `references/starter.html`. It contains the full `<head>` with `@font-face` declarations and all base styles already wired up, a working cover, and a single example body section. Customize from there.
4. **Build the document.** Each top-level body section is `<section class="page">` which forces a new PDF page. The cover is `<section class="cover">` (full-bleed, no chrome).
5. **Render with the two-pass script** at `scripts/render.py`. It renders the cover (no header/footer) and the body (with running header and page-numbered footer) separately, then merges them with pypdf. This is non-negotiable — single-pass renders cannot suppress chrome on the cover while showing it on body pages.
6. **If the document has a Table of Contents with page numbers**, follow the two-pass TOC workflow at the bottom of this file. Render once, detect actual page numbers from the rendered PDF, write them back into the TOC, render again.
7. **Preview every render.** Always rasterize the PDF with `pdftoppm` and view several pages — at minimum the cover, the first body page, any stat-heavy or table-heavy page, and the colophon. Print fidelity is the whole point of this skill; visual confirmation is mandatory before declaring done.

## Critical render details

These are hard-won and easy to get wrong. The render script already gets them right; do not change these without reason.

- **No `@page { margin: ... }` in the HTML.** Chromium honors `@page` margins and silently overrides the `margin` parameter in `page.pdf()`, which breaks the header/footer layout. Keep `@page { size: Letter; }` only.
- **Two passes, not one.** Pass 1 renders the cover only with `display_header_footer=False` and `margin: 0` all around. Pass 2 renders the body only with `display_header_footer=True` and the running header/footer templates. Then pypdf concatenates them.
- **Hide the right things on each pass.** Pass 1 adds CSS `section.page { display: none !important; }`. Pass 2 adds CSS `section.cover { display: none !important; }`. The starter template uses these exact classes.
- **`prefer_css_page_size: True` is fragile.** When mixed with `@page` margin rules or with explicit `margin` parameters, it produces unpredictable results. Leave it off (the default).
- **Page numbering offset.** Playwright's `pageNumber` token in the footer template restarts at 1 for the body PDF. After merging, the cover is PDF page 1 and the body footer "1" appears on PDF page 2. The TOC in the starter template uses body-relative numbers (matching what the reader sees in the footer), not absolute PDF page numbers. Stay consistent: either footer "01" appears on the first content page (the convention used in the existing Movemental PDFs), or shift the entire numbering scheme — but pick one and document it.

## Rendering

The render script lives at `scripts/render.py`. It takes one argument — the path to the input HTML — and writes the output PDF next to it.

```bash
python3 scripts/render.py path/to/document.html
# Produces: path/to/document.pdf
```

Write your HTML using the local-copy asset pattern the starter template uses — reference the logo as `logo.png` and fonts as `fonts/inter-300.woff2`. You do **not** need to copy those files yourself: before rendering, `render.py` stages the bundled `assets/logo.png` and `assets/fonts/*.woff2` (resolved relative to the script's own location) into the HTML's working directory if they are not already there. Pass `--no-stage` to skip this when you are managing assets yourself (for example, an HTML that points at `../assets/...` directly). The header logo is also injected from the staged copy, falling back to the skill's `assets/logo.png` if the working directory has none.

The render script does the following:
0. Stages bundled assets (`logo.png`, `fonts/*.woff2`) into the HTML's directory if missing, unless `--no-stage` is passed.
1. Launches headless Chromium via Playwright.
2. Loads the HTML twice in separate contexts.
3. Pass 1: hides body sections, renders cover to `_cover.pdf` with margins 0 and no chrome.
4. Pass 2: hides cover, renders body to `_body.pdf` with header template (mini-wordmark left, doc title right) and footer template (movemental.ai left, page number right). Body margins: top 0.75in, bottom 0.6in, left/right 1.0in.
5. Merges the two PDFs with pypdf and writes the result.
6. Deletes the intermediate `_cover.pdf` and `_body.pdf` (or keeps them — there's a `--keep-intermediates` flag).

If the user wants different margins, header text, or footer text, edit the constants at the top of the render script (`HEADER_TITLE`, `FOOTER_LEFT`, `BODY_MARGIN_*`). Do not override these via the HTML's `@page` rules.

## The TOC two-pass workflow

Documents with a Table of Contents that lists page numbers (Field Guides, board books) need this. Tables and bullet TOCs without page numbers don't.

1. In the TOC, use string placeholders for each page number: `PG_INTRO`, `PG_AUTH`, `PG_WHY`, etc. The starter template's TOC uses this convention. Each placeholder is unique and contains no other meaningful text.
2. Render the PDF once with placeholders in place.
3. Run `scripts/detect_toc_pages.py path/to/document.pdf`. It scans the rendered PDF, matches a hand-picked distinctive opener phrase from each section's body prose (not the section title — that recurs on the TOC page and will produce false hits), and prints a Python dict mapping placeholder names to body-relative page numbers.
4. Edit the markers list in `scripts/detect_toc_pages.py` to match the distinctive openers in your document. Or paste the detected dict back into your document HTML, replacing each `PG_X` with the zero-padded two-digit page number.
5. Re-render. The TOC now shows real page numbers that match the footer.

The detection script ignores the TOC page itself (you tell it which PDF page the TOC is on) so that "AI Organizational Statement" appearing in the TOC doesn't match before the actual Layer 01 page. If your TOC isn't on page 5 (PDF) / page 4 (body footer), pass `--toc-pdf-page N` to skip it.

## Quality bar

- All Inter weights from 100 to 700 are bundled. Use them. The cover title is 100 or 200, never heavier. Section titles are 200. Subheads are 500. Body is 400. Tracked-caps labels are 500 or 600. See the type scale in `references/brand-system.md`.
- The palette is monochrome plus one warm-gray panel tint. Do not introduce other colors. If you need to differentiate, use weight, size, or position — not hue.
- Generous whitespace is the brand. Tight typography is not. Body pages should breathe. Empty space at the bottom of a section page is correct, not a bug.
- Use the components in `references/components.md` rather than inventing new layouts. If a content shape doesn't fit any existing component, prefer extending the closest one over building something new.
- Run a contact-sheet preview (`scripts/contact_sheet.py path/to/document.pdf`) on documents longer than 10 pages to catch orphaned headings, awkward whitespace, or page-break issues across the whole doc at once.

## Examples of what this skill produces

Two reference documents were produced with this exact pipeline:
- A 10-page Movemental × Youthfront MOU (cover, 9 numbered sections, signature page, appendix module list)
- A 33-page "It Starts With Safety" Field Guide (cover, intro, authors' note, TOC, 5 numbered layer pages, statistics-heavy data section, two-paths comparison table, citations, colophon)

Both use the same components, the same brand tokens, and the same render pipeline. The skill's job is to make every future Movemental PDF visually continuous with these.
