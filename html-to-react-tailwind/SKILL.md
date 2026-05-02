---
name: html-to-react-tailwind
description: Convert HTML/CSS/JS files into production-ready React components with Tailwind CSS. Handles CSS-to-utility mapping, JS-to-React state/effects, component decomposition, and TypeScript types. Triggers on "HTML to React", "convert HTML", "migrate to React", "React conversion".
allowed-tools:
  - "Read"
  - "Write"
  - "Edit"
  - "Bash"
  - "Grep"
  - "Glob"
  - "Agent"
---

# HTML/CSS/JS to React + Tailwind Conversion

Convert static HTML/CSS/JavaScript into idiomatic, production-ready React components styled with Tailwind CSS.

Convert: $ARGUMENTS

$ARGUMENTS should include:
- Source HTML file path(s) or inline HTML to convert
- Optionally: target output directory
- Optionally: framework context (Next.js, Vite, React Router)
- Optionally: Tailwind version (v3 or v4 — default v4)
- Optionally: component library preference (shadcn/ui, Radix, headless)
- Optionally: "audit" to analyze HTML before converting
- Empty — ask the user what to convert

## Before Starting

1. **Read the source HTML/CSS/JS files completely** — understand every element, style, and behavior before writing any React code
2. **Read the project's existing styles** — check `globals.css`, `tailwind.config.ts`, or CSS entry point for existing theme tokens
3. **Read existing components** — check `src/components/` or equivalent for patterns already established in the project
4. **Identify the target stack** — check `package.json` for React version, TypeScript, Tailwind version, and existing component libraries

## Conversion Workflow

### Phase 1: Audit the Source

Analyze the HTML/CSS/JS and produce a structured inventory:

```
## Source Audit

### Structure
- [list every semantic section: header, nav, hero, features, footer, etc.]
- [note nesting depth and repeated patterns]

### Styling Approach
- [ ] Inline styles → will map to Tailwind utilities
- [ ] CSS classes (external stylesheet) → will map to Tailwind utilities
- [ ] CSS variables → will map to @theme tokens
- [ ] Media queries → will map to responsive prefixes (sm:, md:, lg:)
- [ ] Animations/transitions → will map to Tailwind animate-* or CSS @keyframes
- [ ] Pseudo-elements (::before, ::after) → will use Tailwind before:/after: or custom CSS

### Behavior (JavaScript)
- [ ] DOM manipulation → will become React state + JSX conditionals
- [ ] Event listeners → will become React event handlers (onClick, onChange, etc.)
- [ ] Fetch/AJAX → will become useEffect + fetch or data fetching library
- [ ] Timers/intervals → will become useEffect with cleanup
- [ ] localStorage/sessionStorage → will become custom hook
- [ ] Form validation → will become controlled components with validation
- [ ] Scroll effects → will become useEffect with IntersectionObserver or scroll listener
- [ ] Modals/toggles → will become useState boolean + conditional rendering

### Repeated Patterns
- [identify elements that appear 2+ times with same structure — these become components]
- [identify elements that share styling — these share variant props]

### External Dependencies
- [fonts, icon libraries, CDN scripts, images, etc.]
```

### Phase 2: Map CSS to Tailwind

Convert every CSS property to its Tailwind equivalent. Follow these rules strictly:

#### Layout & Display

| CSS | Tailwind |
|-----|----------|
| `display: flex` | `flex` |
| `display: grid` | `grid` |
| `display: none` | `hidden` |
| `display: block` | `block` |
| `display: inline-flex` | `inline-flex` |
| `position: relative` | `relative` |
| `position: absolute` | `absolute` |
| `position: fixed` | `fixed` |
| `position: sticky` | `sticky` |
| `z-index: 10` | `z-10` |

#### Flexbox

| CSS | Tailwind |
|-----|----------|
| `flex-direction: column` | `flex-col` |
| `align-items: center` | `items-center` |
| `justify-content: center` | `justify-center` |
| `justify-content: space-between` | `justify-between` |
| `flex-wrap: wrap` | `flex-wrap` |
| `flex: 1` | `flex-1` |
| `flex-shrink: 0` | `shrink-0` |
| `gap: 16px` | `gap-4` |

#### Grid

| CSS | Tailwind |
|-----|----------|
| `grid-template-columns: repeat(3, 1fr)` | `grid-cols-3` |
| `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` | `grid-cols-[repeat(auto-fit,minmax(300px,1fr))]` |
| `grid-column: span 2` | `col-span-2` |
| `grid-gap: 24px` | `gap-6` |

