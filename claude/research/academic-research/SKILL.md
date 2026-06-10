---
name: academic-research
description: Deep academic research using free open-access sources — Semantic Scholar, OpenAlex, arXiv, PubMed Central, and CORE. Searches across databases, retrieves papers, extracts key findings, and produces a well-organized research report with full citations.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

Conduct deep academic research on: $ARGUMENTS

$ARGUMENTS can include:
- A research topic or question (e.g. `the relationship between organizational structure and innovation`)
- A discipline filter (e.g. `--field neuroscience`, `--field theology`, `--field organizational-theory`)
- A date range (e.g. `--since 2020`)
- An output path override (default: `_research/academic/`)
- A depth flag (e.g. `--depth quick` for 5-10 papers, `--depth deep` for 20-30+)
- Empty — ask the user what they want to research

---

## Purpose

This skill performs **live academic research** across the best free, open-access scholarly databases available. It searches multiple sources, retrieves abstracts and (where available) full text, synthesizes findings, and produces a structured research report with proper citations.

**What it produces:**
- `_research/academic/[topic-slug]/README.md` — executive summary and key findings
- `_research/academic/[topic-slug]/literature-review.md` — organized synthesis of the literature
- `_research/academic/[topic-slug]/paper-profiles.md` — individual paper summaries with metadata
- `_research/academic/[topic-slug]/citation-network.md` — key citation relationships and influential papers
- `_research/academic/[topic-slug]/source-index.md` — all searches run, URLs fetched, retrieval status

---

## Source Databases

### 1. Semantic Scholar (Primary)

**What it is:** AI-powered academic search engine from the Allen Institute for AI. Covers 200M+ papers across all fields. Provides abstracts, citation counts, influential citation flags, open-access PDF links, and TLDR summaries.

**API Endpoint:** `https://api.semanticscholar.org/graph/v1/`

**Key API routes:**
```
# Search for papers by keyword
GET https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=20&fields=title,abstract,year,citationCount,influentialCitationCount,openAccessPdf,authors,url,tldr,publicationTypes,journal

# Get a specific paper with full details
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,year,citationCount,influentialCitationCount,openAccessPdf,authors,references,citations,url,tldr,journal,publicationTypes,fieldsOfStudy

# Get a paper's references
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,abstract,year,citationCount,authors,url&limit=50

# Get a paper's citations
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title,abstract,year,citationCount,authors,url&limit=50

# Search by author
GET https://api.semanticscholar.org/graph/v1/author/search?query={name}&fields=name,paperCount,citationCount,hIndex
```

**Usage notes:**
- No API key required for basic use (rate-limited to ~100 requests/5 min)
- The `influentialCitationCount` field distinguishes papers that are merely cited from those that are deeply engaged with — prioritize high influential citation counts
- The `tldr` field provides AI-generated paper summaries — very useful for rapid screening
- The `openAccessPdf` field links directly to free full text when available
- Use `fieldsOfStudy` to filter by discipline
- Pagination: use `offset` parameter for additional results

### 2. OpenAlex (Comprehensive Metadata)

**What it is:** Free, open catalog of 250M+ scholarly works. Successor to Microsoft Academic Graph. Rich metadata including institutional affiliations, concepts, citation data, and open-access status.

**API Endpoint:** `https://api.openalex.org/`

**Key API routes:**
```
# Search works (papers)
GET https://api.openalex.org/works?search={query}&per_page=25&sort=cited_by_count:desc

# Filter by publication year
GET https://api.openalex.org/works?search={query}&filter=publication_year:2020-2025&per_page=25

# Filter by open access
GET https://api.openalex.org/works?search={query}&filter=is_oa:true&per_page=25

# Get a specific work by DOI
GET https://api.openalex.org/works/doi:{doi}

# Search authors
GET https://api.openalex.org/authors?search={name}

# Search concepts/topics
GET https://api.openalex.org/concepts?search={concept}

# Get institution details
GET https://api.openalex.org/institutions?search={name}
```

**Usage notes:**
- Completely free, no API key needed (polite pool: add `mailto` parameter for better rate limits)
- Excellent for citation count data and understanding a paper's impact
- The `concepts` field maps papers to a hierarchical topic taxonomy — useful for finding related work
- Use `filter=is_oa:true` to limit results to open-access papers with available full text
- Supports complex filters: `filter=publication_year:>2019,concepts.id:C41008148` (computer science)
- Returns `open_access.oa_url` for direct links to free full text

