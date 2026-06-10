---
name: seo-setup
description: "Set up SEO infrastructure for Next.js 15 — Metadata API (title, description, OG, Twitter), dynamic sitemap.xml, robots.txt, structured data (JSON-LD), canonical URLs, and OG image generation via Next.js ImageResponse. Use when launching any public-facing page or site."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up SEO infrastructure: $ARGUMENTS

$ARGUMENTS can include:
- "audit" — scan existing pages for missing metadata and fix
- "full" — complete setup: metadata + sitemap + robots + structured data + OG images (default)
- "metadata-only" — just the metadata patterns, no sitemap or OG images
- "with-blog" — include article/blog structured data patterns
- Empty — full setup

---

## Before Starting

1. Read `src/app/layout.tsx` — check existing metadata config
2. Read `src/lib/config/tenant.config.ts` — get brand name, description, domain
3. Read `src/lib/env.ts` — check for `NEXT_PUBLIC_APP_URL`
4. Read `src/app/(public)/` — catalog all public pages that need metadata
5. Check if `src/app/sitemap.ts` or `src/app/robots.ts` already exist

---

## Architecture

```
src/app/
  layout.tsx               ← Root metadata (title template, OG defaults)
  sitemap.ts               ← Dynamic sitemap — fetches all public URLs
  robots.ts                ← robots.txt
  opengraph-image.tsx      ← Default OG image (Next.js ImageResponse)
  (public)/
    page.tsx               ← Per-page metadata via generateMetadata()
    articles/[slug]/
      page.tsx             ← Dynamic metadata from DB
      opengraph-image.tsx  ← Per-article OG image

src/lib/seo/
  metadata.ts              ← buildMetadata() helper
  structured-data.ts       ← JSON-LD builders (Article, Person, Organization)
  og-image.ts              ← OG image generation helpers
```

---

## Step 1 — Root Layout Metadata

Edit `src/app/layout.tsx` — add `metadata` export:

```typescript
import type { Metadata } from "next";
import { tenantConfig } from "@/lib/config/tenant.config";

const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://yourdomain.com";

export const metadata: Metadata = {
  metadataBase: new URL(APP_URL),

  title: {
    default: tenantConfig.name,
    template: `%s | ${tenantConfig.name}`,
  },

  description: tenantConfig.tagline,

  openGraph: {
    type: "website",
    siteName: tenantConfig.name,
    title: tenantConfig.name,
    description: tenantConfig.tagline,
    url: APP_URL,
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: tenantConfig.name,
      },
    ],
  },

  twitter: {
    card: "summary_large_image",
    title: tenantConfig.name,
    description: tenantConfig.tagline,
    images: ["/opengraph-image"],
  },

  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large" },
  },

  alternates: {
    canonical: APP_URL,
  },
};
```

---

## Step 2 — buildMetadata Helper

Create `src/lib/seo/metadata.ts`:

```typescript
import type { Metadata } from "next";
import { tenantConfig } from "@/lib/config/tenant.config";

const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://yourdomain.com";

interface BuildMetadataOptions {
  title: string;
  description?: string;
  path?: string;           // e.g. "/articles/my-article"
  image?: string;          // Absolute URL or path
  noIndex?: boolean;
  type?: "website" | "article";
  publishedAt?: string;    // ISO date for articles
  authors?: string[];
}

export function buildMetadata(opts: BuildMetadataOptions): Metadata {
  const {
    title,
    description = tenantConfig.tagline,
    path = "",
    image = "/opengraph-image",
    noIndex = false,
    type = "website",
    publishedAt,
    authors,
  } = opts;

  const url = `${APP_URL}${path}`;
  const imageUrl = image.startsWith("http") ? image : `${APP_URL}${image}`;

  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      type,
      title,
      description,
      url,
      siteName: tenantConfig.name,
      images: [{ url: imageUrl, width: 1200, height: 630, alt: title }],
      ...(publishedAt && { publishedTime: publishedAt }),
      ...(authors && { authors }),
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [imageUrl],
    },
    robots: noIndex
      ? { index: false, follow: false }
      : { index: true, follow: true },
  };
}
```

---

## Step 3 — Per-Page Metadata (static)

Example for a static public page:

```typescript
// src/app/(public)/about/page.tsx
import { buildMetadata } from "@/lib/seo/metadata";

export const metadata = buildMetadata({
  title: "About",
  description: "Learn about our mission and approach.",
  path: "/about",
});

export default function AboutPage() { ... }
```

---

## Step 4 — Dynamic Metadata (from DB)

For dynamic routes like `/articles/[slug]`:

```typescript
// src/app/(public)/articles/[slug]/page.tsx
import { buildMetadata } from "@/lib/seo/metadata";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const article = await getArticleBySlug(slug); // your service

  if (!article) return buildMetadata({ title: "Not found", noIndex: true });

  return buildMetadata({
    title: article.title,
    description: article.excerpt ?? undefined,
    path: `/articles/${slug}`,
    image: article.heroImageUrl ?? undefined,
    type: "article",
    publishedAt: article.publishedAt?.toISOString(),
    authors: [article.authorName],
  });
}
```

---

## Step 5 — Default OG Image

Create `src/app/opengraph-image.tsx`:

```typescript
import { ImageResponse } from "next/og";
import { tenantConfig } from "@/lib/config/tenant.config";

export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          height: "100%",
          backgroundColor: "#000",
          color: "#fff",
          fontFamily: "sans-serif",
          padding: "60px",
        }}
      >
        <div style={{ fontSize: 72, fontWeight: 700, marginBottom: 24 }}>
          {tenantConfig.name}
        </div>
        <div style={{ fontSize: 32, opacity: 0.7, textAlign: "center" }}>
          {tenantConfig.tagline}
        </div>
      </div>
    ),
    size
  );
}
```

For custom fonts, load via `fetch()` in the ImageResponse function.

---

## Step 6 — Dynamic Sitemap

Create `src/app/sitemap.ts`:

```typescript
import type { MetadataRoute } from "next";
import { db } from "@/lib/database/db";
import { articles, courses, frameworks } from "@/lib/database/schema";
import { eq } from "drizzle-orm";
import { getTenantOrgId } from "@/lib/tenant";

const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://yourdomain.com";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const orgId = getTenantOrgId();

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    { url: APP_URL, lastModified: new Date(), changeFrequency: "weekly", priority: 1 },
    { url: `${APP_URL}/about`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: `${APP_URL}/articles`, lastModified: new Date(), changeFrequency: "daily", priority: 0.9 },
  ];

  // Dynamic: articles
  const articleRows = await db
    .select({ slug: articles.slug, updatedAt: articles.updatedAt })
    .from(articles)
    .where(eq(articles.organizationId, orgId));

  const articlePages: MetadataRoute.Sitemap = articleRows.map((a) => ({
    url: `${APP_URL}/articles/${a.slug}`,
    lastModified: a.updatedAt ?? new Date(),
    changeFrequency: "weekly",
    priority: 0.7,
  }));

  return [...staticPages, ...articlePages];
}
```

---

## Step 7 — robots.txt

Create `src/app/robots.ts`:

```typescript
import type { MetadataRoute } from "next";

const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://yourdomain.com";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/account/",
          "/admin/",
          "/_next/",
        ],
      },
    ],
    sitemap: `${APP_URL}/sitemap.xml`,
  };
}
```

---

## Step 8 — Structured Data (JSON-LD)

Create `src/lib/seo/structured-data.ts`:

```typescript
import { tenantConfig } from "@/lib/config/tenant.config";

const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? "https://yourdomain.com";

export function buildOrganizationLD() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: tenantConfig.name,
    url: APP_URL,
    description: tenantConfig.tagline,
  };
}

export function buildArticleLD(article: {
  title: string;
  description?: string;
  slug: string;
  publishedAt?: Date;
  updatedAt?: Date;
  authorName?: string;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: article.title,
    description: article.description,
    url: `${APP_URL}/articles/${article.slug}`,
    datePublished: article.publishedAt?.toISOString(),
    dateModified: article.updatedAt?.toISOString(),
    author: article.authorName
      ? { "@type": "Person", name: article.authorName }
      : undefined,
    publisher: { "@type": "Organization", name: tenantConfig.name },
  };
}
```

Inject in page components:
```typescript
import { buildArticleLD } from "@/lib/seo/structured-data";

export default function ArticlePage({ article }) {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(buildArticleLD(article)) }}
      />
      {/* page content */}
    </>
  );
}
```

---

## Verify

1. `pnpm typecheck` — no metadata errors
2. `pnpm dev` — visit `/sitemap.xml` → valid XML with all URLs
3. Visit `/robots.txt` → correct disallow rules
4. Open DevTools → Network → see correct OG tags in `<head>`
5. Use [Open Graph Debugger](https://developers.facebook.com/tools/debug/) on a deployed URL
6. Use [Google Rich Results Test](https://search.google.com/test/rich-results) for JSON-LD

---

## Anti-Patterns

- NEVER use `<Head>` from `next/head` in App Router — use `metadata` exports
- NEVER set `noIndex: true` on pages you want indexed
- NEVER hardcode the domain — always use `NEXT_PUBLIC_APP_URL` env var
- NEVER skip `metadataBase` in root layout — relative OG image URLs break without it
- NEVER generate sitemap from static data only — fetch from DB for accuracy
