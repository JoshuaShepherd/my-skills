---
name: paratext-author
description: Write missing or stub paratext for any platform surface — books, courses, podcast episodes — in Alan Hirsch's voice. Queries the database for gaps, writes content, and updates via SQL. Use after running /paratext-audit to fill what it found.
user-invocable: true
allowed-tools: Read, Grep, Glob, mcp__supabase__execute_sql, mcp__supabase__list_tables
---

Write paratext for: $ARGUMENTS

$ARGUMENTS format: `[surface] [slug-or-identifier]`

Examples:
- `books the-mdna` — write all missing paratext for one book
- `books all` — write missing paratext for every book
- `courses mdna` — write missing paratext for one course
- `courses all` — write missing paratext for every course
- `chapters the-mdna` — write chapter excerpts for one book
- `podcasts all` — write missing episode descriptions
- `series all` — write missing series descriptions

If surface is omitted, ask the user which surface to target before proceeding.

---

## Step 1 — Identify Tenant Org

```sql
SELECT id, name, slug FROM organizations WHERE slug = 'alan-hirsch' OR name ILIKE '%hirsch%' LIMIT 5;
```

Store the `org_id` for all subsequent queries.

---

## Step 2 — Fetch Current State

Query only the fields that need authoring. Never rewrite content that is already populated and passes the minimum length check.

### For `books [slug]`

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
  b.publication_date,
  b.publisher,
  -- Status flags
  CASE WHEN b.subtitle IS NULL THEN 'MISSING' ELSE 'OK' END AS subtitle_status,
  CASE WHEN b.description IS NULL THEN 'MISSING' WHEN LENGTH(b.description) < 100 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN b.excerpt IS NULL THEN 'MISSING' WHEN LENGTH(b.excerpt) < 40 THEN 'STUB' ELSE 'OK' END AS excerpt_status,
  CASE WHEN b.theological_themes IS NULL OR b.theological_themes::text = '[]' OR b.theological_themes::text = 'null' THEN 'MISSING' ELSE 'OK' END AS themes_status,
  CASE WHEN b.ai_key_points IS NULL OR b.ai_key_points::text = '[]' OR b.ai_key_points::text = 'null' THEN 'MISSING' ELSE 'OK' END AS key_points_status,
  CASE WHEN b.meta_title IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_title_status,
  CASE WHEN b.meta_description IS NULL THEN 'MISSING' ELSE 'OK' END AS meta_desc_status
FROM books b
WHERE b.organization_id = '[ORG_ID]'
  AND b.slug = '[SLUG]';  -- Remove this line for 'all'
```

Also fetch chapter titles to inform your understanding of the book's structure:

```sql
SELECT chapter_number, title FROM book_chapters
WHERE book_id = '[BOOK_ID]'
ORDER BY chapter_number;
```

Also fetch the book's actual content from the local markdown corpus:

```
Look in content-library/ or _docs/ for markdown files matching the book slug.
If a markdown corpus file exists, read it to extract key arguments, quotes, and themes.
```

### For `courses [slug]`

```sql
SELECT
  c.id, c.title, c.slug, c.description, c.subtitle, c.learning_outcomes,
  CASE WHEN c.description IS NULL THEN 'MISSING' WHEN LENGTH(c.description) < 100 THEN 'STUB' ELSE 'OK' END AS desc_status,
  CASE WHEN c.subtitle IS NULL THEN 'MISSING' ELSE 'OK' END AS subtitle_status,
  CASE WHEN c.learning_outcomes IS NULL OR c.learning_outcomes::text = '[]' THEN 'MISSING' ELSE 'OK' END AS outcomes_status
FROM courses c
WHERE c.organization_id = '[ORG_ID]'
  AND c.slug = '[SLUG]';
```

```sql
SELECT w.id, w.week_number, w.title, w.theme, w.description, w.objectives,
  CASE WHEN w.theme IS NULL THEN 'MISSING' ELSE 'OK' END AS theme_status,
  CASE WHEN w.description IS NULL OR w.description ILIKE 'By the end of this week%' THEN 'NEEDS_REWRITE' ELSE 'OK' END AS desc_status,
  CASE WHEN w.objectives IS NULL OR w.objectives::text = '[]' THEN 'MISSING' ELSE 'OK' END AS objectives_status
