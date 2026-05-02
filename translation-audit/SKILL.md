---
name: translation-audit
description: >
  Deep linguistic audit of translated books in the Alan Hirsch corpus. Randomly samples ~10,000
  words from a target language (Brazilian Portuguese, Latin American Spanish, German, European
  Portuguese, or Mandarin Chinese) alongside the corresponding English source, then grades the
  translation on a 100-point rubric across six linguistic dimensions. Produces a full markdown
  report with specific issues, exact locations, improvement recommendations, and an agentic
  confidence overview for non-speakers. Use when asked to audit, grade, review, or quality-check
  any translation in the corpus. Trigger phrases: "audit [language] translation", "grade the
  Spanish", "check translation quality", "review the German corpus", "translation QA".
allowed-tools: Read Bash Glob Grep Write
metadata:
  filePattern: "corpus/alan_hirsch/**/*.md"
---

# Translation Audit — Alan Hirsch Corpus

## Purpose

Perform a rigorous, evidence-based linguistic quality audit of translated books in the Alan Hirsch corpus. The audit samples ~10,000 words from a specified language, identifies the matching English source passages, and grades the translation on a structured 100-point rubric.

**This skill applies to:** Brazilian Portuguese (`pt-BR`), Latin American Spanish (`es`), German (`de`), European Portuguese (`pt`), French (`fr`), and Mandarin Chinese (`zh`).

> **Note on Mandarin:** The corpus does not currently contain Mandarin (zh) translations. If `zh` or `mandarin` is requested, report this clearly and offer to audit one of the available languages instead.

---

## Invocation

```
/translation-audit [language]
```

**Arguments:**

| Argument | Language | Corpus Suffix |
|----------|----------|---------------|
| `es` or `spanish` | Latin American Spanish | `-es` |
| `pt-BR` or `brazilian` or `portuguese-BR` | Brazilian Portuguese | `-pt-BR` |
| `pt` or `portuguese` | European Portuguese | `-pt` |
| `de` or `german` | German | `-de` |
| `fr` or `french` | French | `-fr` |
| `zh` or `mandarin` or `chinese` | Mandarin (not in corpus) | — |

If no language is specified, ask the user to choose.

---

## Corpus Inventory

The corpus lives at: `corpus/alan_hirsch/`

Available translations by language suffix:

| Language | Available Books |
|----------|-----------------|
| `-es` | 5q-es, disciplism-es, fast-forward-to-mission-es, metanoia-es, on-the-verge-es, reframation-es, rejesus-es, right-here-right-now-es, the-faith-of-leap-es, untamed-es |
| `-pt-BR` | disciplism-pt-BR, metanoia-pt-BR, on-the-verge-pt-BR, reframation-pt-BR, rejesus-pt-BR, right-here-right-now-pt-BR, the-faith-of-leap-pt-BR, the-forgotten-ways-handbook-pt-BR, untamed-pt-BR |
| `-pt` | 5q-pt, reframation-pt, the-faith-of-leap-pt, the-forgotten-ways-pt |
| `-de` | the-forgotten-ways-de |
| `-fr` | the-forgotten-ways-fr |

---

## Step-by-Step Execution

### Step 1 — Build the inventory

```bash
ls corpus/alan_hirsch/ | grep "\-[LANG_SUFFIX]$"
```

For each matching book directory, run:
```bash
ls corpus/alan_hirsch/[book-slug]/
```

Build a mental map of: `{ book_slug → [chapter_files] }` for the target language.

Also identify the English source book for each translation:
- `5q-es` → `5q`
- `reframation-pt-BR` → `reframation`
- `the-forgotten-ways-de` → `the-forgotten-ways`
- etc. (strip the language suffix to get the English slug)

### Step 2 — Stratified random sampling

**Goal:** Collect approximately 10,000 words of translated text, distributed across as many books and chapters as possible.

**Sampling strategy:**
1. If multiple books exist: select 2–4 books, spread across the available set (not all from one book)
2. Within each book: select chapters from different positions — pick from the beginning (ch01–02), middle (ch04–06), and end (last chapters)
3. Read each selected chapter in full
4. Track a running word count from the frontmatter `word_count` field or estimate from character count
5. Continue sampling until you have approximately 10,000 words of translated text
6. If a single book only (e.g., German has only `the-forgotten-ways-de`), sample 5–7 chapters distributed across the book

**Read selected translation files:**
```bash
cat corpus/alan_hirsch/[book-slug]/[chapter-file].md
```

### Step 3 — Locate English source passages

