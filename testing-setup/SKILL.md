---
name: testing-setup
description: "Bootstrap Vitest (unit + integration) and Playwright (e2e) test infrastructure for Next.js 15 or Vite + React — config files, test utilities, fixture factories, database test helpers, and CI integration. Use when adding tests to a new or existing project."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up testing infrastructure: $ARGUMENTS

$ARGUMENTS can include:
- "vitest" — unit/integration only (skip Playwright)
- "playwright" — e2e only (skip Vitest)
- "full" — both (default)
- "with-db" — include database test helpers (test transactions, seed/teardown)
- Framework hint: "nextjs" or "vite" (auto-detected if omitted)
- Empty — full setup, auto-detect framework

---

## Before Starting

1. Read `package.json` to detect framework and see existing test config
2. Read `tsconfig.json` to understand path aliases
3. Check if `vitest.config.ts` or `playwright.config.ts` already exists
4. Read `src/lib/database/schema.ts` to understand table structure (for fixtures)
5. Check `src/lib/env.ts` for env validation patterns

---

## Architecture

```
tests/
  unit/              ← Vitest: pure functions, services, schemas
    setup.ts         ← Global test setup (vi.mock, env, etc.)
    helpers/
      factories.ts   ← Type-safe fixture factories
      db.ts          ← DB test helpers (if with-db)
  integration/       ← Vitest: API routes, hooks (MSW or real DB)
  e2e/               ← Playwright: full browser flows
    fixtures/
      auth.ts        ← Authenticated page fixture
    pages/           ← Page object models

vitest.config.ts
playwright.config.ts
```

---

## Step 1 — Install Packages

### Vitest
```bash
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom msw
```

### Playwright
```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium
```

---

## Step 2 — Vitest Config

Create `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/unit/setup.ts"],
    include: ["tests/unit/**/*.test.ts", "tests/unit/**/*.test.tsx"],
    exclude: ["tests/e2e/**"],
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["src/**"],
      exclude: ["src/components/ui/**", "src/app/globals.css"],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

---

## Step 3 — Vitest Setup File

Create `tests/unit/setup.ts`:

```typescript
import "@testing-library/jest-dom";
import { vi } from "vitest";

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    refresh: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}));

// Mock Next.js headers (for server actions / server components)
vi.mock("next/headers", () => ({
  cookies: () => ({
    getAll: () => [],
    setAll: vi.fn(),
  }),
  headers: () => new Headers(),
}));

// Silence console.error for expected errors in tests
const originalError = console.error;
beforeEach(() => {
  console.error = (...args: unknown[]) => {
    if (typeof args[0] === "string" && args[0].includes("Warning:")) return;
    originalError(...args);
  };
});
afterEach(() => {
  console.error = originalError;
});
```

---

## Step 4 — Fixture Factories

Create `tests/unit/helpers/factories.ts`:

```typescript
import { faker } from "@faker-js/faker";

// Install: pnpm add -D @faker-js/faker

export function makeUser(overrides: Partial<{
  id: string;
  email: string;
  name: string;
}> = {}) {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    created_at: faker.date.past().toISOString(),
    ...overrides,
  };
}

// Add more factories per table as needed:
// makeOrganization(), makeCourse(), makeArticle(), etc.
```

---

## Step 5 — Database Test Helpers (with-db flag)

Create `tests/unit/helpers/db.ts`:

```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "@/lib/database/schema";

let db: ReturnType<typeof drizzle>;

export function getTestDb() {
  if (!db) {
    const client = postgres(process.env.DATABASE_URL!, { max: 1 });
    db = drizzle(client, { schema });
  }
  return db;
}

/**
 * Wrap a test in a rolled-back transaction.
 * Usage: await withTestTransaction(async (tx) => { ... });
 */
export async function withTestTransaction<T>(
  fn: (tx: ReturnType<typeof getTestDb>) => Promise<T>
): Promise<T> {
  const db = getTestDb();
  return await db.transaction(async (tx) => {
    const result = await fn(tx as ReturnType<typeof getTestDb>);
    tx.rollback(); // always roll back after test
    return result;
  });
}
```

Add to `.env.test`:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test_db
```

---

## Step 6 — Playwright Config

Create `playwright.config.ts`:

```typescript
import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost:3000";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? "github" : "list",

  use: {
    baseURL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },

  projects: [
    // Setup: create authenticated session
    { name: "setup", testMatch: /.*\.setup\.ts/ },

    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        storageState: "tests/e2e/.auth/user.json",
      },
      dependencies: ["setup"],
    },
  ],

  webServer: {
    command: "pnpm dev",
    url: baseURL,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

---

## Step 7 — Playwright Auth Fixture

Create `tests/e2e/auth.setup.ts`:

```typescript
import { test as setup } from "@playwright/test";
import path from "path";

const authFile = path.join(__dirname, ".auth/user.json");

setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel("Password").fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("/");

  // Save authenticated state
  await page.context().storageState({ path: authFile });
});
```

Add to `.env.local`:
```bash
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=testpassword123
```

---

## Step 8 — Page Object Model (example)

Create `tests/e2e/pages/LoginPage.ts`:

```typescript
import type { Page } from "@playwright/test";

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto("/login");
  }

  async signIn(email: string, password: string) {
    await this.page.getByLabel("Email").fill(email);
    await this.page.getByLabel("Password").fill(password);
    await this.page.getByRole("button", { name: "Sign in" }).click();
  }

  async waitForRedirect(path: string) {
    await this.page.waitForURL(path);
  }
}
```

---

## Step 9 — Package.json Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

---

## Step 10 — .gitignore Additions

Add to `.gitignore`:

```
# Test artifacts
tests/e2e/.auth/
test-results/
playwright-report/
coverage/
```

---

## Verify

1. `pnpm test:run` — Vitest runs with 0 failures
2. `pnpm dev` in one terminal, `pnpm test:e2e` in another — Playwright passes
3. `pnpm test:coverage` — Coverage report generated in `coverage/`

---

## Anti-Patterns

- NEVER test implementation details — test behavior from the user's perspective
- NEVER commit `.auth/` files — they contain session tokens
- NEVER use `page.waitForTimeout()` — use `waitForURL`, `waitForSelector`, or `expect().toBeVisible()`
- NEVER write e2e tests that depend on test ordering — each test must be independent
- NEVER mock the database in integration tests — use real DB with rolled-back transactions
