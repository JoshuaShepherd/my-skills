---
name: review-scrape
description: Scrape book reviews from Goodreads and Amazon — fetches actual review text, ratings, dates, and reviewer metadata. Organizes by book, extracts quotable lines, analyzes sentiment patterns, and outputs structured markdown for copy strategy and social proof.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__new_page, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__wait_for, mcp__chrome-devtools__click, mcp__chrome-devtools__press_key
---

Scrape book reviews for: $ARGUMENTS

$ARGUMENTS should be one of:
- An author name (e.g. `"Alan Hirsch"`) — scrapes reviews for all discoverable books
- `--book "The Forgotten Ways"` to scrape reviews for a single book
- `--isbn 978-0801072826` or `--asin B01N0SYZPZ` to target a specific edition
- `--goodreads-url https://www.goodreads.com/book/show/12345` to scrape a specific Goodreads page
- `--editorial-only` to skip reader reviews and only collect professional/editorial reviews
- `--refresh` to re-scrape books that already have review files (updates stats, adds new reviews)
- `--max-reviews N` to limit reader reviews per book (default: 100)
- Empty — ask the user for the author name

## Before Starting

1. Confirm browser tools are available (`mcp__chrome-devtools`) — required for scraping review pages
2. Check `content-library/reviews/` for any existing review files for this author
3. Read `src/lib/database/schema.ts` for the `books` table definition — use `isbn`, `asin`, `title`, `slug` to match books
4. Read existing research in `_docs/` or `movemental-ai/_docs/movement_leader_research/` for any prior review summaries to build on
5. If existing review files are found, load them and run in **incremental mode** — add new reviews, update stats, don't overwrite existing data

## Pipeline Stages

### Stage 1 — Discover Books

1. **Database lookup**: Query the `books` table for all books by the author (match by `author_id` or author name in tenant config)
2. **Goodreads search**: Navigate to `https://www.goodreads.com/search?q={author+name}` and extract book listings
3. **Amazon search**: Search `https://www.amazon.com/s?k={author+name}&i=stripbooks` and extract book listings
4. **Cross-reference**: Match discovered books with DB records by ISBN/ASIN/title
5. **Build book manifest**: For each book, record:
   - `title`, `isbn`, `asin`, `goodreads_url`, `amazon_url`, `goodreads_id`
   - `publication_year`, `publisher`, `co_authors`

### Stage 2 — Scrape Goodreads Reviews

For each book in the manifest:

#### 2a — Book Stats Page
1. Navigate to the Goodreads book page (e.g. `https://www.goodreads.com/book/show/{id}`)
2. Extract aggregate stats:
   - **Average rating** (e.g. 4.08)
   - **Total ratings count** (e.g. 1,581)
   - **Total reviews count** (e.g. 96)
   - **Rating distribution** (count per star: 5★, 4★, 3★, 2★, 1★)
3. Extract the book's Goodreads genre tags / shelves (e.g. "theology", "church", "missional")

#### 2b — Individual Reviews
1. Navigate to the reviews page, sorted by **most popular** first
2. For each review visible on the page, extract:
   - `reviewer_name` — display name
   - `reviewer_url` — profile link (for verification, not storage)
   - `rating` — star count (1–5), or null if no rating
   - `date` — review date
   - `text` — full review text (expand "...more" if truncated)
   - `likes` — number of likes/helpful votes
3. Paginate through reviews:
   - Click "next page" or scroll to load more
   - Stop when you reach `--max-reviews` (default 100) or run out of pages
   - Prioritize: most-liked reviews first, then most recent
4. **Important**: If Goodreads blocks or rate-limits, wait 3–5 seconds between page loads. If blocked entirely, log a warning and continue to Amazon.

#### 2c — Goodreads "Community Reviews" Breakdown
If available, extract the "Community Reviews" breakdown:
- Filter by rating to get representative reviews at each star level
- Aim for at least 2–3 reviews per star level to understand the full sentiment spectrum

### Stage 3 — Scrape Amazon Reviews

