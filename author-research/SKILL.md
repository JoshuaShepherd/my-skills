---
name: author-research
description: Deep research for book authors — searches Google Scholar, Internet Archive, JSTOR, Google Books/Ngram, Library of Congress, HathiTrust, OECD/World Bank data, historic newspapers, and news archives. Produces an organized research dossier with primary sources, data, historical context, and full citations.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

Conduct deep research for a book or long-form writing project on: $ARGUMENTS

$ARGUMENTS can include:
- A research topic or question (e.g. `the history of communal movements in America`)
- A source-type focus (e.g. `--type primary-sources`, `--type statistics`, `--type historical`, `--type news`)
- A time period (e.g. `--era 1960-1980`, `--era victorian`, `--era modern`)
- A geographic focus (e.g. `--region europe`, `--region global`)
- An output path override (default: `_research/general/`)
- A depth flag (e.g. `--depth quick` for survey, `--depth deep` for comprehensive)
- Empty — ask the user what they're writing about and what they need

---

## Purpose

This skill is built for **authors researching a book or long-form writing project**. It searches across the richest freely available sources for the kind of material that makes great non-fiction: primary documents, historical records, statistical data, expert scholarship, cultural artifacts, and news archives. It produces an organized research dossier — the kind of file an author keeps on their desk throughout the writing process.

**What it produces:**
- `_research/general/[topic-slug]/README.md` — research overview and key discoveries
- `_research/general/[topic-slug]/primary-sources.md` — historical documents, archives, original texts
- `_research/general/[topic-slug]/scholarship.md` — key books, papers, and expert perspectives
- `_research/general/[topic-slug]/data-and-statistics.md` — quantitative data, tables, trends
- `_research/general/[topic-slug]/timeline.md` — chronological development of the topic
- `_research/general/[topic-slug]/quotable.md` — compelling quotes, passages, and anecdotes
- `_research/general/[topic-slug]/further-leads.md` — promising leads for deeper research
- `_research/general/[topic-slug]/source-index.md` — all searches, URLs, retrieval status

---

## Source Library

### 1. Google Scholar (Cross-Disciplinary Academic Search)

**What it is:** The broadest academic search engine. Indexes papers, books, theses, court opinions, patents, and technical reports across all disciplines. Often finds material that specialized databases miss.

**Web Endpoint:** `https://scholar.google.com/scholar?q={query}`

**Search strategy:**
```
# Basic search
https://scholar.google.com/scholar?q={query}

# With date range
https://scholar.google.com/scholar?q={query}&as_ylo=2015&as_yhi=2025

# Exact phrase
https://scholar.google.com/scholar?q="{exact phrase}"

# Author search
https://scholar.google.com/scholar?q=author:"{name}"+{topic}

# Exclude patents and citations
https://scholar.google.com/scholar?q={query}&as_vis=1
```

**What to extract:**
- Paper/book titles and authors
- Citation counts (indicates influence)
- "Cited by" links (for finding related work)
- "Related articles" links
- Snippet text showing relevant passages
- Links to free full-text versions (look for [PDF] links)

**Usage notes:**
- No API — use via web search/fetch
- Google Scholar often finds free versions of paywalled papers (preprints, author copies)
- Citation count is the best quick proxy for a work's influence
- The "Cited by" link for a foundational work is a goldmine — it shows every paper that built on it
- Also use web search: `"scholar.google.com" {topic} {additional terms}`

### 2. Internet Archive / Open Library (Digitized Books & Media)

**What it is:** Massive digital library of books, periodicals, audio, video, software, and web pages. Open Library provides controlled digital lending of full books. The Wayback Machine archives web pages.

**Web Endpoints:**
```
# Search the full archive
https://archive.org/search?query={query}

# Search books specifically
https://archive.org/search?query={query}&and[]=mediatype:texts

# Open Library book search
https://openlibrary.org/search?q={query}

# Open Library search API
https://openlibrary.org/search.json?q={query}&limit=20

# Wayback Machine (for archived web pages)
https://web.archive.org/web/{url}
```

**What to extract:**
- Full-text books in the public domain
- Digitized periodicals and magazines
- Historical documents and pamphlets
- Audio recordings (lectures, interviews, radio)
- Book metadata (publication info, subjects, editions)

