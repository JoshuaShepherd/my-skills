# Home page spec — `index.html`

Canonical section order. Skip a section only if the reference image clearly implies its absence (e.g., a stark editorial reference might omit "personas"). Every skipped section gets a row in `_reference/NOTES.md` under "Sections deliberately omitted" with the reason.

## 1. Nav

Per [movemental-nav-spec.md](movemental-nav-spec.md). On the home page the logo's anchor is non-functional (it points to the same page), and no nav link is marked `aria-current="page"`.

## 2. Hero

The hero is the strongest carrier of the reference's aesthetic. It **must** visibly match the reference's hero pattern as captured in the style spec.

Required content:
- Eyebrow — small uppercase label or kicker line (e.g., "Missional theology · Formation · Movement")
- Headline (`h1`) — the leader's positioning sentence
- Tagline / dek — one short paragraph (1–2 lines)
- Primary CTA + Secondary CTA — both omittable if the reference is text-only editorial
- Hero image (placeholder OK — use `images/hero-placeholder.{ext}` and document in NOTES.md)

HTML scaffold:

```html
<header class="ml-hero ml-hero--{pattern}">
  <!-- pattern: bleed-overlay | split | portrait-dominant | art-bg-portrait-fg | text-only | editorial-stack -->
  <div class="ml-hero-media">
    <img src="images/hero-placeholder.webp" alt="" />
  </div>
  <div class="ml-hero-inner">
    <p class="ml-hero-eyebrow">{eyebrow}</p>
    <h1 class="ml-hero-title">{headline}</h1>
    <p class="ml-hero-tagline">{tagline}</p>
    <div class="ml-hero-ctas">
      <a class="ml-button ml-button-primary" href="#">{primary CTA}</a>
      <a class="ml-button ml-button-ghost" href="#">{secondary CTA}</a>
    </div>
  </div>
</header>
```

Pattern-specific CSS rules live in `components.css`. Examples:
- `.ml-hero--bleed-overlay` — absolute-positioned `.ml-hero-media` with `.ml-hero-inner` overlaying via gradient scrim
- `.ml-hero--split` — `grid-template-columns: 1fr 1fr` with media one side, content the other
- `.ml-hero--text-only` — no `.ml-hero-media` element rendered; `.ml-hero-inner` centered with generous vertical padding

## 3. Featured quote

A single pull quote from the leader. Use placeholder copy clearly labeled `Placeholder until substrate is provided.` if no substrate is supplied.

Visual treatment varies by reference:
- Editorial → large serif quote with hairline rule above/below
- Modern → quote with ornamental quotation-mark glyph or accent color block to the left
- Brutalist → all-caps quote, no decoration, hard slab type

```html
<section class="ml-quote" aria-labelledby="featured-quote-heading">
  <h2 id="featured-quote-heading" class="visually-hidden">Featured quote</h2>
  <blockquote class="ml-quote-text">"{quote}"</blockquote>
  <cite class="ml-quote-cite">— {Leader Name}, <em>{Work}</em></cite>
</section>
```

## 4. Personas / "Find your path"

A 3–4 card strip of audience routes. Omit if the reference is clearly single-audience.

Default personas (adjust to leader): Leaders / Practitioners / Learners / Communities.

```html
<section class="ml-section" id="personas" aria-labelledby="personas-title">
  <h2 id="personas-title" class="ml-section-title">Find your path</h2>
  <p class="ml-section-desc">Whether you're a leader, practitioner, or learner, start here.</p>
  <div class="home-personas-grid">
    <a href="#" class="ml-card ml-card--persona">
      <div class="ml-card-icon" aria-hidden="true">◇</div>
      <h3 class="ml-card-title">Leaders</h3>
      <p class="ml-card-desc">Strategy, movement, systems</p>
    </a>
    <!-- repeat -->
  </div>
</section>
```

Icon glyphs (◇ ○ △ □) are placeholders — replace with the reference's iconography vocabulary or omit entirely if the reference uses no icons.

## 5. Theme portals / "Explore by theme"

A grid (3 across desktop, 2 across tablet, 1 across mobile) of portal cards linking to themes the leader is known for.

