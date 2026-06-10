---
name: article-audit
description: Audit a complete article against all criteria — Alan's five voice markers, SEO/GEO requirements, section architecture, corpus citation quality, pillar alignment, and CTA. Returns per-criterion scores, specific failing passages, and a prioritized revision list. Use before publishing any article, or to diagnose why an article isn't performing.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit this article: $ARGUMENTS

$ARGUMENTS should be either: (a) a file path to an existing article markdown file, or (b) the article content pasted directly. If neither, ask the user to provide the article.

---

## What This Audit Covers

Six audit dimensions, each scored independently:

1. **Voice Fidelity** — Alan's five markers scored 0.0–1.0 each + failure mode check
2. **Section Architecture** — mandatory sections present, word counts in range, order correct
3. **SEO Requirements** — keyword placement, H structure, meta fields, URL slug, internal links
4. **GEO Requirements** — definition anchor quality, entity disambiguation, citation quality, FAQ presence
5. **Corpus Citation** — passages grounded in Alan's actual books, citations formatted correctly, no invented quotes
6. **Pillar & Funnel Alignment** — pillar assignment correct, CTA present and linked, no orphan content

---

## Dimension 1: Voice Fidelity

Score each marker 0.0–1.0 based on presence, density, and authenticity.

### Marker 1: Christocentric Anchoring (weight: 30%, target: ≥0.7)

Count explicit references to: Jesus, Christ, Lord, Kingdom, Gospel, sent by God, mission of God, missio Dei.

- **≥0.7 (pass):** 2–3 explicit references in the body; at least one in the opening and one in the close; grounded in Jesus's mission, not just God generically
- **0.4–0.6 (weak):** References present but thin; mostly God-language without Christological specificity; missing from opening or close
- **<0.4 (fail):** Fewer than 2 references; or references are decorative rather than load-bearing; Jesus not connected to the argument

Score and quote the specific passages that carry (or fail to carry) this marker.

### Marker 2: Pastoral Warmth (weight: 20%, target: ≥0.5)

Count "we," "you," "I" instances. Check distribution: target is 45% "we", 35% "you", 20% "I".

- **≥0.5 (pass):** Relational, invitational language throughout; reader feels included not lectured; "I" present but not dominant
- **0.3–0.5 (weak):** Third-person dominant; or "you" used preachy/prescriptive rather than invitational; or "I" absent (feels impersonal)
- **<0.3 (fail):** Academic tone; no reader address; feels like a paper, not a conversation

Check for generic motivational language ("you've got this!") — flag as failure even if warmth score is otherwise passing.

### Marker 3: Narrative Imagery (weight: 15%, target: ≥0.6)

Count metaphors and analogies. Target: ~8.5 per 1000 words. Check for Alan's primary metaphor systems.

- **Movement/DNA:** Apostolic Genius, movement DNA, genetic code, dormant potential, fractal patterns
- **Organic/biological:** seed, vine, tree, growth, organism, health, DNA
- **Journey/travel:** path, road, pilgrimage, quest, hitting the road with Jesus
- **Ocean/water:** streams, currents, red ocean vs. blue ocean, scattering

- **≥0.6 (pass):** Multiple metaphor systems present; metaphors are load-bearing (they carry the argument) not decorative
- **0.4–0.6 (weak):** Some metaphors but thin; only one system used; metaphors feel generic rather than Alan's signature
- **<0.4 (fail):** Bare prose; metaphors absent or only clichés

Score and name the dominant metaphor systems used.

### Marker 4: Theological Depth (weight: 10%, target: ≥0.7)

Count: theological terms, biblical references, historical examples with specific data.

Historical examples require specificity to score:
- "The early church grew" → 0 (too vague)
- "The early church grew from 25,000 to 20 million between AD 100–310" → 1 (counts)

- **≥0.7 (pass):** 1–2 historical examples with specific data; biblical integration woven not proof-texted; theological concepts named and unpacked
- **0.4–0.7 (weak):** Historical examples vague; or scripture quoted sermonically; or theology stays at surface
- **<0.4 (fail):** No historical grounding; no scripture; generic spirituality language

### Marker 5: Prophetic Intensity (weight: 25%, target: 0.5–0.8)

Count: questions, urgency statements, reframing moves, challenge language.
Target: ~3.2 questions per 1000 words. Also check calibration — too high is preaching, too low is passive.

- **0.5–0.8 (pass):** Questions present at openings and transitions; urgency felt; article challenges rather than confirms existing assumptions; balance with pastoral warmth
- **0.3–0.5 (weak):** Too gentle; no productive tension; reads as information delivery not prophetic challenge
- **>0.8 (over):** Hectoring; all challenge no warmth; reader feels lectured

