#!/usr/bin/env bash
# Link the route-audit skill into a repo, house-convention style.
#
#   ./install.sh /home/josh/dev/01-Movemental-Core/movementalai-studio
#
# Safe to re-run. Never copies the skill — one canonical copy in my-skills,
# symlinks everywhere else, so the skill cannot drift between repos.

set -euo pipefail

REPO="${1:-}"
if [[ -z "$REPO" ]]; then
  echo "usage: install.sh <path-to-repo>" >&2
  exit 1
fi
if [[ ! -d "$REPO/.git" ]]; then
  echo "error: $REPO does not look like a git repo" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

echo "skill:  $SKILL_DIR"
echo "repo:   $REPO"
echo

# If the whole library is already linked, there is nothing to do.
for base in .claude/skills .cursor/skills; do
  target="$REPO/$base"
  if [[ -L "$target" ]]; then
    resolved="$(readlink -f "$target")"
    if [[ -e "$resolved/$SKILL_NAME" ]]; then
      echo "✓ $base is a symlink to $resolved — skill already available, nothing to do."
      continue
    fi
  fi

  mkdir -p "$target"
  ln -sfn "$SKILL_DIR" "$target/$SKILL_NAME"
  echo "✓ linked $base/$SKILL_NAME"
done

echo
echo "Add to $REPO/.gitignore if not already present:"
echo "  .claude/skills/"
echo "  .cursor/skills/"
echo
echo "The skill is versioned in my-skills. What belongs in this repo is the audit's"
echo "output: routes.manifest.yaml, e2e/routes/*.spec.ts, docs/audit/routes/."