For each translation chapter sampled, find the corresponding English source chapter:
- Same `canonical_id` with the English book slug, OR
- Match by `chapter_slug` in the English book directory

```bash
ls corpus/alan_hirsch/[english-book-slug]/
cat corpus/alan_hirsch/[english-book-slug]/[matching-chapter].md
```

Read and retain the corresponding English passages for comparison.

### Step 4 — Apply the linguistic rubric

Evaluate the translation against the rubric below. For each dimension, document:
- The score awarded
- Maximum points available
- 2–5 specific issues with **exact location** (book slug, chapter file, paragraph or sentence)
- The problematic source text
- The current translation
- A recommended improvement

---

## Linguistic Rubric (100 Points)

### Dimension 1 — Semantic Fidelity (25 pts)

Measures whether the translation transfers the complete propositional and theological content of the source, without omission, addition, or distortion.

**Full marks (23–25):** Every concept present. Nuanced qualifiers preserved. Theological paradoxes intact. No paraphrasing that shifts meaning.

**Good (18–22):** Minor omissions of secondary clauses. Occasional softening of strong assertions. No core meaning lost.

**Adequate (12–17):** Noticeable condensation. Some metaphors flattened. Key theological nuances diluted.

**Weak (6–11):** Significant omissions. Paraphrase replaces precision. Source arguments obscured.

**Poor (0–5):** Major conceptual losses. Fundamental misrepresentation of the author's position.

**Watch for in theological texts:**
- Omission of conditional clauses ("if," "unless," "insofar as")
- Softening of prophetic statements
- Loss of rhetorical tension (e.g., antithesis, paradox)
- Addition of explanatory glosses not in source

---

### Dimension 2 — Register and Voice Preservation (20 pts)

Measures whether Alan's distinctive pastoral-prophetic voice is preserved: Christocentric gravity, narrative energy, prophetic urgency, collegial warmth, and theological depth.

**Full marks (18–20):** Voice is unmistakably Alan's in the target language. Christocentric tone intact. Prophetic passages carry weight. Pastoral warmth present.

**Good (14–17):** Voice largely preserved. Occasional flatness or over-formality. Prophetic urgency slightly diluted.

**Adequate (9–13):** Noticeably more generic. Theological depth present but voice is not distinctive. Feels like academic prose rather than pastoral-prophetic writing.

**Weak (4–8):** Voice largely lost. Translation sounds like a committee-produced document. No distinctiveness.

**Poor (0–3):** Alan's voice is unrecognizable. Register mismatch throughout.

**Watch for in theological texts:**
- Academic formalization of conversational passages
- Loss of direct address ("you," "we")
- Removal of rhetorical questions
- Toning down of prophetic imperatives
- Loss of sentence rhythm and staccato emphasis

---

### Dimension 3 — Target Language Fluency (20 pts)

Measures whether the translation reads naturally in the target language — free of calques, unidiomatic constructions, and source-language interference.

**Full marks (18–20):** Reads as if written natively. No detectable English substrate. Idioms and expressions are target-language native.

**Good (14–17):** Mostly fluent. Occasional stiff construction. Minor Anglicisms.

**Adequate (9–13):** Clearly translated. Some awkward phrases. Sentence-level interference evident.

**Weak (4–8):** Pervasive Anglicisms. Frequent unidiomatic constructions. Reading is effortful.

**Poor (0–3):** Machine-translation feel. Text is difficult to read in the target language.

**Language-specific watchpoints:**
- **Spanish (es):** ser/estar conflation, improper subjunctive, false cognates (e.g., "actual" ≠ "actual"), direct calques of "to be"
- **Portuguese pt-BR:** Europeanisms intruding (clitic placement), informal register shifts, false friends from Spanish
- **Portuguese pt:** Over-reliance on gerunds in pt-BR style (Brazilianisms in European PT), register mismatch for Portuguese publishing conventions
- **German (de):** Overly literal compound words, English loan words where German equivalents exist, improper Konjunktiv II for reported speech
- **French (fr):** Anglicisms ("challenge," "timing"), register shifts between soutenu and courant, calqued progressive forms ("est en train de")

---

### Dimension 4 — Theological Terminology Accuracy (15 pts)

Measures accurate rendering of Alan's specialized theological vocabulary, biblical citations, and missiological terminology.

**Full marks (14–15):** All key terms correctly and consistently rendered. Biblical citations match standard translations in target language. Missiological terms appropriately localized or explained.

**Good (11–13):** Key terms mostly correct. 1–2 instances of inconsistent rendering. Biblical quotes largely accurate.

