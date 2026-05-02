# Worked example — 6 teams / 180 staff / hybrid / 9 months

**Hypothetical client:** "RiverCity Youth Collective" (not a real org — label as example).
**Run date:** 2026-04-16.

This example runs the full `nonprofit-pricing-research` pipeline end-to-end. Every comp links to a real public source. Every pricing assumption is visible.

---

## 1. Intake (filled)

```
ORG BASICS
- Org name: RiverCity Youth Collective (example)
- Primary mission: youth services + after-school programs + seasonal camps
- Staff headcount: 180 (145 FTE + 35 part-time / program seasonal)
- Teams to include (6):
    1. Executive + Finance                  8 people
    2. Programs — After-school              42 people
    3. Programs — Camps & Residential       58 people
    4. Fundraising / Development            18 people
    5. Marcom / Digital                     14 people
    6. Ops / IT / HR / Volunteer Coord.     40 people
- Existing AI tools: staff-level ChatGPT Plus on personal accounts; no org contract
- Anthropic contract status: in active sales conversation; targeting Enterprise (>150 seats rule)

DESIRED OUTCOMES
- Every staff member completes Foundations track within 6 months
- Each of the 6 teams ships 2 documented sandbox use cases by month 9
- Governance doc published, acceptable-use signed by all staff, incident playbook tested once
- Leadership can speak to board about AI posture, retention, and ROI by month 6
- Sponsor: COO. Final sign-off: CEO + Board Governance Committee.

DELIVERY SHAPE
- 9 months (Q1 start through Q3 finish)
- Hybrid: ~40% onsite (roughly 5 onsite trips across the year)
- Cohort sizing: foundations org-wide in 2 large cohorts; applied in per-team cohorts
- English only
- Captions required on all async video; WCAG 2.1 AA

DATA & POLICY CONSTRAINTS
- Youth PII, donor PII, volunteer screening records in scope
- No PHI expected (camp medical intake is kept in a separate HIPAA-scoped system and stays there)
- Existing records-retention schedule (general ops); no existing AI acceptable-use doc
- LMS: TalentLMS (admin contact known)

BUDGET
- Envelope: $150K–$280K USD (flexible; board will approve up to $300K on a strong case)
- USD; FY July–June
- No single restricted gift; general operating + a small capacity-building grant
- Expectation: nonprofit-standard discount on rates

PROCUREMENT
- Direct (no formal RFP); board governance committee review
- Minimum engagement floor: ~$75K (below that they'd prefer to self-serve with free courses)
```

---

## 2. Observed market signals — comps table

Eight comps, at least three evidence types. Sources accessed 2026-04-16.

| # | Program / Vendor | Mode | Audience | Depth | Cohort size | Duration | Price | Per learner | Source | Confidence |
|---|---|---|---|---|---|---|---|---|---|:-:|
| 1 | **Anthropic AI Fluency for Nonprofits** | async | nonprofit | literacy | self-paced | self-paced | **$0** | $0 | https://anthropic.skilljar.com/ai-fluency-for-nonprofits | strong |
| 2 | **NTEN AI for Nonprofits Tech-Readiness Cohort** | hybrid peer-learning | US nonprofit | literacy + applied | org-level | 6 months, 8–10 hrs/mo | **$0** (selected orgs) | $0 | https://www.nten.org/learn/nonprofit-tech-readiness/ai-for-nonprofits | strong |
| 3 | **NTEN AI for Foundations Professional Certificate** | async self-serve | foundations / nonprofit | literacy → intermediate | individual | multi-course | $500 member / $1,000 non-member | $500–$1,000 | https://www.nten.org/learn/professional-certificates/ai-for-foundations | strong |
| 4 | **NTEN individual AI courses** | async | nonprofit | literacy | individual | per course | $60 member / $120 non-member | $60–$120 | https://www.nten.org/education/courses/ | strong |
| 5 | **FCNY AI for Nonprofits Sprint (NYC cohort)** | hybrid peer-learning | nonprofit | literacy | 5–10 per org | 4–6 months | **$0** (funded by OpenAI / Robin Hood Foundation) | $0 | https://www.fcny.org/aisprint/ai-for-nonprofits-sprint-nyc-cohort/ | strong |
| 6 | **Microsoft AI Skills for Nonprofits** | async | nonprofit | literacy | individual | modular | **$0** | $0 | https://learn.microsoft.com/en-us/training/paths/introduction-to-ai-skills-for-nonprofits/ | strong |
| 7 | **NJIT AI Literacy Microcredential** | async | general + ed | literacy | individual | 10 courses | $200 | $200 | https://ldi.njit.edu/ai-literacy | moderate (audience: general, not nonprofit-specific) |
| 8 | **Independent AI consultant — custom onsite training** (industry survey data) | live onsite | mixed | applied | ~20 staff / day | 1 day | $3,000–$6,000/day | $150–$300/learner/day | https://nicolalazzari.ai/guides/ai-consultant-pricing-us ; https://www.futuristsspeakers.com/how-much-should-you-charge-for-workshops/ | moderate (survey-based; not nonprofit-specific) |
| 9 | **Nonprofit consultant hourly (sector survey)** | mixed | nonprofit | mixed | n/a | n/a | $85–$150/hr | n/a | https://www.nonprofit.ist/nonprofitconsultantsurvey | moderate (self-reported survey) |
| 10 | **Independent AI consultant hourly (general)** | mixed | general | mixed | n/a | n/a | $150–$300/hr | n/a | https://nicolalazzari.ai/guides/ai-consultant-pricing-us | moderate |

