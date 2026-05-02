---
name: pathway-content
description: Master skill for authoring any content type on an Alan Hirsch pathway page. Understands the 12-section architecture, all five pathways, book-to-pathway mapping, Alan's voice system, and where every piece of existing content lives. Use this when writing or auditing any pathway page content — or delegate to a specialized sub-skill (pathway-faq, pathway-quotes, pathway-scripture, etc.) for a single section.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Author pathway content: $ARGUMENTS

$ARGUMENTS should include: pathway slug + section name (e.g., `metanoia faq`, `reframation case-studies`, `mdna all`). If incomplete, ask the user.

**Valid slugs:** `reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`
**Valid sections:** `overview`, `model`, `quotes`, `visualizations`, `scripture`, `case-studies`, `faq`, `practices`, `reflection-questions`, `courses`, `content`, `glossary`, `all`

---

## 1. Before Writing — Load Context

### Read the voice spec
`/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`

### Read existing content for this pathway
- Vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/`
- Articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/articles/`
- Course reaped content: `/Users/joshuashepherd/Desktop/Dev/repos/docs/courses/[slug]/reaped-content/`

### Read primary books for this pathway
Use the Pillar-to-Book Map (§2) to identify the right chapters. Read 3–6 most relevant chapters before writing.

---

## 2. Pillar-to-Book Map

All books live at: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/`
MDX versions at: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/mdx/`

| Pathway | Primary Books (slug) | Key Chapters | Secondary Books |
|---------|---------------------|--------------|-----------------|
| **Reframation** | `reframation` | All 18 chapters — especially ch01 (Moving the Moon), ch03 (Stranded in Grey Town), ch07 (The Great Reframation) | `the-forgotten-ways` (ch04 Jesus is Lord), `rejesus` |
| **Metanoia** | `metanoia` | All 9 chapters — especially ch02 (Metanoi-eh), ch04 (Christo-logic), ch05 (Wholehearted), ch07 (Paradigm), ch08 (Platformed) | `the-forgotten-ways` (ch04), `disciplism` |
| **mDNA** | `the-forgotten-ways`, `the-forgotten-ways-handbook` | TFW ch04–ch09 (the six mDNA elements), Handbook ch01–ch07 | `on-the-verge` (ch04 Apostolic Genius), `5q`, `fast-forward-to-mission` |
| **Movement Intelligence** | `on-the-verge`, `fast-forward-to-mission`, `the-forgotten-ways` | OTV ch01–ch16, TFW ch06 (Missional-Incarnational Impulse), ch09 (Organic Systems) | `the-permanent-revolution`, `5q` |
| **Discipleship** | `untamed`, `disciplism` | Untamed ch01–ch14, Disciplism all | `right-here-right-now`, `rejesus`, `the-forgotten-ways` (ch05 Disciple Making) |

