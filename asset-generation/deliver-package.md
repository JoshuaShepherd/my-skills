
Package and deliver asset prompts or images as an interactive HTML page: $ARGUMENTS

$ARGUMENTS should include:
- The content to package (prompts, images, or both)
- Optionally: page title and heading
- Optionally: output file path
- Optionally: style theme (dark/light/brand)
- Empty — ask the user what to package

## Before Starting

1. Read `{{CONFIG_PATH}}` for brand name (used in footer/branding)
2. Read `{{STYLES_PATH}}` for brand color tokens (if using brand theme)
3. Gather all content to include — prompts, image paths, metadata

## Page Types

### 1. Prompt Delivery Page
Tabbed interface showing 2-4 prompts with one-click copy buttons.
- Use case: scroll-stop prompt sets, multi-variant prompts, A/B test prompts

### 2. Asset Gallery Page
Grid/carousel of generated images with metadata, download buttons, and comparison tools.
- Use case: reviewing asset-series output, sharing mood boards with stakeholders

### 3. Before/After Comparison Page
Side-by-side or slider comparison of original and edited images.
- Use case: showing edit refinements, brand-check before/after

### 4. Asset Package Page
Combined prompts + generated images + metadata in a single deliverable.
- Use case: complete scroll-stop package (prompts + generated frames + video prompt)

## Execution

### Step 1 — Gather Content
Collect all content to include:
- Prompt texts (escape HTML entities: `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`)
- Image file paths (convert to base64 for embedding, or use relative paths)
- Metadata (object name, settings used, generation date)

### Step 2 — Choose Theme

#### Dark Theme (Default — VoltFlow style)
```css
--bg: #02040a;
--surface: rgba(255, 255, 255, 0.03);
--border: rgba(255, 255, 255, 0.08);
--text: #e4e4e7;
--text-muted: #71717a;
--accent: #BFF549;
--accent-hover: #d4ff7a;
--font-heading: 'Space Grotesk', sans-serif;
--font-body: 'Archivo', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

#### Brand Theme ({{AUTHOR_NAME}} warm)
```css
--bg: #1a1512;
--surface: rgba(250, 245, 228, 0.04);
--border: rgba(250, 245, 228, 0.1);
--text: {{BRAND_LIGHT}};
--text-muted: {{BRAND_MUTED}};
--accent: {{BRAND_PRIMARY}};
--accent-hover: #E5BE6A;
--font-heading: 'Playfair Display', serif;
--font-body: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

#### Light Theme
```css
--bg: #FAFAF8;
--surface: #FFFFFF;
--border: #E5E5E3;
--text: #1a1a1a;
--text-muted: #6B6B6B;
--accent: {{BRAND_ACCENT}};
--accent-hover: #D4714F;
```

### Step 3 — Build the HTML

Write a self-contained HTML file with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PAGE_TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* Theme variables — swap block for different themes */
    :root {
      {{THEME_VARIABLES}}
    }

    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Floating background orbs */
    .orb {
      position: fixed;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.15;
      pointer-events: none;
      z-index: 0;
    }
    .orb-1 { width: 400px; height: 400px; background: var(--accent); top: -100px; right: -100px; }
    .orb-2 { width: 300px; height: 300px; background: var(--accent); bottom: -80px; left: -80px; opacity: 0.1; }

    /* Container */
    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
      position: relative;
      z-index: 1;
    }

    /* Heading */
    .heading {
      font-family: var(--font-heading);
      font-size: clamp(2.5rem, 6vw, 4rem);
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 0.5rem;
    }
    .heading-muted {
      opacity: 0.3;
    }
    .subtitle {
      color: var(--text-muted);
      font-size: 1.1rem;
      margin-bottom: 2.5rem;
    }

    /* Tabs */
    .tabs {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
      overflow-x: auto;
    }
    .tab {
      padding: 0.6rem 1.2rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: transparent;
      color: var(--text-muted);
      font-family: var(--font-body);
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tab:hover { border-color: var(--accent); color: var(--text); }
    .tab.active {
      background: var(--accent);
      color: var(--bg);
      border-color: var(--accent);
      font-weight: 600;
    }
    .tab .short-label { display: none; }

    /* Prompt card */
    .prompt-card {
      display: none;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      position: relative;
      backdrop-filter: blur(10px);
    }
    .prompt-card.active { display: block; }
    .prompt-text {
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.7;
      color: var(--text);
      white-space: pre-wrap;
      word-break: break-word;
    }

    /* Copy button */
    .copy-btn {
      position: absolute;
      top: 1rem;
      right: 1rem;
      padding: 0.5rem 1rem;
      background: var(--accent);
      color: var(--bg);
      border: none;
      border-radius: 6px;
      font-family: var(--font-body);
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s ease;
      z-index: 2;
    }
    .copy-btn:hover { background: var(--accent-hover); transform: translateY(-1px); }
    .copy-btn.copied { background: #22c55e; }

    /* Image grid */
    .image-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
      margin-top: 1.5rem;
    }
    .image-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      background: var(--surface);
    }
    .image-card img {
      width: 100%;
      height: auto;
      display: block;
    }
    .image-card .meta {
      padding: 0.75rem 1rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    /* Footer */
    .footer {
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.8rem;
      text-align: center;
    }

    /* Confetti canvas */
    #confetti-canvas {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      z-index: 9999;
    }

    /* Responsive */
    @media (max-width: 640px) {
      .tab .full-label { display: none; }
      .tab .short-label { display: inline; }
      .container { padding: 2rem 1rem; }
    }
  </style>
