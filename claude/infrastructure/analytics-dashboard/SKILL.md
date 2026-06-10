---
name: analytics-dashboard
description: Build React analytics dashboard components for this platform — KPI metric cards, time series charts (Recharts), funnel views, and per-tenant data scoping. Uses shadcn/ui + Recharts, wired to React Query hooks over the analytics_events Supabase table.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Build analytics dashboard components: $ARGUMENTS

$ARGUMENTS should include:
- `--section <kpi|charts|funnel|all>` — which components to build (default: all)
- `--route <path>` — where to place the dashboard page (default: /account/analytics)
- `--dry-run` — preview structure without writing

---

## Before Starting

1. Check `package.json` for `recharts` — install if missing: `pnpm add recharts`
2. Read `src/hooks/simplified/` — understand existing React Query hook patterns
3. Read `src/lib/services/custom/analytics.service.ts` — understand data shape
4. Read `src/components/ui/` — confirm available shadcn components
5. Read `src/lib/config/tenant.config.ts` — check for analytics feature flags

---

## Architecture

```
src/
├── app/(public)/account/analytics/
│   └── page.tsx                    ← dashboard page (Server Component)
├── components/analytics/
│   ├── KpiCard.tsx                 ← single metric card
│   ├── KpiGrid.tsx                 ← 2x2 grid of KPI cards
│   ├── EventTimeSeriesChart.tsx    ← line/area chart over time
│   ├── TopContentChart.tsx         ← bar chart — most viewed content
│   ├── UserFunnelChart.tsx         ← funnel: visit → enroll → complete
│   ├── AnalyticsDashboard.tsx      ← composes all panels
│   └── index.ts
└── hooks/custom/
    └── use-analytics.ts            ← React Query hooks for analytics data
```

---

## Step 1 — Install Recharts

```bash
pnpm add recharts
```

---

## Step 2 — Analytics React Query Hook

Create `src/hooks/custom/use-analytics.ts`:

```typescript
'use client'

import { useQuery } from '@tanstack/react-query'

interface AnalyticsSummary {
  totalEvents: number
  uniqueUsers: number
  uniqueSessions: number
  courseStarts: number
  courseCompletions: number
  completionRate: number
}

interface DailyEventCount {
  date: string
  count: number
  uniqueUsers: number
}

interface TopContent {
  contentId: string
  contentType: string
  views: number
}

async function fetchAnalyticsSummary(days: number): Promise<AnalyticsSummary> {
  const res = await fetch(`/api/custom/analytics/summary?days=${days}`)
  if (!res.ok) throw new Error('Failed to fetch analytics summary')
  return res.json()
}

async function fetchDailyEvents(days: number): Promise<DailyEventCount[]> {
  const res = await fetch(`/api/custom/analytics/daily?days=${days}`)
  if (!res.ok) throw new Error('Failed to fetch daily events')
  return res.json()
}

async function fetchTopContent(days: number): Promise<TopContent[]> {
  const res = await fetch(`/api/custom/analytics/top-content?days=${days}`)
  if (!res.ok) throw new Error('Failed to fetch top content')
  return res.json()
}

export function useAnalyticsSummary(days = 30) {
  return useQuery({
    queryKey: ['analytics', 'summary', days],
    queryFn: () => fetchAnalyticsSummary(days),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useDailyEvents(days = 30) {
  return useQuery({
    queryKey: ['analytics', 'daily', days],
    queryFn: () => fetchDailyEvents(days),
    staleTime: 5 * 60 * 1000,
  })
}

export function useTopContent(days = 30) {
  return useQuery({
    queryKey: ['analytics', 'top-content', days],
    queryFn: () => fetchTopContent(days),
    staleTime: 5 * 60 * 1000,
  })
}
```

---

## Step 3 — KPI Card Component

Create `src/components/analytics/KpiCard.tsx`:

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface KpiCardProps {
  title: string
  value: string | number
  subtitle?: string
  trend?: number     // percent change vs previous period
  loading?: boolean
}

