---
name: liveblocks-workspace
description: "Work with the Liveblocks + BlockNote collaborative workspace — add features, debug content rendering, configure rooms, manage auth, set up webhooks, add comments/threads, implement version history, or troubleshoot collaborative editing. Use when touching any workspace/docs collaboration code."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, WebFetch
---

Liveblocks workspace task: $ARGUMENTS

$ARGUMENTS can include:
- "debug" — diagnose why content doesn't render or rooms don't connect
- "add comments" — wire up FloatingComposer + AnchoredThreads/FloatingThreads
- "add mentions" — implement resolveUsers / resolveMentionSuggestions on LiveblocksProvider
- "add version history" — implement useHistoryVersions + HistoryVersionPreview UI
- "add notifications" — set up InboxNotification UI and webhook email triggers
- "add offline" — enable offlineSupport_experimental
- "add server edit" — implement withProsemirrorDocument for AI/server-side doc modification
- "bump room version" — reset all rooms by incrementing WORKSPACE_LIVEBLOCKS_ROOM_VERSION
- "audit" — check all CSS imports, provider config, auth route, feature flags, env vars
- Any free-form task description

---

## Before Starting

1. Read `docs/internal/engineering/LIVEBLOCKS_BLOCKNOTE_WORKSPACE.md` — canonical internal reference
2. Read `src/components/workspace/CollaborativeEditor.tsx` — the editor component
3. Read `src/components/workspace/CollaborativeRoom.tsx` — the provider wrapper
4. Read `src/app/api/liveblocks-auth/route.ts` — auth token issuance
5. Read `src/lib/workspace/liveblocks-room.ts` — room ID versioning
6. Read `src/lib/config/tenant.config.ts` — check `features.collaborativeWorkspace` flag
7. Check `package.json` for `@liveblocks/*` and `@blocknote/*` versions

---

## Architecture

### Component hierarchy

```text
WorkspaceDocPage (src/app/(public)/workspace/docs/[...slug]/page.tsx)
  └── CollaborativeRoom (providers)
        ├── LiveblocksProvider (authEndpoint="/api/liveblocks-auth")
        │     └── RoomProvider (id={roomId})
        │           └── ClientSideSuspense (fallback=skeleton)
        │                 └── CollaborativeEditor
        │                       ├── BlockNoteView (editor)
        │                       ├── FloatingComposer (editor)
        │                       └── AnchoredThreads (editor, threads)
```

### Key packages (v3.17.0)

- `@liveblocks/client` — core client
- `@liveblocks/react` — hooks (`useThreads`, `useRoom`, `useOthers`, `useSelf`, `useHistoryVersions`, `useInboxNotifications`)
- `@liveblocks/react-blocknote` — `useCreateBlockNoteWithLiveblocks`, `FloatingComposer`, `AnchoredThreads`, `FloatingThreads`, `HistoryVersionPreview`
- `@liveblocks/react-ui` — `InboxNotification`, `InboxNotificationList`, comment UI
- `@liveblocks/node` — `Liveblocks`, `prepareSession`, `upsertRoom`, `WebhookHandler`
- `@liveblocks/node-prosemirror` — `withProsemirrorDocument` for server-side edits
- `@blocknote/core`, `@blocknote/mantine`, `@blocknote/react` — BlockNote editor

### Required CSS imports (ALL FOUR needed)

```tsx
import "@blocknote/core/fonts/inter.css";
import "@blocknote/mantine/style.css";
import "@liveblocks/react-ui/styles.css";
import "@liveblocks/react-blocknote/styles.css";
```

Missing `@liveblocks/react-blocknote/styles.css` causes thread marks, anchored threads, floating composer, cursor carets, and toolbar to be invisible.

### Room ID versioning

Room IDs follow the pattern `workspace:<version>:<slug>`. Version is in `WORKSPACE_LIVEBLOCKS_ROOM_VERSION` at `src/lib/workspace/liveblocks-room.ts`. Bump the version to force fresh rooms when seeding is broken (Liveblocks persists `hasContentSet: true` even on empty docs).

### Initial content seeding

Pass `initialContent` in the **second argument** (liveblocksOptions) of `useCreateBlockNoteWithLiveblocks`, NOT in blocknoteOptions. Content must be TipTap-compatible JSON:

```tsx
const editor = useCreateBlockNoteWithLiveblocks(
  {},                                          // blocknoteOptions — empty
  { initialContent: tiptapCompatibleJSON },    // liveblocksOptions — seed here
  [markdown],                                  // deps
);
```

### Auth constraints

- `/api/liveblocks-auth` requires Supabase session
- Do NOT pass `organizationId` to `prepareSession` — causes 403 on threads/comments
- Session grants `workspace:*` with `FULL_ACCESS`
- `upsertRoom` stores metadata (title, section, slug) when `TENANT_ORG_ID` is set

