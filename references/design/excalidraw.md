
Create or integrate Excalidraw diagrams and whiteboard components: $ARGUMENTS

$ARGUMENTS should include:
- What to create (diagram, flowchart, architecture, wireframe, whiteboard component)
- Optionally: target component path
- Optionally: programmatic scene data (elements to generate)
- Optionally: export format (svg, png, json)
- Optionally: integration type (embedded component, static export, collaborative)
- Empty — ask the user what they need

## Authoritative Documentation

### Primary References
- Developer Docs: https://docs.excalidraw.com/
- API Overview: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api
- Installation: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/installation
- Integration: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/integration

### Component API
- Props: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/props
- UIOptions: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/props/ui-options
- Imperative API: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/props/excalidraw-api
- Children Components: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/children-components

### Programmatic Creation
- Element Skeletons: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/excalidraw-element-skeleton
- JSON Schema: https://docs.excalidraw.com/docs/codebase/json-schema

### Export & Utils
- Export Utilities: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/export
- Utils: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils

### Children Components
- MainMenu: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/children-components/main-menu
- WelcomeScreen: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/children-components/welcome-screen
- Footer: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/children-components/footer
- Sidebar: https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/children-components/sidebar

### Ecosystem
- Mermaid-to-Excalidraw: https://docs.excalidraw.com/docs/@excalidraw/mermaid-to-excalidraw/api
- Library Browser: https://libraries.excalidraw.com/
- GitHub: https://github.com/excalidraw/excalidraw
- npm: https://www.npmjs.com/package/@excalidraw/excalidraw

## Before Starting

1. Confirm `@excalidraw/excalidraw` is installed — if not: `pnpm add @excalidraw/excalidraw`
2. For programmatic export without React: `pnpm add @excalidraw/utils`
3. For Mermaid conversion: `pnpm add @excalidraw/mermaid-to-excalidraw`
4. Excalidraw does NOT support SSR — must use dynamic import in Next.js

## Element Types

| Type | Key Properties | Use For |
|---|---|---|
| `rectangle` | base + roundness | Boxes, containers, cards |
| `ellipse` | base | Circles, ovals |
| `diamond` | base | Decision nodes, highlights |
| `line` | points, bindings | Connectors, paths |
| `arrow` | points, start/end bindings, arrowheads | Flow connections |
| `text` | text, fontSize, fontFamily, textAlign | Labels, annotations |
| `freedraw` | points, pressures | Sketches, hand-drawn |
| `image` | fileId, status, scale | Embedded images |
| `frame` | name | Grouping/framing areas |

### Font Families
- `1` = Virgil (hand-drawn, default)
- `2` = Helvetica (clean)
- `3` = Cascadia (monospace/code)

### Fill Styles
- `"solid"` — flat fill
- `"hachure"` — diagonal lines (sketchy)
- `"cross-hatch"` — cross-hatched lines

### Roughness
- `0` = Architect (clean lines)
- `1` = Artist (slightly sketchy, default)
- `2` = Cartoonist (very sketchy)

## Programmatic Scene Creation

### convertToExcalidrawElements

Creates fully qualified elements from minimal skeletons:

```typescript
import { convertToExcalidrawElements } from "@excalidraw/excalidraw";

const elements = convertToExcalidrawElements([
  // Rectangle with label
  {
    type: "rectangle",
    x: 0, y: 0,
    width: 200, height: 80,
    strokeColor: "#1e1e1e",
    backgroundColor: "#a5d8ff",
    fillStyle: "solid",
    roughness: 0,
    label: { text: "Component A", fontSize: 16 },
  },
  // Another rectangle
  {
    type: "rectangle",
    x: 300, y: 0,
    width: 200, height: 80,
    backgroundColor: "#b2f2bb",
    fillStyle: "solid",
    roughness: 0,
    label: { text: "Component B" },
  },
  // Arrow connecting them
  {
    type: "arrow",
    x: 200, y: 40,
    width: 100, height: 0,
    points: [[0, 0], [100, 0]],
    label: { text: "calls" },
  },
  // Standalone text
  {
    type: "text",
    x: 0, y: -40,
    text: "System Architecture",
    fontSize: 24,
    fontFamily: 2,
  },
]);
```

### Arrow Bindings (connecting shapes)

```typescript
const elements = convertToExcalidrawElements([
  { type: "rectangle", id: "box-a", x: 0, y: 0, width: 150, height: 80,
    label: { text: "Service A" } },
  { type: "rectangle", id: "box-b", x: 350, y: 0, width: 150, height: 80,
    label: { text: "Service B" } },
  { type: "arrow", x: 150, y: 40,
    start: { type: "rectangle", id: "box-a" },
    end: { type: "rectangle", id: "box-b" },
    label: { text: "HTTP" } },
]);
```

