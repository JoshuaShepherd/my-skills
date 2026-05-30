---
name: movement-leader-substrate
description: Author the machine-readable substrate document for a movement leader — identity resolution, relational traversal, conceptual indexing, voice fidelity. Produces a single `{SLUG}_RESEARCH_COLLATED.md` matching the canonical substrate schema. Use when creating or refreshing the primary research artifact for a movement leader. NOT a consulting deliverable — no fit scores, gap analyses, or marketing playbooks.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# Movement Leader Substrate

Produce the **canonical substrate document** for a movement leader at `docs/movement_leader_research/{slug}/{SLUG}_RESEARCH_COLLATED.md`. The substrate is a machine-readable corpus that downstream systems (RAG, agent context, voice agents, network graphs, page generators) consume.

## Invocation

```
/movement-leader-substrate $ARGUMENTS
```

`$ARGUMENTS`:
- A leader name or slug: `Alan Hirsch`, `alan-hirsch`, `Brad Brisco`
- `--refresh` to regenerate from existing per-topic source files without re-running web research
- `--from-research` to assume `docs/movement_leader_research/{slug}/` source files exist and only build the substrate
- Empty → ask for the leader

## What this skill IS

A single output, one file: `{SLUG}_RESEARCH_COLLATED.md` serving four functions only.

| Function | What it enables | Substrate sections |
|----------|-----------------|--------------------|
| **Identity resolution** | Disambiguate the subject from namesakes; canonical biographical facts | Identity, Disambiguation, Editorial bio |
| **Relational traversal** | Walk co-author, endorsement, organizational, intellectual-influence edges | Network graph, Intellectual genealogy, Organizational affiliations |
| **Conceptual indexing** | Look up frameworks, books, themes, claims by name | Frameworks, Bibliography, Theme map, Content analysis, Theological positioning |
| **Voice fidelity** | Generate or audit content in the leader's voice | Voice fingerprint (weighted markers, hallmark lexicon, antithesis prohibition, representative quotes) |

## What this skill IS NOT (do not include)

These belong to OTHER skills or other documents. **Never include in the substrate**:

| Excluded | Lives elsewhere |
|----------|-----------------|
| Movemental Fit Score / Fit Verdict (1–10 rating) | `tam-profile` (separate consulting artifact) |
| NOTs assessment ("content is NOT translated", etc.) | `tam-profile` |
| Gap analysis as a strategic deliverable | Removed; only factual content-gap tables are allowed in Distribution inventory |
| Content marketing playbook / Top-5 opportunities | Separate marketing artifact, not substrate |
| Fragmentation narrative ("the story of fragmentation") | Factual inventory only; no narrative framing |
| Revenue model / monetization estimates | Out of scope |
| Audience persona / psychographic narrative | Out of scope |
| Logo URLs / strip groups / logo quality | `affiliation-scrape` (different output channel for logo strips) |
| Per-platform follower deep-dive narrative | Reach metrics table only — no commentary |

If you find yourself writing prose like "the opportunity for Movemental is..." or "this leader's strength is...", stop. That is consulting, not substrate.

## Canonical schema

The output file MUST follow this section order and these table schemas. Reference implementation: [docs/movement_leader_research/alan-hirsch/ALAN_HIRSCH_RESEARCH_COLLATED.md](docs/movement_leader_research/alan-hirsch/ALAN_HIRSCH_RESEARCH_COLLATED.md) and [scripts/build-alan-hirsch-substrate.py](scripts/build-alan-hirsch-substrate.py).

### Front matter

```
# {Full Name} — Movement Leader Research (Substrate)

**Slug:** `{slug}`
**Version:** 2.0.0 (substrate)
**Last updated:** {YYYY-MM-DD}
**Purpose:** Machine-readable corpus for identity resolution, relational traversal, conceptual indexing, and voice fidelity. Not a consulting report.
```

### 1. Identity

A flat table. Every row needs a source citation. Required fields:

```
| Field | Value | Source |
|-------|-------|--------|
| Full legal name | ... | [URL] |
| Known as | ... | ... |
| Born | YYYY-MM-DD | ... |
| Birthplace | ... | ... |
| Childhood | ... | ... |
| Current location | ... | ... |
| Nationality | ... | ... |
| Heritage | ... | ... |
| Primary roles | ... | ... |
| Primary organizations | ... | ... |
| US sponsor (if applicable) | ... | ... |
| Spouse / partner | ... | ... |
| Education | ... | ... |
| Coined term (if applicable) | ... | ... |
```

### 2. Disambiguation

Required for any leader whose name returns ≥ 2 distinct public figures. Format:

```
{N} public figures named {Name} — **subject is #{X} only**.

| # | Identity | Disambiguate with | Exclude |
|---|----------|-------------------|---------|
| 1 | **{subject}** — {one-line distinguisher} | {distinctive terms} | — |
| 2 | {namesake} — {distinguisher} | {their terms} | {our subject's terms} |

**Reliable modifiers:** {3-5 search terms that uniquely retrieve the subject} — combined with exclusion of {namesake terms}.
```

