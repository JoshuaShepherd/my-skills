# Per-route prompt template

> Copy this file, rename to `{route-slug}.md`, fill placeholders, and run in an agent session when a route is not covered by AGENT_RUNBOOK Prompts 04–09.

---

## Metadata

| Field | Value |
|-------|-------|
| **Route** | `{ROUTE}` e.g. `/content/articles/[slug]` |
| **Stitch order** | `{ORDER}` e.g. 9 |
| **Stitch prompt id** | `{STITCH_ID}` e.g. article-detail |
| **Cache file** | `.stitch/designs/{PAGE_SLUG}.html` |
| **Migration prompt** | [AGENT_RUNBOOK.md](./AGENT_RUNBOOK.md) Prompts 04–09 or custom |

---

## Copy-paste prompt

```
Stitch → React migration: {ROUTE} for {{TENANT_SLUG}}.

## Read first
- docs/build/stitch-migration/TENANT_MANIFEST.md — org, design theme, copy slots, excluded routes
- docs/build/stitch-migration/AGENT_RUNBOOK.md — non-negotiables + incomplete template policy

## Skills (invoke in order)
1. {{STITCH_REACT_SKILL}} — Archive Protocol, HTML decomposition, Phase 8 report
2. .claude/skills/stitch-page-port/SKILL.md — tenant copy, feature gates, hook wiring, synthesis

## Sources
- Stitch cache: .stitch/designs/{PAGE_SLUG}.html + .png
- Stitch spec: STITCH_ROUTE_INDEX.md + {{STITCH_PROMPTS_HTML}} → id={STITCH_ID}
- Reference code: {{REFERENCE_REPO}}/src/app/(public){AH_ROUTE_PATH}
- Checklist: COMPONENT_CHECKLIST.md → "{ROUTE}"
- Token bridge: docs/build/notes/stitch-token-bridge.md

## Required sections (in order)
{SECTION_LIST}

## Intended L4 components
| Section | Component path | Hook / config | Client? |
|---------|----------------|---------------|---------|
| {Section1} | `src/components/...` | {hook or tenantConfig} | yes/no |

## Current state
- [ ] PlaceholderPage
- [ ] Partial implementation
- [ ] page-old.tsx archived

## Conversion steps (stitch-page-port + stitch-react)
1. Read cached HTML + screenshot — visual audit
2. Read reference page + components for data-wiring patterns
3. Archive existing page.tsx → page-old.tsx
4. Decompose Stitch HTML into section components (plan → approve if >4 sections)
5. Apply token bridge — no wireframe hex (#111, #666)
6. Wire hooks from src/hooks/ if they exist; else static tenant copy from manifest
7. If hooks missing: flag BLOCKED for Prompts 13–14 before marking BUILT
8. Compose Server Component page.tsx with feature flags at page level
9. Handle loading / empty / error states in client sections

## Incomplete template correction
For each checklist section NOT in Stitch HTML:
- Implement from {{REFERENCE_REPO}} component + tenant tokens
- Use shadcn Card, Button, Input, Tabs, Accordion
- Match spacing: py-16 md:py-24, container max-w-7xl, 8px grid
- Mark PARTIAL with note "Stitch gap: {section}"

## Tenant copy slots (from TENANT_MANIFEST + {{CONTENT_RESEARCH}})
{TENANT_COPY_NOTES}

## Verification
- [ ] Section order matches checklist
- [ ] One h1 per page
- [ ] Semantic tokens only
- [ ] tenantConfig for tenant strings
- [ ] pnpm typecheck
- [ ] Update COMPONENT_CHECKLIST → BUILT or PARTIAL

## Report
Emit stitch-react Phase 8 conversion report when done.
```

---

## Section list helper

Pull section order from:

1. Stitch prompt text in `{{STITCH_PROMPTS_HTML}}` (`PROMPTS` entry for `{STITCH_ID}`)
2. [COMPONENT_CHECKLIST.md](./COMPONENT_CHECKLIST.template.md) row for `{ROUTE}`
3. `{{L5_PAGES}}` route table

If sources disagree, **Stitch prompt library section order wins** for IA; log conflict in gap audit.

---

## Cluster quick reference

See `.claude/skills/stitch-page-port/references/clusters.md` for full section specs per cluster.
