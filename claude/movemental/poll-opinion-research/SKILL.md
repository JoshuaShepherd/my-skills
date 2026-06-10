---
name: poll-opinion-research
description: Research public opinion, polling data, and sentiment trends using Pew Research, Gallup, Ipsos, Eurobarometer, YouGov, and other major polling organizations. Produces a structured report with data tables, trend analysis, and full source attribution.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

Research public opinion and polling data on: $ARGUMENTS

$ARGUMENTS can include:
- A topic (e.g. `public attitudes toward AI`, `trust in institutions`, `political polarization`)
- A geographic focus (e.g. `--region US`, `--region EU`, `--region global`)
- A time range (e.g. `--since 2020`, `--trend 2015-2025`)
- A demographic focus (e.g. `--demo age`, `--demo partisan`, `--demo education`)
- An output path override (default: `_research/polling/`)
- A depth flag (e.g. `--depth quick` for headline numbers, `--depth deep` for full trend analysis)
- Empty — ask the user what topic they want opinion data on

---

## Purpose

This skill performs **live research across major polling and public opinion organizations** to find the most current and authoritative data on what people think, believe, and feel about a given topic. It retrieves published survey findings, trend data, demographic breakdowns, and cross-national comparisons, then organizes everything into a structured, citation-rich report.

**What it produces:**
- `_research/polling/[topic-slug]/README.md` — headline findings and executive summary
- `_research/polling/[topic-slug]/data-tables.md` — all extracted polling numbers in table format
- `_research/polling/[topic-slug]/trend-analysis.md` — how opinion has changed over time
- `_research/polling/[topic-slug]/demographic-breakdowns.md` — opinion by age, education, gender, party, etc.
- `_research/polling/[topic-slug]/methodology-notes.md` — sample sizes, margins of error, methods
- `_research/polling/[topic-slug]/source-index.md` — all searches run, pages fetched, retrieval status

---

## Source Organizations

### 1. Pew Research Center (Primary — US & Global)

**What it is:** Non-partisan fact tank. Conducts extensive public opinion polling on technology, politics, religion, media, demographics, and global affairs. Among the most respected and frequently cited survey organizations. Regularly publishes AI-specific opinion research.

**Web Endpoints:**
```
# Main search
https://www.pewresearch.org/search/{query}

# Topic pages (curated collections)
https://www.pewresearch.org/topic/science/science-issues/artificial-intelligence/
https://www.pewresearch.org/topic/politics-policy/
https://www.pewresearch.org/topic/internet-technology/
https://www.pewresearch.org/topic/religion/

# Data sets (downloadable)
https://www.pewresearch.org/datasets/

# Global Attitudes
https://www.pewresearch.org/global/
```

**Search strategy:**
```
site:pewresearch.org "{topic}" survey 2024 OR 2025
site:pewresearch.org "{topic}" public opinion
site:pewresearch.org "{topic}" Americans say
```

**What to extract:**
- Headline percentages (e.g., "52% of Americans say...")
- Trend data (same question asked over multiple years)
- Demographic breakdowns (age, education, party, race/ethnicity, gender)
- Methodology boxes (sample size, dates, margin of error)
- Full report URLs for citation

**Usage notes:**
- Reports are freely available online with detailed methodology
- Pew often publishes crosstabs and topline questionnaires as PDFs
- Their data is considered gold standard for non-partisan opinion research
- Check both the main report and any "detailed tables" or "appendix" links

### 2. Gallup (Primary — US & Global Tracking)

**What it is:** Long-running polling organization with tracking polls on confidence in institutions, economic outlook, social issues, and well-being. Valuable for longitudinal trends spanning decades.

**Web Endpoints:**
```
# Main search
https://news.gallup.com/search/default.aspx?q={query}

# Topic pages
https://news.gallup.com/topic/technology.aspx
https://news.gallup.com/topic/world-affairs.aspx
https://news.gallup.com/topic/politics.aspx

# Gallup Analytics (some data free, some gated)
https://www.gallup.com/analytics/
```

**Search strategy:**
```
site:gallup.com "{topic}" poll survey 2024 OR 2025
site:news.gallup.com "{topic}" Americans
"gallup poll" "{topic}" 2024 OR 2025
```

**What to extract:**
- Tracking poll trend lines (Gallup often asks the same question for 10-50+ years)
- "Confidence in institutions" data
- Economic confidence index numbers
- "Most important problem" data
- Demographic breakdowns where published

