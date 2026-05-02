---
name: course-validate
description: Validate a course against the Transformational Course Charter — checks Four Necessities, section completeness, word counts, and structure. Use before publishing or after authoring.
user-invocable: true
allowed-tools: Read, Bash, Grep, Glob
---

Validate course against the Charter: $ARGUMENTS

$ARGUMENTS should be a course slug. If empty, ask the user.

## Before Starting

1. Read `_docs/TRANSFORMATIONAL_COURSE_CHARTER.md` for the Four Necessities
2. Read `_docs/TRANSFORMATIONAL_COURSE_PLAYBOOK.md` for the canonical structure
3. Read `src/lib/schemas/course-learn.ts` for valid SECTION_TYPES

## Data Gathering

Fetch the course data. Prefer reading from the database via an API call or script:
- Check if there's an API route at `src/app/api/custom/courses/[slug]/weeks/`
- Alternatively, read markdown source files from `content-library/courses/[slug]/` if they exist
- Or check `forgotten-ways-course/docs/` for the forgotten-ways course

Build a complete picture: all weeks, all sections per week, all child items (reflection_questions, discussion_prompts, exercises).

## Validation Checks

### 1. STRUCTURE (8-Week Compliance)

- [ ] Exactly 8 weeks (numbered 1-8, no Week 0)
- [ ] Week 1 is introduction/orientation
- [ ] Week 8 is synthesis/closing/commissioning
- [ ] Weeks 2-7 are core modules
- [ ] Each week has sections in correct order

### 2. FOUR NECESSITIES (per core week, 2-7)

#### Dissonance
- [ ] At least one of: `lordship_opening`, `chat_dissonance`, `scripture`, or reframing content per week
- [ ] Opening section creates tension or challenges assumptions

#### Action
- [ ] At least one of: `field_experiment`, `practical_exercise`, `chat_action`, or action-oriented content per week
- [ ] Action content has concrete, time-boxed steps
- [ ] Note: `chat_action` (AI Lab companion) satisfies this necessity — standalone `field_experiment` / `practical_exercise` sections are recommended but not required

#### Reflection
- [ ] At least one of: `reflection` (with 6-8 questions), `chat_reflection`, or structured reflection content per week
- [ ] If standalone `reflection` section exists, count reflection_questions — flag if < 6 or > 8
- [ ] Note: `chat_reflection` (AI Lab companion) satisfies this necessity — standalone `reflection` sections with question lists are recommended but not required

#### Community
- [ ] `discussion` or `cohort_session` section present per week
- [ ] Discussion prompts follow E/E/E/J structure (Explore, Evaluate, Employ, Journal) for cohort sessions
- [ ] Week 1 includes community onboarding element

### 3. SECTION COMPLETENESS (per core week 2-7)

Check that each core week has all 14 canonical sections:

| M.N.X | section_type | Required? |
|-------|-------------|-----------|
| M.N.1 | lordship_opening | Required |
| M.N.2 | reading | Required |
| M.N.3 | video | Required |
| M.N.4 | scripture | Required |
| M.N.5 | reflection OR chat_reflection | Required (either form) |
| M.N.6 | practical_exercise OR chat_action | Required (either form) |
| M.N.7 | field_experiment | Recommended |
| M.N.8 | discussion | Required |
| M.N.9 | cohort_session | Recommended |
| M.N.10 | integration | Required |
| M.N.11 | lordship_closing | Required |
| M.N.12 | looking_ahead | Required (weeks 2-6) |
| M.N.13 | resource_blurb | Recommended |
| M.N.14 | action | Recommended |

### 4. CONTENT QUALITY (if content is available)

- [ ] Reading sections: 2,500-3,500 words (flag if outside range)
- [ ] Video sections: have video_url or embed_code (or flagged as placeholder)
- [ ] No placeholder text remaining ("[Content TBD]", "[TODO]", "Lorem ipsum")
- [ ] No empty content fields on published sections
- [ ] Lordship openings include prayer/devotional element
- [ ] Lordship closings include commitment + blessing

### 5. EXCLUSIONS (things that must NOT be present)

- [ ] No "Week 0" references
- [ ] No mDNA assessment links/buttons in course flow
- [ ] No "adapted to your level" or "personalized pathway" language
- [ ] No variable course duration badges

## Output Format

```
## Course Validation Report: [course title] ([slug])

### Overall: PASS / FAIL (X/5 checks passing)

### 1. Structure ✅/❌
- [details]

### 2. Four Necessities ✅/❌
- Dissonance: [status per week]
- Action: [status per week]
- Reflection: [status per week, question counts]
- Community: [status per week]

### 3. Section Completeness ✅/❌
- Week 1: X/Y sections present
- Week 2: X/14 canonical sections
- ...
- Week 8: X/Y sections present
- Missing sections: [list]

### 4. Content Quality ✅/❌/⚠️ SKIPPED (no content yet)
- [details or "draft course — content not yet authored"]

### 5. Exclusions ✅/❌
- [details]

### Action Items
1. [Most critical fix first]
2. [...]
```

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- AI Lab chat types (`chat_dissonance`, `chat_action`, `chat_reflection`) satisfy the Four Necessities for Dissonance, Action, and Reflection respectively — standalone section equivalents are recommended but not required
- Be strict on: structure (8 weeks), community (discussion/cohort per week), and at least one form of dissonance/action/reflection per week
- Be advisory on recommended items (resource_blurb, field_experiment, standalone reflection questions)
- If the course is in draft status with no content, skip content quality checks but still validate structure and section completeness
- Always report the total section count and any gaps