**Adequate (7–10):** Several term inconsistencies. Some terms transliterated when translation exists. Biblical citations occasionally paraphrased.

**Weak (3–6):** Significant term errors. APEST, mDNA, or other core vocabulary rendered inconsistently or incorrectly.

**Poor (0–2):** Core theological terms untranslated, mistranslated, or omitted.

**Key terms to verify:**
| English | Check rendering in target language |
|---------|-----------------------------------|
| APEST (Apostle, Prophet, Evangelist, Shepherd, Teacher) | Maintained or officially localized? |
| mDNA (Missional DNA) | Preserved acronym or translated? |
| apostolic genius | Consistent rendering? |
| missional | Consistently rendered (not just "missionary")? |
| liminality / communitas | Correctly glossed or transliterated? |
| Christocentric | Correct theological term in target language? |
| discipleship / disciplism | Consistent rendering throughout? |
| incarnational / incarnational impulse | Target-language theological standard? |

---

### Dimension 5 — Syntactic Adaptation (10 pts)

Measures whether sentence structure has been appropriately restructured for the target language's syntax, rather than mirroring English word order.

**Full marks (9–10):** Sentences fully restructured for target language. Verb placement, clause ordering, and paragraph organization follow target-language conventions.

**Good (7–8):** Most sentences restructured. Occasional English word-order calques.

**Adequate (4–6):** Noticeable structural Anglicisms. Some sentences are syntactically uncomfortable.

**Weak (2–3):** Widespread structural interference. Text reads as translated, not native.

**Poor (0–1):** Near word-for-word structural calque throughout.

**Language-specific requirements:**
- **German:** Verb-second rule, subordinate clause verb-final placement, correct Satzklammer
- **Spanish/Portuguese:** Appropriate subject-verb inversion in questions, correct relative clause structure, proper placement of reflexive pronouns
- **French:** Correct inversion in questions, appropriate use of "dont" vs "de qui," liaison in flowing prose

---

### Dimension 6 — Internal Consistency (10 pts)

Measures whether key terms, names, and concepts are translated consistently across the sampled chapters, with no unexplained variation.

**Full marks (9–10):** All key terms consistent. No unexplained variation. Consistent use of formal/informal address throughout.

**Good (7–8):** Minor inconsistencies in secondary terms. Core vocabulary consistent.

**Adequate (4–6):** Noticeable inconsistencies in important terms. Reader would notice variation.

**Weak (2–3):** Core terminology inconsistent. "Missional" rendered 3 different ways, etc.

**Poor (0–1):** Fundamental inconsistency throughout. Suggests multiple translators without harmonization.

---

## Report Template

After completing the analysis, produce the following report verbatim in structure (populate with your findings):

---

