---
name: book-frontmatter
description: >
  Phase 02 of the books pipeline — generate, repair, or recompute YAML
  frontmatter for every chapter in a book and validate against the Zod schema
  at `scripts/lib/frontmatter-schema.ts`. Recomputes `content_sha256`,
  `word_count`, `char_count`, `estimated_reading_time`, and `Opening excerpt`
  to match the current body. Validates `book.json` against `BookManifest` and
  every chapter against `ChapterFrontmatter`. Use after `/book-convert` +
  `/book-validate` pass, before `/book-ingest`. Trigger phrases: "fix the
  frontmatter", "regenerate frontmatter", "validate book.json", "phase 02",
  "schema-validate the corpus".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "02"
  reference: "docs/html/books-pipeline.html#phase-2"
---

# Book Frontmatter — Phase 02: Markdown → MDX (frontmatter-validated)

## Purpose

Bring every chapter's frontmatter into compliance with the corpus schema:

- **Identity:** `file_id` (ULID), `canonical_title`, `book_slug`, `chapter_number`, `chapter_slug`, `chapter_title`, `display_title`.
- **Integrity:** `content_class`, `source_type`, `language`, `word_count`, `char_count`, `estimated_reading_time`, `page_range_start/end`, `content_sha256`.
- **RAG metadata:** `key_concepts`, `themes`, `mentions_scriptures`, `mentions_figures`, `primary_topic`, `secondary_topics`.
- **Citations:** `citations[]` with `id`, `kind` (scripture | book | article), `ref`.
- **Vector store linkage:** `embedding_model`, `embedding_version`, `last_indexed_at`, `vector_store_ids` map.
- **Author + book identity:** `author`, `co_authors`, `year`, `edition`, `publisher`, `isbn`, `tenant`, `tenant_id`.

Validate against `scripts/lib/frontmatter-schema.ts` (Zod). Validate `book.json` against `BookManifest`. Block advancement to Phase 03 on any schema failure.

## Invocation

`$ARGUMENTS`:

- **`<book-slug-or-dir>`** — Required.
- **`--mode <repair|validate-only|regenerate>`** — Default: `repair`.
  - `repair` — fix what's broken; preserve hand-edited fields.
  - `validate-only` — report violations without writing.
  - `regenerate` — rewrite all derived fields from scratch (preserves `summary`/`[PENDING-REVIEW]`).
- **`--report <path>`** — Default: `<book-dir>/.ingest/frontmatter-<YYYY-MM-DD>.json`.

## Process

### Step 0 — Verify per-chapter granularity (CRITICAL)

Before generating frontmatter, confirm Phase 01 produced one file per book chapter. If a chapter file's body contains *multiple* `### Chapter N:` markers, Phase 01 mis-split a part-hierarchy book and lumped multiple chapters into one file (see [book-convert](../book-convert/SKILL.md) → "Books with PART hierarchy"). **Fix this before frontmatter** — generating frontmatter on a merged file produces wrong `chapter_number`, sparse coverage in the e-reader's chapter list, and chapter-level RAG queries that miss most of the book.

```bash
python3 -c "
import re, glob
problems = []
for f in glob.glob('corpus/alan_hirsch/<book-slug>/*.md'):
    text = open(f).read()
    # Skip frontmatter
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        text = text[end+5:] if end > 0 else text
    chapters = re.findall(r'^### Chapter \d+', text, re.MULTILINE)
    if len(chapters) > 1:
        problems.append((f, chapters))
for f, chs in problems:
    print(f'MERGED: {f} contains {len(chs)} chapter markers: {chs}')
print('OK' if not problems else 'RUN PHASE 01 RE-SPLIT FIRST')
"
```

If anything prints `MERGED:`, run the part-hierarchy splitter (see [book-convert](../book-convert/SKILL.md) Step 4) before continuing.

### Step 1 — Inventory + parse

```bash
for f in corpus/alan_hirsch/<book-slug>/*.md; do
  head -100 "$f" | python3 -c "
import sys, yaml
text = sys.stdin.read()
parts = text.split('---', 2)
if len(parts) >= 3:
    fm = yaml.safe_load(parts[1])
    print(f'{sys.argv[1]}: keys={sorted(fm.keys())}')
"
done
```

### Step 2 — Recompute derived fields

For each chapter file (Python script):

