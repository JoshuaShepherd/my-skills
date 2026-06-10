# Content Library page spec — `library.html`

A browsable index of all of the leader's content across types: books, articles, videos, podcasts, courses, assessments.

## 1. Nav

Per [movemental-nav-spec.md](movemental-nav-spec.md). Mark the "Library" link with `aria-current="page"`.

## 2. Library hero (compact)

Smaller than the home hero — typically no full-bleed image. Echo the home hero's *typography and color treatment* so the page reads as part of the same site, but at lower visual intensity.

```html
<header class="ml-hero ml-hero--compact">
  <div class="ml-hero-inner">
    <p class="ml-hero-eyebrow">Content Library</p>
    <h1 class="ml-hero-title">{Headline — one-sentence statement of what's in the library}</h1>
    <p class="ml-hero-tagline">{Optional: a sentence on how it's organized.}</p>
    <form class="library-search" role="search" onsubmit="event.preventDefault()">
      <label class="visually-hidden" for="library-search-input">Search library</label>
      <input id="library-search-input" type="search" placeholder="Search books, articles, videos…" />
    </form>
  </div>
</header>
```

The `library-search` form is required regardless of whether the nav search is included — the library is where search is most expected. Style follows the reference's input vocabulary.

## 3. Filter chips

A horizontal row of content-type chips:

```html
<nav class="ml-filter-chips" aria-label="Content type">
  <button type="button" class="ml-filter-chip is-active" data-filter="all">All</button>
  <button type="button" class="ml-filter-chip" data-filter="books">Books</button>
  <button type="button" class="ml-filter-chip" data-filter="articles">Articles</button>
  <button type="button" class="ml-filter-chip" data-filter="videos">Videos</button>
  <button type="button" class="ml-filter-chip" data-filter="podcasts">Podcasts</button>
  <button type="button" class="ml-filter-chip" data-filter="courses">Courses</button>
  <button type="button" class="ml-filter-chip" data-filter="assessments">Assessments</button>
</nav>
```

The chips don't have to filter live in the template (they can be static demonstrative elements). If the style spec's motion field is `moderate` or `rich`, wire them up in `main.js` to filter visible cards by `[data-type]` attribute.

Style follows the reference's button vocabulary — pill, square, underline-only, or text.

Optionally include a second row of topic filters if the leader has clear topical clusters (mDNA / formation / APEST / leadership / etc.):

```html
<nav class="ml-filter-chips ml-filter-chips--topics" aria-label="Topic">
  <button type="button" class="ml-filter-chip" data-topic="mdna">mDNA</button>
  <!-- … -->
</nav>
```

## 4. Resource grid

A unified grid mixing content types. Each card includes:
- Type badge (`BOOK`, `ARTICLE`, `VIDEO`, `PODCAST`, `COURSE`, `ASSESSMENT`)
- Cover or thumbnail
- Title
- One-line description
- Meta line: date OR read-time OR duration

```html
<section class="library-grid" aria-label="Library">
  <article class="ml-card ml-card--library" data-type="book">
    <div class="ml-card-media">
      <img src="images/cover-placeholder-book.webp" alt="" loading="lazy" />
    </div>
    <div class="ml-card-body">
      <span class="ml-card-meta">Book · {YYYY}</span>
      <h3 class="ml-card-title">{Title — placeholder}</h3>
      <p class="ml-card-desc">{One-line description.}</p>
    </div>
  </article>
  <!-- ×12 across mixed types -->
</section>
```

Grid density follows the style spec:

| Density (from spec) | Columns |
|---------------------|---------|
| `sparse` / editorial | 2 desktop, 1 tablet, 1 mobile, generous gutters |
| `balanced` / modern | 3 desktop, 2 tablet, 1 mobile |
| `dense` / portal | 4 desktop, 3 tablet, 1 mobile, tight gutters |
| Brutalist / list-style | List rows, single column, hard rules between |

## 5. Featured collection (optional)

A horizontally-scrolling carousel (or static row, depending on motion field) of one curated collection: "If you're new to {Leader}'s work, start here…"

```html
<section class="ml-section library-featured" aria-labelledby="library-featured-title">
  <h2 id="library-featured-title" class="ml-section-title">Start here</h2>
  <p class="ml-section-desc">{Optional one-line on how to read this collection.}</p>
  <div class="library-featured-rail">
    <a href="#" class="ml-card ml-card--featured">
      <div class="ml-card-media"><img src="images/cover-placeholder-1.webp" alt="" loading="lazy" /></div>
      <div class="ml-card-body">
        <span class="ml-card-meta">Book · Foundational</span>
        <h3 class="ml-card-title">{Title}</h3>
      </div>
    </a>
    <!-- ×3-5 -->
  </div>
</section>
```

`.library-featured-rail` uses `overflow-x: auto` with scroll-snap if motion ≥ moderate.

## 6. Pagination or load-more

Match the reference's energy:

| Reference | Control |
|-----------|---------|
| Editorial | Numbered pagination: `← Prev 1 2 3 … Next →` |
| Modern / portal | "Load more" button under the grid |
| Brutalist / utility | No control — `<noscript>` fallback note "Showing 12 of N" |

```html
<!-- Editorial -->
<nav class="library-pagination" aria-label="Library pagination">
  <a href="#" rel="prev" aria-disabled="true">← Prev</a>
  <a href="#" aria-current="page">1</a>
  <a href="#">2</a>
  <a href="#">3</a>
  <span>…</span>
  <a href="#" rel="next">Next →</a>
</nav>

<!-- Modern -->
<div class="library-loadmore">
  <button type="button" class="ml-button ml-button-secondary">Load more</button>
</div>
```

## 7. Footer

Same markup as the home page footer.
