#!/usr/bin/env bash
# Read-only WSL + Cursor/Claude health probe for intensive coding sessions.
# Prints a human report + a final MACHINE_SUMMARY line for agents.
set -euo pipefail

SEVERITY_OK=0
SEVERITY_WARN=1
SEVERITY_CRIT=2
MAX_SEV=$SEVERITY_OK
FINDINGS=()

note() {
  local sev="$1"
  local code="$2"
  local msg="$3"
  FINDINGS+=("${sev}|${code}|${msg}")
  if (( sev > MAX_SEV )); then
    MAX_SEV=$sev
  fi
}

sev_label() {
  case "$1" in
    0) echo OK ;;
    1) echo WARN ;;
    2) echo CRIT ;;
    *) echo "?" ;;
  esac
}

bytes_from_human() {
  # Accepts du -sb first field or /proc kB values handled elsewhere.
  echo "$1"
}

pct() {
  local num="$1" den="$2"
  if (( den <= 0 )); then
    echo 0
    return
  fi
  echo $(( (num * 100) / den ))
}

hr_bytes() {
  local b="${1:-0}"
  if command -v numfmt >/dev/null 2>&1; then
    numfmt --to=iec --suffix=B "$b" 2>/dev/null || echo "${b}B"
  else
    echo "${b}B"
  fi
}

dir_bytes() {
  local p="$1"
  if [[ -e "$p" ]]; then
    du -sb "$p" 2>/dev/null | awk '{print $1}'
  else
    echo 0
  fi
}

echo "=== wsl-cursor-health ==="
echo "host=$(hostname)  time=$(date -Is)  kernel=$(uname -r)"
echo

# --- Memory / swap ---
mem_total_kb=$(awk '/MemTotal:/ {print $2}' /proc/meminfo)
mem_avail_kb=$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)
swap_total_kb=$(awk '/SwapTotal:/ {print $2}' /proc/meminfo)
swap_free_kb=$(awk '/SwapFree:/ {print $2}' /proc/meminfo)
swap_used_kb=$(( swap_total_kb - swap_free_kb ))
mem_used_pct=$(pct $((mem_total_kb - mem_avail_kb)) "$mem_total_kb")
swap_used_pct=$(pct "$swap_used_kb" "$swap_total_kb")

echo "## Memory"
echo "  MemTotal=$(hr_bytes $((mem_total_kb * 1024)))  MemAvailable=$(hr_bytes $((mem_avail_kb * 1024)))  used≈${mem_used_pct}%"
echo "  SwapTotal=$(hr_bytes $((swap_total_kb * 1024)))  SwapUsed=$(hr_bytes $((swap_used_kb * 1024)))  used≈${swap_used_pct}%"

if (( mem_used_pct >= 90 )) || (( mem_avail_kb < 512 * 1024 )); then
  note $SEVERITY_CRIT mem "Low free RAM (available $(hr_bytes $((mem_avail_kb * 1024))), used≈${mem_used_pct}%)"
elif (( mem_used_pct >= 80 )); then
  note $SEVERITY_WARN mem "Elevated RAM use (available $(hr_bytes $((mem_avail_kb * 1024))), used≈${mem_used_pct}%)"
fi

if (( swap_total_kb > 0 )); then
  # Absolute GiB thresholds matter more than % when swap=16GB is configured.
  if (( swap_used_pct >= 40 )) || (( swap_used_kb >= 4 * 1024 * 1024 )); then
    note $SEVERITY_CRIT swap "Heavy swap use ($(hr_bytes $((swap_used_kb * 1024))), ${swap_used_pct}%) — WSL memory reclaim / wsl --shutdown likely needed"
  elif (( swap_used_pct >= 15 )) || (( swap_used_kb >= 1024 * 1024 )); then
    note $SEVERITY_WARN swap "Notable swap use ($(hr_bytes $((swap_used_kb * 1024))), ${swap_used_pct}%) — session aging / memory pressure"
  fi
fi

# --- Load ---
echo
echo "## CPU / load"
ncpu=$(nproc)
loadavg=$(cut -d' ' -f1-3 /proc/loadavg)
load1=$(cut -d' ' -f1 /proc/loadavg)
uptime_str=$(uptime -p 2>/dev/null || true)
echo "  cpus=${ncpu}  loadavg=${loadavg}  ${uptime_str}"
# bash cannot float-compare easily; use awk
load_ratio=$(awk -v l="$load1" -v n="$ncpu" 'BEGIN { if (n<=0) print 0; else printf "%.2f", l/n }')
high_load=$(awk -v r="$load_ratio" 'BEGIN { exit !(r+0 >= 1.5) }' && echo yes || echo no)
warn_load=$(awk -v r="$load_ratio" 'BEGIN { exit !(r+0 >= 1.0) }' && echo yes || echo no)
if [[ "$high_load" == yes ]]; then
  note $SEVERITY_CRIT load "Load ${load1} on ${ncpu} CPUs (ratio ${load_ratio}) — CPU saturation"
