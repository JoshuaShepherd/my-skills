---
name: paratext-audit
description: Audit paratext (supporting content) across all platform surfaces — courses, books, articles, exercises, field experiments, and reflection questions. Reports presence, voice quality, rendering gaps, and SEO/GEO readiness. Use before publishing content or to find what needs authoring.
user-invocable: true
allowed-tools: Read, Grep, Glob, mcp__supabase__execute_sql, mcp__supabase__list_tables
---

Audit paratext: $ARGUMENTS

$ARGUMENTS should be a surface to audit: `courses`, `weeks`, `exercises`, `reflections`, `experiments`, `books`, `chapters`, `series`, `podcasts`, `all`.
If omitted, defaults to `all`.
Optionally scope to a specific item: `books the-mdna` or `courses mdna`.

---

## What Is Paratext?

Paratext is everything that frames, introduces, or contextualizes the main content:
- Course and week **descriptions, objectives, themes**
- Exercise **purpose** statements (the "why" before the "what")
- Reflection question **guidance** (hints that deepen the reflection)
- Field experiment **success_criteria** (what "done well" looks like)
- Book **subtitle, description, excerpt, theological_themes, ai_key_points**
- Book chapter **excerpt** (shown in ToC before the reader opens a chapter)
- Book series **description**
- Podcast episode **description**
- Lesson **descriptions** (previews before opening a lesson)
- **meta_title** and **meta_description** fields for SEO/GEO on all surfaces

Paratext optimization has five dimensions:

| Dimension | Question |
|-----------|----------|
| **Presence** | Is the field populated in the database? |
| **Rendering** | Is it surfaced in the UI where a user would see it? |
| **Placement** | Is it at the right moment in the learning journey? |
| **Voice** | Does it sound like Alan Hirsch, not generic LMS copy? |
| **SEO/GEO** | Is it discoverable by search engines and AI assistants? |

---

## Audit Protocol

### Step 1 — Identify Tenant Org

Run this SQL to find the Alan Hirsch organization ID:

```sql
SELECT id, name, slug FROM organizations WHERE slug = 'alan-hirsch' OR name ILIKE '%hirsch%' LIMIT 5;
```

Store the `org_id` for all subsequent queries.

### Step 2 — Course-Level Paratext

```sql
SELECT
  c.id,
  c.title,
  c.slug,
  c.subtitle,
  c.description,
  c.learning_outcomes,
  c.meta_title,
  c.meta_description,
  CASE WHEN c.subtitle IS NULL THEN 'MISSING' ELSE 'OK' END AS subtitle_status,
  CASE WHEN c.description IS NULL THEN 'MISSING' WHEN LENGTH(c.description) < 100 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN c.learning_outcomes IS NULL OR c.learning_outcomes::text = '[]' THEN 'MISSING' ELSE 'OK' END AS outcomes_status,
  CASE WHEN c.meta_title IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_title_status,
  CASE WHEN c.meta_description IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_desc_status
FROM courses c
WHERE c.organization_id = '[ORG_ID]'
ORDER BY c.title;
```

### Step 3 — Week-Level Paratext

```sql
SELECT
  w.id,
  w.week_number,
  w.title,
  w.theme,
  w.description,
  w.objectives,
  c.title AS course_title,
  CASE WHEN w.description IS NULL THEN 'MISSING' WHEN LENGTH(w.description) < 50 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN w.objectives IS NULL OR w.objectives::text = '[]' THEN 'MISSING' ELSE 'OK' END AS objectives_status,
  CASE WHEN w.theme IS NULL THEN 'MISSING' ELSE 'OK' END AS theme_status
FROM course_weeks w
JOIN courses c ON w.course_id = c.id
WHERE c.organization_id = '[ORG_ID]'
ORDER BY c.title, w.week_number;
```

### Step 4 — Exercise Paratext

```sql
SELECT
  e.id,
  e.title,
  e.purpose,
  e.description,
  e.instructions,
  e.deliverables,
  l.title AS lesson_title,
  c.title AS course_title,
  CASE WHEN e.purpose IS NULL THEN 'MISSING' WHEN LENGTH(e.purpose) < 30 THEN 'STUB' ELSE 'OK' END AS purpose_status,
  CASE WHEN e.description IS NULL THEN 'MISSING' ELSE 'OK' END AS desc_status,
  CASE WHEN e.instructions IS NULL OR LENGTH(e.instructions) < 20 THEN 'MISSING' ELSE 'OK' END AS instructions_status
FROM exercises e
LEFT JOIN course_lessons l ON e.lesson_id = l.id
LEFT JOIN courses c ON COALESCE(l.course_id, e.course_id) = c.id
WHERE c.organization_id = '[ORG_ID]'
ORDER BY c.title, l.title, e.block_order;
```

