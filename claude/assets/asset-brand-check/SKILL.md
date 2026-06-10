---
name: asset-brand-check
description: Audit generated image assets against the platform's brand guidelines. Use before publishing to verify color palette, typography, tone, and visual consistency.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Audit image assets against brand guidelines: $ARGUMENTS

$ARGUMENTS should include:
- Path(s) to the image(s) to audit (file or directory)
- Optionally: specific brand concerns to check
- Optionally: the intended use context (hero, OG card, course cover, etc.)
- Empty — ask the user for the image path

## Before Starting

1. Read `src/lib/config/tenant.config.ts` to understand brand identity
2. Read `src/app/globals.css` to understand the design token palette
3. Read `tailwind.config.ts` for font and color configuration
4. Load the image(s) to audit

## Brand Guidelines — Alan Hirsch Platform

### Color Palette

#### Approved Colors
| Role | Token | Hex Range | Description |
|------|-------|-----------|-------------|
| Primary | `--primary` | Warm amber/gold tones | CTAs, accents, highlights |
| Background | `--background` | Cream to warm white | Page backgrounds |
| Foreground | `--foreground` | Warm charcoal to dark brown | Text, headings |
| Muted | `--muted` | Warm grey, sage undertones | Secondary text, borders |
| Card | `--card` | Cream, warm white | Card surfaces |
| Accent | `--accent` | Terracotta, warm amber | Badges, highlights |

#### Color Affinities (preferred in generated images)
- Terracotta: `#C75B39` range
- Amber/Gold: `#D4A84B` range
- Sage: `#87A878` range
- Cream: `#FAF5E4` range
- Warm Charcoal: `#2C2C2C` to `#3D3D3D`
- Warm Grey: `#8B8680` range

