---
name: stitch-download
description: "Browse Stitch projects, download all screens (HTML + screenshots), and generate an organized local gallery with an index.html for browser viewing. Use when reviewing designs before conversion, comparing screens, or sharing with stakeholders."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

Download and organize Stitch project designs for browser viewing: $ARGUMENTS

$ARGUMENTS should include:
- A Stitch project ID, OR "list" to browse all projects
- Optionally: "shared" to include projects shared with you (default: owned only)
- Optionally: a specific screen ID or screen title to download a single screen
- Optionally: "refresh" to re-download screens that already exist locally
- Empty — list all projects and ask the user which to download

---

## Purpose

This skill connects to the Stitch MCP, inventories existing projects and screens, downloads all assets (HTML source + full-resolution screenshots), and generates a local browseable gallery at `.stitch/designs/index.html`. The gallery organizes screens by project with thumbnails, metadata, and links to full HTML previews — making it easy to review designs in the browser, share with stakeholders, or select screens for conversion with `/stitch-react`.

## Before Starting

1. **Check for the fetch script** — Verify `scripts/fetch-stitch.sh` exists. If not, create it (simple curl wrapper with redirect handling).
2. **Check existing cache** — Read `.stitch/designs/` to see what's already downloaded. Avoid re-downloading unless the user specifies "refresh".
3. **Ensure `.stitch/` is gitignored** — Check `.gitignore` for `.stitch/` entry. Add it if missing (these are large binary/HTML files).

---

## Phase 1 — Inventory Projects

### If no project ID provided (or "list"):
1. Call `mcp__stitch__list_projects` (and optionally with `filter: "view=shared"` if user asked for shared).
2. Present a table:

```
## Stitch Projects

| # | Project Title | Project ID | Screens |
|---|--------------|------------|---------|
| 1 | Homepage Explorations | 12345 | 6 |
| 2 | Dashboard V2 | 67890 | 14 |
| ... | ... | ... | ... |
```

3. Ask the user which project(s) to download.

### If project ID provided:
1. Call `mcp__stitch__get_project` to verify it exists and get the title.
2. Proceed to Phase 2.

---

## Phase 2 — Inventory Screens

1. Call `mcp__stitch__list_screens` with the selected project ID.
2. For each screen, extract: `name` (resource name), `title`, `deviceType`, `width`, `height`.
3. Present a screen inventory:

```
## Screens in "[Project Title]"

| # | Screen Title | Device | Dimensions | Cached? |
|---|-------------|--------|------------|---------|
| 1 | Homepage Hero | DESKTOP | 2560×4200 | No |
| 2 | Homepage Mobile | MOBILE | 390×2800 | Yes |
| ... | ... | ... | ... | ... |

Download all N screens? (Y/n)
```

4. If the user confirms, proceed to Phase 3. If they select specific screens, note which ones.

---

## Phase 3 — Download & Organize

### Directory structure
```
.stitch/designs/
  ├── {project-slug}/
  │   ├── _project.json              # Project metadata
  │   ├── {screen-slug}.html         # Full HTML source
  │   ├── {screen-slug}.png          # Full-res screenshot
  │   ├── {screen-slug}.meta.json    # Screen metadata
  │   └── ...
  ├── {another-project-slug}/
  │   └── ...
  └── index.html                     # Browseable gallery (generated in Phase 4)
```

### Slug generation
- Project slug: project title → lowercase, spaces→hyphens, strip special chars. Example: "Homepage Explorations" → `homepage-explorations`
- Screen slug: screen title → lowercase, spaces→hyphens, strip parenthetical suffixes, strip special chars. Example: "Homepage: The Modern Archivist (Full)" → `homepage-the-modern-archivist`

### For each screen:

1. **Call `mcp__stitch__get_screen`** with the screen's resource name to get download URLs, dimensions, and full metadata.

2. **Check local cache** — if `{project-slug}/{screen-slug}.html` already exists and user didn't specify "refresh", skip. Report as "cached".

3. **Download HTML:**
   ```bash
   bash scripts/fetch-stitch.sh "{htmlCode.downloadUrl}" ".stitch/designs/{project-slug}/{screen-slug}.html"
   ```

4. **Download screenshot** — append `=w{width}` to the screenshot URL for full resolution:
   ```bash
   bash scripts/fetch-stitch.sh "{screenshot.downloadUrl}=w{width}" ".stitch/designs/{project-slug}/{screen-slug}.png"
   ```

5. **Save screen metadata:**
   ```json
   {
     "screenId": "projects/{project}/screens/{screen}",
     "title": "Homepage Hero",
     "width": 2560,
     "height": 4200,
     "deviceType": "DESKTOP",
     "projectId": "12345",
     "projectTitle": "Homepage Explorations",
     "fetchedAt": "2026-03-22T14:00:00Z"
   }
   ```

