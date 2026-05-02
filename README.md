# my-skills

Single source of truth for skill bundles discovered under:

- `~/Desktop/movemental` (full tree walk)
- `~/Desktop/Dev/repos` (full tree walk, including nested worktrees such as `movemental-sites/<site>/`)

The sync script never reads from this checkout of `my-skills` itself (only writes into it).

## Layout

| Source | Destination under this repo |
|--------|---------------------------|
| `<repo>/.claude/skills/<name>/` | `<name>/` |
| `<repo>/.cursor/skills/<name>/` | `cursor/<name>/` |
| `<repo>/.agents/skills/<name>/` | `agents/<name>/` |
| `<repo>/skills/repo-specific/<portal>/<name>/` | `repo-specific/<portal>/<name>/` |

Each bundle is synced with **`SKILL.md`** or **`skill.md`** as the entry file (plus sibling assets).

## Refresh from all repos

```bash
python3 scripts/sync-claude-skills.py
```

This overwrites each destination folder with **`rsync --delete`** from the chosen canonical source (see below) and regenerates **`SKILLS_MANIFEST.json`**.

### Canonical copy when the same name appears in multiple repos

1. `~/Desktop/movemental` wins over other repos.
2. Otherwise the lexicographically first repo path wins.
3. Tie-break: newest marker file (`SKILL.md` / `skill.md`) mtime.

Alternates are listed under `sources` in the manifest.

## Reference-only trees

`_reference/` is not scanned and is not overwritten by the sync script—keep upstream Anthropic samples or templates there.

## Using skills in a project

Copy or symlink the bundle you need into that repo’s `.claude/skills/` (Claude Code), `.cursor/skills/` (Cursor), or `.agents/skills/` as appropriate.
