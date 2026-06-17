---
name: movemental-publish-gate
description: Pre-publication quality gate for research and authoritative content headed to movemental.ai. Run before posting any article, research synthesis, field guide, footnote source, /voices or /footnotes claim, or long-form doc. Checks ten red-light gates — AI-slop and register-jargon, citation and evidence integrity, factual/hallucination risk, doctrine drift (movement leaders vs orgs, "Trusted voices"), EEAT self-evidence, mechanical correctness, and legal/sensitivity — and returns a RED / YELLOW / GREEN verdict with the exact blocking items and which fix skill to run. A slop, mistake, and quality-control checker that decides "is this safe to publish yet?" Use whenever the user says publish / post / ship / "is this ready" / "check this before it goes live" / "QC this" about Movemental content. Routes to plain-prose, movemental-prose, and movemental-narrative-audit rather than duplicating them.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent, Write
---

Run the publication gate on Movemental content: $ARGUMENTS

`$ARGUMENTS` is a file path, a directory, or pasted prose. Prefix with `gate:` for verdict only (default), or `fix:` to run the routed fix skills after reporting. If empty, ask what to gate.

This skill answers one question: **is this safe to publish on movemental.ai yet, and if not, exactly what blocks it?** It does not rewrite prose itself — it diagnoses, decides, and routes. The specialist skills do the fixing.

---

## How to run it

1. **Read the target** in full, including frontmatter. Note `audience_tier` / `canon_section` / `slug` / `author` / where it will live (`docs/articles/`, `docs/build/research/articles/`, `/footnotes`, `/voices`, home-tier).
2. **Walk all ten gates below in order.** Each gate returns one of: **RED** (blocks publication), **YELLOW** (fix strongly recommended, author may override with reason), **GREEN** (clear). Do not skip a gate because the piece "looks clean" — the slop and citation gates fail most often on polished-looking drafts.
3. **Apply the hard gates** (bottom of file). Any one hard-gate hit forces an overall **RED** regardless of the other nine.
4. **Emit the verdict block** (template at the bottom). Be specific: quote the offending line, name the file:line, and name the exact next action.
5. If invoked with `fix:`, after reporting, launch the routed skills for each RED/YELLOW gate (see the routing column).

Higher public surfaces raise the bar. A `/footnotes` claim or a home-tier stat is held to the strictest reading of every gate; an internal `raw/` research note is held mainly to citation integrity and doctrine.

---

## The ten gates

### 1. Register & AI-shaped prose → does `plain-prose` / `movemental-prose` need to run?
The user's first question is always "does the prose skill need to run?" Answer it here.

Scan for the **register markers** (see `references/red-light-checklist.md` §1, and the watchlist that ships with `plain-prose`): substrate, scaffold, leverage, surface (v.), artifact, load-bearing, robust, orchestrate, operationalize, unlock, north star, flywheel, unpack, interrogate, problematize, deeply/fundamentally, "it's worth noting," "at the end of the day." Run the **costume-or-term-of-art test** before flagging — a real term of art in its home field is fine.

Also scan for **AI cadence tells**: stacked tricolons, symmetrical "It's not X, it's Y" repeated, em-dash overload, hedge stacking, a conclusion that only restates the intro, "In today's rapidly evolving…", title-cased section headers, bullet lists where prose belongs.

- **RED** — register markers are load-bearing (the argument leans on costume words) OR three or more distinct AI-cadence tells. → Route to **`plain-prose`** (register/jargon) then **`movemental-prose`** (Movemental line-level cadence).
- **YELLOW** — a handful of swappable costume words or one or two cadence tells. → Recommend `plain-prose`.
- **GREEN** — reads like a person talking to one senior leader.

### 2. Citation & evidence integrity (EEAT dimension B)
The backbone. Every **material or empirical** claim that a reader could act on or quote must be traceable. Label each load-bearing claim: **Sourced** (author/date/publication/URL) · **Attributed** (named org, no specific report) · **Unsourced** · **Contradicted** (better evidence weakens it).

- **RED** — any load-bearing claim is **Unsourced** on a public surface; a **Contradicted** or fabricated-precision stat is used (e.g. a bare "68%", "studies show," broken-telephone figures); empirical claims presented as theological/ethical certainty without a layer label.
- **YELLOW** — claims are Attributed but not Sourced; gaps not yet marked "to verify."
- **GREEN** — material facts Sourced, limits stated, primary + synthesis clearly separated.
- Reference: `docs/build/notes/eeat-research-content-qualification-rubric.md` (movemental-ai repo) Dimension B and the per-claim confidence table; `docs/research/authoritative-sources-ai-nonprofits-faith-formation.md`.

### 3. Factual accuracy & hallucination
Names, dates, book/article titles, org names, quotes, and links must be real and verifiable. AI drafts invent plausible titles, misattribute quotes, and fabricate URLs.

- **RED** — a quote/attribution/figure can't be traced; an invented or misremembered book title, org, or person; a dead or fabricated link; a real person assigned words or positions they didn't say.
- **YELLOW** — a citation that's probably right but unverified; a paraphrase that risks misquoting.
- Verify links with `WebFetch` or `Bash` (curl -I) when in doubt. Cross-check named entities against the leader research and corpus before trusting them.

