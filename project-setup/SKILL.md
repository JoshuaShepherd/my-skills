---
name: project-setup
description: "Bootstrap a production-ready React + Tailwind + Supabase + Sentry app — either Next.js 15 (App Router) or Vite + React Router. Installs all core libraries, writes every config file, sets up shadcn/ui, Supabase auth clients, Sentry three-config, Zod env validation, React Query, dark mode, and the full token system. Asks Vite vs Next.js upfront. Use when starting any new project in this stack."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Bootstrap a new project: $ARGUMENTS

$ARGUMENTS can include:
- Project name (e.g. "my-app")
- Framework hint: "nextjs" or "vite" (if omitted, the skill asks)
- "with-stripe" to include Stripe setup
- "with-gsap" to include GSAP animation library
- "with-ai" to include Vercel AI SDK + OpenAI dependencies
- "minimal" to skip optional libraries and get the leanest possible setup
- Empty — asks all questions interactively

---

## Purpose

This skill configures the complete production stack used across all projects in this workspace. It handles both frameworks with identical auth, styling, and monitoring patterns. The end result is a running `pnpm dev` with:

- React 19 + TypeScript 5 (strict)
- Tailwind CSS v3 + shadcn/ui (new-york style, CSS variable theming)
- Supabase auth + database (browser and server clients)
- Sentry error monitoring (production-only, redacts secrets)
- React Query (`@tanstack/react-query`) for data fetching
- React Hook Form + Zod validation
- Lucide React icons
- next-themes dark mode
- Zod-validated environment variables
- Semantic token system (light + dark mode)
- `pnpm` only (never npm or yarn)

---

## Phase 0 — Gather Requirements

Ask the user all of the following before writing any files:

### Q1: Framework
> "**Vite or Next.js?**
> - **Vite** — SPA, client-side routing (React Router), ideal for dashboards, tools, or apps without SSR/SEO needs
> - **Next.js 15** — App Router, SSR/RSC, file-based routing, ideal for content sites, marketing pages, and full-stack apps
>
> Type `vite` or `nextjs`:"

### Q2: Project name
> "Project name? (used for package.json `name`, folder, and Sentry project slug)"

### Q3: App URL
> "Production URL? (e.g. `https://myapp.com`) — used in metadata and Supabase redirect config. Leave blank to set later."

### Q4: Supabase project
> "Supabase project URL? (e.g. `https://xyzabcdef.supabase.co`) — paste your Project URL from the Supabase dashboard. Leave blank to configure later."
> Also ask: "Supabase Anon key? (from Supabase → Project Settings → API)"

### Q5: Sentry (optional)
> "Include Sentry error monitoring? (y/n) — If yes, paste your Sentry DSN (from sentry.io → Project → Client Keys)."

### Q6: Optional libraries
> "Which optional libraries do you need? (space-separated, or press enter to skip)
> - `stripe` — payment + subscriptions
> - `gsap` — scroll animations, micro-interactions
> - `ai` — Vercel AI SDK + `@ai-sdk/openai` for streaming LLM responses
> - `resend` — transactional email
> - `motion` — Framer Motion (lightweight alternative to GSAP for component animations)"

