---
name: vite-audit
description: Audit Vite configuration for correctness and optimization — build performance, plugins, resolve config, dev server, environment variables, and production output. Use before deploying or after config changes.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Audit the Vite configuration for this React 19 + Express SPA project. Check for correctness, performance, and optimization opportunities.

Target: $ARGUMENTS (default: full audit)

## Pre-flight

1. Read `vite.config.ts`, `package.json`, `tsconfig.json`, and `index.html`.
2. Glob for `src/**/*.{ts,tsx}` barrel files (`index.ts` that re-export).
3. Check installed Vite version and plugin versions in `node_modules`.

## Audit Checklist

### 1. CORE CONFIG
- [ ] Uses `defineConfig` wrapper (enables IDE autocomplete and type safety)
- [ ] Config function receives `{ mode, command }` for conditional logic
- [ ] `loadEnv` used correctly if accessing env vars in config (not `process.env` directly for `.env` files)
- [ ] No hardcoded secrets in `define` — only public/build-time values
- [ ] `define` values use `JSON.stringify()` for string replacements
- [ ] `process.env.*` replacements don't leak server secrets to client bundle

### 2. PLUGINS
- [ ] `@vitejs/plugin-react` present for React JSX transform
- [ ] Plugin order is correct (React before Tailwind for proper HMR)
- [ ] `@tailwindcss/vite` used instead of PostCSS plugin (Tailwind v4 best practice)
- [ ] No duplicate plugins (e.g., both PostCSS autoprefixer AND Tailwind Vite plugin)
- [ ] No unnecessary plugins that slow dev startup
- [ ] Consider `vite-plugin-compression` for pre-compressed assets if not using Vercel (Vercel auto-compresses)

### 3. RESOLVE & ALIASES
- [ ] Path aliases match `tsconfig.json` `paths` configuration exactly
- [ ] Alias target uses `path.resolve` with `__dirname` or `import.meta.dirname` (not relative strings)
- [ ] `resolve.extensions` not unnecessarily expanded (defaults are fine: `.mjs`, `.js`, `.mts`, `.ts`, `.jsx`, `.tsx`, `.json`)
- [ ] No barrel file re-exports causing unnecessary module loading — prefer direct imports
- [ ] TypeScript `moduleResolution: "bundler"` set (optimal for Vite)

### 4. BUILD OPTIMIZATION
- [ ] `build.target` appropriate for audience (default `'baseline-widely-available'` is good for modern apps)
- [ ] `build.outDir` matches Vercel `outputDirectory` config
- [ ] `build.sourcemap` configured:
  - `'hidden'` for production with Sentry (uploads maps, doesn't expose to users)
  - `true` for development/staging
  - `false` only if no error tracking
- [ ] `build.minify` uses default `'oxc'` (30-90x faster than terser, near-identical compression)
- [ ] `build.cssMinify` not set to less optimal value than default
- [ ] `build.reportCompressedSize` set to `false` for faster builds on large projects
- [ ] `build.chunkSizeWarningLimit` at reasonable value (default 500 KB)
- [ ] Code splitting configured via `build.rollupOptions.output.manualChunks` if needed:
  - Vendor chunk for `react`, `react-dom`, `react-router-dom`
  - Separate chunk for heavy deps (`openai`, `@google/genai`, `motion`)
- [ ] `build.cssCodeSplit: true` (default) for async chunk CSS isolation

### 5. DEV SERVER
- [ ] `server.port` set explicitly for consistent dev URL
- [ ] `server.host` set to `'0.0.0.0'` or `true` if network access needed (mobile testing)
- [ ] `server.proxy` correctly forwards `/api` to Express backend
- [ ] Proxy uses `changeOrigin: true` for correct `Host` header
- [ ] `server.warmup` configured for frequently-used files (speeds up initial page load):
  ```ts
  server: {
    warmup: {
      clientFiles: ['./src/App.tsx', './src/main.tsx']
    }
  }
  ```
- [ ] HMR not unnecessarily disabled
- [ ] `server.fs.allow` not overly permissive

### 6. ENVIRONMENT VARIABLES
- [ ] Only `VITE_*` prefixed vars are exposed to client (by design)
- [ ] No server secrets passed via `define` to client bundle
- [ ] `loadEnv` called with correct directory (`.` or `process.cwd()`)
- [ ] `envPrefix` not changed from default `'VITE_'` without good reason
- [ ] `GEMINI_API_KEY` in `define` — verify this doesn't leak to client bundle
  - If used server-side only, remove from `define` and access via Express
  - If used client-side, prefix as `VITE_GEMINI_API_KEY`

### 7. CSS & STYLING
- [ ] Tailwind CSS v4 using `@tailwindcss/vite` plugin (not PostCSS)
- [ ] No redundant `autoprefixer` in PostCSS config (Tailwind v4 handles this)
- [ ] No `postcss.config.js` conflicting with Vite plugin setup
- [ ] CSS imports use native CSS when possible (avoid Sass/Less unless needed)
- [ ] No unused CSS preprocessor dependencies in `package.json`

### 8. TYPESCRIPT INTEGRATION
- [ ] `tsconfig.json` `target` matches or is compatible with Vite's `build.target`
- [ ] `moduleResolution: "bundler"` (optimal for Vite)
- [ ] `isolatedModules: true` (required for Vite's esbuild transform)
- [ ] `allowImportingTsExtensions: true` if using `.ts`/`.tsx` in imports
- [ ] `noEmit: true` (Vite handles emit, TS only type-checks)
- [ ] `jsx: "react-jsx"` for React 19 automatic JSX transform
- [ ] `lib` includes `"DOM"` and `"DOM.Iterable"` for browser APIs
- [ ] `skipLibCheck: true` for faster type checking (standard practice)

### 9. DEPENDENCY OPTIMIZATION
- [ ] Heavy dependencies considered for `optimizeDeps.include` to speed up dev cold start:
  - `react`, `react-dom`, `react-router-dom`
  - `openai`, `@google/genai` (large packages)
- [ ] Problematic CJS packages in `optimizeDeps.include` if causing issues
- [ ] `vite` not duplicated in both `dependencies` AND `devDependencies`
- [ ] `autoprefixer` in `devDependencies` is redundant with Tailwind v4 — can be removed

## Output Format

```
## Vite Audit Report

### Score: X/9 dimensions passing

### Critical Issues
1. [DIMENSION] — [severity: CRITICAL/HIGH/MEDIUM/LOW] — description
   Current: `current config`
   Fix: specific fix with code

### Warnings
1. [DIMENSION] — description
   Recommendation: what to change

### Optimizations
1. [DIMENSION] — description
   Benefit: expected improvement

### Passing
- [DIMENSION] — what's configured correctly

### Recommended vite.config.ts
(Only if changes needed — show the complete corrected file)
```