FROM course_weeks w
WHERE w.course_id = '[COURSE_ID]'
ORDER BY w.week_number;
```

```sql
SELECT l.id, l.title, l.description, l.week_number,
  CASE WHEN l.description IS NULL THEN 'MISSING'
       WHEN LENGTH(l.description) < 30 THEN 'STUB'
       WHEN l.description IN ('Opening video','Dissonance','Reflection','Action step','Cohort meeting','Exit ticket','Commissioning') THEN 'STUB'
       ELSE 'OK' END AS desc_status
FROM course_lessons l
WHERE l.course_id = '[COURSE_ID]'
ORDER BY l.week_number;
```

### For `chapters [book-slug]`

```sql
SELECT bc.id, bc.chapter_number, bc.title, bc.excerpt,
  CASE WHEN bc.excerpt IS NULL THEN 'MISSING' WHEN LENGTH(bc.excerpt) < 40 THEN 'STUB' ELSE 'OK' END AS excerpt_status
FROM book_chapters bc
JOIN books b ON bc.book_id = b.id
WHERE b.slug = '[SLUG]' AND bc.organization_id = '[ORG_ID]'
ORDER BY bc.chapter_number;
```

### For `podcasts [slug-or-all]`

```sql
SELECT pe.id, pe.title, pe.slug, pe.description, pe.episode_number, ps.name AS series_name,
  CASE WHEN pe.description IS NULL THEN 'MISSING' WHEN LENGTH(pe.description) < 60 THEN 'STUB' ELSE 'OK' END AS desc_status
FROM podcast_episodes pe
LEFT JOIN podcast_series ps ON pe.series_id = ps.id
WHERE pe.organization_id = '[ORG_ID]'
ORDER BY ps.name, pe.episode_number;
```

---

## Step 3 — Write the Paratext

Write **only** fields that have status MISSING, STUB, or NEEDS_REWRITE. Do not regenerate content that is already OK.

### Voice Requirements (mandatory for all output)

All paratext must pass Alan Hirsch's five voice markers:

| Marker | Minimum | What to do |
|--------|---------|-----------|
| **Christocentric** | ≥1 ref per 100 words | Ground every description in Jesus, Lord, Kingdom, or Gospel |
| **Pastoral warmth** | "We/you" present | Invitational, relational — never clinical or prescriptive |
| **Narrative imagery** | ≥1 metaphor per paragraph | Movement/DNA, organic/seed/growth, journey/road, ocean/current |
| **Theological depth** | ≥1 historical example or framework term | Early church, Chinese underground, Methodist, SMRC, mDNA, APEST |
| **Prophetic intensity** | ≥1 challenge or reframing question | Not motivational — prophetically grounded |

**Failure modes to avoid in all output:**
- Generic catalog copy: "This book explores...", "In this course you will learn..."
- Corporate vocabulary: leverage, optimize, scalable, best practices
- Antithesis patterns: "Not X, but Y"
- Missing Christocentric anchor in any text > 80 words
- Rushing to application before establishing meaning

### Field-Specific Guidelines

#### `books.description` (100–300 words, 2–3 paragraphs)
- Open with the central theological tension or question the book addresses
- Paragraph 2: what Alan argues and the key frameworks/concepts introduced
- Paragraph 3: the invitation and stakes — why this matters for the reader's community
- Do not summarize chapter by chapter
- Must include at least one historical example (early church, Chinese underground, etc.)

#### `books.excerpt` (40–100 words)
- A single striking passage that captures the book's prophetic voice
- Suitable as a pullquote — should feel like Alan speaking, not about Alan
- Can be adapted from the actual book text if available in corpus, or written in his voice
- Christocentric anchor required
- No antithesis patterns

#### `books.subtitle` (8–15 words)
- Describes the book's core argument or distinctive contribution
- Should be searchable — include a primary keyword (e.g., "apostolic," "missional," "movement")
- Plain, direct, not cute

#### `books.theological_themes` (JSON array of 3–6 strings)
- Short theme labels, each 1–4 words
- Examples: `["Apostolic Genius", "Movement DNA", "Jesus is Lord", "Missional Church", "APEST", "Communitas"]`
- Use Alan's framework terms where applicable

#### `books.ai_key_points` (JSON array of 4–6 strings, each 10–20 words)
- Complete sentences, written in Alan's voice
- Each captures one transferable insight from the book
- Structured as a claim, not a topic label
- Examples: `["Apostolic Genius is the latent movement potential embedded in every genuine Jesus community.", "The early church grew from 25,000 to 20 million in 200 years with no buildings and no centralized hierarchy."]`

#### `book_chapters.excerpt` (40–80 words)
- A hook for the chapter — what question it opens, what tension it surfaces
- Written as though previewing the chapter to a reader deciding whether to read it
- Draws from the chapter's actual content if available in corpus
- 1–2 sentences max

#### `course_weeks.description` (80–150 words)
- Written in Alan's first-person voice, speaking directly to the learner
- Opens with the week's central question or tension — not "by the end of this week"
- Names the theological or historical ground for the week
- Ends with an invitation or prophetic challenge
- Generic LMS format ("By the end of this week you will:") is always a STUB — rewrite it

#### `course_lessons.description` (40–100 words)
- 1–2 sentences previewing what the learner is about to encounter
- Not a summary — a hook
- For videos: set up the central question Alan will address
- For reflections: name the space being opened, not the answer
- For exercises/steps: name the concrete commitment and what it produces
- For cohort meetings: name the central question for the conversation

#### `podcast_episodes.description` (60–120 words)
- Opens with the episode's central question or tension
- Names who Alan is in conversation with (if applicable)
- Names 2–3 key ideas or turning points in the conversation
- Ends with why this conversation matters for the listener's community

---

## Step 4 — Write and Execute SQL Updates

For each field that needs content, write the UPDATE statement and execute it immediately.

**Pattern for books:**
```sql
UPDATE books SET
  description = '[WRITTEN CONTENT]',
  excerpt = '[WRITTEN EXCERPT]',
  subtitle = '[WRITTEN SUBTITLE]',
  theological_themes = '["Theme 1", "Theme 2", "Theme 3"]'::jsonb,
  ai_key_points = '["Key insight one.", "Key insight two.", "Key insight three."]'::jsonb
