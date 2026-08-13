# Book citations — reference

Canonical sources copied from the books repo (refined 2026-08):

| File | Role |
|------|------|
| [reference/hirsch-citation-restoration.md](reference/hirsch-citation-restoration.md) | Original Phase 0–6 restoration recipe (extract → match → load → review → verify → convert-path fix) |
| [reference/CONVERT_HOOK.md](reference/CONVERT_HOOK.md) | Ingest-time preservation contract + post-convert assertion |

## Runtime library (books repo)

All under `scripts/citations/` unless noted:

- `pdf_extract.py` / `epub_extract.py` — deterministic extract
- `normalize.py` / `match.py` / `load.py` — match + idempotent insert
- `assert_notes_markers.py` / `convert_hook.py` — fail bodies-without-markers
- `generic_phase5_compile.py` — `[^n]` → noteref HTML + assert vs notes JSON
- `review_cli.py` / `populate_review_queue.py` — human residuals
- `scripts/corpus_fix_citations.py` — `[^n]n` / bare / caret / linkish → clean `[^n]`
- `docs/problem-examples-two/_scan_defects.py` — `dup_fn` / CIT scanners

## Staging vs loaded form

```text
PDF/EPUB ──extract──► data/citations/{slug}.json
                         │
                         ▼
Cleanup MD ──form──► clean [^n]  +  db/notes/*.json
                         │
              phase5 compile
                         ▼
HTML ──► <sup class="noteref" data-note="N">N</sup>
DB   ──► chapter_notes (non-empty body)
```

## Confidence thresholds (do not loosen)

- ≥ 0.95 auto-apply
- 0.80–0.95 review queue
- < 0.80 reject
- Ambiguous exact match → reject
