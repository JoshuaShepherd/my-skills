# wsl-cursor-health — reference

## Why this environment gets slow

Intensive Cursor + Claude sessions stack:

- **WSL2 VM RAM balloon** + page cache that is slow to return to Windows
- **Swap** once the `.wslconfig` `memory=` cap is hit (feels like “Cursor lag” even if Windows Task Manager looks fine)
- **tsserver / extensionHost / MCP npx** node processes holding multi‑GB RSS
- **Caches**: `~/.cache` (Playwright), `~/.npm/_npx`, Windows `%APPDATA%\Cursor\Cache*`
- **VHDX growth** on `C:` (sparse helps; compact still needed sometimes)

## Probe thresholds (check-health.sh)

| Signal | WARN | CRIT |
|--------|------|------|
| Mem used (vs MemAvailable heuristic) | ≥80% used | ≥90% used or MemAvailable < 512MiB |
| Swap used | ≥15% or ≥1GiB | ≥40% or ≥4GiB |
| Load / nproc | ratio ≥1.0 | ratio ≥1.5 |
| `/` or `/tmp` df | ≥80% | ≥90% |
| Windows `C:` | ≥85% | ≥90% |
| `max_user_watches` | < 524288 | — |
| tsserver RSS sum | ≥1GiB | ≥2GiB |
| extensionHost RSS | ≥1.5GiB | — |
| node process count | ≥40 | — |
| `~/.cache` | ≥8GiB | — |
| `~/.cursor-server` | ≥4GiB | — |
| `~/.npm/_npx` | ≥2GiB | — |
| Windows Cursor Roaming | ≥3GiB | — |
| WSL uptime | ≥48h, or ≥24h **with** swap | — |
| `ext4.vhdx` | ≥80GiB | — |

Tune by editing the script if host RAM class changes.

## `.wslconfig` (Windows `%USERPROFILE%\.wslconfig`)

Takes effect only after `wsl --shutdown`.

Recommended pattern for heavy Cursor/Claude on a 16GB+ host:

```ini
[wsl2]
memory=12GB
swap=16GB
processors=6
localhostForwarding=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

Notes:

- Leave **headroom** for Windows + Cursor UI (do not set `memory=` to full host RAM).
- `autoMemoryReclaim=gradual` reduces the need for constant shutdowns; shutdown still helps after pathological swap.
- `sparseVhd=true` helps new freespace; it does not replace occasional compact.

## Soft IDE actions

| Symptom | Action |
|---------|--------|
| High tsserver RSS | Command Palette → **TypeScript: Restart TS Server** |
| Bloated extensionHost / sticky UI | **Developer: Reload Window** |
| MCP tools wedged after npx clear | Restart the MCP server / reload window |
| Many stale node children | Identify PIDs from probe; kill only orphans |

## Safe vs unsafe clears

**Safe (scripted, CONFIRM=1):**

- `~/.npm/_npx`
- `~/.cache/ms-playwright` (reinstall browsers later)
- Trash under `~/.local/share/Trash`
- cwd `.vite` / `.turbo`

**Safe but manual (Cursor quit first, Windows):**

- `%APPDATA%\Cursor\Cache`
- `%APPDATA%\Cursor\CachedData`
- `%APPDATA%\Cursor\Code Cache`
- `%APPDATA%\Cursor\GPUCache`

PowerShell example (Cursor **closed**):

```powershell
Remove-Item -Recurse -Force "$env:APPDATA\Cursor\Cache","$env:APPDATA\Cursor\CachedData","$env:APPDATA\Cursor\GPUCache" -ErrorAction SilentlyContinue
```

**Do not delete as part of this skill:**

- `~/.cursor/projects` (chat/composer state)
- `~/.claude` transcripts / projects (unless user explicitly asks)
- repo `node_modules`, `.git`, `.env*`
- entire `%APPDATA%\Cursor` (wipes settings/extensions)

## `wsl --shutdown`

Run from **Windows** PowerShell or cmd:

```powershell
wsl --shutdown
```

Effects: all distros stop; RAM returns to Windows; next open cold-starts Ubuntu/Cursor server. Warn about unsaved buffers and running `pnpm dev` / Docker-in-WSL.

## Compact VHDX (optional)

Only when host disk is tight or `ext4.vhdx` is huge:

1. `wsl --shutdown`
2. In PowerShell (path from probe):

```powershell
Optimize-VHD -Path "C:\Users\<You>\AppData\Local\Packages\<DistroPackage>\LocalState\ext4.vhdx" -Mode Full
```

`Optimize-VHD` needs Hyper-V module / Windows edition support. Alternative: `diskpart` → `select vdisk file=...` → `compact vdisk`.

If `sparseVhd=true` already and free space inside Linux is ample, compact is lower priority than memory/swap hygiene.

## inotify

For large monorepos:

```bash
# temporary
sudo sysctl -w fs.inotify.max_user_watches=524288
# persistent: /etc/sysctl.d/99-wsl-inotify.conf
```

## Re-probe

After any remediation, run `check-health.sh` again and compare `MACHINE_SUMMARY`.
