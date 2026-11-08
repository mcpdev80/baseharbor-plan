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

