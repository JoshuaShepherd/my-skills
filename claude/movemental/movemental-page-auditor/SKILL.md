---
name: movemental-page-auditor
description: Audit any Movemental page (HTML mockup or production React) across six passes — narrative sequencing, copy & language, typography/hierarchy, UI/proof/demonstration, proof burden, and cross-site role — and return a structured, ranked critique. Use this skill whenever the user asks to audit, review, critique, diagnose, or "be tough on" a Movemental page (`/`, `/fragmentation`, audience pages, articles, `/book`, `/system`, `/walkthrough`, FAQ, `/assess`, `/assessment-new`, audience concept pages), or asks questions like "is this page working?", "what's weak here?", "what's missing?", "should this section exist?", "does this page duplicate /X?". Judges against Movemental canon (two intelligences, the AI Stewardship Sequence, six stages, formation, inspectability, field guide), not generic design best practices. Use this skill even when the user doesn't explicitly say "audit" — if they are asking for a serious, opinionated read of a whole page (not just one section), this is the right tool. Complements, does not replace, `movemental-narrative-audit` (strategic alignment only) and `page-audit` (UI/DESIGN.md compliance).
---

# Movemental page auditor

A six-pass, opinionated audit for any Movemental page. The output is structured, ranked, and Movemental-specific — it does not read like a generic UX review.

This skill **complements** three siblings and should be preferred when the audit needs to cover **rhetoric, sequencing, proof posture, and cross-site role at once**:

- `movemental-narrative-audit` — strategic / editorial alignment against two-intelligences + six stages only; narrower.
- `page-audit` — UI, DESIGN.md tokens, Stitch fidelity, technical architecture.
- `design-audit` — DESIGN.md compliance, broader.
- `article-audit`, `pathway-audit` — prefer these when the target is specifically an article or pathway.
- `alan-voice` — voice-level editing; use **after** this audit surfaces copy issues.

---

## When this skill triggers

Trigger phrases include, but are not limited to:

- "Audit this page" / "review this page" / "critique the homepage"
- "Is this page working?" / "What's weak here?" / "What's missing?"
- "Give me tough feedback on /X" / "be opinionated about /X"
- "Does this section earn its place?" / "Does this page duplicate /Y?"
- "Should we add a proof block here?" / "Is this page too textual?"

Also trigger when the user shares a page (React file, HTML mockup, URL, or screenshot) and asks for a serious read — even without the word "audit."

Do **not** trigger for single-section edits, copy tweaks, or typography-only questions — use `alan-voice`, `design-audit`, or direct editing instead.

---

## Inputs the auditor needs

Before running, confirm (or infer from context):

| Input | Required? | Example |
| ----- | --------- | ------- |
| **Page type** | yes | homepage, about, audience, article, system, walkthrough, faq, field-guide, assessment |
| **Route** | yes | `/`, `/fragmentation`, `/churches`, `/book`, `/assess`, `/walkthrough` |
| **Source** | yes | React component path, HTML mockup path, or pasted content |
| **Artifact family** | yes | home, fragmentation, book, assess, audience, evidence, services, platform, legal |
| **Mockup or production?** | yes | HTML mockup in `docs/html/`, production React under `src/components/sections/`, or live URL |
| **Primary / secondary** | yes | primary = top-nav or funnel-entry page; secondary = supporting page |
| **Canonical references** | optional | any prompt files in `docs/build/prompts/` that govern this page |
| **Screenshot** | optional | useful for typography/hierarchy pass |

**Proceed with partial inputs.** If a field is missing, infer from the route and flag the assumption in the output under `## A. Page role diagnosis`.

---

## Ground truth — read before judging

Load the starred files every time. Load the per-page-type rubric from `references/page-types.md` for the relevant type.