## React Integration

### Basic Embedded Component

```tsx
"use client";

import { Excalidraw } from "@excalidraw/excalidraw";
import { useState } from "react";
import type { ExcalidrawImperativeAPI } from "@excalidraw/excalidraw/types";

export function WhiteboardEditor() {
  const [api, setApi] = useState<ExcalidrawImperativeAPI | null>(null);

  return (
    <div className="w-full h-[600px] rounded-lg border overflow-hidden">
      <Excalidraw
        excalidrawAPI={setApi}
        theme="light"
        UIOptions={{
          canvasActions: {
            toggleTheme: true,
            export: { saveFileToDisk: true },
          },
        }}
      />
    </div>
  );
}
```

### Next.js Integration (required pattern)

Excalidraw does NOT support SSR. Always use dynamic import:

```tsx
// components/ExcalidrawWrapper.tsx
"use client";

import { Excalidraw, convertToExcalidrawElements } from "@excalidraw/excalidraw";

interface Props {
  initialElements?: any[];
  theme?: "light" | "dark";
}

export default function ExcalidrawWrapper({ initialElements, theme = "light" }: Props) {
  return (
    <Excalidraw
      theme={theme}
      initialData={
        initialElements
          ? { elements: convertToExcalidrawElements(initialElements) }
          : undefined
      }
    />
  );
}
```

```tsx
// In your page or component
import dynamic from "next/dynamic";

const ExcalidrawWrapper = dynamic(
  () => import("@/components/ExcalidrawWrapper"),
  { ssr: false }
);

export default function Page() {
  return (
    <div className="w-full h-[600px]">
      <ExcalidrawWrapper theme="light" />
    </div>
  );
}
```

### Read-Only Viewer (static export)

```tsx
"use client";

import { Excalidraw } from "@excalidraw/excalidraw";

export function DiagramViewer({ elements }: { elements: any[] }) {
  return (
    <div className="w-full h-[400px]">
      <Excalidraw
        initialData={{ elements }}
        UIOptions={{
          canvasActions: {
            export: false,
            loadScene: false,
            clearCanvas: false,
          },
          tools: { image: false },
        }}
      />
    </div>
  );
}
```

## Imperative API

Access via the `excalidrawAPI` callback prop:

```typescript
const [api, setApi] = useState<ExcalidrawImperativeAPI | null>(null);
<Excalidraw excalidrawAPI={setApi} />
```

| Method | Description |
|---|---|
| `api.updateScene({ elements, appState })` | Update scene programmatically |
| `api.getSceneElements()` | Get all non-deleted elements |
| `api.getAppState()` | Get current app state |
| `api.getFiles()` | Get current files |
| `api.scrollToContent(target?, opts?)` | Scroll/zoom to fit content |
| `api.setActiveTool({ type })` | Set drawing tool |
| `api.toggleSidebar({ name })` | Toggle sidebar |
| `api.setToast({ message })` | Show toast |
| `api.addFiles(files)` | Add image files |

**Note:** Ref support was removed in v0.17.0. Use the `excalidrawAPI` callback.

## Export

### From React Component

```typescript
import {
  exportToSvg,
  exportToBlob,
  exportToCanvas,
  exportToClipboard,
  serializeAsJSON,
} from "@excalidraw/excalidraw";

// Export to SVG
const svg = await exportToSvg({
  elements: api.getSceneElements(),
  appState: api.getAppState(),
  files: api.getFiles(),
});

// Export to PNG blob
const blob = await exportToBlob({
  elements: api.getSceneElements(),
  appState: { ...api.getAppState(), exportWithDarkMode: false },
  files: api.getFiles(),
  mimeType: "image/png",
});

// Export to JSON string
const json = serializeAsJSON(
  api.getSceneElements(),
  api.getAppState(),
  api.getFiles(),
  "local"
);
```

### Standalone Export (no React)

```typescript
import { exportToSvg, exportToBlob } from "@excalidraw/utils";

// Server-side or script-based export
const svg = await exportToSvg({ elements, appState, files });
```

## Mermaid-to-Excalidraw

Convert Mermaid diagrams to Excalidraw elements:

```typescript
import { parseMermaidToExcalidraw } from "@excalidraw/mermaid-to-excalidraw";

const { elements, files } = await parseMermaidToExcalidraw(`
  flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
