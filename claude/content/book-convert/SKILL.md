---
name: book-convert
description: >
  Phase 01 of the books pipeline — convert any PDF or EPUB book into lossless,
  paginated, footnoted Markdown using the right tool for the input type
  (Marker for native-text PDFs, MinerU for scanned PDFs, Pandoc for EPUB,
  Mistral OCR as hosted fallback). Auto-routes by file type, writes per-chapter
  MD with `<!-- page: N -->` markers and `[^N]` footnotes, and lands the output
  in `corpus/alan_hirsch/<book-slug>/chapters/`. Use when ingesting a new book
  source file from `_inbox/` into the corpus. Trigger phrases: "convert this
  PDF", "ingest this book", "run phase 01", "PDF to markdown".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "01"
  reference: "docs/html/books-pipeline.html#phase-1"
---

# Book Convert — Phase 01: Source → Markdown

## Purpose

Convert a single book source (PDF or EPUB) into the canonical Markdown shape used by the rest of the pipeline:

- One `.md` file per chapter under `corpus/alan_hirsch/<book-slug>/chapters/`
- `<!-- page: N -->` HTML-comment page markers at the start of each source page
- `[^N]` Markdown footnote references in body, `[^N]: <citation>` definitions at chapter end (or in a separate Notes file)
- Headings preserved at correct levels (chapter title `##`, section `###`, sub-section `####`)
- Tables, lists, blockquotes, and equations preserved
- Images extracted to `corpus/alan_hirsch/<book-slug>/images/figure-NN.<ext>` and referenced via Markdown image syntax

This is **lossless** — every word, footnote, page number, table cell, and figure caption from the source must appear in the output. Phase 01b (`book-validate`) proves it.

## Invocation

`$ARGUMENTS` should specify:

- **`--input <path>`** — Path to the PDF or EPUB. Required.
- **`--out <dir>`** — Target chapters directory. Default: `corpus/alan_hirsch/<inferred-slug>/chapters/`.
- **`--strategy <auto|marker|mineru|pandoc|mistral-ocr>`** — Conversion engine. Default: `auto` (route by file type).
- **`--book-slug <slug>`** — Override the auto-inferred slug.
- **`--language <code>`** — BCP-47 language code. Default: `en`.

If arguments are missing, ask the user. Never proceed without an explicit input path.

## Routing Decision

```
input.epub                                      → Pandoc
input.pdf  + has text layer  + native           → Marker
input.pdf  + no text layer   + GPU available    → MinerU 2.5-Pro
input.pdf  + no text layer   + no GPU           → Mistral OCR 3 (hosted)
input.pdf  + complex multi-column / equations    → Marker (preferred) or MinerU
```

Detect text-layer presence:

```bash
pdftotext -l 1 "$INPUT" - | wc -c   # if < 100 chars on a 1-page sample, treat as scanned
```

Detect GPU:

```bash
nvidia-smi >/dev/null 2>&1 || system_profiler SPDisplaysDataType 2>/dev/null | grep -q "Apple M"
```

## Process

### Step 1 — Pre-flight

1. Verify `$INPUT` exists and is readable.
2. Infer `<book-slug>` from the filename if not given (lowercase, kebab-case, strip extension).
3. Create the target directory: `mkdir -p corpus/alan_hirsch/<book-slug>/chapters/ corpus/alan_hirsch/<book-slug>/images/`.
4. Pre-archive any existing MD in the target directory to `_archive/<book-slug>-<YYYY-MM-DD>-pre-convert/`.
5. Verify the chosen tool is installed; if not, install:

   ```bash
   # Marker — MUST install against Python 3.12+
   # `uv tool install marker-pdf` alone defaults to Python 3.9, which fails
   # at import time with `TypeError: unsupported operand type(s) for |: '_GenericAlias' and 'NoneType'`
   # because surya uses PEP 604 union syntax (X | None).
   uv tool install --python 3.12 marker-pdf

   # MinerU
   uv pip install -U mineru

   # Pandoc (Homebrew)
   brew install pandoc

   # pdftotext / pdfinfo (poppler)
   brew install poppler
   ```

   First run downloads Surya layout/OCR/text-recognition models (~1 GB) into `~/Library/Caches/datalab/models/`. Cached after that.

