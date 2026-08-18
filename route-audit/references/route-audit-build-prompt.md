# Route Audit — Build Prompt

*Paste this whole file into a fresh Cursor or Claude Code window opened at the root of
`movementalai-studio` (ZenWrite / Studio). It stands up the rerunnable route-audit system once.
After that, the `route-audit` skill's own prompts take over and this file is never needed again.*

---

## Runner — how you work

**The Runner governs how; the Phases govern what.** Read this section fully before Phase 0.

**Self-persisting package.** On kickoff, save this prompt verbatim to
`docs/build/prompts/route-audit/PROMPT.md` and create `docs/build/prompts/route-audit/STATE.md`
beside it. Update STATE.md at every phase boundary. The package on disk is the source of truth — not
this chat window. A brand-new window must be able to open that directory and resume exactly.

**Re-entry.** If `docs/build/prompts/route-audit/STATE.md` already exists when you start, read it,
report where the build stopped, and resume at the first incomplete phase. Do not restart.

**The loop, per phase.** Read the phase → do only what it says → verify against its Done-when gate
with real evidence → write a checkpoint report → **stop and wait for me**. No silent multi-phase runs.

**Checkpoint report format.**
```
PHASE <n> — <name>
Done-when evidence: <the actual command output / file diff / count>
Files touched: <list>
Deviations from the plan: <or "none">
Next: PHASE <n+1> — awaiting your go
```

**Prime directives.**
- Ground everything in the real repo. If a fact here is marked *verify-before-use*, verify it and
  report what you actually found before building on it. Guessed structure is the top cause of these
  builds failing.
- Never invent a route, a selector, or a fixture slug. If you cannot confirm it exists, say so.
- Reversible over clever. No destructive git operations, no rewriting existing e2e infrastructure.
- Note adjacent problems in STATE.md under "Observed, not fixed". Do not wander off to fix them.

**Failure protocol.** If a phase cannot complete — a tool is missing, a fact contradicts this prompt,
the router is not where I said — stop, report exactly what you found, and propose the smallest
correction. Do not improvise around a broken assumption.

---

## Decisions already locked — do not re-litigate

1. **Chrome DevTools MCP diagnoses; Playwright certifies.** DevTools sessions are for finding out
   *why* something is broken. The pass/fail signal is always a committed Playwright spec. No route is
   ever marked signed off on the strength of an agent having looked at it.
2. **Attach to a signed-in Chrome** via `--browserUrl` and a dedicated `--user-data-dir`. Do not
   script login. Do not launch a clean browser for authenticated routes.
3. **`routes.manifest.yaml` is a contract.** Mechanical fields regenerate; `must_render` / `must_not`
   / `notes` are human-authored and never overwritten by tooling, and never edited to make a failure
   disappear.
4. **Phases of 12–15 routes**, fresh agent window each. Accessibility-tree snapshots are large; a
   window carrying three phases starts summarising instead of checking.
5. **Reuse the existing `e2e/` Playwright setup.** Do not create a second Playwright config or a
   second auth harness.
6. **State lives at `docs/audit/routes/`** — `state.json` (authoritative), `STATE.md` (human),
   `evidence/` (screenshots and console dumps).
7. **The skill is canonical in `my-skills/route-audit/`** and symlinked into this repo. Never copy it
   in.

**Testing-last is inverted here, deliberately.** The usual rule defers tests to the end. This build's
*product* is a test suite, so specs appear from Phase 4 onward. What still defers to the end: type
tightening, CI wiring, and any refactor of existing e2e infrastructure. Do not touch those until
Phase 7.

---

## Verified vs assumed facts

| Fact | Status |
|---|---|
| Repo is Vite + React with an Express server under `server/` | **verify** — confirm from `package.json` and `server/app.ts` |
| Routes are declared in React Router config (likely `src/App.tsx` or a routes module), **not** a filesystem convention | **verify first — Phase 1 depends entirely on this** |
| Playwright e2e assets already exist under `e2e/` (e.g. `e2e/api/route-coverage.spec.ts`) | **verify** — read the existing config and auth setup before adding anything |
| `my-skills` is symlinked into every repo in this workspace | **verify** — `ls -la .claude/skills` before installing |
| Dev server port | **verify** — read from `vite.config.*`; do not assume 5173 |

Report all five at the Phase 0 checkpoint. If any is wrong, stop.

---

## PHASE 0 — Preflight and grounding

**Goal.** Know the real repo before changing it.

**Steps.**
1. Save this prompt to `docs/build/prompts/route-audit/PROMPT.md`; create `STATE.md`.
2. Confirm each row of the facts table above with a command and its output.
3. Locate the router source. Show me the actual route declarations, not a summary.
4. Read the existing `e2e/` setup: Playwright config, any auth/storage-state helper, how tests are run.
5. Check `npx playwright --version` and whether Chromium is installed.

**Done-when.** All five facts reported with evidence; router file path and route count stated; existing
Playwright config quoted.

**Do NOT yet.** Write any code. Install anything. Create the manifest.

---

## PHASE 1 — Install the skill

**Goal.** `route-audit` available to both Cursor and Claude Code in this repo.

