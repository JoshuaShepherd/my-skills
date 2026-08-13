# Cursor Prompt — Conversion-defect remediation (post-cleanup / seed repair)

**Repo:** sources + `scripts/citations/` live here  
**Database:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`) — load only if the user asks  
**Scope:** **One book per run.** Works on books already through `PROMPT.md`, or any seed under `data/corpus/` / working tree under `data/cleanup/` after convert.  
**Build slug:** `book-defect-remediation-<book-slug>-YYYYMMDD`  
**Parent recipe:** [`PROMPT.md`](PROMPT.md) (faithful cleanup)  
**Defect inventories (evidence):** [`docs/problem-examples/`](../../problem-examples/), [`docs/problem-examples-two/`](../../problem-examples-two/)

This is the **remediation lane**: hunt and fix the conversion-residue classes catalogued in those inventories. It does **not** replace Phase 0–7 of the parent recipe — use it when:

- A book already has a working tree (`data/cleanup/{slug}/`) and still fails chrome / shred / citation-form gates, or
- You are repairing imported corpus seeds in place before (or instead of) a full re-convert, or
- A later book finishes convert/cleanup and needs a focused defect sweep against the shared taxonomy.

**Prime directives (same as parent):**

1. Imported / working Markdown first; PDF/EPUB is completeness + citation oracle — never invent wording.
2. Citations are not an LLM guess — use `scripts/citations/*` + prior JSON.
3. One book at a time; snapshot before DB writes; no silent deletion.
4. Do **not** treat theological wording, intentional fragment paragraphs, or true section headings as defects.

---

## Runner

1. Copy or refresh `STATE.md` for the book (`STATE.template.md`); set `mode=remediation` (or keep existing mode and add `remediation_pass=true`).
2. Point `working_tree` at `data/cleanup/{slug}/` when present; else `data/corpus/alan-hirsch/{slug}/` (or peer corpus root for non-Hirsch books).
3. Per defect class: announce → scan → fix (deterministic first) → verify counts → update STATE → **stop and report** unless the user says continue.
4. Prefer `/loop` for hybrid / oracle-bound classes after deterministic strip is clean.

---

## Unified defect taxonomy

Stable codes map to inventory files. Use these in `audit.json` `defect_codes` and STATE.

| Code | Class | Lane | Inventory refs |
|------|--------|------|----------------|
| `RH` | Running heads / repeating titles mid-body (`## PARADIGM`, `Introduction N`, `N the permanent revolution`, letter-spaced heads, Untamed-style labels) | det → hybrid if adjacent text truncated | pe/01, pe2/01 |
| `FO` | Folios / bare page digits / title+page chrome | deterministic | pe/02, pe2/02 |
| `HY` | Soft hyphens / EOL `word-` + newline shreds; missing second half | det join → non-det restore if half missing | pe/04, pe2/03 |
| `SP` | Mid-sentence paragraph splits / shredding | hybrid / non-det | pe/03, pe2/04 |
| `CIT` | Glued `.N` / stuck digits, orphan `[^n]`, caret `^[n]`, spaced URLs in notes, malformed `[^n](Ibid.)` | hybrid + citation pipeline | pe/05, pe2/05 |
| `IMG` | Empty alts; chrome/marker screenshots as figures; path check | det path/alt flag; editorial for chrome images | pe/06, pe2/06 |
| `ENC` | PUA bullets, ligature/Th loss (`Te`/`T ey`), escaped `\[`/`\]`, drop-caps | det unescape/PUA; hybrid restore letters | pe/07, pe/11, pe2/08 |
| `LAY` | Column/diagram OCR mixups; TOC `<br>`; spaced title chrome; APEST letter dumps | det for `<br>`/known chrome; non-det rebuild diagrams | pe/08, pe2/07 |
| `TOC` | TOC / index / authors bleed into body chapters | hybrid | pe/09, pe2/07, pe2/09 |
| `TR` | Truncated tails / mid-URL cuts / missing sentence halves | non-det oracle | pe/10, pe2/09 |
| `BL` | Chapter bleed / wrong chunk / notes file with body identity | hybrid | pe2/09 |
| `LIST` | Corrupted list markers (e.g. all `- 3`) | hybrid + PDF numbering | pe/12 |
| `META` | `[PENDING-REVIEW]` YAML summaries | det list; editorial replace or deliberate null | pe/13 |

`pe` = `docs/problem-examples/`, `pe2` = `docs/problem-examples-two/`.

---

## Severity-informed book order (Hirsch seeds)

Use when remediating the 12 seeded books (override freely; still one at a time):

1. **Critical text integrity:** `metanoia` → `the-forgotten-ways` → `the-permanent-revolution` (acquire PDF/EPUB before Permanent Revolution if missing)
2. **Chrome / layout:** `on-the-verge` → `reframation` → `rejesus` → `right-here-right-now`
3. **Citation form:** `the-faith-of-leap` → `fast-forward-to-mission` → `the-forgotten-ways-handbook`
4. **Light polish:** `5q` → `the-shaping-of-things-to-come`

For **any new book** after convert: run the scan checklist below; do not assume Hirsch-specific strings — derive exact running-head lists from that book's title / chapter titles / audit.

---

## PHASE R0 — Inventory + oracle

1. Confirm `book_slug`, `working_tree`, `source_path` (PDF/EPUB), text layer OK.
2. If `data/cleanup/{slug}/audit.json` exists, load it; else create a remediation audit stub.
3. Open inventory exemplars for this book's severity tier (links above) — treat them as **pattern catalogs**, not as permission to copy fixes across books blindly.
4. Record in STATE: which taxonomy codes are in-scope for this pass.

**Stop and report.**

---

## PHASE R1 — Deterministic strip (scripts / regex first)

Apply only mechanical fixes. Build or extend a per-book pattern list in `data/cleanup/{slug}/remediation_patterns.json` (exact strings + regexes discovered from audit).

### R1 checklist (run in order)

1. **`FO` / `RH`:** Remove standalone folio lines; strip exact `N {book title}` / `{chapter title} N` / `Introduction N` lines; strip mid-prose splices of the same; strip exact repeating `## SECTION` running heads when they match page-header pattern (Metanoia `PARADIGM` / `PLATFORMED` / `NOTES`; Untamed-style labels). Letter-spaced headers → match known pattern list per chapter.
2. **`LAY` (safe):** Replace `<br>` with spaces inside TOC / table cells; strip trailing head digit chrome (ReJesus ` 3` on headings) when audit confirms pattern.
3. **`HY` (safe joins only):** Join `-\n` / `U+00AD` when both halves are present on adjacent lines; do not invent the missing half.
4. **`ENC` (safe):** Unescape body `\[` / `\]` when not link/footnote syntax (5Q-style); map known PUA bullet codepoints → `-` / `*`.
5. **`IMG`:** Assert every `![](path)` resolves; list empty alts; do not invent alt text in this phase.
6. **`META`:** List all `[PENDING-REVIEW]` summaries; strip or null only if STATE says summaries are not required for load — **do not invent** author-voice abstracts.
7. **`CIT` (detect only in R1):** Emit glued-marker / orphan-ref / spaced-URL candidate lists for Phase R2–R3 — do not auto-place notes here without citation JSON.

Re-scan; write counts into `audit.json` + STATE.

**Stop and report.**

---

## PHASE R2 — Hybrid repairs (agent + oracle)

For remaining hits, open working chapter + matching `source/` page span only.

| Code | Fix rule |
|------|----------|
| `RH`/`FO` residual | Mid-sentence title+page leaks (`…church 75`); join surrounding sentence after chrome removal |
| `SP` | Merge mid-sentence paragraph breaks; keep intentional epigraphs / one-line quotes |
| `HY` incomplete | Restore missing half **verbatim** from PDF/EPUB (`Chris-` / `verted`) |
| `CIT` | Unspace URLs; unstick `word12` / `.N` candidates; feed into citation match pipeline — never invent note bodies |
| `LAY` diagrams | Flag column/APEST letter dumps; rebuild only with figure/oracle evidence |
| `TOC`/`BL` | Move index/authors/next-chapter stumps out of body files; fix notes-file YAML that steals a body chapter title |
| `LIST` | Restore true 1…N or plain `-` from source; do not guess |
| `IMG` chrome | Drop decorative rule/blank page screenshots only when PDF review shows non-figure |
| `ENC` drop-cap / Th | Restore letters only when oracle shows full word (`Don’t`, `They`, `The`) |

**Not allowed:** paraphrasing, “summarizing” damaged paragraphs, renumbering notes to hide gaps.

**Stop and report** after each major class or chapter batch.

---

## PHASE R3 — Cursor loop (until remediation gates)

### Loop body

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

### Remediation gates (book)

| Gate | Check |
|------|--------|
| RG1 | Zero (or STATE-waived) `RH`/`FO`/`LAY` chrome hits for known patterns |
| RG2 | Soft-hyphen / safe `-\n` joins done; no open `HY` with both halves present |
| RG3 | No truncation tails vs oracle; no chapter-bleed stumps |
| RG4 | Split-paragraph candidates = 0 or waived epigraphs listed |
| RG5 | Citation forms: `dup_fn=0` (`[^n]n` stripped); no orphan Pandoc refs without defs/notes plan; glued/caret/linkish marker lists cleared or queued to `scripts/citations` |
| RG6 | Image paths resolve; empty-alt + chrome-image decisions recorded |
| RG7 | No `[PENDING-REVIEW]` left unless STATE explicitly defers summaries |
| RG8 | Word drift / coverage still within parent PROMPT exemplar thresholds |

When `REMEDIATION_COMPLETE` and the user wants DB load, continue parent **Phase 5–7** (citations → load → final gates).

---

## Scan recipes (deterministic hunters)

Prefer extending `docs/problem-examples-two/_scan_defects.py` (or a cleanup-local script) rather than one-off agent greps. Minimum signals:

- Bare folio lines: `^\d{1,3}$`
- Title+page / page+title chrome (book- and chapter-specific)
- Soft hyphen `U+00AD` and `\w-\n\w`
- Mid-sentence breaks: lowercase end → blank line → lowercase start
- Glued markers: `\.\d{1,3}(?=\s+[A-Z])`, `\w\d{1,3}(?=\s)`
- Duplicate pandoc markers: `\[\^(\d{1,3})\]\1(?!\d)` → count as `dup_fn` (must be 0)
- Caret / linkish: `(?<!\[)\^\d+`, `\[\^\d+\]\([^)]+\)`
- Escaped brackets: `\\[\[\]]`
- TOC `<br>`
- `!\[\]\(` empty alts; path existence
- `\[PENDING-REVIEW\]`
- Repeated list markers: `^- \d+ ` identical across consecutive items

Record false-positive notes (verse numbers, years, intentional `### Stories` repeats) in STATE — do not “fix” them.

---

## Anti-patterns

- Running remediation without an oracle when `TR`/`HY`-incomplete/`CIT` placement is in scope.
- Stripping a string that is also a real subhead without checking repetition + page-header pattern.
- Inventing `[PENDING-REVIEW]` replacements “in Alan’s voice.”
- Treating empty image alts as missing files (paths were OK in the 12-book scan).
- Skipping parent citation Phase 5 because glued digits were regex-deleted instead of restored as noterefs.

---

## Quick start

```text
1. Set book_slug + working_tree + source_path in STATE
2. R0: list in-scope taxonomy codes from pe/pe2 for this book
3. R1: deterministic strip → report counts
4. R2: hybrid/oracle fixes for residuals
5. R3: /loop until REMEDIATION_COMPLETE or NEEDS_HUMAN
6. If loading: resume PROMPT.md Phase 5–7
```

For brand-new books after their first convert: run this remediation pass as the standard “defect sweep” before declaring READY_FOR_LOAD — the parent [`PROMPT.md`](PROMPT.md) now embeds the same taxonomy in Phases 2–4 so a separate remediation run is only needed for books that skipped it or for corpus-only repairs.
