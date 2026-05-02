---
name: tam-score
description: Score and rank movement leader candidates using the Seven Gates and 100-point Movemental rubric
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Score: Evaluate Movement Leader Candidates

Apply the full Movemental evaluation rubric to one or more candidates, producing scored profiles and tier assignments.

## Invocation

```
/tam-score $ARGUMENTS
```

**Arguments:**
- One or more candidate names. Examples:
  - `/tam-score Mark Sayers` — score a single candidate
  - `/tam-score all unscored` — score all candidates in the UNSCORED section
  - `/tam-score rescore 50-75` — rescore candidates ranked 50-75

---

## Before Starting

1. **Read the rubric** at `intelligence/leader-research/tam-search/03-RUBRIC.md` — this is the scoring authority
2. **Read existing profiles** at `intelligence/leader-research/tam-search/02-CANDIDATE-PROFILES.md` — for format and benchmarks
3. **Read the master list** at `intelligence/leader-research/tam-search/01-MASTER-RANKED-LIST.md` — for current rankings
4. **Note the benchmarks**: Alan Hirsch = 100/100, Brad Brisco = 88/100, Michael Frost = 94/100

---

## Phase 1: Research the Candidate

For each candidate being scored, gather data via web search:

| Data Point | Sources to Check |
|------------|-----------------|
| Published books | Amazon, Goodreads, publisher sites |
| Current role/affiliations | Personal website, LinkedIn, org sites |
| Audience size | Twitter/X, Instagram, Facebook, YouTube, newsletter |
| Speaking/conferences | Conference sites, event listings |
| Education/training | Seminary affiliations, academic posts |
| Co-authors/endorsers | Book pages, blurbs, co-publications |
| Courses/training programs | Personal site, org platforms |
| Revenue signals | Book sales rank, course pricing, speaking fees, consulting |
| Movement evidence | Orgs founded, networks catalyzed, practitioners multiplied |
| Theological depth | Book content, published articles, teaching |

---

## Phase 2: Seven Gates Assessment

Evaluate each gate with a verdict and 1-2 sentence evidence:

```markdown
### Seven Gates Assessment

| Gate | Verdict | Evidence |
|------|---------|----------|
| 1. Embodied Practice (10+ years) | PASS/FAIL | [evidence] |
| 2. Multiplication Evidence | PASS/FAIL | [evidence] |
| 3. Movement Over Institution | PASS/FAIL | [evidence] |
| 4. Prophetic Edge | PASS/FAIL | [evidence] |
| 5. Credibility Through Suffering | PASS/N/A | [evidence or "not assessed"] |
| 6. Theological Depth | PASS/FAIL | [evidence] |
| 7. Network Coherence (Scenius Test) | PASS/FAIL | [evidence] |
```

**If a candidate FAILS any gate (except Gate 5):** Flag them as "Does Not Pass Gates" with an explanation. Do not proceed to quantitative scoring unless the failure is borderline and worth discussion.

---

## Phase 3: 100-Point Quantitative Scoring

Apply the rubric exactly as defined in `03-RUBRIC.md`:

```markdown
### Scoring Breakdown

| Category | Score |
|----------|-------|
| 1A: Theological Foundation (15) | /15 |
| 1B: Movement Practice Integration (10) | /10 |
| 2A: Current Audience Size (10) | /10 |
| 2B: Audience Quality & Engagement (10) | /10 |
| 3A: Content Quality & Depth (12) | /12 |
| 3B: Content Consistency & Platform Readiness (8) | /8 |
| 4A: Current Revenue Streams (8) | /8 |
| 4B: Platform Business Model Alignment (7) | /7 |
| 5A: Existing Network Connections (6) | /6 |
| 5B: Collaboration History & Referral Potential (4) | /4 |
| 6A: Leadership Development & Mentoring (6) | /6 |
| 6B: Community Building & Platform Ownership Mindset (4) | /4 |
| **Subtotal** | **/100** |
| Bonus: Underrepresented demographic | +0-5 |
| Bonus: Emerging voice (<40, <10 yrs) | +0-3 |
| Bonus: Geographic diversity | +0-2 |
| Bonus: Gender diversity | +0-1 |
| **TOTAL** | **/100+bonus** |
```

For each sub-score, provide a 1-sentence justification.

---

## Phase 4: Tier Assignment

| Tier | Score Range | Priority | Action |
|------|-------------|----------|--------|
| Flagship | 90-100 | IMMEDIATE | Maximum investment, founding cohort |
| Proven | 75-89 | HIGH | Standard platform development |
| Emerging | 60-74 | SELECTIVE | Targeted support, mentoring |
| Pipeline | 45-59 | DEVELOPMENT | Growth focus, future potential |
| Below 45 | <45 | NOT READY | Monitor only |

---

## Phase 5: Write the Profile

Append the full profile to `intelligence/leader-research/tam-search/02-CANDIDATE-PROFILES.md` using this format:

```markdown
## #[rank] [Full Name] - [score]/100

**Domain**: [primary domain]
**Affiliations**: [key orgs]
**Notable Works**: [books, frameworks]
**Audience**: [size estimate]

**Seven Gates**: [PASS ALL / FAIL: Gate X]

**Scoring Breakdown**:
| Category | Score |
|----------|-------|
| [full breakdown] |

**Notes**: [key observations, network value, risks, unique contributions]
```

Update the master list ranking in `01-MASTER-RANKED-LIST.md` — insert at the correct position by score.

---

## Phase 6: Comparative Notes

After scoring, provide:

1. **How this candidate compares** to the nearest-scored existing candidates
2. **Unique contribution** they would bring to the scenius
3. **Risk factors** (potential for dilution, controversy, misalignment)
4. **Recommended next action** (profile, reflected understanding, outreach)

---

## Key Rules

1. **Use only live-sourced data.** Every score must be backed by verifiable information from web search.
2. **Apply the rubric exactly** — do not invent new criteria or modify point ranges.
3. **Benchmark against Hirsch (100), Frost (94), Brisco (88)** — these are the calibration points. A score of 90+ should genuinely rival these leaders' profiles.
4. **Be honest about gaps.** If data is unavailable for a scoring category, score conservatively and note "insufficient data" rather than guessing high.
5. **The Scenius Test (Gate 7) is critical.** A high-scoring candidate who would dilute network coherence should be flagged, not just scored.
6. **Never inflate scores** to fill quota. A smaller, higher-quality TAM is better than a padded list.
7. **Preserve all existing profiles** — append new ones, never overwrite.
