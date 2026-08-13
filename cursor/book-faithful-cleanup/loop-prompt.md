# Phase 4 / remediation loop body

Paste as the `/loop` prompt (substitute `{book_slug}`).

## Cleanup loop (Phase 4)

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

## Remediation loop (R3)

```text
Book: {book_slug}
Mode: remediation
Working tree: data/cleanup/{book_slug}/  (or corpus seed if no cleanup tree)
Oracle: data/cleanup/{book_slug}/source/  (or Phase-1 extract)
Audit: data/cleanup/{book_slug}/audit.json
Taxonomy: RH FO HY SP CIT IMG ENC LAY TOC TR BL LIST META
Evidence: docs/problem-examples/ + docs/problem-examples-two/

On each tick:
1. Load audit; pick highest-severity remaining code
   (TR/BL/missing_section > SP/HY-incomplete > RH/FO/LAY >
    CIT > ENC/LIST/IMG > META).
2. Fix ONE code (or one chapter×code). Copy missing text verbatim
   from oracle. Strip chrome; do not rewrite sentences.
3. Refresh defect counts for that code; update audit.json + STATE.md.
4. If all in-scope codes clear → write REMEDIATION_COMPLETE and stop.
5. If same chapter×code fails 3 ticks → NEEDS_HUMAN and stop.
```

## Arming `/loop`

- Prefer dynamic interval (self-paced) with 3–5 minute heartbeat fallback.
- Unique sentinel: `AGENT_LOOP_TICK_book_cleanup_{slug}` (or `_remediation_{slug}`).
- On Windows PowerShell use the loop skill’s `Start-Sleep` pattern.
- Refresh `audit.json` every tick — loop without gates = infinite polish.
