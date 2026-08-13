# Cursor Prompt — Faithful book cleanup (PDF/EPUB → movemental chapters)

**Repo:** sources + `scripts/citations/` live here  
**Database:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`)  
**Scope:** **One book per run.** Re-apply this recipe for every PDF or EPUB.  
**Build slug:** `book-faithful-cleanup-<book-slug>-YYYYMMDD`  
**Companion:** citation restoration at `Alan Hirsch/docs/build/prompts/hirsch-citation-restoration/` (already completed for the Hirsch English corpus)  
**Defect remediation (same taxonomy, focused pass):** [`REMEDIATION.md`](REMEDIATION.md) — use for post-cleanup sweeps or corpus-only repairs; Phases 2–4 below already embed this taxonomy so new books do not skip it  
**Defect evidence catalogs:** [`docs/problem-examples/`](../../problem-examples/), [`docs/problem-examples-two/`](../../problem-examples-two/)  
**Imported corpus seed (check first):**  
`data/corpus/alan-hirsch/{book-slug}/`  
    (plus `_index/`, `_meta/`, `_archive/` under `data/corpus/alan-hirsch/`)  
**Formatting reference (canonical structure):**  
`C:\Users\Josh\Desktop\movemental-docs\docs\library\corpus\alan-hirsch\`  
    (exemplars: `the-church-as-movement`, `spent-matches`, and peer book folders — **body/structure only**; see citation divergence below)

---

## Runner

Package at `docs/prompts/book-faithful-cleanup/`. Save this as `PROMPT.md`, maintain `STATE.md` for the active book. Per phase: announce → execute → verify with real counts → update STATE → **stop and report** before the next phase unless the user says continue.

This recipe is intentionally **hybrid**:

| Lane | Owner | What it may do |
|------|--------|----------------|
| **Deterministic** | Python (`PyMuPDF` / `fitz`, `pymupdf4llm`, `ebooklib`+`BeautifulSoup`, existing `scripts/citations/*`) | Extract text, detect superscripts, strip running heads, measure fidelity, assert gates, emit SQL/JSON |
| **Non-deterministic** | Cursor agent (+ `/loop`) | Merge split paragraphs, fix heading hierarchy, reconcile ambiguous layout, place residual citations from the review queue, judge edge cases **against source text only** |

**Prime directives:**

1. **Imported corpus first, PDF/EPUB as completeness oracle.** For Hirsch books under `data/corpus/alan-hirsch/{book-slug}/`, seed the working tree from that Markdown **before** re-exporting from Supabase or re-converting from scratch. The PDF/EPUB remains ground truth for **missing chapters, truncated tails, drop-caps, and citation markers/bodies** — never “improve” wording, never paraphrase, never invent missing sentences.
2. **Match the formatting exemplar** for structure and prose layout (movemental-docs section below). Do not invent a third house style.
3. **Citations are not an LLM guess.** Marker detection stays in `scripts/citations/pdf_extract.py` / `epub_extract.py` (PyMuPDF span geometry / EPUB markup). Finish citations from PDF extract + prior `data/citations/{slug}.json` / DB notes — do not send chapter text to a model to invent footnote positions.
4. **One book at a time.** Finish gates for book *N* before starting *N+1*.
5. **Idempotent + snapshotted.** Snapshot `book_chapters.content` (and notes) into `recon.*` before every write. Re-running must not duplicate markers or notes.
6. **No truncation, no silent deletion.** If text cannot be verified against source, queue it — do not drop it.
7. **Ask before destructive DB changes** (delete chapters, replace entire book, wipe notes).

---

## Canonical formatting example (movemental-docs corpus)

Treat the cleaned books under

`C:\Users\Josh\Desktop\movemental-docs\docs\library\corpus\alan-hirsch\{book-slug}\`

as the **house format for chaptered book text**. Best structural exemplar: `the-church-as-movement` (`conversion_engine: pymupdf4llm-0.0.27`). Also usable: `spent-matches` and other peer folders.

### On-disk layout to emit / repair toward

```text
{book-slug}/
  book.json                 # catalog + per-chapter index
  chapters/
    ch00-front-matter.md
    ch00b-contents.md       # optional extras with letter suffixes
    ch01-foreword.md
    ch02-introduction.md
    part-1-{slug}.md        # section dividers as their own files
    ch03-{chapter-slug}.md  # body chapters
    …
    chNN-epilogue.md
    chNN-acknowledgments.md
    chNN-notes.md           # endnote *apparatus file* in corpus examples
  .ingest/                  # optional validation artifacts
    validation-*.json
    frontmatter-*.json
```

### `book.json` contract (mirror the exemplar)

Required spirit of fields (see `the-church-as-movement/book.json`):

- Book: `book_slug`, `canonical_title`, `display_title`, `subtitle`, `author`, `co_authors`, `year`, `publisher`, `isbn`, `language`
- Totals: `total_chapters` (body chapter count), `total_word_count`, `total_char_count`
- Provenance: `source_type` (`pdf`|`epub`), `conversion_engine` (prefer `pymupdf4llm-<version>`), `corpus_path`, `tenant`, `pipeline_version`, `last_validated_at`
- `chapters[]`: `chapter_number`, `chapter_slug`, `chapter_title`, `content_class`, `file`, `word_count`, `page_range_start`, `page_range_end`

`content_class` values used in the exemplar: `front-matter` | `chapter` | `back-matter` | `notes` | `appendix` (and peers). Map these onto Supabase `section_role` + `content_class` at load time (below).

### Chapter Markdown contract (YAML + body)

Every chapter file:

1. **YAML frontmatter** with at least: `canonical_title`, `book_slug`, `chapter_number`, `chapter_slug`, `chapter_title`, `display_title`, `content_class`, `source_type`, `language`, `word_count`, `char_count`, `estimated_reading_time`, `page_range_start`, `page_range_end`, `content_sha256`, plus book-level `author` / `isbn` / `tenant` as in the exemplar.
2. **Body** after `---`:
   - Title line: `## {N}. {Title}` for numbered body chapters, or `## {Title}` for front/back matter.
   - Page anchors: `<!-- page: {n} -->` at page boundaries (1-based print pages as in exemplar).
   - Prose in plain Markdown paragraphs (blank-line separated) — **not** one giant HTML blob while cleaning.
   - Epigraphs as Markdown blockquotes (`>`), attribution on following quote lines.
   - Subheads as `### {N}.{M} {Heading}` (or `###` without numbers when the source has unnumbered subheads).
   - Emphasis with `*…*` / `**…**` matching source italics/bold — do not invent emphasis.
3. **No running heads, folios, or PDF chrome** in the body.
4. **No mid-sentence paragraph splits** from line wraps; join soft hyphens; restore drop-caps (exemplar still shows rare `on’t` missing leading `D` — treat that class of defect as **must-fix** against source).

Open an exemplar chapter beside the work chapter when judging heading level, epigraph shape, or part-divider brevity (`part-1-distributing.md` is intentionally tiny).

### Validation thresholds (from exemplar `.ingest/validation-*.json`)

Reuse these as deterministic gates where possible:

| Layer | Threshold | Notes |
|-------|-----------|--------|
| Word drift (book) | ≤ **2%** (`word_drift: 0.02`) | Exemplar passed at ~0.44% |
| Per-page fuzzy | ≥ **0.95** (prefer ≥0.99) | Sampled pages vs source |
| 5-gram coverage | ≥ **0.99** | File-boundary 5-grams may false-fail; confirm with fuzzy/embed before failing the book |
| Embed / TF-IDF cosine | ≥ **0.97** | Per body chapter vs source page span |

### Citation divergence (important)

The corpus examples often keep apparatus as a trailing `chNN-notes.md` with Pandoc-style `[^id]:` definitions and an empty `citations: []` in frontmatter. **That is not the target citation model for Hirsch / movemental DB books.**

For this cleanup recipe:

- **Do** match the corpus for: folder layout, `book.json`, YAML frontmatter, Markdown body structure, page comments, heading levels, part files, fidelity gates.
- **Do not** treat corpus endnote files as the final citation design for Hirsch.
- **Instead** integrate the already-built citation pipeline: non-empty `chapter_notes` rows + inline `<sup class="noteref" data-note="N">N</sup>` in the HTML that lands in Supabase (and equivalent markers when staging Markdown — e.g. `[^N]` only as a temporary bridge if needed, then compile to `chapter_notes` + noteref on load).
- Corpus `citations: []` / notes chapters are a formatting reference for **prose**, not a license to drop restored Hirsch footnotes.

---

## Recommendation: start from imported corpus, then PDF-cross-ref

### Hirsch books with a seed under `data/corpus/alan-hirsch/{book-slug}/`

**Prefer: `mode=seed-from-corpus`.** Copy/normalize the imported chapter Markdown into `data/cleanup/{book_slug}/`, then use the PDF/EPUB only as a **cross-reference** to:

1. **Completeness** — detect missing chapters/sections (seed folders are often body-only; e.g. metanoia seed may omit a chapter the PDF has), truncated endings, drop-caps, chrome still in body.
2. **Citations** — finish markers + `chapter_notes` from PDF/EPUB extract (`scripts/citations/*`) and any prior `data/citations/{slug}.json` / live DB notes. Do **not** treat seed Markdown as citation-complete.

Also pull live Supabase chapter IDs + notes in Phase 0 so load maps by `id` and citation work is not wiped.

**Seed → corpus-shaped working tree → PDF oracle + citation extract → audit gaps → loop → load.**

### Alan Hirsch English books already in `movemental` but **no** local seed

**Prefer: export chapters + notes from Supabase** (`mode=repair-from-db`), normalize into the corpus Markdown shape, then repair against source PDF/EPUB (same completeness + citation finish rules).

Reasons:

- Chapter boundaries (`section_role`, `content_class`, `sort_order`) are already close to the desired chunking.
- Citation restoration (`hirsch-citation-restoration`) already loaded non-empty `chapter_notes` and many `<sup class="noteref">` markers. A full re-ingest from PDF would risk wiping that work.
- Remaining defects are mostly **PDF-conversion residue**.

### Brand-new books (not in seed corpus, not yet in DB, or irreparably mangled)

**Prefer: deterministic `pymupdf4llm` convert → corpus Markdown + `book.json` → citation hook → Cursor loop → Supabase load** (`mode=convert-from-source`).

Only choose full re-ingest for an existing Hirsch book if Phase 0 fidelity audit shows catastrophic loss (wrong edition, scanned OCR soup, or chapter map that cannot be reconciled). Ask the user before replacing live rows.

### Seed inventory (imported)

Present under `data/corpus/alan-hirsch/`:

| Path | Role |
|------|------|
| `{book-slug}/` | Chapter Markdown + `{slug}-book.json` starting points |
| `_index/` | Catalog / vector index helpers |
| `_meta/` | Book metadata + canonical terms |
| `_archive/` | Prior pre-convert snapshots (reference only; do not seed from archive unless asked) |

Book folders currently seeded: `5q`, `fast-forward-to-mission`, `metanoia`, `on-the-verge`, `reframation`, `rejesus`, `right-here-right-now`, `the-faith-of-leap`, `the-forgotten-ways`, `the-forgotten-ways-handbook`, `the-permanent-revolution`, `the-shaping-of-things-to-come`.

---

## Target movemental shape (two layers)

### Layer A — Working corpus (match formatting example)

Local tree under `data/cleanup/{book_slug}/` (seeded from `data/corpus/alan-hirsch/{book_slug}/` when present, and optionally published back into movemental-docs corpus when asked) must look like the exemplar: `book.json` + `chapters/*.md` with YAML + Markdown body + `<!-- page: N -->`.

### Layer B — Supabase (`movemental`)

| Table | Role |
|-------|------|
| `books` | One row; `slug` is the stable key |
| `book_chapters` | **One row per logical section** (same grain as corpus chapter files). `content` is HTML derived from cleaned Markdown |
| `chapter_notes` | Footnotes/endnotes; `body` **never empty**; `note_type` ∈ `footnote` \| `endnote` \| `sidenote` |

Map corpus → DB:

| Corpus | Supabase |
|--------|----------|
| `content_class: front-matter` | `section_role=front_matter`; refine `content_class` to `title_page` / `foreword` / `preface` / `introduction` / … when known |
| `content_class: chapter` | `section_role=body`, `content_class=chapter` |
| `content_class: back-matter` | `section_role=back_matter`; refine to `conclusion` / `afterword` / `epilogue` / … |
| `content_class: notes` | Prefer **not** storing a giant notes HTML chapter as the only apparatus for Hirsch; load into `chapter_notes` + noterefs. A slim `content_class=notes` row is optional only if product UI still expects it |
| `content_class: appendix` | `section_role=back_matter`, `content_class=appendix` |
| part divider files | `section_role=section_divider`, `content_class=section_divider` |
| Markdown headings / paragraphs / blockquotes | HTML `h1`/`h2`/`h3`, `<p>`, `<blockquote>`, `<em>` |
| Inline note markers | `<sup class="noteref" data-note="N">N</sup>` |

Also maintain: `sort_order` (authoritative reading order), `page_start` / `page_end` from frontmatter, `text_quality_flags` / `data_quality_flags`. Goal: clean `v_chapter_text_quality` for the book (`splitParagraphCandidates`, `runningHeadsRemoved`, `pdf_edition_flags`).

---

## Libraries (deterministic stack)

Do **not** introduce a second PDF stack. Stay on Artifex PyMuPDF:

| Job | Library | Module / usage |
|-----|---------|----------------|
| Low-level spans, superscripts, footnote geometry | **PyMuPDF** (`import fitz`) | `scripts/citations/pdf_extract.py` — `page.get_text("dict")` |
| Faithful body Markdown/text with reading order, header/footer options | **pymupdf4llm** | `pymupdf4llm.to_markdown(..., page_chunks=True)`, prefer `header=False` / `footer=False` (or DetectHeaders margins) so running heads are not baked into body text |
| EPUB body + notes | **ebooklib** + **BeautifulSoup** (`lxml`) | `scripts/citations/epub_extract.py` for notes; spine XHTML for body |
| Matching / normalize | existing helpers | `scripts/citations/normalize.py`, `match.py`, `load.py` |
| Post-convert assertion | existing | `scripts/citations/assert_notes_markers.py`, `convert_hook.py` |
| Fuzzy residual match only | `rapidfuzz` (already used in citation match) | Never below documented confidence thresholds for auto-apply |

Install if missing (project venv):

```bash
pip install pymupdf pymupdf4llm ebooklib beautifulsoup4 lxml rapidfuzz
```

Scanned PDFs with no text layer: **out of scope** for auto-cleanup (same rule as citation restoration). Report and stop.

---

## Known conversion failure modes (fix for)

Cursor loop work is allowed only for these classes of defects, always with source-side evidence. Stable audit codes in parentheses map to [`REMEDIATION.md`](REMEDIATION.md) and the problem-example inventories.

1. **Split paragraphs** (`SP`) — mid-sentence breaks from PDF line wraps / column breaks (Forgotten Ways–scale shredding).
2. **Drop-caps / missing first letters** (`ENC`) — e.g. `on’t` ← `Don’t`; Metanoia-style `Te` / `T ey` / `of en` from Th/fi ligature or drop-cap loss — restore only from oracle.
3. **Running heads / page numbers** (`RH`, `FO`) leaked into body — forms seen in corpus:
   - Folio + book/chapter title (`76 the permanent revolution`, `…church 75`)
   - `Introduction N` chrome (Forgotten Ways)
   - Repeating `## PARADIGM` / `## PLATFORMED` / `## NOTES` mid-sentence (Metanoia)
   - Letter-spaced / tracked headers (`Pu t t in g O ur H e ar t s…`, `M oving the M oon 5`)
   - Untamed-style repeating section labels (`the untamed god`)
   - Bare folio lines; trailing head digits (ReJesus `### Title 3`)
4. **Hyphenation artifacts** (`HY`) — soft hyphens (`U+00AD`), `Christ-` + newline + `ianity`; when the second half is **missing**, oracle-restore (not delete).
5. **Ligature / encoding / escape glitches** (`ENC`) — PUA bullets (Metanoia), body `\[…\]` escapes (5Q EPUB→MD) — fix from source / safe unescape, not by guessing.
6. **Missing or misplaced noteref markers** (`CIT`) — glued `.N` / stuck `word12`, orphan `[^n]` without defs, caret `^[n]`, spaced URLs in notes, `[^n](Ibid.)` malformations — integrate from `data/citations/{slug}.json` + match pipeline; residuals stay in review queue.
7. **Loose note-body paragraphs** (`CIT`) still in content after notes were moved to `chapter_notes`.
8. **Truncation / missing halves** (`TR`) — chapter ends before source ends; mid-URL cuts; hyphen shreds with no continuation.
9. **Format drift from exemplar** — missing YAML, missing `<!-- page: N -->`, wrong heading levels, HTML left unconverted; TOC `<br>` soup (`LAY`); `[PENDING-REVIEW]` summary stubs (`META`) — list and resolve deliberately (do not invent author-voice abstracts).
10. **Wrong section role / over-chunking / bleed** (`BL`, `TOC`) — pages stored as chapters; next-chapter stumps at file tails (Verge); index/authors dumped into body (Permanent Revolution ch04); notes files carrying body-chapter YAML identity (Faith of Leap).
11. **Column / diagram OCR mixups** (`LAY`) — multi-column models linearized wrong; APEST letter dumps as fake paragraphs — rebuild only against PDF figure/oracle.
12. **List marker corruption** (`LIST`) — repeated wrong indices (ReJesus all `- 3`) — restore from source numbering.
13. **Images** (`IMG`) — verify paths resolve (missing files were **not** the Hirsch-seed failure mode); flag empty alts; drop chrome/marker screenshots only with PDF review — do not invent alt text in the deterministic lane.

**Not** failure modes to “fix creatively”: theological wording, spelling that matches the source edition, intentional fragment paragraphs (epigraphs, one-line quotes), intentional repeated section heads that are real structure (confirm against oracle before stripping).

---

## PHASE 0 — Choose book + starting baseline

### Inputs (fill in STATE)

- `book_slug`
- `source_path` (PDF or EPUB on disk) — **always required** for completeness + citations cross-ref
- `corpus_seed_path` — `data/corpus/alan-hirsch/{book_slug}/` when present (check this first)
- `organization_id` / project id `vhaiiiykcukrlyvwlgip`
- `mode`: `seed-from-corpus` | `repair-from-db` | `convert-from-source`

**Mode selection (deterministic):**

1. If `data/corpus/alan-hirsch/{book_slug}/` has chapter `.md` files → **`seed-from-corpus`**
2. Else if book exists in Supabase with usable chapters → **`repair-from-db`**
3. Else → **`convert-from-source`**

### 0A. If `seed-from-corpus` (default when seed exists)

**Check the imported seed first.** Do not skip straight to PDF convert or DB export for body text.

1. Inventory seed files: `{slug}-book.json` / `book.json`, chapter `*.md`, images if any. Record count in STATE.
2. Compare seed chapter list to PDF/EPUB TOC (or page heuristic) **and** to live Supabase `book_chapters` when the book is already loaded — list **missing / extra / out-of-order** sections in STATE (`completeness_gaps`).
3. Copy seed into the working tree (normalize filenames toward exemplar `chapters/chNN-….md` layout as needed):

```text
data/cleanup/{book_slug}/
  book.json                   # from seed + fields required by exemplar contract
  chapters/
    chNN-….md                 # seeded body (YAML may need exemplar-field fill)
  seed/                       # untouched copy of data/corpus/alan-hirsch/{slug}/
  db/
    chapters_raw/{id}.html    # Supabase HTML snapshot when book exists (for id map + diff)
    chapters_manifest.json
    notes/{chapter_id}.json   # preserve live citation work
  citations/{book_slug}.json  # prior extraction JSON if present
  source/                     # filled in Phase 1 from PDF/EPUB
  audit.json                  # filled in Phase 2
```

4. Pull Supabase chapter IDs + notes (same SQL as 0B) when the book is in `movemental` — seed is body baseline; DB notes/markers are citation baseline until Phase 5 finishes against PDF.
5. PDF/EPUB is **not** optional: Phase 1 still builds the oracle used to fill `completeness_gaps` and finish citations.

### 0B. If `repair-from-db` (no local seed)

Export a local working tree **in corpus shape** (no live writes yet). Side-by-side with an exemplar from movemental-docs while normalizing:

```text
data/cleanup/{book_slug}/
  book.json                   # same contract as movemental-docs exemplar
  chapters/
    ch00-….md                 # YAML frontmatter + Markdown body (HTML→MD on export)
    …
  db/
    chapters_raw/{id}.html    # untouched Supabase HTML snapshot for diff/load
    chapters_manifest.json    # id, title, section_role, content_class, sort_order, word_count
    notes/{chapter_id}.json   # chapter_notes rows (preserve citation work)
  citations/{book_slug}.json  # prior extraction JSON if present
  source/                     # filled in Phase 1
  audit.json                  # filled in Phase 2
```

Convert exported HTML → Markdown carefully (preserve noteref as visible markers / temporary `[^N]`). Prefer editing **Markdown** in the loop so the result matches the formatting example; compile back to HTML only at load.

Use Supabase MCP `execute_sql` (or a small export script) to pull:

```sql
SELECT bc.id, bc.slug, bc.title, bc.section_role, bc.content_class,
       bc.sort_order, bc.word_count, bc.content,
       bc.text_quality_flags, bc.data_quality_flags
FROM book_chapters bc
JOIN books b ON b.id = bc.book_id
WHERE b.slug = :slug
ORDER BY bc.sort_order;

SELECT cn.*
FROM chapter_notes cn
JOIN book_chapters bc ON bc.id = cn.chapter_id
JOIN books b ON b.id = bc.book_id
WHERE b.slug = :slug
ORDER BY bc.sort_order, cn.note_number;
```

Also pull pending review rows:

```sql
SELECT * FROM recon.citation_review_queue
WHERE book_slug = :slug AND build_slug = 'hirsch-citation-restoration'
  AND bucket IN ('review','reject');  -- know what is still open
```

### 0C. If `convert-from-source`

Confirm text layer (`fitz`: empty `get_text()` ⇒ scanned ⇒ stop). Record page count, TOC if present, ISBN vs `books.isbn`.

### 0D. Inventory gate

Done when STATE has: slug, mode, `corpus_seed_path` (or none), source format, page count, seed chapter file count, completeness gaps vs PDF (if seed), chapter row count from DB (if any), prior citation JSON present yes/no, scanned yes/no.

**Stop and report.**

---

## PHASE 1 — Deterministic ground-truth extract (no DB writes)

Build / refresh under `data/cleanup/{book_slug}/source/`:

### 1A. Body extract

**PDF:**

```python
import pymupdf4llm
chunks = pymupdf4llm.to_markdown(
    source_path,
    page_chunks=True,
    # strip repeating chrome when API available in installed version:
    # header=False, footer=False
)
# write source/pages/0001.md … and source/full.md
```

Also keep a plain-text oracle:

```python
import fitz
doc = fitz.open(source_path)
# per-page page.get_text("text") → source/pages_txt/
```

**EPUB:** explode spine XHTML to `source/epub_parts/` in spine order (deterministic). EPUB body is usually higher fidelity than PDF — prefer it when both exist for the same edition.

### 1B. Citation extract (always)

```bash
# reuse existing library — never reimplement superscripts in the agent
python -c "from scripts.citations.pdf_extract import extract_pdf; ..."
# or epub_extract.extract_epub
```

Write/refresh `data/citations/{book_slug}.json` (or `data/cleanup/{book_slug}/citations.json`).

If Hirsch Phase 1 JSON already exists and source file is unchanged, **reuse it**; only re-extract when source bytes or extractor version changed.

### 1C. Chapter map from source

Deterministically propose chapter page ranges from PDF TOC (`doc.get_toc()`) or EPUB nav. Map each proposed section to an existing `book_chapters.id` when in `repair-from-db` mode (title normalize + `sort_order` tiebreak — same rules as citation `match.py`).

Done when: page/part files exist, citation JSON exists, `source/chapter_map.json` lists `{title, page_start, page_end, db_chapter_id?}`.

**Stop and report.**

---

## PHASE 2 — Fidelity audit (deterministic diff)

For each mapped chapter (seed or DB working Markdown vs PDF/EPUB oracle):

1. Normalize both sides with `normalize_for_match` (strip tags, NFKC, collapse ws).
2. Compute:
   - `source_word_count` vs `working_word_count`
   - coverage: fraction of source fingerprint windows (e.g. 40-char shingles) found in working text
   - tail check: last ~200 normalized chars of source chapter appear in working text (truncation detector)
   - head check: first substantive paragraph after title
3. **Completeness vs seed:** any PDF/EPUB section with no seed/working chapter, or seed chapter with coverage failure → `defect_codes` include `missing_section` / `seed_incomplete` (fill from oracle in Phase 3–4; do not invent).
4. Scan working HTML/Markdown for defect regexes / taxonomy codes (`RH` `FO` `HY` `SP` `CIT` `IMG` `ENC` `LAY` `TOC` `TR` `BL` `LIST` `META` — see [`REMEDIATION.md`](REMEDIATION.md)). Minimum hunters (extend `docs/problem-examples-two/_scan_defects.py` when available):
   - running heads / folios: book title repeated, chapter-title+page mid-prose, `Introduction N`, letter-spaced headers, bare `^\d{1,3}$` paragraphs, `_Hirsch_`, `indd`
   - soft hyphens / `-\n` rejoining candidates; mid-sentence paragraph splits
   - glued footnote digits / orphan Pandoc refs / spaced URLs in notes
   - TOC `<br>`, escaped `\[`/`\]`, PUA bullets, repeated identical list markers
   - empty image alts + missing paths; `[PENDING-REVIEW]` YAML
   - chapter-tail bleed (`### Chapter N` / Part openers that belong next); index/authors dumps
   - loose note bodies: `<p><sup>N.</sup> …</p>`
   - `assert_notes_markers.analyze(html)`
5. Compare citation JSON note set vs `chapter_notes` (numbers + body equality after normalize) — seed body is **not** citation-complete until this passes.
6. Emit `data/cleanup/{book_slug}/audit.json`:

```json
{
  "book_slug": "...",
  "chapters": [
    {
      "chapter_id": "...",
      "title": "...",
      "coverage": 0.0,
      "truncation_suspected": false,
      "split_paragraph_candidates": 0,
      "notes_extracted": 0,
      "notes_in_db": 0,
      "markers_in_html": 0,
      "defect_codes": ["SP", "TR", "RH", "CIT:missing_marker:12", "seed_incomplete"]
    }
  ],
  "completeness_gaps": [],
  "taxonomy_totals": {
    "RH": 0, "FO": 0, "HY": 0, "SP": 0, "CIT": 0,
    "IMG": 0, "ENC": 0, "LAY": 0, "TOC": 0, "TR": 0,
    "BL": 0, "LIST": 0, "META": 0
  },
  "totals": {}
}
```

**Auto-pass threshold (chapter clean):** coverage ≥ 0.995, no truncation, zero loose note bodies, every `chapter_notes.body` non-empty, markers present for every note with `marker_present=true`, `assert_notes_markers` ok, split candidates = 0 (or explicitly waived epigraphs listed in STATE), taxonomy codes above clear or STATE-waived, no open `completeness_gaps` for that chapter.

Done when audit JSON exists and unclean chapters are listed.

**Stop and report.** Do not edit HTML until Phase 3.

---

## PHASE 3 — Deterministic repairs (scripts first)

Apply only mechanical fixes that cannot change meaning. Persist discovered exact strings/regexes in `data/cleanup/{book_slug}/remediation_patterns.json` for idempotent re-runs (same artifact as [`REMEDIATION.md`](REMEDIATION.md) R1).

1. Remove known running-head / folio lines (exact pattern list from audit) — including folio+title, `Introduction N`, repeating header-as-`##`, letter-spaced heads, trailing head digits when confirmed chrome.
2. Join soft-hyphen line breaks (`-\n` / `U+00AD`) when **both halves are present**; leave incomplete shreds for Phase 4 oracle restore.
3. NFKC / encoding: expand ligatures **only when source oracle shows the expanded form**; map known PUA bullets → Markdown list markers; unescape body `\[`/`\]` when not link/footnote syntax; replace TOC/table `<br>` with spaces.
4. Delete loose note-body paragraphs whose `(note_number, body)` already exists in `chapter_notes`.
5. Insert missing `<sup class="noteref" data-note="N">N</sup>` for citation matches with confidence ≥ 0.95 using `scripts/citations/load.py` helpers (`insert_marker`, `already_has_marker`) — same thresholds as hirsch-citation-restoration. Emit glued-marker / orphan-ref candidate lists for residuals (do not invent notes).
6. Images: fail on missing paths; record empty-alt counts (alts are editorial — not auto-written here).
7. `[PENDING-REVIEW]` summaries: list all; strip/null only if STATE says summaries are not required for load — never invent author-voice abstracts.
8. Recompute `word_count` / refresh `text_quality_flags` locally in the working files.

Re-run Phase 2 audit. Whatever remains (`SP`, incomplete `HY`, `TR`/`BL`, diagrams, list renumbering, citation residuals) goes to the Cursor loop.

**Stop and report.**

---

## PHASE 4 — Cursor loop (non-deterministic, source-bound)

Use Cursor **`/loop`** (see loop skill) so cleanup continues until gates pass or a hard stop condition hits.

### Loop prompt (paste as the loop body)

```text
Book: {book_slug}
Working tree: data/cleanup/{book_slug}/   (corpus Markdown + book.json)
Seed (if any): data/corpus/alan-hirsch/{book_slug}/  (starting body only)
Format exemplar: movemental-docs/.../alan-hirsch/the-church-as-movement/
Oracle: data/cleanup/{book_slug}/source/   (PDF/EPUB cross-ref — completeness + citations)
Audit: data/cleanup/{book_slug}/audit.json
Notes: data/cleanup/{book_slug}/db/notes/  (do not drop)
Taxonomy: RH FO HY SP CIT IMG ENC LAY TOC TR BL LIST META
Evidence: docs/problem-examples/ + docs/problem-examples-two/
         (pattern catalog — confirm each hit against this book’s oracle)

On each tick:
1. Load audit.json; pick the unclean chapter with highest severity
   (TR/BL/missing_section > CIT missing notes > SP/HY-incomplete/ENC drop-cap >
   RH/FO/LAY chrome > CIT markers > LIST/IMG > META/frontmatter/page-marker
   drift vs exemplar).
2. Open that chapters/*.md file + the matching exemplar chapter style +
   the corresponding source page range only. Prefer patching seed text;
   copy missing spans verbatim from the PDF/EPUB oracle.
3. Fix ONE taxonomy code (or one chapter×code) at a time. Allowed edits:
   merge split paragraphs; restore missing/drop-cap/hyphen halves copied
   verbatim from oracle; fill completeness gaps; strip RH/FO/LAY chrome
   (including mid-prose title+page and repeating header-as-heading);
   move bleed/TOC/index stumps to the correct file; fix LIST markers from
   source; fix ##/### hierarchy to exemplar conventions; ensure
   <!-- page: N --> markers; re-place citation markers from JSON; unspace
   note URLs — never rewrite sentences in your own words; never invent
   PENDING-REVIEW summaries or footnote bodies.
4. Run local checks:
   - word drift / fuzzy / coverage vs source page span
   - taxonomy counts for the code you touched (refresh audit.taxonomy_totals)
   - assert notes still accounted for (DB notes JSON + markers in MD)
   - frontmatter word_count / content_sha256 refresh
5. Update audit.json + STATE.md (chapter status, remaining counts).
6. If all chapters clean → write READY_FOR_LOAD and stop the loop.
7. If stuck (same chapter×code fails 3 ticks) → mark NEEDS_HUMAN and stop.
```

### Loop cadence

- Prefer **dynamic** `/loop` (self-paced): next wake when the chapter file or `audit.json` changes, with a fallback heartbeat (e.g. 3–5 minutes) while a long chapter is in progress.
- On Windows PowerShell, follow the loop skill’s PowerShell `Start-Sleep` pattern; unique sentinel `AGENT_LOOP_TICK_book_cleanup_{slug}`.

### Hard rules inside the loop

- Copy restored text **verbatim** from `source/` (or EPUB part). If the oracle is ambiguous (two editions), stop and ask.
- Do not auto-accept citation matches &lt; 0.95; leave in review queue tooling (`scripts/citations/review_cli.py`).
- Do not renumber notes to hide gaps (gaps are findings).
- Do not merge two DB chapters or split one without updating `chapter_map.json` and asking when live IDs would change.

Done when `READY_FOR_LOAD` exists or `NEEDS_HUMAN` with a short blocker list.

**Stop and report.**

---

## PHASE 5 — Citation integration pass (full)

Seed Markdown and formatting exemplars are **not** citation-complete. Even if Phase 3 inserted high-confidence markers, run a dedicated citation reconcile for this book against the PDF/EPUB extract:

1. Ensure `data/citations/{book_slug}.json` is current (from Phase 1B).
2. Match → auto / review / reject (reuse `scripts/citations/match.py` thresholds: ≥0.95 auto, 0.80–0.95 review, &lt;0.80 reject; ambiguous exact → reject).
3. Upsert `chapter_notes` with **non-empty** bodies only.
4. Insert missing noterefs; strip duplicate loose bodies.
5. Refresh `recon.citation_review_queue` for residuals (new `build_slug` for this cleanup run, or continue hirsch queue if still open — record choice in STATE).
6. Run `assert_notes_markers` across all body chapters.

Wire the convert hook for any *future* re-ingest:

- `scripts/citations/convert_hook.py`
- docs: `Alan Hirsch/docs/build/prompts/hirsch-citation-restoration/CONVERT_HOOK.md`

Done when note/marker counts in STATE match extract vs DB (or explicitly listed residuals).

**Stop and report.**

---

## PHASE 6 — Load to Supabase

1. Compile cleaned Markdown → HTML (headings, paragraphs, blockquotes, emphasis, noteref). Keep `db/chapters_raw` for rollback diff.
2. Snapshot first:

```sql
-- pattern already used by citation restoration
INSERT INTO recon.snap_chapter_content_citations (…)
SELECT … WHERE book slug = :slug;
-- also snapshot notes if a dedicated snap table is used for this build
```

3. Update `book_chapters.content` (and flags/word_count/page_start/page_end) from compiled HTML — **by `id`**, never by title alone.
4. Upsert `chapter_notes` on `(chapter_id, note_number)` from preserved notes JSON + any Phase 5 additions.
5. Do not delete chapters unless Phase 0 agreed a full replace.
6. Optionally copy the cleaned `book.json` + `chapters/*.md` into movemental-docs corpus when the user asks (formatting parity with exemplars).
7. Re-read via MCP: coverage spot-check 3 chapters (first body, middle, last body) + Pirsig-style known note if this is *The Forgotten Ways*.

Done when live row hashes/lengths match working tree and audit gates still pass on exported live content.

**Stop and report.**

---

## PHASE 7 — Final gates (book complete)

All must be true:

| Gate | Check |
|------|--------|
| G1 Faithfulness | Body chapters meet exemplar thresholds (word drift ≤2%, fuzzy ≥0.95, coverage ~0.99+ with boundary caveat); no truncation tails |
| G2 Structure | Corpus layout valid (`book.json` + chapter files); DB `section_role` / `content_class` / `sort_order` coherent; no page-sized junk chapters |
| G3 Format parity | Markdown matches exemplar conventions (YAML, `##`/`###`, `<!-- page: N -->`, blockquote epigraphs); no drop-cap loss |
| G4 Citations | Non-empty `chapter_notes`; markers in loaded HTML; `assert_notes_markers` green — **not** “notes-only trailing chapter” as sole storage for Hirsch |
| G5 Quality view | `v_chapter_text_quality` shows 0 (or waived) `split_paragraph_candidates` for this slug; no new bad `pdf_edition_flags` |
| G6 Idempotence | Re-run Phase 2 audit → zero unclean chapters |
| G7 No chrome | No running heads / folios / letter-spaced header chrome / TOC `<br>` soup in Markdown or HTML (`RH` `FO` `LAY`) |
| G8 Taxonomy | `audit.taxonomy_totals` clear (or STATE-waived) for `HY` `SP` `TR` `BL` `ENC` `LIST` `CIT` residuals; `IMG` paths OK; `META` resolved or deferred in STATE |

Update STATE: `phase=complete`, final counts, residuals (if any) linked to review queue IDs.

Then — and only then — the runner may accept the next `book_slug`.

---

## Suggested Hirsch order (`seed-from-corpus` when seed exists)

Process worst conversion pressure first (updated from [`docs/problem-examples-two/10-book-severity-summary.md`](../../problem-examples-two/10-book-severity-summary.md)), while protecting citation-heavy titles. For each slug below, **check `data/corpus/alan-hirsch/{slug}/` first**:

1. `metanoia` — repeating section heads + hyphen/encoding; PDF available; often already advanced in cleanup
2. `the-forgotten-ways` — highest hyphen/missing-half + shred pressure (citation crown jewel — loop discipline required)
3. `the-permanent-revolution` — severe chrome + glued markers; **acquire PDF/EPUB first** if missing
4. `on-the-verge` → `reframation` → `rejesus` → `right-here-right-now` — TOC/layout/folio chrome
5. `the-faith-of-leap` → `fast-forward-to-mission` → handbook — citation form / glued markers
6. `5q` (EPUB, lighter) → `the-shaping-of-things-to-come` → `untamed` / `disciplism` as sources allow

Override freely; always one at a time. Books that already finished an older cleanup without taxonomy codes: run [`REMEDIATION.md`](REMEDIATION.md) once before declaring them complete.

---

## Anti-patterns

- Skipping `data/corpus/alan-hirsch/{slug}/` when it exists and re-converting from PDF or re-exporting DB as the body baseline — **use the seed first**; PDF is the completeness/citation cross-ref.
- Treating seed Markdown as citation-complete — always finish citations from PDF/EPUB extract + `chapter_notes`.
- Seeding from `_archive/` without an explicit ask — archive is historical reference only.
- Re-converting all Hirsch books from PDF because “cleaner” — **destroys citation work**; seed-or-export-and-repair instead.
- Copying corpus `chNN-notes.md` + empty `citations: []` as the *only* citation strategy for Hirsch — use `chapter_notes` + noteref.
- Letting the model invent footnote numbers or CSL.
- Renumbering notes to hide gaps.
- “Summarizing” a damaged paragraph instead of copying from source.
- Inventing `[PENDING-REVIEW]` replacements “in the author’s voice,” or stripping real subheads that only look like running heads (confirm repetition + oracle).
- Deleting glued footnote digits instead of restoring noterefs via the citation pipeline.
- Loading to prod without `recon` snapshot.
- Running the Cursor loop without refreshing `audit.json` / `taxonomy_totals` each tick (loop without gates = infinite polish).
- Editing only Supabase HTML while ignoring the corpus Markdown contract (format will diverge from exemplars).
- Skipping the defect taxonomy on a “clean enough” convert — Phases 2–4 must still emit and clear the codes (or waive in STATE).

---

## Quick start (operator)

```text
1. Copy STATE.template.md → STATE.md; set book_slug + source_path
2. Check data/corpus/alan-hirsch/{slug}/ first → mode=seed-from-corpus when present
   (else repair-from-db if in Supabase, else convert-from-source)
3. Open formatting exemplar: movemental-docs/.../the-church-as-movement/
4. Phase 0: seed (or export) → data/cleanup/{slug}/; list completeness gaps vs PDF
5. Run Phase 1 extracts (pymupdf4llm + scripts/citations) — PDF is required cross-ref
6. Run Phase 2 audit (include taxonomy_totals from problem-examples); share unclean + gap counts
7. Phase 3 scripts (remediation_patterns.json); then /loop Phase 4 until READY_FOR_LOAD
8. Phase 5 finish citations; Phase 6 compile MD→HTML + load; Phase 7 gates (incl. G8 taxonomy)
9. Mark book complete; pick next slug
```

For a brand-new PDF with no seed: set `mode=convert-from-source`, skip seed copy, emit corpus Markdown via pymupdf4llm + TOC map (like the exemplar `conversion_engine`), run citation extract/hook, then the same audit → loop → load path.

For books already cleaned before this taxonomy existed: run [`REMEDIATION.md`](REMEDIATION.md) against `data/cleanup/{slug}/` (or the corpus seed), then resume Phase 5–7 if loading.
