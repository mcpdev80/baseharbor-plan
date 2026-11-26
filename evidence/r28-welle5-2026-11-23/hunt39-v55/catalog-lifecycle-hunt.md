# Bug-hunt slice H-V55 — catalog/lifecycle trace (Befundung, no fixes)

- Card/mission: w215-huntV55 (BUG-HUNT SLICE H-V55)
- Dispatch: coordinator -> Codex (w200/w136) card disposition only
- Worktree (isolated, pinned releasedesse): /tmp/opencode/w215-huntV55-wt @ d766e49c2
- Planning repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ONLY, origin = https://github.com/mcpdev80/baseharbor-plan.git
- Planning repo remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`

## Base attestation

- Releasedesse SHA (mission, exact): `d766e49c2`
- `git ls-remote origin d766e49c2` -> not a branch ref; present as a commit in the baseharbor checkout history
- develop HEAD moved `d766e49c2 -> 28296a2e6e920592741c9397486358deac7e95b2` between releasedesse and now
- Worktree base: `git ls-remote lane-origin develop` = `28296a2e6e920592741c9397486358deac7e95b2` (github.com/mcpdev80)
- `git -C /tmp/opencode/w215-huntV55-wt log --oneline -1` = `d766e49c2 Merge pull request #1848 from mcpdev80/lane-0428-313-restore-identity`

## Scope

- Surface catalog: `scripts/pr-gate-coverage.json` (schema `baseharbor.pr-gate-coverage/v1`, release `v0.4.27`)
- 63 gates, 298 source components, 15 native_checks
- Task: for every runtime-identity + data.capabilities row, trace the product code path that satisfies it; flag dead catalog entries (named component unreachable by any executed gate) and any fixture that consents default-open. No fixes.

## Catalog model (what "executed gate" means)

- Gates in `pr-gate-coverage.json` declare a `demo_contract {profile, capabilities}` (the data.capabilities rows) and a `covers` surface list.
- Executed paths today:
  - Native gates via `scripts/ci-native-pr-gate.sh`, selected by `scripts/pr-native-gate-plan.py` from `native_checks` (`native_checks[].covers` surface -> exact `go test -run`).
  - Demo acceptance harness `baseharbor-demo` @ `f23b6e09be34601ba542a3087e19b80764a4165d` `scripts/acceptance.sh`, dispatched with `DEMO_ATOMIC_GATE=1 GATE=<id>`. Runs the atomic lifecycle gates (lifecycle, data-capabilities, observability, backup-restore, policy, identity, connectivity, security, ...) against a disposable fixture.
- The demo `tests/gates.json` registry (f23b6e09) lists the gates the acceptance harness runs: config-matrix, guided, shell-ux, init, lifecycle, data-capabilities, observability, policy, identity, connectivity, security, mcp, agent, reconciliation, failure, backup-restore, full-destroy.

## Finding 1 — data.capabilities row reaches two concrete code paths (LOW severity, confirmed reachable)

- Row: gate `atomic/docker/data-capabilities` / `atomic/podman/data-capabilities`, `demo_contract.capabilities = [database.sql, cache.key-value, object-storage.s3, secrets, runtime-resource]`.
- Native executor (ci-native-pr-gate.sh lines 113-118, gate `native/{docker,podman}/data-capabilities`):
  - `prepare_exact_runtime_image` (builds candidate binary, pins to HEAD SHA).
  - `run_exact_test TestApplicationCapabilityLifecycleExistingCore 20m ./cmd/baha BASEHARBOR_CORELESS_ACCEPTANCE=1`.
  - `run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent 20m ./cmd/baha BASEHARBOR_CORELESS_ACCEPTANCE=1`.
- Product code that stamps the synthetic operator for this gate: `cmd/baha/ci_integration_operator_enabled.go` (build tag `baseharbor_ci_operator_testonly`).
  - Consent gate: `if os.Getenv("DEMO_ATOMIC_GATE") != "1" { return ctx }` (line 25) — the synthetic operator is injected ONLY when the atomic gate env is explicitly "1".
  - The managed-local boundary admits only exact canonical commands for gate == "data-capabilities" (`ciIntegrationManagedLocalGateReason`, lines 154-181: `ciIntegrationGuidedAppNew`, `ciIntegrationGuidedAppEdit`, `ciIntegrationDataCapabilitiesFootprintShow`, `ciIntegrationMCPFootprintParityGate`).
  - Membership: `ciAcceptanceMembershipProvider.ResolveClaimMembership` (line 612) fails closed on `ErrClaimsNotVerified` for an unverified principal.
- Digest-consent test: `cmd/baha/app_capability_runtime_test.go:363` `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` (`BASEHARBOR_CORELESS_ACCEPTANCE != "1"` -> `t.Skip`).
- Trace is complete: surface `source.gate.atomic.{docker,podman}.data.capabilities` -> `native/{docker,podman}/data-capabilities` native check (validate-pr-gate-coverage.py line 91) -> the two go tests -> the tagged operator seam.

## Finding 2 — dead catalog entries (named component unreachable by any executed NATIVE gate) — MEDIUM severity

