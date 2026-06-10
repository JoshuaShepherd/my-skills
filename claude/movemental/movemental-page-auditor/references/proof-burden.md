# Proof burden — claim strength, evidence discipline, soften/link decisions

Movemental makes serious claims. The site's credibility depends on **every strong claim being either proved on-page, clearly linked to its proof, or softened to a positioning statement.** DESIGN.md's L2b trust pattern governs the inspectable-citation posture.

This pass categorizes every strong claim into one of four buckets and proposes an action.

---

## 1. Four categories

| Category | Definition | Action |
| -------- | ---------- | ------ |
| **Requires evidence** | Factual or quantitative claim that a reasonable skeptic could contest | Add citation on-page (L2b) or move the claim to a page that carries the source |
| **Positioning language** | Subjective, non-factual framing (e.g., "we believe that...") that does not promise a verifiable outcome | Acceptable as-is |
| **Should be softened** | A factual claim with no on-page or easily-linked proof; cannot be dropped entirely | Soften to positioning until proof arrives (e.g., "some of the largest" → "a growing number of") |
| **Should be linked out** | A strong claim whose proof lives elsewhere in the site | Add a visible link to `/evidence`, `/articles/...`, `/book/read/...`, `/fragmentation`, `/case-studies`, `/platform`, `/system`, or `/walkthrough` **when that route is live** |

Every strong claim gets exactly one category. Ambiguity resolves in favor of the more conservative choice.

---

## 2. Claim-strength rubric

Use this to decide whether a claim is "strong enough" to require treatment:

### Always strong (always needs treatment)

- **Quantitative claims** — any number, percentage, count, dollar figure, or time estimate.
- **Capability claims** — "does X," "prevents Y," "eliminates Z."
- **Outcome claims** — "produces X," "results in Y," "transforms Z."
- **Credibility claims** — "trusted by," "used by," "recognized as."
- **Comparative claims** — "better than," "unlike," "only."
- **AI-behavior claims** — "the model will," "the model won't," "grounded in," "never leaks."
- **Research claims** — "studies show," "data suggests," "research confirms."

### Sometimes strong (treat based on context)

- **Authority claims** — "we work at the intersection of..." (positioning if not quantified; strong if combined with a capability claim).
- **Formation claims** — "forms judgment," "develops discernment" (positioning if framed as practice; strong if framed as measurable outcome).
- **Scope claims** — "covers X," "includes Y" (strong when used to price or sell; positioning when descriptive).

### Usually positioning (rarely needs treatment)

- "We believe that..." / "We are convinced that..."
- "Our conviction is..."
- "The path we commend..."
- "We work with..." (when not claiming exclusivity)

---

## 3. Soften-or-link decision tree

For every claim flagged as strong:

```
Is there a source for this claim?
├── Yes, source is a book chapter, article, or research file in the repo
│   └── Is the source linked on-page?
│       ├── Yes → OK (mark "linked out")
│       └── No → Action: add visible link → "should be linked out"
├── Yes, source is an external study or citation
│   └── Is the citation visible on-page (L2b pattern)?
│       ├── Yes → OK
│       └── No → Action: add L2b citation or soften → "requires evidence"
├── Yes, source is a customer / case study
│   └── Is the customer verifiable and named (with permission)?
│       ├── Yes → OK
│       └── No → Action: remove or generalize → "requires evidence" → "should be softened"
└── No source exists today
    └── Action: soften to positioning → "should be softened"
```

---

## 4. High-risk claim zones on Movemental

Pay **extra attention** to these:

### Credibility / trust
- "Trusted by mission-driven organizations" — unless a logo strip with verifiable attribution appears, **soften** or **remove**.
- "Founded by / built by experts in..." — unless a named team page exists, **soften**.
- "Years of experience in..." — unless dated and specific, **soften**.

### AI behavior
- "Our AI will never..." — if you cannot show the guardrail in `/evidence` or product surfaces (`/platform`, `/system`), **soften**. (`/walkthrough` is archived until restored.)
- "Grounded in your corpus" — requires an evidence section or architecture copy on `/platform` / `/system`; otherwise **link to `/evidence`** (or `/walkthrough` when live).
- "Preserves your voice" — requires a demonstrated example; otherwise **soften** or **link**.
- "Multi-tenant isolation" / "data boundaries" — requires the architecture page to actually describe the boundary; otherwise **soften** or **link to system**.

### Formation
- "Forms judgment in leaders" — can be positioning; ensure it's framed as practice, not guaranteed outcome.
- "Produces movement" — aggressive; **soften** unless multi-case evidence exists.
- "Results in durable change" — **soften** unless cases link.

### Fragmentation consequences
- Stats about scattered content (e.g., "X% of mission-driven organizations...") — **requires evidence**, always.
- "Credibility is collapsing" — acceptable as positioning when framed per the book; **requires evidence** when quantified.
- "Search and AI surfaces will misrepresent you" — strong claim; **link out** to articles/evidence when available, **soften** otherwise.

### Systems / infrastructure
- "Digital infrastructure" is canonical (positioning-level).
- "Used at scale" / "production-ready" — **soften** unless a live deployment count exists.

### Authority
- "We are the only..." — almost always wrong; **soften** or remove.
- "Leading platform for..." — **soften** or remove.
- "World-class..." — always remove.

---

## 5. L2b pattern (from DESIGN.md)

When a claim **requires evidence**, prefer the L2b inline evidence pattern:

- Render the claim.
- Append a small, legible citation: source name + year + link (or an inline footnote link).
- Where possible, link to a local page that carries the evidence (article, book chapter, research file).

Do **not** use placeholder source names ("Source A / Source B"). If citations are not ready, **soften** the headline until they are.

---

## 6. Link-out destinations — when each is right

| Destination | Use when the claim is about... |
| ----------- | ------------------------------ |
| **`/evidence`** | Architecture, trust posture, AI grounding, inspectability |
| **`/articles/...`** | A specific research memo, case study, methodology, industry analysis |
| **`/book/read/...`** | Canonical doctrine — two intelligences (Ch. 2), six stages (Ch. 5), the AI Stewardship Sequence (Ch. 12) |
| **`/fragmentation`** | The six-stage walkthrough, stage motion, or an audience-specific rail |
| **`/case-studies`** | A specific customer outcome |
| **`/platform` / `/system`** | Architecture, constraints, product behavior at the narrative level |
| **`/walkthrough`** | Product behavior at UI walkthrough level — **only when the route is live** |
| **`/assess` or `/assessment-new`** | Diagnostic instruments (operational vs. dual-intelligence) |

**Rule:** every strong claim that is not evidenced on-page must have a **visible link** to one of these. Buried links in body text do not count.

---

## 7. Output for Pass 5

Produce a table:

| Claim | Category | Action |
| ----- | -------- | ------ |
| "Shaped by real movement, church, nonprofit, and institutional questions." | positioning | keep |
| "80% of mission-driven orgs will face credibility collapse by 2027." | requires evidence | cite or soften |
| "Our AI is grounded in your corpus." | linked out | add visible link to `/evidence` or `/platform` (or `/walkthrough` when live) |
| "We are the leading platform for formation-driven AI." | should be softened | rewrite as positioning |

Quote each claim **verbatim** from the page. Do not paraphrase — the diagnostic depends on the exact wording.

Keep the table focused on **strong claims only.** Do not include every sentence.
