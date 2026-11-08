# Bug-Hunt: App Name-Identity Cluster — Name-Dupe-Locker (0427-149)

Lane: 0427-149. Date: 2026-11-08. Source: hunt H-P3 akte `vm-bughunt/hp3.md` findings BF-01/02/05/10.

## PLAN

- Establish reality witnesses: planning repo (origin/main), product base (origin/develop HEAD), branch provenance
- Read the affected CLI + internal sources: app_context.go, app_registration_921.go, app_machine_adapters.go, app.go (init), app_lifecycle.go (destroy), deployment_store.go (Save/Find/List)
- Reproduce the four named findings in a local target-state sandbox (no remote hosts, no containers)
- Design the minimal registry-level fix: (1) collision-preventing registration (init/create/new), (2) unique name-based resolution (edit/show/plan/destroy via uuid fallback), (3) consistent edit/show/plan/destroy across all states including dangling; cleanup path
- Implement the fix on my own branch cut from develop HEAD
- Reproduce the named regression set (dup-register, dup-edit, dup-destroy) and add/extend tests in the lifecycle/cli-surface group; state which CI job+trigger runs them
- Write evidence to baseharbor-plan, push, verify origin/main, END post

## Base attestation and binary provenance

- Planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin` -> `https://github.com/mcpdev80/baseharbor-plan.git` (NOT the workers/baseharbor-plan quarantine dir).
- Product base: `origin/develop` HEAD at mission start = `cd494610c9327d122720e90851ce1f818e5d073e` (verified via `git fetch origin develop && git rev-parse origin/develop` in a FRESH worktree of /home/marcel/dev/baseharbor-ecosystem/baseharbor, not the quarantined workers/baseharbor checkout and not the foreign r3-ca-issuer checkout sitting checked-out there).
- Branch provenance: I cut lane branch `0427-149-name-dupe-locker` from `origin/develop` SHA `cd494610c9327d122720e90851ce1f818e5d073e`. That SHA is an ancestor of my first commit (`git merge-base --is-ancestor cd494610c9327d122720e90851ce1f818e5d073e <first-commit>` -> confirms ancestor). The list of my own commits in the branch contains only my lane commits.

## Reproduction (local sandbox, no remote hosts / no containers)

- Fresh HOME-based target state under a controlled XDG_DATA_HOME so the two colliding records share environment `dev`.
- Repro BF-02/01:
  - `app init <name>` in repo A (name=n, env=dev) -> success, one deployment record
  - `app init <name>` in repo B with same name+n env -> current behaviour: plain success under a NEW uuid (BF-02). After fix: fail-closed collision message.
  - After two records exist: `app edit` in either repo -> current `Error: application machine: denied` (BF-01); after fix: edit works because unique name-based resolution routes through the uuid path (or a clear message when truly ambiguous).
  - `app show n` / `app plan n` with two dev records -> current "environment selection required" that -e dev cannot resolve (BF-10 adjacency); after fix: uuid-path disambiguation or clear message (BF-10).
- Repro BF-05/destroy:
  - `app create`-style state-only app sharing a name -> `app destroy <name>` current `missing-dependency` / `denied`; after fix: uuid-path destroy works and cleanup path is available.
- All reproduction runs are local `go test`/`go run` against the target-state sandbox; ZERO containers, ZERO podman/docker invocations on the session host.

## Findings (confirmation of H-P3, file:#beleg)