### Christocentric Spine (runs through ALL pathways)
Every pathway is grounded in the confession "Jesus is Lord." The spine includes: allegiance to King Jesus, gospel fullness (cross + resurrection + Kingdom + Spirit), obedience, communal formation, sentness. See: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/_shared/christocentric-spine/PORTAL_MAP_AND_CHRISTOCENTRIC_SPINE.md`

### Cross-cutting book chapters for Christocentric content:
- `the-forgotten-ways` ch04 — "The Heart of It All: Jesus Is Lord"
- `rejesus` ch05 — "The Shema Schema"
- `metanoia` ch04 — "Christo-logic"
- `disciplism` ch06 — "It's All About Jesus"

---

## 3. Canonical 12-Section Architecture

Every pathway page follows this structure. All sections must stand alone as sidebar nav anchors.

**GROUP 1 — UNDERSTAND**
1. **Overview** (400–600 words) — The invitation. Felt problem → concept → what's been lost → core reframe question
2. **The Model** (named per pathway) — The intellectual framework with phases/elements (4–8 items, 60–100 words each)
3. **Quotes** (3–5) — Citable pull quotes from Alan's actual books. Definitional + prophetic + pastoral mix
4. **Visualizations** — Design briefs for diagrams illustrating the pathway's core model

**GROUP 2 — EXAMINE**
5. **Scripture** — Primary passage with exegesis + 3–5 supporting refs + redemptive history thread
6. **Case Studies** (2–4) — Cards linking to dedicated pages. Biblical + historical + contemporary mix
7. **FAQ** (6–10 Q&A) — GEO-optimized. Common confusions, objections, term clarifications

**GROUP 3 — APPLY**
8. **Practices** (3–5 steps) — Concrete, sequential, doable. Individual + communal + leadership mix
9. **Reflection Questions** (6–10) — Inward-facing, open-ended, personal/communal/missional

**GROUP 4 — GO DEEPER**
10. **Courses** — Platform courses that develop this pathway theme
11. **Content** — Curated books, articles, podcasts, videos (3–5 each)
12. **Glossary Terms** (5–10) — Movemental vocabulary central to this pathway

### Model Names (never say "Framework"):
| Pathway | Model Name |
|---------|-----------|
| Metanoia | The U-Shaped Journey |
| mDNA | The Six mDNA Elements |
| Reframation | The Seven Reframes |
| Movement Intelligence | Movement Dynamics |
| Discipleship | Life-on-Life Multiplication |

---

## 4. Alan Hirsch Voice (Required in Every Section)

### Five Voice Markers

| Marker | Weight | What It Looks Like |
|--------|--------|--------------------|
| **Christocentric Anchoring** | 30% | 2–3 explicit Jesus/Christ/Kingdom/Gospel references. Everything grounded in Jesus. |
| **Prophetic Intensity** | 25% | Challenging language, urgency, reframing questions. ~3.2 questions per 1000 words. |
| **Pastoral Warmth** | 20% | Direct address: 45% "we", 35% "you", 20% "I". Relational, invitational. |
| **Narrative Imagery** | 15% | ~8.5 metaphors per 1000 words. Movement/DNA, organic, journey metaphors. |
| **Theological Depth** | 10% | Historical examples (~4.8 per 1000 words), biblical integration woven not proof-texted. |

### Rhetorical Posture: Speaking From Ahead
Alan describes what the reader doesn't yet see as if it's already visible. He does not say "imagine if…" — he says "here's what I've seen."

### Argument Patterns
- **Pattern A:** Reframe → Ground in historical example → Extract principle → Connect to framework → Land prophetically
- **Pattern B:** Story → Tension → Scripture woven → Resolution → Application
- **Pattern C:** Diagnosis → Historical Parallel → Recovery → Vision

### Anti-Patterns (NEVER use)
- Antithesis: "Not X, but Y" — always additive, forward-building
- Corporate consultant: "leverage," "optimize," "best practices"
- Detached academic: "It could be argued that…"
- Rushing to practice before understanding
- Homiletical openings: leading with a Scripture quote
- Generic motivational language

### Signature Stories (use with authentic detail)
- Early church: 25,000 → 20 million (AD 100–310), no buildings, no hierarchy, under persecution
- Chinese underground church: 2M → 120M in 60 years under same conditions
- SMRC: South Melbourne Restoration Community, 1983–1998, inner-city Melbourne
- George and John: Greek brothers, drug dealers → faith → George in prison → 50+ to faith in 6 months

---

## 5. Research Process

Before writing any section:

1. **Grep** for the topic keyword across the primary books:
   ```
   Grep: pattern="[keyword]" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/"
   ```
2. **Read** the 3–6 most relevant chapters in full
3. **Extract:**
   - Direct quotes (verbatim, 2–5 sentences)
   - Definitional passages (GEO-quotable)
   - Framework explanations
   - Stories and historical examples
4. **Cite:** `Book Title — ch[N] "[Chapter Title]"`

Also check existing pathway content for consistency:
- Vision docs: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/`
- Research: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/`
- Reviews: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/content/reviews/`

---

## 6. Output

Write content as markdown. Include:

```
---
pathway: [slug]
section: [section name]
word_count: [approximate]
books_cited: [list of book slugs used]
voice_check: [pass/flag — note any markers below target]
---

[Content]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/[section-name].md`

If writing a full pathway (`all`), produce all 12 sections in order. For individual sections, delegate to the appropriate specialized skill if one exists:
- FAQ → `pathway-faq`
- Quotes → `pathway-quotes`
- Scripture → `pathway-scripture`
- Case Studies → `pathway-case-study`
- Overview → `pathway-overview`
- Glossary → `pathway-glossary`
- Visualizations → `pathway-visualization`
- Articles (standalone) → `pathway-article-gen`

---

## Rules

- Never invent quotes. If paraphrasing, mark it as such.
- Always read existing pathway content first — coherence across sections matters.
- The Core Question reframe (usual question → better question) goes in the Overview, displayed prominently.
- Case study model names must use the real model name — "The U-Shaped Journey" not "this process."
- FAQ answers must be self-contained — no "as mentioned above."
- Application sections (Practices, Reflection Questions) come AFTER understanding sections. Application is earned.
- The Christocentric spine runs through everything. If a section has no Jesus reference, it's incomplete.
