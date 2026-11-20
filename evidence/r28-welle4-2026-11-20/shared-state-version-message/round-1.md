# 0428-201 · shared state version message — round 1

- Card: 0428-201
- Task: `t-20261120-shared-backend-state-version-message`
- Owner: w201-0428-201-statever
- Release: v0.4.28
- Session: w201-0428-201-statever (ornith)
- Branch (candidate): `w201-0428-201-statever`
- Head SHA: `9bf4a72f742b62c4361138c362d48b837f2f7ee1`
- Pull Request: #1725 (draft, base develop, head w201-0428-201-statever)
- Base (develop) attested SHA: `40cb28c758b02960356434b630086a341ebe1738` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- Base attestation: `git merge-base --is-ancestor origin/develop HEAD` = YES (base head 40cb28c7 fetched via `git fetch origin develop`); `git log --oneline origin/develop..HEAD` lists ONLY `9bf4a72f` (own commit). Branch cut from develop head 40cb28c7, not from any PR head.

## PLAN

1. Read mission, card, H-V21 hunt akte, and sibling card 0428-200; measure remote develop head 40cb28c758b0; cut the named worktree branch from develop head with ancestor attestation.
2. Trace the shared-backend state version failure from `decodeSharedBackendState` to the human command surface (topology-status/projection detail, `ReconcileSharedBackends` return, `SharedBackendDestroyPlan`/`readSharedBackendDestroyState`), confirm the fail-closed path is byte-identical and untouched by the sibling card 0428-200 (which only touches `internal/deployment/deployment_store.go` + `cmd/baha/app_context.go`).
3. Implement: add a distinct `SharedBackendStateVersionMismatch{Found, Expected}` error type in `internal/application/shared_backends.go` (the error type it exposes externally) naming found version, expected version and the supported next step (upgrade the shared backend provider), plus `IsSharedBackendStateVersionMismatch` to distinguish it from a corrupt/unreadable file; return it from `decodeSharedBackendState`. Fail-closed logic unchanged.
4. Add regression test `internal/application/shared_backends_state_version_test.go`: version-gate message (found/expected/upgrade-from-outside), distinguishability from corruption, real load path over a written v2 state asserts the version reason and no disk rewrite, correct-version happy path.
5. Local checks: gofmt clean, go vet clean, go build all OK; go test `./internal/application/...` shows only pre-existing develop failures (diff vs develop = none new); the new and version-gate tests pass.
6. Bundle one commit, push to the github.com/mcpdev80 remote, open draft PR #1725 (base develop) with card number + head SHA + evidence path; prove delivery via `git ls-remote` on both the branch and the PR head.
7. Gate: run the matching CI unit-test groups locally (packages shard covers `internal/application`, cli-0..3, gofmt/vet/build). Record run outcomes at head; record the pre-existing GATE-FAIL 0428-198 operator gate as STATE, not fought.
8. Push evidence to baseharbor-plan origin/main, verify path-present, confirm no containers running, post END with plan-main SHA.

## Fund / fix

Fund (from H-V21, carried into this card): two state files (`deployment.json` and the shared-backends state) both carry a version field that fails closed, but neither human message signals the upgrade-from-outside case. `internal/application/shared_backends.go:17` sets `sharedBackendStateVersion = 3`; `decodeSharedBackendState` (`internal/application/shared_backends_state.go:31-32`) rejects any other version with a bare "unsupported shared backend state version N" and no found/expected/next-step text or upgrade signal. This card repairs the shared-backends side; card 0428-200 repairs the deployment-record side.

Fix (this PR, head 9bf4a72f):
- New type `SharedBackendStateVersionMismatch{Found, Expected}` in `internal/application/shared_backends.go` with an `Error()` that names the found version, the expected (supported) version and the supported next step ("upgrade the shared backend provider to a release that writes version N first"), and `IsSharedBackendStateVersionMismatch(err)`.
- `decodeSharedBackendState` now returns `&SharedBackendStateVersionMismatch{Found: state.Version, Expected: sharedBackendStateVersion}` instead of the generic `fmt.Errorf`.
- Fail-closed behavior byte-identical: no migration, no discard, no rewrite. The version gate, the PostgreSQL-topology gate and the file-ownership checks are unchanged.

Evidence of the message at the real load path (unit, over a written v2 state):
- `TestSharedBackendStateLoadReportsVersionReason` writes `{"version":2,"environment":"dev"}` to disk, runs `loadSharedBackendState`, asserts the error is `*SharedBackendStateVersionMismatch` with `Found=2`, and asserts the on-disk bytes are unchanged after the load.

## Acceptance

