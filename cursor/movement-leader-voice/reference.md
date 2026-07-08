# Voice guide output schema

Reference implementation: **brad-brisco** repo, `docs/voice/BRAD_BRISCO_VOICE.md`.

## Header block

```markdown
# {Full Name} — Voice & Style Guide

**Purpose:** Canonical voice identity for Writing Studio, AI Lab, agents, and human
editors. Self-contained: describes how {Name} sounds, builds arguments, and uses
language — grounded in their published corpus, not in comparison to any other author.

**Status:** Canonical for `docs/voice/`
**Last updated:** {YYYY-MM-DD}
**Corpus basis:** {named books + research files actually read}
```

## How to Use This Document

Table: `Mode | What to load` — Write / Rewrite / Audit / Agent system prompt.

## Sections 1–18 (canonical titles)

1. **Who {Name} Is in Print and Speech** — roles, magnum opus, *N voices in one*, core operating principle, rhetorical posture, what they are not.
2. **The {N} Voice Markers** — `Marker | Weight | Target | What It Means`. Typically five markers; weights sum to 100%; coherence target (e.g. ≥0.75).
3. **How {Name} Sounds (Prose Character)** — register/tone; vocabulary `Preferred | Avoid`; structural habits; metaphor density; question frequency.
4. **{Signature Rhetoric}** — distinctive teaching device with canonical forms and when to use vs plain prose.
5. **Failure Modes (Never Sound Like These)** — `Failure mode | Example | Why it fails`.
6. **Order of Operations** — numbered argument sequence; dialogical vs homiletical tone.
7. **Argument Patterns** — Pattern A/B/C with steps and "use for" guidance.
8. **Signature Phrases and Recurring Moves** — grouped by theme; use naturally, never stuffed.
9. **Scripture and Citation Habits** — frequency, placement, favored moves; scholars they actually quote.
10. **Openings and Closings** — `Style | Example` tables; what to avoid as first line.
11. **Style and Mode Variants** — marker shifts across styles, modes, content forms.
12. **Speaking vs. Writing** — `Dimension | Writing | Speaking`.
13. **First-Person and Corpus Constraints** — approved first-person material; **Do not invent** list.
14. **Writing Studio Rules** — artifact output, voice self-check, corpus sourcing, tenant theme slugs.
15. **Pre-Output Checklist** — `[ ]` per marker + structural/refusal rules; coherence target.
16. **Voice Fidelity Audit** — 0.0–1.0 rubric per marker; automatic failures list.
17. **Sample Passages (Voice Anchors)** — exact corpus excerpts labeled by rhetorical move.
18. **Version History** — `Version | Date | Changes`.

Close with **Sources** — exact corpus files read.

## Deriving each element

- **Markers** — trait whose absence makes text "not them"; derived from what recurs and what the leader corrects in readers.
- **Vocabulary** — leader's real lexicon from corpus; include explicitly rejected terms.
- **Failure modes** — register the leader most reliably avoids.
- **Sample passages** — exact quotes only; drop a move if no real quote exists.
- **First-person constraints** — corpus-verifiable biography only; everything else under "Do not invent."

## Audit mode (`--audit {path}`)

Load the guide, score the draft against Section 16 rubric, report per-marker scores and automatic failures. Do not rewrite the guide.