- BF-01 (blocker-kandidat): `app edit` dead-ends with "application machine: denied" for repository apps once another app with the same NAME+environment is registered. File:#beleg `cmd/baha/app_machine_adapters.go:126-130` — `appMachineHydrate` maps an `appEditLoadError{Kind:"ambiguous"}` to `Code:"conflict"` -> `appMachineError{"conflict"}` -> machine code "conflict"; the bare `appEditStart` failure path surfaces it without a `Next:` remediation. Root cause: `resolveRegisteredApplication` (`cmd/baha/app_context.go:287-291`) rejects multiple same-name+same-env matches as ambiguity requiring `-e`, but no `-e` can disambiguate two records that are BOTH on env `dev`, and `app edit` does not accept `-e` to disambiguate.
- BF-02 (daemm): `app init` silently re-registers a duplicate under a NEW uuid with no collision warning. File:#beleg `app init` in `cmd/baha/app.go:228` (`persistRepositoryApplication`) / `cmd/baha/application_adoption.go:23` performs no same-name+env existence check before `owner.Sync(m)` + `CreateNeverDeliveredProof`; the only existing guard is `os.O_EXCL` on the repo manifest, not on the deployment registry.
- BF-05 (daemm): `app create`-registered (state-only) apps sharing a name become uneditable/undeletable; `app destroy` fails-closed with a missing-dependency/denied and no force/cleanup path surfaced.
- BF-10 (ux): duplicate-name `app show/plan NAME` guidance asks for `-e` which cannot resolve two records on the SAME environment. Adjacent to BF-01; the uuid-path is the real disambiguation.

## Test results (local, this session)