elif [[ "$warn_load" == yes ]]; then
  note $SEVERITY_WARN load "Load ${load1} on ${ncpu} CPUs (ratio ${load_ratio})"
fi

# --- Disk ---
echo
echo "## Disk"
df -h / /tmp 2>/dev/null | sed 's/^/  /'
if [[ -d /mnt/c ]]; then
  df -h /mnt/c 2>/dev/null | tail -n +2 | sed 's/^/  /' || true
fi

root_use=$(df -P / | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
tmp_use=$(df -P /tmp 2>/dev/null | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
if (( root_use >= 90 )); then
  note $SEVERITY_CRIT disk "WSL root filesystem ${root_use}% full"
elif (( root_use >= 80 )); then
  note $SEVERITY_WARN disk "WSL root filesystem ${root_use}% full"
fi
if [[ -n "${tmp_use:-}" ]] && (( tmp_use >= 90 )); then
  note $SEVERITY_CRIT tmp "/tmp ${tmp_use}% full — builds/agents may fail"
elif [[ -n "${tmp_use:-}" ]] && (( tmp_use >= 80 )); then
  note $SEVERITY_WARN tmp "/tmp ${tmp_use}% full"
fi

if [[ -d /mnt/c ]]; then
  c_use=$(df -P /mnt/c 2>/dev/null | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
  if [[ -n "${c_use:-}" ]] && (( c_use >= 90 )); then
    note $SEVERITY_CRIT windisk "Windows C: ${c_use}% full — VHD growth / Cursor caches constrained"
  elif [[ -n "${c_use:-}" ]] && (( c_use >= 85 )); then
    note $SEVERITY_WARN windisk "Windows C: ${c_use}% full"
  fi
fi

# --- inotify ---
echo
echo "## File watchers"
watches=$(cat /proc/sys/fs/inotify/max_user_watches 2>/dev/null || echo 0)
instances=$(cat /proc/sys/fs/inotify/max_user_instances 2>/dev/null || echo 0)
echo "  max_user_watches=${watches}  max_user_instances=${instances}"
if (( watches > 0 && watches < 524288 )); then
  note $SEVERITY_WARN inotify "max_user_watches=${watches} (<524288) — large monorepos may drop watchers"
fi

# --- Top memory processes (Cursor / Node / Claude signals) ---
echo
echo "## Top memory processes"
ps -eo pid,rss,comm,args --sort=-rss 2>/dev/null | awk 'NR==1 || NR<=12 {printf "  %s\n", $0}'

tss_rss_kb=$(ps -eo rss,args --sort=-rss 2>/dev/null | awk '/tsserver|typescript/ && !/awk/ {s+=$1} END {print s+0}')
ext_rss_kb=$(ps -eo rss,args --sort=-rss 2>/dev/null | awk '/extensionHost/ && !/awk/ {s+=$1} END {print s+0}')
cursor_server_rss_kb=$(ps -eo rss,args --sort=-rss 2>/dev/null | awk '/\.cursor-server\// && !/awk/ {s+=$1} END {print s+0}')
node_count=$(ps -eo comm 2>/dev/null | grep -c '^node$' || true)

echo "  totals: tsserver_rss=$(hr_bytes $((tss_rss_kb * 1024)))  extensionHost_rss=$(hr_bytes $((ext_rss_kb * 1024)))  cursor-server_rss=$(hr_bytes $((cursor_server_rss_kb * 1024)))  node_procs=${node_count}"

if (( tss_rss_kb >= 2 * 1024 * 1024 )); then
  note $SEVERITY_CRIT tsserver "TypeScript language service using $(hr_bytes $((tss_rss_kb * 1024))) — reload TS server / close unused windows"
elif (( tss_rss_kb >= 1024 * 1024 )); then
  note $SEVERITY_WARN tsserver "TypeScript language service using $(hr_bytes $((tss_rss_kb * 1024)))"
fi

if (( ext_rss_kb >= 1536 * 1024 )); then
  note $SEVERITY_WARN extensionHost "extensionHost using $(hr_bytes $((ext_rss_kb * 1024))) — consider disabling heavy extensions / reload window"
fi

if (( node_count >= 40 )); then
  note $SEVERITY_WARN nodes "High node process count (${node_count}) — stale vite/test/mcp children?"
fi

# --- Cache / state sizes (Linux side) ---
echo
echo "## Linux caches & agent state"
declare -A PATHS=(
  ["~/.cache"]="$HOME/.cache"
  ["~/.cursor"]="$HOME/.cursor"
  ["~/.cursor/projects"]="$HOME/.cursor/projects"
  ["~/.cursor-server"]="$HOME/.cursor-server"
  ["~/.claude"]="$HOME/.claude"
  ["~/.npm/_npx"]="$HOME/.npm/_npx"
  ["~/.pnpm-store"]="$HOME/.pnpm-store"
  ["~/.local/share/Trash"]="$HOME/.local/share/Trash"
)

for label in "~/.cache" "~/.cursor" "~/.cursor/projects" "~/.cursor-server" "~/.claude" "~/.npm/_npx" "~/.pnpm-store" "~/.local/share/Trash"; do
  p="${PATHS[$label]}"
  if [[ -e "$p" ]]; then
    b=$(dir_bytes "$p")
    echo "  ${label}=$(hr_bytes "$b")"
    case "$label" in
      "~/.cache")
        if (( b >= 8 * 1024 * 1024 * 1024 )); then
          note $SEVERITY_WARN linux_cache "~/.cache is $(hr_bytes "$b") — Playwright/npm/pip caches candidates"
        fi
        ;;
      "~/.cursor-server")
        if (( b >= 4 * 1024 * 1024 * 1024 )); then
          note $SEVERITY_WARN cursor_server "~/.cursor-server is $(hr_bytes "$b") — old server builds can be pruned after reload"
        fi
        ;;
      "~/.npm/_npx")
        if (( b >= 2 * 1024 * 1024 * 1024 )); then
          note $SEVERITY_WARN npx "~/.npm/_npx is $(hr_bytes "$b") — stale MCP npx installs"
        fi
        ;;
      "~/.local/share/Trash")
        if (( b >= 1 * 1024 * 1024 * 1024 )); then
          note $SEVERITY_WARN trash "Trash is $(hr_bytes "$b")"
        fi
        ;;
    esac
  else
    echo "  ${label}=(missing)"
  fi
