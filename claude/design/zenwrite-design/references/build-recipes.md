# ZenWrite Build Recipes — copy-paste, token-correct skeletons

Start from the matching skeleton, then fill it in. Every skeleton here is already token-correct,
accessible, and sphere-aware. **Do not invent alternative markup for these patterns** — the point of
the design chain is that these shapes are the same everywhere.

Import conventions (repo):
```tsx
import { getViewAccent, navItemClasses } from '@/src/lib/viewAccents';
import ViewPageHeader from '@/src/components/ViewPageHeader';
import StatusChip from '@/src/components/StatusChip';
import { LoadingState, EmptyState, ErrorState } from '@/src/components/StateLayouts';
```

---

## 1. Home tile (dual-sphere directory)

Content-sphere tile uses violet; community tiles resolve hover/accent from the sphere. Prefer
`getViewAccent(view)` for community accents rather than the inline strings shown here.

```tsx
<button
  onClick={() => onSelectView('organize')}
  className="group w-full flex items-center gap-4 p-5 bg-white border border-brand-violet/10
             rounded-2xl shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md
             hover:bg-brand-violet/[0.04] hover:border-brand-violet/25
             focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none"
>
  <span className="p-3 rounded-xl bg-brand-violet/5 text-brand-violet">
    <FolderOpen size={22} strokeWidth={1.75} aria-hidden />
  </span>
  <div className="text-left">
    <h4 className="font-serif text-lg font-light">Organize</h4>
    <p className="text-xs text-stone-500 font-serif">Your full library, themes, and courses.</p>
  </div>
  <ChevronRight className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-brand-violet" aria-hidden />
</button>
```

Sphere accent/hover (use the token or `getViewAccent`):
| Tile | accent | hover wash |
|------|--------|-----------|
| create, edit, organize | `text-brand-violet` | `hover:bg-brand-violet/[0.04] hover:border-brand-violet/25` |
| engage / kairos | `text-sky-700` | `hover:bg-sky-500/[0.06] hover:border-sky-500/30` |
| manage | `text-emerald-700` | `hover:bg-emerald-500/[0.06] hover:border-emerald-500/30` |
| analyze | `text-rose-700` | `hover:bg-rose-500/[0.06] hover:border-rose-500/30` |

Section header (between the two sphere columns):
```tsx
<div className="flex items-center gap-3 mb-6">
  <h3 className="font-serif text-2xl font-light italic text-brand-violet tracking-tight">Create &amp; Craft</h3>
  <div className="h-px flex-1 bg-brand-violet/10" />
  <span className="font-manrope text-[10px] font-extrabold uppercase tracking-[0.25em] text-brand-violet/40">Content Workspaces</span>
</div>
```

---

## 2. Slide-in right panel (secondary editing task)

Used by MetadataPanel, AcademicPanel, RevisionPanel, TeleprompterPanel. Extract a `SlideInPanel`
primitive only once you have a real third consumer.

```tsx
export default function ExamplePanel({ open, onClose, items }: Props) {
  if (!open) return null;
  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40" onClick={onClose} aria-hidden />
      {/* Panel */}
      <aside
        role="dialog"
        aria-label="Example panel"
        className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white border-l border-brand-violet/10
                   shadow-2xl z-50 flex flex-col animate-in slide-in-from-right duration-300"
      >
        <header className="flex items-center justify-between px-6 py-4 border-b border-brand-violet/5">
          <h2 className="font-serif text-lg font-light italic text-brand-violet">Panel Title</h2>
          <button
            onClick={onClose}
            aria-label="Close panel"
            className="text-stone-400 hover:text-brand-violet rounded-lg p-1
                       focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none"
          >
            <X size={18} aria-hidden />
          </button>
        </header>
        <div className="flex-1 overflow-y-auto p-6">
          {items.length === 0
            ? <EmptyState title="Nothing here yet" message="Add an item to get started." />
            : <ul className="space-y-3">{/* cards with StatusChip */}</ul>}
        </div>
      </aside>
    </>
  );
}
```

Wire in `App.tsx`: add an `examplePanelOpen` boolean, render `<ExamplePanel open={examplePanelOpen}
onClose={() => setExamplePanelOpen(false)} ... />` alongside the other overlays. Add `ESC` to close.

---

## 3. Full-screen overlay wizard (multi-step, demands attention)

Used by PublishPanel, CourseCreateWizard, SettingsModal.

```tsx
<div className="fixed inset-0 z-50 flex items-center justify-center">
  <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} aria-hidden />
  <div
    role="dialog"
    aria-modal="true"
    className="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg border border-brand-violet/10
               animate-in zoom-in-95"
  >
    <header className="px-6 py-4 border-b border-brand-violet/5">
      <p className="font-manrope text-[10px] font-extrabold uppercase tracking-[0.25em] text-brand-violet/50">Step {step} of {total}</p>
      <h2 className="font-serif text-xl font-light italic text-brand-violet">New Course</h2>
    </header>
    <div className="p-6 space-y-4">{/* step fields */}</div>
    <footer className="flex items-center justify-end gap-3 px-6 py-4 border-t border-brand-violet/5">
      <button className="px-4 py-2 text-sm text-stone-500 hover:text-brand-violet focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none rounded-lg">Back</button>
      <button className="px-4 py-2 text-sm rounded-lg bg-brand-violet text-white hover:bg-brand-violet/90 focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none">Continue</button>
    </footer>
  </div>
</div>
```

