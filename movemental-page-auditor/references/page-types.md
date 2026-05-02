# Per-page-type sequencing rubrics

Use the rubric that matches the page being audited. Each rubric defines:

- **Job** — the single thing this page must do in the site.
- **Arc** — the correct narrative sequence for this type.
- **Abstraction level** — where to start (how close to the thesis) and where to end.
- **CTA posture** — when the page has earned the ask.
- **Red flags** — failure patterns specific to the type.
- **Must-have sections / must-not sections.**

---

## Homepage (`/`)

**Job:** Compressed argument. Recognition → tension → pivot → named system → staged confidence → trust → path selection. **Not** a short fragmentation page; **not** a second book opening.

**Arc (in order):**

1. Hero — tension + promise (felt).
2. Problem — recognition (two intelligences named, legible).
3. Consequence — weight / urgency (coherence, interpretation, representation).
4. Turn — relief / pivot to agency.
5. System — named answer (the AI Stewardship Sequence or six stages compressed).
6. What must come together — informational + relational intelligence (paired definition).
7. Audience applicability — concrete, short cards.
8. Authority / Why Movemental — proof-adjacent, not self-declared.
9. Grounding — what this is not / what this produces.
10. Invitation — single action, clean.

**Abstraction level:** Opens **at the problem**, not at the thesis. Ends at **named actions / routes**.

**CTA posture:** Primary CTA appears twice — once after the system is named (§5 or §6), once at the invitation. Before §5, only in-page anchors.

**Red flags:**

- Hero tries to be the whole argument.
- Three or more consecutive sections in the same shape (eyebrow + giant headline + short explanation).
- "Human Layer / Technology Layer" (drift from informational / relational).
- Unsourced quantitative claims.
- Book or the AI Stewardship Sequence field guide is mentioned but resolves nowhere (use `BOOK_HUB_PATH` / `SSSS_FIELD_GUIDE_PATH`).
- Secondary CTA says "See the path" (too generic — prefer "See the framework", "Read the book", or "AI Stewardship Sequence field guide").

**Must-have sections:** hero, problem, consequence, turn, named system, applicability, invitation.
**Must-not sections:** full interactive fragmentation walkthrough, full book reader, any "chapter one" opening repeated.

**Ground truth beyond the starred list:**
- `docs/build/prompts/home-page-narrative-credibility-ia-plan.md`
- `docs/build/prompts/home-page-fragmentation-funnel-narrative.md`

---

## About (`/about`, `/manifesto`)

**Job:** Light orientation — why Movemental exists, who's behind it, pointers to `/book`, `/fragmentation`, `/evidence`. **Not** a second opening of the full thesis.

**Arc:**

1. Opening — one paragraph of honest situation.
2. Origin — short, dated, first-person-plural if collective.
3. Conviction — 2–4 beats (can borrow from `docs/articles/the-movemental-thesis.md`), each with one concrete line.
4. What we are building — brief; link out to `/platform`, `/walkthrough`, `/system`.
5. Invitation — to `/contact` or `/book`.

**Abstraction level:** Opens at **situated origin**, not at the thesis. Ends at a **single action**.

**CTA posture:** One primary CTA at the end. No mid-page conversion attempts.

**Red flags:**

- Reads as a manifesto that re-opens the fragmentation argument.
- Generic "founded on a belief that..." language.
- No named people or dated story.
- More than 4 "why we exist" sections.

**Must-have:** origin, conviction, build, invitation.
**Must-not:** repeat fragmentation walkthrough; re-define two intelligences; list the six stages.

---

## Audience page (`/nonprofits`, `/churches`, `/institutions`)

**Job:** Recognize this audience's specific fragmentation and name the integration points that matter for them. Hand off to shared surfaces (`/book`, `/fragmentation`, `/assess`, `/walkthrough`).

**Arc:**

1. Audience-specific hero — names the segment, states the specific tension.
2. Two equal errors for this audience — mirrors the top-level frame but concrete (e.g., "ignore donor sentiment" / "over-automate donor voice").
3. Fragmentation as this audience experiences it — concrete channels (donor letters / pastoral care notes / faculty knowledge).
4. Integration points for this audience — what must come together **specifically**.
5. Path forward (the AI Stewardship Sequence compressed) — same sequence, applied to this audience.
6. What this produces — concrete outcomes for this audience.
7. Proof / cases (if available; soften if not).
8. Invitation — to `/contact` or audience-specific CTA.

**Abstraction level:** Concrete from §1. Never generic.

**CTA posture:** CTA appears once mid-page (after §5) and once at end.

