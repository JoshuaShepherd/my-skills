---
name: book-validate
description: >
  Phase 01b of the books pipeline — prove no words were lost during PDF/EPUB →
  Markdown conversion. Runs a five-layer validation harness (word-count diff,
  fuzzy alignment, 5-gram coverage, embedding similarity, vision LLM judge)
  comparing the converted MD against the original source. Cheap checks first,
  semantic checks last, LLM judge only on samples. A chapter that fails any
  layer goes back to Phase 01 before advancing. Use after `/book-convert`,
  before `/book-frontmatter`. Trigger phrases: "validate this book", "run
  the harness", "prove no words were lost", "phase 01b".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "01b"
  reference: "docs/html/books-pipeline.html#validation"
---

# Book Validate — Phase 01b: Layered Validation

## Purpose

Prove that the converted Markdown is character-faithful to the original PDF/EPUB. Catch four classes of failure that downstream phases cannot recover from:

1. **Dropped content** — sidebars, footnotes, captions, alternate lines of long blockquotes.
2. **OCR substitutions** — wrong characters that pass spell-check (e.g., "rn" → "m").
3. **Reordering** — multi-column reading order broken.
4. **Silent paraphrase** — content rewriting that pdftotext/word-count cannot detect.

The harness is **layered** — cheap checks first, semantic checks last, LLM judge only on samples. Total cost for a 300-page book: under $1 in API spend, under 10 minutes of wall time.

## Invocation

`$ARGUMENTS` should specify:

- **`<book-dir>`** — Path to `corpus/alan_hirsch/<book-slug>/`. Required (positional).
- **`--source <path>`** — Override the original source file. Default: auto-detect from `_inbox/<book-slug>.pdf` or `archive/pdf/<book-slug>.pdf`.
- **`--min-fuzzy <ratio>`** — Threshold for layer 2. Default: `0.95`.
- **`--min-coverage <ratio>`** — Threshold for layer 3. Default: `0.99`.
- **`--min-embed <cosine>`** — Threshold for layer 4. Default: `0.97`.
- **`--skip-judge`** — Skip the layer-5 vision LLM judge (saves ~$0.50 per book).
- **`--judge-pages <N>`** — Number of random pages to send to the vision judge. Default: `8`.
- **`--report <path>`** — Where to write the validation report. Default: `<book-dir>/.ingest/validation-<YYYY-MM-DD>.json`.

## Process

### Layer 0 — Source-text normalization (do this BEFORE any layer)

The thresholds in layers 1–3 assume the source-text and MD-text streams are comparable in basic ways. They are not, by default. Without normalization a clean conversion will look like a 30%+ failure on layer 3. Do all of the following before running any comparison:

1. **Use plain `pdftotext`, NOT `pdftotext -layout`.** The `-layout` flag preserves the source's columnar layout, which scrambles word order against Marker's logical-reading-order Markdown. Result: 5-gram coverage drops below 80% on multi-column books even when the conversion is faithful.
2. **Normalize Unicode quotes / dashes / spaces.** Marker often emits straight ASCII quotes; the source PDF uses curly typographic ones. Every contraction (`don't` vs `don't`) breaks ~5–10 surrounding 5-grams. Apply a translate table on both sides of the comparison:

   ```python
   QUOTE_MAP = str.maketrans({
       "‘": "'", "’": "'", "‚": "'", "‛": "'",
       "“": '"', "”": '"', "„": '"', "‟": '"',
       "–": "-", "—": "-", "―": "-",
       " ": " ",  # NBSP → space
       "…": "...",
   })
   normalized = text.translate(QUOTE_MAP).lower()
   ```

3. **Strip InDesign / printer-pipeline footer artifacts from the source.** Books exported from InDesign CS3-CS6 carry per-page footer lines like `0310331005_OnVerge_int_CS4.indd  ii  3/1/11  8:44 AM`. Marker correctly strips these from the MD; your validator must strip them from the source-text comparand or every page will look like the MD lost ~10 words. Robust regexes:

   ```python
   src = re.sub(r"^\s*\d{8,}_\w+\.indd[^\n]*\n", "", src, flags=re.MULTILINE)
   src = re.sub(r"^\s*\d+/\d+/\d+\s+\d+:\d+\s*[AP]M\s*$", "", src, flags=re.MULTILINE)
   src = re.sub(r"^\s*\d+\s*$", "", src, flags=re.MULTILINE)  # bare page numbers
   ```

4. **Strip running headers** (chapter title repeated at the top of each page) when present. Detect by finding any short string that appears at the start of >50 page boundaries in the source extraction.
5. **Lowercase + collapse whitespace** before tokenization so casing and indentation don't fragment 5-grams.