### Q7: Font pair
> "Font pair? (or press enter for the default)
> - **Default:** Newsreader (serif headings) + Manrope (sans body) — editorial, warm, scholarly
> - `inter` — Inter + Inter (clean, modern, SaaS-friendly)
> - `geist` — Geist Sans + Geist Mono (Vercel's system font)
> - `custom` — I'll configure my own after setup"

Confirm all answers with the user before proceeding.

---

## Phase 1 — Scaffold the Project

### If Vite:

Check if the project directory exists. If not, create it:

```bash
pnpm create vite@latest <project-name> -- --template react-ts
cd <project-name>
```

Remove the Vite template boilerplate:
- Delete `src/App.css`, `src/index.css` (will be replaced by globals.css)
- Clear `src/App.tsx` content
- Clear `src/main.tsx` content (will be rewritten)

### If Next.js:

Check if the project directory exists. If not, create it:

```bash
pnpm create next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-git
cd <project-name>
```

Remove Next.js template boilerplate:
- Clear `src/app/page.tsx` (replace with minimal placeholder)
- Clear `src/app/globals.css` (will be rewritten with full token system)
- Remove `public/vercel.svg`, `public/next.svg`

---

## Phase 2 — Install Core Dependencies

Run in the project root. Split into logical groups so failures are easy to diagnose.

### Always install

```bash
# UI + styling
pnpm add tailwindcss-animate class-variance-authority clsx tailwind-merge lucide-react next-themes

# Forms + validation
pnpm add react-hook-form @hookform/resolvers zod

# Data fetching
pnpm add @tanstack/react-query

# Supabase (always both packages — SSR version covers all cases)
pnpm add @supabase/supabase-js @supabase/ssr

# Dev tools
pnpm add -D tsx dotenv
```

### Next.js only

```bash
# Sentry for Next.js (wraps webpack, instruments RSC + edge)
pnpm add @sentry/nextjs
```

### Vite only

```bash
# React Router for client-side routing
pnpm add react-router-dom

# Sentry for React (browser only in Vite)
pnpm add @sentry/react
```

### If `stripe` requested

```bash
pnpm add stripe @stripe/stripe-js
```

### If `gsap` requested

```bash
pnpm add gsap @gsap/react
```

### If `ai` requested

```bash
pnpm add ai @ai-sdk/openai @ai-sdk/react
```

### If `resend` requested

```bash
pnpm add resend
```

### If `motion` requested

```bash
pnpm add motion
```

After installation, initialize shadcn/ui:

```bash
pnpm dlx shadcn@latest init
```

When prompted by the shadcn CLI:
- Style: **New York**
- Base color: **Neutral**
- CSS variables: **Yes**
- Tailwind config: `tailwind.config.ts`
- Global CSS: `src/app/globals.css` (Next.js) or `src/index.css` → rename to `src/globals.css` (Vite)
- Components alias: `@/components`
- Utils alias: `@/lib/utils`

Install the core shadcn components immediately after init:

```bash
pnpm dlx shadcn@latest add button card input label badge tabs select textarea dialog sheet dropdown-menu avatar separator progress scroll-area accordion
```

---

## Phase 3 — TypeScript Config

### tsconfig.json (Next.js — overwrite what create-next-app generated)

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### tsconfig.json (Vite — overwrite what create-vite generated)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

---

## Phase 4 — Tailwind Config

Write `tailwind.config.ts` (same for both frameworks, adjust `content` paths):

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    // Next.js:
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    // Vite (replace the above with):
    // "./index.html",
    // "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-body)", "ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
        heading: ["var(--font-heading)", "system-ui", "sans-serif"],
        display: ["var(--font-heading)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        serif: ["var(--font-heading)", "var(--font-serif)", "ui-serif", "Georgia", "serif"],
        body: ["var(--font-body)", "ui-sans-serif", "system-ui", "sans-serif"],
        label: ["var(--font-body)", "system-ui", "sans-serif"],
      },
      fontSize: {
        display: ["56px", { lineHeight: "1.05", letterSpacing: "-0.02em", fontWeight: "800" }],
        h1: ["48px", { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "800" }],
        h2: ["40px", { lineHeight: "1.15", letterSpacing: "-0.01em", fontWeight: "700" }],
        h3: ["28px", { lineHeight: "1.2", fontWeight: "600" }],
        h4: ["20px", { lineHeight: "1.25", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "1.7", fontWeight: "400" }],
        body: ["16px", { lineHeight: "1.7", fontWeight: "400" }],
        small: ["14px", { lineHeight: "1.6", fontWeight: "400" }],
        label: ["12px", { lineHeight: "1.4", letterSpacing: "0.04em", fontWeight: "500" }],
        button: ["14px", { lineHeight: "1.2", fontWeight: "600" }],
        micro: ["10px", { lineHeight: "1.4", letterSpacing: "0.05em", fontWeight: "700" }],
      },
      borderRadius: {
        "card-lg": "2.5rem",
        button: "var(--radius-button)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      maxWidth: {
        content: "var(--container-content)",
        measure: "var(--measure)",
        "measure-wide": "var(--measure-wide)",
      },
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
        popover: { DEFAULT: "hsl(var(--popover))", foreground: "hsl(var(--popover-foreground))" },
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        secondary: { DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" },
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },
        destructive: { DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" },
        success: { DEFAULT: "hsl(var(--success))", foreground: "hsl(var(--success-foreground))" },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        nav: { DEFAULT: "hsl(var(--nav-bg))", foreground: "hsl(var(--nav-fg))" },
        surface: "hsl(var(--surface))",
        "surface-bright": "hsl(var(--surface-bright))",
        "surface-container-lowest": "hsl(var(--surface-container-lowest))",
        "surface-container-low": "hsl(var(--surface-container-low))",
        "surface-container": "hsl(var(--surface-container))",
        "surface-container-high": "hsl(var(--surface-container-high))",
        "surface-container-highest": "hsl(var(--surface-container-highest))",
        "primary-container": "hsl(var(--primary-container))",
        "on-primary-container": "hsl(var(--on-primary-container))",
        "outline-variant": "hsl(var(--outline-variant))",
        "surface-light": "hsl(var(--bg-light))",
        "surface-warm": "hsl(var(--bg-warm))",
        "surface-elevated": "hsl(var(--bg-elevated))",
        "border-light": "hsl(var(--border-light))",
        "text-dark": "hsl(var(--text-dark))",
        "text-muted-dark": "hsl(var(--text-muted-dark))",
        chart: {
          "1": "hsl(var(--chart-1))",
          "2": "hsl(var(--chart-2))",
          "3": "hsl(var(--chart-3))",
          "4": "hsl(var(--chart-4))",
          "5": "hsl(var(--chart-5))",
        },
      },
      keyframes: {
        "accordion-down": { from: { height: "0" }, to: { height: "var(--radix-accordion-content-height)" } },
        "accordion-up": { from: { height: "var(--radix-accordion-content-height)" }, to: { height: "0" } },
        "fade-up": { from: { opacity: "0", transform: "translateY(16px)" }, to: { opacity: "1", transform: "translateY(0)" } },
        "fade-in": { from: { opacity: "0" }, to: { opacity: "1" } },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-up": "fade-up 0.5s ease-out forwards",
        "fade-in": "fade-in 0.4s ease-out forwards",
      },
      transitionDuration: {
        fast: "var(--duration-fast)",
        normal: "var(--duration-normal)",
        slow: "var(--duration-slow)",
      },
      transitionTimingFunction: {
        out: "var(--ease-out)",
        expressive: "var(--ease-expressive)",
      },
      boxShadow: {
        "nav-scroll": "0 4px 6px -1px hsl(var(--foreground) / 0.08), 0 2px 4px -2px hsl(var(--foreground) / 0.05)",
        "primary-glow": "var(--shadow-primary-glow)",
        "primary-glow-sm": "var(--shadow-primary-glow-sm)",
        "primary-glow-md": "var(--shadow-primary-glow-md)",
        "primary-glow-lg": "var(--shadow-primary-glow-lg)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

> **Font variants:** If the user chose `inter`, replace the CSS variable references with `Inter, ui-sans-serif`. If `geist`, use `Geist, ui-sans-serif`. The variable wiring stays the same — only the font names change in globals.css.

---

## Phase 5 — Globals CSS (Token System)

Write `src/app/globals.css` (Next.js) or `src/globals.css` (Vite) with the full token system.

**This is the core visual identity file.** The tokens below are neutral defaults. The user should customize `--primary`, `--background`, and font variables for their brand.

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* === Neutral Default Palette === */
    /* Swap these HSL values for your brand colors */
    --background: 0 0% 98%;
    --foreground: 224 71% 4%;
    --card: 0 0% 100%;
    --card-foreground: 224 71% 4%;
    --popover: 0 0% 100%;
    --popover-foreground: 224 71% 4%;
    --primary: 220 90% 56%;         /* Brand blue — REPLACE WITH YOUR COLOR */
    --primary-foreground: 0 0% 100%;
    --secondary: 220 14% 96%;
    --secondary-foreground: 220 9% 46%;
    --muted: 220 14% 96%;
    --muted-foreground: 220 9% 46%;
    --accent: 220 14% 96%;
    --accent-foreground: 220 9% 46%;
    --destructive: 0 74% 42%;
    --destructive-foreground: 0 0% 98%;
    --success: 142 71% 28%;
    --success-foreground: 0 0% 98%;
    --border: 220 13% 91%;
    --input: 220 13% 91%;
    --ring: 220 90% 56%;
    --radius: 0.5rem;
    --radius-button: 9999px;

    /* === Typography === */
    /* Set font families here; Tailwind config reads via var() */
    --font-heading: system-ui, sans-serif;   /* Override with your heading font */
    --font-body: system-ui, sans-serif;      /* Override with your body font */
    --font-serif: Georgia, serif;
    --font-mono: ui-monospace, monospace;
    --line-height-heading: 1.1;
    --line-height-body: 1.65;

    /* === Motion === */
    --duration-fast: 150ms;
    --duration-normal: 300ms;
    --duration-slow: 450ms;
    --ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
    --ease-expressive: cubic-bezier(0.16, 1, 0.3, 1);

    /* === Layout === */
    --container-content: 90rem;
    --measure: min(65ch, 50rem);
    --measure-wide: min(90rem, 95vw);

    /* === Surface hierarchy (Material 3 inspired) === */
    --surface: var(--background);
    --surface-bright: 0 0% 100%;
    --surface-container-lowest: 0 0% 100%;
    --surface-container-low: 220 14% 97%;
    --surface-container: 220 14% 95%;
    --surface-container-high: 220 14% 93%;
    --surface-container-highest: 220 14% 90%;
    --primary-container: 220 90% 96%;
    --on-primary-container: 220 90% 30%;
    --outline-variant: 220 13% 85%;
    --bg-elevated: 220 14% 95%;
    --bg-light: 0 0% 98%;
    --bg-warm: 30 20% 97%;
    --border-light: 220 13% 88%;
    --text-dark: 224 71% 4%;
    --text-muted-dark: 220 9% 40%;

    /* === Nav === */
    --nav-bg: var(--surface-bright);
    --nav-fg: var(--foreground);

    /* === Charts === */
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;

    /* === Shadows === */
    --shadow-primary-glow: 0 4px 14px hsl(var(--primary) / 0.12);
    --shadow-primary-glow-sm: 0 2px 8px hsl(var(--primary) / 0.08);
    --shadow-primary-glow-md: 0 8px 32px hsl(var(--primary) / 0.06);
    --shadow-primary-glow-lg: 0 16px 48px hsl(var(--primary) / 0.06);
  }

  .dark {
    --background: 224 71% 4%;
    --foreground: 213 31% 91%;
    --card: 224 71% 6%;
    --card-foreground: 213 31% 91%;
    --popover: 224 71% 6%;
    --popover-foreground: 213 31% 91%;
    --primary: 210 100% 66%;
    --primary-foreground: 224 71% 4%;
    --secondary: 222 47% 11%;
    --secondary-foreground: 215 20% 65%;
    --muted: 223 47% 11%;
    --muted-foreground: 215 20% 65%;
    --accent: 216 34% 17%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 63% 31%;
    --destructive-foreground: 210 40% 98%;
    --success: 142 60% 42%;
    --success-foreground: 0 0% 98%;
    --border: 216 34% 17%;
    --input: 216 34% 17%;
    --ring: 210 100% 66%;
    --surface: 224 71% 4%;
    --surface-bright: 224 71% 6%;
    --surface-container-lowest: 224 71% 3%;
    --surface-container-low: 224 71% 5%;
    --surface-container: 224 71% 7%;
    --surface-container-high: 224 71% 9%;
    --surface-container-highest: 224 71% 12%;
    --primary-container: 220 60% 12%;
    --on-primary-container: 210 80% 70%;
    --outline-variant: 217 33% 20%;
    --bg-elevated: 224 71% 7%;
    --bg-light: 224 71% 4%;
    --bg-warm: 220 30% 6%;
    --border-light: 217 33% 20%;
    --text-dark: 213 31% 91%;
    --text-muted-dark: 215 20% 65%;
    --nav-bg: var(--surface-bright);
    --nav-fg: var(--foreground);
    --chart-1: 210 100% 66%;
    --chart-2: 160 60% 55%;
    --chart-3: 30 80% 65%;
    --chart-4: 280 65% 70%;
    --chart-5: 340 75% 65%;
  }
}