```python
import hashlib, re, yaml, sys
from pathlib import Path

def split_fm(text):
    if not text.startswith('---\n'): return None, text
    end = text.find('\n---\n', 4)
    return text[:end+5], text[end+5:]

for path in Path('corpus/alan_hirsch/<book-slug>').glob('*.md'):
    raw = path.read_text()
    fm_block, body = split_fm(raw)
    if not fm_block: continue
    body_stripped = body.strip()
    sha = hashlib.sha256(body_stripped.encode()).hexdigest()
    chars = len(body_stripped)
    words = len(body_stripped.split())
    minutes = max(1, round(words / 200))
    excerpt = ' '.join(
        l for l in body.split('\n')
        if l.strip() and not l.lstrip().startswith(('#', '>'))
    )[:500]
    new_fm = re.sub(r'(content_sha256:\s*).*', f'\\1{sha}', fm_block)
    new_fm = re.sub(r'(word_count:\s*).*', f'\\1{words}', new_fm)
    new_fm = re.sub(r'(char_count:\s*).*', f'\\1{chars}', new_fm)
    new_fm = re.sub(r'(estimated_reading_time:\s*).*', f'\\1{minutes}', new_fm)
    path.write_text(new_fm + body)
    print(f'{path.name}: words={words}, sha={sha[:12]}…')
```

### Step 3 — Validate against Zod

```bash
pnpm tsx scripts/validate-corpus.ts corpus/alan_hirsch/<book-slug> --schema-only
```

If the script does not exist or does not yet support `--schema-only`, write a quick Node.js wrapper that:

1. Reads every `.md` file's frontmatter
2. Parses YAML
3. Runs `ChapterFrontmatter.parse(fm)` from `scripts/lib/frontmatter-schema.ts`
4. Reports violations per file

For `book.json`, run `BookManifest.parse(JSON.parse(text))`.

### Step 4 — Repair common defects

Frequent issues observed across the corpus:

| Defect | Fix |
|---|---|
| `canonical_title` contains kerning artifact (`Mc Neal`) | Replace with correct form (`McNeal`) |
| `Opening excerpt` reflects pre-edit body (e.g. fabricated paragraph) | Regenerate from current body |
| `mentions_scriptures` empty when body has scripture references | Run scripture-detection regex (`\b\d?\s?[A-Z][a-z]+\.?\s+\d+:\d+(-\d+)?\b`) and populate |
| `mentions_figures` missing well-known authors quoted in body | Cross-reference body against a known-authors list |
| `chapter_number: 0` for non-front-matter chapter | Renumber based on file's position in book |
| `summary: "[PENDING-REVIEW]…"` | Leave as-is — Phase 5 task per `_prompts/00-CONTEXT.md` |
| `content_sha256` doesn't match current body | Recompute (Step 2) |
| `co_authors` missing when book has multiple authors | Add from `book.json:author[]` |

### Step 5 — Update book.json totals

```python
total_words = sum chapter.word_count
total_chars = sum chapter.char_count
update book.json: { total_chapters, total_word_count, total_char_count, last_validated_at }
```

### Step 6 — Report

```
Phase 02 — Frontmatter
  Files validated:        18 / 18
  Schema failures:        0
  Recomputed sha:         18
  Recomputed word_count:  18
  book.json:              valid against BookManifest
  Opening excerpts:       18 refreshed
  PENDING-REVIEW summaries: 18 (preserved — Phase 5 task)

  Verdict: PASS — advance to /book-ingest
```

## Quality Checks

- Every `.md` file has a parseable YAML frontmatter block.
- Every `content_sha256` matches `sha256(body.strip())`.
- Every `word_count` matches `len(body.strip().split())` ± 0.
- Every `chapter_number` is a non-negative integer.
- `book.json` is valid against `BookManifest`.
- No `Footnote reference \d+` placeholder strings (cf. Reframation Appendix 3).
- No `Mc Neal`, `Mome ntu m`, or other kerning artifacts in `canonical_title` / `display_title`.

## Out of Scope

- Body content fixes — handled by `/book-fix`.
- Generating `summary` Phase 5 prose — out of scope per project convention.
- ULID minting for new files — handled by `/book-convert` at conversion time.

## References

- [docs/html/books-pipeline.html#phase-2](../../../docs/html/books-pipeline.html#phase-2)
- [scripts/lib/frontmatter-schema.ts](../../../scripts/lib/frontmatter-schema.ts) — Zod schema source of truth
- [scripts/validate-corpus.ts](../../../scripts/validate-corpus.ts) — CLI validator