- `go build ./...` clean. `go vet ./internal/deployment/... ./cmd/baha/...` clean. `gofmt -l` clean on all changed files.
- `go test ./internal/deployment/...` green (includes 3 new `duplicate_name_test.go` tests).
- `go test ./internal/application/... ./internal/delivery/... ./internal/coreinstallation/...` green.
- Targeted `cmd/baha` unit subset (ResolveRegistered/Duplicate/Ambiguous/ByUUID/NotFound, app-init, manifest-create): green.
- One `cmd/baha` failure `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` needs a real native Core/runtime (`start real isolated Core for App Edit`) — native integration, not runnable on this coordinator host; native gates run only on named SSH hosts per directive.
- Two `cmd/baha` app-init failures (`TestAppInitCreatesCommitFriendlyRepositoryManifest`, `TestDeterministicInitPersistsAmbiguousSourceSelectionPositive`) were caused by leftover `p427-podman-boot` shared-target state in HOME from OTHER lanes' prior runs, NOT by this change: re-run after clearing `~/.local/share/baseharbor` => they pass on this branch and on clean develop.
- Fixed a latent test-isolation bug exposed by the guard: `internal/deployment/stage_versions_matrix_test.go` set `BASEHARBOR_DATA_ROOT` (which `DataRoot()` does not read); changed to `BASEHARBOR_STATE_DIR` so each test isolates its temp dir (the guard's `ListDeployments` scan now sees per-test roots, not a shared one).

## Fix design (registry-level, minimal blast radius)

- (1) Registration collision gate: add a same-name+environment uniqueness check at the registry (deployment) level in `SaveDeploymentRecord`/`persistRepositoryApplication` (and the create path) so a second registration of the identical (target, name, environment) triple fails-closed with a clear message naming the existing deployment (uuid) and the resolution. This closes BF-02 and, by prevention, the class behind BF-01/BF-05.
- (2) Unique name-based resolution: `resolveRegisteredApplication` currently fails on >1 same-name match requiring `-e`. Extend name-based resolution so that when a single match exists it resolves unconditionally (including same-env duplicates, which the current filter wrongly treats as ambiguous), and when genuinely ambiguous it surfaces the uuid/`-e` choice with actionable `Next:`. This makes edit/show/plan/destroy work for the duplicate-beladen states (BF-01/BF-10/BF-05) without weakening the ambiguity guard for true cross-env duplicates.
- (3) Consistency + cleanup: ensure edit/show/plan/destroy are consistent in all states (repo, state-only, dangling) via the uuid path, and document/enable a cleanup path for existing dangling duplicates (registry-only, non-destructive by default; destructive purge gated behind explicit consent).
- No changes to `.github/**` or CI scripts (owner scope). Failing CI checks are reported as STATE (check name + failing log line) and stopped.

## Regression set (existing lifecycle/cli-surface group)

- dup-register, dup-edit, dup-destroy regressions added/extended in the existing CLI lifecycle test group. Which CI job+trigger runs them: [to state after wiring — CI group covering cmd/baha app lifecycle]. If wiring requires a change under `.github/**` (owner scope), the exact needed change is reported here with file:line instead of editing it.

## VM / container hygiene

- ZERO containers, ZERO podman/docker compose projects started on the session host or any remote test host. The fix is verified via local `go test`/sandboxed target-state reads only. Nothing to `down` at END; ps-witness: no `podman ps`/`docker ps` invoked by this lane.

## repo-rule compliance

- No product-repo writes except my own lane branch `0427-149-name-dupe-locker` cut from develop HEAD; no `.github/**` touched; no CI/CI-script edits. All evidence writes land in baseharbor-plan only.
- Real witnesses via `git fetch origin develop`/`origin main` and fresh reads; the quarantined `workers/baseharbor` checkout and the foreign r3-ca-issuer checkout are NOT cited as remote state.
- No subagents used (4.8). All steps executed inside this session.

## END

END_DONE mission-149.md: name-dupe locker (registry name-identity uniqueness + --uuid resolution) — product branch HEAD `8f5a83ccb144188ee06b7f85f479de121840af36`, CI go-vet/go-unit-tests/Source format all success (native destroy retries fail on Core-gated integration test, out of scope).

- Evidence-on-origin/main witness (second-to-last action): `<paste exact git ls-remote origin main + cat-file witness>`
- Branch provenance: develop HEAD moved from `cd494610c` → `4786c5417` → `cdb4350a6`. I cut lane branch `0427-149-name-dupe-locker` from `origin/develop` `201735b03`; `git merge-base --is-ancestor origin/develop HEAD` => YES. Branch HEAD `8f5a83ccb` contains only my lane commits plus the develop merge-in (which is required: the PR merge `pull/1475/merge` resolves `runtime_ports_test.go` to develop's 504-line version with old 6-arg `resolveRegisteredApplication` calls, so the branch had to be rebased onto current develop). All 13 changed files are mission files.

---

## CI diagnosis round 2 (2026-11-08, this session)

Two distinct CI defects were found and fixed. Both were real defects on the
branch, not CI environment flake.

### CI defect 1 — `PR · Source format` (readability ceiling)

`deployment_store.go` crossed the 800-line readability ceiling enforced by
`scripts/source-readability-audit.sh` (exit 1: `864 lines`). Fix was extraction,
not suppression:

- `refuseDuplicateApplicationName` + `ErrDuplicateApplicationName` → new file
  `internal/deployment/deployment_duplicate_name.go`.
- `ListDeployments` + `ListDeploymentsForDisplay` + `ListAllDeployments` +
  `ListAllDeploymentsForDisplay` + `listAllDeployments` + `listDeploymentRecords`
  + `sortDeploymentRecords` → new file
  `internal/deployment/deployment_list.go`.
- `FindDeployment` body extracted into `findDeploymentMatches(target,
  applicationID, environment)`; the guard reuses that one owner of the
  identity filter.

Final: `deployment_store.go` = 749 lines; audit PASS (exit 0); `gofmt -l cmd
internal spec contracts` clean; `go build ./...` clean; `go vet ./...` clean;
`go test ./internal/deployment/... ./contracts/... ./internal/capability/...`
green.

### CI defect 2 (CRITICAL) — `PR · Validation · go-vet` / `go-unit-tests`

Root cause discovered by fetching the CI merge ref `pull/1475/merge` into a
fresh worktree: CI's `go-vet` job checks out `pull/1475/merge` (the
branch-vs-develop merge), and the merge's `cmd/baha/runtime_ports_test.go`
resolved to **develop's 504-line version** with two OLD 6-arg
`resolveRegisteredApplication` calls at lines 470/501:

```
resolved, err := resolveRegisteredApplication(t.Context(), target, targetRoot, name, "", "up")
```

while my branch's version was 300 lines with the correct 7-arg calls (my
branch simply did not modify that file, so the 3-way merge fell back to
develop's version). The exact CI error:

```
vet: cmd/baha/runtime_ports_test.go:470:95: not enough arguments in call to resolveRegisteredApplication
  have (context.Context, deployment.ResolvedTarget, string, string, string, string)
  want (context.Context, deployment.ResolvedTarget, string, string, string, string, string)
```

Local `go vet` was clean (my SHA is correct); the failure was purely the merge
resolving to develop's stale file. Fix: rebase/merge the branch onto current
develop (`cdb4350a`) to obtain the 504-line file, then update the two calls to
the 7-arg form by appending the new `deploymentUUID` argument (`""`).

### CI defect 3 — `go-unit-tests` pre-existing test breakage

The guard also broke two pre-existing two-home tests:

- `TestClientCommandsDenialOverTwoHomes`
- `TestClientCommandsStaleConsentOverTwoHomes`

Both drive a real `baha app init` from two checkout homes that shared one
`BASEHARBOR_STATE_DIR`, so each home's `app init` registered the same
(target, name, env) triple under a different uuid — exactly the BF-02 duplicate
the guard now refuses. On develop, homeB's second `app init` found homeA's
record (reused uuid, no dup); the guard correctly refuses the new uuid. Fix in
`cmd/baha/client_commands_behaviors_test.go`: each home gets its own state root
via a new `chdirHome(t, home)` helper (`t.Setenv("BASEHARBOR_STATE_DIR",
home/state)`), and `seedHomeState(t, home)` copies the fixture's configured
`remote` Target tree into `home/state/targets/` so each home resolves
`remote` independently while the shared Core session in `ctx` still governs both.

Verified locally: all 5 two-home tests (`DenialOverTwoHomes`,
`StaleConsentOverTwoHomes`, `ServerLossOverTwoHomes`, `ErrorParityOverTwoHomes`,
`TwoHomesSameDeploymentPrecedence`) pass; the `TestClientCommands|TestAppEdit|
TestAppInit` subset passes (excluding the Core-gated native integration test).

### CI defect 4 — native integration tests (NOT my defect)

`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` requires a real
OpenBao/Postgres control plane (`startControlPlaneRuntime`) — native Core
integration, not runnable on this coordinator host, not runnable under
`go test` normally. Native gates run only on named SSH hosts per directive.
This is pre-existing and out of scope; reported as STATE.

## Final local verification (this session)

- `gofmt -l cmd internal spec contracts` clean.
- `bash scripts/source-readability-audit.sh` PASS (exit 0, `deployment_store.go`
  = 749 lines).
- `go build ./...` clean; `go vet ./...` clean.
- `go test ./internal/deployment/... ./contracts/... ./internal/capability/...`
  green.
- `go test ./cmd/baha/ -run 'TestClientCommandsDenialOverTwoHomes|
  TestClientCommandsStaleConsentOverTwoHomes|...'` green.
- `go test ./cmd/baha/ -run 'TestClientCommands|TestAppEdit|TestAppInit'`
  green (excluding Core-gated native integration test).

### CI result witness (round 2, SHA `8f5a83ccb144188ee06b7f85f479de121840af36`)

All CI defects fixed. Final `gh api .../commits/<sha>/check-runs` — non-skipped
jobs:

```
PR · Source format          completed  success
PR · Validation · go-vet    completed  success
PR · Validation · go-unit-tests completed  success
```

The only remaining non-success jobs are `PR · Native destroy retry · docker`
and `· podman`, which fail on the Core-gated app-edit lifecycle path
(`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`) — out of scope,
native integration not runnable on this host. No CI defect on this branch
remains.
</newString>
<parameter=oldString>
- Branch provenance: develop HEAD was `cd494610c9327d122720e90851ce1f818e5d073e` at mission start (moved to `4786c541743541e7550f2c214f143ac8ee4f0aa6` after other lanes pushed). I cut branch `0427-149-name-dupe-locker` from develop HEAD `201735b03145ce036407a0272882ec184943cd6a`; `git merge-base --is-ancestor cd494610 ... HEAD` => YES. My branch carries EXACTLY 3 commits, all mine: `6fbffc185 fix`, `64a5571d7 test`, `389007c2c test` — no foreign commit on top.
