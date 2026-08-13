# Convert pipeline integration — citation preservation

The `book-convert` / Phase 01 path is **not in this repo** (sources + repair scripts only). Wire these hooks into the converter that writes `book_chapters.content` and `chapter_notes`.

## Required behavior on ingest

1. Extract footnotes/endnotes from the **source PDF/EPUB** with `scripts/citations/pdf_extract.py` or `epub_extract.py` (deterministic — never LLM).
2. Emit inline markers in chapter HTML:
   ```html
   <sup class="noteref" data-note="N">N</sup>
   ```
3. Upsert `chapter_notes` in the **same transaction** as the chapter content write (`body` never empty).
4. Fail the job if the classic bug signature appears:

```bash
python scripts/citations/assert_notes_markers.py --dir path/to/emitted/chapters
```

Or in Python:

```python
from scripts.citations.convert_hook import post_convert_assert, convert_chapter_citations

post_convert_assert(chapter_html)  # raises if bodies without markers
```

## Assertion rule

**FAIL** when a chapter has loose note-body paragraphs (`<p><sup>N.</sup> …</p>`) or extracted note bodies, but **zero** `<sup class="noteref">` markers.

That is exactly how the Hirsch English corpus was mangled.

## Repair path (already run)

Build slug `hirsch-citation-restoration` repaired 12 in-scope books via:

- extract ? match ? snapshot ? load ? review queue

Re-ingest of a single book through the updated convert path should produce correct notes with **no** repair step.