### 4. Doctrine alignment → does `movemental-narrative-audit` need to run?
Check against Movemental canon (see `references/red-light-checklist.md` §4 and the canonical doctrine doc).

- **RED (hard gate)** — **doctrine drift**: movement leaders placed as a fourth audience funnel/sibling card; any recruiting/roster/"nominate a leader" framing; the public label for the movement-leader surface is anything other than **"Trusted voices"** (not "Committed voices," "Scenius," "ambassadors," "partners"); "Scenius" used as a public H1; the two-intelligences / six-stage / infrastructure model misstated.
- **YELLOW** — framework vocabulary drifts but the argument is recoverable. → Route to **`movemental-narrative-audit`**.
- Canon: `docs/build/strategy/movement-leaders-as-ecosystem-layer.md`; CLAUDE.md "Canonical doctrine."

### 5. EEAT self-evidence
Does the piece earn Experience, Expertise, Authoritativeness, Trust — or just assert them? Honest limits and counter-arguments stated? Author identifiable? Quotable, stable claims a machine could lift?

- **RED** — makes authority claims it doesn't back; no honest limits on a piece whose whole job is credibility; anonymous on a surface that needs a named voice.
- **YELLOW** — thin counter-argument pass; few extractable claims. Reference EEAT rubric Dimensions C and E.

### 6. Mechanical correctness
- **RED** — leftover placeholders (`[TODO]`, `[RE-VALIDATE]`, `lorem`, `TK`, `XXX`, `<placeholder>`); broken internal links; missing/invalid frontmatter where the surface contract requires it (`src/lib/articles-schema.ts`); a duplicate of existing canon (grep the articles/research index before publishing a "new" piece).
- **YELLOW** — heading hierarchy skips, prose width, spelling/typos, markdown that renders wrong.

### 7. Legal / sensitivity / pre-decision
- **RED (hard gate)** — persona/seat entities presented as real leaders; unconfirmed pricing, scholarships, partnerships, or outcomes stated as fact; anything that "cannot be quoted without misleading" (EEAT Dimension E ≤ 4); private/internal strategy leaking onto a public surface without redaction.

### 8. Scope & audience fit
- **YELLOW** — leader dossier content pushed into the *org* research series (different product); marketing copy dressed as research; internal ops notes promoted to a public article. Cap and redirect rather than publish in the wrong place.

### 9. Originality & duplication
- **RED** — re-argues "settled thinking" (corpus-audit Part 3) without new primary evidence; near-duplicate of an existing article. → Mine for footnotes instead of publishing.

### 10. Surface readiness (the wiring)
- **YELLOW** — claims not yet mapped to the `claim` + `cite` + `footnote` registry shape (`src/lib/citations/eeat-registry.ts`); no stable slug; internal links to canon not named. Not a publication blocker by itself, but list it so it isn't forgotten.

---

## Hard gates — any one forces overall RED

1. A **load-bearing claim is Unsourced**, or a **Contradicted / fabricated stat** appears, on a public surface (Gate 2).
2. An **unverifiable quote, attribution, title, or link** (Gate 3).
3. **Doctrine drift** — fourth funnel, recruiting/roster, wrong public label, "Scenius" as public H1 (Gate 4).
4. **Placeholders / RE-VALIDATE markers** left in the body (Gate 6).
5. **Persona/unconfirmed entities or pre-decision facts** stated as real (Gate 7).

A piece can be beautifully written and still RED on any of these. Prose polish never overrides an integrity gate.

---

## Verdict block (emit this)

```text
PUBLISH GATE — [path or title]
Surface: [docs/articles | /footnotes | /voices | research raw | home-tier | …]
Overall: 🔴 RED — do not publish  |  🟡 YELLOW — publish with fixes  |  🟢 GREEN — clear

Gate                         Light   Blocking finding (file:line)            Route / fix
1  Register & AI prose        🔴/🟡/🟢  …                                       plain-prose · movemental-prose
2  Citation integrity         …       …                                       (fix sourcing) · EEAT rubric B
3  Factual / hallucination    …       …                                       verify before publish
4  Doctrine alignment         …       …                                       movemental-narrative-audit
5  EEAT self-evidence         …       …
6  Mechanical correctness     …       …
7  Legal / sensitivity        …       …
8  Scope & audience fit       …       …
9  Originality / duplication  …       …
10 Surface readiness          …       …

BLOCKERS (must clear before publish):
  - …

NEXT ACTION: [the single most important thing, named precisely — e.g. "Run plain-prose on ¶2–5, then source the '68%' stat in Gate 2, then re-gate."]
```

When unsure between two lights, take the stricter one and say why. The gate exists to keep slop and mistakes off movemental.ai — false-green is the only truly costly error.

---

## What this skill is not

- Not a rewriter. It diagnoses and routes; **`plain-prose`** and **`movemental-prose`** do prose fixes, **`movemental-narrative-audit`** fixes doctrine/argument.
- Not the EEAT *scoring* rubric — that 0–100 model (`eeat-research-content-qualification-rubric.md`) decides *whether a corpus doc is worth promoting*. This gate decides *whether a piece already chosen for publication is safe to ship*. Use the rubric to pick; use this gate to clear.
- Not `alan-voice` / `article-audit` — if the piece is Alan-Hirsch-corpus voice, stop and route there instead.