**Usage notes:**
- Published poll reports at news.gallup.com are free to read
- Some deeper analytics and datasets require subscription
- Gallup's value is in **longitudinal trends** — always look for historical comparison
- Note when data is from Gallup Panel (online) vs. traditional phone polling

### 3. Ipsos (Global Multi-Country Surveys)

**What it is:** Multinational research firm that publishes regular global surveys on technology perceptions, social issues, trust, and current events. Excellent for cross-country comparison data.

**Web Endpoints:**
```
# Main search/publications
https://www.ipsos.com/en/knowledge/search?search={query}

# Global Advisor surveys
https://www.ipsos.com/en/ipsos-global-advisor

# What Worries the World (monthly tracking)
https://www.ipsos.com/en/what-worries-world
```

**Search strategy:**
```
site:ipsos.com "{topic}" survey global 2024 OR 2025
"ipsos" "{topic}" public opinion poll
site:ipsos.com artificial intelligence OR AI survey
```

**What to extract:**
- Cross-country comparison tables (typically 25-30 countries)
- "What Worries the World" monthly tracking data
- Global averages vs. country-specific figures
- Trust/confidence metrics
- Infographics and data visualizations (note the data within them)

**Usage notes:**
- Published reports and infographics are free
- Ipsos Global Advisor surveys typically cover 25-30 countries with ~1,000 respondents each
- Reports often come with downloadable PDFs containing full data tables
- Particularly strong on AI perceptions — they run regular multi-country AI surveys

### 4. Eurobarometer (EU Public Opinion)

**What it is:** The European Commission's public opinion survey program. Conducted in all EU member states plus candidate countries. Covers technology, science, values, social issues, and EU policy.

**Web Endpoints:**
```
# Main portal
https://europa.eu/eurobarometer/screen/home

# Search surveys
https://europa.eu/eurobarometer/surveys/browse/all/theme/all

# Open data portal (full datasets)
https://data.europa.eu/data/datasets?query=eurobarometer
```

**Search strategy:**
```
site:europa.eu eurobarometer "{topic}"
"eurobarometer" "{topic}" 2024 OR 2025
"special eurobarometer" "{topic}"
"standard eurobarometer" "{topic}"
```

**What to extract:**
- Country-by-country breakdowns across all EU members
- Trend data (Eurobarometer has tracked some questions for 40+ years)
- Demographic breakdowns (age, education, occupation, urbanization)
- Special Eurobarometer reports on specific themes (AI, science, digital)
- Standard Eurobarometer tracking questions on trust, economy, issues

**Usage notes:**
- All reports and datasets are **completely free** and open
- Full datasets are downloadable from the EU Open Data Portal
- Two types: "Standard" (biannual tracking survey) and "Special" (topic-specific deep dives)
- The Special Eurobarometer on AI/digital is particularly rich
- Reports include methodology, sample sizes per country, and margin of error
- Available in all EU languages

### 5. YouGov (High-Frequency Digital Polling)

**What it is:** Online polling firm that publishes a high volume of topical polls across US, UK, and other markets. Fast-turnaround polling on current events and trending topics. Also runs brand tracking.

**Web Endpoints:**
```
# Main results/articles
https://today.yougov.com/search?q={query}

# Topics
https://today.yougov.com/topics/technology
https://today.yougov.com/topics/politics

# YouGov-Cambridge tracking
https://today.yougov.com/topics/yougov-cambridge
```

**Search strategy:**
```
site:today.yougov.com "{topic}" poll
site:yougov.co.uk "{topic}" survey
"yougov" "{topic}" 2024 OR 2025 poll results
```

**What to extract:**
- Topical poll results (often with demographic crosstabs)
- Favorability/approval ratings
- "Most important issue" tracking
- Brand/entity perception data
- Cross-country comparisons (US/UK primarily)

**Usage notes:**
- Published poll results are free to read
- YouGov polls are online panel-based (note this in methodology)
- Very high volume — useful for finding polls on niche topics
- YouGov-Cambridge Centre for Public Opinion Research produces more rigorous studies
- Data Explorer tool sometimes allows custom crosstabs

### 6. Morning Consult (Tech & Industry Tracking)

**What it is:** Data intelligence company with high-frequency polling. Strong coverage of technology perception, brand trust, and industry-specific sentiment. Publishes regular AI tracking data.

