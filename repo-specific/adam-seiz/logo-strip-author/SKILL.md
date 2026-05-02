---
name: logo-strip-author
description: Author a complete social proof / logo strip section for an author or leader — copy, grouping strategy, TypeScript content definition, React component spec, CSS/Tailwind implementation, and logo download checklist. Run after affiliation-scrape and affiliation-audit.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
---

Author the logo strip section for: $ARGUMENTS

$ARGUMENTS should include:
- A person slug (e.g. `alan-hirsch`) — reads `content-library/affiliations/{slug}.json`
- Optionally: a target page or component path to write to (e.g. `--page src/app/(public)/about/page.tsx`)
- Optionally: a layout variant: `--layout grouped` (default) / `--layout flat` / `--layout marquee`
- Optionally: `--max N` to limit the strip to N logos (default: 12)
- Optionally: `--dark` to generate a dark-background variant instead of light
- Optionally: `--tenant` to wire output to the tenant config system instead of inline

## Before Starting

1. Read `content-library/affiliations/{slug}.json` — the scraped + audited affiliation data
2. If not found, instruct user to run `/affiliation-scrape {name}` then `/affiliation-audit {slug}`
3. Read `src/lib/config/tenant.config.ts` — understand the tenant config structure if `--tenant` is passed
4. Read `src/app/globals.css` — note the CSS variables (primary, muted, border, background, etc.)
5. Scan `public/images/orgs/` — see which logos are already downloaded locally
6. If a target page is given, read that file to understand the existing layout and component imports

## What to Produce

This skill produces **four deliverables** in sequence:

1. **Content definition** — TypeScript data structure for the strip
2. **Copy** — headline, sub-headline, group labels, and link copy
3. **React component** — the `LogoStrip` or `SocialProof` component (or a section block for an existing page)
4. **Logo checklist** — which logos need to be downloaded locally and how

---

## Deliverable 1 — Content Definition

### Strip Selection Rules

From the affiliation JSON, select logos for the strip using this priority:

1. **Include all** `include_in_strip: true` + `confidence: HIGH` + logo grade A or B
2. **Include** `include_in_strip: true` + `confidence: HIGH` + logo grade C (with note)
3. **Include** `include_in_strip: true` + `confidence: MEDIUM` + logo grade A or B (up to `--max`)
4. **Exclude** any `confidence: LOW`
5. **Exclude** any logo grade D or F (flag for manual fix)
6. **Cap at** `--max` logos total (default: 12), prioritizing by `prominence_score` desc

### Group Organization

Sort selected logos into groups. Canonical group order:

1. **Publishers** (`strip_group: "publishers"`) — highest credibility, always first
2. **Academic** (`strip_group: "academic"`) — seminaries, universities
3. **Networks** (`strip_group: "networks"`) — movements, coalitions, denominational partnerships
4. **Speaking** (`strip_group: "speaking"`) — speaking bureaus, major conference series
5. **Media** (`strip_group: "media"`) — magazines, podcasts, outlets, websites
6. **Partners** (`strip_group: "partners"`) — ministry and strategic partners

Within each group, sort by `prominence_score` descending.

If a group has only 1 logo, merge it into the nearest semantically appropriate group and note the merge.

### TypeScript Content Shape

Define the content as a TypeScript object (place in `src/lib/content/social-proof/{slug}.ts` or inline in tenant config):

```typescript
export type LogoStripOrg = {
  id: string
  name: string
  shortName?: string
  category: string
  logoPath: string          // relative to public/ e.g. /images/orgs/baker-books.svg
  logoAlt: string
  website: string
  relationshipDescription: string   // 1 sentence for tooltip/screen reader
  prominenceScore: number           // 1–10
}

export type LogoStripGroup = {
  id: string
  label: string             // e.g. "Published by"
  orgs: LogoStripOrg[]
}

export type SocialProofSection = {
  headline: string
  subHeadline?: string
  groups: LogoStripGroup[]
  footnote?: string         // e.g. "Logos used with permission for identification purposes"
}
```

Output the fully populated `SocialProofSection` object with all selected orgs.

---

## Deliverable 2 — Copy

### Headline Strategy

Choose the headline based on which credibility signal is strongest:

| Primary strength | Headline pattern |
|----------------|-----------------|
| Publisher credibility | "Published by the world's leading voices in Christian publishing" |
| Speaker credibility | "A trusted voice on the world's most important stages" |
| Movement/network depth | "Embedded in the networks shaping the global church" |
| Media reach | "A voice that has reached millions through leading media" |
| Balanced across all | "Trusted across the global church — by publishers, movements, and stages" |

For Alan Hirsch specifically, use the networks/publisher frame — his credibility comes from depth of publication and movement embeddedness.

