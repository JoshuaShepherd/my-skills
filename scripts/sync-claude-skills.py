#!/usr/bin/env python3
"""
Discover Claude skill bundles under movemental and ~/Desktop/Dev/repos, then
rsync them into this repo (my-skills) as the single source of truth.

Walks the full directory tree (nested monorepos like movemental-sites/<site>/).

Skill locations:
  - <tree>/**/.claude/skills/<skill-name>/   (SKILL.md or skill.md)
  - <tree>/**/.cursor/skills/<skill-name>/   → cursor/<skill-name>/
  - <tree>/**/.agents/skills/<skill-name>/   → agents/<skill-name>/
  - <tree>/**/skills/repo-specific/<portal>/<skill-name>/

Excludes: .git, node_modules, _reference, this repo (my-skills), common build dirs.

Conflict policy for duplicate skill-name across repos:
  1) movemental wins over other repos
  2) else lexicographically smallest repo path wins
  3) tie-break: newest mtime on SKILL.md (or skill.md)
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


MY_SKILLS = Path(__file__).resolve().parent.parent
MY_SKILLS_RESOLVED = MY_SKILLS.resolve()
MOVEMENTAL = Path.home() / "Desktop" / "movemental"
DEV_REPOS = Path.home() / "Desktop" / "Dev" / "repos"

MARKERS = ("SKILL.md", "skill.md")

SKIP_DIR_NAMES = frozenset({
    ".git",
    "node_modules",
    "_reference",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".turbo",
})


def marker_path(skill_dir: Path) -> Path | None:
    for name in MARKERS:
        p = skill_dir / name
        if p.is_file():
            return p
    return None


def walk_skipped_parts(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def hits_from_standard_skills_dir(skills_dir: Path, dest_prefix: str | None) -> list[SkillHit]:
    """skills_dir is .../.claude/skills, .../.cursor/skills, or .../.agents/skills."""
    repo_root = skills_dir.parent.parent.resolve()
    hits: list[SkillHit] = []
    if not skills_dir.is_dir():
        return hits
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        m = marker_path(skill_dir)
        if not m:
            continue
        key = skill_dir.name if dest_prefix is None else f"{dest_prefix}/{skill_dir.name}"
        hits.append(
            SkillHit(
                dest_key=key,
                src_dir=skill_dir.resolve(),
                repo_root=repo_root,
                marker=m.resolve(),
            )
        )
    return hits


def hits_from_repo_specific(repo_specific: Path) -> list[SkillHit]:
    repo_root = repo_specific.parent.parent.resolve()
    hits: list[SkillHit] = []
    if not repo_specific.is_dir():
        return hits
    for portal in sorted(repo_specific.iterdir()):
        if not portal.is_dir():
            continue
        for skill_dir in sorted(portal.iterdir()):
            if not skill_dir.is_dir():
                continue
            if walk_skipped_parts(skill_dir):
                continue
            m = marker_path(skill_dir)
            if not m:
                continue
            key = f"repo-specific/{portal.name}/{skill_dir.name}"
            hits.append(
                SkillHit(
                    dest_key=key,
                    src_dir=skill_dir.resolve(),
                    repo_root=repo_root,
                    marker=m.resolve(),
                )
            )
    return hits


@dataclass
class SkillHit:
    """One discovered skill directory."""

    dest_key: str
    src_dir: Path
    repo_root: Path
    marker: Path


def discover_in_tree(tree_root: Path) -> list[SkillHit]:
    hits: list[SkillHit] = []
    if not tree_root.is_dir():
        return hits
    for dirpath, dirnames, _ in os.walk(tree_root, topdown=True):
        p = Path(dirpath)
        try:
            rp = p.resolve()
            if rp == MY_SKILLS_RESOLVED or MY_SKILLS_RESOLVED in rp.parents:
                dirnames.clear()
                continue
        except OSError:
            pass

        dirnames[:] = [d for d in sorted(dirnames) if d not in SKIP_DIR_NAMES]

        if p.name == "skills":
            parent = p.parent.name
            if parent == ".claude":
                hits.extend(hits_from_standard_skills_dir(p, None))
            elif parent == ".cursor":
                hits.extend(hits_from_standard_skills_dir(p, "cursor"))
            elif parent == ".agents":
                hits.extend(hits_from_standard_skills_dir(p, "agents"))
        elif p.name == "repo-specific" and p.parent.name == "skills":
            hits.extend(hits_from_repo_specific(p))
    return hits


def movemental_rank(repo_root: Path) -> int:
    try:
        return 0 if repo_root.resolve() == MOVEMENTAL.resolve() else 1
    except OSError:
        return 1


def choose_canonical(group: list[SkillHit]) -> SkillHit:
    def sort_key(h: SkillHit) -> tuple:
        mtime = -h.marker.stat().st_mtime
        return (movemental_rank(h.repo_root), str(h.repo_root), mtime)

    return sorted(group, key=sort_key)[0]


def rsync_merge(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsync", "-a", "--delete", f"{src}/", f"{dst}/"],
        check=True,
    )


def main() -> int:
    all_hits: list[SkillHit] = []

    if MOVEMENTAL.is_dir():
        all_hits.extend(discover_in_tree(MOVEMENTAL))

    if DEV_REPOS.is_dir():
        all_hits.extend(discover_in_tree(DEV_REPOS))

    by_key: dict[str, list[SkillHit]] = {}
    for h in all_hits:
        by_key.setdefault(h.dest_key, []).append(h)

    manifest_skills: dict = {}
    synced = 0

    for key, group in sorted(by_key.items()):
        canon = choose_canonical(group)
        dest = MY_SKILLS / Path(*key.split("/"))
        rsync_merge(canon.src_dir, dest)

        alts = []
        for h in group:
            alts.append(
                {
                    "repo": str(h.repo_root),
                    "skill_dir": str(h.src_dir),
                    "marker": str(h.marker),
                    "marker_mtime_iso": datetime.fromtimestamp(
                        h.marker.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "is_canonical": h.src_dir == canon.src_dir,
                }
            )

        manifest_skills[key] = {
            "canonical_repo": str(canon.repo_root),
            "canonical_skill_dir": str(canon.src_dir),
            "sources": alts,
        }
        synced += 1

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "my_skills_root": str(MY_SKILLS),
        "scan_roots": [str(MOVEMENTAL), str(DEV_REPOS)],
        "skill_count": synced,
        "skills": manifest_skills,
    }

    manifest_path = MY_SKILLS / "SKILLS_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Synced {synced} skill bundle(s) into {MY_SKILLS}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
