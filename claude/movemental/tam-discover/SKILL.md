---
name: tam-discover
description: Discover new movement leader candidates for the Movemental TAM using network-based and content-based search strategies
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Discovery: Find New Movement Leader Candidates

Discover new candidates for the Movemental Total Addressable Market of movement leaders.

## Invocation

```
/tam-discover $ARGUMENTS
```

**Arguments:**
- A domain, search focus, or specific directive. Examples:
  - `/tam-discover soul care / psychology` — search a specific domain
  - `/tam-discover network: Exponential Conference 2024-2025 speakers` — mine a specific network
  - `/tam-discover content: "household discipleship" practitioners` — content-based keyword search
  - `/tam-discover emerging voices under 40` — search with a lens
  - `/tam-discover` (no args) — run a full sweep across all domains

---

## Before Starting

1. **Read the master list** at `intelligence/leader-research/tam-search/01-MASTER-RANKED-LIST.md` to know all 156 existing candidates
2. **Read the rubric** at `intelligence/leader-research/tam-search/03-RUBRIC.md` for the Seven Gates and scoring criteria
3. **Read the search plan** at `intelligence/leader-research/tam-search/04-SEARCH-PLAN.md` for existing query strategies
4. **Read the content search strategy** at `intelligence/leader-research/tam-search/05-CONTENT-SEARCH-STRATEGY.md` for keyword clusters and domain-specific searches

---

## Phase 1: Determine Search Strategy

Based on the arguments, select one or more search approaches:

### A) Network-Based Search
Mine specific networks, conferences, publishers, and co-author chains:
- Conference speaker lists (Exponential, Missio Alliance, Q Ideas, Justice Conference, Inhabit)
- Publisher catalogs (IVP, Baker, Zondervan, Brazos Press, Cascade)
- Organization leadership (Forge, 100 Movements, V3, NewThing, 3DM, Saturate, Send Network)
- Co-author/endorsement chains from existing top-tier candidates
- Seminary faculty lists (Fuller, Asbury, Northern, Wheaton, Regent, George Fox)
- Podcast guest networks (The Carey Nieuwhof Leadership Podcast, The Phil Vischer Podcast, Nomad Podcast, Homebrewed Christianity, The Liturgists)

### B) Content-Based Search
Search for movemental DNA through content signals rather than network connections:
- Use the keyword clusters from `05-CONTENT-SEARCH-STRATEGY.md`
- Search for books, articles, Substack, podcasts with movemental vocabulary
- Key signals: multiplication, incarnational, kingdom, decentralized, everyday, practice/rhythms, communitas, prophetic, transformation
- Domain-specific searches: psychology/soul care, technology/culture, worship/liturgy, family/parenting, leadership/organization, justice/urban

### C) International Search
Find movement leaders outside US/anglophone networks:
- Search by region: Latin America, Sub-Saharan Africa, East Asia, South/Southeast Asia, Europe, Middle East/North Africa
- Search for English-language content by international practitioners
- Look for translated works, global conference speakers, international network nodes
- Use `/tam-international` skill for deeper international focus

---

## Phase 2: Execute Searches

For each search:

1. **Run the query** using WebSearch
2. **Extract candidate names** from results
3. **Deduplicate** against the master list (check all 156 names)
4. **For each new name, capture:**

| Field | Description |
|-------|-------------|
| Full Name | As published |
| Primary Domain | e.g., "Soul care/leader resilience" |
| Key Affiliations | Orgs, networks, churches, seminaries |
| Notable Works | Books, courses, frameworks (titles) |
| Website/Primary Platform | URL |
| Approximate Audience | Social followers, newsletter size, book sales signals |
| Network Connections | Links to existing TAM candidates |
| Discovery Source | How we found them (query, network, referral) |

---

## Phase 3: Initial Gate Check

For each new candidate, quickly assess the Seven Gates of Credibility:

1. **Embodied Practice (10+ years)** — Not just theory
2. **Multiplication Evidence** — Created multipliers who create multipliers
3. **Movement Over Institution** — Catalyzes organic spread
4. **Prophetic Edge** — Challenges status quo
5. **Credibility Through Suffering** — Cost paid (bonus, not required)
6. **Theological Depth** — Even if implicit
7. **Network Coherence (Scenius Test)** — Enhances, doesn't dilute

Mark each gate: PASS / FAIL / UNCLEAR (needs research)

---

## Phase 4: Document Results

### For each new candidate found:

Add them to the master list at `intelligence/leader-research/tam-search/01-MASTER-RANKED-LIST.md`:
- If scored: place in the scored section at the correct rank position
- If not yet scored: add to an "UNSCORED — NEEDS EVALUATION" section at the bottom

### Create a search log entry:

Append to or create `intelligence/leader-research/tam-search/06-SEARCH-LOG.md`:

```markdown
## [Date] — [Search Focus]

**Strategy**: Network / Content / International
**Queries run**: [list]
**New candidates found**: [count]
**Names**: [list with domains]
**Notes**: [observations about gaps, clusters, surprises]
```

---

## Phase 5: Summary Report

Output a summary including:

1. **New candidates found** (count and names)
2. **Domains represented** (where they cluster)
3. **Gate assessment highlights** (strongest new finds)
4. **Gaps identified** (domains or demographics still underrepresented)
5. **Recommended next steps** (deeper research, scoring, network mapping)

---

## Key Rules

1. **Never fabricate candidates.** Every name must come from a live web search or documented source.
2. **Always deduplicate** against the full master list before adding.
3. **Log every search query** — reproducibility matters.
4. **Critical distinction**: We seek writers who ARE movemental (embody transformation, multiplication, credibility through practice), not just those who WRITE ABOUT movements. 10% are apostolic articulators; 90% are domain practitioners with movemental DNA.
5. **Bias toward hidden gems** — the most valuable discoveries are people NOT already in the network's echo chamber.
6. **International candidates are high priority** — the movement is global; the list should reflect that.
7. **Do not score candidates in this skill** — use `/tam-score` for full rubric evaluation.
8. **Preserve existing data** — never overwrite or remove existing entries in the master list.
