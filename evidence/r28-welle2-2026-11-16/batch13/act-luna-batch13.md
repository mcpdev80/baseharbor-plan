# CODEX-REVIEW — Luna batch 13

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch13.md` · PR #1590, Perses dashboard selection r2.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`).

## Candidate and CI

- Authenticated GitHub account: `mcpdev80`.
- PR #1590 is OPEN and DRAFT; base `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; head `lane-0428-080-r28-perses-selection` @ `1781277d3356f0f52fb3bef242bb7f1074fba573`.
- Diff remains two files: `internal/capability/perses_selection.go` and `internal/capability/perses_selection_test.go`.
- Exact-head run `43894440297` is `pull_request`, completed SUCCESS on the exact head. It reports 6 successful jobs and 24 skipped jobs. Skipped gates are not merge evidence; the PR remains draft.
- No local product tests were run by this reviewer.

## Findings

### Non-forgeable identity witness

PASS for the reviewed API gate: `NonForgeableAvailable()` returns the AND of `SelectionConfirmed`, `MetricPresent`, `MetricCurrent`, and `TargetAuthorized`; `EligibleFor` checks this method and does not trust the exported `Available` result. `TestIdentitySelectionNeverForgeableDirectAvailable` exercises `IdentitySelectionWitness{Available: true}` with no evidence and verifies fail-closed behavior. The related negative evidence-flag tests are present.

This is a library boundary that depends on callers truthfully supplying the evidence flags; the correction prevents forging availability through the raw `Available` field. Production evidence derivation remains assigned to 078.

### Per-dashboard backend gate — unresolved cross-backend prerequisite

The new `backendSignals[backend]` check correctly prevents a Prometheus signal from enabling Loki or Tempo, and `TestEligibleForPerBackendGate` covers that separation. However, `EligibleFor` first requires `witness.NonForgeableAvailable()` for every catalog key. That witness represents Keycloak identity selection. Thus a missing Keycloak identity signal still suppresses Prometheus/Loki/Tempo dashboards even when the requested dashboard's own backend signal is present. The positive tests all use an available identity witness; there is no regression proving an unrelated backend remains eligible without Keycloak identity evidence.

The owner decision requires fail-closed Keycloak identity availability and says the catalog still requires each real backend signal; it does not establish Keycloak identity as a global prerequisite for unrelated backend dashboards. The batch12 recipe also explicitly left that global prerequisite conditional on an Owner decision. The hard-coded global gate therefore remains unsupported and the per-dashboard correction is incomplete.

**Recipe:** apply the Keycloak identity witness only to identity-dashboard availability. For Prometheus, Loki, and Tempo entries, require their own real backend signal and Target authorization. Add a test where Keycloak evidence is absent but one unrelated backend has valid evidence; that backend must remain eligible unless the Owner explicitly records identity selection as a global prerequisite. Retain the forged-`Available` regression and per-backend cross-gating tests.

### 0428-078 compatibility

PR #1606 remains OPEN/DRAFT, base branch `lane-0428-080-r28-perses-selection` with base SHA `e6f5e650d048c28004cdc59608e9205c648bb509`, not corrected head `1781277d3`. Its `PersesIdentityDashboardAvailability` still accepts `ObservabilitySupportStatus`, and its diff has no `cmd/baha/app_status_result.go` production call-site change. **078 compatibility: NOT CONFIRMED.** After #1590 resolves the global-gate finding, rebase/stack #1606 onto the corrected head and demonstrate the production resolver consumes the non-forgeable evidence rather than a supplied status enum.

## Verdict

**REQUEST CHANGES** for PR #1590 at `1781277d3356f0f52fb3bef242bb7f1074fba573`. The raw-`Available` regression is fixed, but the global Keycloak witness still gates unrelated backend dashboards without an Owner decision establishing that prerequisite. The exact-head draft CI run succeeded; skipped jobs remain skipped. Keep the PR draft. 078 cannot yet be confirmed as buildable on this candidate.

## repo-rule compliance and turn-start flags

- Read-only product review; no product code, PR state, CI, task state, or release state changed. No merge, approval, or GitHub review mutation.
- Turn-start flags forwarded to the coordinator: worker pool 1/4 (ornith 1/2, laptop 0/2); `NO_ELIGIBLE_WORK` holds on ornith:2, laptop:1, laptop:2; missing GUI TODO `workers/todos/0428-078-.json`; 38 open PRs.
