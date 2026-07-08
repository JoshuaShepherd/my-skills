---
name: integrate-stitch-template
description: "Fully integrate a Google Stitch screen (or set of screens) into the movement-leader-html-templates platform. Given Stitch instructions (project title + ID and one or more screens with titles + screen IDs), this scaffolds the template folder, pulls the HTML + screenshot from Stitch, gives it a Framer-style name, copy-edits the content to fit the movement-leader author/pastor platform without breaking the UI, swaps placeholder/external images for local repo assets, extracts design tokens, and rebuilds + validates the catalog. Runs in both Claude Code and Cursor. Use when adding a new template from a Stitch design."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__stitch__get_screen, mcp__stitch__get_project, mcp__stitch__list_screens
---

Integrate a Stitch design into the template platform: $ARGUMENTS

`$ARGUMENTS` is a **Stitch Instructions** block (the format Stitch hands you) plus optional naming. Parse:

- **Project** — title + numeric project ID.
- **Screens** — for each screen: a human title (often `Persona | Page (Vn)`) and a hex screen ID. Multiple screens are allowed.
- **Name** (optional) — desired template display name and/or slug. If absent, you choose one (see Phase 2).
- Empty — ask the user to paste the Stitch Instructions block.

This skill assumes the repo **movement-leader-html-templates** (the one whose `scripts/import-stitch-template.mjs` and `templates/<slug>/` layout this skill targets). If the current working directory isn't that repo, find it (it is a sibling under the same parent, e.g. `…/movement-leader-html-templates`) and run all `node`/`npm` commands from its root.

---

## What "fully integrated" means

A finished template matches every other folder under `templates/`:

```
templates/<slug>/
  catalog.yaml          # name, subtitle, tags, color_mode, fonts, hero, ready_for_publish
  metadata.json         # slug, projectId, projectTitle, screens{key→screenId}, fetchedAt
  DESIGN.md             # mood / typography / color contract for re-generation
  tokens.json           # palette + fonts extracted from the screen's tailwind.config
  README.md             # title + re-import command
  screens/
    home.html           # Stitch HTML, header-stamped, copy-edited, local images
    home.png            # full-width screenshot
    home.meta.json      # screenId, dimensions, fetchedAt
```

Then `npm run catalog` regenerates `catalog/templates.json` and `npm run validate <slug>` passes with no errors.

---

## Phase 0 — Preflight

1. Confirm repo root: `scripts/import-stitch-template.mjs`, `scripts/new-template.mjs`, and `templates/` all exist. If not, locate the repo and `cd` there for the rest of the run.
2. Confirm **Stitch access** — you need one of:
   - The **Stitch MCP** connected (tools `mcp__stitch__get_screen`, `get_project`, `list_screens`), **or**
   - `STITCH_API_KEY` set in the environment (the `npm run import` path uses it directly).
   - If neither is available, **stop and tell the user** you need one of them, or the signed `downloadUrl`s for each screen. Do not invent or scrape URLs — Stitch download URLs are short-lived signed GCS links returned only by `get_screen`.
3. Read one existing template end-to-end as your reference for the house style — `templates/heritage-noir/` or `templates/curated-editorial/` are good models for copy + image conventions.

---

## Phase 1 — Map screens to logical keys

Stitch titles are auto-generated; the repo uses **stable logical keys** in `metadata.json`. Map each screen:

| Key | Use |
|-----|-----|
| `home` | Primary landing / hero (always present) |
| `article` | Long-form reader |
| `course` | Pathway / course landing |
| `book` | Book or teaching hub |

A single homepage screen → just `home`. File names mirror keys (`screens/home.html`, `screens/home.png`).

---

## Phase 2 — Choose the name

Templates carry a **Framer-style evocative name**, not the author's name. Look at existing titles (`Heritage`, `Hearth`, `Nocturne`, `Vesper`, `Verdant`, `Dispatch`, `Curator`) — one or two words evoking the *visual style*, never the persona.