#### Color Violations (flag these)
- ❌ Pure black (#000000) backgrounds
- ❌ Cold/corporate blues (#0066CC, #1a73e8)
- ❌ Neon or high-saturation colors
- ❌ Pure white (#FFFFFF) as dominant background (should be warm cream)
- ❌ Cool greys without warm undertones
- ❌ Gradient rainbow / multi-colored effects

### Tone & Mood

#### Approved Qualities
- ✅ Warm, inviting, relational
- ✅ Scholarly but accessible
- ✅ Missional, communal, formational
- ✅ Grounded, authentic, practical
- ✅ Contemplative, thoughtful depth

#### Tone Violations (flag these)
- ❌ Corporate, sterile, clinical
- ❌ Stock-photo generic (perfectly posed business people)
- ❌ Overly polished / artificial perfection
- ❌ Dark, edgy, aggressive
- ❌ Playful / cartoonish (unless specifically for a casual context)
- ❌ Tech-bro / startup aesthetic

### Typography in Images

#### Approved Styles
- Serif fonts for titles/quotes (Playfair Display, Merriweather family)
- Clean sans-serif for body/labels (Inter, Open Sans family)
- Condensed sans-serif for impact (Oswald family)

#### Typography Violations
- ❌ Comic Sans, papyrus, or novelty fonts
- ❌ All-caps body text (all-caps OK for short labels/badges)
- ❌ Text with insufficient contrast (< 4.5:1 ratio)
- ❌ Text without clear hierarchy (all same size/weight)
- ❌ Decorative/script fonts for body text

### Visual Motifs

#### On-Brand Motifs
- Open books, journals, handwritten notes
- Community gatherings, small groups, circles
- Urban neighborhoods, streets, doorways
- Maps, pathways, compass imagery
- Natural textures: wood, linen, paper, stone
- Shared meals, bread, table settings
- Seeds, seedlings, growth imagery

#### Off-Brand Motifs
- ❌ Corporate offices, boardrooms
- ❌ Solo individuals on pedestals/stages (unless teaching context)
- ❌ Technology/screens as the central subject
- ❌ Military/conquest imagery
- ❌ Luxury/wealth signaling

## Audit Checklist

For each image, evaluate against these dimensions:

### 1. Color Palette Alignment (Weight: HIGH)
- [ ] Dominant colors match brand palette (warm earth tones)
- [ ] No cold/corporate colors dominating
- [ ] No neon or oversaturated elements
- [ ] Dark mode assets use warm darks, not pure black

### 2. Tone & Mood (Weight: HIGH)
- [ ] Feels warm and inviting
- [ ] Scholarly but not cold
- [ ] Communal/relational, not individualistic
- [ ] Authentic, not stock-photo generic

### 3. Typography (Weight: MEDIUM — only if text present)
- [ ] Font styles match brand family
- [ ] Text hierarchy is clear
- [ ] Contrast meets WCAG AA (4.5:1)
- [ ] No novelty or inappropriate fonts

### 4. Composition & Quality (Weight: MEDIUM)
- [ ] Appropriate aspect ratio for intended use
- [ ] No AI artifacts (extra fingers, distorted text, etc.)
- [ ] Resolution sufficient for intended display size
- [ ] Composition supports content placement (negative space for text overlays)

### 5. Visual Motifs (Weight: LOW)
- [ ] Imagery aligns with brand motifs
- [ ] No off-brand subject matter
- [ ] Cultural sensitivity appropriate

## Execution

### Step 1 — Load Images
Read each image file using the Read tool (supports PNG, JPG, WebP).

### Step 2 — Visual Analysis
For each image, analyze against all 5 dimensions. Use your multimodal understanding to assess:
- Dominant colors and their warmth/coolness
- Overall mood and tone
- Text legibility and style (if present)
- Composition quality
- Subject matter appropriateness

### Step 3 — Score and Report

## Output Format

```
## Brand Audit Report

### Image: public/images/generated/hero/forgotten-ways.png
### Intended Use: Hero image for course detail page

### Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| Color Palette | 9/10 | ✅ Pass |
| Tone & Mood | 8/10 | ✅ Pass |
| Typography | 7/10 | ⚠️ Minor issues |
| Composition | 9/10 | ✅ Pass |
| Visual Motifs | 10/10 | ✅ Pass |

### Overall: ✅ APPROVED (43/50)

### Details

#### Color Palette (9/10) ✅
- Dominant warm amber and terracotta tones — on brand
- Background gradient uses cream to warm gold — excellent
- Minor: small area of slightly cool grey in shadow region

#### Tone & Mood (8/10) ✅
- Warm, scholarly feel — matches brand
- Community gathering scene feels authentic
- Minor: lighting slightly dramatic for a platform that values accessibility

#### Typography (7/10) ⚠️
- Title text uses appropriate serif font
- Subtitle contrast is borderline (estimated 3.8:1) — recommend darkening text or adding overlay
- ACTION: Increase subtitle text contrast

#### Composition (9/10) ✅
- Good negative space for text overlay on the right
- Subject placement follows rule of thirds
- Resolution sufficient for hero display (2048px)

#### Visual Motifs (10/10) ✅
- Small group gathered around a table — perfect brand alignment
- Books and journals visible — on-brand scholarly motif
- Natural lighting through windows — warm, authentic

### Recommended Refinements
1. **Increase subtitle contrast** — darken text or add semi-transparent overlay
   → Use `/asset-edit` with: "Darken the subtitle text to improve contrast against the background"
2. **Slightly warm the shadow areas** — shift cool grey shadows toward warm grey
   → Use `/asset-edit` with: "Warm up the shadow areas, shifting from cool grey toward warm brown-grey"

### Verdict
Image is ready for use with minor text contrast adjustment recommended.
```

## Batch Audit

When auditing a directory of images (e.g., a full series), provide:
1. Individual audit for each image
2. Cross-image consistency check:
   - Are all images using the same color palette?
   - Is the lighting direction consistent?
   - Is the composition template consistent?
   - Are there outliers that break the visual rhythm?
3. Summary table with pass/fail for each image

## Scoring Guide

| Score | Status | Meaning |
|-------|--------|---------|
| 9-10 | ✅ Pass | On-brand, ready for production |
| 7-8 | ⚠️ Minor | Usable with minor refinements recommended |
| 5-6 | 🔶 Moderate | Needs refinement before publishing |
| 1-4 | ❌ Fail | Off-brand, regenerate or major edit needed |

Threshold for approval: 35/50 overall, with no single dimension below 5/10.
