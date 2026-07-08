---
name: pathway-content-author
description: >-
  Generate the full markdown content for any Movemental pathway page — all twelve canonical
  sections — in the documented voice and style of a given author, grounded in that author's own
  books and research in the repo (the books corpus and movement_leader_research /
  dashboard-content). GENERAL skill: works for any tenant author and any pathway theme once an
  author and a theme are given. Use it whenever someone wants to write, draft, or generate the
  content for a pathway page — e.g. "write the [theme] pathway in [author]'s voice", "generate
  the pathway content for [author] on [topic]", "draft the [slug] pathway from [author]'s books",
  or loosely "do the [author] pathway on [theme]". Produces corpus-grounded, voice-applied,
  four-necessities-complete pathway markdown (the Phase 1 narrative content) that feeds the
  code-level pathway-author and pathway-audit skills. It is the CONTENT layer; it does not build
  the page template or the code-level [slug].ts.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

Generate pathway page content: $ARGUMENTS

`$ARGUMENTS` should name the **author** and the **pathway theme** (and may add any standard
parameter below). Example: `author: brad-brisco, theme: Bivocational Mission, reframing: "What
if your job is not what you do to fund the mission, but part of the mission itself?"`. If the
author or theme is missing, ask for them before proceeding — they are the two required inputs.

---

## What this skill does, and where it sits

A Movemental pathway page is the canonical **twelve content sections** authored in the tenant
author's voice and grounded in that author's corpus. The page template (hub and individual
page) already exists. This skill produces the thing the template needs: **the markdown content
of the twelve sections**, written in the right author's voice, drawn from that author's books,
with citations, the four pedagogical necessities discharged, and the standard parameters set.

It is the manual's **"Phase 1 — Pathway design"**, generalized across authors and made
voice-aware and corpus-grounding. It runs *before* the code-level `pathway-author` skill (which
turns this markdown into `src/lib/content/pathways/[slug].ts`) and before `pathway-audit`.

It does **not**: build the HTML/React page template, write the code-level `[slug].ts`, configure
the AI Lab agent, or invent the author's positions. Stop at the reviewed markdown unless asked
to hand off to `pathway-author`.

## The prime directive: the author's real voice, the author's real corpus

Two non-negotiables, inherited from the platform's publication gates:

- **Corpus-grounding.** Every framework, claim, story, historical example, and practice traces
  to something the author actually wrote or said, found in the repo. Never invent a position the
  author has not taken. If the corpus does not support a section, say so and narrow the section —
  do not fabricate.
- **The author's own voice — not a generic "thought-leader" voice, and not another author's
  voice.** Load *this* author's documented voice from the repo and apply it. Alan Hirsch does not
  sound like Brad Brisco; a pathway written in the wrong voice is a failure even if every fact is
  right.

If you cannot find the author's voice documentation or corpus in the repo, stop and tell the
user where you looked — do not proceed on a guessed voice.

---

## Standard parameters

Resolve these before generating. Required inputs are the first two; the rest are derived from the
repo (and confirmed with the user) when not supplied.

