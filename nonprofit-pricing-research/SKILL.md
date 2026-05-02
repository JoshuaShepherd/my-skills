---
name: nonprofit-pricing-research
description: Produce transparent, defensible pricing intelligence for AI-literacy and applied AI training engagements for nonprofits. Runs a scoping intake, gathers real market comps, and outputs a client-ready memo plus internal pricing workbook with low/base/high ranges and a sensitivity table. Use when asked to price an AI training engagement, write a nonprofit AI training SOW, research what similar programs cost, or prepare a proposal for an AI rollout. NOT for legal, tax, or HR compensation advice.
metadata:
  author: josh
  version: "1.0.0"
---

# Nonprofit AI Training Pricing Research

Turn a vague ask ("we want to roll out Claude across the org") into a defensible pricing package: intake → comps → ranged estimate → client memo. Every number is traceable to either a named comp or a documented assumption. No fabricated vendors, awards, or prices.

## Invocation

```
/nonprofit-pricing-research {org-name}              # Run the full pipeline
/nonprofit-pricing-research --intake-only           # Just capture the scoping answers
/nonprofit-pricing-research --comps-only {segment}  # Pull comps for a segment, no estimate
/nonprofit-pricing-research --refresh {org-name}    # Re-run comps against prior intake
```

## Identity

**Who this skill helps.** Internal leads, fractional CAIOs, or external consultants pricing an AI rollout for a 501(c)(3) or similarly-sized mission-driven org.

**What this skill will not do.**

- Not legal advice, not tax advice, not HR compensation advice.
- Will not output a single "the price is $X" number — only ranges with drivers.
- Will not fabricate comparable vendors, RFP awards, or rate cards. If evidence is thin, say so and recommend validation steps (RFQ, three bids, paid discovery).
- Will not give price-coordination or price-matching guidance. Stay clear of anything that could read as collusion.
- Will not produce pricing that differs based on the client's race, religion, national origin, or other protected class.

## Inputs — scoping intake

Capture these before doing any comp research. If answers are missing, ask. Do not fill gaps with assumptions without flagging them.

### Intake questionnaire (copy-paste to client or fill in with sponsor)

```
ORG BASICS
- Org name, 501(c)(3) EIN (or international equivalent):
- Primary mission area (youth services / healthcare / education / arts / …):
- Staff headcount (FTE + part-time + regular volunteers in staff-adjacent roles):
- Teams to include (name + headcount per team):
- Existing AI tools in use (Claude, ChatGPT, Copilot, Gemini, in-house…):
- Current Anthropic contract status (none / Pro / Team / Enterprise / in sales):

DESIRED OUTCOMES
- What does "success" look like in plain English? (list 3-6 outcomes)
- Who will sign off on the final deliverable?
- Which outcomes are measurable; which are narrative?

DELIVERY SHAPE
- Timeframe (months) and any hard end-date:
- Onsite / remote / hybrid mix (approx % onsite):
- Cohort sizing preference (one big cohort vs small per-team cohorts):
- Languages required:
- Accessibility requirements (captions, WCAG level, alt formats):

DATA & POLICY CONSTRAINTS
- Data categories staff will touch (youth PII, donor PII, PHI, financial, HR…):
- Existing acceptable-use / records-retention policies to align to:
- Regulatory hooks (FERPA, HIPAA-adjacent, state privacy laws, mandated-reporting adjacencies):
- LMS platform (which one, admin contact):

BUDGET
- Budget envelope (range OK):
- Currency:
- Fiscal year boundary:
- Funder constraints (specific restricted gift? grant line item?):
- Discount expectations (nonprofit standard discount? pro-bono hours?):

PROCUREMENT
- Decision process (sponsor + committee + board?):
- RFP or direct? If RFP, required bid format?
- Minimum engagement floor the org will entertain:
```

### Intake quality bar

Before moving to comps, re-read the intake. Every cost driver downstream maps to one of these answers. If an answer would change an assumption by >20%, flag it.

## Process — comparable research ("comps") protocol

### What counts as a comp

A comp must match on at least two of three axes:

| Axis | What to match |
|---|---|
| **Delivery mode** | live hours, async, hybrid — with similar live-hour density |
| **Audience** | nonprofit vs commercial (do not treat Fortune-500 rates as nonprofit comps without labeling) |
| **Depth** | "101 literacy" vs "applied workflows" vs "builder / eval / automation" |

A match on only one axis is a weak comp. Label it that way.

### Evidence types — in descending preference

1. **Public rate cards** and published statements of work (vendor sites, nonprofit consulting directories).
2. **Posted training-vendor pricing** (NTEN, TechSoup, AI-for-Education, Digital Learning Institute, etc.).
3. **Public RFP awards** — government, education, and nonprofit RFP awards; cite jurisdiction and award date.
4. **Industry surveys** — label methodology limitations explicitly. Nonprofit.ist Consultant Rates Survey, Consulting Success, Stack Expert guides.
5. **First-principles modeling** — when evidence is thin, build the estimate from documented hourly/daily rate assumptions, cohort sizing, and prep-to-delivery ratios. Label clearly as modeled, not comped.

### Search strategy

Pull comps from at least three evidence types. Record every source. Minimum six distinct comps for a meaningful range. For each comp, capture:

```
comp_id:
delivery_mode:       live / async / hybrid
audience:            nonprofit / commercial / gov / k12 / higher-ed
depth:               literacy / applied / builder / leadership
cohort_size:
duration:            hours / weeks / months
total_price_usd:
price_per_learner:
price_per_delivery_hour:
source_url:
date_accessed:
confidence:          strong / moderate / weak (based on axes matched + recency)
notes:
```

### Free programs are comps too

