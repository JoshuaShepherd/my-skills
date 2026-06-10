---
name: sentry-setup
description: Set up Sentry error monitoring for a Vite + React 19 SPA with Express API — client SDK, server SDK, error boundaries, source maps, and Vercel serverless support.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Sentry error monitoring: $ARGUMENTS

$ARGUMENTS should include:
- A target: "client", "server", "full" (default: full — both client and server)
- Optionally: --dry-run to preview changes without writing
- Empty — run full setup and prompt for Sentry DSN / org / project

---

## Before Starting

1. Read `package.json` to confirm framework (Vite + React vs Next.js)
2. Read `src/main.tsx` to understand the React entry point and React version
3. Read `server/index.ts` and `server/vercel.ts` to understand Express setup
4. Read `vite.config.ts` to understand existing plugins and build config
5. Read `.env.example` to see existing env var patterns
6. Check if Sentry is already installed (`grep "@sentry" package.json`)
7. Read `_docs/type/TYPE_SAFETY.md` for type conventions

---

## Architecture

```
Client (Vite + React 19 SPA)
  src/instrument.ts          ← Sentry.init() — imported FIRST in main.tsx
  src/main.tsx               ← React 19 error handlers (onUncaughtError, onCaughtError, onRecoverableError)
  vite.config.ts             ← sentryVitePlugin for source map upload (prod builds only)

Server (Express 4 API)
  server/instrument.ts       ← Sentry.init() — imported FIRST in index.ts and vercel.ts
  server/index.ts            ← Sentry.setupExpressErrorHandler(app) AFTER all routes
  server/vercel.ts           ← Same error handler for Vercel serverless
```

---

## Step 1 — Install Packages

```bash
pnpm add @sentry/react @sentry/node
pnpm add -D @sentry/vite-plugin
```

- `@sentry/react` — Client SDK with React 19 error handlers, ErrorBoundary, browserTracingIntegration, replayIntegration
- `@sentry/node` — Server SDK with Express integration, request isolation
- `@sentry/vite-plugin` — Source map upload during `vite build` (dev-only, no runtime cost)

---

## Step 2 — Client Instrument File

Create `src/instrument.ts`:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enabled: !!import.meta.env.VITE_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],

  // Performance: capture 100% in dev, 20% in prod (adjust as needed)
  tracesSampleRate: import.meta.env.DEV ? 1.0 : 0.2,

  // Trace propagation to our own API
  tracePropagationTargets: [/^\/api/],

  // Session Replay: 10% of sessions, 100% of error sessions
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  environment: import.meta.env.MODE,
});
```

Key decisions:
- `enabled` gate — gracefully no-ops when DSN is missing (local dev without Sentry)
- `tracePropagationTargets` — only propagate to `/api` (our Express backend via Vite proxy)
- Sample rates tuned for a small team (adjust when traffic grows)

---

## Step 3 — Wire Client Entry Point

Edit `src/main.tsx`:

1. Import `./instrument` as the VERY FIRST import (before React, before anything)
2. Replace `createRoot(el).render(...)` with React 19 error handlers:

```typescript
import "./instrument";                          // ← FIRST
import * as Sentry from "@sentry/react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
// ... other imports

const root = createRoot(document.getElementById("root")!, {
  onUncaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
    console.warn("Uncaught error", error, errorInfo.componentStack);
  }),
  onCaughtError: Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
});

root.render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>
);
```

React 19 error handlers replace the old ErrorBoundary-only approach:
- `onUncaughtError` — errors that bubble past all boundaries
- `onCaughtError` — errors caught by an ErrorBoundary
- `onRecoverableError` — errors React recovers from automatically

---

## Step 4 — Server Instrument File

Create `server/instrument.ts`:

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enabled: !!process.env.SENTRY_DSN,

  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.2 : 1.0,

  environment: process.env.NODE_ENV || "development",
});
```

---

## Step 5 — Wire Server Entry Points

### server/index.ts

1. Import `./instrument` as the FIRST import (after dotenv, which must load env vars before Sentry reads them)
2. Add `Sentry.setupExpressErrorHandler(app)` AFTER all routes, BEFORE the SPA catch-all