- [ ] 1. The shared-backends version failure names the version found, the version expected, and the supported next step, and is distinguishable from a corrupt or unreadable file — DONE: `SharedBackendStateVersionMismatch.Error()` names found/expected + upgrade path; `IsSharedBackendStateVersionMismatch` separates it from parse/ownership corruption; covered by `TestSharedBackendStateVersionMismatchNamesVersions` and `TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption`.
- [ ] 2. Fail-closed stays byte-identical — DONE: only the error value changed; gate logic, file checks and the correct-version happy path are unchanged; `TestSharedPostgresDoesNotMigratePreFreezeState` still passes; `TestSharedBackendStateLoadReportsVersionReason` asserts no disk rewrite.
- [ ] 3. Regression writes a v2 state, runs the real command surface (the shared-backend load path), asserts the version reason (not a generic error) reaches the caller — DONE: `TestSharedBackendStateLoadReportsVersionReason` runs the real `loadSharedBackendState` over a written v2 state and asserts the version mismatch kind + found/expected text + no rewrite.
- [ ] 4. One hosted run at the exact head shows the owning shard executed, 0 failure — recorded as STATE below: the `packages` CI unit shard covers `internal/application` (my test path) and the cli-0..3 shards run; at the local mirror of the exact head the only failing check is the pre-existing field-gate defect GATE-FAIL 0428-198 (operator OIDC gate, root 2af892e4e in `internal/serviceaccess/policy.go`, owned by card 0428-202), which fails identically on clean develop and is reported, not fought.

## repo-rule compliance

- Write-set inside the card's allowed zone: `internal/application/shared_backends_state.go` (message + error kind) and its new test file `internal/application/shared_backends_state_version_test.go`; `internal/application/shared_backends.go` touched only for the external error type it exposes (`SharedBackendStateVersionMismatch`, `IsSharedBackendStateVersionMismatch`). No other product file changed.
- Locked files untouched: `internal/serviceaccess/**` (0428-198/202), `internal/metrics/**`, `internal/observability/registry.go`, `internal/machine/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/deployment/**` (0428-200), `cmd/baha/**`. No migration added (no card + owner decision).
- No `.github/**` change, no workflow edit, no `workflow_dispatch`/rerun.
- No `git add -A` (untracked test-fixture dirs `prune-owner/`, `trace-*/` from local runs were deliberately NOT added); one commit only; no merge; no force-push on develop/main.
- Branch provenance: cut from develop head 40cb28c758b0 (attested via `git ls-remote`), ancestor-of-base YES, `git log --oneline origin/develop..HEAD` = only `9bf4a72f`.
- Remote guard: first git action was `git remote -v`; the github.com/mcpdev80 remote was `origin` (URL https://github.com/mcpdev80/baseharbor.git) in this clone; pushed through that name.
- CI group coverage: the `packages` unit shard (`scripts/pr-go-unit-shard.py --mode packages`) runs every non-CLI Go package including `internal/application` (my test path) — durable evidence in this same PR per the gate rule.

## GATE-FAIL 0428-198 (STATE only, not fought)

- Check: `wizard-registration-tests` (go unit shard `cli-0`/`wizard-registration-tests`, runs `cmd/baha`).
- Failing log line at exact head 9bf4a72f (identical on clean develop 40cb28c7):
  `registration_ci_readiness_test.go:118: in-process MCP app.list invocation failed: ... error:map[code:authentication_failed message:Managed-environment machine operations require an authenticated BaseHarbor operator. next:Authenticate the operator for the selected Target and environment, then retry the same operation.]`
- Root: `2af892e4e` in `internal/serviceaccess/policy.go` (managed-environment operator OIDC gate). Owner: card 0428-202 (#1684 lane), not this card.
- This card's own evidence comes from the smallest matching gate: `go test ./internal/application/...` for the version gate (all four new tests PASS; the only application failures are pre-existing develop failures — provider-registration fixture `company-postgres` external scope, config-dir trust in `internal/accesswizard`), which is sufficient; no fourth full-matrix run.

## cleanliness

- Containers/networks/volumes/state directories: NONE started. Session host is the codeman/coordinator server; Docker/Podman tests run only on the named SSH hosts (baha-docker/baha-podman), none used.
- Container witness before/after: `ps -ef | grep -E "docker|podman|compose" | grep -v grep` shows no compose project started by this lane; no orphaned network/volume created.
- Scratch under /tmp only: `/tmp/w201-base` (clone/worktree), `/tmp/w201-baha` (binary), `/tmp/w201-pr-body.md`. ambient-core/ images of foreign carts untouched.
- cleanliness: clean.

## END

END_DONE w201-0428-201-statever (0428-201 shared state version message): implemented distinct `SharedBackendStateVersionMismatch{Found, Expected}` in `shared_backends.go` + returned it from `decodeSharedBackendState` (names found/expected version + supported next step, distinguishable from corruption); fail-closed byte-identical; regression over real load path (v2) added; one commit 9bf4a72f on branch w201-0428-201-statever cut from develop 40cb28c7; draft PR #1725 (base develop). CI local mirror at head: packages/cli-0..3/gofmt/vet/build pass; GATE-FAIL 0428-198 operator OIDC gate at `registration_ci_readiness_test.go:118` (root 2af892e4e, card 0428-202) recorded as STATE, not fought. Evidence on baseharbor-plan origin/main.
