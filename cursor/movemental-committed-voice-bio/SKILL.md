---
name: movemental-committed-voice-bio
description: Generate the Committed Voices onboarding entry for a specific movement leader from their research dossier. Use when asked to "draft the committed-voice bio for <leader>", "generate Committed Voices entry for <slug>", or "extract committed-voices markdown for <author>". Reads the leader's research dossier under movemental-ai/docs/movement_leader_research/<slug>/ and emits one structured markdown file (YAML frontmatter + slightly-warm third-person editorial bio) that maps directly onto the CommittedVoice type rendered at /onboarding/committed-voices.
disable-model-invocation: true
---

Generate the Committed Voices markdown for the leader in `$ARGUMENTS`.

`$ARGUMENTS` is the author slug (`alan-hirsch`, `brad-brisco`, `jr-woodward`, `lucas-pulley`, `rowland-smith`, `liz-rios`, `jamie-roach`, `rob-wegner`, `neil-cole`, etc.) or a display name that resolves to a slug (kebab-case the legal name). If empty, ask the operator which leader to write for and list the available dossiers.

Optional flags inside `$ARGUMENTS`:
- `--no-save` → print the file to chat only, do not write to disk.
- `--save-to=<path>` → write to a specific path instead of the default.
- `--dry-run` → walk the dossier, report which extracted fields were/weren't found, do not draft.
- `--no-reserve` → omit the reserve fields (`signature_frameworks`, `lineage`, `sources`, `research_completed_at`) for callers that only want the v1 CommittedVoice slice.

---

## Source of truth

Canonical research dossier:

```
/home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/
```

A lighter mirror exists at `/home/josh/dev/01-Movemental-Core/movemental-visual-editor-main/docs/movement_leader_research/<slug>.md` (per-leader auth / tenant notes only — not enough to write the bio from).

Prefer the canonical `movemental-ai` location. Fall back to the visual-editor mirror only to cross-check the leader's display name, primary email, and any platform-side status notes.

The rendered surface this file feeds: `src/components/onboarding/committed-voices-task-page.tsx` driven by the `CommittedVoice` type in `src/lib/committed-voices.ts` of the `movemental-visual-editor-main` repo. Treat that type as the v1 contract.

---

## Phase 1 — Resolve the slug and locate the dossier

1. Normalize `$ARGUMENTS` to a slug:
   - Lowercase, kebab-case, strip punctuation. `"Alan Hirsch"` → `alan-hirsch`. `"JR Woodward"` → `jr-woodward`. `"L. Rowland Smith"` → `rowland-smith`.
2. Confirm the dossier directory exists:
   ```bash
   ls /home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/
   ```
   If missing, list available dossiers and ask the operator which to use:
   ```bash
   ls -1 /home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/ | grep -v '\.md$'
   ```
3. Hard requirement: at least one of `summary.md`, `profile/biography.md`, or `profile/identity.md` MUST exist inside the dossier (older dossiers may instead have `README.md` or `_staff/legacy/<SLUG_UPPER>_AUTHOR_PROFILE.md`). If none are present, stop and tell the operator the dossier is too thin — this skill is a translation skill, not a research skill, and depends on the upstream author-research pipeline having produced at least a baseline profile.

---

## Phase 2 — Read the dossier (in this priority order)

Read all of these that exist. Skip silently if missing.

