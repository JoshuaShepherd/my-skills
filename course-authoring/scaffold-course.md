
Scaffold a new course: $ARGUMENTS

## Inputs

Parse the arguments for:
- **slug** (required) — e.g., `mdna-primer`
- **title** (required) — e.g., "mDNA Primer: Recovering the Genetics of Ecclesia"
- **portal** (optional) — one of: reframation, metanoia, mdna, mx, {{course-slug}}

If any required input is missing, ask the user.

## Before Starting

1. Read `{{SCHEMA_PATH}}` — find the `courses`, `courseWeeks`, and `courseLessons` table definitions
2. Read `{{SCHEMAS_DIR}}/course-learn.ts` — understand SECTION_TYPES
3. Read `src/lib/config/lesson-types.ts` — canonical type list
4. Read `{{DOCS_DIR}}/TRANSFORMATIONAL_COURSE_PLAYBOOK.md` — the 8-week structure and M.N.X element layout
5. Read 1-2 existing ingestion scripts in `{{SCRIPTS_DIR}}/` for patterns (e.g., `ingest-{{course-slug}}-course.ts`)

## Course Structure (8 Weeks)

Every course follows this exact structure. **8 weeks total, numbered 1-8. No Week 0.**

| Week | Role | Core Sections |
|------|------|--------------|
| **Week 1** | Introduction & Orientation | welcome, video, reading, assessment, reflection, practical_exercise, looking_ahead |
| **Weeks 2-7** | Core Modules | lordship_opening, video, reading, scripture, reflection, practical_exercise, field_experiment, discussion, cohort_session, integration, lordship_closing, looking_ahead, resource_blurb, action |
| **Week 8** | Synthesis & Commissioning | reading, reflection, integration, assessment, commissioning, journey_continues, post_course |

## Canonical Section Order per Core Week (2-7)

Each core week gets these sections in this order (M.N.X naming):

| Order | M.N.X | section_type | Sidebar Label |
|-------|-------|-------------|---------------|
| 1 | M.N.1 | lordship_opening | Opening |
| 2 | M.N.2 | reading | Reading |
| 3 | M.N.3 | video | Video |
| 4 | M.N.4 | scripture | Scripture |
| 5 | M.N.5 | reflection | Reflection |
| 6 | M.N.6 | practical_exercise | Exercise |
| 7 | M.N.7 | field_experiment | Field Experiment |
| 8 | M.N.8 | discussion | Discussion |
| 9 | M.N.9 | cohort_session | Cohort Session |
| 10 | M.N.10 | integration | Integration |
| 11 | M.N.11 | lordship_closing | Closing |
| 12 | M.N.12 | looking_ahead | Looking Ahead |
| 13 | M.N.13 | resource_blurb | Resource |
| 14 | M.N.14 | action | Formation Companion |

## Process

### Step 1: Create the ingestion script

Create `{{SCRIPTS_DIR}}/scaffold-course-[slug].ts` that:

1. Connects to the database using the project's Drizzle setup
2. Creates the `courses` row with:
   - title, slug, description (placeholder), status: "draft"
   - duration_weeks: 8
   - course_type: "formation"
   - portal_themes: `["<portal>"]` if portal provided
   - organization_id from `getOrgId()`
3. Creates 8 `courseWeeks` rows (week_number 1-8) with:
   - Titles: "Introduction & Orientation" (1), "Module N: [TBD]" (2-7), "Synthesis & Commissioning" (8)
   - order_index matching week_number
4. Creates `courseLessons` rows for each week following the canonical section order above
   - Each lesson: title (from sidebar label + week context), slug (auto-generated), section_type, section_order, week_id, course_id, status: "draft", content: "" (empty — to be authored)
   - For Week 1: use the introduction sections
   - For Weeks 2-7: use the full canonical order (14 sections each)
   - For Week 8: use the closing sections

### Step 2: Optionally scaffold markdown files

Ask the user if they also want a markdown content directory. If yes, create:

```
content-library/courses/[slug]/
  course-manifest.json
  week-01-introduction.md
  week-02-module-02.md
  ...
  week-08-synthesis.md
```

Each markdown file should have section headers matching M.N.X naming:
```markdown
## M2.1 — Lordship Opening
[Content TBD]

## M2.2 — Main Reading
[Content TBD — target: 2,500-3,500 words]
```

The manifest should list all lessons with ids, types, and week assignments.

### Step 3: Report

Output a summary:
- Course created: title (slug)
- Weeks: 8
- Total sections: N
- Sections per week breakdown
- Next steps: "Use `/course-author` to generate content for each M.N.X element"

## Rules

- **8 weeks exactly.** Week 1 = introduction, Week 8 = closing. No Week 0.
- Use `getOrgId()` for organization_id scoping
- Set all content to draft status
- Follow the project's Drizzle insert patterns from existing scripts
- Never hardcode UUIDs — let the database generate them
- Validate the slug doesn't already exist before inserting