`);

api.updateScene({ elements, files });
```

## Custom UI Components

Render as children of `<Excalidraw>`:

```tsx
<Excalidraw>
  <MainMenu>
    <MainMenu.DefaultItems.LoadScene />
    <MainMenu.DefaultItems.Export />
    <MainMenu.DefaultItems.SaveAsImage />
    <MainMenu.Separator />
    <MainMenu.Item onSelect={() => console.log("custom")}>
      Custom Action
    </MainMenu.Item>
  </MainMenu>

  <WelcomeScreen>
    <WelcomeScreen.Center>
      <WelcomeScreen.Center.Logo>
        <img src="/logo.svg" alt="Logo" />
      </WelcomeScreen.Center.Logo>
      <WelcomeScreen.Center.Heading>
        Start Drawing
      </WelcomeScreen.Center.Heading>
    </WelcomeScreen.Center>
  </WelcomeScreen>
</Excalidraw>
```

## .excalidraw File Format

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

- Elements render in array order (first = back, last = front)
- Deleted elements have `isDeleted: true` (soft-delete)
- `serializeAsJSON` strips deleted elements and internal state

## Diagram Templates

### Flowchart

```typescript
const flowchart = convertToExcalidrawElements([
  { type: "rectangle", id: "start", x: 100, y: 0, width: 150, height: 60,
    backgroundColor: "#a5d8ff", roughness: 0, label: { text: "Start" } },
  { type: "diamond", id: "decide", x: 100, y: 120, width: 150, height: 100,
    backgroundColor: "#ffec99", roughness: 0, label: { text: "Condition?" } },
  { type: "rectangle", id: "yes", x: -50, y: 280, width: 150, height: 60,
    backgroundColor: "#b2f2bb", roughness: 0, label: { text: "Yes Path" } },
  { type: "rectangle", id: "no", x: 250, y: 280, width: 150, height: 60,
    backgroundColor: "#ffc9c9", roughness: 0, label: { text: "No Path" } },
  { type: "arrow", start: { id: "start" }, end: { id: "decide" }, x: 175, y: 60 },
  { type: "arrow", start: { id: "decide" }, end: { id: "yes" }, x: 100, y: 220,
    label: { text: "Yes" } },
  { type: "arrow", start: { id: "decide" }, end: { id: "no" }, x: 250, y: 220,
    label: { text: "No" } },
]);
```

### Architecture Diagram

```typescript
const architecture = convertToExcalidrawElements([
  // Title
  { type: "text", x: 0, y: -50, text: "System Architecture",
    fontSize: 28, fontFamily: 2 },
  // Boxes
  { type: "rectangle", id: "client", x: 0, y: 0, width: 180, height: 70,
    backgroundColor: "#a5d8ff", roughness: 0, label: { text: "Client App" } },
  { type: "rectangle", id: "api", x: 250, y: 0, width: 180, height: 70,
    backgroundColor: "#b2f2bb", roughness: 0, label: { text: "API Server" } },
  { type: "rectangle", id: "db", x: 500, y: 0, width: 180, height: 70,
    backgroundColor: "#ffec99", roughness: 0, label: { text: "Database" } },
  // Connections
  { type: "arrow", start: { id: "client" }, end: { id: "api" },
    x: 180, y: 35, label: { text: "REST" } },
  { type: "arrow", start: { id: "api" }, end: { id: "db" },
    x: 430, y: 35, label: { text: "SQL" } },
]);
```

## Output Format

```
## Excalidraw Implementation Report

### Type: Embedded whiteboard component
### Component: components/diagrams/SystemDiagram.tsx

### Elements
- 5 rectangles (service boxes)
- 4 arrows (connections)
- 1 text (title)

### Integration
- Dynamic import with ssr: false
- Theme synced to app theme
- Export to SVG enabled

### Next Steps
- Import into target page
- Connect to data for dynamic diagrams
- Add collaboration if needed
```

## Rules

- Always use dynamic import with `ssr: false` in Next.js
- Use `"use client"` directive on wrapper components
- Use `convertToExcalidrawElements` for programmatic scene creation
- Use `excalidrawAPI` callback prop (not refs) for imperative access
- Set `roughness: 0` for clean/architect style, `1` for sketchy
- Parent container must have explicit height — Excalidraw fills its container
- Use `fontFamily: 2` (Helvetica) for clean text, `1` (Virgil) for hand-drawn feel
- Export with `@excalidraw/utils` for server-side/non-React contexts
- Use Mermaid-to-Excalidraw for converting existing Mermaid diagrams
