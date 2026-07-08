---
name: movement-leader-themes
description: Derive a movement leader's core themes from their own book corpus and research, then author the canonical theme docs in `docs/themes/` — a `CORE_THEMES.md` taxonomy (which themes earn pathway status, and why) plus one deep-dive `{slug}.md` per theme (12-section pathway content, grounded and cited). Run inside a leader's website repo against `docs/books/`, `docs/movement_leader_research/`, and any other content. Use when standing up or refreshing the theme system for a movement leader. Self-contained; reference implementation is the brad-brisco repo.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# Movement Leader Themes

Read a movement leader's **own corpus** — full books, research dossier, articles — and produce the canonical theme documents for their website in `docs/themes/`:

1. **`docs/themes/CORE_THEMES.md`** — the organizing taxonomy. Which 4–6 themes earn *pathway-level* status, which candidates are deliberately rejected (folded into tags/modules), how the themes relate as a single integrated argument, and how books map to themes. This is a *decision record*, not a brochure.
2. **`docs/themes/{slug}.md`** — one deep-dive per core theme: 12-section pathway content in the leader's voice, every substantive claim grounded in the corpus and footnoted.

The defining discipline: **themes are read out of the corpus, not imposed on it.** Read the full books before naming a single theme. Internet summaries and pre-existing config are inputs to *check against*, never the source of truth.

## Invocation

```
/movement-leader-themes $ARGUMENTS
```

`$ARGUMENTS`:
- A leader name or slug: `Brad Brisco`, `brad-brisco`. Defaults to the current repo's leader if obvious.
- `--taxonomy-only` → write `CORE_THEMES.md` only; skip the per-theme deep-dives.
- `--theme {slug}` → (re)write a single deep-dive file, assuming `CORE_THEMES.md` already exists.
- `--refresh` → regenerate from the existing corpus without re-deriving the taxonomy from scratch (keep the slug set, refresh content).
- Empty → infer the leader from the repo; if ambiguous, ask.

## Inputs (in priority order)

Run from the leader's website repo root. Use whatever exists; never block on a missing source.

| Source | Path | Weight |
|--------|------|--------|
| **Full book corpus** | `docs/books/{book-slug}/chapters/*.md` | **Highest** — read the actual chapters, not summaries |
| Book front matter / metadata | `docs/books/{book-slug}/*.md`, `README.md` | High — title, structure, publication year |
| Research dossier | `docs/movement_leader_research/{slug}/` | Medium — validates and contextualizes; may over/under-weight themes vs. the books |
| Collated substrate | `**/{SLUG}_RESEARCH_COLLATED.md` | Medium — theme map, frameworks, content analysis |
| Articles / resources | `docs/**/articles/`, `docs/*-resources/`, `docs/workspace/` | Medium — confirm themes, add tactical detail |
| Voice guide | `docs/voice/{SLUG}_VOICE.md` | Required for per-theme writing — the deep-dives must be in voice |
| Existing config | `src/lib/config/tenant.config.ts`, `src/lib/content/pathways/*.ts` | Check-against only — confirm or challenge, do not inherit blindly |

If `docs/books/` is empty, stop and say so: this skill derives themes from a book corpus. Offer to run against the research dossier alone only if the user confirms (lower-confidence output).

---

## Part A — `CORE_THEMES.md` (the taxonomy)

The taxonomy is an editorial argument with a decision record. Reference implementation: **brad-brisco repo, `docs/themes/CORE_THEMES.md`** (five themes derived from a six-book corpus).

### Section schema

```
# {Full Name} — Core Themes

**Purpose:** Fresh assessment of {Name}'s core themes after full book corpus
ingestion (`docs/books/`) and movement leader research. This document proposes
the organizing system for pathway pages, evergreen articles, and courses.

**Status:** Draft for review
**Last updated:** {YYYY-MM-DD}
**Corpus reviewed:** {N books}, research tree, {article sources}
```

