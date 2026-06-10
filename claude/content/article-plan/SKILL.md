---
name: article-plan
description: Strategically plan a single evergreen article — pillar assignment, keyword targeting, section outline, corpus references, internal link targets, and CTA. Run this before article-author when you want to align on strategy before writing. Use when deciding what to write or how to structure a specific article.
user-invocable: true
allowed-tools: Read, Grep, Glob, mcp__supabase__execute_sql
---

Plan an evergreen article about: $ARGUMENTS

$ARGUMENTS should be a topic, concept, or keyword (e.g., "APEST", "incarnational mission", "what is Apostolic Genius"). If none given, ask what article to plan.

---

## What This Skill Produces

A complete article brief that can be handed directly to `article-author`. It covers:
1. Pillar assignment and article tier
2. Primary keyword + semantic variants
3. Full section outline with H2/H3 structure
4. Target word count
5. Corpus references to pull (which books, which chapters)
6. Internal link targets (pathways, courses, related articles)
7. CTA target
8. Meta title + description
9. URL slug
10. Competitor landscape notes

---

## Step 1 — Assign to a Pillar

Every article lives in exactly one of Alan's six content pillars. Assign based on the primary concept being explored:

| Pillar | Core Question | Flagship Concepts |
|--------|---------------|-------------------|
| **APEST / 5Q** | What gifts does the whole church need? | Five-fold ministry, APEST gifts, church intelligence, 5Q |
| **Apostolic Genius / mDNA** | What makes movements tick? | mDNA, Apostolic Genius, movement DNA, 6 elements |
| **Missional Church** | What does "sent" mean for the church? | Incarnational mission, everyday mission, sentness |
| **Movemental Thinking** | How do movements form and sustain? | Movemental, movements vs. institutions, apostolic future |
| **Metanoia / Discipleship** | What does real conversion demand? | Metanoia, transformation, formation, discipleship |
| **Christology / Lordship** | Who is Jesus and what does his lordship cost? | Christocentric mission, Lordship, Jesus-shaped, ReJesus |

Then assign an article tier:

| Tier | Type | Word Count | Competition |
|------|------|------------|-------------|
| **Tier 1 — Pillar Page** | Broadest term in the pillar | 3,500–4,500 | High |
| **Tier 2 — Cluster Article** | Specific facet within the pillar | 2,200–3,200 | Medium |
| **Tier 3 — Long-tail** | Narrow, high-intent question | 1,500–2,200 | Low |

**Rule:** Each pillar should have exactly one Tier 1 pillar page. Cluster articles link up to it. Long-tail articles link up to cluster articles.

---

## Step 2 — Keyword Strategy

**Primary keyword:** The exact phrase a pastor, leader, or theologian would type into Google or ask an AI.
- Should be 2–5 words
- Should reflect real search intent (informational or definitional)
- Examples: "what is APEST", "apostolic genius meaning", "incarnational mission church"

**Semantic variants (3–5):** Related phrases that should appear naturally in the article body.
- Synonyms, related frameworks, question variants
- Examples for APEST: "five-fold ministry", "Ephesians 4 gifts", "APEST framework", "5Q ministry", "apostolic prophetic evangelistic shepherding teaching"

**GEO-priority terms:** Phrases AI systems are likely to be asked. Include these in the Definition Anchor section specifically.
- Usually the most literal "what is X" form
- Include Alan's name + the concept: "Alan Hirsch APEST", "Alan Hirsch mDNA" — entity disambiguation for AI citation

---

## Step 3 — Section Outline

Generate a complete H2/H3 outline. H2s are the major sections; H3s are sub-facets within them. Headlines should mirror real search queries where possible.

**Mandatory sections (all articles):**

1. **[Opening/Hero]** — No heading. Question, reframe, or tension. Primary keyword in first 100 words.
2. **What Is [Term]?** ← H2 — GEO-optimized definition anchor
3. **Why This Matters / The Problem** ← H2 — stakes, diagnosis, historical parallel
4. **[Core Teaching — 2–3 H2s]** — Main framework content, H3s within each
5. **Common Misunderstandings About [Term]** ← H2 — 2–3 H3s (high GEO value)
6. **[Biblical Foundation]** ← H2 — scripture woven into argument (can merge with core teaching for Tier 3)
7. **What This Means in Practice** ← H2 — application, earned after theology
8. **[How This Connects]** ← H2 — optional for cluster; required for pillar pages
9. **[CTA section]** ← No heading or soft H2 — formation invitation

