
Run the layer validation chain bottom-up. Stop at the first failure and report it.

1. Run `pnpm db:check`
2. Run `pnpm contracts:check`
3. Run `pnpm services:check`
4. Run `pnpm routes:check`
5. Run `pnpm hooks:check`
6. Run `pnpm ui:check`

If all pass, report "All 6 layers valid."
If one fails, report which layer failed and suggest the fix approach (always fix at the source layer, never upstream).
