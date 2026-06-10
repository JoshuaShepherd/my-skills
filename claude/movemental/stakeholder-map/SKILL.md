---
name: stakeholder-map
description: Deep-research Youthfront stakeholders and map their full connection networks for donor cultivation
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, WebSearch, WebFetch, mcp__linkedin__get_person_profile, mcp__linkedin__search_people, mcp__linkedin__get_company_profile, mcp__linkedin__close_session
---

Research and map the full connection network for Youthfront stakeholders: $ARGUMENTS

$ARGUMENTS should be one of:
- A stakeholder name (e.g. `Tim Smith`) — research a single stakeholder
- `--all` — research all stakeholders in the registry
- `--unresearched` — research only stakeholders without an existing connection map
- `--refresh NAME` — re-research a previously mapped stakeholder
- `--add "Name" "Role" "Title"` — add a new stakeholder to the registry, then research them
- Empty — show the current registry and ask the user which stakeholder(s) to research

---

## Context

This skill is used **outside** the Youthfront donor platform to seed stakeholder connection data that will later be imported into the app. "Stakeholders" are the people in Youthfront's inner orbit — board members, executives, key staff, major donors, church partners — whose existing relationships are the bridges to new high-value donors.

The goal is to produce a comprehensive, structured map of each stakeholder's external connections: who they know, through what context, and how those connections could become pathways to donor cultivation.

**Project path:** `~/Desktop/Dev/repos/non-profit-dashboard`

---

## Before Starting

1. Read the stakeholder registry: `~/Desktop/Dev/repos/non-profit-dashboard/public/data/insiders.json`
2. Read existing LinkedIn data: `~/Desktop/Dev/repos/non-profit-dashboard/public/data/insiders-linkedin.json`
3. Read any existing connection maps in: `~/Desktop/Dev/repos/non-profit-dashboard/public/data/stakeholder-connections/`
4. Check LinkedIn MCP session health — run a lightweight lookup to confirm the session is active. If it fails, tell the user to run `uvx linkedin-scraper-mcp --login` to re-authenticate.
5. Read the connection mapping strategy doc for context on relationship types and scoring: `~/Desktop/Dev/repos/non-profit-dashboard/_docs/agentic-connection-mapping.md`

If the `stakeholder-connections/` directory doesn't exist, create it.

---

## Research Pipeline

For each stakeholder, execute these stages sequentially. Stream progress to the user after each stage.

### Stage 1 — Compile Existing Intelligence

Gather everything already known about this stakeholder from project files:

1. Pull their record from `insiders.json` (affiliations, role, summary, sources)
2. Pull their LinkedIn enrichment from `insiders-linkedin.json` (experience, education, skills, connections)
3. Check if any prospect records reference them (search `prospects-tier1.json` through `prospects-tier4-part2.json` for name mentions in `fields.network_connections` or similar)
4. Check harvest data if available: `_docs/api-sources/kc-donor-prospecting/harvest/output/` for LittleSis relationships, 990 cross-references, FEC co-giving

Compile into a working profile document. Identify **gaps** — what affiliations, boards, churches, clubs, or networks are unknown or unconfirmed.

### Stage 2 — LinkedIn Deep Dive

Use the LinkedIn MCP tools to pull the stakeholder's full profile and extract connection signals:

```
mcp__linkedin__get_person_profile:
  url: [stakeholder's LinkedIn URL from registry]
  sections: experience, education, interests, honors, contact_info
```

From the profile, extract and structure:
- **Current and past employers** — with titles, dates, and overlap potential
- **Board and volunteer roles** — explicitly listed or mentioned in descriptions
- **Education** — alma maters, graduation years, honors societies
- **Professional associations** — any mentioned in headline, about, or experience
- **Publications and speaking** — books, articles, conference appearances
- **Endorsements and skills** — top skills indicate professional circles

Then search for **adjacent stakeholders** at the same organizations:

```
mcp__linkedin__search_people:
  keywords: [organization name]
  company: [organization name]
  location: "Kansas City"
```

Run this for the stakeholder's top 3-5 most connection-rich affiliations (boards, employers, churches). The goal is to find **who else** is in those organizations — especially people who might also appear in the prospect database.

**Rate limit awareness:** Track lookups. Stop LinkedIn searches if approaching 80 for the day. Report remaining quota to the user.

### Stage 3 — Web Research

Run targeted web searches to fill gaps LinkedIn doesn't cover:

1. **Board memberships:** `"{stakeholder name}" board OR trustee OR director "Kansas City"`
2. **Church affiliation:** `"{stakeholder name}" church OR congregation OR parish "Kansas City"`
3. **Civic and social:** `"{stakeholder name}" rotary OR chamber OR country club OR "Kansas City"`
4. **Philanthropy:** `"{stakeholder name}" foundation OR gift OR donor OR fundraiser "Kansas City"`
5. **Event co-attendance:** `"{stakeholder name}" gala OR luncheon OR awards "Kansas City" 2024 OR 2025 OR 2026`
6. **Family connections:** `"{stakeholder name}" spouse OR wife OR husband "Kansas City"` (only if relevant signals exist)
7. **News and features:** `"{stakeholder name}" Kansas City Business Journal OR Startland OR Flatland`