For each book in the manifest:

#### 3a — Product Page Stats
1. Navigate to the Amazon product page using ASIN or ISBN search
2. Extract:
   - **Average rating** (e.g. 4.6)
   - **Total ratings count**
   - **Rating distribution** (percentage per star)
   - **"Top reviews"** section

#### 3b — Individual Reviews
1. Navigate to the full reviews page (`/product-reviews/{ASIN}`)
2. Sort by **Top reviews** (most helpful first)
3. For each review, extract:
   - `reviewer_name`
   - `rating` — star count
   - `date`
   - `title` — review headline
   - `text` — full review body
   - `helpful_votes` — "X people found this helpful"
   - `verified_purchase` — boolean
   - `vine_review` — boolean (Amazon Vine program)
4. Paginate until `--max-reviews` or exhausted
5. Then sort by **Most recent** and grab the 10 most recent reviews (to capture current sentiment)

#### 3c — Amazon "Most helpful" Reviews
Specifically flag the top 3 positive and top 3 critical reviews that Amazon highlights — these are the most-read reviews and carry outsized influence.

### Stage 4 — Scrape Editorial/Professional Reviews

Search for published reviews from blogs, journals, and publications:

1. **Web search queries** (per book):
   - `"{book title}" "alan hirsch" book review`
   - `"{book title}" review site:thegospelcoalition.org OR site:patheos.com OR site:christianitytoday.com`
   - `"{book title}" review site:englewoodreview.org OR site:9marks.org OR site:lifeandleadership.com`
   - `"{book title}" review missional OR church OR movement`