If you skip these and the conversion is genuinely good, you will see ~70–85% coverage and a ~5–8% word-count drift — and waste the user's time chasing phantom failures. The numbers the published thresholds (99% / 95% / 2%) were calibrated against assume layer 0 has run.

### When layer 0 is not enough

For some sources — especially InDesign-from-2011 PDFs with heavy per-page chrome (printer codes, running heads, page numbers, marginalia) — layer 0 normalization will not be sufficient to clear the 99% / 95% / 2% bars even on a faithful conversion. Signs you've hit the noise floor:

- After normalization, layer 1 drift is between 3–8% and layer 3 coverage is 80–90%.
- Spot-checking the missing 5-grams shows mostly fragments of running headers, footnote-number-only lines, or table-of-contents leader-dot artifacts.
- Layer 2 fuzzy passes on body-text pages but fails on every page that has a sidebar, chart, or photo caption.

In that situation, **do not keep tightening the layer-0 regexes indefinitely.** Switch to `/book-audit` instead — it's a sample-based, vision-aware comparator that handles layout chrome correctly. Note in the validation report which layers were skipped and why, then proceed.

### Layer 1 — Word-count diff (cost: ~0)

For each chapter MD file, strip Markdown syntax (headings, emphasis, blockquotes, code fences, footnote refs, image refs), then compare against the plain-text extraction of the source.

```bash
python3 -c "
import sys, re, subprocess
md = open(sys.argv[1]).read()
# Strip frontmatter
md = re.sub(r'^---.*?^---', '', md, flags=re.MULTILINE | re.DOTALL)
# Strip MD syntax
md = re.sub(r'(\*\*|\*|_|\`+|#+|>|\[\^[a-z0-9]+\]|!\[[^\]]*\]\([^)]+\)|\[[^\]]*\]\([^)]+\))', '', md)
md_words = len(md.split())
src = subprocess.check_output(['pdftotext', sys.argv[2], '-']).decode()
src_words = len(src.split())
drift = abs(md_words - src_words) / src_words
print(f'MD: {md_words}  SRC: {src_words}  drift: {drift:.2%}')
exit(0 if drift < 0.02 else 1)
" <chapter.md> <source.pdf>
```

**Pass criterion:** `drift < 2%` per chapter and `< 1%` book-wide. Larger drift indicates dropped content (small) or whole sections missing (large).

### Layer 2 — Character-level fuzzy alignment (cost: ~0)

Use `rapidfuzz.token_set_ratio` per page. Catches OCR substitutions, soft hyphenation issues, and reordering within a page.

```python
from rapidfuzz import fuzz
import pdfplumber

with pdfplumber.open(source_pdf) as pdf:
    for i, page in enumerate(pdf.pages):
        page_text = page.extract_text() or ''
        # Find the corresponding MD slice by `<!-- page: N -->` marker
        md_slice = extract_md_for_page(book_dir, i + 1)
        ratio = fuzz.token_set_ratio(page_text, md_slice)
        if ratio < 95:
            print(f"FAIL page {i+1}: {ratio}%")
```

**Pass criterion:** `ratio >= 95%` per page. EPUB inputs skip this layer (no source pages).

### Layer 3 — 5-gram coverage (cost: ~0)

Tokenize source and MD; build sets of every contiguous 5-word sequence; compute set intersection / source. Catches dropped sidebars, footnotes, captions — content that other layers may pass on volume but miss specifically.

```python
from collections import Counter

def ngrams(text, n=5):
    words = text.lower().split()
    return Counter(' '.join(words[i:i+n]) for i in range(len(words) - n + 1))

src_grams = ngrams(source_text)
md_grams = ngrams(md_text)
covered = sum(1 for g in src_grams if g in md_grams)
coverage = covered / len(src_grams)
```

**Pass criterion:** `coverage >= 99%`. Investigate any drop above 1% — list the missing 5-grams to find the dropped passages.

### Layer 4 — Embedding similarity (cost: low)

Embed each MD chunk and the corresponding source-text chunk; require cosine similarity ≥ 0.97. Catches paraphrasing — content that has the same meaning but different words (the failure mode that bit *On the Verge* Ch. 1 and *Reframation* Ch. 1 + Ch. 4).

