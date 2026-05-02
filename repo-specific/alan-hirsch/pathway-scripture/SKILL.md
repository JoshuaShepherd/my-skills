---
name: pathway-scripture
description: Write exegetical Scripture content for Alan Hirsch pathway pages. Produces a primary passage with theological commentary, 3–5 supporting references, and a redemptive history thread — all in Alan's voice. This is theology, not homiletics. Scripture is woven into the argument, grounding the pathway's concepts in biblical reality. Use when writing the Scripture section of any pathway page.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Write Scripture content for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally a specific passage to develop.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — check if Scripture content already exists
3. Read the thematic deep dives: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/thematic-deep-dives/`

---

## Step 2 — How Alan Uses Scripture

Alan Hirsch is **not a proof-texter and not a homilist**. His biblical method is distinctive:

1. **Scripture governs but rarely leads** — it appears mid-argument to ground, illuminate, and deepen, not as an opening proof
2. **Woven, not stacked** — no lists of verses, no "As Paul says in…" openers
3. **Theological interpretation** — he reads Scripture through the lens of Christocentric monotheism, missional theology, and movement dynamics
4. **Historical-linguistic depth** — he uses etymology (Greek, Hebrew), historical context, and early church interpretation
5. **Integrative** — a single passage connects to multiple frameworks (e.g., Ephesians 4 connects APEST, body of Christ, maturity, mission)

### How Alan Treats Key Passages

Search for how Alan himself handles Scripture in his books:
```
Grep: pattern="(Ephesians|Colossians|Acts 15|Mark 1|Romans 12|Genesis 1)" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/" output_mode="content" -C=5
```

---

## Step 3 — Corpus Research

### Pathway-to-Scripture Map (from Alan's books)

| Pathway | Primary Passage | Alan's Key Book Treatment | Supporting Refs |
|---------|----------------|---------------------------|-----------------|
| **Reframation** | John 1:1–3, 14 (the Logos, incarnation, all things made through him) | `reframation` ch07, ch12 | Colossians 1:15–20, Genesis 1:31, Romans 1:19–20, Psalm 24:1 |
| **Metanoia** | Mark 1:14–15 (*Metanoiete* — the Kingdom has come near) | `metanoia` ch02 | Romans 12:1–2, Philippians 2:5–11, 2 Corinthians 3:18, Ezekiel 36:26 |
| **mDNA** | Ephesians 4:1–16 (the APEST gifts, body of Christ, maturity) | `5q` ch02, ch07; `the-forgotten-ways` ch08 | Acts 2:42–47, 1 Corinthians 12, Deuteronomy 6:4–9 (Shema) |
| **Movement Intelligence** | Acts 1:8 / Matthew 28:18–20 (sentness, all authority, go) | `on-the-verge`; `the-forgotten-ways` ch06 | John 20:21, Acts 13:1–3, Mark 4:26–32 (seed parables) |
| **Discipleship** | Matthew 4:19 (Follow me, I will make you…) | `untamed`; `disciplism` | Luke 9:23–24, Matthew 28:19–20, John 15:1–8 (vine and branches) |

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

### Research Process

1. **Read how Alan handles the primary passage** in his books — find the chapter(s) where he develops it
2. **Read his treatment of supporting passages** — how does he connect them?
3. **Note his exegetical moves:**
   - Greek/Hebrew etymology (e.g., *metanoiete*, *apostolos*, *Shema*)
   - Historical context (e.g., what "Jesus is Lord" meant in Caesar's empire)
   - Theological framework connections (e.g., how Ephesians 4 grounds APEST)
4. **Extract his actual exegetical language** — use his phrasing, not generic commentary

---

## Step 4 — Write Scripture Content

### Structure

**Primary Passage** (200–300 words total)
- Full passage text (ESV or NRSV, clearly formatted as blockquote)
- Exegetical commentary (150–250 words):
  - What the passage establishes about this pathway's concept
  - Greek/Hebrew depth where Alan uses it
  - Historical context (what this meant in its original setting)
  - How it connects to the pathway's model (U-Shaped Journey, Seven Reframes, Six Elements, etc.)
  - What it claims about Jesus — Christocentric grounding

**Supporting References** (3–5, each 40–80 words)
- Reference with key phrase quoted
- One sentence of theological context: what this passage adds that the primary passage doesn't
- How Alan uses this passage in his framework

**Redemptive History Thread** (150–250 words)
- How this pathway's concept threads through the biblical narrative: Creation → Fall → Israel → Prophets → Jesus → Church → New Creation
- Not a systematic theology survey — a narrative arc
- Show the continuity: this concept is not a modern invention but a recovery of something that runs through the whole story
- End with eschatological horizon: where is this concept headed in God's purposes?

### Theological Posture

Alan's exegesis is:
- **Christocentric monotheism** — the Shema + the Lordship of Christ held together
- **Missional** — Scripture read through the lens of God's mission, not individual spiritual life
- **Communal** — addressed to communities, not isolated individuals
- **Integrative** — passages connect to each other and to the broader framework
- **Accessible but deep** — not dumbed down, but not inaccessible

### Voice Calibration for Scripture Section

| Marker | Calibration |
|--------|-------------|
| **Christocentric Anchoring** | Highest — this is where Christ is most explicitly present |
| **Theological Depth** | Highest — etymology, historical context, exegetical insight |
| **Pastoral Warmth** | Moderate — reverent, invitational, not preachy |
| **Narrative Imagery** | Lower — precision over metaphor here |
| **Prophetic Intensity** | Moderate — let the text do the challenging |

### Anti-Patterns
- Never proof-text — no "The Bible says X, therefore Y"
- Never stack verses without commentary — each reference earns its place
- Never open with "In this passage, we see…" — that's homiletical
- Never treat Scripture as illustration of a point — it IS the point
- Never ignore how Alan himself handles the passage in his books

---

## Output

```
---
pathway: [slug]
section: scripture
primary_passage: [reference]
supporting_refs: [list]
books_cited: [list — where Alan treats these passages]
---

## Scripture: [Pathway Name]

### [Primary Passage Reference]

> [Full passage text]

[Exegetical commentary — 150–250 words]

### Supporting References

**[Reference 1]** — "[key phrase]"
[40–80 words of theological context]

**[Reference 2]** — "[key phrase]"
[40–80 words]

**[Reference 3]** — "[key phrase]"
[40–80 words]

### Redemptive History

[150–250 words tracing the concept through the biblical narrative]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/scripture.md`