1. `summary.md` (and `README.md` if present) — dashboard + executive summary, digital presence facts, current role, books list, podcast counts.
2. `profile/biography.md` — narrative bio + voice/character notes.
3. `profile/identity.md` — disambiguation hard facts (location, birth year, name spelling).
4. `profile/theology.md`, `content/frameworks.md` — structured author dossier (frameworks, distinctive positions).
5. `network/organizations.md` — org list (drives `credentials` + `secondary_links`).
6. `profile/voice-analysis.md` — voice markers, signature frameworks, themes.
7. `profile/calling-profile.md` — vocational arc (informs the second bio paragraph).
8. `fragmentation-story.md` — motivation framing (informs paragraph three's hinge).
9. `_misc/digital-presence-discovery.md` (and `digital-presence/*`) — verified URLs, social handles.
10. `content/books.md` (and `_misc/content-analysis-root.md`) — book titles, publishers, years.
11. Fallback only: older `_staff/legacy/<SLUG_UPPER>_*.md` profiles (`AUTHOR_PROFILE`, `RESEARCH_SUMMARY`, `VOICE_IDENTITY`, `CALLING_PROFILE`, `ORGS`, `COMPLETE_PROFILE`) when a freshly researched leader lacks the categorized files above.
12. Mirror file `…/movemental-visual-editor-main/docs/movement_leader_research/<slug>.md` — cross-check display name + platform-side notes only.

---

## Phase 3 — Extract the working set

Pull the following from the dossier into a working set in scratch context before drafting. Every value below maps onto a frontmatter field in the output file.

### Identity
- **display_name** — canonical, exactly as the dossier and the visual-editor mirror agree. Include any earned title (Rev., Dr., etc.) only if the dossier uses it consistently.
- **first_name_only** — for internal use; not emitted in output.
- **location_line** — "City, State" (US) or "Region & Region" (multi-base). Pull from `profile/identity.md` (Canonical Identity) or `_staff/identity-verification.md` Quick Facts. Examples: "Los Angeles area, California", "Colorado Springs, Colorado", "Central Florida & Puerto Rico".

### Role line
- **role** — one line, " · " separated, at most three entries, with current role first. Each entry is "<Title>, <Org>" or just "<Title>" when the org is in the title (e.g., "National Director, Forge America"). Pull from the *current* institutional role in `summary.md` / `README.md`, then the most load-bearing two founded or co-founded orgs. Drop honorary or historical roles. Hard ceiling 90 characters.

### Tagline
- **short_tagline** — one sentence, third person, 18–28 words. The leader's distinctive contribution in plain language. Avoid "thought leader," "voice in the space," "renowned." Anchor on something a reader can verify: a coined framework, a measurable scope, a category they are the first/only in.

### Themes
- **themes** — exactly three Title Case phrases, each ≤ 28 chars. These are the leader's load-bearing surfaces, not generic categories. Pull from `profile/voice-analysis.md` (Vocabulary and Terminology Preferences) and `content/frameworks.md` when present, else from the dossier's executive summary. Prefer specificity ("Mujerista theology") over generality ("Theology"). Don't use "Leadership" or "Discipleship" alone — too generic.

### Editorial bio (the prose)
- **editorial_bio** — 2 to 3 paragraphs, 150–220 words total. Third person, slightly warmer than a pure editorial register (see §Voice below and §Voice exemplars). Each paragraph must contain at least one proper noun specific to this leader (book title, org, co-author, city, framework name).

### Credentials
- **credentials** — 3 to 6 bullet lines. Each line: "<Role / Position>, <Org> — <one-clause why-it-matters>". The trailing clause is what differentiates this from a CV — it tells the reader why the credential is load-bearing. Examples:
  - "Founder, Passion2Plant — only national BIPOC-woman-led church planting network in the U.S."
  - "Adjunct, Fuller Theological Seminary"
  - "National Director, V3 Church Planting Movement"
  Drop credentials with no why-it-matters clause unless they are themselves famous enough (degrees, ordination lines, named seminary boards).

### Featured works
- **featured_works** — 3 to 5 entries. Each entry: `"<Title> (<Publisher>, <Year>)"` or for co-authored work `"<Title> (with <Co-author>, <Publisher>, <Year>)"`. Use the leader's *most-cited or most-load-bearing* works, not just their latest. Italicize is not needed in YAML strings — the rendering surface decides.

### Links
- **primary_url** — the leader's canonical personal/author domain. From `digital-presence/websites.md` or `_misc/digital-presence-discovery.md`. Absolute URL.
- **secondary_links** — 2 to 3 entries of `{ label, href }` for the leader's most load-bearing org sites or platforms (not social media). Use the org's display name as `label`. Absolute URLs.

### Reserve fields (omit with `--no-reserve`)
- **signature_frameworks** — 3 to 7 entries of `{ name, definition }`. The leader's load-bearing frameworks. Definition is one sentence. Pull from `content/frameworks.md` or `profile/theology.md` "Key Frameworks & Models" when present.
- **lineage** — optional `{ sources, peers, downstream }` — three to ten entries each, slugs preferred where the named person is also a movement leader in the network. Drawn from `_misc/network/collaborators.md` or `network/organizations.md` if present; otherwise omit entirely.
- **sources** — the filenames inside the dossier directory the skill actually consulted, relative paths. Drives provenance.
- **research_completed_at** — ISO date from the dossier `README.md` if present; else omit.
- **generated_at** — today's ISO date (the skill's run date).

