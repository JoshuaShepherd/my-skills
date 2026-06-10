# my-skills

Single source of truth for skill bundles discovered under:

- `~/Desktop/movemental` (full tree walk)
- `~/Desktop/Dev/repos` (full tree walk, including nested worktrees such as `movemental-sites/<site>/`)
- `~/.claude/skills/` (global Claude Code skills—symlinks into `~/.agents/skills/` are copied as **`agents/<name>/`**)
- `~/.agents/skills/` (global agent skills → **`agents/<name>/`**)

The sync script never reads from this checkout of `my-skills` itself (only writes into it).

## Layout

| Source | Destination under this repo |
|--------|---------------------------|
| `<repo>/.claude/skills/<name>/` | `claude/<domain>/<name>/` |
| `<repo>/.cursor/skills/<name>/` | `cursor/<name>/` |
| `<repo>/.agents/skills/<name>/` | `agents/<name>/` |
| `<repo>/skills/repo-specific/<portal>/<name>/` | `repo-specific/<portal>/<name>/` |
| `~/.claude/skills/<name>/` (real bundle, not under `~/.agents`) | `claude/<domain>/<name>/` |
| `~/.claude/skills/<name>/` → resolves under `~/.agents/skills/` | `agents/<name>/` |
| `~/.agents/skills/<name>/` | `agents/<name>/` |

**12 domains** under `claude/`: `movemental`, `content`, `research`, `design`, `assets`, `stitch`, `studio`, `agents`, `infrastructure`, `integrations`, `codegen`, `docs`.

Domain assignment lives in [`scripts/skill-domains.json`](scripts/skill-domains.json). Browse skills in [`CATALOG.md`](CATALOG.md).

Each bundle is synced with **`SKILL.md`** or **`skill.md`** as the entry file (plus sibling assets).

Non-skill reference docs live under [`references/`](references/). Vendor OpenAI skills live under [`vendor/skills-openai/`](vendor/skills-openai/).

## Refresh from all repos

```bash
python3 scripts/sync-claude-skills.py
```

This overwrites each destination folder with **`rsync --delete`** from the chosen canonical source (see below) and regenerates **`SKILLS_MANIFEST.json`**.

### Canonical copy when the same name appears in multiple repos

1. `~/Desktop/movemental` wins over other repos.
2. Project repos (anything under the scanned trees except home) win over `~/.claude/skills` and `~/.agents/skills`.
3. Otherwise the lexicographically first repo path wins.
4. Tie-break: newest marker file (`SKILL.md` / `skill.md`) mtime.

Alternates are listed under `sources` in the manifest.

### Verify home bundles after sync

```bash
python3 scripts/verify-home-skills-in-repo.py
```

### Validate domain assignments

```bash
python3 scripts/assign-skill-domains.py --check
python3 scripts/assign-skill-domains.py --write-catalog
```

## Reference-only trees

`_reference/` is not scanned and is not overwritten by the sync script—keep upstream Anthropic samples or templates there.

### Nested vendor bundles (e.g. `skills-anthropic`)

Some projects store a single folder `.claude/skills/skills-anthropic/` whose **`SKILL.md` files live under `skills/<name>/`**, not at the bundle root. The sync script does **not** split those into installable folders.

To install **one** Anthropic sample skill elsewhere, copy from:

`_reference/skills-anthropic/skills/<name>/`

into your project’s `.claude/skills/<name>/` (include any README / notices from `_reference/skills-anthropic/` as needed).

## For consumers (clone and install)

After cloning this repository:

1. Pick a bundle path: `claude/<domain>/<name>/`, `cursor/<name>/`, `agents/<name>/`, or `repo-specific/<portal>/<name>/`.
2. Copy or symlink it into the matching **flat** runtime directory on your machine.

Examples:

```bash
REPO_ROOT="$(pwd)"   # path to this checkout

ln -sf "$REPO_ROOT/claude/content/article-author" ~/.claude/skills/article-author
ln -sf "$REPO_ROOT/cursor/ssot-dashboard" ~/.cursor/skills/ssot-dashboard
ln -sf "$REPO_ROOT/agents/find-skills" ~/.agents/skills/find-skills

# Or use the helper (reads skill-domains.json / manifest):
scripts/install-skill.sh article-author
scripts/install-skill.sh ssot-dashboard --runtime cursor
```

Use **`SKILLS_MANIFEST.json`** as the machine-readable index (`skill_count`, `dest_path`, `domain`, `runtime_name`, alternates).

Reorganization guide: [`docs/build/prompts/skills-organization-prompt.md`](docs/build/prompts/skills-organization-prompt.md)

## Using skills in a project

Copy or symlink the bundle you need into that repo’s `.claude/skills/` (Claude Code), `.cursor/skills/` (Cursor), or `.agents/skills/` as appropriate. Runtime discovery requires a **flat** install path (`~/.claude/skills/<name>/SKILL.md`); the domain folders in this repo are organizational only.
