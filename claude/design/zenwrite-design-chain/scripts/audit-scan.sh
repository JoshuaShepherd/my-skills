#!/usr/bin/env bash
# ZenWrite design-chain drift scanner.
# Fast, deterministic grep pass that surfaces the mechanical violations an audit
# should look at first. It does NOT judge — it locates. Human/model review each hit.
#
# Usage:
#   bash audit-scan.sh [SCOPE...]
# SCOPE defaults to "src". Pass files or dirs to narrow (e.g. src/components/HomeScreen.tsx).

set -uo pipefail

SCOPE=("${@:-src}")
TSX=(--include='*.tsx' --include='*.ts' --include='*.jsx' --include='*.css')
hr() { printf '\n\033[1m%s\033[0m\n' "$1"; }
scan() { grep -rnE "$1" "${SCOPE[@]}" "${TSX[@]}" 2>/dev/null; }

hr "1. Hardcoded hex in className (→ use @theme tokens: bg-brand-violet, etc.)"
scan '(bg|text|border|ring|from|to|via|fill|stroke)-\[#[0-9a-fA-F]{3,8}\]' || echo "  clean"

hr "2. Raw hex / rgb in inline style attributes"
scan 'style=\{?\{?[^}]*(#[0-9a-fA-F]{3,8}|rgb\()' || echo "  clean"

hr "3. Dynamic Tailwind color strings (purge-unsafe — use static maps)"
scan '(bg|text|border|ring)-\$\{' || echo "  clean"

hr "4. Interactive elements — verify each has focus-visible ring"
echo "   (Review buttons/links/inputs below; each needs focus-visible:ring-2 focus-visible:ring-brand-violet)"
scan '<(button|a|input|select|textarea)\b' | head -60 || echo "  none"

hr "5. Global dark-mode hijack (ANTI-PATTERN — ZenWrite is light-primary)"
scan 'prefers-color-scheme|darkMode|media \(prefers-color-scheme' || echo "  clean"

hr "6. Ad-hoc status badges (should reuse StatusChip primitive)"
scan '(bg-(emerald|amber|rose|stone)-[0-9]+.*rounded-full|rounded-full.*text-(emerald|amber|rose|stone)-[0-9]+)' | grep -vi 'StatusChip' | head -30 || echo "  clean"

hr "7. Async views — confirm Loading/Empty/Error states exist"
echo "   (Files using catalogs/lists should import from StateLayouts)"
scan 'LoadingState|EmptyState|ErrorState' | head -20 || echo "  none referenced"

hr "8. Font hygiene — literary text should use font-serif (Newsreader)"
echo "   (Spot-check headings/body use font-serif; eyebrows/labels use font-manrope)"
scan 'font-(serif|sans|manrope|mono)' | wc -l | xargs printf "  %s font-* utilities in scope\n"

hr "Done. Cross-reference hits against references/audit-checklist.md severity table."