### Step 5 — Reflection Question Paratext

```sql
SELECT
  r.id,
  r.question,
  r.guidance,
  r.question_type,
  l.title AS lesson_title,
  c.title AS course_title,
  CASE WHEN r.guidance IS NULL THEN 'MISSING' ELSE 'OK' END AS guidance_status
FROM reflection_questions r
LEFT JOIN course_lessons l ON r.lesson_id = l.id
LEFT JOIN courses c ON COALESCE(l.course_id, r.course_id) = c.id
WHERE c.organization_id = '[ORG_ID]'
ORDER BY c.title, l.title, r.block_order;
```

### Step 6 — Field Experiment Paratext

```sql
SELECT
  fe.id,
  fe.title,
  fe.description,
  fe.instructions,
  fe.success_criteria,
  fe.experiment_type,
  l.title AS lesson_title,
  CASE WHEN fe.description IS NULL THEN 'MISSING' ELSE 'OK' END AS desc_status,
  CASE WHEN fe.success_criteria IS NULL THEN 'MISSING' ELSE 'OK' END AS criteria_status
FROM field_experiments fe
LEFT JOIN course_lessons l ON fe.lesson_id = l.id
LEFT JOIN course_enrollments ce ON fe.enrollment_id = ce.id
ORDER BY l.title;
```

### Step 7 — Book-Level Paratext

```sql
SELECT
  b.id,
  b.title,
  b.slug,
  b.subtitle,
  b.description,
  b.excerpt,
  b.theological_themes,
  b.ai_key_points,
  b.meta_title,
  b.meta_description,
  b.status,
  CASE WHEN b.subtitle IS NULL THEN 'MISSING' ELSE 'OK' END AS subtitle_status,
  CASE WHEN b.description IS NULL THEN 'MISSING' WHEN LENGTH(b.description) < 100 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN b.excerpt IS NULL THEN 'MISSING' WHEN LENGTH(b.excerpt) < 40 THEN 'STUB' ELSE 'OK' END AS excerpt_status,
  CASE WHEN b.theological_themes IS NULL OR b.theological_themes::text = '[]' OR b.theological_themes::text = 'null' THEN 'MISSING' ELSE 'OK' END AS themes_status,
  CASE WHEN b.ai_key_points IS NULL OR b.ai_key_points::text = '[]' OR b.ai_key_points::text = 'null' THEN 'MISSING' ELSE 'OK' END AS key_points_status,
  CASE WHEN b.meta_title IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_title_status,
  CASE WHEN b.meta_description IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_desc_status
FROM books b
WHERE b.organization_id = '[ORG_ID]'
ORDER BY b.title;
```

**Rendering note:** The book detail page (`/content/books/[slug]/page.tsx`) renders `subtitle`, `description` (as Synopsis), `excerpt` (as pullquote), `theological_themes` (as badges), and `ai_key_points` (as Key Ideas). However, the layout's `generateMetadata` uses `books.description` and `books.title` — it does **not** use `books.meta_title` or `books.meta_description`. Flag this as a rendering gap if those fields are populated.

### Step 8 — Book Chapter Paratext

Two chapter tables exist: `book_chapters` (primary) and `books_chapters` (legacy). Prefer `book_chapters` unless data is only in `books_chapters`.

```sql
-- Primary chapter table
SELECT
  bc.id,
  bc.chapter_number,
  bc.title,
  bc.excerpt,
  bc.meta_title,
  bc.meta_description,
  bc.status,
  bc.is_preview,
  b.title AS book_title,
  CASE WHEN bc.excerpt IS NULL THEN 'MISSING' WHEN LENGTH(bc.excerpt) < 40 THEN 'STUB' ELSE 'OK' END AS excerpt_status,
  CASE WHEN bc.meta_title IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_title_status,
  CASE WHEN bc.meta_description IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_desc_status
FROM book_chapters bc
JOIN books b ON bc.book_id = b.id
WHERE bc.organization_id = '[ORG_ID]'
ORDER BY b.title, bc.chapter_number;
```

**Rendering note:** Chapter `excerpt` is **not rendered** — the Table of Contents on the book detail page shows only `chapter_number` and `title` as links. Chapter `meta_title` and `meta_description` are **not used** — no per-chapter metadata generation exists. Both are rendering gaps.

### Step 9 — Book Series Paratext

```sql
SELECT
  bs.id,
  bs.name,
  bs.slug,
  bs.description,
  bs.status,
  CASE WHEN bs.description IS NULL THEN 'MISSING' WHEN LENGTH(bs.description) < 60 THEN 'STUB' ELSE 'OK' END AS desc_status,
  COUNT(b.id) AS book_count
FROM book_series bs
LEFT JOIN books b ON b.series_id = bs.id AND b.organization_id = '[ORG_ID]'
WHERE bs.organization_id = '[ORG_ID]'
GROUP BY bs.id, bs.name, bs.slug, bs.description, bs.status
ORDER BY bs.name;
```

