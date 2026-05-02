
Manage the Gemini prompt template library: $ARGUMENTS

$ARGUMENTS should be one of:
- `list` — Show all available prompt templates
- `show <template-name>` — Display a specific template with its variables
- `create <template-name>` — Create a new prompt template
- `use <template-name> [--var key=value ...]` — Instantiate a template with variables
- `update <template-name>` — Modify an existing template
- `delete <template-name>` — Remove a template
- Empty — show the list of available templates

## Template Storage

Templates are stored in `{{ASSET_DOCS_DIR}}/` as individual markdown files:

```
{{ASSET_DOCS_DIR}}/
  _index.md              ← Master index of all templates
  hero-course.md         ← Course hero/cover images
  hero-page.md           ← Generic page hero images
  og-image.md            ← Open Graph / social sharing images
  quote-card.md          ← Quote cards for social media
  book-cover.md          ← Book cover images
  podcast-artwork.md     ← Podcast episode artwork
  thumbnail-video.md     ← Video thumbnails
  banner-email.md        ← Email banner headers
  chapter-header.md      ← Book/course chapter headers
  certificate.md         ← Course completion certificates
  social-square.md       ← Square social media posts
  social-story.md        ← Vertical story format
  series-module.md       ← Course module series template
```

## Template Format

Each template file follows this structure:

```markdown

## Prompt Template

[STYLE ANCHOR]
Editorial photography style, shot on Sony A7IV, 85mm f/1.4, natural light.
Warm earth-tone color palette: terracotta, amber, sage, cream.
Subtle film grain, warm color grade. Soft golden-hour side lighting.

[SUBJECT]
{{subject}}

[SETTING]
An intimate, well-lit space with natural textures — wood surfaces, linen,
visible bookshelves. {{mood}} atmosphere.

[TEXT — if applicable]
{{#if title}}The image should include "{{title}}" in bold serif text,
centered in the upper third.{{/if}}
{{#if subtitle}}"{{subtitle}}" in smaller sans-serif below the title,
warm cream color.{{/if}}

[COMPOSITION]
Subject occupies the left 60% of the frame. Negative space on the right
for UI text overlay. Shallow depth of field, background softly blurred.
Medium close-up framing following rule of thirds.

## Usage Example

/asset-prompt-library use hero-course --var title="The {{COURSE_NAME}}" --var subject="an open compass on a hand-drawn map with a seedling growing beside it"
```

## Built-in Templates

### Create the initial library with these templates on first use:

#### 1. `hero-course` — Course Cover Images
- Aspect: 16:9, Resolution: 2048, Thinking: high
- Variables: `title` (required), `subtitle`, `subject` (required), `mood`
- Style: Editorial photography, warm earth tones, golden-hour lighting
- Composition: Subject left 60%, negative space right for text overlay

#### 2. `hero-page` — Generic Page Heroes
- Aspect: 16:9, Resolution: 2048, Thinking: high
- Variables: `subject` (required), `mood`, `focus_area`
- Style: Wide establishing shot, atmospheric, warm palette
- Composition: Cinematic wide-angle, subject centered or rule-of-thirds

#### 3. `og-image` — Open Graph Cards
- Aspect: 16:9, Resolution: 1024, Thinking: minimal
- Variables: `title` (required), `subtitle`, `background_style`
- Style: Clean editorial, warm gradient or textured background
- Composition: Title prominent center-left, brand mark bottom-left

#### 4. `quote-card` — Social Quote Cards
- Aspect: 1:1, Resolution: 1024, Thinking: minimal
- Variables: `quote` (required), `attribution` (default: "{{AUTHOR_NAME}}"), `background`
- Style: Warm paper/linen texture, serif typography
- Composition: Quote centered with generous margins, attribution bottom-right

#### 5. `book-cover` — Book Cover Images
- Aspect: 3:4, Resolution: 2048, Thinking: high
- Variables: `title` (required), `author` (default: "{{AUTHOR_NAME}}"), `subject` (required), `genre_feel`
- Style: Rich, layered, sophisticated
- Composition: Title upper third, visual center, author bottom

#### 6. `podcast-artwork` — Podcast Episode Art
- Aspect: 1:1, Resolution: 1024, Thinking: minimal
- Variables: `show_title` (required), `episode_title`, `guest_name`, `episode_number`
- Style: Clean, modern, consistent template with episode variations
- Composition: Show title top, visual center, episode info bottom

#### 7. `thumbnail-video` — Video Thumbnails
- Aspect: 16:9, Resolution: 1024, Thinking: minimal
- Variables: `title` (required), `speaker`, `topic_visual`
- Style: High contrast for small display, warm palette
- Composition: Speaker/visual left, title right, bold text

#### 8. `banner-email` — Email Header Banners
- Aspect: 3:1, Resolution: 1024, Thinking: minimal
- Variables: `headline` (required), `background_style`
- Style: Clean, warm gradient, minimal elements
- Composition: Headline centered, brand mark subtle corner

