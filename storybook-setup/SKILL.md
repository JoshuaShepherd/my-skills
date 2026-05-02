---
name: storybook-setup
description: "Set up Storybook 8 for Next.js 15 or Vite + React — component dev environment, story scaffolding, shadcn/ui integration, dark mode toggle, accessibility checks (a11y addon), and visual regression snapshot configuration. Use when setting up a component library or design system workflow."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Set up Storybook: $ARGUMENTS

$ARGUMENTS can include:
- Framework hint: "nextjs" or "vite" (auto-detected)
- "with-a11y" — include accessibility addon (default: included)
- "with-chromatic" — include Chromatic visual regression testing
- "minimal" — bare Storybook without addons
- Empty — full setup with a11y addon

---

## Before Starting

1. Read `package.json` to detect framework (Next.js vs Vite)
2. Read `src/app/globals.css` — need to import this in Storybook for Tailwind + tokens
3. Read `tailwind.config.ts` — need to configure content paths
4. Check if `.storybook/` already exists
5. Read `src/components/ui/button.tsx` as example of existing component patterns

---

## Architecture

```
.storybook/
  main.ts              ← Framework config, addons, webpack/vite overrides
  preview.ts           ← Global decorators, Tailwind CSS import, dark mode

src/components/
  ui/
    button.stories.tsx ← Example story for existing shadcn component
  [domain]/
    MyComponent.stories.tsx

stories/               ← (optional) design system documentation stories
  Introduction.mdx
  Colors.stories.tsx
  Typography.stories.tsx
```

---

## Step 1 — Install Storybook

### Next.js
```bash
pnpm dlx storybook@latest init --type nextjs --no-dev
# or manually:
pnpm add -D @storybook/nextjs @storybook/addon-essentials @storybook/addon-interactions @storybook/addon-a11y storybook
```

### Vite + React
```bash
pnpm add -D @storybook/react-vite @storybook/addon-essentials @storybook/addon-interactions @storybook/addon-a11y storybook
```

---

## Step 2 — .storybook/main.ts (Next.js)

```typescript
import type { StorybookConfig } from "@storybook/nextjs";

const config: StorybookConfig = {
  stories: [
    "../src/**/*.mdx",
    "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)",
    "../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)",
  ],

  addons: [
    "@storybook/addon-essentials",      // controls, actions, docs, viewport
    "@storybook/addon-interactions",    // play() function testing
    "@storybook/addon-a11y",            // accessibility checks
    // "@chromatic-com/storybook",      // uncomment if with-chromatic
  ],

  framework: {
    name: "@storybook/nextjs",
    options: {},
  },

  docs: { autodocs: "tag" },

  staticDirs: ["../public"],
};

export default config;
```

---

## Step 3 — .storybook/main.ts (Vite)

```typescript
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: [
    "../src/**/*.mdx",
    "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)",
  ],

  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
  ],

  framework: {
    name: "@storybook/react-vite",
    options: {},
  },

  docs: { autodocs: "tag" },
};

export default config;
```

---

## Step 4 — .storybook/preview.ts

```typescript
import type { Preview } from "@storybook/react";
import "../src/app/globals.css";   // Import Tailwind + CSS variables

// Mock Next.js navigation for stories
import { initialize, mswLoader } from "msw-storybook-addon"; // optional

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: "light",
      values: [
        { name: "light", value: "#ffffff" },
        { name: "dark", value: "#09090b" },  // Match globals.css --background
      ],
    },
    layout: "centered",
  },

  decorators: [
    (Story, context) => {
      // Apply dark mode class when background is dark
      const isDark = context.globals.backgrounds?.value === "#09090b";
      return (
        <div className={isDark ? "dark" : ""}>
          <Story />
        </div>
      );
    },
  ],

  globalTypes: {
    darkMode: {
      description: "Toggle dark mode",
      defaultValue: "light",
      toolbar: {
        title: "Theme",
        icon: "circlehollow",
        items: ["light", "dark"],
        dynamicTitle: true,
      },
    },
  },
};

export default preview;
```

---

## Step 5 — Example Story (Button)

Create `src/components/ui/button.stories.tsx`:

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta: Meta<typeof Button> = {
  title: "UI/Button",
  component: Button,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "destructive", "outline", "secondary", "ghost", "link"],
    },
    size: {
      control: "select",
      options: ["default", "sm", "lg", "icon"],
    },
    disabled: { control: "boolean" },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Button",
    variant: "default",
    size: "default",
  },
};

export const Destructive: Story = {
  args: {
    children: "Delete",
    variant: "destructive",
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      {(["default", "secondary", "destructive", "outline", "ghost", "link"] as const).map(
        (variant) => (
          <Button key={variant} variant={variant}>
            {variant}
          </Button>
        )
      )}
    </div>
  ),
};

export const Loading: Story = {
  args: {
    children: "Loading...",
    disabled: true,
  },
};
```

---

## Step 6 — Story Scaffold for Domain Components

Template for any new component `MyComponent`:

```typescript
// src/components/[domain]/MyComponent.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { MyComponent } from "./MyComponent";

const meta: Meta<typeof MyComponent> = {
  title: "[Domain]/MyComponent",   // e.g. "Cards/CourseCard"
  component: MyComponent,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",              // "centered" | "padded" | "fullscreen"
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    // Provide sensible default props
  },
};

export const WithLongContent: Story = {
  args: {
    // Edge case: long text
  },
};
```

---

## Step 7 — Package.json Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "storybook": "storybook dev -p 6006",
    "storybook:build": "storybook build",
    "storybook:test": "test-storybook"
  }
}
```

---

## Step 8 — .storybook/tsconfig.json (if needed)

If TypeScript path aliases (`@/`) don't resolve in Storybook:

```json
{
  "extends": "../tsconfig.json",
  "compilerOptions": {
    "paths": {
      "@/*": ["../src/*"]
    }
  }
}
```

And in `main.ts`:
```typescript
import path from "path";

const config: StorybookConfig = {
  // ...
  webpackFinal: async (config) => {
    config.resolve!.alias = {
      ...config.resolve!.alias,
      "@": path.resolve(__dirname, "../src"),
    };
    return config;
  },
};
```

For Vite: add alias in `main.ts` via `viteFinal`.

---

## Step 9 — Chromatic (with-chromatic flag)

```bash
pnpm add -D chromatic @chromatic-com/storybook
```

Add to CI workflow (`.github/workflows/ci.yml`):

```yaml
- name: Publish to Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    buildScriptName: storybook:build
```

---

## Verify

1. `pnpm storybook` — opens at `http://localhost:6006`
2. Button story renders with all variants
3. Controls panel works — change variant, see live update
4. Dark mode toggle works — component matches dark theme
5. A11y addon shows no violations on Button stories
6. `pnpm storybook:build` — builds static export without errors

---

## Anti-Patterns

- NEVER import from `src/app/` in stories — avoid Next.js app router internals
- NEVER use real API calls in stories — mock with `msw-storybook-addon` or static data
- NEVER skip `tags: ["autodocs"]` on reusable components — auto-generates documentation
- NEVER store Chromatic tokens in code — use GitHub secrets
- NEVER write stories for pages — stories are for components and design system atoms
