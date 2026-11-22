# static-suite-1746-c289f117 - STOP: static gates unreachable without release-orchestrator dispatch

## Status
END_BLOCKED (technical STOP). The mission (karte t-20261120-r28-perses-tempo-source-verwandt) asked to run ONLY the prescribed static release-suite gates on PR #1746's exact head c289f117 — via `gh workflow run pre-release-runtime-suite.yml --ref <branch>`. That workflow has NO `workflow_dispatch` trigger; it is `workflow_call` only. HTTP 422 confirmed. The static gates can only run through the release orchestrator `pre-release.yml` (Release Validation job, lines 672-687, calls the suite with `runtime: static`), which itself is `workflow_call` and fires only from the authenticated trusted-planner chain. That is release-owner scope with required release inputs; a lane may not dispatch it, and the mission forbids substituting a runtime-cell.

## Reality check
- Planning-remote verified before any action:
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Worktree remote guard: origin = https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80). Correct GitHub remote.
- PR #1746 head = c289f117211babd63fc616a234156cca9886ee81 (matches mission). Branch lane-0428-208-static-release-gate, draft=false, state=OPEN.
- PR-run 44983299350 (db 7194) = completed/SUCCESS at this head via ci.yml "PR Selected Core-less" path. Mission says do not rerun that run.
- develop 82825e95a6f (via origin). #1754 merged, cli-3 zsh-lücke closed in the Draft-Go cell.

## What was tried / measured
1. Read `pre-release-runtime-suite.yml` at develop: `on: workflow_call` (line 633). Inputs include `runtime` (static/docker/podman) and `gate` (Atomic gate from baseharbor-demo/tests/gate-resources.json) plus the full trusted-planner evidence-reuse envelope.
2. Attempted the mission's exact dispatch:
   `gh workflow run pre-release-runtime-suite.yml --repo mcpdev80/baseharbor --ref lane-0428-208-static-release-gate`
   Result: HTTP 422 — "Workflow does not have 'workflow_dispatch' trigger".
3. Mapped the call chain for the static gate:
   - `pre-release.yml` line 67: runs the runtime suite only when `EVENT_NAME == workflow_call` (authenticated caller, not raw user dispatch).
   - `pre-release.yml` lines 672-687 (Release Validation job): `uses: ./.github/workflows/pre-release-runtime-suite.yml` with `runtime: static`, `gate: ${{ matrix.gate }}`, `ref: ${{ needs.source.outputs.candidate_sha }}`, plus the full evidence-reuse envelope.
   - `release.yml` lines 142/145: `workflow_dispatch`/`push` on tags `v*`, with a **required** `tag` input (release-owner scope).
   - `supplemental-release-validation.yml`: does not call the runtime suite at all (checkout + go test only).
4. Confirmed 44983299350 executed ZERO static jobs: no job whose name matches 'static'/'Static' (the run ran only docker/podman coreless-lifecycle; `PR · Selected Runtime` and `PR · Exact full Pre-Release` were skipped).

## Why this is a STOP, not a fix
- The prescribed command cannot run: `pre-release-runtime-suite.yml` has no `workflow_dispatch` trigger (HTTP 422). There is no `-f <inputs that select only the static cells>` that makes a non-dispatchable workflow dispatch.
- The only path to the static gates is the release orchestrator `pre-release.yml` (or `release.yml`), both of which require the trusted-planner `workflow_call` / a release `tag` input. Setting up such a dispatch would mean authorizing a release-orchestrator run with release-owner inputs — outside a lane's write-set and authorization, and the mission forbids standing up a runtime-cell as a substitute.
- No file was changed. No workflow was dispatched. No run was started. PR #1746 untouched.

## What a resolution requires (report, do not execute)
- To prove the static gates green on c289f117, the static path must be run through the release orchestrator (`pre-release.yml` Release Validation with `runtime: static`, or `release.yml` with a real `tag`), i.e. release-owner scope with the trusted planner inputs. This is a coordinator/Owner action (shared release-orchestrator control flow). Reported here with file:line; not executed.

## End
- New head: c289f117211babd63fc616a234156cca9886ee81 (already on #1746; no hop performed this turn).
- Run: none started. PR-run 44983299350 left as-is (completed/success, ci.yml coreless path; zero static jobs).
- Failed jobs: n/a (no run started).
- Static gates: NOT executed; unreachable from a lane without the release-orchestrator `workflow_call` (release-owner scope). Reported with file:line, not fixed.
- Cleanliness: nothing started (no containers/compose/docker/podman launched). No .github/** edited. No dispatch attempted beyond the one confirming HTTP 422.
