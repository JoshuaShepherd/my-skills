
Build charts and data visualizations using Recharts: $ARGUMENTS

$ARGUMENTS should include:
- What data to visualize and the chart type (line, bar, area, pie, radar, scatter, composed, treemap, funnel, sankey, radial-bar)
- Optionally: data source path or inline data
- Optionally: customization requirements (colors, tooltips, legends, responsive)
- Optionally: target component path
- Empty — ask the user what they want to chart

## Authoritative Documentation

### Primary References
- Getting Started: https://recharts.github.io/en-US/guide/getting-started/
- Customization Guide: https://recharts.github.io/en-US/guide/customize/
- Performance Guide: https://recharts.github.io/en-US/guide/performance/
- API Reference: https://recharts.github.io/en-US/api/
- Examples: https://recharts.github.io/en-US/examples/

### Chart Type APIs
- LineChart: https://recharts.github.io/en-US/api/LineChart/
- BarChart: https://recharts.github.io/en-US/api/BarChart/
- AreaChart: https://recharts.github.io/en-US/api/AreaChart/
- ComposedChart: https://recharts.github.io/en-US/api/ComposedChart/
- ScatterChart: https://recharts.github.io/en-US/api/ScatterChart/
- PieChart: https://recharts.github.io/en-US/api/PieChart/
- RadarChart: https://recharts.github.io/en-US/api/RadarChart/
- RadialBarChart: https://recharts.github.io/en-US/api/RadialBarChart/
- Treemap: https://recharts.github.io/en-US/api/Treemap/
- FunnelChart: https://recharts.github.io/en-US/api/FunnelChart/
- Sankey: https://recharts.github.io/en-US/api/Sankey/

### Key Component APIs
- XAxis: https://recharts.github.io/en-US/api/XAxis/
- YAxis: https://recharts.github.io/en-US/api/YAxis/
- Tooltip: https://recharts.github.io/en-US/api/Tooltip/
- Legend: https://recharts.github.io/en-US/api/Legend/
- CartesianGrid: https://recharts.github.io/en-US/api/CartesianGrid/
- ResponsiveContainer: https://recharts.github.io/en-US/api/ResponsiveContainer/
- Brush: https://recharts.github.io/en-US/api/Brush/
- ReferenceLine: https://recharts.github.io/en-US/api/ReferenceLine/

### Migration & Accessibility
- 3.0 Migration Guide: https://github.com/recharts/recharts/wiki/3.0-migration-guide
- Accessibility Wiki: https://github.com/recharts/recharts/wiki/Recharts-and-accessibility
- GitHub: https://github.com/recharts/recharts
- npm: https://www.npmjs.com/package/recharts

## Before Starting

1. Confirm `recharts` is installed — if not: `pnpm add recharts`
2. Charts require `"use client"` directive in Next.js App Router
3. Read existing chart components for project styling patterns
4. Determine the chart type based on the data shape and visualization goal

## Chart Type Selection Guide

| Data Type | Goal | Chart |
|---|---|---|
| Time series / continuous | Show trends | LineChart or AreaChart |
| Categorical comparison | Compare values | BarChart |
| Part-of-whole | Show proportions | PieChart |
| Multi-variable comparison | Compare profiles | RadarChart |
| Correlation | Show relationships | ScatterChart |
| Mixed series types | Overlay different viz | ComposedChart |
| Hierarchy | Show nested proportions | Treemap |
| Conversion flow | Show drop-off | FunnelChart |
| Flow between stages | Show quantities moving | Sankey |
| Progress / gauge | Show completion | RadialBarChart |

## Data Format

Recharts expects an **array of flat objects**:

```typescript
const data = [
  { name: "Jan", sales: 4000, revenue: 2400 },
  { name: "Feb", sales: 3000, revenue: 1398 },
  { name: "Mar", sales: 2000, revenue: 9800 },
];
```

- Each object = one data point
- Property names referenced via `dataKey` props
- `dataKey` can be a string, dot-path (`"nested.value"`), or accessor function
- Pie/Scatter can receive data directly on the series component

## Core Patterns

### Pattern 1 — Line Chart (Time Series)

```tsx
"use client";

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from "recharts";

interface ChartProps {
  data: Array<{ name: string; value: number }>;
}

export function TrendChart({ data }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
        <XAxis
          dataKey="name"
          className="text-muted-foreground"
          tick={{ fontSize: 12 }}
        />
        <YAxis className="text-muted-foreground" tick={{ fontSize: 12 }} />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line
          type="monotone"
          dataKey="value"
          stroke="hsl(var(--primary))"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Pattern 2 — Bar Chart (Categorical)

```tsx
"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from "recharts";

