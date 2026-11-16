# 0428-078 Perses dashboard identity — on-resolver round-3 (2026-11-16)

Task: `t-20261114-r28-perses-dashboard-selection`
Handoff card: `t-20261114-r28-perses-dashboard-identity`
Mission: `/var/tmp/missions/mission-identity-078-r3-handoff.md`
Candidate (acceptance SHA): `d94d477d92f16c9fba5f76b681a332ee03f8456e` = PR #1650 head = branch head.

Owner decision / batch14 akte: `evidence/r28-welle2-2026-11-16/batch14/act-luna-batch14.md` (referenced by mission; not present in this evidence tree this shift).

This lane's base attestation: candidate `d94d477d92f16c9fba5f76b681a332ee03f8456e` (== PR #1650 head == `refs/pull/1650/head`). Clean ancestor of this lane: `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd` (080-head, LUNA-APPROVED) is an ancestor of `d94d477d` — verified with `git merge-base --is-ancestor origin/080sel d94d477d` => PASS. No foreign commit carried on top (branch == r2 head, zero own commits this shift).

## RESULT

END_BLOCKED — production call-site gate can never go positive: the Keycloak identity dashboard's `keycloak-metrics` native signal is declared in `internal/capability/reference.go:160` but is NEVER registered in the runtime observability signal registry by any production path. The r2 witness in `internal/metrics/perses_identity_witness.go` matches `source.ID == "keycloak-metrics"` (`perses_identity_witness.go:16` const, `perses_identity_witness.go:117` match). No code anywhere creates that registry entry, so `MetricPresent`/`MetricCurrent` are permanently false, `NonForgeableAvailable()` is permanently false, and `identity_dashboard_eligible` in `cmd/baha/app_status_result.go:161` can never become true. The gate is fail-closed by construction but ALSO unreachable-once-positive: it is not a working gate, it is a permanently-closed door.

## PLAN

- Step 1: Establish remote truth via git ls-remote for PR #1650 head and 080 base; verify base ancestor; clean branch. DONE.
- Step 2: Read mission + r2 witness/call-site; confirm exact scope (production call-site gate only, no new resolver). DONE.
- Step 3: Empirically verify whether a real managed Keycloak deploy registers the `keycloak-metrics` signal the witness needs. DONE — PROVED IT DOES NOT.
- Step 4: Confirm by exhaustive code search that no production path creates the signal. DONE — zero matches outside reference.go declaration + witness const/match + my transient diagnostic.
- Step 5: Report END_BLOCKED with file:line per mission STOP clause. DONE.

## EMPIRICAL WITNESS (run on baha-docker, 2026-11-16)

- Host: `baha-docker` (rootless-safe Docker 29.8.1; claim via `bash coordinator/scripts/vm-lock.sh claim baha-docker lane-0428-078-perses-identity-on-resolver-r3`, released after).
- Cloned PR #1650 head `d94d477d`, added a smoke test `TestStatusResultIdentityGateVM` that deploys a managed Keycloak identity provider (acceptance env `BASEHARBOR_IDENTITY_LIFECYCLE_ACCEPTANCE=1`) and then lists the observability signal registry via the same `observability.List` path the witness uses, asserting a real `keycloak-metrics` native signal exists.
- Result: the deploy completed, but the registry at the witness's own path (`bhruntime.DataDir("") + /observability/signals.json`) contained ZERO signals (`ALL signals (0)`; `RAW signals.json=""`). No Keycloak metrics signal was registered under provider `keycloak`, under any ID.
- Follow-up code search: `keycloak-metrics` as a signal ID exists only in `internal/capability/reference.go:160` (descriptor, Port 9000 /metrics, Mode ObservabilityNative), `internal/metrics/perses_identity_witness.go:16` (const) and `:117` (match). The managed Keycloak container exposes no metrics endpoint at port 9000 (`internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/core.go` — PublicPort/AdminPort only). No `RegisterProviderSignals`/`RegisterTarget`/`ReconcileSignals` call produces a `keycloak-metrics` entry. The prometheus/otel provider-realization paths (`internal/metrics/realization.go`, `internal/telemetry/realization.go`) register application/collector signals under generated IDs, never a dedicated `keycloak-metrics`.
- The witness unit test `internal/metrics/perses_identity_witness_test.go:39` seeds the signal manually (`observability.Update`), which is why the unit positive path passes — it does NOT reflect a real deploy.

