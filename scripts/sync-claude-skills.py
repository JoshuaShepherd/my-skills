#!/usr/bin/env python3
"""
Discover Claude skill bundles under movemental, ~/Desktop/Dev/repos, and user
global skill dirs (~/.claude/skills, ~/.agents/skills), then rsync them into
this repo (my-skills) as the single source of truth.

Walks the full directory tree (nested monorepos like movemental-sites/<site>/).

Skill locations:
  - <tree>/**/.claude/skills/<skill-name>/   → claude/<domain>/<skill-name>/
  - <tree>/**/.cursor/skills/<skill-name>/   → cursor/<skill-name>/
  - <tree>/**/.agents/skills/<skill-name>/   → agents/<skill-name>/
  - <tree>/**/skills/repo-specific/<portal>/<skill-name>/
  - ~/.claude/skills/<name>/  → claude/<domain>/<name>/ (or agents/<name>/ if symlink → ~/.agents/skills)
  - ~/.agents/skills/<name>/  → agents/<name>/

Excludes: .git, node_modules, _reference, this repo (my-skills), common build dirs.

Conflict policy for duplicate skill-name across repos:
  1) movemental wins over other repos
  2) project repos win over ~/.claude and ~/.agents home bundles
  3) else lexicographically smallest repo path wins
  4) tie-break: newest mtime on SKILL.md (or skill.md)
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
HOME_CLAUDE_ROOT = Path.home() / ".claude"
HOME_AGENTS_ROOT = Path.home() / ".agents"
HOME_CLAUDE_SKILLS = HOME_CLAUDE_ROOT / "skills"
HOME_AGENTS_SKILLS = HOME_AGENTS_ROOT / "skills"

MARKERS = ("SKILL.md", "skill.md")
DOMAINS_FILE = Path(__file__).resolve().parent / "skill-domains.json"

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


def load_skills_domain_map() -> dict[str, str]:
    if not DOMAINS_FILE.is_file():
        return {}
    data = json.loads(DOMAINS_FILE.read_text(encoding="utf-8"))
    return data.get("skills", {})


def claude_dest_key(skill_name: str, skills_map: dict[str, str]) -> str:
    domain = skills_map.get(skill_name)
    if domain:
        return f"claude/{domain}/{skill_name}"
    print(
        f"Warning: no domain for {skill_name!r} in {DOMAINS_FILE.name}; "
        f"syncing to claude/_unassigned/{skill_name}/",
        flush=True,
    )
    return f"claude/_unassigned/{skill_name}"


def walk_skipped_parts(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def hits_from_standard_skills_dir(
    skills_dir: Path,
    dest_prefix: str | None,
    skills_map: dict[str, str] | None = None,
) -> list[SkillHit]:
    """skills_dir is .../.claude/skills, .../.cursor/skills, or .../.agents/skills."""
    repo_root = skills_dir.parent.parent.resolve()
    hits: list[SkillHit] = []
    if not skills_dir.is_dir():
        return hits
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        resolved = skill_dir.resolve()
        m = marker_path(resolved)
        if not m:
            continue
        if dest_prefix is None:
            key = claude_dest_key(skill_dir.name, skills_map or {})
        else:
            key = f"{dest_prefix}/{skill_dir.name}"
        hits.append(
            SkillHit(
                dest_key=key,
                src_dir=resolved,
                repo_root=repo_root,
                marker=m.resolve(),
                runtime_name=skill_dir.name,
            )
        )
    return hits


def hits_from_home_claude_skills(skills_map: dict[str, str]) -> list[SkillHit]:
    """
    ~/.claude/skills/<name>/ → claude/<domain>/<name>/ unless the bundle resolves
    under ~/.agents/skills/ (e.g. symlink) → agents/<name>/.
    """
    hits: list[SkillHit] = []
    if not HOME_CLAUDE_SKILLS.is_dir():
        return hits
    agents_root: Path | None = None
    if HOME_AGENTS_SKILLS.is_dir():
        try:
            agents_root = HOME_AGENTS_SKILLS.resolve()
        except OSError:
            agents_root = None
    repo_root = HOME_CLAUDE_ROOT
    for skill_dir in sorted(HOME_CLAUDE_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        try:
            resolved = skill_dir.resolve()
        except OSError:
            continue
        m = marker_path(resolved)
        if not m:
            continue
        under_agents = bool(
            agents_root
            and (resolved == agents_root or agents_root in resolved.parents)
        )
        key = (
            f"agents/{skill_dir.name}"
            if under_agents
            else claude_dest_key(skill_dir.name, skills_map)
        )
        hits.append(
            SkillHit(
                dest_key=key,
                src_dir=resolved,
                repo_root=repo_root,
                marker=m.resolve(),
                runtime_name=skill_dir.name,
            )
        )
    return hits


def hits_from_home_agents_skills(skills_map: dict[str, str]) -> list[SkillHit]:
    """~/.agents/skills/<name>/ → agents/<name>/"""
    if not HOME_AGENTS_SKILLS.is_dir():
        return []
    return hits_from_standard_skills_dir(HOME_AGENTS_SKILLS, "agents", skills_map)


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
                    runtime_name=skill_dir.name,
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
    runtime_name: str


def discover_in_tree(tree_root: Path, skills_map: dict[str, str]) -> list[SkillHit]:
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
                hits.extend(hits_from_standard_skills_dir(p, None, skills_map))
            elif parent == ".cursor":
                hits.extend(hits_from_standard_skills_dir(p, "cursor", skills_map))
            elif parent == ".agents":
                hits.extend(hits_from_standard_skills_dir(p, "agents", skills_map))
        elif p.name == "repo-specific" and p.parent.name == "skills":
            hits.extend(hits_from_repo_specific(p))
    return hits


def repo_rank(repo_root: Path) -> int:
    """Lower wins. movemental < project repos < home ~/.claude / ~/.agents."""
    try:
        r = repo_root.resolve()
        if MOVEMENTAL.is_dir() and r == MOVEMENTAL.resolve():
            return 0
        if r == HOME_CLAUDE_ROOT.resolve() or r == HOME_AGENTS_ROOT.resolve():
            return 2
    except OSError:
        pass
    return 1


def choose_canonical(group: list[SkillHit]) -> SkillHit:
    def sort_key(h: SkillHit) -> tuple:
        mtime = -h.marker.stat().st_mtime
        return (repo_rank(h.repo_root), str(h.repo_root), mtime)

    return sorted(group, key=sort_key)[0]


def rsync_merge(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsync", "-a", "--delete", f"{src}/", f"{dst}/"],
        check=True,
    )


def manifest_entry(key: str, hit: SkillHit, skills_map: dict[str, str], alts: list) -> dict:
    runtime_name = hit.runtime_name
    domain: str | None = None
    if key.startswith("claude/"):
        parts = key.split("/")
        if len(parts) >= 3:
            domain = parts[1]
    entry = {
        "runtime_name": runtime_name,
        "dest_path": key.replace("/", "/"),
        "canonical_repo": str(hit.repo_root),
        "canonical_skill_dir": str(hit.src_dir),
        "sources": alts,
    }
    if domain:
        entry["domain"] = domain
    elif runtime_name in skills_map:
        entry["domain"] = skills_map[runtime_name]
    return entry


def main() -> int:
    skills_map = load_skills_domain_map()
    all_hits: list[SkillHit] = []

    if MOVEMENTAL.is_dir():
        all_hits.extend(discover_in_tree(MOVEMENTAL, skills_map))

    if DEV_REPOS.is_dir():
        all_hits.extend(discover_in_tree(DEV_REPOS, skills_map))

    all_hits.extend(hits_from_home_claude_skills(skills_map))
    all_hits.extend(hits_from_home_agents_skills(skills_map))

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

        manifest_skills[key] = manifest_entry(key, canon, skills_map, alts)
        synced += 1

    scan_roots = [str(MOVEMENTAL), str(DEV_REPOS)]
    if HOME_CLAUDE_SKILLS.is_dir():
        scan_roots.append(str(HOME_CLAUDE_SKILLS.resolve()))
    if HOME_AGENTS_SKILLS.is_dir():
        scan_roots.append(str(HOME_AGENTS_SKILLS.resolve()))

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "my_skills_root": str(MY_SKILLS),
        "scan_roots": scan_roots,
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
