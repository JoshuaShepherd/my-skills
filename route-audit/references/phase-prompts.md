# The prompts

These are the reproducible part of the skill. Use them verbatim; substitute only the bracketed values.
Improvised prompts produce a different audit every time, which is the same as no audit.

Each prompt is self-contained — paste into a **fresh** Cursor or Claude Code window inside the repo.
Freshness is deliberate: snapshots are large, and a window carrying three phases of accessibility trees
starts summarising instead of checking.

---

## PROMPT 0 — Bootstrap (once per repo)

```
You are setting up a rerunnable route audit for this repo. Use the `route-audit` skill.

Do these in order and stop at the checkpoint.

1. PREFLIGHT. Run the five preflight checks from references/setup-and-install.md. Report each as
   pass/fail with the actual output. If any fail, stop and tell me — do not proceed.

2. FIND THE ROUTER. Locate where routes are actually declared. This is a Vite + React app, so it is
   a React Router configuration, not a filesystem convention — check src/App.tsx and any routes
   module. Also note the Express API routes under server/routes/. Report the file paths you found
   and how many UI routes are declared. Do not guess; show me the declarations.

3. GENERATE THE MECHANICAL MANIFEST. Run scripts/build-route-manifest.mjs against that source.
   It writes routes.manifest.yaml with path / fixtures / auth / phase filled and must_render empty.
   Report the route count and the phase grouping it chose.

4. ASSIGN PHASES. Group the routes into zones of 12–15. Propose the grouping to me as a table
   (phase, route count, routes). Do not proceed past this without my agreement.

CHECKPOINT — stop here and show me: preflight results, router source, route count, proposed phases.
```

---

## PROMPT 1 — Author the assertions (once per phase, before its first walk)

```
Use the `route-audit` skill. We are authoring assertions for phase [PHASE-ID] of
routes.manifest.yaml.

For each route in this phase:

1. Find what the page is SUPPOSED to contain. Sources, in order of authority:
   - the repo's own page/component spec docs (search docs/ for the page name)
   - the component tree the route actually renders
   If a spec doc exists, it wins — the audit measures the code against the spec, not against itself.

2. Write must_render entries for the REQUIRED components only. Prefer stable selectors
   ([data-section="..."], data-testid) over visible text. Where no stable hook exists, note it in
   `notes` as "needs data-section attribute" — we will add it during repair, not now.

3. Write must_not entries. Every route gets console_errors and network_failures. Add text
   assertions for placeholder content you know this codebase leaves behind.

4. For parameterised routes, give me at least two real fixture URLs and tell me where the fixture
   data comes from. If you cannot confirm the fixture exists in the dev database, say so — do not
   invent a slug.

Edit routes.manifest.yaml in place. Do NOT touch must_render entries for routes outside this phase.

CHECKPOINT — show me the diff of routes.manifest.yaml and flag any route where you were unsure what
the page is supposed to contain.
```

---

## PROMPT 2 — The walk (per phase, fresh window)

```
Use the `route-audit` skill. Walk phase [PHASE-ID].

PREFLIGHT first — all five checks, reported with real output. Record the base URL and git SHA.

Then, for EVERY route and fixture in phase [PHASE-ID] of routes.manifest.yaml, in order, using
Chrome DevTools MCP against the already-signed-in browser:

  a. navigate_page to the fixture URL
  b. take_snapshot
  c. list_console_messages — record every error and warning VERBATIM
  d. list_network_requests — record every request with status >= 400, with its URL and status
  e. check each must_render entry against the snapshot; record present / absent / wrong count
  f. check each must_not entry
  g. take_screenshot → docs/audit/routes/evidence/[PHASE-ID]/<route-slug>.png

RULES — these are not optional:
- FIX NOTHING. Not a typo, not an import, not a className. This phase captures evidence only.
  Fixing mid-walk invalidates the routes already walked and destroys the cross-route pattern.
- Record actual text, not summaries. "console.error: Warning: Text content did not match..." —
  not "hydration warning present".
- If a route will not load at all, record that and move on. Do not investigate yet.
- If you find yourself compressing findings to save context, STOP and tell me the phase is too
  large. Do not silently degrade.

Write everything to docs/audit/routes/state.json — every route in this phase moves to `walked`,
with its failures listed. Update STATE.md.

CHECKPOINT — report a table: route | must_render pass/fail | console errors | network failures.
Then stop. Do not triage in this turn.
```

---

## PROMPT 3 — Triage (fresh window, after the walk)

