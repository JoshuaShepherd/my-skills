---
name: movemental-narrative-audit
description: >
  Audits any platform page’s copy, narrative arc, mental models, and business
  positioning against Movemental’s canonical story (dual intelligences,
  six-stage progression, infrastructure thesis, scenius/credibility). Use when
  the user asks for narrative alignment, messaging audit, “does this match our
  model”, framework drift, editorial re-alignment, or copy QA against the
  fragmentation book, fragmentation page, home page, docs/articles, or
  docs/design/DESIGN.md.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, Write
---

# Movemental narrative alignment audit

Use this skill when the goal is **strategic and editorial alignment** — not pixel-level design QA. For full UI/design/conversion audits, run **`page-audit`** after or in parallel.

---

## Ground truth — read before judging

Establish shared vocabulary from these artifacts (read what is relevant to the page under audit; at minimum skim the starred items):

| Priority | Artifact | Why it matters |
| -------- | -------- | -------------- |
| ★ | `src/components/sections/home/home-hero.tsx` + `home-page-content.tsx` | Live product headline, dual-intelligence promise, CTAs to system + fragmentation story |
| ★ | `src/app/(site)/fragmentation/page.tsx` + `src/components/sections/fragmentation-story/fragmentation-story-content.ts` | Six-stage narrative, audience rails, metadata framing |
| ★ | `docs/book-development/fragmentation-manuscript-ordered/` especially `05-the-six-stages-at-a-glance.md`, `02-two-intelligences.md`, `03-fragmentation-is-structural.md` | Canonical definitions, ordering constraints, stall patterns |
| ★ | `docs/articles/two-intelligences-integration.md`, `docs/articles/the-story-of-movemental.md` | Operating language: two intelligences, infrastructure, ownership, scenius |
| | Other `docs/articles/*.md`, `docs/content/articles/*.md` | Topic depth, playbooks, workflows — use when the audited page matches that domain |
| | `docs/design/DESIGN.md` §1 (pillars, quality bar) | Editorial voice: clarity, trust through inspectability, one voice, calm motion |
| | `docs/business-docs/` (as needed) | MVP, positioning, audience research — for claims that touch product scope |

**Do not invent Movemental doctrine.** If a claim is not supported by the above after reading, flag it as **unsupported** or **drift**.

---

## North star (synthesis — verify against sources)

1. **Problem frame:** Organizations and leaders pay a **fragmentation tax** on **two intelligences** — **informational** (corpus, frameworks, media, data) and **relational** (people, trust, communication graph). Fixes framed only as “content” or “tools” misread the structure.
2. **Offer frame:** Movemental is **digital infrastructure** (foundation: library, graph, voice, pathways), not “a website” or generic AI content — **AI amplifies grounded corpus**, it does not replace voice or relationship.
3. **Progress model:** **Six ordered stages** — Fragmentation → Integration → Activation → Formation → Multiplication → Movement. Skipping Integration produces fluent surface without load-bearing foundation; **most stalls are Fragmentation → Integration**.
4. **Moral / credibility frame:** Credibility that survives AI noise is **embedded in networks of verified humans** (scenius); formation requires **relationship** at the seam with information.
5. **Product principles** (from canonical articles): e.g. formation over pure growth, humans-over-hacks, technology ordered under mission — **only cite principles explicitly present in the artifacts you read**.

---

## Audit dimensions

Score each **Aligned / Partial / Misaligned / N/A** with one sentence of evidence (quote or section id).

### 1. Copy — language and claims
- Headlines and CTAs use **shared vocabulary** (fragmentation, integration, foundation, pathway, corpus, formation, etc.) consistently with home + fragmentation story, or deliberately define new terms.
- No **false sequencing** (e.g. promising “movement” or “multiplication” while ignoring integration).
- **Audience** (movement leader, nonprofit, church, institution) is explicit where the page is audience-specific.

### 2. Narrative — arc and tension
- Clear **problem → reframe → mechanism → proof/next step** (editorial arc may vary by page type).
- **Stakes** match the book’s diagnosis (tax, dual fragmentation, AI visibility) without exaggeration.
- **CTA** matches funnel stage (e.g. education vs contact vs product).

### 3. Framework — mental model integrity
- **Two intelligences** invoked correctly when the page is about org capacity, AI, or “systems.”
- **Six stages** named in correct order if referenced; dependencies respected (no “activation” without integrated foundation).
- Distinguish **symptoms** (more content, new tool) from **foundation** work when prescribing fixes.

### 4. Business model — positioning
- **Infrastructure / ownership / network** claims align with `the-story-of-movemental.md` and home metadata — no contradictions with curated network, leader revenue, or transparency themes unless intentionally scoped.
- Pricing, services, or “how it works” pages tie outcomes to **integration → downstream stages**, not magic AI.

### 5. Design charter overlap (light touch)
- If copy fights **DESIGN.md** pillars (e.g. hype that breaks “trust through inspectability”), note under **Copy** or **Narrative** — defer visual token violations to `page-audit`.

---

## Workflow

1. **Identify** route + primary content files (`page.tsx`, section components, `docs/content` if MD-driven).
2. **Load** starred ground-truth files above (and domain articles if applicable).
3. **Extract** the page’s implied thesis, audience, stage emphasis, and CTAs.
4. **Score** the five dimensions; list **drift patterns** (generic SaaS, tool-first, AI-replacement, skip-integration, etc.).
5. **Recommend** re-alignment: prioritized bullets — **rewrite** (exact placement: hero, section X), **restructure** (move proof earlier), **add link** (fragmentation, evidence), **remove claim**.
6. **Optional fix prompt** — short block the user can paste to an agent: goal, files, non-negotiables, forbidden phrases.

---

## Output template

```markdown
# Narrative alignment audit — <Page title / route>

## Executive read
[2–3 sentences: who this page is for, what it currently “says,” biggest gap vs canonical story]

## Ground truth cited
- [List files actually read]

## Dimension scores
| Dimension | Score | Notes |
| --------- | ----- | ----- |
| Copy | | |
| Narrative | | |
| Framework | | |
| Business model | | |
| Design charter (copy-level) | | |

## Findings (prioritized)
### Must fix (misleading or off-model)
### Should improve (partial alignment)
### Optional polish

## Re-alignment recommendations
1. …
2. …

## Agent fix prompt (optional)
[Paste-ready block]
```

---

## Related skills

- **`page-audit`** — UI, DESIGN.md tokens, Stitch fidelity, technical architecture.
- **`design-audit`** — Broader DESIGN.md compliance.
- **`pathway-audit`** / **`article-audit`** — When the target is a pathway or longform article specifically.

---

## Additional reference

For a longer article index and example drift patterns, see [reference.md](reference.md).
