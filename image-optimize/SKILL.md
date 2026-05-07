---
name: image-optimize
description: Optimize images from the local images repo (convert to WebP, generate responsive variants, resize) and upload to Supabase Storage preserving the multi-tenant folder structure. Use when adding new images, syncing the images repo to storage, or generating responsive sets for existing assets.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Optimize and upload images to Supabase Storage: $ARGUMENTS

$ARGUMENTS should include:
- A scope: tenant slug (`alan-hirsch`, `brad-brisco`, `movemental`, etc.), specific category (`alan-hirsch/headshots`), or a single file path
- Optionally: `--dry-run` to preview without uploading
- Optionally: `--responsive` to generate responsive variant sets (base, -desktop, -mobile, -tablet, -2x)
- Optionally: `--force` to overwrite existing files in storage
- Optionally: `--skip-optimize` to upload as-is without WebP conversion
- Empty — list available tenants and ask what to sync

## Architecture

### Local Images Repo (source of truth for raw assets)
```
/Users/joshuashepherd/Desktop/dev/repos/images/
  {tenant-slug}/              # alan-hirsch, brad-brisco, josh-shepherd, movemental, youthfront
    art/                      # Abstract art, portal icons, pathway illustrations
    articles/                 # Article feature images
    books/                    # Book cover images
    brand/                    # Brand assets (logos, marks)
    certificates/             # Certificate backgrounds/templates
    courses/                  # Course cover images
    headshots/                # Author/speaker headshots
    heroes/                   # Hero section backgrounds
    logos/                    # Logo variants
    orgs/                     # Partner organization logos
    podcasts/                 # Podcast cover art
    portals/                  # Portal/topic entry images
    social/                   # Social media cards
    testimonials/             # Testimonial author photos
    videos/                   # Video thumbnails
  shared/                     # Cross-tenant assets
    fallbacks/
    platform/
    ui/
```

### Supabase Storage (CDN delivery)
- **Bucket:** `media-library` (public)
- **Base URL:** `https://vhaiiiykcukrlyvwlgip.supabase.co/storage/v1/object/public/media-library/`
- **Path mapping:** Images repo path maps 1:1 to storage path
  - `images/alan-hirsch/headshots/alan-hero-4x5.webp` → `media-library/alan-hirsch/headshots/alan-hero-4x5.webp`
  - `images/shared/fallbacks/placeholder.webp` → `media-library/shared/fallbacks/placeholder.webp`

### App Integration
- `src/lib/utils/storage-url.ts` → `resolveStorageUrl()` converts relative paths to full Supabase URLs
- `next.config.ts` → `remotePatterns` allows `*.supabase.co/storage/**`
- Components use `next/image` with `sizes` prop for responsive loading
- `media_items` database table tracks metadata (optional registration)

## Before Starting

1. Confirm the images repo exists at `/Users/joshuashepherd/Desktop/dev/repos/images/`
2. Confirm env vars are available in the tenant app project:
   ```bash
   cd /Users/joshuashepherd/Desktop/dev/repos/movemental-sites/alan-hirsch && grep SUPABASE_SERVICE_ROLE_KEY .env.local
   ```
3. Identify the scope — which tenant and/or category to process
4. Inventory source files: count, formats, sizes

## Optimization Pipeline

### Step 1 — Inventory Source Files

```bash
# Count files by tenant and format
find /Users/joshuashepherd/Desktop/dev/repos/images/{TENANT} -type f \
  -not -name '.DS_Store' \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

Report:
- Total files per category
- Format breakdown (webp vs png vs jpg vs jpeg)
- Files needing conversion (non-WebP)
- Files missing responsive variants

### Step 2 — Convert to WebP

Any non-WebP images (PNG, JPG, JPEG) should be converted. Use `sharp` via a Node script in the alan-hirsch project.

```typescript
import sharp from "sharp";
import * as fs from "fs";
import * as path from "path";

const QUALITY_MAP: Record<string, number> = {
  headshots: 88,     // High quality for faces
  heroes: 82,        // Large images, balance size vs quality
  art: 82,
  books: 85,         // Book covers need detail
  courses: 82,
  logos: 90,          // Logos need crisp edges
  orgs: 90,
  portals: 82,
  brand: 90,
  social: 85,
  certificates: 85,
  articles: 82,
  podcasts: 85,
  testimonials: 85,
  videos: 80,        // Thumbnails can be smaller
  fallbacks: 75,
};

