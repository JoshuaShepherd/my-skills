---
name: email-setup
description: "Set up transactional email via Resend for Next.js 15 or Vite + Express — React Email templates, send helpers, welcome/magic-link/notification emails, and local dev preview. Use when adding email to any project in this stack."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up transactional email: $ARGUMENTS

$ARGUMENTS can include:
- Provider hint: "resend" (default) or "sendgrid"
- "with-templates" — scaffold common templates (welcome, magic-link, notification)
- "minimal" — just the send helper and one example template
- Empty — full Resend setup with common templates

---

## Before Starting

1. Read `package.json` to detect framework (Next.js vs Vite + Express)
2. Read `src/lib/env.ts` to see existing env var patterns
3. Check if `resend` or `@sendgrid/mail` is already installed
4. Read `src/lib/config/tenant.config.ts` for brand name, sender email, support email

---

## Architecture

```
src/lib/email/
  client.ts          ← Resend SDK singleton
  send.ts            ← send() helper with Result<T> pattern
  templates/
    WelcomeEmail.tsx
    MagicLinkEmail.tsx
    NotificationEmail.tsx
    _Base.tsx         ← Shared layout (logo, footer, brand colors)

src/app/api/email/
  preview/route.ts   ← GET: render template in browser (dev only)

emails/              ← (optional) standalone React Email dev server
```

---

## Step 1 — Install Packages

```bash
pnpm add resend @react-email/components @react-email/render
```

For local preview dev server (optional):
```bash
pnpm add -D react-email
```

---

## Step 2 — Environment Variables

Add to `.env.local` and `.env.example`:

```bash
# --- Email (Resend) ---
# API key from resend.com/api-keys
RESEND_API_KEY=re_...
# From address (must be a verified domain in Resend)
RESEND_FROM_EMAIL=hello@yourdomain.com
RESEND_FROM_NAME=Your App
```

Add to `src/lib/env.ts`:

```typescript
server: {
  RESEND_API_KEY: z.string().startsWith("re_"),
  RESEND_FROM_EMAIL: z.string().email(),
  RESEND_FROM_NAME: z.string().min(1),
},
```

---

## Step 3 — Resend Client

Create `src/lib/email/client.ts`:

```typescript
import { Resend } from "resend";

export const resend = new Resend(process.env.RESEND_API_KEY);
```

---

## Step 4 — Send Helper

Create `src/lib/email/send.ts`:

```typescript
import type { ReactElement } from "react";
import { render } from "@react-email/render";
import { resend } from "./client";

interface SendEmailOptions {
  to: string | string[];
  subject: string;
  template: ReactElement;
  replyTo?: string;
  from?: string;
}

type Result<T> = { ok: true; data: T } | { ok: false; error: string };

export async function sendEmail(options: SendEmailOptions): Promise<Result<{ id: string }>> {
  const { to, subject, template, replyTo, from } = options;

  const fromAddress = from ?? `${process.env.RESEND_FROM_NAME} <${process.env.RESEND_FROM_EMAIL}>`;

  try {
    const { data, error } = await resend.emails.send({
      from: fromAddress,
      to: Array.isArray(to) ? to : [to],
      subject,
      react: template,
      replyTo,
    });

    if (error) return { ok: false, error: error.message };
    return { ok: true, data: { id: data!.id } };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : "Unknown error" };
  }
}
```

---

## Step 5 — Base Layout Template

Create `src/lib/email/templates/_Base.tsx`:

```typescript
import {
  Body,
  Container,
  Head,
  Html,
  Preview,
  Section,
  Text,
  Hr,
  Link,
} from "@react-email/components";
import { tenantConfig } from "@/lib/config/tenant.config";

interface BaseEmailProps {
  preview: string;
  children: React.ReactNode;
}

export function BaseEmail({ preview, children }: BaseEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>{preview}</Preview>
      <Body style={{ backgroundColor: "#f6f9fc", fontFamily: "sans-serif" }}>
        <Container style={{ maxWidth: "560px", margin: "40px auto", backgroundColor: "#ffffff", borderRadius: "8px", padding: "40px" }}>
          <Text style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "24px" }}>
            {tenantConfig.name}
          </Text>
          {children}
          <Hr style={{ margin: "32px 0", borderColor: "#e6e6e6" }} />
          <Section>
            <Text style={{ fontSize: "12px", color: "#8898aa" }}>
              {tenantConfig.name} · {tenantConfig.tagline}
            </Text>
            <Text style={{ fontSize: "12px", color: "#8898aa" }}>
              <Link href="{{{RESEND_UNSUBSCRIBE_URL}}}">Unsubscribe</Link>
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}
```

---

## Step 6 — Common Templates