export function ComparisonChart({ data }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### Pattern 3 — Area Chart (Stacked)

```tsx
<AreaChart data={data}>
  <defs>
    <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
      <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
    </linearGradient>
  </defs>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip content={<CustomTooltip />} />
  <Area
    type="monotone"
    dataKey="sales"
    stroke="hsl(var(--primary))"
    fillOpacity={1}
    fill="url(#colorSales)"
    stackId="1"
  />
</AreaChart>
```

### Pattern 4 — Pie / Donut Chart

```tsx
<PieChart>
  <Pie
    data={data}
    cx="50%"
    cy="50%"
    innerRadius={60}   // 0 for solid pie, >0 for donut
    outerRadius={100}
    dataKey="value"
    nameKey="name"
    paddingAngle={2}
    label
  >
    {data.map((entry, i) => (
      <Cell key={i} fill={COLORS[i % COLORS.length]} />
    ))}
  </Pie>
  <Tooltip />
  <Legend />
</PieChart>
```

### Pattern 5 — Composed Chart (Mixed)

```tsx
<ComposedChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis yAxisId="left" />
  <YAxis yAxisId="right" orientation="right" />
  <Tooltip content={<CustomTooltip />} />
  <Legend />
  <Bar yAxisId="left" dataKey="sales" fill="hsl(var(--primary))" />
  <Line yAxisId="right" type="monotone" dataKey="growth" stroke="hsl(var(--chart-2))" />
</ComposedChart>
```

### Pattern 6 — Radar Chart

```tsx
<RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
  <PolarGrid />
  <PolarAngleAxis dataKey="subject" />
  <PolarRadiusAxis />
  <Radar dataKey="score" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.3} />
</RadarChart>
```

## Custom Tooltip (Tailwind-styled)

```tsx
interface TooltipProps {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}

function CustomTooltip({ active, payload, label }: TooltipProps) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-lg border bg-card p-3 shadow-md">
      <p className="text-sm font-medium text-foreground">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} className="text-sm text-muted-foreground">
          <span className="inline-block w-3 h-3 rounded-full mr-2" style={{ backgroundColor: entry.color }} />
          {entry.name}: <span className="font-medium text-foreground">{entry.value.toLocaleString()}</span>
        </p>
      ))}
    </div>
  );
}
```

## Custom Legend (Tailwind-styled)

```tsx
function CustomLegend({ payload }: { payload?: Array<{ value: string; color: string }> }) {
  if (!payload) return null;

  return (
    <div className="flex items-center justify-center gap-4 mt-4">
      {payload.map((entry, i) => (
        <div key={i} className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }} />
          {entry.value}
        </div>
      ))}
    </div>
  );
}
```

## Color Palette (Semantic Tokens)

Use CSS variables from the design system for chart colors:

```typescript
const CHART_COLORS = [
  "hsl(var(--primary))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];
```

If chart-specific tokens don't exist, define them in `globals.css`:
```css
:root {
  --chart-1: var(--primary);
  --chart-2: 173 58% 39%;
  --chart-3: 197 37% 24%;
  --chart-4: 43 74% 66%;
  --chart-5: 27 87% 67%;
}
```

## Animation Configuration

All series components accept:

| Prop | Type | Default | Description |
|---|---|---|---|
| `isAnimationActive` | boolean | `true` | Enable/disable animation |
| `animationBegin` | number | `0` | Delay before animation (ms) |
| `animationDuration` | number | `1500` | Animation duration (ms) |
| `animationEasing` | string | `"ease"` | `"linear"`, `"ease"`, `"ease-in"`, `"ease-out"`, `"ease-in-out"` |

For `prefers-reduced-motion`, disable animations:
```tsx
const prefersReducedMotion = typeof window !== "undefined"
  ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
  : false;

<Line isAnimationActive={!prefersReducedMotion} />
```

## ResponsiveContainer Rules

```tsx
<ResponsiveContainer width="100%" height={400}>
  {/* chart here */}
</ResponsiveContainer>
```

- **Parent must have defined dimensions** — 100% of undefined = 0
- Use `height` as a fixed number or `aspect` prop for ratio-based sizing
- `debounce` prop throttles resize events (default 0)
- Never use `width="100%"` AND `height="100%"` without a sized parent

## Synchronized Charts

Charts with the same `syncId` share tooltip position and brush selection:

```tsx
<LineChart data={data} syncId="dashboard">
  {/* ... */}
</LineChart>

<BarChart data={data} syncId="dashboard">
  {/* ... */}
</BarChart>
```

## Performance Optimization

1. **Large datasets (500+ points):** Set `isAnimationActive={false}`
2. **Downsample data** before passing to Recharts (LTTB algorithm)
3. **Memoize** data arrays and callbacks with `useMemo`/`useCallback`
4. **Use `throttleDelay`** on chart containers for mouse events
5. **Lazy load** charts with Intersection Observer — only mount when visible
6. **Hide dots** on line charts: `dot={false}` reduces SVG nodes significantly
7. **Avoid recreating** objects/arrays on every render (stable references)

## Accessibility

- Set `accessibilityLayer={true}` on chart containers for ARIA labels and keyboard navigation
- Wrap charts in `<div role="img" aria-label="Description of chart">`
- Consider providing a data table alternative for screen readers
- Recharts is NOT fully accessible out of the box — manual ARIA attributes are needed

## Next.js Integration Rules

- **Always add `"use client"`** at the top of chart component files
- Recharts relies on browser APIs — it cannot render server-side
- Works with both App Router and Pages Router
- Wrap in a client component; keep parent pages as server components

## Output Format

```
## Chart Implementation

### Chart Type: Line Chart (Time Series)
### Component: components/charts/TrendChart.tsx

### Data Shape
{ name: string, value: number }[]

### Features
- Responsive (fills parent width)
- Custom tooltip with Tailwind styling
- Semantic color tokens
- Animation with reduced-motion support
- Accessible (role="img" with aria-label)

### Next Steps
- Import into target page
- Pass data from server component
```

## Rules

- Always wrap charts in `ResponsiveContainer` with explicit height
- Always use `"use client"` in Next.js
- Use semantic color tokens (`hsl(var(--primary))`) — never hardcoded hex values
- Custom tooltips must use Tailwind classes matching the design system
- Disable animations when `prefers-reduced-motion` is set
- Hide dots on line charts by default (`dot={false}`) for cleaner appearance
- Use `type="monotone"` for smooth lines, `type="linear"` for straight segments
- For bar charts, add `radius={[4, 4, 0, 0]}` for rounded top corners
- Parent containers must have defined dimensions for ResponsiveContainer to work
- Memoize data and callbacks for performance
