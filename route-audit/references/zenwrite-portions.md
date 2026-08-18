# ZenWrite / Movemental Studio — route-audit portions

This repo does **not** use React Router path trees for the studio SPA. Use this map when the user asks to audit “Create”, “Money”, “public pricing”, etc.

## Commands (repo root)

```bash
pnpm exec node scripts/build-route-manifest.mjs          # merge AppView + reader routes
pnpm exec node scripts/gen-route-specs.mjs --phase <id>  # regenerate one phase spec
pnpm audit:routes                                       # certified: 1-public + 2-studio-home
pnpm audit:routes:all                                   # every e2e/routes/*.spec.ts
pnpm exec playwright test e2e/routes/<phase>.spec.ts
```

Contract: `routes.manifest.yaml` · State: `docs/audit/routes/` · Specs: `e2e/routes/`

## Portion → phase

| User says / surface | Phase id | Fixture pattern |
|---------------------|----------|-----------------|
| Public pricing, subscribe, feeds, robots, sitemap | `1-public` | `/pricing`, `/subscribe`, … |
| Home | `2-studio-home` | `/` |
| Create, Organize, Citations, Collection, Library, Calendar | `3-studio-content` | `/?view=create` … |
| Reach/Engage, Programs, Money, Manage, Analyze, Communications | `4-studio-community` | `/?view=engage` … |
| Book reading / peer preview | `5-studio-reading` | `/?view=book-reading&bookId=…` |
| Operations, Flow, theme/sample review | `6-studio-ops` | `/?view=admin`, `/?view=flow&phase=kickoff` |
| Published reader HTML (`/articles/:slug`, books, …) | `7-public-content` | real slug fixtures only |
| Signed-out / auth confirm | `auth` | no session / confirm token |

## Single-route path

1. Resolve the URL or `?view=` from the table (or ask if ambiguous).
2. Preflight (setup-and-install.md).
3. DevTools: navigate → snapshot → console → network (≥400) → screenshot under `docs/audit/routes/evidence/<phase>/`.
4. If fixing: repair source → update `must_render` in the manifest → `gen-route-specs` for that phase → `playwright test` that spec.
5. Sign-off only in a **later turn** when the committed spec is green on the current SHA.

## Regression-only path

Skip DevTools. Run:

```bash
pnpm audit:routes:all
# or one phase:
pnpm exec playwright test e2e/routes/3-studio-content.spec.ts
```

Only red routes get a DevTools diagnose session.

## Fixture rule

Never invent slugs. If `REPLACE-ME` remains in the manifest, `test.skip` is correct. Ask the user for a real published slug or seed before walking `7-public-content`.
