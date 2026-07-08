---
name: movement-leader-voice
description: >-
  Authors the canonical voice and style guide for a movement leader at
  docs/voice/{SLUG}_VOICE.md — corpus-grounded markers, prose character, failure
  modes, audit rubric, and sample passages. Use when standing up or refreshing a
  leader's voice identity, generating docs/voice, running movement-leader-voice,
  or preparing themes/content in the leader's voice. Distinct from Movemental
  company voice (movemental-voice) and generic voice-designer.
disable-model-invocation: true
---

# Movement Leader Voice

Read a movement leader's **own corpus** and produce the canonical guide at `docs/voice/{SLUG_UPPER}_VOICE.md`. Downstream systems (Writing Studio, AI Lab, voice-fidelity evals, editors) load this file.

**Discipline:** describe the voice from the corpus, on the leader's own terms — never compare to another author. Every marker, phrase, and sample anchors in something the leader actually wrote or said.

## Invocation

```
/movement-leader-voice {leader-slug}
/movement-leader-voice Brad Brisco
/movement-leader-voice --audit docs/drafts/article.md
/movement-leader-voice --refresh
```

Run from the **leader repo root** (e.g. `movement-leader-websites/michael-cooper/`).

| Flag | Effect |
|------|--------|
| `{slug}` or display name | Defaults to cwd repo if obvious |
| `--audit {path}` | Score draft against Section 16 rubric; do not rewrite guide |
| `--refresh` | Regenerate from corpus; append version-history row |
| (empty) | Infer leader from repo; ask if ambiguous |

## Inputs (priority order)

| Source | Path | Yields |
|--------|------|--------|
| **Book corpus** | `docs/books/{book-slug}/chapters/*.md` | **Highest** — rhythm, lexicon, samples |
| Voice analysis | `docs/movement_leader_research/{slug}/profile/voice-analysis.md` | Marker hypotheses |
| Collated substrate | `**/{SLUG}_RESEARCH_COLLATED.md` | Fingerprint, quotes |
| Biography | `**/profile/biography.md`, `**/_misc/committed-voice.md` | Approved first-person |
| Articles / talks | `docs/**/articles/`, transcripts | Speaking vs writing |

If `docs/books/` is empty, derive from research dossier and mark the guide **research-grounded** (lower confidence; tag unverified sample passages).

## Execution protocol

**Read this skill, then execute phases 1–3 to completion** unless `--audit` (audit-only mode).

### Phase 1 — Inventory

```bash
ls docs/books/*/chapters/ 2>/dev/null
ls docs/movement_leader_research/*/profile/voice-analysis.md 2>/dev/null
ls docs/voice/ 2>/dev/null
```

For large corpora, delegate per-book reading via **Task** (`subagent_type: explore`, one agent per book) → each returns markers, lexicon, structural habits, 3–5 exact sample passages with attribution. Synthesize centrally.

### Phase 2 — Write

Write `docs/voice/{SLUG_UPPER}_VOICE.md` with all **18 sections** per [reference.md](reference.md). Marker weights sum to 100%. Every sample passage is an exact, attributed quote.

### Phase 3 — Verify

- All 18 sections present; titles match schema
- Weights sum to 100%; measurable targets per marker
- Self-contained — no cross-author comparisons
- Sample passages exact and sourced; "Do not invent" lists specific refusals
- Pre-output checklist and audit rubric reference the same markers
- Sources list real files read

Print a session report: slug, output path, corpus basis, marker count, sample-passage count.

## Key rules

1. **Self-contained, never comparative.**
2. **Corpus-grounded** — read books before writing the guide.
3. **No fabricated quotes or biography.**
4. **Markers are measurable** — numeric targets, not mood words.
5. **One canonical file** — `docs/voice/{SLUG_UPPER}_VOICE.md`; leave research files untouched.
6. **Reference implementation:** brad-brisco repo, `docs/voice/BRAD_BRISCO_VOICE.md`.

## Additional resources

- Full 18-section schema: [reference.md](reference.md)