#### Spacing (4px base: 1 unit = 0.25rem = 4px)

| CSS | Tailwind |
|-----|----------|
| `margin: 0` | `m-0` |
| `margin: 4px` | `m-1` |
| `margin: 8px` | `m-2` |
| `margin: 12px` | `m-3` |
| `margin: 16px` | `m-4` |
| `margin: 24px` | `m-6` |
| `margin: 32px` | `m-8` |
| `margin: 0 auto` | `mx-auto` |
| `margin-top: 16px` | `mt-4` |
| `padding: 16px` | `p-4` |
| `padding: 16px 24px` | `px-6 py-4` |

For non-standard values, use arbitrary values: `margin: 13px` → `m-[13px]` (but prefer snapping to the scale).

#### Typography

| CSS | Tailwind |
|-----|----------|
| `font-size: 12px` / `0.75rem` | `text-xs` |
| `font-size: 14px` / `0.875rem` | `text-sm` |
| `font-size: 16px` / `1rem` | `text-base` |
| `font-size: 18px` / `1.125rem` | `text-lg` |
| `font-size: 20px` / `1.25rem` | `text-xl` |
| `font-size: 24px` / `1.5rem` | `text-2xl` |
| `font-size: 30px` / `1.875rem` | `text-3xl` |
| `font-weight: 400` | `font-normal` |
| `font-weight: 500` | `font-medium` |
| `font-weight: 600` | `font-semibold` |
| `font-weight: 700` | `font-bold` |
| `text-align: center` | `text-center` |
| `text-decoration: underline` | `underline` |
| `text-transform: uppercase` | `uppercase` |
| `line-height: 1.5` | `leading-normal` |
| `letter-spacing: -0.025em` | `tracking-tight` |
| `white-space: nowrap` | `whitespace-nowrap` |
| `text-overflow: ellipsis` + `overflow: hidden` | `truncate` |

#### Colors

Map source colors to semantic tokens. Never use raw hex in components.

```
Source CSS:                    →  Tailwind:
color: #333                   →  text-foreground
color: #666                   →  text-muted-foreground
background-color: #fff        →  bg-background
background-color: #f5f5f5     →  bg-muted
border-color: #e5e5e5         →  border-border
background-color: #0066FF     →  bg-primary
color: white (on primary bg)  →  text-primary-foreground
```

If the source has a custom color palette, extract it to `@theme` tokens in CSS:

```css
@theme {
  --color-brand: #0066FF;
  --color-brand-light: #E6F0FF;
  --color-brand-dark: #0052CC;
}
```

#### Borders & Rounded Corners

| CSS | Tailwind |
|-----|----------|
| `border: 1px solid` | `border` |
| `border-bottom: 1px solid` | `border-b` |
| `border-radius: 4px` | `rounded` |
| `border-radius: 8px` | `rounded-lg` |
| `border-radius: 12px` | `rounded-xl` |
| `border-radius: 9999px` | `rounded-full` |

#### Shadows

| CSS | Tailwind |
|-----|----------|
| `box-shadow: 0 1px 2px rgba(0,0,0,0.05)` | `shadow-sm` |
| `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` | `shadow-md` |
| `box-shadow: 0 10px 15px rgba(0,0,0,0.1)` | `shadow-lg` |

#### Responsive Breakpoints

Map media queries to Tailwind responsive prefixes (mobile-first):

```
Source CSS:                                  Tailwind:
@media (min-width: 640px) { ... }      →    sm:...
@media (min-width: 768px) { ... }      →    md:...
@media (min-width: 1024px) { ... }     →    lg:...
@media (min-width: 1280px) { ... }     →    xl:...
```

Write base styles for mobile, then add `sm:`, `md:`, `lg:` prefixes for larger screens.

```html
<!-- Source: display:none on mobile, flex on desktop -->
<nav class="hidden md:flex items-center gap-6">
```

#### Transitions & Animations

| CSS | Tailwind |
|-----|----------|
| `transition: all 0.2s ease` | `transition-all duration-200 ease-in-out` |
| `transition: color 0.15s` | `transition-colors duration-150` |
| `transition: transform 0.3s` | `transition-transform duration-300` |
| `transform: scale(1.05)` | `scale-105` (on hover: `hover:scale-105`) |
| `opacity: 0` → `opacity: 1` | Use `animate-fade-in` (define in @theme) |

