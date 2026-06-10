# Prompt: Make `my-skills` the master, shareable skill set (GitHub-ready)

Use this document as a **step-by-step operator prompt** to finish turning this **`my-skills` repository** into the **single source of truth** for Claude Code (`.claude/skills/`), Cursor (`.cursor/skills/`), and agent runtimes (`.agents/skills/`), so others can clone the repo and copy or symlink bundles without missing anything you use locally.

> **Audit snapshot (this machine, 2026-05-06/07):** `scripts/sync-claude-skills.py` already walks `~/Desktop/movemental` and `~/Desktop/Dev/repos` and rsyncs **immediate child** skill folders (those containing `SKILL.md` or `skill.md` at the bundle root). A path-normalized spot-check of `~/Desktop/Dev/repos`, `~/Desktop/movemental`, and `~/.claude/skills` showed **real gaps** only for skills that live **outside** those scan roots or **inside** nested trees that the script does not flatten.

---

## 0. Ground rules (read first)

1. **Destination layout in this repo** (from `README.md`):

   | Source on disk | Destination in `my-skills` |
   |----------------|----------------------------|
   | `<repo>/.claude/skills/<name>/` | `claude/<domain>/<name>/` |
   | `<repo>/.cursor/skills/<name>/` | `cursor/<name>/` |
   | `<repo>/.agents/skills/<name>/` | `agents/<name>/` |
   | `<repo>/skills/repo-specific/<portal>/<name>/` | `repo-specific/<portal>/<name>/` |

   Domain assignment: [`scripts/skill-domains.json`](../../../scripts/skill-domains.json). Full reorg guide: [`skills-organization-prompt.md`](skills-organization-prompt.md).

2. **Do not treat plain path-string equality as the truth.** When comparing “is this skill in the repo?”, always map through the table above. For example, a skill at `~/.cursor/skills/ssot-dashboard/` must appear as `cursor/ssot-dashboard/` in the repo, not `ssot-dashboard/`.

3. **`_reference/`** is intentionally **not** part of the sync walk. It holds upstream or sample trees (e.g. Anthropic’s `skills-anthropic` layout). It **is** visible on GitHub and is the right place for **read-only** reference material—but it is not a substitute for a proper synced bundle if you want one folder per installable skill at the repo root.

4. **Git visibility:** This repo’s `.gitignore` is minimal (e.g. `.DS_Store`, local settings). Any skill you add as normal files under the layout above will be **visible on GitHub** after commit.

---

## 1. Close the “user home” gap (Claude global skills)

**Problem:** Skills installed only under `~/.claude/skills/<name>/` are **not** discovered by `sync-claude-skills.py` today (scan roots are only `~/Desktop/movemental` and `~/Desktop/Dev/repos`).

**On this machine, the following global bundles existed under `~/.claude/skills/` but had no matching top-level `<name>/` in `my-skills` at audit time:**

- `author-research`
- `domain-finder`
- `frontend-cleanup`
- `poll-opinion-research`
- `supabase-add-tenant-user`

**`react-components` also appeared under the home listing in one check; confirm its real path:** if it lives under `~/.agents/skills/react-components/`, map it to `agents/react-components/` (see step 2), not to a top-level folder.

### Finished work

1. **Choose one:**

   - **A (recommended):** Extend `scripts/sync-claude-skills.py` with an optional third scan root, e.g. `Path.home() / ".claude" / "skills"`, using the **same** `hits_from_standard_skills_dir(..., dest_prefix=None)` logic as project `.claude/skills`, **or**
   - **B:** Manually `rsync -a --delete ~/.claude/skills/<name>/` into `my-skills/<name>/` for each missing bundle.

2. **Preserve bundle integrity:** Copy the whole directory (Skill frontmatter, sibling scripts, assets)—not only `SKILL.md`.

3. **Resolve symlinks:** Some entries under `~/.claude/skills/` may be **symlinks** into `~/.agents/skills/` (for example `react-components`). Copy from the **real** bundle directory (or use `rsync -L`) so the repo contains actual files, and map to `agents/<name>/` per the layout table—not a dangling symlink.

4. **Regenerate the manifest** (step 5).

---

## 2. Close the “user agents” gap (`.agents/skills`)

**Problem:** The sync script **does** support `.agents/skills/<name>/` **inside** scanned repos, but **`~/.agents/skills/` is not scanned**.

**Example gap at audit:** `~/.agents/skills/find-skills/` → should land as **`agents/find-skills/`** in `my-skills`. **`react-components`** under `~/.agents/skills/` → **`agents/react-components/`**.

### Finished work

1. Add `Path.home() / ".agents" / "skills"` as a scan root (mirror of step 1A), **or** rsync each bundle into `my-skills/agents/<name>/`.

2. Run manifest regeneration (step 5).

---

## 3. Decide policy for nested vendor trees (e.g. `skills-anthropic`)

**Problem:** Some repos keep a **single** folder `.claude/skills/skills-anthropic/` that contains **`skills/<skill-name>/SKILL.md`** nested **below** the bundle root. The current discoverer only considers **immediate children** of `.claude/skills/` that themselves contain `SKILL.md`/`skill.md`. So **individual** Anthropic skills inside that tree are **not** emitted as separate top-level repo folders.

**What you already have:** `_reference/skills-anthropic/` mirrors that upstream layout for documentation and licensing—**good for sharing the source tree**, not the same as “one folder = one installable skill” at the root.

