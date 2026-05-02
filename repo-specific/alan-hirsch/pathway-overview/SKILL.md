---
name: pathway-overview
description: Write or rewrite the Overview section for an Alan Hirsch pathway page — the 400–600 word thematic summary that serves as the invitation to enter. Combines corpus research, Alan's voice, and the pathway's core reframe question. This is the first content users read below the hero and core question — it must be the best prose on the page.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Write the Overview for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally a focus angle or audience.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — understand what already exists
3. Read existing pathway articles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/articles/`
4. Read the concept definition if available: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/concept-definitions/`
5. Read the thematic deep dive if available: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/thematic-deep-dives/`

---

## Step 2 — Corpus Research

### Book-to-Pathway Map

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

| Pathway | Primary Books | Key Chapters for Overview |
|---------|--------------|--------------------------|
| **Reframation** | `reframation` | ch01 (Moving the Moon), ch03 (Stranded in Grey Town) — the felt problem and invitation |
| **Metanoia** | `metanoia` | ch01 (Apocalypse of the Ecclesial Soul), ch02 (Metanoi-eh) — diagnosis and definition |
| **mDNA** | `the-forgotten-ways` | ch01 (A View from the Edge), ch03 (Preparing for the Journey) — the case for mDNA |
| **Movement Intelligence** | `on-the-verge` | ch01–ch03 — the apostolic future and why it matters |
| **Discipleship** | `untamed` | ch01–ch03 — what discipleship has become vs. what Jesus intended |

### Research Process
1. Read the opening 2–3 chapters of the primary book — the Overview mirrors how Alan himself introduces the concept
2. Extract: the core problem he names, the definition he builds, the invitation he extends
3. Note any signature stories or historical examples he uses in the introduction
4. Find the passage where he articulates the "usual question vs. better question" reframe

---

## Step 3 — Write the Overview

### Specifications

- **Length:** 400–600 words
- **Target:** The best single piece of prose on the pathway page
- **Function:** This is the invitation to enter — not a summary of the framework, not a table of contents

### Structure (organic, not rigid)

1. **Open with the felt problem** (50–80 words)
   - Name what is wrong, broken, or lost — without despair
   - Use Alan's diagnostic language: "eclipse," "amnesia," "reduction," "domestication," "taming"
   - Prophetic intensity here — urgency without panic

2. **Define the concept** (80–120 words)
   - What this pathway names and recovers
   - Etymology or linguistic depth where Alan uses it (e.g., *meta* + *noia*, *reframation* as portmanteau)
   - How it sits within Alan's broader framework map

3. **Christocentric grounding** (80–120 words)
   - How does Jesus embody, inaugurate, or demonstrate this concept?
   - What did Jesus model that the church has lost or reduced?
   - Scripture woven, not proof-texted

4. **What has been lost in Western Christianity** (60–100 words)
   - The historical drift — how did we get here?
   - One concrete historical example (early church, Chinese underground church, etc.)

5. **The Core Question Reframe** (40–60 words)
   - This is the thesis of the entire pathway
   - Format: *Usual question:* [How the church typically frames it] → *Better question:* [How Alan reframes it]
   - This should be visually distinct — it's the hook that earns the scroll

### Voice Calibration for Overview

The Overview is Alan at his most invitational. All five markers present, but calibrated:

| Marker | Calibration |
|--------|-------------|
| **Christocentric Anchoring** | High — Jesus must appear in the grounding section |
| **Prophetic Intensity** | High in opening (diagnosis), moderate in middle, warm in close |
| **Pastoral Warmth** | High throughout — this is an invitation, not a lecture |
| **Narrative Imagery** | 2–3 strong metaphors. One historical example. |
| **Theological Depth** | Moderate — accessible but not shallow. Save deepest theology for the Model section. |

### Rhetorical Posture
- Speaking From Ahead: Alan has already been where the reader is going
- Opens with the problem the reader feels, then reframes it
- Does NOT use antithesis ("Not X, but Y") — builds forward
- Ends with the Core Question, which creates productive dissonance that earns the scroll to the Model section below

---

## Step 4 — Quality Check

Before delivering, verify:

- [ ] 400–600 words
- [ ] Opens with felt problem, not definition
- [ ] Definition appears after the problem is named
- [ ] Jesus/Christ referenced explicitly at least twice
- [ ] At least one historical example with specific data
- [ ] Core Question Reframe present and clearly formatted
- [ ] No antithesis patterns
- [ ] No corporate consultant or detached academic language
- [ ] Would a pastor read this aloud to their congregation? (Readability test)
- [ ] Does it make the reader want to scroll to the Model section? (Engagement test)

---

## Output

```
---
pathway: [slug]
section: overview
word_count: [actual count]
books_cited: [list]
voice_check: pass
---

[Overview prose — 400–600 words]

**The Core Question**
*Usual question:* [How the church typically frames it]
*Better question:* [How Alan reframes it]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/overview.md`
