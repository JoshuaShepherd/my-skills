---
name: tam-profile
description: Score a movement leader's fit with the Movemental platform — a consulting deliverable (Fit Score 1–10, NOTs assessment, opportunity ladder). Distinct from the substrate. For the canonical research artifact, use `movement-leader-substrate`.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Profile (Fit Scoring)

This skill produces a **consulting-style fit assessment** for a movement leader against the Movemental platform. It is intentionally narrow: a Fit Score, a NOTs assessment, and an opportunity ladder.

> **For the canonical research artifact, use [`movement-leader-substrate`](../movement-leader-substrate/SKILL.md).** That skill writes `{SLUG}_RESEARCH_COLLATED.md` — the machine-readable corpus consumed by downstream systems. This skill (`tam-profile`) is a separate deliverable used for prioritizing outreach, not for substrate.

## Invocation

```
/tam-profile $ARGUMENTS
```

`$ARGUMENTS`: a leader's full name. Examples: `Mark Sayers`, `Danielle Strickland`, `Steve Addison`.

## Output

A single file: `docs/movement_leader_research/{slug}/tam-profile.md`.

Required sections only — keep this tight, no padding:

```markdown
# {Name} — TAM Profile (Fit Assessment)

**Date:** YYYY-MM-DD
**Movemental Fit Score:** X/10
**Fit Verdict:** Full Fit / Content-No-Movement / Affinity / Not Fit

## Three Recognitions
- **Movement Leader:** [yes/no + 1-line evidence]
- **mDNA Aligned:** [yes/no + 1-line evidence]
- **Content Creator:** [yes/no + 1-line evidence]

## NOTs Assessment
- [ ] Content is NOT translated / multilingual
- [ ] Content is NOT structured or repurposed across formats
- [ ] Content is NOT interconnected (books, courses, articles live in silos)
- [ ] Content is NOT owned / unified under one platform
- [ ] Content is NOT legible to AI systems
- [ ] Content is NOT optimized for discoverability (SEO/GEO)
- [ ] Content is NOT connected to an AI agent that reflects their voice

## Opportunity Ladder (top 5)
1. ...
2. ...

## Fit Score Justification
[2–3 sentences explaining the score based on theological alignment, content volume, audience size, revenue potential, network value, and gap severity.]

## Calibration Note
- Alan Hirsch = 8.6/10 (anchor)
- 9+ is exceptional, requires strong evidence
```

## Process

1. **Check for substrate first.** If `docs/movement_leader_research/{slug}/{SLUG}_RESEARCH_COLLATED.md` exists, read it — everything you need for scoring is already there. Do not re-research.
2. **If no substrate exists**, call `movement-leader-substrate` first. Substrate is the prerequisite, not a parallel artifact.
3. **Compute the Fit Score** from substrate data using the rubric below. Do not invent new facts.
4. **Write only the deliverable above.** No identity tables, no bibliographies, no frameworks. Those belong to the substrate.

## Fit Score Rubric (1–10)

| Dimension | Weight | What to evaluate |
|-----------|--------|-------------------|
| Theological alignment with mDNA | 25% | Substrate: Theological positioning + Distinctive claims |
| Content volume and quality | 20% | Substrate: Bibliography count, Reach metrics |
| Audience size and engagement | 20% | Substrate: Reach metrics |
| Revenue potential | 15% | Substrate: Distribution inventory |
| Network contribution value | 10% | Substrate: Network graph, Intellectual genealogy |
| Gap severity (how much Movemental solves) | 10% | NOTs assessment + Distribution inventory gaps |

## What this skill does NOT produce

These belong elsewhere — do not duplicate them here:

| Don't produce | Where it belongs |
|---------------|-------------------|
| Identity table, biography, disambiguation, timeline, frameworks, bibliography, voice fingerprint, intellectual genealogy, network graph | `movement-leader-substrate` |
| Logo strip data, logo URLs, logo quality | `affiliation-scrape` |
| Voice agent design | `voice-designer` |
| Welcome letter | `movemental-welcome-letter` |
| Committed-voice front matter | `movemental-committed-voice-bio` |

## Key rules

1. **Substrate is the source.** All scoring inputs come from the substrate. If a fact is missing from the substrate, add it to the substrate first — do not record it here.
2. **One file output.** `tam-profile.md` only. No multi-file dossier from this skill.
3. **No fabrication.** Every score component must trace to a substrate row.
4. **Calibrate against Alan Hirsch (8.6).** A 9+ rating must beat Hirsch on a documentable dimension.
