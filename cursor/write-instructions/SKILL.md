---
name: write-instructions
description: Author or refine agent instructions — use when asked to write a system prompt, create or update agent instructions, compose instruction layers (identity, theme, mode, style, dynamic context), or tune agent voice and behavior.
---

Author or refine agent instructions: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for prompt engineering guidance:
   - Use `mcp__openai-docs__search_openai_docs` with query "system instructions best practices" for latest recommendations
   - Use `mcp__openai-docs__search_openai_docs` with query "agent instructions" for agents-specific patterns
2. Read the existing instruction architecture to understand the composable pattern:
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/core.ts` — identity + voice markers + failure modes
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/themes.ts` — theme-specific layers (metanoia, movemental, mdna)
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/modes.ts` — pedagogical modes (teacher, coach, reflection, mentor, companion)
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/styles.ts` — interaction styles (conversation, challenge, socratic, evaluative, explainer)
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/context.ts` — dynamic user context per run
3. Read the writing assistant instruction pattern:
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/writing-assistant/instructions.ts` — `buildWritingAssistantPrompt()` with pluggable content sources
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/writing-assistant/instructions/identity.ts` — voice identity template
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/writing-assistant/instructions/content-forms.ts` — content form templates
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/writing-assistant/instructions/examples.ts` — voice calibration examples

## Instruction Architecture

Instructions are composed from **layers** that are concatenated at runtime:

```
┌─────────────────────────────────┐
│  STATIC (cached by dimension key)│
│  ┌───────────────────────────┐  │
│  │  Core Identity            │  │  — who the agent IS, voice markers, failure modes
│  │  + Theme Layer            │  │  — theological/framework lens
│  │  + Mode Layer             │  │  — pedagogical approach
│  │  + Style Layer            │  │  — interaction pattern
│  └───────────────────────────┘  │
├─────────────────────────────────┤
│  DYNAMIC (fresh per run)        │
│  ┌───────────────────────────┐  │
│  │  User Context             │  │  — name, role, language, kairos, engagement
│  │  + Conversation History   │  │  — continuity from prior turns
│  │  + Page/Content Context   │  │  — what the user is currently viewing
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Static sections are cached by key `{theme}-{mode}-{style}` (max 100 entries) for performance.
### Dynamic sections are NEVER cached — they change per run.

## Writing Instructions

### Core Identity Section
Define who the agent is. Include:
- **Role statement**: "You are [name], a [role] who [purpose]."
- **Voice markers**: 3-5 dimensions that define the voice (e.g., Christocentric Anchoring, Pastoral Warmth, Narrative Imagery, Theological Depth, Prophetic Intensity)
- **Signature elements**: Recurring phrases, metaphors, or framing devices the voice uses
- **Failure modes**: What the agent must NOT do (e.g., "Never simplify theological terms", "Never invent citations")

### Theme/Mode/Style Layers
Each adds a focused paragraph or two. Keep them modular — they should make sense in any combination.

### Dynamic Context Section
Built from `RunContext` at runtime. Use the `DynamicInstructionsGenerator` pattern:

```typescript
export const myDynamicInstructions: DynamicInstructionsGenerator = async (
  baseInstructions: string,
  context: Record<string, unknown>
) => {
  const sections: string[] = [baseInstructions];

  if (context.userName) {
    sections.push(`## User Context\nYou are speaking with ${context.userName}.`);
  }

  return sections.join('\n\n');
};
```

## For Writing Assistant Instructions

Use the pluggable content source pattern from movemental-dashboard:

```typescript
export function buildWritingAssistantPrompt(content: AgentPromptContent): string {
  return [
    content.headerTemplate,        // from voice_identities table
    content.coreIdentity,          // from voice_identities table
    content.platformContext,       // from voice_identities table
    buildContentFormSection(content.contentForms),  // from content_form_templates table
    buildExamplesSection(content.examples),          // from writing_examples table
  ].filter(Boolean).join('\n\n');
}
```

This allows org-specific voice swapping without code changes.

## Rules

- Never hardcode tenant-specific names, content, or theological positions — use `brandConfig` or DB-backed content
- Keep total instruction length under 10,000 tokens (static + dynamic combined)
- Voice markers should be descriptive enough for the LLM to calibrate tone
- Failure modes are as important as positive instructions — always include them
- Test instruction changes by running the agent and checking voice fidelity
- For book-related agents, include mandatory retrieval instructions ("Always use file_search before answering questions about specific books")
- Use markdown formatting in instructions — LLMs parse it well
- Check OpenAI docs MCP for any changes to instruction handling or token limits
