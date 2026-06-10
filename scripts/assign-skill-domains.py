#!/usr/bin/env python3
"""Domain assignment, validation, dedupe reports, and CATALOG.md generation."""

from __future__ import annotations

import argparse
import filecmp
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

MY_SKILLS = Path(__file__).resolve().parent.parent
DOMAINS_FILE = Path(__file__).resolve().parent / "skill-domains.json"

RESERVED_TOP_DIRS = frozenset({
    "_reference",
    "agents",
    "art",
    "authoring-skills",
    "career",
    "claude",
    "cursor",
    "docs",
    "references",
    "repo-specific",
    "scripts",
    "vendor",
    "analytics",
    "data",
    "design",
    "strategy",
    "stitch",
    "skills-openai",
    ".git",
    ".github",
    ".claude",
})

LEGACY_FOLDERS = ("analytics", "data", "design", "strategy", "stitch")
MARKERS = ("SKILL.md", "skill.md")


def load_domain_data() -> tuple[dict[str, str], dict[str, list[str]]]:
    data = json.loads(DOMAINS_FILE.read_text(encoding="utf-8"))
    skills_map: dict[str, str] = data["skills"]
    domains: dict[str, list[str]] = data["domains"]
    return skills_map, domains


def marker_path(skill_dir: Path) -> Path | None:
    for name in MARKERS:
        p = skill_dir / name
        if p.is_file():
            return p
    return None


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and marker_path(path) is not None