/* Global resets */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  font-family: var(--font-body, system-ui, sans-serif);
  line-height: var(--line-height-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading, system-ui, sans-serif);
  line-height: var(--line-height-heading);
}
```

> **If user chose a named font pair:**
> - `inter` → add `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap')` and set `--font-heading: 'Inter', ...` and `--font-body: 'Inter', ...`
> - `geist` → install `geist` package (`pnpm add geist`) and set vars accordingly
> - For Next.js font pairs, use `next/font/google` in layout.tsx instead of CSS imports (preferred)

---

## Phase 6 — Environment Variable Validation

Write `src/lib/env.ts`:

```typescript
/**
 * Zod-validated environment variables.
 * Import `env` instead of accessing `process.env` directly.
 */
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),

  // Supabase (required for auth + database)
  NEXT_PUBLIC_SUPABASE_URL: z.string().url().optional(),      // Next.js: NEXT_PUBLIC_ prefix
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().optional(),       // Vite: use VITE_ prefix instead
  // VITE_SUPABASE_URL: z.string().url().optional(),           // Vite variant
  // VITE_SUPABASE_ANON_KEY: z.string().optional(),           // Vite variant

  // Sentry (optional — app runs without it)
  NEXT_PUBLIC_SENTRY_DSN: z.string().url().optional(),
  SENTRY_DSN: z.string().url().optional(),
  SENTRY_AUTH_TOKEN: z.string().optional(),
  SENTRY_ORG: z.string().optional(),
  SENTRY_PROJECT: z.string().optional(),

  // Stripe (optional)
  STRIPE_SECRET_KEY: z.string().optional(),
  STRIPE_WEBHOOK_SECRET: z.string().optional(),
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().optional(),

  // AI (optional)
  OPENAI_API_KEY: z.string().optional(),
  OPENAI_MODEL: z.string().optional(),

  // Email (optional)
  RESEND_API_KEY: z.string().optional(),
  RESEND_FROM_DOMAIN: z.string().optional(),

  // Multi-tenant org scoping (optional — used when one deployment = one org)
  TENANT_ORG_ID: z.string().uuid().optional(),
});

export type Env = z.infer<typeof envSchema>;

const parsed = envSchema.safeParse(
  typeof process !== "undefined" ? process.env : import.meta.env  // works for both Next.js and Vite
);

if (!parsed.success) {
  console.error("Environment validation failed:", parsed.error.flatten());
  throw new Error("Invalid environment variables — check your .env.local");
}

export const env = parsed.data;
```

