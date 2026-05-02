---
name: video-researcher
description: Research real-world statistics, insights, and compelling data about online courses, completion rates, learning effectiveness, and transformative education — then organize findings into suggested video components, script lines, and data visualizations for course explainer videos. Use before scripting or updating video content.
user-invocable: true
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Grep, Glob
---

Research for transformative course videos: $ARGUMENTS

$ARGUMENTS may include:
- A research focus (e.g., `completion rates`, `cohort vs self-paced`, `corporate training ROI`, `transfer gap`)
- A specific video scene to update (e.g., `S05`, `S06`, `Act 2`)
- A narrative angle (e.g., `why online courses fail`, `what makes cohorts work`, `the formation gap`)
- Empty — run the full research sweep across all categories

---

## Research Categories

Run web searches across these domains. Each category maps to scenes in the course explainer video library (`_docs/videos/courses/_shared/scripts/course-explainer-scenes.md`).

### Category 1: Market Size & Scale (→ S05)
- Global e-learning market size (2025-2026 current, 2030+ projections)
- Corporate training spend globally
- Number of online learners worldwide
- MOOC enrollment numbers (Coursera, edX, Udemy totals)
- Growth rate and trajectory

**Search queries:**
- `global e-learning market size 2025 2026 billion`
- `corporate training spending worldwide 2025 2026`
- `online learning market projections 2030`
- `MOOC enrollment statistics 2025 2026`

### Category 2: Completion & Dropout Rates (→ S06)
- MOOC completion rates (latest Harvard/MIT data or successors)
- Self-paced course completion rates
- Corporate e-learning completion rates
- Dropout timing (when do people quit?)
- Trend over time (is it getting worse?)

**Search queries:**
- `MOOC completion rate 2024 2025 statistics`
- `online course dropout rate statistics`
- `online course completion rate trend getting worse`
- `when do online course learners drop out`

### Category 3: The Transfer Gap (→ S07)
- Percentage of learners who apply what they learned
- Corporate training transfer rates
- "Knowing-doing gap" research
- Kirkpatrick model Level 3/4 data
- Cost of non-transfer (wasted training spend)

**Search queries:**
- `training transfer gap statistics percentage apply learning`
- `corporate training effectiveness percentage employees apply skills`
- `knowing doing gap online learning research`
- `Kirkpatrick level 3 transfer rate statistics`

### Category 4: Cohort & Community Effect (→ S08)
- Cohort-based course completion rates vs self-paced
- Community learning outcomes research
- Social learning effectiveness data
- Accountability and peer effects on completion
- Specific cohort programs with published data (altMBA, On Deck, Reforge, etc.)

**Search queries:**
- `cohort based course completion rate vs self paced`
- `community based learning outcomes research 2024 2025`
- `social learning completion rates statistics`
- `altMBA completion rate cohort based learning`

### Category 5: Transformative Learning & Formation (→ S09-S12)
- Mezirow's transformative learning theory — empirical evidence
- Disorienting dilemma research
- Experiential learning outcomes vs passive
- Reflection in learning — impact data
- Community/communitas in education research

**Search queries:**
- `transformative learning theory empirical evidence outcomes`
- `experiential learning vs passive lecture outcomes statistics`
- `reflection in learning impact effectiveness research`
- `disorienting dilemma transformative education research`

### Category 6: The Counter-Narrative (→ compelling contrasts)
- What top-performing courses do differently
- Engagement vs completion (the real metric?)
- Faith-based / formation-oriented programs with data
- Microlearning, spaced repetition, active recall — what actually works

**Search queries:**
- `what makes online courses effective research 2025`
- `active learning vs passive learning completion outcomes`
- `spaced repetition learning effectiveness statistics`
- `faith based online education outcomes`

---

## Before Starting

1. Read `_docs/videos/courses/_shared/scripts/course-explainer-scenes.md` — understand the existing scene library and its current statistics
2. Read `_docs/videos/style-guide/brand-tokens.md` — understand the visual vocabulary for suggesting components
3. Note which statistics are already cited and their dates — flag anything outdated

---

## Research Protocol

For each category:

1. **Search** — Run 2-4 web searches using the suggested queries (adapt based on what you find)
2. **Verify** — Cross-reference claims across multiple sources. Prefer:
   - Academic studies (Harvard, MIT, Stanford)
   - Industry reports (HolonIQ, Statista, Josh Bersin, Class Central)
   - Government data (NCES, UNESCO)
   - Named programs with published metrics
3. **Extract** — Pull the specific number, the source, the year, and the context
4. **Flag confidence** — Mark each finding as:
   - **VERIFIED** — multiple credible sources agree
   - **REPORTED** — single credible source, not independently confirmed
   - **ESTIMATED** — derived or extrapolated from partial data
   - **OUTDATED** — data is 3+ years old and may have shifted

---

## Output Format

### Part 1: Research Brief

Organize findings by category. For each finding:

```markdown
### [Category Name] (→ Scene [ID])

#### [Finding headline]
- **Stat**: [The number or claim]
- **Source**: [Organization, report name, year]
- **URL**: [Link if available]
- **Confidence**: VERIFIED | REPORTED | ESTIMATED | OUTDATED
- **Context**: [1-2 sentences on what this means and any caveats]
```

### Part 2: Scene Update Recommendations

For each existing scene (S05-S08 especially), recommend:
- Which stats to keep, update, or replace
- New stats that strengthen the narrative
- Suggested revised narration lines (keeping voice/tone consistent)
- Any new visual concepts the data suggests

### Part 3: New Component Suggestions

Propose 3-5 new video components or scene variants that the research supports:

```markdown
#### [Component Name]
- **Data point**: [The compelling stat]
- **Narrative hook**: [1-2 sentence script suggestion]
- **Visual concept**: [How this could be animated]
- **Best used in**: [Full explainer / social cut / ad / standalone]
- **Scene pairing**: [Which existing scene it strengthens or extends]
```

### Part 4: Source Index

A clean table of all sources cited, with URLs, for fact-checking and attribution.

---

## File Output

Save the complete research brief to:
`_docs/videos/courses/_shared/lab/[topic]-research-[YYYY-MM-DD].md`

Create the `lab/` directory if it doesn't exist.

If updating specific scene statistics, also note the recommended changes in:
`_docs/videos/courses/_shared/lab/scene-update-recommendations.md`

---

## Rules

- Never fabricate statistics. If you can't find a number, say so.
- Always cite sources with year. A stat without a date is useless.
- Prefer recent data (2023-2026). Flag anything older than 3 years.
- Cross-reference market size numbers — they vary wildly by source and definition.
- The narrative purpose matters: we're telling the story of why information alone doesn't transform, and why community-based formation does. Research should serve that arc.
- Don't just dump numbers — contextualize. "5% completion" means nothing without "out of every 100 people who sign up..."
- Keep the Movemental voice in mind when suggesting narration lines — measured, cinematic, warm. Not hype. Not startup pitch.
