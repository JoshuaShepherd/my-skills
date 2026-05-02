---
name: pathway-quotes
description: Find, verify, and curate quotes from Alan Hirsch's books for pathway pages. Conducts corpus research across all 13 books, extracts verbatim passages, verifies attribution, and produces 3–5 citable pull quotes per pathway — definitional, prophetic, and pastoral. These are the sentences AI engines will cite verbatim.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Find and curate quotes for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally a specific theme or concept to find quotes about.

---

## Step 1 — Load Context

1. Read the voice spec: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/profile/voice-system/ALAN_HIRSCH_VOICE_AND_STYLE_PROMPT.md`
2. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — check if quotes already exist (many have unverified quotes flagged for source verification)
3. Read the existing quotable lines collection: `/Users/joshuashepherd/Desktop/Dev/repos/docs/intelligence/leader-research/alan-hirsch/content/reviews/_quotable-lines.md`
4. Read the portal quotes collection: `/Users/joshuashepherd/Desktop/Dev/repos/docs/knowledge/QUINTESSENTIAL_QUOTES_BY_PORTAL.md`

---

## Step 2 — Book-to-Pathway Map

Books path: `/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/`

| Pathway | Primary Books to Search | Secondary |
|---------|------------------------|-----------|
| **Reframation** | `reframation` (ch01–ch18) | `the-forgotten-ways` (ch04), `rejesus` |
| **Metanoia** | `metanoia` (ch01–ch09) | `the-forgotten-ways` (ch04), `disciplism` |
| **mDNA** | `the-forgotten-ways` (ch04–ch09), `the-forgotten-ways-handbook` | `on-the-verge` (ch04), `5q` |
| **Movement Intelligence** | `on-the-verge`, `fast-forward-to-mission`, `the-forgotten-ways` | `the-permanent-revolution` |
| **Discipleship** | `untamed`, `disciplism` | `right-here-right-now`, `rejesus` |

---

## Step 3 — Corpus Research

This is the core of this skill. Be thorough.

### Search Strategy

1. **Grep across all primary book chapters** for the pathway's core concepts:
   ```
   Grep: pattern="[concept keyword]" path="/Users/joshuashepherd/Desktop/Dev/repos/docs/books/english/[book-slug]/" output_mode="content" -C=3
   ```

2. **Read the most promising chapters in full** — quotes live in context. A great quote often comes in the middle of a developing argument, not at chapter beginnings.

3. **Look for these quote types:**
   - **Definitional:** Alan's most precise, crisp articulation of a concept. These are GEO gold — AI engines quote these verbatim. Look for sentences that begin with the concept name and define it.
   - **Prophetic/challenging:** Alan naming what the church has lost, calling to recover it. These have urgency, edge, and vision. Look for passages with exclamation, strong verbs, or direct challenge.
   - **Pastoral/invitational:** Alan speaking with warmth to the reader about what becomes possible. Look for "we" language, invitation, vision of the future.
   - **Narrative:** Alan telling a story that crystallizes the concept. Short enough to quote (2–3 sentences max).

4. **Extract verbatim** — copy the exact words. Do not paraphrase, reconstruct, or "improve" Alan's language.

5. **Record the citation:** `Book Title — ch[N] "[Chapter Title]"`

### Quality Criteria for a Quotable Passage

A great pathway quote must:
- Stand alone without surrounding context
- Be 1–3 sentences (ideally under 50 words for cards, up to 80 for featured quotes)
- Be distinctively Alan — not generic theological language
- Serve the pathway's core thesis
- Be actually quotable — rhythm, memorability, precision

---

## Step 4 — Verify and Curate

### For each candidate quote:

1. **Verify it is verbatim** — re-read the source passage to confirm exact wording
2. **Check if it's already used** — search existing pathway vision docs and articles
3. **Categorize:** definitional / prophetic / pastoral / narrative
4. **Rate quotability** (1–5): Is this something a pastor would put on a slide? Would an AI engine cite it as authoritative?

### Select 3–5 quotes per pathway

**Required mix:**
- At least 1 definitional (crisp concept definition)
- At least 1 prophetic/challenging (calling the church forward)
- At least 1 pastoral/invitational (warmth, vision, hope)

**If existing quotes in the vision doc are flagged as "unverified" or "reconstructed":**
- Search the books for the actual source
- If found verbatim: update with verified citation
- If not found: flag as "attributed but not verified in indexed corpus" and provide the closest actual passage found
- If the quote appears to be reconstructed (not in any book): replace it with a verified quote on the same theme

---

## Step 5 — Output

```
---
pathway: [slug]
section: quotes
quote_count: [number]
books_searched: [list of all books searched]
verification_status: [all verified / partially verified — note which need further verification]
---

## Quotes: [Pathway Name]

**Quote 1** *(definitional)*
"[Verbatim quote from Alan's book]"
— Alan Hirsch, *[Book Title]*, ch[N] "[Chapter Title]"
**Verification:** ✅ Verified verbatim from source

**Quote 2** *(prophetic)*
"[Verbatim quote]"
— Alan Hirsch, *[Book Title]*, ch[N] "[Chapter Title]"
**Verification:** ✅ Verified verbatim from source

**Quote 3** *(pastoral)*
"[Verbatim quote]"
— Alan Hirsch, *[Book Title]*, ch[N] "[Chapter Title]"
**Verification:** ✅ Verified verbatim from source

### Additional Candidates (not selected but notable)

**[Quote]** — *[Book Title]*, ch[N]
Reason not selected: [too long / overlaps with Quote 2 / etc.]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/quotes.md`

---

## Rules

- **Never invent, reconstruct, or "improve" quotes.** Every quote must be verifiable in the indexed books.
- If a vision doc has quotes marked "verify in Metanoia book" — this skill's job is to do that verification.
- Paraphrases are acceptable as supplementary material but must be clearly marked as paraphrases with "(paraphrase)" label.
- Always provide the full citation path so future editors can re-verify.
- If a concept has no strong quotable passage in the books, say so honestly rather than fabricating one.
