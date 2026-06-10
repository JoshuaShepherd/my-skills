---
name: course-scaffold
description: Scaffold a new 8-week course with all canonical section types, database rows, and optional markdown file structure. Use when creating a new course from scratch.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Scaffold a new course: $ARGUMENTS

## Inputs

Parse the arguments for:
- **slug** (required) — e.g., `mdna-primer`
- **title** (required) — e.g., "mDNA Primer: Recovering the Genetics of Ecclesia"
- **portal** (optional) — one of: reframation, metanoia, mdna, mx, forgotten-ways

If any required input is missing, ask the user.

## Before Starting

1. Read `_docs/COURSE_STRATEGY.md` — the authoritative reference for the 8-week structure and canonical section order
2. Read `src/lib/database/schema.ts` — find `courses`, `courseWeeks`, `courseLessons` table definitions
3. Read `src/lib/schemas/course-learn.ts` — understand SECTION_TYPES
4. Read `src/lib/config/lesson-types.ts` — canonical type list
5. Read `scripts/ingest-forgotten-ways-course.ts` for insert patterns

## Course Structure (8 Weeks)

Every course follows this exact structure. **8 weeks total, numbered 1–8. No Week 0.**

### Week 1 — Introduction & Orientation

| # | section_type | Sidebar label | Purpose |
|---|-------------|---------------|---------|
| 1 | `video` | "Opening video" | Course promise, who it's for, what to expect |
| 2 | `reading` | *(none)* | Course overview: 8-week structure, transformation loop, cohort norms |
| 3 | `chat_dissonance` | "Context discovery" | Baseline context capture for AI personalisation |
| 4 | `looking_ahead` | *(none)* | What happens next; Week 2 preview |

### Weeks 2–7 — Core Transformation Modules (The Loop)

Each week follows this order — **do not deviate**:

| # | section_type | Sidebar label | Purpose |
|---|-------------|---------------|---------|
| 1 | `video` | "Opening video" | Alan delivers the week's concept (~5 min) |
| 2 | `chat_dissonance` | "Dissonance" | AI conversation that surfaces tension before the reading |
| 3 | `reading` | *(none)* | Main teaching: 2,000–3,500 words |
| 4 | `case_study` | *(none)* | Witness: a concrete story that makes the concept real |
| 5 | `chat_action` | "Action step" | AI conversation: name one concrete step |
| 6 | `chat_reflection` | "Reflection" | AI conversation: look back after acting |
| 7 | `discussion` | "Cohort meeting" | Group discussion prompt (share + respond) |
| 8 | `reflection` | "Exit ticket" | Three close options + next week preview |

### Week 8 — Synthesis & Sending

| # | section_type | Sidebar label | Purpose |
|---|-------------|---------------|---------|
| 1 | `chat_dissonance` | "Dissonance" | The tension between "learned it" and "living it" |
| 2 | `reading` | *(none)* | The ecosystem alive — all elements as one system |
| 3 | `case_study` | *(none)* | Witness: synthesis and sending |
| 4 | `chat_action` | "Action step" | Name the 30/60/90 day plan |
| 5 | `chat_reflection` | "Reflection" | Evidence of change |
| 6 | `discussion` | "Cohort meeting" | Cohort reflects on the ecosystem |
| 7 | `integration` | *(none)* | Week 8 commitment framework |
| 8 | `video` | "Sending video" | Alan sends the learner — a charge, not a graduation |
| 9 | `reading` | *(none)* | Synthesis and sending (final teaching) |
| 10 | `chat_reflection` | "Reflection" | Final reflection |
| 11 | `field_experiment` | *(none)* | The written 30/60/90 day plan |
| 12 | `discussion` | "Commissioning" | Commissioning session |
| 13 | `integration` | *(none)* | Final commitment |
| 14 | `lordship_opening` | *(none)* | Sending liturgy (7-movement ritual) |
| 15 | `reflection` | "Exit ticket" | Course close |

---

## Process

### Step 1: Create the ingestion script

Create `scripts/scaffold-course-[slug].ts` that:

1. Connects to the database using the project's postgres/Drizzle setup
2. Creates the `courses` row with:
   - title, slug, description (placeholder), status: "draft"
   - duration_weeks: 8
   - course_type: "formation"
   - portal_themes: `["<portal>"]` if portal provided
   - organization_id from env TENANT_ORG_ID
3. Creates 8 `courseWeeks` rows (week_number 1–8) with:
   - Week 1: "Introduction & Orientation"
   - Weeks 2–7: "Week N — [TBD]" (theme to be authored)
   - Week 8: "Week 8 — Synthesis & Sending"
   - order_index matching week_number
4. Creates `courseLessons` rows for each week following the canonical section order above
   - Each lesson: title (descriptive placeholder), slug (auto-generated from title + week), section_type, section_order (global counter), week_id, course_id, status: "draft", content: "" (empty — to be authored via `/course-author`)
   - Use the sidebar labels from the tables above where they exist; null otherwise

### Step 2: Optionally scaffold markdown files

Ask the user if they also want a markdown content directory. If yes, create:

```
content-library/courses/[slug]/
  course-manifest.json
  week-01-introduction.md
  week-02-[theme].md
  ...
  week-08-synthesis.md
```

Each markdown file should have section headers matching the transformation loop:

```markdown
## Week 2 — Opening Video
[Content TBD — ~700 words, ~5 min]

## Week 2 — Dissonance
[Content TBD — 200-350 words]

## Week 2 — Main Teaching
[Content TBD — 2,000-3,500 words]

## Week 2 — Case Study
[Content TBD — 300-600 words]

## Week 2 — Action Step
[Content TBD — 150-250 words]

## Week 2 — Reflection
[Content TBD — 150-250 words]

## Week 2 — Cohort Meeting
[Content TBD — 200-400 words]

## Week 2 — Exit Ticket
[Content TBD — 150-250 words]
```

The manifest should list all lessons with ids, types, and week assignments.

### Step 3: Report

Output a summary:
- Course created: title (slug)
- Weeks: 8
- Total sections: N
- Sections per week breakdown
- Next steps: "Use `/course-author` to generate content for each section"

---

## Rules

- **8 weeks exactly.** Week 1 = introduction, Week 8 = synthesis and sending. No Week 0.
- **Transformation loop order is fixed** for Weeks 2–7: video → chat_dissonance → reading → case_study → chat_action → chat_reflection → discussion → reflection
- Use env TENANT_ORG_ID for organization_id scoping
- Set all content to draft status
- Follow the project's postgres insert patterns from `scripts/ingest-forgotten-ways-course.ts`
- Never hardcode UUIDs — let the database generate them
- Validate the slug doesn't already exist before inserting
- Reference `_docs/COURSE_STRATEGY.md` for any structure questions — it is the authoritative source
