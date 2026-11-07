# 0427-116-remote-up-cli: r4-correct — real CLI `baha app up` success-path discriminator (docker + podman)

- Role: Worker (lane 0427-116-r4-correct, ornith1.5; session ses_e49dd08feffecTpIdkhFEks8ZX); coordinator `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-cli-path` (0427-116, PR #1407, branch `work/r27-remote-up-cli`). Mission `coordinator/missions/0427-116-r4-correct.txt`.
- Basis drift handled (Owner directive 2026-11-07): develop advanced to `c8a79faff` (#1420/#1424/#1425/#1426). Merged `origin/develop` into the candidate before the r4-final push; `git merge-base --is-ancestor c8a79faff HEAD` rc0.
- Result: PR #1407 head `4402d3f4b` carries one new **red-first** cmd/baha test that drives the real CLI up-path (`executeApplicationUpLifecycle` -> `executeRemoteApplicationApply` in `cmd/baha/app_remote_lifecycle.go`) for a connector-bound, broker-less pure-client app and asserts the behavioral discriminator #1407 introduced at the production write seam: the up-path routes through the bound target's connector transport, takes NO managed-service issuer and touches NO local Core (injected `applicationCoreBootstrap` never called, no local installation state), then fails closed at the connector seam (no live enrolled node). Same cell asserts the broker-required intent fails closed before mutation. The success seam (`err == nil`) is unit-unreachable at the live-enrolled-node connector boundary; the genuine success round-trip (`Publish`+`ApplyApplication` with `err == nil` on both families) is the internal/application cell `remote_pureclient_apply_roundtrip_test.go`, which the mission forbids calling from the cmd/baha layer.
- CI (own run, 4.6): drift-refreshed head `c4d528645` (developer `812c99c88` merged, #1383 conflict-free vs scoped write-set). Hosted run `42381393714` terminal **success**; `PR · Validation · go-unit-tests` success (8m34s) covers the new cmd/baha test AND the internal round-trip via `go test ./cmd/baha` + `go test ./internal/...` (PR trigger against develop); `go-build`/`go-vet` success too. Docker/podman runtime gates skipped by the path rule (not failures).

## PLAN (numbered; mirrors live board workers/todos/0427-116-r4-correct.json)

1. Read mission + card + prior akte (round-4, act-1419e); verify planning zone is baseharbor-plan ONLY (not workers/baseharbor-plan phantom) — DONE
2. git fetch origin develop + work/r27-remote-up-cli; confirm c8a79faff (current develop) ancestor of HEAD after merge; own-commits list clean, delta scoped — DONE
3. Trace remote-up CLI up-path; confirm connector seam unit-unreachable, success proven via internal round-trip cell — DONE
4. Baseline: full cmd/baha suite = EXIT=1 with ONLY pre-existing TestAppEditCommandCompleteProviderEditRunsRealLifecycle (out of scope); internal/application clean — DONE
5. Write red-first cmd/baha success-discriminator test; prove red (fail) when path forced through local Core bootstrap, green (pass) on fixed head — DONE
6. go build ./... + go vet ./cmd/baha/ ./internal/application/ rc=0; gofmt clean — DONE
7. Commit 4402d3f4b; fast-forward push 5900dc6b7..4402d3f4b to work/r27-remote-up-cli; PR #1407 OPEN MERGEABLE base develop — DONE
8. Own-run CI 42379326641 terminal success: go-unit-tests PASS (covers new cmd/baha test + internal round-trip); go-build/vet/gofmt PASS; runtime gates skipped by path rule — DONE
9. Write + publish evidence r27-welle5-folge-2026-11-07/remote-up-cli/round-4.md to baseharbor-plan origin/main before END — DONE
10. Teardown: own containers 0 (pure unit tests, nothing started); vm-locks none held — DONE
11. END post to 594fd2f5 — last action

## Planning-zone attestation (required)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the real planning repo; `workers/baseharbor-plan` phantom zone NOT used).
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Phantom SHAs `9ca27c9f`, `aff1532c`, `e53eedd0`: none is an ancestor of develop or of this candidate; this lane cites none of them as evidence.

## Base attestation + basis refresh (Owner directive 2026-11-07)

- Remote witnesses (`git ls-remote origin refs/heads/work/r27-remote-up-cli refs/heads/develop`):
  - `5900dc6b71a2adfec1842164066475061a44d616 refs/heads/work/r27-remote-up-cli` (candidate head before the r4-final push — the develop-merge head)
  - `c8a79faff91cd870ac3904a2a392922a24cc7e13 refs/heads/develop` (current develop; #1420/#1424/#1425/#1426)
- Method: fresh clone in this lane's own persistent zone `/tmp/r27-up-cli-wt` (quarantined `workers/baseharbor` NOT used). Merge `origin/develop` into the candidate (ort strategy, zero conflicts). Post-merge:
  - `git merge-base --is-ancestor c8a79faff HEAD` => rc0 (c8a79faff IS now an ancestor of HEAD).
  - `git merge-base origin/develop HEAD` => `c8a79faff` (the develop merge base is current).
  - `git diff --name-only origin/develop..HEAD` scoped to card files only: `cmd/baha/app_remote_lifecycle.go`, `cmd/baha/app_remote_pureclient_apply_test.go`, `cmd/baha/app_remote_up_success_discriminator_test.go`, `cmd/baha/app_repository_integration_test.go`, `cmd/baha/app_workload_integration_test.go`, `cmd/baha/repository_runtime_fixture_test.go`, `internal/application/remote_pureclient_apply_roundtrip_test.go`. The last three test files are develop's own drift carried by the merge (verified: `git log origin/develop..HEAD -- <file>` attributes them to develop, not this lane), not edits by this lane.
- Push witness: `5900dc6b7..4402d3f4b HEAD -> work/r27-remote-up-cli` (fast-forward, no force). After: `git ls-remote origin refs/heads/work/r27-remote-up-cli` => `4402d3f4b053b2b740520874f19a7c7ac732bcb0`. PR #1407 API `headRefOid` = same; state OPEN, base develop, MERGEABLE.
- Ancestor witnesses: `git merge-base --is-ancestor 5900dc6b71 HEAD` = YES; `git merge-base --is-ancestor c8a79faff HEAD` = YES (single candidate branch, no second branch created — exactly-one-candidate rule).
- Own-commits witness `git log --format="%h %s" origin/develop..HEAD` (all card-chain, no foreign commit):
  - `4402d3f4b test(r27 remote-up): assert real CLI up-path takes connector route, no local Core (owner round-4)` (this lane)
  - `c24058e78 Merge branch 'develop' into HEAD` (develop refresh)
  - `5900dc6b7 Merge branch 'develop' into HEAD`
  - `0b3608987 test(r27 remote-up): assert success + fail-closed for pure-client up path (owner round-3)`
  - `86f990a6 Merge branch 'develop' into work/r27-remote-up-cli`
  - `c87c8b64 fix(r27 remote-up): pure-client app up routes through connector, no local Core bootstrap [carry original round-1 test shape]`
  - `fa7a6165 fix(r27 remote-up): pure-client app up routes through connector, no local Core bootstrap`

## Repo-rule compliance

- No edits under `.github/**` by this lane; no reruns, no workflow_dispatch, no runner infrastructure. Failing hosted state (the one pre-existing App-Edit test) reported as STATE with run id + log line only; out of scope.
- VM cells: none of this lane's work is a normal test, so no VM compose project was started; own containers 0, podman 0 (ps-witness below). No `baha-runner-*` host used.
- Single candidate branch `work/r27-remote-up-cli`, single PR #1407; basis refresh by merge (no force-push, no second branch).
- Evidence only in baseharbor-plan; this file contains NO markdown checkboxes.
- No subagents; every step executed in this session.
- No self-merge; PR left OPEN for CODEX-REVIEW.
- #1419/#117 reference correct: #117 = merged fail-closed owner-fix (PR #1419 merged develop `beb923fe6`); NOT an success transcript. The success transcript in this lane is the internal/application round-trip cell (err == nil, both families) plus the cmd/baha real-CLI discriminator that proves the fixed up-path takes the connector route and fails closed at the seam. The genuine `err == nil` success through the real CLI against a live enrolled node is a VM/transcript concern and, per the unit boundary, is unit-unreachable; this lane proves the discriminating CLI behavior instead.

## Baseline (pre-change) cmd/baha failures

- Full `go test ./cmd/baha/` EXIT=1. The ONLY failing test: `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (app_edit_apply_test.go:957): "start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner".
- This is the App-Edit integration test, unrelated to card t-20261106-r27-remote-up-cli-path. My write-set is `cmd/baha/app_remote_lifecycle.go` + the remote-up tests only. Left untouched (out of scope).
- `go test ./internal/application/ -count=1` => ok (clean) on the merged head.

## Red-first proof (required by mission)

- The real CLI up-path (`executeRemoteApplicationApply` -> `runApplicationMemoryPreflight` for a connector-bound target -> `remoteApplicationProjectRuntime` -> connector transport `NodeMemory`) terminates at the live-enrolled-node connector seam with `targetsession.ErrUnavailable` ("authenticated Connector session is unavailable; reconcile before retrying a mutation") in a unit runner — this is the ground-truth failure mode.
- Discriminator asserted by the new test: `applicationCoreBootstrap` is NEVER called (bootstrapCalls == 0) and NO local installation state is created (`coreinstallation.Load` of the Core target root returns os.ErrNotExist).
- Red controlled experiment: inject a single `applicationCoreBootstrap(...)` call into the up-path (simulating the pre-fix HEAD that routed the pure-client remote up through the local Core). Result: `--- FAIL: TestRemoteUpRealCLIPathTakesConnectorRouteNeverLocalCore` at `bootstrapCalls=1` with "the head must route through the connector route". Green: fixed head => PASS. This proves the test is genuinely red-first (fails on the pre-fix behavior, passes on the fixed behavior).

## CI coverage (new-test rule 2026-11-07)

- The new cmd/baha test (`cmd/baha/app_remote_up_success_discriminator_test.go`, package `cmd/baha`) is executed by the existing hosted job `PR · Validation · go-unit-tests` via `go test ./cmd/baha` (ci.yml "Run release-source tests" step: `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`). The internal round-trip cell (`internal/application/remote_pureclient_apply_roundtrip_test.go`) runs via `go test ./internal/...` in the same job.
- Trigger: pull_request opened/synchronize/reopened against develop (ci.yml PR trigger block). No new test runs only locally or in a VM cell: both the cmd/baha and internal/application packages run under the hosted go-unit-tests job.
- No `.github/**` change was required: the existing `PR · Validation · go-unit-tests` group already covers the changed path. (If a future change needed a new VM-transcript test picked up by a docker/podman acceptance group, that `.github/**` change is Owner scope — reported as finding with file:line, not edited.)

## repo-rule compliance

- No `.github/**` edits, no reruns, no workflow_dispatch, no runner infrastructure. Pre-existing App-Edit failure reported as STATE only.
- Single candidate branch `work/r27-remote-up-cli`, single PR #1407; basis refresh by merge (no force, no second branch).
- Evidence only in baseharbor-plan; no markdown checkboxes.
- No subagents; every step in this session.
- No self-merge; PR left OPEN.

## Drift refresh to 812c99c88 (Owner drift-befund 2026-11-07)

- develop continued to `812c99c88` (owner merged #1383), which touches the three test files the earlier c8a79faff merge already carried: `cmd/baha/app_repository_integration_test.go`, `cmd/baha/app_workload_integration_test.go`, `cmd/baha/repository_runtime_fixture_test.go`.
- Pre-refresh my head `4402d3f4b` was based on `c8a79faff`, so `git merge-base --is-ancestor origin/develop HEAD` FAILED against `812c99c88`.
- Method (before any CODEX-REVIEW): `git fetch origin develop`, `git merge --no-edit origin/develop` => ort merge, **zero conflicts**, 3 files changed (the #1383 test files only). Post-merge witnesses:
  - `git merge-base --is-ancestor 812c99c88 HEAD` => rc0 (812c99c88 IS now an ancestor of HEAD).
  - `git merge-base origin/develop HEAD` => `812c99c88` (current develop merge base).
  - new HEAD `c4d528645` (refresh merge commit, no content edits by this lane).
  - scoped write-set CONFIRMED conflict-free / byte-identical to `4402d3f4b`: `git diff 4402d3f4b HEAD -- cmd/baha/app_remote_lifecycle.go cmd/baha/app_remote_up_success_discriminator_test.go internal/application/remote_pureclient_apply_roundtrip_test.go cmd/baha/app_remote_pureclient_apply_test.go` => empty. #1383 did not touch my write-set.
  - `go build ./...` rc0; `go vet ./cmd/baha/ ./internal/application/` rc0; `gofmt -l` on scoped files empty; new discriminator test PASS (both subtests).
  - diff vs develop now scoped to card files only: `cmd/baha/app_remote_lifecycle.go`, `cmd/baha/app_remote_pureclient_apply_test.go`, `cmd/baha/app_remote_up_success_discriminator_test.go`, `internal/application/remote_pureclient_apply_roundtrip_test.go` (the 3 #1383 test files dropped from the delta because develop now includes them).
  - Push: `4402d3f4b..c4d528645 HEAD -> work/r27-remote-up-cli` (fast-forward, no force). Remote head `c4d528645`; PR #1407 OPEN MERGEABLE base develop.
- Own-commits `git log origin/develop..HEAD`: `c4d528645 Merge branch 'develop' into HEAD` (refresh) on top of `4402d3f4b`; no foreign commit.

## CI coverage (new-test rule 2026-11-07)

- The new cmd/baha test (`cmd/baha/app_remote_up_success_discriminator_test.go`, package `cmd/baha`) runs under hosted job `PR · Validation · go-unit-tests` via `go test ./cmd/baha` (ci.yml "Run release-source tests": `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`). The internal round-trip cell (`internal/application/remote_pureclient_apply_roundtrip_test.go`) runs via `go test ./internal/...` in the same job.
- Trigger: pull_request opened/synchronize/reopened against develop (ci.yml PR trigger block). No new test runs only locally or in a VM cell; both packages are covered by the hosted go-unit-tests job.
- No `.github/**` change required: the existing `PR · Validation · go-unit-tests` group already covers the changed path. (A future VM-transcript test picked up by a docker/podman acceptance group would be an Owner-scope `.github/**` change — reported as finding with file:line, not edited.)

## Publication block (second-to-last action)

- Before push, `git log --oneline origin/main..HEAD` => `71e173f9 evidence(r27 w5-folge-2026-11-07): remote-up-cli round-4 — real CLI baha app up success-path discriminator (docker+podman) on PR #1407; developer head refreshed c8a79faff then 812c99c88 (#1383 conflict-free vs scoped write-set), head c4d528645, CI 42381393714 go-unit-tests PASS; success seam unit-unreachable at live-enrolled-node connector -> proven via internal round-trip cell + cmd/baha real-CLI connector-route discriminator` — lists ONLY this lane's commit.
- Push: `62c47f16..71e173f9 HEAD -> main`; `git log --oneline origin/main..HEAD` after push => empty (fully published).
- `git ls-tree -r origin/main --name-only | grep remote-up-cli/round-4` => `evidence/r27-welle5-folge-2026-11-07/remote-up-cli/round-4.md` (present on origin/main).
- `git ls-remote origin refs/heads/main` => `71e173f917e28379dd7787575005f05b31a3f31e refs/heads/main` (final; round-4 file path present on origin/main).

## Teardown witness

- Own containers: `docker ps -aq --filter name=bh-` delta 0 from own work; `docker ps` empty afterwards (no project of this lane was started — pure unit tests). `podman ps -aq` = 0. No `baha-runner-*` host used as a test host.
- vm-locks: none held by this lane.

## END

END_DONE 0427-116-r4-correct: PR #1407 drift-freedom confirmed — head c4d528645 = developer head 812c99c88 (#1383) merged conflict-free vs scoped write-set (812c99c88 is-ancestor-of-HEAD rc0, merge-base 812c99c88; app_remote_lifecycle.go + remote_pureclient_* byte-identical to 4402d3f4b, #1383 test files untouched); red-first cmd/baha success-discriminator drives real CLI baha app up for connector-bound broker-less pure-client app, asserts connector route / no local Core bootstrap / fail-closed at connector seam (red proven by injecting Core bootstrap), same cell broker-required fails closed before mutation; internal round-trip cell proves the unit-unreachable err==nil success seam (docker+podman); CI 42381393714 terminal success go-unit-tests PASS 8m34s + go-build/vet (go test ./cmd/baha + ./internal/...) covers new cmd/baha test + internal round-trip; docker/podman runtime gates skipped by path rule; success seam genuinely unit-unreachable (live-enrolled-node connector), real CLI success against a live node is a VM/transcript concern outside the unit boundary; #1419/#117 referenced correctly (#117=merged fail-closed owner-fix, NOT an success transcript); diff vs develop scoped to card files only; no .github; PR OPEN MERGEABLE base develop for CODEX-REVIEW; evidence=evidence/r27-welle5-folge-2026-11-07/remote-up-cli/round-4.md published to origin/main 71e173f9; own containers 0 podman 0
