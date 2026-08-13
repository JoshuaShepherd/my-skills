# Conversion-defect remediation (post-cleanup / seed repair)

Use when a book already has `data/cleanup/{slug}/` (or corpus seed) and still fails
chrome / shred / citation-form gates — or as the focused sweep after first convert.
Does **not** replace parent Phases 0–7; resume parent Phase 5–7 after
`REMEDIATION_COMPLETE` when loading.

**Build slug:** `book-defect-remediation-{slug}-YYYYMMDD`  
**Parent:** skill `book-faithful-cleanup`  
**Evidence:** `docs/problem-examples/`, `docs/problem-examples-two/`

## Runner

1. STATE: `mode=remediation` or `remediation_pass=true`
2. Working tree: `data/cleanup/{slug}/` else corpus seed
3. Per class: announce → scan → fix (deterministic first) → verify counts → STATE → stop unless continue
4. `/loop` for hybrid classes after deterministic strip (see [loop-prompt.md](loop-prompt.md))

## Taxonomy (same codes as parent)

`RH` `FO` `HY` `SP` `CIT` `IMG` `ENC` `LAY` `TOC` `TR` `BL` `LIST` `META`

## Phase R0 — Inventory + oracle

Confirm slug, working tree, source_path, text layer. Load or stub `audit.json`. List in-scope codes in STATE. **Stop and report.**

## Phase R1 — Deterministic strip

Build `remediation_patterns.json`. Order:

1. `FO`/`RH` — folios, title+page, `Introduction N`, repeating `## SECTION` heads, letter-spaced headers
2. `LAY` safe — TOC `<br>`, trailing head digits when confirmed
3. `HY` safe joins only (both halves present)
4. `ENC` safe — unescape `\[`/`\]`, PUA → list markers
5. `IMG` — path assert; list empty alts (no invented alt text)
6. `META` — list `[PENDING-REVIEW]`; strip/null only if STATE allows — never invent abstracts
7. `CIT` detect only — emit glued/orphan/spaced-URL lists for R2/R3 / `book-citations`

Re-scan → STATE. **Stop and report.**

## Phase R2 — Hybrid + oracle

| Code | Rule |
|------|------|
| RH/FO residual | Mid-sentence title+page; rejoin sentence after strip |
| SP | Merge mid-sentence breaks; keep intentional epigraphs |
| HY incomplete | Restore missing half **verbatim** from oracle |
| CIT | Unspace URLs; unstick digits; feed match pipeline — never invent bodies |
| LAY diagrams | Rebuild only with figure/oracle evidence |
| TOC/BL | Move stumps; fix notes-file YAML theft |
| LIST | Restore numbering from source |
| IMG chrome | Drop decorative screenshots only with PDF review |
| ENC drop-cap/Th | Restore letters only when oracle shows full word |

**Stop and report** after each major class/batch.

## Phase R3 — Loop

Use remediation loop body in [loop-prompt.md](loop-prompt.md).

### Remediation gates

| Gate | Check |
|------|--------|
| RG1 | RH/FO/LAY clear or waived |
| RG2 | Safe HY joins done |
| RG3 | No truncation / bleed stumps |
| RG4 | SP = 0 or waived epigraphs |
| RG5 | `dup_fn=0`; CIT forms cleared or queued to citations scripts |
| RG6 | Image paths OK; alt/chrome decisions recorded |
| RG7 | META resolved or deferred in STATE |
| RG8 | Word drift / coverage still within parent thresholds |

Then continue parent **Phase 5–7** if loading.

## Scan hunters (minimum)

Prefer `docs/problem-examples-two/_scan_defects.py`:

- Bare folios `^\d{1,3}$`; title+page chrome
- Soft hyphen `U+00AD` / `\w-\n\w`
- Mid-sentence breaks (lowercase → blank → lowercase)
- Glued markers; `dup_fn` `\[\^(\d{1,3})\]\1(?!\d)`
- Caret / linkish; escaped brackets; TOC `<br>`
- Empty alts; `[PENDING-REVIEW]`; repeated identical list indices

Record false positives (verse numbers, years) in STATE — do not “fix” them.

## Anti-patterns

- Remediation without oracle when TR / incomplete HY / CIT placement is in scope
- Stripping a real subhead that only looks like a running head
- Inventing PENDING-REVIEW replacements
- Deleting glued digits instead of restoring noterefs via [[book-citations]]