**Usage notes:**
- Public domain works are freely downloadable in multiple formats
- In-copyright books available via "controlled digital lending" — 1-hour borrow
- The Internet Archive's collection of scanned periodicals is extraordinary for historical research
- Search within texts is supported for many digitized works
- Open Library API returns structured JSON with ISBNs, covers, subjects, and edition data

### 3. JSTOR Open Access

**What it is:** Digital library of academic journals, books, and primary sources. Thousands of journals are now in JSTOR's open-access collection, freely available without institutional access.

**Web Endpoints:**
```
# Main search
https://www.jstor.org/action/doBasicSearch?Query={query}

# Open access filter
https://www.jstor.org/action/doBasicSearch?Query={query}&acc=oa

# Search within a discipline
https://www.jstor.org/action/doBasicSearch?Query={query}&disc={discipline_code}
```

**Search strategy:**
```
site:jstor.org "{topic}" open access
site:jstor.org "{topic}" {key author}
"jstor" "{topic}" free full text
```

**What to extract:**
- Journal articles (abstracts always free; full text for open-access items)
- Book chapters and reviews
- Primary source documents in JSTOR's special collections
- Citation metadata

**Usage notes:**
- JSTOR open access includes thousands of journal titles with full-text access
- Even for non-open-access articles, abstracts and first pages are viewable
- JSTOR's humanities and social science coverage is particularly deep
- Primary Source collections include letters, pamphlets, and historical documents
- Some content becomes open access after an embargo period (moving wall)

### 4. Google Books & Google Ngram Viewer (Text Search & Word Trends)

**What it is:** Google Books searches inside millions of digitized books with snippet view. Ngram Viewer tracks the frequency of words and phrases across centuries of published text — invaluable for understanding how ideas have evolved.

**Web Endpoints:**
```
# Google Books search
https://www.google.com/search?tbm=bks&q={query}

# Google Books API
https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=20

# With subject filter
https://www.googleapis.com/books/v1/volumes?q={query}+subject:{subject}&maxResults=20

# Ngram Viewer
https://books.google.com/ngrams/json?content={word1,word2}&year_start=1800&year_end=2019&corpus=en-2019&smoothing=3
```

**What to extract from Google Books:**
- Book titles, authors, publication dates, publishers
- Snippet views showing relevant passages (search within books)
- Subject classifications
- Related books
- Preview availability

**What to extract from Ngram Viewer:**
- Word/phrase frequency over time (when did a concept enter the discourse?)
- Comparative frequency (which of two related terms dominates?)
- Inflection points (when did usage spike or drop?)
- Historical context for the evolution of ideas and terminology

**Usage notes:**
- Google Books snippet view often reveals the most relevant passages in a book — great for deciding what to acquire and read
- Ngram data covers 1500-2019 across multiple language corpora
- Ngram is phenomenal for book introductions — "The term X first appeared in the 1840s and peaked in usage around..."
- The API returns structured JSON with ISBNs, descriptions, categories, and preview links
- Use Ngram case-insensitive smoothing=3 for cleaner trend lines

### 5. Library of Congress Digital Collections (Primary Sources)

**What it is:** The world's largest library, with massive free digital collections: manuscripts, maps, photographs, newspapers, audio recordings, legislation, and more.

**Web Endpoints:**
```
# Main digital collections search
https://www.loc.gov/search/?q={query}&fa=online-format:online+text

# Collections by format
https://www.loc.gov/collections/

# Chronicling America (historic newspapers 1777-1963)
https://chroniclingamerica.loc.gov/search/pages/results/?andtext={query}&dateFilterType=yearRange&date1=1800&date2=1963

# Prints & Photographs
https://www.loc.gov/pictures/search/?q={query}

# Maps
https://www.loc.gov/maps/?q={query}

# Manuscripts
https://www.loc.gov/manuscripts/?q={query}

# Congress.gov (legislation)
https://www.congress.gov/search?q={query}
```