```python
from openai import OpenAI
import numpy as np

client = OpenAI()
def embed(text):
    return client.embeddings.create(
        input=text[:8000],
        model="text-embedding-3-large",
    ).data[0].embedding

for chunk_id, (md_text, src_text) in chunks.items():
    md_emb = np.array(embed(md_text))
    src_emb = np.array(embed(src_text))
    cos = (md_emb @ src_emb) / (np.linalg.norm(md_emb) * np.linalg.norm(src_emb))
    if cos < 0.97:
        print(f"FAIL {chunk_id}: cos={cos:.4f}")
```

**Pass criterion:** `cos >= 0.97` per chunk. If many chunks fall in 0.94–0.97, it's likely formatting drift; if any chunk falls below 0.94, suspect a rewrite.

### Layer 5 — Vision LLM judge (cost: high; sample only)

Pick `--judge-pages` random pages. For each, render the source page as PNG (`pdftoppm -png -r 200 source.pdf -f N -l N tmp/page-N`), extract the corresponding MD slice, and send both to Claude Opus 4.7 vision (or Claude Sonnet 4.6 for cost).

Prompt:

```
You are a forensic document comparator. The image is a single page from a published book.
The text below is the converted Markdown for that page. Your job is to list anything visible
in the image that is missing from the markdown, or anything in the markdown that is not in
the image. Be specific: cite exact words, page positions (top/middle/bottom-left/right), and
the type of element (body text, footnote, caption, page header, table cell, figure, sidebar).

Image: <page-N.png>
Markdown:
\`\`\`md
<md slice>
\`\`\`

Output format:
- MISSING_FROM_MD: <description>
- EXTRA_IN_MD: <description>
- MATCH: (only emit if clean)
```

Aggregate findings across the sampled pages. Any non-MATCH finding fails the layer.

**Pass criterion:** all sampled pages return `MATCH` or only-trivial `EXTRA_IN_MD` findings (e.g., page numbers, running headers we intentionally added).

## Output

Write a JSON report to `<book-dir>/.ingest/validation-<YYYY-MM-DD>.json`:

```json
{
  "book_slug": "on-the-verge",
  "source": "/Users/joshuashepherd/Desktop/Dev/repos/#archive/alan-books-old/pdf/on-the-verge.pdf",
  "ran_at": "2026-04-27T18:30:00Z",
  "thresholds": { "fuzzy": 0.95, "coverage": 0.99, "embed": 0.97 },
  "layers": {
    "word_count": { "passed": true, "book_drift": 0.008, "worst_chapter": { "ch04": 0.018 } },
    "fuzzy":      { "passed": true, "min_ratio": 0.96, "worst_pages": [{"page": 47, "ratio": 0.94}] },
    "coverage":   { "passed": false, "coverage": 0.987, "missing_examples": ["the urban tribe whoever they might", "..."] },
    "embed":      { "passed": false, "min_cos": 0.91, "worst_chunks": [{"id": "ch01-0042", "cos": 0.91}] },
    "judge":      { "passed": false, "findings": [{"page": 23, "missing": "footnote 1 about Verge Network"}] }
  },
  "verdict": "FAIL — return to Phase 01"
}
```

Print a human-readable summary:

```
Phase 01b — Validation
  Layer 1 word count:    PASS  (book drift 0.8%; worst Ch.4 1.8%)
  Layer 2 fuzzy align:   PASS  (min 0.96 across 296 pages)
  Layer 3 5-gram cover:  FAIL  (98.7% — dropped sidebar on p.57)
  Layer 4 embed sim:     FAIL  (Ch.1 chunk 0042 cos 0.91 — paraphrase)
  Layer 5 vision judge:  FAIL  (p.23 missing footnote 1)

  Verdict: FAIL — return to Phase 01

  Recommended next: re-run /book-convert with --strategy=marker
```

## Pass / Fail Routing

| Outcome | Next step |
|---|---|
| All layers PASS | Advance to `/book-frontmatter` (Phase 02) |
| Layer 1 fails (drift > 2%) | Re-run `/book-convert` with a different strategy |
| Layer 2 fails (some pages < 95%) | Targeted spot-fix per page; re-run validation |
| Layer 3 fails (coverage < 99%) | List missing 5-grams; restore from PDF; re-run |
| Layer 4 fails (paraphrase suspected) | Run `/book-audit` to characterize; then `/book-fix` |
| Layer 5 fails (vision judge findings) | Address each finding; spot-fix; re-run validation |

## Out of Scope

- Frontmatter validity — that's `/book-frontmatter`
- Heading-hierarchy correctness — that's `/book-audit`
- Translation accuracy — that's the existing `/translation-audit` skill

## References

- [docs/html/books-pipeline.html#validation](../../../docs/html/books-pipeline.html#validation)
- [rapidfuzz docs](https://rapidfuzz.github.io/RapidFuzz/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