### Overall Voice Coherence Score

Weighted average: `(Marker1 × 0.30) + (Marker2 × 0.20) + (Marker3 × 0.15) + (Marker4 × 0.10) + (Marker5 × 0.25)`

**Target: ≥0.75.** Below 0.75, the article should not publish before revision.

### Failure Mode Check

Flag any of these as automatic issues requiring revision regardless of scores:

- [ ] **Antithesis patterns** — "not X, but Y"; "Instead of X, we should Y"; "Contrary to X"
- [ ] **Corporate consultant vocabulary** — "leverage," "optimize," "best practices," "scalable," "key takeaways," "actionable insights"
- [ ] **Detached academic phrasing** — "The ecclesiological implications suggest..."; "Research indicates..."; "It could be argued that..."
- [ ] **Rushing to practice** — application appears before theology and meaning are established (before the 60% mark)
- [ ] **Homiletical opening** — article opens with a scripture quotation or "As [verse] says..."
- [ ] **Missing first-person narrative** — no "I've seen...", "Let me walk you through...", "My experience..."
- [ ] **Generic motivational language** — "You've got this!" "Believe in yourself!" "Start your journey today!"
- [ ] **Missing Christocentric anchor** — movement/mission language not grounded in Jesus specifically

---

## Dimension 2: Section Architecture

Check that all mandatory sections are present, in the correct order, and within word count range.

| Section | Required | Word Count Target | Check |
|---------|----------|-------------------|-------|
| Opening hook (no heading) | Yes | 150–250 | Present? Starts with question/reframe (not scripture)? Keyword in first 100 words? |
| **H2: What Is [Term]?** | Yes | 200–350 | Present? Definitional? GEO-ready? |
| **H2: Stakes/Problem** | Yes | 250–400 | Present? Diagnosis + historical parallel? |
| **H2: Core Teaching × 2–4** | Yes | 600–1,200 total | Present? Multiple H3s? H2s as questions? Corpus cited? |
| **H2: Common Misunderstandings** | Yes | 300–500 | Present? 2–3 H3s? Dissolution not just negation? |
| **H2: Biblical Foundation** | Yes (may merge) | 200–350 | Scripture woven? Not proof-texted? Not leading? |
| **H2: What This Means in Practice** | Yes | 250–400 | Present? Prose not steps? Application earned? |
| **H2: How This Connects** | Tier 1 required, others optional | 150–250 | Present (Tier 1)? Internal links? |
| CTA / Formation Invitation | Yes | 100–200 | Present? One CTA? Prophetic close? |
| FAQ | Optional but recommended | 200–400 | Present? 3–5 Q&As? Complete standalone answers? |

**Total word count check:**
- Tier 1: 3,500–4,500 — flag if outside range
- Tier 2: 2,200–3,200 — flag if outside range
- Tier 3: 1,500–2,200 — flag if outside range

**Order check:** Sections must follow the sequence above. Application (Section 7) must come after Core Teaching (Section 4). Flag if not.

---

## Dimension 3: SEO Requirements

Score pass/fail for each item:

**H Structure:**
- [ ] Primary keyword in H1 (article title)
- [ ] Primary keyword appears within first 100 words of body
- [ ] Primary keyword in at least one H2
- [ ] H2s mirror real search queries ("What Is X?", "How Does X Work?", "Why Does X Matter?")
- [ ] H3s are genuine sub-points, not just continuations

**Keyword distribution:**
- [ ] Primary keyword: natural density, not stuffed (flag if appears more than once every 100 words)
- [ ] 3–5 semantic variants present in body
- [ ] GEO disambiguation phrase present: "Alan Hirsch [concept]" or "Alan Hirsch developed..."

**Meta fields (check if present in frontmatter):**
- [ ] `meta_title` — 50–60 characters, leads with keyword, ends with `— Alan Hirsch`
- [ ] `meta_description` — 140–160 characters, includes keyword, contains question or tension
- [ ] `slug` — short, keyword-anchored, lowercase, hyphens, no stop words

**Internal links:**
- [ ] Minimum 3 internal links (to related articles, pathways, or courses)
- [ ] Maximum 8 internal links
- [ ] Anchor text is natural and descriptive (not "click here" or "read more")

---

## Dimension 4: GEO Requirements

Score pass/fail:

**Definition Anchor (Section 2):**
- [ ] Clean opening definition sentence (20–30 words, complete, crisp)
- [ ] Self-contained — a reader can understand the concept from this section alone
- [ ] Entity disambiguation: attributes the concept to Alan Hirsch explicitly
- [ ] Does not open with "According to Alan Hirsch..." (too academic) — embed the attribution naturally

**Factual specificity:**
- [ ] Historical examples include specific numbers, dates, or locations (not vague)
- [ ] Framework components are named precisely (APEST = Apostolic, Prophetic, Evangelistic, Shepherding, Teaching — not just "five gifts")

**First-person authoritative statements:**
- [ ] At least 2 first-person passages (increases GEO citation rate)
- [ ] Statements are grounded in known biographical facts or corpus (not invented)

**Citation quality:**
- [ ] Book sources cited in correct format: `*Book Title* — ch[N] "[Chapter Title]"`
- [ ] No invented Alan quotes or paraphrases without attribution
- [ ] Direct quotes are verbatim from corpus (not close paraphrases presented as quotes)

**FAQ:**
- [ ] FAQ section present (optional but recommended — flag if absent)
- [ ] Each Q&A is complete and self-contained
- [ ] Questions reflect real search phrasing

---

## Dimension 5: Corpus Citation

- [ ] Article draws on Alan's actual books, not general theological knowledge alone
- [ ] At minimum 1–2 direct citations from the corpus (blockquotes or close-referenced paraphrases)
- [ ] Citations use the correct format
- [ ] No invented quotes (flag any Alan-attributed statement not verifiable in corpus)
- [ ] Books cited are appropriate to the pillar (see pillar-to-book map in `article-corpus`)

If the article cites Alan without a book source, flag each instance for verification.

---

## Dimension 6: Pillar and Funnel Alignment

- [ ] Article is clearly assigned to one of the six pillars
- [ ] Topic fits the pillar assignment (not cross-pillar confusion)
- [ ] One primary CTA present, linking to a pathway or course
- [ ] CTA is appropriate to the pillar (not a random cross-sell)
- [ ] No orphan content — the article connects to something deeper in the funnel
- [ ] If Tier 2/3: link to the Tier 1 pillar page is present

---

## Audit Output Format

Return the audit as:

---

# Article Audit: [Article Title or File Path]

**Overall Readiness:** [PUBLISH READY / NEEDS REVISION / MAJOR REVISION REQUIRED]
**Word Count:** [actual] / [target range]
**Tier:** [1/2/3] — **Pillar:** [name]

---

## Voice Fidelity Scores

| Marker | Score | Target | Status |
|--------|-------|--------|--------|
| Christocentric Anchoring | 0.X | ≥0.7 | ✓ / ✗ |
| Pastoral Warmth | 0.X | ≥0.5 | ✓ / ✗ |
| Narrative Imagery | 0.X | ≥0.6 | ✓ / ✗ |
| Theological Depth | 0.X | ≥0.7 | ✓ / ✗ |
| Prophetic Intensity | 0.X | 0.5–0.8 | ✓ / ✗ |
| **Overall Coherence** | **0.X** | **≥0.75** | **✓ / ✗** |

**Failure modes found:**
- [List specific failures with quoted passages]

---

## Section Architecture

| Section | Present | Word Count | Status | Notes |
|---------|---------|------------|--------|-------|
| Opening hook | ✓/✗ | [N] | ✓/✗ | |
| What Is [Term]? | ✓/✗ | [N] | ✓/✗ | |
| [etc.] | | | | |

---

## SEO Score: [X]/[total checks] passing

**Failures:**
- [specific items failing, with what's needed to fix]

---

## GEO Score: [X]/[total checks] passing

**Failures:**
- [specific items failing]

---

## Corpus Citation: [GROUNDED / WEAK / UNVERIFIED]

**Issues:**
- [specific unattributed or suspect passages]

---

## Pillar & Funnel: [ALIGNED / MISALIGNED]

**Issues:**
- [specific alignment problems]

---

## Priority Revision List

Rank issues by impact (fix these first):

1. **[CRITICAL]** [Issue] — [What to do to fix it]
2. **[HIGH]** [Issue] — [Fix]
3. **[MEDIUM]** [Issue] — [Fix]
4. **[LOW]** [Issue] — [Fix]

---

## Publish Decision

**[PUBLISH READY]** — All dimensions pass. Ready to go.

**[NEEDS REVISION]** — Minor issues. Fix the Priority Revision List items, then publish.

**[MAJOR REVISION REQUIRED]** — Voice coherence below 0.6, or multiple mandatory sections missing, or corpus citations unverifiable. Significant rewrite needed before this article should go live.