**Red flags:**

- Opens with the same thesis as the homepage (re-opens chapter one).
- Uses generic "organizations" language instead of nonprofits / churches / institutions.
- No audience-specific artifacts named (no mention of donor letters, sermons, syllabi, etc.).
- Three audience pages that are copy-paste identical save for one noun.

**Must-have:** audience-specific channels, integration points, path, invitation.
**Must-not:** full two-intelligences definition (link to book Ch. 2 instead); full six-stage walkthrough (link to `/fragmentation`).

**Ground truth beyond starred:**
- `docs/build/prompts/audience-and-org-pages-copy-prompts-v2.md`
- `docs/build/prompts/audience-pages-canonical-merge-from-new-routes.md`
- `docs/build/prompts/audience-pages-narrative-audit.md`

---

## Article (`/articles/[slug]`)

**Job:** Prove or develop one argument in depth. **Articles prove; book teaches; fragmentation animates.**

**Arc:**

1. Where-am-I paragraph — what problem, what canonical frame it sits inside (link to stage or intelligence).
2. The argument — sustained, evidence-backed.
3. Counterpoint — honest acknowledgment of the other side.
4. Synthesis — what follows from the argument.
5. What this changes for the reader — concrete.
6. Further reading — linked list (book chapters, related articles, evidence).

**Abstraction level:** Starts concrete (a case, a claim, a moment), resolves to implication.

**CTA posture:** No sales CTA in the body. End with "further reading" and maybe one subscribe/contact line.

**Red flags:**

- "Hot take" with no where-am-I paragraph.
- Introduces new vocabulary without mapping to existing terms or proposing a glossary update.
- Unsourced quantitative claims.
- Reads like a blog post (casual, reactive) when the site promises longform argumentation.

**Must-have:** where-am-I graf, counterpoint, further reading.
**Must-not:** re-open the full fragmentation argument; re-teach two intelligences if the article is not about them.

**Defer to:** `article-audit` skill when doing a deep article-only audit; use this skill when auditing an article as part of a page-family review.

---

## System / platform / how-it-works (`/platform`, `/system`, `/how-it-works`)

**Job:** Show **what is built** and under what constraints. Architecture story, not marketing restatement of the thesis.

**Arc:**

1. Opening — what this is, in one paragraph.
2. The architecture — diagram, layers, data boundaries.
3. The constraints — tenant isolation, corpus grounding, human-in-the-loop, policy boundaries.
4. What it does — concrete capabilities.
5. What it does not do — explicit refusal posture (especially AI-related).
6. Proof / walkthrough link — to `/walkthrough` or `/evidence`.
7. Invitation — to contact or deeper page.

**Abstraction level:** Concrete and technical. No thesis re-opening.

**CTA posture:** CTA appears once at end; before that, deep-dive links to `/walkthrough` or `/evidence`.

**Red flags:**

- "Powered by AI" as a headline (inflated claim, vague).
- No diagram, no constraints named.
- Describes product behavior as magic without showing the constraint.
- Conflates demo with production without labeling.

**Must-have:** constraints, what-it-does-not-do, link to `/walkthrough` or `/evidence`.
**Must-not:** fabricate capabilities; re-open the fragmentation thesis.

---

## Walkthrough (`/walkthrough`)

**Job:** **Show, with captions, how the product actually works** — AI in context, libraries, pathways, formation workflows. Primary owner of AI posture on the site.

**Arc:**

1. Opening — what you're about to see, and what environment (demo vs. live).
2. Scene 1 — corpus + library (what data the model sees).
3. Scene 2 — pathway / formation workflow.
4. Scene 3 — AI behavior (clearly labeled demo if not live).
5. Scene 4 — governance / guardrails.
6. What this is — and what a demo is not.
7. Invitation — to contact, or to `/evidence`.

**Abstraction level:** Concrete from §1. Every claim paired with a visible artifact.

**CTA posture:** CTA at end. Mid-page links only to adjacent proof.

**Red flags:**

- No labeling of demo vs. production.
- Testimonials in a demo context.
- Claims about formation that are not paired with a shown workflow.
- No mention of what the model can and cannot see.

**Must-have:** data-boundary scene, AI labeled demo/production, governance scene.
**Must-not:** imply customer data; import fake case studies.

---

## FAQ (`/faq`)

**Job:** Anticipate objections and provide short, honest, inspectable answers. Not a sales page; not a glossary.

**Arc:**

