---
name: pathway-article-gen
description: Generate standalone articles for the Alan Hirsch platform — grounded in pathway themes, written in Alan's voice, with full corpus research, SEO/GEO architecture, and proper citations. Produces Tier 1 pillar articles (3,500–4,500 words), Tier 2 cluster articles (2,200–3,200 words), and Tier 3 long-tail articles (1,500–2,200 words). Each article maps to a pathway pillar and connects to the broader content ecosystem.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Write an article about: $ARGUMENTS

$ARGUMENTS should include the topic and optionally: pathway/pillar, tier (1/2/3), target keyword, or a specific brief to execute.

---

## Step 1 — Strategic Plan

### Assign to a Pathway Pillar

| Pillar | Core Question | Key Concepts | Primary Books |
|--------|---------------|-------------|---------------|
| **Reframation** | How do we see truly again? | Immanent frame, sacred/secular divide, re-enchantment, cosmic Christ | `reframation`, `rejesus` |
| **Metanoia / Transformation** | What does real conversion demand? | Metanoia, U-shaped journey, rival lords, paradigm shift | `metanoia`, `disciplism` |
| **APEST / 5Q** | What gifts does the whole church need? | Fivefold ministry, APEST, Ephesians 4, body intelligence | `5q`, `the-permanent-revolution` |
| **mDNA / Apostolic Genius** | What makes movements tick? | mDNA, six elements, Apostolic Genius, movement DNA | `the-forgotten-ways`, `the-forgotten-ways-handbook`, `on-the-verge` |
| **Missional Church / Movement Intelligence** | What does "sent" mean? | Incarnational mission, sentness, multiplication, organic systems | `on-the-verge`, `fast-forward-to-mission`, `right-here-right-now` |
| **Christology / Lordship** | Who is Jesus and what does his lordship cost? | Jesus Is Lord, Christocentric, ReJesus, Shema | `rejesus`, `the-forgotten-ways` (ch04), `metanoia` (ch04) |

### Assign Tier

- **Tier 1 (Pillar Page):** Broadest term in the pillar → 3,500–4,500 words. One per pillar.
- **Tier 2 (Cluster):** Specific facet of the pillar → 2,200–3,200 words. 3–8 per pillar.
- **Tier 3 (Long-tail):** Narrow, high-intent question → 1,500–2,200 words. Unlimited.

### Establish Keywords
- Primary keyword + 3–5 semantic variants
- Include "Alan Hirsch [concept]" as a GEO disambiguation variant

---

## Step 2 — Corpus Research

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

### Research Process

1. **Glob** to identify chapters by title:
   ```
   Glob: pattern="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/*.md"
   ```

2. **Grep** for the topic keyword across those files:
   ```
   Grep: pattern="[keyword]" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/"
   ```

3. **Read** the 3–6 most relevant chapters in full

4. **Extract:**
   - **Direct quotes** (2–5 sentences, verbatim, blockquote-worthy)
   - **Definitional passages** (crisp enough to be GEO-cited)
   - **Framework explanations** (how Alan builds the concept step by step)
   - **Stories and historical examples**
   - Citation: `Book Title — ch[N] "[Chapter Title]"`

5. **Check existing content** for overlap:
   - Pathway articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[pathway-slug]/articles/`
   - Existing articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/04-articles/`
   - Content-library articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/content/articles/`
   - Concept definitions: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/concept-definitions/`

---

## Step 3 — Write the Article

### Voice (Required — All Five Markers)

Read the full spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`

| Marker | Weight | Target |
|--------|--------|--------|
| **Christocentric Anchoring** | 30% | ≥0.7 — 2–3 explicit Jesus/Christ/Kingdom/Gospel references |
| **Prophetic Intensity** | 25% | 0.5–0.8 — ~3.2 questions per 1000 words |
| **Pastoral Warmth** | 20% | ≥0.5 — "we" (45%), "you" (35%), "I" (20%) |
| **Narrative Imagery** | 15% | ≥0.6 — ~8.5 metaphors per 1000 words |
| **Theological Depth** | 10% | ≥0.7 — 1–2 historical examples per substantial section |

**Rhetorical Posture:** Speaking From Ahead — Alan describes what the reader doesn't yet see as if it's already visible.

**Antithesis prohibition:** Never "not X, but Y." Always additive, forward-building.

**Order of ideas:** Reframe → Meaning → Theological depth → Complexity → Implication. Application is earned, not appended.

### Section Architecture (all mandatory unless noted)

**Section 1: Opening Hook** (150–250 words, no heading)
- Question, reframe, or productive tension — never a standalone scripture quote
- Primary keyword in first 100 words
- Establishes urgency — prophetic, not academic

**Section 2: What Is [Term]?** (200–350 words)
- H2: exact match to primary search query
- GEO anchor — quotable as standalone definition
- Opening definition sentence: crisp, complete, 20–30 words
- GEO disambiguation: "Alan Hirsch developed [term] in [book] as a framework for..."

**Section 3: Why This Matters** (250–400 words)
- Diagnosis section: what the church has lost, reduced, or domesticated
- One historical parallel with specific data
- Transferable principle
- Do NOT rush to solution

**Section 4: Core Teaching** (600–1,200 words, 2–4 H2s)
- Substantive framework content from corpus
- Corpus citations with blockquotes
- Metaphor density: ~8.5 per 1000 words
- Scripture woven where it clarifies

**Section 5: Common Misunderstandings** (300–500 words)
- 2–3 H3s naming and dissolving misconceptions
- "The fuller reality is..." not "Not X, but Y"

**Section 6: Biblical Foundation** (200–350 words)
- 1–2 passages, paraphrased or quoted sparingly
- Argument, not homily

**Section 7: What This Means in Practice** (250–400 words)
- Application earned by everything above
- Direct address: "you" and "we"
- Prophetic challenge woven in

**Section 8: How This Connects** (150–250 words, Tier 1 required)
- Framework ecosystem map
- Internal links to related articles, pathways, courses

**Section 9: Formation Invitation** (100–200 words)
- Warm close — not a sales pitch
- One CTA to pathway or course
- Ends with prophetic challenge or open question

**FAQ Section** (optional, 200–400 words)
- 3–5 Q&A pairs, GEO-optimized

---

## Step 4 — SEO/GEO Check

- [ ] Primary keyword in H1, first 100 words, at least one H2
- [ ] Definition anchor (Section 2) is clean, complete, quotable
- [ ] "Alan Hirsch [concept]" disambiguation present
- [ ] Direct quotes from corpus with citations
- [ ] Meta title: 50–60 chars, keyword-leading
- [ ] Meta description: 140–160 chars, question or tension
- [ ] Internal links: 3–8
- [ ] No antithesis patterns, no consultant vocabulary, no academic detachment

---

## Output

```
---
title: [Full title]
slug: /[url-slug]
pillar: [pillar name]
pathway: [pathway slug]
tier: [1/2/3]
primary_keyword: [keyword]
meta_title: [50-60 chars]
meta_description: [140-160 chars]
word_count: [approximate]
books_cited: [list]
cta_target: [pathway or course slug]
---

[Full article content in markdown]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[pathway-slug]/articles/[slug].md`
