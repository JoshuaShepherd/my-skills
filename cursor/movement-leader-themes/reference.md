# Theme docs output schema

Reference implementation: **brad-brisco** repo — `docs/themes/CORE_THEMES.md` (five themes, six-book corpus) and `docs/themes/discipleship.md` (sibling deep-dives).

## Part A — `CORE_THEMES.md`

### Header

```markdown
# {Full Name} — Core Themes

**Purpose:** Fresh assessment of {Name}'s core themes after full book corpus
ingestion (`docs/books/`) and movement leader research. This document proposes
the organizing system for pathway pages, evergreen articles, and courses.

**Status:** Draft for review
**Last updated:** {YYYY-MM-DD}
**Corpus reviewed:** {N books}, research tree, {article sources}
```

### Required sections

1. **Executive Summary** — single integrated argument; table `# | pathway slug | Title | Role in the corpus`; justify theme count; list themes that should **not** become pathways.
2. **Methodology** — "What we read" table; four tests for pathway status; what keeps a theme subordinate (method, context, borrowed framework).
3. **The Integrated Argument** — ASCII flow diagram; magnum-opus structure mapping where supported.
4. **Theme {n}: {Title}** (per theme) — Slug, EEAT tags, one-line claim; what it is; entails table; primary corpus; what belongs here; pathway reframe table; 6-lesson course outline; why it earns pathway status.
5. **Themes Considered and Rejected as Pathways** — mandatory table.
6. **Mapping: Books → Themes**
7. **Mapping: Pathways → Content Types**
8. **Relationship to Existing Platform Config**
9. **Decision Record**
10. **Sources**

### Deriving themes

- Read every book's chapters before proposing taxonomy.
- Prefer the leader's own organizing structure over invented clustering.
- Use the leader's coined terms.
- 4–6 themes normal; resist inflation of methods/contexts/borrowed frameworks.
- Existing config slugs: confirm and explain by default.

## Part B — `{slug}.md` deep-dive

### Front matter

```yaml
---
author: {slug}
title: {Theme Title}
slug: {theme-slug}
reframing_question: "{provocation}"
companion_pillar: {eeat-tag}
primary_corpus:
  - {Book (ch. N, "Chapter Title")}
companion_course: {course-slug}
group_order: [Understand, Examine, Apply, Go deeper]
theme_order: {n}
one_line_claim: "{claim}"
last_updated: {YYYY-MM-DD}
---
```

### 12 sections

1. Hero / provocation
2. Overview
3. The model / framework
4. The scripture thread
5. The historical context
6. The cases (plural, corpus-grounded)
7. The practices (numbered, footnoted)
8. The curated resources
9. The AI Lab
10. FAQs
11. Distortion warnings (≥2)
12. Invitation

Each substantive section: ≥3 grounded citations. Close with footnote list (`claim · source · page · type`) and HTML delivery-note self-check.

### Four necessities

Every deep-dive must include **dissonance**, **action** (practices), **reflection**, and **community** (named cohort/relationship).
