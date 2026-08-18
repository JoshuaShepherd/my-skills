# STATE and sign-off

## Where state lives

```
docs/audit/routes/
  STATE.md            # human-readable narrative + the table below
  state.json          # machine-readable, the actual source of truth
  evidence/
    2-themes/
      themes-apest.png
      themes-apest.console.txt
```

The package on disk is the source of truth, **not the chat window**. A fresh Cursor window opens
`docs/audit/routes/STATE.md` and resumes exactly where the last one stopped. This is the only reason
the audit survives a context reset.

## The six route states

| State | Meaning | How it is reached |
|---|---|---|
| `untested` | In the manifest, never walked | Default on manifest entry |
| `walked` | Evidence captured, not yet judged | End of a walk phase |
| `failed` | One or more assertions or `must_not` rules violated | Triage |
| `fixed_pending_verify` | Source changed, spec written, not yet verified in a later turn | Repair |
| `signed_off` | Committed spec passes on the current SHA | Sign-off gate |
| `deferred` | Knowingly out of scope, with a written reason and an owner | Explicit human decision |

There is no `probably_fine`. If it is not `signed_off`, it is not done.

## `state.json`

```json
{
  "base_url": "http://localhost:5173",
  "commit": "a1c9f2e",
  "updated_at": "2026-08-07T14:22:00Z",
  "phases": {
    "2-themes": {
      "status": "in_progress",
      "spec": "e2e/routes/2-themes.spec.ts",
      "routes": {
        "/themes": {
          "state": "signed_off",
          "verified_at": "2026-08-07T14:20:11Z",
          "verified_commit": "a1c9f2e"
        },
        "/themes/apest": {
          "state": "fixed_pending_verify",
          "failures": [
            "cases section rendered 1 card, manifest requires min_count 2",
            "console.error: Warning: Text content did not match. Server: \"\" Client: \"3 cases\""
          ],
          "root_cause": "PathwayCases falls back to single-card render when cases array length < 2",
          "fix_commit": "a1c9f2e"
        },
        "/themes/communitas": {
          "state": "failed",
          "failures": ["[data-section=\"ai-lab\"] absent"],
          "root_cause": null
        }
      },
      "observed_not_fixed": [
        "Theme hero images are 1200px unoptimised across the zone — separate ticket, not this audit"
      ]
    }
  }
}
```

## The sign-off gates

A route may move to `signed_off` only when **all five** hold:

1. A spec file exists at `e2e/routes/<phase>.spec.ts` containing assertions for this route.
2. That spec is **committed** to git.
3. `npx playwright test e2e/routes/<phase>.spec.ts` passed, with the output recorded.
4. The pass happened on the **current** SHA, recorded as `verified_commit`.
5. The verification happened in a **later turn** than the fix.

Gate 5 is the one that will feel like bureaucracy and is the one that matters. An agent that fixes and
verifies in the same breath is pattern-matching on its own intention rather than reading a result. The
separation forces it to look at real test output.

A phase closes when every route in it is `signed_off` or `deferred` with a reason.

## Rerun semantics

On re-entry:

1. Read `state.json`. Read the current SHA.
2. Regenerate the mechanical half of the manifest; diff against the previous.
   - New route in the router → add as `untested`, note it as a finding if it is absent from the spec docs.
   - Route removed → mark `deferred` with reason `route removed at <sha>`; delete its assertions.
3. Run the full existing suite: `npx playwright test e2e/routes/`.
   - Any previously `signed_off` route whose spec now fails drops to `failed`. **Prior sign-off confers
     nothing.** This is the point of the ratchet.
4. Report: signed off / failed / untested / deferred counts, then the failed list with evidence.
5. Resume at the earliest phase that is not closed.

## STATE.md

Keep the narrative short and current — three sections is enough:

```markdown
# Route Audit — STATE

**Base URL:** http://localhost:5173 · **Commit:** a1c9f2e · **Updated:** 2026-08-07

## Where we are
Phase 2 (themes) in progress. Phases 1 closed. 14 of 61 routes signed off.

## Open failures
- `/themes/communitas` — ai-lab section absent. Root cause unknown; suspect the pathway content
  record has no bound lab. Needs a data check, not a component fix.

## Observed, not fixed
- Theme hero images unoptimised across the zone. Separate ticket.
```

Do not let STATE.md grow into a log. `state.json` holds the detail; `evidence/` holds the proof;
STATE.md holds only what a person needs to pick this up cold.