6. **Save project metadata** (once per project) as `_project.json`:
   ```json
   {
     "projectId": "12345",
     "title": "Homepage Explorations",
     "screenCount": 6,
     "fetchedAt": "2026-03-22T14:00:00Z"
   }
   ```

### Progress reporting
After each screen, report:
```
[3/6] ✓ Homepage Hero — 2560×4200 — 142KB HTML, 890KB PNG
```

---

## Phase 4 — Generate Gallery

Create `.stitch/designs/index.html` — a self-contained HTML file (no external dependencies) that presents all downloaded screens as a browseable gallery.

### Gallery features:
- **Project grouping** — screens organized under project headings
- **Thumbnail grid** — PNG screenshots displayed as cards in a responsive CSS grid
- **Screen metadata** — title, device type, dimensions shown on each card
- **Click to view** — clicking a thumbnail opens the full HTML file in a new tab
- **Click to view screenshot** — secondary link to open the full-res PNG
- **Filter by device** — simple toggle buttons for DESKTOP / MOBILE / TABLET
- **Search** — text filter across screen titles
- **Dark background** — designs display best on a neutral dark background
- **Timestamps** — show when each screen was fetched
- **Archive/hide screens** — each card has a ✕ button to archive it (dims + grays out the card, hides by default)
- **Show Archived toggle** — reveals archived screens so they can be restored with ↩
- **Undo** — toast notification with undo for every archive/restore action
- **Persistent state** — archive state saved in localStorage (survives page reload) and optionally in `_hidden.json`
- **Export list** — copies a text list of all archived screen titles + IDs to clipboard for manual Stitch cleanup

### Gallery architecture:

The gallery is a self-contained HTML file with these interactive features:

**Archive/Hide workflow:**
1. Each card has a ✕ button in the top-right corner
2. Clicking it archives the screen — card dims to 35% opacity, grayscales the thumbnail, and shows an "ARCHIVED" label
3. A toast notification appears with an **Undo** button (4-second window)
4. Archived cards are hidden by default — click **Show Archived** in the controls to reveal them
5. Archived screens can be restored with the ↩ button
6. State persists in `localStorage` across page reloads
7. **Export List** copies all archived screen titles + keys to clipboard for manual Stitch cleanup

**Filtering:**
- Device type toggles (All / Desktop / Mobile)
- Text search across screen titles
- Show/hide archived toggle with count badge
- Empty category groups auto-hide

**Data flow:**
- `_manifest.json` (per project) — source of truth for screen metadata, generated during download
- `_hidden.json` (gallery root) — optional file-based persistence of archived screens (can be committed or shared)
- `localStorage['stitch-gallery-hidden']` — browser-side persistence, merged on load

### Building the gallery:
1. Read all `_project.json` files in `.stitch/designs/*/` to get project metadata.
2. Read all `*.meta.json` files in each project directory to get screen metadata.
3. Sort projects alphabetically by title.
4. Within each project, sort screens by: device type (DESKTOP first) then title alphabetically.
5. Populate the template with actual data.
6. Write to `.stitch/designs/index.html`.

---

## Phase 5 — Report

```markdown
## Stitch Download Complete

### Summary
- **Projects:** {count}
- **Screens downloaded:** {count} ({count} new, {count} cached)
- **Total size:** ~{size}

### Projects
| Project | Screens | Directory |
|---------|---------|-----------|
| {title} | {count} | `.stitch/designs/{slug}/` |
| ... | ... | ... |

### Gallery
Open in browser: `.stitch/designs/index.html`

```bash
open .stitch/designs/index.html
```

### Next Steps
- Browse the gallery to review designs
- Use `/stitch-react {projectId} {route}` to convert a screen to React components
- Re-run `/stitch-download {projectId} refresh` to update with new screens
```

---

## Rules

- **Never modify project source code.** This skill only writes to `.stitch/designs/`.
- **Always use `scripts/fetch-stitch.sh`** for downloads. AI built-in fetch fails on Google Cloud Storage signed URLs.
- **Never re-download cached screens** unless the user specifies "refresh". Check for existing files first.
- **Keep the gallery self-contained** — no CDN links, no external CSS/JS. Everything inline in one HTML file.
- **Preserve existing gallery state** — when downloading a new project, merge into the existing gallery rather than overwriting screens from other projects.
- **Handle download failures gracefully** — if a screen fails to download, log it, continue with the next, and include the failure in the report.
- **Respect URL expiration** — Stitch signed URLs expire. If a download fails, note that the user may need to re-list screens to get fresh URLs.
