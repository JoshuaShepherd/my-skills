# Cross-site role map — who owns what, who links where

The core risk the page auditor polices is: **every page trying to be chapter one.** The homepage, `/about`, `/manifesto`, audience heroes, `/book`, `/fragmentation`, and even some articles all drift toward re-opening the same opening.

This map names, per page / artifact family, **what the page owns**, **what it must link to**, and **what it must not re-open**. Source: `docs/build/prompts/strategy-artifacts-placement-and-flow.md`.

---

## 1. Canonical ownership table

| Argument / artifact | Primary owner | Secondary surfaces |
| ------------------- | --------------- | ------------------- |
| **Canonical stage model** (six stages, names, order) | The company vocabulary itself — same everywhere | Homepage compresses; audience pages apply; articles cite |
| **Public walkthrough of the six stages** | `/fragmentation` | `/book/read/...` for depth; homepage compresses; audience pages apply to their segment |
| **Two intelligences — full definition** | Book Ch. 2 (`/book/read/two-intelligences`) | `/fragmentation` applies; homepage names the pair + links; `/assessment-new` operationalizes |
| **AI Stewardship Sequence (full staircase)** | `/articles/ssss-field-guide-for-organizational-leaders` (compiled guide) + `the-ssss-framework` canon | Homepage compresses (4 cards); audience pages apply; `/book` links here for “operating sequence” |
| **Book** (*From Fragmentation to Movement*) | `/book` (landing) + `/book/read/[slug]` (reader) | Homepage CTA; `/fragmentation` outro; `/about` link row |
| **Credibility / epistemic collapse evidence** | Prior manuscript Ch. 1 + research articles | `/evidence`; articles; homepage L2b only when citations ready |
| **AI product truth** | `/platform` + `/system` + `/evidence` | `/fragmentation` for staged narrative; homepage one crisp claim; FAQ for scope questions. **`/walkthrough` is archived** (see `_archived/walkthrough`) until a live route returns — do not require links to it. |
| **Architecture + constraints** | `/platform` / `/system` (and `/how-it-works` if present) | `/evidence`; FAQ for edges; captioned product UI on platform/system pages when available |
| **Inspectable research + deep arguments** | `/articles/*` | `/evidence` curates; book chapters cross-link; homepage rotates 2–4 |
| **Case studies / customer proof** | `/case-studies` | Homepage proof band (when verified); `/evidence` references |
| **Assessments hub + operational readiness** | `/assess` (hub; system readiness at `#system-readiness`) | Linked from services, pricing, fragmentation outro, nav; homepage secondary CTA for ops-ready buyers where relevant |
| **Dual-intelligence diagnostic** | `/assessment-new` | Linked from `/fragmentation`, homepage after model curiosity, book Ch. 2 |
| **Formation maturity** | `/assess/formation` | Audience pages (churches / institutions) |

---

## 2. Per-page ownership and linking

### Homepage (`/`)

**Owns:** The compressed argument — recognition, tension, named system, path selection.
**Must link to:** `/fragmentation` (staged narrative), `/book` (book), `/articles/ssss-field-guide-for-organizational-leaders` (AI Stewardship Sequence field guide), `/book/read/two-intelligences` (Ch. 2), `/platform` or `/system` (product architecture), `/contact` (invitation), one or more audience pages. Do **not** require `/walkthrough` until that route is live again.
**Must not re-open:** full two-intelligences definition, full six-stage walkthrough, full book opening, aggressive AI demo, fabricated stats.

### `/about` (and `/manifesto` if present)

**Owns:** Orientation — why Movemental exists, who's behind it, first-person-plural honest situation.
**Must link to:** `/book`, `/articles/ssss-field-guide-for-organizational-leaders`, `/fragmentation`, `/evidence` (currently **301 → `/faq`** — use `/faq` directly if you want stable hrefs), `/contact`.
**Must not re-open:** the full thesis, the full AI Stewardship Sequence, the full stage model.

### Audience pages (`/nonprofits`, `/churches`, `/institutions`)

**Owns:** Audience-specific recognition — naming this segment's fragmentation and the integration points that matter for them.
**Must link to:** `/fragmentation` (with audience query param if supported), `/book`, `/platform` or `/system` for product depth, `/contact` or `/apply`.
**Must not re-open:** the paired-intelligence definition, the full six-stage walkthrough, generic AI-position language.

### `/book` and `/book/read/[slug]`

**Owns:** The book landing and reader (*From Fragmentation to Movement*). Not the AI Stewardship Sequence staircase — link to `/articles/ssss-field-guide-for-organizational-leaders` for that.
**Must link to:** `/fragmentation`, the AI Stewardship Sequence field guide article (once on hub), `/evidence` or `/faq` for inspectable research claims.
**Must not re-open:** marketing-flavored chapter openings on `/book`. Reader has minimal chrome.

### `/fragmentation`

**Owns:** The public six-stage walkthrough.
**Must link to:** `/book/read/*` for chapter depth, `/assess` (hub) and/or `/assessment-new` for diagnostics, `/evidence` or `/faq` for research claims.
**Must not re-open:** a second compressed argument that duplicates the homepage. Must not become a second book reader.

### `/walkthrough` (archived)

**Repo status:** No live `(site)/walkthrough` route; prior page lives under `src/app/(site)/_archived/walkthrough/`. **Until restored**, audits should **not** flag “missing `/walkthrough` link” for AI product claims — use **`/platform`**, **`/system`**, and **`/evidence`** instead.

