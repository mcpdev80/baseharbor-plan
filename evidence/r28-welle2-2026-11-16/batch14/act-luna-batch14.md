# CODEX-REVIEW — Luna batch 14

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch14.md` · PR #1590 selection r3; conditional follow-on #1650.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`).

## Object 1 — PR #1590

- Authenticated GitHub account: `mcpdev80`.
- PR #1590 is OPEN and DRAFT; base `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; head `lane-0428-080-r28-perses-selection` @ `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.
- Diff: `internal/capability/perses_selection.go` and `internal/capability/perses_selection_test.go`.
- Exact-head run `43900438284` is `pull_request`, completed SUCCESS on `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`. Six jobs succeeded and 24 were skipped. Those skipped jobs are not merge evidence; PR remains draft.
- No local product tests were run by this reviewer.

### Review findings

The r3 change scopes `NonForgeableAvailable()` to `DashboardBackendIdentity`; Prometheus, Loki, and Tempo use their own backend signal gate without requiring Keycloak identity evidence. The exact-head tests include `TestEligibleForPrometheusStaysEligibleWithoutKeycloakSignal`, `TestEligibleForLokiAndTempoEligibleWithoutKeycloakSignal`, and `TestFilterEligibleDashboardsBatch13Scoping`, which exercise the previous batch13 defect. The identity dashboard still fails closed unless its identity witness and own backend signal are present. The forged `Available` result is not used as the gate: `NonForgeableAvailable()` remains based on the four evidence flags.

**Verdict: APPROVE CONTENT** for PR #1590 at `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`. This is a content verdict only; it does not accept the task or satisfy skipped merge gates.

### Binding 078-onset confirmation

**Confirmed: 078 may stack on #1590 at `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.** The r3 head preserves the `IdentitySelectionWitness`, `NonForgeableAvailable()`, and per-backend signal API while correcting the identity-only scope. The 078 lane must rebase onto this head before relying on it.

## Object 2 — PR #1650

PR #1650 is OPEN/DRAFT, head `c8430f826e9128815147fb7f6257c74ff0c61faa`, but its base branch `lane-0428-080-r28-perses-selection` is still at obsolete SHA `1781277d3356f0f52fb3bef242bb7f1074fba573`. The current #1590 head is `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.

**NOT REVIEWED / no verdict.** Rebase #1650 onto the confirmed #1590 r3 head, reconcile the duplicate identity catalog additions with r3's `DashboardBackendIdentity` / `keycloak-identity` API, then request review of the resulting exact head. The current diff changes only `internal/capability/perses_selection.go` and its tests; it does not include the production status-result call site, so this review makes no claim that 078 production fan-in is implemented.

## repo-rule compliance and turn-start flags

- Read-only product review; no product code, PR state, CI, task state, or release state changed. No merge, approval, or GitHub review mutation.
- Turn-start flags forwarded to the coordinator: worker pool 1/4 (ornith 0/2, laptop 1/2); `NO_ELIGIBLE_WORK` holds on ornith:1, ornith:2, laptop:2; missing GUI TODO `workers/todos/0428-080-.json`; 37 open PRs.
