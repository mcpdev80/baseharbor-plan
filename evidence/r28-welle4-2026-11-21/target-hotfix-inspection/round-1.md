# 0428-220 hottarget: target-hotfix-inspection-config-missing

ROLE: Worker. CARD: t-20261121-target-hotfix-inspection-config-missing (0428-220).
BRANCH: lane-0428-220-hottarget. PR: one new PR against develop.

## PLAN

1. Reality check: ls-remote develop, plan.py show, no foreign PR
2. Reproduce remotely via PR, capture failing error line
3. Fix hotfix path to use configured target record
4. Regression: configured-target OK + unknown-target fail-closed
5. Evidence at END SHA: ancestry, files, single author
6. Write evidence file + cleanliness + END post

## Reality check (witnessed)

- Planning repo remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified BEFORE first evidence commit).
- develop HEAD via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`.
- `python3 scripts/plan.py show t-20261121-target-hotfix-inspection-config-missing`: state=ready, depends on t-20261121-all-targets-config-loss (accepted). Card schema still `kanban_status: planned`, `resolution:` empty, but `superseded_by: t-20261120-cli-operator-entrypoints` and the note ends with `owner-entscheidung: basis-inhalt neu landen oder karte erneut schneiden`.
- `gh pr list --repo mcpdev80/baseharbor --search "0428-220"`: no PR yet (no foreign PR owns this card).
- Worktree cut from develop at e6c199e7b7dd (base SHA attested above); git identity `0428-220-hottarget <0428-220@baseharbor.local>`.

## Reproduction (local, on current base e6c199e7b7dd)

- Test `TestTargetInspectionProjectsBuiltInAccessCapabilities` PASSES on current develop:
  `go test ./cmd/baha/ -count=1 -run TestTargetInspectionProjectsBuiltInAccessCapabilities -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` => `ok github.com/mcpdev80/baseharbor/cmd/baha 0.048s`.
- Fail-closed still holds: unknown target `never-configured` returns `"target \"never-configured\" is not configured"` (test `TestReproUnknownTargetFailsClosed`, removed after run).
- Root cause of the ORIGINAL CI failure: the test originally ran `t.Setenv("BASEHARBOR_TARGET", "edge-a")` BEFORE `createTarget(...)`, so `effectiveTarget` selected `edge-a` while it was unregistered -> `ResolveTarget` returned "is not configured". Fix `46017060d` ("test(0428-198): register target before selecting it", author Marcel, 2026-11-21 05:43) flips the order (register-then-select) and lives in PR #1726 head, NOT in develop.
- `46017060d` NOT ancestor of develop (`git merge-base --is-ancestor 46017060d develop` => NO). develop's `target_hotfix_test.go` already has the corrected order and passes.

## Root-cause comparison with 0428-210 (#1739)

- 0428-210 (#1739, `79d962a063be`): PRODUCT fix in `cmd/baha/app_commands.go` -- tolerates `deployment.ErrConfigMissing` in the `--all-targets` inventory AFTER the operator-auth gate (the only place ErrConfigMissing is tolerated on that read path). NOT in develop.
- 0428-220 (this card): the failing line was `target_hotfix_test.go` test-ordering, NOT `deployment.ErrConfigMissing` on the inspection read path. `collectTargetInspection` -> `effectiveTarget` -> `ResolveTarget` behaves correctly: returns configured target when registered, fails closed when not.
- => NO shared root cause. Different mechanism (test ordering vs ErrConfigMissing tolerance), different files.

## Querbehauptung (cross-reference 0428-223)

- 0428-223 class: `umgebung`, message `target "<name>" is not configured`, root since `80961866f`.
- This card's mechanism is a TEST-ORDERING artifact, not a `deployment.ErrConfigMissing` resolution bug, and does not reproduce on develop. It does NOT repair the 0428-223 `umgebung` class.
- clears 0428-223 class: nein -- different failure class (test setup), no product change to the resolution path; the 0428-223 root is a separate class:umgebung case.

## Acceptance-criteria disposition (diagnostic step)

Acceptance requires: state whether 0428-210 and this card share one root cause; if no, deliver the fix here.
- Shared root cause: NO.
- Fix deliverable: the inspected product path already behaves correctly on the current base (configured target returned; unknown target fails closed). The only defect was a test-ordering artifact fixed upstream in PR #1726 (`46017060d`), which the mission forbids making a pure test-only change.
- => The failure is already resolved on develop. No product write-set change is required. A PR here would only carry a redundant test-ordering revert/forward.

## Scope decision

- Mission forbids parking in an interactive dialog. Posted a QUESTION to the coordinator (session 9142ab1f) asking: (A) card already resolved on develop -> close as already-resolved, no PR; or (B) deliver product hardening on the hotfix path seeding configured target into resolution.
- Awaiting owner call before any PR. No product files written. Worktree clean.

## Repo-rule compliance

- Write-set touched: NONE (no product change). Only read-only investigation + one temporary repro test (removed).
- TABU untouched: `.github/**`, `scripts/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go`.
- No bare `go test ./...` or `go test ./cmd/baha/` on this host. Targeted `-run` with the required skip of RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication.
- No subagents. No second branch. No merge. No `.github` edit. No workflow_dispatch/rerun.

## Cleanliness

- `docker ps -a --filter name=bh-` before: (no docker test run)
- `docker ps -a --filter name=bh-` after: (no docker test run)
- `git worktree list`: lane-0428-220-hottarget-wt at e6c199e7b7dd (develop), clean.
- No test-owned containers/networks/volumes/state left behind. Host at ~97% disk; tmpfs /tmp full -> used private TMPDIR under the worktree (removed).

## Status

- BLOCKED on owner scope decision. No PR opened. No product change.