```
Use the `route-audit` skill. Triage phase [PHASE-ID].

Read docs/audit/routes/state.json. Do not re-walk anything — work from the recorded evidence.

1. CLUSTER the failures by suspected root cause. For each cluster give me:
   - the cluster name in one line
   - which routes it explains
   - the ONE file you believe is responsible, with the specific lines
   - your confidence, and what would confirm it

2. Look for the pattern I care about most: several routes failing for one reason. If every failure
   looks unique, say so plainly — but check first whether they share a component, a data shape, or
   a layout wrapper.

3. Separate genuine failures from manifest errors. If a must_render entry asserts something the
   page was never supposed to have, that is a manifest bug — flag it for MY decision. Do NOT edit
   the manifest to make a failure disappear. That is the one move that would make this whole
   system worthless.

4. List anything you noticed that is real but out of scope, under `observed_not_fixed`.

Write the clusters and root causes into state.json.

CHECKPOINT — show me the clusters ranked by how many routes each explains. Recommend a fix order.
Do not write any fix code in this turn.
```

---

## PROMPT 4 — Repair and ratchet (per cluster)

```
Use the `route-audit` skill. Fix cluster "[CLUSTER-NAME]" from phase [PHASE-ID].

1. FIX THE SOURCE. Address the root cause, not each symptom. If the honest fix is larger than this
   audit's scope, say so and propose the smaller safe fix plus a ticket — do not quietly do the
   large refactor inside an audit.

2. ADD THE MISSING HOOKS. If routes in this cluster lack stable selectors, add data-section
   attributes now so the assertions can be structural. Update routes.manifest.yaml accordingly.

3. WRITE THE SPEC. Generate or extend e2e/routes/[PHASE-ID].spec.ts via
   scripts/gen-route-specs.mjs, then hand-check it. One assertion per must_render entry, plus a
   console-error listener and a response listener for status >= 400. Reuse the existing e2e/ setup
   and auth harness — do not stand up a second Playwright configuration.

4. The spec is the deliverable. The source fix without a spec is a fix that will be undone by
   someone in three weeks and nobody will notice.

5. Mark each affected route `fixed_pending_verify` in state.json with the fix commit. Do NOT mark
   anything signed_off in this turn — verification happens in a later turn, from real test output.

CHECKPOINT — show me the source diff, the spec diff, and the updated state entries.
```

---

## PROMPT 5 — Sign-off (fresh window, later turn)

```
Use the `route-audit` skill. Sign off phase [PHASE-ID].

1. Confirm the working tree is clean and record the SHA.
2. Run: npx playwright test e2e/routes/[PHASE-ID].spec.ts
   Paste the REAL output. Do not paraphrase it, do not report a result you did not see.
3. For each route, check the five sign-off gates in references/state-and-signoff.md. A route moves
   to signed_off only if all five hold — including gate 5, that the fix landed in an earlier turn
   than this verification.
4. Any route still red drops to `failed` with the new evidence. Go back to PROMPT 3 for those.
5. Update state.json and STATE.md. Close the phase only if every route is signed_off or deferred
   with a written reason and an owner.

CHECKPOINT — report signed off / failed / deferred counts for the phase, the SHA, and the raw test
output. If you are tempted to sign off a route on the strength of having looked at it, don't — say
what is missing instead.
```

---

## PROMPT 6 — Signed-out pass (after all authenticated phases close)

```
Use the `route-audit` skill. Run the signed-out pass (phase `auth`).

Open a fresh browser context with NO session — a clean profile or incognito, not the audit profile.

For every route in routes.manifest.yaml:
- auth: public → must render normally. Same must_render assertions apply.
- auth: required or admin → must redirect cleanly to the login route. Assert: final URL is the
  login route, no 5xx, and NO protected content flashes before the redirect (check the snapshot
  immediately after navigation, and check console/network for authenticated API calls that fired
  anyway).

The flash-of-protected-content case is the reason this pass exists. A route that redirects but
renders the dashboard for 400ms has leaked. Look for it specifically.

Write assertions into e2e/routes/auth.spec.ts — separate file, the assertions are different.
Then run PROMPT 5 against phase `auth`.

CHECKPOINT — report any route that renders protected content while signed out as a SECURITY
finding, at the top, separately from ordinary failures.
```

---

## PROMPT 7 — Rerun (the steady state)

```
Use the `route-audit` skill. Re-run the route audit.

1. Preflight. Record base URL and SHA.
2. Regenerate the mechanical half of routes.manifest.yaml. Diff against committed.
   - New routes → add as untested; flag any that are absent from the spec docs as a finding.
   - Removed routes → mark deferred with reason, drop their assertions.
3. Run the whole suite: npx playwright test e2e/routes/
4. Any previously signed_off route that now fails drops to `failed`. Prior sign-off confers
   nothing — that is the point.
5. Report: signed off / failed / untested / deferred, then each failure with its evidence.
6. Only the failed routes get a DevTools session. Do NOT re-walk green routes; that is the cost
   this whole system exists to avoid.

CHECKPOINT — the counts, the failure list, and a recommended next phase to work.
```

---

## A note on running these unattended

Every prompt ends at a checkpoint on purpose. A nine-phase autonomous run produces a large diff, a
confident summary, and no way to tell which parts were actually verified. If the user explicitly asks
for an unattended run, say plainly what they are giving up — and still hold PROMPT 5's gate 5, because
a self-verifying loop with no turn boundary is exactly the failure mode this design exists to prevent.
