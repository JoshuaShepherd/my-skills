#!/usr/bin/env python3
"""
Fail if ~/.claude/skills or ~/.agents/skills contains a skill bundle that is
missing from my-skills after applying the same dest_key rules as sync-claude-skills.py.

Exit 0: all home bundles have a matching folder under MY_SKILLS.
Exit 1: mismatch or unreadable paths.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MY_SKILLS = Path(__file__).resolve().parent.parent
_SYNC = Path(__file__).resolve().parent / "sync-claude-skills.py"


def _load_sync():
    spec = importlib.util.spec_from_file_location("sync_claude_skills", _SYNC)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {_SYNC}")
    mod = importlib.util.module_from_spec(spec)
    # Register before exec so dataclasses can resolve forward refs / module dict.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    mod = _load_sync()
    missing: list[tuple[str, str]] = []
    keys_seen: set[str] = set()

    for h in mod.hits_from_home_claude_skills():
        keys_seen.add(h.dest_key)
        dest = MY_SKILLS / Path(*h.dest_key.split("/"))
        if not dest.is_dir() or not mod.marker_path(dest):
            missing.append((h.dest_key, str(h.src_dir)))

    for h in mod.hits_from_home_agents_skills():
        keys_seen.add(h.dest_key)
        dest = MY_SKILLS / Path(*h.dest_key.split("/"))
        if not dest.is_dir() or not mod.marker_path(dest):
            missing.append((h.dest_key, str(h.src_dir)))

    if missing:
        print("Missing repo folders for home skill bundle(s):", file=sys.stderr)
        for key, src in sorted(missing):
            print(f"  dest_key={key!r} src={src}", file=sys.stderr)
        return 1

    print(f"OK: {len(keys_seen)} home bundle(s) present under {MY_SKILLS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
