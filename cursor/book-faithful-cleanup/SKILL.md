---
name: book-faithful-cleanup
description: >-
  Faithful PDF/EPUB → movemental chapter Markdown conversion and cleanup: seed-from-corpus,
  repair-from-db, or convert-from-source; fidelity audit; deterministic repairs; Cursor /loop
  until READY_FOR_LOAD; Phase 5 citations (book-citations); optional Supabase load. Use when
  converting a book, running book-faithful-cleanup, pymupdf4llm convert, defect remediation,
  or iterating cleanup until perfected — never paraphrase source text.
disable-model-invocation: true
---

# Book faithful cleanup

One-book hybrid recipe: **deterministic extract/repair** + **Cursor `/loop`** until gates pass,
with **citations integrated** (see skill `book-citations`). Source text is sacred — copy
verbatim from the PDF/EPUB oracle; never invent wording, footnotes, or summaries.

**Primary repo:** books workspace (`docs/prompts/book-faithful-cleanup/`, `scripts/citations/`)  
**Database:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`) — ask before destructive writes  
**Formatting exemplar:** `movemental-docs/.../alan-hirsch/the-church-as-movement/`  
**Full recipe:** [reference/PROMPT.md](reference/PROMPT.md)  
**Defect sweep:** [reference/REMEDIATION.md](reference/REMEDIATION.md)  
**STATE template:** [reference/STATE.template.md](reference/STATE.template.md)

## Invocation

```
/book-faithful-cleanup {book_slug}                 # full Phases 0–7 (stop between phases unless continue)
/book-faithful-cleanup {book_slug} convert         # mode=convert-from-source
/book-faithful-cleanup {book_slug} loop            # Phase 4 /loop until READY_FOR_LOAD or NEEDS_HUMAN
/book-faithful-cleanup {book_slug} remediate       # REMEDIATION.md taxonomy sweep
```

Copy STATE template → `docs/prompts/book-faithful-cleanup/STATE.md` (or `STATE.{slug}.md`).
Per phase: **announce → execute → verify with real counts → update STATE → stop and report**
unless the user said continue / arm the loop.

## Hybrid lanes

| Lane | Owner | May do |
|------|--------|--------|
| Deterministic | Python (`fitz`, `pymupdf4llm`, `ebooklib`, `scripts/citations/*`) | Extract, strip chrome, measure fidelity, assert gates, emit SQL/JSON |
| Non-deterministic | Cursor agent + `/loop` | Merge SP, heading hierarchy, ambiguous layout, residual citations from review queue — **against source only** |

## Prime directives

1. **Imported corpus first, PDF/EPUB as completeness + citation oracle.** Prefer `data/corpus/.../{slug}/` when present; never “improve” wording.
2. **Match the formatting exemplar** (layout, YAML, `<!-- page: N -->`, headings) — not a third house style.
3. **Citations are not an LLM guess** — use `book-citations` / `scripts/citations/*`.
4. **One book at a time.** Finish gates before the next slug.
5. **Idempotent + snapshotted.** No duplicate markers/notes; snapshot before DB writes.
6. **No truncation / silent deletion.** Unverifiable → queue, do not drop.
7. Ask before destructive DB changes.

## Mode selection

1. Seed chapters exist under corpus → **`seed-from-corpus`**
2. Else book in Supabase with usable chapters → **`repair-from-db`**
3. Else → **`convert-from-source`** (pymupdf4llm → corpus MD + citation hook → audit → loop → load)

Scanned PDF (no text layer): **stop**.

## Progress checklist

```
book-faithful-cleanup:
- [ ] 0 Choose mode; STATE; seed/export/inventory; completeness gaps
- [ ] 1 Ground-truth extract (pymupdf4llm + fitz + citation JSON + chapter_map)
- [ ] 2 Fidelity audit → audit.json + taxonomy_totals
- [ ] 3 Deterministic repairs → remediation_patterns.json; re-audit
- [ ] 4 /loop until READY_FOR_LOAD or NEEDS_HUMAN
- [ ] 5 Citation integration (skill book-citations)
- [ ] 6 Load to Supabase (if asked) — snapshot first
- [ ] 7 Final gates G1–G8; mark complete
```

---

## Phase map (summary)

| Phase | What | Stop? |
|------:|------|-------|
| 0 | Inputs, mode, working tree under `data/cleanup/{slug}/` | Yes |
| 1 | Body + citation extract; `source/chapter_map.json` | Yes |
| 2 | Coverage / truncation / taxonomy audit | Yes — no edits yet |
| 3 | Mechanical RH/FO/HY/loose-notes/high-confidence CIT | Yes |
| 4 | `/loop` source-bound cleanup | When READY or NEEDS_HUMAN |
| 5 | Full citation reconcile (extract → match → notes → noteref) | Yes |
| 6 | MD→HTML load by chapter `id` | Yes |
| 7 | Gates G1–G8 | Book complete |

### Working tree shape

```text
data/cleanup/{book_slug}/
  book.json
  chapters/*.md          # YAML + Markdown + <!-- page: N -->
  source/                # oracle pages + chapter_map
  db/notes/              # citation bodies (preserve)
  audit.json
  remediation_patterns.json
  READY_FOR_LOAD         # loop success sentinel
```

### Validation thresholds (exemplar)

| Gate | Threshold |
|------|-----------|
| Word drift (book) | ≤ 2% |
| Per-page fuzzy | ≥ 0.95 (prefer ≥ 0.99) |
| 5-gram coverage | ≥ 0.99 (boundary caveat) |
| Embed / TF-IDF cosine | ≥ 0.97 |

### Defect taxonomy (must clear or STATE-waive)

`RH` `FO` `HY` `SP` `CIT` `IMG` `ENC` `LAY` `TOC` `TR` `BL` `LIST` `META`  
Evidence: `docs/problem-examples/`, `docs/problem-examples-two/`. Focused pass: [reference/REMEDIATION.md](reference/REMEDIATION.md).

---

## Phase 4 — Iterative loop until perfected

Use Cursor **`/loop`** (loop skill). Prefer dynamic wake on `audit.json` / chapter file changes; Windows PowerShell `Start-Sleep` fallback; sentinel `AGENT_LOOP_TICK_book_cleanup_{slug}`.

### Loop body (paste)

```text
Book: {book_slug}
Working tree: data/cleanup/{book_slug}/   (corpus Markdown + book.json)
Seed (if any): data/corpus/.../{book_slug}/  (starting body only)
Format exemplar: movemental-docs/.../the-church-as-movement/
Oracle: data/cleanup/{book_slug}/source/
Audit: data/cleanup/{book_slug}/audit.json
Notes: data/cleanup/{book_slug}/db/notes/  (do not drop)
Taxonomy: RH FO HY SP CIT IMG ENC LAY TOC TR BL LIST META
Evidence: docs/problem-examples/ + docs/problem-examples-two/

On each tick:
1. Load audit.json; pick unclean chapter with highest severity
   (TR/BL/missing_section > CIT missing notes > SP/HY-incomplete/ENC >
   RH/FO/LAY > CIT markers > LIST/IMG > META).
2. Open that chapters/*.md + exemplar style + matching source page range only.
   Prefer patching seed text; copy missing spans verbatim from oracle.
3. Fix ONE taxonomy code (or one chapter×code) at a time. Allowed:
   merge SP; restore drop-cap/hyphen halves from oracle; fill gaps; strip chrome;
   move bleed/TOC stumps; fix LIST from source; ##/### + <!-- page: N -->;
   re-place citation markers from JSON; unspace note URLs —
   never rewrite sentences; never invent PENDING-REVIEW or footnote bodies.
4. Run local checks (drift/coverage, taxonomy_totals, notes+markers, sha256).
5. Update audit.json + STATE.md.
6. If all clean → write READY_FOR_LOAD and stop.
7. If same chapter×code fails 3 ticks → NEEDS_HUMAN and stop.
```

### Hard rules inside the loop

- Verbatim oracle copy only; ambiguous edition → ask.
- Citation matches &lt; 0.95 → review queue (`book-citations`), not auto-accept.
- Do not renumber notes to hide gaps.
- Do not merge/split DB chapters without updating `chapter_map` + asking when live IDs change.
- Refresh `audit.json` / `taxonomy_totals` every tick — loop without gates = infinite polish.

---

## Phase 5 — Citations (required)

Even when body looks clean, seed/exemplar Markdown is **not** citation-complete.

1. Run skill **`book-citations`** for this slug (extract → form → match → notes → compile/assert).
2. Wire `convert_hook` for future re-ingest.
3. Record extract vs applied vs residuals in STATE.

Staging MD uses `[^n]`; loaded HTML uses noteref + `chapter_notes`. Do **not** treat corpus `chNN-notes.md` + empty `citations: []` as the final movemental model.

---

## Phase 7 — Final gates

| Gate | Check |
|------|--------|
| G1 Faithfulness | Drift/fuzzy/coverage; no truncation |
| G2 Structure | `book.json` + chapters; DB roles coherent |
| G3 Format parity | YAML, headings, page comments, no drop-cap loss |
| G4 Citations | Non-empty notes; markers; `assert_notes_markers` green |
| G5 Quality view | split-paragraph / pdf_edition flags clean or waived |
| G6 Idempotence | Re-audit → zero unclean |
| G7 No chrome | RH/FO/LAY clear |
| G8 Taxonomy | Totals clear or STATE-waived |

Only then accept the next `book_slug`.

## Anti-patterns

- Skipping corpus seed when it exists and re-converting from PDF (destroys citation work)
- Treating seed MD as citation-complete
- Inventing footnotes, CSL, or `[PENDING-REVIEW]` author-voice abstracts
- Loop without refreshing audit gates
- Loading without `recon` snapshot
- Editing only Supabase HTML while ignoring corpus Markdown contract

## Quick start

```text
1. STATE from template; set book_slug + source_path
2. Pick mode (seed → repair-from-db → convert-from-source)
3. Open exemplar the-church-as-movement
4. Phases 0–3 with stop/report
5. /loop Phase 4 until READY_FOR_LOAD
6. book-citations Phase 5; load if asked; gates G1–G8
```

## Additional resources

- Full Phases 0–7 detail: [reference/PROMPT.md](reference/PROMPT.md)
- Loop paste body (+ remediation loop): [loop-prompt.md](loop-prompt.md)
- Condensed defect sweep: [remediation.md](remediation.md)
- Full remediation recipe: [reference/REMEDIATION.md](reference/REMEDIATION.md)
- STATE template: [state-template.md](state-template.md) (also under `reference/`)
- Citations-only workflow: skill `book-citations`
