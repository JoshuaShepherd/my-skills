#!/usr/bin/env tsx
/**
 * Mirror design audit skills from claude/design → cursor/
 * with Cursor-compatible frontmatter (disable-model-invocation, no allowed-tools).
 *
 * Usage: tsx scripts/sync-design-audit-skills-to-cursor.ts
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CLAUDE_ROOT = path.join(ROOT, "claude/design");
const CURSOR_ROOT = path.join(ROOT, "cursor");

/** Canonical design audit skills under claude/design/. */
export const DESIGN_AUDIT_SKILLS = [
  "audit-experience",
  "chat-ui-audit",
  "color-audit",
  "design-audit",
  "design-chain-audit",
  "icon-audit",
  "page-audit",
  "responsive-audit",
  "ui-hook-wiring-audit",
  "visual-storytelling-audit",
] as const;

function transformFrontmatter(raw: string): string {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return raw;

  const [, frontmatter, body] = match;
  const lines = frontmatter.split("\n").filter((line) => {
    const trimmed = line.trim();
    return (
      !trimmed.startsWith("user-invocable:") &&
      !trimmed.startsWith("allowed-tools:") &&
      !trimmed.startsWith("argument-hint:")
    );
  });

  if (!lines.some((l) => l.startsWith("disable-model-invocation:"))) {
    lines.push("disable-model-invocation: true");
  }

  return `---\n${lines.join("\n")}\n---\n${body}`;
}

function copyDir(src: string, dest: string) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.name === "SKILL.md") {
      const content = fs.readFileSync(srcPath, "utf8");
      fs.writeFileSync(destPath, transformFrontmatter(content));
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function syncSkill(skillName: string) {
  const src = path.join(CLAUDE_ROOT, skillName);
  const dest = path.join(CURSOR_ROOT, skillName);
  if (!fs.existsSync(src)) {
    throw new Error(`Missing claude skill: ${src}`);
  }
  copyDir(src, dest);
  console.log(`✓ ${skillName}`);
}

function main() {
  for (const skill of DESIGN_AUDIT_SKILLS) {
    syncSkill(skill);
  }
  console.log(`✓ ${DESIGN_AUDIT_SKILLS.length} design audit skill(s) synced to cursor/`);
}

main();
