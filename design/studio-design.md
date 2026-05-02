
Generate an AI Studio design prompt for: $ARGUMENTS

$ARGUMENTS should include:
- What you want to build (e.g., "a course detail page", "a fintech dashboard", "a spa landing page", "a dark mode portfolio")
- Optionally: mood/vibe hints ("warm and scholarly", "bold and techy", "luxury minimal")
- Optionally: specific constraints ("must have pricing table", "needs hero with video embed")
- Empty — ask the user what they want to build

## Purpose

This skill produces a **complete design prompt** ready to paste into Google AI Studio Build mode (or any generative UI tool). The prompt describes the *experience, mood, structure, and interaction design* using evocative language that gives the AI enough direction to make beautiful design decisions without over-constraining the output.

**This is the design complement to `/studio-export`** — that skill gives AI Studio the data model and business rules; this skill gives it the visual design brief.

**Include:** Layout patterns, visual mood, color direction, typography personality, animation intent, anti-patterns to avoid, accessibility requirements, responsive expectations, reference inspirations.

**Exclude:** Exact hex codes (use color moods instead), pixel-perfect measurements, specific component implementations, database schemas, API contracts.

## Elicitation — Before Generating

If the user's request is vague, ask **up to 3 targeted questions** to get clarity. Pick from:

1. **What is this?** — Page type, product category, who uses it
2. **What's the vibe?** — Warm/cool, playful/serious, minimal/rich, light/dark
3. **What's the hero moment?** — The single most important thing the user should see/feel/do

Do NOT ask all three if the request already provides enough context. If the user gives a clear brief, skip straight to generation.

## The 5-Dimension Design Brief

Structure the AI Studio prompt around these five dimensions. For each dimension, use **evocative, directional language** — not prescriptive specs. The goal is to paint a picture that lets the AI make the call on execution.

### Dimension 1: Pattern & Layout (The Skeleton)

Choose the structural pattern based on what's being built. Draw from these proven patterns:

**Page-Level Patterns:**
- **Hero-Centric** — Full-bleed hero dominates, content cascades below. Best for: landing pages, product launches, course detail pages.
- **Content Hub** — Search/filter bar up top, card grid below, sidebar categories. Best for: libraries, article listings, resource directories.
- **Split Composition** — Two-column: copy on one side, visual on the other. Alternating sections. Best for: feature showcases, about pages, comparison layouts.
- **Bento Grid** — Modular card system with varying sizes. Information-dense but scannable. Best for: dashboards, feature overviews, portfolio showcases.
- **Storytelling Scroll** — Full-width sections that unfold a narrative as you scroll. Each section is a chapter. Best for: case studies, long-form landing pages, annual reports.
- **Compact Utility** — Dense, functional, minimal chrome. Every pixel earns its place. Best for: tools, editors, settings, admin panels.
- **Immersive Gallery** — Large imagery dominates. Minimal UI. Content speaks through visuals. Best for: photography, luxury products, creative portfolios.
- **Dashboard Shell** — Fixed sidebar + header, scrollable main area, card-based widgets. Best for: analytics, admin, user dashboards.

**Section-Level Patterns:**
- **Cinematic Hero** — Full viewport, background image/video, overlay text, dual CTA. Dramatic entrance.
- **Card Grid** — 2-4 columns of cards, consistent sizing, hover states. The workhorse.
- **Testimonial/Social Proof** — Quotes, avatars, star ratings. Carousel or staggered grid.
- **Pricing Table** — 2-4 tier columns, feature comparison, highlighted recommended tier.
- **Feature Showcase** — Icon + heading + description blocks. 3-column or alternating left/right.
- **Stats/Metrics Band** — Full-width strip with 3-5 key numbers. High contrast.
- **CTA Section** — Centered, focused, single action. Often dark/contrasting background.
- **FAQ Accordion** — Expandable questions. Clean, scannable.
- **Timeline/Steps** — Numbered or connected progression. Vertical or horizontal.
- **Sticky Navigation** — Tab bar or sidebar that follows scroll. Anchors to sections.

**Hero Variants** (from the template library):
- Compact (50vh, quick entry)
- Cinematic (100vh, dual CTA, dramatic)
- Two-Column (copy + image side by side)
- Minimal (text-only, dark, CMS-friendly)
- Title Strip (breadcrumb + H1, subpage header)
- Split (50/50 image-copy)
- Banner (short, centered headline)
- Card Overlay (full-bleed + floating card)
- Bottom Strip (image + dark band below)
- Asymmetric (40% image, 60% copy)

### Dimension 2: Style & Aesthetic (The Skin)

Describe the visual personality. Use one or more of these style directions as anchors:

