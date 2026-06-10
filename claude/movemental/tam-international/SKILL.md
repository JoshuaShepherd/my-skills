---
name: tam-international
description: Discover and research international movement leaders outside US/anglophone networks — mapping the global TAM
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM International: Map the Global Movement Leader Landscape

Systematically discover movement leaders operating internationally — outside the US evangelical echo chamber. The movement is inherently global (Chinese house church, Latin American base communities, African independent churches, European new monasticism), and the TAM must reflect this.

## Invocation

```
/tam-international $ARGUMENTS
```

**Arguments:**
- A region, country, network, or directive. Examples:
  - `/tam-international Latin America` — search a region
  - `/tam-international South Korea` — search a specific country
  - `/tam-international Lausanne Movement` — mine an international network
  - `/tam-international majority world` — focus on Global South leaders
  - `/tam-international European new monasticism` — search a movement stream
  - `/tam-international` (no args) — full global sweep

---

## Before Starting

1. **Read the master list** to check existing international representation
2. **Read the rubric** — the Seven Gates and 100-point scoring apply globally, but with cultural sensitivity
3. **Note the existing international candidates** on the list (e.g., Michael Frost - Australia, Mark Sayers - Australia, Evan Mawarire - Zimbabwe, Andrew Jones - Europe)

---

## Regional Search Strategy

### Region 1: Australia / New Zealand / Pacific
**Why high priority**: Forge originated here; Michael Frost, Mark Sayers already on list; strong missional movement tradition

**Search vectors:**
- Forge Australia/NZ faculty and alumni leaders
- Morling College, Whitley College, Vose Seminary missional faculty
- Australian Church Planting networks
- New Zealand church multiplication leaders
- Pacific Island movement leaders with English-language content

### Region 2: United Kingdom / Ireland
**Why high priority**: Fresh Expressions, new monasticism, missional pioneer movement well-established

**Search vectors:**
- Fresh Expressions Network leaders and practitioners
- Church Mission Society (CMS) pioneers and faculty
- Church Army, Urban Expression, 24-7 Prayer leadership
- St. Mellitus College, Ridley Hall missional theology faculty
- Northern/Scottish church planting networks
- New monastic communities (Northumbria, Iona, etc.)

### Region 3: Continental Europe
**Search vectors:**
- European Church Planting Network (ECPN) leaders
- Forge Europe, 24-7 Prayer European leaders
- New monastic movements (Taizé adjacent, Protestant new monasticism)
- Scandinavian missional church leaders
- German/Dutch missional ecclesiology thinkers
- Eastern European movement leaders with English content

### Region 4: Sub-Saharan Africa
**Why critical**: Fastest-growing church globally; massive organic movement tradition

**Search vectors:**
- African church multiplication movement leaders
- Disciple Making Movement (DMM) practitioners with published content
- African theological educators writing in English
- Leaders of African-initiated churches with global influence
- South African missional leaders (Stellenbosch, UNISA networks)
- East African revival tradition leaders with contemporary voice

### Region 5: Latin America
**Search vectors:**
- Latin American Theological Fellowship (FTL/CLADE) leaders
- Misión Integral practitioners with English-language content
- Brazilian church planting movement leaders
- Colombian, Argentine, Mexican missional thought leaders
- COMIBAM (Cooperación Misionera Iberoamericana) leadership
- René Padilla / Samuel Escobar lineage of holistic mission thinkers

### Region 6: East Asia
**Search vectors:**
- Chinese house church movement thinkers with English publications
- South Korean missional church leaders
- Japanese/Taiwanese church planting leaders
- Back to Jerusalem movement voices
- Asian diaspora leaders bridging East/West

### Region 7: South / Southeast Asia
**Search vectors:**
- Indian church multiplication leaders with English content
- Filipino missional practitioners
- Indonesian/Malaysian movement leaders
- South Asian theological voices (SAIACS, ATC networks)
- Myanmar, Thailand, Vietnam underground/organic church voices

### Region 8: Middle East / North Africa
**Search vectors:**
- Persecution-context movement leaders with public profile
- Lebanese, Egyptian Christian thought leaders
- Iranian diaspora church leaders
- Middle Eastern church planting networks
- Arabic-language Christian authors with English translations

---

## Phase 2: Search Execution

For each region/focus:

1. **Run web searches** combining region + movement keywords:
   - `"[region] church planting movement leader author"`
   - `"[region] missional church practitioner"`
   - `"[region] disciple making movement leader"`
   - `"[country] Christian thought leader multiplication"`
   - `"[network/org] leadership faculty speakers"`

2. **Mine international networks:**
   - Lausanne Movement participants and resource authors
   - World Evangelical Alliance leadership
   - Langham Partnership scholars
   - Oxford Centre for Mission Studies alumni
   - International Journal of Frontier Missiology authors
   - Global Church Movements affiliated leaders

3. **Check international publishers:**
   - Langham Literature / Hippo Books (Africa)
   - Regnum Books International
   - William Carey Library
   - SPCK (UK)
   - Wipf & Stock international authors

---

## Phase 3: Cultural Sensitivity in Evaluation

When applying the Seven Gates and rubric internationally:

| Gate/Criteria | Cultural Adaptation |
|--------------|-------------------|
| Audience Size | Adjust expectations — 5K engaged followers in a country of 10M Christians may be more significant than 50K in the US |
| Content Forms | Books may not be the primary form — teaching series, oral tradition, community curricula matter |
| Digital Presence | Many majority-world leaders have minimal digital footprint despite massive movement impact |
| Revenue Streams | Bivocational is the norm, not the exception; "revenue potential" means different things |
| Network Connections | May not connect to US networks but may be deeply networked regionally |
| Language | English-language content is a practical requirement for the platform but shouldn't be the only signal |
| Multiplication Evidence | May be the STRONGEST signal — majority-world movements often far exceed Western multiplication rates |

### Adjusted Gate 7: Network Coherence (International)
Does this leader's work represent a **genuine extension** of the movement (missional-incarnational, multiplication, Kingdom) into their cultural context? Or is it a disconnected parallel?

---

## Phase 4: Output

For each new international candidate discovered:

### Quick Profile
```markdown
## [Full Name] — [Country/Region]

**Domain**: [primary domain]
**Language(s)**: [languages of content]
**Key Affiliations**: [orgs, networks, institutions]
**Notable Works**: [books, courses, movements catalyzed]
**English Content Available**: [yes/no/partial — specify what]
**Digital Presence**: [brief assessment]
**Estimated Reach**: [audience indicators]
**Connection to Existing TAM**: [names of connected candidates, if any]
**Initial Gate Assessment**: [PASS ALL / FAIL: Gate X / NEEDS RESEARCH]
**Notes**: [what makes them distinctive or important]
```

### Regional Summary

**Output file**: `intelligence/leader-research/international/[region-slug].md`

```markdown
# International TAM: [Region Name]

## Summary
- **Candidates found**: [count]
- **Strongest candidates**: [top 3-5 names]
- **Key networks identified**: [regional networks worth deeper mining]
- **Language considerations**: [English content availability]

## Candidates
[Quick profiles for all candidates found]

## Regional Insights
- [What does the movement look like in this region?]
- [How does it differ from US expression?]
- [What unique contributions could these leaders bring to the scenius?]

## Gaps and Next Steps
- [What couldn't be found? Who is likely missing?]
- [Regional networks to mine deeper]
- [Translation/language barriers to address]
```

### Update Master List
Add qualified international candidates to `01-MASTER-RANKED-LIST.md` in the unscored section with a `[INTERNATIONAL]` tag.

---

## Key Rules

1. **The movement is global by nature.** Alan Hirsch's own framework draws on Chinese house church, early church, and global movements. The TAM must reflect this.
2. **English-language content is a practical requirement** but should not be the only discovery signal. Leaders who publish in other languages but have some English-language content are valid candidates.
3. **Adjust audience size expectations by context.** A leader with 3,000 engaged followers in a country with a small Christian population may have outsized influence.
4. **Multiplication evidence may be strongest internationally.** Disciple-making movements in India, China, and Africa often achieve multiplication rates that dwarf Western church growth.
5. **Never fabricate international candidates.** The temptation is high because data is scarcer — resist it.
6. **Regional networks are goldmines.** One well-connected regional leader can surface 10+ candidates.
7. **Flag language barriers honestly.** If a leader has zero English content, note the opportunity but be transparent about the platform limitation.
8. **Diversity is not the goal — movement fidelity is.** International candidates must pass the same gates. But recognizing that movement DNA expresses differently across cultures is essential.
