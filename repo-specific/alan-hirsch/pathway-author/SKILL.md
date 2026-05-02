---
name: pathway-author
description: Write or update content for a pathway page — any single section or a full pathway. Follows the canonical 12-section architecture, Alan Hirsch's voice, and SEO/GEO best practices. Use when writing new pathways, filling missing sections, or improving existing content.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Author pathway content: $ARGUMENTS

$ARGUMENTS should include: pathway slug and section name (e.g., `metanoia overview` or `metanoia all`). If incomplete, ask the user.

Valid slugs: `reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`
Valid sections: `overview`, `model`, `quotes`, `visualizations`, `scripture`, `case-studies`, `faq`, `practices`, `reflection-questions`, `courses`, `content`, `glossary`, `all`

## Before Starting

1. Read `src/lib/content/pathways/types.ts` — the TypeScript interfaces for all pathway fields
2. Read the existing pathway file: `src/lib/content/pathways/[slug].ts` — understand what already exists before writing
3. Read a complete pathway for voice reference: `src/lib/content/pathways/metanoia.ts`
4. Read `src/lib/config/tenant.config.ts` for canonical pathway metadata (themes, titles)
5. If writing case studies, check: `src/lib/content/pathways/case-studies/[slug]/` if it exists
6. For content/courses sections, check what exists in the database or use known Alan Hirsch catalog

Never overwrite existing content without flagging it first.

---

## Canonical Page Architecture

Every pathway page has 12 content sections organized in 4 groups. The sidebar TOC surfaces 7 of these as primary navigable anchors. Write with this structure in mind — each section must stand alone as an anchor destination.

**GROUP 1 — UNDERSTAND** (reading mode)
1. Overview
2. The Model *(named specifically per pathway — never "Framework")*
3. Quotes
4. Visualizations

**GROUP 2 — EXAMINE** (reading + scanning mode)
5. Scripture
6. Case Studies *(cards on page; each links to dedicated page)*
7. FAQ

**GROUP 3 — APPLY** (action mode)
8. Practices
9. Reflection Questions

**GROUP 4 — GO DEEPER** (card/media scanning mode)
10. Courses
11. Content *(books, articles, podcasts, videos)*
12. Glossary Terms

**7 Primary Nav Items (sidebar TOC):**
Overview → [Named Model] → Case Studies → FAQ → Practices → Courses → Content

---

## Section Specifications

### 1. Overview (400–600 words)

Alan's best prose on what this concept is and why it matters. This is the invitation to enter — not a summary of the framework.

- Open with the felt problem or the question this pathway answers
- Define the concept precisely — what it is, what it is NOT
- Christocentric framing: how does Jesus embody or inaugurate this?
- Name what has been lost or distorted in Western Christianity
- End with the core reframe: usual question → better question
- Tone: pastoral, prophetic, invitational — not academic

Maps to: `intro` + `reframe` fields in the TypeScript type

### 2. The Model

The named intellectual framework. The nav label uses the actual model name — never "Framework."

| Pathway | Model Name |
|---------|-----------|
| Metanoia | The U-Shaped Journey |
| mDNA / mDNA | The Six mDNA Elements |
| Reframation | The Seven Dimensions |
| Movement Intelligence | Movement Dynamics |
| Discipleship | Life-on-Life Multiplication |

Structure:
- **Title**: the model's proper name
- **Intro** (100–200 words): explain the shape/logic — why this model, where it came from
- **Phases or Elements** (4–8): each needs `num`, `title`, `body` (60–100 words)
  - Titles should be single evocative words or short phrases (e.g., "Unravel", "Unlock")
  - Bodies: concrete, specific, no padding
- **AfterNote** (50–100 words): realistic expectations — timeline, caveats, common mistakes

Maps to: `framework` field

### 3. Quotes (3–5 quotes)

Citable pull quotes from Alan's actual books and talks. These are the sentences AI engines will cite verbatim.

- Each: 1–3 sentences maximum
- Cite source if known (book title, chapter, or talk)
- Mix: one definitional, one provocative/prophetic, one pastoral
- Must be quotable standalone — no dependent context needed

Maps to: `quote` field (currently single; flag if multiple needed)

### 4. Visualizations

Written as a design brief — describe the diagram(s) that would illustrate this pathway for a designer or asset-generate skill.

- Type: flow diagram / cycle / matrix / exploded view / timeline
- Key elements and their relationships
- What the visualization should communicate at a glance
- Any existing Alan Hirsch diagrams this is based on (cite if known)

Maps to: notes for design handoff; not currently in the TypeScript type — add as comment or `extras` field

### 5. Scripture (exegetical)

Not a list of proof texts. An exegetical look at how Scripture illuminates and grounds this pathway.

- **Primary passage**: full text (not just reference) + 100–150 word exegetical note
- **Supporting refs** (3–5): reference + one sentence of context each
- **Redemptive history** (100–200 words): how this concept threads through OT and NT
- **Historical note**: key moments in church history where this concept was at stake

Maps to: `scripture` field

### 6. Case Studies (2–4 studies)

Multiple case studies, not one. They appear as editorial cards on the pathway page; each card links to a dedicated page.

