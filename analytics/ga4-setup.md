---
name: ga4-setup
description: Set up Google Analytics 4 for any React/Next.js app — org-wide property, per-tenant custom dimensions, typed event utilities, Measurement Protocol for server-side events, and GA4 Admin API for programmatic tenant provisioning.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Google Analytics 4: $ARGUMENTS

$ARGUMENTS should include:
- `--mode <free|scale>` — free uses single property + custom dimensions; scale uses Admin API per-tenant sub-properties
- `--framework <nextjs|vite|remix>` — affects how gtag.js is loaded (default: nextjs)
- `--dry-run` — preview without writing

---

## Architecture Options

### Free Tier — Single Property + Custom Dimensions (recommended to start)

```
GA4 Account
└── Property: "Your App"  (G-XXXXXXXXXX)
    ├── Custom Dimensions: tenant_id, org_id, user_role, environment
    └── Looker Studio reports filtered per tenant_id
```

### Scale Tier — Per-Tenant Sub-Properties (GA4 Admin API)

```
GA4 Account
├── Property: "Rollup" (all data)
└── Sub-Properties (one per tenant, via Admin API)
    ├── Tenant A Property
    ├── Tenant B Property
    └── ...
```

---

## Step 1 — Human-Required (one-time)

Cannot be automated — requires Google account access:

1. Create GA4 account → analytics.google.com → Admin → Create Account
2. Create property → Get Measurement ID (`G-XXXXXXXXXX`)
3. Create web data stream → copy Measurement ID
4. **For Measurement Protocol (server events):** Admin → Data Streams → Measurement Protocol API Secrets → Create
5. **For Admin API (tenant provisioning):** Google Cloud Console → Enable "Google Analytics Admin API" → Create Service Account → download key

---

## Step 2 — Load gtag.js

### Next.js (App Router)

Edit root layout (`src/app/layout.tsx` or `app/layout.tsx`):

```tsx
import Script from 'next/script'

const GA_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
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

### Vite / React Router

In `index.html`:
```html
<!-- Injected conditionally at build time or via env check in main.tsx -->
```

In `src/main.tsx` or a `ga4.ts` module:
```typescript
const GA_ID = import.meta.env.VITE_GA4_MEASUREMENT_ID

if (GA_ID) {
  const script = document.createElement('script')
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`
  script.async = true
  document.head.appendChild(script)

  window.dataLayer = window.dataLayer || []
  function gtag(...args: unknown[]) { window.dataLayer.push(args) }
  gtag('js', new Date())
  gtag('config', GA_ID, { anonymize_ip: true, allow_google_signals: false })
}
```

---

## Step 3 — Typed Event Utility

Create `src/lib/analytics/ga4.ts`:

```typescript
type GAEvent =
  | 'sign_up' | 'sign_in'
  | 'course_started' | 'course_completed'
  | 'upgrade_clicked' | 'checkout_started' | 'purchase_completed'
  | 'resource_viewed' | 'assessment_taken'
  | string // escape hatch for custom events

interface GAEventParams {
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
  interface Window { gtag: (...args: unknown[]) => void }
}

export function trackEvent(name: GAEvent, params: GAEventParams = {}) {
  if (typeof window === 'undefined' || !window.gtag) return
  if (process.env.NODE_ENV !== 'production') return // dev guard

  window.gtag('event', name, {
    environment: 'production',
    ...params,
  })
}

export function setGAUser(userId: string, properties: Record<string, string> = {}) {
  if (typeof window === 'undefined' || !window.gtag) return
  const GA_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID
    ?? import.meta.env?.VITE_GA4_MEASUREMENT_ID
  if (!GA_ID) return

  window.gtag('set', 'user_properties', properties)
  window.gtag('config', GA_ID, { user_id: userId })
}
```

---

## Step 4 — Server-Side Measurement Protocol

Create `src/lib/analytics/ga4-server.ts`:

```typescript
const GA_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID
  ?? process.env.GA4_MEASUREMENT_ID
const API_SECRET = process.env.GA4_API_SECRET

export async function sendServerEvent(
  clientId: string,
  events: Array<{ name: string; params?: Record<string, unknown> }>
) {
  if (!GA_ID || !API_SECRET) return

  await fetch(
    `https://www.google-analytics.com/mp/collect?measurement_id=${GA_ID}&api_secret=${API_SECRET}`,
    {
      method: 'POST',
      body: JSON.stringify({ client_id: clientId, events }),
    }
  ).catch(() => {}) // never let analytics errors surface
}
```

---

## Step 5 — Custom Dimensions (Free Tier)

Set up manually in GA4 Admin → Custom Definitions → Create:

| Name        | Scope  | Purpose                          |
|-------------|--------|----------------------------------|
| tenant_id   | Event  | Per-deployment identifier        |
| org_id      | User   | Organization UUID                |
| user_role   | User   | Role-based segmentation          |
| environment | Event  | Filter dev/staging noise         |
| content_id  | Event  | Specific content UUID            |
| content_type| Event  | course, article, pathway         |

---

## Privacy Requirements

- `anonymize_ip: true` — required for GDPR baseline
- `allow_google_signals: false` — opt out of cross-site behavioral tracking
- Never send email, name, or PII as event properties
- Use UUID (not email) as `user_id`

---

## Anti-Patterns

- Do NOT send PII to GA4 — hard rejection + GDPR violation
- Do NOT load gtag with `strategy="beforeInteractive"` — blocks page render
- Do NOT set `tracesSampleRate: 1.0` in production for high-traffic apps
- Do NOT skip `anonymize_ip: true` in GA4 config
- Do NOT call `trackEvent` in Server Components (Next.js) — client-only
