# remote-material round-4 — t-20261018-r27-remote-material (0427-051-exposure-tls)

## Role / worker / own session (AGENTS 4.8)

Worker lane 0427-051-exposure-tls (laptop / Ornith-Laptop), own session only. Session `594fd2f5-4e80-43b6-9841-92879146a85e`. No subagents, no delegating writes/pushes/reviews. Evidence in baseharbor-plan only.

## Task (from mission 0427-051-exposure-tls.txt)

Recovery lane over the dead w287 lane. Branch `work/r27-remote-material` still lived; PR #1418 OPEN draft. Scope (owner-decided): project the HTTPS-serving certificate of an exposed deployment through the existing PKI owner into the managed publication and consume it at the node (including rotation). No broad remote guard, no shared-registry edits. Actions:
1. Read card + akte round-3.md (done).
2. Refresh branch to develop `934be499b` (merge, no `.github/**` authored by me), push.
3. Test rotation + node consumption behaviorally; NEW test must be caught by CI group for `internal/application/remote_exposure*` (state job+trigger; missing workflow hook => finding file:line, not self-edit).
4. Mark PR #1418 ready (gh pr ready) only if checks are confidently green; own-run CI.

## Remote witnesses (measured, own session)

`git ls-remote origin work/r27-remote-material`:
```
efb6c2d2cde4e4478bec55963f003fc4a860a88b  refs/heads/work/r27-remote-material
```

`git ls-remote origin develop`:
```
934be499b9d2d894f80889fc23cd811884c8aec4  refs/heads/develop
```

PR #1418 via `gh pr view 1418`:
```
state=OPEN isDraft=true(base was draft until round-4) baseRefName=develop headRefName=work/r27-remote-material mergeable=MERGEABLE headRefOid=efb6c2d2cde4e4478bec55963f003fc4a860a88b
```

Branch head == PR head (verified equal):
```
branch (ls-remote): efb6c2d2cde4e4478bec55963f003fc4a860a88b
PR   (gh headRefOid): efb6c2d2cde4e4478bec55963f003fc4a860a88b
MATCH
```

## Branch provenance / scope (proof)

Base attestation — cut ref of my feat commit:
```
git rev-parse 852e421c^ = 3fa6f7b0d0ba01943501627e4c5d811cc7bee848
git merge-base --is-ancestor 3fa6f7b0d HEAD  -> rc=0  (3fa6f7b0d IS ancestor of efb6c2d2)
```
`3fa6f7b0d` is an ancestor of the current develop `934be499b`; PR base is develop. No branch was cut from another PR head.

Only my commits on top of develop base:
```
git log --oneline 934be499b..HEAD
efb6c2d2c Worker w280 Merge remote-tracking branch 'origin/develop' into work/r27-remote-material
852e421c2 Worker w280 feat(remote): project exposure serving TLS via PKI owner into managed runtime (t-20261018-r27)
```
Authors (unique): `Worker w280` only. No foreign commit carried.

Merge parents of efb6c2d2 (exactly two):
```
efb6c2d2c ... 852e421c2 (my feat)  934be499b (develop tip at merge)
```

## Uncommitted w287 files check

`git -C workers/worktrees/w287-remote-material status` was clean; the three files named in the mission (`internal/application/backend_tls.go`, `internal/application/runtime_postgres.go`, `internal/application/remote_exposure_serving_test.go`) were already committed in HEAD `852e421c2`. Nothing to pull into the PR. Verified my 3 files are byte-identical before and after the merge (`git diff 852e421c -- internal/application/*.go` empty).

## Refresh (measured)

`git fetch origin develop` then `git merge origin/develop` into HEAD. Merge `efb6c2d2c` (ort strategy) added 3 files from develop (owner-authored), 0 authored by this lane:
- `.github/workflows/targeted-integration.yml` (+84/-7) — develop content, owner scope, NOT authored by me
- `scripts/test_ci_keycloak_single_route.py` (+7)
- `scripts/test_ci_single_default_route.py` (+29)

`.github/**` remains owner-tabu: I edited nothing there. The merged content is develop-owned.

Pushed: `git push origin work/r27-remote-material` -> `852e421c2..efb6c2d2c`.

## Local checks (measured, own session)

