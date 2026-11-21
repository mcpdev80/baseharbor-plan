# 0428-218 r2 — exact operator-auth denial message pinned in MCP seam test

ROLLE: WORKER. CARD: t-20261121-mcp-operator-seam-uncovered (0428-218). PR: #1741.
CORREKTURRUNDE nach CODEX-REVIEW `evidence/r28-welle4-2026-11-21/mcp-operator-seam/review-1.md` (Verdikt: REQUEST CHANGES, plan 9ac0a0cd + 577bd6a8).

## PLAN

- Read mission /218 and review-1 verdict; record numbered plan in live board + this evidence.
- Resolve remotes, base head drift, ancestry; set own git identity in tree.
- Patch `cmd/baha/mcp_operator_seam_test.go`: decode `error.Message`, assert exact gate text on anonymous prod request; keep existing assertions.
- Mutation proof in an in-akter throwaway tree: wrong product text = RED, restored text = GREEN.
- Local verify: go vet + build + named `go test` run (skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication).
- Basis-nachzug: measure base head, merge-base-is-ancestor, rev-list count, diff --name-only.
- Commit + push to lane-0428-218; prove delivery with ls-remote; run ci-fast-check.sh; wait PR Selected Checks.
- Commit evidence to baseharbor-plan origin/main; verify path present; docker ps -a cleanliness.

## Remote witnesses (measured now)

- lane-0428-218-mcp-operator-seam: `de4a45ec5ca6e5c064d991420c796162ee6c1494` (pre-fix candidate head) — `git ls-remote lane-origin refs/heads/lane-0428-218-mcp-operator-seam`.
- base lane-0428-198-cli-shard-operator-env: `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` — `git ls-remote lane-origin refs/heads/lane-0428-198-cli-shard-operator-env`.
- PR #1741 head after fix: `fb5a5deaf36ba160b527019a3ef4eea85060905d` (PR auto-retargeted from base lane head to my candidate lane) — `gh pr view 1741 --repo mcpdev80/baseharbor`.
- PR base: lane-0428-198-cli-shard-operator-env, draft=false, state=OPEN, mergeStateStatus=UNSTABLE.
- Remote URL resolved: lane-origin -> https://github.com/mcpdev80/baseharbor.git (never pushed through a name without this URL).

## Basis-nachzug (tooling-issue #24)

- Base head measured now: `e45430f2f1b7` — NO drift since review-1.
- merge-base-is-ancestor before fix: `git merge-base --is-ancestor origin/lane-0428-198-cli-shard-operator-env HEAD` returned 0 (base IS ancestor).
- `git rev-list --count origin/lane-0428-198-cli-shard-operator-env..HEAD` = 1 (single candidate commit).
- `git diff --name-only origin/lane-0428-198-cli-shard-operator-env..HEAD` = `cmd/baha/mcp_operator_seam_test.go` only.
- After rebase/commit: head `fb5a5deaf`; `git log --oneline origin/lane-0428-198-cli-shard-operator-env..HEAD` lists only my own commit `fb5a5deaf test(0428-218): pin exact operator-auth denial message in MCP seam test`.
- Identity in tree: `git config user.name "0428-218-msgassert"` / `user.email "0428-218-msgassert@baseharbor.local"`; `git log -1 --format=%an` before commit = `0428-218-msgassert`.

## Fix (reviewer Finding 1 recipe)

`cmd/baha/mcp_operator_seam_test.go` decoded payload shape extended:

```go
var payload struct {
    Error *struct {
        Code    string `json:"code"`
        Message string `json:"message"`
    } `json:"error"`
}
...
if payload.Error.Message != "Managed-environment machine operations require an authenticated BaseHarbor operator." {
    t.Fatalf("anonymous denial does not carry the exact production gate message: %q", payload.Error.Message)
}
```

Exact gate text source: `internal/operatorauth/authorization.go:286` (`decision.Reason`) and `cmd/baha/mcp.go:301` (`machine.Error.Message`) — both `"Managed-environment machine operations require an authenticated BaseHarbor operator."`.

Existing assertions kept unchanged: stamped managed `target.create` succeeds; anonymous managed `target.create` is an MCP machine error; outputs differ; `error.code == "authentication_failed"`; `operatorauth.PrincipalFromContext(anonymous)` is absent (missing principal). The case still tips both directions.

## Mutation proof (reviewer test requirement: case MUST go RED on product-text change)

Throwaway worktree `/tmp/w0428-218-mcp-mutant` (branch head de4a45ec5), fixed test copied in, product text mutated then restored — no product commit, no push, removed after.

