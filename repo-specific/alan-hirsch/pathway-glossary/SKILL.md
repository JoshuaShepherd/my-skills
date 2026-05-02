---
name: pathway-glossary
description: Generate glossary terms for an Alan Hirsch pathway page. Produces 5–10 movemental vocabulary definitions drawn from Alan's books, using his language, linked to the full glossary. These are the terms a reader needs to inhabit this pathway — not a dictionary, but a language school.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Generate glossary terms for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally specific terms to define.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/`
3. Read existing concept definitions: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/concept-definitions/`
4. Read the pathway's primary books (see Book Map below)

---

## Step 2 — Book-to-Pathway Map

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

| Pathway | Primary Books | Where Terms Are Defined |
|---------|--------------|------------------------|
| **Reframation** | `reframation` | ch01–ch18 — immanent frame, reframation, sacred/secular divide, buffered self, porous self, re-enchantment |
| **Metanoia** | `metanoia` | ch02–ch08 — metanoia, poenitentia, U-shaped journey, wicked problem, elegant solution, Christo-logic, rival lords |
| **mDNA** | `the-forgotten-ways`, `the-forgotten-ways-handbook` | TFW ch04–ch09 — Apostolic Genius, mDNA, six elements, communitas, liminality, organic systems |
| **Movement Intelligence** | `on-the-verge`, `fast-forward-to-mission`, `the-forgotten-ways` | sentness, incarnational mission, exponential multiplication, reproducible patterns |
| **Discipleship** | `untamed`, `disciplism` | disciple-making, everyday mission, life-on-life, untamed discipleship, formation |

**Cross-cutting terms** (relevant to all pathways): APEST, Apostolic Genius, mDNA, Christocentric, missional, movemental, formation

---

## Step 3 — Research Process

1. **Identify candidate terms** — Grep the primary books for terms unique to or essential for this pathway
2. **Read Alan's own definitions** — Find the passages where he introduces, defines, or explains each term
3. **Check existing concept definitions** at `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/concept-definitions/`
4. **Prioritize:** Terms that are (a) coined or distinctively used by Alan, (b) essential to understanding this pathway, (c) likely to confuse a newcomer

---

## Step 4 — Generate Glossary

### Requirements

- **5–10 terms** per pathway
- **Ordered** from most foundational → most specialized
- **Alan's language** — use his actual definitions where possible, with citation

### Term Structure

For each term:

**[Term Name]**
Definition: 1–3 sentences in Alan's voice — precise, warm, grounded. Not a dictionary definition but a movemental one. What does this term open up?
Source: `Book Title — ch[N]` (where Alan defines or develops the term)

### Expected Terms by Pathway

**Reframation:** Reframation, Immanent Frame, Sacred/Secular Divide, Re-enchantment, Buffered Self, Porous Self, Plausibility Structure, Cosmic Christ, Public Truth
**Metanoia:** Metanoia, Poenitentia, U-Shaped Journey, Wicked Problem, Elegant Solution, Christo-logic, Rival Lords, Soft Eyes, Corporate Lament, Paradigm
**mDNA:** mDNA (Missional DNA), Apostolic Genius, Jesus Is Lord, Disciple Making, Missional-Incarnational Impulse, APEST Culture, Organic Systems, Communitas, Liminality
**Movement Intelligence:** Sentness, Incarnational Mission, Exponential Multiplication, Reproducible Patterns, Simple Systems, Movement Dynamics, Adaptive Challenge, Red Ocean/Blue Ocean
**Discipleship:** Discipleship, Disciple-Making, Everyday Mission, Formation, Untamed, Life-on-Life, Apprenticeship, Missional Discipleship

---

## Step 5 — Voice

Glossary definitions are precision-pastoral. More definitional clarity than prophetic intensity, but still warm and grounded.

| Marker | In Glossary Context |
|--------|-------------------|
| **Christocentric Anchoring** | Connect terms to Jesus/Kingdom where natural — don't force it on every term |
| **Pastoral Warmth** | These are invitations into a language, not entries in an encyclopedia |
| **Theological Depth** | Etymology, original language (Greek, Hebrew), historical context where it enriches |
| **Narrative Imagery** | One metaphor or story reference per 2–3 definitions |
| **Prophetic Intensity** | Low — save for the overview, not the glossary |

### Anti-Patterns
- Never "Not X, but Y"
- Never generic dictionary definitions — use Alan's actual framing
- Never define a term without connecting it to the pathway's logic

---

## Output

```
---
pathway: [slug]
section: glossary
term_count: [number]
books_cited: [list]
---

## Glossary: [Pathway Name]

**[Term 1]**
[Definition — 1–3 sentences in Alan's voice]
*Source: Book Title — ch[N]*

**[Term 2]**
[Definition]
*Source: Book Title — ch[N]*

...
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/glossary.md`