If `--dry-run`, stop here and report the working set as a checklist of what was found and what is missing per the field list. Do not draft.

---

## Phase 4 — Draft the file

Follow the master spec below verbatim. The output is a single Markdown file with YAML frontmatter and one body section. Do not paraphrase the spec — re-read it on every invocation.

### Output file shape

```markdown
---
slug: <slug>
display_name: <Display Name>
role: <Title 1, Org 1 · Title 2, Org 2>
location_line: <City, State or Region>
short_tagline: >-
  <one sentence, 18–28 words, third person>
themes:
  - <Theme 1>
  - <Theme 2>
  - <Theme 3>
credentials:
  - <line 1>
  - <line 2>
  - <line 3>
  - <line 4>
featured_works:
  - <Title (Publisher, Year)>
  - <Title (Publisher, Year)>
  - <Title (Publisher, Year)>
primary_url: <https://…>
secondary_links:
  - label: <Org Display Name>
    href: <https://…>
  - label: <Org Display Name>
    href: <https://…>
# --- reserve fields (omit block entirely if --no-reserve) ---
signature_frameworks:
  - name: <Framework Name>
    definition: <one sentence>
  - name: <Framework Name>
    definition: <one sentence>
sources:
  - summary.md
  - profile/biography.md
  - <files actually consulted>
research_completed_at: <YYYY-MM-DD>
generated_at: <YYYY-MM-DD>
---

## Editorial bio

<paragraph 1>

<paragraph 2>

<paragraph 3 — optional, only if the total stays in budget>
```

The body uses a single H2 (`## Editorial bio`). Two or three paragraphs of continuous prose. No headers inside the body, no bullet lists, no italics-on-titles requirement — the rendering surface decides styling. Keep titles in plain text inside the prose; the YAML carries the structured copies.

---

## Phase 5 — Self-check before output

Run this checklist. If any item fails, revise in place before writing.

1. **YAML parses.** Every key is lowercase snake_case. Every list has at least one entry. No trailing colons without values.
2. **All required fields present and non-empty**: `slug`, `display_name`, `role`, `location_line`, `short_tagline`, `themes` (exactly 3), `credentials` (3–6), `editorial_bio` (the body section), `featured_works` (3–5), `primary_url`, `secondary_links` (2–3).
3. **Length budgets**:
   - `role` ≤ 90 characters
   - `location_line` ≤ 50 characters
   - `short_tagline` ≤ 200 characters and between 18 and 28 words
   - Each `theme` ≤ 28 characters
   - Each `credentials` line ≤ 110 characters
   - Each `featured_works` entry ≤ 90 characters
   - Editorial bio total word count between **150 and 220** (body section only, excluding the `## Editorial bio` header).
4. **Specificity**: every paragraph of the editorial bio contains at least one proper noun pulled from this specific dossier. If you swapped only the names, the bio should *not* fit another leader.
5. **URLs**: every URL is absolute (starts with `http://` or `https://`).
6. **No forbiddens** (from the master spec).

If any check fails, revise the offending field in place, then re-run the check.

---

## Phase 6 — Output and save

1. Print the file to chat as a continuous Markdown block.
2. Unless `--no-save`, write the file to:
   ```
   /home/josh/dev/01-Movemental-Core/movemental-ai/docs/movement_leader_research/<slug>/committed-voice.md
   ```
   If `--save-to=<path>` is set, write there instead. If the target file already exists, write to `committed-voice-<YYYY-MM-DD>.md` alongside it — do not overwrite a prior draft without the operator saying so.
3. Report back in one short message:
   - Slug + display name + current role used.
   - Editorial-bio word count.
   - Self-check pass/fail per item.
   - Path the file was saved to (or `not saved (--no-save)`).
   - Any required fields the dossier did not supply, with the choice you made (e.g. "no `location_line` in dossier; used Kansas City because Sentralized Conference runs there").

---

## Master spec (source of truth — re-read every invocation)