**Search strategy:**
```
site:morningconsult.com "{topic}" poll survey
"morning consult" "{topic}" 2024 OR 2025 survey
site:pro.morningconsult.com "{topic}"
```

**What to extract:**
- Technology adoption and perception metrics
- AI-specific tracking polls
- Brand trust and favorability data
- Demographic and partisan breakdowns
- Trend tracking over quarters

**Usage notes:**
- Some content is free, some requires Pro subscription
- Their AI tracking data is among the most current available
- Note when data is from free reports vs. gated Pro content

### 7. ANES & GSS (US Longitudinal — Deep Demographic Data)

**What it is:**
- **ANES** (American National Election Studies): Deep surveys on political attitudes, values, and participation. Conducted every election cycle since 1948.
- **GSS** (General Social Survey): Broad sociological survey on American attitudes and behaviors. Conducted since 1972 by NORC at University of Chicago.

**Web Endpoints:**
```
# GSS Data Explorer
https://gssdataexplorer.norc.org/
https://gss.norc.org/

# ANES
https://electionstudies.org/
https://electionstudies.org/data-center/
```

**Search strategy:**
```
site:gssdataexplorer.norc.org "{topic}"
site:electionstudies.org "{topic}"
"general social survey" "{topic}" trend
"ANES" "{topic}" attitudes
```

**What to extract:**
- Multi-decade trend lines on social attitudes
- Extremely detailed demographic breakdowns
- Political behavior and participation data (ANES)
- Social trust, religion, work, family, race attitudes (GSS)

**Usage notes:**
- Both datasets are **completely free** to access and download
- GSS Data Explorer allows running crosstabs online without downloading data
- These are the gold standard for understanding long-term American attitude change
- Academic-quality methodology — probability samples, detailed codebooks
- ANES cumulative file spans 1948-present; GSS spans 1972-present

### 8. Stanford HAI AI Index (AI-Specific Annual Report)

**What it is:** The Stanford Institute for Human-Centered AI publishes an annual AI Index Report that compiles AI-related polling data, public perception trends, policy attitudes, and industry sentiment from multiple sources.

**Web Endpoint:**
```
https://aiindex.stanford.edu/report/
```

**Search strategy:**
```
site:aiindex.stanford.edu public opinion OR perception OR survey
"AI Index Report" public opinion "{year}"
"Stanford HAI" AI public perception survey
```

**What to extract:**
- Aggregated public opinion data from multiple polling sources
- Cross-national AI perception comparisons
- AI policy preference data
- Workforce and industry sentiment on AI
- Media coverage analysis of AI topics

**Usage notes:**
- The full report is **free to download** as PDF
- Published annually (typically March-April)
- Compiles data from Pew, Ipsos, Gallup, Eurobarometer, and other sources — very useful as a meta-source
- Includes data visualizations that synthesize multiple polls

---

## Research Process

### Phase 1 — Scope & Strategy

Before searching, establish:
1. **Topic** — What opinion/attitude are we measuring?
2. **Geography** — US only? EU? Global? Specific countries?
3. **Time frame** — Current snapshot? Trend over time?
4. **Demographic interest** — Any particular breakdowns needed (age, party, education)?
5. **Search terms** — Generate 3-5 query variations:
   - The topic as commonly polled (e.g., "artificial intelligence" not just "AI")
   - Related framings (e.g., "automation" OR "machine learning" alongside "AI")
   - Polling-specific language ("survey" "poll" "public opinion" "Americans say")

State the strategy before executing.

### Phase 2 — Multi-Source Search

Search across all relevant sources in priority order:

**For US opinion:**
1. Pew Research Center (most authoritative, detailed methodology)
2. Gallup (best for longitudinal tracking)
3. YouGov / Morning Consult (most current, highest frequency)
4. ANES / GSS (deepest demographic data, longer time horizons)

**For global/comparative opinion:**
1. Pew Global Attitudes
2. Ipsos Global Advisor
3. Eurobarometer (EU-specific)
4. YouGov (US/UK comparison)

**For AI-specific opinion:**
1. Pew (regular AI surveys)
2. Stanford HAI AI Index (aggregated data)
3. Ipsos (global AI perception surveys)
4. Morning Consult (AI tracking)
5. Eurobarometer Special on Digital/AI

