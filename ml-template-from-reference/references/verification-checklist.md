# Verification checklist — post-scaffold

Run through every item before reporting the template complete. Each failing item gets a row in `_reference/NOTES.md` under "Known deviations" with the reason — don't silently smooth over drift.

## Reference & spec preserved

- [ ] All source reference images live in `_reference/` with original basenames.
- [ ] `_reference/style-spec.md` is filled out — no `{placeholder}` markers remaining.
- [ ] `_reference/style-spec.json` mirrors the markdown and parses as valid JSON (`python -m json.tool _reference/style-spec.json` exits 0).
- [ ] `_reference/NOTES.md` exists, records provenance (original paths + date archived), and the user's intent ("match exactly", "warm tones only", etc.).

## File structure

- [ ] `index.html`, `library.html`, `articles.html` all exist.
- [ ] All three load locally (open `index.html` in a browser) without console errors.
- [ ] `css/tokens.css`, `css/base.css`, `css/components.css`, `css/pages.css` all exist.
- [ ] `js/main.js` exists and is referenced with `defer`.
- [ ] Every image referenced in HTML resolves to a file under `images/` — no `404`s.

## Nav

- [ ] Identical nav markup appears at the top of all three pages.
- [ ] Logo links to `index.html`.
- [ ] `articles.html` and `library.html` nav links resolve correctly between pages.
- [ ] `aria-current="page"` is set on the matching nav link for each page (library on library.html, articles on articles.html, none on index.html).
- [ ] Mobile hamburger toggles `aria-expanded` and reveals/hides the drawer.
- [ ] Log in + primary CTA visible on every page.
- [ ] Current-page link is visually distinguishable.

## Hero

- [ ] The hero pattern in `index.html` visibly matches the pattern named in `style-spec.md`.
- [ ] Eyebrow, `h1`, tagline, and CTAs are all present (or any omission is documented in NOTES.md).
- [ ] Hero image is a real file (placeholder OK, but `<img src>` resolves).
- [ ] Library and articles heroes are present in their lower-intensity variants.

## Design tokens

- [ ] Colors in the rendered page eyeball-match the reference's palette (open both side by side).
- [ ] Display font and body font in the rendered page match the spec.
- [ ] Border-radius, button shape, and divider style match the spec.
- [ ] Density (gutter / whitespace) matches the spec.
- [ ] No tokens declared in `tokens.css` that aren't actually used by `components.css` or `pages.css`.

## Page content

- [ ] **Home** has all canonical sections (or noted omissions): nav, hero, quote, personas, portals, featured book, pathway CTA, latest articles, newsletter, footer.
- [ ] **Library** has: nav, compact hero with search, filter chips, resource grid (≥ 6 cards spanning multiple types), featured collection (or noted omission), pagination/load-more, footer.
- [ ] **Articles** has: nav, editorial hero, featured article, topic chips (or noted omission), article grid (≥ 6 cards), optional sidebar (or standalone newsletter), pagination, footer.
- [ ] All placeholder copy is labeled (`Placeholder until substrate is provided.` or similar). No fabricated book titles, quotes, dates, or author names.

## Responsive

- [ ] At 1280px: layout matches the reference's intended desktop view.
- [ ] At 768px: nav collapses to hamburger, grids reflow, hero adapts.
- [ ] At 375px: no horizontal scroll; touch targets ≥ 44px; type remains legible.

## Accessibility

- [ ] All images have `alt` attributes (`alt=""` for purely decorative imagery).
- [ ] Nav has `aria-label="Primary"`.
- [ ] Mobile toggle has `aria-expanded` and `aria-controls`.
- [ ] `:focus-visible` rings are visible on all interactive elements.
- [ ] Color contrast on body text ≥ 4.5:1 against its background; large text ≥ 3:1.
- [ ] Headings nest correctly — one `h1` per page, then `h2` → `h3`, no skipped levels.
- [ ] All forms have a label (visible or `.visually-hidden`).
- [ ] `prefers-reduced-motion` disables reveal animations.

## Cross-leader consistency

- [ ] Class names follow the `.ml-*` contract from `file-organization.md` — no ad-hoc class names for the nav, hero, cards, buttons, or footer.
- [ ] CSS architecture follows the four-file convention (`tokens.css` → `base.css` → `components.css` → `pages.css`).
- [ ] No framework, no build step, no bundler introduced.
- [ ] No external script tags beyond Google Fonts + `js/main.js`.

## Reference fidelity check

Open the primary reference image and `index.html` side by side. Ask three questions:

1. Could a designer recognize this template was built from the reference, by sight alone?
2. If yes, is the nav still recognizably "movemental" — same link set, same login + CTA placement?
3. Does the library and articles page feel like part of the same site as the home page?

If any answer is "no," log the failure in `_reference/NOTES.md` under "Known deviations" with the specific drift and a proposed fix for the next iteration.

## Sign-off

Once every checkbox passes (or has a documented deviation), the template is ready. Recommend the user run `/movemental-page-auditor` next for a rigorous opinionated read, or `/asset-generate` to replace the image placeholders.
