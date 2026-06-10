---
name: tam-audit
description: Audit the TAM master list for gaps, staleness, scoring inconsistencies, demographic imbalances, and missing research — produces an actionable health report
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Audit: Health Check the Movement Leader List

Evaluate the current state of the TAM master list, identifying gaps, inconsistencies, stale data, demographic imbalances, and missing research. Produces an actionable health report with prioritized recommendations.

## Invocation

```
/tam-audit $ARGUMENTS
```

**Arguments (optional):**
- A specific audit focus. Examples:
  - `/tam-audit` — full audit across all dimensions
  - `/tam-audit demographics` — focus on gender, age, ethnicity, geography balance
  - `/tam-audit domains` — check domain coverage gaps
  - `/tam-audit staleness` — identify candidates whose data may be outdated
  - `/tam-audit scoring` — check for scoring inconsistencies
  - `/tam-audit profiles` — check which candidates have/lack deep profiles
  - `/tam-audit international` — assess global representation

---

## Before Starting

1. **Read the full master list** at `intelligence/leader-research/tam-search/01-MASTER-RANKED-LIST.md`
2. **Read the rubric** at `intelligence/leader-research/tam-search/03-RUBRIC.md`
3. **Read existing profiles** at `intelligence/leader-research/tam-search/02-CANDIDATE-PROFILES.md`
4. **Scan the profiles directory** at `intelligence/leader-research/profiles/` for completed deep dives
5. **Scan the international directory** at `intelligence/leader-research/international/` for global research
6. **Scan the network directory** at `intelligence/leader-research/network/` for mapping data
7. **Scan the reflected understandings** at `intelligence/leader-research/reflected-understandings/` for completed documents

---

## Audit Dimensions

### 1. Completeness Audit

| Check | What to Assess |
|-------|---------------|
| **Unscored candidates** | How many of the 156 candidates lack scores? |
| **Incomplete profiles** | Who has a score but no deep profile? |
| **Missing reflected understandings** | Which top-tier candidates lack a reflected understanding? |
| **Missing network data** | Which candidates have no affiliation/connection data? |
| **Missing digital presence data** | Who lacks verified website/social data? |

Produce a completeness matrix:

```markdown
| Candidate | Score | Profile | Reflected Understanding | Network Map | Status |
|-----------|-------|---------|------------------------|-------------|--------|
| Alan Hirsch | 100 | Yes | Yes | Yes | COMPLETE |
| Mark Sayers | 88 | No | No | Partial | NEEDS WORK |
```

### 2. Domain Coverage Audit

Check representation across the domain categories from the rubric:

| Domain | Expected % | Target Count | Actual Count | Gap |
|--------|-----------|--------------|--------------|-----|
| Apostolic/Missional | 10% | 15-20 | ? | ? |
| Psychology/Soul Care | 10% | 15-20 | ? | ? |
| Leadership/Organization | 15% | 20-30 | ? | ? |
| Justice/Urban | 10% | 15-20 | ? | ? |
| Worship/Liturgy | 8% | 10-15 | ? | ? |
| Family/Youth/Parenting | 8% | 10-15 | ? | ? |
| Technology/AI Ethics | 5% | 5-10 | ? | ? |
| Global Mission/Cross-Cultural | 10% | 15-20 | ? | ? |
| Spiritual Formation | 10% | 15-20 | ? | ? |
| Social Entrepreneurship | 5% | 5-10 | ? | ? |
| Education/Discipleship | 5% | 5-10 | ? | ? |
| Health/Wellness/Embodiment | 4% | 5-8 | ? | ? |

Flag domains with fewer than 50% of target candidates.

### 3. Demographic Audit

Assess representation across:

| Dimension | What to Check |
|-----------|--------------|
| **Gender** | Male/female/non-binary ratio. Flag if >75% male |
| **Ethnicity/Race** | Diversity of racial/ethnic backgrounds. Flag if >70% white |
| **Age/Generation** | Distribution across generations. Flag if >60% one generation |
| **Geography** | US vs international. Flag if >80% US-based |
| **Denomination** | Spread across traditions. Flag if >50% one tradition |
| **Career Stage** | Established vs emerging. Flag if <15% emerging voices |

**Note:** Some of this data won't be explicitly recorded. Use web research to fill in gaps for top-tier candidates. Do not guess — mark "unknown" when uncertain.

### 4. Scoring Consistency Audit

Check for scoring anomalies:

| Check | What to Look For |
|-------|-----------------|
| **Score inflation** | Are lower-ranked candidates scored more generously than higher ones? |
| **Benchmark drift** | Do scores still calibrate against Hirsch (100), Frost (94), Brisco (88)? |
| **Missing justifications** | Do scored profiles have per-category justification? |
| **Gate failures** | Are any candidates scored despite failing a gate? |
| **Bonus misapplication** | Are bonus points applied consistently? |
| **Outliers** | Any scores that seem too high or too low relative to peers? |

### 5. Staleness Audit

Flag candidates whose data may be outdated:

| Signal | Action |
|--------|--------|
| Role/org changed | Verify current position via web search |
| New books published since scoring | May affect content quality score |
| Audience size shifted | May affect audience scoring |
| New controversy/departure | May affect gate assessment |
| Death/retirement | Remove or reclassify |

For the top 30 candidates, spot-check one data point each via web search.

### 6. Network Health Audit

Assess the quality of the scenius network:

| Check | What to Assess |
|-------|---------------|
| **Connectivity** | What % of candidates have connections to 3+ others? |
| **Clusters** | Are natural clusters identified and documented? |
| **Bridges** | Are bridge figures between clusters identified? |
| **Isolates** | How many candidates have 0-1 connections? Are they valid? |
| **International links** | Do international candidates connect to the core? |

---

## Output

**Output file**: `intelligence/leader-research/tam-search/07-AUDIT-REPORT.md`

```markdown
# TAM Audit Report — [Date]

## Executive Summary
[3-5 bullet summary of the TAM's current health]

## Audit Scores

| Dimension | Health | Grade |
|-----------|--------|-------|
| Completeness | [%] | A-F |
| Domain Coverage | [%] | A-F |
| Demographics | [assessment] | A-F |
| Scoring Consistency | [assessment] | A-F |
| Data Freshness | [assessment] | A-F |
| Network Health | [assessment] | A-F |
| **Overall** | | **[grade]** |

## Detailed Findings
[By dimension, with specific names and data]

## Priority Actions

### Immediate (this week)
1. [specific action with candidate names]
2. [specific action]

### Short-term (this month)
1. [specific action]
2. [specific action]

### Ongoing
1. [specific action]
2. [specific action]

## Recommended Skill Runs
- `/tam-discover [domain]` — to fill domain gaps
- `/tam-score [names]` — to score unscored candidates
- `/tam-profile [names]` — to deepen thin profiles
- `/tam-international [region]` — to improve global representation
- `/tam-network-map [scope]` — to strengthen network data
```

---

## Key Rules

1. **Be honest and specific.** Name names, cite numbers, flag gaps directly. Vague "could be improved" assessments are useless.
2. **Prioritize by impact.** A missing profile for a 95-score candidate matters more than for a 55-score one.
3. **The TAM is finite by design.** The goal is not "more candidates" but "the right candidates, well-researched." Quality over quantity.
4. **Cross-reference all audit dimensions.** A domain gap + a demographic gap in the same area = high priority fix.
5. **Produce actionable recommendations** — every finding should map to a specific skill invocation or research task.
6. **This audit should be run periodically** (quarterly recommended) to keep the TAM healthy.
7. **Never delete candidates** based on audit findings. Flag them for review; let the human decide.
8. **Compare to the 2028 vision.** The Movemental scenius targets ~100 curated leaders. How close is the TAM to supporting that selection?