```
You are writing the Committed Voices entry for the Movemental dashboard
onboarding. This is the artifact a movement leader will see in the
"Committed Voices" task: a roster of peers who have already verbally
committed, rendered as cards. The new leader is meant to recognize the
roster and accept that they are joining the same cohort-shaped
commitment.

The entry is therefore an editorial bio about the leader, written for
other movement leaders, in third person. Its job is to be specific
enough that the reader trusts Movemental did the research, and warm
enough that the reader feels they are joining people, not entries in a
database.

INPUT
A research dossier for the leader, drawn from author-research outputs
under movemental-ai/docs/movement_leader_research/<slug>/. The dossier
contains some subset of: summary, profile/ (identity, biography,
theology, voice-analysis, calling-profile), network/organizations,
content/ (books, frameworks, content-audit), analysis/audience-analysis,
fragmentation story, and digital-presence inventory.

OUTPUT
One Markdown file with YAML frontmatter and one `## Editorial bio` body
section, conforming to the shape and field definitions in
§Phase 3 and §Phase 4 of this skill.

VOICE — slightly warmer than the baseline editorial register
The three existing Committed Voices entries (Liz Rios, JR Woodward,
Rowland Smith) are the calibration baseline. They are declarative,
dense with proper nouns, and devoid of marketing voice. The new entry
should match their *information density and refusal of buzzwords*, but
allow slightly more cadence and connective tissue. Concretely:

