---
name: posthog-setup
description: Set up PostHog product analytics for this Next.js 15 + Supabase multi-tenant platform — person identification, group analytics (org + tenant), session replay, feature flags, funnels, and server-side event capture.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up PostHog product analytics: $ARGUMENTS

$ARGUMENTS should include:
- `--host <url>` — PostHog Cloud (default: https://app.posthog.com) or self-hosted URL
- `--replay` — enable session replay (default: enabled with 10% sample rate)
- `--flags` — enable feature flags (default: enabled)
- `--dry-run` — preview without writing

---

## Why PostHog Alongside GA4

GA4 = marketing analytics (traffic sources, conversions, attribution)
PostHog = product analytics (user behavior, feature adoption, funnels, retention)

They are complementary. PostHog excels at:
- Funnels (where do users drop off in the course enrollment flow?)
- Session replay (watch what a user actually did before churning)
- Feature flags (roll out AI Lab to 10% of users)
- Retention cohorts (which users come back week over week?)
- Product-specific events with rich metadata

---

## Before Starting

1. Read `src/app/layout.tsx` — understand root layout and existing providers
2. Read `src/lib/env.ts` — understand env var validation
3. Read `src/lib/tenant.ts` — understand `getTenantOrgId()`
4. Read `src/lib/supabase/` — understand auth session structure
5. Grep for `posthog` to check if already partially installed

---

## Step 1 — Install

```bash
pnpm add posthog-js posthog-node
```

- `posthog-js` — browser SDK
- `posthog-node` — server-side event capture (API routes, Server Actions)

---

## Step 2 — Environment Variables

Add to `src/lib/env.ts`:

```typescript
// In the public (client-side) schema:
NEXT_PUBLIC_POSTHOG_KEY: z.string().startsWith('phc_').optional(),
NEXT_PUBLIC_POSTHOG_HOST: z.string().url().default('https://app.posthog.com'),
```

Add to `.env.local.example`:

```bash
# --- PostHog ---
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
# POSTHOG_PERSONAL_API_KEY=   # Only needed for Admin API (creating projects, etc.)
```

---

## Step 3 — PostHog Provider (Client)

Create `src/lib/analytics/posthog-provider.tsx`:

```tsx
'use client'

import posthog from 'posthog-js'
import { PostHogProvider as PHProvider } from 'posthog-js/react'
import { useEffect } from 'react'

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY
    const host = process.env.NEXT_PUBLIC_POSTHOG_HOST

    if (!key) return // graceful no-op without key

    posthog.init(key, {
      api_host: host,
      person_profiles: 'identified_only', // don't create anonymous profiles
      capture_pageview: false,             // manual in Next.js (route changes)
      capture_pageleave: true,
      session_recording: {
        maskAllInputs: true,               // mask sensitive input values
        maskInputFn: (text, element) => {
          if (element?.type === 'password') return '***'
          return text
        },
      },
      loaded: (ph) => {
        if (process.env.NODE_ENV === 'development') {
          ph.debug()
          ph.opt_out_capturing() // don't track dev sessions in prod PostHog
        }
      },
    })
  }, [])

  return <PHProvider client={posthog}>{children}</PHProvider>
}
```

---

## Step 4 — Wire Provider in Root Layout

Edit `src/app/layout.tsx`:

```tsx
import { PostHogProvider } from '@/lib/analytics/posthog-provider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <PostHogProvider>
          {children}
        </PostHogProvider>
      </body>
    </html>
  )
}
```

---

## Step 5 — Page View Tracking (Next.js App Router)

Next.js App Router doesn't emit page view events on route changes automatically.
Create `src/lib/analytics/posthog-page-view.tsx`:

```tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'
import { usePostHog } from 'posthog-js/react'
import { useEffect } from 'react'

/**
 * Tracks page views on route changes in Next.js App Router.
 * Add to root layout inside a Suspense boundary.
 */
export function PostHogPageView() {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const posthog = usePostHog()

  useEffect(() => {
    if (!pathname || !posthog) return

    let url = window.origin + pathname
    if (searchParams.toString()) {
      url += `?${searchParams.toString()}`
    }

    posthog.capture('$pageview', { $current_url: url })
  }, [pathname, searchParams, posthog])

  return null
}
```

Add to `src/app/layout.tsx`:

```tsx
import { Suspense } from 'react'
import { PostHogPageView } from '@/lib/analytics/posthog-page-view'

// Inside PostHogProvider:
<PostHogProvider>
  <Suspense fallback={null}>
    <PostHogPageView />
  </Suspense>
  {children}
</PostHogProvider>
```

---

## Step 6 — Person Identification (Tie Events to Users)

Create `src/lib/analytics/posthog-identify.tsx`:

```tsx
'use client'

import { usePostHog } from 'posthog-js/react'
import { useEffect } from 'react'
import { getTenantOrgId } from '@/lib/tenant'

interface PostHogIdentifyProps {
  userId: string | null
  orgId: string | null
  role: string | null
  email?: string | null  // optional — PostHog can store email for internal use
}

/**
 * Identifies the current user in PostHog.
 * Mount this in authenticated layouts only.
 */
export function PostHogIdentify({ userId, orgId, role, email }: PostHogIdentifyProps) {
  const posthog = usePostHog()

  useEffect(() => {
    if (!posthog) return

    if (userId) {
      posthog.identify(userId, {
        // Person properties — shown in PostHog UI
        org_id: orgId,
        user_role: role,
        tenant_id: getTenantOrgId(),
        // email is optional — PostHog handles it specially for person display
        ...(email && { email }),
      })

      // Group analytics — tie events to org and tenant
      if (orgId) {
        posthog.group('organization', orgId, {
          name: orgId, // update with real org name if available
          tenant_id: getTenantOrgId(),
        })
      }

      posthog.group('tenant', getTenantOrgId())

    } else {
      // User logged out — reset identity
      posthog.reset()
    }
  }, [userId, orgId, role, posthog])

  return null
}
```

Mount in authenticated layout (e.g., `src/app/(auth)/layout.tsx`):

```tsx
import { PostHogIdentify } from '@/lib/analytics/posthog-identify'
import { createSupabaseServerClient } from '@/lib/supabase/server'

export default async function AuthLayout({ children }) {
  const supabase = createSupabaseServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <>
      <PostHogIdentify
        userId={user?.id ?? null}
        orgId={user?.user_metadata?.org_id ?? null}
        role={user?.user_metadata?.role ?? null}
        email={user?.email ?? null}
      />
      {children}
    </>
  )
}
```

---

## Step 7 — Typed Event Utility

Create `src/lib/analytics/posthog-events.ts`:

```typescript
'use client'

import posthog from 'posthog-js'
import { getTenantOrgId } from '@/lib/tenant'

type ProductEvent =
  | 'course_started'
  | 'course_completed'
  | 'module_viewed'
  | 'resource_viewed'
  | 'assessment_taken'
  | 'upgrade_clicked'
  | 'checkout_started'
  | 'purchase_completed'
  | 'ai_lab_opened'
  | 'ai_chat_sent'
  | 'pathway_viewed'
  | 'framework_viewed'

interface EventProps {
  content_id?: string
  content_type?: string
  content_name?: string
  week_number?: number
  value?: number
  currency?: string
  [key: string]: string | number | boolean | undefined
}

/**
 * Fire a typed PostHog event with automatic tenant context.
 */
export function captureEvent(event: ProductEvent, props: EventProps = {}) {
  if (typeof window === 'undefined') return

  posthog.capture(event, {
    tenant_id: getTenantOrgId(),
    environment: process.env.NODE_ENV,
    ...props,
  })
}
```

---

## Step 8 — Server-Side Event Capture

Create `src/lib/analytics/posthog-server.ts`:

```typescript
import 'server-only'
import { PostHog } from 'posthog-node'

let _client: PostHog | null = null

function getPostHogClient(): PostHog | null {
  const key = process.env.NEXT_PUBLIC_POSTHOG_KEY
  const host = process.env.NEXT_PUBLIC_POSTHOG_HOST

  if (!key) return null

  if (!_client) {
    _client = new PostHog(key, {
      host,
      flushAt: 1,   // flush immediately in serverless
      flushInterval: 0,
    })
  }

  return _client
}

/**
 * Capture a server-side PostHog event.
 * Use in API routes, Server Actions, or webhooks.
 */
export async function captureServerEvent(
  distinctId: string,  // Supabase user UUID, or 'anonymous'
  event: string,
  properties: Record<string, unknown> = {}
) {
  const client = getPostHogClient()
  if (!client) return

  client.capture({
    distinctId,
    event,
    properties: {
      tenant_id: process.env.TENANT_ORG_ID,
      environment: process.env.NODE_ENV,
      $lib: 'posthog-node',
      ...properties,
    },
  })

  // In serverless, flush is critical — events are lost otherwise
  await client.flush()
}
```

Usage in a Stripe webhook:

```typescript
import { captureServerEvent } from '@/lib/analytics/posthog-server'

// In checkout.session.completed:
await captureServerEvent(session.client_reference_id, 'purchase_completed', {
  value: session.amount_total / 100,
  currency: session.currency,
})
```

---

## Step 9 — Feature Flags

Use PostHog feature flags to gate features per tenant/user.

```tsx
'use client'

import { useFeatureFlagEnabled } from 'posthog-js/react'

export function AILabSection() {
  const isEnabled = useFeatureFlagEnabled('ai-lab')

  if (!isEnabled) return null

  return <div>AI Lab content</div>
}
```

Create flags in PostHog dashboard → Feature Flags → Create:
- `ai-lab` — rolled out by `tenant_id` or `user_role`
- `new-course-player` — percentage rollout
- `pricing-v2` — A/B test

---

## Step 10 — Verify

1. Open PostHog dashboard → Live Events — confirm events appear
2. Navigate between pages — confirm `$pageview` fires
3. Sign in — confirm `identify` sets user properties
4. Trigger `captureEvent('course_started', { content_id: 'test' })` — verify in Live Events
5. Check group analytics — org and tenant groups appear

---

## Anti-Patterns

- Do NOT call `posthog.capture()` in Server Components — use `posthog-node` in server context
- Do NOT identify anonymous users — use `person_profiles: 'identified_only'`
- Do NOT skip `posthog.reset()` on logout — previous user data bleeds into next session
- Do NOT track events in development without `opt_out_capturing()` — pollutes production data
- Do NOT store sensitive data in event properties — PostHog data is accessible to team members
- Do NOT forget `await client.flush()` in serverless — events are silently dropped otherwise
- Do NOT wrap the PostHogProvider in a `use client` layout root — keep it as deep as possible