PublishPanel is a distinct full-bleed variant: `fixed inset-0 z-[60] bg-brand-lavender/95 backdrop-blur-xl`.

---

## 4. Community screen (Engage / Manage / Analyze / Kairos)

Lead with the sphere accent via `getViewAccent`; **keep primary CTAs `bg-brand-violet`.**

```tsx
export default function EngageScreen({ ... }: Props) {
  const accent = getViewAccent('engage');
  const [tab, setTab] = useState<'threads' | 'review'>('threads');
  return (
    <div className={`min-h-screen ${accent.pageWash ?? ''}`}>
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <ViewPageHeader view="engage" eyebrow="Scholarly Community" title="Engage Center" />

        {/* Tabs — accent for active, neutral otherwise */}
        <div className="flex gap-2 border-b border-brand-violet/5">
          {(['threads', 'review'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm font-manrope uppercase tracking-wider transition-all duration-200
                          focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none
                          ${tab === t ? accent.tabActive : accent.tabInactiveHover}`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Cards: shared neutral/violet shell; CTA stays brand-violet */}
        <div className="rounded-2xl border border-brand-violet/10 bg-white p-6">
          <button className="px-4 py-2 rounded-lg bg-brand-violet text-white hover:bg-brand-violet/90
                             focus-visible:ring-2 focus-visible:ring-brand-violet focus-visible:outline-none">
            New thread
          </button>
        </div>
      </div>
    </div>
  );
}
```

Swap `'engage'` for `'manage'` (emerald) or `'analyze'` (rose) — everything else is identical.

---

## 5. Catalog / list section (Organize-style)

```tsx
<div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
  <ViewPageHeader view="organize" eyebrow="Content Workspaces" title="Library" />

  {loading && <LoadingState title="Aligning catalog nodes…" message="Resting data streams…" />}
  {error && <ErrorState title="System Resonant Desync" message={error} />}
  {!loading && !error && items.length === 0 && (
    <EmptyState title="No matching workspace items" message="Try clearing filters." />
  )}

  {!loading && !error && items.length > 0 && (
    <ul className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((it) => (
        <li key={it.id}
            className="rounded-2xl border border-brand-violet/10 bg-white p-5 shadow-sm
                       transition-all duration-200 hover:shadow-md hover:border-brand-violet/25">
          <div className="flex items-start justify-between gap-3">
            <h4 className="font-serif text-lg font-light">{it.title}</h4>
            <StatusChip status={it.status} />
          </div>
          {/* pencil (inline edit) · trash (two-step confirm) · dropdown (type/status) */}
        </li>
      ))}
    </ul>
  )}
</div>
```

Every list/manuscript card exposes: **pencil** (inline title edit), **trash** (two-step delete
confirm), **dropdown** (format/status/type selector).

---

## 6. Primitives reuse (don't re-implement)

```tsx
<StatusChip status="in-review" />
<StatusChip status="published" label="Live" />
<VoiceFidelityChip score={87} />
<VoiceFidelityChip score={72} compact />
```

`StatusChip` normalizes status → color-coded pill via a **static** map (published→emerald,
draft→stone, in-review→amber, scheduled→brand-lavender/brand-violet, default→stone). If you need a
new status, extend that static map — never build the class string dynamically.

---

## 7. Editor extension (the hero surface)

Extend `Editor.tsx`, don't rebuild it. Respect the theme + idle-fade contract.

```tsx
// Theme mapping (canonical)
const surfaceClasses =
  settings.theme === 'paper' ? 'bg-workspace-bg-paper text-workspace-text-paper'
  : settings.theme === 'sepia' ? 'bg-workspace-bg-sepia text-workspace-text-sepia'
  : 'bg-workspace-bg-ink text-workspace-text-ink';

<div className={`relative min-h-screen ${surfaceClasses} transition-colors duration-500`}>
  {/* chapter spine (book mode): fixed left w-[240px] */}
  {/* title + contenteditable — measure/fontSize/lineHeight from settings as inline style */}
  {/* selection bubble toolbar: lucide icons size 13; AI transform uses brand-violet + .ai-pulse */}
</div>
```

Rules: bottom stack is `FloatingComposer` above `BottomNav`; both participate in the idle-fade
contract (`duration-700`). Caret: ink theme uses light caret (`#ECECF0`), paper/sepia use brand
violet — prefer `caret-current`. **Never add persistent editor chrome.**

---

## 8. App.tsx wiring cheatsheet

```tsx
// View switch
{currentView === 'organize' && <OrganizeScreen … />}
{(currentView === 'create' || activeManuscript) && (
  activeManuscript?.type === 'video' || activeManuscript?.type === 'podcast'
    ? <MediaSurface … /> : <Editor … />
)}

// Overlay flag (parallel to view)
{examplePanelOpen && <ExamplePanel open onClose={() => setExamplePanelOpen(false)} … />}

// NavigationAxis idle-fade wrapper (never on home; never fade in create-editing? — matches existing)
{currentView !== 'home' && (
  <div className={`transition-all duration-700 z-50 ${
    currentView !== 'create' && isIdle
      ? 'opacity-0 select-none pointer-events-none -translate-y-2'
      : 'opacity-100 pointer-events-auto translate-y-0'}`}>
    <NavigationAxis … />
  </div>
)}
```