def canonical_bundles(root: Path = MY_SKILLS) -> list[str]:
    """All canonical Claude skill names under claude/<domain>/."""
    names: list[str] = []
    claude_root = root / "claude"
    if claude_root.is_dir():
        for domain_dir in sorted(claude_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            for skill_dir in sorted(domain_dir.iterdir()):
                if is_skill_dir(skill_dir):
                    names.append(skill_dir.name)
    # During migration, also accept legacy top-level bundles
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.name in RESERVED_TOP_DIRS or entry.name.startswith("."):
            continue
        if is_skill_dir(entry) and entry.name not in names:
            names.append(entry.name)
    return sorted(set(names))


def top_level_bundles(root: Path = MY_SKILLS) -> list[str]:
    """Legacy: top-level-only bundles (should be empty post-migration)."""
    names: list[str] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.name in RESERVED_TOP_DIRS or entry.name.startswith("."):
            continue
        if is_skill_dir(entry):
            names.append(entry.name)
    return names


def claude_bundle_path(name: str, skills_map: dict[str, str], root: Path = MY_SKILLS) -> Path | None:
    flat = root / name
    if is_skill_dir(flat):
        return flat
    domain = skills_map.get(name)
    if domain:
        nested = root / "claude" / domain / name
        if is_skill_dir(nested):
            return nested
    return None


def read_description(skill_dir: Path) -> str:
    marker = marker_path(skill_dir)
    if not marker:
        return ""
    text = marker.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.strip().startswith("description:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")[:120]
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return skill_dir.name


def legacy_orphan_md_files(root: Path = MY_SKILLS) -> list[Path]:
    orphans: list[Path] = []
    for folder in LEGACY_FOLDERS:
        base = root / folder
        if not base.is_dir():
            continue
        for md in base.rglob("*.md"):
            if md.name in ("README.md", "SKILL.md", "skill.md"):
                continue
            stem = md.stem
            if claude_bundle_path(stem, load_domain_data()[0], root) is None:
                orphans.append(md)
    return sorted(orphans)


def legacy_stale_md_files(root: Path = MY_SKILLS) -> list[tuple[Path, Path]]:
    """Legacy .md files where a top-level/claude bundle exists with same stem."""
    skills_map, _ = load_domain_data()
    pairs: list[tuple[Path, Path]] = []
    for folder in LEGACY_FOLDERS:
        base = root / folder
        if not base.is_dir():
            continue
        for md in base.rglob("*.md"):
            if md.name in ("README.md", "SKILL.md", "skill.md"):
                continue
            bundle = claude_bundle_path(md.stem, skills_map, root)
            if bundle is not None:
                pairs.append((md, bundle))
    return sorted(pairs, key=lambda x: str(x[0]))


def cursor_bundles(root: Path = MY_SKILLS) -> set[str]:
    cursor_dir = root / "cursor"
    if not cursor_dir.is_dir():
        return set()
    return {p.name for p in cursor_dir.iterdir() if is_skill_dir(p)}


def repo_specific_bundles(root: Path = MY_SKILLS) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    base = root / "repo-specific"
    if not base.is_dir():
        return out
    for portal in sorted(base.iterdir()):
        if not portal.is_dir():
            continue
        for skill in sorted(portal.iterdir()):
            if is_skill_dir(skill):
                out[skill.name].append(portal.name)
    return dict(out)


def dirs_equal(a: Path, b: Path) -> bool:
    if not a.is_dir() or not b.is_dir():
        return False
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    if cmp.diff_files:
        return False
    for sub in cmp.subdirs:
        if not dirs_equal(a / sub, b / sub):
            return False
    return True


def cmd_check(root: Path, skills_map: dict[str, str]) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    bundles = canonical_bundles(root)
    legacy_top = top_level_bundles(root)
    unassigned = [b for b in bundles if b not in skills_map]
    if unassigned:
        errors.append(f"Unassigned bundles ({len(unassigned)}): {', '.join(unassigned)}")
    if legacy_top:
        warnings.append(
            f"Legacy top-level bundles still present ({len(legacy_top)}): "
            + ", ".join(legacy_top[:20])
            + (" ..." if len(legacy_top) > 20 else "")
        )

    orphans = legacy_orphan_md_files(root)
    if orphans:
        warnings.append(
            "Legacy orphan .md files (no bundle): "
            + ", ".join(str(p.relative_to(root)) for p in orphans)
        )

    stale = legacy_stale_md_files(root)
    if stale:
        warnings.append(
            f"Legacy stale .md copies where bundle exists: {len(stale)} files "
            "(retire in Phase 1)"
        )

    cursor = cursor_bundles(root)
    overlap_cursor = sorted(set(bundles) & cursor)
    if overlap_cursor:
        warnings.append(
            f"Canonical ∩ cursor ({len(overlap_cursor)}): {', '.join(overlap_cursor[:20])}"
            + (" ..." if len(overlap_cursor) > 20 else "")
        )

    rs = repo_specific_bundles(root)
    canonical_names = set(bundles)
    overlap_rs = sorted(set(rs) & canonical_names)
    if overlap_rs:
        warnings.append(f"Canonical ∩ repo-specific names: {len(overlap_rs)}")

    print("# Domain assignment check\n")
    print(f"Canonical Claude bundles: {len(bundles)}")
    print(f"Mapped skills in skill-domains.json: {len(skills_map)}")
    print()

    if warnings:
        print("## Warnings\n")
        for w in warnings:
            print(f"- {w}")
        print()

    if errors:
        print("## Errors\n")
        for e in errors:
            print(f"- {e}")
        print()
        return 1

    print("OK: all canonical bundles assigned to a domain.")
    return 0


def cmd_dedupe_repo_specific(root: Path, skills_map: dict[str, str]) -> int:
    rs = repo_specific_bundles(root)
    delete: list[str] = []
    keep_diff: list[str] = []
    portal_only: list[str] = []

    for name, portals in sorted(rs.items()):
        canonical = claude_bundle_path(name, skills_map, root)
        if canonical is None:
            portal_only.append(f"{name} (portals: {', '.join(portals)})")
            continue
        identical_all = True
        for portal in portals:
            overlay = root / "repo-specific" / portal / name
            if not dirs_equal(canonical, overlay):
                identical_all = False
                keep_diff.append(f"{name} @ {portal}")
        if identical_all:
            delete.append(f"{name} (portals: {', '.join(portals)})")

    print("# repo-specific dedupe report\n")
    print(f"## Identical to canonical — safe to delete ({len(delete)})\n")
    for line in delete:
        print(f"- {line}")

    print(f"\n## Differs from canonical — keep ({len(keep_diff)})\n")
    for line in keep_diff:
        print(f"- {line}")

    print(f"\n## Portal-only — no canonical ({len(portal_only)})\n")
    for line in portal_only:
        print(f"- {line}")

    report_path = root / "_docs" / "_build" / "repo-specific-dedupe-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "# repo-specific dedupe report\n\n"
        + "\n".join(f"- {x}" for x in delete)
        + "\n\n## keep\n\n"
        + "\n".join(f"- {x}" for x in keep_diff)
        + "\n\n## portal-only\n\n"
        + "\n".join(f"- {x}" for x in portal_only)
        + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {report_path.relative_to(root)}")
    return 0


def cmd_write_catalog(root: Path, skills_map: dict[str, str], domains: dict[str, list[str]]) -> int:
    by_domain: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    for domain in domains:
        for name in domains[domain]:
            bundle = claude_bundle_path(name, skills_map, root)
            if bundle is None:
                bundle = root / "claude" / domain / name
            desc = read_description(bundle) if bundle and bundle.is_dir() else ""
            rel = f"claude/{domain}/{name}"
            by_domain[domain].append((name, desc, rel))

    lines = [
        "# Skill catalog",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Install any skill flat into `~/.claude/skills/<name>/` (see `scripts/install-skill.sh`).",
        "",
    ]

    total = 0
    for domain in sorted(by_domain.keys()):
        items = sorted(by_domain[domain], key=lambda x: x[0])
        total += len(items)
        lines.append(f"## {domain} ({len(items)})")
        lines.append("")
        lines.append("| Skill | Description | Path |")
        lines.append("|-------|-------------|------|")
        for name, desc, rel in items:
            safe_desc = desc.replace("|", "\\|")
            lines.append(f"| `{name}` | {safe_desc} | `{rel}` |")
        lines.append("")

    lines.insert(4, f"**Total canonical Claude skills:** {total}")
    lines.insert(5, "")

    catalog = root / "CATALOG.md"
    catalog.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {catalog} ({total} skills)")
    return 0


def resolve_domain(name: str, skills_map: dict[str, str]) -> str | None:
    return skills_map.get(name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill domain assignment utilities")
    parser.add_argument("--check", action="store_true", help="Validate domain assignments")
    parser.add_argument(
        "--dedupe-repo-specific",
        action="store_true",
        help="Report repo-specific overlay dedupe candidates",
    )
    parser.add_argument("--write-catalog", action="store_true", help="Generate CATALOG.md")
    parser.add_argument("--root", type=Path, default=MY_SKILLS, help="my-skills root")
    args = parser.parse_args()

    if not DOMAINS_FILE.is_file():
        print(f"Missing {DOMAINS_FILE}", file=sys.stderr)
        return 1

    skills_map, domains = load_domain_data()

    if not any([args.check, args.dedupe_repo_specific, args.write_catalog]):
        parser.print_help()
        return 1

    rc = 0
    if args.check:
        rc = max(rc, cmd_check(args.root, skills_map))
    if args.dedupe_repo_specific:
        rc = max(rc, cmd_dedupe_repo_specific(args.root, skills_map))
    if args.write_catalog:
        rc = max(rc, cmd_write_catalog(args.root, skills_map, domains))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
