---
name: tam-network-map
description: Map relationships, co-authorships, endorsements, and organizational connections between movement leaders in the TAM
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Network Map: Trace the Movement Leader Graph

Map the relational web between movement leaders — co-authorships, endorsements, shared organizations, conference circuits, and institutional ties. This skill reveals the scenius structure and identifies network clusters, bridge figures, and isolated candidates.

## Invocation

```
/tam-network-map $ARGUMENTS
```

**Arguments:**
- A leader name, organization, or directive. Examples:
  - `/tam-network-map Alan Hirsch` — map all connections radiating from one leader
  - `/tam-network-map Forge Network` — map all leaders connected through an organization
  - `/tam-network-map top 20` — map connections among the top 20 ranked candidates
  - `/tam-network-map clusters` — identify and name the natural clusters in the TAM
  - `/tam-network-map bridges` — find leaders who connect otherwise separate clusters
  - `/tam-network-map isolates` — find candidates with few/no connections to others

---

## Before Starting

1. **Read the master list** at `intelligence/leader-research/tam-search/01-MASTER-RANKED-LIST.md`
2. **Read existing profiles** at `intelligence/leader-research/profiles/` for affiliation data
3. **Read existing candidate profiles** at `intelligence/leader-research/tam-search/02-CANDIDATE-PROFILES.md`

---

## Phase 1: Define Scope

Based on the argument, determine what to map:

| Mode | Scope | Output |
|------|-------|--------|
| **Leader-centric** | All connections from one leader outward | Ego network diagram |
| **Org-centric** | All leaders connected through one org | Organization membership map |
| **Top N** | Connections among the top N candidates | Core network structure |
| **Clusters** | Natural groupings across the full TAM | Cluster identification |
| **Bridges** | Leaders who connect separate clusters | Bridge figure analysis |
| **Isolates** | Candidates with minimal connections | Gap identification |

---

## Phase 2: Research Connections

For each leader in scope, research these connection types via web search:

### Connection Types (weighted by strength)

| Type | Weight | How to Find |
|------|--------|-------------|
| **Co-authored book** | 5 | Amazon, publisher catalogs |
| **Co-founded organization** | 5 | Org websites, about pages |
| **Book endorsement/blurb** | 3 | Amazon "praise for" sections, book covers |
| **Same organization leadership** | 3 | Org team pages |
| **Conference co-speakers** | 2 | Conference speaker lists |
| **Podcast guest on their show** | 2 | Podcast episode lists |
| **Shared publisher** | 1 | Publisher catalogs |
| **Academic colleague** | 2 | Seminary faculty pages |
| **Cited/referenced in work** | 2 | Book indexes, footnotes, bibliographies |
| **Public mutual endorsement** | 2 | Social media, interviews |

---

## Phase 3: Build the Network Data

For each connection found, record:

```markdown
| Leader A | Leader B | Connection Type | Weight | Evidence |
|----------|----------|----------------|--------|----------|
| Alan Hirsch | Michael Frost | Co-authored book | 5 | "The Shaping of Things to Come" (2003) |
| Alan Hirsch | Michael Frost | Co-founded org | 5 | Forge Mission Training Network |
| Alan Hirsch | Dave Ferguson | Book endorsement | 3 | Endorsement on "On the Verge" |
```

---

## Phase 4: Cluster Analysis

Identify natural groupings based on connection density:

### Expected Clusters (validate/update via research)

| Cluster Name | Hub Leaders | Binding Element |
|-------------|-------------|-----------------|
| **Forge/Missional Core** | Hirsch, Frost, Brisco, Roxburgh | Forge Network, missional theology |
| **Multiplication/Exponential** | Ferguson, Wilson, Moore, Wegner | Exponential Conference, church planting |
| **Spiritual Formation** | Barton, Comer, Scazzero, Thompson | Transforming Center, soul care |
| **Justice/Urban** | Perkins, Strickland, Fitch | CCDA, neighborhood mission |
| **Worship/Liturgy** | Hicks, Ruis, Warren (T.H.) | Ancient-future, liturgical renewal |
| **Academic/Theological** | McKnight, Smith (J.K.A.), Hunter | Seminary networks, published theology |
| **International** | Sayers (Melbourne), Addison (global), Mawarire (Harare) | Cross-border movement |

### Bridge Figures
Leaders who connect two or more clusters (high strategic value for the scenius):
- Bridge leaders often have: co-authorships across clusters, conference appearances in multiple circuits, academic + practitioner roles

### Isolates
Candidates with 0-1 connections to other TAM members:
- May be: hidden gems in unexplored domains, candidates who need re-evaluation, or truly disconnected

---

## Phase 5: Output

### Network Data File

**Output file**: `intelligence/leader-research/network/[scope-slug]-network.md`

Structure:
```markdown
# Network Map: [Scope Description]

## Summary
- **Nodes**: [count of leaders mapped]
- **Connections**: [count of edges]
- **Clusters identified**: [count]
- **Bridge figures**: [names]
- **Isolates**: [names]

## Connection Table
[Full table from Phase 3]

## Clusters
[Cluster analysis from Phase 4]

## Bridge Figures
[Analysis of who connects clusters and why they matter]

## Isolates
[List with notes on why isolated and whether concerning]

## Network Insights
- [Key observations about the scenius structure]
- [Gaps: which clusters are underconnected?]
- [Recommendations: who to research/recruit to strengthen the network]
```

### Visualization Data (optional)

If producing a visualization-ready format, output a JSON adjacency list:

```json
{
  "nodes": [
    {"id": "alan-hirsch", "name": "Alan Hirsch", "cluster": "forge-core", "score": 100}
  ],
  "edges": [
    {"source": "alan-hirsch", "target": "michael-frost", "type": "co-author", "weight": 5}
  ]
}
```

**Output file**: `intelligence/leader-research/network/[scope-slug]-network.json`

---

## Key Rules

1. **Every connection must have evidence.** No assumed connections — cite the book, org page, or conference listing.
2. **Use weighted connection types** — a co-authored book (5) is not the same as sharing a publisher (1).
3. **Bridge figures are strategically critical.** They connect clusters and multiply the scenius effect. Flag them prominently.
4. **Isolates are a signal, not a problem.** An isolated high-scorer might be a hidden gem in an untapped domain. An isolated low-scorer might not belong.
5. **The network IS the scenius.** This is not academic graph theory — it directly maps to Movemental's core value proposition of credibility through connection.
6. **Create the `intelligence/leader-research/network/` directory** if it doesn't exist.
7. **International connections are high priority.** Cross-border edges indicate global movement coherence.
8. **Update, don't overwrite.** If network data already exists, merge new connections into the existing file.
