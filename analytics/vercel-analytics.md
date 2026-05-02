---
name: vercel-analytics
description: Set up Vercel Analytics (page views, custom events) and Speed Insights (Core Web Vitals) for Next.js or Vite projects deployed to Vercel. Zero-config for page views — no API key needed. Always enable Speed Insights (free, unlimited).
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Set up Vercel Analytics and Speed Insights: $ARGUMENTS

---

## Free Tier Limits

| Feature              | Free             | Pro              |
|----------------------|------------------|------------------|
| Page views           | 2,500/month      | 100,000/month    |
| Custom events        | 2,500/month      | 100,000/month    |
| Speed Insights       | Unlimited        | Unlimited        |
| Data retention       | 30 days          | 90 days          |

**Always install Speed Insights** — it's free, unlimited, and gives you LCP, FID/INP, CLS, and TTFB per route.

---

## Step 1 — Install

```bash
pnpm add @vercel/analytics @vercel/speed-insights
```

---

## Step 2 — Wire to Framework

### Next.js App Router

Edit root layout:
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

### Vite / React

In `src/main.tsx` or root `App.tsx`:
```tsx
import { inject } from '@vercel/analytics'
import { injectSpeedInsights } from '@vercel/speed-insights'

inject()
injectSpeedInsights()
```

Or as React components:
```tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/react'

function App() {
  return (
    <>
      <Router />
      <Analytics />
      <SpeedInsights />
    </>
  )
}
```

---

## Step 3 — Activate in Vercel Dashboard

Packages alone don't activate data collection — you must enable it:

1. Go to vercel.com → your project → **Analytics** tab
2. Click **Enable** → select plan
3. Speed Insights activates automatically when the package is installed

No environment variables needed — Vercel injects the project token at build time.

---

## Step 4 — Custom Events (optional)

Use sparingly — counts toward the 2,500/month limit.

```typescript
import { track } from '@vercel/analytics'

// Track high-value conversion events only:
track('Upgrade Clicked', { source: 'pricing-page' })
track('Purchase Completed', { plan: 'pro', value: 49 })
track('Course Enrolled', { course: 'course-slug' })
```

Create a typed wrapper to avoid string typos:

```typescript
export const va = {
  upgradeClicked: (source: string) => track('Upgrade Clicked', { source }),
  purchaseCompleted: (plan: string, value: number) => track('Purchase Completed', { plan, value }),
  courseEnrolled: (slug: string) => track('Course Enrolled', { course: slug }),
}
```

---

## What You Get

- **Page views** by route pattern (e.g., `/courses/[slug]` grouped automatically)
- **Bounce rate** and **session duration**
- **Top pages** ranked by views
- **Core Web Vitals** (LCP, FID/INP, CLS, TTFB) per route
- **Custom event funnels** (limited)
- **Country breakdown** of visitors

---

## What This Doesn't Replace

Vercel Analytics is intentionally lightweight. For deeper analytics:
- **Funnels, cohorts, session replay** → use PostHog
- **Traffic source attribution** → use GA4
- **Per-user behavior** → use PostHog identify
- **Error monitoring** → use Sentry

---

## Anti-Patterns

- Do NOT use custom events for high-frequency interactions (scroll, hover) — you'll hit the limit instantly
- Do NOT expect cross-session user tracking — Vercel Analytics is cookieless and privacy-first by design
- Do NOT skip enabling in the Vercel Dashboard — installed packages without activation = no data
- Do NOT remove `<Analytics />` from SSR-heavy pages — it's lightweight and always needed
