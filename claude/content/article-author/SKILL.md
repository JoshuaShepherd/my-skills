---
name: article-author
description: Write a complete evergreen pillar article in Alan Hirsch's voice — with corpus research from his books, full SEO/GEO architecture, and proper citations. This is the main writing skill. It runs planning, corpus research, and writing in sequence. Use when writing any new article for the platform.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, mcp__supabase__execute_sql
---

Write an evergreen article about: $ARGUMENTS

$ARGUMENTS should include the topic and optionally: pillar, tier (1/2/3), target keyword, style variant, or an existing article-plan brief to execute. If a brief is provided, skip to Step 3. If only a topic is given, run the full flow.

---

## Step 1 — Strategic Plan

Before writing, establish the brief. If an `article-plan` brief was provided in $ARGUMENTS, use it directly and skip to Step 3.

Otherwise, run the planning logic from `article-plan`:

**Assign pillar** (one of six):

| Pillar | Core Q | Key Concepts |
|--------|--------|-------------|
| **APEST / 5Q** | What gifts does the whole church need? | Five-fold ministry, APEST gifts, 5Q, Ephesians 4 |
| **Apostolic Genius / mDNA** | What makes movements tick? | mDNA, Apostolic Genius, 6 elements, movement DNA |
| **Missional Church** | What does "sent" mean? | Incarnational mission, sentness, everyday mission |
| **Movemental Thinking** | How do movements form? | Movemental, apostolic future, movement dynamics |
| **Metanoia / Discipleship** | What does real conversion demand? | Metanoia, transformation, formation, discipleship |
| **Christology / Lordship** | Who is Jesus and what does his lordship cost? | Christocentric, ReJesus, Jesus-shaped, Lordship |

**Assign tier:**
- Tier 1 (Pillar Page): Broadest term in the pillar → 3,500–4,500 words
- Tier 2 (Cluster): Specific facet → 2,200–3,200 words
- Tier 3 (Long-tail): Narrow, high-intent → 1,500–2,200 words

**Establish keywords:** Primary keyword + 3–5 semantic variants. Include "Alan Hirsch [concept]" as a GEO disambiguation variant.

**Draft the outline** using the section architecture in Step 3.

---

## Step 2 — Corpus Research

Before writing, pull relevant passages from Alan's books. This grounds the article in his actual words and enables proper citations.

### Local corpus path:
`/Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch/`

### Pillar-to-book map:

| Pillar | Primary Books | Secondary |
|--------|--------------|-----------|
| **APEST / 5Q** | `5q` | `reframation`, `on-the-verge` |
| **Apostolic Genius / mDNA** | `the-forgotten-ways` | `on-the-verge`, `5q` |
| **Missional Church** | `right-here-right-now` | `rejesus`, `on-the-verge`, `fast-forward-to-mission` |
| **Movemental Thinking** | `on-the-verge`, `fast-forward-to-mission` | `the-forgotten-ways`, `5q` |
| **Metanoia / Discipleship** | `metanoia`, `disciplism` | `rejesus` |
| **Christology / Lordship** | `rejesus`, `reframation` | `metanoia` |

### Research process:
1. Use the manifest to identify the most relevant chapter titles before reading full content:
   - Glob: `/Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch/**/*.md`
   - Grep for the topic keyword across those files
2. Read the 3–6 most relevant chapters in full (not every chapter — be selective)
3. Extract:
   - **Direct quotes** (2–5 sentences; verbatim; strong enough to blockquote)
   - **Definitional passages** (crisp enough to be GEO-quoted)
   - **Framework explanations** (how Alan explains the concept step by step)
   - **Stories and historical examples** he uses in context
4. Note the citation for each: `Book Title — ch[N] "[Chapter Title]"`

**If Supabase has richer content** (run a search if local files seem incomplete):
```sql
SELECT b.title, bc.chapter_number, bc.title as ch_title,
       LEFT(bc.content, 500) as excerpt
FROM book_chapters bc
JOIN books b ON bc.book_id = b.id
WHERE bc.content ILIKE '%{keyword}%'
ORDER BY b.title, bc.chapter_number
LIMIT 20;
```
Project ID: `vhaiiiykcukrlyvwlgip`

**Citation format:** `**Source:** Book Title — ch[N] "[Chapter Title]"`
Never invent quotes. If paraphrasing, mark it as such.

---

## Step 3 — Write the Article

Write the complete article in markdown following this exact section architecture. All sections are mandatory unless marked optional.

### Alan's Voice (Apply to Every Section)

All five markers required — same as the `alan-voice` skill:

| Marker | Weight | Target |
|--------|--------|--------|
| **Christocentric Anchoring** | 30% | ≥0.7 — 2–3 explicit Jesus/Christ/Kingdom/Gospel references |
| **Pastoral Warmth** | 20% | ≥0.5 — "we" (45%), "you" (35%), "I" (20%) |
| **Narrative Imagery** | 15% | ≥0.6 — ~8.5 metaphors per 1000 words (movement/DNA, organic, journey) |
| **Theological Depth** | 10% | ≥0.7 — 1–2 historical examples per substantial section |
| **Prophetic Intensity** | 25% | 0.5–0.8 — ~3.2 questions per 1000 words |

