---
name: analytics-audit
description: Audit the analytics implementation across all providers (GA4, PostHog, Vercel Analytics, Supabase) — verifies events fire correctly, tenant_id is set on all events, no duplicates, user identity is wired, and privacy/GDPR compliance is met.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent
---

Run a comprehensive analytics audit: $ARGUMENTS

$ARGUMENTS should include:
- `--provider <ga4|posthog|vercel|supabase|all>` — scope the audit (default: all)
- `--fix` — attempt to fix issues found (default: report only)

---

## Audit Protocol

Run ALL checks in order. Report findings with severity:
- **CRITICAL** — Data is not being collected at all
- **HIGH** — Data is inaccurate or missing key dimensions
- **MEDIUM** — Best practice violation, data quality issue
- **LOW** — Minor improvement, future-proofing

---

## Check 1: Provider Installation

### 1a. Verify packages are installed

```bash
grep -E "@vercel/analytics|@vercel/speed-insights|posthog-js|posthog-node" package.json
```

**Flag CRITICAL if** any expected provider package is missing.

### 1b. Verify root layout wiring

Read `src/app/layout.tsx`. Check for:
- `<Analytics />` from `@vercel/analytics/react`
- `<SpeedInsights />` from `@vercel/speed-insights/next`
- `<PostHogProvider>` wrapping children
- GA4 `<Script>` tags with `strategy="afterInteractive"`

**Flag CRITICAL if** any provider component is missing from root layout.

### 1c. Check for duplicate provider initialization

Grep for `posthog.init\|Sentry.init\|gtag\('config'` — each should appear exactly once in the codebase (in the instrument/provider file). Multiple calls = duplicate initialization = data inflation.

**Flag HIGH if** any provider is initialized more than once.

---

## Check 2: Environment Variable Coverage

### 2a. Verify all analytics env vars are set

Check `.env.local.example` for:
- `NEXT_PUBLIC_GA4_MEASUREMENT_ID`
- `GA4_API_SECRET`
- `NEXT_PUBLIC_POSTHOG_KEY`
- `NEXT_PUBLIC_POSTHOG_HOST`

Grep `src/lib/env.ts` to verify they're validated at runtime.

**Flag HIGH if** env vars are used in code but not validated in `env.ts`.

### 2b. Check development guard patterns

Grep for `process.env.NODE_ENV === 'development'` or `opt_out_capturing()` in analytics initialization files.

**Flag MEDIUM if** no dev guard exists — dev events will pollute production data.

---

## Check 3: Tenant Isolation

This is the most critical check for a multi-tenant platform.

### 3a. GA4 events include tenant_id

Read `src/lib/analytics/ga4.ts`. Verify `trackEvent()` automatically appends `tenant_id: getTenantOrgId()`.

**Flag CRITICAL if** `getTenantOrgId()` is not called in the base event function.

### 3b. PostHog events include tenant_id

Read `src/lib/analytics/posthog-events.ts`. Verify `captureEvent()` automatically appends `tenant_id`.

**Flag CRITICAL if** `getTenantOrgId()` is not in the base capture function.

### 3c. PostHog groups are set

Read the auth provider/identify component. Verify `posthog.group('organization', orgId)` and `posthog.group('tenant', tenantId)` are called after login.

**Flag HIGH if** group analytics are not configured — you won't be able to filter PostHog by org.

### 3d. Supabase analytics_events has RLS

Run via Supabase MCP:
```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE tablename = 'analytics_events'
AND schemaname = 'public';
```

Then check policies:
```sql
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'analytics_events';
```

**Flag CRITICAL if** RLS is disabled or no SELECT policy exists — all orgs can see each other's data.

---

## Check 4: User Identity

### 4a. PostHog identify is called after auth

Grep for `posthog.identify\|PostHogIdentify` in auth-related components. Verify it's called with `userId` (Supabase UUID, not email).

**Flag HIGH if** identify is never called — all events will be anonymous, losing person-level analytics.

### 4b. GA4 user_id is set after auth

Grep for `setGA4User` or `gtag.*user_id`. Verify it's called in an auth effect.

