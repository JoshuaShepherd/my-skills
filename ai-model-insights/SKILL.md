---
name: ai-model-insights
description: Analyze AI model research (from ai-model-research) and generate strategic insights — capability comparisons, cost projections for real workloads, use case routing recommendations, and provider selection guidance. Run ai-model-research first to generate fresh data, then use this skill to interpret it.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

Generate AI model insights and recommendations for: $ARGUMENTS

$ARGUMENTS can include:
- A use case or project description (e.g. `--use-case "RAG chatbot for legal docs"`)
- Monthly volume estimates (e.g. `--volume "500K messages/month"`)
- A budget ceiling (e.g. `--budget "$500/month"`)
- A provider preference or constraint (e.g. `--prefer anthropic`, `--exclude grok`)
- A research snapshot directory (default: latest in `_docs/ai-intelligence/`)
- A quality vs cost priority (e.g. `--priority quality` or `--priority cost`)
- Empty — ask the user for their use case and volume estimates

---

## Purpose

This skill reads the research output from `ai-model-research` and **interprets it strategically** for a specific use case, workload, or decision context. It does not re-scrape the web — it synthesizes the structured data already captured into actionable guidance.

**What it produces:**
- `_docs/ai-intelligence/insights/[slug]-[date].md` — full insight report
- Strategic model selection recommendation with rationale
- Side-by-side cost projections for top 3–5 candidate models
- Use case routing matrix (which model for which task type)
- Risk and lock-in analysis
- Decision scorecard

---

## Phase 1 — Input Gathering

### 1.1 — Load Research Data

First, locate the most recent (or specified) research snapshot:

```
Check: _docs/ai-intelligence/[latest-date]/
Expected files:
  - _OVERVIEW.md
  - providers/openai.md
  - providers/gemini.md
  - providers/claude.md
  - providers/grok.md
  - _PRICING_MATRIX.md
  - _SOURCE_INDEX.md
```

If no research snapshot exists, output:
> "No AI model research found. Run `/ai-model-research` first to generate fresh model data, then re-run this skill."

Note the research date and any data quality flags from the source index.

### 1.2 — Elicit Use Case (if not provided in $ARGUMENTS)

If the user hasn't described their use case, ask these questions:

1. **What is the application?** Describe what users will do with it (e.g., chat with documents, generate code, summarize emails, run autonomous agents).
2. **What are the volume estimates?** Approximate requests/month and average prompt size (input + output tokens per request).
3. **What is the budget ceiling?** Maximum monthly AI API spend acceptable.
4. **What are the non-negotiables?** E.g., data privacy (no training on data), latency requirements, specific modalities needed, SOC 2 / HIPAA compliance, specific geographies.
5. **What's the quality bar?** How critical is accuracy? (Low-stakes content generation vs. medical/legal advice vs. financial decisions.)

Produce an internal **Use Case Brief** capturing:
- Application type
- Primary task types (classification, generation, extraction, reasoning, coding, multimodal)
- Volume profile (requests/month, tokens/request, concurrency)
- Budget ceiling
- Hard constraints
- Quality requirement (1–5 scale)

---

## Phase 2 — Candidate Model Selection

### 2.1 — Filter by Hard Constraints

From all models in the research data, eliminate any that fail hard constraints:
- Missing required modalities
- Insufficient context window
- Unavailable in required region
- Missing compliance certifications
- Exceeds budget ceiling even at minimal usage

### 2.2 — Score Remaining Models

For each surviving candidate, score on a 1–5 scale across these dimensions:

| Dimension | Weight | Scoring Guidance |
|-----------|--------|-----------------|
| **Task Fit** | 30% | Does this model's documented strengths align with the primary task type? |
| **Cost Efficiency** | 25% | How does cost per request compare to alternatives at the stated volume? |
| **Context Window** | 15% | Does the window comfortably fit the expected prompt size with room to grow? |
| **Reliability / Maturity** | 15% | GA vs Preview, known stability, error rate, rate limit generosity |
| **Ecosystem / DX** | 10% | SDK quality, documentation, tooling, function calling support |
| **Strategic Risk** | 5% | Vendor lock-in, pricing stability, provider financial health |

Compute weighted score for each candidate. Present top 3–5 candidates.

### 2.3 — Task-Type Routing Matrix

If the application has multiple task types (e.g., a RAG chatbot that does retrieval, summarization, AND code generation), recommend different models per task:

| Task Type | Recommended Model | Reason | Fallback |
|-----------|------------------|--------|---------|
| [task 1] | [model] | [1-sentence rationale] | [cheaper alternative] |
| [task 2] | [model] | [1-sentence rationale] | [cheaper alternative] |
| [task N] | [model] | [1-sentence rationale] | [cheaper alternative] |

This is one of the highest-value outputs — many teams over-use a flagship model for tasks that a faster/cheaper model handles equally well.

---

## Phase 3 — Cost Projections

### 3.1 — Per-Model Cost Model

For each top candidate model, calculate:

**Inputs required:**
- Requests per month (from use case brief)
- Avg input tokens per request
- Avg output tokens per request
- Cache hit rate estimate (if applicable)
- Batch-eligible % (if applicable)

**Calculation:**
```
Monthly input cost  = (requests × avg_input_tokens / 1_000_000) × input_price_per_1M
Monthly output cost = (requests × avg_output_tokens / 1_000_000) × output_price_per_1M
Cache savings       = (requests × cache_hit_rate × avg_input_tokens / 1_000_000) × (input_price - cached_price)
Batch savings       = (batch_eligible_requests × avg_tokens / 1_000_000) × batch_discount
Monthly total       = input_cost + output_cost - cache_savings - batch_savings
```

Show the math explicitly for the top 3 models.

### 3.2 — Cost Comparison Table

| Model | Provider | Monthly Cost | Per-Request Cost | vs Cheapest | vs Most Expensive |
|-------|----------|-------------|-----------------|-------------|------------------|
| [ranked by total monthly cost] |

### 3.3 — Volume Sensitivity Analysis

Show how costs scale at different volume levels:

| Volume | [Model 1] | [Model 2] | [Model 3] | Break-even Points |
|--------|-----------|-----------|-----------|------------------|
| 10K req/mo | $X | $X | $X | |
| 100K req/mo | $X | $X | $X | |
| 500K req/mo | $X | $X | $X | |
| 1M req/mo | $X | $X | $X | |
| 5M req/mo | $X | $X | $X | |

Note any volume thresholds where a different model becomes cost-optimal.

### 3.4 — Budget Scenario Planning

Given the stated budget ceiling:

- **Conservative scenario** (50% of projected usage): cost = $X → [fits/doesn't fit]
- **Expected scenario** (100% of projected usage): cost = $X → [fits/doesn't fit]
- **Growth scenario** (3× projected usage): cost = $X → [fits/doesn't fit]
- **Budget ceiling reached at:** [X requests/month on recommended model]

### 3.5 — Cost Optimization Opportunities

Flag every applicable optimization with estimated savings:

| Optimization | Applicable Models | Estimated Savings | How to Implement |
|-------------|------------------|-------------------|-----------------|
| Prompt caching | [models] | [X%] | Cache system prompts and shared context |
| Batch API | [models] | [50% typical] | Non-realtime jobs: offline processing |
| Smaller model routing | [models] | [X%] | Route simple tasks to fast/cheap models |
| Context compression | All | [X%] | Summarize long conversation histories |
| Response streaming | [models] | [latency, not cost] | Improve perceived latency |
| Fine-tuning | [models] | [X%] at high volume | Shorter prompts via fine-tuned defaults |

---

## Phase 4 — Strategic Analysis

### 4.1 — Provider Risk Assessment

For each provider in the running, assess:

| Provider | Financial Stability | Pricing Volatility | Data Privacy | Lock-in Risk | Regulatory Risk |
|----------|--------------------|--------------------|--------------|-------------|----------------|
| OpenAI | | | | | |
| Google | | | | | |
| Anthropic | | | | | |
| xAI | | | | | |

**Lock-in risk dimensions:**
- API compatibility (OpenAI-compatible vs proprietary)
- Data portability (can you take conversation history elsewhere?)
- Model availability guarantees (deprecation timelines)
- Pricing change history and patterns

### 4.2 — Build vs. Multi-Provider Strategy

Recommend one of:

**A) Single-provider strategy** — Use one provider for all tasks
- Pros: simpler integration, single billing, consistent behavior
- Cons: single point of failure, no leverage in pricing negotiations
- Recommended when: starting out, < $1K/month, low fault-tolerance requirements

**B) Primary + fallback strategy** — One main provider, one fallback for reliability
- Pros: reliability, negotiation leverage
- Cons: dual integration overhead
- Recommended when: production systems with SLA requirements

**C) Task-routed multi-provider** — Best model per task type
- Pros: optimal cost and capability for each task
- Cons: integration complexity, multiple billing relationships
- Recommended when: > $5K/month, diverse task types with different requirements

