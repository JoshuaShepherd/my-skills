---
name: ga4-setup
description: Set up Google Analytics 4 for this Next.js 15 multi-tenant platform — org-wide property, per-tenant custom dimensions, typed event utilities, server-side Measurement Protocol, and GA4 Admin API for programmatic tenant provisioning.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Google Analytics 4: $ARGUMENTS

$ARGUMENTS should include:
- `--mode <free|scale>` — free uses single property + custom dimensions; scale uses GA4 Admin API to create per-tenant sub-properties (default: free)
- `--dry-run` — preview without writing
- Empty — full setup, prompt for Measurement ID

---

## Before Starting

1. Read `src/app/layout.tsx` — understand root layout structure
2. Read `src/lib/env.ts` — understand env var validation patterns
3. Read `src/lib/tenant.ts` — understand `getTenantOrgId()`
4. Read `src/middleware.ts` — understand auth/routing context
5. Check `package.json` for existing analytics packages
6. Grep for `gtag\|G-` to find any existing GA4 wiring

---

## Architecture

### Free Tier (default) — Single Property + Custom Dimensions

```
GA4 Account (Movemental organization)
└── Property: "Movemental Platform" (G-XXXXXXXXXX)
    ├── Data Stream: Web (your domain)
    ├── Custom Dimensions:
    │   ├── tenant_id      (event-scoped)
    │   ├── org_id         (user-scoped)
    │   ├── user_role      (user-scoped)
    │   └── environment    (event-scoped)
    └── Looker Studio reports filtered per tenant_id
```

### Scale Tier — Per-Tenant Sub-Properties (GA4 360 or Admin API)

```
GA4 Account (Movemental organization)
├── Property: "Movemental Rollup" (all tenants)
└── Sub-Properties (one per tenant, created via Admin API)
    ├── tenant-a.com Property
    ├── tenant-b.com Property
    └── ...
```

---

## Step 1 — Human-Required (one-time, cannot be automated)

These steps require a human with Google account access:

1. **Create GA4 account** at analytics.google.com → Admin → Create Account
2. **Create property** → Name: "Movemental Platform" → Time zone → Currency
3. **Create web data stream** → Enter your domain → Copy Measurement ID (`G-XXXXXXXXXX`)
4. **Enable GA4 Admin API** in Google Cloud Console:
   - Go to console.cloud.google.com → APIs & Services → Enable APIs
   - Search "Google Analytics Admin API" → Enable
   - Create Service Account → download JSON key → extract `GA4_ADMIN_API_KEY`
5. **Create API secret** for Measurement Protocol:
   - GA4 → Admin → Data Streams → your stream → Measurement Protocol API Secrets → Create
   - Copy the secret value → set as `GA4_API_SECRET`

---

## Step 2 — Install Package

```bash
pnpm add server-only
```

No client package needed — gtag.js is loaded via Next.js Script component.

---

## Step 3 — Environment Variables

Add to `src/lib/env.ts` (in the server schema):

```typescript
// Add to the server env schema
GA4_MEASUREMENT_ID: z.string().startsWith('G-').optional(),
GA4_API_SECRET: z.string().optional(),
```

Add to `.env.local.example`:

```bash
# --- Google Analytics 4 ---
NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-XXXXXXXXXX  # public: loaded in browser
GA4_API_SECRET=                               # private: Measurement Protocol server events
```

---

## Step 4 — Load gtag.js in Root Layout

Edit `src/app/layout.tsx`:

```tsx
import Script from 'next/script'

const GA_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        {/* GA4 — only load when ID is set (graceful no-op in dev without it) */}
        {GA_ID && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
              strategy="afterInteractive"
            />
            <Script id="ga4-init" strategy="afterInteractive">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${GA_ID}', {
                  anonymize_ip: true,
                  allow_google_signals: false,
                });
              `}
            </Script>
          </>
        )}
      </body>
    </html>
  )
}
```

Key decisions:
- `strategy="afterInteractive"` — doesn't block page render
- `anonymize_ip: true` — GDPR compliance baseline
- `allow_google_signals: false` — opt out of cross-site tracking

---

## Step 5 — Typed Event Utility

Create `src/lib/analytics/ga4.ts`:

```typescript
'use client'

import { getTenantOrgId } from '@/lib/tenant'

type EventName =
  | 'page_view'
  | 'sign_up'
  | 'sign_in'
  | 'course_started'
  | 'course_completed'
  | 'resource_viewed'
  | 'assessment_taken'
  | 'upgrade_clicked'
  | 'checkout_started'
  | 'purchase_completed'

interface EventParams {
  tenant_id?: string
  org_id?: string
  user_role?: string
  content_id?: string
  content_type?: string
  value?: number
  currency?: string
  [key: string]: string | number | boolean | undefined
}

declare global {
  interface Window {
    gtag: (...args: unknown[]) => void
  }
}

/**
 * Fire a typed GA4 event. Automatically appends tenant_id and environment.
 * Safe to call server-side (no-ops if window is undefined).
 */
export function trackEvent(name: EventName, params: EventParams = {}) {
  if (typeof window === 'undefined') return
  if (!window.gtag) return
  if (!process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID) return

  window.gtag('event', name, {
    tenant_id: getTenantOrgId(),
    environment: process.env.NODE_ENV,
    ...params,
  })
}

/**
 * Set user properties on the GA4 session.
 * Call after Supabase auth resolves.
 */
export function setGA4User(userId: string, orgId: string, role: string) {
  if (typeof window === 'undefined' || !window.gtag) return

  window.gtag('set', 'user_properties', {
    org_id: orgId,
    user_role: role,
  })

  // Use hashed user ID — never raw email or PII
  window.gtag('config', process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID!, {
    user_id: userId,
  })
}
```

---

## Step 6 — Wire User Identity After Auth

In your auth provider or session hook, call `setGA4User` once the session resolves:

```typescript
import { setGA4User } from '@/lib/analytics/ga4'

