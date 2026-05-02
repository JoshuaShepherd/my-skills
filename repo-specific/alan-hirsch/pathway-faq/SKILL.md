---
name: pathway-faq
description: Generate FAQ and QA content for an Alan Hirsch pathway page. Produces 6–10 GEO-optimized Q&A pairs grounded in Alan's books, written in his voice, covering common confusions, objections, term clarifications, and distortion warnings. High SEO/GEO value — AI engines cite FAQ pages directly.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Generate FAQ content for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally specific questions to answer or a number of Q&A pairs to produce.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — check if FAQ content already exists
3. Read the pathway's existing articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/articles/`
4. Read existing QA eval sets if available: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/evals/qa-sets/`

---

## Step 2 — Corpus Research

### Book-to-Pathway Map

| Pathway | Primary Books | Key Chapters |
|---------|--------------|--------------|
| **Reframation** | `reframation` | ch01–ch18 (especially ch03 Grey Town, ch07 Great Reframation) |
| **Metanoia** | `metanoia` | ch02 (Metanoi-eh), ch04 (Christo-logic), ch05 (Wholehearted), ch07 (Paradigm) |
| **mDNA** | `the-forgotten-ways`, `the-forgotten-ways-handbook` | TFW ch04–ch09 (six elements), Handbook ch01–ch07 |
| **Movement Intelligence** | `on-the-verge`, `fast-forward-to-mission` | OTV ch01–ch16 |
| **Discipleship** | `untamed`, `disciplism` | Untamed ch01–ch14, Disciplism all |

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

**Research process:**
1. Grep for the pathway's core concepts across primary books
2. Read 3–5 most relevant chapters
3. Extract: definitions, common objections Alan addresses, distinctions he makes, clarifications he offers
4. Note direct quotes with citations: `Book Title — ch[N] "[Chapter Title]"`

Also check content-library articles for existing definitions:
- `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/content/articles/`
- `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/concept-definitions/`

---

## Step 3 — Generate FAQ Content

### Requirements

- **Minimum 6 Q&A pairs**, ideally 8–10
- **FAQPage schema compatible** — each Q&A must be self-contained and quotable
- **GEO-optimized** — these are the highest-value surface for AI citation

### Question Categories (include at least one from each)

1. **Term clarification** (2–3): "What does [term] actually mean?" / "Isn't [term] just another word for [common equivalent]?"
2. **Common objection** (1–2): "Isn't this just [reductive comparison]?" / "How is this different from [related concept]?"
3. **Practical application** (1–2): "How does [concept] work in a small church?" / "What does this look like in practice?"
4. **Distortion warning** (1): "What does [concept] look like when it goes wrong?" — Alan always names the distortion
5. **Framework connection** (1): "How does [concept] connect to [other Alan Hirsch framework]?"
6. **Attribution/origin** (1): "Who developed [framework]?" / "Where does [term] come from?"

### Question Phrasing
- Phrase as a reader would actually ask — natural language, not academic
- Mirror "People Also Ask" patterns from Google
- Include the primary keyword naturally
- Avoid yes/no questions — each should open into explanation

### Answer Structure
- **60–150 words each** — complete enough to stand alone as a cited answer
- Open with a direct answer in the first sentence
- Then expand with Alan's voice: theological depth, historical example, or framework connection
- Close with forward-building implication — never "as mentioned above"
- Include at least one book reference where the concept is developed further

### Answer Ordering
Progress from most common/accessible → deepest/most challenging:
1. Start with "What is…" / "What does… mean?"
2. Then "How is this different from…" / "Isn't this just…"
3. Then practical: "How do you apply…" / "What does this look like…"
4. Then deep: "What about [edge case]…" / "What does it look like when it goes wrong?"

---

## Step 4 — Voice

### Five Markers (all required)

| Marker | Weight | In FAQ Context |
|--------|--------|----------------|
| **Christocentric Anchoring** | 30% | Ground answers in Jesus/Kingdom — even definitional answers should connect to Christ |
| **Prophetic Intensity** | 25% | Calibrated lower in FAQ — clarity over challenge, but still present in distortion/objection answers |
| **Pastoral Warmth** | 20% | "We" language. Invitational. Meet the questioner where they are. |
| **Narrative Imagery** | 15% | One story or metaphor per 2–3 answers — don't overload FAQ format |
| **Theological Depth** | 10% | Brief but substantive. Etymology, historical notes, Scripture woven when it clarifies. |

### Anti-Patterns
- Never "Not X, but Y" — use additive framing
- Never corporate consultant vocabulary
- Never vague: "some scholars suggest…" — be specific
- Never self-referential: "as discussed in the Overview section" — FAQ must stand alone

---

## Output

```
---
pathway: [slug]
section: faq
qa_count: [number]
books_cited: [list]
voice_check: [pass/flag]
---

**Q1: [Question phrased naturally]**
[Answer — 60–150 words, self-contained, GEO-ready]

**Q2: [Question]**
[Answer]

...
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/faq.md`

If FAQ content already exists in the vision doc, flag differences and ask before overwriting.