For each source:
- Run 2-3 search query variations
- Fetch the most relevant report pages
- Extract data tables, percentages, and trend data
- Record methodology details (sample size, dates, method)
- Log all searches in the source index

### Phase 3 — Data Extraction

For each poll or survey found, extract into structured format:

| Field | Description |
|-------|-------------|
| `source` | Organization name |
| `report_title` | Full title of the report or article |
| `publication_date` | When the report was published |
| `fieldwork_dates` | When the survey was conducted |
| `sample_size` | Number of respondents |
| `population` | Who was surveyed (US adults, global, registered voters, etc.) |
| `method` | Phone, online panel, in-person, mixed |
| `margin_of_error` | Overall and for subgroups if stated |
| `key_findings` | Top-line percentages and findings |
| `demographic_breaks` | Any breakdowns by age, party, education, gender, race, etc. |
| `trend_data` | Same question asked in prior waves, if available |
| `url` | Direct link to the report |

### Phase 4 — Trend Analysis

When the same question has been asked across multiple time periods:

1. **Build a trend table** showing the response over time
2. **Identify inflection points** — when did opinion shift? What was happening?
3. **Note direction and magnitude** — is opinion moving slowly or rapidly? In what direction?
4. **Partisan/demographic divergence** — are different groups trending in different directions?
5. **Cross-national trends** — are patterns consistent globally or divergent?

### Phase 5 — Demographic Deep Dive

Where data permits, build demographic comparison tables:

```markdown
| Demographic | Favorable | Unfavorable | Unsure |
|-------------|-----------|-------------|--------|
| **Age**     |           |             |        |
| 18-29       | X%        | Y%          | Z%     |
| 30-49       | ...       | ...         | ...    |
| 50-64       | ...       | ...         | ...    |
| 65+         | ...       | ...         | ...    |
| **Party**   |           |             |        |
| Democrat    | ...       | ...         | ...    |
| Republican  | ...       | ...         | ...    |
| Independent | ...       | ...         | ...    |
| **Education** |         |             |        |
| College+    | ...       | ...         | ...    |
| Some college| ...       | ...         | ...    |
| HS or less  | ...       | ...         | ...    |
```

Note which breakdowns come from which source — not all polls publish the same demographic cuts.

### Phase 6 — Output Generation

Write all output files with clean markdown formatting.

**README.md structure:**
```markdown
# Public Opinion Research: [Topic]
**Date:** [YYYY-MM-DD]
**Topic:** [topic description]
**Geographic scope:** [US / EU / Global / etc.]
**Sources consulted:** [N organizations, N reports]
**Date range of polls:** [earliest to most recent]

## Headline Findings
[Top 5-7 findings with specific numbers and sources]

## Key Trends
[2-3 sentence summary of how opinion is changing]

## Most Surprising Finding
[The data point that challenges common assumptions]

## Files in This Report
- [data-tables.md](data-tables.md) — All polling numbers in table format
- [trend-analysis.md](trend-analysis.md) — How opinion has changed over time
- [demographic-breakdowns.md](demographic-breakdowns.md) — Opinion by demographic groups
- [methodology-notes.md](methodology-notes.md) — Sample sizes, methods, margins of error
- [source-index.md](source-index.md) — All searches and sources
```

---

## Key Rules

- **Numbers must have sources** — Every percentage, every data point must be attributed to a specific poll with date, source, and sample size. Never state a polling number without attribution.
- **No fabricated poll data** — Never invent survey results. If you cannot find polling data on a specific question, say so. "No data found" is better than a fabricated number.
- **Methodology matters** — Always note sample size, method (phone vs. online), and margin of error. A poll of 500 people has very different reliability than a poll of 5,000.
- **Question wording matters** — The exact wording of a poll question dramatically affects results. When possible, include the actual question text. Note when different polls ask differently-worded questions on the same topic.
- **Margin of error applies to subgroups** — A poll's overall MOE of ±3% may be ±6-8% for a demographic subgroup. Note this when presenting breakdowns.
- **Online vs. probability samples** — Probability samples (Pew, Gallup phone, ANES, GSS) are methodologically stronger than online opt-in panels (YouGov, Morning Consult). Note the difference.
- **Source index is mandatory** — Every search, fetch, and data retrieval must be logged in `source-index.md`.
- **Recency hierarchy** — When the same organization has published multiple waves, always lead with the most recent data and show the trend.