★ `docs/design/DESIGN.md` — pillars (§1), typography tokens, semantic color (§8, §11), trust posture (L2b)
★ `docs/build/prompts/strategy-artifacts-placement-and-flow.md` — canonical artifact ownership across the site
★ `docs/book-development/fragmentation-manuscript-ordered/02-two-intelligences.md` — canonical definition
★ `docs/book-development/fragmentation-manuscript-ordered/05-the-six-stages-at-a-glance.md` — stage order
★ `docs/articles/the-ssss-framework.md` + `why-order-matters.md` — load-bearing AI Stewardship Sequence claims
★ `references/page-types.md` (in this skill) — per-type sequencing rubric
★ `references/copy-patterns.md` — canonical vocabulary + drift lexicon
★ `references/cross-site-map.md` — which page owns which argument

Load on demand:
- `docs/build/prompts/home-page-narrative-credibility-ia-plan.md` — for the homepage
- `docs/build/prompts/home-page-fragmentation-funnel-narrative.md` — for the homepage (funnel spine)
- `docs/articles/two-intelligences-integration.md`, `the-movemental-thesis.md` — when the page makes the paired claim
- Per-audience pathway docs — for audience pages
- `docs/build/prompts/assessment-dual-intelligence-infrastructure-from-assessment-new.md` — for assessment audits

Do **not** invent Movemental doctrine. If a claim is not supported by a file you read, flag it **unsupported** in the output.

---

## The six passes

Run **all six**, in order. Do not skip. The output template depends on every pass being completed.

### Pass 1 — Narrative sequencing (page-type-aware)

Use the matching rubric in `references/page-types.md`. Ask, for every page:

- Does the page **start at the right level of abstraction** for its role?
- Does it **introduce the problem before the solution**?
- Does each section **earn the next** — or is the page a stack of equal-weight thesis slides?
- Does the arc move through **tension → clarification → structure → proof → action** (adjusted for page type)?
- Does the **CTA arrive after enough understanding and trust**, not before?
- Is the page **trying to do too many jobs at once**?
- Does it **duplicate work owned by another page** (check `references/cross-site-map.md`)?

**Score:** `strong` / `uneven` / `confused`. Always provide **section-by-section notes** — one line per section minimum.

### Pass 2 — Copy & language

Flag the following on sight (full lexicon in `references/copy-patterns.md`):

- **SaaS-isms / hype** — "unlock", "revolutionize", "supercharge", "game-changing", "10x", "AI-powered", "seamless", "cutting-edge"
- **Purple prose / elegant-but-empty** — sentences that sound good but transmit no information
- **Vague abstraction** — "we help organizations...", "in this moment", "the future of work"
- **Overly ecclesial language** where clarity would serve better (audience-dependent)
- **Accidental jargon** — internal terms that a new reader cannot decode
- **Repeated phrasing within the page** — same sentence shape in three sections = monotony
- **Claims that outrun on-page proof** — anything quantitative without L2b citation
- **Concept drift from canonical vocabulary** — e.g., "Human Layer / Technology Layer" in place of "informational / relational intelligence"

Positively check for the five Movemental voice markers (see `references/copy-patterns.md` §3):

1. **Clarity** — every sentence earns its place.
2. **Precision** — named concepts used with their canonical meaning.
3. **Seriousness** — no posturing, no winking.
4. **Warmth without sentimentality** — human, not saccharine.
5. **Authority without grandiosity** — confident but not self-declaring.

**Output for this pass:** strongest lines (quote 2–3), weakest lines (quote 2–3), phrases to cut (list), phrases to rewrite (with suggested replacement).

### Pass 3 — Typography & content hierarchy

Ask: **is typography doing real narrative work, or is it decoration?**

Use the checklist in `references/typography-checks.md`. Evaluate:

- **Headline hierarchy** — is H1/H2/H3 strong enough to carry the argument's structure?
- **Monotony** — are there too many large statements in a row? (Three big headlines in sequence = a page that feels elegant but underpowered.)
- **Body copy density** — too gray, too long, too dense, or too weak relative to its heading?
- **Emphasis discipline** — is bold/italic/SerifEm used as a precision instrument or sprinkled decoratively?
- **Section-opening variety** — if every section opens with `divider + eyebrow + H2`, rhythm is flat. Good pages alternate.
- **Contrast levels** — thesis ≠ support ≠ evidence ≠ explanation ≠ CTA. Each should have a distinct typographic weight.

