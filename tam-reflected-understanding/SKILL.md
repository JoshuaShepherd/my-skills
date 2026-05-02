---
name: tam-reflected-understanding
description: Generate a reflected understanding document for a movement leader — a second-person mirror of their calling, audience, content, constraints, and credibility
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# TAM Reflected Understanding: Mirror a Leader's Reality

Generate a reflected understanding document for a single movement leader. This is a second-person ("you") document that speaks the leader's reality back to them — familiar, true, with edges that deepen. It is the document that makes them say "you get me."

## Invocation

```
/tam-reflected-understanding $ARGUMENTS
```

**Arguments:**
- A leader's full name. Examples:
  - `/tam-reflected-understanding Brad Brisco`
  - `/tam-reflected-understanding Mark Sayers`

---

## Before Starting

1. **Read the canonical template** at the movemental-ai repo: `_docs/_prompts/generate-reflected-understanding.md` — this defines the required structure
2. **Read the Alan Hirsch exemplar** at: `_docs/_prompts/alan-hirsch-reflected-understanding.md` (in the movemental-ai repo) — this is the gold standard for tone, length, and pattern
3. **Check for existing profile research** at `intelligence/leader-research/profiles/[slug]/` in this repo
4. **If no profile exists**, run `/tam-profile [name]` first or gather research via web search

---

## Required Sources

The reflected understanding must be grounded in **verified research**, not assumptions. Use these sources in order of priority:

1. **Existing profile** at `intelligence/leader-research/profiles/[slug]/` (summary, gap-analysis, content-analysis, movemental-fit, affiliations)
2. **Live web research** — their website, books, social media, published interviews, podcast appearances
3. **Existing TAM data** — master list entry, candidate profile in `02-CANDIDATE-PROFILES.md`

**Never invent facts.** If information isn't available (e.g., royalty details, specific revenue), either omit or phrase generally ("your publisher," "your current digital reach") without fabricating numbers.

---

## Document Structure

Write in **second person ("you")** throughout. The reader IS the leader. Use the **common frame** (what all movement leaders share) + **dynamic details** (their specific facts).

### Section 1: Title and Intent

```markdown
# [Full Name]: Reflected Understanding

A concise reflection spoken back so the language could be endorsed — familiar, but with edges that deepen.
```

### Section 2: Calling

- **Common**: Success is formation and multiplication; not selling a brand; thinking in terms of movement
- **Dynamic**: THIS leader's framing, language, role, orgs, books, primary contribution
- One short paragraph

### Section 3: Audience

- **Common**: Movement-oriented; multiplication, sentness, formation; mix of pastors, academics, practitioners, international
- **Dynamic**: THIS leader's personas (2-4 bullets if research supports), their TAM or gap (who knows them vs who would be formed if they found the work)
- One short paragraph + optional persona bullets

### Section 4: Existing Content (Before the Platform We're Building)

- **Common**: They already have a body of work; gap is circulation and coherence; offline vs online; silos; the work doesn't "move"
- **Dynamic**: THIS leader's exact locations (sites, books, orgs, conferences, podcasts), main digital asset, content forms and themes
- **NOTs list**: Only the NOTs that apply to THIS leader with THEIR examples:
  - Not translated
  - Not structured/repurposed
  - Not interconnected
  - Not owned/unified
  - Not legible to systems
  - Not optimized for discoverability (SEO/GEO)
  - Not connected to AI that reflects their voice
- End with: "Movemental is built to speak to these NOTs so your content can move."
- One or two short paragraphs + the NOT list

### Section 5: Constraints

- **Common**: Time and attention are the limit; at capacity; cannot become full-time content operator; the issue is capacity, not desire
- **Dynamic**: THIS leader's roles and time sinks, budget reality
- One short paragraph

### Section 6: Commerce

- **Common**: No obvious viable path; trade publishing vs "own platform"; the system isn't built for people like them
- **Dynamic**: THIS leader's publisher, current digital revenue, real commerce (authority driving speaking, consulting, training)
- One short paragraph

### Section 7: Credibility (summation)

- **Common**: Offline/in-the-room credibility is high; online it's partial, fragmented, invisible; gap wasn't fixable before without agencies/budgets/time; now possible
- **Dynamic**: THIS leader's "in the room" vs "online" reality
- One short paragraph

### Section 8: Closing

One sentence: "This document is a reflected understanding for [Full Name], grounded in research and documentation, intended to be right to the point, true, and valuable."

---

## Output

**File path**: `intelligence/leader-research/reflected-understandings/[slug].md`

Example: `intelligence/leader-research/reflected-understandings/mark-sayers.md`

---

## Quality Checklist

Before saving:

- [ ] Every claim is supported by research (no invented stats, deals, or roles)
- [ ] Second person ("you") throughout; no "leaders like you" or generic phrasing where the leader's name or detail fits
- [ ] Each section uses the common frame THEN the dynamic detail
- [ ] NOTs list only includes items that apply to THIS leader with THEIR examples
- [ ] Markdown is clean (headings, bullets, bold/italic matching the Alan Hirsch example)
- [ ] The document feels both shared and personal — they should feel part of a cohort, not a generic template
- [ ] Tone is respectful, honest, and slightly prophetic — not salesy, not flattering, not clinical

---

## Key Rules

1. **Never fabricate.** If you don't have specific data, phrase at a general level or omit.
2. **This is NOT a sales pitch.** It's a mirror. The leader should recognize themselves, not feel sold to.
3. **Common + Dynamic pattern is mandatory.** Lead with shared truth, complete with specific facts.
4. **Use "you" with concrete detail**, never "leaders like you."
5. **The NOTs are the operational core** — they show the leader exactly what Movemental solves for them specifically.
6. **Requires research first.** If no profile exists in `intelligence/leader-research/profiles/[slug]/`, either run `/tam-profile` first or conduct sufficient web research to ground every claim.
7. **Alan Hirsch's reflected understanding is the benchmark.** Match its tone, depth, and specificity.
8. **One leader per document.** Never batch multiple leaders into one reflected understanding.
