# git-land-main — multi-branch, stacks, cleanup

Read this when Phase 1 needs more than “land `HEAD`”.

## Classify every local topic branch

After `git fetch --prune origin`, for each local branch except `main` / `master`:

```bash
git for-each-ref --format='%(refname:short) %(upstream:short) %(upstream:track)' refs/heads
git log --oneline origin/main..<branch>
gh pr list --head <branch> --state all --json number,url,state,mergedAt,baseRefName
```

| Classification | Meaning | Action |
|----------------|---------|--------|
| **Empty vs main** | `git log origin/main..<branch>` is empty | Already on main (or never diverged). Candidate for Phase 10 delete only — still run Phase 9 style verify (`merge-base`) before `-d` |
| **Open PR** | `gh pr list` shows OPEN | Land that PR (phases 2–10). Do not open a second PR |
| **Merged PR, local leftover** | PR MERGED; local branch still exists | Phase 9 then Phase 10. No new PR |
| **Unmerged unique commits** | Commits on branch not in `origin/main`; no PR | Push + create PR, then land |
| **Gone upstream** | `[gone]` after prune | Check `gh pr view` / `git log origin/main..<branch>`. If merged, delete local with `-d`. If not merged, recover: `git push -u origin <branch>` then PR |
| **Dirty / stash-named** | `wip <branch>` stash exists | Pop only when switched onto that branch |

Ignore `HEAD` detached clones and dependabot noise unless the user named them.

## Multiple independent branches

Land **one at a time**. After each successful Phase 10:

1. Stay on synced `main`
2. Take the next queue entry
3. Merge fresh `origin/main` into it before gates/PR (Phase 4)

Default order:

1. Current branch (if it is a topic branch with unique commits or an open PR)
2. Branches with open PRs (oldest PR first, unless the user gave an order)
3. Other local branches with unique commits (alphabetical, or ask once)

Ask once when:

- Two branches touch the same files (`git diff origin/main...<a>` vs `...<b>`)
- The user said “all” but some branches look like abandoned experiments
- A branch has no unique commits and no merged PR (empty / identical to main)

Never combine two features into one squash/PR to “save time” unless asked.

## Stacked branches

A stack is when B was branched from A, not from main.

```bash
git merge-base A B
git log --oneline origin/main..A | wc -l
git log --oneline A..B | wc -l
```

If `A..B` is non-empty and B contains A’s commits, land **A first**.

After A is on `main` and deleted:

```bash
git switch B
git merge origin/main    # prefer merge; rebase B only if private + user asked
git push
```

Then PR B as usual. If B’s PR included A’s commits, GitHub will show a smaller diff after A merges — that is expected.

Do not squash-merge A and then rebase B with force-push unless the user wants a linear stack update.

## Worktrees

```bash
git worktree list
```

If `<branch>` is checked out in another path, `git branch -d` and `git switch` will fail or surprise the other tree.

- Land from the worktree that already has the branch, or
- `git worktree remove <path>` / switch that tree to `main` first

Never delete a branch that another worktree still has checked out.

## Merge method details

```bash
gh repo view --json deleteBranchOnMerge,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed,defaultBranchRef
```

- **Squash:** one commit on main; use when the topic branch is messy WIP. PR number still appears in the squash message if GitHub is configured that way.
- **Merge commit:** preserves branch commits; use when the repo already has `Merge pull request #N` history or the user wants to keep the commits.
- **Rebase merge:** rewriting; only on explicit request.

If `deleteBranchOnMerge` is true, GitHub may delete the remote branch even without `--delete-branch`. Still run Phase 9 + local `-d`.

Conflict with user wording: if they say “squash” but the repo disallows squash, stop and say so — do not silently use `--merge`.

## Already-merged cleanup pass

When the user only wants leftover branches gone (no new land):

```bash
git fetch --prune origin
git switch main
git pull --ff-only origin main
```

For each local topic branch:

```bash
git merge-base --is-ancestor <branch> origin/main && git branch -d <branch>
```

`-d` (not `-D`) is the safety gate. Report any that refused.

Optionally:

```bash
git remote prune origin
```

## Commands to never run in this skill

- `git push origin main` / `git push --force` to main
- `git merge <topic> ` while on `main` as the land mechanism
- `git reset --hard`, `git clean -fd`, `git stash drop` / `clear`
- `git branch -D`, `git push origin --delete` before Phase 9 `ON_MAIN`
- `gh pr merge --admin`
- `git commit --no-verify` unless the user asked

## Stop conditions (report and wait)

- Protected branch requires reviews you cannot satisfy
- CI red and out of scope / needs secrets or external services
- Conflict between branch intent and `origin/main` you cannot resolve without product input
- `git branch -d` refused after a supposed merge
- Detached production deploy hooks (hand off to `git-github-expert` if they also want `vercel --prod`)