If only one public figure with this name exists, write: `No disambiguation required — unique public figure.`

### 3. Editorial bio

2–3 paragraphs. Pull from `committed-voice.md` if present. Should answer:
- Where they came from (origin, formation context)
- What they built / what frameworks they're known for (with the magnum opus named)
- Their current institutional footprint

### 4. Timeline

```
| Year(s) | Milestone | Organization / work | Source |
```

Birth → present. Include conversion / formation events, education, founded orgs, magnum opus publications, current roles.

### 5. Frameworks

One subsection per named framework. Each gets a 5-row table:

```
### {Framework name}

| Field | Value |
|-------|-------|
| Introduced | {year + work} |
| Components | {numbered list inline} |
| Visual / model | {description; "—" if none} |
| Adoption evidence | {concrete numbers, programs, denominations} |
| Source | [link to canonical work] |

{1–2 sentence summary of the framework's core argument.}
```

Frameworks must be **named** (proper noun or trademark-able phrase). "Discipleship" is not a framework. "mDNA / Apostolic Genius" is.

### 6. Bibliography

Full books table — every published book, in newest-first order:

```
| Title | Author(s) | Publisher | Year | ISBN-13 | Key themes | One sentence | URL |
```

`One sentence` is a single sentence (≤ 200 chars) describing the book's argument. `URL` is the canonical retail page (Amazon preferred; publisher page acceptable).

After the table:

```
**Summary:** {N} entries ({M} unique titles); {S} solo, {C} co-authored; publishers {first-year}–{last-year} across {P} imprints; ~{ratings} Goodreads ratings ({editions} editions). Sources: ...
```

#### Theme map

```
| Theme | Primary works |
```

#### Content analysis (structured)

Use the structured Content Analysis template (Primary / Secondary / Emerging themes, each with Description / Key Works / Centrality 1–10).

#### Recommended reading order

```
| Order | Work | Rationale |
```

Numbered 1–N. Rationale is one line per book — why it sits at that position in the curriculum.

### 7. Voice fingerprint

#### Weighted markers (must sum to 100%)

```
| Marker | Target | Weight |
|--------|--------|--------|
| {Marker 1} | ≥ 0.7 | 30% |
| {Marker 2} | 0.5–0.8 | 25% |
| ...
| **Coherence target** | ≥ 0.75 | — |
```

5 markers, weights summing to 100%. Each marker is a measurable voice trait, not a vibe.

#### Hallmark lexicon (9+ terms)

Inline comma-separated. These are the leader's signature terms — words that, in combination, identify their writing.

#### Antithesis prohibition (non-negotiable)

One paragraph naming the specific anti-pattern the leader avoids (e.g. "Do not use contrastive negation→affirmation patterns: 'not X but Y'..."). Cite the source file from which this prohibition was derived. If no such prohibition is documentable from the corpus, write: `No documented antithesis prohibition.`

#### Representative quotes (5+)

Direct quotes from the corpus, each with attribution to the source work:

```
> "{exact quote}" — *{work}*, {context}
```

### 8. Theological positioning

```
| Domain | Position |
|--------|----------|
| Tradition | ... |
| Ecclesiology | ... |
| Missiology | ... |
| Leadership | ... |
| Christology | ... |
| Anthropology / formation | ... |
| Culture | ... |
```

#### Distinctive claims (bulleted)

What ONLY this author says — claims that distinguish them from peers in the same tradition.

### 9. Intellectual genealogy

#### Upstream influences

```
| Person | Ideas adopted | Source |
```

#### Downstream impact (documented)

```
| Channel | Evidence |
```

#### Peer dialogue

```
| Person | Relationship | Shared themes |
```

#### Constructive tensions (documented)

```
| Counterparty | Topic | {Subject} position | Source |
```

Only include if public tensions are documentable from URLs. Empty section is acceptable.

#### Comparable authors (reach / genre, not affinity scores)

```
| Author | Overlap |
```

### 10. Network graph

#### Co-authors

```
| Person | Joint works | Edge weight | Notes |
```

Edge weight 1–10. Co-authorship of N books = 3 + (2×N) bounded at 10.

#### Endorsements received (sample)

```
| From | For | Year | URL / note |
```

#### Organizational affiliations

Structured list of organizations founded, led, or affiliated with. NOT logo data.

#### JSON graph (nodes + edges)

```json
[ {"id": "...", "name": "...", "type": "person|org"} ]
```

```json
[ {"source": "...", "target": "...", "type": "co-author|endorsement|founder|board|...", "weight": 1-10} ]
```

### 11. Reach metrics

Single flat table — no narrative:

```
| Signal | Value | Date | Source |
```

Examples: assessment completions, Goodreads ratings, Twitter followers, podcast appearances count, Google Scholar profile presence, Wikipedia presence.

### 12. Distribution inventory

