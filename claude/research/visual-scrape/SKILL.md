---
name: visual-scrape
description: Extract visuals (charts, diagrams, illustrations) from a PDF book and generate contextual markdown — each image paired with what it communicates and why it matters in context. Use when scraping book visuals.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Extract visuals from a PDF book and contextualize them: $ARGUMENTS

$ARGUMENTS should be a path to a PDF file. Optionally include:
- `--pages 1-50` to limit to a page range
- `--vectors` to also capture vector diagrams (rendered as full-page PNGs)
- `--output-dir path/to/dir` to control where images land

If no arguments are given, ask the user for the PDF path.

---

## Step 1 — Extract Images

Run the Python extraction script:

```bash
python3 /Users/joshuashepherd/Desktop/Dev/repos/movemental-content-studio/.claude/skills/visual-scrape/extract_visuals.py "<pdf_path>" [flags]
```

This produces:
- A folder of PNG/JPG image files
- A `manifest.json` listing every extracted visual with page number, type, and dimensions

Report to the user: how many visuals were found, from how many pages.

If zero visuals are found with default settings, retry with `--vectors` flag to capture vector-drawn diagrams. Let the user know you're doing this.

---

## Step 2 — Contextualize Each Visual

For each visual in the manifest, read the PDF page where the visual appears (and the page before/after for context) using the Read tool.

For each visual, determine:

1. **Visual Type** — Chart, diagram, table, illustration, framework, model, photograph, map, infographic, timeline, or other
2. **Description** — What the visual literally shows (shapes, labels, relationships, data)
3. **The Point** — What argument, insight, or concept the visual supports in context of the surrounding text. This is the most important field — it answers "why is this here?"
4. **Chapter/Section** — Which chapter or section the visual belongs to (from headers or running text)
5. **Caption** — The original caption if one exists near the visual, or "[no caption]"
6. **Suggested Alt Text** — A concise accessibility description

---

## Step 3 — Generate Markdown Output

Create a markdown file in the output directory called `visuals.md` with this structure:

```markdown
# Visuals — [Book Title]

> Extracted from `[filename.pdf]` — [N] visuals from [M] pages

---

## [Chapter/Section Name]

### Page [N] — [Visual Type]

![Description](./[filename].png)

**Original Caption:** [caption or "none"]

**What it shows:** [literal description of the visual]

**The point:** [contextual argument — why this visual matters, what it proves or illustrates in the author's argument]

**Alt text:** [suggested alt text]

---
```

Group visuals by chapter/section when possible. Order by page number within each group.

---

## Step 4 — Summary

End by printing a summary:
- Total visuals extracted and contextualized
- Breakdown by visual type (e.g., "5 diagrams, 3 charts, 2 illustrations")
- Any pages where vector content was detected but not extracted (suggest `--vectors` if not already used)
- The path to `visuals.md` and the image folder

---

## Notes

- **Large PDFs**: For books over 100 pages, suggest processing in chapter ranges (e.g., `--pages 1-30`) to keep context reads manageable
- **Image quality**: Embedded images extract at original resolution. Vector renders are at 2x page resolution.
- **Min size filter**: Images smaller than 100px in either dimension are skipped (icons, bullets, decorations). If the user is missing expected visuals, suggest `--min-size 50`.
- **The "point" is the value**: Anyone can rip images from a PDF. The contextual analysis of what each visual argues is what makes this skill useful. Spend time on Step 2.