- Method: for every gate's `covers` surface of the form `source.gate.atomic.*`, checked against `native_checks[].covers`. A surface with no native check is not reached by the native gate path.
- Native checks today (15): native/docker/greenfield, onboarding, perses-runtime-smoke, data-capabilities, guided, coreless-lifecycle, environment-destroy, podman/installation-destroy, workstation-onboarding, second-target-conflict, data-capabilities, guided, coreless-lifecycle, environment-destroy, service-stop.
- Gates whose `source.gate.atomic.*` surface has NO native check (cataloged component, no executed native gate):
  - `atomic/static/ci-fast-check` -> surface `source.gate.atomic.static.ci.fast.check` (run by `scripts/ci-fast-check.sh` from `ci-fast-check` static gate, not a native check).
  - `atomic/docker/lifecycle` -> `source.gate.atomic.docker.lifecycle`.
  - `atomic/docker/observability` -> `source.gate.atomic.docker.observability`.
  - `atomic/docker/backup-restore` -> `source.gate.atomic.docker.backup.restore`.
  - `atomic/docker/control-plane-recovery` -> `source.gate.atomic.docker.control.plane.recovery`.
  - `atomic/podman/observability` -> `source.gate.atomic.podman.observability`.
  - `atomic/podman/backup-restore` -> `source.gate.atomic.podman.backup.restore`.
  - `atomic/podman/control-plane-recovery` -> `source.gate.atomic.podman.control.plane.recovery`.
- Reachability nuance (important for disposition, not a fix): these surfaces ARE exercised through the demo acceptance harness `acceptance.sh GATE=<lifecycle|observability|backup-restore|control-plane-recovery>` run from `.github/workflows/pre-release-runtime-suite.yml` line 334 with `DEMO_ATOMIC_GATE=1`. They are reachable as demo gates but are NOT registered as a `native_check` (validate-pr-gate-coverage.py line 87 `resolve_native_checks` only sees `native_checks[]`). So the dead-catalog finding is precise: the `source.gate.atomic.*` surfaces for lifecycle/observability/backup-restore/control-plane-recovery have no `native_check` row, only the demo-acceptance path.
- `atomic/podman/lifecycle` maps to `native/podman/service-stop` (covers `source.gate.atomic.podman.lifecycle`) — reachable via native check. Not a dead entry.
- The `native/docker/data-capabilities` and `native/podman/data-capabilities` surfaces (the data.capabilities rows the mission names) both HAVE native checks. The data.capabilities rows are therefore not dead.

## Finding 3 — consent is NOT default-open (LOW severity, confirmed fail-closed)

- The mission asked for "any gate whose fixture consents default-open". Evidence:
  - Synthetic operator injection is gated by `DEMO_ATOMIC_GATE == "1"` (`cmd/baha/ci_integration_operator_enabled.go:25`). Without it the function returns the unmodified context and the request falls through to the normal operator-auth OIDC boundary.
  - The managed-local admission list admits only exact canonical command forms (arg-count + token match, `equalArgs` at line 294), never a wildcard. Every unlisted command hits `ciIntegrationManagedLocalGateReason` returning `"command-not-in-managed-workload-set: ..."` and the fail-closed OIDC path.
  - `internal/operatorauth/authorization.go:46,90` return `ErrClaimsNotVerified` (fail closed) on an unverified principal; `internal/operatorauth/context.go:115` documents claim-based resolution fails closed.
  - Digest consent in the data-capabilities test is opt-in: `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` skips unless `BASEHARBOR_CORELESS_ACCEPTANCE == "1"`.
- No fixture in the traced catalog consents default-open. The consent model is explicit + fail-closed.

## Findings list for Codex

- F1 (MEDIUM): 8 gate `source.gate.atomic.*` surfaces (lifecycle, observability, backup-restore, control-plane-recovery x docker/podman; + ci-fast-check static) have no `native_check` row in `scripts/pr-gate-coverage.json` `native_checks[]`. They are reached via the demo-acceptance harness only, not via the native gate selection (`scripts/pr-native-gate-plan.py`). Disposition: either add the missing `native_check` rows (if the gates should be native) or annotate them as demo-acceptance-only. Owner: outside this hunt's write-set — report file `scripts/pr-gate-coverage.json` `native_checks` array + `scripts/pr-native-gate-plan.py` line 87 for card disposition.
- F2 (LOW): confirmed — no consent-default-open in the traced catalog; the data.capabilities + managed-operator boundary fail closed. No action.

## Reproduction

- Catalog model: `python3 -c "import json;d=json.load(open('scripts/pr-gate-coverage.json'));print(len(d['gates']),'gates',len(d['native_checks']),'native_checks')" ` (run in /tmp/opencode/w215-huntV55-wt).
- Dead-surface check: map each `gates[].covers` `source.gate.atomic.*` surface to `native_checks[].covers`.
- Native data-capabilities executor: `scripts/ci-native-pr-gate.sh` case `native/{docker,podman}/data-capabilities` (lines 113-118).
- Demo acceptance harness + gates registry: `baseharbor-demo` @ f23b6e09 `scripts/acceptance.sh` + `tests/gates.json`.

## Cleanliness

- No containers, volumes, compose projects, or state directories started. Hunt is read-only catalog trace + demo git fetch to /tmp.
- `docker ps -a` before: (no host docker used; coordinator host, not a test host)
- `docker ps -a` after: (unchanged)
- cleanliness: clean — no new containers/volumes/state dirs; all work in /tmp/opencode/w215-huntV55-wt and a one-shot `git fetch` of the pinned demo ref. ambient-core/ images untouched.

## Status

- END_DONE. Pure Befundung. No product changes, no cards created. Findings F1/F2 handed to Codex (w200/w136) for card disposition. Akte pushed to baseharbor-plan origin/main.