### src/lib/email/templates/WelcomeEmail.tsx
```typescript
import { Button, Section, Text } from "@react-email/components";
import { BaseEmail } from "./_Base";
import { tenantConfig } from "@/lib/config/tenant.config";

interface Props {
  name: string;
  dashboardUrl: string;
}

export function WelcomeEmail({ name, dashboardUrl }: Props) {
  return (
    <BaseEmail preview={`Welcome to ${tenantConfig.name}, ${name}`}>
      <Text style={{ fontSize: "20px", fontWeight: "600" }}>
        Welcome, {name}
      </Text>
      <Text style={{ color: "#525f7f" }}>
        You're now part of {tenantConfig.name}. Here's everything you need to get started.
      </Text>
      <Section style={{ textAlign: "center", marginTop: "24px" }}>
        <Button
          href={dashboardUrl}
          style={{
            backgroundColor: "#000",
            color: "#fff",
            padding: "12px 24px",
            borderRadius: "6px",
            textDecoration: "none",
          }}
        >
          Go to your dashboard
        </Button>
      </Section>
    </BaseEmail>
  );
}
```

### src/lib/email/templates/MagicLinkEmail.tsx
```typescript
import { Button, Section, Text } from "@react-email/components";
import { BaseEmail } from "./_Base";

interface Props {
  magicLink: string;
  expiresInMinutes?: number;
}

export function MagicLinkEmail({ magicLink, expiresInMinutes = 10 }: Props) {
  return (
    <BaseEmail preview="Your sign-in link">
      <Text style={{ fontSize: "20px", fontWeight: "600" }}>Your sign-in link</Text>
      <Text style={{ color: "#525f7f" }}>
        Click below to sign in. This link expires in {expiresInMinutes} minutes.
      </Text>
      <Section style={{ textAlign: "center", marginTop: "24px" }}>
        <Button
          href={magicLink}
          style={{
            backgroundColor: "#000",
            color: "#fff",
            padding: "12px 24px",
            borderRadius: "6px",
            textDecoration: "none",
          }}
        >
          Sign in
        </Button>
      </Section>
      <Text style={{ fontSize: "12px", color: "#8898aa" }}>
        If you didn't request this, you can safely ignore this email.
      </Text>
    </BaseEmail>
  );
}
```

### src/lib/email/templates/NotificationEmail.tsx
```typescript
import { Text } from "@react-email/components";
import { BaseEmail } from "./_Base";

interface Props {
  title: string;
  body: string;
  ctaLabel?: string;
  ctaUrl?: string;
}

export function NotificationEmail({ title, body, ctaLabel, ctaUrl }: Props) {
  return (
    <BaseEmail preview={title}>
      <Text style={{ fontSize: "20px", fontWeight: "600" }}>{title}</Text>
      <Text style={{ color: "#525f7f" }}>{body}</Text>
      {ctaUrl && ctaLabel && (
        <Text>
          <a href={ctaUrl} style={{ color: "#000", fontWeight: "500" }}>{ctaLabel} →</a>
        </Text>
      )}
    </BaseEmail>
  );
}
```

---

## Step 7 — Usage Examples

### In an API route (server-side only)
```typescript
import { sendEmail } from "@/lib/email/send";
import { WelcomeEmail } from "@/lib/email/templates/WelcomeEmail";

// After user signs up:
const result = await sendEmail({
  to: user.email,
  subject: `Welcome to ${tenantConfig.name}!`,
  template: <WelcomeEmail name={user.name} dashboardUrl={`${APP_URL}/dashboard`} />,
});

if (!result.ok) {
  console.error("Failed to send welcome email:", result.error);
  // Don't block the user flow — email is non-critical
}
```

---

## Step 8 — Dev Preview Route (optional)

Create `src/app/api/email/preview/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { render } from "@react-email/render";
import { WelcomeEmail } from "@/lib/email/templates/WelcomeEmail";

// Only available in development
export async function GET(request: Request) {
  if (process.env.NODE_ENV === "production") {
    return NextResponse.json({ error: "Not available" }, { status: 404 });
  }

  const { searchParams } = new URL(request.url);
  const template = searchParams.get("template") ?? "welcome";

  const templates: Record<string, React.ReactElement> = {
    welcome: <WelcomeEmail name="Test User" dashboardUrl="http://localhost:3000/dashboard" />,
  };

  const html = render(templates[template] ?? templates.welcome);
  return new NextResponse(html, { headers: { "Content-Type": "text/html" } });
}
```

Preview at: `http://localhost:3000/api/email/preview?template=welcome`

---

## Step 9 — Package.json Scripts (optional)

```json
{
  "scripts": {
    "email:dev": "email dev --dir src/lib/email/templates --port 3001"
  }
}
```

Run `pnpm email:dev` to open the React Email dev server with live preview.

---

## Verify

1. `pnpm typecheck` — no errors
2. Add a real `RESEND_API_KEY` to `.env.local`
3. Hit `POST /api/email/test` or call `sendEmail()` directly in a test
4. Check Resend dashboard → Emails for delivery confirmation
5. `GET /api/email/preview` — verify HTML renders correctly in browser

---

## Anti-Patterns

- NEVER call `sendEmail()` from client components — server-side only (API routes, Server Actions)
- NEVER block user flows on email send failures — log and continue
- NEVER use unverified sender domains — Resend will reject or spam-filter
- NEVER hardcode recipient emails — always use user data from auth
- NEVER send emails in unit tests — mock `sendEmail()` with `vi.mock()`