Write `.env.local.example` (never `.env` — secrets stay out of git):

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# For Vite projects, use VITE_ prefix instead:
# VITE_SUPABASE_URL=https://your-project.supabase.co
# VITE_SUPABASE_ANON_KEY=your-anon-key

# Database (for Drizzle ORM — not needed if using Supabase JS client only)
# DATABASE_URL=postgresql://postgres:[password]@db.your-project.supabase.co:5432/postgres

# Sentry (optional — errors only sent in production)
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_AUTH_TOKEN=your-auth-token
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project

# Stripe (optional)
STRIPE_SECRET_KEY=sk_live_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# AI (optional)
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o

# Email (optional)
RESEND_API_KEY=re_xxx
RESEND_FROM_DOMAIN=hello@yourapp.com

# Multi-tenant scoping (optional)
TENANT_ORG_ID=your-org-uuid
```

Add `.env.local` to `.gitignore` (if not already present).

---

## Phase 7 — Supabase Clients

### Next.js: Browser client

**`src/lib/supabase/client.ts`**:

```typescript
import { createBrowserClient } from "@supabase/ssr";

export function createSupabaseBrowserClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

### Next.js: Server client

**`src/lib/supabase/server.ts`**:

```typescript
import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createSupabaseServerClient() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet: Array<{ name: string; value: string; options: CookieOptions }>) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
          } catch {
            // Called from Server Component — safe to ignore; middleware refreshes the session.
          }
        },
      },
    },
  );
}
```

