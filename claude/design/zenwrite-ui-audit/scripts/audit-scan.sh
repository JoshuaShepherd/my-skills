#!/usr/bin/env bash
# ZenWrite UI drift & engineering scanner.
# Fast, deterministic grep pass that surfaces the mechanical violations an audit should look at
# first. It does NOT judge — it LOCATES. Review each hit against references/audit-checklist.md
# (design) and references/react-tailwind-audit.md (engineering) for severity.
#
# Usage:
#   bash audit-scan.sh [SCOPE...]
# SCOPE defaults to "src". Pass files or dirs to narrow (e.g. src/components/HomeScreen.tsx).

set -uo pipefail

SCOPE=("${@:-src}")
TSX=(--include='*.tsx' --include='*.ts' --include='*.jsx' --include='*.css')
hr() { printf '\n\033[1m%s\033[0m\n' "$1"; }
scan() { grep -rnE "$1" "${SCOPE[@]}" "${TSX[@]}" 2>/dev/null; }

hr "1. Hardcoded hex in className (→ use @theme tokens: bg-brand-violet, etc.)  [CRITICAL/HIGH]"
scan '(bg|text|border|ring|from|to|via|fill|stroke)-\[#[0-9a-fA-F]{3,8}\]' || echo "  clean"

hr "2. Raw hex / rgb in inline style attributes  [HIGH]"
scan 'style=\{?\{?[^}]*(#[0-9a-fA-F]{3,8}|rgb\()' || echo "  clean"

hr "3. Dynamic Tailwind color strings (purge-unsafe — use static maps)  [CRITICAL]"
scan '(bg|text|border|ring)-\$\{' || echo "  clean"

hr "4. Raw palette instead of semantic tokens (prefer brand-*/community-* / getViewAccent)  [MEDIUM]"
scan '(bg|text|border|ring)-(indigo|violet|purple)-[0-9]{2,3}' || echo "  clean"

hr "5. Interactive elements — verify each has a focus-visible ring + accessible name  [HIGH]"
echo "   (each needs focus-visible:ring-2 focus-visible:ring-brand-violet; icon-only needs aria-label)"
scan '<(button|a|input|select|textarea)\b' | head -60 || echo "  none"

hr "6. Global dark-mode hijack (ANTI-PATTERN — ZenWrite is light-primary)  [CRITICAL]"
scan 'prefers-color-scheme|darkMode|media \(prefers-color-scheme' || echo "  clean"

hr "7. Ad-hoc status badges (should reuse StatusChip primitive)  [HIGH]"
scan '(bg-(emerald|amber|rose|stone)-[0-9]+.*rounded-full|rounded-full.*text-(emerald|amber|rose|stone)-[0-9]+)' | grep -vi 'StatusChip' | head -30 || echo "  clean"

hr "8. Async views — confirm Loading/Empty/Error states exist  [MEDIUM]"
echo "   (files using catalogs/lists should import from StateLayouts)"
scan 'LoadingState|EmptyState|ErrorState' | head -20 || echo "  none referenced"

hr "9. Effects — verify each useEffect with a timer/listener cleans up  [CRITICAL if leaking]"
scan 'useEffect|setInterval|setTimeout|addEventListener' | head -40 || echo "  none"

hr "10. Type escape hatches (repo is strict:true)  [HIGH]"
scan ':\s*any\b|as any\b' | head -20 || echo "  clean"

hr "11. List keys — check none use array index for reorderable lists  [HIGH]"
scan 'key=\{(index|i|idx)\}' || echo "  clean"

hr "12. Font hygiene — literary text should use font-serif (Newsreader)  [MEDIUM]"
echo "   (headings/body → font-serif; eyebrows/labels → font-manrope; keys/scores → font-mono)"
scan 'font-(serif|sans|manrope|mono)' | wc -l | xargs printf "  %s font-* utilities in scope\n"

hr "Done. Cross-reference hits against references/audit-checklist.md + react-tailwind-audit.md."
