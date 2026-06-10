#!/usr/bin/env bash
# Install a skill from my-skills into the correct runtime directory (flat symlink target).
#
# Usage:
#   scripts/install-skill.sh article-author
#   scripts/install-skill.sh ssot-dashboard --runtime cursor
#   scripts/install-skill.sh find-skills --runtime agents
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="${1:-}"
RUNTIME="${RUNTIME:-claude}"
DOMAINS_FILE="$REPO_ROOT/scripts/skill-domains.json"
MANIFEST="$REPO_ROOT/SKILLS_MANIFEST.json"

usage() {
  echo "Usage: $0 <skill-name> [--runtime claude|cursor|agents]" >&2
  exit 1
}

[[ -n "$SKILL_NAME" ]] || usage

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --runtime)
      RUNTIME="${2:-}"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

resolve_claude_src() {
  local name="$1"
  local domain
  domain="$(python3 - "$DOMAINS_FILE" "$name" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
print(data["skills"].get(sys.argv[2], ""))
PY
)"
  if [[ -n "$domain" && -d "$REPO_ROOT/claude/$domain/$name" ]]; then
    echo "$REPO_ROOT/claude/$domain/$name"
    return 0
  fi
  if [[ -f "$MANIFEST" ]]; then
    local path
    path="$(python3 - "$MANIFEST" "$name" <<'PY'
import json, sys
manifest = json.load(open(sys.argv[1]))
name = sys.argv[2]
for key, entry in manifest.get("skills", {}).items():
    if entry.get("runtime_name") == name or key.endswith("/" + name):
        print(key.replace("/", "/"))
        break
PY
)"
    if [[ -n "$path" && -d "$REPO_ROOT/$path" ]]; then
      echo "$REPO_ROOT/$path"
      return 0
    fi
  fi
  return 1
}

case "$RUNTIME" in
  claude)
    SRC="$(resolve_claude_src "$SKILL_NAME")" || {
      echo "Could not resolve Claude skill: $SKILL_NAME" >&2
      exit 1
    }
    DEST="$HOME/.claude/skills/$SKILL_NAME"
    ;;
  cursor)
    SRC="$REPO_ROOT/cursor/$SKILL_NAME"
    DEST="$HOME/.cursor/skills/$SKILL_NAME"
    ;;
  agents)
    SRC="$REPO_ROOT/agents/$SKILL_NAME"
    DEST="$HOME/.agents/skills/$SKILL_NAME"
    ;;
  *)
    echo "Unknown runtime: $RUNTIME" >&2
    exit 1
    ;;
esac

if [[ ! -d "$SRC" ]]; then
  echo "Source bundle not found: $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
ln -sfn "$SRC" "$DEST"
echo "Installed $SKILL_NAME → $DEST"