- One sentence per bio may carry a single human-temperature framing
  word that the baseline would omit ("distinct in tone," "live cohort
  operator's discipline"). Liz Rios's entry already does this; lean
  there rather than toward Woodward's tighter register.
- Connective phrases ("simultaneously across," "and brings," "alongside
  the") are fine where they earn their place. Avoid filler ("of course,"
  "in many ways," "it's worth noting").
- One light sentence-of-character per bio is allowed — something a
  trusted colleague might say about the leader. It must not be opinion;
  it must be inference from the dossier.
- Do not warm the bio by inserting adjectives. Warm it by varying
  cadence and naming concrete adjacencies.

VOICE — failure modes (never sound like these)
- Marketing register: "renowned thought leader," "shaping the
  conversation," "passionate about." Delete on sight.
- Generic affirmation: "has made significant contributions to."
- Boilerplate stat hype: "a STAGGERING three decades."
- Reflexive lists of three when two or four serve better.
- "Not X but Y" as the default move (one use, fine).
- Em-dash-comma cadence that reads as AI rhythm.
- "Author of" laundry lists; the YAML `featured_works` carries the
  list already, so the bio names two or three key titles in prose with
  brief context, not all of them.

VOICE — sentence-length variance
Vary sentence length deliberately. Some sentences are eight words. Some
are twenty-five. Some are forty. Do not pace the bio at one rhythm.

VOICE — proper nouns
Every paragraph must carry at least one specific proper noun from the
dossier: a book title, an org, a co-author, a city, a framework name,
or a verifiable scope number ("150,000+ APEST assessments," "18+ years
teaching"). This is the primary mechanism of credibility.

MUST APPEAR (across the bio, distributed)
- The leader's current institutional role, named explicitly.
- At least two of their books or major works, named.
- At least one named org or network they founded, co-founded, or lead.
- At least one specific co-author, collaborator, or institutional
  adjacency (where the dossier supplies one).
- At least one place-anchor (city, region, country) consistent with
  `location_line`.

MUST APPEAR (in the YAML frontmatter)
See §Phase 3. Required fields: `slug`, `display_name`, `role`,
`location_line`, `short_tagline`, `themes` (exactly 3), `credentials`
(3–6), `featured_works` (3–5), `primary_url`, `secondary_links` (2–3).

FORBIDDEN
- Hype words: "renowned," "world-class," "leading voice,"
  "thought leader," "passionate," "transformative" (as a modifier).
- Hollow superlatives: "one of the most important" without naming
  the metric, "deeply influential" without naming the influence.
- The word "ecosystem." Replace with "network," "circle,"
  "constellation," or just name the orgs.
- First person. The bio is third person throughout.
- Second person. The bio is third person throughout.
- Italics on book titles inside the bio body. Plain text only — the
  rendering surface decides styling.
- Bullet lists or sub-headers inside the `## Editorial bio` section.
- Invented stats. Use only numbers that appear in the dossier verbatim.
- Invented anecdotes or quotes.
- Honorific stacking ("the great," "the legendary"). Use earned titles
  only when the dossier uses them consistently (Rev., Dr., Bishop).

WORD COUNT
Editorial bio body: 150 to 220 words across 2 or 3 paragraphs. Two
paragraphs is the default; three is only used when the dossier
genuinely supports a distinct third move (e.g., a separate
denominational/academic surface for Liz Rios).

SANITY CHECK BEFORE OUTPUTTING
1. Does every paragraph contain at least one proper noun pulled from
   this specific leader's dossier?
2. Could the bio be sent for any other leader with only the names
   swapped? If yes, the bio has failed — add specificity.
3. Is the bio between 150 and 220 words?
4. Does the YAML parse and do all required fields have non-empty
   values?
5. Are all URLs absolute?
6. Is the role line ≤ 90 chars, the location_line ≤ 50, every theme
   ≤ 28, every credential ≤ 110, every featured_works entry ≤ 90?
7. Are there exactly three themes?
8. Are there 3–5 featured works and 2–3 secondary links?

If any check fails, revise the offending field in place before output.
```

---

## Voice exemplars (warmer-than-baseline calibration)

These three Committed Voices entries are the calibration baseline. Read them before drafting. The new entry should match their density and refuse their forbiddens, leaning slightly toward Liz Rios's register (warmer) rather than JR Woodward's (tightest).

### Liz Rios (warmer end of baseline — preferred register)

> Liz Rios has carried thirty-five years of ministry across pastoring, planting, teaching, and consulting — and into infrastructure. She founded Passion2Plant, the only national BIPOC-woman-led church planting network in the United States, and directs Púlpito Fellows, a three-year, bilingual preaching fellowship funded by the Lilly Endowment.
>
> Her work runs simultaneously across denominational, academic, and movement spaces: ordained Disciples of Christ; adjunct faculty at Fuller; board member at Sojourners; senior consultant with Freedom Road; consulting editor at Outreach Magazine. She holds a BA, MA, EdD, DMin, and a 2025 MA in Social Justice from Union.
>
> She writes from a mujerista frame — distinct in tone and theological surface area from anyone else inside Movemental's circle — and brings a live cohort operator's discipline to what a leader-platform actually has to carry.

### JR Woodward (tightest end of baseline)

> JR Woodward has spent three decades planting churches that hold tight community, life-forming discipleship, locally rooted presence, and boundary-crossing mission together. He leads the V3 Church Planting Movement nationally and trains church planters across North America.
>
> His written corpus runs from Creating a Missional Culture (IVP, 2012) through The Church as Movement (IVP, 2016, with Dan White Jr.) to The Scandal of Leadership (100 Movements Publishing, 2023) — the trade book based on his Manchester Ph.D. on the powers of domination in the church.
>
> He co-founded Missio Alliance and the Praxis Gathering, teaches as adjunct faculty at Fuller, Central, and Missio Seminary, and serves on the boards of Reliant Mission, Movement Leaders Collective, and the Fuller Global Mission Advisory Council.

### Rowland Smith (middle of baseline)

> Rowland Smith carries the National Director role at Forge America while founding and directing The Pando Collective, a Front-Range micro-church network, and pastoring missional culture at The Church at Pulpit Rock in Colorado Springs.
>
> He has authored Life Out Loud: Joining Jesus Outside the Walls of the Church (100 Movements Publishing, 2019) and curated and edited Red Skies: 10 Essential Conversations Exploring Our Future as the Church (100 Movements Publishing, 2022) — a multi-author conversation with Alan Hirsch, Michael Frost, Debra Hirsch, Brian Sanders, Mark DeYmaz, Rich Robinson, and others.
>
> He teaches as adjunct faculty at Fuller, Denver Seminary, and Grand Canyon University, holding an MA in Global Leadership and a DMiss from Fuller. His doctoral dissertation, Missional Emergence, has its own published authority record.

---

## Notes for the implementer

- The skill is a translation skill, not a research skill. It refuses to draft from a thin dossier.
- The output file is the canonical artifact for the Committed Voices surface. The TypeScript array in `src/lib/committed-voices.ts` will eventually be replaced by a loader that globs these files; until then, the operator copies the YAML values into the TS array by hand.
- Reserve fields (`signature_frameworks`, `lineage`, `sources`, `research_completed_at`) exist for the future Reflected Understanding and `/voices/[slug]` surfaces. The Committed Voices card ignores them.
- The skill never writes to Supabase. The schema-to-DB migration is a separate decision (see the standardization memo).
- The skill never edits the rendered TypeScript. It only writes one Markdown file per leader.