### Step 2 — Run the converter

#### Native-text PDF → Marker

```bash
# CRITICAL flags:
#   --disable_ocr        — skip OCR for native-text PDFs. Marker runs OCR by
#                          default ("Recognizing Text" phase) even on PDFs that
#                          already have an embedded text layer; this is the
#                          dominant time sink (≈ 40 s/page on Apple Silicon CPU).
#                          Skipping it cuts a 352-page InDesign export from
#                          ~3 hours to ~30–45 min.
#   TORCH_DEVICE=cpu     — force CPU on Apple Silicon. The Surya layout model
#                          OOMs the MPS backend at ~5 GiB on books with image-
#                          heavy or multi-column pages and aborts on page 1.
#                          On real CUDA GPUs you can drop this and let Marker
#                          use the GPU.
TORCH_DEVICE=cpu marker_single "$INPUT" \
  --output_format markdown \
  --paginate_output \
  --disable_ocr \
  --output_dir "$OUT_TMP/"
```

Output structure: Marker creates `$OUT_TMP/<input-stem>/<input-stem>.md` plus extracted images alongside it (e.g. `_page_3_Picture_0.jpeg`). It is **not flat** — there's a sub-directory per input file.

Marker writes page separators as `{N}-----------------------------------------------` (long-dash rule) when `--paginate_output` is set. Older versions emit a bare `{N}` line. The Step 3 normalizer matches both.

Decide whether to disable OCR by sniffing the text layer first:

```bash
chars=$(pdftotext -l 5 "$INPUT" - | wc -c)
[ "$chars" -gt 2000 ] && OCR_FLAG="--disable_ocr" || OCR_FLAG=""
```

If `pdftotext` returns >2 000 chars in 5 sample pages the PDF has a real text layer; pass `--disable_ocr`. If the sample is small and dominated by ligature glyphs, the embedded text is broken and you should let Marker OCR it.

#### Scanned PDF → MinerU 2.5-Pro

**Critical:** override defaults that strip headers, footers, footnotes, and page numbers.

```bash
mineru -p "$INPUT" -o "$OUT_TMP/" \
  --keep-headers --keep-footers --keep-footnotes --keep-page-numbers
```

#### Scanned PDF, no GPU → Mistral OCR 3 (hosted)

```bash
curl https://api.mistral.ai/v1/ocr \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -F document=@"$INPUT" -F model="mistral-ocr-2512" \
  -F output_format="markdown" > "$OUT_TMP/book.md"
```

Cost: ~$1–2 per 1k pages. Confirm with the user before invoking if the book exceeds 500 pages.

#### EPUB → Pandoc

```bash
pandoc "$INPUT" \
  -t gfm+footnotes \
  --wrap=none \
  --reference-location=section \
  --split-level=1 \
  --extract-media="$OUT_DIR/../images/" \
  -o "$OUT_TMP/book.md"
```

If the EPUB is messy, normalize through Calibre first:

```bash
ebook-convert "$INPUT" "$OUT_TMP/clean.epub"
```

then re-run Pandoc against `clean.epub`.

### Step 3 — Normalize page markers

Marker (current `marker-pdf` 1.x) outputs page separators as `{N}-----------------------------------------------` (long-dash rule). Older Marker emits a bare `{N}` line. MinerU outputs per-page block JSON. Mistral OCR outputs per-page JSON. Pandoc has no page numbers from EPUB (acceptable — note in book.json that `page_marker_style: none`).

Rewrite all variants into the canonical HTML-comment form. The post-processor we use is checked into the repo at `scripts/postprocess_marker.py` (or `/tmp/marker-on-the-verge/postprocess.py` for one-off runs); it handles both modern and legacy Marker separators in one pass:

```python
PAGE_SEPARATOR_PATTERNS = [
    re.compile(r"^\{(\d+)\}-{5,}\s*$", re.MULTILINE),   # modern: {N}-----
    re.compile(r"^\{(\d+)\}\s*$",       re.MULTILINE),   # legacy: bare {N}
]
for pat in PAGE_SEPARATOR_PATTERNS:
    content = pat.sub(r"<!-- page: \1 -->", content)
```