**What to extract:**
- Primary source documents (letters, manuscripts, speeches)
- Historical photographs with captions and dates
- Historic newspaper articles and editorials
- Maps and cartographic materials
- Legislative records and congressional documents
- Audio recordings (speeches, oral histories, music)

**Usage notes:**
- Everything in the digital collections is **free and public**
- Chronicling America is extraordinary for historical research — full-text searchable newspapers from 1777-1963
- The Prints & Photographs division has millions of images with detailed cataloging
- Manuscript collections include papers of presidents, scientists, and cultural figures
- LOC subject headings are standardized — learning them helps with precise searches
- Digital collections are continuously growing as more material is digitized

### 6. HathiTrust Digital Library (Research Library Collections)

**What it is:** Partnership of major research libraries. 17M+ digitized volumes. Full-text search across the entire corpus. Public domain works are fully accessible; in-copyright works are searchable with snippet results.

**Web Endpoints:**
```
# Full-text search
https://babel.hathitrust.org/cgi/ls?q1={query}&field1=ocr&a=srchls

# Catalog search
https://catalog.hathitrust.org/Search/Home?lookfor={query}&type=all

# Advanced search with date
https://babel.hathitrust.org/cgi/ls?q1={query}&field1=ocr&yop=after&year=1800&yop2=before&year2=1950
```

**What to extract:**
- Full text of public domain books (pre-1929 US publications)
- Snippet results from in-copyright books (showing relevant passages)
- Rare and out-of-print books not available elsewhere
- Serial publications and periodicals
- Government documents and reports

**Usage notes:**
- Public domain works are fully readable and downloadable as PDF
- For in-copyright works, full-text search returns snippet results (like Google Books but different corpus)
- HathiTrust often has books that Google Books doesn't and vice versa — search both
- Particularly strong for 19th and early 20th century materials
- "Emergency Temporary Access" during certain periods allows broader borrowing
- The research center tools allow computational analysis of the full corpus

### 7. OECD Data & World Bank Open Data (Global Statistics)

**What it is:** The two most comprehensive free sources for international economic, social, and development statistics. OECD covers developed economies; World Bank covers all countries with emphasis on development indicators.

**Web Endpoints:**
```
# OECD Data
https://data.oecd.org/searchresults/?q={query}
https://stats.oecd.org/

# World Bank Open Data
https://data.worldbank.org/indicator?tab=all
https://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=100

# World Bank search
https://datacatalog.worldbank.org/search?q={query}

# Common World Bank indicators:
# NY.GDP.PCAP.CD - GDP per capita
# SP.POP.TOTL - Population
# SE.ADT.LITR.ZS - Literacy rate
# IT.NET.USER.ZS - Internet users (% of population)
# SL.UEM.TOTL.ZS - Unemployment rate
```

**What to extract:**
- Country-level statistics across hundreds of indicators
- Time series data (many indicators tracked annually since 1960+)
- Cross-country comparison tables
- Development indicators (poverty, health, education, infrastructure)
- Economic data (GDP, trade, employment, inflation)
- Technology adoption metrics (internet access, mobile subscriptions)

**Usage notes:**
- Both are **completely free** with downloadable datasets
- World Bank API returns structured JSON — easy to extract specific data
- OECD data is particularly strong on education, labor, health, and economic policy
- World Bank data is particularly strong on development, poverty, and low/middle-income countries
- Both offer visualization tools on their websites
- Data can be cited as: "World Bank, World Development Indicators, [year]"

### 8. Chronicling America + News Archives (Historical & Modern News)

**What it is:** Chronicling America (Library of Congress) provides digitized US newspapers from 1777-1963. For modern news, web search and news aggregators provide coverage.

**Web Endpoints:**
```
# Chronicling America — historic newspapers
https://chroniclingamerica.loc.gov/search/pages/results/?andtext={query}&dateFilterType=yearRange&date1={start_year}&date2={end_year}

# Chronicling America — browse by state/title
https://chroniclingamerica.loc.gov/newspapers/

# Modern news via web search
Search: "{topic}" site:nytimes.com OR site:washingtonpost.com OR site:reuters.com OR site:apnews.com
```

**What to extract:**
- Historical newspaper articles (full text + page images)
- Contemporary accounts of historical events
- Editorials and opinion pieces showing period attitudes
- Advertisements (social history gold)
- Modern news coverage of your topic

