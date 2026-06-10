---
name: supabase-analytics
description: Set up Supabase-native analytics for this multi-tenant platform — custom analytics_events table (RLS-scoped per org), per-tenant views, pg_stat_statements for query performance, and Logflare for log analytics.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Supabase analytics: $ARGUMENTS

$ARGUMENTS should include:
- `--events` — create analytics_events table and service (default: yes)
- `--perf` — set up pg_stat_statements query performance monitoring (default: yes)
- `--logflare` — configure Logflare log analytics (default: optional)
- `--dry-run` — preview SQL and code without writing

---

## Why Supabase Analytics

GA4 and PostHog track user behavior. Supabase analytics tracks:
- **Platform-level events** with full database context (e.g., which exact course_lesson was completed)
- **Query performance** (which queries are slow, how many calls per second)
- **Per-tenant data** fully isolated via RLS — tenants only see their own analytics
- **Organizational metrics** (enrollment counts, completion rates) via aggregated views

---

## Before Starting

1. Confirm Supabase project: `vhaiiiykcukrlyvwlgip` (movemental)
2. Read `src/lib/database/schema.ts` — understand existing table patterns
3. Read `src/lib/tenant.ts` — understand `getTenantOrgId()`
4. Read `src/lib/services/simplified/` — understand service patterns
5. Check if `analytics_events` table already exists via Supabase MCP

---

## Step 1 — analytics_events Table

Add to `src/lib/database/schema.ts`:

```typescript
export const analyticsEvents = pgTable('analytics_events', {
  id: uuid('id').defaultRandom().primaryKey(),
  organizationId: uuid('organization_id').notNull(),
  userId: uuid('user_id').references(() => authUsers.id, { onDelete: 'set null' }),
  sessionId: text('session_id'),           // browser session identifier
  eventName: text('event_name').notNull(), // snake_case: course_started, etc.
  contentType: text('content_type'),       // course, pathway, article, resource
  contentId: uuid('content_id'),           // references the content entity
  properties: jsonb('properties').$type<Record<string, unknown>>(),
  url: text('url'),                        // full URL at time of event
  referrer: text('referrer'),
  userAgent: text('user_agent'),
  environment: text('environment').notNull().default('production'),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
}, (table) => [
  index('analytics_events_org_id_idx').on(table.organizationId),
  index('analytics_events_event_name_idx').on(table.eventName),
  index('analytics_events_created_at_idx').on(table.createdAt),
  index('analytics_events_user_id_idx').on(table.userId),
])
```

Generate and push:

```bash
pnpm drizzle:gen
pnpm drizzle:push
```

---

## Step 2 — RLS Policy

Run this migration via Supabase MCP or SQL editor:

```sql
-- Enable RLS
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- Org members can read their own org's events
CREATE POLICY "analytics_events_org_read"
  ON analytics_events
  FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id
      FROM organization_members
      WHERE user_id = auth.uid()
    )
  );

-- Service role can insert (used by API routes)
CREATE POLICY "analytics_events_service_insert"
  ON analytics_events
  FOR INSERT
  WITH CHECK (true); -- scoped by API route logic, not RLS

-- No direct update or delete for users
```

---

## Step 3 — Per-Tenant Analytics Views

Run via Supabase MCP:

```sql
-- Aggregated event counts per org, per day
CREATE OR REPLACE VIEW analytics_daily_summary AS
SELECT
  organization_id,
  event_name,
  DATE_TRUNC('day', created_at AT TIME ZONE 'UTC') AS event_date,
  COUNT(*) AS event_count,
  COUNT(DISTINCT user_id) AS unique_users,
  COUNT(DISTINCT session_id) AS unique_sessions
FROM analytics_events
WHERE environment = 'production'
GROUP BY organization_id, event_name, event_date;

-- Course engagement per org
CREATE OR REPLACE VIEW analytics_course_engagement AS
SELECT
  organization_id,
  content_id AS course_id,
  COUNT(*) FILTER (WHERE event_name = 'course_started') AS starts,
  COUNT(*) FILTER (WHERE event_name = 'course_completed') AS completions,
  COUNT(DISTINCT user_id) AS unique_learners,
  ROUND(
    COUNT(*) FILTER (WHERE event_name = 'course_completed')::numeric
    / NULLIF(COUNT(*) FILTER (WHERE event_name = 'course_started'), 0) * 100,
    1
  ) AS completion_rate_pct
FROM analytics_events
WHERE content_type = 'course'
  AND environment = 'production'
GROUP BY organization_id, content_id;
```