Run it on the Marker output:

```bash
python3 scripts/postprocess_marker.py \
  --input "$OUT_TMP/<input-stem>/<input-stem>.md" \
  --out-dir "corpus/alan_hirsch/<book-slug>/" \
  --book-slug "<book-slug>"
```

This step also splits chapters (Step 4) — see the script for the combined logic.

### Step 4 — Split into chapters

Walk the normalized book.md. Detect chapter boundaries by `^## ` headings (Marker / MinerU) or `<h1>` separators (Pandoc with `--split-level=1`). Write one file per chapter to `corpus/alan_hirsch/<book-slug>/chapters/` with the naming convention:

```
<book-slug>-ch01-<chapter-slug>.md
<book-slug>-ch02-<chapter-slug>.md
…
<book-slug>-ch11-foreword.md         # front matter uses higher numeric prefix in some books
<book-slug>-ch12-preface.md
```

(Match the existing convention in `corpus/alan_hirsch/<other-book>/` — every book in the corpus uses `ch01`, `ch02`, etc. with zero-padded prefixes.)

**Books with PART hierarchy — CRITICAL:** Some books (*On the Verge*, *5Q*, *The Forgotten Ways*, anything with "Part 1 / Part 2 …" structure) emit two heading levels from Marker:

- `## Apostolic Genius` ← part heading (H2)
- `### Chapter N: …` ← actual chapter heading (H3) inside the part

A naïve split on `^## ` only cuts at part boundaries, lumping every chapter inside a part into one giant file. For *On the Verge* this collapsed **8 of 10 body chapters into 2 files** (`ch05-introduction` swallowed Chapters 1, 2, 3; `ch07-verge-vibe` swallowed Chapters 5, 6, 7, 8, 9, 10). Downstream phases accepted the broken shape, which silently dropped 80% of the book from the e-reader's chapter list and from per-chapter RAG retrieval.

**Detection (run before splitting):**

```bash
python3 -c "
import re, sys
text = open(sys.argv[1]).read()
h2 = len(re.findall(r'^## ', text, re.MULTILINE))
h3_chapters = len(re.findall(r'^### Chapter \d+', text, re.MULTILINE))
print(f'## headings: {h2}')
print(f'### Chapter N headings: {h3_chapters}')
if h3_chapters > h2 // 2:
    print('PART HIERARCHY DETECTED — split on ### Chapter N boundaries, not ## only')
" "$OUT_TMP/<stem>/<stem>.md"
```

If the `### Chapter N` count is meaningfully greater than the `## ` count, **the splitter MUST cut on `### Chapter N:` boundaries** (with `## ` boundaries used as secondary cuts for true non-chapter sections like the Introduction, Final Thoughts, Notes, Appendix).

**Correct splitting algorithm:**

1. Walk the normalized markdown line-by-line.
2. Track candidate boundaries. A new chapter starts at:
   - `^## ` if the heading text matches a non-chapter section name (Introduction, Final Thoughts, Notes, Appendix, Foreword, Acknowledgments, Contents, Cover) — a `chapter_type != 'chapter'`.
   - `^### Chapter \d+:` (the long form with title) — a body chapter.
3. **Trim back** to include any preceding bare `### Chapter N` line (Marker often emits both `### Chapter 2` and `### Chapter 2: The Silver Imagination` on consecutive lines).
4. Each segment becomes one file in reading-order, named `<book-slug>-chNN-<slug>.md` where `NN` is the file's reading-order position (zero-padded), not the book's chapter number.

**`scripts/postprocess_marker.py` currently defaults to splitting on `## ` only.** When the detection script above flags PART HIERARCHY, **either**:
- Pass `--split-on=h3-chapters` to the post-processor (when implemented), **or**
- Run the manual re-split helper at [`/tmp/otv-fix/resplit_chapters.py`](../../../docs/build/prompts/fix-on-the-verge.md) as a follow-up — see the *On the Verge* fix prompt for a working example.

**Verification after splitting:**