```typescript
import dotenv from "dotenv";
// ... dotenv.config() calls ...
import "./instrument";                           // ← after dotenv, before everything else
import * as Sentry from "@sentry/node";
// ... other imports ...

// ... routes ...

// Sentry error handler — AFTER all routes, BEFORE SPA catch-all
Sentry.setupExpressErrorHandler(app);

// SPA catch-all (production only)
if (isProduction) { ... }
```

### server/vercel.ts

1. Import `./instrument` as the FIRST import
2. Add `Sentry.setupExpressErrorHandler(app)` after routes

```typescript
import "./instrument";                           // ← FIRST
import * as Sentry from "@sentry/node";
// ... other imports ...

// ... routes ...

Sentry.setupExpressErrorHandler(app);

export default function handler(req, res) {
  app(req, res);
}
```

---

## Step 6 — Vite Source Map Plugin

Edit `vite.config.ts`:

```typescript
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");
  return {
    build: {
      sourcemap: "hidden",                       // ← generate maps but don't expose in prod
    },
    plugins: [
      react(),
      tailwindcss(),
      // Sentry source maps — LAST plugin, only runs during production builds
      sentryVitePlugin({
        org: env.SENTRY_ORG,
        project: env.SENTRY_PROJECT,
        authToken: env.SENTRY_AUTH_TOKEN,
        sourcemaps: {
          filesToDeleteAfterUpload: ["./dist/**/*.map"],
        },
        disable: !env.SENTRY_AUTH_TOKEN,          // skip when no auth token (local builds)
      }),
    ],
    // ... rest of config
  };
});
```

Key decisions:
- `sourcemap: "hidden"` — generates maps for Sentry upload but doesn't serve them to users
- `disable` gate — local `vite build` works without Sentry credentials
- `filesToDeleteAfterUpload` — removes .map files from dist after upload (security)
- Plugin goes LAST so other plugins finish transforming first

---

## Step 7 — Environment Variables

Add to `.env.example`:

```bash
# --- Sentry (error monitoring) ---
# Client DSN (public, safe for browser): Sentry → Project → Settings → Client Keys (DSN)
VITE_SENTRY_DSN=
# Server DSN (same DSN or separate project): same location
SENTRY_DSN=

# Source map upload (CI/CD only, not needed locally):
# SENTRY_ORG=
# SENTRY_PROJECT=
# SENTRY_AUTH_TOKEN=
```

Naming:
- `VITE_` prefix for client vars (Vite exposes these to the browser)
- No prefix for server-only vars (Express reads from `process.env`)

---

## Step 8 — Verify

1. `pnpm lint` — TypeScript check passes
2. `pnpm build:check` — full stack type validation
3. `pnpm dev:all` — app starts without errors (Sentry gracefully disabled without DSN)
4. Add DSN to `.env.local`, trigger a test error, verify it appears in Sentry dashboard

---

## Anti-Patterns

- Do NOT wrap the entire app in `<Sentry.ErrorBoundary>` when using React 19 — use `reactErrorHandler()` on `createRoot` instead
- Do NOT import instrument.ts after other modules — it must be FIRST so Sentry can patch globals
- Do NOT put `SENTRY_AUTH_TOKEN` in `.env.local` — it belongs in CI/CD secrets only
- Do NOT set `tracesSampleRate: 1.0` in production for high-traffic apps
- Do NOT add `sendDefaultPii: true` without reviewing privacy/GDPR requirements
- Do NOT forget `Sentry.setupExpressErrorHandler(app)` — without it, Express errors are silently swallowed

---

## Optional Enhancements (not in base setup)

- **Sentry.ErrorBoundary** for granular UI sections (video editor, content editor) with custom fallback UIs
- **Sentry.feedbackIntegration()** for user-facing error reports
- **@sentry/profiling-node** for server-side CPU profiling
- **Sentry.setUser()** after auth — tie errors to specific users
- **Custom breadcrumbs** in apiFetch() for API request tracking
