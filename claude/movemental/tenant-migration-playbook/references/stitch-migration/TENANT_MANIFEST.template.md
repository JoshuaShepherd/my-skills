# Tenant manifest — Movemental migration parameters

> **Fork this file to `TENANT_MANIFEST.md` before running any prompt.** Agents read it in Prompt 00 and substitute `{{VAR}}` placeholders throughout [AGENT_RUNBOOK.md](./AGENT_RUNBOOK.md).

---

## Platform (shared — same for all tenants)

| Variable | Value |
|----------|-------|
| `{{SUPABASE_PROJECT_ID}}` | `vhaiiiykcukrlyvwlgip` |
| `{{SUPABASE_PROJECT_REF}}` | `vhaiiiykcukrlyvwlgip` |
| `{{REFERENCE_REPO}}` | `../../../alan-hirsch` |
| `{{STITCH_PROMPTS_HTML}}` | `../../../brad-brisco/docs/build/stitch-prompts.html` |
| `{{STITCH_PROJECT_NAME}}` | `movemental-base-wireframe` |
| `{{STITCH_REACT_SKILL}}` | `../../../brad-brisco/.claude/skills/stitch-react/SKILL.md` |
| `{{TENANT_MIGRATE_SKILL}}` | `../../../brad-brisco/.claude/skills/tenant-migrate/SKILL.md` |
| `{{L4_SECTIONS}}` | `../../../brad-brisco/docs/internal/design/L4_SECTIONS.md` |
| `{{L5_PAGES}}` | `../../../brad-brisco/docs/internal/design/L5_PAGES.md` |
| `{{REFERENCE_PLATFORM_UI}}` | `docs/internal/engineering/REFERENCE_PLATFORM_UI_INVENTORY.md` |
| `{{REFERENCE_PAGE_COMPARISON}}` | `docs/internal/engineering/REFERENCE_PAGE_COMPARISON.md` |

---

## Target tenant (change per leader)

| Variable | Example: Danielle Strickland |
|----------|------------------------------|
| `{{TENANT_SLUG}}` | `danielle-strickland` |
| `{{TENANT_NAME}}` | Danielle Strickland |
| `{{TENANT_ORG_ID}}` | `aab5a6f6-d8af-44d5-a0e2-b8f76da06124` |
| `{{TENANT_TAGLINE}}` | _Fill from research_ |
| `{{TARGET_REPO}}` | `movement-leader-websites/danielle-strickland` |
| `{{DESIGN_THEME}}` | _e.g. Earthy Boldness — see docs/build/notes/_ |
| `{{DESIGN_CHARTER}}` | `docs/internal/design/DESIGN_CHARTER.md` |
| `{{GLOBALS_CSS}}` | `src/app/globals.css` |
| `{{TENANT_CONFIG}}` | `src/lib/config/tenant.config.ts` |
| `{{CONTENT_RESEARCH}}` | `../../../../movemental-ai/docs/movement_leader_research/_onboarded_leaders/danielle-strickland/` |
| `{{CORPUS_SLUG}}` | _none or corpus id_ |
| `{{AI_ASSISTANT_LABEL}}` | Danielle Strickland AI |
| `{{STORAGE_PREFIX}}` | `media-library/danielle-strickland/` |

---

## Reference tenants (leak grep boundaries)

| Variable | Value |
|----------|-------|
| `{{SOURCE_TENANT_NAME}}` | Alan Hirsch |
| `{{SOURCE_TENANT_SLUG}}` | `alan-hirsch` |
| `{{SOURCE_ORG_ID}}` | `6bc0fcf7-2e55-4914-b88d-c6eb49eb0d71` |
| `{{STITCH_PLACEHOLDER_TENANT}}` | Brad Brisco (Stitch wireframe copy — not shipped) |
| `{{STITCH_PLACEHOLDER_ORG_ID}}` | `8dd3436b-b5dc-4427-a3a4-973e8450314b` |

---

## Pathways / themes (5 slots)

| # | Slug | Title |
|---|------|-------|
| 1 | `{{PATHWAY_SLUG_1}}` | _Fill_ |
| 2 | `{{PATHWAY_SLUG_2}}` | _Fill_ |
| 3 | `{{PATHWAY_SLUG_3}}` | _Fill_ |
| 4 | `{{PATHWAY_SLUG_4}}` | _Fill_ |
| 5 | `{{PATHWAY_SLUG_5}}` | _Fill_ |

---

## Feature flags (align with DB in Prompt 15)

| Feature | Enabled | Notes |
|---------|---------|-------|
| articles | false | Enable when org has articles |
| books | false | |
| courses | false | Port infra before enabling |
| podcasts | false | |
| videos | false | |
| chat | false | Requires vector store + agent env |
| themes / pathways | false | Uses `themes[]` in tenant.config |
| assessments | false | Stitch optional #34 |
| auth | true | |
| search | false | |
| certificates | false | |

---

## Route scope

### In scope

All routes in `{{STITCH_PROMPTS_HTML}}` except excluded rows below.

### Tenant-unique routes (build if product requires)

| Route | Notes |
|-------|-------|
| _Add per leader_ | Not in base Stitch library |

### Excluded routes (do not port unless product adds)

| Route | Reason |
|-------|--------|
| `/reneighbor` | Brad Brisco tenant-unique (Stitch #35) |
| `/hero-showcase` | Alan demo |
| `/ai-lab-archive` | Alan demo |
| `/[orgSlug]/*` | Alan org landing |

### Legacy redirects

| Legacy | Target |
|--------|--------|
| `/library` | `/content` |
| `/essays` | `/content/articles` |
| `/sign-in` | `/auth/signin` |
| `/auth` | `/auth/signin` |

---

## Content leak grep patterns

Run on `src/` after migration slices (Prompt 10, 15):

```
{{SOURCE_TENANT_NAME}}
{{SOURCE_TENANT_SLUG}}
alanhirsch
mDNA
APEST
Forgotten Ways
5Q
{{STITCH_PLACEHOLDER_TENANT}}
Brad Brisco
reneighbor
```

**Allowlist:** `docs/internal/engineering/*` comparison docs; comments "ported from reference platform".

---

## Branch naming

| Pattern | Use |
|---------|-----|
| `slice/Sxx-stitch-{topic}` | UI migration slices |
| `slice/Sxx-backend-{topic}` | Backend parity slices |
| `slice/Sxx-migration-{topic}` | Structural port from Alan |

Never commit directly to `main`.

---

## Local skills (target repo)

| Skill | Path |
|-------|------|
| Orchestrator | `.claude/skills/tenant-migration-playbook/SKILL.md` |
| Intake | `.claude/skills/stitch-intake-audit/SKILL.md` |
| Token bridge | `.claude/skills/stitch-token-bridge/SKILL.md` |
| Page port | `.claude/skills/stitch-page-port/SKILL.md` |
| UI validate | `.claude/skills/stitch-migration-validate/SKILL.md` |
| Backend parity | `.claude/skills/tenant-backend-parity/SKILL.md` |
| Structural port | `.claude/skills/tenant-structural-port/SKILL.md` |

---

*Template — copy to TENANT_MANIFEST.md and fill all tenant-specific values.*
