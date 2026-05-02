---
name: writing-agent-builder
description: Architect AI agents that write well — system prompt design, voice integration, tool selection, RAG for source material, guardrails for quality, and multi-agent writing pipelines. Use when building any agent whose primary output is prose (stories, articles, copy, dialogue, scripts).
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent, Bash
---

Build or improve a writing agent: $ARGUMENTS

$ARGUMENTS can include:
- A writing agent concept to architect (`architect: [concept]`)
- An existing agent to audit for writing quality (`audit: [path]`)
- A specific component to build (`component: instructions | tools | guardrails | pipeline | rag`)
- A writing domain: `fiction`, `nonfiction`, `journalism`, `copywriting`, `screenwriting`, `poetry`, `academic`, `conversational`
- An agent framework target: `openai-agents-sdk`, `claude-agent-sdk`, `vercel-ai-sdk`, `langchain`, `custom`
- Empty — ask what the user wants to build

---

## Why Most Writing Agents Produce Bad Prose

Writing agents fail for predictable reasons. Understanding these failures is the foundation of building agents that write well.

### The Five Writing Agent Anti-Patterns

**1. The Content Mill** — The agent has been told WHAT to write but not HOW to write well. It produces structurally correct, stylistically dead prose. Every sentence is medium-length. Every paragraph starts with a topic sentence. It reads like a B+ college essay.

**Fix:** Encode prose craft principles directly in the system prompt. Use the `prose-craft` skill's seven lenses as agent-level directives.

**2. The Voice Cosplayer** — The agent has been given a vague voice description ("write like Hemingway") and produces a caricature — short sentences, fishing references, whiskey. It captures surface features but misses the structural DNA of the voice.

**Fix:** Use the `voice-designer` skill to build a full 6-layer voice profile. Feed the agent specific, measurable voice markers, not impressionistic descriptions.

**3. The Structure Ignorer** — The agent writes from beginning to end in a single pass with no structural awareness. Stories have no arc. Articles have no argument. The reader doesn't know why they're reading.

**Fix:** Encode structural principles from `story-architect` or `nonfiction-craft`. Better yet: use a multi-step pipeline where structure is planned before prose is written.

**4. The Source Fabricator** — The agent invents quotes, citations, facts, and anecdotes. It sounds authoritative but nothing checks out.

**Fix:** RAG pipeline with source material. Guardrails that flag unsourced claims. Instructions that explicitly say "never invent quotes or citations — if you don't have a source, say so."

**5. The Revision-Free Writer** — The agent writes once and delivers. No self-editing, no quality check, no revision pass.

**Fix:** Multi-pass pipeline: draft → self-critique → revise. Or: separate drafting agent and editing agent with handoff.

---

## Architecture Patterns for Writing Agents

### Pattern 1: Single Agent with Rich Instructions

Best for: Conversational writing, short-form content, chat-based writing assistants.

```
User Message → [Writing Agent with detailed instructions] → Response
                    ↑
              Voice profile + craft principles + domain rules
```

**When to use:** The output is < 2000 words, the voice is consistent, and the quality bar is "good enough with occasional greatness."

**System prompt structure:**
```
1. Identity (who the agent is, voice profile)
2. Craft Principles (prose quality directives — from prose-craft)
3. Domain Rules (genre conventions, structural requirements)
4. Source Handling (how to use retrieved context, citation rules)
5. Failure Modes (what never to do)
6. Pre-response Checklist (self-audit before sending)
```

### Pattern 2: Plan-Write-Revise Pipeline

Best for: Long-form content, articles, chapters, scripts.

```
User Request
    ↓
[Planner Agent] → outline + structural plan
    ↓
[Writer Agent] → first draft (using plan + source material)
    ↓
[Editor Agent] → critique + revision notes
    ↓
[Writer Agent] → revised draft
    ↓
Final Output
```

**When to use:** The output is > 2000 words, structural quality matters, and you need consistent quality at scale.

**Agent roles:**
- **Planner**: Structural expertise. Uses `story-architect` or `nonfiction-craft` principles. Output: outline, beat sheet, argument map.
- **Writer**: Voice + craft expertise. Uses `voice-designer` profile + `prose-craft` principles. Writes to the plan.
- **Editor**: Critical reader. Uses `editorial-lens` checklist. Identifies weaknesses, suggests specific revisions.

### Pattern 3: Voice-Switching Agent

Best for: Multi-character fiction, agents that adapt voice to context, brand agents with audience-specific modes.

```
User Request + Context
    ↓
[Router] → selects voice profile
    ↓
[Writer Agent + Dynamic Instructions]
    ↑
    Voice Profile A / B / C (loaded from DB or file)
```

**When to use:** The agent needs to write in multiple distinct voices depending on character, audience, or context.

