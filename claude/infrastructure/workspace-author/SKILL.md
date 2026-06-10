---
name: workspace-author
description: "Write new workspace documents — articles, research notes, project docs, and ebook sections — following Brad Brisco's voice identity, EEAT theme taxonomy, and the workspace frontmatter conventions. Use when creating new content for docs/workspace/."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch, TodoWrite
---

Write a new workspace document: $ARGUMENTS

$ARGUMENTS should be one of:
- A content brief (e.g., "article on third places and missional community")
- A section + title (e.g., "articles/why-covocational-is-first-choice")
- A research topic (e.g., "research note on theology of work")
- Empty — ask the user what to write

## Before You Write Anything

### 1. Load voice identity

Read `docs/workspace/author/voice-identity.md` completely. Every piece of content must pass the five voice markers:

1. **Missional Framing** (≥0.7) — Ground in missio Dei, sentness, local mission field
2. **Pastoral Warmth** (≥0.5) — "We," "you," relational, encouraging
3. **Theological Grounding** (≥0.6) — Scripture and doctrine before practice
4. **Practical Application** (≥0.6) — Clear "so what?" and next steps
5. **Prophetic Clarity** (0.4–0.7) — Name what must change, without cynicism

Never sound like: corporate consultant, detached academic, program jockey, hype/buzz, vague encouragement.

### 2. Load theme taxonomy

Read `docs/workspace/insights/eeat-content-pipeline.md` for the EEAT theme taxonomy:

**Tier 1 (Primary):**
- `missional-ecclesiology` — Church as sent, missio Dei
- `church-planting-multiplication` — Strategies, models, practices
- `covocational-ministry` — Marketplace work + ministry
- `missional-living-practice` — Everyday mission, practices
- `neighborhood-place` — Theology of place, neighboring

**Tier 2 (Supporting):**
- `theological-foundations-mission`, `leadership-culture-change`, `work-vocation-worship`, `digital-ecclesiology`, `discipleship-formation`, `hospitality-community`, `resources-stewardship`

### 3. Check existing corpus

Before writing, search the workspace for related content to avoid duplication and find material to reference:

```
grep -r "TOPIC_KEYWORDS" docs/workspace/ --include="*.md" -l
```

Read the article index: `docs/workspace/meta/article-index.md`

## Document Types

### Articles (`articles/`)

Full articles for the covocational resource library. These are the primary published content.

**Frontmatter format:**
```yaml
---
title: "Article Title"
source: "Original publication or 'Original'"
url: "https://..."
published_at: "YYYY-MM-DD"
author: "Brad Brisco"
content_type: "article"
themes: ["covocational-ministry", "church-planting-multiplication"]
status: draft
audience: collaborators
updated: YYYY-MM-DD
---
```

**Structure:**
1. **Lead paragraph** (2-4 sentences) — Why this matters to a covocational planter
2. **Sections** (H2) — 3-6 sections building the argument
3. **Subsections** (H3) — As needed for depth
4. **Callouts** — Use `> **Practice:**` for actionable takeaways
5. **See also** — Links to related workspace docs

**Length:** 800-2000 words. Medium paragraphs. Clear subheads.

**Filename:** Lowercase kebab-case, no `brad-brisco-` prefix. e.g., `why-covocational-is-first-choice.md`

### Research Notes (`research/`)

Working research for theological foundations, literature review, or topic exploration.

**Frontmatter:**
```yaml
---
title: "Research Topic"
description: "One-line summary"
order: N
---
```

**Structure:**
1. **Core Argument** — Thesis in 2-3 sentences
2. **Reading List** — Key sources (books, articles, scholars)
3. **Key Themes** — Bullet points of major findings
4. **Questions** — Open questions for further exploration
5. **Connections** — Links to other workspace docs this informs

### Project Docs (`projects/`)

Active collaborative project documents — guides, frameworks, plans.

**Frontmatter:**
```yaml
---
title: "Project Name"
description: "One-line summary"
order: N
---
```

**Structure:** Flexible — use whatever structure serves the project. Include:
- Overview and goals
- Key principles or framework
- Next steps with `- [ ]` task checkboxes
- References to related workspace docs

### Ebook manuscripts (`books/`)

Additions or revisions to covocational e-book manuscripts live alongside other book content in `books/`.

**Frontmatter:**
```yaml
---
title: "Ebook Title"
description: "One-line summary"
order: N
---
```

Follow the existing ebook voice and structure. Read 1–2 existing ebooks in `docs/workspace/books/` before writing.

## Writing Process

### Step 1: Research

- Search the workspace corpus for related content
- Read the voice identity and failure modes
- If the topic overlaps existing articles, read them first
- For new theological ground, search the books in `docs/workspace/books/`

### Step 2: Outline

Present a brief outline to the user before writing:
- Proposed title
- Target section (which workspace directory)
- Theme tags (from EEAT taxonomy)
- 3-5 section headings
- Key corpus references to weave in

Wait for user approval before drafting.

### Step 3: Draft

Write the full document following the voice markers. Key rules:
- **Why before what** — Theological/missional grounding before practical steps
- **Congregation and planter in view** — Speak to both
- **Frameworks from Brad's corpus** — Reference his actual books, concepts, and language
- **Scripture woven in** — Not proof-texted; carries the argument
- **No invented anecdotes** — Only use stories from the provided corpus

### Step 4: Self-Check

Before presenting the draft, verify:
- [ ] All 5 voice markers are present at required levels
- [ ] No failure mode language (corporate, academic, hype, vague)
- [ ] Frontmatter is complete and correctly formatted
- [ ] Theme tags are valid (from the taxonomy)
- [ ] Title is clear and specific
- [ ] Filename follows conventions (kebab-case, no prefix)
- [ ] No metadata or frontmatter details leak into the prose body
- [ ] `> **Practice:**` callouts for actionable takeaways
- [ ] Cross-references to related workspace docs where relevant

### Step 5: Write to disk

Save to `docs/workspace/{section}/{filename}.md`

Update the article index at `docs/workspace/meta/article-index.md` if writing an article.

## Research-Driven Articles

When the user asks for content based on a research need:

1. **Use WebSearch** to find current sources, statistics, and perspectives
2. **Check the books** in `docs/workspace/books/` for Brad's existing positions
3. **Cross-reference** with existing workspace research notes
4. **Cite sources** — Use inline references and a "Sources" or "See Also" section
5. **Ground in Brad's voice** — External research supports Brad's theological framework, not the other way around

## Things to Never Do

- Never put metadata, status fields, or editorial notes in the rendered body text
- Never invent quotes, stories, or statistics
- Never use language from the failure modes list
- Never write without loading the voice identity first
- Never skip the outline step for articles
- Never duplicate content that already exists in the workspace