For each result, extract:
- The **organization or context** (e.g., "Nelson-Atkins Museum Board of Trustees")
- The **relationship type** (board, church, professional, social, civic, philanthropic, family, event)
- The **evidence** (URL or description)
- Whether the affiliation is **current or historical**

### Stage 4 — Cross-Reference Against Prospect Database

This is where connection mapping happens. For every affiliation discovered in Stages 1-3:

1. Search the prospect database for others at the same organization:
   - Grep prospect JSON files for the organization name
   - Check `fields.board_roles`, `fields.employer`, `fields.church_affiliations`, `fields.network_connections`
2. Search the stakeholder registry for other insiders at the same organization
3. For each match, record a **connection edge**

### Stage 5 — Synthesize Connection Map

Compile all discoveries into a structured connection map for this stakeholder.

---

## Output Format

For each stakeholder, write a JSON file to:
`~/Desktop/Dev/repos/non-profit-dashboard/public/data/stakeholder-connections/{stakeholder-id}.json`

```json
{
  "stakeholder_id": "ins-tim-smith",
  "stakeholder_name": "Tim Smith",
  "role": "board",
  "title": "Board Chair",
  "researched_at": "2026-03-22T14:30:00Z",
  "research_sources": ["linkedin", "web_search", "990_crossref", "fec_cogiving", "littlesis"],
  "linkedin_quota_used": 3,

  "profile": {
    "summary": "Board chair with 30+ years NPO fundraising leadership...",
    "location": "Kansas City, MO",
    "current_employer": "Non Profit DNA",
    "church": "Village Presbyterian Church",
    "neighborhood": "Prairie Village",
    "alma_maters": ["Liberty University"],
    "professional_focus": ["nonprofit fundraising", "faith-based development"]
  },

  "affiliations": [
    {
      "organization": "Non Profit DNA",
      "type": "employer",
      "role": "President",
      "status": "active",
      "since": "2000",
      "source": "linkedin",
      "connection_potential": "high",
      "notes": "Consulting practice — clients are NPO leaders, many likely in prospect DB"
    },
    {
      "organization": "Museum of the Bible",
      "type": "employer",
      "role": "Former CDO",
      "status": "historical",
      "period": "2014-2017",
      "source": "linkedin",
      "connection_potential": "moderate",
      "notes": "DC-based but faith/museum donor network may overlap KC"
    }
  ],

  "connections": [
    {
      "connected_to": {
        "id": "prospect-uuid-here",
        "name": "James Hebenstreit",
        "type": "prospect",
        "tier": 1
      },
      "connection_type": "board",
      "shared_context": "Both serve on Nelson-Atkins Museum Board of Trustees",
      "strength": "strong",
      "evidence": "Nelson-Atkins 2025 annual report",
      "evidence_url": "https://example.com/source",
      "status": "active",
      "discovered_via": "web_search",
      "approach_suggestion": "Tim mentions Youthfront's camp impact at the next Nelson-Atkins board dinner — natural peer conversation between fellow trustees."
    },
    {
      "connected_to": {
        "id": "ins-mike-king",
        "name": "Mike King",
        "type": "stakeholder",
        "role": "executive"
      },
      "connection_type": "professional",
      "shared_context": "Both former Youthfront executives; Tim was VP Development 1996-2000",
      "strength": "strong",
      "evidence": "LinkedIn employment history",
      "status": "active",
      "discovered_via": "linkedin"
    }
  ],

  "connection_summary": {
    "total_connections": 12,
    "prospect_connections": 7,
    "stakeholder_connections": 5,
    "by_type": {
      "board": 3,
      "professional": 4,
      "church": 2,
      "philanthropic": 2,
      "social": 1
    },
    "strongest_bridges": [
      "Nelson-Atkins Museum Board (3 prospects)",
      "Village Presbyterian Church (2 prospects)",
      "Non Profit DNA client network (2 prospects)"
    ]
  },

  "gaps_and_recommendations": [
    "Church affiliation unconfirmed — ask Tim directly",
    "Country club / social memberships unknown — high-value gap for Leawood/Mission Hills prospects",
    "Children's schools unknown — could unlock parent network connections",
    "Tim's consulting clients (Non Profit DNA) likely overlap with prospect DB but are not publicly listed"
  ],

  "new_stakeholder_candidates": [
    {
      "name": "Sarah Chen",
      "reason": "Co-trustee at Nelson-Atkins, appears connected to 4 Tier 1 prospects",
      "recommended_action": "Add to stakeholder registry and research"
    }
  ]
}
```

### After Each Stakeholder