**Implementation:**
```typescript
const writerAgent = new Agent({
  name: 'Adaptive Writer',
  instructions: (context: RunContext<WritingContext>) => {
    const voiceProfile = getVoiceProfile(context.context.voiceId);
    const craftPrinciples = getCraftPrinciples(context.context.domain);
    return buildWriterPrompt(voiceProfile, craftPrinciples);
  },
});
```

### Pattern 4: Research-Write Agent with RAG

Best for: Non-fiction, journalism, research-backed content.

```
User Request
    ↓
[Research Agent] → searches sources, extracts relevant passages
    ↓
Source material (quotes, data, context)
    ↓
[Writer Agent] → writes using source material + voice + structure
    ↓
[Fact-Check Guardrail] → flags unsourced claims
    ↓
Final Output
```

**When to use:** Accuracy matters. The agent writes about real things and must not fabricate.

**RAG design for writing agents:**
- **Retrieval**: Vector search over source corpus (books, articles, research)
- **Context window management**: Don't dump everything — curate the 3-5 most relevant passages
- **Citation injection**: Retrieved passages include source metadata; the agent must cite them
- **Fallback behavior**: If no source material is found, the agent must say so — never fill the gap with invention

---

## Building the System Prompt

The system prompt is the single most important component of a writing agent. Everything else — tools, RAG, guardrails — is infrastructure. The prompt is the craft.

### Section 1: Identity and Voice

Use the `voice-designer` 6-layer framework. Include:

```markdown
## Who You Are
[Role statement — one paragraph]

## Your Voice
[Voice markers with targets — the quantified profile]

## Signature Elements
[Recurring phrases, metaphor systems, pronoun patterns]

## Never Sound Like
[3-5 failure modes with examples]
```

### Section 2: Craft Principles

Encode the relevant subset of `prose-craft` principles. Don't include all seven lenses for every agent — select the ones that matter most for this domain.

**For fiction agents:**
```markdown
## Writing Quality
- Vary sentence length deliberately. Three longs then a short. Fragments for emphasis.
- Show, don't tell. Level 2-3 on the specificity ladder. Never "she felt sad."
- Verbs carry prose. Cut adverbs. Replace weak verbs. Limit "to be" verbs.
- Enter scenes late, leave early. Skip throat-clearing.
- Every scene must advance plot, reveal character, or deepen theme — ideally two of three.
```

**For non-fiction agents:**
```markdown
## Writing Quality
- Lead with the strongest material. Don't bury the insight in paragraph three.
- Concrete examples before abstract principles. The reader needs to see before they understand.
- One idea per paragraph. If a paragraph argues two things, split it.
- Use the "so what?" test: after every section, the reader should know why it matters.
- Vary paragraph length. A one-sentence paragraph is a spotlight.
```

### Section 3: Structural Awareness

Encode the relevant structural principles from `story-architect` or `nonfiction-craft`:

```markdown
## Structure
[For articles: section architecture with word counts]
[For stories: scene/chapter structure with arc requirements]
[For dialogue: conversation flow patterns]
```

### Section 4: Source Handling

```markdown
## Using Source Material
- When source material is provided in context, USE IT. Ground your writing in real evidence.
- Direct quotes go in blockquotes with full attribution.
- Paraphrases are marked: "Drawing from [source]..."
- NEVER invent a quote, statistic, or citation. If you don't have a source, say so.
- If paraphrasing, the paraphrase must be faithful to the original meaning.
```

### Section 5: Self-Audit Checklist

```markdown
## Before Delivering
- [ ] Voice markers all at target levels?
- [ ] No failure mode violations?
- [ ] Structure complete (all required sections present)?
- [ ] Sources cited where used?
- [ ] Opening sentence creates a question in the reader's mind?
- [ ] Closing sentence lands on an image or challenge, not a summary?
- [ ] No throat-clearing, no "very"/"really", no passive voice without reason?
```

---

## Tools for Writing Agents

### Source Retrieval Tools

```typescript
// Search a corpus of source material
const searchCorpus = tool({
  name: 'search_corpus',
  description: 'Search the source material corpus for passages relevant to the current topic. Use BEFORE writing to ground your prose in real sources.',
  parameters: z.object({
    query: z.string().describe('What to search for'),
    maxResults: z.number().optional().default(5),
  }),
  execute: async (params) => { /* vector search implementation */ },
});
```

### Voice Calibration Tools

```typescript
// Check voice fidelity of a draft
const checkVoice = tool({
  name: 'check_voice',
  description: 'Analyze a passage against the voice profile. Returns scores for each voice marker and flags any failure modes.',
  parameters: z.object({
    text: z.string().describe('The passage to analyze'),
  }),
  execute: async (params) => { /* voice analysis implementation */ },
});
```

