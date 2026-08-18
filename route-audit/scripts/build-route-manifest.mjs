#!/usr/bin/env node
/**
 * build-route-manifest.mjs
 *
 * Enumerate UI routes from a React Router source tree and merge them into
 * routes.manifest.yaml WITHOUT clobbering human-authored assertions.
 *
 * The mechanical half (path, auth, phase, fixtures) is regenerated.
 * The authored half (must_render, must_not, notes) is preserved verbatim.
 * That asymmetry is the point: a contract the generator rewrites is not a contract.
 *
 *   node scripts/build-route-manifest.mjs --src src --out routes.manifest.yaml
 *   node scripts/build-route-manifest.mjs --dry            # print the diff, write nothing
 *
 * Requires: yaml  (npm i -D yaml)
 */

import fs from "node:fs";
import path from "node:path";
import YAML from "yaml";

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? fallback : args[i + 1];
};
const SRC = opt("src", "src");
const OUT = opt("out", "routes.manifest.yaml");
const DRY = args.includes("--dry");

// ---------------------------------------------------------------- discovery

/** Files likely to declare routes. Cheap heuristic, then confirm by content. */
function candidateFiles(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (["node_modules", "dist", ".git", "__tests__"].includes(entry.name)) continue;
      candidateFiles(full, acc);
    } else if (/\.(tsx?|jsx?)$/.test(entry.name)) {
      acc.push(full);
    }
  }
  return acc;
}

/**
 * Extract route paths. Handles both JSX (<Route path="/x" />) and object
 * config ({ path: "/x", element: ... }).
 *
 * This is deliberately a regex pass, not an AST walk. It is fast, it is
 * good enough to enumerate, and — critically — its output is REVIEWED by a
 * human at the bootstrap checkpoint. If it misses a route, the reviewer
 * catches it. Silent completeness is not claimed.
 */
function extractRoutes(source) {
  const found = new Set();
  const jsx = /<Route\b[^>]*\bpath\s*=\s*["'`]([^"'`]+)["'`]/g;
  const obj = /\bpath\s*:\s*["'`]([^"'`]+)["'`]/g;
  for (const re of [jsx, obj]) {
    let m;
    while ((m = re.exec(source)) !== null) found.add(m[1]);
  }
  return [...found];
}

function normalise(p) {
  if (!p.startsWith("/")) p = "/" + p;
  return p.replace(/\/+$/, "") || "/";
}

// Routes that are not UI pages and should never enter the manifest.
const EXCLUDE = [/^\/api\b/, /^\*$/, /^\/\*/];

function isUiRoute(p) {
  return !EXCLUDE.some((re) => re.test(p));
}

// -------------------------------------------------------------- classifying

function guessAuth(p) {
  if (/^\/(admin|studio\/admin)/.test(p)) return "admin";
  if (/^\/(dashboard|account|settings|studio|editor|inbox)/.test(p)) return "required";
  return "public";
}

function guessPhase(p) {
  if (p === "/") return "1-public";
  const top = p.split("/")[1] ?? "";
  const map = {
    themes: "2-themes",
    pathways: "2-themes",
    library: "3-library",
    content: "3-library",
    courses: "4-formation",
    formation: "4-formation",
    about: "5-about",
    contact: "5-about",
    admin: "6-admin",
    dashboard: "7-dashboard",
    studio: "7-dashboard",
  };
  return map[top] ?? "1-public";
}

/** ":slug" style params get a placeholder fixture a human must replace. */
function seedFixtures(p) {
  if (!p.includes(":")) return [p];
  return [p.replace(/:([A-Za-z0-9_]+)/g, "REPLACE-ME-$1")];
}

// ------------------------------------------------------------------- merge

const files = candidateFiles(SRC);
const discovered = new Map();
for (const f of files) {
  const src = fs.readFileSync(f, "utf8");
  if (!/react-router|createBrowserRouter|<Route\b/.test(src)) continue;
  for (const raw of extractRoutes(src)) {
    const p = normalise(raw);
    if (!isUiRoute(p)) continue;
    if (!discovered.has(p)) discovered.set(p, f);
  }
}

let existing = { meta: {}, routes: [] };
if (fs.existsSync(OUT)) existing = YAML.parse(fs.readFileSync(OUT, "utf8")) ?? existing;
const byPath = new Map((existing.routes ?? []).map((r) => [r.path, r]));

const merged = [];
const added = [];
for (const [p, file] of [...discovered.entries()].sort()) {
  const prev = byPath.get(p);
  if (prev) {
    merged.push({
      ...prev,                       // authored fields survive untouched
      path: p,
      auth: prev.auth ?? guessAuth(p),
      phase: prev.phase ?? guessPhase(p),
      fixtures: prev.fixtures?.length ? prev.fixtures : seedFixtures(p),
      declared_in: file,
    });
  } else {
    added.push(p);
    merged.push({
      path: p,
      fixtures: seedFixtures(p),
      auth: guessAuth(p),
      phase: guessPhase(p),
      must_render: [],
      must_not: ["console_errors", "network_failures"],
      declared_in: file,
    });
  }
}

const removed = [...byPath.keys()].filter((p) => !discovered.has(p));

const out = {
  meta: {
    ...(existing.meta ?? {}),
    router_sources: [...new Set([...discovered.values()])],
    generated_at: new Date().toISOString(),
  },
  routes: merged,
};

// ------------------------------------------------------------------ report

console.log(`scanned ${files.length} files`);
console.log(`routes discovered: ${discovered.size}`);
console.log(`  new:     ${added.length}${added.length ? "\n    " + added.join("\n    ") : ""}`);
console.log(`  removed: ${removed.length}${removed.length ? "\n    " + removed.join("\n    ") : ""}`);

const needsFixtures = merged.filter((r) =>
  r.fixtures.some((f) => f.includes("REPLACE-ME")),
);
if (needsFixtures.length) {
  console.log(`\n⚠ ${needsFixtures.length} parameterised route(s) need real fixture URLs:`);
  for (const r of needsFixtures) console.log(`    ${r.path}`);
}
const unasserted = merged.filter((r) => !(r.must_render?.length));
if (unasserted.length) {
  console.log(`\n⚠ ${unasserted.length} route(s) have no must_render assertions yet.`);
}

if (removed.length) {
  console.log(
    `\nNote: removed routes are NOT deleted from ${OUT} automatically — ` +
      `mark them deferred in state.json with a reason, then remove by hand.`,
  );
}

if (DRY) {
  console.log("\n--dry: nothing written.");
} else {
  fs.writeFileSync(OUT, YAML.stringify(out, { lineWidth: 100 }));
  console.log(`\nwrote ${OUT}`);
}