```markdown
# Translation Quality Audit Report
## Alan Hirsch Corpus — [Language Name]

**Audit Date:** [Date]
**Language Audited:** [Full language name] (`[code]`)
**Books Sampled:** [list]
**Chapters Sampled:** [count] chapters, ~[word count] words
**English Baseline:** [corresponding English book(s)]

---

## Agentic Confidence Overview

*Why should a non-speaker trust this audit?*

[Write 3–5 paragraphs here addressing: (1) the objective, text-internal evidence methods used (cross-referencing source vs. target, terminology tracking, structural comparison) that do not require native-speaker intuition; (2) how the rubric criteria — fidelity, register, consistency — can be evaluated against the English original even without target-language fluency; (3) Claude's multilingual training and evaluation on [target language] theological and literary prose; (4) the specific calibration signals used (e.g., known biblical citation forms in [target language], established missiological vocabulary standards, recognized publishing conventions); (5) what limitations remain and how the report flags uncertainty where it exists.]

---

## Executive Summary

**Overall Score: [X] / 100** — [Grade: Excellent / Good / Adequate / Needs Revision / Poor]

| Dimension | Score | Max | Grade |
|-----------|-------|-----|-------|
| Semantic Fidelity | | 25 | |
| Register & Voice | | 20 | |
| Target Language Fluency | | 20 | |
| Theological Terminology | | 15 | |
| Syntactic Adaptation | | 10 | |
| Internal Consistency | | 10 | |
| **TOTAL** | | **100** | |

**Key Strengths:**
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**Priority Issues:**
- [Bullet 1 — most important]
- [Bullet 2]
- [Bullet 3]

---

## Corpus Sample

### Sampled Material

| Book | Chapter File | Words | Position in Book |
|------|-------------|-------|-----------------|
| [slug] | [filename] | [n] | [Early/Middle/Late] |
| ... | ... | ... | ... |
| **Total** | | **~[total]** | |

---

## Detailed Findings by Dimension

### 1. Semantic Fidelity — [X] / 25

**Assessment:** [2–3 sentence overall assessment of this dimension]

#### Issues Found

---

**Issue SF-01** · Severity: [Critical / Major / Minor]

- **Location:** `[book-slug]/[chapter-file].md`, paragraph [N] / section "[section heading]"
- **English source:**
  > "[Exact English passage]"
- **Current translation:**
  > "[Current translated passage]"
- **Problem:** [Specific explanation of what semantic content is lost, distorted, or added]
- **Recommended improvement:**
  > "[Suggested improved translation]"
- **Impact on score:** −[N] pts

---

**Issue SF-02** · Severity: [Critical / Major / Minor]
[... repeat structure ...]

---

### 2. Register & Voice Preservation — [X] / 20

**Assessment:** [2–3 sentence overall assessment]

#### Issues Found

---

**Issue RV-01** · Severity: [Critical / Major / Minor]

- **Location:** `[book-slug]/[chapter-file].md`, paragraph [N]
- **English source:**
  > "[passage]"
- **Current translation:**
  > "[passage]"
- **Problem:** [Explanation]
- **Recommended improvement:**
  > "[Suggestion]"
- **Impact on score:** −[N] pts

---

[... continue for each dimension: TF = Target Language Fluency, TT = Theological Terminology, SA = Syntactic Adaptation, IC = Internal Consistency ...]

---

## Findings Summary Table

| ID | Dimension | Severity | Location | Issue Summary |
|----|-----------|----------|----------|---------------|
| SF-01 | Semantic Fidelity | Major | `[file]` p.[N] | [Short description] |
| SF-02 | Semantic Fidelity | Minor | `[file]` p.[N] | [Short description] |
| RV-01 | Register & Voice | Major | `[file]` p.[N] | [Short description] |
| TF-01 | Target Fluency | Critical | `[file]` p.[N] | [Short description] |
| TT-01 | Theological Terms | Major | `[file]` p.[N] | [Short description] |
| SA-01 | Syntactic Adapt. | Minor | `[file]` p.[N] | [Short description] |
| IC-01 | Consistency | Major | `[file]` p.[N] | [Short description] |
| ... | ... | ... | ... | ... |

---

## Recommendations

### Immediate Revisions (Critical/Major issues)
[Numbered list of the most important changes needed, referencing issue IDs]

### Structural Considerations
[Any patterns suggesting systemic translation approach issues — e.g., translator unfamiliar with Alan's missiological vocabulary, possible machine-translation base with light human editing, multiple translators without style guide, etc.]

### Glossary Gaps
[Any terms that need standardized translations or glossary entries that appear to be missing]

---

## Auditor Notes

*Limitations and confidence qualifications for this specific audit:*

[Honest statement of what this audit cannot confirm — e.g., cultural idiom appropriateness for a specific regional audience, whether target-language readers would flag additional issues, any chapters that could not be cross-referenced due to missing English source material, word count limitations of the sample.]

---

*Report generated by Claude Code translation-audit skill — Alan Hirsch Corpus*
*Rubric version: 1.0 | Skill path: .claude/skills/translation-audit/SKILL.md*
```

---

## Execution Notes

- **Sample size target:** ~10,000 words of translated text. If a language has very few chapters (e.g., French fr has only 5 chapters, ~4,000 words total), audit the complete available corpus and note the limited sample size in the report.
- **Issue density:** Aim to document 2–5 issues per rubric dimension. Do not manufacture issues — if a dimension is well-executed, say so and award full or near-full marks with a brief explanation.
- **Exact quotation:** Always quote the actual text from the file — never paraphrase what the text says. Preserve formatting (bold, italics, blockquotes) in the quoted passages.
- **Location precision:** Every issue must include the exact file name and a locating reference (paragraph number from the top of the content body, or section heading). This allows the translator to find the passage immediately.
- **No hedging on scores:** Commit to a specific numeric score for each dimension. Document your reasoning. Do not give fractional scores.
- **Mandarin not available:** If `zh`/`mandarin` is requested, respond: "Mandarin (zh) translations are not currently in the Alan Hirsch corpus. Available languages: Latin American Spanish (es), Brazilian Portuguese (pt-BR), European Portuguese (pt), German (de), French (fr). Please choose one of these."
- **Output destination:** Write the report to `corpus/alan_hirsch/_index/translation-audit-[lang]-[YYYY-MM-DD].md`. Also print the full report to the conversation.