### Finished work (pick a policy and implement it)

1. **Reference-only (minimal change):** Document in the main `README.md` that consumers who want a specific Anthropic sample skill should copy from `_reference/skills-anthropic/skills/<name>/` into their project’s `.claude/skills/<name>/`.

2. **Flattened installables (more work, clearer for users):** Add a small follow-up script or a second pass in the sync script that, for selected roots, **promotes** each `skills-anthropic/skills/<name>/` into `my-skills/_reference/anthropic-skills-flat/<name>/` or into top-level `<name>/` (only if names do not collide with your custom skills). Resolve **naming collisions** explicitly in the manifest.

3. **License:** Ensure `THIRD_PARTY_NOTICES` and any license files from vendor trees stay in repo where required.

---

## 4. Widen “Desktop” coverage if you keep skills outside `Dev/repos`

**Problem:** If you ever place projects under `~/Desktop/<something>` **not** under `~/Desktop/Dev/repos` or `~/Desktop/movemental`, the current script will miss them.

**Audit note:** `~/Desktop/movemental/.claude/skills/...` **is** under `~/Desktop/movemental` and matches the `MOVEMENTAL` constant in the script—**no change needed** for that path.

### Finished work

- If you have (or will have) other Desktop trees with skills, either move those repos under `~/Desktop/Dev/repos`, **or** add additional `discover_in_tree` roots in the script (with clear comments and manifest `scan_roots` updates).

---

## 5. Run sync, verify manifest, and commit

### Finished work

1. From the repo root:

   ```bash
   python3 scripts/sync-claude-skills.py
   ```

2. Open **`SKILLS_MANIFEST.json`** and confirm:

   - `scan_roots` lists every root you intend (after you extend the script).
   - `skill_count` matches expectations.
   - For contentious names, `sources` lists alternates so you can trace **which repo won** the canonical copy.

3. **Drift check (optional but strong):** Add a CI job or a local script that fails if:

   - Any `SKILL.md` under configured scan roots maps to a `dest_key` that is missing in the repo, or
   - Home directories (`~/.claude/skills`, `~/.agents/skills`) contain bundles not listed in the manifest (once those roots are added).

4. **Git**

   ```bash
   git status
   git add -A
   git commit -m "Sync skills: include home scan roots and close manifest gaps."
   git push
   ```

---

## 6. Document consumption for others (sharing contract)

### Finished work — publish clear instructions

1. In **`README.md`**, add a short **“For consumers”** section:

   - Clone the repo.
   - Pick a bundle path (`claude/<domain>/<name>/`, `cursor/<name>/`, `agents/<name>/`, or `repo-specific/...`).
   - Install via **copy** or **symlink** into the correct dot-folder on their machine:

     ```bash
     ln -s "$(pwd)/claude/content/article-author" ~/.claude/skills/article-author
     ln -s "$(pwd)/cursor/ssot-dashboard" ~/.cursor/skills/ssot-dashboard
     ln -s "$(pwd)/agents/find-skills" ~/.agents/skills/find-skills
     scripts/install-skill.sh article-author
     ```

2. Mention **`SKILLS_MANIFEST.json`** as the machine-readable index for tooling (search by key, list sources).

3. If you rely on **`npx skills`** or other installers, link to them where relevant (some home bundles document this in their own `SKILL.md`).

---

## 7. Definition of “done”

You can call this repo the **master set** when:

1. **Every** skill you actively use from:

   - `~/Desktop/movemental`
   - `~/Desktop/Dev/repos`
   - `~/.claude/skills` *(after extending sync or manual copy)*
   - `~/.agents/skills` *(after extending sync or manual copy)*

   has a **committed** counterpart under `my-skills` using the **correct prefix** (`cursor/`, `agents/`, `repo-specific/`, or top-level).

2. **`SKILLS_MANIFEST.json`** reflects the same scan roots and regenerates cleanly.

3. **`README.md`** explains layout, sync command, and how third-party / `_reference` trees differ from installable bundles.

4. A fresh clone + symlink/copy reproduces your environment **without** referring to paths that only exist on one laptop.

---

## Appendix A — Audit leftovers to interpret carefully

- **False “missing” alarms:** Any automated diff that compares external paths to repo paths **without** applying the `cursor/` and `agents/` prefixes will incorrectly flag skills that **are** present (e.g. `cursor/ssot-dashboard`, `agents/supabase-postgres-best-practices`).
- **`skills-openai/...` nested under `.claude/skills/`:** If a repo stores OpenAI-related skills as **nested folders under** `.claude/skills/skills-openai/`, confirm whether your sync result matches how you want consumers to install them (single mega-bundle vs flattened skills). Same class of issue as `skills-anthropic`.

---

## Appendix B — Quick verification commands (operator)

```bash
# Top-level global Claude skills (should all appear under my-skills/<name>/ after fixes)
ls ~/.claude/skills

# Global agent skills (should appear under my-skills/agents/<name>/ after fixes)
ls ~/.agents/skills 2>/dev/null

# Regenerate manifest after sync script changes
python3 scripts/sync-claude-skills.py

# Count skill entry files in repo (sanity)
find . -path ./_reference -prune -o \( -name SKILL.md -o -name skill.md \) -print | wc -l
```

When these commands and the checklist in section 7 agree, the repo is ready to act as the **master, GitHub-shareable** skill library.
