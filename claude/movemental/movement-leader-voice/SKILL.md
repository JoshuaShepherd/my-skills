---
name: movement-leader-voice
description: Author the canonical voice & style guide for a movement leader at `docs/voice/{SLUG}_VOICE.md` — a self-contained, corpus-grounded reference (five weighted voice markers, prose character, signature rhetoric, failure modes, argument patterns, signature phrases, citation habits, audit rubric, and sample passages) describing how this leader sounds, on their own terms, not by comparison to anyone else. Run inside a leader's website repo against `docs/books/`, `docs/movement_leader_research/`, and any other content. Use when standing up or refreshing a leader's voice identity for Writing Studio, AI Lab, agents, and human editors. Distinct from the Movemental company voice ([[movemental-voice]]) and the generic [[voice-designer]]. Reference implementation is the brad-brisco repo.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Movement Leader Voice

Read a movement leader's **own corpus** — full books, research dossier, articles, talks — and produce the **canonical voice & style guide** at `docs/voice/{SLUG_UPPER}_VOICE.md`. The guide is the single source of truth that downstream systems (Writing Studio, AI Lab personas, voice-fidelity evals, human editors) load to write, rewrite, or audit content in this leader's voice.

The defining discipline: **describe the voice from the corpus, on the leader's own terms.** The guide is self-contained — it never says "like Alan Hirsch but…" or compares the leader to another author. Every marker, phrase, and sample is anchored in something the leader actually wrote or said.

## Invocation

```
/movement-leader-voice $ARGUMENTS
```

`$ARGUMENTS`:
- A leader name or slug: `Brad Brisco`, `brad-brisco`. Defaults to the current repo's leader if obvious.
- `--audit {path}` → score an existing draft against the guide's markers (Section 16 mode); do not rewrite the guide.
- `--refresh` → regenerate the guide from the current corpus, preserving the version-history table and appending a new row.
- Empty → infer the leader from the repo; if ambiguous, ask.

## Inputs (in priority order)

Run from the leader's website repo root. Use whatever exists; never block on a missing source.

| Source | Path | What it yields |
|--------|------|----------------|
| **Full book corpus** | `docs/books/{book-slug}/chapters/*.md` | **Highest** — rhythm, vocabulary, structural habits, sample passages |
| Voice analysis (research) | `docs/movement_leader_research/{slug}/profile/voice-analysis.md` | Marker hypotheses, hallmark lexicon, antithesis prohibition |
| Collated substrate | `**/{SLUG}_RESEARCH_COLLATED.md` | Voice fingerprint, frameworks, representative quotes |
| Content/biography | `**/profile/biography.md`, `**/_misc/committed-voice.md` | Approved first-person material, roles, magnum opus |
| Articles / talks / transcripts | `docs/**/articles/`, `docs/workspace/`, transcripts | Speaking vs. writing contrast; signature moves |

If `docs/books/` is empty, derive what you can from the research dossier and say plainly that the guide is research-grounded rather than corpus-grounded (lower confidence; mark sample passages as `unverified` if not from primary text).

---

## Output schema — `docs/voice/{SLUG_UPPER}_VOICE.md`

Self-contained. Reference implementation: **brad-brisco repo, `docs/voice/BRAD_BRISCO_VOICE.md`** (18 sections). Match its depth and structure. Section titles below are canonical; keep them.

```
# {Full Name} — Voice & Style Guide

**Purpose:** Canonical voice identity for Writing Studio, AI Lab, agents, and human
editors. Self-contained: describes how {Name} sounds, builds arguments, and uses
language — grounded in their published corpus, not in comparison to any other author.

**Status:** Canonical for `docs/voice/`
**Last updated:** {YYYY-MM-DD}
**Corpus basis:** {named books + research files actually read}
```

Then a **How to Use This Document** table (`Mode | What to load` — Write / Rewrite / Audit / Agent system prompt), followed by the numbered sections:

1. **Who {Name} Is in Print and Speech** — Who they are (roles, magnum opus, formation), the *N voices in one* (their composite register), the **core operating principle** (their one governing rule, e.g. "theology before tactics"), the **rhetorical posture** (their default move toward a reader), and **what they are not** (the registers they never occupy).
2. **The {N} Voice Markers** — A `Marker | Weight | Target | What It Means` table. Typically five markers; weights sum to 100%; each target is a measurable floor/band (e.g. `≥0.7`, `0.4–0.7`). State the overall coherence target (e.g. `≥0.75`). Markers must be measurable traits, not vibes.
3. **How {Name} Sounds (Prose Character)** — Register & tone table; **vocabulary preferences** (`Preferred | Avoid` two-column table using the leader's actual terms); structural habits; metaphor density (images per 1000 words + a `Domain | Images they use` table); question frequency.
4. **{Signature Rhetoric}** — The leader's distinctive teaching device (e.g. paradigm-shift contrast pairs, chiasm, redefinition), with canonical forms and rules for when to use it vs. plain prose.
5. **Failure Modes (Never Sound Like These)** — `Failure mode | Example | Why it fails`. The registers that betray the voice (corporate consultant, detached academic, hype, vague encouragement, etc.), each with a concrete wrong example.
6. **Order of Operations** — The numbered sequence the leader follows when building an argument; note dialogical-vs-homiletical and epistemic tone.
7. **Argument Patterns** — The named structures (Pattern A/B/C…) the leader reuses, each with steps and "use for" guidance.
8. **Signature Phrases and Recurring Moves** — Grouped by theme; the leader's actual phrases. "Use naturally — never stuffed into every paragraph."
9. **Scripture and Citation Habits** — How they handle Scripture (frequency, placement, favored moves, what to avoid) and how they cite scholars/practitioners (to carry the argument, not perform scholarship); name the voices they actually quote.
10. **Openings and Closings** — `Style | Example` tables for how they open and close; what to avoid as a first line.
11. **Style and Mode Variants** — How marker emphasis shifts across styles (Explainer/Coach/Challenge…), modes (Teacher/Coach/Guide/Strategist…), and content forms (blog/article/chapter/lesson/social/email).
12. **Speaking vs. Writing** — `Dimension | Writing | Speaking` contrast; what loosens in spoken content.
13. **First-Person and Corpus Constraints** — **Approved first-person material** (only corpus-verifiable biography) and **Do not invent** (the specific fabrications to refuse). This section is load-bearing for hallucination control.
14. **Writing Studio Rules** — The operating rules when producing publishable content under the leader's name (output is the artifact, voice self-check, source from corpus, use tenant theme slugs).
15. **Pre-Output Checklist** — A `[ ]` checklist covering each marker's target plus the structural and refusal rules. Ends with the coherence target.
16. **Voice Fidelity Audit** — A 0.0–1.0 scoring rubric per marker (`Score | Marker1 | Marker2 | …`) and a list of **automatic failures**.
17. **Sample Passages (Voice Anchors)** — Direct excerpts **from the leader's published corpus**, each labeled by the move it demonstrates (theological declarative, definitional chiasm, term redefinition, practical diagnosis, etc.). These calibrate rhythm and confidence. Never fabricate a quote; attribute each to its work.
18. **Version History** — `Version | Date | Changes`.

Close with a **Sources** list of the exact corpus files read.

### Deriving each element

- **Markers** come from what recurs and what the leader *corrects* in readers. Read the books; the marker is the trait whose absence would make the text "not them."
- **Vocabulary tables** use the leader's real lexicon — pull preferred terms and the words they explicitly reject from the corpus.
- **Antithesis / failure modes**: find the register the leader most reliably avoids (often visible as their most-corrected reader misreading) and name it precisely.
- **Sample passages** must be exact quotes from primary text, each chosen to demonstrate one named move. If you cannot find a real quote for a move, drop the move — do not invent an exemplar.
- **First-person constraints** come from biography you can verify in the corpus/dossier. Everything not verifiable goes in "Do not invent."

---

## Process

### Phase 1 — Inventory the corpus

```bash
ls docs/books/*/chapters/ 2>/dev/null
ls docs/movement_leader_research/*/profile/voice-analysis.md 2>/dev/null
ls docs/voice/ 2>/dev/null
```

For a large corpus, delegate per-book reading to subagents via the Agent tool — each returns: recurring markers, lexicon (preferred/avoided), structural habits, 3–5 candidate sample passages with exact quotes and attribution. Synthesize centrally so markers and weights are consistent.

### Phase 2 — Write the guide

Write `docs/voice/{SLUG_UPPER}_VOICE.md` with all 18 sections. Markers' weights must sum to 100%. Every sample passage is a real, attributed quote.

### Phase 3 — Verify

- All 18 sections present; section titles match the schema.
- Voice marker weights sum to 100%; each has a measurable target.
- The guide is **self-contained**: no "like {other author}" comparisons anywhere.
- Every sample passage is an exact quote with a source; no fabricated quotes.
- "Do not invent" lists the specific biographical fabrications to refuse.
- Pre-output checklist and audit rubric are both present and reference the same markers.
- Sources list the real files read.

## Key rules

1. **Self-contained, never comparative.** The guide describes this leader on their own terms. Strip every cross-author comparison.
2. **Corpus-grounded.** Markers, lexicon, and especially sample passages trace to the leader's actual text. Read the books before writing the guide.
3. **No fabricated quotes or biography.** Sample passages are exact and attributed. First-person material is corpus-verifiable; everything else is explicitly listed under "Do not invent."
4. **Markers are measurable.** Each of the five markers is a trait with a numeric target, scorable in the audit rubric — not a mood word. Weights sum to 100%.
5. **One file per leader.** `docs/voice/{SLUG_UPPER}_VOICE.md` is the canonical guide; the research files stay untouched as sources.
6. **Distinct from neighbors.** This is the *individual leader's* voice — not the Movemental company voice ([[movemental-voice]]) and not a generic persona ([[voice-designer]]).
7. **Reference implementation is brad-brisco.** When a section's depth is unclear, open the brad-brisco repo's `docs/voice/BRAD_BRISCO_VOICE.md` and match it.