```bash
# Every body chapter (1..N) should be its own file with chapter_number = its book chapter
ls corpus/alan_hirsch/<book-slug>/*.md | wc -l   # expect ~16-20 files for a typical Hirsch book
grep -l "^chapter_number: [1-9]" corpus/alan_hirsch/<book-slug>/*.md | wc -l   # expect to match book chapter count
```

If `chapter_number` only takes 2-3 distinct positive values (e.g., just 4 and 5), you have the part-merge bug.

**Pre-clean the target directory.** If `corpus/alan_hirsch/<book-slug>/` already contains old MD chapter files (e.g. from a previous Supabase export), delete them before writing — but **preserve `images/` and `<slug>-book.json`**:

```bash
rm -f corpus/alan_hirsch/<book-slug>/*.md
# images/ and book.json stay
```

If you skip this, you'll end up with a mixture of old and new chapters that downstream phases cannot disambiguate.

**Front-matter preamble check.** The script emits a `ch00-front-matter.md` file for whatever appears before the first `## ` heading (endorsements, copyright, dedication, ToC). The check is `len(re.findall(r"[A-Za-z]", preamble)) > 100` — this counts total letters, not consecutive ones. An earlier version used `[A-Za-z]{20}` (twenty consecutive letters) which prose almost never has, and silently dropped 1,000+ words of front matter. If you adapt this script, keep the letter-count form.

### Step 5 — Footnotes

Marker emits Pandoc-style `[^N]` references natively. Pandoc preserves them. MinerU and Mistral OCR may emit footnotes as inline parentheticals or as a flat list at the end. If any chapter has `[N]` (bracketed digit, no caret) or raw inline digits where superscripts were, run a one-pass conversion:

```bash
python3 scripts/footnote_normalize.py corpus/alan_hirsch/<book-slug>/chapters/*.md
```

The script should rewrite `[N]` → `[^N]` only when the digit follows sentence-ending punctuation (conservative pattern; see [docs/build/prompts/fix-on-the-verge.md](../../../docs/build/prompts/fix-on-the-verge.md) Issue 14 for the regex).

### Step 6 — Images

Marker writes extracted images **alongside the markdown**, not in a sibling `images/` directory. For *On the Verge*, the output dir contained the .md plus 65 `.jpeg` files named `_page_NN_Picture_M.jpeg` and `_page_NN_Figure_M.jpeg`. Marker uses `.jpeg` (not `.jpg`).

The chapter MD files reference these images flat — `![](_page_18_Picture_1.jpeg)` — relative to the markdown file. Two things to do:

1. Copy/move the images to `corpus/alan_hirsch/<book-slug>/images/`:

   ```bash
   mkdir -p corpus/alan_hirsch/<book-slug>/images/
   cp /tmp/marker-output/<book-slug>/*.jpeg corpus/alan_hirsch/<book-slug>/images/
   ```

   **Quote each glob separately** in zsh — a single `*.jpeg *.png` in zsh fails the whole `cp` if either pattern has zero matches. Run them as separate commands or use `setopt nullglob`.

2. Rewrite the image refs in every chapter MD to point into `images/`:

   ```bash
   for f in corpus/alan_hirsch/<book-slug>/*.md; do
     sed -i '' 's|!\[\](_page_|![](images/_page_|g' "$f"
   done
   ```

   (`-i ''` is the BSD/macOS sed form. On Linux, drop the `''`.)

If figures could not be extracted (Marker/MinerU sometimes leave placeholders), insert TODO markers:

```markdown
<!-- TODO: extract Figure NN as image from PDF p.<page> -->
```

The published convention for this corpus is to leave Marker's `_page_NN_Picture_M.jpeg` filenames in place rather than rename to `figure-NN.<ext>`. Renaming requires manual figure-number assignment from captions; defer it to a later cleanup pass unless the book has fewer than ~10 figures.

### Step 7 — Hand off to Phase 01b

Run the validation harness immediately:

```bash
# next skill
/book-validate corpus/alan_hirsch/<book-slug>/
```

Do **not** advance to Phase 02 (`book-frontmatter`) until validation passes.

## Output

Print a structured summary:

```
Phase 01 — Conversion complete
  Source:       _inbox/<file>.pdf
  Book slug:    <book-slug>
  Strategy:     marker | mineru | pandoc | mistral-ocr
  Pages:        <N>
  Chapters:     <N> files written to corpus/alan_hirsch/<book-slug>/chapters/
  Images:       <N> extracted to corpus/alan_hirsch/<book-slug>/images/
  Footnotes:    <N> [^N] references detected
  Page markers: <N> <!-- page: N --> markers inserted
  Pre-archive:  _archive/<book-slug>-<date>-pre-convert/

Next: run /book-validate corpus/alan_hirsch/<book-slug>/
```

## Quality Checks

- Every chapter file has at least one `<!-- page: N -->` marker (unless EPUB input).
- Every footnote reference `[^N]` in the body has a matching `[^N]: <text>` definition somewhere in the corpus.
- No raw `{N}` page separators remain.
- No `0310331005_OnVerge_int_CS4.indd`-style InDesign footer artifacts remain.
- Heading hierarchy is sane (one `##` chapter title per file; `###`/`####` for sections).

## Known Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Multi-column reading order broken | PDFMiner-based tool used | Switch to Marker (Surya layout) |
| Footnotes missing | MinerU defaults strip them | Add `--keep-footnotes` flag |
| Page numbers gone | MinerU defaults strip them | Add `--keep-page-numbers` flag |
| Tables flattened | MarkItDown / pdfplumber used | Switch to Marker or MinerU |
| Equations garbled | PyMuPDF4LLM used | Switch to Marker (preserves LaTeX) |
| Letter-spaced kerning (`F O R E W O R D`) | InDesign tracked-out caps not normalized | Run universal kerning sweep (see fix-on-the-verge.md Issue 8) |
| Alternate-line drops in long quotes | LlamaParse / generic conversion | Re-convert with Marker; manually verify long blockquotes |
| `marker_single` import error: `unsupported operand type(s) for \|: '_GenericAlias' and 'NoneType'` | Marker installed against Python 3.9 (default uv tool target). Surya uses PEP 604 `X \| None` which needs Python ≥3.10 | Reinstall: `uv tool uninstall marker-pdf && uv tool install --python 3.12 marker-pdf` |
| `RuntimeError: MPS backend out of memory (... max allowed: 9.07 GiB)` | Surya layout model exceeds the Mac MPS memory cap on image-heavy or multi-column pages | Re-run with `TORCH_DEVICE=cpu` env var. Slower but reliable. (Do **not** use `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` — risks freezing macOS.) |
| Marker spends hours on "Recognizing Text" phase for a native-text PDF | Marker runs OCR by default even when the PDF already has an embedded text layer | Sniff text layer with `pdftotext`; pass `--disable_ocr` for native-text inputs (≈5–10× speedup) |
| Background `marker_single` task disappears mid-run | Claude Code session restart wipes `/tmp` and the harness task-output dir, killing the child process | For very long conversions, launch with `nohup marker_single … > path/in/repo.log 2>&1 &` so progress survives session resets |

## Timing Expectations (Apple Silicon, CPU)

- 350-page native-text PDF, `--disable_ocr`: layout ~30 min, table-rec ~5 min, render ~2 min → **~40 min total**.
- 350-page native-text PDF, OCR enabled (default): layout ~30 min, OCR ~2.5 hours, render ~5 min → **~3 hours total**.
- First run also downloads ~1 GB of Surya models (one-time).

If the host has a real CUDA GPU (not MPS), drop `TORCH_DEVICE=cpu` and expect 5–10× faster end-to-end.

## Out of Scope

- Frontmatter generation — handled by `/book-frontmatter` (Phase 02)
- Quality audit — handled by `/book-audit`
- Translation — translations are converted separately per locale into `corpus/alan_hirsch/<book-slug>-<lang>/`

## References

- [docs/html/books-pipeline.html#phase-1](../../../docs/html/books-pipeline.html#phase-1) — Pipeline brief, Phase 01 tool comparison
- [Marker GitHub](https://github.com/datalab-to/marker)
- [MinerU GitHub](https://github.com/opendatalab/MinerU)
- [Pandoc EPUB guide](https://pandoc.org/epub.html)
- [Mistral OCR 3 docs](https://mistral.ai/news/mistral-ocr-3)
