# Red-light checklist — the watchlists behind the ten gates

Detail for `SKILL.md`. Every item is a *signal*, not an automatic kill — run the judgment test named in each section before flagging. The gate's job is to be specific, not trigger-happy.

---

## §1 — Register markers & AI-cadence tells (Gate 1)

### Register-jargon watchlist
This mirrors the watchlist that ships with the **`plain-prose`** skill (`references/register-markers.md`). The decisive test for every word: **could you swap it for a plainer word with no loss of meaning?** Yes → costume, cut it. No → term of art, keep it.

- **Systems / infra / AI English:** substrate · scaffold(ing) · primitive (n.) · surface (v.) · artifact · load-bearing · robust · leverage (v.) · orchestrate · pipeline · stack · surface area · composable.
- **Consulting / strategy English:** operationalize · actionable · optimize · unlock · double down · north star · flywheel · lever · bandwidth (for time) · at scale · value-add · drive (alignment) · ecosystem.
- **Academic / theory English:** unpack · interrogate · foreground/centre · problematize · valence · lens (through the lens of) · modality · instantiate · dialectic.
- **Empty intensifiers & hedges (usually just cut):** deeply · fundamentally · profoundly · "at the end of the day" · "in many ways" · "it's worth noting that" · arguably · "a kind of / a sort of" · meaningfully · materially.

**RED when** these carry the argument ("the relational substrate is the load-bearing primitive"). **YELLOW when** a few are swappable decoration. **GREEN when** the only technical words are genuine terms of art doing real work.

### AI-cadence tells (the "slop" feel)
- Stacked tricolons ("clear, honest, and durable") appearing every paragraph.
- The "It's not X — it's Y" antithesis used more than once or twice.
- Em-dash overload; every sentence a parenthetical.
- Hedge stacking ("it could be argued that perhaps in some sense").
- A conclusion that restates the intro and adds nothing.
- Opener clichés: "In today's rapidly evolving landscape," "Now more than ever," "Imagine a world where."
- Title-Cased Section Headers; bullet lists where connected prose belongs.
- Perfectly symmetrical paragraph lengths; mechanical "Firstly/Secondly/Finally."
- Hollow signposting: "It's important to note," "Let's dive in," "At its core."

Three or more distinct tells → RED. One or two → YELLOW.

---

## §2 — Per-claim confidence labels (Gate 2)

Label every load-bearing claim:

| Label | Meaning | Effect |
|---|---|---|
| **Sourced** | Traceable primary or reputable secondary, with citation | Clears |
| **Attributed** | Named org, no specific report/edition | YELLOW |
| **Unsourced** | Stated as fact, no citation | RED on a public surface |
| **Contradicted** | Better evidence weakens it | RED — flag for rewrite |

Fabricated-precision smells: a bare percentage with no source ("68%"), "studies show / research suggests" with no study, round numbers presented as measured, a statistic whose original was a range now stated as a point. Treat an unsourced headline stat as **Contradicted until proven**.

Layer test: is the claim **empirical** (needs a source), **ethical/theological** (needs to be labeled as conviction, not data), or **advocacy** (needs to be owned as a position)? Empirical claims dressed as certainty are RED.

---

## §4 — Movemental doctrine drift list (Gate 4)

Canon: `docs/build/strategy/movement-leaders-as-ecosystem-layer.md` and CLAUDE.md "Canonical doctrine — movement leaders vs organizations."

RED on any of:
- Movement leaders shown as a **fourth sibling card** beside churches / nonprofits / institutions in an audience hub, grid, or funnel.
- Any **recruiting / roster-growth** surface — "nominate a leader," "join the roster," ambassador funnel. `/voices` is trust and ecosystem proof, never a sign-up.
- The public label for the movement-leader surface is anything other than **"Trusted voices."** Not "Committed voices," "Scenius," "ambassadors," "partners." (Internal type names like `CommittedVoice` / `COMMITTED_VOICES` stay as-is — they're code, not public copy.)
- **"Scenius"** used as a public H1 or headline.
- The **two intelligences**, **six-stage progression**, or **infrastructure thesis** misstated, miscounted, or renamed.
- Organizations not framed as the **primary implementation audience**.

YELLOW when the vocabulary drifts but the structure is recoverable → route to `movemental-narrative-audit`.

---

## §6 — Placeholder & mechanical scan (Gate 6)

Grep the body before clearing:
- `TODO` · `TK` · `XXX` · `FIXME` · `[RE-VALIDATE]` · `lorem` · `<placeholder>` · `[insert` · `[name]` · `???` · trailing "..." stubs.
- Empty/duplicate frontmatter; missing required keys for the surface (`src/lib/articles-schema.ts`).
- Internal links: resolve every `](/…)` and `](../…)`. Dead link → RED.
- Duplication: grep the articles + research index for the title/slug/thesis before publishing a "new" piece.

---

## §7 — Legal / sensitivity scan (Gate 7)

RED on any of:
- A **persona or seat** (demo/placeholder identity) presented as a real leader or customer.
- **Pricing, scholarships, partnerships, headcounts, or outcomes** stated as settled when they're pre-decision or unconfirmed.
- A claim that **cannot be quoted without misleading** (EEAT rubric Dimension E ≤ 4).
- **Internal strategy** (positioning memos, competitor teardown specifics, unreleased plans) on a public surface without redaction.

---

## Quick routing table

| Gate trips RED/YELLOW | Run this skill / action |
|---|---|
| 1 — register / AI prose | `plain-prose` → `movemental-prose` |
| 2 — citation integrity | Source each claim; use EEAT rubric Dimension B; mark "to verify" |
| 3 — factual / hallucination | Verify links (`WebFetch`/curl), cross-check entities against leader research/corpus |
| 4 — doctrine | `movemental-narrative-audit` |
| 5 — EEAT self-evidence | Add limits, counter-arguments, named author; EEAT rubric C & E |
| 6 — mechanical | Fix placeholders, frontmatter, links; dedupe vs index |
| 7 — legal / sensitivity | Redact or confirm before publishing |
| 8 — scope | Move to correct surface (org research vs `/voices` vs marketing) |
| 9 — duplication | Mine for footnotes instead of re-publishing |
| 10 — surface wiring | Map to `eeat-registry.ts`; assign stable slug; name internal links |
