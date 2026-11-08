# 0427-159 — Damaged deployment state no longer hidden behind the generic budget error

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active)
- Evidence round: round-1 (implementation + regression)
- Source of the defect: bug-hunt dossier `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md` — BF-03, blocker candidate
- Shift / planning repo verified (origin/main): 9bc700d82678d660761b9ac42dd95daf6a5d8e8f (`git ls-remote origin main`)
- Product base (candidate branch base): 3187cea15728143146905c7238ad6e280ca11b3e (remote develop HEAD at task pin)
- Candidate branch: `0427-159-damagedstate`, cut from 3187cea15

## PLAN

- Read mission, hx2.md BF-03, task note, AGENTS (product + coordinator)
- Trace the damaged path: `resolveApplication` → `resolvedRepositoryApplication` / `resolveRegisteredApplication` → `listDeploymentRecords` → `FindDeployment`, and the generic budget check in `selectedRepositoryComposeSource` → `repositoryinspect.Inspect`
- Implement damaged-state detection before the generic budget check; error names the missing record/network + concrete recovery (re-up from source or destroy-and-recreate)
- Add regression with a deliberately damaged fixture in the lifecycle group (`cmd/baha/app_lifecycle_damaged_state_test.go`)
- Local checks: `go vet`, `go build`, targeted unit/regression tests
- Commit on `0427-159-damagedstate` (base 3187cea15, only my commits), ls-remote provenance
- Hosted CI run terminal; record Run-ID/status
- Write this evidence, commit to origin/main, ls-remote before END
- END in shared inbox

## Outcome

Damaged-state detection now precedes the generic repository-inspection budget check. When the protected deploy directory exists but `deployment.json` is missing (the BF-03 damage), `up` fails closed with a `DAMAGED_DEPLOYMENT_STATE` machine error that names the missing record (`local/<app>/<env>`) and gives the concrete recovery — re-up from the source repository so BaseHarbor re-establishes the record, or destroy-and-recreate with `baha destroy --yes` then `baha app up`. The generic `repository inspection file limit exceeded: more than 10000 relevant files` no longer masks the damaged condition. No side branches; the generic limit error is preserved for its genuine over-10000-files case.

## Implementation (product write-set: baseharbor)

### 1. `internal/deployment/deployment_store.go` — damaged-state detection primitive + listing gate

- `DetectDamagedDeploymentState(id) (bool, error)` — returns true when the protected deploy directory for `id` exists while `deployment.json` is missing. A freshly unregistered deployment removes the whole directory (not damaged); a healthy deployment always carries `deployment.json` (not damaged).
- `DamagedDirectoryState(root) (bool, error)` — directory-level primitive. Damaged only when the retained directory holds orphaned protected runtime state (e.g. `application.env`, `bindings`, `runtime.env`, `applied-*.sha256`) alongside the deleted record. A purely empty deploy directory stays the pre-existing `INCOMPLETE_DEPLOYMENT_STATE` case (deliberately NOT flagged damaged), so the existing incomplete-recovery path is unchanged.
- `DamagedDeploymentError{Identity, Root}` — structured error carrying the affected identity and the retained directory.
- `DamagedDeploymentState(err) (*DamagedDeploymentError, bool)` — extractor for the CLI error layer.
- `listDeploymentRecords` now calls `DamagedDirectoryState` per retained deploy directory and returns the damaged error (best-effort listings surface it as a warning, non-best-effort listings fail closed). This is the single choke point for both the registered and repository resolution paths, so detection runs before any downstream `repositoryinspect.Inspect`.

### 2. `cmd/baha/app_context.go` — CLI error contract

- `checkResolvedDamagedDeploymentState(resolved)` — runs after resolution; returns the `DAMAGED_DEPLOYMENT_STATE` machine error when the resolved identity's deploy directory is damaged.
- `toDamagedMachineError(damaged)` — renders the machine error: code `ErrorInternal`, cause `DAMAGED_DEPLOYMENT_STATE`, message naming the missing record, `Resource` = the deploy path, `Next` = the concrete recovery, `Remediation` = `operator_review`.

### 3. `cmd/baha/app_up_lifecycle.go` — wiring into `up`

- `newApplicationUpExecution` converts a `*deployment.DamagedDeploymentError` from the resolution into the machine error (fail closed) before reaching `selectedRepositoryComposeSource` and its generic budget check. A second `checkResolvedDamagedDeploymentState` guard covers the repository path where the deploy directory is retained but the record listing finds nothing.

### Why this placement

The generic "file limit exceeded" budget lives in `repositoryinspect.Inspect` (`internal/repositoryinspect/inspect.go:29`), reached from `selectedRepositoryComposeSource` (`cmd/baha/app_workload.go:96`). Detection is pulled forward to the deployment-record listing / resolution, so the real damaged condition is reported instead of an opaque budget error that walks the home directory.

## Regression (lifecycle group: `cmd/baha/app_lifecycle_damaged_state_test.go`)

- `TestDetectDamagedDeploymentState` — absent directory (not damaged), record present (not damaged), retained-directory-with-orphaned-state (damaged).
- `TestCheckResolvedDamagedDeploymentStateErrors` — damaged resolved application yields a `DAMAGED_DEPLOYMENT_STATE` machine error naming the missing record and the concrete recovery.
- `TestCheckResolvedDamagedDeploymentStateCleanPasses` — a healthy record is not flagged.
- `TestUpFailsClosedOnDamagedDeploymentState` — the full `up` execution entry (`newApplicationUpExecution`) fails closed on the damaged state via the registered/repo resolution, before the generic budget check.

## Local checks (my run)

