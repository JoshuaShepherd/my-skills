# STATE — book-faithful-cleanup

**Project:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`)  
**Corpus seed root:** `data/corpus/alan-hirsch/` (or peer author root)  
**Formatting exemplar:** `…/movemental-docs/docs/library/corpus/alan-hirsch/the-church-as-movement/`  
**Started:** YYYY-MM-DD  
**Current book:** `{book_slug}`  
**Mode:** `seed-from-corpus` | `repair-from-db` | `convert-from-source` | `remediation`  
**Build slug:** `book-faithful-cleanup-{book_slug}-YYYYMMDD`  
**Remediation pass:** no / yes  
**Current phase:** 0

---

## Book inputs

| Field | Value |
|-------|-------|
| book_slug | |
| corpus_seed_path | `data/corpus/…/{book_slug}/` or none |
| seed_chapter_files | count or none |
| source_path | |
| source_format | pdf / epub |
| text_layer_ok | yes / no / unknown |
| prior_citations_json | path or none |
| completeness_gaps | list or none (seed vs PDF) |
| exemplar_opened | the-church-as-movement (or other) |
| taxonomy_in_scope | RH FO HY SP CIT IMG ENC LAY TOC TR BL LIST META (subset) |
| remediation_patterns | `data/cleanup/{slug}/remediation_patterns.json` or none |

---

## Phase status

| Phase | Status | Notes |
|------:|--------|-------|
| 0 Baseline seed/export / inventory | | |
| 1 Ground-truth extract | | |
| 2 Fidelity audit | | |
| 3 Deterministic repairs | | |
| 4 Cursor loop cleanup | | |
| 5 Citation integration | | |
| 6 Load to Supabase | | |
| 7 Final gates | | |

---

## Counts (refresh each phase)

| Metric | Value |
|--------|------:|
| Seed chapter files | |
| Corpus chapter files (working) | |
| DB chapter rows | |
| Body chapters | |
| Completeness gaps (vs PDF) | |
| Unclean chapters (audit) | |
| Taxonomy residuals (RH/FO/HY/SP/CIT/…) | |
| Notes in DB | |
| Markers in content | |
| Review-queue residuals | |
| Book word drift vs source | |

---

## Loop

| Field | Value |
|-------|-------|
| Loop armed | no |
| Sentinel | `AGENT_LOOP_TICK_book_cleanup_{slug}` |
| READY_FOR_LOAD | no |
| REMEDIATION_COMPLETE | no / n/a |
| NEEDS_HUMAN | no |
| Blocker | |

---

## Decisions log

-
