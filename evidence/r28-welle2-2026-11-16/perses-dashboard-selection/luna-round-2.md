# Luna batch12 REQUEST CHANGES — correction akte (worker w080-r2, 2026-11-16)

- Card: `t-20261114-r28-perses-dashboard-selection` · PR #1590 · lane `lane-0428-080-r28-perses-selection`
- Base candidate (acceptance SHA): `1873ba33f38bf7c21a21b4bdb19c8a1525b1785e` (PR #1590 head == branch head before correction)
- Correction candidate: `1781277d3356f0f52fb3bef242bb7f1074fba573` (one commit, clean FF over `1873ba33`)
- Reviewer verdict being corrected: CODEX-REVIEW Luna batch12 `act-luna-batch12.md` (origin/main), REQUEST CHANGES on `1873ba33`.
- Worker: `w080-r2` (lane `lane-0428-080-r28-perses-selection`)

## PLAN

- Reality check: `git ls-remote origin` (baseharbor + baseharbor-plan), PR #1590 head = lane `lane-0428-080-r28-perses-selection` = `1873ba33f`, clean FF ancestor.
- Read akte `act-luna-batch12.md` + owner decision `owner-round-1.md`; inspect `internal/capability/perses_selection.go` + `perses_selection_test.go` on the committed head.
- Reconcile the three PFLICHTEN against the committed candidate; decide the correction shape against the identity r3/r4 precedent.
- Implement the correction (two files only), run `go build`/`go vet`/`gofmt` + focused tests with a writable `TMPDIR`.
- Commit one FF correction, refspec-push, `git ls-remote` witness, push evidence to `origin/main`, ls-remote witness of the evidence path.
- Formless END post.

## Reality witnesses

- baseharbor remote heads (git ls-remote, this session):
  - `lane-0428-080-r28-perses-selection` == `refs/pull/1590/head` == `1873ba33f38bf7c21a21b4bdb19c8a1525b1785e` (base candidate).
  - baseharbor-plan `origin/main` == `4496226a3d9e6f76e9aca101aff0fc4f58939d0d`.
- Base attestation: this lane's correction is a clean fast-forward over `1873ba33`; `git merge-base --is-ancestor 1873ba33 HEAD` => PASS; `git merge-base 1873ba33 HEAD` => `1873ba33`. Only one of my own commits sits on top (`1781277d3`). Branch cut at `1873ba33` (no foreign commit carried).
- The prior worker akte `luna-round-1.md` (same akte dir) recorded the same provenance for the base candidate: `git ls-remote` this session repeats it unchanged.

## Reconciling Luna batch12 against the committed candidate `1873ba33`

The committed candidate already replaced the caller-supplied `persesSelected bool` + `backendSignals map[DashboardBackend]bool` with an `IdentitySelectionWitness` and derives `Available = AND(evidence flags)` via `NewIdentitySelectionWitness`; `EligibleFor` gated on `!witness.Available`. Against the three PFLICHTEN it still had two real gaps:

1. PFLICHT 1 — non-forgeable input: `Available` is an exported struct field; a caller can construct `IdentitySelectionWitness{Available: true}` directly and bypass the constructor. Positive availability is still directly supplyable (review finding 1, identity r3 precedent).
2. PFLICHT 2 — per-backend gate: `EligibleFor` gated on a single cross-dashboard aggregate `witness.Available`, so one Keycloak witness globally enabled all three backend dashboards and an absent witness globally suppressed them (review finding 2).
3. PFLICHT 3 — real signal path: no production call-site threads the resolved `keycloak-metrics` signal from `internal/capability/reference.go`. This is the selection-thread fan-in the owner has not authorized (identity r4 STOP Klausel; mission PFLICHT 3 "owner-wort bleibt rahmen").

## Correction (two files, write-set disjoint)

### PFLICHT 1 — NonForgeableAvailable()
- Added `func (w IdentitySelectionWitness) NonForgeableAvailable() bool` returning the AND of the four real-evidence flags. `Available` stays exported as a consumer result, but is now explicitly documented as NOT a valid gate input.
- Every gate/decision path (`EligibleFor`) uses `NonForgeableAvailable()`, never `Available`. `Available` is kept as the second-line AND(evidence) guard.
- Regression `TestIdentitySelectionNeverForgeableDirectAvailable`: the exact Luna case — `IdentitySelectionWitness{Available: true}` with no evidence — fails closed in the production gate, not just the helper.

### PFLICHT 2 — per-dashboard backend gate
- `EligibleFor(key, witness, backendSignals map[DashboardBackend]bool)`, `EligibleCount(witness, backendSignals)`, `FilterEligibleDashboards(catalog, witness, backendSignals)` — the single aggregate witness is replaced by a per-backend `backendSignals` map.
- A dashboard is eligible only when its OWN backend has a real signal (`backendSignals[backend]`) AND the witness is non-forgeably available. No single witness globally enables/disables every backend (review finding 2 resolved).
- Two new tests: `TestEligibleForPerBackendGate` (only the backend with a real signal is eligible; a shared signal does not enable a different key) and `TestFilterEligibleDashboardsPerBackendOnly`.

### PFLICHT 3 — real signal path (left to the 078-selection-thread)
- The production fan-in (`cmd/baha/app_status_result.go` → identity-dashboard availability) and the resolved-signal source (`internal/capability/reference.go` Keycloak `keycloak-metrics`, `Status: ObservabilitySupported, Mode: ObservabilityNative, Protocol: openmetrics, Verification: ObservabilityVerifyBackend`) are both present but NOT wired into a production path.
- Per the identity r3/r4 precedent and the mission PFLICHT 3, this lane does NOT invent the central resolver. Positive availability stays derived from a real-signal witness. The wiring is the `lane-0428-078-perses-identity` selection-thread task.
- Blocker-text for the 078 card: **wartet auf 080-r2 resolver-landung** (078 stacks on this lane's corrected selection/fan-in; 078 wires the prod path and proves it with the resolved `keycloak-metrics` signal + authorized Target, per the owner directive "080 zuerst als zuständigen Selection-/Resolver-Pfad klaeren und fertigstellen; DANACH 078 darauf aufsetzen").

## New signatures (explicitly listed for the 078 follow lane — rebasable)

- `func (c PersesDashboardCatalog) EligibleFor(key string, witness IdentitySelectionWitness, backendSignals map[DashboardBackend]bool) (DashboardEligibility, error)`
- `func (c PersesDashboardCatalog) EligibleCount(witness IdentitySelectionWitness, backendSignals map[DashboardBackend]bool) (int, error)`
- `func FilterEligibleDashboards(catalog PersesDashboardCatalog, witness IdentitySelectionWitness, backendSignals map[DashboardBackend]bool) ([]string, error)`
- `func (w IdentitySelectionWitness) NonForgeableAvailable() bool` (new; the only valid non-forgeable gate entrance)
- `type IdentitySelectionWitness struct { SelectionConfirmed, MetricPresent, MetricCurrent, TargetAuthorized, Available bool }` — `Available` stays exported; use `NonForgeableAvailable()` for gates.
- Test helpers added: `allBackendSignals()`. No mass renames; the three public selectors keep their names and positions — only their signatures grow by one `backendSignals` argument.

## Tests (self-run, by name)

- `TestIdentitySelectionNeverForgeableDirectAvailable` (NEW) — forged `Available:true` literal fails closed in the production gate.
- `TestEligibleForPerBackendGate`, `TestEligibleForZeroValueWitnessFailsClosedPerBackend`, `TestFilterEligibleDashboardsPerBackendOnly` (NEW) — per-backend gating, no cross-dashboard aggregate.
- `TestIdentitySelectionDerivedNotSupplied`, `TestIdentitySelectionDefaultUnpublishedIsUnavailable`, `TestIdentitySelectionUnavailableWhenNoKeycloakMetricSignal`, `TestIdentitySelectionUnavailableWhenMetricNotCurrentVersion`, `TestIdentitySelectionUnavailableWhenTargetNotAuthorized`, `TestIdentitySelectionNeverDerivedFromCallerStatusBoolean` — retain.
- `TestDashboardCatalogBuildsWithRealBackends`, `TestDashboardEligibleWhenRealSignalAndAuthorizedTarget`, `TestFilterEligibleDashboardsUnknownOwnerFailClosed`, `TestFilterEligibleDashboardsAvailableYieldsExpected`, `TestDashboardCatalogVersionMatchesSeamPin` — retain.

## repo-rule compliance

- Write-set: only `internal/capability/perses_selection.go` + `perses_selection_test.go`. No `.github/**` touched. No merge, no `ready_for_review`, no force-push, no retarget of another PR. No subagent (§4.8). No product write outside the named lane branch.
- Single integration candidate per chain: correction is one FF commit over `1873ba33` on `lane-0428-080-r28-perses-selection`. No second branch invented.
- Governance text: no coordinator directive / dispatch / handoff prose written into any product repo; lane identity and this akte live only in baseharbor-plan evidence.

## CI / test evidence (self-run)

- `go build ./internal/capability/... ./internal/metrics/... ./internal/observability/... ./cmd/baha/...` => exit 0 (TMPDIR redirected because `/tmp` on this host is a tmpfs near disk quota; unrelated to this change).
- `go vet ./internal/capability/... ./internal/metrics/... ./internal/observability/...` => clean.
- `gofmt -l` on both files => clean.
- `go test ./internal/capability/` (writable TMPDIR) => ok.
- `go test ./internal/metrics/... ./internal/observability/...` => ok.
- Full `go test ./...` on this host is blocked only by `/tmp` disk-quota (pre-existing, environmental), not by this change; targeted packages all green.

## Commit / branch provenance

- Base SHA (candidate): `1873ba33f38bf7c21a21b4bdb19c8a1525b1785e` — verified via `git ls-remote` (lane `lane-0428-080-r28-perses-selection` == `refs/pull/1590/head` == `1873ba33`).
- One-commit FF correction: `1781277d3356f0f52fb3bef242bb7f1074fba573`.
- Ancestry: `git merge-base --is-ancestor 1873ba33 HEAD` => PASS; `git merge-base 1873ba33 HEAD` => `1873ba33`. `git log 1873ba33..HEAD` lists only my commit.
- refspec-push: `git push origin 1781277d3:refs/heads/lane-0428-080-r28-perses-selection` => `1873ba33f..1781277d3`.
- POST-PUSH `git ls-remote origin refs/heads/lane-0428-080-r28-perses-selection` => `1781277d3356f0f52fb3bef242bb7f1074fba573` (== my commit). Branch HEAD == my commit; only my one commit carried on top of `1873ba33`.

## END line

DONE — lane-0428-080-r28-perses-selection: Luna batch12 REQUEST CHANGES closed. `IdentitySelectionWitness.Available` is no longer a forgeable gate input — `NonForgeableAvailable()` (AND of the four real-evidence flags) is the only valid non-forgeable entrance and the `EligibleFor` gate uses it; the forged-literal regression fails closed. `EligibleFor`/`EligibleCount`/`FilterEligibleDashboards` now take `backendSignals map[DashboardBackend]bool` and gate each dashboard on its OWN backend signal + the non-forgeable witness — no cross-dashboard aggregate (PFLICHT 2). Positive path stays derived from a real-signal witness; the production fan-in to `cmd/baha/app_status_result.go` is the 078-selection-thread task (PFLICHT 3, resolver wiring left for 078). Candidate `1781277d3` on PR #1590 head; evidence pushed to `origin/main` (path confirmed via `git ls-remote`).

## CI follow-up (EIGENES-RUN-PFLICHT)

- This correction changed only the selection/fan-in catalog signature (`internal/capability/perses_selection.go` + test). It is a draft-PR selection-thread fix; the exact-head PR CI run is owned by the next coordinator tick to observe to terminal. No runner/VM/container work. No `.github/**` touched.