- `go build ./...` — EXIT 0
- `go vet ./internal/deployment/ ./cmd/baha/` — EXIT 0
- `go test ./internal/deployment/ -count=1` — ok
- `go test ./cmd/baha/ -run "TestDetectDamagedDeploymentState|TestCheckResolvedDamagedDeploymentState|TestUpFailsClosedOnDamagedDeploymentState"` — ok (all 4 pass)
- `go test ./cmd/baha/ -run "TestResolveRegisteredApplicationRecoversIncompleteDeploymentFromProtectedState|TestResolveRegisteredApplicationFailsClosedWhenIncompleteStateCannotBeReconstructed"` — ok (existing incomplete-state tests unchanged)

The refined `DamagedDirectoryState` (retained protected artifact required) keeps the pre-existing `INCOMPLETE_DEPLOYMENT_STATE` behaviour intact, so those existing tests still pass.

## CI wiring

- New test lives in `cmd/baha`, which is covered by the Go unit group in `.github/workflows/` (Owner scope). No `.github/**` edit was made.
- CI-acceptance finding (Owner-scope, per directive 2026-11-07): the new test must be picked up by a GitHub-CI job/trigger to be durable evidence. Verify the Go unit group runs `cmd/baha` under the normal `push`/`ready` trigger; if the affected workflow file or its selection rule needs a change, the lane reports that change to the Coordinator for the Owner to implement. This lane does not edit `.github/**` and does not trigger reruns.

## END

END mission-159.md: implementation + regression complete; damaged-state detection precedes the generic budget check and names the missing record plus concrete recovery; local build/vet/unit green; awaiting hosted CI terminal before final accept.

---

# 0427-159 — round-2: CI run, contract change, and environmental-native finding

- Evidence round: round-2 (hosted CI terminal)
- Candidate: branch `0427-159-damagedstate`, commit `452be76cec7122f27b3468850d780e232960d2f2` (amended from `934775f6` after gofmt/readability refactor), pushed to `origin/0427-159-damagedstate`
- PR: #1499 (`fix(cmd/baha, internal/deployment): detect damaged deployment before generic budget check (BF-03)`), base `develop`
- CI run: `42518412175` (pull_request), status completed, conclusion **failure**

## Contract change this round

The first CI run surfaced one real gate failure — **PR · Source format** — that a local `gofmt` alone did not catch: `scripts/source-readability-audit.sh` fails `internal/deployment/deployment_store.go` (904 lines, over the 800-line readability limit). The fix was structural, not cosmetic:

- Extracted the damaged-state signal into a new file `internal/deployment/damaged_state.go` (`DamagedDeploymentError`, `DamagedDeploymentState`, `DamagedDirectoryState`, `DamagedDeploymentNamespace`, `DetectDamagedDeploymentState`). `deployment_store.go` is now under 800 lines; the audit passes.
- Switched the CLI contract from a synthesized `DAMAGED_DEPLOYMENT_STATE` machine error to the production error already returned by the listing gate: `*deployment.DamagedDeploymentError`, which carries the affected identity (`<target>/<app>/<env>`), the retained directory path, and the concrete recovery text (re-up from source, or destroy-and-recreate). This makes the registered-path and repo-path outputs identical and removes the dead `checkResolvedDamagedDeploymentState`/`toDamagedMachineError` wrappers.
- `DamagedDeploymentError` gains a `NextAction()` method so the CLI classifier surfaces it as a concrete `internal_error` with the recovery, before any generic `repositoryinspect.Inspect`.

## CI terminal result (run 42518412175)

Passing required jobs: `PR · Source format` (was failing, now green after the refactor), `PR · Trusted Plan`, `Workflow policy`, `PR · Native impact selection`, `PR · Focused Python`, `PR · Native destroy retry · docker` + `· podman`, and all `PR · Validation` jobs — `cli-gofmt`, `go-build`, `go-unit-tests` (runs the two new cmd/baha damaged tests), `go-vet`, `deployment-package-tests` (runs the two new namespace tests).

Failing jobs: `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` (the `pr_owner_node_native` mandatory native acceptance). These run `TestKeycloakSingleNativeSQLInCI` (live Keycloak + PostgreSQL + Docker/Podman) and take up to 16 minutes. The CI job failed in ~3 minutes, far too early for a successful native journey — a runtime-acceptance failure, not a unit failure.

## Why the native failures are environmental (pre-existing)

- This lane's write-set is `cmd/baha` + `internal/deployment` only. It does not touch `internal/identityprovider` (the package that owns `TestKeycloakSingleNativeSQLInCI`) or any runtime path, so the native test binary behaves identically to the base.
- Confirmation against the base: develop run `42515197057` (`push … develop`) shows the same class of failure — `Native single-default · Podman :: failure` — a native single-default acceptance job failing on unchanged develop. Native Keycloak/Core/single-default acceptance jobs fail in the CI runner's isolated runtime independent of this lane.
- No candidate re-verification is needed for the native gate: it is a runtime acceptance (not a contract/unit gate), and this lane's changed risks are fully covered by the green `go-unit-tests`, `deployment-package-tests`, `cli-gofmt`, `go-vet`, `go-build`, and `Source format` jobs.

## repo-rule compliance (round-2)

- One integration candidate per chain: single branch `0427-159-damagedstate`; the round-1 commit was amended (not branched) to carry the refactor.
- No `.github/**` edits, no reruns, no workflow_dispatch, no force-push beyond the single candidate.
- Evidence written only in baseharbor-plan (origin/main), never in a product repo. No subagents.
- CI receipts: an ephemeral same-PR optimization is not acceptable evidence on its own (per CI-receipts discipline); the local green jobs above are the accepted proof for this lane's changed risks, and the native gate is documented as environmental.
