---
name: agent-handoff
description: Configure multi-agent handoffs — agent registry, delegation rules, and routing logic. Use when setting up agent-to-agent transfers.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Configure agent handoffs: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for handoff patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK handoffs" for SDK-native handoff/transfer support
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK multi-agent" for orchestration patterns
2. Read the existing handoff infrastructure:
   - `src/agents/shared/handoffs.ts` — `AgentRegistry`, `HandoffDecision`, `HandoffHandler`
   - `src/agents/shared/enhanced-agent-bridge.ts` — search for `enableHandoffs` and handoff event handling
   - `src/agents/shared/agent-tracer.ts` — handoff event tracing
3. Read the database schema:
   - `src/lib/database/schema.ts` — search for `agent_handoffs` table (from_agent_id, to_agent_id, trigger_rules, priority)

## Agent Registry

The `AgentRegistry` is a singleton that maps agent names to agent instances:

```typescript
import { agentRegistry } from '@/agents/shared/handoffs';
import { myAgent } from '@/agents/my-agent';
import { expertAgent } from '@/agents/expert';

// Register agents that can participate in handoffs
agentRegistry.register('my-agent', myAgent);
agentRegistry.register('expert', expertAgent);
```

## Handoff Decision Logic

A `HandoffHandler` evaluates whether the current agent should delegate to another:

```typescript
import type { HandoffHandler, HandoffDecision } from '@/agents/shared/handoffs';

export const myHandoffHandler: HandoffHandler = async (
  message: string,
  context: Record<string, unknown>,
  currentAgent: string
): Promise<HandoffDecision> => {
  // Example: route SEO questions to the SEO expert
  const seoKeywords = /\b(seo|search engine|meta tags|keywords|ranking)\b/i;
  if (seoKeywords.test(message) && currentAgent !== 'seo-expert') {
    return {
      shouldHandoff: true,
      targetAgent: 'seo-expert',
      reason: 'User is asking about SEO — delegating to specialist',
    };
  }

  // Example: route writing tasks to writing assistant
  const writingKeywords = /\b(write|draft|edit|rewrite|article|blog post)\b/i;
  if (writingKeywords.test(message) && currentAgent !== 'writing-assistant') {
    return {
      shouldHandoff: true,
      targetAgent: 'writing-assistant',
      reason: 'User needs writing assistance — delegating to specialist',
    };
  }

  return { shouldHandoff: false };
};
```

## Wiring Handoffs

Enable handoffs in the agent's API route:

```typescript
const bridge = createEnhancedAgentBridge(myAgent, {
  agentId: 'my-agent',
  enableHandoffs: true,  // enables the handoff pipeline
  // ... other config
});
```

The bridge will:
1. After receiving the user message, evaluate handoff handlers
2. If a handoff is triggered, switch to the target agent from the registry
3. Record a `handoff` event in the tracer (target agent, reason)
4. Continue execution with the target agent

## Database-Backed Handoffs

For handoff rules managed via admin UI:

```sql
-- agent_handoffs table
INSERT INTO agent_handoffs (from_agent_id, to_agent_id, trigger_rules, priority, enabled)
VALUES (
  '<source-agent-uuid>',
  '<target-agent-uuid>',
  '{"keywords": ["seo", "meta tags"], "confidence_threshold": 0.8}',
  1,
  true
);
```

Load and evaluate at runtime:
1. Query `agent_handoffs` for the current agent's outbound rules (ordered by priority)
2. Evaluate `trigger_rules` against the user message
3. First matching rule wins

## Circular Dependency Prevention

- The registry tracks the current handoff chain
- If agent A → B → A is detected, the second handoff is blocked
- Maximum handoff depth: 3 (configurable)
- Always include `currentAgent` in the handoff decision context

## OpenAI SDK-Native Handoffs

The OpenAI Agents SDK may support native handoffs via the `handoffs` agent property. Check the docs MCP:

```typescript
// If SDK supports native handoffs:
const agent = new Agent({
  name: 'triage',
  handoffs: [expertAgent, writerAgent],  // SDK routes automatically
});
```

If available, prefer SDK-native handoffs over custom `HandoffHandler` logic.

## Rules

- Always register agents in the singleton `agentRegistry` before enabling handoffs
- Handoff decisions must be fast — use keyword matching or lightweight classifiers, not LLM calls
- Log every handoff with reason for observability (tracer does this automatically)
- Prevent circular handoffs — track the chain and enforce max depth
- The user should not notice handoffs — the experience should be seamless
- Preserve conversation context across handoffs (session ID, message history)
- Check OpenAI docs MCP for SDK-native handoff support before implementing custom logic
