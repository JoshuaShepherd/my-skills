---
name: course-author
description: Generate course content for a specific section of the transformation loop, following the actual Forgotten Ways course structure, Charter requirements, and Alan Hirsch's voice. Use when writing individual course sections.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Author course content: $ARGUMENTS

$ARGUMENTS should include: course slug, week number, and section type (e.g., `forgotten-ways 3 dissonance` or `forgotten-ways 4 teaching`). If incomplete, ask the user.

## Before Starting

1. Read `_docs/COURSE_STRATEGY.md` — this is the authoritative reference for structure, section order, voice, and word counts
2. Read `_docs/TRANSFORMATIONAL_COURSE_CHARTER.md` for the Four Necessities
3. Check the course's existing content for context:
   - `content-library/courses/[slug]/` for existing markdown
   - The Forgotten Ways course.json at `/Users/joshuashepherd/Desktop/Dev/repos/forgotten-ways-course/editor/data/course.json` — use this as the canonical reference for tone, depth, and structure
4. If corpus material exists, read relevant source chapters:
   - Check `/Users/joshuashepherd/Desktop/Dev/repos/forgotten-ways-course/_docs/corpus/` or equivalent for book chapters

## The Transformation Loop

Every core week (2–7) follows this exact sequence. Write for the section the user requests.

| Section | DB type | Sidebar label | Word count |
|---------|---------|---------------|-----------|
| Opening video script | `video` | "Opening video" | 600–900 words (~5 min) |
| Dissonance prompt | `chat_dissonance` | "Dissonance" | 200–350 words |
| Main teaching | `reading` | *(none)* | 2,000–3,500 words |
| Case study / Witness | `case_study` | *(none)* | 300–600 words |
| Action step prompt | `chat_action` | "Action step" | 150–250 words |
| Reflection prompt | `chat_reflection` | "Reflection" | 150–250 words |
| Cohort meeting | `discussion` | "Cohort meeting" | 200–400 words |
| Exit ticket | `reflection` | "Exit ticket" | 150–250 words |

Week 1 uses: `video`, `reading` (course overview), `chat_dissonance` (context discovery), `looking_ahead`.
Week 8 is expanded — see `_docs/COURSE_STRATEGY.md` section 5 for the full Week 8 layout.

---

## Section Specifications

### Opening Video Script (`video`)

- Alan delivers the week's core concept to camera — 5 min max (~700 words to speak)
- Structure: hook that names the week's tension → the core concept in plain language → one historical or scriptural grounding → what this means for the learner → closing question or invitation
- Conversational, direct, first-person "we." Not a lecture. Not a summary of the reading.
- Ends with a question that creates anticipation for the dissonance prompt or reading
- Tone: warm, prophetic, invitational
- Do NOT repeat the reading verbatim — the video frames; the reading unpacks

### Dissonance Prompt (`chat_dissonance`)

- This is prompt content for the AI companion, not the learner's direct interface
- Two parts: (1) the tension statement — 2–3 sentences framing the assumption or contradiction the week confronts; (2) the question — 1–2 sentences the learner actually responds to
- The tension should feel like Alan asking a hard question across a table, not a quiz or welcome message
- Do NOT comfort or resolve the tension — hold it open
- Example structure from the course: state the tension ("We confess that Jesus is Lord—and yet..."), then the question ("Which sphere of your life do you most easily keep under Jesus, and which do you notice yourself holding back?")

### Main Teaching / Concept (`reading`)

- Core teaching content for the week. The learner will read this after watching the video and engaging the dissonance.
- Structure: opening hook → framework presentation → scriptural grounding → implications → application preview
- 2–3 subheadings (H3)
- 1–2 blockquotes from Alan's books or Scripture — properly attributed
- Must include: the week's core concept named explicitly; at least one historical or scriptural example (early church, Chinese church, or Scripture); application to the learner's context
- Must advance the course's overarching narrative (not a standalone essay — it connects to what came before and what comes next)
- End with a "what's next" sentence pointing toward the action step
- Source citations format: `**Sources:** The Forgotten Ways — ch[N] "[Chapter title]" (section: "[Section]")`

### Case Study / Witness (`case_study`)

