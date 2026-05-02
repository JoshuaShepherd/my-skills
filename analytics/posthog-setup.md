---
name: posthog-setup
description: Set up PostHog product analytics for any React app — person identification, group analytics (org + tenant), session replay, feature flags, funnels, and server-side event capture via posthog-node.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up PostHog product analytics: $ARGUMENTS

$ARGUMENTS should include:
- `--host <url>` — PostHog Cloud (default: https://app.posthog.com) or self-hosted URL
- `--framework <nextjs|vite|remix>` — affects provider injection pattern (default: nextjs)
- `--replay` — enable session replay (default: on with 10% sample rate)
- `--dry-run` — preview without writing

---

## GA4 vs PostHog — When to Use Each

| Scenario                      | Use            |
|-------------------------------|----------------|
| Traffic sources, attribution  | GA4            |
| User funnels and drop-offs    | PostHog        |
| Session replay                | PostHog        |
| Feature flags / A/B tests     | PostHog        |
| Retention and cohorts         | PostHog        |
| Conversion goal tracking      | GA4 + PostHog  |

---

## Step 1 — Install

```bash
pnpm add posthog-js posthog-node
```

---

## Step 2 — Environment Variables

```bash
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

For Vite, use `VITE_` prefix instead of `NEXT_PUBLIC_`.

---

## Step 3 — Client Provider

### Next.js App Router

Create `src/lib/analytics/posthog-provider.tsx`:

```tsx
'use client'

import posthog from 'posthog-js'
import { PostHogProvider as PHProvider } from 'posthog-js/react'
import { useEffect } from 'react'

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY
    if (!key) return

    posthog.init(key, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? 'https://app.posthog.com',
      person_profiles: 'identified_only',  // no anonymous profiles
      capture_pageview: false,             // handle manually for SPA routing
      capture_pageleave: true,
      session_recording: {
        maskAllInputs: true,               // mask passwords and sensitive fields
      },
      loaded: (ph) => {
        if (process.env.NODE_ENV !== 'production') {
          ph.opt_out_capturing()           // don't pollute prod data in dev
        }
      },
    })
  }, [])

  return <PHProvider client={posthog}>{children}</PHProvider>
}
```

Add to root layout:
```tsx
import { PostHogProvider } from '@/lib/analytics/posthog-provider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <PostHogProvider>{children}</PostHogProvider>
      </body>
    </html>
  )
}
```

### Vite / React Router

In `src/main.tsx`:
```tsx
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'

const key = import.meta.env.VITE_POSTHOG_KEY
if (key && import.meta.env.MODE === 'production') {
  posthog.init(key, {
    api_host: import.meta.env.VITE_POSTHOG_HOST ?? 'https://app.posthog.com',
    person_profiles: 'identified_only',
    session_recording: { maskAllInputs: true },
  })
}

root.render(
  <PostHogProvider client={posthog}>
    <App />
  </PostHogProvider>
)
```

---

## Step 4 — Page View Tracking (Next.js App Router)

Create `src/lib/analytics/posthog-page-view.tsx`:

```tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'
import { usePostHog } from 'posthog-js/react'
import { useEffect } from 'react'

export function PostHogPageView() {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const posthog = usePostHog()

  useEffect(() => {
    if (!pathname || !posthog) return
    let url = window.origin + pathname
    if (searchParams.toString()) url += `?${searchParams.toString()}`
    posthog.capture('$pageview', { $current_url: url })
  }, [pathname, searchParams, posthog])

  return null
}
```

Add inside `<Suspense fallback={null}>` in root layout.

---

## Step 5 — Person Identification

Call after auth resolves:

```typescript
import { usePostHog } from 'posthog-js/react'

// In an auth effect:
const posthog = usePostHog()

if (userId) {
  posthog.identify(userId, {           // userId = UUID, never email
    org_id: orgId,
    user_role: role,
    tenant_id: tenantId,
    // email: optional — PostHog handles it specially
  })

  // Group analytics — tie events to organization
  posthog.group('organization', orgId)
  posthog.group('tenant', tenantId)
} else {
  posthog.reset()                      // CRITICAL: call on logout
}
```

---

## Step 6 — Typed Event Utility

```typescript
import posthog from 'posthog-js'

type ProductEvent =
  | 'course_started' | 'course_completed'
  | 'upgrade_clicked' | 'purchase_completed'
  | 'feature_used' | string

export function captureEvent(event: ProductEvent, props: Record<string, unknown> = {}) {
  if (typeof window === 'undefined') return
  posthog.capture(event, {
    environment: process.env.NODE_ENV,
    ...props,
  })
}
```

---

## Step 7 — Server-Side Events (posthog-node)

```typescript
import { PostHog } from 'posthog-node'

let _client: PostHog | null = null

function getClient() {
  const key = process.env.POSTHOG_KEY ?? process.env.NEXT_PUBLIC_POSTHOG_KEY
  if (!key) return null
  if (!_client) _client = new PostHog(key, { host: process.env.POSTHOG_HOST, flushAt: 1, flushInterval: 0 })
  return _client
}

export async function captureServerEvent(distinctId: string, event: string, props = {}) {
  const client = getClient()
  if (!client) return
  client.capture({ distinctId, event, properties: { environment: process.env.NODE_ENV, ...props } })
  await client.flush()  // REQUIRED in serverless — events dropped without this
}
```

---

## Step 8 — Feature Flags

```tsx
import { useFeatureFlagEnabled } from 'posthog-js/react'

function MyFeature() {
  const isEnabled = useFeatureFlagEnabled('my-feature')
  if (!isEnabled) return null
  return <div>New feature content</div>
}
```

Create flags in PostHog → Feature Flags → Create. Roll out by `tenant_id`, `user_role`, or percentage.

---

## Anti-Patterns

- Do NOT identify anonymous users — use `person_profiles: 'identified_only'`
- Do NOT skip `posthog.reset()` on logout — previous user bleeds into next session
- Do NOT track in dev without opt-out — pollutes production data
- Do NOT skip `await client.flush()` in serverless — events silently dropped
- Do NOT store sensitive data in event properties — team members can see PostHog data