**Usage notes:**
- Chronicling America is **completely free** — full page images and OCR text
- OCR quality varies — try multiple search term spellings for older papers
- Coverage is not uniform — some states/periods have much better coverage than others
- For modern news, respect paywalls — note when an article is behind a paywall and cite it without copying full text
- News archives are crucial for establishing "what people were saying at the time"

### 9. Google News & News Aggregation (Current Coverage)

**What it is:** For understanding the current media landscape around a topic — how it's being covered, by whom, and from what angles.

**Search strategy:**
```
# Google News search
"{topic}" site:reuters.com OR site:apnews.com (for wire services — factual baseline)
"{topic}" site:theatlantic.com OR site:newyorker.com (for long-form analysis)
"{topic}" site:ft.com OR site:economist.com (for economic/business angle)
"{topic}" 2024 OR 2025 feature OR investigation OR analysis (for deep reporting)
```

**What to extract:**
- Key narratives and frames being used
- Expert sources quoted (potential interviewees or citation sources)
- Data points and statistics cited
- Contrasting perspectives and debates
- Timeline of how coverage has evolved

**Usage notes:**
- Use news as a **pointer to deeper sources** — journalists cite reports, studies, and experts
- Track which experts are repeatedly quoted on a topic — they're the authorities to cite
- News coverage reveals the public framing of issues — useful for understanding audience context
- Be aware of publication perspective — note editorial leanings when relevant

---

## Research Process

### Phase 1 — Research Brief

Before searching, establish:
1. **What is being written?** — Book, chapter, article, essay? What's the thesis or narrative arc?
2. **What kind of material is needed?**
   - Primary sources (original documents, speeches, data)
   - Secondary sources (scholarship, analysis, criticism)
   - Statistical data (numbers, trends, comparisons)
   - Historical context (what was happening at the time?)
   - Contemporary voices (news, opinion, cultural artifacts)
   - Quotable material (passages, anecdotes, vivid details)
3. **Time period** — What era(s) are relevant?
4. **Geographic scope** — What regions matter?
5. **Search terms** — Generate 5+ query variations across different framings

State the research brief before executing.

### Phase 2 — Multi-Source Search

Search strategically across sources based on what's needed:

**For historical topics:**
1. Library of Congress (primary sources, newspapers, photographs)
2. HathiTrust (older books, out-of-print material)
3. Internet Archive (digitized books, periodicals)
4. Chronicling America (newspaper accounts)
5. Google Books Ngram (how terminology evolved)
6. Google Scholar (modern scholarship about the historical topic)

**For contemporary topics:**
1. Google Scholar (academic analysis)
2. OECD / World Bank (statistical data)
3. Google News (current coverage and expert sources)
4. JSTOR (deeper scholarly analysis)
5. Google Books (recent books on the topic)

**For cross-cultural or global topics:**
1. World Bank / OECD (comparative data)
2. Google Scholar (cross-cultural studies)
3. Internet Archive (international publications)
4. News search across international outlets

For each source:
- Run multiple query variations
- Prioritize by relevance and credibility
- Extract key data, quotes, and findings
- Log everything in the source index

### Phase 3 — Material Classification

Organize all found material into categories:

**Primary Sources** — Original documents, data, firsthand accounts
- What: Letters, speeches, legislation, data sets, photographs, recordings
- Value: Irrefutable evidence; lets the reader encounter the past/topic directly
- Citation standard: Full archival citation with collection, box/folder if applicable

**Scholarly Sources** — Expert analysis and interpretation
- What: Peer-reviewed papers, academic books, dissertations
- Value: Establishes credibility; shows you've engaged with expert thinking
- Citation standard: Author, title, journal/publisher, year, DOI if available

**Statistical Sources** — Quantitative evidence
- What: Data tables, trend charts, survey results, economic indicators
- Value: Makes abstract claims concrete; enables comparison
- Citation standard: Organization, dataset name, indicator, year(s), URL

**Narrative Sources** — Stories, anecdotes, vivid details
- What: News articles, personal accounts, cultural artifacts
- Value: Makes the writing come alive; connects abstract ideas to human experience
- Citation standard: Author, title, publication, date, URL

