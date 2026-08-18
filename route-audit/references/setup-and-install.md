# Setup, Install, and Preflight

## 1. Where the skill lives

Canonical home is the shared skills library:

```
/home/josh/dev/01-Movemental-Core/my-skills/route-audit/
```

One copy, one source of truth. Never duplicate a skill into a repo — a copied skill drifts, and you
will spend a Tuesday wondering why the audit behaves differently in two repos.

## 2. Connecting it to the studio repo

**Check first whether the whole library is already linked.** In the house layout, `my-skills` is
symlinked into every repo wholesale. If so, dropping the directory into `my-skills` is the entire
install — do nothing else.

```bash
cd /home/josh/dev/01-Movemental-Core/zenwrite
ls -la .claude/skills .cursor/skills 2>/dev/null
ls -la .cursor/skills/route-audit/SKILL.md
```

- If `.claude/skills` is already a symlink → `../my-skills` (or similar): **you are done.** Verify with
  `ls .claude/skills/route-audit`.
- ZenWrite links skills **per-skill**. If `route-audit` is missing, run `scripts/install.sh` from the
  skill directory, or do it by hand:

```bash
REPO=/home/josh/dev/01-Movemental-Core/zenwrite
LIB=/home/josh/dev/01-Movemental-Core/my-skills

mkdir -p "$REPO/.claude/skills" "$REPO/.cursor/skills"
ln -sfn "$LIB/route-audit" "$REPO/.claude/skills/route-audit"
ln -sfn "$LIB/route-audit" "$REPO/.cursor/skills/route-audit"
```

Also index the skill in the repo’s `.cursor/SKILLS.md` under **Route audit** so agents pick it up
from the playbook table.

Cursor and Claude Code both discover skills from these directories; linking both means the same skill
works whichever agent the user opens. Use relative links if the repos are ever cloned to a different
root — absolute links break on a new machine.

**Keep the symlinks out of git.** Add to `.gitignore` (once, at repo root):

```
.claude/skills/
.cursor/skills/
```

The skill is versioned in `my-skills`, not in each consuming repo. What *does* get committed to the
studio repo is the audit's output: `routes.manifest.yaml`, `e2e/routes/*.spec.ts`, and
`docs/audit/routes/STATE.md`. Those are repo artifacts, not skill artifacts.

> **Verify-before-use.** Confirm the actual `my-skills` path and the existing link style in this repo
> before running any of the above. If `.claude/skills` exists as a *real directory* containing real
> skill folders, do not blow it away — add the one symlink inside it.

## 3. Chrome DevTools MCP against a signed-in browser

The whole point is auditing what a logged-in user sees. Attach to a Chrome you have already signed
into rather than letting the MCP server launch a clean one.

**Launch Chrome once, leave it running:**

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-audit-profile" &

# Linux
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-audit-profile" &
```

Sign in by hand in that window, once. The profile persists, so later sessions skip this.

**Wire the MCP server** — `.cursor/mcp.json` in the studio repo (and/or `.mcp.json` for Claude Code):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"]
    }
  }
}
```

A dedicated `--user-data-dir` matters: it keeps the audit profile separate from daily browsing, so the
agent is never one mis-click from a real inbox or a real Stripe dashboard.

> **Verify-before-use.** Confirm the current `chrome-devtools-mcp` flag names and tool names against
> its README before the first run — the tool surface has changed across releases. The tools this skill
> assumes: `navigate_page`, `take_snapshot`, `take_screenshot`, `click`, `fill`,
> `list_console_messages`, `list_network_requests`, `evaluate_script`, `new_page`. If a name differs,
> adapt; the method does not change.

## 4. Preflight — run this at the start of every session

Do not skip. A stale debugging port produces a whole phase of confident, meaningless "failures".

1. **Port alive?** `curl -s http://127.0.0.1:9222/json/version` returns JSON. If not, relaunch Chrome.
2. **Still signed in?** `navigate_page` to an authenticated route; snapshot; confirm you are not
   looking at the login page. If signed out, sign in by hand — do not script it.
3. **App running?** The dev server (or the target deployment) responds. Record the base URL in STATE;
   auditing prod and dev in one phase produces incoherent results.
4. **Clean tree?** `git status --short`. Record the SHA — sign-offs are bound to it.
5. **Playwright installed?** `npx playwright --version`. If browsers are missing,
   `npx playwright install chromium`.

Record all five in the phase report. If any fail, stop and say so; do not proceed on a half-working
harness.

## 5. Signed-out second pass

After the authenticated phases are signed off, repeat the walk in a fresh incognito context (or a
second profile with no session). Public routes must render; private routes must redirect to `/login`
cleanly rather than 500 or flash protected content. Track these as a separate phase (`phase: auth`)
with its own spec file — the assertions are different, so they do not belong in the main specs.