**For the Core Teaching H2s:** Write them as questions or strong declarative statements that would appear in "People Also Ask" results. Each H2 is a distinct facet of the concept, not just a continuation.

**FAQ section (optional but high GEO value):** 3–5 Q&A pairs at the end. These are what AI systems pull verbatim.

---

## Step 4 — Corpus References

Based on the pillar and topic, identify which books and chapters to pull from. Reference the corpus map:

| Pillar | Primary Books |
|--------|--------------|
| **APEST / 5Q** | 5Q (all chapters) → Reframation, On the Verge |
| **Apostolic Genius / mDNA** | On the Verge, Fast Forward to Mission → 5Q |
| **Missional Church** | Right Here Right Now → ReJesus, On the Verge |
| **Movemental Thinking** | On the Verge, Fast Forward → 5Q |
| **Metanoia / Discipleship** | Metanoia, Disciplism → ReJesus |
| **Christology / Lordship** | ReJesus, Reframation → Metanoia |

List the 3–6 specific chapters most likely to contain what's needed. The `article-corpus` skill will retrieve the actual passages.

---

## Step 5 — Internal Link Targets

Check for existing content to link to. Search:
- `src/app/(public)/` for existing page routes
- Pathways: look for pathway pages related to this pillar
- Courses: look for course slugs in the same pillar
- Related articles: other articles in the same cluster

**Minimum internal links per article:**
- Tier 1 (Pillar Page): 5–8 internal links (to cluster articles, pathways, courses)
- Tier 2 (Cluster): 3–5 internal links (up to pillar page, sideways to related clusters, forward to pathway/course)
- Tier 3 (Long-tail): 3–4 internal links (up to cluster, forward to pathway)

---

## Step 6 — CTA Target

Every article has exactly one primary CTA. Priority order:
1. If a pathway exists for this pillar/topic → link to the pathway (lower friction)
2. If no pathway but a course exists → link to the course
3. If neither → note that a pathway needs to be created before this article publishes

---

## Step 7 — Meta and URL

**URL slug rules:**
- Short, keyword-anchored, no stop words
- Lead with the keyword: `/what-is-apest`, `/apostolic-genius`, `/incarnational-mission`
- All lowercase, hyphens, no underscores
- Max 5 words

**Meta title (50–60 chars):**
- Lead with keyword
- End with `— Alan Hirsch` or `| AlanHirsch.com`
- Example: `What Is APEST? The 5Q Framework — Alan Hirsch`

**Meta description (140–160 chars):**
- Include primary keyword
- Contain a question or tension (drives CTR)
- Preview the value ("Discover how...", "Learn why...", "Explore Alan's...")

---

## Output Format

Return the complete article brief as:

---

# Article Brief: [Working Title]

**Pillar:** [one of the six]
**Tier:** [1 / 2 / 3]
**Primary keyword:** [exact phrase]
**Semantic variants:** [3–5 phrases]
**Target word count:** [range]
**URL slug:** `/[slug]`
**Meta title:** [50–60 chars]
**Meta description:** [140–160 chars]

---

## Section Outline

**[Opening — no heading]**
Reframe or tension: [brief note on the opening approach]

**H2: What Is [Term]?**
Definition anchor — GEO-optimized, ~[word count] words

**H2: [Stakes/Problem heading]**
[Note on approach — Diagnosis/Historical Parallel]
  - H3: [specific sub-point]
  - H3: [specific sub-point]

**H2: [Core Teaching 1]**
[Note on what this covers]
  - H3: [sub-facet]
  - H3: [sub-facet]

**H2: [Core Teaching 2]** (if needed)
  - H3: [sub-facet]

**H2: Common Misunderstandings About [Term]**
  - H3: [Misunderstanding 1]
  - H3: [Misunderstanding 2]
  - H3: [Misunderstanding 3]

**H2: [Biblical Foundation or integrated into core]**

**H2: What This Means in Practice**

**[CTA section]**

**FAQ** (optional, 3–5 Q&A pairs)

---

## Corpus References

*Books to pull from (run article-corpus for passages):*
- [Book slug] — chapters [list]: [reason]
- [Book slug] — chapters [list]: [reason]

---

## Internal Link Targets

- [page/pathway/course title] — `[/route]` — link in [section]
- [page/pathway/course title] — `[/route]` — link in [section]

**CTA target:** [pathway or course name] — `[/route]`

---

## Notes for Writer

[Any strategic notes: tone considerations, angle differentiation from competitors, specific stories to include, known Alan quotes to feature, warnings about what to avoid]
