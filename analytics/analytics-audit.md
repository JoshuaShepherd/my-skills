---
name: analytics-audit
description: Audit an analytics implementation across all providers (GA4, PostHog, Vercel Analytics, database events) — verifies events fire correctly, tenant isolation, user identity wiring, event naming consistency, and GDPR/privacy compliance.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent
---

Run a comprehensive analytics audit: $ARGUMENTS

$ARGUMENTS should include:
- `--provider <ga4|posthog|vercel|db|all>` — scope (default: all)
- `--fix` — attempt to fix issues found (default: report only)

---

## Severity Levels

- **CRITICAL** — Data not being collected at all, or tenant data leaking between orgs
- **HIGH** — Key dimension missing, identity not wired, data inaccurate
- **MEDIUM** — Best practice violation, data quality degraded
- **LOW** — Minor improvement opportunity

---

## Check 1: Package Installation

```bash
grep -E "@vercel/analytics|@vercel/speed-insights|posthog-js|posthog-node" package.json
```

**CRITICAL** if any expected provider package is missing.

Check root layout/entry for:
- `<Analytics />` from `@vercel/analytics`
- `<SpeedInsights />` from `@vercel/speed-insights`
- PostHog provider wrapping children
- GA4 gtag Script tags

---

## Check 2: Development Guard

Every analytics provider should be gated in development:

- PostHog: `ph.opt_out_capturing()` in `loaded` callback when `NODE_ENV !== 'production'`
- GA4: `if (process.env.NODE_ENV !== 'production') return` in `trackEvent()`
- DB events: `environment` column set from `process.env.NODE_ENV`

**MEDIUM** if no dev guard — dev events pollute production data.

---

## Check 3: Tenant Isolation (Multi-Tenant Only)

This is the highest-risk area for multi-tenant apps.

### 3a. GA4 events include tenant_id
Read the GA4 event utility. Verify `tenant_id` is appended automatically in the base `trackEvent()` function. Should never rely on callers to pass it.

**CRITICAL** if `tenant_id` not in base event call.

### 3b. PostHog events include tenant_id
Read the PostHog capture utility. Verify `tenant_id` is in base `captureEvent()`.

**CRITICAL** if missing.

### 3c. PostHog group analytics configured
Check auth flow for `posthog.group('organization', orgId)` and `posthog.group('tenant', tenantId)`.

**HIGH** if not configured — PostHog dashboard can't filter by org.

### 3d. Database RLS configured
Run:
```sql
SELECT tablename, rowsecurity FROM pg_tables
WHERE tablename = 'analytics_events';

SELECT policyname, cmd FROM pg_policies
WHERE tablename = 'analytics_events';
```

**CRITICAL** if RLS disabled or no SELECT policy — cross-tenant data exposure.

---

## Check 4: User Identity

### 4a. PostHog identify called after auth
Grep for `posthog.identify` near auth callbacks.

**HIGH** if never called — all events anonymous, no person-level analytics.

### 4b. PostHog reset called on logout
Grep for `posthog.reset()` near sign-out logic.

**HIGH** if missing — user identity bleeding between sessions.

### 4c. GA4 user_id set after auth
Grep for `gtag.*user_id` or `setGAUser`.

**MEDIUM** if missing — cross-session recognition won't work.

### 4d. user_id is UUID, not email
Verify `user_id` values passed to analytics are Supabase UUIDs, not email addresses.

**CRITICAL** if email is used as user_id — GDPR violation.

---

## Check 5: Event Naming Consistency

Grep across all analytics calls:
```bash
grep -r "trackEvent\|captureEvent\|posthog\.capture\|track(" src/ \
  --include="*.ts" --include="*.tsx"
```

Verify:
- All event names are snake_case
- Same semantic event uses identical name across all providers
- No camelCase, PascalCase, or spaces in event names

**MEDIUM** for naming inconsistencies — fragmented data across providers.

---

## Check 6: Privacy & GDPR

### 6a. GA4 IP anonymization
Read GA4 init config. Verify `anonymize_ip: true`.

**CRITICAL** if missing — GDPR baseline violation.

### 6b. No PII in event properties
```bash
grep -r "email\|\.name\|phone\|address" src/lib/analytics/ --include="*.ts"
```

**CRITICAL** if email or names appear as event property values.

### 6c. PostHog session replay masks inputs
Read PostHog init. Verify `session_recording: { maskAllInputs: true }`.

**HIGH** if `maskAllInputs` is false — passwords and form data visible in replays.

### 6d. GA4 Google Signals disabled
Read GA4 config. Verify `allow_google_signals: false`.

**MEDIUM** if missing — enables unwanted cross-site behavioral targeting.

---

## Check 7: Server-Side Events

### 7a. Purchase/payment events fire server-side
Read webhook handler (Stripe, etc.). Verify `purchase_completed` event sent via Measurement Protocol or `posthog-node`.

**HIGH** if webhooks don't fire analytics — purchase data missing.

### 7b. posthog-node flushes in serverless
Read server-side PostHog usage. Verify `await client.flush()` after every `capture()`.

**CRITICAL** if missing — server events silently dropped.

---

## Check 8: Vercel Analytics Activated

Packages installed ≠ data collected. Vercel Analytics requires manual activation.

Reminder: Verify in Vercel Dashboard → project → Analytics tab that it shows "Enabled."

**HIGH** if packages installed but activation unknown.

---

## Output Format

```
# Analytics Audit Report
Date: {date}
Providers: GA4, PostHog, Vercel Analytics, Supabase DB

## Summary
CRITICAL: {n} | HIGH: {n} | MEDIUM: {n} | LOW: {n}

## Findings

### [CRITICAL] tenant_id missing from GA4 events
What: trackEvent() does not append tenant_id automatically
Impact: Cannot segment GA4 data by tenant — all orgs mixed
Evidence: src/lib/analytics/ga4.ts:34
Fix: Add `tenant_id: getTenantId()` to base event params

## Passing
- [PASS] PostHog installed and provider in root layout
- [PASS] IP anonymization enabled in GA4
- [PASS] Session replay masking all inputs
```