#### States

| CSS | Tailwind |
|-----|----------|
| `:hover` | `hover:` |
| `:focus` | `focus-visible:` (prefer over `focus:`) |
| `:active` | `active:` |
| `:disabled` | `disabled:` |
| `:first-child` | `first:` |
| `:last-child` | `last:` |
| `::placeholder` | `placeholder:` |
| `::before` | `before:` |
| `::after` | `after:` |

### Phase 3: Convert JavaScript to React Patterns

#### DOM Manipulation → React State

```javascript
// SOURCE JS
document.getElementById('menu').classList.toggle('hidden');
document.querySelector('.count').textContent = count;
```

```tsx
// REACT
const [isMenuOpen, setIsMenuOpen] = useState(false);
const [count, setCount] = useState(0);

return (
  <>
    {isMenuOpen && <Menu />}
    <span>{count}</span>
  </>
);
```

#### Event Listeners → React Event Handlers

```javascript
// SOURCE JS
button.addEventListener('click', () => { ... });
input.addEventListener('input', (e) => { ... });
window.addEventListener('scroll', handleScroll);
```

```tsx
// REACT
<button onClick={() => { ... }}>
<input onChange={(e) => { ... }}>

useEffect(() => {
  const handleScroll = () => { ... };
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

#### Fetch/AJAX → useEffect or Data Fetching

```javascript
// SOURCE JS
fetch('/api/data')
  .then(res => res.json())
  .then(data => renderItems(data));
```

```tsx
// REACT
const [data, setData] = useState<Item[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetch('/api/data')
    .then(res => res.json())
    .then(setData)
    .finally(() => setLoading(false));
}, []);
```

#### Timers → useEffect with Cleanup

```javascript
// SOURCE JS
setInterval(() => { tick() }, 1000);
```

```tsx
// REACT
useEffect(() => {
  const id = setInterval(() => tick(), 1000);
  return () => clearInterval(id);
}, []);
```

#### Form Handling → Controlled Components

```javascript
// SOURCE JS
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value;
});
```

```tsx
// REACT
const [name, setName] = useState('');

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  // use name state directly
};

<form onSubmit={handleSubmit}>
  <input value={name} onChange={(e) => setName(e.target.value)} />
</form>
```

#### LocalStorage → Custom Hook

```javascript
// SOURCE JS
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme');
```

```tsx
// REACT
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

const [theme, setTheme] = useLocalStorage('theme', 'light');
```

### Phase 4: Decompose into Components

#### Decomposition Rules

| Principle | Rule |
|-----------|------|
| Single Responsibility | Each component does ONE thing |
| Reuse threshold | If a pattern appears 2+ times, extract it |
| Props over hardcoding | All text, colors, sizes become props |
| Composition | Small components compose into larger ones |
| Naming | PascalCase, descriptive, matches domain language |

#### Component Hierarchy

```
components/
├── ui/                    # Primitives (Button, Input, Badge, Avatar)
├── patterns/              # Composed patterns (Card, SearchBar, Dropdown)
├── sections/              # Page sections (Header, Hero, Features, Footer)
└── layouts/               # Layout wrappers (PageLayout, SidebarLayout)
```

#### Identify Components From HTML

Look for these signals in the source HTML:

1. **Repeated structure** — same HTML pattern with different content → component with props
2. **Interactive regions** — forms, modals, dropdowns, toggles → stateful component
3. **Semantic sections** — `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>` → section components
4. **Nested containers** — deep nesting → break into parent/child components
5. **Elements with many classes** — complex styled elements → extract to component with variant props

#### Component Template

```tsx
import { forwardRef, type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface ComponentNameProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined';
  size?: 'sm' | 'md' | 'lg';
}

export const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ className, variant = 'default', size = 'md', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          // base styles
          'rounded-lg transition-colors',
          // variant styles
          variant === 'default' && 'bg-card border border-border',
          variant === 'outlined' && 'border-2 border-primary',
          // size styles
          size === 'sm' && 'p-3 text-sm',
          size === 'md' && 'p-4 text-base',
          size === 'lg' && 'p-6 text-lg',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

ComponentName.displayName = 'ComponentName';
```

### Phase 5: Assemble the Page

Compose section components into a full page that mirrors the original layout:

```tsx
// pages/ConvertedPage.tsx
import { Header } from '@/components/sections/Header';
import { Hero } from '@/components/sections/Hero';
import { Features } from '@/components/sections/Features';
import { Footer } from '@/components/sections/Footer';