done

# Playwright browsers specifically
pw="$HOME/.cache/ms-playwright"
if [[ -d "$pw" ]]; then
  echo "  ~/.cache/ms-playwright=$(hr_bytes "$(dir_bytes "$pw")")"
fi

# --- Windows Cursor caches via /mnt/c ---
echo
echo "## Windows Cursor / WSL config"
win_user="${WSL_CURSOR_WIN_USER:-}"
if [[ -z "$win_user" ]] && command -v cmd.exe >/dev/null 2>&1; then
  win_user=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r' || true)
fi
win_home=""
if [[ -n "${win_user:-}" && -d "/mnt/c/Users/${win_user}" ]]; then
  win_home="/mnt/c/Users/${win_user}"
fi

if [[ -n "$win_home" ]]; then
  for rel in \
    "AppData/Roaming/Cursor" \
    "AppData/Roaming/Cursor/Cache" \
    "AppData/Roaming/Cursor/CachedData" \
    "AppData/Roaming/Cursor/GPUCache" \
    "AppData/Roaming/Cursor/Code Cache" \
    "AppData/Local/Cursor" \
    ".wslconfig"; do
    p="${win_home}/${rel}"
    if [[ -f "$p" ]]; then
      echo "  ${rel}=file ($(hr_bytes "$(stat -c%s "$p" 2>/dev/null || echo 0)"))"
    elif [[ -d "$p" ]]; then
      # du across /mnt/c can be slow; cap depth with timeout-ish via du -sh
      sz=$(du -sb "$p" 2>/dev/null | awk '{print $1}' || echo 0)
      echo "  ${rel}=$(hr_bytes "$sz")"
      if [[ "$rel" == "AppData/Roaming/Cursor" ]] && (( sz >= 3 * 1024 * 1024 * 1024 )); then
        note $SEVERITY_WARN win_cursor "Windows Cursor Roaming profile $(hr_bytes "$sz") — Cache/CachedData clear candidates"
      fi
    fi
  done

  if [[ -f "${win_home}/.wslconfig" ]]; then
    echo "  --- .wslconfig ---"
    sed 's/^/  /' "${win_home}/.wslconfig"
    if ! grep -qiE '^\s*autoMemoryReclaim\s*=' "${win_home}/.wslconfig"; then
      note $SEVERITY_WARN wslconfig "No autoMemoryReclaim in .wslconfig — gradual reclaim helps long Cursor sessions"
    fi
    if ! grep -qiE '^\s*memory\s*=' "${win_home}/.wslconfig"; then
      note $SEVERITY_WARN wslconfig "No memory= cap in .wslconfig — WSL can starve Windows/Cursor UI"
    fi
  else
    note $SEVERITY_WARN wslconfig "No %USERPROFILE%\\.wslconfig — set memory/swap/autoMemoryReclaim for heavy Cursor use"
  fi

  # VHDX size (best-effort; Store distros, Docker, and `wsl --import` layouts)
  vhdx=$(
    find \
      "${win_home}/AppData/Local/Packages" \
      "${win_home}/AppData/Local/wsl" \
      "${win_home}/AppData/Local/Docker" \
      -name 'ext4.vhdx' 2>/dev/null | head -1 || true
  )
  if [[ -n "${vhdx:-}" ]]; then
    vhdx_b=$(stat -c%s "$vhdx" 2>/dev/null || echo 0)
    echo "  ext4.vhdx=$(hr_bytes "$vhdx_b")  path=${vhdx}"
    if (( vhdx_b >= 80 * 1024 * 1024 * 1024 )); then
      note $SEVERITY_WARN vhdx "WSL VHDX is $(hr_bytes "$vhdx_b") — consider compact after wsl --shutdown if host disk is tight"
    fi
  else
    echo "  ext4.vhdx=(not found — optional: locate via PowerShell Get-ChildItem -Recurse -Filter ext4.vhdx)"
  fi
