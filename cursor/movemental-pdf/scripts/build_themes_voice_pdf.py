#!/usr/bin/env python3
"""Collate movement leader docs/voice + docs/themes into a styled PDF."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import markdown
    import yaml
    from weasyprint import HTML
except ImportError as exc:
    print(
        "Missing dependency. Install with: pip3 install weasyprint markdown pyyaml",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

CSS = """
@page {
  size: letter;
  margin: 1in;
  @top-center {
    content: string(doc-title);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 9pt;
    color: #666;
  }
  @bottom-center {
    content: counter(page);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 9pt;
    color: #666;
  }
}
@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1a1a;
}
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 2.5in;
}
.cover h1 {
  font-size: 28pt;
  margin-bottom: 0.4em;
  border: none;
}
.cover .subtitle {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16pt;
  color: #2c3e50;
  margin-bottom: 2em;
}
.cover .meta {
  font-size: 10pt;
  color: #666;
}
h1, h2, h3, h4 {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #2c3e50;
  page-break-after: avoid;
}
h1 {
  font-size: 20pt;
  border-bottom: 2px solid #2c3e50;
  padding-bottom: 0.2em;
  margin-top: 1.5em;
  page-break-before: always;
}
h1:first-of-type { page-break-before: auto; }
h2 { font-size: 15pt; margin-top: 1.2em; }
h3 { font-size: 12pt; margin-top: 1em; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 10pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #ccc;
  padding: 0.4em 0.6em;
  text-align: left;
}
th { background: #f5f5f5; }
blockquote {
  border-left: 3px solid #2c3e50;
  margin: 1em 0;
  padding: 0.2em 1em;
  color: #333;
  page-break-inside: avoid;
}
pre, code {
  font-family: "Consolas", "Monaco", monospace;
  font-size: 9pt;
}
pre {
  background: #f8f8f8;
  padding: 0.8em;
  overflow-x: auto;
  page-break-inside: avoid;
}
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
a { color: #2c3e50; text-decoration: none; }
"""

PART_VOICE = "# Part I — Voice & Style Guide\n\n"
PART_THEMES = "# Part II — Core Themes\n\n"
PART_DEEP = "# Part III — Theme Deep Dives\n\n"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    return meta, body


def display_name_from_h1(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            name = line[2:].strip()
            name = re.sub(r"\s*—\s*(Core Themes|Voice & Style Guide).*$", "", name)
            return name
    return None


def slug_order_from_core_themes(core_text: str) -> list[str]:
    slugs: list[str] = []
    for match in re.finditer(r"`([a-z0-9-]+)`", core_text):
        slug = match.group(1)
        if slug not in slugs and slug != "core-themes":
            slugs.append(slug)
    return slugs


def sort_theme_files(theme_dir: Path, core_path: Path) -> list[Path]:
    core_text = core_path.read_text(encoding="utf-8")
    table_order = slug_order_from_core_themes(core_text)
    deep_files = [p for p in theme_dir.glob("*.md") if p.name != "CORE_THEMES.md"]

    def sort_key(path: Path) -> tuple:
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        order = meta.get("theme_order")
        if order is not None:
            return (0, int(order), path.name)
        slug = path.stem
        if slug in table_order:
            return (1, table_order.index(slug), path.name)
        return (2, 999, path.name)

    return sorted(deep_files, key=sort_key)


def is_export_ready(repo_root: Path) -> bool:
    voice = list((repo_root / "docs/voice").glob("*.md"))
    core = repo_root / "docs/themes/CORE_THEMES.md"
    return bool(voice) and core.is_file()


def build_markdown(repo_root: Path) -> tuple[str, str, list[str]]:
    voice_files = sorted((repo_root / "docs/voice").glob("*.md"))
    core_path = repo_root / "docs/themes/CORE_THEMES.md"
    theme_dir = repo_root / "docs/themes"
    deep_files = sort_theme_files(theme_dir, core_path)

    voice_text = voice_files[0].read_text(encoding="utf-8")
    core_text = core_path.read_text(encoding="utf-8")
    display = (
        display_name_from_h1(voice_text)
        or display_name_from_h1(core_text)
        or repo_root.name.replace("-", " ").title()
    )

    _, voice_body = parse_frontmatter(voice_text)
    _, core_body = parse_frontmatter(core_text)

    parts: list[str] = []
    included: list[str] = []

    parts.append(PART_VOICE + voice_body.strip())
    included.append(str(voice_files[0].relative_to(repo_root)))

    parts.append(PART_THEMES + core_body.strip())
    included.append(str(core_path.relative_to(repo_root)))

    if deep_files:
        deep_sections = []
        for path in deep_files:
            raw = path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(raw)
            title = meta.get("title") or path.stem.replace("-", " ").title()
            deep_sections.append(f"## {title}\n\n{body.strip()}")
            included.append(str(path.relative_to(repo_root)))
        parts.append(PART_DEEP + "\n\n---\n\n".join(deep_sections))

    return display, "\n\n---\n\n".join(parts), included


def md_to_html_body(md: str) -> str:
    return markdown.markdown(
        md,
        extensions=["tables", "toc", "fenced_code", "meta", "sane_lists"],
    )


def build_html(display_name: str, md_content: str) -> str:
    today = date.today().isoformat()
    body = md_to_html_body(md_content)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{display_name} — Voice &amp; Themes</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="cover">
    <h1 style="string-set: doc-title '{display_name} — Voice &amp; Themes';">{display_name}</h1>
    <div class="subtitle">Voice &amp; Themes</div>
    <div class="meta">Movemental · Generated {today}</div>
  </div>
  {body}
</body>
</html>"""


def output_filename(display_name: str) -> str:
    safe = display_name.replace("/", "-")
    return f"{safe} — Voice & Themes.pdf"


def build_pdf(repo_root: Path, output: Path) -> tuple[int, list[str]]:
    display, md_content, included = build_markdown(repo_root)
    html = build_html(display, md_content)
    doc = HTML(string=html).render()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.write_pdf(str(output))
    return len(doc.pages), included


def scan_ready_leaders(scan_root: Path) -> list[Path]:
    ready = []
    for child in sorted(scan_root.iterdir()):
        if child.is_dir() and is_export_ready(child):
            ready.append(child)
    return ready


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, help="Leader repo root")
    parser.add_argument("--output", type=Path, help="Output PDF path")
    parser.add_argument(
        "--scan-root",
        type=Path,
        help="Scan directory for export-ready leader repos",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.home() / "Desktop",
        help="Output directory for batch mode",
    )
    args = parser.parse_args()

    if args.scan_root:
        leaders = scan_ready_leaders(args.scan_root)
        if not leaders:
            print(f"No export-ready leaders under {args.scan_root}", file=sys.stderr)
            raise SystemExit(1)
        for repo in leaders:
            display, _, _ = build_markdown(repo)
            out = args.output_dir / output_filename(display)
            pages, files = build_pdf(repo, out)
            print(f"✓ {repo.name}: {pages} pages → {out}")
            for f in files:
                print(f"    · {f}")
        return

    if not args.repo_root:
        parser.error("--repo-root or --scan-root required")

    repo = args.repo_root.resolve()
    if not is_export_ready(repo):
        print(f"Not export-ready: {repo} (need docs/voice/*.md + docs/themes/CORE_THEMES.md)", file=sys.stderr)
        raise SystemExit(1)

    display, _, _ = build_markdown(repo)
    output = args.output or (Path.home() / "Desktop" / output_filename(display))
    pages, files = build_pdf(repo, output)
    print(f"✓ {pages} pages → {output}")
    for f in files:
        print(f"  · {f}")


if __name__ == "__main__":
    main()