### Next.js: Middleware

**`src/middleware.ts`**:

```typescript
import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

function isRefreshTokenError(error: unknown): boolean {
  return (
    typeof error === "object" && error !== null &&
    "__isAuthError" in error &&
    (error as { code?: string }).code === "refresh_token_not_found"
  );
}

function clearAuthCookies(request: NextRequest, response: NextResponse) {
  request.cookies.getAll().forEach(({ name }) => {
    if (name.startsWith("sb-") && name.includes("-auth-token")) {
      response.cookies.set(name, "", { maxAge: 0, path: "/" });
    }
  });
}

export async function middleware(request: NextRequest) {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    return NextResponse.next({ request });
  }

  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(supabaseUrl, supabaseAnonKey, {
    cookies: {
      getAll() { return request.cookies.getAll(); },
      setAll(cookiesToSet: Array<{ name: string; value: string; options: CookieOptions }>) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
        supabaseResponse = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) =>
          supabaseResponse.cookies.set(name, value, options),
        );
      },
    },
  });

  let user: { id: string } | null = null;
  try {
    const { data } = await supabase.auth.getUser();
    user = data.user;
  } catch (error) {
    if (isRefreshTokenError(error)) {
      clearAuthCookies(request, supabaseResponse);
    } else {
      console.error("[middleware] Supabase auth error:", error);
    }
  }

  // ---- Protected routes ----
  // Edit this list to match your app's protected paths
  const path = request.nextUrl.pathname;
  const isProtected =
    path === "/dashboard" ||
    path.startsWith("/dashboard/") ||
    path === "/account" ||
    path.startsWith("/account/");

  if (isProtected && !user) {
    const redirectUrl = request.nextUrl.clone();
    redirectUrl.pathname = "/auth/signin";
    redirectUrl.searchParams.set("redirect", path);
    return NextResponse.redirect(redirectUrl);
  }

  return supabaseResponse;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};
```

