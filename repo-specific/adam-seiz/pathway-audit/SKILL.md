---
name: pathway-audit
description: Audit a pathway page against the canonical 12-section architecture. Reports what's missing, what's below spec, what's complete, and what needs improvement for SEO/GEO, voice, and formation quality. Use before publishing a pathway or after adding new sections.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit pathway: $ARGUMENTS

$ARGUMENTS should be a pathway slug (e.g., `metanoia`) or `all` to audit every pathway.

Valid slugs: `reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`

## Before Starting

1. Read `src/lib/content/pathways/types.ts` — the TypeScript interfaces
2. Read the pathway file: `src/lib/content/pathways/[slug].ts`
3. Read `src/app/(public)/pathways/[slug]/page.tsx` — check what renders
4. Check for case study pages: `src/app/(public)/pathways/[slug]/case-studies/`
5. Check for reflection questions and glossary terms (may be in `extras` or missing entirely)

---

## Canonical Architecture (what you're auditing against)

Every pathway page must have these 12 sections in 4 groups. The sidebar TOC must surface 7 as primary navigable anchors.

**GROUP 1 — UNDERSTAND**
1. Overview (400–600 words)
2. The Model (named — not "Framework")
3. Quotes (3–5 citable pull quotes)
4. Visualizations (design brief present)

**GROUP 2 — EXAMINE**
5. Scripture (exegetical — not just a reference list)
6. Case Studies (2–4, each with dedicated page at `/pathways/[slug]/case-studies/[case-slug]`)
7. FAQ (6–10 Q&A pairs)

**GROUP 3 — APPLY**
8. Practices (3–5 steps, AfterNote present)
9. Reflection Questions (6–10, distinct from FAQ)

**GROUP 4 — GO DEEPER**
10. Courses (linked, with relevance note)
11. Content (books, articles, podcasts, videos — curated, not exhaustive)
12. Glossary Terms (5–10 terms, linked to full glossary)

**7 Navigable Sections:** Overview → [Named Model] → Case Studies → FAQ → Practices → Courses → Content

---

## Audit Checklist

For each section, check: **Present / Partial / Missing**

### GROUP 1: UNDERSTAND

**Overview**
- [ ] `intro` field exists and is not a stub (< 100 words = stub)
- [ ] Word count: 400–600 words
- [ ] Names the problem/distortion
- [ ] Christocentric framing present
- [ ] `reframe` field present (usual question → better question)
- [ ] Does NOT read as a framework summary

**The Model**
- [ ] `framework` field present
- [ ] `framework.title` is a proper named model (NOT "The Framework", "The Model", or generic)
- [ ] `framework.intro` is 100–200 words
- [ ] At least 4 phases/elements, each with `num`, `title`, `body`
- [ ] Each `body` is 60–100 words (flag if < 30 or > 150)
- [ ] `framework.afterNote` present (realistic expectations)

**Quotes**
- [ ] `quote` field present (or multiple quotes in `extras`)
- [ ] At least 3 distinct quotes (flag if only 1)
- [ ] Each quote is standalone-citable (no dangling context)
- [ ] Source cited where possible

**Visualizations**
- [ ] Visualization description or design brief present (may be in `extras` or comments)
- [ ] *(Flag as missing if nothing — this is a known gap for all pathways)*

### GROUP 2: EXAMINE

**Scripture**
- [ ] `scripture` field present
- [ ] `scripture.refs` lists at least 3 references
- [ ] `scripture.detail` has at least 3 entries, each with `ref` and `text` (not just a word)
- [ ] `scripture.detail[n].text` is exegetical — 30+ words, not just a paraphrase
- [ ] `scripture.history` present (redemptive history note — 80+ words)

**Case Studies**
- [ ] At least one case study present (`caseStudy` field or in `extras`)
- [ ] *(Flag: currently only single `caseStudy` field — multiple needed)*
- [ ] Each case study has: title, lead, at least 3 paragraphs
- [ ] Dedicated page exists: `src/app/(public)/pathways/[slug]/case-studies/[case-slug]/page.tsx`
- [ ] Mix of: biblical + historical OR contemporary (not all from same era)

**FAQ**
- [ ] `qa` field present
- [ ] At least 6 Q&A pairs
- [ ] At least 1 term clarification question (e.g., "X vs. Y?")
- [ ] At least 1 distortion/misapplication question
- [ ] Each answer is 60–150 words
- [ ] Answers are self-contained (no "as mentioned above")
- [ ] Questions read as a real person would ask them (not formal/academic)

### GROUP 3: APPLY

**Practices**
- [ ] `practice` field present
- [ ] At least 3 steps
- [ ] Each step has `label`, `title`, `body`
- [ ] Each `body` is 75–150 words
- [ ] At least one communal or relational practice
- [ ] `practice.afterNote` present with a "First Step" recommendation