### What the comps tell us

- **The floor is zero.** Five of the ten comps are free for a qualifying nonprofit. Any paid proposal has to justify its premium over Anthropic's own free AI Fluency course, NTEN's free cohort, or FCNY's sprint.
- **Off-the-shelf async certificates are ~$60–$500/learner.** That's the price of literacy-only, non-customized, non-governed material.
- **Custom onsite training lands at $3,000–$6,000/day.** A single training day for 20 staff is ~$150–$300/learner/day — but that is *delivery only*, no curriculum adaptation, no LMS, no follow-through.
- **The gap the paid proposal must fill:** custom → sandbox-first → governance artifacts → Anthropic-environment-specific → 9-month accountability → measurement & reporting. If the proposal doesn't include those, it shouldn't cost more than the free options.

---

## 3. Proposed scope (what's in, what's out)

### In

- Discovery (stakeholder interviews with 6 team leads + 2 execs; docs review; kickoff design)
- Foundations track for all 180 staff (async LMS + 2 live org-wide sessions per cohort)
- Applied tracks — tailored per team (3 track variants: program, fundraising, marcom; 6 applied workshops per team)
- Leadership / governance track (exec briefings + quarterly reviews)
- Sandbox-first adoption: each team ships 2 documented use cases with ethics notes
- LMS build in TalentLMS: ~20 modules with job aids, quizzes, reflection prompts
- Weekly office hours (Slack / Zoom) for 36 weeks
- Governance artifacts: acceptable-use doc, data-boundary map, incident playbook, retention policy draft
- Pre/post-assessment + quarterly readouts + final exec readout
- Hybrid delivery: ~5 onsite trips (kickoff, mid-year, major team workshops, closeout)

### Explicitly out (and why)

