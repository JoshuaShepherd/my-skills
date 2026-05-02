---
name: color-audit
description: Expert color palette audit — verify light/dark mode alignment, WCAG contrast compliance, 60-30-10 distribution, and overall color harmony. Checks the palette itself, not just usage.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Expert color palette audit — verify light/dark mode alignment, WCAG contrast compliance, 60-30-10 distribution, and overall color harmony across the platform.

Target: $ARGUMENTS

If no target is provided, audit the full palette in `globals.css` and spot-check usage across `src/components/` and `src/app/(public)/`.

## Before Starting

1. Read `src/app/globals.css` — extract ALL color tokens from `:root` (dark) and `.light` blocks.
2. Read `tailwind.config.ts` — verify every CSS var has a corresponding Tailwind color mapping.
3. Read `_docs/design/DESIGN_CHAIN.md` — confirm the palette spec (Pastoral-Warm: gold primary, warm neutrals).
4. Read `_docs/design/DESIGN_CHARTER.md` if it exists — confirm the color philosophy.

## Audit Dimensions

### 1. TOKEN COMPLETENESS

Verify every token defined in `:root` has a matching override in `.light`:

| Token | `:root` (dark) | `.light` | Status |
|-------|----------------|----------|--------|

**Check for:**
- Tokens defined in `:root` but missing from `.light` (will inherit dark values in light mode)
- Tokens defined in `.light` but not in `:root` (orphaned light-only tokens)
- Tokens in `tailwind.config.ts` colors that reference undefined CSS vars

### 2. CONTRAST COMPLIANCE (WCAG 2.1 AA)

For each semantic token pair, compute the contrast ratio. Use the HSL values from globals.css, convert to hex/RGB, then calculate.

**Required ratios:**
- **Normal text (< 18px / < 14px bold):** 4.5:1 minimum
- **Large text (≥ 18px / ≥ 14px bold):** 3:1 minimum
- **UI components and graphical objects:** 3:1 minimum
- **Focus indicators:** 3:1 against adjacent colors

**Critical pairs to check:**

| Pair | Background Token | Foreground Token | Context |
|------|-----------------|------------------|---------|
| Body text | `--background` | `--foreground` | Main content |
| Card text | `--card` | `--card-foreground` | Cards |
| Primary button | `--primary` | `--primary-foreground` | CTAs |
| Secondary button | `--secondary` | `--secondary-foreground` | Secondary actions |
| Muted text | `--background` | `--muted-foreground` | Subtle labels |
| Muted on card | `--card` | `--muted-foreground` | Card subtitles |
| Destructive | `--destructive` | `--destructive-foreground` | Error states |
| Success | `--success` | `--success-foreground` | Success states |
| Popover text | `--popover` | `--popover-foreground` | Dropdowns |
| Input text | `--input` | `--foreground` | Form fields |
| Border visibility | `--background` | `--border` | Borders |
| Focus ring | `--background` | `--ring` | Focus states |
| Light section text | `--bg-light` | `--text-dark` | Light bands |
| Light section muted | `--bg-light` | `--text-muted-dark` | Light band subtitles |

**Check both `:root` (dark) and `.light` mode values.**

### 3. COLOR HARMONY & PALETTE COHERENCE

Evaluate the palette as a professional UI designer:

- **Hue consistency:** All warm neutrals should share a similar hue angle (around 24-36 for this palette). Flag any neutral that drifts into cool territory (blue/green hue).
- **Saturation scale:** Neutrals should have low, consistent saturation (0-15%). Flag any neutral with saturation > 20%.
- **Lightness ramp:** Background → card → secondary → muted should form a smooth, monotonic lightness ramp. Flag any inversions or large jumps.
- **Primary vs accent distinction:** `--primary` (gold, for CTAs) must be clearly distinct from `--accent` (subtle interactive tint). If they're too similar, outline button hovers will look like primary buttons.
- **Destructive vs success:** These should be clearly distinguishable, including for color-blind users (red-green). Check that they differ in lightness or saturation, not just hue.

### 4. 60-30-10 COLOR DISTRIBUTION

Audit the actual usage distribution across key pages:

- **60% (dominant):** `--background` and `--foreground` — the base canvas. Should dominate.
- **30% (secondary):** `--card`, `--muted`, `--secondary`, `--border` — structural supporting colors.
- **10% (accent):** `--primary` (gold) — CTAs, active states, highlights. Should be sparingly used for impact.

