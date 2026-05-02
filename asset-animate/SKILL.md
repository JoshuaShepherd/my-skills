---
name: asset-animate
description: Create micro-animations from still images — parallax, Ken Burns, floating particles, breathing effects, cinemagraphs. Generates CSS animations, GSAP code, or short video/GIF from a static image. Use for hero backgrounds, social posts, and subtle motion design.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Animate a still image: $ARGUMENTS

$ARGUMENTS should include:
- Path to the source image
- Animation type (parallax, ken-burns, cinemagraph, breathing, particles, float)
- Optionally: target format (css, gsap, mp4, gif, webm)
- Optionally: duration, loop behavior
- Empty — ask the user for the image and animation type

## Before Starting

1. Read the source image to understand its content, composition, and what elements could move
2. Read `src/app/globals.css` for existing animation tokens
3. Check if GSAP is available (`pnpm list gsap`)
4. Determine the animation type and output format

## Animation Types

### 1. Ken Burns — Slow Pan & Zoom
Subtle, cinematic pan and zoom across a still image. Classic documentary technique.
- Movement: Slow zoom in (105-115% over 8-15 seconds) with gentle drift
- Best for: Hero backgrounds, course headers, book cover presentations
- Output: CSS animation or GSAP timeline

```css
/* Ken Burns CSS */
@keyframes ken-burns {
  0% {
    transform: scale(1) translate(0, 0);
  }
  100% {
    transform: scale(1.12) translate(-2%, -1%);
  }
}

.ken-burns-container {
  overflow: hidden;
  position: relative;
}

.ken-burns-image {
  animation: ken-burns 15s ease-in-out infinite alternate;
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .ken-burns-image {
    animation: none;
  }
}
```

```typescript
// Ken Burns GSAP
import gsap from "gsap";

function kenBurns(element: HTMLElement, duration = 15) {
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.to(element, {
      scale: 1.12,
      x: "-2%",
      y: "-1%",
      duration,
      ease: "sine.inOut",
      repeat: -1,
      yoyo: true,
    });
  });
}
```

### 2. Parallax Layers — Depth from a Flat Image
Split a still image into foreground/midground/background layers that move at different
speeds on scroll or mouse movement. Creates a subtle 3D effect.

```typescript
// Parallax GSAP with ScrollTrigger
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function parallaxLayers(container: HTMLElement) {
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    // Background layer — slowest
    gsap.to(container.querySelector(".parallax-bg"), {
      y: "-10%",
      ease: "none",
      scrollTrigger: {
        trigger: container,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });

    // Midground layer — medium speed
    gsap.to(container.querySelector(".parallax-mid"), {
      y: "-20%",
      ease: "none",
      scrollTrigger: {
        trigger: container,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });

    // Foreground layer — fastest
    gsap.to(container.querySelector(".parallax-fg"), {
      y: "-30%",
      ease: "none",
      scrollTrigger: {
        trigger: container,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });
  });
}
```

**Layer separation**: Use NB2 to generate depth-separated layers from a single image:
```
Given this image, generate 3 separate layers for parallax animation:
1. Background layer: just the distant/background elements on a transparent background
2. Midground layer: the main subject/mid-distance elements on a transparent background
3. Foreground layer: any near-camera elements on a transparent background
```

### 3. Breathing / Pulse — Subtle Life
Barely perceptible scale oscillation that makes a static image feel alive.
Like a resting heartbeat — calming, warm.

```css
/* Breathing CSS */
@keyframes breathe {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.015);
  }
}

.breathing-image {
  animation: breathe 6s ease-in-out infinite;
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .breathing-image {
    animation: none;
  }
}
```

```typescript
// Breathing GSAP
gsap.to(element, {
  scale: 1.015,
  duration: 3,
  ease: "sine.inOut",
  repeat: -1,
  yoyo: true,
});
```

### 4. Float / Hover — Gentle Levitation
Element gently floats up and down, as if suspended. Great for cards, icons,
decorative elements.

```css
/* Float CSS */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.floating-element {
  animation: float 4s ease-in-out infinite;
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .floating-element {
    animation: none;
  }
}
```

### 5. Particles — Ambient Floating Specks
Subtle particles (dust, embers, bokeh circles) floating across or around an image.
Adds atmosphere without distraction.

```typescript
// Particle system using Canvas overlay
function createParticles(
  canvas: HTMLCanvasElement,
  options: {
    count?: number;
    color?: string;
    minSize?: number;
    maxSize?: number;
    speed?: number;
    opacity?: number;
  } = {}
) {
  const {
    count = 30,
    color = "#D4A84B",
    minSize = 1,
    maxSize = 3,
    speed = 0.3,
    opacity = 0.4,
  } = options;

  const ctx = canvas.getContext("2d")!;
  canvas.width = canvas.offsetWidth * window.devicePixelRatio;
  canvas.height = canvas.offsetHeight * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  const particles = Array.from({ length: count }, () => ({
    x: Math.random() * canvas.offsetWidth,
    y: Math.random() * canvas.offsetHeight,
    size: Math.random() * (maxSize - minSize) + minSize,
    speedX: (Math.random() - 0.5) * speed,
    speedY: (Math.random() - 0.5) * speed * 0.5,
    opacity: Math.random() * opacity,
    pulse: Math.random() * Math.PI * 2,
  }));

  // Respect reduced motion
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  if (prefersReducedMotion) return;

  function animate() {
    ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);

    for (const p of particles) {
      p.x += p.speedX;
      p.y += p.speedY;
      p.pulse += 0.02;

      // Wrap around edges
      if (p.x < -10) p.x = canvas.offsetWidth + 10;
      if (p.x > canvas.offsetWidth + 10) p.x = -10;
      if (p.y < -10) p.y = canvas.offsetHeight + 10;
      if (p.y > canvas.offsetHeight + 10) p.y = -10;

      const currentOpacity = p.opacity * (0.5 + 0.5 * Math.sin(p.pulse));

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.globalAlpha = currentOpacity;
      ctx.fill();
    }

    requestAnimationFrame(animate);
  }

  animate();
}
```

