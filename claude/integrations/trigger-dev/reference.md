# Trigger.dev doc map (curated)

Authoritative index: `https://trigger.dev/docs/llms.txt` (every page, titled + described).
Any page → raw markdown by appending `.md`. Full dump: `https://trigger.dev/docs/llms-full.txt`.

Prefer the `trigger` MCP server's `search_docs` tool when configured. Only fall back to fetching URLs below when the MCP is unavailable.

## Start here (new to Trigger.dev)

| Topic | URL (add `.md` for raw) |
| --- | --- |
| Introduction | `https://trigger.dev/docs/introduction` |
| Quick start (add to a project) | `https://trigger.dev/docs/quick-start` |
| How it works | `https://trigger.dev/docs/how-it-works` |
| Building with AI (MCP + skills + snippet) | `https://trigger.dev/docs/building-with-ai` |
| Manual setup | `https://trigger.dev/docs/manual-setup` |
| Frameworks, guides & examples | `https://trigger.dev/docs/guides/introduction` |

## Writing tasks

| Topic | URL |
| --- | --- |
| Writing tasks: overview | `https://trigger.dev/docs/writing-tasks-introduction` |
| Tasks: overview | `https://trigger.dev/docs/tasks/overview` |
| schemaTask | `https://trigger.dev/docs/tasks/schemaTask` |
| Scheduled tasks (cron) | `https://trigger.dev/docs/tasks/scheduled` |
| Streaming from tasks | `https://trigger.dev/docs/tasks/streams` |
| Context | `https://trigger.dev/docs/context` |
| Errors & retrying | `https://trigger.dev/docs/errors-retrying` |
| Idempotency | `https://trigger.dev/docs/idempotency` |
| Machines (vCPU/RAM) | `https://trigger.dev/docs/machines` |
| Max duration | `https://trigger.dev/docs/runs/max-duration` |
| Run metadata | `https://trigger.dev/docs/runs/metadata` |

## Triggering, runs, waits, queues

| Topic | URL |
| --- | --- |
| Triggering | `https://trigger.dev/docs/triggering` |
| Runs (lifecycle) | `https://trigger.dev/docs/runs` |
| Concurrency & queues | `https://trigger.dev/docs/queue-concurrency` |
| Wait: overview | `https://trigger.dev/docs/wait` |
| Wait for / until / token | `https://trigger.dev/docs/wait-for`, `.../wait-until`, `.../wait-for-token` |
| Bulk actions | `https://trigger.dev/docs/bulk-actions` |
| Replaying | `https://trigger.dev/docs/replaying` |
| Tags | `https://trigger.dev/docs/tags` |

## Realtime & React hooks

| Topic | URL |
| --- | --- |
| Realtime overview | `https://trigger.dev/docs/realtime/overview` |
| React hooks overview | `https://trigger.dev/docs/realtime/react-hooks/overview` |
| Subscribe (backend) | `https://trigger.dev/docs/realtime/backend/subscribe` |
| Streams to React | `https://trigger.dev/docs/realtime/react-hooks/streams` |
| Trigger from React | `https://trigger.dev/docs/realtime/react-hooks/triggering` |
| Run object schema | `https://trigger.dev/docs/realtime/run-object` |

## AI agents (chat.agent)

| Topic | URL |
| --- | --- |
| AI Agents overview | `https://trigger.dev/docs/ai-chat/overview` |
| Quick start | `https://trigger.dev/docs/ai-chat/quick-start` |
| Anatomy / How it works | `https://trigger.dev/docs/ai-chat/anatomy`, `.../how-it-works` |
| Backend / Frontend | `https://trigger.dev/docs/ai-chat/backend`, `.../frontend` |
| Tools / Sessions | `https://trigger.dev/docs/ai-chat/tools`, `.../sessions` |
| API reference | `https://trigger.dev/docs/ai-chat/reference` |

## Config, CLI & build

| Topic | URL |
| --- | --- |
| trigger.config.ts | `https://trigger.dev/docs/config/config-file` |
| Build extensions overview | `https://trigger.dev/docs/config/extensions/overview` |
| CLI intro | `https://trigger.dev/docs/cli-introduction` |
| CLI dev / deploy / init | `https://trigger.dev/docs/cli-dev-commands`, `.../cli-deploy-commands`, `.../cli-init-commands` |

## Deployment & CI

| Topic | URL |
| --- | --- |
| Deployment overview | `https://trigger.dev/docs/deployment/overview` |
| Preview / dev branches | `https://trigger.dev/docs/deployment/preview-branches`, `.../dev-branches` |
| Environment variables | `https://trigger.dev/docs/deploy-environment-variables` |
| GitHub Actions / integration | `https://trigger.dev/docs/github-actions`, `.../github-integration` |
| Vercel integration | `https://trigger.dev/docs/vercel-integration` |
| Versioning | `https://trigger.dev/docs/versioning` |

## Management API (control plane)

| Topic | URL |
| --- | --- |
| Overview | `https://trigger.dev/docs/management/overview` |
| Authentication | `https://trigger.dev/docs/management/authentication` |
| Multiple clients | `https://trigger.dev/docs/management/multiple-clients` |
| Runs (list/retrieve/cancel/replay) | `https://trigger.dev/docs/management/runs/list` (+ `retrieve`, `cancel`, `replay`) |
| Schedules | `https://trigger.dev/docs/management/schedules/create` (+ list/update/…) |
| Env vars / Queues / Batches | `https://trigger.dev/docs/management/envvars/list`, `.../queues/list`, `.../batches/create` |
| Waitpoints | `https://trigger.dev/docs/management/waitpoints/create` |
| Query (TRQL) | `https://trigger.dev/docs/management/query/execute` |
| OpenAPI spec | `https://trigger.dev/docs/openapi.yml`, `https://trigger.dev/docs/v3-openapi.yaml` |

## Observability, limits, self-hosting

| Topic | URL |
| --- | --- |
| Logging, tracing & metrics | `https://trigger.dev/docs/logging` |
| Dashboards / Query (TRQL) | `https://trigger.dev/docs/observability/dashboards`, `.../observability/query` |
| Limits | `https://trigger.dev/docs/limits` |
| Reduce spend | `https://trigger.dev/docs/how-to-reduce-your-spend` |
| Alerts / troubleshooting | `https://trigger.dev/docs/troubleshooting`, `.../troubleshooting-alerts` |
| Self-hosting overview | `https://trigger.dev/docs/self-hosting/overview` |
| Docker / Kubernetes | `https://trigger.dev/docs/self-hosting/docker`, `.../self-hosting/kubernetes` |

## Migration

| Topic | URL |
| --- | --- |
| Migrating from v3 (→ v4) | `https://trigger.dev/docs/migrating-from-v3` |
| Upgrading packages | `https://trigger.dev/docs/upgrading-packages` |
| From n8n / Mergent | `https://trigger.dev/docs/migration-n8n`, `.../migration-mergent` |

## Official AI tooling for this repo

| Topic | URL |
| --- | --- |
| MCP introduction | `https://trigger.dev/docs/mcp-introduction` |
| MCP tools | `https://trigger.dev/docs/mcp-tools` |
| Skills | `https://trigger.dev/docs/skills` |