- Legal review of the governance artifacts (RiverCity's counsel owns this)
- Full HIPAA audit (scope is non-PHI; if scope grows, revisit under separate SOW)
- Building custom software / API integrations (Anthropic's connectors cover the CRM need)
- Ongoing moderation after month 9 (can be added as a retainer)
- Translation / localization (English only in scope)

---

## 4. Internal pricing workbook

All amounts in USD. Rate ranges anchored to comps #8–#10.

### 4.1 Line items

| # | Line | Low hrs | Low $ | Base hrs | Base $ | High hrs | High $ | Driver / rate |
|---|---|--:|--:|--:|--:|--:|--:|---|
| 1 | Discovery | 24 | 4,200 | 30 | 6,750 | 40 | 11,000 | @ $175 / $225 / $275 per hr |
| 2 | Curriculum adaptation | 100 | 17,500 | 140 | 31,500 | 180 | 49,500 | @ $175 / $225 / $275; ~20 modules |
| 3 | Live facilitation | 16 days | 56,000 | 20 days | 90,000 | 24 days | 132,000 | @ $3,500 / $4,500 / $5,500 per day (comp #8 range) |
| 4 | Async Q&A cap (36 wks) | 100 | 15,000 | 144 | 25,200 | 180 | 36,000 | @ $150 / $175 / $200 per hr |
| 5 | LMS build (TalentLMS) | 120 | 18,000 | 160 | 32,000 | 220 | 55,000 | @ $150 / $200 / $250 per hr |
| 6 | Office hours (36 wks × 2 hrs) | 60 | 12,000 | 72 | 18,000 | 90 | 27,000 | @ $200 / $250 / $300 per hr |
| 7 | Travel (trips) | 4 | 7,200 | 6 | 14,400 | 8 | 28,000 | @ $1,800 / $2,400 / $3,500 per trip |
| 8 | Materials | — | 2,000 | — | 4,000 | — | 8,000 | printed books, stock media, design polish |
| 9 | Measurement & reporting | 30 | 6,000 | 50 | 11,250 | 70 | 19,250 | @ $200 / $225 / $275 per hr |
|   | **Totals** | | **$137,900** | | **$233,100** | | **$365,750** | |

### 4.2 Per-learner math (180 staff, 9 months)

| Tier | Total | Per learner | Per learner / month |
|---|--:|--:|--:|
| Low | $137,900 | $766 | $85 |
| Base | $233,100 | $1,295 | $144 |
| High | $365,750 | $2,032 | $226 |

**Context:** vs NTEN's $500–$1,000/learner async certificate (comp #3), the Base case sits at ~$1,295/learner for a 9-month, custom, sandbox-enabled, governance-producing program. That gap is justifiable; the High case only is if the board wants a substantially richer LMS or more onsite days.

---

## 5. Sensitivity table

Ranked by dollar swing.

| Rank | Driver | Low → High swing | % of total | Notes |
|:-:|---|--:|--:|---|
| 1 | Live-facilitation days (line 3) | $56K → $132K (Δ $76K) | 30–36% of total | Biggest lever. Negotiable via cohort consolidation. |
| 2 | LMS build depth (line 5) | $18K → $55K (Δ $37K) | 13–15% | Thin (slides + Loom) vs rich (edited video + animation) |
| 3 | Curriculum adaptation hrs (line 2) | $17.5K → $49.5K (Δ $32K) | 13–14% | Reusable base curriculum vs fully custom per team |
| 4 | Async Q&A cap (line 4) | $15K → $36K (Δ $21K) | 10–11% | Weekly hour cap is the lever — 3 vs 5 hrs/wk |
| 5 | Travel frequency (line 7) | $7.2K → $28K (Δ $21K) | 5–8% | 4 trips vs 8 trips |

**Immediate negotiation levers if the client's budget is tight:**

1. Consolidate cohorts (e.g., Programs After-school + Camps = 1 cohort instead of 2) → saves ~$20–30K.
2. Ship LMS in "thin" mode (scripted slides + recorded walkthroughs, no studio video) → saves ~$20K.
3. Reduce onsite from 5 trips to 3 → saves ~$8–12K.

**Levers if the scope expands:**

1. Add a Builder track for Ops/IT (Claude Code, API, evals) → +$30–55K.
2. Add HIPAA-scope module (even if PHI stays out of scope) → +$10–15K + legal review.
3. Add ongoing monthly retainer post-month-9 → $4K–$8K/month.

---

## 6. Client-ready memo (short)

> *This is the document that would actually go to RiverCity's COO / board. Keeps observed market signals distinct from proposed pricing.*

### What we heard

You want every one of the 180 staff to leave this year with three things: (a) confidence that they can use Claude safely on real YouthFront work, (b) per-team documented use cases they actually ship, (c) governance YouthFront can show a board or a donor. Budget envelope is $150K–$280K, with flexibility to $300K on a strong case. Delivery is hybrid, with ~40% onsite.

### Observed market signals

The literacy layer is effectively **free** for qualifying nonprofits: Anthropic's AI Fluency for Nonprofits course, NTEN's free 6-month cohort, FCNY's AI Sprint, and Microsoft AI Skills for Nonprofits all cost $0. Paid, off-the-shelf async certificates range from **$60 to $1,000 per learner** (NTEN, NJIT). Custom onsite training from independent AI consultants lands at **$3,000–$6,000/day** — but that is *delivery only*, without the curriculum adaptation, LMS build, sandbox artifacts, or governance documents this engagement proposes.

### Proposed scope

A 9-month, hybrid, sandbox-first engagement across all 6 teams. Foundations track for every staff member, per-team Applied tracks, and a Leadership / governance track for the exec team and board committee. Deliverables include TalentLMS content, governance artifacts (acceptable-use, data-boundary map, incident playbook, retention policy draft), per-team documented use cases with ethics notes, and a final executive readout. Explicitly out of scope: legal review, PHI handling, custom software, translation, post-month-9 moderation.

### Price range

| Tier | Total | What moves it up | What moves it down |
|---|--:|---|---|
| **Low** — $137,900 | $766/learner | consolidated cohorts, thin LMS, 4 trips, 3 hr/wk Q&A cap | — |
| **Base** — $233,100 | $1,295/learner | per-team applied cohorts, rich LMS, 6 trips, 4 hr/wk Q&A | (recommended) |
| **High** — $365,750 | $2,032/learner | full custom per-team curriculum, studio video LMS, 8 trips | adds a Builder track, deeper measurement |

**Recommendation: the Base tier.** It lands at ~$1,295/learner for a program that free comps cannot deliver (custom, sandboxed, governed). If board appetite runs tighter, pull the three levers in §5.

### What we do not yet know (gaps that could move the number >20%)

- Whether the Anthropic Enterprise sales quote will include or exclude HIPAA readiness at the nonprofit discount.
- Actual TalentLMS admin access — if the current LMS admin can't publish SCORM-packaged video, the LMS line moves up.
- Whether any state-level youth-data law (e.g., IL-BIPA concerns on voice/photo) triggers extra governance work.
- Whether the board committee wants a third-party evaluator (not the vendor) running the pre/post assessment.

### How to validate (if RiverCity wants to pressure-test)

1. **RFQ** three nonprofit-serving AI training vendors (we can share a shortlist).
2. **Paid discovery** — two weeks, ~$12–18K, produces a fixed-scope SOW we can competitively bid.
3. **Strip to free baseline** — enroll all staff in Anthropic AI Fluency + NTEN's free cohort, then buy only the custom wrap-around (sandbox + governance + LMS).

---

## 7. Sources

All URLs accessed **2026-04-16**.

| # | Used for | URL |
|---|---|---|
| 1 | Anthropic AI Fluency for Nonprofits (free) | https://anthropic.skilljar.com/ai-fluency-for-nonprofits |
| 2 | NTEN AI for Nonprofits Tech-Readiness cohort (free) | https://www.nten.org/learn/nonprofit-tech-readiness/ai-for-nonprofits |
| 3 | NTEN AI for Foundations Professional Certificate ($500/$1,000) | https://www.nten.org/learn/professional-certificates/ai-for-foundations |
| 4 | NTEN individual courses ($60/$120) | https://www.nten.org/education/courses/ |
| 5 | FCNY AI for Nonprofits Sprint — NYC cohort (free, funded) | https://www.fcny.org/aisprint/ai-for-nonprofits-sprint-nyc-cohort/ |
| 6 | Microsoft AI Skills for Nonprofits (free) | https://learn.microsoft.com/en-us/training/paths/introduction-to-ai-skills-for-nonprofits/ |
| 7 | NJIT AI Literacy Microcredential ($200) | https://ldi.njit.edu/ai-literacy |
| 8 | AI consultant day-rate benchmark ($3–6K/day) | https://nicolalazzari.ai/guides/ai-consultant-pricing-us |
| 9 | Workshop pricing benchmark | https://www.futuristsspeakers.com/how-much-should-you-charge-for-workshops/ |
| 10 | Nonprofit consultant hourly survey ($85–$150/hr) | https://www.nonprofit.ist/nonprofitconsultantsurvey |
| 11 | AI consultant hourly range ($150–$300/hr) | https://nicolalazzari.ai/guides/ai-consultant-pricing-us |

---

## 8. Readability sanity-check

- Every number in §4 maps to a row in §4.1 and a rate in the table.
- Every comp in §2 has a URL.
- The memo in §6 never mixes "observed market signals" with "proposed price."
- The gap between Low and High is 2.65× — inside the skill's 3× guardrail, so no re-scope alarm.
- The Base case falls inside the client's stated $150K–$280K envelope.

— End of worked example —
