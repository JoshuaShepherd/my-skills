---
name: home-consult
description: Strategic consultation for a movement leader home page — mandatory sections rubric, scroll-stop strategy (Spline/NB2/GSAP), copy evaluation, and conversion architecture. Designed for thought leaders in the missional/formation niche.
user-invocable: true
allowed-tools: Read, Grep, Glob, Agent, WebSearch, WebFetch
---

Run a strategic home page consultation for a movement leader platform.

Target: $ARGUMENTS (default: current tenant — read `src/lib/config/tenant.config.ts`)

$ARGUMENTS can be:
- blank / `current` — audit + consult on the current home page
- `sections` — deep dive on mandatory section architecture only
- `scroll-stop` — deep dive on 3D/motion scroll-stop strategy only
- `copy` — deep dive on copy evaluation only (skip hero — do hero last)
- `full` — run every phase in sequence, interactive throughout

---

## Before Starting

1. Read `src/lib/config/tenant.config.ts` — identity, themes, frameworks, features, pricing
2. Read `src/app/(public)/page.tsx` — current home page implementation
3. Read `_docs/current-ui-overviews/01-home.md` — documented UI state
4. Read `_docs/FRONT_END_CONTENT_INVENTORY.md` — content inventory
5. Read `_docs/PATHWAY_MAP_AND_CHRISTOCENTRIC_SPINE.md` — theological spine
6. Read `_docs/COURSE_STRATEGY.md` — formation philosophy (voice markers, transformation loop)
7. Read `_docs/operations/` — business model context (pricing, audiences, positioning)
8. Skim `_docs/COMPLETE_PAGE_COPY_ALAN_HIRSCH.md` for home-related copy

---

## Phase 1: Mandatory Section Rubric

Every movement leader home page must earn its sections. Grade the current page against this rubric.

### The 10-Section Architecture

Movement leader home pages serve 3 jobs: **Declare** (who is this person and why should I care), **Orient** (what can I do here), **Convert** (get me started). Every section belongs to exactly one job.

**JOB 1 — DECLARE (above the fold + first scroll)**

| # | Section | Purpose | Mandatory? | Spec |
|---|---------|---------|------------|------|
| 1 | **Hero** | Identity + primary value proposition | YES | Headline, subhead, 1–2 CTAs, leader image or motion element. Must answer "Who is this?" and "What's in it for me?" in < 5 seconds. |
| 2 | **Social Proof Strip** | Trust + authority | YES | Logos, affiliations, "as seen in," endorsement count, or partner badges. Minimum 4 logos or equivalent. Must appear before any content pitch. |
| 3 | **About the Leader** | Credibility + warmth | YES | 80–150 word bio, portrait, 2–3 proof points (books published, years active, movements launched). Link to full bio. |

**JOB 2 — ORIENT (mid-page — "what's here?")**

| # | Section | Purpose | Mandatory? | Spec |
|---|---------|---------|------------|------|
| 4 | **Pathways / Themes** | Framework entry points | YES (if pathways exist) | 3–6 cards linking to thematic pathways. Each card: icon/image, title, 1-line description. This is the "table of contents" for the leader's body of work. |
| 5 | **Content Sampler** | Taste of depth | RECOMMENDED | 2–4 featured items (articles, videos, podcast episodes). Rotatable or editorially curated. Shows the platform has substance, not just a landing page. |
| 6 | **AI Lab / Interactive** | Differentiation + engagement | YES (if AI features enabled) | Conversational teaser with example prompt. Must feel invitational, not gimmicky. Glass-panel or embedded chat aesthetic. |
| 7 | **Course / Formation CTA** | Transformation pitch | YES (if courses exist) | "Transformation over information" positioning. Feature list (cohort length, format, mentorship). Video placeholder or testimonial. Single CTA. |

**JOB 3 — CONVERT (bottom of page — "get me started")**

| # | Section | Purpose | Mandatory? | Spec |
|---|---------|---------|------------|------|
| 8 | **Pricing / Access Tiers** | Monetization clarity | RECOMMENDED | Show free vs paid tiers. Movement leaders often skip this — but visitors need to know "what's free?" immediately. Can be subtle (not a SaaS pricing grid). |
| 9 | **Newsletter / Email** | Capture low-intent visitors | YES | Headline, 1-line value prop, email input. "Formation delivered, not just information" pattern. |
| 10 | **Scroll-Stop Moment** | Emotional punctuation | RECOMMENDED | A single visually arresting element — 3D object, parallax image, animated quote, cinematic portrait. Placed between Orient and Convert jobs. Purpose: pattern interrupt before the ask. |

### Grading

For each section, report:

| Status | Meaning |
|--------|---------|
| PRESENT | Section exists and meets spec |
| PARTIAL | Section exists but below spec (explain gap) |
| MISSING | Section does not exist |
| N/A | Not applicable (feature not enabled for this tenant) |

