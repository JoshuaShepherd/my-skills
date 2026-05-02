---
name: author-content
description: Write course content for a specific element (M.N.X) of a transformational course — readings, video scripts, reflection questions, exercises, discussion prompts, and more. Use when authoring or generating course content for a specific week and element code.
---

Author course content: $ARGUMENTS

$ARGUMENTS should include: course slug, week number, and element code (e.g., `{{course-slug}} 3 M3.5` for Week 3 reflection questions). If incomplete, ask the user.

## Before Starting

1. Read `{{DOCS_DIR}}/TRANSFORMATIONAL_COURSE_PLAYBOOK.md` for element specs (word counts, structure, checklist per M.N.X)
2. Read `{{DOCS_DIR}}/TRANSFORMATIONAL_COURSE_CHARTER.md` for the Four Necessities
3. Read `{{DOCS_DIR}}/courses/WEEK_0_AND_1_BOILERPLATE_WITH_EXAMPLE.md` for the living example (Metanoia course) — use as voice and tone reference
4. Read the course's existing content to understand context:
   - Check database via API or existing markdown in `content-library/courses/[slug]/`
   - Read the week's other sections for coherence
5. If corpus material exists, read relevant source chapters:
   - Check `{{PROJECT_ROOT}}/{{DOCS_DIR}}/corpus/` for book chapters
   - Look for the course's source book material

## Element Specifications

### M.N.1 — Lordship Opening (150-250 words)
- Short devotional/teaching paragraph grounded in the week's theme
- 1-2 reflective questions that create productive tension (dissonance)
- Brief prayer or moment of stillness
- Tone: contemplative, invitational, Christocentric
- Must include: reference to Jesus's lordship or the gospel

### M.N.2 — Main Reading (2,500-3,500 words)
- Core teaching content for the week
- Grounded in Scripture and Alan's corpus
- Structure: opening hook → framework presentation → scriptural grounding → implications → application preview
- Include 2-3 subheadings (H3)
- Include 1-2 blockquotes from Alan's books or Scripture
- Must advance the course's overarching narrative

### M.N.3 — Video Script (750-1,500 words / 5-10 min)
- Opening hook (30 sec), main teaching (3-5 min), bridge to reading (1 min), closing question (30 sec)
- Conversational tone, direct address ("you")
- Reference 1-2 key concepts from the reading
- End with a provocative or invitational question

### M.N.4 — Anchor Scripture (150-250 words)
- Scripture passage (full text, not just reference)
- Brief intro framing the passage in context of the week's theme
- Suggested reading practice (Meditative Reading, Lectio Divina, etc.)
- No commentary — let Scripture speak

### M.N.5 — Reflection Questions (6-8 questions)
- Each question: open-ended, not yes/no
- Mix of: personal application, theological reflection, contextual discernment
- Progressive depth: start accessible, end with challenge
- Include optional guidance/prompts for deeper thinking
- Format: numbered list with question text

### M.N.6 — Practical Exercises (2-3 exercises)
- Each exercise needs: title, purpose, estimated time (30-120 min), step-by-step instructions, deliverables
- Must be doable in the learner's own context
- At least one exercise that involves another person
- Concrete and actionable — not theoretical

### M.N.7 — Field Experiments (1-2 experiments)
- Objective: what the learner will observe/test
- Steps: concrete, sequential, time-boxed
- Evidence to gather: what to look for, document, measure
- Reflection: what to journal after the experiment
- Must happen outside the study environment (in real life)

### M.N.8 — Discussion Prompts (2-3 prompts)
- Each prompt: title + question text
- Prompt types: conceptual, application, integration
- Designed for small group or online forum
- At least one prompt that invites storytelling

### M.N.9 — Cohort Session Prompts (E/E/E/J structure)
- **Explore** (2-3 prompts): Open discovery, "What did you notice..."
- **Evaluate** (2-3 prompts): Critical thinking, "How does this compare..."
- **Employ** (2-3 prompts): Application, "What will you do with..."
- **Journal** (1-2 prompts): Personal integration, "Write about..."
- Total session time: ~90 minutes

### M.N.10 — Integration Copy (50-100 words per connection)
- 2-3 connections between this week's content and other weeks/themes
- Show how concepts interrelate across the course
- Forward and backward references

### M.N.11 — Lordship Closing (150-200 words)
- Recap the week's key insight (1-2 sentences)
- Commitment invitation: "This week, I will..."
- Blessing or sending: brief, warm, Christocentric
- Transition to the next week's theme

### M.N.12 — Looking Ahead (100-200 words)
- Preview next week's theme (1-2 sentences)
- Connection to this week's learning
- Invitational tone: anticipation, not obligation

### M.N.13 — Resource Blurb (150-250 words)
- 1-2 recommended resources (books, articles, talks)
- Brief description of each and why it matters for this week
- Not required reading — supplemental

### M.N.14 — Formation Companion Context (2-3 sentences + 3-5 starter questions)
- Brief summary of the week's theme for the AI agent
- 3-5 starter questions the learner might explore with the Formation Companion
- Questions should deepen, not repeat, the reflection questions

## Voice: {{AUTHOR_NAME}}

Write as {{AUTHOR_NAME}}. Five voice markers (all must be present):

1. **Christocentric anchoring** — Jesus is Lord. Every framework points back to Jesus. Allegiance, obedience, sentness.
2. **Pastoral warmth** — "We" language. Invitational, not prescriptive. "I wonder if..." not "You must..."
3. **Narrative imagery** — Organic metaphors: movement, journey, seeds, fire, rivers. Early church stories. Chinese underground church.
4. **Theological depth** — Grounded in Scripture and tradition. Not surface-level. Engages with real theological concepts.
5. **Prophetic intensity** — Reframing questions. Productive dissonance. Calls to risk and obedience. "What if the church has been..."

### Voice Anti-Patterns (NEVER use)
- Corporate consultant tone ("leverage," "optimize," "best practices," "scalable")
- Detached academic voice ("It could be argued that..." "Research suggests...")
- Antithesis patterns ("Not X, but Y") — use additive, forward-building language
- Bullet-point lists as primary content (use prose with embedded lists)
- Generic motivational language ("You've got this!" "Believe in yourself!")

## Output

Write the content directly in markdown format. Include:
1. The element code and title as an H2 heading
2. The content following the specification above
3. A brief note on word count and any Charter requirements met

If writing to a file, save to `content-library/courses/[slug]/week-[NN]-[element].md` or update the existing week file.

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- Always check existing content first — don't overwrite without asking
- Stay within word count targets (flag if significantly over/under)
- Every piece of content must serve at least one of the Four Necessities
- Content must be coherent with the course's other weeks — read context first
- Never use placeholder text — generate real, usable content
- Ground teaching in Alan's actual books and frameworks (not made up)
