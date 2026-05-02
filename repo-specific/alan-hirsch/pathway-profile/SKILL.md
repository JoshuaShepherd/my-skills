---
name: pathway-profile
description: Research and write profiles of people and stories for Alan Hirsch pathway pages. Produces leader profiles, movement founder stories, and biographical narratives drawn from Alan's books and research — people who embody the pathway's principles. Use for the Content and Case Study sections, or for standalone biographical content.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Research and write a profile for: $ARGUMENTS

$ARGUMENTS should include a person's name or a pathway slug + "profiles" (e.g., `Wesley`, `Bonhoeffer`, `metanoia profiles`, `mdna leader-profiles`). Optionally specify how the profile connects to a pathway.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read existing leader profiles: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/case-studies/` (includes leader profiles for Wesley, St. Patrick, etc.)
3. Read the story index: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/story-index/`
4. Read Alan's own biographical material: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/biography.md`
5. If the person is from one of Alan's books, read the relevant chapters

---

## Step 2 — People Alan Writes About

### In His Books (searchable at `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/`)

**Biblical Figures:**
- Jesus (throughout — especially `rejesus`, `metanoia` ch04)
- Paul/Saul (movement dynamics, `the-forgotten-ways`, `on-the-verge`)
- Peter (Jerusalem Council, `metanoia`)
- James (Jerusalem Council, `metanoia`)

**Historical Movement Leaders:**
- John Wesley (Methodist movement — `the-forgotten-ways`, `on-the-verge`)
- St. Patrick (Celtic mission — `reframation`, `the-forgotten-ways`)
- Columba / Aidan (Celtic missionaries — `reframation`)
- William Booth (Salvation Army — `the-forgotten-ways`)
- Count Zinzendorf (Moravians — `on-the-verge`)
- Karl Barth / Dietrich Bonhoeffer (Barmen Declaration — `metanoia`)
- Lesslie Newbigin (missional theology — `reframation`, `right-here-right-now`)
- Roland Allen (missionary methods — `the-forgotten-ways`)

**Theologians/Thinkers Alan Engages:**
- Abraham Kuyper ("every square inch" — `reframation`)
- Charles Taylor (immanent frame — `reframation`)
- Gerard Manley Hopkins ("charged with grandeur" — `reframation`)
- Peter Senge (learning organizations — `metanoia`)
- Howard Snyder (church renewal — `the-forgotten-ways`)

**Contemporary Figures:**
- Pat Kavanagh (The Main House — `untamed`)
- George and John (Greek brothers — `untamed`, `the-forgotten-ways`)
- Brad Brisco (co-author, missional practitioner)

### Research Process

1. **Grep the person's name across all books:**
   ```
   Grep: pattern="[name]" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/" output_mode="content" -C=5
   ```

2. **Read the chapters where they appear** — understand how Alan frames their story

3. **Extract:**
   - What Alan highlights about them (what details does he choose?)
   - How he connects their story to his framework
   - What principle or pattern they illustrate
   - Any direct quotes from or about them

---

## Step 3 — Write the Profile

### Profile Structure

1. **Opening Hook** (50–80 words)
   - A single vivid moment, decision, or image that captures who this person is
   - Not a biographical summary — a narrative entry point

2. **Who They Were / Are** (100–150 words)
   - Context: time, place, situation, challenge they faced
   - What they did that matters for this pathway
   - Specific details: numbers, dates, outcomes where available

3. **What Alan Sees in Them** (150–200 words)
   - How does Alan frame this person's significance?
   - Which of his frameworks does their story illuminate?
   - What principle do they embody?
   - Use Alan's own words where possible (with citation)

4. **The Transferable Insight** (80–120 words)
   - What does this story open up for the reader?
   - How does it connect to the pathway's core thesis?
   - Invitation, not prescription — "what if we…"

### Voice for Profiles

Profiles are narrative + theological. Calibrate:

| Marker | Calibration |
|--------|-------------|
| **Christocentric Anchoring** | Show how this person's story connects to Jesus's own pattern |
| **Narrative Imagery** | Highest — vivid, concrete, specific. This is storytelling. |
| **Pastoral Warmth** | High — honor the person, care for the reader |
| **Theological Depth** | Moderate — woven into narrative, not separate section |
| **Prophetic Intensity** | In the Transferable Insight section, not the biography |

### Anti-Patterns
- Never hagiography — Alan is honest about complexity and failure
- Never reduce a person to a lesson — they are human beings first
- Never invent biographical details not found in Alan's books or documented sources
- Never separate the story from the theology — they are one

---

## Output

```
---
pathway: [slug] (if pathway-specific)
section: profile
subject: [person's name]
books_cited: [list]
---

## [Person's Name]: [Subtitle — role/significance in 5 words]

[Opening hook — 50–80 words]

[Who they were/are — 100–150 words]

[What Alan sees in them — 150–200 words]

**The Insight:** [Transferable insight — 80–120 words]

*Sources: [Book citations]*
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/profiles/[person-slug].md` or `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/core-content/case-studies/leader-profile-[person-slug].md`