**Rhetorical posture:** Speaking From Ahead — Alan describes what the reader doesn't yet see as if it's already visible. Not "imagine if…" but "here's what I've seen."

**Antithesis prohibition:** Never "not X, but Y." Always additive, forward-building, integrative.

**Order of ideas:** Reframe → Meaning → Theological depth → Complexity → Implication. Application is earned, not appended.

---

### Section 1: Opening Hook (150–250 words, no heading)

- Opens with a **question, reframe, or productive tension** — never a standalone scripture quote, never a thesis statement
- Primary keyword appears naturally within the first 100 words
- Establishes why this matters NOW — prophetic urgency, not academic framing
- Alan's posture: he's already been where the reader is going. Speak from there.
- No antithesis patterns
- Sets up the Definition Anchor naturally ("So what exactly is…" or a reframe that demands definition)

---

### Section 2: What Is [Term]? (200–350 words)
**H2: "What Is [Term]?"** — exact match to primary search query

This is the **GEO anchor section**. Write it to be quotable as a standalone — AI systems will pull this paragraph.

Structure:
- **Opening definition sentence:** Crisp, complete, 20–30 words. "APEST is [X]." Not vague.
- **Expand the definition:** 3–4 sentences unpacking what the definition means and why it's richer than it sounds
- **Situate in Alan's framework map:** 2–3 sentences connecting it to the broader ecosystem (mDNA, APEST, Metanoia, etc.)
- **GEO disambiguation line:** "Alan Hirsch coined/developed [term] in [book/year] as a framework for..." — helps AI attribute correctly

Tone: Definitional precision + Alan's pastoral register. More clarity here, less prophetic intensity — that comes later.

If the term has components (like APEST = 5 gifts, or mDNA = 6 elements), name them here but don't define each yet — that's Core Teaching.

---

### Section 3: Why This Matters — The Problem (250–400 words)
**H2:** Question or declarative that names the stakes (e.g., "Why the Church Can't Afford to Ignore This", "What We've Lost — and Why It Matters")

This is the **Diagnosis section**. Uses Pattern C opening: name what the church has lost, reduced, or domesticated.

- Use one of Alan's diagnostic terms: "eclipse," "amnesia," "reduction," "domestication," "taming"
- Follow immediately with a **historical parallel** — the early church, Chinese underground church, Methodist movement, or SMRC — with specific data, not vague generalities
- Draw the transferable principle from the historical example
- Close with the implication: this is not an academic problem, it's a lived reality

Do NOT rush to solution here. Sit with the problem. Application is earned later.

Historical examples to use (with specificity):
- Early church: grew from ~25,000 to 20 million between AD 100–310, with no buildings, no centralized hierarchy, under active persecution
- Chinese underground church: grew from 2 million to 120 million in 60 years under the same conditions
- SMRC: South Melbourne Restoration Community, 1983–1998, inner-city Melbourne, marginalized communities
- Methodist movement, CMA, Pentecostal revivals — with specific data where available

---

### Section 4: Core Teaching (600–1,200 words, 2–4 H2s with H3s inside)

The substantive framework content. This is where Alan's corpus is most heavily drawn upon.

**Structural rule:** Each H2 is a distinct facet of the concept — not "Part 1, Part 2" but genuinely different angles. H3s are sub-points within each.

**Headline rule:** H2s should mirror questions people actually ask. Imagine the "People Also Ask" box for your primary keyword.

**Pattern to use:**
- **Pattern A:** Reframe → Ground in historical example → Extract principle → Connect to framework → Land prophetically
- **Pattern B:** Story → Tension → Scripture woven → Theological resolution → Application preview
- Choose the pattern that fits; patterns can nest across the H2s

**Corpus citations:** This is where pulled passages go. Use blockquotes for direct quotes:
> "Verbatim Alan quote..." — *Book Title*, ch[N] "[Chapter Title]"

For paraphrases, close-reference: `(Drawing from *Book Title*, ch[N])`

**Metaphor density:** Actively embed — movement/DNA, organic/biological, journey/travel. ~8.5 per 1000 words target.

**Scripture:** Woven where it clarifies, not where it proves. No stacked quotations. No "As Paul says in..." sermon openings.

**If the concept has enumerable components** (APEST = 5 gifts; mDNA = 6 elements): define each within H3s, but make them feel like a developing argument, not a glossary. Use transitional sentences that build forward.

---

### Section 5: Common Misunderstandings (300–500 words)
**H2: "Common Misunderstandings About [Term]"** or "What [Term] Is NOT" (exception to antithesis rule — this section names the misconception *in order to dissolve it*)

