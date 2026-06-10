---
name: movemental-prose
description: Audit and fix line-level prose in Movemental articles, book chapters, field guides, paratext, emails, and site copy. Catches fuzzy openings, bare cross-references, unanchored abstractions, drift vocabulary, and AI-shaped cadence — so the piece reads like a thoughtful human guide writing for senior leaders, not like AI-polished content. Use before publishing any Movemental prose.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Audit and/or fix Movemental prose: $ARGUMENTS

`$ARGUMENTS` should be a file path, pasted prose, or a directory. Prefix with `audit:` for diagnosis only, `fix:` to apply in-place edits for Critical/High findings, or omit for audit-then-fix. If no argument, ask what to audit.

---

## Before you start

Read these every invocation (they change between runs):

1. **Target piece** — including its frontmatter (`audience_tier`, `canon_section`, `slug`, `author`).
2. **[docs/content/terminology-registers.md](../../../docs/content/terminology-registers.md)** — the endorsed / tolerated / flagged term lists. Source of truth, edited by hand. Re-read on every run.
3. **A representative exemplar** — `docs/articles/the-fragmentation-tax.md` for opening, grounding, and structural diagnosis; `docs/articles/sandbox/the-three-kinds-of-value.md` for named-role grounding. These are the reference cadence.

Determine the audience arm from frontmatter (`audience_tier`, or inferred from path: `sandbox/` = executive; `manuscript-ordered/` = book; others from the piece itself).

---

## What this skill is not

- Not `alan-voice` / `article-audit` — those enforce Alan Hirsch's Christocentric + APEST voice for the sibling repo. If the piece has heavy Jesus/Kingdom/Gospel density and lives in or references the alan-hirsch corpus, stop and recommend `alan-voice`.
- Not `movemental-narrative-audit` — that runs on argument-level alignment (two intelligences, six stages, pathways). Do not re-litigate those here.
- Not a line editor that rewrites for elegance. Josh's voice has cadence and rhetorical structure. This skill catches when those devices stack into AI-telltale patterns — not when they appear at natural rates.

---

## The six checks

Run each in order. For each, quote the passage, mark severity, and propose a specific rewrite. Severity: **Critical** = must fix before publish; **High** = fix unless the author overrides; **Medium** = suggest.

### 1. Opening clarity — Critical

Read the first 60–90 words. By the end of them, can a tired executive director answer all three?

- **Who is this for?** A named role or situation should be on the page.
- **What concrete situation is in view?** A scene, an artefact, a real pressure — not only a mood.
- **Why keep reading for ten more minutes?** The stakes should be legible.

If any are missing, this is Critical.

**Do not** flag literary openings that answer the three questions inside the first paragraph (e.g., `the-fragmentation-tax.md` opens with a donor scene and lands the stakes by word 80).

**Do** flag openings that spend the first paragraph in mood, philosophy, or atmosphere before naming a reader or a situation.

**Repair move:** Rewrite the opening to lead with a named role under specific pressure, or a single concrete artefact. Mood can stay as a half-sentence, not as the structural opener.

### 2. Bare cross-references — High

Grep the piece for markdown links whose surrounding sentence is `See [Title](path)` or similar bare pointer. For each:

- **Load-bearing link** — the sentence names what the reader finds there and why it matters *here*. Keep.
- **Bare pointer** — the sentence is effectively a footnote. Demote to an end-of-piece block.

If a piece has more than two bare pointers, that is a pattern, not a slip. Collapse them into a single `## Where this connects` section at the close, using this template:

```
## Where this connects

- **[Title](path)** — one sentence on what the reader finds there and why it matters.
- **[Title](path)** — …
```

Inside the body, keep only links that the sentence itself uses to advance the argument. The exemplar: `the-fragmentation-tax.md` has zero inline cross-references and remains complete. The counter-exemplar: `the-movemental-thesis.md` has ~20 bare `See [Title]` pointers — that is the pattern to collapse.

### 3. Unanchored abstractions — High

For each specialised or capitalised noun in the piece (fragmentation tax, signal collapse, citation economy, stewardship, formation, two intelligences, movement-shaped imagination, orbits and infra channels, etc.), check: is there a concrete anchor within three sentences? An anchor is one of:

- A named role acting in a specific situation
- A specific artefact (a donor note, a board packet, a thank-you email, a sermon series, a four-hundred-piece archive)
- A number, date, or location
- A named pressure (a board review, a donor fall-off, a staff turnover event)

Abstractions stacked without anchors read as AI. One abstraction per paragraph is fine; three abstractions in a row without an anchor is a flag.

**Repair move:** Insert a concrete anchor using this pattern: `<abstract claim>. A <specific role> <specific action>, and <specific consequence>.` Or cut the abstraction if it was not load-bearing.

### 4. Drift vocabulary — High

Cross-check against the **Flagged** list in `docs/content/terminology-registers.md`. For each flagged term found:

- Count occurrences across the piece.
- Apply the replacement specified in the registers file (e.g., "load-bearing" → plain restatement after the second use).
- If the term is endorsed, move on.
- If tolerated, confirm the piece glosses it on first use.

