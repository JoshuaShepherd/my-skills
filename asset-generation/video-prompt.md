
Generate AI video prompts: $ARGUMENTS

$ARGUMENTS should include:
- Description of the video concept (transition, reveal, transformation, loop)
- Optionally: start frame image path (to use as reference)
- Optionally: end frame image path
- Optionally: target video model (runway, kling, pika, higgsfield)
- Optionally: duration, aspect ratio
- Empty — ask the user for the concept

## Before Starting

1. Read `{{CONFIG_PATH}}` for brand context
2. If start/end frame images exist, read them for visual reference
3. Determine the video type from the categories below

## Video Types

### 1. Product Reveal / Deconstruction
Object assembles or disassembles — scroll-stop format.
- Start: assembled product on clean background
- End: exploded view with all components floating
- Or reverse: parts → assembled (equally compelling)

### 2. Transformation / Before-After
Scene or subject transforms between two states.
- Start: one state (e.g., empty room, closed book, bare landscape)
- End: transformed state (e.g., community gathering, open book with light, flourishing garden)

### 3. Parallax / Depth Reveal
Camera moves through layers of a scene, revealing depth.
- Static 2.5D image brought to life with subtle camera motion
- Great for hero sections, course intros

### 4. Zoom / Scale Transition
Macro to micro or micro to macro journey.
- Start: wide establishing shot
- End: extreme close-up detail (or reverse)

### 5. Loop / Cinemagraph
Seamless looping motion — a single element moves while the rest is still.
- Flickering candle, turning pages, flowing water, breathing animation
- Perfect for website hero backgrounds

### 6. Kinetic Typography
Text animates into frame with cinematic motion.
- Words reveal, assemble, or transform
- Great for course trailers, social clips

### 7. Narrative Sequence
Multi-scene storyboard — 2-4 connected shots telling a micro-story.
- Each scene described with transitions between them

## Prompt Structure

Every video prompt has 5 sections. Write each explicitly for the target video model.

### SECTION 1 — Start Frame
```
START FRAME:
[Detailed description of the opening image — subject, composition, lighting, colors, mood.
Include camera position, lens, and DOF if photorealistic.]
```

### SECTION 2 — End Frame
```
END FRAME:
[Detailed description of the final image — what has changed, what remains constant.
Explicitly state what is DIFFERENT and what is the SAME as the start frame.]
```

### SECTION 3 — Transition Choreography
```
TRANSITION:
[Describe the motion step by step. Include:
- What moves first, second, third (sequencing)
- Speed and easing (slow-in, slow-out, constant, accelerating)
- Direction of motion (up, down, outward, inward, along axis)
- Any rotations or reveals
- Timing: when each motion starts and ends relative to total duration
- What does NOT move (critical for stability)]
```

### SECTION 4 — Style & Constraints
```
STYLE:
- Photorealistic / Cinematic / Illustrated / Abstract
- Lighting: consistent throughout, no flickering
- Camera: locked tripod / slow dolly / orbit / handheld
- Background: pure white / environmental / gradient
- Color: [palette description]
- Quality: high fidelity, smooth motion, no artifacts
```

### SECTION 5 — Technical Specs
```
SPECS:
- Duration: [4-10 seconds]
- Aspect ratio: [16:9 / 9:16 / 1:1]
- Frame rate: [24fps / 30fps / 60fps]
- Resolution: [1080p / 4K]
```

## Brand-Aligned Video Concepts for {{BRAND_NAME}} Platform

### Course Trailer Concepts
- **Book opening**: A closed book slowly opens, pages fan, text illuminates — camera pushes in
- **Community forming**: Empty chairs in a circle → people arriving, settling in, conversation beginning
- **Seed to tree**: Time-lapse of a seed breaking soil, growing into a spreading tree (formation metaphor)
- **Map unfolding**: A folded map opens and spreads across a wooden table, routes illuminating

### Social Content Concepts
- **Quote reveal**: Warm paper texture, words write themselves in ink — serif typography
- **Scroll-stop deconstruction**: Book or journal explodes into floating pages, binding, cover
- **Candle cinemagraph**: Warm scene with a single flickering candle — loopable hero

### Hero Section Concepts
- **Parallax neighborhood**: Layers of a community street scene with subtle depth motion
- **Breathing texture**: Warm linen or paper texture with barely perceptible motion — alive but calm
- **Golden hour shift**: Subtle lighting shift from morning to golden hour across a static scene

## Model-Specific Tips

### Runway Gen-3/Gen-4
- Upload start and end frames as "First Frame" and "Last Frame"
- Keep prompt under 300 words for best results
- Specify camera motion explicitly: "locked tripod, no camera movement"
- Duration: 4-10 seconds
- Use "cinematic, smooth, high quality" as quality markers

### Kling
- Supports longer durations (up to 15 seconds)
- Strong at character consistency
- Prompt in clear, sequential sentences
- Add "no sudden movements, smooth transitions" for stability

### Pika
- Best for stylized/illustrated looks
- Shorter durations (3-5 seconds) produce better quality
- Good at text animation
- Use "consistent lighting, no flickering" explicitly

### Higgsfield
- Excels at product/object animations
- Upload reference images for best consistency
- Strong at physics-based motion (floating, falling, assembling)

## Execution

### Step 1 — Define the Concept
Work with the user to nail down:
- What type of video (from categories above)?
- What's the subject?
- What's the start state and end state?
- What's the intended use (social, hero, course trailer)?

### Step 2 — Generate Start/End Frame Prompts
If the user doesn't have start/end images yet, generate Gemini image prompts first:
- Use `/asset-generate` or `/asset-product-shot` for the start frame
- Use `/asset-generate` or `/asset-exploded-view` for the end frame
- Ensure both use identical lighting, camera angle, and palette

### Step 3 — Write the Video Prompt
Compose the full 5-section video prompt. Show to user for approval.

### Step 4 — Generate Variants
Offer 2-3 variants:
1. **Standard**: As described (e.g., 5 seconds, forward)
2. **Reverse**: End → Start (assembly instead of deconstruction)
3. **Loop**: Forward → Reverse seamlessly (for website backgrounds)

### Step 5 — Deliver
Present all prompts in chat. If the user wants a polished delivery page, suggest `/asset-deliver`.

## Output Format

```
## Video Prompt Set: [CONCEPT NAME]

### Concept
[1-2 sentence description of the video]

### Use Case
[Where this will be used — social, hero section, course trailer, etc.]


### END FRAME PROMPT
[For image generation — paste into Gemini/Midjourney/etc.]

{end frame prompt}


### VARIANT — Reverse Assembly
{reverse version}

### VARIANT — Seamless Loop
{loop version}

