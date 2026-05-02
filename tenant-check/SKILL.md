---
name: tenant-check
description: Audit components for hardcoded tenant strings, non-semantic colors, or missing feature flags. Use before PR review or to check tenant isolation readiness.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit the movemental codebase for tenant config violations.

Target: $ARGUMENTS

If no target, scan `src/components/` and `src/app/(site)/`.

## What to Check

### 1. Hardcoded Tenant Strings

Search for strings that should come from a config or CMS, not be hardcoded in components:

- Brand name "Movemental" hardcoded in components (allowed in metadata/SEO, flagged in reusable components)
- Domain references: `movemental.com` in component code
- Specific leader names (e.g., "Alan Hirsch", "Brad Brisco") in reusable components
- Pricing figures (`$1,000`, `90%`, `10%`) in reusable components vs data arrays
- Contact info, addresses, phone numbers inline

### 2. Non-Semantic Colors

Run the same checks as `tailwind-cleanup` §1:
- Any `bg-white`, `bg-black`, `text-white`, `text-black` outside midnight context
- Any Tailwind palette colors: `bg-blue-*`, `text-gray-*`, etc.
- Any hardcoded hex values in JSX

### 3. Feature Flag Readiness

Check whether optional sections could be gated:
- Sections that might not apply to all future tenants
- Content blocks that assume a specific audience (churches, nonprofits, movement leaders)
- Pricing tiers or economics that are tenant-specific

## Output Format

```markdown
## Tenant Check Report

### Hardcoded Strings
| File | Line | String | Recommendation |
|------|------|--------|---------------|

### Color Violations
| File | Line | Class | Fix |
|------|------|-------|-----|

### Feature Flag Opportunities
| File | Section | Suggestion |
|------|---------|-----------|
```

## Rules

- This is an AUDIT skill — report findings, don't auto-fix.
- Hardcoded strings in page-level `metadata` exports are acceptable (SEO needs).
- Hardcoded strings in data arrays at the top of page files are acceptable for now (will be migrated to CMS/config later).
- Focus on reusable components that would break if used for a different tenant.
