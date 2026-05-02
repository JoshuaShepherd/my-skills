---
name: analytics-dashboard
description: Build React analytics dashboard components — KPI metric cards, Recharts time series and bar charts, funnel views — wired to any data source via React Query hooks. UI-agnostic (works with shadcn/ui, MUI, or raw Tailwind).
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Build analytics dashboard components: $ARGUMENTS

$ARGUMENTS should include:
- `--ui <shadcn|tailwind|mui>` — UI library in use (default: shadcn)
- `--datasource <supabase|api|posthog>` — where data comes from (default: api)
- `--sections <kpi|charts|funnel|all>` — which components to build (default: all)

---

## Before Starting

1. Check `package.json` for `recharts` — install if missing: `pnpm add recharts`
2. Identify the component library in use (shadcn/ui, MUI, custom)
3. Read existing hook patterns to match the data-fetching style
4. Identify the route where the dashboard will live

---

## Core Components

```
components/analytics/
├── KpiCard.tsx              — single metric with trend indicator
├── KpiGrid.tsx              — 2–4 column responsive grid of KPI cards
├── EventTimeSeriesChart.tsx — area/line chart over time (Recharts)
├── TopContentChart.tsx      — horizontal bar chart for top content
├── UserFunnelChart.tsx      — vertical funnel visualization
├── PeriodSelector.tsx       — 7/30/90 day period selector
└── AnalyticsDashboard.tsx   — composes all panels
```

---

## Step 1 — Install Recharts

```bash
pnpm add recharts
```

All Recharts components require `'use client'` in Next.js App Router.

---

## Step 2 — React Query Hook

```typescript
// hooks/use-analytics.ts
import { useQuery } from '@tanstack/react-query'

async function fetchSummary(days: number) {
  const res = await fetch(`/api/analytics/summary?days=${days}`)
  if (!res.ok) throw new Error('Analytics fetch failed')
  return res.json()
}

async function fetchTimeSeries(days: number) {
  const res = await fetch(`/api/analytics/timeseries?days=${days}`)
  if (!res.ok) throw new Error('Time series fetch failed')
  return res.json()
}

export function useAnalyticsSummary(days = 30) {
  return useQuery({
    queryKey: ['analytics', 'summary', days],
    queryFn: () => fetchSummary(days),
    staleTime: 5 * 60 * 1000,
  })
}

export function useAnalyticsTimeSeries(days = 30) {
  return useQuery({
    queryKey: ['analytics', 'timeseries', days],
    queryFn: () => fetchTimeSeries(days),
    staleTime: 5 * 60 * 1000,
  })
}
```

---

## Step 3 — KPI Card

```tsx
// Adapt Card/Skeleton to your UI library

interface KpiCardProps {
  title: string
  value: string | number
  subtitle?: string
  trend?: number    // percent vs previous period
  loading?: boolean
}

export function KpiCard({ title, value, subtitle, trend, loading }: KpiCardProps) {
  if (loading) return <KpiCardSkeleton />

  const trendColor = !trend ? '' : trend > 0 ? 'text-green-600' : 'text-red-600'
  const TrendIcon = !trend ? null : trend > 0 ? '↑' : '↓'

  return (
    <div className="rounded-lg border bg-card p-6">
      <p className="text-sm font-medium text-muted-foreground">{title}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
      {(subtitle || trend !== undefined) && (
        <p className={`mt-1 text-xs ${trendColor || 'text-muted-foreground'}`}>
          {TrendIcon} {trend !== undefined ? `${Math.abs(trend)}% vs last period` : subtitle}
        </p>
      )}
    </div>
  )
}
```

---

## Step 4 — Time Series Chart (Recharts)

```tsx
'use client'

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface DataPoint {
  date: string
  count: number
  uniqueUsers?: number
}

export function EventTimeSeriesChart({ data, loading }: { data?: DataPoint[]; loading?: boolean }) {
  if (loading) return <div className="h-48 animate-pulse rounded bg-muted" />

  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 11 }}
          tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
        />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="count"
          stroke="hsl(var(--primary))"
          strokeWidth={2}
          fill="url(#grad)"
          name="Events"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
```

---

## Step 5 — Dashboard Composition

```tsx
'use client'

import { useState } from 'react'
import { KpiCard } from './KpiCard'
import { EventTimeSeriesChart } from './EventTimeSeriesChart'
import { useAnalyticsSummary, useAnalyticsTimeSeries } from '@/hooks/use-analytics'

export function AnalyticsDashboard() {
  const [days, setDays] = useState(30)
  const { data: summary, isLoading: summaryLoading } = useAnalyticsSummary(days)
  const { data: timeSeries, isLoading: tsLoading } = useAnalyticsTimeSeries(days)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Analytics</h2>
        <select value={days} onChange={(e) => setDays(Number(e.target.value))} className="border rounded px-2 py-1 text-sm">
          <option value={7}>Last 7 days</option>
          <option value={30}>Last 30 days</option>
          <option value={90}>Last 90 days</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <KpiCard title="Events" value={summary?.totalEvents?.toLocaleString() ?? '—'} loading={summaryLoading} />
        <KpiCard title="Unique Users" value={summary?.uniqueUsers?.toLocaleString() ?? '—'} loading={summaryLoading} />
        <KpiCard title="Course Starts" value={summary?.courseStarts?.toLocaleString() ?? '—'} loading={summaryLoading} />
        <KpiCard title="Completion Rate" value={summary ? `${summary.completionRate}%` : '—'} loading={summaryLoading} />
      </div>

      <div className="rounded-lg border p-6">
        <h3 className="mb-4 text-base font-medium">Activity Over Time</h3>
        <EventTimeSeriesChart data={timeSeries} loading={tsLoading} />
      </div>
    </div>
  )
}
```

---

## Chart Color Rules

Always use CSS variables — never hardcoded hex:
- Lines/fills: `hsl(var(--primary))`
- Grid lines: `hsl(var(--border))`
- Secondary series: `hsl(var(--muted-foreground))`
- Tooltip background: `hsl(var(--card))`

---

## Anti-Patterns

- Do NOT hardcode colors in Recharts — use CSS variables for dark mode support
- Do NOT skip `ResponsiveContainer` — fixed-width charts break on mobile
- Do NOT render Recharts in Server Components — requires `'use client'`
- Do NOT fetch analytics data directly in components — always through hooks
- Do NOT show analytics to non-admin users — gate at the page/route level