### 3. arXiv (Preprints — STEM Fields)

**What it is:** The preprint server for physics, mathematics, computer science, quantitative biology, statistics, electrical engineering, and economics. All papers are freely available in full text.

**API Endpoint:** `http://export.arxiv.org/api/query`

**Key API routes:**
```
# Search by keyword
GET http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=20&sortBy=relevance

# Search within title
GET http://export.arxiv.org/api/query?search_query=ti:{query}&max_results=20

# Search within abstract
GET http://export.arxiv.org/api/query?search_query=abs:{query}&max_results=20

# Search by author
GET http://export.arxiv.org/api/query?search_query=au:{author_name}&max_results=20

# Search by category (e.g., cs.AI, cs.CL, physics.soc-ph)
GET http://export.arxiv.org/api/query?search_query=cat:{category}+AND+all:{query}&max_results=20

# Combine with date range
GET http://export.arxiv.org/api/query?search_query=all:{query}+AND+submittedDate:[202001010000+TO+202512312359]&max_results=20
```

**Usage notes:**
- Completely free, no API key needed
- Returns Atom XML — parse for `<entry>` elements containing title, summary, authors, links
- The `<link>` with `title="pdf"` provides direct PDF link
- Every paper on arXiv has full text available — this is the richest free source for STEM
- Common categories: `cs.AI` (AI), `cs.CL` (NLP), `cs.LG` (Machine Learning), `stat.ML`, `q-bio`, `econ`
- arXiv papers are preprints — note they may not be peer-reviewed
- Also search via web: `https://arxiv.org/search/?query={query}&searchtype=all`

### 4. PubMed Central (Biomedical & Life Sciences)

**What it is:** NIH's free full-text archive of biomedical and life sciences literature. Millions of articles from peer-reviewed journals.

**API Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

**Key API routes:**
```
# Search PubMed for article IDs
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax=20&sort=relevance&retmode=json

# Search PMC (full-text subset) for article IDs
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={query}&retmax=20&sort=relevance&retmode=json

# Fetch article summaries by ID
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id1,id2,id3}&retmode=json

# Fetch full abstract
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id}&rettype=abstract&retmode=text

# Fetch full text from PMC
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC{id}&rettype=full&retmode=xml

# Search with date filter
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&mindate=2020/01/01&maxdate=2025/12/31&datetype=pdat&retmode=json
```

**Usage notes:**
- Free, no API key needed (rate-limited to 3 requests/second without key, 10/sec with key)
- Two databases: `pubmed` (citations + abstracts) and `pmc` (full-text open access)
- Always search both — PMC has full text but fewer articles; PubMed has broader coverage
- Use MeSH terms for precise medical/biological searches (e.g., `"organizational innovation"[MeSH]`)
- PMC full-text articles can be retrieved as XML and parsed for sections
- Also searchable via web: `https://pubmed.ncbi.nlm.nih.gov/?term={query}`

### 5. CORE (Global Open Access Aggregator)

**What it is:** Aggregates open-access research papers from repositories and journals worldwide. 200M+ papers, many with full text.

**Web Search Endpoint:** `https://core.ac.uk/search?q={query}`

**Usage notes:**
- Use via web search/fetch — search `site:core.ac.uk {query}` or fetch search results page
- Aggregates from institutional repositories, so often has papers not found elsewhere
- Good for humanities, social sciences, and non-US/UK research
- Full text often available as PDF download
- Particularly useful when Semantic Scholar and OpenAlex return limited results for a niche topic

---

## Research Process

### Phase 1 — Scope & Strategy

Before searching, establish:
1. **Core research question** — What specific question(s) are we trying to answer?
2. **Discipline(s)** — Which fields are relevant? This determines which databases to prioritize.
3. **Date range** — How far back should we look? Default to last 10 years unless topic requires historical depth.
4. **Depth** — Quick survey (5-10 key papers) or deep review (20-30+ papers)?
5. **Search terms** — Generate 3-5 search query variations, including:
   - Direct terminology
   - Synonyms and alternative phrasings
   - Related concepts that might yield relevant results
   - Key author names if known