### Step 10 — Podcast Episode Paratext

```sql
SELECT
  pe.id,
  pe.title,
  pe.slug,
  pe.description,
  pe.meta_title,
  pe.meta_description,
  pe.status,
  pe.episode_number,
  pe.season_number,
  ps.name AS series_name,
  CASE WHEN pe.description IS NULL THEN 'MISSING' WHEN LENGTH(pe.description) < 60 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN pe.meta_title IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_title_status,
  CASE WHEN pe.meta_description IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_desc_status
FROM podcast_episodes pe
LEFT JOIN podcast_series ps ON pe.series_id = ps.id
WHERE pe.organization_id = '[ORG_ID]'
ORDER BY ps.name, pe.season_number, pe.episode_number;
```

---

## Voice Audit

For each populated paratext field, check against Alan Hirsch's five voice markers:

| Marker | Minimum Standard |
|--------|-----------------|
| **Christocentric** | At least 1 reference to Jesus, Kingdom, Lord, or Gospel per 100 words |
| **Pastoral warmth** | "We" or "you" language present; invitational, not prescriptive |
| **Narrative imagery** | At least 1 organic/journey/movement metaphor per paragraph |
| **Theological depth** | At least 1 theological concept, historical reference, or framework term |
| **Prophetic intensity** | At least 1 reframing question or productive challenge |

**Anti-patterns to flag:**
- Generic LMS language: "In this exercise, you will...", "By the end of this module..."
- Corporate: "leverage," "optimize," "best practices," "scalable"
- Academic hedging: "Research suggests...", "It can be argued..."
- Antithesis patterns: "Not X, but Y" structures
- Missing Christocentric anchor: Any description > 80 words with no Jesus/Kingdom reference

**Voice scoring per field:**
- 5/5 markers: ✅ Excellent
- 3–4/5: ⚠️ Needs refinement
- 0–2/5: ❌ Rewrite required

---

## Rendering Audit

Check whether each paratext field is rendered in the UI:

### Courses

| Field | Component | Rendered? | Notes |
|-------|-----------|-----------|-------|
| `courses.subtitle` | `CourseOverviewContent` | ✅ Yes | Shown in hero |
| `courses.description` | `CourseOverviewContent` | ✅ Yes | Shown in overview section |
| `courses.learning_outcomes` | `CourseOverviewContent` | ✅ Yes | Rendered as "What You Will Gain" grid |
| `courses.meta_title/meta_description` | Page `<head>` | ⚠️ Partial | Check if used in generateMetadata |
| `course_weeks.theme` | Course sidebar | ❌ No | Field in schema, never shown |
| `course_weeks.description` | Week intro | ❌ No | Field in schema, never shown |
| `course_weeks.objectives` | Course sidebar/week intros | ❌ No | Field in schema, never shown |
| `course_lessons.description` | Sidebar lesson list | ❌ No | Not shown before opening lesson |
| `exercises.purpose` | `PracticalExerciseSection` | ✅ Yes | Shows as muted subtitle above steps |
| `exercises.description` | `PracticalExerciseSection` | ❌ No | Field exists, not rendered |
| `reflection_questions.guidance` | `ReflectionSection` | ❌ No | Field in schema, not rendered |
| `field_experiments.success_criteria` | `FieldExperimentSection` | ❌ No | Field in schema, not rendered |

### Books

| Field | Component | Rendered? | Notes |
|-------|-----------|-----------|-------|
| `books.subtitle` | Book detail page | ✅ Yes | Shown below title as large muted text |
| `books.description` | Book detail page | ✅ Yes | Rendered as "Synopsis" section, split on `\n\n` |
| `books.excerpt` | Book detail page | ✅ Yes | Rendered as pullquote `<blockquote>` after the action buttons |
| `books.theological_themes` | Book detail page | ✅ Yes | Rendered as badge chips alongside book type badge |
| `books.ai_key_points` | Book detail page | ✅ Yes | Rendered as "Key Ideas" bullet list (up to 6 items) |
| `books.meta_title` | Page `<head>` | ❌ No | Layout uses `books.title` via `buildContentMetadata`, ignores `meta_title` |
| `books.meta_description` | Page `<head>` | ❌ No | Layout uses `books.description`, ignores `meta_description` |
| `book_chapters.excerpt` | ToC on book detail / sidebar | ❌ No | ToC renders only chapter number + title |
| `book_chapters.meta_title` | Per-chapter `<head>` | ❌ No | No per-chapter metadata generation |
| `book_chapters.meta_description` | Per-chapter `<head>` | ❌ No | No per-chapter metadata generation |
| `book_series.description` | Series page | ❓ Unknown | No series index page component confirmed |
| `podcast_episodes.description` | Episode page | ❓ Unknown | Verify against episode detail page component |
| `podcast_episodes.meta_title/meta_description` | Page `<head>` | ❓ Unknown | Check generateMetadata on episode route |