### Research Tools

```typescript
// Web research for fact-checking or enrichment
const researchTopic = tool({
  name: 'research_topic',
  description: 'Search the web for factual information about a topic. Use to verify claims or find supporting evidence. Never write factual claims without checking first.',
  parameters: z.object({
    query: z.string().describe('The research question'),
  }),
  execute: async (params) => { /* web search implementation */ },
});
```

---

## Guardrails for Writing Quality

### Input Guardrails

```typescript
// Ensure the writing request is specific enough
const writingBriefCheck = {
  name: 'writing_brief_check',
  validate: async (message: string) => {
    // Flag if the request is too vague to produce quality output
    const hasTopicOrContent = message.length > 20;
    if (!hasTopicOrContent) {
      return { passed: false, reason: 'Please provide more detail about what you want written.' };
    }
    return { passed: true };
  },
};
```

### Output Guardrails

```typescript
// Check for fabricated citations
const nofabricatedSources = {
  name: 'no_fabricated_sources',
  validate: async (output: string, context: Record<string, unknown>) => {
    // Compare cited sources against retrieved source material
    const citations = extractCitations(output);
    const retrievedSources = context.retrievedSources as string[];
    const fabricated = citations.filter(c => !retrievedSources?.some(s => s.includes(c.source)));
    if (fabricated.length > 0) {
      return { passed: false, reason: `Potentially fabricated sources: ${fabricated.map(f => f.source).join(', ')}` };
    }
    return { passed: true };
  },
};

// Check for common prose quality failures
const proseQualityCheck = {
  name: 'prose_quality_check',
  validate: async (output: string) => {
    const issues = [];
    // Check for "very" and "really" abuse
    const veryCount = (output.match(/\b(very|really|quite|rather)\b/gi) || []).length;
    const wordCount = output.split(/\s+/).length;
    if (veryCount / wordCount > 0.005) {
      issues.push('Excessive use of intensifiers (very, really, quite, rather)');
    }
    // Check for passive voice density
    const passivePatterns = /\b(was|were|is|are|been|being)\s+\w+ed\b/gi;
    const passiveCount = (output.match(passivePatterns) || []).length;
    if (passiveCount / wordCount > 0.02) {
      issues.push('High passive voice density');
    }
    if (issues.length > 0) {
      return { passed: false, reason: `Prose quality issues: ${issues.join('; ')}` };
    }
    return { passed: true };
  },
};
```

---

## Mode: Architect

When designing a new writing agent from scratch:

1. **Clarify the writing domain** — What does this agent write? For whom? In what voice?
2. **Select the architecture pattern** (Single / Pipeline / Voice-Switching / RAG)
3. **Build the voice profile** — Use `voice-designer` to create the 6-layer profile
4. **Draft the system prompt** — All 5 sections, with craft principles from `prose-craft`
5. **Design tools** — Source retrieval, research, voice calibration as needed
6. **Design guardrails** — Input validation + output quality checks
7. **Plan the pipeline** — If multi-agent, define handoffs and data flow
8. **Write sample prompts and expected outputs** — Test the design on paper before building

Deliver: Architecture diagram, system prompt draft, tool specifications, guardrail definitions, sample I/O pairs.

## Mode: Audit

When auditing an existing writing agent:

1. Read the agent's system prompt / instructions
2. Read any voice profile or style guide it references
3. Run a test query and evaluate the output against `prose-craft` and `editorial-lens`
4. Score these dimensions:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Voice specificity | [1-5] | Is the voice profile concrete or vague? |
| Craft encoding | [1-5] | Are prose quality principles in the prompt? |
| Structural awareness | [1-5] | Does the agent plan before writing? |
| Source integrity | [1-5] | Are citations required? Is fabrication prevented? |
| Self-audit | [1-5] | Does the agent check its own output? |
| Failure mode coverage | [1-5] | Are anti-patterns explicitly forbidden? |

5. Provide specific recommendations with priority ranking

---

## Rules

- The system prompt is craft, not configuration. Spend time on it. A writing agent is only as good as its instructions.
- Voice profiles must be concrete and measurable. "Be warm and engaging" is worthless. "Use 'we' 45% of the time, metaphor density ~8 per 1000 words, end on images not summaries" is useful.
- Every writing agent needs failure modes. What it must NOT do is as important as what it should do.
- Multi-step pipelines produce better long-form output than single-pass generation. Plan → Write → Edit beats Write.
- RAG is not optional for factual writing. Any agent that writes about real things must have source material and citation requirements.
- Test with edge cases: What happens when the agent doesn't have enough information? When the topic is outside its expertise? When the user asks for something that violates the voice profile?
- The best writing agents feel like they have taste. That comes from the failure modes — from knowing what NOT to write.