1. **Executive Summary** — State the leader's work as a *single integrated argument*, not a topic grab-bag. Then the recommended **N core themes** in a table: `# | pathway slug | Title | Role in the corpus`. Justify why N is the right number (book architecture, audience, existing config). End with an explicit list of themes that appear in research but should **not** become pathways.
2. **Methodology** — A "What we read" table (`Source | Scope | Weight`) and the **assessment criteria**: a theme earns pathway status only if it passes all four tests — (1) Corpus centrality, (2) Distinctiveness, (3) Course viability, (4) Audience demand. State what keeps a theme *subordinate* (a method, a context, or a borrowed framework).
3. **The Integrated Argument** — How the themes relate. A flow diagram (fenced ASCII) showing the sequence/dependency, plus, where the corpus supports it, a table mapping the leader's own magnum-opus structure to the themes. This section is the strongest evidence for the theme count.
4. **Theme {n}: {Title}** (one block per theme) — with: `Slug`, `EEAT tags`, `One-line claim`; **What this theme is**; **What this theme entails** (`Layer | Content` table); **Primary corpus** (named books/chapters); **What belongs here (not elsewhere)**; **Pathway reframe** (`Usual question | Better question`); **Course outline (proposed)** (6 numbered lessons); **Why this earns/stays pathway status** (corpus evidence).
5. **Themes Considered and Rejected as Pathways** — `Candidate | Why it appeared in research | Why it does not earn a pathway`. This table is mandatory and is where intellectual honesty shows.
6. **Mapping: Books → Themes** — `Book (year) | Primary themes | Secondary themes`.
7. **Mapping: Pathways → Content Types** — `Theme | Evergreen articles | Book anchors | Course | AI Lab persona emphasis`.
8. **Relationship to Existing Platform Config** — Does this confirm or revise `tenantConfig.themes`? Recommend *content* adjustments, not architecture churn.
9. **Decision Record** — `Decision | Rationale`. Every non-obvious call (theme count, keeping X separate from Y, subordinating Z) gets a row.
10. **Sources** — file paths and URLs actually read.

### Deriving the themes (the hard part)

- Read **every** book's chapters before proposing a taxonomy. Note chapter-level investment — a theme that owns whole chapters across multiple books is pathway-grade; a theme that appears once is a tag.
- Prefer the leader's **own** organizing structure (how they sequence their magnum opus) over a topical clustering you invent.
- Name a theme with the leader's **own vocabulary** (their coined terms), not generic church-growth labels.
- 4–6 themes is the normal range. Resist inflation: a borrowed framework (cited from another author), a *method* (e.g. "paradigm shifts"), or a *context* (e.g. "post-Christendom") is subordinate, not a pillar.
- If existing config already names slugs, the default posture is **confirm and explain**, not reshuffle — unless the corpus genuinely contradicts the config, in which case say so in the Decision Record.

---

## Part B — `{slug}.md` (per-theme deep-dive)

Each core theme gets one file: full pathway content in the leader's voice, every substantive section carrying ≥3 grounded citations. Reference implementation: **brad-brisco repo, `docs/themes/discipleship.md`** (and its siblings).

**Load the voice guide first** (`docs/voice/{SLUG}_VOICE.md`). The deep-dive must pass that guide's voice markers. If the voice guide does not exist yet, run [[movement-leader-voice]] first.

### Front matter

```yaml
---
author: {slug}
title: {Theme Title}
slug: {theme-slug}
reframing_question: "{the provocation this pathway turns on}"
companion_pillar: {eeat-tag}
primary_corpus:
  - {Book (ch. N, "Chapter Title")}
companion_course: {course-slug}
group_order: [Understand, Examine, Apply, Go deeper]
theme_order: {n}
one_line_claim: "{the claim}"
last_updated: {YYYY-MM-DD}
---
```

### The 12 sections