---

## SEO/GEO Audit

### Courses
- [ ] `courses.meta_title` — populated for every published course
- [ ] `courses.meta_description` — 150–160 chars, includes primary keyword
- [ ] `courses.learning_outcomes` — populated (AI engines cite these in answers about the course)
- [ ] `course_weeks.description` — populated (week intros improve structured data)
- [ ] `exercises.purpose` — populated (shows intent; E-E-A-T signal)
- [ ] `reflection_questions.guidance` — populated (depth signals expertise)

### Books
- [ ] `books.description` — populated and ≥ 100 words (used by `generateMetadata` as the page meta description)
- [ ] `books.subtitle` — populated (shown on detail page; improves long-tail keyword coverage)
- [ ] `books.excerpt` — populated (pullquote on detail page; high-value E-E-A-T signal)
- [ ] `books.theological_themes` — populated as JSON array (rendered as badge chips; improves topical authority signals)
- [ ] `books.ai_key_points` — populated as JSON array of strings (rendered as "Key Ideas"; AI engines cite these directly)
- [ ] `books.meta_title` — **currently not used in generateMetadata** (rendering gap; flag for fix)
- [ ] `books.meta_description` — **currently not used in generateMetadata** (rendering gap; flag for fix)
- [ ] `book_chapters.excerpt` — populated (not yet rendered, but worth populating for future ToC enhancement)

### Podcasts
- [ ] `podcast_episodes.description` — populated (primary discoverability signal for episodes)
- [ ] `podcast_episodes.meta_title` — populated (check rendering gap before prioritizing)

---

## Output Format

Produce a structured audit report with this shape:

```
## Paratext Audit: [Surface] — [Date]

### Executive Summary
- Total paratext fields inventoried: X
- Fully populated: X (X%)
- Stubs (< minimum length): X
- Missing (NULL): X (X%)
- Rendering gaps: X fields defined but not shown in UI
- Voice quality: X% at ✅ / X% at ⚠️ / X% at ❌

### By Surface

#### Courses
| Course | Subtitle | Description | Learning Outcomes | Meta Title | Meta Desc |
|--------|----------|-------------|-------------------|------------|-----------|
| [name] | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ |

#### Weeks
| Course | Week | Theme | Description | Objectives |
|--------|------|-------|-------------|------------|

#### Exercises (purpose field)
| Course | Lesson | Exercise | Purpose | Description |
|--------|--------|----------|---------|-------------|

#### Reflection Questions (guidance field)
| Course | Lesson | Question (first 60 chars) | Guidance |
|--------|--------|--------------------------|---------|

#### Field Experiments (success_criteria)
| Lesson | Title | Description | Success Criteria |
|--------|-------|-------------|-----------------|

#### Books
| Book | Subtitle | Description | Excerpt | Themes | Key Points | Meta Title | Meta Desc |
|------|----------|-------------|---------|--------|------------|------------|-----------|
| [name] | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ |

#### Book Chapters (excerpt field)
| Book | Ch# | Title | Excerpt | Preview? |
|------|-----|-------|---------|----------|

#### Book Series
| Series | Description |
|--------|-------------|

#### Podcast Episodes
| Series | Ep# | Title | Description | Meta Title | Meta Desc |
|--------|-----|-------|-------------|------------|-----------|

### Rendering Gaps
List fields that are populated but not rendered in the UI.

### Voice Issues
List specific fields/passages that fail voice markers, with the offending text quoted.

### Priority Actions (ordered)
1. [Highest impact gap]
2. ...

### Suggested Next Steps
- To fill missing course/lesson paratext: run `/paratext-author courses [slug]`
- To fill missing book paratext: run `/paratext-author books [slug]`
- To fill missing podcast paratext: run `/paratext-author podcasts [series-name]`
- To fix rendering gaps: edit the relevant component or layout file listed in the Rendering Audit
- To fix voice: run `/alan-voice rewrite: [paste failing text]`
- To fix `books.meta_title/meta_description` not being used: update `src/app/(public)/content/books/[slug]/layout.tsx` to pass `meta_title` and `meta_description` from the DB into `buildContentMetadata`
```

---

## Rules

- Always query the database — never assume what's populated
- Report what exists, not what you think should exist
- Voice audit only applies to populated fields — don't flag missing fields for voice
- Rendering audit is against current component files — read them before reporting
- Priority actions: data gaps first, then rendering, then voice polish
- After auditing, always suggest which surface to author first using `/paratext-author`