2–3 H3s, each one:
- Names the misunderstanding directly (readers recognize themselves)
- Opens into the fuller, richer understanding ("The fuller reality is...")
- Alan's first-person: "I've encountered this confusion again and again..."

**Why this section matters:** Highest GEO value after the Definition Anchor. AI systems pull disambiguation content. Featured snippet territory for Google.

Do not use antithesis *structure* even here — name the misunderstanding, then expand the reality. Don't say "not X, but Y." Say "X tends to flatten into [reduction]. The fuller reality is [expansion]."

---

### Section 6: Biblical Foundation (200–350 words)
**H2:** Something theological and specific (e.g., "The Ephesians 4 Architecture", "What Jesus Modeled in His Mission")

- 1–2 scripture passages — paraphrased or quoted sparingly, introduced because they clarify, not prove
- Brief theological insight connecting the passage to the concept
- Historical or linguistic note where relevant (Alan loves etymology and early church interpretation)
- No sermon-like structure. No "In [verse], we read that..." This is argument, not homily.

*This section can be integrated into Core Teaching for Tier 3 articles where length requires it.*

---

### Section 7: What This Means in Practice (250–400 words)
**H2:** Something actionable but not prescriptive (e.g., "What This Opens Up for Your Church", "Living Into the [Term]")

- Application is **earned here** — this section is paid for by everything above it
- Direct address: "you" and "we" — second person deliberately
- Not a list of steps. Prose with embedded implications.
- Prophetic challenge woven in: "What would it mean if your community took this seriously?"
- Practical enough to be actionable; expansive enough to feel like vision

---

### Section 8: How This Connects (150–250 words) — Required for Tier 1, optional for Tier 2/3
**H2:** "How [Term] Connects to [Related Framework/Concept]"

- Shows where this concept sits in Alan's broader framework ecosystem
- 2–3 internal links with natural anchor text to related articles, pathways, courses
- "If this resonated, the natural next layer is..." — invitational forward movement

---

### Section 9: Formation Invitation / CTA (100–200 words, no heading or soft H2)

- Warm, invitational close — not a sales pitch
- "If you want to go deeper with this..." → link to pathway or course (one CTA only)
- Ends with a **prophetic challenge or open question** — leaves productive tension
- Christocentric where natural — ground the invitation in Jesus's mission, not personal growth

---

### FAQ Section (Optional — High GEO Value, 200–400 words)

If included, place at the very end. 3–5 Q&A pairs.

Format:
**Q: [Question people actually ask — exact phrasing]**
A: [2–5 sentence answer in Alan's voice — complete and self-contained, GEO-ready]

Best FAQ questions:
- "What does [term] mean in the Bible?"
- "What is the difference between [term] and [related term]?"
- "How do you apply [term] in a small church?"
- "Who developed the [term] framework?"
- "What is Alan Hirsch's view on [topic]?"

---

## Step 4 — SEO/GEO Final Check

Before delivering, verify:

**SEO:**
- [ ] Primary keyword in: H1 (article title), first 100 words, at least one H2, meta title, meta description
- [ ] 3–5 semantic variants woven naturally (not stuffed)
- [ ] H2/H3 headlines mirror search intent questions
- [ ] Internal links: minimum 3 (to related articles/pathways/courses), maximum 8
- [ ] Meta title: 50–60 chars, leads with keyword, ends with `— Alan Hirsch`
- [ ] Meta description: 140–160 chars, includes keyword, contains question/tension
- [ ] URL slug: short, keyword-anchored, no stop words, all lowercase with hyphens

**GEO:**
- [ ] Definition Anchor (Section 2) is clean, complete, and quotable as a standalone
- [ ] "Alan Hirsch [concept]" disambiguation phrase present
- [ ] Factual specificity in historical examples (numbers, dates, locations — not vague)
- [ ] Direct quotes from corpus present with citations
- [ ] FAQ section included (or note that it should be added before publishing)
- [ ] Author byline references Alan Hirsch and Forge Mission Training Network

**Voice:**
- [ ] All five markers present (run against alan-voice pre-output checklist)
- [ ] No antithesis patterns
- [ ] No corporate consultant vocabulary
- [ ] No detached academic phrasing
- [ ] Application appears after meaning and theology (Section 7, not before Section 4)
- [ ] First-person narrative present (minimum 2 instances)
- [ ] Christocentric anchoring in opening, core teaching, and close
- [ ] Ends with prophetic challenge or open question
- [ ] Overall voice coherence ≥0.75

---

## Output Format

Deliver the article as:

```
---
title: [Full article title]
slug: /[url-slug]
pillar: [pillar name]
tier: [1/2/3]
primary_keyword: [keyword]
meta_title: [50-60 chars]
meta_description: [140-160 chars]
word_count: [approximate]
books_cited: [list of book slugs used]
cta_target: [pathway or course slug]
---

[Full article content in markdown]
```

If saving to a file: `content-library/articles/[slug].md`

Always ask before writing to a file if the destination is unclear.
