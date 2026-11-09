# 0427-159 r5 — F1/F2 production-path proof: no-false-attribution registry + malformed/mismatch gate

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active), mission-159-r5
- Review judged (verdict = correction, approval withheld): `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r4.md`
- Prior round (r4): F2/F3/F4 fixed; F1 two-case proof and F2 boundary regression remained open (review r4)
- Shift / planning repo verified (origin/main): witness below (`git ls-remote origin main`)
- Product base (candidate chain base): `3187cea15728143146905c7238ad6e280ca11b3e` (ancestor of head)
- Candidate branch: `0427-159-damagedstate`, live head `794ffe435e14276a88d918fd9cc5029ae1f6afc7` (PR #1499)
- develop HEAD (verified no drift): `b3a8042d18ea60f162a32a51df34a499cad6a237`

## PLAN

- Read mission r5, act-1499-review-r4 verdict, round-4; verify PR #1499 head 794ffe43, develop b3a8042d1, base 3187cea15 ancestry
- Trace F1 production path: resolvedRepositoryApplication -> FindDeployment; ownerless (unknown, no network) vs trusted-owner (exact network)
- Trace F2: listDeploymentRecords ValidateDeploymentID gate + DamagedDirectoryState + verifyDeploymentOwnerAtSeam
- F1: add production-path owned-app regression asserting EXACT network name (TestRegistryOwnedAppReportsExactNetwork), distinct from ownerless case
- F1: confirm ownerless regression via production path (TestRegistryForeignOrphanNoFalseAttributionToRequestedApp)
- F2: extend TestListDeploymentRecordsDiscardsMalformedDirectoryNames with seeded owner + real UUIDv4 (valid damaged visible, malformed discarded); add record/dir mismatch integrity regression
- Local checks: go build, go vet, gofmt, targeted F1/F2 unit tests; verify FAIL pre-fix / PASS post-fix in isolated clone
- Push single candidate chain to PR #1499; integrated develop b3a8042d1; show base ancestor + develop..HEAD chain
- Hosted CI terminal success on exact head; no .github/** edit, no rerun/dispatch
- Publish evidence to origin/main before END; ls-remote + cleanliness witness; END only when terminal

## Design (resolved against r4 review)

- F1 (owned-app exact network): the r4 review noted the only registry F1 test was synthetic (built a `DamagedDeploymentError` manually and called `EnrichNetworkForOwnIdentity`). Added `TestRegistryOwnedAppReportsExactNetwork` that runs the REAL `resolvedRepositoryApplication` path with a trusted Core owner, a damaged directory in the requested app's namespace, and the app's own absent workload network, asserting the EXACT derived network name verbatim (not a substring). This is the second of the two requested F1 cases; the first (ownerless -> unknown-owner without requested-app network) is `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp`, already production-path.
- F2 (malformed + mismatch boundary): the r4 review noted the F2 test used a non-v4 placeholder UUID that the shape gate itself discards, so it never proved a valid-UUID damaged entry stays visible. Rebuilt the test with a genuine `stableid.NewUUIDv4` directory and a proven Core owner so the valid UUID is surfaced as damaged while the malformed (non-UUIDv4) directory is discarded. Added `TestListDeploymentRecordsDiscardsRecordDirectoryMismatch` for the record/directory integrity boundary.
- F4 (CI routing): both new tests live in the existing `go-unit-tests` / `deployment-package-tests` groups under the `pull_request` trigger (`go test ./...`); no `.github/**` edit.

## repo-rule compliance

- Evidence lives only in baseharbor-plan. No product repo edits land outside the candidate branch; no `.github/**` edit; no rerun/dispatch; no containers/compose started on any host.
- Subagents: none (4.8) — every step executed inside this own session.
- Planning repo verified (origin/main) witness pasted below in the Run section.
- No markdown checkbox lines anywhere in this evidence file (plain bullets only).

## Implementation (product write-set: baseharbor)

- No product source changed this round. The F2 shape gate (`ValidateDeploymentID`) and the F3 no-false-attribution ownerless branch (`DamagedDeploymentError.Ownerless()`) were already on the candidate from r4 (`43fab0e5`); this round adds only test proof.
- `cmd/baha/app_lifecycle_damaged_state_test.go`: added `TestRegistryOwnedAppReportsExactNetwork`.
- `internal/deployment/damaged_namespace_network_test.go`: extended `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` (proven owner + real UUIDv4 + malformed discarded) and added `TestListDeploymentRecordsDiscardsRecordDirectoryMismatch`.

## Regressions added

- `cmd/baha/app_lifecycle_damaged_state_test.go` `TestRegistryOwnedAppReportsExactNetwork` — production path `resolvedRepositoryApplication`: trusted-owner damaged directory, app's own workload network genuinely absent, asserts `damaged.Identity.Application == "owned-app"` and `damaged.NetworkName == "baseharbor-dev-workload-baseharbor-owned-app-dev"` verbatim plus `RuntimeNetworkStateAbsent`. Distinct from the ownerless case, which withholds any network diagnosis.
- `internal/deployment/damaged_namespace_network_test.go` `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` (extended) — with a proven Core owner and a genuine UUIDv4 damaged directory, asserts the valid UUID entry IS surfaced as a `DamagedDeploymentError` (own root), the malformed `foreign-orphan` directory is neither returned as a record nor advertised as damaged. Proven FAIL without the `ValidateDeploymentID` gate (malformed dir advertised as damage) and PASS with it.
- `internal/deployment/damaged_namespace_network_test.go` `TestListDeploymentRecordsDiscardsRecordDirectoryMismatch` — a valid UUIDv4 directory whose `deployment.json` claims a DIFFERENT deployment id fails closed as an integrity mismatch: not returned as a record, not reclassified as a damaged orphan. Proven against the production `loadDeploymentRecordFile` path-identity check (`record.Identity.DeploymentID != deploymentID`).
- `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` (existing, r4) confirmed production-path F1/F3: FAILS on the pre-F3 F1 base `79f1a8f1` (`foreign orphan must not acquire the requested app's identity`), PASSES on candidate.

## CI wiring

- F1/F2 tests run in the existing Go validation group under the `pull_request` trigger via `go test ./...`: `PR · Validation · go-unit-tests` and `PR · Validation · deployment-package-tests` (both success on the exact head). No `.github/**` edit was made (Owner scope).

## Hosted CI terminal — run 42559458982 (PR #1499, head 794ffe435e)

- Run: CI for PR #1499, `pull_request`, head `794ffe435e14276a88d918fd9cc5029ae1f6afc7`, terminal `completed/success`.
- 26 jobs terminal with 0 failures / 0 non-success: `14 success` + `12 skipped` (the skipped jobs are the legitimately non-applicable gates — Native Keycloak/Core, Targeted HA, Consumer/Pin pins, Exact Candidate, etc.), not a green native result.
- Key Go jobs on the exact head: `go-unit-tests` (job `128972510666`) and `deployment-package-tests` (job `128972510485`) both success; plus `go-build`, `go-vet`, `cli-gofmt`, `runtime-provider-package-tests`, `Focused Python`, `Source format`, `Native impact selection`, `Trusted Plan` all green. Native destroy-retry `docker` (job `128972485210`) and `podman` (job `128972485289`) both executed and passed.
- This lane's write-set (`cmd/baha/app_lifecycle_damaged_state_test.go`, `internal/deployment/damaged_namespace_network_test.go`) is test-only and does not touch any native runtime path; no 172-marker red, no external STATE. Terminal green with no red checks.
- CI was triggered by the authenticated push of this single integration candidate to the PR branch (standard `pull_request` trigger) — no workflow rerun, dispatch, or `.github/**` edit.

## Drift integration

- develop HEAD held at `b3a8042d18ea60f162a32a51df34a499cad6a237` (no drift; the r5 #1502 rebase trigger has not landed). The candidate chain integrates the current develop tip.
- Base attestation: `3187cea15728143146905c7238ad6e280ca11b3e` is an ancestor of `794ffe43` (merge-base --is-ancestor exit 0); develop `b3a8042d1` is an ancestor of `794ffe43`.
- One integration candidate per chain: single branch `0427-159-damagedstate`; branch log `3187cea15..794ffe43` lists only the 4 chain commits (r2 `61f69c20`, F1 `79f1a8f1`, F2/F3 `43fab0e5`, F1/F2 test proof `794ffe43`) on top of develop — no foreign candidate commit.

## Scope and evidence integrity

- No `.github/**` edit, no rerun, no workflow_dispatch, no force-push beyond the single candidate branch, no container/compose started on any host.
- Subagents: none (4.8) — every step executed inside this own session.
- Live source verified via a fresh clone (`/tmp/opencode/0427-159-r5-bh`, exact head `794ffe43`) and the single candidate chain; no quarantined/stale checkout cited.
- No markdown checkbox lines anywhere in this evidence file (plain bullets only).

## Run

- Evidence published to baseharbor-plan `origin/main`: `git ls-remote origin main` witness pasted below.
- Product candidate: branch `0427-159-damagedstate` (PR #1499) head `794ffe435e14276a88d918fd9cc5029ae1f6afc7`; base `3187cea15` and develop `b3a8042d1` both ancestors; `develop..HEAD` contains only the 4 chain commits.
- Hosted CI run `42559458982` terminal `completed/success` (26 jobs, 0 failures).
- No markdown checkbox lines in this evidence file.

### Planning repo witness (origin/main)

```
$ git ls-remote origin main
<SHA>\trefs/heads/main
```

### Product chain witness

```
$ git ls-remote origin refs/heads/0427-159-damagedstate
794ffe435e14276a88d918fd9cc5029ae1f6afc7\trefs/heads/0427-159-damagedstate
$ git ls-remote origin refs/heads/develop
b3a8042d18ea60f162a32a51df34a499cad6a237\trefs/heads/develop
$ git merge-base --is-ancestor 3187cea15728143146905c7238ad6e280ca11b3e 794ffe43 && echo base-ancestor-ok
base-ancestor-ok
$ git log --oneline origin/develop..794ffe43
794ffe43 test(cmd/baha, internal/deployment): F1/F2 production-path proof for no-false-attribution
43fab0e5 fix(cmd/baha, internal/deployment): F2 validate directory names + F3 no-false-attribution ...
79f1a8f1 fix(cmd/baha, internal/deployment): enrich registry damaged-state error with verified network half ...
61f69c20 fix(cmd/baha, internal/deployment): report missing workload network in damaged-state detection ...
b3a8042d fix(r27): target delete honors --yes on non-TTY ...
```

## END

END_DONE 0427-159-r5: F1 two-case proof (owned-app exact network via production path + ownerless foreign-orphan no-attribution) and F2 boundary regression (valid-UUID damaged visible, malformed discarded, record/dir mismatch rejected) added as test-only regressions; both CI-covered in `go-unit-tests` + `deployment-package-tests` (no `.github/**` edit); integrate develop `b3a8042d1` (no drift); single chain; pushed to PR #1499 head `794ffe435e`; hosted CI run `42559458982` terminal success (26 jobs, 0 failures, native Keycloak/Core skipped); evidence published to `origin/main` before END.