---

## Step 4 — Analytics Service

Create `src/lib/services/custom/analytics.service.ts`:

```typescript
import 'server-only'
import { db } from '@/lib/database'
import { analyticsEvents } from '@/lib/database/schema'
import { getTenantOrgId } from '@/lib/tenant'
import type { Result } from '@/lib/types'

interface TrackEventInput {
  userId?: string
  sessionId?: string
  eventName: string
  contentType?: string
  contentId?: string
  properties?: Record<string, unknown>
  url?: string
  referrer?: string
  userAgent?: string
}

/**
 * Persist an analytics event to Supabase.
 * Non-blocking — failures are logged but never surface to users.
 */
export async function trackAnalyticsEvent(input: TrackEventInput): Promise<Result<void>> {
  try {
    await db.insert(analyticsEvents).values({
      organizationId: getTenantOrgId(),
      userId: input.userId ?? null,
      sessionId: input.sessionId ?? null,
      eventName: input.eventName,
      contentType: input.contentType ?? null,
      contentId: input.contentId ?? null,
      properties: input.properties ?? {},
      url: input.url ?? null,
      referrer: input.referrer ?? null,
      userAgent: input.userAgent ?? null,
      environment: process.env.NODE_ENV ?? 'production',
    })

    return { success: true, data: undefined }
  } catch (error) {
    // Never let analytics failures bubble up
    console.error('[analytics] Failed to track event:', error)
    return { success: false, error: 'Analytics tracking failed' }
  }
}

/**
 * Fetch daily event summary for the current tenant.
 */
export async function getAnalyticsSummary(days = 30) {
  const orgId = getTenantOrgId()
  const since = new Date(Date.now() - days * 24 * 60 * 60 * 1000)

  return db
    .select()
    .from(analyticsEvents)
    .where(
      and(
        eq(analyticsEvents.organizationId, orgId),
        eq(analyticsEvents.environment, 'production'),
        gte(analyticsEvents.createdAt, since)
      )
    )
    .orderBy(desc(analyticsEvents.createdAt))
}
```

---

## Step 5 — pg_stat_statements (Query Performance)

Enable the extension and check slow queries:

```sql
-- Enable pg_stat_statements (run once as superuser in Supabase SQL editor)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Check top 20 slowest queries
SELECT
  calls,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  ROUND(stddev_exec_time::numeric, 2) AS stddev_ms,
  LEFT(query, 120) AS query_preview
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Reset stats (run before a load test)
SELECT pg_stat_statements_reset();

-- Queries missing indexes (sequential scans on large tables)
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;
```

Create a script at `scripts/check-slow-queries.ts`:

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

const { data } = await supabase.rpc('get_slow_queries')
console.table(data)
```

---

## Step 6 — Logflare (Optional — Log Analytics)

Supabase integrates natively with Logflare for structured log analytics.

Enable in Supabase Dashboard → Settings → Log Drains:
1. Click "Add drain"
2. Choose "Logflare"
3. Connect your Logflare source
4. Select log types: Postgres, Auth, Edge Functions, Storage

This gives you:
- SQL query logs with execution times
- Auth event logs (sign-ins, sign-ups, failures)
- Edge Function execution logs
- Storage access logs

No code changes needed — it's a Supabase platform integration.

---

## Step 7 — Verify

1. Run `pnpm drizzle:push` — confirm `analytics_events` table created
2. Insert a test event via the service
3. Query it back: `SELECT * FROM analytics_events LIMIT 5`
4. Check RLS: sign in as a user and verify they only see their org's data
5. Query `analytics_daily_summary` view — confirm aggregation works
6. Check `pg_stat_statements` — confirm slow queries visible

---

## Anti-Patterns

- Do NOT write to `analytics_events` directly from client components — always via API route or Server Action
- Do NOT index every column — the three indexes on `organization_id`, `event_name`, and `created_at` cover 95% of queries
- Do NOT store PII in `properties` JSONB — use `user_id` (UUID) only
- Do NOT enable RLS insert policy for authenticated users — inserts must go through the service role API route
- Do NOT query `pg_stat_statements` in production application code — it's a DBA-level diagnostic tool only
- Do NOT skip the `environment` column filter in views — dev events will corrupt production metrics
