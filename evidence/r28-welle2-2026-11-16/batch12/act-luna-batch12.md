# CODEX-REVIEW — Luna batch 12

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch12.md` · PR #1590, dashboard selection / fan-in, owner decision `evidence/r28-welle2-2026-11-16/perses-dashboard-selection/owner-round-1.md`.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`).

## Candidate and CI

- Authenticated GitHub account: `mcpdev80`.
- PR #1590 is OPEN and DRAFT; base `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; head `1873ba33f38bf7c21a21b4bdb19c8a1525b1785e`.
- Diff: two files only — `internal/capability/perses_selection.go` and `internal/capability/perses_selection_test.go`.
- Exact-head run `43885791170` is `pull_request`, completed SUCCESS on that head. Draft source/routing and Draft Go `packages`, `cli-0..3` succeeded. `PR Selected Checks`, native/runtime and other non-draft gates were skipped because the PR is a draft; this is not merge evidence.
- No local product tests were run by this reviewer.

## Findings

### 1. Positive availability can still be supplied directly

`IdentitySelectionWitness` has exported mutable fields, including `Available` (`perses_selection.go:39-60`). `EligibleFor` gates on `if !witness.Available` (`:223`) and does not derive availability from the evidence fields. Any consumer can pass `IdentitySelectionWitness{Available: true}` with every evidence field false. The public constructor also accepts four raw booleans (`:69`), and the tests' positive helper calls it with literal `true` values (`perses_selection_test.go:8-10`). Current tests verify the AND formula through that constructor, but do not test a forged struct literal or a production-derived witness.

This does not meet the owner decision's fail-closed requirement that no caller-supplied status produce positive availability. The comment calls the witness “non-forgeable,” but the type and current gate do not enforce that claim.

**Recipe:** make `Available` unexported and derive it inside the eligibility boundary from the decision's four evidence fields; do not let a caller set the result field. Keep the zero value unavailable. Ensure the production resolver obtains selection from manifest truth, the current Keycloak metric from the real signal inventory, and Target authorization from validated provider-placement evidence before it creates a positive witness. Add regressions proving a direct `Available` assertion cannot pass, and positive/negative resolver tests for signal present/current, selection, and authorization. Stop if the production resolver cannot provide those actual inputs; leave identity unavailable.

### 2. Identity evidence is used as the gate for every dashboard backend

`DefaultDashboardCatalog` contains `prometheus-targets`, `loki-logs`, and `tempo-traces` (`perses_selection.go:158` onward), but no identity dashboard template. `EligibleFor` applies the Keycloak `IdentitySelectionWitness` check before evaluating any of those templates, then marks the dashboard eligible from the static template/version alone. It receives no per-backend signal or authorization witness. Consequently, a positive Keycloak identity witness makes all three backend dashboards eligible, while an absent Keycloak identity signal makes unrelated Prometheus/Loki/Tempo dashboards unavailable. This does not match the task's per-provider signal and Target-authorization acceptance.

**Recipe:** scope the Keycloak identity witness to an identity-dashboard entry. For each Prometheus/Loki/Tempo entry, require its own real backend signal and Target authorization; absent evidence stays unavailable. Add cross-backend tests: Keycloak evidence alone cannot qualify a dashboard whose backend is missing/unauthorized, and an unrelated identity absence does not suppress a dashboard with its own valid backend evidence unless the Owner explicitly makes identity selection a global prerequisite.

### 3. 0428-078 cannot yet be confirmed as a consumer

PR #1606 (`t-20261114-r28-perses-dashboard-identity`) is based on the old selection head `e6f5e650d048c28004cdc59608e9205c648bb509`, not #1590's `1873ba33`. Its current `PersesIdentityDashboardAvailability` still accepts `ObservabilitySupportStatus` (`perses_identity_dashboards.go:441`), and the PR changes only the dashboard resource, its tests, and its golden. `cmd/baha/app_status_result.go` at that head has no `PersesIdentityDashboardAvailability` or `IdentitySelectionWitness` call site. The r3 production-witness blocker therefore remains. This lane has not established that 0428-078 consumes an actual Keycloak signal plus Target authorization through the new fan-in.

**078 compatibility verdict: NOT CONFIRMED YET.** After the witness is technically fail-closed, rebase/stack #1606 on the corrected #1590 head and add one production path that constructs it from real manifest, signal, pin and placement evidence. Replace the status-enum input as availability authority. Keep direct `ObservabilitySupported` caller input unavailable, and add positive/negative production-call-path tests before claiming the identity dashboard available.

## Overall verdict

**REQUEST CHANGES** for PR #1590 at `1873ba33f38bf7c21a21b4bdb19c8a1525b1785e`.

The correction follows the owner decision's intended fail-closed shape at the constructor formula and adds missing-flag tests. It does not enforce the decision at the eligibility boundary, does not scope the identity witness to the identity dashboard, and has no production consumer proving actual signal/authorization inputs. No merge or downstream 0428-078 confirmation is justified from this candidate. Keep the PR draft. Re-review after the three recipes above are addressed and the required gates are observed on the exact head.

## repo-rule compliance and turn-start flags

- Read-only product review; no product files, PR metadata, CI, release, or task state changed.
- No merge or GitHub review mutation.
- Turn-start flags forwarded for coordinator disposition: three expired/unjustified worker-seat holds (ornith:2, laptop:1, laptop:2), missing GUI TODO `workers/todos/0428-080-.json`, and 35 open PRs.
