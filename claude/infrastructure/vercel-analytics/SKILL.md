---
name: vercel-analytics
description: Set up Vercel Analytics (page views, custom events) and Speed Insights (Core Web Vitals) for this Next.js 15 project. Zero-config on Vercel deployments — no API key needed for basic tracking.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Set up Vercel Analytics and Speed Insights: $ARGUMENTS

$ARGUMENTS should include:
- `--events` — also scaffold a typed custom event utility
- `--dry-run` — preview without writing
- Empty — full setup

---

## What This Gives You (Free Tier)

| Feature              | Free Tier              | Pro Tier           |
|----------------------|------------------------|--------------------|
| Page views           | 2,500/month            | 100,000/month      |
| Custom events        | 2,500/month            | 100,000/month      |
| Retention            | 30 days                | 90 days            |
| Speed Insights       | Unlimited              | Unlimited          |
| Core Web Vitals      | Yes (LCP, FID, CLS)    | Yes                |
| Breakdown by route   | Yes                    | Yes                |

Speed Insights is entirely free and unlimited — always enable it.

---

## Before Starting

1. Read `src/app/layout.tsx` — understand root layout
2. Check `package.json` for `@vercel/analytics` or `@vercel/speed-insights`
3. Confirm deployment target is Vercel (check `vercel.json` or `.vercel/`)

---

## Step 1 — Install

```bash
pnpm add @vercel/analytics @vercel/speed-insights
```

---

## Step 2 — Wire into Root Layout

Edit `src/app/layout.tsx`:

```tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        {/* Vercel Analytics — page views + custom events */}
        <Analytics />
        {/* Speed Insights — Core Web Vitals (LCP, FID, CLS, TTFB, INP) */}
        <SpeedInsights />
      </body>
    </html>
  )
}
```

Both components:
- Auto-disable in local dev (no data sent unless `VERCEL_ENV` is set)
- Require zero configuration — Vercel injects the project ID at build time
- Are Server Component safe — they render as lightweight script tags

---

## Step 3 — Custom Events (Optional, with --events flag)

Create `src/lib/analytics/vercel-events.ts`:

```typescript
import { track } from '@vercel/analytics'

/**
 * Typed Vercel Analytics custom events.
 *
 * Counts toward the 2,500/month free tier limit.
 * Use sparingly — reserve for high-value conversion events.
 * Use PostHog for rich product analytics.
 */
export const va = {
  upgradeClicked: (source: string) =>
    track('Upgrade Clicked', { source }),

  checkoutStarted: (plan: string) =>
    track('Checkout Started', { plan }),

  courseEnrolled: (courseSlug: string) =>
    track('Course Enrolled', { course: courseSlug }),

  signUp: (method: 'email' | 'google' | 'github') =>
    track('Sign Up', { method }),
}
```

Usage in a component:

```tsx
import { va } from '@/lib/analytics/vercel-events'

<Button onClick={() => va.upgradeClicked('pricing-page')}>
  Upgrade Now
</Button>
```

---

## Step 4 — Enable in Vercel Dashboard

Vercel Analytics requires explicit activation:
1. Go to vercel.com → your project → Analytics tab
2. Click "Enable" — this activates data collection
3. No environment variables needed — Vercel injects the token at build time

Speed Insights activates automatically when `@vercel/speed-insights` is installed.

---

## Step 5 — Verify

**Page views:**
1. Deploy to Vercel (or run `vercel dev` locally with env vars)
2. Navigate your site → check Vercel Dashboard → Analytics → Page Views
3. Should appear within ~30 seconds

**Speed Insights:**
1. Open Chrome DevTools → Performance tab
2. Run a Lighthouse audit — or just navigate normally
3. Check Vercel Dashboard → Speed Insights → Core Web Vitals
4. LCP, FID/INP, CLS scores appear per route

**Custom events:**
1. Trigger a tracked action (e.g., upgrade button click)
2. Check Vercel Dashboard → Analytics → Events

---

## Routing Breakdown

Vercel Analytics automatically tracks by Next.js route:
- `/` — home
- `/courses/[slug]` — individual course (grouped by pattern)
- `/api/*` — API routes (excluded by default)

This lets you see which pages have the most views and best/worst web vitals.

---

## Anti-Patterns

- Do NOT use Vercel Analytics as your primary product analytics tool — it lacks funnels, cohorts, and session data; use PostHog for that
- Do NOT track high-frequency events (scroll depth, hover, keypress) — you'll exhaust the free tier instantly
- Do NOT add `mode="production"` override without understanding it will send data from local dev
- Do NOT rely solely on Vercel Analytics for conversion tracking — GA4 has better attribution
- Do NOT skip Speed Insights — it's free, unlimited, and directly tied to your Vercel deployment performance score