Also flag:
- **Section order problems** — e.g., social proof below the fold, newsletter above pathways
- **Missing job coverage** — if an entire job (Declare/Orient/Convert) is weak
- **Redundancy** — two sections doing the same job

---

## Phase 2: Scroll-Stop Strategy

This phase evaluates options for the "emotional punctuation" moment — the visual element that stops the scroll and shifts the visitor from scanning to feeling.

### Option Matrix

Evaluate each option against 5 criteria (score 1–5 each):

| Criterion | What it measures |
|-----------|-----------------|
| **Wow Factor** | Does it stop the scroll? Would someone screenshot this? |
| **Brand Fit** | Does it match the leader's aesthetic — theological gravity, not tech-startup flash? |
| **Performance** | Load time, CLS, mobile rendering, GPU usage |
| **Maintainability** | Can it be updated without a developer? Asset pipeline complexity? |
| **Versatility** | Can the same approach work for other movement leaders on the platform? |

### Options to Evaluate

**A. Spline 3D Scene**
- Embedded WebGL scene (e.g., rotating book, abstract theological symbol, organic form)
- Scroll-linked or hover-interactive
- Considerations: bundle size (~200KB+), mobile GPU, fallback needed, Spline account dependency
- Best for: hero replacement or dedicated section with a single 3D object
- Example use: A slowly rotating DNA helix (for mDNA) that responds to scroll position

**B. Nano Banana 2 (NB2) Generated Image**
- AI-generated hero/cinematic image using NB2 prompts (via `/asset-generate`)
- Static or with CSS/GSAP animation layered on top (parallax, Ken Burns, reveal)
- Considerations: no runtime cost, easy to swap, but static without animation layer
- Best for: atmospheric backgrounds, cinematic portraits, abstract theological art
- Example use: Wide-format atmospheric portrait of the leader in a cinematic context

**C. GSAP Scroll Animation**
- Pure code animation triggered by scroll position
- Text reveals, parallax layers, counter animations, morphing shapes
- Considerations: zero external dependency, full control, but needs a developer to change
- Best for: typographic moments, data reveals, section transitions
- Example use: A quote that assembles word-by-word as you scroll, with parallax background

**D. Hybrid: NB2 + GSAP**
- NB2-generated image as the base layer, GSAP animations on top
- Parallax depth, floating particles, breathing effects, reveal masks
- Considerations: best of both — visual richness + motion — but two systems to maintain
- Best for: the scroll-stop section between Orient and Convert
- Example use: NB2 cinematic landscape with GSAP parallax layers and a text overlay that fades in

**E. Hybrid: Spline + NB2 Background**
- Spline 3D object floating over an NB2-generated atmospheric background
- Considerations: highest wow factor but also highest complexity and performance risk
- Best for: hero sections where the leader wants maximum visual impact

### Recommendation Framework

After scoring, recommend based on:
1. **If performance is the top constraint** → Option C (GSAP) or D (NB2 + GSAP)
2. **If wow factor is the top priority** → Option A (Spline) or E (Spline + NB2)
3. **If maintainability matters most** → Option B (NB2) with CSS animation
4. **If this must work for all tenants** → Option D (NB2 + GSAP) — most versatile

Always note: **the scroll-stop is NOT the hero.** It sits mid-page as emotional punctuation. The hero is a separate conversation (do hero last).

---

## Phase 3: Copy Evaluation

Evaluate all non-hero copy on the home page. **Skip the hero section** — that gets its own dedicated pass after everything else is decided.

### Copy Rubric (per section)

For each section's copy, evaluate:

| Criterion | Score 1–5 | What "5" looks like |
|-----------|-----------|---------------------|
| **Clarity** | | A first-time visitor knows what this section is about in < 3 seconds |
| **Voice** | | Passes all 5 Alan Hirsch voice markers (or the tenant leader's equivalent) |
| **Specificity** | | Uses concrete details, not generic filler ("18+ books" not "many publications") |
| **Action** | | Every section ends with a clear next step (CTA, link, or invitation) |
| **Brevity** | | No section has more copy than it needs; every word earns its place |

### Voice Markers (Movement Leader Standard)

These are calibrated for the missional/formation niche. Adapt per tenant:

1. **Christocentric / Core-Anchored** — The leader's central thesis is present, not just implied
2. **Invitational Warmth** — "We" language; the visitor is invited in, not sold to
3. **Narrative Imagery** — Organic metaphors, movement language, not corporate/SaaS speak
4. **Intellectual Substance** — At least one real idea per section, not just emotional appeal
5. **Prophetic Edge** — At least one reframing question or productive dissonance on the whole page

### Anti-Patterns to Flag

- Generic motivational copy ("Transform your leadership journey today!")
- SaaS landing page patterns ("Start your free trial," feature comparison grids)
- Corporate consultant language ("leverage," "optimize," "scalable," "synergy")
- Academic hedging ("it could be argued that perhaps...")
- Empty superlatives ("world-renowned," "groundbreaking," "revolutionary")
- Copy that describes the platform instead of the leader's ideas
- Any section where the copy could apply to any thought leader (not specific to this one)

### Copy Verdict Per Section

For each section, report:
```
**[Section Name]**
- Clarity: X/5 — [note]
- Voice: X/5 — [note]
- Specificity: X/5 — [note]
- Action: X/5 — [note]
- Brevity: X/5 — [note]
- Verdict: STRONG / NEEDS WORK / REWRITE
- Recommendation: [specific suggestion if not STRONG]
```

---

## Phase 4: Conversion Architecture

After sections, scroll-stop, and copy are evaluated, assess the overall conversion flow:

### Conversion Checklist

- [ ] **Primary CTA is clear** — visitor knows the #1 thing they should do
- [ ] **CTA hierarchy exists** — not every section screams equally; there's a primary and secondary path
- [ ] **Free path is obvious** — a visitor who won't pay today still has a clear journey (newsletter, free content, AI Lab)
- [ ] **Paid path is clear** — pricing/access tiers are visible or one click away
- [ ] **Trust precedes ask** — social proof and credibility appear before any conversion ask
- [ ] **Progressive disclosure** — the page doesn't dump everything at once; it unfolds
- [ ] **Mobile conversion works** — CTAs are thumb-reachable, forms are simple, nothing is hidden behind hover states
- [ ] **Return path exists** — newsletter or bookmark-worthy content gives reason to come back

### Funnel Map

Draw the intended visitor flow:
```
Landing → [Declare sections] → [Orient sections] → [Scroll-stop] → [Convert sections]
                                      ↓                                    ↓
                              Explore (pathways, content)          Subscribe / Enroll / Ask
```

Flag any breaks in this flow (dead ends, missing links, unclear next steps).

---

## Output Format

```
## Home Page Consultation: [Leader Name]

### Executive Summary
[2-3 sentences: what's working, what's the biggest gap, what's the #1 action]

### Section Audit
| # | Section | Job | Status | Score | Notes |
|---|---------|-----|--------|-------|-------|
| 1 | Hero | Declare | ... | — | (evaluated last) |
| 2 | Social Proof | Declare | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

### Scroll-Stop Recommendation
| Option | Wow | Brand | Perf | Maint | Versatile | Total |
|--------|-----|-------|------|-------|-----------|-------|
| Spline 3D | ... | ... | ... | ... | ... | /25 |
| NB2 Static | ... | ... | ... | ... | ... | /25 |
| GSAP Animation | ... | ... | ... | ... | ... | /25 |
| NB2 + GSAP | ... | ... | ... | ... | ... | /25 |
| Spline + NB2 | ... | ... | ... | ... | ... | /25 |

**Recommendation:** [Option X] because [reason tied to this leader's brand and constraints]

### Copy Report
[Per-section verdicts from Phase 3]

### Conversion Flow
[Funnel map + checklist results from Phase 4]

### Priority Actions (ordered)
1. [Most impactful action first]
2. ...
3. ...
N. Hero section (always last)

### Discussion Points
[Open questions for the leader/team — things that need a decision, not just execution]
```

---

## Consultation Mode

This skill is **interactive by default**. After producing the initial report:

1. **Pause after each phase** and ask the user if they want to go deeper on any finding
2. **Present tradeoffs as questions**, not decisions — e.g., "Social proof strip: logos only, or logos + endorsement quotes? The tradeoff is..."
3. **When discussing scroll-stop**, show example prompts for the recommended option (NB2 prompts, Spline scene descriptions, GSAP animation specs)
4. **When discussing copy**, offer rewrites inline but mark them as proposals
5. **Always defer hero to last** — when the user brings up the hero, acknowledge it and park it: "Noted — let's nail everything else first, then the hero gets its own pass with full context."

---

## Rules

- This is a consultation, not an audit — the tone is collaborative, not judgmental
- Never prescribe a single "correct" home page — present options with tradeoffs
- Ground every recommendation in the leader's actual body of work and theological posture
- The rubric is for movement leaders in the missional/formation niche — not SaaS, not e-commerce, not personal brand influencers
- Social proof for movement leaders means: organizational affiliations, books published, movements catalyzed, endorsements from peers — NOT follower counts or revenue metrics
- "Scroll-stop" is a moment, not a gimmick — it should serve the leader's message, not distract from it
- Hero is always the last section to finalize — it depends on everything else being settled first
- When recommending NB2, provide actual prompt specs (reference `/asset-generate` skill)
- When recommending GSAP, reference existing GSAP patterns in the codebase
- When recommending Spline, note the performance and fallback requirements
- Keep the multi-tenant lens: recommendations should work for this leader AND be adaptable for others on the platform
