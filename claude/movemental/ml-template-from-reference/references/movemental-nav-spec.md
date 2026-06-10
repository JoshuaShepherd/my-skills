# Movemental (Alan Hirsch-style) navigation — canonical spec

The navigation **structure** is fixed across every movement-leader template. **Styling** (color, typography, density, sticky behavior, search presence) adapts to the reference image. Link semantics, mobile behavior, and the login/CTA placement do not vary by leader.

This consistency lets a user move between movement leaders' sites and find the same affordances in the same places — a cross-leader trust signal, not just a design decision.

## Structure

```
[Logo / Wordmark]   Link · Link · Link · Link   [Log in] [Primary CTA]
```

### Logo

- Text wordmark of the leader's name (e.g., "Alan Hirsch", "Brad Brisco") **or** initials in a square mark if the visual style demands tight/compact navigation.
- Left-aligned. Always clickable. Always links to `index.html`.
- Font: use `--font-display` from the style spec.

### Primary links (4–6 maximum)

Default link set — use this unless the user specifies otherwise:

1. **Books** — leader's books index (placeholder `#` if not yet built)
2. **Articles** — written long-form, links to `articles.html`
3. **Library** — full content library, links to `library.html`
4. **Assessment** *(optional)* — if the leader has a signature assessment
5. **About** — leader bio (placeholder `#` if not yet built)

Adjust labels to match the leader's actual offerings; never reduce below 3 links or exceed 6. Common alternates: "Resources" instead of "Library", "Writing" instead of "Articles", "Speaking" / "Events" / "Cohorts" where relevant.

The `articles.html` and `library.html` links must always resolve to the templates in this scaffold. Other links can be `#`.

### Right-side actions

- **Log in** — ghost / text button. Always present, even if no auth backend exists yet.
- **Primary CTA** — single solid button. Label is the leader's main funnel action: "Take the assessment", "Read The Forgotten Ways", "Join the cohort", "Subscribe". Read from substrate, take from `--primary-cta` flag, or ask the user.

### Search

Optional. Include if the reference's density suggests it:

| Reference density | Search treatment |
|-------------------|------------------|
| Dense content-portal | Visible search field, center-left between logo and links (MasterClass pattern) |
| Modern marketing | Icon-only trigger that expands inline |
| Editorial / minimal | Omit |

## Mobile behavior

Below 768px:

- Logo stays left.
- Primary links collapse into a hamburger drawer (slide-in from right, full-screen overlay, or top-down accordion — match the motion vocabulary in the style spec).
- Primary CTA stays visible in the bar (use a compressed label if necessary, e.g., "Start" instead of "Take the assessment").
- Log in moves into the drawer along with the primary links.

Drawer animation choices:
- Modern → slide-in 250ms ease-out
- Editorial → fade 200ms ease
- Brutalist → instant (no transition)

## Sticky behavior

Default: sticky on scroll, with a subtle shadow when scrolled past 8px (toggle `.is-scrolled` via `js/main.js`).

Adapt to the reference:

| Reference vibe | Sticky treatment |
|----------------|------------------|
| Dense / utility | Always sticky, no shadow until scrolled |
| Editorial / magazine | Unsticky — lives at the top of the document |
| Brutalist | Sticky, hard 2px solid bottom border (no shadow) |
| Modern marketing | Sticky with shadow on scroll |

## HTML scaffold

```html
<header class="ml-nav" data-sticky="true">
  <a href="index.html" class="ml-nav-logo">{Leader Name}</a>

  <button class="ml-nav-toggle" aria-expanded="false" aria-controls="ml-nav-drawer">
    <span class="visually-hidden">Menu</span>
    <svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20">
      <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.5" fill="none" />
    </svg>
  </button>

  <nav class="ml-nav-links" id="ml-nav-drawer" aria-label="Primary">
    <a href="#">Books</a>
    <a href="articles.html">Articles</a>
    <a href="library.html">Library</a>
    <a href="#">Assessment</a>
    <a href="#">About</a>
  </nav>

  <div class="ml-nav-actions">
    <a href="#" class="ml-nav-link-ghost">Log in</a>
    <a href="#" class="ml-button ml-button-primary">{Primary CTA}</a>
  </div>
</header>
```

This markup appears identically on `index.html`, `library.html`, and `articles.html`. The current page is indicated by adding `aria-current="page"` to the matching link and styling it via `.ml-nav-links a[aria-current="page"]` in `components.css`.

## CSS class contract

The scaffold **must** produce these classes — downstream skills (auditors, refactors, React conversions) depend on them:

| Class | Role |
|-------|------|
| `.ml-nav` | Outer `<header>` bar |
| `.ml-nav[data-sticky="true"]` | Sticky variant; JS toggles `.is-scrolled` on scroll |
| `.ml-nav.is-scrolled` | Scrolled state — applies shadow/border |
| `.ml-nav-logo` | Logo / wordmark anchor |
| `.ml-nav-toggle` | Mobile hamburger button |
| `.ml-nav-links` | Container for primary links |
| `.ml-nav-links a[aria-current="page"]` | Current-page indicator |
| `.ml-nav-actions` | Container for login + CTA |
| `.ml-nav-link-ghost` | Text-only login link |
| `.ml-button.ml-button-primary` | Solid CTA |

Visual styling for these classes lives in `components.css`, driven by tokens from `tokens.css`. The class contract above never changes between leaders.

## JS contract — `js/main.js`

The nav requires two behaviors:

```js
// 1. Mobile toggle
const toggle = document.querySelector('.ml-nav-toggle');
const drawer = document.getElementById('ml-nav-drawer');
toggle?.addEventListener('click', () => {
  const expanded = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!expanded));
  drawer.classList.toggle('is-open', !expanded);
});

// 2. Sticky scroll state
const nav = document.querySelector('.ml-nav[data-sticky="true"]');
if (nav) {
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}
```

Anything beyond these two behaviors is style-spec-driven (reveal animations, etc.) and lives elsewhere in `main.js`.