**Red flags:**
- Primary/gold used as a background for large sections (overuse kills impact)
- Too many competing accent colors (primary + destructive + success all visible in one view)
- Muted-foreground used for main body text (too low contrast, should be foreground)
- Border color too prominent (draws attention away from content)

### 5. DARK/LIGHT MODE PERCEPTUAL BALANCE

Check that both modes feel equally polished:

- **Dark mode:** Backgrounds should be truly dark (lightness < 12%). Card should be slightly lighter than background. Text should be warm cream, not pure white (pure white on dark = harsh).
- **Light mode:** Backgrounds should be warm off-white (not pure white). Card can be white. Text should be warm dark, not pure black (pure black on light = harsh).
- **Primary in both modes:** Gold may need to shift slightly between modes. Too-bright gold on light backgrounds washes out; too-dark gold on dark backgrounds lacks pop.
- **Border visibility:** Borders should be visible but subtle in both modes. Check that `--border` has sufficient contrast against `--background` in both themes (target 1.5:1+ for decorative borders, 3:1+ for functional borders).
- **Shadow behavior:** Primary glow shadows should be visible in dark mode and not overwhelming in light mode.

### 6. ACCESSIBILITY BEYOND CONTRAST

- **Color-only information:** Search for UI patterns that convey meaning through color alone (e.g., status dots without labels, color-coded categories without text). Flag these.
- **Focus visibility:** Verify `--ring` is visible against both `--background` and `--card` in both themes.
- **Error states:** Verify `--destructive` is distinguishable from `--primary` — users should not confuse error and brand.
- **Hover/active states:** Check that hover states using `--accent` or `primary/80` maintain contrast with their text.
- **Chart colors:** Verify the 5 chart colors are distinguishable from each other AND from the background in both themes.

### 7. COMPONENT SPOT-CHECK

Scan a sample of component files for color usage violations:

- Components using hardcoded colors instead of tokens (feed into tailwind-cleanup skill)
- Components where bg/text token pairs are mismatched (e.g., `bg-primary` with `text-foreground` instead of `text-primary-foreground`)
- Components using opacity modifiers that drop contrast below WCAG thresholds (e.g., `text-foreground/50` as body text)
- Gradients that make text unreadable at certain scroll positions

## Fixing Protocol

1. **Token fixes (D1):** Edit `globals.css` `:root` and/or `.light` blocks. Both themes must be updated in tandem.
2. **Mapping fixes:** If adding a new token, add the Tailwind mapping in `tailwind.config.ts`.
3. **Never change primary brand color** without explicit user approval — gold (#b58c4c / hsl 36 48% 50%) is the brand identity.
4. **Contrast fixes:** Prefer adjusting lightness over changing hue. Bump lightness in 3-5% increments until ratio is met.
5. **Test after fixing:** Verify both dark and light mode in browser after any token change.

## Output Format

```
## Color Palette Audit

### Palette Summary
| Token | Dark Mode (HSL) | Dark Hex | Light Mode (HSL) | Light Hex | Parity |
|-------|----------------|----------|-------------------|-----------|--------|

### Contrast Report
| Pair | Dark Ratio | Light Ratio | WCAG AA | Status |
|------|-----------|-------------|---------|--------|
| bg/fg | 15.2:1 | 12.8:1 | 4.5:1 | PASS |
| bg/muted-fg | 3.8:1 | 4.2:1 | 4.5:1 | FAIL (dark) |

### Issues Found
1. [SEVERITY: CRITICAL/HIGH/MEDIUM/LOW] — description
   - Current: value
   - Recommended: value
   - Affected: list of components/pages

### Color Harmony Assessment
- Hue consistency: [PASS/ADJUST]
- Saturation scale: [PASS/ADJUST]
- Lightness ramp: [PASS/ADJUST]
- 60-30-10 distribution: [PASS/ADJUST]
- Dark/light perceptual balance: [PASS/ADJUST]

### Recommendations
1. [Priority fix with specific token change]
2. ...
```

## Rules

- Always audit BOTH dark and light mode — never just one.
- Present the full audit report before making any changes.
- When computing contrast, use the actual HSL values from globals.css, converted to RGB. Do not estimate.
- Do not change the primary brand hue (gold ~36°) without user approval.
- If contrast fails, prefer adjusting lightness of the weaker token rather than changing the stronger one.
- Flag but do not auto-fix brand-level decisions (e.g., "primary is too close to destructive"). These need user input.
- This audit complements the tailwind-cleanup skill — color-audit checks the palette itself, tailwind-cleanup checks usage in components.