else
  echo "  (could not resolve Windows user profile under /mnt/c/Users)"
  note $SEVERITY_WARN winpath "Windows profile not resolved — skip host Cursor cache / .wslconfig checks"
fi

# --- Repo-local caches if cwd looks like a project ---
echo
echo "## Workspace caches (cwd)"
cwd=$(pwd -P 2>/dev/null || pwd)
echo "  cwd=${cwd}"
for rel in node_modules .pnpm-store .turbo .vite dist playwright-report test-results .next coverage; do
  if [[ -e "${cwd}/${rel}" ]]; then
    echo "  ./${rel}=$(hr_bytes "$(dir_bytes "${cwd}/${rel}")")"
  fi
done

# --- Uptime heuristic for WSL session age ---
echo
echo "## Session age"
boot_epoch=$(date -d "$(uptime -s 2>/dev/null)" +%s 2>/dev/null || echo 0)
now_epoch=$(date +%s)
if (( boot_epoch > 0 )); then
  age_h=$(( (now_epoch - boot_epoch) / 3600 ))
  echo "  wsl_uptime_hours≈${age_h}  since=$(uptime -s 2>/dev/null)"
  if (( age_h >= 24 )) && (( swap_used_kb >= 512 * 1024 )); then
    note $SEVERITY_WARN session "WSL up ${age_h}h with swap in use — restart cycle often restores snappiness"
  elif (( age_h >= 48 )); then
    note $SEVERITY_WARN session "WSL up ${age_h}h — long sessions accumulate Cursor/TS/Node RSS"
  fi
else
  echo "  (uptime -s unavailable)"
fi

# --- Findings ---
echo
echo "## Findings"
if (( ${#FINDINGS[@]} == 0 )); then
  echo "  (none — no thresholds crossed)"
else
  for f in "${FINDINGS[@]}"; do
    IFS='|' read -r sev code msg <<<"$f"
    printf "  [%s] %s — %s\n" "$(sev_label "$sev")" "$code" "$msg"
  done
fi

echo
echo "## Recommended next actions (do not auto-run destructive steps)"
case $MAX_SEV in
  2)
    echo "  1. Save work. From Windows PowerShell: wsl --shutdown  (kills this session)"
    echo "  2. Reopen Cursor / distro. Re-run this script."
    echo "  3. If still heavy: clear safe caches (see skill reference) + reload TS server / window"
    ;;
  1)
    echo "  1. Prefer soft fixes first: Developer: Reload Window, TypeScript: Restart TS Server"
    echo "  2. Clear safe Linux caches if sizes flagged (Playwright/npx/Trash)"
    echo "  3. If swap stays elevated after soft fixes: wsl --shutdown from Windows"
    ;;
  *)
    echo "  No remediation required. Re-run after long agent sessions or when UI feels laggy."
    ;;
esac

codes=$(printf '%s\n' "${FINDINGS[@]:-}" | awk -F'|' 'NF{print $2}' | paste -sd, -)
echo
echo "MACHINE_SUMMARY severity=$(sev_label "$MAX_SEV") findings=${#FINDINGS[@]} codes=${codes:-none} mem_used_pct=${mem_used_pct} swap_used_pct=${swap_used_pct} load_ratio=${load_ratio} tss_rss_kb=${tss_rss_kb} node_count=${node_count}"
exit 0