**Reflection Questions**
- [ ] Present in `extras` or dedicated field
- [ ] At least 6 questions
- [ ] Distinct from FAQ — these are inward-facing, not clarifying
- [ ] Not yes/no
- [ ] Progressive depth: accessible → challenging
- [ ] *(Flag if missing — this is a new section not yet in most pathways)*

### GROUP 4: GO DEEPER

**Courses**
- [ ] `cta` field present with relevant course link
- [ ] *(Flag if only one course — should list all relevant courses)*

**Content**
- [ ] Books present (at least 3 — check `extras` or `cta`)
- [ ] Articles referenced (at least 2 on-site articles)
- [ ] Podcasts referenced (at least 1 specific episode)
- [ ] Videos referenced (at least 1 specific talk)
- [ ] *(Flag if entirely missing — this is a new section not yet in most pathways)*

**Glossary Terms**
- [ ] At least 5 movemental vocabulary terms identified for this pathway
- [ ] Terms linked to `/pathways/glossary-movemental-language`
- [ ] *(Flag if missing — new section not yet in most pathways)*

---

## Voice Audit

Check for all 5 Alan Hirsch voice markers in prose sections (Overview, Model intro, Practice bodies):

- [ ] Christocentric anchoring — Jesus referenced as Lord, center, or pattern
- [ ] Pastoral warmth — "we" language, invitational phrasing
- [ ] Narrative imagery — organic metaphors, early church references
- [ ] Theological depth — at least one real theological concept engaged
- [ ] Prophetic intensity — at least one reframing question or productive dissonance

**Anti-patterns to flag if present:**
- Corporate consultant language ("leverage," "optimize," "scalable")
- Detached academic hedging ("it could be argued")
- Generic motivation ("you've got this")
- Antithesis patterns ("not X, but Y") — must be additive, not oppositional
- Bullet-point lists used as primary content in prose sections

---

## SEO / GEO Audit

- [ ] `framework.title` is a proper named model (citable by AI engines)
- [ ] FAQ has 6+ standalone-answerable Q&A pairs (FAQPage schema candidate)
- [ ] Overview clearly defines the concept (featured snippet candidate)
- [ ] Scripture section has exegetical depth (E-E-A-T signal)
- [ ] Case studies have dedicated URLs (individually indexable)
- [ ] Quotes are attributed and standalone-citable
- [ ] No section relies on context from another section to make sense

---

## Output Format

Produce a structured audit report with this shape:

```
## Pathway Audit: [Pathway Name] ([slug])

### Summary
Overall status: COMPLETE / NEEDS WORK / STUB
Sections present: X / 12
SEO/GEO ready: YES / PARTIAL / NO

### By Section
| Section | Status | Notes |
|---------|--------|-------|
| Overview | ✅ Complete | 520 words, reframe present |
| The Model | ⚠️ Partial | Good content but named "The Framework" — rename to "The U-Shaped Journey" |
| Quotes | ❌ Missing | Only 1 quote; need 2 more with attribution |
| Visualizations | ❌ Missing | No design brief — new section needed |
| Scripture | ✅ Complete | 4 refs, exegetical depth, history note present |
| Case Studies | ⚠️ Partial | 1 study present; needs 1 more; no dedicated page |
| FAQ | ✅ Complete | 5 Q&A pairs — add 1 more for minimum |
| Practices | ✅ Complete | 5 steps, afterNote present |
| Reflection Questions | ❌ Missing | New section — not yet authored |
| Courses | ⚠️ Partial | CTA links one course; others not listed |
| Content | ❌ Missing | No curated books/articles/podcasts/videos |
| Glossary Terms | ❌ Missing | New section — not yet authored |

### Voice
✅ All 5 markers present
⚠️ Flag: antithesis pattern found in overview ("Not X, but Y")

### SEO / GEO
⚠️ Model not yet named properly — rename for AI citability
✅ FAQ suitable for FAQPage schema
❌ Case study has no dedicated URL

### Priority Actions (ordered)
1. Rename framework.title to "The U-Shaped Journey"
2. Add 2 more quotes with attribution
3. Create dedicated case study page
4. Author Reflection Questions (run /pathway-author [slug] reflection-questions)
5. Author Content section (books/articles/podcasts/videos)
6. Author Glossary Terms section
7. Commission Visualizations design brief
```

If auditing `all`, produce one summary table across all pathways, then a detail section per pathway.

---

## Rules

- Report what exists, not what you think should exist — audit against the canonical spec only
- When a section is "partial," be specific: what's there vs. what's missing
- Priority actions must be in order: structural gaps first, then content quality, then polish
- Never suggest removing content — only adding or improving
- Flag TypeScript type gaps (e.g., single caseStudy vs. needed array) as separate action items
- After auditing, suggest which sections to author first by running `/pathway-author [slug] [section]`