async function convertToWebP(inputPath: string, category: string): Promise<string> {
  const quality = QUALITY_MAP[category] ?? 82;
  const outputPath = inputPath.replace(/\.(png|jpe?g|gif)$/i, ".webp");

  await sharp(inputPath)
    .webp({ quality, effort: 6 })
    .toFile(outputPath);

  return outputPath;
}
```

**Rules:**
- Keep the original file alongside the WebP (don't delete source)
- If a `.webp` already exists for a given base name, skip unless `--force`
- SVG files are NOT converted — upload as-is
- Transparent PNGs (logos, marks) → use WebP with `{ quality: 90, alphaQuality: 100 }` to preserve transparency

### Step 3 — Generate Responsive Variants (when `--responsive`)

For images used in responsive `<Image>` components, generate a set of size variants.

```typescript
interface ResponsivePreset {
  suffix: string;
  maxWidth: number;
  quality: number;
}

const RESPONSIVE_VARIANTS: ResponsivePreset[] = [
  { suffix: "-mobile",  maxWidth: 640,  quality: 80 },
  { suffix: "-tablet",  maxWidth: 1024, quality: 82 },
  { suffix: "-desktop", maxWidth: 1440, quality: 85 },
  { suffix: "-2x",      maxWidth: 2880, quality: 82 },
];

async function generateResponsiveSet(inputPath: string, category: string) {
  const ext = path.extname(inputPath);
  const base = inputPath.replace(ext, "");
  const metadata = await sharp(inputPath).metadata();
  const srcWidth = metadata.width ?? 1920;

  for (const variant of RESPONSIVE_VARIANTS) {
    // Skip if variant would upscale
    if (variant.maxWidth >= srcWidth) continue;

    const outPath = `${base}${variant.suffix}.webp`;
    if (fs.existsSync(outPath)) continue; // Already exists

    await sharp(inputPath)
      .resize({ width: variant.maxWidth, withoutEnlargement: true })
      .webp({ quality: variant.quality, effort: 6 })
      .toFile(outPath);
  }
}
```

**When to generate responsive variants:**
- Headshots used in hero sections → yes
- Course covers → yes
- Book covers → yes
- Art/hero backgrounds → yes
- Logos and org logos → yes (but only `-2x` and base)
- Portal icons → no (already small)
- Social cards → no (fixed dimensions)

### Step 4 — Upload to Supabase Storage

Use the Supabase JS client with the service role key.

```typescript
import { createClient } from "@supabase/supabase-js";

const BUCKET = "media-library";
const IMAGES_REPO = "/Users/joshuashepherd/Desktop/dev/repos/images";

async function uploadToStorage(localPath: string, dryRun = false) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  const supabase = createClient(url, serviceKey);

  // Derive storage path from local path relative to images repo
  // /Users/.../images/alan-hirsch/headshots/file.webp → alan-hirsch/headshots/file.webp
  const storagePath = path.relative(IMAGES_REPO, localPath).replace(/\\/g, "/");

  if (dryRun) {
    console.log(`[dry-run] Would upload: ${storagePath}`);
    return;
  }

  const buffer = fs.readFileSync(localPath);
  const contentType = getMime(path.extname(localPath));

  const { error } = await supabase.storage.from(BUCKET).upload(storagePath, buffer, {
    upsert: true,
    contentType,
  });

  if (error) {
    console.error(`FAIL ${storagePath}: ${error.message}`);
  } else {
    const publicUrl = `${url}/storage/v1/object/public/${BUCKET}/${storagePath}`;
    console.log(`OK   ${storagePath}`);
    console.log(`     ${publicUrl}`);
  }
}

function getMime(ext: string): string {
  const map: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
  };
  return map[ext.toLowerCase()] ?? "application/octet-stream";
}
```

**Upload rules:**
- Always use `upsert: true` so re-runs are safe
- Upload WebP versions (not the original PNG/JPG unless no WebP exists)
- Skip `.DS_Store` and any `reference/` directories (reference images are local-only)
- Skip files larger than 10MB — flag them for manual review
- Upload in batches of 5 concurrent to avoid rate limits

### Step 5 — Verify & Report

After upload, verify by checking the public URL returns 200:

```bash
curl -s -o /dev/null -w "%{http_code}" "https://vhaiiiykcukrlyvwlgip.supabase.co/storage/v1/object/public/media-library/alan-hirsch/headshots/alan-hero-4x5.webp"
```

## Execution Strategy

Write an inline Node script (using `npx tsx`) that performs the full pipeline. Run it from the tenant app project directory so env vars are accessible.

```bash
cd /Users/joshuashepherd/Desktop/dev/repos/movemental-sites/alan-hirsch && npx tsx -e '
  // inline script here
