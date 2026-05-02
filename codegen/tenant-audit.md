
Audit the codebase for tenant config violations.

## Checks

1. **Hardcoded colors**: Search for `bg-blue`, `bg-gray`, `text-gray`, hex values (#xxx, #xxxxxx), rgb()/hsl() in component files under `{{COMPONENTS_DIR}}/` and `src/app/(public)/`
2. **Hardcoded tenant strings**: Search for the tenant name "{{AUTHOR_NAME}}" in components (should use `brandConfig` or `useBrand()`)
3. **Missing feature flags**: Search for chat/AI features rendered without checking `brand.features.*`
4. **Direct API calls**: Search for raw `fetch()` in components (should use hooks from `{{HOOKS_DIR}}/`)
5. **Modified ui components**: Check if any files in `{{UI_COMPONENTS_DIR}}/` have been modified with hardcoded styles

## Output

Report violations grouped by file with line numbers and suggested fixes.
Only scan `{{COMPONENTS_DIR}}/` and `src/app/(public)/`.
Ignore files in `{{UI_COMPONENTS_DIR}}/` for checks 1-4 (those are shadcn base components).
