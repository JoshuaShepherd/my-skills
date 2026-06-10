---
name: dashboard-agent-audit
description: Sign into the Movemental Studio dashboard via Playwright as EACH movement-leader tenant (or a chosen subset), traverse a route span (dashboard, content-books, settings, profile), surface console/API/runtime errors per tenant, and write per-leader JSON audit reports. Use when asked to dashboard audit, run span audit, surface dashboard errors, check whether each tenant/leader is good to go, Playwright audit, traverse dashboard routes, agent audit dashboard, or smoke-test the dashboard as signed-in users. Works headless on Ubuntu/WSL/CI — do not default to Chrome DevTools MCP.
user-invocable: true
---

# Dashboard Agent Audit

Headless, **per-tenant** signed-in traversal of dashboard.movemental.ai (or local Studio) with structured error reporting. Signs in as each movement-leader in turn (isolated browser context per leader), walks a route span, and reports a per-leader pass/fail table — so it answers "is **each** user good to go?", not "is the default user good to go?".

## When to use

- User asks whether each tenant/leader's dashboard is clean (multi-tenant verification)
- User asks to audit, smoke-test, or "view" dashboard routes as signed-in users
- User wants errors surfaced across a route span (not just one page)
- Ubuntu/WSL environment where Chrome DevTools MCP is unreliable
- Before/after shipping a feature that touches multiple dashboard routes

## When NOT to use

- Pure unit/integration tests → `pnpm test:run`
- Single static page design review → design-audit skill
- Database/content gap analysis only → Supabase MCP + corpus scripts
- Live interactive browsing as primary method → use this skill first, then optional cursor-ide-browser for one failing URL

## Credentials & scope (multi-tenant)

Tenancy is app-layer org scoping: every query is auto-filtered by the **signed-in user's active org** (`base.service.ts`). So a single-user audit only ever exercises one org — it would miss a route that works for the `TENANT_ORG_ID` fallback org (Alan's) but 500s/empties for a leader with incomplete org→leader→corpus linkage. This skill therefore signs in **per leader**.

Per-tenant credentials are resolved automatically — no `TEST_USER_*` env:

- **email** — the `auth.users` email for each leader's `user_id`, queried live from the DB (needs `DATABASE_URL` in `.env.local`; the runner loads it).
- **password** — the leader **slug with separators removed**: `alan-hirsch → alanhirsch`, `roy-moran → roymoran`, `brad-brisco → bradbrisco`. Derived in-memory; **never logged or written to a report**.

The runner audits all 16 active leaders by default; `--slug` narrows to one or a comma-list.

## Quick run

```bash
# App must already be reachable (local `pnpm dev`, or prod). The runner does NOT start a server.
pnpm agent:audit -- --span=dashboard                       # all active leaders
pnpm agent:audit -- --span=profile --slug=alan-hirsch      # one leader, its own dossier
pnpm agent:audit -- --span=settings --slug=roy-moran,brad-brisco
pnpm agent:audit -- --span=dashboard --prod                # https://dashboard.movemental.ai
pnpm agent:audit -- --span=dashboard --concurrency=4        # parallel contexts (default 3)
```

Exit code is non-zero if any tenant failed login or any route failed — usable as a CI gate.

## Agent protocol

1. **Read this skill** when triggered.
2. **Confirm `DATABASE_URL`** is in `.env.local` (the runner resolves tenant emails from it). Never echo it.
3. **Confirm target:** local (`PLAYWRIGHT_BASE_URL` / default `http://localhost:3000`) vs prod (`--prod`).
4. **Ensure the app is reachable** — the runner fetches `<baseURL>/login` first and exits with guidance if not. Start `pnpm dev` for local.
5. **Run** `pnpm agent:audit -- --span=<id> [--slug=…] [--prod]`.
6. **Read** `reports/agent-audit/<span>/summary.json` (combined) and `<slug>.json` (per leader).
7. **Present results** using the template in § Present results — a per-tenant table.
8. **On failures:** read screenshots under `reports/agent-audit/<span>/<slug>/<route>.png`; `_login.png` exists when sign-in itself failed.
9. **Optional cross-check:** Sentry MCP (prod errors), PostHog MCP (session replays), Supabase MCP (the data gap behind an empty/500 route).
10. **Do not** rely on Chrome DevTools MCP for the initial audit pass.

## What each route records

Per route, per tenant: nav HTTP status, redirect-to-`/login` (access failure), console errors, uncaught runtime errors (`pageerror`), and **same-origin** `>=400` responses (app routes, RSC payloads, Next API routes). A route is `ok` only when none of those fire. **Limitation:** cross-origin failures (e.g. direct Supabase REST calls) are not captured — confirm those with Sentry/Supabase MCP.

## Spans

| Span | Command | Covers |
| --- | --- | --- |
| `dashboard` | `--span=dashboard` | Home + all unlocked primary-nav routes (from `dashboard-nav.ts`) + account routes |
| `content-books` | `--span=content-books` | Content, books, media surfaces |
| `settings` | `--span=settings` | Settings landing + every `SettingsSubNav` sub-route |
| `profile` | `--span=profile [--slug=<leader>]` | Each leader's own Author Profile dossier sections |

`--slug=<a,b,c>` filters **which tenants** to audit (applies to every span). Add new spans by creating `tests/e2e/spans/<id>.json` (`{ id, description, routes: ["/…"] }`) — no skill edit needed.

## Auth troubleshooting

| Symptom | Fix |
| --- | --- |
| One leader's `login` = FAIL, others OK | That account's password ≠ slug convention, or the auth user is unconfirmed/disabled. Check `auth.users` for that `user_id`; read `<slug>/_login.png`. |
| Every leader redirected to `/login` | App not honoring sessions, or all logins failing — check the app is the expected build and Turnstile state. |
| Sign-in button disabled ~90s then FAIL | Turnstile blocking automated login — run against a Playwright/dev server with the Turnstile **test** key set, not real prod. |
| `Cannot reach <baseURL>` | Start `pnpm dev` (local) or pass `--prod` / `--base-url=…`. |
| No tenants resolved | `DATABASE_URL` missing in `.env.local`, or `movement_leaders.user_id` → `auth.users` linkage broken. |
| Chromium won't launch on Ubuntu | `pnpm exec playwright install chromium` |

## Present results

```markdown
## Dashboard audit — <span> @ <baseURL>

**Summary:** <fully-clean>/<total> tenants clean · <login-failures> login failure(s)

| Tenant | Login | Clean | Verdict |
| --- | --- | --- | --- |
| alan-hirsch | ok | 16/16 | clean |
| roy-moran | ok | 14/16 | 2 route(s) |
| jamie-roach | FAIL | — | login failed |

### Failures
| Tenant | Route | Kinds | Top message |
| --- | --- | --- | --- |
| roy-moran | /commerce | response | 500 GET /api/commerce/... |

### Screenshots
- reports/agent-audit/<span>/<slug>/<route>.png

### Recommended next steps
1. …
```

## Extending

- New feature area → add `tests/e2e/spans/<feature>.json`; optional dedicated `*-audit.spec.ts` for interaction-heavy flows (see `book-editor-audit.spec.ts`).
- CI → run `pnpm agent:audit -- --span=dashboard` against a preview deploy; the non-zero exit on any failure gates the job. Reports land under `reports/agent-audit/` (gitignored) — upload as artifacts.
- Credentials/IA drift: the runner reads tenants live from the DB and routes from the span JSON, so adding a leader or nav item needs no script edit — only a span update for new routes.