The registers file is the extensible list. Do not flag terms not on that list; do surface any repeating specialised noun as a candidate for Josh's review at the end of the audit ("Terms to consider adding to registers:").

### 5. AI-cadence clustering — Medium

Josh's voice has real rhythm. Tricolons, antithesis, and aphoristic sentences appear naturally. The flag is *clustering*, not individual use.

In any single paragraph, count AI-signature devices:

- **Tricolon** — three parallel short sentences or clauses. *"It fills slots. It satisfies calendars. It disappears."*
- **Antithesis / "Not X. Y."** — one sentence negates, the next affirms. *"Sincerity is not the scarce resource. Structure is."*
- **Aphoristic closer** — a short italicised or blockquoted sentence summarising the paragraph. *"The order is the framework."*
- **Meta-adjective stacks** — "load-bearing claim," "structural pressure," "decisive layers," "moral theater" used as compressed shorthand.

Flag a paragraph when **three or more** devices appear in it. Flag a piece when an aphoristic blockquote closer appears more than once outside the final section.

**Repair move:** Rewrite the weakest instance in the paragraph into plain declarative prose. The paragraph's rhythm should still work — if it doesn't, the rhythm was doing work the argument should have done.

### 6. Audience-mismatch vocabulary — Medium

Identify the audience arm (church, nonprofit, institution, movement leader) from frontmatter or context. Cross-check against the **Audience-mismatch flags** section of the registers file. For each mismatched term, either:

- Replace with the sector-appropriate equivalent (registers file suggests defaults).
- Swap the example entirely (a sermon series → a research brief; a major gift → a program renewal).
- Cut the aside if it does not serve the main argument.

Preserve ecumenical phrasing — Movemental's own register is deliberately multi-sector. The flag is when a piece drifts into single-sector dialect without acknowledgement.

---

## Output

### Audit mode

```
# Prose audit: <title or path>

**Readiness:** PUBLISH READY / NEEDS REVISION / MAJOR REVISION
**Audience:** <arm from frontmatter>
**Word count:** <n>

## Findings

### 1. Opening clarity — <CRITICAL / OK>
<quoted first 90 words>

<diagnosis: which of who-for / what-situation / why-now is missing>

**Rewrite:**
<concrete proposed opening, ~60-90 words>

### 2. Bare cross-references — <HIGH / OK>
<count> total. Worst offenders:

- Paragraph N: "See [Title](path)" — demote.
- …

**Recommended Read-next block:**
<the collapsed ## Where this connects block, one line per link>

### 3. Unanchored abstractions — <HIGH / OK>
- "<abstraction>" (para N) — no anchor within three sentences. Proposed anchor: <specific>
- …

### 4. Drift vocabulary — <HIGH / OK>
| Term | Count | Action |
| --- | --- | --- |
| load-bearing | 4 | Replace second, third, fourth occurrence with plain restatement. |
| … | | |

**Terms to consider adding to registers:** <any recurring specialised noun not on the list>

### 5. AI-cadence clustering — <MEDIUM / OK>
- Paragraph N: 3 devices (tricolon + antithesis + meta-adjective). Proposed cut: <which one and what to>.
- Aphoristic blockquote closers: <count>. Keep only the final one.

### 6. Audience-mismatch — <MEDIUM / OK>
- "<term>" in para N — mismatched for <arm>. Replace with "<suggested>".

---

## Priority fix list (max 10)

1. [CRITICAL] Opening — rewrite per above.
2. [HIGH] Cross-references — demote 11 to Where this connects block.
3. …

## Terms Josh should triage for the registers file

- <any new drift candidates surfaced>
```

### Fix mode

For every Critical and High finding, apply Edit calls in place. Medium findings go into a "Suggestions not applied" list at the end.

After edits, report:

```
# Fixes applied: <path>

- Rewrote opening (Critical)
- Collapsed N bare cross-references into Where this connects (High)
- Anchored N abstractions with concrete examples (High)
- Replaced N drift term instances per registers (High)

## Suggestions not applied (Medium)
- Paragraph N: AI-cadence cluster — consider cutting antithesis in sentence 2.
- …

## Terms Josh should consider adding to docs/content/terminology-registers.md
- <term> — seen <count> times across <pieces>.
```

---

## Pre-return checklist

- [ ] Read the registers file this run (not cached from memory).
- [ ] Audience arm identified from frontmatter or context.
- [ ] All six checks run; each quoted passage is real text from the piece.
- [ ] Every proposed rewrite preserves Josh's argument and voice — no flattening to neutral explainer tone.
- [ ] No rewrite introduces new drift vocabulary or new unanchored abstractions.
- [ ] In fix mode, every Edit traces to a specific finding.
- [ ] New drift candidates surfaced for Josh's triage at the end.

## Design notes

- The registers file is the only extensible surface. Add terms there; this skill will read them next run.
- Budgets are soft and paragraph-scoped, not per-piece. Clustering is the signal, not raw counts.
- When in doubt, preserve the author's voice. Flagging a pattern costs little; a bad auto-rewrite costs trust.