**D) Abstraction layer strategy** — Use LiteLLM, OpenRouter, or similar
- Pros: provider-agnostic, easy model swapping
- Cons: additional latency, vendor dependency on abstraction layer
- Recommended when: teams prioritizing flexibility over raw latency

### 4.3 — What's Changed Since Training Cutoff

From the source index, call out the most strategically significant changes discovered via live research:
- New model releases that change the landscape
- Significant pricing changes
- New features or capabilities that affect recommendations
- Provider announcements with strategic implications

---

## Phase 5 — Final Recommendation

### 5.1 — Decision Scorecard

Present the final scoring matrix:

| Model | Provider | Task Fit | Cost | Context | Reliability | DX | Risk | **Total** |
|-------|----------|----------|------|---------|-------------|-----|------|---------|
| [top candidates ranked] |

### 5.2 — Primary Recommendation

Write a clear, opinionated recommendation:

```
## Primary Recommendation: [Model Name]

**Why this model wins for your use case:**
[3–5 bullet points referencing specific evidence from the research]

**At your projected volume of [X requests/month]:**
- Monthly cost: $[X] (vs $[Y] for the next cheapest viable option)
- Per-request cost: $[X]
- Context headroom: [X tokens available vs [Y] needed]

**Specific model ID to use:** `[exact-model-id]`
**API base URL:** `[base URL]`
**Pricing tier:** [tier name]

**Start with:** [specific guidance on first integration step]
```

### 5.3 — Alternative Recommendation

```
## Alternative: [Model Name]

**Consider this instead if:**
- [condition 1 — e.g., "budget drops below $X/month"]
- [condition 2 — e.g., "you need real-time audio input"]
- [condition 3 — e.g., "data privacy requirements prevent OpenAI usage"]

**Trade-offs vs primary recommendation:**
- [what you gain]
- [what you give up]
```

### 5.4 — Implementation Checklist

Specific to the recommended model:

- [ ] Create account / API access at [URL]
- [ ] Store API key as `[ENV_VAR_NAME]` in `.env.local`
- [ ] Install SDK: `[install command]`
- [ ] Set default model to `[exact-model-id]`
- [ ] Configure context window limit: [N tokens]
- [ ] Enable prompt caching if applicable
- [ ] Set up cost alerts in provider dashboard at $[budget × 0.8]
- [ ] Review ToS for your use case: [link]

---

## Output Format

```
## AI Model Insights Report
**Generated:** [YYYY-MM-DD]
**Based on research from:** [research date]
**Use case:** [brief description]
**Volume:** [requests/month]

### Recommendation
**Primary:** [Model] — $[X]/month at projected volume
**Alternative:** [Model] — $[X]/month (use if [condition])
**Multi-model routing:** [Yes/No — if yes, brief description]

### Cost at a Glance
| Model | Monthly | Per-Request | Notes |
|-------|---------|-------------|-------|
| [primary] | $X | $X | Recommended |
| [alt 1] | $X | $X | |
| [alt 2] | $X | $X | |

### Top 3 Optimization Moves
1. [Specific action] → saves ~$X/month
2. [Specific action] → saves ~$X/month
3. [Specific action] → reduces latency / improves reliability

### Risk Flags
- [Any provider, pricing, or lock-in risks to be aware of]

### Full Report
See: `_docs/ai-intelligence/insights/[slug]-[date].md`
```

---

## Key Rules

- **Never recommend a model without showing the math.** Cost projections must be explicit, not vague ("cheaper"). Show the formula, the inputs, and the result.
- **Reference the research, not memory.** Every model capability claim should trace to data in the research snapshot, not the agent's parametric knowledge.
- **Acknowledge the research date.** If the research was done N days ago, note it. Model pricing and availability change often.
- **Be opinionated.** The user needs a decision, not a feature matrix. Make a clear primary recommendation with rationale.
- **Task routing is high-value.** If the use case has multiple task types, always recommend a routing strategy — even if all routes go to the same model, making it explicit opens the door for optimization.
- **Show the alternatives.** Always give at least one strong alternative with clear switching conditions.
- **Flag lock-in.** Always note which models have OpenAI-compatible APIs (easy to swap) vs. proprietary APIs (migration cost to switch).
- **Budget math must be honest.** If the projected cost exceeds the stated budget, say so clearly and show which model/volume combination fits within budget.