- **`slug`** — kebab-case, style-descriptive (e.g. `heritage-noir`, `warm-clay`, `dark-goldline`). If you can't judge the style until the HTML/PNG land, scaffold with a provisional slug and rename after Phase 3 with `node scripts/rename-template-slugs.mjs` (or re-run `new-template.mjs`).
- **`title`** — short evocative name.
- **`subtitle`** — one line: palette + typography + mood (e.g. _"Dark grain, gold serif accents — cinematic heritage editorial"_). Match the existing subtitle cadence in `scripts/apply-template-names.mjs`.

If the user supplied a name, use it. Otherwise pick after you've seen the screenshot, and confirm a one-word title with the user if it's a judgment call.

---

## Phase 3 — Scaffold + fetch from Stitch

### 3a. Scaffold the folder

```bash
node scripts/new-template.mjs <slug> \
  --project-id <projectId> \
  --title "<Display Name>" \
  home:<screenId> [article:<screenId> ...]
```

This writes `catalog.yaml`, `metadata.json`, `DESIGN.md`, `tokens.json`, `README.md` and an empty `screens/`.

### 3b. Pull HTML + screenshot

**Path A — `STITCH_API_KEY` in env (preferred, one command):**

```bash
STITCH_API_KEY=… npm run import -- <slug>
```

`import-stitch-template.mjs` calls `get_screen`, `curl -L`s the `htmlCode.downloadUrl` → `screens/<key>.html`, downloads `screenshot.downloadUrl=w<width>` → `screens/<key>.png`, stamps the `STITCH SCREEN` header comment, writes `<key>.meta.json`, and refreshes the catalog. Single screen: add `--screen home`.

**Path B — Stitch MCP, no key (do what the script does, by hand):**

