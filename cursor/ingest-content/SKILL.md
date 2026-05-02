---
name: ingest-content
description: Ingest course content from markdown files or a content directory into the database — parsing, validating, and upserting weeks, lessons, reflection questions, discussion prompts, and exercises. Use when loading or re-loading course content into the platform database.
---

Ingest course content: $ARGUMENTS

$ARGUMENTS should be a course slug or path to the content directory. If empty, ask the user.

## Before Starting

1. Read any existing ingestion scripts in `{{SCRIPTS_DIR}}/` to understand patterns (e.g., `{{SCRIPTS_DIR}}/ingest-{{course-slug}}-course.ts`)
2. Read `{{SCHEMA_PATH}}` for table definitions (courses, courseWeeks, courseLessons, reflectionQuestions, discussionPrompts, exercises)
3. Read `{{SCHEMAS_DIR}}/course-learn.ts` for SECTION_TYPES
4. Read `src/lib/config/lesson-types.ts` for type mapping

## Locate Content Source

Search for content in these locations (in order):

1. `content-library/courses/[slug]/` — project content library
2. `{{PROJECT_ROOT}}/docs/` — standalone course repo (for {{course-slug}})
3. A path provided directly by the user

Look for:
- `course-manifest.json` — lesson order, types, week structure
- `module-*.md` or `week-*.md` — lesson body content
- Any structured markdown with `## Lesson` or `## M.N.X` headings

## Content Parsing

### Manifest Format (expected)

```json
{
  "courseTitle": "The {{COURSE_NAME}}",
  "weeks": [
    {
      "id": 1,
      "title": "Introduction & Orientation",
      "outcomes": ["..."],
      "lessons": [
        { "id": "lesson-01", "title": "Course Overview", "type": "welcome", "sidebarLabel": "Welcome" }
      ]
    }
  ]
}
```

### Markdown Parsing

For each `module-*.md` or `week-*.md` file:
1. Split on `## Lesson` or `## M` headings
2. Extract per-lesson: id (from heading), title, type (from `**Type:**` line), body content
3. Convert markdown body to HTML using the same approach as existing scripts
4. Handle special blocks:
   - Blockquotes with `> ...` followed by `— [reference]` → scripture blocks
   - Numbered lists → exercise steps
   - Reflection questions marked with `**Question N:**` or numbered items under reflection headings

### Child Item Extraction

From lesson content, extract structured child items:

- **Reflection questions**: Look for numbered questions in reflection-type sections. Create `reflection_questions` rows with question text, question_type, block_order.
- **Discussion prompts**: Look for prompts in discussion/cohort sections. Map to prompt_type (conceptual, application, integration, general) based on E/E/E/J structure.
- **Exercises**: Look for exercise blocks with title, instructions, purpose, estimated time. Create `exercises` rows.

## Validation (Pre-Insert)

Before writing to the database, validate:

1. [ ] All manifest lesson IDs exist in the markdown files
2. [ ] No empty lesson bodies (flag but allow override)
3. [ ] No placeholder text ("[Content TBD]", "[TODO]", "Lorem ipsum")
4. [ ] All lesson types are valid SECTION_TYPES
5. [ ] 8 weeks present (numbered 1-8, no Week 0)
6. [ ] Reflection sections have 6-8 questions each (warn if outside range)

Report validation results and ask for confirmation before proceeding.

## Database Operations

### Create or update the ingestion script

Create/update `{{SCRIPTS_DIR}}/ingest-[slug]-course.ts` that:

1. Connects via project Drizzle setup (`src/lib/database/`)
2. Uses `getOrgId()` for organization scoping
3. Upserts in this order:
   - `courses` row (find by slug, update if exists, insert if not)
   - `courseWeeks` rows (find by course_id + week_number, upsert)
   - `courseLessons` rows (find by course_id + slug or section_order, upsert)
   - `reflectionQuestions` rows (find by lesson_id + block_order, upsert)
   - `discussionPrompts` rows (find by lesson_id + block_order, upsert)
   - `exercises` rows (find by lesson_id + block_order, upsert)
4. Reports: rows created, rows updated, rows skipped

### Run the script

Execute with: `pnpm tsx {{SCRIPTS_DIR}}/ingest-[slug]-course.ts`

## Post-Ingest Verification

After ingestion:
1. Query the course to verify section count matches manifest
2. Verify child items (reflection questions, discussion prompts, exercises) are linked correctly
3. Suggest running `/course-validate [slug]` for Charter compliance

## Output Format

```
## Course Ingestion Report: [title] ([slug])

### Source: [path]
### Validation: PASS / FAIL (with details)

### Ingested:
- Course: [title] (id: [id])
- Weeks: 8
- Sections: N total
  - Week 1: X sections
  - Week 2: X sections
  - ...
- Reflection questions: N
- Discussion prompts: N
- Exercises: N

### Warnings:
- [any non-blocking issues]

### Next Steps:
- Run `/course-validate [slug]` to check Charter compliance
- Review draft sections in the learn view at /content/courses/[slug]/learn
```

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- Always upsert (idempotent) — running twice should not create duplicates
- Set ingested content to status: "draft" unless the user says otherwise
- Never delete existing data — only insert or update
- Preserve existing content if a lesson already has non-empty content (warn and skip)
- Use the project's existing Drizzle patterns — check `{{SERVICES_DIR}}/courses.service.ts` for query conventions