### Sub-Headline

Optional but recommended. 1–2 sentences that contextualize the logos:
- Name the scope (global, evangelical, charismatic, etc.)
- Reference the span of time if notable (e.g., "for over two decades")
- Bridge from the person's mission to the organizations: "Because the work of renewing the church requires the full ecosystem to come together."

### Group Labels

Labels should be relationship-specific and action-oriented:

| Group | Good label | Avoid |
|-------|-----------|-------|
| publishers | "Published by" | "Books" |
| academic | "Teaching at" or "Faculty at" | "Universities" |
| networks | "Part of" or "In partnership with" | "Affiliates" |
| speaking | "Speaking through" or "On stage at" | "Speaking" |
| media | "As featured in" or "Featured in" | "Press" |
| partners | "In ministry with" | "Partners" |

### Tooltip / Accessible Description

For each org, write a 1-sentence relationship description that will be used as:
- `title` attribute on logo `<a>` tag
- `aria-label` for screen readers
- Tooltip on hover (optional)

Pattern: `"{Org name} — {relationship type} since {year/decade}"`
Example: `"Baker Books — Alan's primary publisher since 2006, home of The mDNA and 5Q"`

### Footnote (optional)

If the organization logos may raise IP concerns, add a tasteful footnote:
`"Logos are trademarks of their respective organizations and are used here for identification purposes only."`

---

## Deliverable 3 — React Component

### Design Principles to Encode

**Visual:**
- Logos displayed in grayscale by default (`filter: grayscale(1) opacity(0.7)`)
- On hover: full color + full opacity (`filter: none opacity(1)`) with smooth 200ms transition
- Consistent logo height: 40px mobile, 48px tablet, 56px desktop (variable width)
- Group labels: small caps, muted-foreground, 11px
- Generous horizontal spacing between logos: `gap-8` to `gap-12`
- Section background: `bg-muted/30` or `bg-background` (matches surrounding design)

**Layout — Grouped (default):**
- Each group in its own row or subsection
- Group label left-aligned above the logo row
- Logos in a horizontal flex row (wrapping on mobile)

**Layout — Flat:**
- All logos in a single horizontal row (or two rows)
- No group labels (optionally add a single section label)
- Best for short strips (≤ 8 logos)

**Layout — Marquee:**
- Infinite horizontal scroll animation
- Logos repeat (2x duplication for seamless loop)
- Use CSS animation, not JavaScript — `@keyframes scroll`
- Pause on hover (`animation-play-state: paused`)
- Best for large logo counts (≥ 12) or hero/footer placement

### Component Shell

Generate a production-ready component at `src/components/social-proof/LogoStrip.tsx` (or `SocialProofSection.tsx`):

```tsx
// src/components/social-proof/LogoStrip.tsx
"use client"

import Image from "next/image"
import Link from "next/link"
import { cn } from "@/lib/utils"
import type { SocialProofSection } from "@/lib/content/social-proof/types"

interface LogoStripProps {
  content: SocialProofSection
  variant?: "grouped" | "flat" | "marquee"
  className?: string
}

export function LogoStrip({ content, variant = "grouped", className }: LogoStripProps) {
  // ... implementation based on variant
}
```

**Key implementation details to include:**

1. **Image handling**: Use `next/image` with `unoptimized` for SVGs, set explicit `width` and `height` for PNGs based on 48px height + aspect ratio
2. **Links**: Each logo wraps in `<Link href={org.website} target="_blank" rel="noopener noreferrer">`
3. **Accessibility**: `aria-label={org.relationshipDescription}` on each link; section has `aria-label="Partner organizations"`
4. **Grayscale filter**: Apply via Tailwind `grayscale` utility + `hover:grayscale-0` + `transition-all duration-200`
5. **Opacity**: `opacity-60 hover:opacity-100` alongside the grayscale
6. **Group labels**: `<p className="text-xs font-semibold tracking-widest text-muted-foreground uppercase mb-4">`
7. **Marquee animation**: If variant is `"marquee"`, define a `@keyframes` scroll in a `<style>` block or in globals.css

### Section Wrapper

Wrap the `LogoStrip` in a full section when embedding in a page:

```tsx
<section className="w-full py-16 border-y border-border/50" aria-label="Trusted by leading organizations">
  <div className="container mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-xl font-semibold text-foreground">{content.headline}</h2>
      {content.subHeadline && (
        <p className="mt-2 text-sm text-muted-foreground max-w-2xl mx-auto">{content.subHeadline}</p>
      )}
    </div>
    <LogoStrip content={content} variant="grouped" />
    {content.footnote && (
      <p className="mt-8 text-center text-xs text-muted-foreground/60">{content.footnote}</p>
    )}
  </div>
</section>
```