State the strategy before executing.

### Phase 2 — Multi-Source Search

Run searches across all relevant databases. For each database:

1. **Execute 2-3 query variations** to maximize coverage
2. **Sort by relevance and citation count** to surface the most impactful work
3. **Record every search query and result count** for the source index
4. **Screen results** — read titles and abstracts, flag the most relevant papers

**Priority order for most topics:**
1. Semantic Scholar (broadest, best AI-powered relevance)
2. OpenAlex (best metadata, citation data)
3. arXiv (if STEM-related — full text available)
4. PubMed/PMC (if biomedical/health-related)
5. CORE (for coverage gaps)

**For humanities/theology/social science topics:**
1. Semantic Scholar
2. OpenAlex
3. CORE (stronger in these fields)
4. Web search for specific journal archives (JSTOR open, etc.)

### Phase 3 — Paper Profiling

For each selected paper, extract:

| Field | Description |
|-------|-------------|
| `title` | Full paper title |
| `authors` | All authors with affiliations where available |
| `year` | Publication year |
| `journal` | Journal or conference name |
| `doi` | DOI if available |
| `citation_count` | Total citations |
| `influential_citations` | Influential citation count (from Semantic Scholar) |
| `abstract` | Full abstract |
| `tldr` | AI summary if available |
| `key_findings` | 3-5 bullet points of main findings/arguments (extracted from abstract or full text) |
| `methodology` | Research method used |
| `relevance` | Why this paper matters to our research question |
| `open_access_url` | Direct link to free full text |
| `source_db` | Which database(s) found this paper |

### Phase 4 — Literature Synthesis

Organize findings into a structured literature review:

1. **Thematic organization** — Group papers by sub-theme or argument, not chronologically
2. **Consensus and debate** — Where do researchers agree? Where do they disagree?
3. **Methodological patterns** — What approaches dominate? What's missing?
4. **Evolution of thinking** — How has the field's understanding changed over time?
5. **Key gaps** — What questions remain unanswered?
6. **Seminal works** — Which papers are most-cited and foundational?

### Phase 5 — Citation Network Analysis

Map the citation relationships:

1. **Most-cited papers** in our result set — these are the foundational works
2. **Citation clusters** — groups of papers that cite each other heavily (research communities)
3. **Bridge papers** — papers that connect different research communities or disciplines
4. **Recent high-impact papers** — newer papers with rapid citation accumulation
5. **Recommended further reading** — highly-cited papers in reference lists that we didn't capture

### Phase 6 — Output Generation

Write all output files with clean markdown formatting.

**README.md structure:**
```markdown
# Academic Research: [Topic]
**Date:** [YYYY-MM-DD]
**Research question:** [question]
**Scope:** [fields, date range, depth]
**Papers reviewed:** [N]

## Key Findings
[3-5 top-level findings with supporting citations]

## Research Landscape
[Brief overview of the state of research on this topic]

## Files in This Report
- [literature-review.md](literature-review.md) — Thematic synthesis
- [paper-profiles.md](paper-profiles.md) — Individual paper summaries
- [citation-network.md](citation-network.md) — Citation analysis
- [source-index.md](source-index.md) — All searches and sources
```

---

## Key Rules

- **Live sources only** — All paper data must come from actual API calls or web fetches, not parametric memory. If a database is unavailable, note it and try alternatives.
- **No fabricated citations** — Never invent paper titles, authors, DOIs, or citation counts. Every paper in the report must trace to a real search result.
- **Abstract ≠ full text** — When synthesizing, be clear about whether conclusions come from abstracts or full-text reading. Most synthesis will be abstract-based; flag when full text was available and read.
- **Citation counts are relative** — A paper with 50 citations in a niche field may be more significant than one with 500 in a broad field. Note field context.
- **Preprint caveat** — arXiv papers are preprints. Always note when a source is not peer-reviewed.
- **Source index is mandatory** — Every search query, API call, and URL fetch must be logged in `source-index.md` with result counts and retrieval status.
- **Deduplicate across databases** — The same paper will appear in multiple databases. Deduplicate by DOI or title match. Note which databases found each paper.