**Steps.**
1. Confirm `my-skills` location and existing link style.
2. If the library is already linked wholesale, confirm `route-audit` resolves and do nothing further.
3. Otherwise run `my-skills/route-audit/scripts/install.sh <repo>`.
4. Ensure `.gitignore` covers `.claude/skills/` and `.cursor/skills/`.

**Done-when.** `ls -la .claude/skills/route-audit/SKILL.md` and `.cursor/skills/route-audit/SKILL.md`
both resolve.

**Do NOT yet.** Commit anything into the repo other than the `.gitignore` line.

---

## PHASE 2 — Chrome DevTools MCP

**Goal.** The agent can drive a signed-in browser.

**Steps.**
1. Add the `chrome-devtools` server to `.cursor/mcp.json` (and `.mcp.json` if Claude Code is used)
   per `references/setup-and-install.md`. **Verify the current flag and tool names against the
   package README first** — this surface has changed across releases; report any difference.
2. Give me the exact Chrome launch command for this machine. **I** launch it and sign in — you do not.
3. Once I confirm, verify: `curl -s http://127.0.0.1:9222/json/version`, then `navigate_page` to an
   authenticated route and snapshot to prove the session is live.

**Done-when.** A snapshot of an authenticated route showing signed-in content, not the login page.

**Do NOT yet.** Walk any other route.

---

## PHASE 3 — The manifest

**Goal.** `routes.manifest.yaml` exists with every real route and correct phase grouping.

**Steps.**
1. `npm i -D yaml` if absent.
2. Run `scripts/build-route-manifest.mjs` against the router source found in Phase 0.
3. Review its output against the router declarations by hand. Report any route the regex missed —
   the generator is a fast enumerator, not a proof of completeness, and this review is what makes it
   trustworthy.
4. Replace every `REPLACE-ME` fixture with a real, seeded URL. If you cannot confirm the fixture data
   exists in the dev database, mark it and tell me — do not invent a slug.
5. Propose the phase grouping as a table.

**Done-when.** Manifest committed; route count matches the router; zero `REPLACE-ME` fixtures remain
unflagged; phase table shown to me and agreed.

**Do NOT yet.** Author `must_render` assertions. That is per-phase work under the skill's PROMPT 1.

---

## PHASE 4 — Assertions and specs for phase `1-public` only

**Goal.** Prove the whole pipeline end to end on one small phase before scaling it.

**Steps.**
1. Author `must_render` / `must_not` for the routes in `1-public`, using the repo's own page spec
   docs as the authority for what each page should contain.
2. Run `scripts/gen-route-specs.mjs --phase 1-public`.
3. **Read every generated assertion.** Fix ambiguous selectors. If a route has no stable hooks, add
   `data-section` attributes to the components and update the manifest.
4. Run the spec. Expect failures — that is the system working.

**Done-when.** `e2e/routes/1-public.spec.ts` exists, runs, and produces a real pass/fail list you can
show me. Not "all green" — *real*.

**Do NOT yet.** Fix any application code. Walk any other phase.

---

## PHASE 5 — Scaffold state

**Goal.** The audit is resumable.

**Steps.** Create `docs/audit/routes/` with `state.json` (every route `untested` except the
`1-public` results from Phase 4), `STATE.md`, and an empty `evidence/`. Follow the schema in
`references/state-and-signoff.md` exactly.

**Done-when.** `state.json` validates as JSON and its route list matches the manifest exactly.

---

## PHASE 6 — First real phase, driven by the skill

**Goal.** Prove the skill's own prompts work without this build prompt.

**Steps.** Open a **fresh window**. Run the skill's PROMPT 2 (walk) for phase `1-public`, then
PROMPT 3 (triage), PROMPT 4 (repair), and — in a later turn — PROMPT 5 (sign-off).

**Done-when.** Phase `1-public` is closed in `state.json`: every route `signed_off` or `deferred`
with a reason, each with a `verified_commit`, and the raw passing test output recorded.

**Do NOT yet.** Run the remaining phases. Wire CI.

---

## PHASE 7 — Hardening (only now)

**Goal.** Make it durable.

**Steps.**
1. Add `npm run audit:routes` → `playwright test e2e/routes/`.
2. Wire into CI as a **non-blocking** job first, for at least one week. A brand-new suite that blocks
   merges on day one will be disabled by day three, and then you have nothing.
3. Tighten script types; handle the missing-manifest and malformed-YAML cases.
4. Write `docs/audit/routes/README.md`: how to rerun, how to add a route, how to read STATE.

**Done-when.** `npm run audit:routes` passes locally and in CI; README exists.

---

## Appendix — things that will bite

- **Stale debugging port.** Produces an entire phase of confident, meaningless failures. Preflight
  every session.
- **Dynamic-route fixtures.** Unseeded slugs give false 404s. Pin them and record their source.
- **Ambient console noise.** `must_not: console_errors` is the highest-value assertion in the file.
  Do not blanket-exempt it. Fix the noise, or scope an ignore narrowly with a written reason.
- **Signed-out flash.** A route that redirects but paints protected content for 400ms has leaked.
  Only the signed-out pass (skill PROMPT 6) catches it. Treat any hit as a security finding.
- **Manifest editing to force green.** The single move that would make this entire system worthless.
  If an assertion is wrong, escalate it to me as a manifest bug; do not silently relax it.
