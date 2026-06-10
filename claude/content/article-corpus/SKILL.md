---
name: article-corpus
description: Look up passages, themes, and arguments from Alan Hirsch's book corpus — both from the local markdown files and the Supabase database. Use when researching what Alan actually says about a topic before writing an article. Returns quoted passages with proper citations.
user-invocable: true
allowed-tools: Read, Grep, Glob, mcp__supabase__execute_sql, mcp__supabase__search_docs
---

Find what Alan Hirsch says about: $ARGUMENTS

$ARGUMENTS should be a topic, concept, keyword, or question (e.g., "APEST", "incarnational mission", "what does Alan say about discipleship in Metanoia"). If none given, list the available corpus and ask what to search.

---

## The Book Corpus

### Local Files

**Root path:** `/Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch/`

**Manifest:** `/Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch_manifest.json`
- Contains all book/chapter metadata: canonical_id, book_slug, chapter_number, chapter_slug, chapter_title, word_count

**File naming convention:** `{book-slug}-ch{N}-{chapter-slug}.md`
- e.g., `5q-ch01-introduction.md`, `reframation-ch03-reframing-apest.md`

**Chapter file format:** Markdown with YAML frontmatter
```yaml
---
canonical_id: alan:5q:ch01
book_slug: 5q
book_title: "5Q: Reactivating the Original Intelligence..."
chapter_number: 1
chapter_slug: introduction
chapter_title: "Introduction"
language: en
tenant_id: alan-hirsch
word_count: 4231
---
[content here]
```

### Available Books (English Corpus)

| Slug | Full Title | Primary Pillar | Chapters | Key Topics |
|------|-----------|----------------|----------|------------|
| `the-forgotten-ways` | The Forgotten Ways: Reactivating Apostolic Movements | Apostolic Genius / mDNA | 19 | mDNA, Apostolic Genius, 6 elements, movement DNA, Chinese underground church |
| `the-forgotten-ways-handbook` | The Forgotten Ways Handbook | Apostolic Genius / mDNA | 11 | mDNA assessment, practical application, organizational change |
| `5q` | 5Q: Reactivating the Original Intelligence and Capacity of the Body of Christ | APEST / 5Q | 17 | Five-fold ministry, APEST gifts, church intelligence, ecclesiology |
| `the-permanent-revolution` | The Permanent Revolution | APEST / 5Q | 20 | APEST as equipping ecology, apostolic ministry, movement leadership |
| `reframation` | Reframation: Seeing God, People, and Mission Through Reframe Eyes | Christology / Lordship | 18 | Theology, image of God, missional imagination, atonement |
| `rejesus` | ReJesus: A Wild Messiah for a Tame Church | Christology / Lordship | 10 | Christology, Jesus-shaped faith, discipleship, lordship |
| `metanoia` | Metanoia: The Ancient Way Forward | Metanoia / Discipleship | 9 | Transformation, conversion, repentance, formation |
| `disciplism` | Disciplism | Metanoia / Discipleship | 7 | Discipleship, mentoring, learning communities |
| `untamed` | Untamed | Metanoia / Discipleship | 14 | Wild gospel, untamed faith, Jesus as wild messiah |
| `on-the-verge` | On the Verge: A Journey Into the Apostolic Future of the Church | Movemental Thinking | 16 | Apostolic imagination, movement dynamics, future church |
| `fast-forward-to-mission` | Fast Forward to Mission | Movemental Thinking | 2 | Mission, movement, apostolic, accelerators |
| `right-here-right-now` | Right Here, Right Now: Everyday Mission for Everyday People | Missional Church | 12 | Incarnational mission, everyday mission, sent life |
| `the-shaping-of-things-to-come` | The Shaping of Things to Come | Missional Church | 16 | Post-Christendom, incarnational church, missional innovation |
| `the-faith-of-leap` | The Faith of Leap | Apostolic Genius / mDNA | 10 | Risk, liminality, communitas, pioneering impulse |

**Translations available:** Spanish (`-es`), Portuguese (`-pt`, `-pt-BR`), German (`-de`), and French (`-fr`) versions of select books.

