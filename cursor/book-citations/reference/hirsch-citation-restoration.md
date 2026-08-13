# Cursor Prompt — Restore footnotes & citations, Alan Hirsch English corpus

**Repo:** the one holding Alan Hirsch's source book files
**Database:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`)
**Scope:** 13 English books. 12 source PDFs + 1 EPUB.
**Build slug:** `hirsch-citation-restoration`

---

## ? Runner

Package at `docs/build/prompts/hirsch-citation-restoration/`. Save this as `PROMPT.md`, maintain `STATE.md`. Per phase: announce ? execute ? verify with real counts ? update STATE ? **stop and report**.

**Prime directives:**

- **This is not an LLM task.** Superscript detection is deterministic — font size and baseline offset in the PDF, real markup in the EPUB. Do not send book text to a model to "find the footnotes." It costs a fortune (the corpus is ~1M words) and it will hallucinate placements. Every step here is a script.
- **Never guess a marker position.** A citation attached to the wrong sentence is worse than a missing citation, because it looks authoritative. Below the confidence threshold ? review queue, not the database.
- **Idempotent.** Re-running must not duplicate notes or double-insert markers.
- **Snapshot before every write.** `book_chapters.content` edits go into a `recon` snapshot table first.
- Ask before any destructive change.

---

## The problem

Footnotes were lost or mangled during PDF?Markdown conversion. Current state per book, verified live:

| Book | Body ch. | Note bodies in text | Inline markers | `chapter_notes` rows |
|---|---:|---:|---:|---:|
| The Forgotten Ways | 9 | 160 | 18 | 0 |
| ReFramation | 15 | 30 | 0 | 0 |
| The Forgotten Ways Handbook | 7 | 12 | 37 | 0 |
| Disciplism | 6 | 8 | 3 | 0 |
| Right Here Right Now | 10 | 0 | 18 | 0 |
| Untamed | 10 | 0 | 1 | 0 |
| 5Q | 13 | 0 | 0 | **239 (all empty)** |
| The Permanent Revolution | 13 | 0 | 0 | 0 |
| ReJesus | 8 | 0 | 0 | 0 |
| The Faith of Leap | 9 | 0 | 0 | 0 |
| On the Verge | 11 | 0 | 0 | 0 |
| Metanoia | 9 | 0 | 0 | 0 |
| Fast Forward to Mission | 2 | 0 | 0 | 0 |

Three distinct failure modes:

1. **Notes survived as loose paragraphs, markers lost.** *The Forgotten Ways* has 160 note bodies rendered as `<p><sup>1.</sup> Robert Pirsig highlighted...</p>` but only 18 in-text markers. Note numbering also has gaps (Organic Systems jumps 6 ? 10 ? 13 ? 17), so some notes were dropped entirely.
2. **Notes lost completely.** Eight books have zero notes and zero markers, including *The Permanent Revolution*, *5Q*, *ReJesus* and *The Faith of Leap* — all of which carry substantial apparatus in print. Their citation text is simply gone from the database.
3. **Scaffolded but empty.** *5Q* has 239 `chapter_notes` rows with `marker_present=true`, `definition_present=true`, and **`body` empty on every one**. Something created the shells and never filled them. **Do not treat 5Q as a working reference** — and do not let its row count read as success anywhere.

---

## PHASE 0 — Inventory the sources

1. List every source file, map each to a `books.slug`, and record format (PDF/EPUB), file size, page count.
2. For each PDF, determine whether it has a **real text layer** or is scanned images. `PyMuPDF`: if `page.get_text()` returns almost nothing, it's scanned.
3. **Scanned PDFs are out of scope.** Superscript detection through OCR is unreliable and will produce confident wrong answers. Report them and stop on those.
4. Identify the EPUB. It is the highest-fidelity source — do it first (Phase 2).

**Done when:** a table of 13 books ? source file ? format ? text layer yes/no ? in or out of scope.

---

## PHASE 1 — Extraction library (no database writes)

Build `scripts/citations/` with a clean separation between extraction and loading.

**PDF extractor.** Use `PyMuPDF` (`fitz`) with `page.get_text("dict")` to get every span's text, font size, font name, and bbox.

- Compute the **modal body font size** per page.
- A superscript span is: font size ? 60—80% of body size, **and** baseline raised relative to adjacent spans on the same line, **and** content matching `^\d{1,3}$`.
- Note *bodies* live in a smaller font at the page foot, or in an endnotes section — capture both.
- For each marker, capture **60 characters of preceding text** as an anchor. That anchor is what matching depends on; keep it verbatim including punctuation.

**EPUB extractor.** Far easier and more reliable: parse with `ebooklib` + `BeautifulSoup` and read the real markup — `<a epub:type="noteref">`, `<sup>`, `id`/`href` pairs. The anchor is exact, not fuzzy. Treat EPUB output as ground truth and use it to validate the PDF extractor's behaviour.

**Output** a per-book JSON: `{book_slug, chapter_hint, note_number, marker_anchor_text, note_body, source_page}`. Write these to `data/citations/{slug}.json` and commit them. The extraction is then reproducible without re-reading the sources.

**Done when:** JSON exists for every in-scope book, and the EPUB's numbers reconcile against its own note list exactly.

---

## PHASE 2 — Match to the database

For each extracted marker, find its position in the existing `book_chapters.content`.

1. Resolve the chapter: match extracted chapter titles to `book_chapters` where `section_role='body'`, using `sort_order` as a tiebreak. **Do not use `chapter_number` from the source** — the database numbering was corrected separately and is authoritative.
2. Normalise both sides for matching: strip HTML, collapse whitespace, normalise smart quotes and dashes.
3. Locate the 60-char anchor in the normalised chapter text. Use exact match first, then `rapidfuzz` ratio.
4. Record a **confidence score** per match: exact = 1.0, fuzzy = the ratio.
5. **Thresholds:** ? 0.95 auto-apply — 0.80—0.95 review queue — < 0.80 reject and report.
6. Ambiguity check: if the anchor matches more than one location in the chapter, **reject regardless of score**. A repeated phrase means we cannot know which occurrence carried the note.

**Done when:** a match report per book — auto / review / reject counts — with `The Forgotten Ways` reconciled against its known 160 note bodies.

---

## PHASE 3 — Load

Two writes, both idempotent.

**1. `chapter_notes`** — one row per note:
`organization_id`, `chapter_id`, `note_scope='chapter'`, `note_number`, `note_type` (`footnote` | `endnote`), `body` (the note text — **never empty**; an empty body is the 5Q bug), `marker_present`, `definition_present`, `parsed_csl` (parse with `citeproc`/`anystyle` where the note is a bibliographic reference; leave null otherwise — do not invent CSL), `data_quality_flags` for anything odd.

Upsert on `(chapter_id, note_number)`.

**2. Inline markers in `book_chapters.content`** — insert `<sup class="noteref" data-note="N">N</sup>` at the matched offset, only for matches ? 0.95.

- Snapshot content to `recon.snap_chapter_content_citations` first.
- Skip if a marker for that note already exists — re-running must be a no-op.
- Remove the now-redundant loose `<p><sup>N.</sup> …</p>` note-body paragraphs **only** where the note has been successfully written to `chapter_notes`, so nothing is deleted before it is preserved.

**Fix 5Q explicitly:** its 239 empty rows must either be filled from extraction or deleted. Do not leave empty-bodied notes in the table.

**Done when:** `chapter_notes` is populated with non-empty bodies; markers render; re-running the whole pipeline changes zero rows.

---

## PHASE 4 — Review queue

Everything between 0.80 and 0.95, plus every rejection, goes into `recon.citation_review_queue`: book, chapter, note number, note body, proposed anchor, candidate offsets, confidence, reason.

Build the smallest possible reviewer: show the note, show the candidate sentence, accept or reject. Accepting applies the same insert as Phase 3.

**Done when:** the queue is populated and a human can clear an item in a few seconds.

---

## PHASE 5 — Verify

- Per book: notes extracted vs matched vs applied vs queued vs rejected.
- Numbering gaps per chapter — a chapter running 1,2,3,6,7 means notes 4 and 5 were lost at conversion; report rather than renumber.
- Spot-check five known cases in *The Forgotten Ways*, including the Pirsig note in Organic Systems.
- Confirm nothing regressed: `v_chapter_text_quality` gains no rows, running-head counts stay at zero.

---

## PHASE 6 — Fix the pipeline, not just the data

**This is the point of the exercise.** Repairing 13 books by hand while the converter keeps dropping markers on the next book is the wrong order.

Update the book conversion path (`book-convert` / Phase 01 of the books pipeline) so that footnote markers and bodies are preserved on ingest: emit `<sup class="noteref">` in content and populate `chapter_notes` in the same run. Add a post-convert assertion that fails the job when a book yields note bodies but no markers — the exact signature of this bug.

**Done when:** a re-ingest of one book produces correct notes with no repair step.

---

## Notes on judgement

- If a book's source PDF turns out to be a scan, say so and stop. Do not OCR-and-hope.
- If extracted note count differs wildly from what's in the database (e.g. 160 bodies but 40 extracted), the source file is probably a different edition. Check `books.isbn` and report — do not force a match.
- Gaps in note numbering are **findings, not errors to smooth over**. Report them; never renumber to make a sequence look continuous.
