---
name: add-guardrail
description: Add input or output guardrails to an agent — use when asked to validate, filter, or protect agent input/output, block unwanted content, enforce domain scope, or add rate limiting to agent requests.
---

Add guardrails to an agent: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for guardrail patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK guardrails" for SDK-native guardrail support
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK input validation" for request validation patterns
2. Read the existing guardrail implementation:
   - `{{AGENTS_DIR}}/shared/guardrails.ts` — nonEmpty, maxLength, contentFilter, noErrors implementations
   - `{{AGENTS_DIR}}/shared/enhanced-agent-bridge.ts` — `applyInputGuardrails()` and `applyOutputGuardrails()` in the bridge pipeline
3. Read the database schema for guardrail persistence:
   - `{{SCHEMA_PATH}}` — search for `agent_guardrails` and `agent_guardrail_assignments` tables

## Guardrail Types

### Input Guardrails
Validate user messages BEFORE they reach the agent. Return `{ passed: boolean, reason?: string }`.

```typescript
import type { InputGuardrail } from './types';

export function myInputGuardrail(): InputGuardrail {
  return {
    name: 'my_guardrail',
    validate: async (message: string, context?: Record<string, unknown>) => {
      if (someCondition(message)) {
        return { passed: false, reason: 'Specific reason for rejection' };
      }
      return { passed: true };
    },
  };
}
```

### Output Guardrails
Validate agent responses BEFORE they reach the user. Same interface.

```typescript
import type { OutputGuardrail } from './types';

export function myOutputGuardrail(): OutputGuardrail {
  return {
    name: 'my_output_guardrail',
    validate: async (output: string, context?: Record<string, unknown>) => {
      if (containsProblematicContent(output)) {
        return { passed: false, reason: 'Output failed quality check' };
      }
      return { passed: true };
    },
  };
}
```

## Built-in Guardrails Reference

| Name | Type | What it does |
|------|------|-------------|
| `nonEmpty()` | Input & Output | Rejects empty/whitespace-only messages |
| `maxLength(n)` | Input | Rejects messages over n characters (default 10000) |
| `contentFilter()` | Input | Blocks `<script>`, `javascript:`, event handlers (XSS prevention) |
| `noErrors()` | Output | Detects error indicators like "Error:", "Exception:", "undefined" in output |

## Common Guardrail Patterns

### Domain-Specific Content Filter
```typescript
export function theologicalGuardrail(): InputGuardrail {
  return {
    name: 'theological_scope',
    validate: async (message) => {
      // Keep conversations within the agent's domain
      const offTopicPatterns = [/stock prices/i, /sports scores/i, /write me code/i];
      const isOffTopic = offTopicPatterns.some(p => p.test(message));
      return isOffTopic
        ? { passed: false, reason: 'This question is outside my area of expertise.' }
        : { passed: true };
    },
  };
}
```

### Citation Verification (Output)
```typescript
export function requireCitations(): OutputGuardrail {
  return {
    name: 'require_citations',
    validate: async (output, context) => {
      if (context?.isBookRelated && !output.includes('Source:') && !output.includes('—')) {
        return { passed: false, reason: 'Book-related responses must include citations' };
      }
      return { passed: true };
    },
  };
}
```

### Rate Limiting (Input)
```typescript
export function rateLimiter(maxPerMinute: number): InputGuardrail {
  const timestamps: number[] = [];
  return {
    name: 'rate_limiter',
    validate: async () => {
      const now = Date.now();
      const windowStart = now - 60_000;
      timestamps.push(now);
      const recentCount = timestamps.filter(t => t > windowStart).length;
      return recentCount > maxPerMinute
        ? { passed: false, reason: 'Too many requests. Please wait a moment.' }
        : { passed: true };
    },
  };
}
```

## Wiring Guardrails

Add guardrails to an agent's API route via the EnhancedAgentBridge config:

```typescript
const bridge = createEnhancedAgentBridge(myAgent, {
  inputGuardrails: [
    nonEmpty(),
    maxLength(10000),
    contentFilter(),
    myInputGuardrail(),  // add custom guardrail here
  ],
  outputGuardrails: [
    nonEmpty(),
    noErrors(),
    requireCitations(),  // add custom guardrail here
  ],
});
```

## Optional: Database Persistence

For guardrails managed via admin UI:

1. Insert into `agent_guardrails` table (name, type: 'input'|'output', rules JSON)
2. Assign to agent via `agent_guardrail_assignments` (agent_id, guardrail_id, order, enabled)
3. Load at runtime and convert DB rules to guardrail functions

## Rules

- Guardrails must be fast — they run on every request. Avoid LLM calls in guardrails.
- Input guardrails protect the agent; output guardrails protect the user.
- Return clear, user-friendly rejection messages (they may be shown to the end user).
- Never silently modify content in guardrails — either pass or reject.
- Order matters: put cheap checks (nonEmpty, maxLength) before expensive ones.
- Log guardrail rejections for monitoring (the tracer handles this automatically via the bridge).
- Check OpenAI docs MCP for any SDK-native guardrail features that may supersede custom implementations.
