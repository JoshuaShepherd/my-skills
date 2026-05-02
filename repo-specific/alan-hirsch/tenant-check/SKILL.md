---
name: tenant-check
description: Audit components for hardcoded tenant strings, non-semantic colors, or missing feature flags. Use before PR review or to check tenant isolation.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit the codebase for tenant config violations.

## Checks

1. **Hardcoded colors**: Search for `bg-blue`, `bg-gray`, `text-gray`, hex values (#xxx, #xxxxxx), rgb()/hsl() in component files under `src/components/` and `src/app/(public)/`
2. **Hardcoded tenant strings**: Search for the tenant name "Alan Hirsch" in components (should use `tenantConfig` or `useTenant()`)
3. **Missing feature flags**: Search for chat/AI features rendered without checking `tenant.features.*`
4. **Direct API calls**: Search for raw `fetch()` in components (should use hooks from `src/hooks/`)
5. **Modified ui components**: Check if any files in `src/components/ui/` have been modified with hardcoded styles

## Output

Report violations grouped by file with line numbers and suggested fixes.
Only scan `src/components/` and `src/app/(public)/`.
Ignore files in `src/components/ui/` for checks 1-4 (those are shadcn base components).