- A specific, concrete story that shows the week's concept in action
- NOT a summary of the teaching — a narrative. Show, don't tell.
- Often: the early church, the Chinese underground church, or a specific historical movement
- Or: Alan's own community story (South Melbourne Restoration Community; his own journey)
- Structure: situation → decision or dynamic → outcome → brief implication for the learner
- No subheadings — flowing prose

### Action Step Prompt (`chat_action`)

- Prompt content for the AI companion conversation
- Purpose: help the learner name ONE concrete, doable, time-boxed step for this week
- Must include: the week's theme in one sentence, the invitation to name a step, a time box (7 days or less), and who they'll tell / who will follow up
- Not a to-do list. Not a reflection. One step. Named. Shared with someone.
- Example: "The companion has this week's theme and will help you land on one doable rhythm—one coffee with a neighbour, prayer walks, or another way you 'go out' or 'go deep' in the next 7 days. You'll name a time box and who will follow up with you."

### Reflection Prompt (`chat_reflection`)

- Prompt content for the AI companion conversation *after* the learner has acted
- Purpose: help the learner look back — what did they do? what got in the way? what do they want to carry forward?
- Three movements: (1) what happened; (2) what they noticed; (3) what they want to carry forward
- Invitational, not interrogative. "The companion will guide you through a short reflection and re-commitment."

### Cohort Meeting (`discussion`)

- A structured group discussion prompt — designed for async post + response or sync call
- Three parts: (1) **Share** prompt — the key question for the week, personalized to the cohort's shared experience; (2) response instruction — "Post your reflection; then reply to at least one other person"; (3) **For facilitators** — 2–3 sentences on what to hold in view, what to avoid, and how to link to the next week
- At least one "if you're not sure where to start" option
- The share prompt should draw on the week's core tension — not just "summarize what you learned"

### Exit Ticket (`reflection`)

- Three options for the learner to choose from:
  1. **Journal one sentence** — a specific prompt tied to the week's theme
  2. **Name one commitment** — what they will do or keep doing before the next week
  3. **Review** — a key phrase or sentence from the week to re-read and carry with them
- Brief preview of next week: "What happens next. Week [N+1]: [Theme] — [one-sentence teaser]."
- Optional: a short "if this is you" section for learners who feel behind or uncertain

---

## Voice: Alan Hirsch

Write as Alan Hirsch. Five markers — all must be present:

1. **Christocentric anchoring** — Jesus is Lord. Every framework points back to Jesus. Allegiance, obedience, sentness.
2. **Pastoral warmth** — "We" language. Invitational, not prescriptive. "I wonder if..." not "You must..."
3. **Narrative imagery** — Organic metaphors: movement, journey, seeds, fire, rivers. Early church stories. Chinese underground church.
4. **Theological depth** — Grounded in Scripture and tradition. Not surface-level. Engages with real theological concepts.
5. **Prophetic intensity** — Reframing questions. Productive dissonance. Calls to risk and obedience. "What if the church has been..."

### Anti-Patterns (NEVER use)
- Corporate consultant tone ("leverage," "optimize," "best practices," "scalable")
- Detached academic voice ("It could be argued that..." "Research suggests...")
- Antithesis patterns ("Not X, but Y") — use additive, forward-building language
- Bullet-point lists as primary content (use prose with embedded lists)
- Generic motivational language ("You've got this!" "Believe in yourself!")

---

## Output

Write content directly in markdown format:
1. The section type and week as an H2 heading (e.g., `## Week 4 — Main Teaching`)
2. The content following the specification above
3. A brief note on word count

Save to `content-library/courses/[slug]/week-[NN]-[section-type].md` or update the existing week file.

## Rules

- 8 weeks, numbered 1–8. No Week 0.
- Always check existing content first — don't overwrite without asking
- Stay within word count targets (flag if significantly over/under)
- Every section must serve at least one of the Four Necessities (dissonance, action, reflection, community)
- Content must be coherent with the course's other weeks — read context first
- Never use placeholder text — generate real, usable content
- Ground all teaching in Alan's actual books and frameworks (not made up)
- The transformation loop order is fixed: video → dissonance → teaching → case study → action → reflection → cohort → exit. Do not reorder.
