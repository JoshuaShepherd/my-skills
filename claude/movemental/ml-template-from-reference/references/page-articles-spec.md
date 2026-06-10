# Articles page spec — `articles.html`

The editorial index — separates the leader's written long-form from the broader library.

## 1. Nav

Per [movemental-nav-spec.md](movemental-nav-spec.md). Mark the "Articles" link with `aria-current="page"`.

## 2. Articles hero (editorial header)

The most typographic of the three heroes — usually text-only or with a single small ornament.

```html
<header class="ml-hero ml-hero--text-only ml-hero--editorial">
  <div class="ml-hero-inner">
    <p class="ml-hero-eyebrow">Writing</p>
    <h1 class="ml-hero-title">{One-sentence editorial promise}</h1>
    <p class="ml-hero-tagline">{Optional cadence note — e.g., "New essays monthly. Long-form, not feed-shaped."}</p>
  </div>
</header>
```

If the reference's style spec marked decorative motifs (hairline rules, double rules, ornaments), apply them here — this hero is where typographic restraint earns its decoration.

## 3. Featured article

A large lead card (50–60% page width on desktop). The visual centerpiece of the index.

```html
<section class="articles-featured" aria-labelledby="featured-article-title">
  <article class="ml-card ml-card--featured-article">
    <div class="ml-card-media">
      <img src="images/cover-placeholder-1.webp" alt="" />
    </div>
    <div class="ml-card-body">
      <span class="ml-card-meta">{Topic} · Featured</span>
      <h2 id="featured-article-title" class="ml-card-title">{Article title — placeholder}</h2>
      <p class="ml-card-desc">{2–3 line excerpt.}</p>
      <div class="ml-card-byline">
        <span>{Author name}</span>
        <span>·</span>
        <time datetime="2026-01-01">{Date}</time>
        <span>·</span>
        <span>{N} min read</span>
      </div>
      <a href="#" class="ml-card-cta">Read article →</a>
    </div>
  </article>
</section>
```

The featured card may be image-side, image-top, or image-background depending on the style spec's card construction field.

## 4. Topic filter chips (optional)

If the leader's articles cluster topically (mDNA, formation, APEST, leadership, etc.), surface chips. Use the same `.ml-filter-chip` vocabulary as the library page.

```html
<nav class="ml-filter-chips" aria-label="Topic">
  <button type="button" class="ml-filter-chip is-active" data-topic="all">All</button>
  <button type="button" class="ml-filter-chip" data-topic="mdna">mDNA</button>
  <button type="button" class="ml-filter-chip" data-topic="formation">Formation</button>
  <button type="button" class="ml-filter-chip" data-topic="apest">APEST</button>
  <button type="button" class="ml-filter-chip" data-topic="movement">Movement</button>
</nav>
```

Omit this section if the leader's writing doesn't cluster cleanly.

## 5. Article grid

Equal-weight cards for the rest of the articles.

```html
<section class="articles-grid" aria-label="Articles">
  <article class="ml-card ml-card--article" data-topic="mdna">
    <div class="ml-card-media">
      <img src="images/cover-placeholder-2.webp" alt="" loading="lazy" />
    </div>
    <div class="ml-card-body">
      <span class="ml-card-meta">{Topic} · {N} min read</span>
      <h3 class="ml-card-title">{Article title}</h3>
      <p class="ml-card-desc">{Excerpt.}</p>
      <div class="ml-card-byline">
        <time datetime="2026-01-01">{Date}</time>
      </div>
    </div>
  </article>
  <!-- ×6-9 -->
</section>
```

Grid layout follows the style spec:

| Density / style | Layout |
|-----------------|--------|
| `sparse` / editorial | 2 columns desktop, 1 mobile |
| `balanced` / modern | 3 columns desktop, 2 tablet, 1 mobile |
| Brutalist / list-style | Stacked rows, single column, hard rules |

Card construction (image-top vs image-side vs no-image) follows the style spec's card construction field. For a magazine reference with image-side cards, the grid switches to single column on tablet to preserve the side-by-side layout.

## 6. Sidebar (layout-dependent)

If the style spec's composition tendency is `multi-column editorial`:

```html
<aside class="articles-sidebar" aria-label="Article navigation">
  <section class="articles-sidebar-block">
    <h3>Trending</h3>
    <ol class="articles-sidebar-list">
      <li><a href="#">{Title}</a><span class="ml-card-meta">{N} min</span></li>
      <!-- ×5 -->
    </ol>
  </section>
  <section class="articles-sidebar-block">
    <h3>Get new essays in your inbox</h3>
    <form onsubmit="event.preventDefault()">
      <label class="visually-hidden" for="sidebar-newsletter-email">Email</label>
      <input id="sidebar-newsletter-email" type="email" placeholder="you@example.com" required />
      <button type="submit" class="ml-button ml-button-primary">Subscribe</button>
    </form>
  </section>
</aside>
```

On desktop, the sidebar is sticky alongside the article grid. On mobile, it drops below the grid.

If the style spec indicates a single-column / modern grid, **omit the sidebar entirely** and use a standalone newsletter section between the grid and the footer instead (same markup as the home page newsletter).

## 7. Pagination

Numbered for editorial references; "Load more" for modern; none for brutalist. Same control vocabulary as the library page.

## 8. Footer

Same markup as the home page footer.

## Layout composition

The page wrapper composes the featured article, grid, and optional sidebar:

```html
<main class="articles-page" data-layout="{single | sidebar}">
  <!-- featured -->
  <!-- topic chips (optional) -->
  <div class="articles-body">
    <!-- grid -->
    <!-- sidebar (if data-layout="sidebar") -->
  </div>
  <!-- pagination -->
</main>
```

`.articles-page[data-layout="sidebar"] .articles-body` uses `grid-template-columns: 1fr 18rem` on desktop. `.articles-page[data-layout="single"] .articles-body` is a single column with the grid full-width.