### Supabase Tables

**Primary tables:**
- `books` — book metadata (slug, title, theological_themes, key_topics)
- `book_chapters` — chapter content (content as HTML, word_count, chapter_number, title)
- `books_chapters` — legacy table (same structure, may also be populated)

**Useful SQL for research:**
```sql
-- Find chapters mentioning a topic
SELECT b.title as book_title, bc.chapter_number, bc.title as chapter_title, bc.excerpt
FROM book_chapters bc
JOIN books b ON bc.book_id = b.id
WHERE bc.content ILIKE '%{search_term}%'
ORDER BY b.title, bc.chapter_number;

-- Get all chapters of a specific book
SELECT chapter_number, title, excerpt, word_count
FROM book_chapters bc
JOIN books b ON bc.book_id = b.id
WHERE b.slug = '{book-slug}'
ORDER BY chapter_number;
```

---

## How to Research a Topic

### Step 1 — Identify Relevant Books and Chapters

Start with the manifest to find chapter titles before reading full content:

```
Grep the manifest for the search term:
Pattern: search term keywords
Path: /Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch_manifest.json
```

Or scan chapter titles across the corpus:
```
Glob: /Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch/**/*.md
Then Grep for the topic within those files
```

### Step 2 — Read Relevant Chapters

Use the file naming pattern to read specific chapters:
```
Read: /Users/joshuashepherd/Desktop/dev/repos/alan-books/corpus/alan_hirsch/{book-slug}/{book-slug}-ch{N}-{chapter-slug}.md
```

For a concept likely spanning multiple books, read the most relevant 2–3 chapters (not every chapter).

### Step 3 — Cross-Reference with Supabase (Optional)

If the local files are insufficient or you need full-text search across all content:
- Use `mcp__supabase__execute_sql` with the SQL patterns above
- Project ID: `vhaiiiykcukrlyvwlgip`

### Step 4 — Extract and Format Passages

From the content found, extract:
- **Direct quotes** — verbatim text worth quoting in an article (2–5 sentences max per quote)
- **Key arguments** — the logical chain Alan builds (paraphraseable)
- **Frameworks/definitions** — crisp definitional passages (GEO-valuable)
- **Stories and examples** — specific historical examples Alan uses in this context

---

## Output Format

Return research findings organized as:

### [Topic] — Corpus Research

**Books consulted:** [list]

---

**[Book Title] — ch[N] "[Chapter Title]"**

*Key passage:*
> [verbatim quote if strong enough, or paraphrase clearly marked]

*Argument summary:* [1–3 sentences on what Alan argues here]

*Relevant to article:* [how this passage supports the article topic]

---

[Repeat for each relevant source]

---

**Synthesis:**
- Across the corpus, Alan's position on [topic] is: [1–2 sentences]
- Strongest quotable passages: [bullet list of the best direct quotes with citation]
- Argument patterns present: [which of Pattern A/B/C from alan-voice this content fits]
- Pillar this primarily belongs to: [one of the six pillars]

---

## Citation Format

Always cite using this format (same as AI Lab):

`**Source:** Book Title — ch[N] "[Chapter Title]"`

For direct quotes: Use blockquote formatting with citation below.

Never invent quotes. If a paraphrase is used, mark it as such: `(paraphrased from ch[N])`.

---

## Pillar-to-Book Mapping (Quick Reference)

Use this to know which books to prioritize for a given pillar:

| Pillar | Primary Books | Secondary |
|--------|--------------|-----------|
| **APEST / 5Q** | 5Q | Reframation, On the Verge |
| **Apostolic Genius / mDNA** | The Forgotten Ways | On the Verge, 5Q |
| **Missional Church** | Right Here Right Now | ReJesus, On the Verge, Fast Forward |
| **Movemental Thinking** | On the Verge, Fast Forward | The Forgotten Ways, 5Q |
| **Metanoia / Discipleship** | Metanoia, Disciplism | ReJesus |
| **Christology / Lordship** | ReJesus, Reframation | Metanoia |