**Flag MEDIUM if** GA4 user_id is never set — cross-session user recognition won't work.

### 4c. PostHog reset is called on logout

Grep for `posthog.reset()` near sign-out logic.

**Flag HIGH if** reset is not called — one user's events will bleed into the next user's session on shared devices.

---

## Check 5: Event Naming Consistency

### 5a. Event names are snake_case

Grep for all event tracking calls across `src/`:
```bash
grep -r "trackEvent\|captureEvent\|posthog\.capture\|track(" src/ --include="*.ts" --include="*.tsx"
```

Verify all event names match the canonical taxonomy (snake_case):
- `course_started`, `course_completed`
- `sign_up`, `sign_in`
- `upgrade_clicked`, `checkout_started`, `purchase_completed`
- `resource_viewed`, `assessment_taken`

**Flag MEDIUM if** any events use camelCase, PascalCase, or spaces — causes fragmented data in dashboards.

### 5b. Check for duplicate event names across providers

Verify the same semantic event (e.g., course completed) uses the same name in GA4, PostHog, and Supabase. Inconsistent naming across providers makes cross-referencing impossible.

---

## Check 6: Privacy & GDPR Compliance

### 6a. IP anonymization enabled in GA4

Read the GA4 gtag initialization. Verify:
```javascript
gtag('config', GA_ID, { anonymize_ip: true })
```

**Flag CRITICAL if** `anonymize_ip` is false or missing — GDPR violation.

### 6b. No PII in event properties

Grep for `email\|name\|phone\|address` in analytics event calls. PII should never appear in event property values.

**Flag CRITICAL if** email or name fields are passed as event properties to GA4 or PostHog.

### 6c. Session replay masks sensitive inputs

Read PostHog initialization. Verify:
```javascript
session_recording: { maskAllInputs: true }
```

**Flag HIGH if** `maskAllInputs` is false — passwords and form data will be recorded.

### 6d. GA4 `allow_google_signals` is false

Read GA4 gtag config. Verify `allow_google_signals: false` to opt out of Google cross-site tracking features.

**Flag MEDIUM if** missing — may enable unwanted cross-site behavioral targeting.

---

## Check 7: Server-Side Events

### 7a. Stripe webhooks fire analytics events

Read `src/app/api/webhooks/stripe/route.ts`. Verify `purchase_completed` (or equivalent) is sent via Measurement Protocol or `posthog-node` on `checkout.session.completed`.

**Flag HIGH if** Stripe webhook does not fire analytics events — purchase data will be missing from analytics.

### 7b. posthog-node flushes in serverless

Read `src/lib/analytics/posthog-server.ts`. Verify `await client.flush()` is called after every `client.capture()`.

**Flag CRITICAL if** flush is missing — server events are silently dropped in serverless environments.

---

## Check 8: Vercel Analytics

### 8a. Analytics and SpeedInsights are in root layout

Read `src/app/layout.tsx`. Check for both components.

### 8b. Custom events use `track()` not direct gtag

Read any files using `@vercel/analytics`. Verify they use `import { track } from '@vercel/analytics'`.

### 8c. Vercel Analytics is enabled in dashboard

Reminder: Vercel Analytics requires manual activation in the Vercel Dashboard → Analytics tab. Packages installed but not activated = no data collected.

**Flag HIGH if** packages are installed but activation status is unknown.

---

## Output Format

```
# Analytics Audit Report
Date: {date}
Project: {name}
Providers checked: GA4, PostHog, Vercel Analytics, Supabase

## Summary
- CRITICAL: {n}
- HIGH: {n}
- MEDIUM: {n}
- LOW: {n}

## Findings

### [CRITICAL] tenant_id not set on GA4 events
What: trackEvent() does not append tenant_id
Impact: Cannot segment GA4 data by tenant — all data is mixed
Evidence: src/lib/analytics/ga4.ts:42
Fix: Add `tenant_id: getTenantOrgId()` to the base event call

...

## Passing Checks
- [PASS] PostHog installed and provider wired in root layout
- [PASS] IP anonymization enabled in GA4
...
```
