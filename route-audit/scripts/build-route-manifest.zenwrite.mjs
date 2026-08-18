#!/usr/bin/env node
/**
 * build-route-manifest.mjs — ZenWrite / Movemental Studio
 *
 * Studio UI is NOT React Router path-based. Views are `/?view=<AppView>` from
 * `src/lib/viewAccents.ts`. Public HTML comes from Express `server/routes/reader.ts`
 * (+ vercel.json rewrites). This enumerator merges both surfaces into
 * `routes.manifest.yaml` WITHOUT clobbering human-authored assertions.
 *
 *   node scripts/build-route-manifest.mjs
 *   node scripts/build-route-manifest.mjs --dry
 *   node scripts/build-route-manifest.mjs --out routes.manifest.yaml
 *
 * Requires: yaml (already a workspace dep)
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? fallback : args[i + 1];
};
const OUT = path.resolve(ROOT, opt("out", "routes.manifest.yaml"));
const DRY = args.includes("--dry");

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), "utf8");
}

function normalise(p) {
  if (!p.startsWith("/")) p = "/" + p;
  return p.replace(/\/+$/, "") || "/";
}

/** AppView union members from viewAccents.ts */
function discoverAppViews() {
  const src = read("src/lib/viewAccents.ts");
  const block = src.match(/export type AppView\s*=\s*([\s\S]*?);/);
  if (!block) throw new Error("Could not parse AppView from src/lib/viewAccents.ts");
  const views = [...block[1].matchAll(/'\s*([^']+)\s*'/g)].map((m) => m[1]);
  if (!views.length) throw new Error("AppView union parsed empty");
  return views;
}

