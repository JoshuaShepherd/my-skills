---
name: pathway-case-study
description: Research and write case studies for Alan Hirsch pathway pages. Produces 2–4 case studies per pathway — biblical, historical, and contemporary — with card-level summaries for the pathway page and full narrative pages for dedicated URLs. Draws from Alan's books, documented movements, and his research. Each case study follows the pathway's own arc (U-shape for Metanoia, reframes for Reframation, etc.).
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Write case studies for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally a specific case study to develop (e.g., `metanoia jerusalem-council` or `mdna chinese-church`).

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — check if case studies already exist
3. Read existing case studies in research: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/case-studies/`
4. Read the story index: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/story-index/`

---

## Step 2 — Corpus Research

### Book-to-Pathway Map

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

| Pathway | Where Alan Tells Case Stories |
|---------|------------------------------|
| **Reframation** | `reframation` (Chinese church, Celtic missionaries, Kuyper, Newbigin), `the-forgotten-ways` ch01–ch03 |
| **Metanoia** | `metanoia` (Jerusalem Council, Barmen Declaration, Belhar Confession), `the-forgotten-ways` ch01 |
| **mDNA** | `the-forgotten-ways` ch04–ch09 (early church, Chinese underground, SMRC, Methodist movement), `on-the-verge` ch04 |
| **Movement Intelligence** | `on-the-verge` (multiple movement examples), `fast-forward-to-mission`, `the-forgotten-ways` ch06, ch09 |
| **Discipleship** | `untamed` (SMRC stories, George & John, The Main House), `disciplism`, `right-here-right-now` |

### Research Process

1. **Search Alan's books for movement examples:**
   ```
   Grep: pattern="(church|movement|community|congregation)" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/" output_mode="content" -C=5
   ```

2. **Identify Alan's signature case studies** — he returns to these repeatedly:
   - **Biblical:** Jerusalem Council (Acts 15), Early church (AD 100–310), Antioch church
   - **Historical:** Chinese underground church (1949–present), Celtic missionaries (5th–7th c.), Methodist movement (Wesley), Moravian missionaries, CMA, Pentecostal revivals
   - **Contemporary:** SMRC (South Melbourne Restoration Community, 1983–1998), Forge Network, specific church plants or movements from his consulting/speaking
   - **Confessional:** Barmen Declaration (1934), Belhar Confession (1986)

3. **Read the relevant passages in full** — Alan embeds case studies within theological arguments, not as standalone narratives. Extract the full narrative arc.

4. **Note specific data:** dates, numbers, names, locations. Alan uses specificity (e.g., "2 million to 120 million in 60 years"). Maintain this precision.

---

## Step 3 — Write Case Studies

### Required Mix (per pathway)
- **1 Biblical** — from Acts or the prophets, showing the concept in Scripture
- **1 Historical** — a documented movement from church history
- **1 Contemporary** (if available) — a modern movement or community. If Alan doesn't provide one, note `[content coming]` with suggested candidates

### Structure: Card Content (for pathway page)

Each case study appears as a card on the pathway page. The card has:

- **Title:** Name of the movement/event
- **Context:** Time, place, situation — one sentence
- **Hook:** 2–3 sentences that create desire to read more. Narrative, not summary. End with a tension or insight.

### Structure: Full Page Content

Each card links to a dedicated page at `/pathways/[slug]/case-studies/[case-slug]`. The full page has:

1. **Lead paragraph** (100–150 words) — The problem or moment. Set the scene. What was at stake?

2. **Narrative body** (3–5 paragraphs, 600–1000 words total) — Tell the story through the lens of this pathway's model:
   - **Metanoia:** Downcurve → Turning Point → Upcurve (U-Shaped Journey)
   - **Reframation:** What frame was broken → What was seen differently → What changed
   - **mDNA:** Which elements of Apostolic Genius were present → How they operated → What resulted
   - **Movement Intelligence:** What movement dynamics were at work → How they multiplied → What patterns emerged
   - **Discipleship:** How discipleship was practiced → What formation looked like → How it spread

3. **Implications** (100–150 words) — What this case study reveals about the pathway's principles. Connect back to the framework. What can we learn?

### Voice for Case Studies

Case studies are narrative-heavy. Calibrate the markers:

| Marker | Calibration |
|--------|-------------|
| **Christocentric Anchoring** | Embedded in the narrative — show Jesus at work, not just mentioned |
| **Prophetic Intensity** | In the implications, not the narrative. Let the story do the challenging. |
| **Pastoral Warmth** | Present throughout — care for the people in the story |
| **Narrative Imagery** | Highest here — this IS narrative. Concrete, vivid, specific. |
| **Theological Depth** | Woven into the narrative, not appended. Show how theology was lived. |

### Anti-Patterns for Case Studies
- Never sanitize failure — Alan is honest about what went wrong (SMRC had three phases, including "Death to Chaos")
- Never use a case study as proof — it illustrates and illuminates, it doesn't prove
- Never genericize — keep names, dates, numbers, places specific
- Never moralize at the end — let the implications emerge from the story

---

## Step 4 — Output

```
---
pathway: [slug]
section: case-studies
study_count: [number]
books_cited: [list]
case_types: [biblical, historical, contemporary]
---

## Case Study 1: [Title] — [Biblical/Historical/Contemporary]

### Card (pathway page)
- **Title:** [Name]
- **Context:** [Time, place, situation]
- **Hook:** [2–3 sentences]

### Full Page

[Lead paragraph — 100–150 words]

[Narrative body — 3–5 paragraphs]

**Implications for [Pathway Name]:** [100–150 words]

---

## Case Study 2: [Title] — [Type]

[Same structure]

---

## Case Study 3: [content coming]

*Suggested: [Description of what's needed and candidate movements/examples]*
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/case-studies/`
