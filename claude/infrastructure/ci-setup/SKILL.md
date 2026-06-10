---
name: ci-setup
description: "Set up GitHub Actions CI/CD pipeline for Next.js 15 or Vite + Express — lint, typecheck, unit tests, e2e tests, build validation, and Vercel preview deployment. Writes workflow YAML files and configures branch protection. Use when setting up CI on any new project."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up GitHub Actions CI/CD: $ARGUMENTS

$ARGUMENTS can include:
- "full" — all checks + Vercel deploy (default)
- "checks-only" — lint, typecheck, test — no deploy
- "with-e2e" — include Playwright e2e in CI (default: included)
- "skip-e2e" — skip Playwright (faster CI, less coverage)
- Framework hint: "nextjs" or "vite" (auto-detected)
- Empty — full pipeline auto-detected

---

## Before Starting

1. Read `package.json` for available scripts (lint, typecheck, test:run, build)
2. Check if `.github/workflows/` already exists
3. Read `playwright.config.ts` if present — need baseURL and test config
4. Check if `vercel.json` exists — detect Vercel project setup
5. Run `gh repo view` to get repo name and owner

---

## Architecture

```
.github/
  workflows/
    ci.yml           ← Main CI: lint + typecheck + unit tests (every push/PR)
    e2e.yml          ← E2e tests (PRs to main only — expensive)
    deploy.yml       ← Production deploy gate (merge to main)
  pull_request_template.md
```

---

## Step 1 — Main CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, "slice/**"]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Lint + Typecheck + Unit Tests
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Typecheck
        run: pnpm typecheck

      - name: Unit tests
        run: pnpm test:run
        env:
          CI: true

      - name: Build
        run: pnpm build
        env:
          # Provide all required env vars for build
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.NEXT_PUBLIC_SUPABASE_ANON_KEY }}
          TENANT_ORG_ID: ${{ secrets.TENANT_ORG_ID }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          # Add other required vars here
```

---

## Step 2 — E2E Workflow

Create `.github/workflows/e2e.yml`:

```yaml
name: E2E Tests

on:
  pull_request:
    branches: [main]
  # Allow manual trigger
  workflow_dispatch:

concurrency:
  group: e2e-${{ github.ref }}
  cancel-in-progress: true

jobs:
  e2e:
    name: Playwright E2E
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright browsers
        run: pnpm exec playwright install --with-deps chromium

      - name: Run E2E tests
        run: pnpm test:e2e
        env:
          CI: true
          PLAYWRIGHT_BASE_URL: ${{ secrets.STAGING_URL || 'http://localhost:3000' }}
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.NEXT_PUBLIC_SUPABASE_ANON_KEY }}
          TENANT_ORG_ID: ${{ secrets.TENANT_ORG_ID }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

---

## Step 3 — Required GitHub Secrets

After creating workflows, add these secrets in GitHub → Settings → Secrets → Actions:

**Required for all projects:**
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
TENANT_ORG_ID
DATABASE_URL
```

**For E2E tests:**
```
TEST_USER_EMAIL
TEST_USER_PASSWORD
```

**For Vercel deploy (if applicable):**
```
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
```

**For Stripe (if using payments):**
```
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
```

Add secrets via `gh` CLI:
```bash
gh secret set NEXT_PUBLIC_SUPABASE_URL --body "https://..."
gh secret set NEXT_PUBLIC_SUPABASE_ANON_KEY --body "eyJ..."
# etc.
```

---

## Step 4 — PR Template

Create `.github/pull_request_template.md`:

```markdown
## Summary

<!-- What does this PR do? (1-3 sentences) -->

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Documentation
- [ ] Infrastructure / tooling

## Checklist

- [ ] `pnpm typecheck` passes
- [ ] `pnpm lint` passes
- [ ] `pnpm test:run` passes
- [ ] No hardcoded tenant strings (run `/tenant-check`)
- [ ] No `bg-blue-600` or hardcoded hex colors
- [ ] DB migrations included if schema changed

## Screenshots (if UI changes)

<!-- Before / After -->
```

---

## Step 5 — Branch Protection (optional — manual step)

Configure via GitHub UI → Settings → Branches → Add branch protection rule for `main`:

- Require status checks: `quality` (from ci.yml)
- Require branches to be up to date before merging
- Require linear history (optional — enforces squash/rebase)
- Restrict force pushes

Or via `gh` CLI:
```bash
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["quality"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

---

## Step 6 — Local CI Simulation

Add to `package.json`:
```json
{
  "scripts": {
    "ci": "pnpm lint && pnpm typecheck && pnpm test:run && pnpm build"
  }
}
```

Run `pnpm ci` before pushing to catch failures locally.

---

## Verify

1. Push a branch and open a PR
2. Verify `quality` job runs and passes
3. Verify e2e job runs on PR to main
4. Check CI badge: `gh run list --limit 5`

---

## Anti-Patterns

- NEVER commit secrets to workflow files — always use `${{ secrets.NAME }}`
- NEVER skip `--frozen-lockfile` in CI — prevents unintended updates
- NEVER run e2e on every push to feature branches — too slow
- NEVER set `timeout-minutes` too high — runaway jobs waste CI credits
- NEVER put `DATABASE_URL` (prod) in CI — use a dedicated test DB or Supabase branch