/** Static + dynamic public reader paths from reader.ts + vercel.json */
function discoverPublicPaths() {
  const found = new Map(); // path -> declared_in

  const reader = read("server/routes/reader.ts");
  const typeRoutes = {
    article: "/articles/:slug",
    book: "/books/:slug",
    podcast: "/podcast/:slug",
    video: "/video/:slug",
    newsletter: "/newsletter/:slug",
    lesson: "/lessons/:slug",
    course: "/courses/:slug",
  };
  for (const p of Object.values(typeRoutes)) {
    found.set(p, "server/routes/reader.ts");
  }
  found.set("/books/:slug/cited-works", "server/routes/reader.ts");

  for (const m of reader.matchAll(/readerRouter\.get\(\s*['`]([^'`]+)['`]/g)) {
    let p = m[1];
    // Skip template-literal interpolations (e.g. `/${pathSeg}/:slug`)
    if (p.includes("${")) continue;
    p = normalise(p.replace(/\/$/, "") || "/");
    if (p.startsWith("/api")) continue;
    found.set(p, "server/routes/reader.ts");
  }

  // Known public shells from vercel.json (exclude SPA catch-all and external proxies)
  const VERCEL_PUBLIC = [
    "/feeds",
    "/articles/:slug",
    "/books/:slug",
    "/podcast/:slug",
    "/video/:slug",
    "/newsletter/:slug",
    "/lessons/:slug",
    "/courses/:slug",
    "/themes/:slug",
    "/subscribe",
    "/pricing",
    "/library/books/:slug",
    "/formation/courses/:slug/sales",
    "/membership",
    "/bundles/:slug",
    "/access",
    "/checkout",
    "/success",
    "/cancel",
    "/account/purchases",
    "/licensing",
    "/sitemap.xml",
    "/robots.txt",
    "/auth/confirm",
  ];
  for (const p of VERCEL_PUBLIC) {
    if (!found.has(p)) found.set(p, "vercel.json");
  }

  // Feeds (separate router)
  for (const p of ["/feeds/articles.xml", "/feeds/newsletter.xml", "/feeds/podcast.xml"]) {
    found.set(p, "server/routes/feeds.ts");
  }

  return found;
}

function guessAuth(p, kind) {
  if (kind === "studio") {
    if (p.includes("view=admin") || p.includes("view=flow")) return "admin";
    return "required";
  }
  if (p.startsWith("/account/")) return "required";
  return "public";
}

function guessPhase(p, kind) {
  if (kind === "studio") {
    if (p === "/" || p.includes("view=home")) return "2-studio-home";
    if (/view=(create|organize|citations|collection|library|calendar)/.test(p)) {
      return "3-studio-content";
    }
    if (/view=(engage|programs|money|manage|analyze|communications)/.test(p)) {
      return "4-studio-community";
    }
    if (/view=(admin|flow|theme-review|sample-review)/.test(p)) return "6-studio-ops";
    if (/view=(book-reading|reading-preview|peer-invitation)/.test(p)) {
      return "5-studio-reading";
    }
    return "2-studio-home";
  }
  // public
  if (p.startsWith("/themes") || p.startsWith("/feeds") || p === "/sitemap.xml" || p === "/robots.txt") {
    return "1-public";
  }
  if (
    /^\/(articles|books|podcast|video|newsletter|lessons|courses)\b/.test(p)
  ) {
    return "7-public-content";
  }
  if (
    /^\/(subscribe|pricing|membership|access|checkout|success|cancel|licensing|library|formation|bundles|account)\b/.test(
      p,
    )
  ) {
    return "1-public";
  }
  return "1-public";
}

function seedFixtures(p) {
  if (!p.includes(":")) return [p];
  return [p.replace(/:([A-Za-z0-9_]+)/g, "REPLACE-ME-$1")];
}

function studioPath(view) {
  if (view === "home") return "/";
  return `/?view=${view}`;
}

// ------------------------------------------------------------------ discover

const views = discoverAppViews();
const publicPaths = discoverPublicPaths();
const discovered = new Map(); // path -> { declared_in, kind }

for (const view of views) {
  const p = studioPath(view);
  discovered.set(p, {
    declared_in: "src/lib/viewAccents.ts",
    kind: "studio",
    view,
  });
}

for (const [p, file] of publicPaths) {
  // Avoid colliding with studio "/"
  if (discovered.has(p) && discovered.get(p).kind === "studio") continue;
  discovered.set(p, { declared_in: file, kind: "public" });
}

let existing = { meta: {}, routes: [] };
if (fs.existsSync(OUT)) {
  existing = YAML.parse(fs.readFileSync(OUT, "utf8")) ?? existing;
}
const byPath = new Map((existing.routes ?? []).map((r) => [r.path, r]));

const merged = [];
const added = [];
for (const [p, meta] of [...discovered.entries()].sort((a, b) =>
  a[0].localeCompare(b[0]),
)) {
  const prev = byPath.get(p);
  const auth = prev?.auth ?? guessAuth(p, meta.kind);
  const phase = prev?.phase ?? guessPhase(p, meta.kind);
  const fixtures = prev?.fixtures?.length ? prev.fixtures : seedFixtures(p);

  if (prev) {
    merged.push({
      ...prev,
      path: p,
      auth,
      phase,
      fixtures,
      declared_in: meta.declared_in,
      surface: meta.kind,
      ...(meta.view ? { app_view: meta.view } : {}),
    });
  } else {
    added.push(p);
    merged.push({
      path: p,
      fixtures,
      auth,
      phase,
      must_render: [],
      must_not: ["console_errors", "network_failures"],
      declared_in: meta.declared_in,
      surface: meta.kind,
      ...(meta.view ? { app_view: meta.view } : {}),
    });
  }
}

const removed = [...byPath.keys()].filter((p) => !discovered.has(p));

const out = {
  meta: {
    ...(existing.meta ?? {}),
    base_url_hint: "http://localhost:3001",
    e2e_base_url_hint: "http://localhost:3011",
    router_sources: [
      "src/lib/viewAccents.ts",
      "server/routes/reader.ts",
      "vercel.json",
    ],
    generated_at: new Date().toISOString(),
    notes:
      "Studio routes use ?view= query params. Public HTML is Express reader + feeds.",
  },
  routes: merged,
};

console.log(`AppViews: ${views.length}`);
console.log(`Public paths: ${publicPaths.size}`);
console.log(`routes discovered: ${discovered.size}`);
console.log(`  new:     ${added.length}${added.length ? "\n    " + added.join("\n    ") : ""}`);
console.log(`  removed: ${removed.length}${removed.length ? "\n    " + removed.join("\n    ") : ""}`);

const byPhase = new Map();
for (const r of merged) {
  byPhase.set(r.phase, (byPhase.get(r.phase) ?? 0) + 1);
}
console.log("\nPhase grouping:");
for (const [ph, n] of [...byPhase.entries()].sort()) {
  console.log(`  ${ph}: ${n}`);
}

const needsFixtures = merged.filter((r) =>
  r.fixtures.some((f) => String(f).includes("REPLACE-ME")),
);
if (needsFixtures.length) {
  console.log(`\n⚠ ${needsFixtures.length} parameterised route(s) need real fixture URLs:`);
  for (const r of needsFixtures) console.log(`    ${r.path}`);
}

if (DRY) {
  console.log("\n--dry: nothing written.");
} else {
  fs.writeFileSync(OUT, YAML.stringify(out, { lineWidth: 100 }));
  console.log(`\nwrote ${OUT}`);
}