### 6. Cinemagraph — Isolated Motion
Most of the image is still, but one element moves (flickering candle, turning pages,
flowing water, waving flag). This requires generating a short video loop.

**Use NB2 + Video Model approach:**
1. Generate the still image with `/asset-generate`
2. Create a video prompt with `/asset-video-prompt` describing the isolated motion
3. The video prompt should emphasize: "Only [ELEMENT] moves. Everything else is completely still."

**Alternative — CSS approach for simple cinemagraph effects:**
```css
/* Cinemagraph-like effect: overlay a looping video of just the moving element */
.cinemagraph-container {
  position: relative;
  overflow: hidden;
}

.cinemagraph-still {
  width: 100%;
  height: auto;
}

.cinemagraph-motion {
  position: absolute;
  /* positioned exactly over the moving element */
  top: var(--motion-top);
  left: var(--motion-left);
  width: var(--motion-width);
  height: var(--motion-height);
  /* mask to blend edges */
  mask-image: radial-gradient(ellipse, black 60%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse, black 60%, transparent 100%);
}
```

## Integration with React Components

### Creating an Animated Hero Component

```tsx
"use client";

import { useRef, useEffect } from "react";
import Image from "next/image";
import gsap from "gsap";

interface AnimatedHeroProps {
  src: string;
  alt: string;
  animation: "ken-burns" | "breathing" | "parallax";
  children?: React.ReactNode;
}

export function AnimatedHero({ src, alt, animation, children }: AnimatedHeroProps) {
  const imageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!imageRef.current) return;
    const mm = gsap.matchMedia();

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      const el = imageRef.current!.querySelector("img");
      if (!el) return;

      switch (animation) {
        case "ken-burns":
          gsap.to(el, {
            scale: 1.12,
            x: "-2%",
            y: "-1%",
            duration: 15,
            ease: "sine.inOut",
            repeat: -1,
            yoyo: true,
          });
          break;
        case "breathing":
          gsap.to(el, {
            scale: 1.015,
            duration: 3,
            ease: "sine.inOut",
            repeat: -1,
            yoyo: true,
          });
          break;
      }
    });

    return () => mm.revert();
  }, [animation]);

  return (
    <div ref={imageRef} className="relative overflow-hidden">
      <Image
        src={src}
        alt={alt}
        fill
        className="object-cover"
        priority
      />
      {children && (
        <div className="relative z-10">{children}</div>
      )}
    </div>
  );
}
```

## Output Formats

| Format | Tool | Use Case |
|--------|------|----------|
| CSS | Write CSS keyframes + classes | Simple animations, no JS dependency |
| GSAP | Write GSAP timeline code | Complex animations, scroll-triggered, interactive |
| React Component | Write a client component | Direct integration into the app |
| MP4/WebM | Video model generation | Cinemagraphs, complex motion, social posts |
| GIF | ffmpeg conversion from video | Legacy support, email, simple social |

## Output Report

```
## Animation Report

### Source: public/images/generated/hero/forgotten-ways.png
### Animation: Ken Burns (slow pan & zoom)
### Output Format: GSAP + React Component

### Implementation
- Component: src/components/content/AnimatedHero.tsx
- Animation: 15s ease-in-out infinite yoyo
- Scale: 1.0 → 1.12
- Drift: 0,0 → -2%,-1%

### Accessibility
- ✅ prefers-reduced-motion: animation disabled
- ✅ No layout shift (overflow: hidden on container)
- ✅ will-change: transform (GPU accelerated)
- ✅ No width/height animation (transform only)

### Performance
- ✅ GPU-composited (transform + opacity only)
- ✅ No repaints or reflows
- ✅ Single element animated

### Next Steps
- Import AnimatedHero component into the target page
- Use `/design-audit` to check motion accessibility compliance
```

## Rules

1. **ALWAYS** include `prefers-reduced-motion` support — this is non-negotiable
2. **Only animate transform and opacity** — never width, height, top, left, margin
3. **Keep durations subtle**: 3-15 seconds for ambient, 150-300ms for interactions
4. **No auto-playing video with sound** — muted only, or use CSS/Canvas animations
5. **GPU-composited** — use `will-change: transform` or `translateZ(0)` for smooth rendering
6. **Maximum subtlety** — if a user notices the animation consciously, it's probably too much.
   The goal is to make the page feel *alive*, not *animated*.
