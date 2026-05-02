---
name: analytics-setup
description: Bootstrap the complete analytics stack for any React app — GA4 (org-wide + per-tenant), PostHog, Vercel Analytics, and database-native event tracking. Orchestrates the sub-skills in sequence and validates each layer.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Bootstrap the full analytics stack: $ARGUMENTS

$ARGUMENTS should include:
- `--providers <list>` — ga4, posthog, vercel, db (default: all)
- `--framework <nextjs|vite|remix>` — React framework in use (default: nextjs)
- `--dry-run` — show plan without writing

---

## Before Starting

1. Read `package.json` — identify existing analytics packages
2. Read root layout / entry point — understand provider injection point
3. Check for existing analytics initialization (grep `gtag|posthog|track`)
4. Check for existing env var patterns

---

## Analytics Stack Decision Matrix

| Need                          | Tool                  |
|-------------------------------|-----------------------|
| Page views, traffic sources   | Google Analytics 4    |
| User funnels, session replay  | PostHog               |
| Core Web Vitals (Vercel)      | Vercel Speed Insights |
| Lightweight page views        | Vercel Analytics      |
| Database-level event log      | Custom events table   |
| Error tracking                | Sentry (separate)     |

---

## Setup Order (always follow this sequence)

### 1. Vercel Analytics — zero-config, start here

```bash
pnpm add @vercel/analytics @vercel/speed-insights
```

Add to root layout:
```tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

// At end of <body>:
<Analytics />
<SpeedInsights />
```

### 2. PostHog — product analytics

Run `/posthog-setup` or see `analytics/posthog-setup.md`.

### 3. Google Analytics 4 — marketing analytics

Run `/ga4-setup` or see `analytics/ga4-setup.md`.

### 4. Database Events — first-party persistence

Run `/supabase-analytics` or implement a custom `analytics_events` table.

### 5. Dashboard — visualization

Run `/analytics-dashboard` or see `analytics/analytics-dashboard.md`.

### 6. Audit — validate everything works

Run `/analytics-audit` or see `analytics/analytics-audit.md`.

---

## Universal Multi-Tenant Data Model

For any multi-tenant deployment, every analytics event must carry:

| Dimension     | Description                        |
|---------------|------------------------------------|
| `tenant_id`   | Deployment/tenant identifier       |
| `org_id`      | Organization UUID (from auth)      |
| `user_id`     | User UUID (never email)            |
| `user_role`   | member, admin, etc.                |
| `environment` | production, preview, development   |

Gate all analytics in dev:
```typescript
if (process.env.NODE_ENV !== 'production') return
```

---

## Environment Variables (all providers)

```bash
# Vercel Analytics — no vars needed (auto-configured on Vercel)

# PostHog
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com

# Google Analytics 4
NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GA4_API_SECRET=           # Measurement Protocol (server events)

# Database events — use existing DB connection
```

---

## Standard Event Taxonomy

Use snake_case across all providers for cross-referencing:

```
page_view             sign_up             sign_in
course_started        course_completed    module_viewed
resource_viewed       assessment_taken
upgrade_clicked       checkout_started    purchase_completed
feature_used          search_performed
```
