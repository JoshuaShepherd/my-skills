---
name: analytics-setup
description: Bootstrap the complete analytics stack for this Next.js 15 + Supabase project — GA4 (org-wide + per-tenant), PostHog, Vercel Analytics, and Supabase-native analytics. Runs sub-skills in sequence and validates each layer.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Bootstrap the full analytics stack: $ARGUMENTS

$ARGUMENTS should include:
- `--providers <list>` — comma-separated subset to install: ga4, posthog, vercel, supabase (default: all)
- `--dry-run` — show what would be done without writing files
- Empty — install everything, prompt for credentials

---

## Before Starting

1. Read `package.json` to identify what analytics packages are already installed
2. Read `src/app/layout.tsx` to understand the root layout structure
3. Read `src/lib/env.ts` to understand existing env var validation patterns
4. Read `src/lib/tenant.ts` and `src/lib/config/tenant.config.ts` for multi-tenant context
5. Grep for existing analytics calls: `gtag\|posthog\|va\.track\|Analytics` across `src/`
6. Check `.env.local.example` for any existing analytics vars

---

## Architecture Overview

```
Analytics Stack (ordered by setup priority)
├── 1. Vercel Analytics       — zero-config page views + Core Web Vitals (free)
├── 2. PostHog                — product analytics, funnels, session replay, feature flags
├── 3. Google Analytics 4     — org-wide + per-tenant reporting, Measurement Protocol
└── 4. Supabase Analytics     — custom events table, per-tenant RLS views, query perf
```

### Multi-Tenant Data Model

All analytics data carries these dimensions:

| Dimension     | Source                          | Use                               |
|---------------|----------------------------------|-----------------------------------|
| `tenant_id`   | `getTenantOrgId()` / env var    | Isolate per-deployment data       |
| `org_id`      | Supabase auth session            | Org-level rollup                  |
| `user_id`     | Supabase `auth.users.id`        | Person-level identity             |
| `user_role`   | Supabase session claims          | Segment by membership tier        |
| `environment` | `process.env.NODE_ENV`          | Filter dev/staging noise          |

---

## Step 1 — Vercel Analytics (start here, zero config)

Run `/vercel-analytics` or follow inline:

```bash
pnpm add @vercel/analytics @vercel/speed-insights
```

Edit `src/app/layout.tsx`:

```tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
```

This gives immediate page view tracking and Core Web Vitals — no env vars needed.

---

## Step 2 — PostHog

Run `/posthog-setup` or follow [posthog-setup/SKILL.md].

Covers: install, provider, person identification, group analytics (org + tenant), session replay, feature flags.

---

## Step 3 — Google Analytics 4

Run `/ga4-setup` or follow [ga4-setup/SKILL.md].

Covers: gtag.js install, org-wide property, per-tenant custom dimensions, event utilities, Measurement Protocol for server-side events, GA4 Admin API for programmatic tenant provisioning.

---

## Step 4 — Supabase Analytics

Run `/supabase-analytics` or follow [supabase-analytics/SKILL.md].

Covers: analytics_events table, RLS per org, per-tenant views, pg_stat_statements, Logflare.

---

## Step 5 — Analytics Dashboard

Run `/analytics-dashboard` or follow [analytics-dashboard/SKILL.md].

Covers: KPI cards, time series charts, funnel views, React Query hooks, per-tenant data scoping.

---

## Step 6 — Audit & Validate

Run `/analytics-audit` or follow [analytics-audit/SKILL.md].

Verifies all providers fire correctly, events are tenant-scoped, no duplicates, privacy compliant.

---

## Environment Variables Checklist

Add to `.env.local.example` and to Vercel Dashboard → Settings → Environment Variables:

```bash
# --- Vercel Analytics ---
# Auto-enabled when deployed to Vercel. No vars needed.

# --- PostHog ---
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com  # or self-hosted URL
POSTHOG_PERSONAL_API_KEY=                          # server-side only (Admin API, CI)

# --- Google Analytics 4 ---
NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-XXXXXXXXXX        # org-wide property
GA4_API_SECRET=                                     # Measurement Protocol server events
GA4_ADMIN_API_KEY=                                  # Admin API (tenant provisioning)

# --- Supabase Analytics (uses existing connection) ---
# No additional vars needed — uses DATABASE_URL from Supabase config
```

---

## Anti-Patterns

- Do NOT fire analytics events before checking `typeof window !== 'undefined'`
- Do NOT hardcode `tenant_id` — always read from `getTenantOrgId()` or session
- Do NOT send PII (email, name) to GA4 — use anonymized user_id (hash or UUID)
- Do NOT initialize PostHog in Server Components — use the client provider pattern
- Do NOT track events in dev without an environment filter (pollutes production data)
- Do NOT skip the audit step — duplicate events silently inflate metrics

---

## Quick Reference — Event Taxonomy

Use snake_case event names consistently across all providers:

```
page_view           — automatic (all providers)
sign_up             — user completes registration
sign_in             — user logs in
course_started      — user begins a course
course_completed    — user finishes all modules
resource_viewed     — user opens a resource
assessment_taken    — user submits an assessment
upgrade_clicked     — user clicks an upgrade/pricing CTA
checkout_started    — user enters Stripe checkout
purchase_completed  — Stripe webhook confirms payment
```