export default function ConvertedPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <main>
        <Hero />
        <Features />
      </main>
      <Footer />
    </div>
  );
}
```

### Phase 6: Validate

After conversion, run these checks:

```bash
# TypeScript — no type errors
npx tsc --noEmit

# Lint — no lint violations
npx eslint src/components/

# Build — compiles cleanly
npm run build
```

#### Visual Validation Checklist

- [ ] Layout matches source at all breakpoints (mobile, tablet, desktop)
- [ ] Colors match source (use browser DevTools color picker to verify)
- [ ] Typography matches (font family, size, weight, line-height)
- [ ] Spacing matches (padding, margin, gap)
- [ ] Interactive states work (hover, focus, active, disabled)
- [ ] Animations/transitions replicate source behavior
- [ ] Images and icons render correctly
- [ ] Forms submit and validate correctly
- [ ] Responsive behavior matches source media queries
- [ ] Dark mode works if source had dark mode

## Conversion Pitfalls

| Problem | Solution |
|---------|----------|
| Raw hex colors in className | Use semantic tokens (`bg-primary`, `text-foreground`) or extract to `@theme` |
| Inline styles left in JSX | Convert every inline style to Tailwind utilities |
| Giant monolithic component | Decompose — no component should exceed ~150 lines of JSX |
| Hardcoded text content | Pass as props or children |
| Missing TypeScript types | Every prop needs a type — extend HTML element attributes |
| `class` attribute in JSX | Must be `className` |
| `for` attribute on `<label>` | Must be `htmlFor` |
| `onclick="..."` inline handlers | Must be `onClick={...}` React handlers |
| `style="..."` inline CSS | Convert to Tailwind classes |
| Self-closing tags (`<img>`, `<br>`, `<input>`) | Must be `<img />`, `<br />`, `<input />` |
| `tabindex` | Must be `tabIndex` |
| `class` → `className` but also `stroke-width` → `strokeWidth` | All SVG/HTML attributes must use camelCase in JSX |
| CSS `!important` | Use Tailwind `!` prefix: `!text-foreground` (but avoid — fix specificity instead) |
| CSS `:nth-child()` selectors | Use `[&:nth-child(n)]:` arbitrary variant |
| CSS `@keyframes` | Define in globals.css, reference with `animate-[name]` or `@theme` `--animate-*` |
| `<a href="#">` | Use proper routing (`<Link>`) or `<button>` for actions |

## cn() Utility

Always include this in the project if not already present:

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Required packages: `clsx`, `tailwind-merge`

## Output Structure

```
src/
├── components/
│   ├── ui/              # Extracted primitive components
│   ├── sections/        # Page section components
│   └── layouts/         # Layout components
├── hooks/               # Custom hooks (from JS behavior conversion)
├── lib/
│   └── utils.ts         # cn() utility
└── pages/
    └── [PageName].tsx   # Assembled page
```

## Rules

- **Read the source completely before writing any code** — understand every element, style, and behavior
- **Convert ALL CSS to Tailwind utilities** — no leftover CSS classes or inline styles in the output
- **Use semantic color tokens** — never raw palette colors (`bg-blue-500`) in components; extract to `@theme`
- **Mobile-first responsive design** — base styles for mobile, `md:` and `lg:` for larger screens
- **TypeScript for everything** — every component gets typed props extending HTML element attributes
- **`cn()` for conditional classes** — never string-concatenate classNames
- **`forwardRef` on all components** — enables ref forwarding for composition
- **Preserve ALL original behavior** — every hover effect, animation, toggle, form validation must work identically
- **Preserve semantic HTML** — keep `<nav>`, `<main>`, `<section>`, `<article>`, `<header>`, `<footer>`
- **Preserve accessibility** — keep ARIA attributes, add missing ones (alt text, roles, labels)
- **No component exceeds 150 lines of JSX** — decompose if larger
- **Use `focus-visible:` not `focus:`** — for keyboard-only focus indicators
- **Use `disabled:opacity-50 disabled:pointer-events-none`** — on all interactive elements
- **Snap spacing to the 4px scale** — prefer `p-4` over `p-[17px]`
- **Clean up dead code** — remove any JS that was only needed for DOM manipulation (querySelector, getElementById, classList, etc.)