1. Opening — one sentence of framing ("questions we get most").
2. Clustered Q&As — grouped by theme (safety, AI, cost, process, fit, scope).
3. Link-outs — to book, articles, evidence.
4. Invitation — light, at the end.

**Abstraction level:** Concrete, plain-spoken. No thesis restatement.

**CTA posture:** One CTA at the end. Most questions end with a link-out, not a sales pitch.

**Red flags:**

- Marketing-flavored answers ("Great question! Our platform is uniquely...").
- Evasive answers to pricing, scope, or AI limits.
- No link-outs to deeper content.

**Must-have:** honest scope answers, AI limits, link-outs.
**Must-not:** re-teach the thesis; hide pricing; make unverifiable claims.

---

## Book (`/book`, `/book/read/[slug]`)

**Job:** The **authoritative home** of *From Fragmentation to Movement* (fragmentation thesis, two intelligences, six stages). `/book` is the landing; `/book/read/*` is the reading experience. **Not** the AI Stewardship Sequence staircase — that lives at `/articles/ssss-field-guide-for-organizational-leaders` (`SSSS_FIELD_GUIDE_PATH` in `src/lib/canon-routes.ts`).

**Arc for `/book`:**

1. Hero — names the book; one cross-link to the AI Stewardship Sequence field guide for the operating sequence.
2. Why this exists — one short paragraph.
3. Spine / TOC — chapter list, linked.
4. Endorsements / contributors — if available and verifiable.
5. Export / subscribe — get the book.
6. Link out — to `/fragmentation`, the AI Stewardship Sequence field guide article, `/evidence`, relevant articles.

**Arc for `/book/read/[slug]`:**

1. Chapter header + navigation (prev / next / TOC).
2. Chapter body — canonical manuscript text.
3. Further reading — related articles, related chapters.
4. Subscribe / contact — light.

**Abstraction level:** `/book` is thesis-level; chapter reader is whatever the chapter is.

**CTA posture:** `/book` has one subscribe + one read. Reader has minimal chrome.

**Red flags:**

- `/book` conflates the book with the AI Stewardship Sequence field guide (wrong URL or missing cross-link).
- Chapter reader has aggressive sales CTAs interrupting the text.
- Endorsements are unattributed or fake.

**Must-have:** spine, chapter navigation, honest endorsement attribution.
**Must-not:** duplicate the book opening in marketing copy on `/book`.

---

## Assessment (`/assess`, `/assessment-new`, `/assess/formation`)

**Job:**

- `/assess` — **System Readiness Diagnostic** (operational).
- `/assessment-new` — **Dual-intelligence infrastructure assessment** (philosophical).
- `/assess/formation` — formation maturity (audience-specific depth).

**Semantic separation is non-negotiable.** Do not blend the instruments.

**Arc:**

1. Opening — what is being measured (plain language; no ambiguity about which instrument).
2. Context picker — audience or org type if relevant.
3. Instrument — Likert or equivalent, grouped by dimension.
4. Results — scores + interpretation + suggested next step.
5. Lead capture — opt-in, honest.
6. Next step — routed by result (e.g., high operational readiness → `/walkthrough`; low two-intelligences integration → `/fragmentation` + book).

**Abstraction level:** Plain language. No thesis re-opening; name the dimension being measured.

**CTA posture:** The assessment **is** the CTA. The follow-up is the routed next step.

**Red flags:**

- Nav or hero blur the distinction between `/assess` and `/assessment-new`.
- Questions span both operational and philosophical dimensions without labeling.
- Results page re-teaches the whole thesis.
- No honest "we don't have enough signal yet" state.

**Must-have:** explicit name of what is measured, routed follow-up, honest opt-in.
**Must-not:** merge instruments; hide scope; over-promise diagnosis.

**Ground truth beyond starred:**
- `docs/build/prompts/assessment-dual-intelligence-infrastructure-from-assessment-new.md`

---

## When the page type is unclear

If the route doesn't match any of the above cleanly (e.g., `/evidence`, `/case-studies`, `/pricing`, `/services`, `/contact`), infer the **closest analog** and flag the choice in the output:

- `/evidence` → closest to "proof / system" hybrid; borrow arc from **system** + apply strict proof burden (Pass 5).
- `/case-studies` → closest to **article** (each case = one article); shared page follows **audience** arc.
- `/pricing`, `/services` → closest to **system**; be strict on scope claims and what-is-not-included.
- `/contact` → minimal; arc is just form + trust signals + honest response-time promise.
- `/cookies`, `/privacy`, `/terms` → legal; skip the audit except to verify tone consistency and link integrity.
