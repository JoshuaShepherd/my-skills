---
name: pathway-visualization
description: Generate visualization design briefs for Alan Hirsch pathway pages. Produces detailed specifications for diagrams, charts, and visual models that illustrate each pathway's core framework — suitable for handoff to a designer or asset-generate tool. Understands Alan's existing visual models (U-Shaped curve, mDNA hexagon, APEST pentagon, etc.) and translates them into actionable design briefs.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Generate visualization briefs for: $ARGUMENTS

$ARGUMENTS should include a pathway slug (`reframation`, `metanoia`, `mdna`, `movement-intelligence`, `discipleship`) and optionally a specific model or concept to visualize.

---

## Step 1 — Load Context

1. Read the existing pathway vision doc: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/vision/` — check if visualization briefs already exist
2. Read the pathway's Model section — the visualization should illustrate the named model
3. Read the design charter: `/Users/joshuashepherd/Desktop/Dev/repos/docs/07-design/alan-hirsch-design/DESIGN_CHARTER.md`
4. Read the style guide: `/Users/joshuashepherd/Desktop/Dev/repos/docs/07-design/MOVEMENTAL_STYLE_GUIDE.md`
5. Read the design tokens: `/Users/joshuashepherd/Desktop/Dev/repos/docs/07-design/design-tokens.md`

---

## Step 2 — Alan's Visual Models

Alan Hirsch uses specific visual frameworks throughout his books. The visualization should be a refined digital version of these, not a reinvention.

### Known Visual Models by Pathway

| Pathway | Primary Visual | Source | Shape |
|---------|---------------|--------|-------|
| **Metanoia** | The U-Shaped Curve | *Metanoia* book | U-curve with 7 phases plotted along it. Downcurve (left), floor (center), upcurve (right). Jesus's arc overlaid: incarnation → cross → resurrection |
| **mDNA** | The Six Elements of Apostolic Genius | *The Forgotten Ways* | Hexagonal or circular diagram with Jesus Is Lord at center, six elements radiating outward. Each element connects to adjacent elements. |
| **Reframation** | The Immanent Frame / Open Heaven | *Reframation* | Split diagram: closed ceiling (left, gray) vs. open heaven (right, luminous). Spheres of life beneath both. |
| **Reframation** | The Seven Reframes | *Reframation* | Two-column grid: "Distorted Frame" → "True Frame" for each of 7 reframes |
| **Movement Intelligence** | Movement Multiplication Curve | *On the Verge* | Exponential growth curve showing addition vs. multiplication trajectories |
| **Discipleship** | Life-on-Life Chain | *Untamed*, *Disciplism* | Chain or vine diagram showing person-to-person multiplication |
| **APEST** | The APEST Pentagon | *5Q* | Five-pointed shape with Apostle, Prophet, Evangelist, Shepherd, Teacher at points |

### Cross-Pathway Visuals
- **Christocentric Spine** — vertical axis running through all pathways with "Jesus Is Lord" at center
- **Pathway Map** — overview showing all five pathways and their relationships

---

## Step 3 — Generate Visualization Brief

### Brief Structure (for each visualization)

**1. Title and Purpose**
- What this visualization communicates at a glance
- What question it answers for the viewer
- Where it appears on the page (inline with Model section, standalone card, hero companion)

**2. Type**
- Flow diagram / cycle / matrix / exploded view / timeline / split comparison / curve / network map
- Choose based on the model's logic: sequences → flow/curve, taxonomies → grid/radial, relationships → network

**3. Layout and Shape**
- Precise description of the visual structure
- Number of elements, their arrangement, relationships
- Direction of reading (left-to-right, center-out, top-down, along a curve)
- Symmetry, hierarchy, emphasis

**4. Labels and Text**
- Every text element that appears in the visualization
- Phase/element names
- Any overlay text or callout quotes
- Subtitle or descriptor text

**5. Tone and Palette**
- Emotional quality: contemplative / urgent / luminous / organic / structured
- Color direction: reference Movemental design tokens where possible
- Contrast guidance: what should feel heavy vs. light, closed vs. open
- This is NOT implementation — it's creative direction

**6. Reference**
- Which of Alan's book diagrams this is based on
- Any existing implementations (HTML prototypes, course materials)
- Size/format suggestions: card, full-width, sidebar, hero companion

**7. Accessibility Notes**
- Alt text recommendation (complete enough for screen readers)
- Can the content be understood without the visual? (link to the text equivalent)

---

## Step 4 — Secondary Visualizations

Beyond the primary model diagram, each pathway can benefit from:

**Concept Map** — How this pathway's key terms relate to each other
- Type: network/node diagram
- Nodes = glossary terms, edges = relationships
- Central node = pathway name

**Before/After Frame** — What this pathway changes about perception
- Type: split panel or slider
- Left: the distorted/reduced view
- Right: the recovered/reframed view
- Powerful for Reframation, Metanoia, and mDNA

**Timeline** — Historical examples on a timeline
- Type: horizontal timeline
- Nodes = case studies plotted by date
- Shows the concept appearing across centuries

---

## Step 5 — Voice (Design Briefs)

Design briefs are written for designers, not readers. The voice is:
- **Clear and specific** — no ambiguity about what's needed
- **Visually descriptive** — "organic line weight, not sharp geometry," "luminous, not clinical"
- **Grounded in content** — every visual element traces to an actual concept or framework
- **Brand-aware** — reference Movemental design system where applicable

### Anti-Patterns for Visualization Briefs
- Never describe a visualization without knowing the underlying model — read the Model section first
- Never use generic stock-visual language ("an inspirational image of people together")
- Never propose a visualization that contradicts Alan's actual model structure
- Never forget accessibility — every visualization needs a text equivalent

---

## Output

```
---
pathway: [slug]
section: visualizations
viz_count: [number]
model_reference: [which Alan Hirsch model this illustrates]
---

## Visualizations: [Pathway Name]

### Visualization 1: [Title]

**Purpose:** [What it communicates at a glance]
**Type:** [diagram type]
**Source model:** [Alan's book/framework reference]

**Layout:**
[Precise description of visual structure — 100–200 words]

**Labels:**
[Every text element]

**Tone:**
[Emotional quality and color direction — 50–100 words]

**Accessibility:**
Alt text: "[Complete description for screen readers]"

---

### Visualization 2: [Title]

[Same structure]
```

Save to: `/Users/joshuashepherd/Desktop/Dev/repos/docs/pathways/[slug]/visualizations.md`