2. For each editorial review found, extract:
   - `publication` — outlet name
   - `reviewer_name` — author of the review
   - `date` — publication date
   - `url` — direct link
   - `sentiment` — Positive / Mixed / Critical
   - `key_quote` — the single most representative sentence (for use in marketing)
   - `full_text` — if accessible (don't scrape paywalled content — note as `[paywalled]`)

### Stage 5 — Analyze & Extract

Process all collected reviews to produce actionable intelligence:

#### 5a — Sentiment Analysis
For each book, categorize reviews into themes:

**Praise themes** — What do people love? Group by recurring pattern:
- e.g. "paradigm-shifting", "practical frameworks", "scholarly yet accessible"
- Count how many reviews mention each theme
- Extract the 3 best-written review quotes for each praise theme

**Criticism themes** — What do people criticize? Group by recurring pattern:
- e.g. "repetitive", "too academic", "weak on application"
- Count how many reviews mention each criticism
- Extract the most articulate critical quotes (useful for addressing objections)

**Surprise themes** — What unexpected reactions appear?
- e.g. "changed my ministry", "read it three times", "assigned in seminary"

#### 5b — Quotable Lines
Extract the **20 most quotable review excerpts** across all books, ranked by:
1. Specificity (names a concept, not just "great book")
2. Emotional resonance (would make someone want to read the book)
3. Credibility signal (verified purchase, known reviewer, high helpful votes)
4. Brevity (1–3 sentences max)

Tag each quote with:
- `use_case` — where this quote could appear on the platform:
  - `hero` — powerful enough for the home page
  - `book-detail` — relevant to a specific book page
  - `social-proof` — general credibility signal
  - `course-conversion` — speaks to transformation/formation
  - `ai-lab-trust` — speaks to depth of Alan's work
  - `newsletter` — could entice email subscription
  - `social-media` — shareable as a standalone post

#### 5c — Reader Language Map
Analyze HOW readers describe Alan and his work in their own words. Extract:
- The 10 most common adjectives readers use
- The 5 most common verbs (what does Alan's work DO to people?)
- The 3 most common comparisons ("like X but Y", "reminds me of Z")
- Terms readers use that Alan himself doesn't use (market language gaps)
- The emotional arc: what did they feel before, during, and after reading?

This map is gold for copy — it tells you how to speak about Alan in the language his audience already uses.

#### 5d — Objection Map
From negative and mixed reviews, build an objection map:
- What concerns do people have BEFORE reading? (addressed in marketing copy)
- What frustrates people DURING reading? (addressed in content strategy)
- What do people wish was different AFTER reading? (addressed in course/platform design)

### Stage 6 — Output

Save results to `content-library/reviews/{author-slug}/` with these files:

#### Per-book files:
```
content-library/reviews/alan-hirsch/
├── _manifest.json              # Book list with URLs, ISBNs, stats
├── the-forgotten-ways.md       # All reviews + analysis for this book
├── the-shaping-of-things.md
├── 5q.md
├── the-permanent-revolution.md
├── rejesus.md
├── [other-books].md
├── _editorial-reviews.md       # All editorial/professional reviews across books
├── _quotable-lines.md          # Top 20 quotes ranked by use case
├── _reader-language-map.md     # How readers talk about Alan
├── _objection-map.md           # Criticism themes + how to address them
└── _sentiment-summary.md       # Cross-book sentiment dashboard
```

#### Per-book markdown format:

```markdown
# Reviews: {Book Title}

**Last scraped**: {date}
**Goodreads**: {rating} avg · {count} ratings · {review_count} reviews
**Amazon**: {rating} avg · {count} ratings

## Rating Distribution

| Stars | Goodreads | Amazon |
|-------|-----------|--------|
| 5★    | {n} ({%}) | {n} ({%}) |
| 4★    | {n} ({%}) | {n} ({%}) |
| 3★    | {n} ({%}) | {n} ({%}) |
| 2★    | {n} ({%}) | {n} ({%}) |
| 1★    | {n} ({%}) | {n} ({%}) |

## Praise Themes

### {Theme 1} — mentioned in {n} reviews
{Summary of what reviewers say}

> "{Best quote}" — {reviewer}, {platform}, {rating}★

> "{Second best quote}" — {reviewer}, {platform}, {rating}★

### {Theme 2} — mentioned in {n} reviews
...

## Criticism Themes

### {Theme 1} — mentioned in {n} reviews
{Summary}

> "{Representative quote}" — {reviewer}, {platform}, {rating}★

## Most Helpful Reviews

### ★★★★★ — {title}
**{reviewer}** · {platform} · {date} · {helpful_votes} helpful
{full text}

### ★★★★ — {title}
...

### ★★★ — {title}
...

### ★★ — {title}
...

### ★ — {title}
...

## All Scraped Reviews

<details>
<summary>{n} reviews collected</summary>

| # | Platform | Rating | Date | Reviewer | Helpful | Title |
|---|----------|--------|------|----------|---------|-------|
| 1 | Goodreads | 5 | 2024-01-15 | Jane D. | 42 | "Changed my ministry" |
...

### Review 1
**{title}** · {rating}★ · {reviewer} · {platform} · {date}
{full text}

### Review 2
...

</details>
```

#### _quotable-lines.md format:

```markdown
# Quotable Review Lines — Alan Hirsch

**Last updated**: {date}
**Total quotes extracted**: 20

## Hero-Grade (strongest for home page / marketing)

> "{quote}" — {reviewer}, reviewing *{book}* ({platform}, {rating}★, {helpful} helpful)
**Use cases**: hero, social-proof
**Why it works**: {1-sentence explanation}

> ...

## Book-Specific (for detail pages)

### The Forgotten Ways
> "{quote}" — ...

### 5Q
> "{quote}" — ...

## Transformation / Formation (for course pages)
> "{quote}" — ...

## Social Media Ready (standalone shareable)
> "{quote}" — ...
```

#### _reader-language-map.md format:

```markdown
# Reader Language Map — Alan Hirsch

**Source**: {n} reviews across {m} books

## How Readers Describe Alan
**Most common adjectives**: {list with counts}
**Most common verbs (what his work does)**: {list}
**Comparisons readers make**: {list}

## Language Gaps
Terms readers use that Alan/the platform doesn't:
- "{term}" — used by {n} reviewers, appears {0} times on platform

## Emotional Arc
**Before reading**: {what readers expected or felt}
**During reading**: {what the experience was like}
**After reading**: {how they describe the impact}

## Copy Implications
{3-5 sentences on how this language map should inform platform copy}
```

## Key Design Rules

- **Idempotent** — Safe to re-run. New reviews are appended, stats are updated, existing reviews are not duplicated (match by reviewer + date + first 50 chars of text)
- **Rate-limit respectful** — 3–5 second delays between page loads on Goodreads/Amazon. If blocked, stop and report progress.
- **No login required** — Only scrape publicly visible reviews. Do not attempt to log in to Goodreads or Amazon.
- **Attribution preserved** — Every quote includes reviewer name, platform, date, and rating. Never fabricate or alter review text.
- **Privacy-conscious** — Store reviewer display names only, not profile URLs or identifying information beyond what's publicly displayed
- **Graceful degradation** — If one platform blocks, continue with the other. If a book isn't found, skip and report.
- **Prioritize quality over quantity** — 50 well-chosen, high-signal reviews per book are more valuable than 500 scraped indiscriminately

## Output Report

Print a summary after completion:

```
## Review Scrape Report: {Author Name}

### Books Processed: {n}

| Book | Goodreads | Amazon | Editorial | Total |
|------|-----------|--------|-----------|-------|
| The Forgotten Ways | 4.08 (87 reviews) | 4.6 (45 reviews) | 8 | 140 |
| ... | ... | ... | ... | ... |

### Stage 1 — Discovery: OK
- Books in DB: {n}
- Books on Goodreads: {n}
- Books on Amazon: {n}
- Matched: {n}

### Stage 2 — Goodreads: OK / PARTIAL / BLOCKED
- Reviews scraped: {n} across {m} books
- Blocked on: [list any books where scraping failed]

### Stage 3 — Amazon: OK / PARTIAL / BLOCKED
- Reviews scraped: {n} across {m} books

### Stage 4 — Editorial: OK
- Editorial reviews found: {n} across {m} publications

### Stage 5 — Analysis: OK
- Praise themes identified: {n}
- Criticism themes identified: {n}
- Quotable lines extracted: {n}

### Output
- Files written to: content-library/reviews/{author-slug}/
- Total files: {n}

### Warnings
- [any non-blocking issues, rate limiting, missing books, etc.]

### Next Steps
1. Review `_quotable-lines.md` for copy-ready social proof
2. Review `_reader-language-map.md` to inform platform copy voice
3. Review `_objection-map.md` to address concerns in marketing
4. Use quotes in `/copy-strategy-worksheet` (Parts 2.2, 3.1, 10.2)
5. Consider adding top quotes to `tenant.config.ts` testimonials section
```

## Anti-Scraping Considerations

Goodreads and Amazon actively resist scraping. Strategies:

1. **Use browser tools** (`mcp__chrome-devtools`) rather than raw HTTP — renders JavaScript, handles dynamic loading
2. **Human-like pacing** — 3–5 seconds between page loads, vary the interval
3. **Don't paginate too deep** — Top 100 reviews per book is plenty; going to page 50 will trigger blocks
4. **Fallback to WebSearch** — If direct scraping fails, use `WebSearch` queries like `site:goodreads.com "the forgotten ways" review` to find cached/indexed review content
5. **Accept partial results** — Getting 60% of reviews with high signal is better than getting blocked trying for 100%
6. **Session management** — If using browser, don't clear cookies between requests for the same domain within a run

## Error Handling

- Goodreads CAPTCHA / block → log warning, report partial results, suggest retry with `--goodreads-url` for manual URL input
- Amazon bot detection → log warning, continue with Goodreads + editorial only
- Book not found on platform → skip, add to warnings with search terms tried
- Review text truncated and can't expand → save truncated text, flag as `[truncated]`
- Rate limit hit → pause 30 seconds, retry once, then skip to next book
- No reviews found for a book → create empty file with stats only, note in report