### Phase 4 — Timeline Construction

Build a chronological timeline of the topic:

```markdown
## Timeline: [Topic]

| Year | Event | Significance | Source |
|------|-------|-------------|--------|
| [year] | [what happened] | [why it matters] | [source] |
```

Include:
- Key events and milestones
- Publication dates of influential works
- Policy/legislative changes
- Cultural moments (when the topic entered public consciousness)
- Data inflection points (when trends shifted)

### Phase 5 — Quotable Material

Extract the most compelling quotes and passages:

```markdown
## Quotable Passages

### On [sub-theme]

> "[Exact quote]"
> — [Author], *[Source]*, [Year], p. [page if known]

**Context:** [Why this quote matters; how it could be used in the book]
```

Look for:
- Pithy definitions or framings
- Surprising or counterintuitive statements from experts
- Vivid descriptions or analogies
- Historical figures' own words on the topic
- Data points that tell a story in one sentence

### Phase 6 — Further Leads

Document promising avenues for deeper research:

```markdown
## Further Leads

### Archives to Explore
- [Archive name] at [Institution] — [what's there and why it matters]

### People to Interview / Read
- [Name] — [who they are, why they matter, where to find their work]

### Books to Acquire and Read
- [Title] by [Author] ([Year]) — [why it's relevant, citation count or reputation]

### Datasets to Download
- [Dataset] from [Source] — [what it contains, URL]

### Conferences / Proceedings
- [Conference name] — [relevant proceedings or keynotes]
```

### Phase 7 — Output Generation

Write all output files with clean markdown formatting.

**README.md structure:**
```markdown
# Research Dossier: [Topic]
**Date:** [YYYY-MM-DD]
**Research context:** [What's being written and why]
**Scope:** [time period, geography, disciplines]
**Sources searched:** [N databases, N individual sources found]

## Top Discoveries
[5-7 most valuable finds — the material that will most directly serve the writing]

## Research Landscape
[Brief overview: who studies this, what's the state of knowledge, where are the debates?]

## Source Quality Assessment
[Which sources were richest? Where are the gaps? What might require library/archive visits?]

## Files in This Dossier
- [primary-sources.md](primary-sources.md) — Historical documents and original materials
- [scholarship.md](scholarship.md) — Academic papers, books, and expert analysis
- [data-and-statistics.md](data-and-statistics.md) — Quantitative data and trends
- [timeline.md](timeline.md) — Chronological development
- [quotable.md](quotable.md) — Compelling quotes and passages
- [further-leads.md](further-leads.md) — Promising avenues for deeper research
- [source-index.md](source-index.md) — All searches and sources
```

---

## Key Rules

- **No fabricated sources** — Never invent book titles, article titles, authors, dates, or quotes. Every item must trace to a real search result. "I couldn't find X" is always better than a hallucinated citation.
- **Primary sources are gold** — Always prioritize original documents over secondary accounts. An author's own words, the original data, the actual legislation — these are what make great non-fiction.
- **Source everything** — Every fact, quote, and data point gets a citation. When writing for an author, the citation trail is as important as the content.
- **Note access levels** — Clearly distinguish between freely available material, snippet-only results, and paywalled content. The author needs to know what they can access immediately vs. what requires library visits or purchases.
- **Ngram data tells a story** — When relevant, include Google Ngram data showing how key terms have risen and fallen in usage. This is remarkable material for book introductions and historical framing.
- **The "further leads" file is crucial** — An author doesn't expect AI to do ALL the research. The highest-value output is often the leads that point toward rich material the author can pursue: specific archives, specific people to talk to, specific books to read deeply.
- **Quotable material must be exact** — Only include quotes you've actually found in a fetched source. Never reconstruct or paraphrase a quote and present it in quotation marks.
- **Source index is mandatory** — Every search, API call, and URL fetch must be logged in `source-index.md` with result counts and retrieval status.
- **Think like a research assistant** — The author needs material that is *usable*: properly cited, well-organized, and contextualized. A pile of links is not research. Organized, annotated material with clear citations is research.