**When live again, would own:** AI product truth — how the model sits inside libraries, pathways, formation workflows, and governance.

### `/evidence`

**Owns:** Argument-level proof — trust patterns, architecture, retrieval grounding, multi-tenant posture.
**Must link to:** specific articles with data, book chapters, `/platform` or `/system` for architecture-level UI or diagrams when relevant.
**Must not re-open:** the full thesis. Must not use placeholder sources.

### `/platform` / `/system` / `/how-it-works`

**Owns:** Architecture story — layers, constraints, capabilities, explicit non-capabilities.
**Must link to:** `/evidence`, `/pricing` (and `/walkthrough` when that route is live again).
**Must not re-open:** fragmentation walkthrough. Must not claim capabilities it cannot show.

### `/articles/*` and `/articles/[slug]`

**Owns:** Inspectable research and deep argument. Each article owns one claim in depth.
**Must link to:** relevant stage or intelligence definition (book / fragmentation), related articles, `/evidence`.
**Must not re-open:** the full thesis. Must include a "where am I?" paragraph early.

### `/case-studies`

**Owns:** Narrative proof — engagement stories, outcomes where verified.
**Must link to:** `/evidence`, relevant articles, `/contact`.
**Must not re-open:** thesis. Must not fabricate logos, quotes, or metrics. In-progress cases clearly labeled.

### `/assess`

**Owns:** Assessments hub — explains dual-intelligence, system readiness, and formation snapshot entry points; hosts the **system readiness** instrument at `#system-readiness`.
**Must link to:** `/platform`, `/fragmentation`, `/contact` for follow-up (and `/walkthrough` only when live).
**Must not re-open:** collapsing `/assessment-new` into the same labels or scores as system readiness. Semantic separation is mandatory.

### `/assessment-new`

**Owns:** Dual-intelligence diagnostic — paired intelligences × six stages × infra channels.
**Must link to:** `/fragmentation`, `/book/read/two-intelligences`, `/contact` for follow-up.
**Must not re-open:** operational system readiness. Semantic separation from `/assess` is mandatory.

### `/contact`

**Owns:** Form + trust signals + honest response-time promise.
**Must link to:** nothing aggressive; minimal.
**Must not re-open:** thesis. No additional marketing sections.

### `/pricing`, `/services`

**Owns:** Scope truth — what is included, what is not, at what commitment level.
**Must link to:** `/platform` or `/system` for what-you-get, `/assess` when diagnostics help qualification, `/case-studies` if relevant, `/contact`.
**Must not re-open:** thesis. Must not hide scope. Must not imply capabilities not in `/platform`.

### `/faq`

**Owns:** Honest, short answers to the questions we get most.
**Must link to:** book, articles, evidence, platform/system (product depth), pricing, `/assess` when diagnostics are relevant.
**Must not re-open:** thesis. Must not evade pricing or AI-limit questions.

### Legal (`/privacy`, `/terms`, `/cookies`)

**Owns:** Legal compliance. Tone should match the rest of the site.
**Must link to:** standard legal links.
**Must not re-open:** thesis. No marketing copy mixed in.

---

## 3. Re-opening patterns to flag aggressively

The auditor should flag the following as **"re-opening an argument another page owns":**

- **Any page** (other than homepage + book + fragmentation) that opens with a paragraph about "organizations facing AI."
- **Any page** (other than book Ch. 2 + homepage § "what must come together") that fully defines informational vs. relational intelligence.
- **Any page** (other than fragmentation) that walks through all six stages in sequence.
- **Any page** (other than `/platform`, `/system`, or `/evidence`) that makes multiple AI capability claims without linking to one of those.
- **Any audience page** that opens with generic "organizations" framing before naming the audience.
- **Any article** that introduces new vocabulary without mapping to the canonical set.
- **Any page** with three or more sections that could live on the homepage verbatim (sign of duplication).

---

## 4. Missing-link patterns to flag

- Page mentions the **book** but does not link to `/book` or a specific `/book/read/...` slug.
- Page mentions **the AI Stewardship Sequence** / “four steps” but does not link to `/articles/ssss-field-guide-for-organizational-leaders` (or the `the-ssss-framework` article when context is narrow).
- Page mentions **two intelligences** but does not link to Ch. 2.
- Page mentions **fragmentation** but does not link to `/fragmentation`.
- Page makes a **quantitative claim** but does not link to `/evidence` or the article that carries the source.
- Page describes **AI behavior** but does not link to `/platform`, `/system`, or `/evidence` (or `/walkthrough` when live).
- Page makes **case-study claims** but does not link to `/case-studies`.

---

## 5. Ownership is static; implementation may drift — verify before citing

A memory or map like this is frozen in time. Before the auditor recommends "link to `/book/read/X`" or "move this to `/evidence`":

- **Confirm the target route exists** (Glob or Read).
- **Confirm the target page actually owns the claim the audit is handing off.** (A landing page that says it owns the thesis but is thin doesn't own it in practice.)
- **If ownership is aspirational but not shipped**, flag that in the audit and suggest **softening** until the target surface is real.

---

## 6. Output for Pass 6

In the output template's **A. Page role diagnosis** and **F. Priority fixes**, include:

- **Role statement** — "This page owns X; it links to Y; it must not re-open Z."
- **Re-opened arguments** — list, with the page that actually owns them.
- **Missing links** — list, with the recommended destination and anchor.
- **Over-reach / under-reach** — if the page claims more than its job, or less.