- GOVERNED run correct text: `go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run 'TestMCPOperatorSeamReachesGateBothDirections'` -> `ok` (exit 0).
- Mutant A — product text changed at `cmd/baha/mcp.go:302` to `"...authenticated BaseHarbor operator (mutated text)."`:
  `go test ... -run 'TestMCPOperatorSeamReachesGateBothDirections'` ->
  `--- FAIL: TestMCPOperatorSeamReachesGateBothDirections` / `mcp_operator_seam_test.go:95: anonymous denial does not carry the exact production gate message: "Managed-environment machine operations require an authenticated BaseHarbor operator (mutated text)."` / `FAIL` (exit 1 = RED, as required).
- Mutant B — text restored to production value:
  same named run -> `ok` (exit 0 = GREEN). The case is sensitive: RED on change, GREEN on restore. A case that stayed green in both st would have been a pointless pass.

## Hosted CI evidence (run 44882418434, head fb5a5deaf, PR · PR #1741)

- Aggregate `PR Selected Checks` / run 44882418434: terminal status COMPLETED, conclusion FAILURE. Failure is inherited base failures only, not candidate-introduced.
- My test job `PR · Go unit · cli-3` (job 136780430782): conclusion SUCCESS (my test is in cli-3 per `scripts/pr-go-unit-shard.py`; matches prior run 44873244947/job 136752270714).
- go-build, go-vet, Focused Python, Trusted Plan, Native gate plan, Source format, Workflow policy, owner: SUCCESS.
- cli-0 (job 136780430791): FAILURE. Failing line: `--- FAIL: TestAppListAllTargetsWorksAfterInstallationDestroy` (line in `app_list_all_targets_test.go`, inventory depended on deleted Target config `docker-dev`, configured `config.yaml` missing).
- packages (job 136780430748): FAILURE. Failing lines:
  - `--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (`loki_test.go:522`)
  - `--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability` (`loki_test.go:586`)
  - `--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (`loki_test.go:633`)
- These exact failing first-level test names and lines also occur in same-base baseline run 44867737078 on base SHA e45430f2f1b7 (reviewer-1 recorded the identical three packages failures and the identical cli-0 failure). Inherited from base: cli-0 failure = 0428-210 / PR #1739; packages failures = 0428-142 / PR #1702. NOT introduced by this write-set. Booked as inheritance with line; aggregate booked as FAILURE until a required aggregate shows success on a candidate head.
- Byte counts per protocol (three per protocol):
  - cli-0: `--log` = 45764 bytes; `--log-failed` = 6932 bytes; `--job 136780430791 --log` = 45764 bytes.
  - packages: `--log` = 66915 bytes; `--log-failed` = 27354 bytes; `--job 136780430748 --log` = 66915 bytes.
  - cli-3 (my test): `--log` = 44206 bytes.
  - Counts measured per-job from per-job logs only (aggregate `gh run view --log` omits whole jobs, documented defect in card 0428-217).

## Stop criterion

Stopped while the required aggregate (run 44882418434) is FAILURE from inherited base cli-0/packages failures. Exact text + `authentication_failed` + missing-principal + stamped-success are all asserted and the candidate's own required cli-3 job passes; the required aggregate completion/success is not shown because of base defects outside this write-set. Per the GATE RULE this one inherited-failure case is reported as STATE (check + failing line) — the route to a required-passing aggregate is a change outside this card's write-set (shared base planner / base required-plan / release matrix), a coordinator action.

## repo-rule compliance

- Write-set: only `cmd/baha/mcp_operator_seam_test.go` changed (9 insertions, 1 deletion vs de4a45ec5).
- `cmd/baha/mcp.go` untouched (owned by 0428-204 / #1726).
- `.github/**` and `scripts/**` untouched (owner scope).
- `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go` untouched (taboo).
- No workflow file edited, no workflow_dispatch, no rerun authored.
- One integration candidate only: lane-0428-218-mcp-operator-seam; no second branch invented.
- Subagents: none (4.8). Every step ran in this session.

## Cleanliness

- Before: PID 3965938. `docker ps -a`:
  ```
  CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
  ```
  header only, no containers.
- After mutation work (throwaway worktree removed, `git worktree prune`): no containers created by this lane.
- End: PID to be recorded before END. `docker ps -a` must still be header-only; orphans of dead lanes exhaust the daemon address pools and block later gates.

## END

Evidence path verified on origin/main:
```text
evidence/r28-welle4-2026-11-21/mcp-operator-seam/round-2-exactmessage.md
```
(origin/main fc2913ed; commit 6400b372 rebased onto new origin/main, pushed)

END 0428-218-msgassert BLOCKED — fix committed fb5a5deaf, delivered (origin lane-0428-218-mcp-operator-seam fb5a5deaf), required cli-3 job SUCCESS in run 44882418434; the exact gate message is now pinned and the mutation proof shows RED on product-text change / GREEN on restore. The required aggregate (run 44882418434) stays FAILURE from inherited base defects (cli-0 `TestAppListAllTargetsWorksAfterInstallationDestroy`; packages `TestPersesLokiDatasourceMultiSource*`), booked as STATE with failing lines — outside this write-set. Coordinator action to resolve base defects or approve a route to a required-passing aggregate.