WHERE id = '[BOOK_ID]';
```

**Pattern for book chapters:**
```sql
UPDATE book_chapters SET excerpt = '[WRITTEN EXCERPT]'
WHERE id = '[CHAPTER_ID]';
```

**Pattern for course weeks:**
```sql
UPDATE course_weeks SET
  theme = '[WEEK THEME]',
  description = '[WRITTEN DESCRIPTION]',
  objectives = '["Objective 1", "Objective 2", "Objective 3"]'::jsonb
WHERE id = '[WEEK_ID]';
```

**Pattern for course lessons:**
```sql
UPDATE course_lessons SET description = '[WRITTEN DESCRIPTION]'
WHERE id = '[LESSON_ID]';
```

**Pattern for podcast episodes:**
```sql
UPDATE podcast_episodes SET description = '[WRITTEN DESCRIPTION]'
WHERE id = '[EPISODE_ID]';
```

Execute updates in batches by surface. After each batch, confirm with a SELECT that the rows were updated.

---

## Step 5 — Verify and Report

After all updates are written, run a final count query per surface:

```sql
-- Example for books
SELECT
  CASE WHEN description IS NULL THEN 'MISSING' WHEN LENGTH(description) < 100 THEN 'STUB' ELSE 'OK' END AS status,
  COUNT(*) FROM books WHERE organization_id = '[ORG_ID]' GROUP BY 1;
```

Report back with:
- How many fields were written per surface
- Any fields that could not be written (missing source material, unclear content)
- Rendering gaps encountered (fields written but not yet rendered in UI)
- Suggested next step (re-run `/paratext-audit` to confirm zero gaps)

---

## Rules

- **Never overwrite OK content.** Only write MISSING, STUB, or NEEDS_REWRITE fields.
- **Always query before writing.** Never assume what's populated.
- **Use the book corpus.** Check `content-library/` for markdown source files before inventing content.
- **Write in batches by surface.** Don't interleave books and courses in a single session.
- **Execute SQL immediately after writing.** Don't stage updates — write and apply in one pass.
- **Voice check before SQL.** Re-read each piece of content before executing. If it fails any voice marker, rewrite it first.
- **Run paratext-audit after.** Always close by suggesting the user verify with `/paratext-audit [surface]`.
