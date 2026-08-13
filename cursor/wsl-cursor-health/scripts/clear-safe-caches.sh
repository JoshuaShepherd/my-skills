#!/usr/bin/env bash
# Clear *safe* Linux-side caches that accumulate during Cursor/Claude intensive work.
# Does NOT delete Cursor project history, Claude transcripts, or git data.
# Requires CONFIRM=1. Optional targets via args.
set -euo pipefail

CONFIRM="${CONFIRM:-0}"
if [[ "$CONFIRM" != "1" ]]; then
  echo "Refusing to clear caches without CONFIRM=1" >&2
  echo "Usage: CONFIRM=1 bash scripts/clear-safe-caches.sh [npx|playwright|trash|vite|all]" >&2
  exit 2
fi

targets=("$@")
if (( ${#targets[@]} == 0 )); then
  targets=(npx trash)
fi
if [[ "${targets[0]}" == "all" ]]; then
  targets=(npx playwright trash vite)
fi

cleared=()
skip() { echo "skip: $1"; }
do_rm() {
  local p="$1"
  if [[ -e "$p" ]]; then
    local before
    before=$(du -sh "$p" 2>/dev/null | awk '{print $1}')
    rm -rf "$p"
    echo "cleared: $p (was ${before})"
    cleared+=("$p")
  else
    skip "$p (missing)"
  fi
}

for t in "${targets[@]}"; do
  case "$t" in
    npx)
      do_rm "$HOME/.npm/_npx"
      ;;
    playwright)
      do_rm "$HOME/.cache/ms-playwright"
      ;;
    trash)
      do_rm "$HOME/.local/share/Trash/files"
      do_rm "$HOME/.local/share/Trash/info"
      ;;
    vite)
      # Only cwd-relative common caches; never touch node_modules
      for p in .vite .turbo; do
        if [[ -d "$PWD/$p" ]]; then
          do_rm "$PWD/$p"
        else
          skip "$PWD/$p"
        fi
      done
      ;;
    *)
      echo "unknown target: $t" >&2
      exit 1
      ;;
  esac
done

echo "done: cleared ${#cleared[@]} paths"
echo "NOTE: Windows Cursor Cache/CachedData must be cleared with Cursor quit, from Explorer or PowerShell."
echo "NOTE: wsl --shutdown must be run from Windows (PowerShell/cmd), not from inside this shell."
