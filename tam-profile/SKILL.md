---
name: tam-profile
description: Deep-dive research on an individual movement leader — digital presence, content landscape, affiliations, gaps, and Movemental fit analysis
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Profile: Deep Research on a Movement Leader

Conduct comprehensive research on a single movement leader, producing a structured dossier covering their digital presence, content landscape, affiliations, audience, gaps, and Movemental platform fit.

## Invocation

```
/tam-profile $ARGUMENTS
```

**Arguments:**
- A leader's full name. Examples:
  - `/tam-profile Mark Sayers`
  - `/tam-profile Danielle Strickland`
  - `/tam-profile Steve Addison`

---

## Before Starting

1. **Check if research already exists** in `intelligence/leader-research/` for this leader
2. **Read the rubric** at `intelligence/leader-research/tam-search/03-RUBRIC.md` for evaluation criteria
3. **Read the reflected understanding template** — the profile feeds directly into reflected understanding generation
4. **Create the output directory**: `intelligence/leader-research/profiles/[slug]/`

---

## Phase 1: Digital Presence Discovery

Search comprehensively for the leader's digital footprint:

| Platform | What to Find |
|----------|-------------|
| Personal website | URL, structure, content types, freshness |
| Social media | Twitter/X, Instagram, Facebook, LinkedIn, YouTube — follower counts, posting frequency, engagement |
| Podcast | Own podcast or frequent guest appearances |
| Substack/Newsletter | Subscriber signals, posting cadence |
| Amazon/Goodreads | Books published, ratings, review counts |
| Speaking/Events | Conference appearances, speaking topics |
| Academic | Seminary appointments, published papers |
| Organizations | Founded, led, affiliated |

**Output file**: `intelligence/leader-research/profiles/[slug]/digital-presence.md`

---

## Phase 2: Content Landscape Analysis

Map the leader's complete body of work:

### Books
For each book:
- Title, year, publisher
- Goodreads rating and review count
- Key themes / framework introduced
- Co-authors (if any)

### Other Content Forms
- Courses / training programs (platform, pricing, enrollment signals)
- Articles / blog posts (volume, recency, where published)
- Podcasts (own show or frequent guest)
- Video content (YouTube, Vimeo, teaching series)
- Assessments / tools (like APEST, if applicable)
- Frameworks / models (named, cited by others)

### Content Themes
Identify 3-5 core themes across all content. Map to movemental DNA keywords:
- Multiplication, incarnational, kingdom, decentralized, everyday, practice/rhythms, communitas, prophetic, transformation

**Output file**: `intelligence/leader-research/profiles/[slug]/content-analysis.md`

---

## Phase 3: Affiliation & Network Mapping

Document all organizational connections:

| Connection Type | Details |
|----------------|---------|
| Founded/Co-founded | Orgs they started |
| Current leadership roles | Boards, executive positions |
| Network memberships | Forge, Exponential, V3, NewThing, etc. |
| Publisher relationships | Which publishers, how many titles |
| Seminary/Academic ties | Teaching, adjunct, advisory |
| Co-authors | Who they've written with |
| Endorsers/Endorsees | Who blurbs their books, whose books they blurb |
| Conference circuit | Where they speak regularly |
| Connections to existing TAM | Links to candidates on the master list |

**Output file**: `intelligence/leader-research/profiles/[slug]/affiliations.md`

---

## Phase 4: Gap Analysis

Analyze the gap between their offline credibility and online legibility:

### Embodied Work Indicators (Offline Credibility)
- Track record of practice (years, context)
- Multiplication evidence (people/orgs catalyzed)
- Peer recognition (endorsements, invitations, co-authorship)
- Institutional affiliations and roles

### Digital Expression (Online Legibility)
- Is their content discoverable via search?
- Is their body of work structured and interconnected?
- Do they own their primary platform or depend on publishers/orgs?
- Is their content optimized for AI discoverability (structured, semantic)?
- Is their voice captured in any digital AI system?

### The NOTs Assessment
Which of these apply to this leader?
- [ ] Content is NOT translated / multilingual
- [ ] Content is NOT structured or repurposed across formats
- [ ] Content is NOT interconnected (books, courses, articles live in silos)
- [ ] Content is NOT owned / unified under one platform
- [ ] Content is NOT legible to AI systems
- [ ] Content is NOT optimized for discoverability (SEO/GEO)
- [ ] Content is NOT connected to an AI agent that reflects their voice

**Output file**: `intelligence/leader-research/profiles/[slug]/gap-analysis.md`

---

## Phase 5: Movemental Fit Analysis

Assess platform fit using the three core recognitions:

1. **Movement Leader** — Is this person (or their org) movement-oriented?
2. **mDNA Aligned** — Does their work embody the six elements of apostolic movement?
3. **Content Creator** — Do they create and publish content (teaching, writing, courses, talks)?

**Fit verdict**: Full Fit (2+ of 3) / Content-No-Movement / Affinity / Not Fit

### Revenue Model Assessment
- Current revenue streams (books, speaking, consulting, courses, assessments)
- Digital revenue potential (what could Movemental unlock?)
- Platform business model alignment (subscription, course, community fit)

### Movemental Fit Score (1-10)
Rate overall fit considering:
- Theological alignment with mDNA
- Content volume and quality
- Audience size and engagement
- Revenue potential
- Network contribution value
- Gap severity (how much does Movemental solve?)

**Output file**: `intelligence/leader-research/profiles/[slug]/movemental-fit.md`

---

## Phase 6: Executive Summary

Produce a single-page summary combining all research:

```markdown
# [Full Name] — Leader Profile Summary

**Domain**: [primary domain]
**Movemental Fit Score**: [X/10]
**Fit Verdict**: [Full Fit / Content-No-Movement / Affinity / Not Fit]

## Quick Facts
- **Current Role**: [title, org]
- **Location**: [city, country]
- **Books**: [count] ([top title])
- **Audience**: [total estimate across platforms]
- **Key Affiliations**: [top 3-5]
- **Network Connections**: [links to existing TAM candidates]

## Key Findings
[3-5 bullet points — what matters most]

## Gap Summary
[2-3 sentences on offline vs online credibility gap]

## NOTs That Movemental Addresses
[Bulleted list of applicable NOTs]

## Recommended Next Steps
- [ ] Score with /tam-score
- [ ] Generate reflected understanding with /tam-reflected-understanding
- [ ] Map network connections with /tam-network-map
- [ ] [Other specific actions]
```

**Output file**: `intelligence/leader-research/profiles/[slug]/summary.md`

---

## Key Rules

1. **Never fabricate biographical data, statistics, or affiliations.** Every claim must come from a live web source.
2. **Track all sources.** Create `intelligence/leader-research/profiles/[slug]/sources.md` listing every URL consulted.
3. **The profile feeds downstream skills.** Ensure data is structured consistently so `/tam-score` and `/tam-reflected-understanding` can consume it.
4. **Check for existing research first** — update rather than duplicate if partial research exists.
5. **Be specific about audience numbers** — "10K Twitter followers" is better than "moderate social presence."
6. **The NOTs assessment is critical** — this is what shows the leader why Movemental matters to them specifically.
7. **Movemental Fit Score calibration**: Alan Hirsch = 8.6/10 (established benchmark). A 9+ is exceptional.
8. **Write for a reader who will use this to decide whether to invest time in outreach.** Be honest about weaknesses and risks, not just strengths.
