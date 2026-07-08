---
name: trigger-dev
description: >-
  Work with Trigger.dev (v4) — the open-source background jobs framework for
  writing durable tasks, scheduled/cron jobs, waits, Realtime, React hooks, and
  chat.agent AI agents in TypeScript. Use when the user mentions Trigger.dev,
  writes or triggers tasks, sets up trigger.config.ts, uses @trigger.dev/sdk,
  the trigger.dev CLI, the Management API, or asks how background jobs / queues /
  retries work. ALWAYS fetch current docs before writing code.
---

# Trigger.dev

Trigger.dev is an open-source background-jobs framework: write reliable, long-running workflows as plain async TypeScript (no timeouts, elastic scaling, built-in queuing, automatic retries, and real-time monitoring). Run on Trigger.dev Cloud or self-host.

**The current version is v4.** The SDK training data of most models is stale (v2/v3). Do not write Trigger.dev code from memory — fetch the live docs first (below).

## Rule 0: fetch live docs before writing code

Trigger.dev publishes an LLM-friendly doc surface. Use it as the source of truth, in this order:

1. **Official MCP server (best)** — if a `trigger` MCP server is configured, use its `search_docs` tool (works without auth). It returns current, version-pinned docs.
2. **`llms.txt` index** — fetch `https://trigger.dev/docs/llms.txt` to discover every page (a titled + described link list). Use it to locate the exact page(s) you need.
3. **Any page as raw markdown** — append `.md` to any docs URL, e.g. `https://trigger.dev/docs/tasks/overview.md`, `https://trigger.dev/docs/management/overview.md`.
4. **Full dump** — `https://trigger.dev/docs/llms-full.txt` is the entire docs in one file. Use only when you need broad context (large).
5. **Context7 fallback** — resolve `trigger.dev` if the above are unreachable.

See [reference.md](reference.md) for a curated map of the highest-value pages by topic (tasks, triggering, waits, schedules, Realtime, Management API, deployment, self-hosting, AI agents).

## Recommended: install the official tooling

Trigger.dev ships first-party AI tooling. Recommend installing when helping a user set up Trigger.dev in a repo:

```bash
# Add Trigger.dev to an existing project (creates /trigger + trigger.config.ts)
npx trigger.dev@latest init

# Live MCP server: search docs, trigger tasks, deploy, monitor runs
npx trigger.dev@latest install-mcp            # interactive; detects clients
npx trigger.dev@latest install-mcp --client cursor --client claude-code

# Portable skills that teach AI assistants current task/realtime/chat patterns
npx trigger.dev@latest skills

# Run the local dev server (watches ./trigger, registers tasks)
npx trigger.dev@latest dev
```

- **MCP server** = live project interaction (docs search, trigger, deploy, monitor). Add `--readonly` to hide `deploy`/`trigger_task`/`cancel_run`.
- **Skills** = offline instruction sets dropped into `.claude/skills/`, `.cursor/skills/`, `.agents/skills/`, drawing API guidance from a version-pinned reference shipped in `@trigger.dev/sdk`. Install these if the AI keeps emitting old v2/v3 code.
- Both are complementary — install both when possible.

## Non-negotiable v4 patterns

Verify against live docs, but these are the invariants:

- **Import from `@trigger.dev/sdk`.** NEVER `@trigger.dev/sdk/v3`. NEVER `client.defineJob()` (deprecated v2).
- **Every task is a named `export`.** Define with `task()` / `schemaTask()` / `schedules.task()`.
- **Trigger from backend code** with `tasks.trigger<typeof myTask>("task-id", payload)` using a **type-only import** of the task (so task code isn't bundled into your app).
- **`triggerAndWait()` returns a `Result`**, not the output. Check `result.ok` then read `result.output`, or call `.unwrap()`.
- **Never wrap `triggerAndWait` / `batchTriggerAndWait` / waits in `Promise.all`** — unsupported.
- **No task timeouts** by design; use `maxDuration` in config if you need a ceiling.

### Task

```ts
import { task } from "@trigger.dev/sdk";

export const myTask = task({
  id: "my-task",
  retry: { maxAttempts: 3, factor: 1.8, minTimeoutInMs: 500, maxTimeoutInMs: 30_000 },
  run: async (payload: { url: string }) => {
    return { success: true };
  },
});
```

### Triggering (backend)

```ts
import type { myTask } from "./trigger/my-task";
import { tasks } from "@trigger.dev/sdk";

const handle = await tasks.trigger<typeof myTask>("my-task", { url: "https://example.com" });
const batch = await tasks.batchTrigger<typeof myTask>("my-task", [
  { payload: { url: "https://example.com/1" } },
  { payload: { url: "https://example.com/2" } },
]);
```

### Schema-validated task

```ts
import { schemaTask } from "@trigger.dev/sdk";
import { z } from "zod";

export const processVideo = schemaTask({
  id: "process-video",
  schema: z.object({ videoUrl: z.string().url() }),
  run: async (payload) => { /* payload typed + validated */ },
});
```

### Config (`trigger.config.ts`, project root)

```ts
import { defineConfig } from "@trigger.dev/sdk/build";

export default defineConfig({
  project: "<your-project-ref>",
  dirs: ["./trigger"],
});
```

### Waits & errors

```ts
import { wait } from "@trigger.dev/sdk";
await wait.for({ seconds: 30 });
await wait.until({ date: new Date("2025-01-01") });
// wait.forToken(...) for external/human-in-the-loop callbacks

import { AbortTaskRunError, retry } from "@trigger.dev/sdk";
// throw new AbortTaskRunError("won't retry") for permanent failures
// retry.onThrow(fn, { maxAttempts: 3 }) to retry a block, not the whole task
```

## Management API (server-side control plane)

Same `@trigger.dev/sdk` package. Configure once, then use resource namespaces (`runs`, `schedules`, `envvars`, `queues`, `batches`, `waitpoints`).

```ts
import { configure, runs } from "@trigger.dev/sdk";

configure({ secretKey: process.env.TRIGGER_SECRET_KEY }); // omit if env var is set
const completed = await runs.list({ limit: 10, status: ["COMPLETED"] });
```

For multiple projects/environments/preview branches in one process, use `new TriggerClient({...})` per target (no shared global state). See `management/multiple-clients.md`.

## Common gotchas (the AI's own failure modes)

1. Task not exported → won't be registered.
2. Importing from `@trigger.dev/sdk/v3` or using `client.defineJob()` → v2/v3, wrong.
3. Calling `myTask.trigger()` from backend instead of `tasks.trigger("id", payload)`.
4. Treating `triggerAndWait` result as the output (it's a `Result` — use `.ok`/`.output` or `.unwrap()`).
5. `Promise.all` around waits or `*AndWait` calls.
6. Adding manual timeouts to tasks.

## Model / version pinning

This repo's rule: pin versions, never alias. Trigger.dev packages are pinned in `package.json` (`@trigger.dev/sdk`, `@trigger.dev/react-hooks`); upgrade deliberately and read `migrating-from-v3.md` / `upgrading-packages.md` before bumping majors.