| Style | Keywords | Best For |
|-------|----------|----------|
| **Glassmorphism** | Frosted glass, translucent layers, depth, vibrant backdrop | Dashboards, modals, modern apps |
| **Aurora UI** | Vibrant gradients, mesh, Northern Lights, luminous | Landing pages, hero sections, creative |
| **Soft UI / Neumorphism 2.0** | Soft shadows, subtle depth, tactile, monochromatic | Wellness, health, minimalist apps |
| **Linear/Vercel Aesthetic** | Dark mode, subtle borders, high contrast, developer-centric | Dev tools, SaaS, technical products |
| **Bento Grid** | Modular, clean, organized, information-dense | Dashboards, feature showcases |
| **Liquid Glass** | Fluid shapes, organic movement, glossy, dynamic | Creative agencies, interactive experiences |
| **Brutalism** | Raw, bold, unconventional, high-contrast, geometric | Art, experimental, bold brands |
| **Y2K Revival** | Metallic, chrome, retro-futuristic, bold colors | Entertainment, nostalgia, fashion |
| **Claymorphism** | 3D inflated, soft shadows, playful, tactile | Consumer apps, playful brands |
| **Gradient Mesh** | Complex multi-color gradients, organic flow | Backgrounds, hero sections |
| **Minimalist Luxury** | Maximum white space, serif typography, subtle gold | Fashion, premium services, editorial |
| **Cyberpunk** | Neon, glitch effects, tech-noir, high energy | Gaming, nightlife, edgy tech |
| **Organic/Biomorphic** | Nature-inspired shapes, earth tones, flowing forms | Wellness, sustainability, food |
| **Editorial** | Magazine-style, strong typographic hierarchy, clean columns | Blogs, news, publishing, content |
| **Scandinavian Minimal** | Warm white space, natural materials palette, functional beauty | Lifestyle, furniture, home |
| **Art Deco** | Geometric symmetry, gold accents, ornate borders, opulence | Hotels, events, luxury dining |
| **Hand-Drawn / Sketch** | Imperfect lines, illustration-style, personal, warm | Education, children, personal brands |
| **Retro Terminal** | Monospace, green-on-black, CRT glow, command-line | Dev portfolios, hacker tools, nostalgia |
| **Vaporwave** | Pink/purple/teal, glitch, 80s nostalgia, dreamy | Music, art, cultural commentary |
| **Swiss/International** | Grid-based, Helvetica, objective clarity, functional | Corporate, institutional, data-heavy |
| **Warm Academic** | Rich wood tones, scholarly textures, inviting depth, bookish | Education, theology, thought leadership |

When writing the prompt, don't just name the style — **describe what it feels like** to use the interface:
- "The page should feel like stepping into a well-lit bookshop at golden hour"
- "Navigation should feel weightless — elements floating on frosted glass"
- "The dashboard should feel like mission control: dense but calm, every widget purposeful"

### Dimension 3: Color & Theme (The Palette)

Direct color through **mood and psychology**, not hex codes. Let the AI choose the exact palette.

**Color Moods:**
- **Trust & Authority** — Deep navy, reliable blue, clean grey. Established, secure.
- **Vibrant & Modern** — Indigo, emerald accents, white space. Forward-thinking, energetic.
- **Luxury & Premium** — Warm blacks, gold accents, cream. Sophisticated, exclusive.
- **Healthcare / Wellness** — Cyan, health green, clean white. Calm, trustworthy.
- **Creative & Playful** — Pink, purple, warm cream, orange accents. Fun, approachable.
- **Warm & Scholarly** — Amber, terracotta, sage, cream, warm charcoal. Inviting, intellectual.
- **Dark Mode Excellence** — True black base, subtle card surfaces, bright accent. Dramatic, focused.
- **Earth & Nature** — Forest green, warm brown, sand, moss. Grounded, organic.
- **Sunset / Golden Hour** — Warm oranges, soft pinks, deep purple horizons. Emotional, aspirational.
- **Monochromatic Drama** — Single hue across full tonal range. Confident, cohesive.
- **High Contrast Editorial** — Near-black type on near-white. Bold color used only as punctuation.

**Color Principles to include:**
- 60-30-10 rule (dominant, secondary, accent)
- WCAG AA compliance (4.5:1 text contrast minimum)
- Light and dark mode considerations if relevant
- Never pure black on pure white (too harsh)

### Dimension 4: Typography (The Voice)

Describe the **personality** of the type, not the font name. Let the AI pick fonts that match.

