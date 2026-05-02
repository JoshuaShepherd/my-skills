---
name: stripe-setup
description: "Set up Stripe payments for Next.js 15 or Vite + Express — subscriptions, one-time payments, webhooks, customer portal, billing middleware, and Supabase subscription sync. Use when adding payments to any project in this stack."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Stripe payments: $ARGUMENTS

$ARGUMENTS can include:
- "subscriptions" — recurring billing with plans (default)
- "one-time" — single charge / product purchase
- "both" — subscriptions + one-time payments
- "with-portal" — include Stripe Customer Portal (default: included)
- "minimal" — webhooks + basic checkout only, no portal
- Empty — full subscription setup with portal

---

## Before Starting

1. Read `package.json` to detect framework (Next.js vs Vite + Express)
2. Read `src/lib/env.ts` to see existing env var patterns
3. Read `src/lib/database/schema.ts` — check for existing subscriptions/customers tables
4. Check Supabase MCP for `subscriptions`, `stripe_customers` tables
5. Read `src/lib/services/simplified/` for service patterns to match

---

## Architecture

```
src/lib/stripe/
  client.ts          ← Stripe SDK singleton
  prices.ts          ← Price/plan ID constants
  helpers.ts         ← getOrCreateCustomer(), syncSubscription()

src/app/api/
  stripe/
    checkout/route.ts       ← POST: create checkout session
    portal/route.ts         ← POST: create customer portal session
    webhooks/route.ts       ← POST: handle Stripe webhook events

src/lib/services/custom/
  stripe.service.ts         ← Business logic (subscription status, etc.)

src/hooks/custom/
  use-subscription.ts       ← Current user's subscription state

src/components/pricing/
  CheckoutButton.tsx
  ManageBillingButton.tsx
  PricingCard.tsx
```

---

## Step 1 — Install Packages

```bash
pnpm add stripe @stripe/stripe-js
```

---

## Step 2 — Environment Variables

Add to `.env.local` and `.env.example`:

```bash
# --- Stripe ---
# Public key (safe for browser)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
# Secret key (server only — never expose to browser)
STRIPE_SECRET_KEY=sk_test_...
# Webhook signing secret: stripe listen --forward-to localhost:3000/api/stripe/webhooks
STRIPE_WEBHOOK_SECRET=whsec_...
# Price IDs from Stripe Dashboard
STRIPE_PRICE_MONTHLY=price_...
STRIPE_PRICE_YEARLY=price_...
```

Add to `src/lib/env.ts`:

```typescript
server: {
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),
  STRIPE_PRICE_MONTHLY: z.string().startsWith("price_").optional(),
  STRIPE_PRICE_YEARLY: z.string().startsWith("price_").optional(),
},
client: {
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().startsWith("pk_"),
},
```

---

## Step 3 — Stripe Client Singleton

Create `src/lib/stripe/client.ts`:

```typescript
import Stripe from "stripe";

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-06-20",
  typescript: true,
});
```

Create `src/lib/stripe/prices.ts`:

```typescript
export const PRICES = {
  monthly: process.env.STRIPE_PRICE_MONTHLY!,
  yearly: process.env.STRIPE_PRICE_YEARLY!,
} as const;

export type PricePlan = keyof typeof PRICES;
```

---

## Step 4 — Database Schema

Add to `src/lib/database/schema.ts` (if not present):

```typescript
export const stripeCustomers = pgTable("stripe_customers", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id").notNull().unique(),
  organizationId: uuid("organization_id").references(() => organizations.id),
  stripeCustomerId: text("stripe_customer_id").notNull().unique(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const subscriptions = pgTable("subscriptions", {
  id: uuid("id").defaultRandom().primaryKey(),
  organizationId: uuid("organization_id").references(() => organizations.id).notNull(),
  stripeSubscriptionId: text("stripe_subscription_id").notNull().unique(),
  stripePriceId: text("stripe_price_id").notNull(),
  status: text("status").notNull(), // active | canceled | past_due | trialing
  currentPeriodStart: timestamp("current_period_start").notNull(),
  currentPeriodEnd: timestamp("current_period_end").notNull(),
  cancelAtPeriodEnd: boolean("cancel_at_period_end").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
```

Then run: `pnpm drizzle:gen && pnpm drizzle:push`

---

## Step 5 — Stripe Helpers

Create `src/lib/stripe/helpers.ts`:

```typescript
import { stripe } from "./client";
import { db } from "@/lib/database/db";
import { stripeCustomers } from "@/lib/database/schema";
import { eq } from "drizzle-orm";

export async function getOrCreateStripeCustomer(
  userId: string,
  email: string,
  orgId?: string
): Promise<string> {
  const existing = await db.query.stripeCustomers.findFirst({
    where: eq(stripeCustomers.userId, userId),
  });

  if (existing) return existing.stripeCustomerId;

  const customer = await stripe.customers.create({
    email,
    metadata: { userId, organizationId: orgId ?? "" },
  });

  await db.insert(stripeCustomers).values({
    userId,
    organizationId: orgId,
    stripeCustomerId: customer.id,
  });

  return customer.id;
}
```

---

## Step 6 — Checkout Route