```html
<section class="ml-section" id="exploration" aria-labelledby="exploration-title">
  <h2 id="exploration-title" class="ml-section-title">Explore by theme</h2>
  <p class="ml-section-desc">Portals into {theme A}, {theme B}, {theme C}.</p>
  <div class="home-portals-grid">
    <a href="#" class="ml-card ml-card--portal">
      <div class="ml-card-media">
        <img src="images/cover-placeholder-1.webp" alt="" loading="lazy" />
      </div>
      <div class="ml-card-body">
        <span class="ml-card-meta">Portal</span>
        <h3 class="ml-card-title">{Theme name}</h3>
        <p class="ml-card-desc">{One-line description.}</p>
      </div>
    </a>
    <!-- repeat 3-6 times -->
  </div>
</section>
```

## 6. Featured book / signature work

Large card or split section featuring the leader's magnum opus.

```html
<section class="ml-section home-featured-book" id="featured-book" aria-labelledby="featured-book-title">
  <div class="home-featured-book-media">
    <img src="images/cover-placeholder-book.webp" alt="" />
  </div>
  <div class="home-featured-book-body">
    <span class="ml-card-meta">Signature work</span>
    <h2 id="featured-book-title" class="ml-section-title">{Book title}</h2>
    <p>{One- or two-paragraph description. Placeholder until substrate is provided.}</p>
    <a class="ml-button ml-button-primary" href="#">Read the book</a>
  </div>
</section>
```

## 7. Pathway / Assessment CTA

A wide banner-style section calling the user into the leader's primary funnel action. Mirrors the nav's primary CTA but with context.

```html
<section class="ml-section home-pathway" id="pathway" aria-labelledby="pathway-title">
  <h2 id="pathway-title" class="ml-section-title">{CTA headline}</h2>
  <p>{One-paragraph description of what the assessment / pathway delivers.}</p>
  <a class="ml-button ml-button-primary" href="#">{Primary CTA label}</a>
</section>
```

## 8. Latest articles strip

A 3-card horizontal strip of recent articles. Links to `articles.html`.

```html
<section class="ml-section" id="latest-articles" aria-labelledby="latest-articles-title">
  <div class="ml-section-header">
    <h2 id="latest-articles-title" class="ml-section-title">Latest articles</h2>
    <a class="ml-section-more" href="articles.html">See all articles →</a>
  </div>
  <div class="home-articles-strip">
    <article class="ml-card ml-card--article">
      <div class="ml-card-media">
        <img src="images/cover-placeholder-2.webp" alt="" loading="lazy" />
      </div>
      <div class="ml-card-body">
        <span class="ml-card-meta">{Topic} · {N min read}</span>
        <h3 class="ml-card-title">{Article title — placeholder}</h3>
        <p class="ml-card-desc">{Excerpt.}</p>
      </div>
    </article>
    <!-- repeat ×3 -->
  </div>
</section>
```

## 9. Newsletter signup

Email-only form, single field + button. Button matches the reference's button vocabulary.

```html
<section class="ml-section home-newsletter" id="newsletter" aria-labelledby="newsletter-title">
  <h2 id="newsletter-title" class="ml-section-title">Stay in the conversation</h2>
  <p>{One-line value prop.}</p>
  <form class="home-newsletter-form" onsubmit="event.preventDefault()">
    <label class="visually-hidden" for="newsletter-email">Email address</label>
    <input id="newsletter-email" type="email" placeholder="you@example.com" required />
    <button type="submit" class="ml-button ml-button-primary">Subscribe</button>
  </form>
</section>
```

`onsubmit="event.preventDefault()"` keeps the form inert in the template — no backend wired up.

## 10. Footer

A wide footer with: leader wordmark, social links, link columns (Resources / About / Legal), and a copyright line. Tone matches the reference (dense utility vs sparse editorial).

```html
<footer class="ml-footer">
  <div class="ml-footer-inner">
    <div class="ml-footer-brand">
      <span class="ml-footer-wordmark">{Leader Name}</span>
      <p class="ml-footer-tagline">{Short positioning line.}</p>
    </div>
    <div class="ml-footer-cols">
      <div class="ml-footer-col">
        <h3>Resources</h3>
        <a href="library.html">Library</a>
        <a href="articles.html">Articles</a>
        <a href="#">Books</a>
      </div>
      <div class="ml-footer-col">
        <h3>About</h3>
        <a href="#">Bio</a>
        <a href="#">Speaking</a>
        <a href="#">Contact</a>
      </div>
      <div class="ml-footer-col">
        <h3>Legal</h3>
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
      </div>
    </div>
  </div>
  <div class="ml-footer-bottom">
    <small>© {YYYY} {Leader Name}. All rights reserved.</small>
  </div>
</footer>
```