**Typography Moods:**
- **Clean & Scalable** — Geometric sans-serif, engineered for screens. Tech, SaaS, tools.
- **Elegant & Editorial** — High-contrast serif for headlines, clean sans for body. Fashion, luxury, publishing.
- **Friendly & Approachable** — Rounded, slightly warm, generous x-height. Consumer apps, education.
- **Bold & Unconventional** — Heavy display type, tight spacing, raw. Creative agencies, art.
- **Scholarly & Trustworthy** — Traditional serif with modern sensibility. Education, theology, research.
- **Monospace & Technical** — Code-font energy, precise, developer. Dev tools, data, terminals.

**Type Hierarchy Guidance:**
- Headlines should stop you mid-scroll
- Subheadings provide the bridge between scanning and reading
- Body text should be effortlessly readable (16px+ base, 1.5+ line height)
- No more than 2 font families per page
- No more than 3-4 distinct sizes in a single view

### Dimension 5: Animation & Interaction (The Soul)

Describe **how the page should feel in motion** — not CSS keyframes.

**Entrance & Reveal:**
- "Content should fade up gently as it enters the viewport, each element a beat behind the last — like a conversation unfolding"
- "The hero should feel like a curtain rising — background first, then headline, then CTA"
- "Cards should stagger in like a deck being dealt"

**Hover & Interaction:**
- "Cards should lift slightly on hover, casting a deeper shadow — a subtle invitation"
- "Buttons should feel pressable — a gentle scale-down on click, spring-back on release"
- "Navigation items should have a quiet underline that slides in from the left"

**Scroll & Motion:**
- "Parallax should be subtle — barely noticeable — like looking out a train window"
- "Progress should be visible: a thin bar at the top growing as you scroll"
- "Sections should have breathing room — the page should never feel rushed"

**Loading & Transitions:**
- "Skeleton loaders that shimmer, matching the final content shapes"
- "Page transitions that feel like turning a page, not teleporting"
- "Nothing should ever pop in — everything arrives with intention"

**Rules to always include:**
- Respect `prefers-reduced-motion` — provide a graceful static fallback
- Keep interaction animations under 300ms
- Keep ambient animations slow and gentle (4s+)
- Only animate `transform` and `opacity` for performance
- No more than 3-4 simultaneous animations
- Nothing should autoplay with sound

## Anti-Patterns — Always Include

Every prompt should include a "What to Avoid" section. Select the relevant anti-patterns:

**Design:**
- No more than 3 primary colors
- No more than 2 font families
- No inconsistent spacing (use an 8px grid)
- No pure black on pure white
- No low-contrast grey text
- No unoptimized images

**UX:**
- No hamburger menus on desktop
- No hover-dependent interactions on mobile
- No auto-playing carousels
- No hidden navigation without clear affordance
- Minimum 44x44px tap targets
- No layout shifts on load

**Content:**
- No lorem ipsum — use realistic placeholder content
- No walls of text without hierarchy
- No "click here" links
- Icons must have labels or tooltips

**Accessibility:**
- WCAG AA compliance minimum
- Keyboard navigation must work
- Focus states must be visible
- Color alone must not convey information
- Screen reader support for all interactive elements

## Responsive Expectations

Always include responsive guidance:
- **Desktop** (1440px+): Full layout, all features visible
- **Tablet** (768px): Graceful column collapse, touch-friendly
- **Mobile** (375px): Single column, thumb-zone navigation, no horizontal scroll
- Images should be responsive and lazy-loaded
- Typography should scale fluidly

## Reference Anchors

When relevant, reference real-world design inspirations using evocative descriptions:
- "The density of a Linear dashboard but with warmer tones"
- "The editorial elegance of a Monocle magazine spread"
- "The immersive scroll of an Apple product page"
- "The calm utility of a Notion workspace"
- "The bold typography of a Pentagram case study"
- "The glass-layer depth of iOS Control Center"

Do NOT link to URLs — describe the *quality* you're referencing.

## Combining with /studio-export

If the user has already generated a `/studio-export` for the same feature, mention it in the prompt:
- "This design prompt pairs with a separate data specification (feature constitution) that defines all data models, API contracts, and business rules. This prompt focuses exclusively on the visual and interaction design."

## Output Format

Generate a single markdown document structured as:

```markdown
# AI Studio Design Brief: [Feature Name]

## What We're Building
[1-2 sentence description of the page/feature and its purpose]

## The Experience
[2-3 sentences describing what it should FEEL like to use this. Emotional, evocative.]

## Layout & Structure
[Pattern selection with description of how sections flow]

## Visual Style
[Style direction with experiential language — what does it feel like?]

## Color Direction
[Color mood with emotional rationale]

## Typography
[Type personality description]

## Motion & Interaction
[Animation intent in natural language]

## What to Avoid
[Selected anti-patterns relevant to this build]

## Responsive Behavior
[How it adapts across breakpoints]

## Reference Inspirations
[2-4 evocative quality references]