export function KpiCard({ title, value, subtitle, trend, loading }: KpiCardProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader className="pb-2">
          <Skeleton className="h-4 w-24" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-16 mb-1" />
          <Skeleton className="h-3 w-32" />
        </CardContent>
      </Card>
    )
  }

  const TrendIcon = trend === undefined || trend === 0
    ? Minus
    : trend > 0 ? TrendingUp : TrendingDown

  const trendColor = trend === undefined || trend === 0
    ? 'text-muted-foreground'
    : trend > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {(subtitle || trend !== undefined) && (
          <div className={`flex items-center gap-1 text-xs mt-1 ${trendColor}`}>
            {trend !== undefined && <TrendIcon className="h-3 w-3" />}
            {trend !== undefined && (
              <span>{Math.abs(trend)}% vs last period</span>
            )}
            {subtitle && !trend && (
              <span className="text-muted-foreground">{subtitle}</span>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

---

## Step 4 — KPI Grid

Create `src/components/analytics/KpiGrid.tsx`:

```tsx
'use client'

import { KpiCard } from './KpiCard'
import { useAnalyticsSummary } from '@/hooks/custom/use-analytics'

interface KpiGridProps {
  days?: number
}

export function KpiGrid({ days = 30 }: KpiGridProps) {
  const { data, isLoading } = useAnalyticsSummary(days)

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
      <KpiCard
        title="Total Events"
        value={data?.totalEvents.toLocaleString() ?? '—'}
        loading={isLoading}
      />
      <KpiCard
        title="Unique Users"
        value={data?.uniqueUsers.toLocaleString() ?? '—'}
        loading={isLoading}
      />
      <KpiCard
        title="Course Starts"
        value={data?.courseStarts.toLocaleString() ?? '—'}
        loading={isLoading}
      />
      <KpiCard
        title="Completion Rate"
        value={data ? `${data.completionRate}%` : '—'}
        subtitle={`${data?.courseCompletions ?? 0} completions`}
        loading={isLoading}
      />
    </div>
  )
}
```

---

## Step 5 — Time Series Chart

Create `src/components/analytics/EventTimeSeriesChart.tsx`:

```tsx
'use client'

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { useDailyEvents } from '@/hooks/custom/use-analytics'

interface EventTimeSeriesChartProps {
  days?: number
}

export function EventTimeSeriesChart({ days = 30 }: EventTimeSeriesChartProps) {
  const { data, isLoading } = useDailyEvents(days)

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Activity Over Time</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <Skeleton className="h-48 w-full" />
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={data}>
              <defs>
                <linearGradient id="eventGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
                tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }} />
              <Tooltip
                contentStyle={{
                  background: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '6px',
                }}
              />
              <Area
                type="monotone"
                dataKey="count"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                fill="url(#eventGradient)"
                name="Events"
              />
              <Area
                type="monotone"
                dataKey="uniqueUsers"
                stroke="hsl(var(--muted-foreground))"
                strokeWidth={1.5}
                fill="none"
                strokeDasharray="4 2"
                name="Unique Users"
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  )
}
```

---

## Step 6 — Dashboard Composition

Create `src/components/analytics/AnalyticsDashboard.tsx`:

```tsx
'use client'

import { useState } from 'react'
import { KpiGrid } from './KpiGrid'
import { EventTimeSeriesChart } from './EventTimeSeriesChart'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

export function AnalyticsDashboard() {
  const [days, setDays] = useState(30)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Analytics</h2>
        <Select value={String(days)} onValueChange={(v) => setDays(Number(v))}>
          <SelectTrigger className="w-36">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="7">Last 7 days</SelectItem>
            <SelectItem value="30">Last 30 days</SelectItem>
            <SelectItem value="90">Last 90 days</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <KpiGrid days={days} />
      <EventTimeSeriesChart days={days} />
    </div>
  )
}
```

---

## Step 7 — Dashboard Page

Create `src/app/(public)/account/analytics/page.tsx`:

```tsx
import { AnalyticsDashboard } from '@/components/analytics/AnalyticsDashboard'
import { createSupabaseServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function AnalyticsPage() {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/sign-in')

  // TODO: check user is admin before showing analytics
  const isAdmin = user.user_metadata?.role === 'admin'
  if (!isAdmin) redirect('/account')

  return (
    <main className="container py-8">
      <AnalyticsDashboard />
    </main>
  )
}
```

---

## Design Rules

- Use `hsl(var(--primary))` and `hsl(var(--muted-foreground))` for chart colors — never hardcoded hex
- Use `hsl(var(--border))` for grid lines and dividers
- Use `hsl(var(--card))` for tooltip backgrounds
- All charts must be responsive via `ResponsiveContainer`
- Loading states must use `<Skeleton>` — never show empty charts
- Numbers over 1,000 must use `.toLocaleString()` for comma formatting

---

## Anti-Patterns

- Do NOT call analytics APIs directly from UI components — always via hooks
- Do NOT render Recharts in Server Components — all chart components must be `'use client'`
- Do NOT hardcode colors in chart components — use CSS variables via `hsl(var(--*))`
- Do NOT skip `ResponsiveContainer` — fixed-width charts break on mobile
- Do NOT show analytics to non-admin users — gate in page.tsx before rendering