### Vite: Supabase client (browser only)

**`src/lib/supabase/client.ts`**:

```typescript
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error("Missing VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY");
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

> **Vite note:** Use `@supabase/supabase-js` directly (not `@supabase/ssr`) since there's no server. The `@supabase/ssr` package is still installed (included in the install step) but only the browser client is used. You can add server functions via Supabase Edge Functions.

---

## Phase 8 — Sentry Setup

Skip this phase if the user declined Sentry.

### Next.js: Three config files

**`sentry.client.config.ts`**:

```typescript
import * as Sentry from "@sentry/nextjs";

const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN;
const isProduction = process.env.NODE_ENV === "production";

if (dsn && isProduction) {
  Sentry.init({
    dsn,
    enabled: true,
    enableLogs: true,
    tracesSampleRate: 0.1,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    integrations: [
      Sentry.replayIntegration({ maskAllText: true, maskAllInputs: true, blockAllMedia: true }),
      Sentry.consoleLoggingIntegration({ levels: ["warn", "error"] }),
    ],
    beforeSend(event) {
      const req = event.request as { headers?: Record<string, string> } | undefined;
      if (req?.headers) {
        for (const k of ["authorization", "cookie", "x-api-key"]) {
          const match = Object.keys(req.headers).find((h) => h.toLowerCase() === k);
          if (match) req.headers[match] = "[Redacted]";
        }
      }
      return event;
    },
    ignoreErrors: [/^chrome-extension:\/\//i, /^moz-extension:\/\//i, "Network Error", "AbortError"],
  });
}
```

**`sentry.server.config.ts`**:

```typescript
import * as Sentry from "@sentry/nextjs";

const dsn = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;

if (dsn) {
  Sentry.init({
    dsn,
    tracesSampleRate: 0.1,
    enableLogs: true,
    sendDefaultPii: false,
  });
}
```

**`sentry.edge.config.ts`**:

```typescript
import * as Sentry from "@sentry/nextjs";

const dsn = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;

if (dsn) {
  Sentry.init({ dsn, tracesSampleRate: 0.1, enableLogs: true });
}
```

### Next.js: next.config.ts with Sentry wrapper

**`next.config.ts`**:

```typescript
import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = {
  trailingSlash: false,
  compress: true,
  productionBrowserSourceMaps: false,
  serverExternalPackages: ["postgres", "drizzle-orm", "@supabase/ssr", "sharp"],
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "*.supabase.co", pathname: "/storage/**" },
    ],
  },
};

export default withSentryConfig(nextConfig, {
  org: process.env.SENTRY_ORG ?? "<your-sentry-org>",
  project: process.env.SENTRY_PROJECT ?? "<your-sentry-project>",
  silent: !process.env.CI,
  widenClientFileUpload: true,
  webpack: { treeshake: { removeDebugLogging: true } },
});
```

### Next.js without Sentry: plain next.config.ts

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false,
  compress: true,
  productionBrowserSourceMaps: false,
  serverExternalPackages: ["postgres", "drizzle-orm", "@supabase/ssr", "sharp"],
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "*.supabase.co", pathname: "/storage/**" },
    ],
  },
};

export default nextConfig;
```