1. **Hero / provocation** — Name the default assumption the reader holds, then turn it with the reframing question (bolded).
2. **Overview** — What this pathway helps the reader recover/do; end with the 2–3 concrete capabilities they'll gain.
3. **The model / framework** — The 2–4 named frameworks that reframe the conversation, each defined in the leader's terms.
4. **The scripture thread** — The passages the corpus actually leans on for this theme (woven, not proof-texted).
5. **The historical context** — Why the distortion exists; where the alternative has worked.
6. **The cases** — **Plural.** Two+ concrete, corpus-grounded witnesses (people, movements, moments the leader actually cites). Never fabricate a case; if the corpus frames the theme around a model figure and a movement, use those.
7. **The practices** — Numbered, concrete, startable-now actions, each footnoted. Theology before tactics — but real tactics.
8. **The curated resources** — Book/chapter anchors, companion pillar, companion course, vetted external works the leader endorses.
9. **The AI Lab** — Invite the reader to bring a real situation into the AI Lab companion, staying in this pathway's frame. No script.
10. **FAQs** — The real objections this theme provokes, answered in voice and cited.
11. **Distortion warnings** — ≥2 named failure modes (the reductions/counterfeits of this theme), each cited.
12. **Invitation** — One concrete next step with real people (named cohort/course + a do-it-now alternative), looping back to the theme system.

### Sections close with

- **Citations** — a `[^n]` list. Each: `claim: {what} · source: {Book, ch. N "Title"} · page: {range or —} · type: book|article|reference`. Every footnote must trace to the corpus; never invent a page or a quote.
- **Delivery note** — an HTML comment self-check: section count, cases-plural confirmation, distortions ≥2, four necessities present (dissonance / action / reflection / community), ≥3 citations per substantive section, voice profile applied, and an explicit "no fabrication" line.

### The four necessities (must all be present)

Every deep-dive must create **dissonance** (name the gap), prescribe **action** (practices), prompt **reflection** (structured questions), and point to **community** (named cohort/relationship). The delivery note verifies these.

---

## Process

### Phase 1 — Inventory the corpus

```bash
ls docs/books/*/chapters/ 2>/dev/null
ls docs/movement_leader_research/ 2>/dev/null
ls docs/voice/ docs/themes/ 2>/dev/null
```

Build a list of books (slug, title, chapter count, year) and note which research/voice artifacts exist. For a large corpus, delegate per-book reading to subagents via the Agent tool (one agent per book → returns chapter-level theme notes), then synthesize.

### Phase 2 — Derive and write the taxonomy

Apply the four-test filter, select 4–6 themes, write `docs/themes/CORE_THEMES.md`. Stop here if `--taxonomy-only`.

### Phase 3 — Write the per-theme deep-dives

Ensure the voice guide exists (run [[movement-leader-voice]] if not). For each theme slug, write `docs/themes/{slug}.md` with full front matter, 12 sections, citations, and delivery note. For a multi-theme run, one subagent per theme is appropriate — but every agent must load the same voice guide and the relevant book chapters.

### Phase 4 — Verify

- `CORE_THEMES.md`: every theme block has all required subsections; the rejected-themes table is present; the decision record explains every non-obvious call; sources list real paths.
- Each `{slug}.md`: 12 sections present; cases are plural and corpus-grounded; ≥2 distortions; ≥3 citations per substantive section; four necessities present; front matter complete; no fabricated pages, quotes, or biography.
- Cross-check: every slug in `CORE_THEMES.md` has a deep-dive file (unless `--taxonomy-only`), and no orphan deep-dive exists without a taxonomy entry.

## Key rules

1. **Read the books first.** No theme may be named before its supporting chapters are read. Research dossiers and config are checked against the corpus, never substituted for it.
2. **Themes are the leader's, in the leader's words.** Use their coined terms; resist generic church-growth labels and imported frameworks-as-pillars.
3. **Reject honestly.** The rejected-themes table and decision record are mandatory. A taxonomy with no rejections is under-examined.
4. **Every claim traces to the corpus.** Inline footnotes with book + chapter + page (or `—`). Never fabricate a page number, quote, case, or biographical detail.
5. **Deep-dives must be in voice.** Load `docs/voice/{SLUG}_VOICE.md` and pass its markers. Voice fidelity is not optional.
6. **Cases are always plural and always real.** If the corpus offers only a model figure and a movement, use those two — do not invent a contemporary planter.
7. **Confirm config by default.** When existing theme slugs exist, the strong prior is to confirm and explain; only revise when the corpus contradicts, and record why.
8. **Reference implementation is brad-brisco.** When a section's depth or shape is unclear, open the brad-brisco repo's `docs/themes/CORE_THEMES.md` and `docs/themes/{slug}.md` and match them.