### Tenant Config Variant (if `--tenant` passed)

If the section is being wired to tenant config, add a `socialProof` key to the config:

```typescript
// In src/lib/content/social-proof/{slug}.ts — export the content object
// In a page that uses useTenant() — import and reference
// In tenant.config.ts — optionally add a feature flag: features.socialProof: true
```

---

## Deliverable 4 — Logo Download Checklist

For every logo in the final strip:

1. **Status check**: Is the logo already in `public/images/orgs/`?
   - If yes: verify the filename matches the `logoPath` in the content definition
   - If no: it needs to be downloaded

2. **Download instructions** (per logo that needs downloading):
   - Source URL (from `logo_url` in affiliation JSON)
   - Target path: `public/images/orgs/{id}.{ext}` (use `.svg` for SVGs, `.webp` or `.png` for rasters)
   - Command: `curl -o public/images/orgs/{id}.svg "{logo_url}"`
   - For PNGs: convert to WebP if possible (`cwebp -q 90 {id}.png -o {id}.webp`)

3. **Naming convention for org logos:**
   - `public/images/orgs/{org-id}.svg` — SVG version (preferred)
   - `public/images/orgs/{org-id}.webp` — WebP raster (fallback)
   - `public/images/orgs/{org-id}-dark.svg` — Dark mode variant (if needed)
   - `public/images/orgs/{org-id}-2x.webp` — Retina variant (if PNG is used)

4. **Optimization reminders:**
   - SVGs: run through `svgo` to minimize file size (`npx svgo --input public/images/orgs/`)
   - PNGs/WebP: ensure dimensions are correct for 48px display height (width should be proportional)
   - All images should be < 50KB; logos > 50KB may slow page load

---

## Output Format

Print a summary, then write the files:

```
## Logo Strip: [Person Name]

### Final Strip Selection
N logos selected across M groups

| Group | Label | Logos | Notes |
|-------|-------|-------|-------|
| publishers | "Published by" | Baker, IVP, Zondervan | 3 logos |
| networks | "Part of" | Forge, 5Q, Communitas | 3 logos |
| media | "As featured in" | CT, Relevant, Leadership | 3 logos |
| speaking | "Speaking through" | Premier, Chartwell | 2 logos |

### Copy
**Headline:** "Trusted across the global church"
**Sub-headline:** "Alan's work has been published, taught, and recognized by the world's leading voices in Christian publishing, ministry, and movement building — for over two decades."
**Footnote:** "Logos are trademarks of their respective organizations."

### Files Written
1. `src/lib/content/social-proof/alan-hirsch.ts` — content definition
2. `src/components/social-proof/LogoStrip.tsx` — component
3. Updated `src/components/social-proof/index.ts` — exports

### Logo Download Checklist
Run these commands to download missing logos:
\`\`\`bash
curl -o public/images/orgs/baker-books.svg "https://bakerpublishinggroup.com/logo.svg"
curl -o public/images/orgs/ivp.svg "https://ivpress.com/logo.svg"
# ... etc
\`\`\`

Logos already present locally:
- ✅ public/images/orgs/forge-international.svg
- ✅ public/images/orgs/5q-collective.webp

### Implementation Note
To embed in a page:
\`\`\`tsx
import { LogoStrip } from "@/components/social-proof/LogoStrip"
import { alanHirschSocialProof } from "@/lib/content/social-proof/alan-hirsch"

<LogoStrip content={alanHirschSocialProof} variant="grouped" />
\`\`\`

### Next Steps
1. Run logo download commands above
2. Run \`npx svgo --input public/images/orgs/\` to optimize SVGs
3. Drop \`<LogoStrip>\` into the target page
4. Run \`/design-audit\` on the page after implementation to check visual quality
5. Run \`/asset-brand-check\` if any logos were generated rather than downloaded
```

## Rules

- **Never fabricate affiliations** — only use orgs from the affiliation JSON with HIGH or MEDIUM confidence
- **Grayscale is the standard** — the default state must be grayscale; only override if explicitly asked for full-color
- **Semantic HTML** — use `<section>` with `aria-label`, not `<div>` soup
- **shadcn/ui conventions** — no hardcoded colors; use `text-muted-foreground`, `border-border`, `bg-muted` etc.
- **next/image required** — never use raw `<img>` tags
- **Logo paths must be local** — final implementation must reference `/images/orgs/` paths, not external URLs (prevents hotlinking and load-time variance)
- **Tenant config for tenant strings** — if any text is tenant-specific (the author's name, for example), wire it through tenant config not inline
- **Mobile first** — write responsive classes in mobile-first order (`text-xs md:text-sm`)
- **Performance** — the logo strip must not add more than 200KB of total image weight; flag if the download checklist would exceed this
