---
name: auth-setup
description: "Set up Supabase Auth for Next.js 15 (App Router) or Vite + React — sign-up, sign-in, OAuth providers, session middleware, protected routes, RLS user scoping, and auth UI components. Handles both frameworks with SSR-safe cookie patterns. Use when bootstrapping auth on any new project."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Supabase Auth: $ARGUMENTS

$ARGUMENTS can include:
- Framework hint: "nextjs" or "vite" (if omitted, auto-detects from package.json)
- Providers: "email", "google", "github", "magic-link" (default: email + magic-link)
- "with-roles" to add role-based access control (user/admin/owner)
- "minimal" for email-only, no OAuth
- Empty — auto-detects framework and asks about providers

---

## Before Starting

1. Read `package.json` to detect framework (Next.js vs Vite)
2. Read `src/lib/env.ts` or `.env.example` to see existing env var patterns
3. Check if `@supabase/ssr` is already installed (`grep "@supabase" package.json`)
4. Read `src/middleware.ts` (Next.js) or `src/main.tsx` (Vite) for existing setup
5. Read `src/lib/supabase/` if it exists — do not overwrite working clients
6. Check `src/lib/database/schema.ts` for existing user/profile tables

---

## Architecture

### Next.js 15 (App Router)
```
src/lib/supabase/
  server.ts          ← createServerClient() — SSR-safe, uses cookies()
  browser.ts         ← createBrowserClient() — singleton for client components
  middleware.ts      ← refreshSession() helper called from middleware.ts

src/middleware.ts    ← Session refresh + route protection
src/app/(auth)/
  login/page.tsx     ← Sign-in form
  signup/page.tsx    ← Sign-up form
  callback/route.ts  ← OAuth + magic link exchange
  auth-error/page.tsx

src/hooks/custom/use-auth.ts     ← useUser(), useSession(), useSignOut()
src/components/auth/
  LoginForm.tsx
  SignupForm.tsx
  AuthProvider.tsx   ← Client-side session listener
```

### Vite + React
```
src/lib/supabase/
  client.ts          ← createClient() — browser singleton

src/hooks/use-auth.ts
src/components/auth/
  LoginForm.tsx
  SignupForm.tsx
  AuthGuard.tsx      ← Redirect wrapper for protected routes
```

---

## Step 1 — Install Packages

```bash
pnpm add @supabase/ssr @supabase/supabase-js
```

Note: Never install `@supabase/auth-helpers-nextjs` — it is deprecated. `@supabase/ssr` is the correct package.

---

## Step 2 — Environment Variables

Add to `.env.local` and `.env.example`:

```bash
# --- Supabase ---
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
# Server-only (service role — NEVER expose to browser):
# SUPABASE_SERVICE_ROLE_KEY=
```

Add to `src/lib/env.ts` (Zod schema):

```typescript
export const env = createEnv({
  client: {
    NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
    NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  },
  server: {
    SUPABASE_SERVICE_ROLE_KEY: z.string().min(1).optional(),
  },
  // ...
});
```

---

## Step 3 — Supabase Clients (Next.js)

### src/lib/supabase/server.ts
```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import type { Database } from "@/lib/database/types";

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Server Component — cookies set by middleware, not here
          }
        },
      },
    }
  );
}
```

### src/lib/supabase/browser.ts
```typescript
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "@/lib/database/types";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### src/lib/supabase/middleware.ts
```typescript
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session — do NOT remove this
  const { data: { user } } = await supabase.auth.getUser();

  return { supabaseResponse, user };
}
```

---

## Step 4 — Middleware (Next.js)

Edit `src/middleware.ts` — add session refresh and protected route logic:

```typescript
import { type NextRequest, NextResponse } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

// Routes that require authentication
const PROTECTED_ROUTES = [
  "/account",
  "/dashboard",
  "/content/courses",
];

export async function middleware(request: NextRequest) {
  const { supabaseResponse, user } = await updateSession(request);
  const pathname = request.nextUrl.pathname;

  const isProtected = PROTECTED_ROUTES.some((route) =>
    pathname.startsWith(route)
  );

  if (isProtected && !user) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirectTo", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

---

## Step 5 — Auth Callback Route (Next.js)

Create `src/app/(auth)/callback/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const redirectTo = searchParams.get("redirectTo") ?? "/";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(`${origin}${redirectTo}`);
    }
  }

  return NextResponse.redirect(`${origin}/auth-error`);
}
```

---

## Step 6 — Auth Hook

Create `src/hooks/custom/use-auth.ts`:

```typescript
"use client";
import { createClient } from "@/lib/supabase/browser";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { User } from "@supabase/supabase-js";

export function useAuth() {
  const supabase = createClient();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_, session) => {
        setUser(session?.user ?? null);
        router.refresh();
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };

  return { user, loading, signOut };
}
```

---

## Step 7 — Auth UI Components

### src/components/auth/LoginForm.tsx
```typescript
"use client";
import { createClient } from "@/lib/supabase/browser";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export function LoginForm() {
  const supabase = createClient();
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirectTo") ?? "/";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
    } else {
      router.push(redirectTo);
      router.refresh();
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSignIn} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? "Signing in..." : "Sign in"}
      </Button>
    </form>
  );
}
```

---

## Step 8 — OAuth Providers (optional)

For Google or GitHub OAuth, add to `LoginForm.tsx`:

```typescript
const handleOAuth = async (provider: "google" | "github") => {
  await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${window.location.origin}/callback?redirectTo=${redirectTo}`,
    },
  });
};
```

Enable providers in Supabase Dashboard → Authentication → Providers.

---

## Step 9 — RLS User Scoping

For tables that need user-level RLS (not org-level):

```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Users can only see their own row
CREATE POLICY "users_own_profile"
  ON profiles FOR ALL
  USING (auth.uid() = user_id);
```

For org-scoped tables (multi-tenant), use `organization_id` via `getTenantOrgId()` — see `src/lib/tenant.ts`.

---

## Step 10 — Role-Based Access (with-roles flag)

If "with-roles" was requested, add a `user_roles` table and helper:

```typescript
// src/lib/auth/get-user-role.ts
import { createClient } from "@/lib/supabase/server";

export async function getUserRole(): Promise<"user" | "admin" | "owner" | null> {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return null;

  const { data } = await supabase
    .from("user_roles")
    .select("role")
    .eq("user_id", user.id)
    .single();

  return (data?.role as "user" | "admin" | "owner") ?? "user";
}
```

---

## Verify

1. `pnpm typecheck` — No TypeScript errors
2. `pnpm dev` — App starts, login page renders
3. Create a test account in Supabase Dashboard → Authentication → Users
4. Sign in → verify redirect works
5. Access a protected route without session → verify redirect to `/login`

---

## Anti-Patterns

- NEVER use `@supabase/auth-helpers-nextjs` — it is deprecated
- NEVER use `cookies().get/set/remove` — always use `getAll/setAll`
- NEVER call `supabase.auth.getSession()` in Server Components — use `getUser()` (validates JWT server-side)
- NEVER skip `router.refresh()` after sign-in — Next.js cache must be invalidated
- NEVER store `SUPABASE_SERVICE_ROLE_KEY` in client-side env vars (no `NEXT_PUBLIC_` prefix)
- NEVER remove the `updateSession` call from middleware — sessions expire without it