'
```

Or, for larger operations, write a temporary script file:

```bash
cd /Users/joshuashepherd/Desktop/dev/repos/movemental-sites/alan-hirsch && cat > /tmp/image-optimize.ts << 'SCRIPT'
// full script
SCRIPT
npx tsx /tmp/image-optimize.ts
```

## Naming Conventions

### File Naming
- Use lowercase kebab-case: `alan-hero-4x5.webp`
- Include aspect ratio in name when relevant: `-4x5`, `-16x9`, `-3x4`, `-1x1`
- Responsive suffixes: `-mobile`, `-tablet`, `-desktop`, `-2x`
- Category prefix when helpful: `art-course-`, `art-portal-`, `book-`, `course-`
- No spaces in filenames — use hyphens

### Storage Path Structure
```
media-library/
  {tenant-slug}/
    {category}/
      {descriptive-name}[-{aspect}][-{variant}].webp
```

Examples:
```
alan-hirsch/headshots/alan-hero-4x5.webp
alan-hirsch/headshots/alan-hero-4x5-mobile.webp
alan-hirsch/courses/course-forgotten-ways-cover-desktop.webp
alan-hirsch/art/art-portal-forgotten-ways.webp
brad-brisco/headshots/brad-brisco-primary.webp
movemental/logos/movemental-logo.webp
shared/fallbacks/placeholder.webp
```

## Using Uploaded Images in the App

### In Components (via resolveStorageUrl)
```tsx
import { resolveStorageUrl } from "@/lib/utils/storage-url";
import Image from "next/image";

// Pass relative storage path — resolveStorageUrl prepends the Supabase base URL
<Image
  src={resolveStorageUrl("alan-hirsch/headshots/alan-hero-4x5.webp")!}
  alt="Alan Hirsch"
  width={800}
  height={1000}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  priority
/>
```

### In Tenant Config
```typescript
// tenant.config.ts
hero: {
  imageUrl: "alan-hirsch/headshots/alan-hero-4x5.webp",  // relative path
}
```

### Best Practices for next/image
- Always set `sizes` prop for responsive images — prevents downloading oversized images
- Use `priority` on above-the-fold hero images only
- Use `fill` with `object-cover` for background images in containers
- Set explicit `width`/`height` for known-dimension images (book covers, avatars)
- Use `placeholder="blur"` with `blurDataURL` for large hero images (generate tiny base64 with sharp)

## Output Format

```
## Image Optimization Report

### Scope: {tenant-slug}/{category or "all"}
### Mode: {optimize + upload | dry-run | optimize-only}

### Inventory
| Category    | Source Files | Already WebP | Converted | Responsive Sets |
|-------------|-------------|--------------|-----------|-----------------|
| headshots   | 24          | 20           | 4         | 6 sets          |
| art         | 32          | 32           | 0         | 0               |
| ...         | ...         | ...          | ...       | ...             |

### Conversions
- Converted 4 PNG/JPG files to WebP (saved ~2.3MB total)
- Generated 24 responsive variants across 6 base images

### Uploads
- Uploaded: 60 files to media-library/{tenant-slug}/
- Skipped: 12 files (already exist, no changes)
- Failed: 0

### Storage URLs
Key images for integration:
- Hero: `{base-url}/alan-hirsch/headshots/alan-hero-4x5.webp`
- Instructor: `{base-url}/alan-hirsch/headshots/alan-instructor.webp`
- ...

### Next Steps
- Update `tenant.config.ts` if hero/instructor URLs changed
- Run `/image-optimize {next-tenant}` for other tenants
- Review responsive variant quality in browser DevTools
```

## Integration with Other Skills

| Workflow | Chain |
|----------|-------|
| New headshot → optimize → upload | `/asset-headshot` → `/image-optimize alan-hirsch/headshots` |
| New hero art → optimize → upload | `/asset-generate hero` → `/image-optimize alan-hirsch/heroes` |
| Full tenant image sync | `/image-optimize alan-hirsch` |
| New tenant onboarding | `pnpm storage:scaffold --org {slug}` → add images to repo → `/image-optimize {slug}` |
| Course cover set | `/asset-generate cover-course` → `/image-optimize alan-hirsch/courses --responsive` |

## Error Recovery

| Issue | Fix |
|-------|-----|
| `SUPABASE_SERVICE_ROLE_KEY` missing | Check `.env.local` in the alan-hirsch project |
| Upload fails with 413 | File too large — resize with sharp first, or increase bucket limit |
| WebP conversion fails | Ensure `sharp` is installed: `cd alan-hirsch && pnpm add -D sharp` |
| Storage path conflict | Use `upsert: true` (already default in the pipeline) |
| Transparent PNG loses transparency | Use `{ alphaQuality: 100 }` in WebP options |
| Reference images uploaded | Exclude `reference/` directories from the upload walk |
