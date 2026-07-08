# Obvious Players — Content Source Checklist

The comprehensiveness contract for `movement-leader-content-harvest`. Every category must be
**checked** and its result recorded in `content/sources-swept.md` — either found items or an
explicit "checked, none found." **Books are out of scope everywhere on this list.**

For each category: run the searches, then follow the leader's own channel/feed/archive to
enumerate items **exhaustively** (not just page one). Substitute the leader's name and known
aliases/handles for `{name}` / `{alias}` / `{site}`.

---

## 1. Owned websites & blogs
- `{name}` official site; `{alias}` blog; `{name} blog`
- Enumerate via `sitemap.xml`, `/feed`, `/rss`, archive/date pages, category pages
- Legacy/defunct blogs (Blogger/blogspot, WordPress.com, Typepad, Squarespace) — often **FETCH** (fragile)
- Wayback Machine (`web.archive.org`) for dead domains and deleted posts
- **Disposition bias:** owned + old/at-risk primary text → FETCH

## 2. YouTube
- Channel(s): `youtube.com/@{alias}`, legacy `/user/…`, `/c/…`; resolve to channel ID
- Enumerate uploads via the channel RSS: `https://www.youtube.com/feeds/videos.xml?channel_id=…` and the uploads playlist
- Guest/third-party appearances: `{name}` interview / sermon / talk / keynote
- `yt-dlp` (if present) for metadata + auto-captions → TRANSCRIBE
- **Bias:** own videos on a live channel → LINK (+ TRANSCRIBE for the words)

## 3. Vimeo
- `vimeo.com/{user}`, showcases, org accounts that host their talks
- Cross-check against YouTube — same talk often on both → merge, list alt URL

## 4. Podcasts — as host
- Show on Apple Podcasts (capture the `id…`), Spotify, Podbay, Overcast, Pocket Casts
- The show's **RSS feed** enumerates every episode → catalog all; TRANSCRIBE primary ones

## 5. Podcasts — as guest
- `{name}` podcast interview / guest / episode
- Host-side pages (the outlet's episode page is the canonical link)
- Common hosts in this space: Theology in the Raw, Shifting Culture, Missio Alliance, Exponential / Future Church, Everyday Disciple, Verge, New Churches, Carey Nieuwhof

## 6. Standalone audio & sermons
- Sermon archives (church site, SermonAudio, Vimeo/YouTube audio), talk recordings, audio courses
- Conference audio (see Talks)

## 7. Talks, conferences & events
- `{name}` keynote / session / plenary / workshop + conference names from the network dossier
- Exponential, Missio Alliance, Verge, Lausanne, Forge, Greenbelt, denominational gatherings
- Often audio/video elsewhere → link the recording, note the event even when no recording is recoverable

## 8. Journals, magazines & ministry outlets (articles)
- **Author-archive pages** (enumerate all pages): Outreach Magazine, ChurchLeaders, Missio Alliance, Christianity Today, Relevant, Missio Publishing blog, Verge Network, Exponential, 100 Movements, V3, denominational magazines
- `{name}` site:outreachmagazine.com (and each outlet); `{name}` author archive
- **Bias:** live outlet → LINK; defunct outlet or PDF-only → FETCH

## 9. Academic & scholarly
- Google Scholar, academia.edu, ResearchGate, ORCID, JSTOR, ATLA, institutional repositories
- Journal articles, dissertations, book chapters in edited volumes (chapter = article-like, IN scope; the whole book = out of scope), conference papers
- PDFs → usually FETCH (fragile, primary)

## 10. Newsletters & Substack
- Substack (`{alias}.substack.com` — enumerate the archive), Beehiiv, Mailchimp/ConvertKit web archives, Ghost
- Owned long-form → often FETCH

## 11. Long-form social & syndication
- Medium (`medium.com/@{alias}`), LinkedIn articles/newsletters, Patreon posts, Ghost
- Note: short social posts (tweets/IG captions) are generally SKIP unless they are the only home of substantive content
- Threads/X long posts only if they carry real content

## 12. Online courses & teaching
- Course platforms (Teachable, Thinkific, Podia, Kajabi), org LMS, cohort/masterclass pages
- Free lesson content → catalog; gated → LINK + note access

## 13. Interviews & features (text)
- `{name}` interview (magazine/blog Q&A), profile features, guest posts on others' blogs
- Distinct from podcast interviews (category 5)

## 14. Aggregators & disambiguation backstop
- Wikipedia, Goodreads *author page* (for the profile/handles only — **not** to catalog books here), personal Linktree/link-in-bio, org staff/contributor pages
- Use these to discover channels you missed and to confirm identity — then loop back through the relevant category above

---

## Recording rules
- **One row per canonical item**; merge cross-platform copies with alternate URLs.
- Capture: title, type, date (or "—"), canonical URL, alt URLs, host/outlet, is-primary (their own words vs. about them), disposition, notes.
- A **book** encountered anywhere → `books-seen.md`, not the content inventory.
- Every category ends with a one-line coverage note in `sources-swept.md`.