**Card content (for the pathway page):**
- Title (e.g., "The Jerusalem Council, Acts 15")
- Context: time/place/situation (one sentence)
- Hook: 2–3 sentence narrative summary that creates desire to read more

**Full case study content (for the dedicated page at `/pathways/[slug]/case-studies/[case-slug]`):**
- Lead paragraph: the problem or moment
- Narrative body (3–5 paragraphs): downcurve, turning point, upcurve — or equivalent for the pathway
- Implications: what this case study reveals about the pathway's principles
- Return link back to pathway

Mix of: biblical (Acts, prophets), historical (Reformation, early church movements), contemporary (movements from Alan's research)

Maps to: `caseStudy` field (currently single) → flag that array is needed; write as array

### 7. FAQ (6–10 Q&A pairs)

Common confusions, objections, and term clarifications. These are GEO's highest-value surface — AI engines cite FAQ pages directly.

- Order: easiest/most common → deepest/most challenging
- Questions: phrased as a reader would actually ask them — not "What is X?" but "Isn't this just the same as Y?"
- Answers: 60–150 words each — complete enough to stand alone
- At least 2 term clarifications (e.g., metanoia vs. repentance)
- At least 1 that addresses a common misapplication or distortion

Maps to: `qa` field

### 8. Practices (3–5 practices)

How to begin. Concrete, sequential, doable in a real church or life context.

- Each step: `label` ("Step 1"), `title` (evocative name), `body` (75–150 words)
- Mix: individual, communal, leadership
- At least one practice that requires another person
- **AfterNote**: a "First Step" — the single most important entry point, with a concrete action

Maps to: `practice` field

### 9. Reflection Questions (6–10 questions)

Distinct from FAQ (which answers common questions externally). These turn inward — toward the reader's own life, community, and calling.

- Not rhetorical — genuinely open-ended
- Not yes/no
- Mix: personal application, communal discernment, missional imagination
- Progress from accessible → challenging
- Formatted as numbered list

Maps to: new field — add to `extras` or propose TypeScript extension

### 10. Courses

Which of Alan's platform courses most directly develops this pathway theme?

For each course:
- Title, slug, and 1–2 sentence description of relevance to this pathway
- How it deepens what the pathway introduces

Map to: `cta` field (currently) + proposed `courses` array extension

### 11. Content (curated)

The 3–5 most essential entry points for each content type. Editorial, not exhaustive.

**Books** (3–5): title, author, 1-sentence description of why this book for this pathway
**Articles** (3–5): on-site articles tagged to this theme, with slug
**Podcasts** (2–3): specific episodes, not just show — title, host, 1-sentence hook
**Videos** (2–3): specific talks, not playlists — title, context, 1-sentence hook

Maps to: new `content` array — propose TypeScript extension

### 12. Glossary Terms

The 5–10 movemental vocabulary terms most central to this pathway. Brief definitions, linked to the full glossary page.

- Term name
- 1–2 sentence definition (Alan's own language where possible)
- Link: `/pathways/glossary-movemental-language#[term-slug]`

Maps to: new `glossaryTerms` array — propose TypeScript extension

---

## Voice: Alan Hirsch

Write as Alan Hirsch. All five markers must be present in every section:

1. **Christocentric anchoring** — Jesus is Lord. Every framework points back to Jesus. Allegiance, obedience, sentness.
2. **Pastoral warmth** — "We" language. Invitational, not prescriptive. "I wonder if..." not "You must..."
3. **Narrative imagery** — Organic metaphors: movement, journey, seeds, fire, rivers. Early church stories. Chinese underground church.
4. **Theological depth** — Grounded in Scripture and tradition. Engages with real theological concepts.
5. **Prophetic intensity** — Reframing questions. Productive dissonance. Calls to risk and obedience. "What if the church has been..."

### Voice Anti-Patterns (NEVER use)
- Corporate consultant tone ("leverage," "optimize," "best practices," "scalable")
- Detached academic voice ("It could be argued that..." "Research suggests...")
- Antithesis patterns ("Not X, but Y") — use additive, forward-building language
- Bullet-point lists as primary content in prose sections (use flowing prose with embedded structure)
- Generic motivational language ("You've got this!")

---

## Output Format

Write content as a TypeScript object matching the `PathwayContent` interface from `src/lib/content/pathways/types.ts`.

If adding a section that has no existing TypeScript field (Reflection Questions, Content, Glossary Terms), output:
1. The content in markdown for immediate use
2. A proposed TypeScript interface extension to add to `types.ts`
3. A note flagging the type change needed

Save to: `src/lib/content/pathways/[slug].ts` — update only the section(s) being authored.

---

## Rules

- Never use placeholder text — every word should be real, usable content grounded in Alan's actual frameworks
- Always read existing content first — coherence across sections matters
- Case study model names must use the real model name — "The U-Shaped Journey" not "this process"
- Quotes must be attributable to Alan's actual corpus — do not invent quotations
- FAQ answers must be self-contained — no "as mentioned above"
- If a TypeScript type extension is needed, propose it but do not modify `types.ts` without confirming
- The named model (section 2) nav label must match the actual model name in the content