</head>
<body>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <canvas id="confetti-canvas"></canvas>

  <div class="container">
    <h1 class="heading">
      {{HEADING_LINE1}}<br>
      <span class="heading-muted">{{HEADING_LINE2}}</span>
    </h1>
    <p class="subtitle">{{SUBTITLE}}</p>

    <div class="tabs">
      {{TABS_HTML}}
    </div>

    {{CARDS_HTML}}

    {{IMAGES_HTML}}

    <div class="footer">
      Generated with Gemini Image Generation &mdash; {{BRAND_NAME}} &mdash; {{DATE}}
    </div>
  </div>

  <script>
    // Tab switching
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.prompt-card').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
      });
    });

    // Keyboard shortcuts: 1, 2, 3 switch tabs
    document.addEventListener('keydown', (e) => {
      const n = parseInt(e.key);
      if (n >= 1 && n <= 9) {
        const tabs = document.querySelectorAll('.tab');
        if (tabs[n - 1]) tabs[n - 1].click();
      }
    });

    // Copy with confetti
    document.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const card = btn.closest('.prompt-card');
        const text = card.querySelector('.prompt-text').textContent;
        navigator.clipboard.writeText(text).then(() => {
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          fireConfetti(btn);
          setTimeout(() => {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 2000);
        });
      });
    });

    // Minimal confetti implementation
    function fireConfetti(origin) {
      const canvas = document.getElementById('confetti-canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const rect = origin.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;

      const particles = Array.from({ length: 40 }, () => ({
        x: cx, y: cy,
        vx: (Math.random() - 0.5) * 12,
        vy: (Math.random() - 0.8) * 12,
        size: Math.random() * 6 + 3,
        color: ['#BFF549', '{{BRAND_PRIMARY}}', '{{BRAND_ACCENT}}', '{{BRAND_SECONDARY}}', '{{BRAND_LIGHT}}'][Math.floor(Math.random() * 5)],
        life: 1,
        decay: Math.random() * 0.02 + 0.015,
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 10,
      }));

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let alive = false;
        for (const p of particles) {
          if (p.life <= 0) continue;
          alive = true;
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.3;
          p.life -= p.decay;
          p.rotation += p.rotSpeed;

          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = p.life;
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
          ctx.restore();
        }
        if (alive) requestAnimationFrame(animate);
        else ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
      animate();
    }
  </script>
</body>
</html>
```

### Step 4 — Populate the Template

Replace placeholders:

| Placeholder | Source |
|-------------|--------|
| `{{PAGE_TITLE}}` | Object name or concept |
| `{{HEADING_LINE1}}` | First word(s) of heading |
| `{{HEADING_LINE2}}` | Second word(s) — displayed faded |
| `{{SUBTITLE}}` | Brief description |
| `{{THEME_VARIABLES}}` | CSS variables from chosen theme |
| `{{TABS_HTML}}` | Generated tab buttons |
| `{{CARDS_HTML}}` | Generated prompt cards |
| `{{IMAGES_HTML}}` | Image grid (if images included) |
| `{{BRAND_NAME}}` | From tenant config |
| `{{DATE}}` | Current date |

For each prompt/tab:
```html
<!-- Tab button -->
<button class="tab active" data-target="prompt-a">
  <span class="full-label">Assembled Shot</span>
  <span class="short-label">Assembled</span>
</button>

<!-- Prompt card -->
<div id="prompt-a" class="prompt-card active">
  <button class="copy-btn">Copy</button>
  <div class="prompt-text">{{PROMPT_TEXT_ESCAPED}}</div>
</div>
```

### Step 5 — Write & Open

```bash
# Write the file
# (use the Write tool to create the HTML file)

# Open in browser (macOS)
open prompts.html
```

Default output path: `prompts.html` in the working directory.
Custom path via argument: `/asset-deliver --output public/prompts/scroll-stop-smoothie.html`

## Output Format

```
## Delivery Page Created

### File: prompts.html
### Theme: Dark (VoltFlow)
### Content:
- Tab A: Assembled Shot prompt
- Tab B: Deconstructed Shot prompt
- Tab C: Video Transition prompt

### Features
- ✅ Tabbed navigation (A/B/C)
- ✅ One-click copy with confetti
- ✅ Keyboard shortcuts (1/2/3)
- ✅ Mobile responsive
- ✅ Self-contained (no external dependencies except Google Fonts)

### Opened in browser ✅
```

## Integration with Other Skills

| Workflow | Skills Chain |
|----------|-------------|
| Scroll-stop content | `/asset-product-shot` → `/asset-exploded-view` → `/asset-video-prompt` → `/asset-deliver` |
| Course asset review | `/asset-series` → `/asset-brand-check` → `/asset-deliver` (gallery) |
| Prompt sharing | `/asset-generate` → `/asset-deliver` (prompts + images) |
| Edit comparison | `/asset-edit` → `/asset-deliver` (before/after) |