For each screen key:
1. `mcp__stitch__get_screen` with `{ projectId, screenId, name: "projects/<projectId>/screens/<screenId>" }`.
2. Download the HTML: `curl -L -f -sS --compressed "<detail.htmlCode.downloadUrl>" -o templates/<slug>/screens/<key>.html` (the repo's `scripts/fetch-stitch.sh <url> <out>` is exactly this wrapper).
3. Download the screenshot at full width: `curl -L … "<detail.screenshot.downloadUrl>=w<detail.width>" -o templates/<slug>/screens/<key>.png` (retry without `=w<width>` if it fails).
4. Prepend the header comment if absent:
   ```html
   <!--
     STITCH SCREEN
     Template: <slug>
     Screen key: <key>
     Title: <title>
     Screen ID: <screenId>
     Project: <projectId>
     Downloaded: <ISO timestamp>
   -->
   ```
5. Write `screens/<key>.meta.json` mirroring the shape in any existing `*.meta.json` (screenKey, screenId, title, deviceType, width, height, htmlFile, pngFile, name, fetchedAt).

Verify each `.html` is real markup (not an error page) and each `.png` is non-trivial in size before continuing.

---

## Phase 4 — Copy-edit to fit the platform (without breaking the UI)

The screens are demos of **how a movement leader's public platform presents their sermons, books, and formation courses.** Reframe the generic Stitch copy to that story while keeping it honest as a demo.

**The cardinal rule: edit text *content* only — never structure.** This is what "without breaking the UI" means:

- Replace the inner text of elements; keep every tag, `class`, wrapper, `<svg>`/icon, and `aria-*` exactly as-is.
- Keep replacement text roughly the **same length** as the original. Buttons, nav links, chips, and stat labels live in fixed/flex containers — a label that doubles in length wraps or overflows. Match word count for short UI strings; you have more room in paragraphs.
- Don't touch `tailwind.config`, `<style>`, layout classes, grid/flex counts, or the number of repeated cards/items.
- Keep the existing **author persona** if the Stitch screen already names one (e.g. a homepage built around "Dr. Elias Thorne" keeps that persona) — just make the surrounding copy coherent. If the persona is a bare placeholder (`Lorem`, `Your Name`), give it a plausible movement-leader author persona consistent with the rest of the repo's demos (e.g. "Jordan Ellis is a pastor and author building a single home for sermons, books, and formation courses").
- Apply plain-prose instincts: concrete, human, no register-jargon. If the `/plain-prose` skill is available and copy is heavy, run it on the prose blocks.

Edit hero headline/subhead, section intros, card blurbs, CTA labels, footer, and `<title>`/meta. Leave nav structure and counts alone.

---

## Phase 5 — Images: swap placeholders for local repo assets

Templates must reference **root-absolute local paths** so previews render from the gallery server. Remove every external host (`lh3.googleusercontent.com`, `picsum`, etc.) and any stray `/images/leaders/<name>.jpg` placeholder that doesn't match the persona.

Available local assets (see `images/README.md`, `catalog/images.json`, `catalog/stock-images.json`):

| Folder | Use | Path form |
|--------|-----|-----------|
| `images/stock/` | Generic hero / portrait / book-cover / landscape fills, by aspect ratio | `/images/stock/portrait-4x5.jpg`, `/images/stock/landscape-16x9.jpg`, `/images/stock/book-cover-1.jpg` |
| `images/voices/` | `.webp` leader portraits for "trusted voices" rows | `/images/voices/<slug>.webp` |
| `images/leaders/` | `.jpg` full leader portraits | `/images/leaders/<slug>.jpg` |
| `images/brand/` | Movemental logo | `/images/brand/movemental-logo-transparent.h224.webp` |

Two ways, combine as needed:

1. **Automated aspect-ratio swap** — `npm run apply:stock` rewrites external `<img src>` and `background-image: url(...)` to the aspect-matched stock image (`scripts/apply-stock-images.mjs`). Run it, then review the result.
2. **Hand-place meaningful images** — the hero portrait, "trusted voices" row, and brand logo read better with intentional choices. Match the container's aspect ratio (`aspect-[4/5]` → a `portrait-4x5`, `aspect-video` → a `landscape-16x9`) so nothing distorts. For a voices/leaders row, pull real slugs from `catalog/images.json`.

After: `grep -nE "lh3\.googleusercontent|http.*\.(jpg|png|webp)" templates/<slug>/screens/*.html` should return nothing but intentional, allowed URLs. Confirm no `<img>` is left with a broken/placeholder `src`.

---

## Phase 6 — Document the design

- **`tokens.json`** — extract the screen's `tailwind.config` colors + `fontFamily` and the `<style>` body palette into `colors`, `fonts`, `borderRadius`, `spacing`. Set `colorMode` to `LIGHT`/`DARK` (check `<html class="dark">`).
- **`catalog.yaml`** — fill `title`, `subtitle`, `tags` (e.g. `[dark, editorial, serif]`), `color_mode`, `fonts.display`/`fonts.body` (the actual families), `hero.aspect_ratio` to match the hero image, and `ready_for_publish: true` once it looks right. `project_title` should match the display name.
- **`DESIGN.md`** — fill Mood / Typography / Color mode so a Stitch re-generation stays on-style.
- **`README.md`** — title + the re-import command.

`new-template.mjs` already seeds these; you're replacing the placeholder lines, not rewriting structure.

---

## Phase 7 — Rebuild, validate, preview

```bash
npm run catalog              # regenerate catalog/templates.json
npm run validate <slug>      # must show ✓ with no errors
```

Validation warns (not errors) until `screens/<key>.html` + `.png` exist — by Phase 7 they should, so warnings should be gone. Optionally preview:

```bash
npm run dev                  # http://localhost:3000 — find the new card in the grid
```

Open `templates/<slug>/screens/home.html` (or `view.html`) and eyeball: layout intact, copy coherent, images loading, no overflow.

---

## Phase 8 — Report

Tell the user: the slug + display name, screens imported, what copy you reframed, which images you placed, token/catalog status, and the validate result. Note anything left for them (e.g. a name you want confirmed, a screen that needs a real portrait).

---

## Notes for both runtimes

- **Claude Code & Cursor** both run this from a `SKILL.md`; everything here is shell (`node`/`npm`/`curl`/`grep`) plus optional Stitch MCP calls, so it works identically in either. Prefer the repo's own scripts (`new-template.mjs`, `import-stitch-template.mjs`, `apply-stock-images.mjs`, `build-catalog.mjs`, `validate-templates.mjs`) over re-implementing — that's the established pattern.
- Never commit `STITCH_API_KEY`. It comes from the environment or `.env.local` (gitignored).
- `.stitch/` is a scratch cache and is gitignored; the durable output lives under `templates/<slug>/`.