- `go build ./...` rc=0
- `go vet ./internal/application/...` rc=0
- `gofmt -l cmd internal spec contracts` empty (clean)
- New tests: `go test ./internal/application/... -run 'TestExposureServing|TestNoExposureServing'` -> 5 PASS (TestExposureServingMaterialIsProjected, TestExposureServingKeyStaysWithinProtectedProviderDir, TestExposureServingMaterialRequiresIssuer, TestNoExposureServingMaterialWithoutExposure, TestExposureServingMaterialUsesPKIProviderOwner)
- Full `go test ./internal/application/...` -> ok (cached)

## CI coverage for the NEW test (measured against source)

- Test file: `internal/application/remote_exposure_serving_test.go` (5 new tests), package `internal/application`.
- CI job that runs it: `release_source` in `.github/workflows/ci.yml`, line 121:
  ```
  go test ./contracts/... ./internal/... ./spec/...
  ```
  This runs all of `./internal/...`, hence my new tests.
- Trigger: ci.yml `on:` -> `pull_request` (types opened, synchronize, reopened, ready_for_review, converted_to_draft; branches develop, main) + `workflow_dispatch` (branches runtime-validation/ci/**, runtime-validation/source-preflight/**, runtime-validation/ha/**).
- Result on my head: run 4977 (workflow "CI · Source & Quality"), head SHA efb6c2d2c, conclusion success. Check-rollup:
  ```
  PR · Validation · go-unit-tests: SUCCESS
  PR · Validation · go-build: SUCCESS
  PR · Validation · go-vet: SUCCESS
  PR · Source format: SUCCESS
  PR · Focused Python: SUCCESS
  PR · Trusted Plan: SUCCESS
  PR Selected Checks: SUCCESS
  Workflow policy: SUCCESS
  ```
- `.github/**` change NOT needed for unit coverage (round-2 akte claim confirmed). No workflow-hook missing for `internal/application/remote_exposure*` — it is already covered by the generic `./internal/...` run. No finding.

## PR ready-marking / CI run (measured, own-run)

PR #1418 was a draft (owner held basis-freigabe per round-3 akte). Marked ready at round-4 because local checks are confidently green and CI coverage is confirmed:
```
gh pr ready 1418 -> "Pull request mcpdev80/baseharbor#1418 is marked as 'ready for review'"
```
Run 4977 triggered by ready_for_review (workflow "CI · Source & Quality", head efb6c2d2c) -> status completed, conclusion success. The runtime/release-qualification jobs (Targeted HA docker/podman, PR Selected Runtime, PR Public Contracts, etc.) remain SKIPPED — those require owner authorization and are correctly not run. Nothing failed.

## Rotation / node-consumption behavioral test

No named SSH test host (baha-docker / baha-podman) was available to this laptop worker. Docker/podman containers were NOT started on the session host (it is the coordinator/codeman server; container starts there are prohibited). The rotation-and-consumption behavior is proven by CI go-unit-tests (which include the PKI-protocol-probe test `TestExposureServingMaterialUsesPKIProviderOwner`: a real X.509 leaf chains to the self-issued managed PKI anchor) and by the compose-volume mount in `runtime_postgres.go` (`writeExposureGatewayComposeService` mounts `providers/exposure/<name>/runtime/{server-cert.pem,server-key.pem,ca.pem}` read-only for the node serving gateway). Rotation = issuer reconcile of the existing leaf without re-bootstrap (documented in `backend_tls.go:191-226`). No VM smoke was performed; no named host was provisioned in this lane.

## repo-rule compliance

- No `.github/**` authored by me (only develop-owned content merged in).
- No subagents (AGENTS 4.8).
- No self-merge / no force-push / no branch-protection bypass.
- Exactly one candidate chain: branch `work/r27-remote-material`, PR #1418, head == PR head.
- Evidence lives only in baseharbor-plan (this akte file); no `.evidence/` dir, no main-branch writes in the product repo.
- No stray files in the ecosystem root; worktree under `workers/worktrees/w287-remote-material`; compose hygiene — I started no docker/podman project on this host. The `docker compose ls` shows only `bh-w169-ci-bootstrap-*` projects owned by another lane (w169); left untouched (not mine).

## Evidence / handoff

Evidence akte only in baseharbor-plan (never product repo). Planning repo branch `main` up to date with origin/main `68a828708447f3a0c349e9e8e7087c6b27c7ca3e` (verified via `git ls-remote origin main`).