Free or heavily subsidized programs (NTEN AI for Nonprofits cohort, Anthropic AI Fluency for Nonprofits, FCNY AI Sprint, Microsoft AI Skills for Nonprofits) are material comps — a client will ask "why pay at all?" The honest answer is one of: customization depth, sandbox-first model with the client's own data, governance artifacts, Anthropic-environment-specific training, on-call office hours, or measurement/reporting. If your proposal does not add one of those, do not propose a paid program — recommend the free one and charge only for a lighter wrap-around.

### Observed market signals vs proposed price

Always separate the two in the output:

- **Observed market signals** — the comps table. You are reporting what exists.
- **Proposed price** — your modeled range based on the intake + the comps. You are recommending.

Never merge them. A client needs to see the comps independently of your recommendation.

## Outputs — three artifacts per engagement

### Artifact 1 — Internal pricing workbook (not client-facing)

A working markdown document with every assumption exposed. Line items:

- **Discovery**: stakeholder interviews, docs review, kickoff design
- **Curriculum adaptation**: foundations + applied + leadership track module design
- **Live facilitation**: workshop delivery hours, with prep-to-delivery ratio noted
- **Async grading / Q&A cap**: weekly hours cap × weeks
- **LMS build**: micro-videos, job aids, worksheets, quizzes (module-count × hrs/module)
- **Office hours**: weekly hrs × weeks
- **Travel**: per-trip cost × number of trips (hybrid or onsite only)
- **Materials**: printed workbooks, asset licensing, design polish
- **Measurement / reporting**: pre/post assessments, quarterly readouts, final exec readout

For each line: **low / base / high** with the hour count, rate, and driver that moved it.

**Rate ranges to use as defaults** (2025–2026 USD; revise if geography differs):

| Role | Hourly range | Daily range |
|---|---|---|
| Senior AI consultant / lead facilitator (nonprofit-leaning) | $175–$300 | $3,500–$6,000 |
| Curriculum designer / instructional designer | $150–$250 | $2,500–$4,500 |
| Junior facilitator / TA for cohort Q&A | $100–$175 | — |
| LMS producer (video + editing + quizzing) | $120–$200 | — |

Cite the source of whichever range you actually use in the totals (see §Source table).

### Artifact 2 — Sensitivity table

What moves the estimate most. Rank the top 5 drivers:

```
driver                       swing (low→high)   pct_of_total   notes
live-facilitation days       $X–$Y              __%            biggest lever
cohort sizing                $X–$Y              __%            fewer cohorts = fewer facilitation hrs
curriculum adaptation hrs    $X–$Y              __%            reusable vs fully custom
LMS production depth         $X–$Y              __%            thin (slides + Loom) vs rich (edited video)
travel frequency             $X–$Y              __%            hybrid only
```

### Artifact 3 — Client-ready memo

~2–3 pages. Format:

```
1. What we heard (intake recap — 3 bullets of outcomes + 3 constraints)
2. Observed market signals (comps table with confidence column)
3. Proposed scope (what's included, what's explicitly out)
4. Price range (low / base / high with one paragraph per tier: what's different at each)
5. What we do not know yet (gaps that would move the number by >20%)
6. How to validate (RFQ language, three-bid recommendation, paid discovery option)
7. Sources (full citation list — never summarize away the URL)
```

## Ethics and accuracy rules

1. **No fabricated vendors, awards, or prices.** If a comp cannot be sourced, do not include it.
2. **Confidence labels on every claim.** Strong / moderate / weak.
3. **Evidence-thin is a result, not a failure.** When comps are sparse, say so in the memo and recommend an RFQ, three bids, or a paid discovery.
4. **Never output a single number.** Always low/base/high with drivers. A single number invites the client to anchor without seeing uncertainty.
5. **Free programs get a fair airing.** Always list NTEN, Anthropic's own AI Fluency for Nonprofits, and any free regional cohort program as part of the comps set, even if your engagement is paid.
6. **No protected-class-based pricing.** Nonprofit-status is fine; the person's demographics are not pricing inputs.
7. **Competition-norm caution.** Do not coordinate, match, or signal pricing to other consultants. This skill gives *estimates* to a *client*, not signals to a peer market.
8. **Transparent assumptions.** Every hour count and rate must have a visible driver. A reader should be able to delete any line and see the total change.

## Source table template (used in every output)

```
| # | Claim | Source | URL | Date accessed | Confidence |
|---|-------|--------|-----|---------------|------------|
```

## Worked example

See `examples/worked-example-180-staff.md` for a full run against a hypothetical engagement (6 teams / 180 staff / hybrid / 9 months).

## Process summary (the pipeline)

1. Load or capture the intake (§Inputs).
2. Sanity-check intake answers against the intake quality bar.
3. Research comps — at least 3 evidence types, minimum 6 distinct entries, with the per-comp schema filled in.
4. Build the pricing workbook line-by-line with low/base/high.
5. Compute the sensitivity table.
6. Write the client memo, clearly separating observed market signals from proposed price.
7. Save:
   - Internal workbook to `docs/build/outputs/pricing/<org>-workbook.md`
   - Client memo to `docs/build/outputs/pricing/<org>-client-memo.md`
   - Comps CSV to `docs/build/outputs/pricing/<org>-comps.csv`
8. Present all three to the user and stop. Wait for corrections on geography, currency, discount policy, minimum engagement size.

## Stop conditions

Stop and ask the user before continuing if any of these are true:

- The intake is missing a budget envelope AND a target timeframe.
- Fewer than 4 defensible comps could be found.
- The proposed range spans more than 3× (low vs high) — that's a sign the intake isn't tight enough.
- The client is subject to a regulator the skill does not know (foreign government, SEC-registered, etc.).

— End of skill —