## STOP CLAUSE (mission line 5)

Mission STOP: "referenz.go hat wirklich keinen keycloak-metric-pfad -> END_BLOCKED mit file:line." TRUE — confirmed.

- `internal/capability/reference.go:160` — the `keycloak-metrics` native openmetrics signal is declared for the Keycloak integration descriptor, but the realized Keycloak provider serves no metrics endpoint (no port 9000 scrape path in the container).
- `internal/metrics/perses_identity_witness.go:16` + `:117` — the witness gates identity availability on a registry signal with `ID == "keycloak-metrics"`, which no production path writes.
- `cmd/baha/app_status_result.go:161` — the call-site surfaces `identityWitness.NonForgeableAvailable()`, which is permanently false because the witness can never attest the missing signal.

This is not a cosmetic fail-closed (a gate that stays shut until real evidence appears). It is a gate whose only "real evidence" path is undefined in the code: the referenced signal declaration has no realization. Fixing it is a product change (realize a real Keycloak metrics signal path, or bind the gate to an existing real signal), which is OUTSIDE the r3 handoff scope ("production call-site stufe") and outside this lane's write-set. Per the mission STOP clause this lane reports STOP and stops.

## Scope / conflicts

- No product code changed this shift. Branch `lane-0428-078-perses-identity-on-resolver-r3` == r2 head `d94d477d` == PR #1650 head == `refs/pull/1650/head`. Zero own commits; no foreign commit carried on top; `git merge-base --is-ancestor origin/080sel HEAD` => PASS.
- No `.github/**` touched. No merge, no ready_for_review, no force-push, no retarget. No subagent (§4.8).
- The smoke test that proved the finding was transient: it cannot pass (the gate is unreachable-once-positive), so it was reverted — leaving the branch exactly at r2 head. The diagnostic output above is the durable witness.

## CI

Not run. No product change this shift (branch == r2 head); no CI required. The blocker is a missing signal realization, not a test.

## VM hygiene

- `baha-docker` docker ps: empty. `docker ps -a --filter name=bh-`: empty. Disk 78G free. No lane-owned containers/volumes/state left.
- vm-lock released: `bash coordinator/scripts/vm-lock.sh release baha-docker lane-0428-078-perses-identity-on-resolver-r3` => `FREE host=baha-docker`.

## Evidence provenance

- `git ls-remote origin refs/pull/1650/head` => `d94d477d92f16c9fba5f76b681a332ee03f8456e` (== refs/pull/1650/head).
- `git ls-remote origin refs/pull/1590/head` => `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd` (080-head, LUNA-APPROVED, base of PR #1650).
- Clean-ancestor check: `git merge-base --is-ancestor origin/080sel d94d477d` => PASS.
- Branch HEAD after revert: `d94d477d92f16c9fba5f76b681a332ee03f8456e`.

## END line

BLOCKED — lane-0428-078-perses-identity-on-resolver-r3: the Keycloak identity dashboard `keycloak-metrics` native signal is declared in `internal/capability/reference.go:160` but never registered in the runtime observability signal registry by any production path; the r2 witness (`internal/metrics/perses_identity_witness.go:16`/`:117`) matches that unreachable ID, so `NonForgeableAvailable()` / `identity_dashboard_eligible` (`cmd/baha/app_status_result.go:161`) is permanently false. Empirically confirmed on `baha-docker`: a real managed-Keycloak deploy registered zero signals at the witness's registry path. Per mission STOP clause, END_BLOCKED with file:line. Branch left == r2 head `d94d477d` == PR #1650 head; no product change, no `.github/**`, no subagent.
