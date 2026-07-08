#!/usr/bin/env tsx
/**
 * movemental-site-template-publish — preview asset builder.
 *
 * Renders a standalone template HTML, screenshots desktop + mobile previews,
 * uploads them to the `template-previews` Storage bucket, verifies the public
 * URLs, and prints a ready-to-paste `preview_manifest` / `design_tokens` /
 * `hero_config` block for the front_end_templates seed row.
 *
 * Run FROM THE REPO ROOT so node resolves @playwright/test + @supabase/supabase-js:
 *   cp .claude/skills/movemental-site-template-publish/scripts/publish-stitch-template-assets.ts scripts/
 *   pnpm exec playwright install chromium   # once, if needed
 *   pnpm tsx scripts/publish-stitch-template-assets.ts --slug <slug> [--html <path>] [--no-mobile]
 *
 * Requires NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY in .env.local.
 */
import { readFileSync, mkdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { parseArgs } from "node:util";

import { createClient } from "@supabase/supabase-js";
import { chromium } from "@playwright/test";
import { config } from "dotenv";

config({ path: ".env.local" });
config({ path: ".env" });

const BUCKET = "template-previews";

const { values } = parseArgs({
  options: {
    slug: { type: "string" },
    html: { type: "string" },
    "no-mobile": { type: "boolean", default: false },
  },
});

const slug = values.slug;
if (!slug || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
  console.error("Missing or invalid --slug (kebab-case, e.g. quiet-editorial)");
  process.exit(1);
}

const htmlPath = resolve(values.html ?? `docs/html/templates/${slug}/index.html`);
const outDir = resolve(`docs/html/templates/${slug}/.previews`);
mkdirSync(outDir, { recursive: true });

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

function publicUrl(path: string): string {
  const base = (SUPABASE_URL ?? "").replace(/\/$/, "");
  return `${base}/storage/v1/object/public/${BUCKET}/${path}`;
}

type Screen = {
  key: string;
  label: string;
  device: "desktop" | "mobile";
  width: number;
  height: number;
  file: string;
};

async function main() {
  if (!SUPABASE_URL || !SERVICE_KEY) {
    console.error(
      "Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env.local.\n" +
        "Cannot upload to Storage. Fall back to placeholder image URLs in the seed row\n" +
        "(see SKILL.md step 4) or add the service-role key and re-run.",
    );
    process.exit(2);
  }

  const screens: Screen[] = [
    { key: "home-desktop", label: "Home", device: "desktop", width: 1440, height: 900, file: join(outDir, "home-desktop.png") },
  ];
  if (!values["no-mobile"]) {
    screens.push({ key: "home-mobile", label: "Home (mobile)", device: "mobile", width: 390, height: 844, file: join(outDir, "home-mobile.png") });
  }

  // 1. Render screenshots
  const fileUrl = `file://${htmlPath}`;
  // Allow an explicit Chromium path (e.g. when `playwright install` can't fetch the
  // pinned build on a bleeding-edge OS but a compatible build is already cached).
  const exe = process.env.PLAYWRIGHT_CHROMIUM_PATH?.trim();
  const browser = await chromium.launch(exe ? { executablePath: exe } : undefined);
  try {
    for (const s of screens) {
      const page = await browser.newPage({
        viewport: { width: s.width, height: s.height },
        deviceScaleFactor: 2,
      });
      await page.goto(fileUrl, { waitUntil: "networkidle" });
      // Let webfonts + Tailwind CDN settle.
      await page.waitForTimeout(600);
      await page.screenshot({ path: s.file }); // viewport crop (not fullPage) → hero-forward thumbnail
      await page.close();
      console.log(`rendered ${s.key} → ${s.file}`);
    }
  } finally {
    await browser.close();
  }

  // 2. Upload PNGs + the reference HTML
  const supabase = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const uploaded: { path: string; url: string }[] = [];

  async function upload(storagePath: string, body: Buffer, contentType: string) {
    const { error } = await supabase.storage.from(BUCKET).upload(storagePath, body, {
      contentType,
      cacheControl: "3600",
      upsert: true,
    });
    if (error) {
      console.error(`upload failed ${storagePath}: ${error.message}`);
      process.exit(1);
    }
    const url = publicUrl(storagePath);
    uploaded.push({ path: storagePath, url });
    console.log(`uploaded ${storagePath}`);
  }

  for (const s of screens) {
    await upload(`${slug}/${s.key}.png`, readFileSync(s.file), "image/png");
  }
  await upload(`${slug}/home-desktop.html`, readFileSync(htmlPath), "text/html; charset=utf-8");

  // 3. Verify public URLs
  console.log("\nverifying public URLs (expect 200)…");
  for (const u of uploaded) {
    const res = await fetch(u.url, { method: "HEAD" });
    if (!res.ok) {
      console.error(`FAIL ${u.path}: HTTP ${res.status}`);
      process.exit(1);
    }
    console.log(`200 ${u.url}`);
  }

  // 4. Emit a paste-ready manifest block for the seed row
  const manifest = screens.map((s) => {
    const entry: Record<string, string> = {
      key: s.key,
      label: s.label,
      device: s.device,
      image_url: publicUrl(`${slug}/${s.key}.png`),
    };
    if (s.key === "home-desktop") entry.html_url = publicUrl(`${slug}/home-desktop.html`);
    return entry;
  });

  console.log("\n--- paste into the front_end_templates seed row ---\n");
  console.log("preview_manifest (JSON):");
  console.log(JSON.stringify(manifest, null, 2));
  console.log('\nhero_config (default): {"screen_key":"home-desktop","aspect_ratio":"4/5","slot_strategy":"overlay"}');
  console.log("\nimage_url(s):");
  for (const m of manifest) console.log(`  ${m.key}: ${m.image_url}`);
  console.log("\nDone. Now write/upsert the catalog row (SKILL.md step 5).");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