### Vite: Sentry setup

**`src/lib/sentry.ts`**:

```typescript
import * as Sentry from "@sentry/react";

export function initSentry() {
  const dsn = import.meta.env.VITE_SENTRY_DSN as string | undefined;
  const isProduction = import.meta.env.PROD;

  if (dsn && isProduction) {
    Sentry.init({
      dsn,
      tracesSampleRate: 0.1,
      replaysSessionSampleRate: 0.1,
      replaysOnErrorSampleRate: 1.0,
      integrations: [
        Sentry.replayIntegration({ maskAllText: true, maskAllInputs: true }),
      ],
      ignoreErrors: ["Network Error", "AbortError"],
    });
  }
}
```

Call `initSentry()` at the top of `src/main.tsx` before rendering the app.

---

## Phase 9 — Providers & Layout

### Next.js: Providers

**`src/app/providers.tsx`**:

```typescript
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () => new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 60 * 1000,
          refetchOnWindowFocus: false,
        },
      },
    }),
  );

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </ThemeProvider>
  );
}
```

### Next.js: Root layout

**`src/app/layout.tsx`** — font loading depends on the user's chosen font pair.

For the **default (Newsreader + Manrope)** pair:

```typescript
import type { Metadata } from "next";
import { Newsreader, Manrope, JetBrains_Mono } from "next/font/google";
import { Providers } from "./providers";
import "./globals.css";

const newsreader = Newsreader({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
  variable: "--font-heading",
  display: "swap",
});

const manrope = Manrope({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-body",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Your App",
  description: "Your app description",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${newsreader.variable} ${manrope.variable} ${jetbrainsMono.variable}`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

For **`inter`**: Use `Inter` from `next/font/google` for both `--font-heading` and `--font-body`.
For **`geist`**: Install `geist` package; import `GeistSans` and `GeistMono`.
For **`custom`**: Use `var(--font-heading)` placeholders — the user fills in the font later.

### Next.js: Minimal placeholder page

**`src/app/page.tsx`**:

```typescript
export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-h1 font-heading">Your app is running</h1>
        <p className="text-muted-foreground">Edit <code>src/app/page.tsx</code> to get started.</p>
      </div>
    </main>
  );
}
```

### Vite: main.tsx entry

**`src/main.tsx`**:

```typescript
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";
import { initSentry } from "./lib/sentry";  // omit if no Sentry
import App from "./App";
import "./globals.css";

initSentry();  // omit if no Sentry

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 60 * 1000, refetchOnWindowFocus: false },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>,
);
```

### Vite: App.tsx

**`src/App.tsx`**:

```typescript
import { Routes, Route } from "react-router-dom";

function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-h1 font-heading">Your app is running</h1>
        <p className="text-muted-foreground">Edit <code>src/App.tsx</code> to get started.</p>
      </div>
    </main>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
    </Routes>
  );
}
```

### Vite: vite.config.ts

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
  },
});
```

---

## Phase 10 — Package.json Scripts

Add/merge these into `package.json` scripts (do not replace existing scripts):

### Next.js scripts

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx",
    "check:env": "tsx scripts/check-env.ts"
  }
}
```

### Vite scripts (already set by create-vite, but standardize)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx",
    "check:env": "tsx scripts/check-env.ts"
  }
}
```

Write **`scripts/check-env.ts`** — validates all env vars and reports missing ones:

```typescript
import { config } from "dotenv";
config({ path: ".env.local" });

const required: string[] = [
  // Add vars that are truly required for your app to function:
  // "NEXT_PUBLIC_SUPABASE_URL",
  // "NEXT_PUBLIC_SUPABASE_ANON_KEY",
];

const missing = required.filter((k) => !process.env[k]);
if (missing.length > 0) {
  console.error("Missing required env vars:", missing.join(", "));
  process.exit(1);
}
console.log("Environment OK");
```

---

## Phase 11 — Utility Helpers

### `src/lib/utils.ts` (shadcn standard — may already exist after init)

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### `src/lib/tenant.ts` (multi-tenant scope — always useful, opt-in at runtime)

```typescript
/**
 * Returns the tenant org ID from TENANT_ORG_ID env var.
 * Services use this to scope queries by organization_id.
 * Returns null when not set — app works without it for single-tenant deployments.
 */