Factual catalogue ONLY — no marketing analysis. Subsections: Books, Articles & blogs, Audio, Video, Courses & assessments, Websites & orgs, Social, Academic / papers, Translations.

If the leader has a content gap (e.g. flagship book has no audiobook), record it as a row in a `Content gap table (factual state only)`. Do NOT extend into "opportunities" or "what they should do."

### 13. Sources (provenance)

```
| URL | Verifies |
```

Plus a list of digital-presence file pointers for traceability.

### 14. Open questions

Bulleted list of facts the research could not establish. Honesty over fabrication.

## Process

### Phase 1 — Check what exists

```bash
ls docs/movement_leader_research/{slug}/
```

If the per-topic source files exist (`profile/`, `content/`, `network/`, `media/`, `digital-presence/`, `analysis/`), this is `--refresh` mode: read those files and assemble the substrate.

If only a `committed-voice.md` exists, this is a thin profile — flag what's missing and offer to run targeted research.

If the directory does not exist, this is a cold start — research before writing.

### Phase 2 — Source the data

For each substrate section, the canonical source files (when they exist):

| Substrate section | Source files |
|-------------------|--------------|
| Identity | `profile/identity.md`, `identity-verification.md`, `committed-voice.md` |
| Disambiguation | `profile/identity.md` (disambiguation section), `identity-verification.md` |
| Editorial bio | `committed-voice.md` editorial bio block |
| Timeline | `{SLUG}_TIMELINE.md`, `profile/biography.md` |
| Frameworks | `{SLUG}_AUTHOR_PROFILE.md` (frameworks), `profile/theology.md`, content files for adoption evidence |
| Bibliography | `content/books.md` |
| Theme map + Content analysis | `analysis/content-analysis.md` |
| Voice fingerprint | `profile/voice-analysis.md`, `committed-voice.md` signature_frameworks |
| Theological positioning | `profile/theology.md`, `analysis/content-analysis.md` (theological positioning) |
| Intellectual genealogy | `network/collaborators.md`, `profile/theology.md` |
| Network graph | `network/collaborators.md`, `network/endorsements.md`, `network/organizations.md` |
| Reach metrics | `digital-presence/*`, `content/*`, `media/*` |
| Distribution inventory | `digital-presence/*`, `content/*`, `fragmentation-story.md` (factual inventory only) |
| Sources | `sources.md` |

For cold-start research without these files, delegate the data-gathering phase via the Agent tool to a research subagent rather than running 30+ WebSearch calls from the main thread.

### Phase 3 — Write the substrate

Write directly to `docs/movement_leader_research/{slug}/{SLUG_UPPER}_RESEARCH_COLLATED.md`.

- Preserve source citations as inline links or `[^source-id]` footnotes after non-obvious claims
- All tables use the schema above — do not invent new columns
- Empty sections get an explicit note (`No documented {X}.`) rather than being omitted
- Never fabricate numbers, dates, ISBNs, or quotes. If you cannot verify, leave the cell empty or use `unknown`.

### Phase 4 — Update the manifest

Write `docs/movement_leader_research/{slug}/{SLUG_UPPER}_COLLATION_MANIFEST.json`:

```json
{
  "slug": "{slug}",
  "version": "2.0.0",
  "generated_at": "YYYY-MM-DD",
  "sources": [
    { "path": "profile/identity.md", "sha256": "...", "wordCount": N, "sectionsUsed": ["Identity", "Disambiguation"] }
  ]
}
```

### Phase 5 — Verify

- Every section from the canonical schema is present (or marked as "No documented X")
- No prohibited content (fit score, NOTs, marketing playbook, opportunity ladder, revenue projections, persona narratives, logo URLs)
- All numeric claims trace to a source file or URL
- Voice marker weights sum to 100%
- Bibliography is newest-first and includes ISBN-13 where available
- JSON graph parses

## Key rules

1. **Substrate, not consulting.** If a section reads like a recommendation, remove it. The substrate enables decisions; it does not make them.
2. **Every claim is traceable.** Inline link, footnote, or source file path after each non-obvious claim.
3. **Schema-fidelity over completeness.** A section with 3 rows that match the schema is better than a section with 30 rows that drift into commentary.
4. **No fabrication.** "Unknown" or "Not catalogued" is always preferable to a guessed number.
5. **One file per leader.** Substrate is a single document. The per-topic source files remain on disk untouched; the substrate is the consolidated, schema-conformant read surface.
6. **Disambiguation is required** if a name search returns multiple distinct figures. Skipping this enables identity confusion downstream.
7. **Antithesis prohibition is the voice fingerprint's load-bearing element.** If you cannot find it, search the corpus until you can — it usually shows up as the leader's most-corrected reader misreading.
8. **The reference implementation is Alan Hirsch.** When in doubt, look at `docs/movement_leader_research/alan-hirsch/ALAN_HIRSCH_RESEARCH_COLLATED.md` for what each section should look like at the schema's expected depth.