Create `src/app/api/stripe/checkout/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { stripe } from "@/lib/stripe/client";
import { getOrCreateStripeCustomer } from "@/lib/stripe/helpers";
import { createClient } from "@/lib/supabase/server";
import { getTenantOrgId } from "@/lib/tenant";
import { z } from "zod";

const schema = z.object({
  priceId: z.string().startsWith("price_"),
  successUrl: z.string().url().optional(),
  cancelUrl: z.string().url().optional(),
});

export async function POST(request: Request) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid request" }, { status: 400 });
  }

  const { priceId, successUrl, cancelUrl } = parsed.data;
  const orgId = getTenantOrgId();
  const customerId = await getOrCreateStripeCustomer(user.id, user.email!, orgId);

  const session = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: successUrl ?? `${process.env.NEXT_PUBLIC_APP_URL}/account?success=true`,
    cancel_url: cancelUrl ?? `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    subscription_data: {
      metadata: { organizationId: orgId },
    },
  });

  return NextResponse.json({ url: session.url });
}
```

---

## Step 7 — Customer Portal Route

Create `src/app/api/stripe/portal/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { stripe } from "@/lib/stripe/client";
import { createClient } from "@/lib/supabase/server";
import { db } from "@/lib/database/db";
import { stripeCustomers } from "@/lib/database/schema";
import { eq } from "drizzle-orm";

export async function POST() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const customer = await db.query.stripeCustomers.findFirst({
    where: eq(stripeCustomers.userId, user.id),
  });

  if (!customer) {
    return NextResponse.json({ error: "No billing account found" }, { status: 404 });
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: customer.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/account`,
  });

  return NextResponse.json({ url: session.url });
}
```

---

## Step 8 — Webhook Handler

Create `src/app/api/stripe/webhooks/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { stripe } from "@/lib/stripe/client";
import { db } from "@/lib/database/db";
import { subscriptions } from "@/lib/database/schema";
import { eq } from "drizzle-orm";
import type Stripe from "stripe";

export async function POST(request: Request) {
  const body = await request.text();
  const sig = request.headers.get("stripe-signature")!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  switch (event.type) {
    case "customer.subscription.created":
    case "customer.subscription.updated": {
      const sub = event.data.object as Stripe.Subscription;
      const orgId = sub.metadata.organizationId;
      await db
        .insert(subscriptions)
        .values({
          organizationId: orgId,
          stripeSubscriptionId: sub.id,
          stripePriceId: sub.items.data[0].price.id,
          status: sub.status,
          currentPeriodStart: new Date(sub.current_period_start * 1000),
          currentPeriodEnd: new Date(sub.current_period_end * 1000),
          cancelAtPeriodEnd: sub.cancel_at_period_end,
        })
        .onConflictDoUpdate({
          target: subscriptions.stripeSubscriptionId,
          set: {
            status: sub.status,
            stripePriceId: sub.items.data[0].price.id,
            currentPeriodStart: new Date(sub.current_period_start * 1000),
            currentPeriodEnd: new Date(sub.current_period_end * 1000),
            cancelAtPeriodEnd: sub.cancel_at_period_end,
            updatedAt: new Date(),
          },
        });
      break;
    }
    case "customer.subscription.deleted": {
      const sub = event.data.object as Stripe.Subscription;
      await db
        .update(subscriptions)
        .set({ status: "canceled", updatedAt: new Date() })
        .where(eq(subscriptions.stripeSubscriptionId, sub.id));
      break;
    }
  }

  return NextResponse.json({ received: true });
}
```

---

## Step 9 — UI Components

### src/components/pricing/CheckoutButton.tsx
```typescript
"use client";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface Props {
  priceId: string;
  label?: string;
}

export function CheckoutButton({ priceId, label = "Get started" }: Props) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    const res = await fetch("/api/stripe/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ priceId }),
    });
    const { url } = await res.json();
    if (url) window.location.href = url;
    setLoading(false);
  };

  return (
    <Button onClick={handleCheckout} disabled={loading}>
      {loading ? "Loading..." : label}
    </Button>
  );
}
```

---

## Step 10 — Local Webhook Testing

```bash
# Install Stripe CLI (one-time)
brew install stripe/stripe-cli/stripe

# Forward webhooks to local dev server
stripe listen --forward-to localhost:3000/api/stripe/webhooks

# Trigger a test event
stripe trigger customer.subscription.created
```

---

## Verify

1. `pnpm typecheck` — no errors
2. Create a test checkout: click CheckoutButton, complete with card `4242 4242 4242 4242`
3. Verify webhook fires and subscription row is created in DB
4. Open portal: ManageBillingButton → verify Stripe portal loads
5. Cancel subscription in portal → verify status updates to `canceled`

---

## Anti-Patterns

- NEVER log or store raw webhook payloads — they contain PII
- NEVER skip `stripe.webhooks.constructEvent()` signature verification
- NEVER use Stripe test keys in production (check `sk_live_` vs `sk_test_`)
- NEVER grant refunds or cancel subscriptions from client-side code — server only
- NEVER store `STRIPE_SECRET_KEY` in client env vars (no `NEXT_PUBLIC_` prefix)
