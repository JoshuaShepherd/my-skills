---
name: ai-model-research
description: Live browser research on all major AI models — OpenAI, Gemini, Claude, and Grok. Extracts authoritative model profiles, capability breakdowns, benchmark data, use case guidance, and full pricing for every model tier. Produces a dated snapshot report with source index for future reference. Run this before ai-model-insights.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

Research and document the current state of all major AI models for: $ARGUMENTS

$ARGUMENTS can include:
- A focus area or use case (e.g. `--focus agentic`, `--focus multimodal`, `--focus coding`)
- A provider filter (e.g. `--providers openai,claude` to limit scope)
- An output directory override (default: `_docs/ai-intelligence/`)
- A specific date context (default: today's date from the environment)
- Empty — run the full research suite for all four providers

---

## Purpose

This skill performs a **live, browser-grounded extraction** of authoritative model intelligence across OpenAI, Google Gemini, Anthropic Claude, and xAI Grok. Because AI model releases, pricing changes, and benchmark updates happen faster than any training cutoff can track, all information must come from **live web sources** fetched during this run — not from the agent's parametric knowledge alone.

**What it produces:**
- `_docs/ai-intelligence/[YYYY-MM-DD]/` — dated snapshot directory
- `_OVERVIEW.md` — executive model landscape map
- `providers/openai.md` — all OpenAI models, pricing, and use profiles
- `providers/gemini.md` — all Google Gemini models, pricing, and use profiles
- `providers/claude.md` — all Anthropic Claude models, pricing, and use profiles
- `providers/grok.md` — all xAI Grok models, pricing, and use profiles
- `_PRICING_MATRIX.md` — unified cross-provider pricing comparison table
- `_SOURCE_INDEX.md` — all URLs fetched during this run, with date and retrieval status

---

## Phase 1 — Date & Cutoff Awareness

Before any research, explicitly note:
1. The current date (from environment context or ask user)
2. The agent's knowledge cutoff date
3. The delta (days/months since cutoff)

State: *"My training cutoff is [date]. Today is [date]. That is [N] days/months of model releases and pricing changes that must come from live web sources. Fetching now."*

This framing ensures no stale parametric data pollutes the output.

---

## Phase 2 — Authoritative Source Discovery

### 2.1 — Primary Source URLs to Always Fetch

Fetch these directly — they are the canonical, first-party sources:

**OpenAI**
- `https://platform.openai.com/docs/models` — full model list with descriptions
- `https://openai.com/api/pricing/` — current pricing for all models
- `https://openai.com/research/` — latest research announcements

**Google Gemini**
- `https://ai.google.dev/gemini-api/docs/models` — full model list
- `https://ai.google.dev/gemini-api/docs/pricing` — Gemini API pricing
- `https://cloud.google.com/vertex-ai/generative-ai/pricing` — Vertex AI pricing

**Anthropic Claude**
- `https://docs.anthropic.com/en/docs/about-claude/models/overview` — full model list
- `https://www.anthropic.com/pricing` — pricing page
- `https://www.anthropic.com/research` — latest research

**xAI Grok**
- `https://docs.x.ai/docs/models` — full model list
- `https://x.ai/api` — pricing and API overview
- `https://x.ai/blog` — latest announcements

### 2.2 — Supplementary Sources

Use web search to find any additional authoritative information:

```
Search queries to run:
1. "OpenAI model lineup 2024 2025 gpt-4o o1 o3 capabilities" site:openai.com OR site:platform.openai.com
2. "Google Gemini models 2025 Pro Ultra Flash comparison" site:ai.google.dev OR site:deepmind.google
3. "Claude 3 Opus Sonnet Haiku Claude 4 models 2025" site:anthropic.com
4. "Grok models xAI 2025 capabilities pricing" site:x.ai OR site:docs.x.ai
5. "AI model benchmark comparison MMLU HumanEval 2025"
6. "LLM pricing comparison OpenAI Anthropic Google 2025"
```

Also fetch any blog posts or release announcements that appear in search results from the official domains.

---

## Phase 3 — Per-Provider Model Extraction

For each provider, extract every currently available model. For each model capture:

### Model Profile Fields

| Field | Description |
|-------|-------------|
| `model_id` | Official API model ID (e.g. `gpt-4o`, `claude-3-5-sonnet-20241022`) |
| `display_name` | Human-readable name |
| `tier` | `flagship` / `balanced` / `fast` / `legacy` / `experimental` |
| `release_date` | When it was released or announced |
| `status` | `GA` / `Preview` / `Deprecated` / `Research Preview` |
| `context_window` | Max input tokens |
| `max_output_tokens` | Max output tokens |
| `modalities_in` | Text, Images, Audio, Video, Documents, Code |
| `modalities_out` | Text, Images, Audio, Code |
| `training_cutoff` | Knowledge cutoff date |
| `strengths` | Top 3–5 capability strengths (from official docs + benchmarks) |
| `weaknesses` | Top 2–3 limitations (from official docs + known issues) |
| `best_for` | Primary use case recommendations |
| `not_ideal_for` | Use cases where this model underperforms |
| `benchmark_scores` | Key benchmarks: MMLU, HumanEval, MATH, GPQA, etc. |
| `features` | Special features: function calling, structured output, streaming, code interpreter, etc. |
| `api_access` | How to access: API only, ChatGPT Plus, Enterprise, Vertex AI, etc. |
| `input_price` | $ per 1M input tokens |
| `output_price` | $ per 1M output tokens |
| `cached_input_price` | $ per 1M cached input tokens (if offered) |
| `batch_price` | Batch API discount pricing (if offered) |
| `free_tier` | Free tier limits (if any) |
| `rate_limits` | Default RPM/TPM limits |
| `source_urls` | URLs where this model's details were found |

### 3.1 — OpenAI Model Suite

Extract the full OpenAI model family. Expected categories (verify against live docs):
- **GPT-4o family**: GPT-4o, GPT-4o mini, and any variants
- **o-series reasoning models**: o1, o1-mini, o1-pro, o3, o3-mini, and any variants
- **GPT-4 Turbo legacy**: Note if deprecated
- **GPT-3.5 legacy**: Note status
- **Embedding models**: text-embedding-3-small, text-embedding-3-large
- **Image models**: DALL-E 3, GPT-image-1
- **Audio/speech**: Whisper, TTS models
- **Moderation**: omni-moderation

For each model, note the "recommended for" guidance from OpenAI's official docs.

### 3.2 — Google Gemini Model Suite

Extract the full Gemini family. Expected categories (verify against live docs):
- **Gemini 2.0 family**: 2.0 Flash, 2.0 Flash-Lite, 2.0 Pro, 2.0 Flash Thinking
- **Gemini 1.5 family**: 1.5 Pro, 1.5 Flash, 1.5 Flash-8B (note if superseded)
- **Gemini 1.0 legacy**: 1.0 Pro (note status)
- **Gemma open models**: Available via API
- **Specialized**: Gemini for Google Workspace, Vertex AI variants

Note the distinction between Gemini API (ai.google.dev) and Vertex AI pricing.

### 3.3 — Anthropic Claude Model Suite

Extract the full Claude family. Expected categories (verify against live docs):
- **Claude 3.5 family**: Claude 3.5 Sonnet, Claude 3.5 Haiku
- **Claude 3 family**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- **Claude 4 family**: Any new releases
- **Claude Instant legacy**: Note if deprecated

Note Anthropic's tier naming convention (Opus = most capable, Sonnet = balanced, Haiku = fast).

### 3.4 — xAI Grok Model Suite

Extract the full Grok family. Expected categories (verify against live docs):
- **Grok-2 family**: grok-2, grok-2-mini, grok-2-vision, grok-2-image
- **Grok-3 family**: Any grok-3 variants announced or released
- **Aurora**: Image generation model
- **Any other xAI models**

Note Grok's unique access channels: X Premium, xAI API.

---

## Phase 4 — Cross-Provider Analysis

After extracting all model data, generate these cross-cutting comparisons:

### 4.1 — Capability Tier Map

Group all models across providers into tiers:

| Tier | Description | Models |
|------|-------------|--------|
| **Frontier** | Most capable, highest cost | [list] |
| **Balanced** | Best capability-to-cost ratio | [list] |
| **Fast/Cheap** | Speed and volume workloads | [list] |
| **Specialized** | Purpose-built (reasoning, vision, etc.) | [list] |
| **Legacy** | Older generation, generally avoid | [list] |

### 4.2 — Context Window Comparison

Rank all models by context window size. Note practical implications.

### 4.3 — Multimodal Coverage Matrix

| Model | Text In | Images In | Audio In | Video In | Text Out | Images Out | Audio Out |
|-------|---------|-----------|----------|----------|----------|------------|-----------|
| [each model] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### 4.4 — Agentic / Tool Use Readiness

Rate each model for agentic use on a scale of 1–5 based on:
- Function/tool calling support
- Structured output / JSON mode
- Multi-step reasoning reliability
- Context utilization quality
- Rate limits and latency

### 4.5 — Benchmark Summary Table

If benchmarks are found in official docs or linked research, compile:

| Model | MMLU | HumanEval | MATH | GPQA | LMSYS | Notes |
|-------|------|-----------|------|------|-------|-------|
| [each model] | | | | | | |

Note: Only include benchmarks explicitly cited by official sources or credible third-party evaluation sites. Flag any benchmarks that appear cherry-picked or incomparable.

---

## Phase 5 — Pricing Matrix

Create `_PRICING_MATRIX.md` with a unified pricing table.

### 5.1 — Per-Token Pricing

| Model | Provider | Input ($/1M) | Output ($/1M) | Cached Input | Batch Input | Batch Output |
|-------|----------|-------------|---------------|--------------|-------------|--------------|
| [all models sorted by input price asc] |

### 5.2 — Free Tiers & Limits

| Provider | Free Tier | RPM | TPM | Daily Limit | Notes |
|----------|-----------|-----|-----|-------------|-------|

### 5.3 — Volume / Commitment Pricing

Document any volume discounts, committed use pricing, enterprise agreements, or special programs (e.g., OpenAI Batch API 50% discount, Anthropic caching discounts).

### 5.4 — Cost Estimation Formulas

Provide concrete cost examples for common workload patterns:

**Pattern 1: 1M chatbot messages/month** (avg 500 input + 200 output tokens each)
- Model X: $[calculation]
- Model Y: $[calculation]
- Cheapest viable option: [recommendation]

**Pattern 2: 100K RAG document queries** (avg 2000 input + 500 output tokens)
- [calculations per model]

**Pattern 3: 10K code generation tasks** (avg 1500 input + 1000 output tokens)
- [calculations per model]

---

## Phase 6 — Source Index

Create `_SOURCE_INDEX.md` with every URL fetched during this research run:

```markdown
# AI Model Research — Source Index
**Research Date:** [YYYY-MM-DD]
**Agent Knowledge Cutoff:** [date]

## Sources Fetched

| # | URL | Provider | Content Type | Status | Notes |
|---|-----|----------|-------------|--------|-------|
| 1 | https://platform.openai.com/docs/models | OpenAI | Model list | ✅ Fetched | [any notes] |
| 2 | ... | | | | |

## Search Queries Run

1. [query] → [N results, top result URL]
2. ...

## Sources Unavailable or Blocked

| URL | Reason | Fallback Used |
|-----|--------|---------------|

## Data Freshness Notes

[Any areas where live data was unavailable and parametric knowledge was used as fallback — flag these clearly]
```

---

## Output Format

After all research and writing is complete, print:

```
## AI Model Research Complete
**Date:** [YYYY-MM-DD]
**Cutoff delta:** [N days since training cutoff]

### Providers Covered
- OpenAI: [N models documented]
- Google Gemini: [N models documented]
- Anthropic Claude: [N models documented]
- xAI Grok: [N models documented]
- Total: [N] models across [N] providers

### Files Created
- `_docs/ai-intelligence/[date]/_OVERVIEW.md`
- `_docs/ai-intelligence/[date]/providers/openai.md`
- `_docs/ai-intelligence/[date]/providers/gemini.md`
- `_docs/ai-intelligence/[date]/providers/claude.md`
- `_docs/ai-intelligence/[date]/providers/grok.md`
- `_docs/ai-intelligence/[date]/_PRICING_MATRIX.md`
- `_docs/ai-intelligence/[date]/_SOURCE_INDEX.md`

### Key Findings (Summary)
- Cheapest frontier model: [model] at $[X]/1M input tokens
- Largest context window: [model] at [N]M tokens
- Most multimodal: [model] — supports [N] input modalities
- Best for agentic use: [model] — [brief reason]
- Biggest change since training cutoff: [what's new]

### Data Quality Flags
[Any areas where live fetching failed and parametric fallback was used]

### Next Step
Run `/ai-model-insights [focus]` to generate analysis, cost projections, and recommendations.
```

---

## Key Rules

- **Live sources only** — Do not produce model cards from memory alone. Every model profile must trace to a fetched URL in the source index. If a page is unavailable, note it and flag any fallback use.
- **No hallucinated pricing** — Pricing changes constantly. If you cannot fetch current pricing, explicitly state the data is from training cutoff and flag it as potentially stale.
- **Dated snapshots** — All output goes in a date-stamped directory so multiple research runs can be compared over time.
- **Acknowledge what changed** — Always note the delta between training cutoff and research date and call out major changes you discovered via live fetch.
- **Benchmark skepticism** — Note when benchmark comparisons are not apples-to-apples (different test sets, self-reported vs. third-party, etc.).
- **Pricing completeness** — Every model that has an API must have pricing. If pricing is unavailable or "contact sales," say so explicitly.
- **Source index is mandatory** — The `_SOURCE_INDEX.md` is required. It makes this research reproducible and auditable.