---

## Official Liveblocks API Reference

When implementing new features, fetch the official docs first:

- BlockNote integration: https://liveblocks.io/docs/api-reference/liveblocks-react-blocknote
- React hooks: https://liveblocks.io/docs/api-reference/liveblocks-react
- React UI components: https://liveblocks.io/docs/api-reference/liveblocks-react-ui
- Node.js SDK: https://liveblocks.io/docs/api-reference/liveblocks-node
- Node ProseMirror: https://liveblocks.io/docs/api-reference/liveblocks-node-prosemirror
- REST API: https://liveblocks.io/docs/api-reference/rest-api-endpoints
- Authentication: https://liveblocks.io/docs/authentication
- Webhooks: https://liveblocks.io/docs/platform/webhooks
- Comments: https://liveblocks.io/docs/ready-made-features/comments
- Notifications: https://liveblocks.io/docs/ready-made-features/notifications
- Text editor overview (BlockNote): https://liveblocks.io/docs/ready-made-features/multiplayer-editing/text-editor/blocknote

---

## Env vars

- `LIVEBLOCKS_SECRET_KEY` (optional) — Bearer token for API calls, auth, webhooks
- `LIVEBLOCKS_WEBHOOK_SECRET` (optional) — Webhook signature verification
- `TENANT_ORG_ID` (required for persistence) — UUID from `public.organizations`

---

## Common patterns

### Adding `resolveUsers` for mentions

```tsx
<LiveblocksProvider
  authEndpoint="/api/liveblocks-auth"
  resolveUsers={async ({ userIds }) => {
    // Fetch from your user API
    const res = await fetch(`/api/users?ids=${userIds.join(",")}`);
    return res.json();
  }}
  resolveMentionSuggestions={async ({ text, roomId }) => {
    // Return user IDs or mention objects matching search text
    const res = await fetch(`/api/users/search?q=${encodeURIComponent(text)}`);
    return res.json();
  }}
>
```

### Adding version history

```tsx
import { useHistoryVersions, HistoryVersionSummaryList, HistoryVersionSummary } from "@liveblocks/react";
import { HistoryVersionPreview } from "@liveblocks/react-blocknote";

// Inside RoomProvider context:
const { versions, isLoading } = useHistoryVersions();
// Render HistoryVersionSummaryList + HistoryVersionPreview
```

### Adding notifications

```tsx
import { useInboxNotifications } from "@liveblocks/react/suspense";
import { InboxNotification, InboxNotificationList } from "@liveblocks/react-ui";

const { inboxNotifications } = useInboxNotifications();
// Render InboxNotificationList with InboxNotification items
```

### Server-side document editing

```tsx
import { withProsemirrorDocument } from "@liveblocks/node-prosemirror";

await withProsemirrorDocument(
  { roomId: "workspace:2:section/doc", client: liveblocks },
  async (api) => {
    const text = api.getText();
    await api.update((doc, tr) => { /* modifications */ });
  }
);
```

### Adding FloatingThreads (mobile)

```tsx
import { FloatingThreads } from "@liveblocks/react-blocknote";

// Alongside AnchoredThreads:
<FloatingThreads editor={editor} threads={threads} />
```

---

## Troubleshooting checklist

1. **Content invisible?** Check all 4 CSS imports are present
2. **Empty editor / seeding broken?** Bump `WORKSPACE_LIVEBLOCKS_ROOM_VERSION` or delete room in dashboard
3. **401 on connect?** User must be logged in (Supabase session required)
4. **503 on connect?** `LIVEBLOCKS_SECRET_KEY` not set in env
5. **403 on threads/comments?** Do NOT pass `organizationId` to `prepareSession`
6. **Webhook snapshots failing?** Verify `TENANT_ORG_ID` exists in `public.organizations`
7. **Console warning about initialContent?** Safe false positive — ignore
8. **Feature not showing?** Check `tenantConfig.features.collaborativeWorkspace === true`

---

## Rules

- **Never modify `@liveblocks/*` or `@blocknote/*` node_modules** — report version issues
- **Always read the internal doc** (`docs/internal/engineering/LIVEBLOCKS_BLOCKNOTE_WORKSPACE.md`) before making changes
- **Test room connectivity** after auth changes — a bad auth response breaks all collaboration
- **Do not add `organizationId` to JWT** — see auth constraints above
- **Use versioned room IDs** — never construct room IDs manually, use `workspaceRoomIdFromSlug()`
- **Run tests** after changes: `pnpm test:run -- workspace`
- **Follow the tenant config pattern** — feature flags in `tenant.config.ts`, not hardcoded booleans