| Parameter | Required | How to resolve if absent |
|-----------|:--------:|--------------------------|
| `author` | **yes** | — (ask). A tenant/leader slug, e.g. `alan-hirsch`, `brad-brisco` |
| `theme` / `title` | **yes** | — (ask). The pathway's subject |
| `reframing_question` | recommended | Draft one from the theme + the author's framing of it in the corpus, then confirm with the user. This is the disturbance that opens the formation work |
| `slug` | derived | Kebab-case the theme (e.g. `bivocational-mission`) |
| `companion_pillar` | derived | Look up the author's pillar map (research / dashboard-content); ask if unclear |
| `primary_corpus` | derived | The book(s) the theme draws from; pick from the author's bibliography by theme match; confirm |
| `companion_course` | optional | Link if a matching course exists; otherwise omit |
| `output_path` | derived | Default `content/pathways/<author>/<slug>.md` (or the user's chosen location) |

---

## Workflow

Work through these in order. Steps 1–2 are research; step 3 is generation; steps 4–5 are
checking and output. Read the reference file named in each step before doing that step.

### 1. Resolve the author and load their voice
Read **`references/voice-application.md`**. Locate this author's voice documentation in the repo
(in priority order: a dedicated voice skill such as `alan-voice` if one exists; the author's
`dashboard-content/` Part III — Voice & Editorial Identity; the raw
`movement_leader_research/<author>/` voice files). Build a short **working voice profile**: the
author's markers, signature moves, anti-patterns, and the rhetorical posture. You will apply this
in step 3 and check against it in step 4.

### 2. Gather the corpus material for this theme
Read **`references/corpus-gathering.md`**. Identify the primary corpus draws (books) for the
theme, then gather, *per canonical section*, the specific material that section needs — the
framework's source chapter, the author's biblical engagement, the historical parallels, the
narrative cases, the embodied practices, the distortions the author names. Record each with a
citation (book, chapter, page where available). This becomes the citations block. Gather before
you write; do not write a section you have no corpus for.

### 3. Generate the twelve sections, in canonical order, applying voice where it matters
Read **`references/pathway-content-model.md`** — it specifies what each of the twelve sections
must contain, the four-necessities pedagogy, and the per-section voice intensity. Write the
sections in order into the template (`assets/pathway-content-template.md`). Apply the author's
voice **in proportion to the section**: the hero, model, scripture thread, historical context,
cases, practices, distortions, and invitation are voice-forward; the curated resources, FAQs,
and AI Lab invitation are lighter and more structural. Ground every substantive section in the
corpus with citations.

### 4. Self-check before output
Verify, in this order (details in `references/pathway-content-model.md`):
- **Completeness** — all twelve sections present and in order; **cases are plural**; **distortion
  warnings present**; **AI Lab invitation present**; **invitation names one concrete next step**.
- **Pedagogy** — all four necessities discharged: dissonance (hero/model/distortions), action
  (practices), reflection (structured reflection questions, not a journaling gesture), community
  (a named cohort or practice partnership in the invitation).
- **Corpus-grounding** — every substantive section cites ≥3 corpus sources; no invented position;
  every citation resolves in the citations block.
- **Voice** — the working voice profile's markers are present and its anti-patterns absent; it
  reads as *this* author, not a generic voice.

If any check fails, revise before delivering.

### 5. Output and hand off
Write the completed markdown to `output_path`. Tell the user what you produced and offer the
handoff: this markdown is the input to the code-level `pathway-author` skill (which writes
`src/lib/content/pathways/<slug>.ts`) and to `pathway-audit`. Do not run those unless asked.

---

## Voice intensity by section (apply voice *where relevant*)

| Section | Voice intensity | Why |
|---------|-----------------|-----|
| 1 Hero / provocation | **Highest** | The reframing question is the author's sharpest move |
| 2 Overview | High | Sets the frame in the author's terms |
| 3 Model / framework | High | The author's own framework, in their language |
| 4 Scripture thread | High | The author's biblical engagement, not generic exegesis |
| 5 Historical context | High | The author's chosen parallels and how they tell them |
| 6 Cases | High | Narrative is voice-bearing; tell the cases as the author tells them |
| 7 Practices | **Highest** | Embodied invitation in the author's pastoral/prophetic register |
| 8 Curated resources | Light | Mostly pointers and links; voice in the framing line only |
| 9 AI Lab invitation | Light–Medium | Short, in-voice invitation to converse |
| 10 FAQs | Medium | Answers in voice; questions plain |
| 11 Distortion warnings | High | The author's own naming of cheap/reduced versions |
| 12 Invitation | **Highest** | The closing call; voice and concreteness both peak |

---

## Output format

Deliver one markdown file following `assets/pathway-content-template.md`: a parameter front-matter
block, the twelve sections in canonical order with their headings, inline citation markers, and a
citations block at the end that mirrors the footnotes-registry schema (claim, source, page, type).
State the author and theme used, the primary corpus drawn from, and note any section you had to
narrow for lack of corpus support.

---

## Examples

**Example 1 — full generate:**
Input: `author: brad-brisco, theme: Bivocational Mission`
Action: resolve voice + corpus → draft a reframing question and confirm → gather from Brad's
books on work/vocation/mission → write twelve sections in Brad's voice → self-check → output
`content/pathways/brad-brisco/bivocational-mission.md`.

**Example 2 — author named, theme loose:**
Input: "do the APEST pathway for Alan"
Action: theme = APEST vocation; load Alan's voice (via `alan-voice` if present); primary corpus =
5Q and The Permanent Revolution; companion pillar = the APEST pillar; generate and output.

**Example 3 — missing inputs:**
Input: "write a pathway page"
Action: ask which author and which theme before doing anything else — they are the two required
parameters.