export function getTenantOrgId(): string | null {
  const id = typeof process !== "undefined"
    ? process.env.TENANT_ORG_ID
    : (import.meta.env as Record<string, string>).VITE_TENANT_ORG_ID;
  return id ?? null;
}
```

---

## Phase 12 — Verify the Setup

Run in order and show all output to the user:

```bash
# 1. Type check
pnpm typecheck

# 2. Lint
pnpm lint

# 3. Start dev server (just confirm it starts, then ctrl+c)
pnpm dev
```

If `pnpm typecheck` or `pnpm lint` fails, fix the errors before declaring success.

Common issues:
- **Missing `@types/node`**: `pnpm add -D @types/node`
- **shadcn components not found**: re-run `pnpm dlx shadcn@latest add <component>`
- **`next/font` module not found in Vite**: Only use `next/font` in Next.js — Vite uses CSS `@import` or `fontsource` packages
- **`import.meta.env` types missing in Vite**: add `/// <reference types="vite/client" />` to `src/vite-env.d.ts`

---

## Phase 13 — Final Report

Output a structured summary:

```markdown
## Project Setup Complete

### Project
- **Name:** [name]
- **Framework:** [Next.js 15 App Router | Vite + React Router]
- **Location:** [path]

### Installed Libraries
| Category | Packages |
|----------|---------|
| UI | tailwindcss, shadcn/ui (new-york), lucide-react, tailwindcss-animate |
| Styling | class-variance-authority, clsx, tailwind-merge, next-themes |
| Forms | react-hook-form, @hookform/resolvers, zod |
| Data | @tanstack/react-query |
| Auth/DB | @supabase/supabase-js, @supabase/ssr |
| Monitoring | [Sentry package] |
| [Optional] | [any extras requested] |

### Files Written
- `tailwind.config.ts` — full token system
- `src/app/globals.css` — semantic CSS variables (light + dark)
- `src/lib/env.ts` — Zod-validated environment variables
- `src/lib/supabase/client.ts` — Supabase browser client
- [Next.js] `src/lib/supabase/server.ts` — Supabase server client
- [Next.js] `src/middleware.ts` — auth guard + session refresh
- [Next.js] `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- [Next.js] `next.config.ts` — [with/without] Sentry wrapper
- [Vite] `vite.config.ts`, `src/main.tsx`, `src/App.tsx`
- `src/app/providers.tsx` — QueryClient + ThemeProvider
- `src/app/layout.tsx` — root layout with fonts
- `src/lib/utils.ts` — cn() helper
- `src/lib/tenant.ts` — getTenantOrgId()
- `scripts/check-env.ts` — env validation script
- `.env.local.example` — env template
- `components.json` — shadcn config

### Next Steps
1. Copy `.env.local.example` to `.env.local` and fill in your values
2. Customize `--primary` color in `src/app/globals.css` for your brand
3. Update font variables if using custom fonts
4. Set protected routes in `src/middleware.ts`
5. Run `/type-safety-chain <supabase-project-id>` to implement the DB→hooks chain
6. Run `pnpm dev` to verify everything loads

### Commands
\`\`\`bash
pnpm dev          # Start dev server
pnpm typecheck    # TypeScript check
pnpm lint         # ESLint
pnpm check:env    # Validate env vars
\`\`\`
```

---

## Critical Rules

1. **pnpm only** — never npm or yarn
2. **Never hardcode secrets** — all credentials go in `.env.local` (not `.env`)
3. **Never use `get`/`set`/`remove` for Supabase cookies** — only `getAll`/`setAll` via `@supabase/ssr`
4. **Sentry only initializes in production** — check `NODE_ENV === "production"` in client config
5. **Push `"use client"` to leaf components** — layouts and pages stay as Server Components in Next.js
6. **Tailwind semantic classes only** — `bg-primary`, not `bg-blue-600`; `text-muted-foreground`, not `text-gray-500`
7. **shadcn components, not raw HTML** — use `Button`, `Card`, `Input` etc. from `@/components/ui`
8. **Verify before closing** — always run `pnpm typecheck` and `pnpm dev` at the end