1. Update `insiders.json` — fill in any new affiliations, church, or location data discovered
2. Update `insiders-linkedin.json` — if new LinkedIn data was pulled
3. Write the connection map JSON file
4. Report to the user:
   - Stakeholder name and role
   - Number of connections discovered (by type)
   - Top 3 strongest bridge opportunities
   - Any new stakeholder candidates discovered
   - Gaps that need human input
   - LinkedIn quota remaining

### After All Stakeholders (batch mode)

Write a master graph file to:
`~/Desktop/Dev/repos/non-profit-dashboard/public/data/stakeholder-connections/_graph.json`

```json
{
  "generated_at": "2026-03-22T16:00:00Z",
  "stakeholder_count": 17,
  "total_connections": 89,
  "total_unique_prospects_reached": 42,

  "edges": [
    {
      "from": "ins-tim-smith",
      "to": "prospect-uuid",
      "connection_type": "board",
      "shared_context": "Nelson-Atkins Museum Board",
      "strength": "strong"
    }
  ],

  "hub_organizations": [
    {
      "organization": "Nelson-Atkins Museum",
      "stakeholders_connected": ["ins-tim-smith", "ins-cheryl-reinhardt"],
      "prospects_connected": ["uuid-1", "uuid-2", "uuid-3"],
      "total_people": 5,
      "connection_type": "board"
    }
  ],

  "multi_path_prospects": [
    {
      "prospect_id": "prospect-uuid",
      "prospect_name": "James Hebenstreit",
      "paths": 3,
      "connectors": ["ins-tim-smith", "ins-ed-garlich", "ins-mike-king"],
      "strongest_path_score": 87
    }
  ],

  "new_stakeholder_candidates": [
    {
      "name": "Sarah Chen",
      "nominated_by": ["ins-tim-smith", "ins-cheryl-reinhardt"],
      "reason": "Appears in 2 stakeholder connection maps, connected to 4 Tier 1 prospects",
      "recommended_priority": "high"
    }
  ],

  "coverage_gaps": [
    "3 board members have no LinkedIn profile — manual research needed",
    "Church affiliations confirmed for only 4 of 17 stakeholders",
    "No stakeholder coverage in healthcare/hospital sector"
  ]
}
```

---

## Key Design Rules

- **Incremental** — Skip stakeholders who already have a connection map file unless `--refresh` is used. Always check for existing data before researching.
- **Source everything** — Every connection must have a `discovered_via` field and evidence. No hallucinated connections.
- **LinkedIn budget** — Track daily usage. Never exceed 80 lookups. Report quota after each stakeholder.
- **Prospect matching** — When cross-referencing, use fuzzy matching (case-insensitive, handle middle names/initials). Flag uncertain matches for human review.
- **Stakeholder discovery** — If research reveals someone who is clearly a "hidden stakeholder" (e.g., a major donor's spouse who sits on 3 boards with Tier 1 prospects), add them to `new_stakeholder_candidates` — do NOT auto-add to the registry without user confirmation.
- **Privacy** — Do not record personal phone numbers, home addresses, or non-public email addresses. Stick to professional affiliations and publicly available information.
- **Idempotent writes** — Connection map files can be safely overwritten. The `researched_at` timestamp indicates freshness.
- **Confirm before batch** — If `--all` is used and there are more than 5 unresearched stakeholders, show the list and estimated LinkedIn quota cost before proceeding. Ask the user to confirm.

## Error Handling

- **LinkedIn session expired** — Stop and instruct user to run `uvx linkedin-scraper-mcp --login`
- **LinkedIn rate limit approaching** — Warn at 60 lookups, hard stop at 80. Save progress and report what was completed.
- **Stakeholder not found in registry** — Suggest using `--add` to register them first
- **No prospect matches found** — This is a valid outcome. Record it in the connection map with empty `connections` array and note in `gaps_and_recommendations`.
- **Ambiguous prospect match** — Record the match with `"confidence": "low"` and flag for human review

## Progress Reporting

After completing research for each stakeholder, output a summary block:

```
## Stakeholder Research Complete: Tim Smith (Board Chair)

### Connections Discovered: 12
- Board co-service: 3 (Nelson-Atkins, Kauffman Foundation, UMKC Trustees)
- Professional overlap: 4 (Non Profit DNA clients, Museum of the Bible alumni)
- Church: 2 (Village Presbyterian)
- Philanthropic: 2 (KC Community Foundation, Midwest Trust)
- Social: 1 (Mission Hills Country Club — unconfirmed)

### Top Bridge Opportunities
1. **James Hebenstreit** via Nelson-Atkins Board (strength: strong)
2. **Margaret Sullivan** via Village Presbyterian (strength: moderate)
3. **David Chen** via Kauffman Foundation (strength: moderate)

### New Stakeholder Candidates
- Sarah Chen — co-trustee at Nelson-Atkins, connected to 4 Tier 1 prospects

### Gaps Needing Human Input
- Country club membership unconfirmed
- Children's schools unknown
- Non Profit DNA client list not publicly available

### LinkedIn Quota: 74/100 remaining today
```
