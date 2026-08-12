#!/usr/bin/env bash
# Symlink git-land-main into Cursor (and Claude) flat skill dirs.
#
#   ./install.sh              # home only
#   ./install.sh --all        # home (same as default)
#
# Never copies the skill — one canonical tree under my-skills/cursor/.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

mkdir -p "$HOME/.cursor/skills" "$HOME/.claude/skills"
ln -sfn "$SKILL_DIR" "$HOME/.cursor/skills/$SKILL_NAME"
ln -sfn "$SKILL_DIR" "$HOME/.claude/skills/$SKILL_NAME"
echo "✓ ~/.cursor/skills/$SKILL_NAME → $SKILL_DIR"
echo "✓ ~/.claude/skills/$SKILL_NAME → $SKILL_DIR"
