---
name: supabase-analytics
description: Set up Supabase-native analytics for any multi-tenant app — custom analytics_events table with RLS per org, aggregated views, pg_stat_statements for query performance monitoring, and optional Logflare log analytics.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Supabase analytics: $ARGUMENTS

$ARGUMENTS should include:
- `--orm <drizzle|prisma|raw>` — ORM to use for table definition (default: drizzle)
- `--dry-run` — show SQL and code without writing

---

## Why First-Party Database Analytics

GA4 and PostHog are great but can't join your data. A first-party events table lets you:
- Join events to your domain entities (courses, users, organizations)
- Query with full SQL flexibility — no API quotas
- Own your data forever — no vendor lock-in
- Compute precise business metrics (completion rates, revenue per cohort)
- Expose per-tenant analytics scoped by RLS — tenants see only their own data

---

## Step 1 — analytics_events Table

### Drizzle Schema

```typescript
export const analyticsEvents = pgTable('analytics_events', {
  id: uuid('id').defaultRandom().primaryKey(),
  organizationId: uuid('organization_id').notNull(),
  userId: uuid('user_id'),                        // nullable — pre-auth events
  sessionId: text('session_id'),
  eventName: text('event_name').notNull(),         // snake_case: course_started
  contentType: text('content_type'),               // course, article, etc.
  contentId: uuid('content_id'),
  properties: jsonb('properties').$type<Record<string, unknown>>(),
  url: text('url'),
  referrer: text('referrer'),
  environment: text('environment').notNull().default('production'),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
}, (t) => [
  index('ae_org_idx').on(t.organizationId),
  index('ae_event_idx').on(t.eventName),
  index('ae_created_idx').on(t.createdAt),
])
```

### Raw SQL (alternative)

```sql
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  session_id TEXT,
  event_name TEXT NOT NULL,
  content_type TEXT,
  content_id UUID,
  properties JSONB DEFAULT '{}',
  url TEXT,
  referrer TEXT,
  environment TEXT NOT NULL DEFAULT 'production',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ae_org_idx ON analytics_events(organization_id);
CREATE INDEX ae_event_idx ON analytics_events(event_name);
CREATE INDEX ae_created_idx ON analytics_events(created_at DESC);
```

---

## Step 2 — RLS Policy

```sql
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- Org members read their own org's events
CREATE POLICY "read_own_org_analytics"
  ON analytics_events
  FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members
      WHERE user_id = auth.uid()
    )
  );

-- Service role inserts (from API routes, not direct client calls)
-- Note: Supabase service role bypasses RLS by default
```

---

## Step 3 — Aggregated Views

```sql
-- Daily event summary per org
CREATE OR REPLACE VIEW analytics_daily AS
SELECT
  organization_id,
  event_name,
  DATE_TRUNC('day', created_at) AS event_date,
  COUNT(*) AS event_count,
  COUNT(DISTINCT user_id) AS unique_users,
  COUNT(DISTINCT session_id) AS unique_sessions
FROM analytics_events
WHERE environment = 'production'
GROUP BY organization_id, event_name, event_date;

-- Content engagement per org
CREATE OR REPLACE VIEW analytics_content_engagement AS
SELECT
  organization_id,
  content_type,
  content_id,
  COUNT(*) FILTER (WHERE event_name LIKE '%_started') AS starts,
  COUNT(*) FILTER (WHERE event_name LIKE '%_completed') AS completions,
  COUNT(DISTINCT user_id) AS unique_users
FROM analytics_events
WHERE environment = 'production'
  AND content_id IS NOT NULL
GROUP BY organization_id, content_type, content_id;
```

---

## Step 4 — Analytics Service

```typescript
// src/lib/analytics/db-events.ts (server-only)

interface TrackInput {
  organizationId: string
  userId?: string
  sessionId?: string
  eventName: string
  contentType?: string
  contentId?: string
  properties?: Record<string, unknown>
  url?: string
  referrer?: string
}

export async function trackDbEvent(input: TrackInput): Promise<void> {
  try {
    await db.insert(analyticsEvents).values({
      ...input,
      environment: process.env.NODE_ENV ?? 'production',
    })
  } catch (error) {
    // Never let analytics failures surface
    console.error('[analytics] DB track failed:', error)
  }
}
```

Always call from server context (API routes, Server Actions, webhooks). Never from browser.

---

## Step 5 — pg_stat_statements (Query Performance)

Enable once as superuser:
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

Query slow statements:
```sql
SELECT
  calls,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  LEFT(query, 100) AS query_preview
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

Find tables with sequential scans (missing indexes):
```sql
SELECT tablename, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;
```

Reset after changes: `SELECT pg_stat_statements_reset();`

---

## Step 6 — Logflare (Optional)

Enable in Supabase Dashboard → Settings → Log Drains → Add Logflare drain.

Captures: Postgres query logs, Auth event logs, Edge Function logs, Storage access logs.

No code changes needed — platform-level integration.

---

## Anti-Patterns

- Do NOT insert events from browser clients — always via server/API route with service role
- Do NOT query `pg_stat_statements` from application code — DBA diagnostic only
- Do NOT store PII in `properties` JSONB — use `user_id` UUID only
- Do NOT skip `environment` filter in views — dev data will corrupt production metrics
- Do NOT over-index — start with `organization_id`, `event_name`, and `created_at` only