#### 9. `chapter-header` — Chapter/Module Headers
- Aspect: 16:9, Resolution: 1024, Thinking: minimal
- Variables: `number` (required), `title` (required), `motif`
- Style: Numbered overlay, warm tones, editorial
- Composition: Large number background (low opacity), title centered

#### 10. `certificate` — Course Completion Certificates
- Aspect: √2:1 (1.414:1), Resolution: 2048, Thinking: high
- Variables: `course_title` (required), `recipient_name` (required), `date`, `credential_id`
- Style: Formal but warm, parchment-feel, elegant borders
- Composition: Title top, recipient center (large), details bottom, brand seal

#### 11. `social-square` — Square Social Posts
- Aspect: 1:1, Resolution: 1024, Thinking: minimal
- Variables: `headline` (required), `visual_subject`, `cta_text`
- Style: Bold, high-contrast for social feeds, warm palette
- Composition: Visual top half, text bottom half (or full bleed with overlay)

#### 12. `social-story` — Vertical Story Format
- Aspect: 9:16, Resolution: 2048, Thinking: minimal
- Variables: `headline` (required), `body_text`, `visual_subject`, `cta_text`
- Style: Immersive vertical, warm tones, mobile-optimized text size
- Composition: Visual fills frame, text overlaid with gradient protection

#### 13. `series-module` — Series Consistency Template
- Aspect: 16:9, Resolution: 2048, Thinking: high
- Variables: `series_name` (required), `module_number` (required), `module_title` (required), `subject` (required)
- Style: Locked style anchor (defined on first generation)
- Composition: Consistent across series, only subject varies
- Special: Includes style anchor block for cross-item consistency

## Operations

### `list`
Read `{{ASSET_DOCS_DIR}}/_index.md` and display all templates with descriptions.

### `show <template-name>`
Read the template file, display the full prompt template with its variables and an example.

### `create <template-name>`
1. Ask the user for: description, asset type, variables, and the prompt template body
2. Write the template file to `{{ASSET_DOCS_DIR}}/<template-name>.md`
3. Update `{{ASSET_DOCS_DIR}}/_index.md`

### `use <template-name> [--var key=value ...]`
1. Read the template file
2. Substitute all `{{variable}}` placeholders with provided values
3. Validate all required variables are provided
4. Output the instantiated prompt — ready to paste into `/asset-generate`
5. Optionally: pipe directly to generation if the user confirms

### `update <template-name>`
1. Read the existing template
2. Apply the user's requested changes
3. Save the updated template

### `delete <template-name>`
1. Confirm with the user
2. Delete the template file
3. Update `{{ASSET_DOCS_DIR}}/_index.md`

## Initialization

On first invocation, if `{{ASSET_DOCS_DIR}}/` doesn't exist:
1. Create the directory
2. Create `_index.md` with the master list
3. Create all 13 built-in templates
4. Report completion

## Output Format — `list`

```
## Gemini Prompt Template Library

| # | Template | Asset Type | Aspect | Description |
|---|----------|-----------|--------|-------------|
| 1 | hero-course | 16:9 @2048 | Course cover/hero images |
| 2 | hero-page | 16:9 @2048 | Generic page hero backgrounds |
| 3 | og-image | 16:9 @1024 | Open Graph / link preview images |
| 4 | quote-card | 1:1 @1024 | Social media quote cards |
| 5 | book-cover | 3:4 @2048 | Book cover images |
| ... | ... | ... | ... |

Use `/asset-prompt-library show <name>` to view a template.
Use `/asset-prompt-library use <name> --var key=value` to instantiate.
```

## Output Format — `use`

```
## Instantiated Prompt: hero-course

### Variables
- title: "The {{COURSE_NAME}}"
- subtitle: "Reactivating Apostolic Movements"
- subject: "an open compass on a hand-drawn map with a seedling"
- mood: "warm, contemplative, hopeful"

### Ready-to-Use Prompt
> Editorial photography style, shot on Sony A7IV, 85mm f/1.4, natural light.
> Warm earth-tone color palette: terracotta, amber, sage, cream.
> Subtle film grain, warm color grade. Soft golden-hour side lighting.
>
> An open compass lying on a hand-drawn map with a small seedling growing beside it.
>
> An intimate, well-lit space with natural textures — wood surfaces, linen,
> visible bookshelves. Warm, contemplative, hopeful atmosphere.
>
> The image should include "The {{COURSE_NAME}}" in bold serif text,
> centered in the upper third. "Reactivating Apostolic Movements" in
> smaller sans-serif below the title, warm cream color.
>
> Subject occupies the left 60% of the frame. Negative space on the right
> for UI text overlay. Shallow depth of field, background softly blurred.

### Next Steps
- Run `/asset-generate` with this prompt
- Or modify variables and re-instantiate
```