**Output:** what's visually working, where hierarchy collapses, where monotony sets in.

### Pass 4 — UI / proof / demonstration

Ask: **is the page too textual for the burden it carries?**

For each major claim or concept, decide whether it needs:

| Component | When to recommend |
| --------- | ----------------- |
| **Comparison block** | Page positions itself against an alternative (before/after, with/without us) |
| **Proof strip** | A quantitative claim or credibility signal lives on-page |
| **System map / diagram** | Architecture or process is described but not shown |
| **Preview frame** | Product behavior is described in prose instead of a UI screenshot/mock |
| **Audience cards** | Page promises applicability across segments but shows none |
| **AI demo (clearly labeled)** | AI behavior is described but not demonstrated — label demo vs. production |
| **Pull quote** | An endorsement or testimonial exists and is verifiable |
| **Process rail** | Sequential steps are described in prose where a rail would read faster |
| **FAQ accordion** | A cluster of objections appears as prose |
| **Interactive selector** | Audience or stage switching would change the reader's mental model |
| **No UI needed** | Copy alone is enough — give explicit permission to leave it text |

**Output:** a table — `Placement | Kind | Why` — with a short rationale per row. Do not recommend more than 5 new components in one audit.

### Pass 5 — Proof burden

For every strong claim, categorize (use the decision table in `references/proof-burden.md`):

- **Requires evidence** — must add citation or move to a page that carries the source.
- **Positioning language** — acceptable as-is; not a factual claim.
- **Should be softened** until proof arrives on-page.
- **Should be linked out** — to `/evidence`, `/articles/...`, `/book/read/...`, `/fragmentation`, `/case-studies`, or `/walkthrough`.

Pay extra attention to pages that make **serious claims** about:

- **Credibility / trust** (who we are, what we've done)
- **AI behavior** (what the model will and won't do)
- **Formation** (what transformation we claim to produce)
- **Fragmentation consequences** (what breaks, by how much)
- **Systems / infrastructure** (what we build vs. describe)
- **Authority** (why our judgment should be trusted)

**Output:** a table — `Claim | Category | Action (cite / soften / link / keep)`. Quote the claim exactly.

### Pass 6 — Cross-site role

Ask:

- What **job** is this page supposed to do in the overall site?
- Does it **own that job**, or is it re-opening an argument another page owns?
- Does it **duplicate** other pages (especially opening chapters of the thesis)?
- Does it **own too much** (trying to be everything) or **too little** (a thin placeholder)?
- Does it **link properly** into the artifact flow (book, fragmentation, evidence, articles, walkthrough)?

**Core risk: every page trying to be chapter one.** The homepage, `/about`, `/manifesto`, audience hero sections, `/book`, and `/fragmentation` all tend to re-open the same opening. Flag aggressively.

Use `references/cross-site-map.md` — it names, per artifact family, what the page **owns**, what it **links to**, and what it **must not re-open**.

**Output:** explicit role statement + a list of re-opened arguments or missed links.

---

## Output template — always use this structure

```markdown
# Page auditor — <route>

**Page type:** <homepage | about | audience | article | system | walkthrough | faq | field-guide | assessment>
**Artifact family:** <home | fragmentation | book | assess | audience | evidence | services | platform | legal>
**Primary / secondary:** <primary | secondary>
**Source:** <file path or URL>
**Ground truth read:** [bulleted list of files]
**Assumptions flagged:** [anything inferred rather than given]

---

## A. Page role diagnosis
- **What this page appears to be trying to do:** …
- **Whether that is correct for its route and type:** …
- **Scope drift / overreach:** …

## B. Sequencing score — <strong | uneven | confused>
**Arc summary (1–2 sentences):** …

**Section-by-section:**
- §1 [name] — [one-line note; flag whether it earns §2]
- §2 [name] — …
- (continue for every section)

## C. Copy score
- **Strongest lines:**
  - "…" (why it works)
- **Weakest lines:**
  - "…" (why it falls)
- **Phrases to cut:**
  - "…" — SaaS-ism / hype / vague / repeated
- **Phrases to rewrite:**
  - "…" → suggested: "…"

## D. Typography & hierarchy score
- **What is visually working:** …
- **Where hierarchy collapses:** …
- **Monotony risks:** …

## E. Missing proof / UI / structure opportunities
| Placement | Kind | Why |
| --------- | ---- | --- |
| §3 after the two-intelligences split | System map | Page describes the pair but never shows them mapped to channels |
| §5 closing | Proof strip | Claim "shaped by real movement questions" has no link-out |
| …

## F. Priority fixes — ranked by impact × ease
1. **[Pass # · Section]** — [specific fix; one sentence]
2. …
(maximum 10; cut anything below the 10th in importance)

---

## Optional: agent prepend block
```text
Follow the page auditor's output for <route>. Non-negotiables:
- …
- …
```
```

**Rules for the output:**

- **Always** name the six section letters A–F, even if a section is short.
- **Always** quote copy verbatim in passes C and E5 — paraphrases lose the diagnostic.
- **Never** produce more than **10 priority fixes**. If you have 15 candidates, rank and drop the bottom 5.
- **Rank by impact × ease** — a 1-hour fix that lifts the page 30% beats a 20-hour overhaul that lifts it 40%.

---

## Principles — internalize before judging

These are the standard of quality the audit enforces:

1. **No generic SaaS tone.** Movemental is editorial, calm, authoritative — closer to a Harper's essay than a Salesforce landing page. "Transform your organization with AI" is a failure state.
2. **No inflated AI claims.** AI is a function of **corpus + graph + governance**. Do not let a page imply magic, autonomy, or replacement of judgment.
3. **No decorative UI without meaning.** Every visual element must advance the argument. "Looks premium" is not a reason.
4. **Sequencing matters.** Rhetorical position is a feature. A correct line in the wrong place is still wrong.
5. **Pages don't duplicate the full thesis unless they own it.** If `/fragmentation` owns the walkthrough, the homepage compresses and links; if `/book` owns the field guide frame, audience pages cite — they do not re-open.
6. **Typography is part of the argument.** Italic serif emphasis is a precision instrument. Headline hierarchy tracks the structure of the claim.
7. **Proof burden rises with claim strength.** A quantitative claim requires a citation or a move to an article. A strong unverified claim gets softened or moved.
8. **Examples and systems often outperform abstract paragraphs.** When in doubt, swap a thesis restatement for a concrete example or a shown system.
9. **Formation language stays concrete.** Donor letters, pastoral care, faculty knowledge, governance, discernment. Not "impact," "journey," or "transformation" as floating abstractions.
10. **"Modern editorial" ≠ "minimal statements floating in whitespace."** Breathing layout is good; empty layout is evasive. A page should have density commensurate with its ambition.

---

## Danger to avoid

This skill is **not a general design critic.** It is a **Movemental page auditor.** Judge pages according to:

- **Movemental site architecture** — artifact ownership, cross-page flow
- **Movemental rhetoric** — vocabulary, voice, proof posture
- **Movemental design language** — DESIGN.md pillars, tonal stacking, semantic tokens
- **Narrative flow** — tension → clarification → structure → proof → action, adjusted for page type

Do **not** import generic UX platitudes ("above the fold," "reduce cognitive load," "increase conversion," "use social proof") unless they are also Movemental standards and grounded in the canonical artifacts.

---

## Workflow summary (what to do when invoked)

1. **Gather inputs** — route, type, source, artifact family, primary/secondary. Confirm what's missing.
2. **Read ground truth** — starred files + per-page-type reference. Note what you read in the output.
3. **Run all six passes** in order. Quote copy verbatim in C and E5.
4. **Draft output** using the template. Every section A–F must appear.
5. **Rank priority fixes** — max 10, by impact × ease.
6. **Offer an agent prepend block** if the user plans to hand the audit to an implementer agent.

Keep the final audit **tight**. A good audit is 700–1,200 words — long enough to be specific, short enough to be acted on.