// After Supabase auth session loads:
useEffect(() => {
  if (session?.user) {
    setGA4User(
      session.user.id,           // Supabase UUID — safe to send
      session.user.user_metadata.org_id,
      session.user.user_metadata.role ?? 'member'
    )
  }
}, [session])
```

---

## Step 7 — Server-Side Measurement Protocol

Create `src/lib/analytics/ga4-server.ts`:

```typescript
import 'server-only'

const GA_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID
const API_SECRET = process.env.GA4_API_SECRET

interface ServerEvent {
  name: string
  params?: Record<string, string | number | boolean>
}

/**
 * Send server-side events via GA4 Measurement Protocol.
 * Use for Stripe webhooks, API-only events, or server actions.
 */
export async function sendServerEvent(
  clientId: string, // GA4 client_id from cookie: _ga=GA1.x.CLIENT_ID
  events: ServerEvent[]
): Promise<void> {
  if (!GA_ID || !API_SECRET) return

  await fetch(
    `https://www.google-analytics.com/mp/collect?measurement_id=${GA_ID}&api_secret=${API_SECRET}`,
    {
      method: 'POST',
      body: JSON.stringify({
        client_id: clientId,
        events: events.map(e => ({
          name: e.name,
          params: {
            tenant_id: process.env.TENANT_ORG_ID,
            environment: process.env.NODE_ENV,
            ...e.params,
          },
        })),
      }),
    }
  ).catch(() => {
    // Never let analytics failures surface to users
  })
}
```

Usage in a Stripe webhook route:

```typescript
// src/app/api/webhooks/stripe/route.ts
import { sendServerEvent } from '@/lib/analytics/ga4-server'

// In the checkout.session.completed handler:
await sendServerEvent(session.client_reference_id, [{
  name: 'purchase_completed',
  params: {
    value: session.amount_total / 100,
    currency: session.currency.toUpperCase(),
  }
}])
```

---

## Step 8 — GA4 Admin API: Programmatic Tenant Provisioning (Scale Mode)

Create `src/lib/analytics/ga4-admin.ts`:

```typescript
import 'server-only'

/**
 * Programmatically create a GA4 property for a new tenant.
 * Called when a new tenant organization is onboarded.
 *
 * Requires: GA4 Admin API enabled + service account JSON key
 *
 * Note: Sub-properties require GA4 360 (paid). For free tier,
 * use custom dimensions instead — this is for scale deployments.
 */
export async function provisionTenantGA4Property(tenantId: string, displayName: string) {
  const apiKey = process.env.GA4_ADMIN_API_KEY
  if (!apiKey) throw new Error('GA4_ADMIN_API_KEY not set')

  // GA4 Admin API v1beta
  const response = await fetch(
    'https://analyticsadmin.googleapis.com/v1beta/properties',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        displayName: `${displayName} Analytics`,
        timeZone: 'America/New_York',
        currencyCode: 'USD',
        industryCategory: 'EDUCATION',
        // Link to parent account
        parent: `accounts/${process.env.GA4_ACCOUNT_ID}`,
      }),
    }
  )

  if (!response.ok) {
    throw new Error(`GA4 Admin API error: ${response.statusText}`)
  }

  const property = await response.json()

  // Create a web data stream for this tenant
  await fetch(
    `https://analyticsadmin.googleapis.com/v1beta/${property.name}/dataStreams`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'WEB_DATA_STREAM',
        webStreamData: {
          defaultUri: `https://${tenantId}.yourdomain.com`,
        },
        displayName: `${displayName} Web`,
      }),
    }
  )

  return property
}

/**
 * Grant a tenant admin read access to their GA4 property.
 */
export async function grantTenantGA4Access(propertyId: string, email: string) {
  const apiKey = process.env.GA4_ADMIN_API_KEY
  if (!apiKey) return

  await fetch(
    `https://analyticsadmin.googleapis.com/v1beta/properties/${propertyId}/accessBindings`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user: email,
        roles: ['predefinedRoles/viewer'], // viewer only — they can't edit
      }),
    }
  )
}
```

---

## Step 9 — Custom Dimensions (Free Tier)

Set these up manually in GA4 Admin → Custom Definitions → Create:

| Name        | Scope  | Description                              |
|-------------|--------|------------------------------------------|
| tenant_id   | Event  | Deployment identifier (TENANT_ORG_ID)    |
| org_id      | User   | Supabase organization UUID               |
| user_role   | User   | member, admin, super_admin               |
| environment | Event  | production, preview, development         |
| content_id  | Event  | Course/pathway/article UUID              |
| content_type| Event  | course, pathway, article, resource       |

---

## Step 10 — Verify

1. Open browser DevTools → Network → filter `collect`
2. Navigate a page — confirm `collect` requests fire with your Measurement ID
3. In GA4 → Reports → Realtime — confirm your session appears
4. Fire a custom event: `trackEvent('sign_in')` — verify it appears in Realtime
5. Check `tenant_id` custom dimension is populated in event params

---

## Anti-Patterns

- Do NOT send email addresses, names, or any PII — GA4 will reject them and you'll violate GDPR
- Do NOT call `trackEvent` in Server Components — it's client-only
- Do NOT load the gtag script unconditionally — gate on `GA_ID` being set
- Do NOT use `strategy="beforeInteractive"` — gtag doesn't need to block rendering
- Do NOT send `user_id` as an email — use the Supabase UUID only
- Do NOT skip `anonymize_ip: true` — required for GDPR baseline compliance
