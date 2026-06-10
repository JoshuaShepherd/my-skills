# Movemental narrative audit — extended reference

## Fragmentation book (manuscript)

Primary path: `docs/book-development/fragmentation-manuscript-ordered/`

| File | Use when auditing… |
| ---- | -------------------- |
| `00-preface-the-scatter-field.md` | Scatter metaphor, emotional opening |
| `02-two-intelligences.md` | Definitions of informational vs relational |
| `03-fragmentation-is-structural.md` | Why tool/content fixes fail |
| `05-the-six-stages-at-a-glance.md` | **Authoritative stage list and ordering** |
| `06-what-integration-actually-is.md` | Foundation vs symptoms |
| `09-why-integration-stalls.md` | Political/theological stall language |
| `12-formation-as-the-moral-stage.md` | Formation + relationship seam |
| `14-multiplication-when-the-work-stops-depending-on-you.md` | Multiplication vs franchising |
| `16-movement-when-platforms-become-a-field.md` | Movement / field language |

Live book experience (reading UI, routes): `src/app/(site)/book/` — use for **product** alignment; manuscript folder for **thesis** alignment.

## Articles — high-signal defaults

Start here when the page touches these themes:

| Theme | Starting files |
| ----- | ---------------- |
| Core “why” + scenius | `docs/articles/the-story-of-movemental.md` |
| Two intelligences (long) | `docs/articles/two-intelligences-integration.md` |
| Transformation vs information | `docs/articles/03-transformation-over-information.md` |
| Fragmentation cost | `docs/articles/the-cost-of-fragmentation.md`, `docs/articles/intelligence-fragmentation.md` |
| AI + integration | `docs/articles/ai-collapses-the-cost-of-integration.md`, `docs/articles/context-changes-everything.md` |
| Playbooks | `docs/articles/playbook-movement-leader.md`, `playbook-nonprofit.md`, `playbook-church.md`, `playbook-institution.md` |
| Published-style articles | `docs/content/articles/*.md` |

Use `Glob` on `docs/articles/` for domain-specific audits (fundraising, governance, courses).

## Code anchors for live copy

- Home narrative chain: `src/components/sections/home/home-*.tsx` (see `home-page-content.tsx` for section order).
- Fragmentation story shell: `fragmentation-story-new-shell.tsx` and stages under `fragmentation-story-stage-*.tsx`.
- Site metadata patterns: `src/app/(site)/page.tsx`, `src/app/(site)/fragmentation/page.tsx`.

## Common drift patterns (shorthand)

| Pattern | Why it’s misaligned |
| ------- | --------------------- |
| “AI will write your content” | Conflicts with grounded corpus + voice; often implies replacement not amplification |
| “Grow faster / scale overnight” | Conflicts with formation-over-growth and ordered stages |
| “All-in-one tool” without foundation | Tool-first; misses integration + library/graph/voice |
| “Join thousands” open network | May conflict with curated network / credibility framing unless sourced |
| Skipping to Movement/Multiplication | Violates stage dependencies from Ch.5 |
| Single-intelligence framing | Omits relational intelligence when both apply |

## Pairing with `page-audit`

| This skill (`movemental-narrative-audit`) | `page-audit` |
| ---------------------------------------- | ------------- |
| Thesis, vocabulary, stage logic, offer | Tokens, layout, a11y, Stitch parity, SEO mechanics |
| “Are we saying the right thing?” | “Are we building it right?” |

Run narrative first when messaging is in question; run both for a full ship review.
