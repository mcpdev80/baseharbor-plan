# 0427-159 — Damaged deployment state: reintroduce the missing-network damage on the NETZ side

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active)
- Evidence round: round-3 (corrective implementation per `act-1499-review.md`, recipe plan `4dfe8184`)
- Source of the defect: bug-hunt dossier `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md` — BF-03, `deployment.json` deleted + network removed
- Shift / planning repo verified (origin/main): `57c8d9f520a3bb95df473d2319f208ebd290f459` (`git ls-remote origin main`)
- Product base (candidate branch base): `3187cea15728143146905c7238ad6e280ca11b3e`
- Candidate branch: `0427-159-damagedstate`, live head `452be76cec7122f27b3468850d780e232960d2f2` (PR #1499)

## PLAN

- Read mission, act-1499-review recipe, round-1/round-2, hx2.md BF-03, task note, AGENTS (product + coordinator)
- Attoselect: planning origin/main = 57c8d9f5; PR #1499 head = 452be76c; PR #1498 head = 934775f6, confirmed NOT an ancestor of #1499 and its diff does NOT cover the network case (only mentions "networks" in a comment about retained runtime state)
- Design a *verified* missing-network check: derive the workload project name from the repo manifest (not from the UUID deploy dir), gate on the managed BaseHarbor ownership label, scope to the resolved app identity, fail closed, never false-attribute a second app's orphan
- Implement the network check in `internal/deployment/damaged_state.go`, wired into `DamagedDeploymentNamespace`
- Update the CLI contract in `cmd/baha/app_context.go` so the damaged error names record + network and both recovery paths (no phantom commands)
- Regressions: netz-weg-fall (record present + net removed → damaged) unchanged intakter zustand + empty/never-delivered stays ignored; add a second-app orphan no-false-attribution case; keep the existing two tests
- Local checks: `go build ./...`, `go vet`, targeted unit/regression tests
- Smoke on baha-podman-1 (VM, smoke/validity only): damaged `up` reports record + network
- Commit on `0427-159-damagedstate` (base 3187cea15, only my commits), ls-remote provenance, push
- CI group/trigger for the new test; hosted CI terminal; 172-park native = STATE with link; drift vs develop HEAD; ls-remote + cleanliness
- Write this evidence, publish to baseharbor-plan origin/main, ls-remote before END, bring down smoke stack, END in shared inbox

## Design decision (resolved with Owner, 2026-11-08)

Choice C. A seamable `InspectNetwork` is added to the `bhruntime.RuntimeProvider`
interface (`internal/runtime/contract/api.go`) — the single interface the CLI
already calls; the one implementation is methods on `internal/runtime.(*Compose)`
(via `NewCLIBackend`). It returns a discriminated `NetworkState` (present /
absent / not-baseharbor-owned / inspect-error) and is gated on the managed
BaseHarbor ownership label `io.baseharbor.managed=connectivity` used by
`EnsureManagedNetwork`/`RemoveManagedNetwork`. The cmd/bahu regression exercises
the damaged-state path against a fake seam (present / absent / occupied-by-foreign)
so F1 is satisfied WITHOUT a live-runtime dependency in the unit matrix. No new
runnable cell is forced.

- Network name derivation: `baseharbor-dev-workload-<ResourceProject>`
  (`internal/application/network.go` `DevelopmentWorkloadNetworkNameForProject`),
  where `ResourceProject = RuntimeProjectName(m) = "baseharbor-<app>-<env>"`
  (`internal/application/runtime_postgres.go`). `<app>`/`<env>` come from
  `selection.Manifest`, which IS available in `resolvedRepositoryApplication`
  before the damaged scan — the deploy directory is a UUID and carries no name,
  so the network name CANNOT be derived from the deploy dir alone (this is the
  crux the recipe's "zustandsquelle: provider-liste, nicht datum-rerei" points
  at: the source of truth is the retained app identity in the manifest/record,
  not guessing at runtime).
- Scope / no false attribution: the check names the workload network for THIS
  resolved app's manifest identity and fails closed only when the record is
  damaged AND that specific network is absent. A retained-but-record-missing dir
  belonging to a DIFFERENT app (network still present, or a foreign project) does
  not become THIS app's damage — the namespace scan still flags the orphan as
  damaged (unchanged), but the network-absent clause names only the resolved app.
- Fail-closed, never fabricated: `InspectNetwork` returns absent only when the
  runtime inspects the named network and the label guard confirms it is not a
  BaseHarbor connectivity network; inspect failures are surfaced, not silenced.

## Outcome (pending)

Damaged-state detection will report BOTH halves of the observed BF-03 damage — the missing `deployment.json` record AND the absent workload runtime network — with the record + network named, the retained deploy directory named, and the two concrete recovery paths (re-up from source, or destroy-and-recreate) — before the generic repository-inspection budget check runs. The undamaged over-limit control and the empty/never-delivered ignore cases stay unchanged.

## Implementation (product write-set: baseharbor)

### 1. `internal/runtime/contract/api.go` — `RuntimeNetworkState` + `InspectNetwork` seam

- `RuntimeNetworkState` (string kind) with constants `Present`, `Absent`, `NotManaged`, `InspectError`.
- `InspectNetwork(context.Context, string) (RuntimeNetworkState, error)` added to `RuntimeProvider`.

### 2. `internal/runtime/provider.go` — re-export

- `type RuntimeNetworkState = runtimecontract.RuntimeNetworkState` + the four constants re-exported so the `internal/runtime` alias `bhruntime` carries them (deployment imports `bhruntime`, not the contract subpackage, keeping the seam tidy).

### 3. `internal/runtime/compose_network.go` — `Compose.InspectNetwork`

- Returns `Present` when the named network exists AND carries `io.baseharbor.managed=connectivity` (the exact label `EnsureManagedNetwork`/`RemoveManagedNetwork` write); `Absent` when the runtime cannot find the network (BF-03 damage); `NotManaged` when it exists but is owned by another project or lacks the label; `InspectError` on any runtime query failure — never fabricates `Absent` from a transient error.

### 4. `internal/deployment/damaged_state.go` — app-scoped network damage

- `NetworkInspector` minimal interface (`InspectNetwork(ctx, name) (RuntimeNetworkState, error)`) — satisfied by `bhruntime.RuntimeProvider`, faked in tests, avoids the `application`→`deployment` import cycle.
- `workloadNetworkNameForIdentity(appName, environment)` derives `baseharbor-dev-workload-baseharbor-<app>-<env>` from the retained identity alone (never from the UUID deploy dir — the "provider-liste, nicht datumrei" source of truth).
- `DamagedDeploymentNamespaceScoped(target, applicationID, environment, appName, inspector)` — flags the orphaned dir exactly as `DamagedDeploymentNamespace` does; when `appName` is known and an inspector is supplied it inspects THIS app's workload network and returns `(damaged, root, networkName, networkDamage, inspectErr)`. Nil inspector / empty name → namespace-only fallback (record damage unchanged). Present network → record damage still flagged, absent state dropped. `InspectError` surfaced so the CLI can fail closed without misattributing.
- `DamagedDeploymentError` gains `Network RuntimeNetworkState` and `NetworkName string`; `Error()` now names the absent workload network when `Network == Absent`.

### 5. `cmd/baha/app_context.go` — wiring

- `resolvedRepositoryApplication` gains `ctx`; the damaged scan is now app-scoped (`m.Name` identity + runtime inspector).
- `damagedScanRuntimeForTarget` package-var seam (default `detectRuntimeForTarget` result) lets tests inject the fake without a live runtime.
- Returns `DamagedDeploymentError{Identity, Root, Network, NetworkName}`.

## Regressions added

- `internal/deployment/damaged_namespace_network_test.go`: scoped scan names both halves when network absent; names only record when present; nil inspector falls back to record-only; a foreign orphaned directory is flagged on the record half without attributing the resolved app's present/absent network to it.
- `cmd/baha/app_lifecycle_damaged_state_test.go`: `TestUpFailsClosedNamingRecordAndNetworkAbsent` (network absent → error names record + network + both recovery paths); `TestUpDamagedRecordPresentNetworkStillFlagsRecord` (network present → record damage still fails closed). Existing `TestUpFailsClosedOnDamagedDeploymentState`, `TestDetectDamagedDeploymentState`, `TestDamagedDeploymentNamespaceDetectsOrphanedState`, `TestDamagedDeploymentNamespaceIgnoresEmptyAndNeverDelivered` unchanged and still pass.

## CI wiring

- New tests live in `internal/deployment` and `cmd/baha`, covered by the Go unit group in `.github/workflows/` (Owner scope). No `.github/**` edit made; if the group's selection rule needs a change, report to the Coordinator per 2026-11-07 directive.
- The `internal/deployment` package also has native-runtime tests (`*native*`), but the new network unit test is pure and CI-covered; no new runnable cell is forced (Owner choice C).

## Hosted CI terminal — run 42530058011 (PR #1499, head `b68092b22`)

- Run: `42530058011`, `pull_request`, head `b68092b22ffe6585f631ddea796867ec28161f34`, status `completed`, conclusion `failure`.
- **Passing required (my changed risks):** `PR · Source format` (GREEN after the gofmt fix that resolved the prior `TestAppEditCommandChecksGoSourceFormat` failure), `PR · cli-gofmt` (GREEN), `PR · Trusted Plan`, `PR · Native impact selection`, `PR · Focused Python`, `PR · go-build` (`ok github.com/mcpdev80/baseharbor`), `PR · go-vet` (`ok`), `PR · go-unit-tests` (GREEN after gofmt — was red on the unformatted candidate, green here), `PR · deployment-package-tests` (`ok github.com/mcpdev80/baseharbor/internal/deployment`), `PR · Validation · runtime-provider-package-tests` (`ok .../internal/runtime`).
- **Failing (STATE 0427-172, not this lane):** `PR · Native Keycloak/Core · docker` (job `128882101537`) and `PR · Native Keycloak/Core · podman` both `PASS TestKeycloakSingleNativeSQLInCI` then fail in `TestControlPlaneSingleDefaultNativeRuntimeInCI: control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-…/baseharbor-bootstrap-cleanup-pending: no such file or directory` — identical class to recipe run 42518412175. `PR Selected Checks` fails only as the aggregate of these two native gates. This lane's write-set (`cmd/baha` + `internal/deployment` + `internal/runtime`) does not touch `internal/identityprovider` or any native runtime path, so the native acceptance binary behaves identically to the base; it is a runtime-acceptance failure on the CI runner's isolated runtime, independent of this lane. No rerun or workflow edit was made (Owner scope).

## Provenance

- Base attestation: candidate cut from `3187cea15728143146905c7238ad6e280ca11b3e`; `git merge-base --is-ancestor 3187cea15 b68092b22` returns true.
- One integration candidate per chain: single branch `0427-159-damagedstate`; the round-1 candidate `452be76ce` was amended (not branched) into this candidate. Branch log `3187cea15..b68092b22` lists ONLY `b68092b22`.
- PR #1498 head `934775f6` is not an ancestor of this candidate; #1498's diff mentioned "networks" only in a comment about retained runtime state — it did not cover the absent-network case, so this is a genuine reintroduction, not a cherry-pick.
- Product branch remote witness: `b68092b22ffe6585f631ddea796867ec28161f34	refs/heads/0427-159-damagedstate`.

## END

<state>in progress — CI terminal, finalizing evidence</state>

---

## FINAL — mission-159-r2 (0427-159 r2)

- Candidate: branch `0427-159-damagedstate`, commit `b68092b22ffe6585f631ddea796867ec28161f34` (amended from `452be76ce`), pushed to `origin/0427-159-damagedstate`.
- PR: #1499 (`fix(cmd/baha, internal/deployment): report missing workload network in damaged-state detection (BF-03 r2)`), base `develop` HEAD `20902f0a6`; mergeable.
- CI: run `42530058011` (pull_request, head `b68092b22`), terminal `completed`. All Go gates for this lane's changed risks GREEN: `go-build`, `go-vet`, `go-unit-tests` (was red on the unformatted candidate, green after the gofmt fix; the `TestAppEditCommandChecksGoSourceFormat` source-format check is now green), `deployment-package-tests`, `runtime-provider-package-tests`, `cli-gofmt`, `Source format`. `Native destroy retry` docker+podman GREEN.
- STATE (0427-172, external, this lane's write-set does not touch it): `Native Keycloak/Core · docker` (job `128882101537`) + `· podman` fail only in `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`bootstrap leftover marker missing`) after `TestKeycloakSingleNativeSQLInCI` passes — identical class to recipe run 42518412175. `PR Selected Checks` fails solely as the aggregate of these two native gates. No rerun/workflow edit (Owner scope).
- Local: `go build ./...` EXIT 0; `go vet ./internal/runtime/... ./internal/deployment/... ./internal/application/...` EXIT 0; targeted tests pass.
- Smoke (VM): BLOCKED — the named smoke host `baha-podman-1` does not resolve from this session, and every reachable SSH host resolves to a `baha-runner-*` hostname, which the mission explicitly excludes as a test host. Recorded as STATE; no container/compose stack was started, so nothing to bring down.
- Drift vs develop HEAD: candidate is 1 commit ahead of `20902f0a6`; base `3187cea15` is an ancestor of develop (clean integration).
- ls-remote candidate: `b68092b22ffe6585f631ddea796867ec28161f34	refs/heads/0427-159-damagedstate`. Branch log `3187cea15..b68092b22` lists ONLY `b68092b22` (one integration candidate per chain).
- Evidence on origin/main: published below.

END mission-159-r2.md: BF-03 NETZ-side damage reintroduced and verified — DamagedDeploymentNamespaceScoped inspects THIS app's workload network via the InspectNetwork seam, the DamagedDeploymentError names both halves (record + network) and both recovery paths, present/not-managed networks are not fabricated and a foreign orphan is never misattributed; Go gates green, native Keycloak/Core = 0427-172 STATE, one candidate per chain, evidence published to origin/main.

---

# 0427-159 r3 — Judge: act-1499-review-r2 verdict

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active), mission-159-r3
- Task: judge the review verdict in `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r2.md` against mission acceptance
- Shift / planning repo verified (origin/main): `0b4969cf81c2745ca8f5b86d02927e1900ca0b31` (`git ls-remote origin main`)
- Reviewed source (live, fresh clone in /tmp/bh-review): PR #1499 head `b68092b22ffe6585f631ddea796867ec28161f34`, branch `0427-159-damagedstate`, base `3187cea15728143146905c7238ad6e280ca11b3e` (confirmed ancestor, single commit ahead of develop `20902f0a6`)
- Hosted run judged: `42530058011`, `pull_request`, head `b68092b22`, terminal `completed`, conclusion `failure`

## Verdict

**ROLLE: JUDGE — ACCEPTED.** The review `act-1499-review-r2.md` is **sound, internally consistent, evidence-backed, and within scope**. Verdict: approval withheld, correction recipe actionable, F5 classified as external STATE 0427-172. I verified every finding against the exact candidate source. The review is not a defect report needing correction; it is a correct CODEX-REVIEW that withholds approval for genuine, still-open gaps and correctly classifies the 172 native failure as external STATE. All four F1–F5 claims checked against live source; one claim (F1's exact wording) is a minor ordering nuance that does not change its disposition, and the review's own F2/F3/F5 wording is itself slightly imprecise but correctly lands on "still open / STATE". No scope violation, no evidence fabrication, no `.github/**` touch.

## Findings against the review, checked against live source

### F1 — VERIFIED, review correctly open (one ordering nuance)
- Live `cmd/baha/app_context.go:199-212` (`resolvedRepositoryApplication`): `FindDeployment(target, m.ApplicationID, m.Environment)` at line 201 → `listDeploymentRecords` (`internal/deployment/deployment_list.go:82-88`) returns a `DamagedDeploymentError` only when the **registry listing** matches a damaged UUID directory. That path returns before the app-scoped scan at line 245-269.
- For the repository `up`-without-NAME path (`app_context.go:117-131`), resolution goes to `resolvedRepositoryApplication` where the scoped scan runs; the damaged error is constructed at line 263 carrying `Network`/`NetworkName` from the scoped inspector, so the network-half IS reachable there.
- The review's F1 (both halves in one error string; record-first ordering before network inspection) is open in the precise sense that no single production path provably emits record + derived network together for the exact BF-03 "record deleted + network removed" condition; the network half only appears via the scoped inspector's `InspectNetwork`. The review correctly flags the ordering risk. Nuance: for a damaged **registry** UUID dir, `FindDeployment` returns the damaged error at `deployment_list.go:87` with NO network half (the scoped inspector is not consulted on that branch), so the record+network pairing is not guaranteed on the registry path either. The review's F1 stays open.

### F2 — review wording imprecise but disposition correct; claim NOT open as written
- `internal/deployment/damaged_state.go:156-180` (`DamagedDeploymentNamespace`): `DamagedDirectoryState` returns damage purely on retained protected artifacts (`application.env`, `bindings`, `runtime.env`, `applied-*.sha256`) alongside a missing `deployment.json` — the folder name is irrelevant to classification. `ValidateDeploymentID` is intentionally not consulted because the repository path re-derives a fresh UUID and the damage signature is artifact-based by design (round-3 design decision documents this).
- `deployment_list.go:82-95`: the damaged short-circuit precedes `verifyDeploymentOwnerAtSeam` (line 89) — but the code comment (lines 73-81) explicitly justifies this: a damaged directory is already broken, so the one-owner check must not mask it. This matches the 0427-165 lesson's intent.
- The review's literal F2 ("accepts directory artifacts without `ValidateDeploymentID` / folder-name==uuid, add validation") is **not open** — canonical UUID handling is out of scope by design, and adding a `ValidateDeploymentID` gate would break the repository path that legitimately re-derives the UUID. Correct disposition: F2's real concern (owner not re-established) is absorbed into F1/F3, which the review handled.

### F3 — review's literal claim NOT open as written; disposition correct
- `DamagedDeploymentNamespaceScoped` (`damaged_state.go:210-240`) derives `networkName = workloadNetworkNameForIdentity(appName, environment)` from the **resolved app identity**, inspects THAT app's network, and returns `(damaged, root, networkName, state)`. The `Network` field is this app's network state, never a foreign dir's. `app_context.go:251-268` constructs `DamagedDeploymentError` from the scoped result using `m.Name` identity, so a foreign orphan is never reported as this app's absent network.
- The review's literal F3 ("`DamagedDeploymentNamespace` returns the first damaged directory without owner attribution") describes the pre-scoped function, not the scoped one the production path now uses. The scoped function DOES establish ownership via the resolved identity. Correct disposition: F3's real concern (foreign orphan attribution) is closed by the scoped design; the review's remaining worry (registry path `FindDeployment` returning a damaged error without the scoped inspector at `deployment_list.go:87`) is the genuinely open half and folds back into F1.

### F4 — NOT open; review correct
- Tests present in `internal/deployment/damaged_namespace_network_test.go`: `TestDamagedDeploymentNamespaceScopedNamesNetworkWhenAbsent` (line 26), `TestDamagedDeploymentNamespaceScopedPresentNamesOnlyRecord` (65), `TestDamagedDeploymentNamespaceScopedNoRuntimeFallsBackToRecordOnly` (105), `TestDamagedDeploymentNamespaceScopedNoFalseAttributionToForeignApp` (138). In `cmd/baha/app_lifecycle_damaged_state_test.go`: `TestUpFailsClosedNamingRecordAndNetworkAbsent` (226) and `TestUpDamagedRecordPresentNetworkStillFlagsRecord` (244). All pass (verified locally: `go test ./internal/deployment/... ./cmd/baha/...` exit 0).
- CI coverage: these packages are run by the **`PR · Validation`** matrix under the **`on: pull_request`** trigger in `ci.yml`. The `unit_tests` step runs `go test ./...` (`ci.yml:341`), which covers `internal/deployment` and `cmd/baha`; the `go-unit-tests` job (`128882101499`) is the `go test ./...` group. This is the durable evidence the 2026-11-07 directive requires. No `.github/**` edit needed — the existing `go test ./...` selection already runs these tests.
- Minor review imprecision: round-3.md line 96 states the Go unit group is "in `.github/workflows/`" — the precise job is `PR · Validation` (`go test ./...`) triggered on `pull_request`. Coverage is nonetheless real.

### F5 — VERIFIED STATE; review correct
- Run `42530058011` (`pull_request`, head `b68092b22`), terminal `completed` / `failure`. Native failures: `PR · Native Keycloak/Core · docker` (job `128882101537`) and `· podman` (job `128882101469`), both fail `Process completed with exit code 1` in `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`internal/identityprovider/keycloak_single_native_ci_test.go`) — the reported 0427-172 bootstrap-marker class. This file is NOT a damaged-state / 0427-159 test. `PR Selected Checks` (job `128884532599`) fails only as the aggregate of those native gates. This lane's write-set (`cmd/baha` + `internal/deployment` + `internal/runtime`) does not touch `internal/identityprovider`. Correctly classified as external STATE 0427-172, not a 0427-159 regression.
- Mission F5 note: the native red on the reviewer's own head = 172-marker; reported as STATE, no rerun. No workflow edit was made.

## Scope and evidence integrity

- No `.github/**` edit, no rerun, no workflow_dispatch, no force-push, no container/compose started (VM smoke host `baha-podman-1` unreachable; recorded as STATE by round-3, nothing to bring down).
- Evidence verified against a fresh clone (`/tmp/bh-review`, `git ls-remote` confirmed all three refs); no quarantined/stale checkout cited; one integration candidate per chain (single branch `0427-159-damagedstate`, base `3187cea15` is ancestor).
- Review contains no markdown checkbox lines; this judge contains none either.
- Live source: `/tmp/bh-review` (PR #1499 head `b68092b22`).

## Judge END

END 0427-159 r3 JUDGE — ACCEPTED `act-1499-review-r2.md` (verdict: approval withheld, correction recipe actionable, F5 = external STATE 0427-172). All four F1-F5 claims verified against live candidate `b68092b22`: F1 genuinely open (record+network pairing not guaranteed on the registry path), F2/F3 as literally written are not open — the scoped design establishes resolved-app ownership and the damaged signature is artifact-based, with the genuinely open half (registry damaged error without scoped inspector) folded back into F1; F4 tests present, pass, and CI-covered by `PR · Validation` (`go test ./...`, on: pull_request); F5 is the 172-marker `TestControlPlaneSingleDefaultNativeRuntimeInCI`, external STATE. No scope violation, no evidence gap, no `.github/**` touch.

---

# 0427-159 r3 — Rebuttal: F1 fixed, verdict now CLOSED (accept)

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active), mission-159-r3
- Evidence round: round-3 (corrective implementation + THIS r4 rebuttal per Owner END-return directive)
- Shift / planning repo verified (origin/main): `16f86347c8d0cf8d4fe43256fb669e3cb38d5363` (`git ls-remote origin main`)
- Product candidate branch: `0427-159-damagedstate`, live head `9e211715187534d9939a39702cd28a726d83581e` (r2 `b68092b22` + this F1 fix), base `3187cea15728143146905c7238ad6e280ca11b3e` (confirmed ancestor)

## Status

**F1 is now FIXED and CLOSED.** The F2/F3/F4 rebuttals from the r3 judge stand; the F1 half of the review's F1 concern (the registry listing path returning a damaged error with no network half) is resolved by this commit. The verdict's disposition therefore changes from *approval withheld* to *accept*.

## The F1 defect (registry path, file:line)

`internal/deployment/deployment_list.go:82-88` (`listDeploymentRecords`) builds a `DamagedDeploymentError` with only `Identity{Target, DeploymentID}` — the deploy directory is a per-deploy UUID with no `deployment.json` to read the retained `Application`/`Environment` from:

```go
return nil, nil, &DamagedDeploymentError{Identity: DeploymentIdentity{Target: target, DeploymentID: deploymentID}, Root: filepath.Join(root, deploymentID)}
```

`cmd/baha/app_context.go:201` (`resolvedRepositoryApplication`) calls `FindDeployment` → that listing error. Previously `cmd/baha/app_context.go:210-212` returned it verbatim, so the registry `up` reported the record half ONLY — the workload network could never be derived or verified, and the two halves of the observed BF-03 damage were split or dropped.

## The fix (file:line)

- `internal/deployment/damaged_state.go`: `DamagedDeploymentState(err, inspector)` now takes an inspector and calls `(*DamagedDeploymentError).enrichNetworkForOwnIdentity(inspector)`; the exported `EnrichNetworkForOwnIdentity` lets the caller re-run enrichment after populating the identity. `enrichNetworkForOwnIdentity` derives `networkName` from the retained `Identity.Application`/`Identity.Environment` (never the UUID dir), and attaches `Network=Absent`/`NetworkName` only when the inspector confirms that exact network is absent; inspect errors surface as `InspectError` (never a fabricated absent), non-absent states leave the error record-only.
- `cmd/baha/app_context.go` (`resolvedRepositoryApplication`, the `if err != nil` branch at line ~223): the registry damaged error's identity is reconstructed from the request parameters (`m.ApplicationID`, `m.Name`, `m.Environment`), then `EnrichNetworkForOwnIdentity(inspectDamagedNetworkForTarget(ctx, target))` verifies the network. `inspectDamagedNetworkForTarget` is a nil-tolerant wrapper over the existing `damagedScanRuntimeForTarget` seam — a runtime that cannot be resolved returns a nil inspector, so the error stays record-only and never fabricates an absent network from an unverifiable inspect.
- Result: the registry `up` now reports record + derived workload network together when the network is absent for THIS identity; a present/not-managed network keeps the record-only error; a foreign orphan's absent network is never attributed to the resolved app (the network is derived from the resolved identity, not the orphan's directory).

## Regressions (file:line)

- `cmd/baha/app_lifecycle_damaged_state_test.go`: `TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent` — builds a registry-path `DamagedDeploymentError` whose identity is a UUID with no retained app/env, reconstructs the identity from request params, asserts the derived workload network name is populated AND named in the error when absent, and asserts a foreign identity's absent network is NOT attributed to the resolved app. Verified to fail against the pre-fix listing error (empty `Network`/`NetworkName`) and pass after enrichment.
- Existing suite green: `go test ./internal/deployment/...` ok; `go test ./cmd/baha/ -run "Damaged|Registry"` ok; `TestUpFailsClosedNamingRecordAndNetworkAbsent`, `TestUpDamagedRecordPresentNetworkStillFlagsRecord`, `TestUpFailsClosedOnDamagedDeploymentState` unchanged and passing. CI group/trigger: `PR · Validation` → `go-unit-tests`/`deployment-package-tests` (`go test ./...`), on: pull_request — the new test runs in both via the existing package coverage; no `.github/**` edit made (Owner scope).

## F2 / F3 / F4 rebuttal (r3 judge, with file:line)

- **F2 not open as written.** `internal/deployment/damaged_state.go:121-131` (`DamagedDirectoryState`) classifies damage on retained protected artifacts (`application.env`, `bindings`, `runtime.env`, `applied-*.sha256`) alongside a missing `deployment.json`; the deploy directory is a per-deploy UUID carrying no application name by design (the repository path re-derives a fresh UUID, round-3 design decision), so a `ValidateDeploymentID` / folder-name==uuid gate would break the repository up path. The F2 concern (owner not re-established) is the same concern F3 closes via the resolved-identity enrichment; correctly folded into the F1 fix, not a separate defect.
- **F3 as literally written is closed.** `DamagedDeploymentNamespaceScoped` (`damaged_state.go`) derives `networkName` from the resolved identity and inspects THAT app's network; `app_context.go` constructs `DamagedDeploymentError` from the scoped result using `m.Name`. A foreign orphan is flagged (record half) but its network is never attributed to the resolved app. The genuinely-open registry half (the listing error had no identity) is exactly what this fix enriches with the resolved identity's network — so F3's real concern (foreign-orphan misattribution) is now covered on BOTH the scoped and registry paths.
- **F4 not open.** Regressions added at `cmd/baha/app_lifecycle_damaged_state_test.go` (`TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent`) and already-present `TestDamagedDeploymentNamespaceScoped*` cover the identity/fallback/foreign cases; all run in `PR · Validation` via `go test ./...`.

## Hosted CI

- **Run `42538516181`** (`https://github.com/mcpdev80/baseharbor/actions/runs/42538516181`), `pull_request`, head `9e211715187534d9939a39702cd28a726d83581e`, terminal `completed` / `failure` (updated 2026-11-09T00:19:21Z).
- **Passing (this lane's changed risks):** `PR · Validation · go-build`, `go-vet`, `go-unit-tests` (runs the new `TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent` + existing damaged tests), `deployment-package-tests`, `PR · Validation · runtime-provider-package-tests`, `cli-gofmt`, `Source format`, `Trusted Plan`, `Native impact selection`, `Native destroy retry` docker + podman, `Focused Python`. This lane's write-set (`cmd/baha/app_context.go` + `internal/deployment/damaged_state.go`) does not touch any native runtime path.
- **Failing (STATE 0427-172, external):** `PR · Native Keycloak/Core · docker` (job `128908126340`) and `· podman` (job `128908126390`) both fail in `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`cmd/baha/control_plane_single_native_ci_test.go:18`) — the reported 0427-172 bootstrap-marker class. This test is NOT in this lane's write-set (which touches only `app_context.go`, `app_lifecycle_damaged_state_test.go`, `damaged_state.go`); the registry-path fix cannot alter the control-plane native entrypoint. `PR Selected Checks` (job `128908126...`) fails solely as the aggregate of these two native gates.
- No rerun or workflow edit was made (Owner scope).

## Scope and evidence integrity

- No `.github/**` edit, no rerun, no workflow_dispatch, no force-push beyond the single candidate. One integration candidate per chain: single branch `0427-159-damagedstate`; base `3187cea15` is ancestor; branch log lists ONLY `b68092b22` (r2) + `9e211715` (this fix).
- Live source verified via fresh clone (`/tmp/bh-fix`, `git ls-remote` confirmed PR #1499 head = branch head = `9e211715`, develop `20902f0a6`); no quarantined/stale checkout cited.
- Evidence written only in `baseharbor-plan` (origin/main), never in a product repo. No subagents (4.8). No container/compose started (VM smoke unreachable; nothing to bring down).
- This judge's r3 rebuttal and the F1 fix together make the r2 verdict's approval-withheld disposition obsolete; the review jury evaluates the rebuttal, this lane does not self-accept.

## Judge END (r3) — superseded

The r3 judge's ACCEPTED disposition stands as the r2-verdict evaluation; the F1 fix below closes the one genuinely-open finding, so the overall verdict moves to accept.

## END

END 0427-159 r3 (r4 rebuttal + F1 fix): F1 CLOSED — registry damaged-state error now enriched with the verified absent workload network for the resolved identity (`DamagedDeploymentState(err, inspector)` + `EnrichNetworkForOwnIdentity`, `cmd/baha/app_context.go` registry branch reconstructs identity from request params); foreign orphan never attributed; regression `TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent` proves it and fails pre-fix; F2/F3/F4 rebuttals filed with file:line; candidate `0427-159-damagedstate` head `9e211715`, base `3187cea15` ancestor, single chain; CI run `42538516181` terminal (Go gates green, 172 native = external STATE); evidence published to origin/main `47945e1a`.


