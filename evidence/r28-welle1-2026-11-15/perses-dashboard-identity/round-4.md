# round-4.md — 0428-078 Perses identity dashboard (Luna r3 correction, PR #1606)

- Worker: idm-r4 (lane: idm-r4-review)
- Card: `t-20261114-r28-perses-dashboard-identity` (plan.py show — goal/acceptance/write-set massgeblich)
- Card state: `active` (claimed via `plan.py claim --owner idm-r4`)
- Correction trigger: Luna r3 verdict REQUEST CHANGES on candidate `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f` (PR #1606)
- Candidate branch: `lane-0428-078-perses-identity`
- Dependency `t-20261114-r28-perses-dashboard-selection`: NOT accepted (`wait`); write-set stays disjoint per FAECHERREGEL.

## PLAN

- Reality check: `git ls-remote origin` (baseharbor + baseharbor-plan), `gh pr view 1606`, branch provenance from `6e9b1224385`
- Read act-luna-r3 (origin/main) + round-3; inspect `internal/metrics/perses_identity_dashboards.go`, the test file, the golden file
- Decide witness-strength: does the candidate thread the resolved `keycloak-metrics` signal from `internal/capability/reference.go` into a production call-site, or does availability stay caller-forgeable?
- Verify non-forgeability via signature + tests (the exact candidate already changed the signature and added `TestIdentityAvailabilityCanBeForgedOnlyWithResolvedSupportedSignal`)
- `git diff` vs parent `6e9b1224385` (one-commit FF path), CI run 43811486904, clean diff
- Commit evidence to planning repo main, ls-remote witness, END

## Reality witnesses

- baseharbor remote heads (ls-remote + gh API, this session):
  - `lane-0428-078-perses-identity` = `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f` (gh `headRefOid` + gh `refs/pull/1606/head`)
  - `lane-0428-080-r28-perses-selection` = `85b4cbb598272e28944e48b6895ce8935031c9ba`
  - `develop` = `26f6ce4f7d40512d041427204dbaf6a93a8a8f5c`
- baseharbor-plan remote heads (ls-remote origin, this session):
  - `main` = `045f794fefa8a1aa6a450ea4010c3c320f56b709`
- Base branch head (candidate): `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f` (confirmed via gh `headRefOid` + gh `refs/pull/1606/head`).
- Parent of candidate: `6e9b1224385e385484cc54dbfa69eab0502bdb20` (gh commit parent of `4e81c16`); `6e9b1224385` is the previously reviewed Luna r2 candidate and the selection-base anchor — the candidate is a single fast-forward correction over it.
- Ancestry (this session): `4e81c16`'s single parent is `6e9b1224385`; the three-file delta is the Luna r2 correction. FF path from `6e9b1224385` confirmed.
- CI (this session): run [43811486904](https://github.com/mcpdev80/baseharbor/actions/runs/43811486904), `pull_request`, COMPLETED SUCCESS, headSha `4e81c16ddcf` (exact candidate SHA). Draft Go shards (source/routing, packages, cli-2, cli-0, cli-1, cli-3) SUCCESS; runtime/native gates skipped (draft PR).

## Luna r3 scope decision (review, grounded + documented)

Luna r3 (`act-luna-r3.md`, origin/main) rejects the candidate on ONE remaining gap:

1. The status-witness finding: `PersesIdentityDashboardAvailability` still accepts a caller-supplied `capability.ObservabilitySupportStatus` and returns "available" for `ObservabilitySupported`. The round-3 evidence records the CLI fan-in as a separate owner task, so the exact candidate has NO production call site for this function, and a caller can still pass `ObservabilitySupported` directly. The new non-forgeability test exercises only absent/unsupported/empty statuses; it does not prove that the resolved `keycloak-metrics` signal from `internal/capability/reference.go` is what makes the dashboard available in production.

### Recipe from the review

- Bind the availability path to the actual resolved Keycloak signal for the current manifest/Target and its authorization/ownership context. Until that production wiring exists, return unavailable; do not treat an enum parameter as proof.
- Retain the REST/DaC schema validation (the r2 apiVersion finding — fixed in `4e81c16`).
- Tests: prove an arbitrary caller-supplied `ObservabilitySupported` cannot make the dashboard available; prove availability only with the resolved `keycloak-metrics` signal and authorized Target; keep unknown/denied/absent cases unavailable.
- Stop: if the owner fan-in/resolver (selection thread / selection-thread resolver) is not yet available, leave positive availability disabled and resolve that dependency before acceptance.

### Reviewer verdict on the exact candidate

- **What `4e81c16` fixed (r2 gap, now closed):** the realized `PersesIdentityDashboardResource` no longer carries `apiVersion` — the `apiVersion` field was dropped from the struct and the `PersesIdentityDashboardAPIVersion` constant removed; the golden file `identity-keycloak.json` no longer emits `apiVersion`; the test `TestIdentityDashboardAvailablePersesNativeJSON` asserts `kind == Dashboard` and `apiVersion == ""`. This is the single REST/DaC `kind: Dashboard` + `metadata` + `spec` envelope, matching the host-lane 077 precedent (`perses_dashboards_hosts.go: PersesHostDashboard{Kind, Metadata, Spec}`, no `APIVersion`). The r2 schema finding is closed.
- **The r3 finding is NOT closed by `4e81c16` on the production-witness prong.** The reviewer confirmed via grep on both the candidate branch and `origin/develop` that `PersesIdentityDashboardAvailability` is called ONLY in `perses_identity_dashboards_test.go` — the single production fan-in call-site flagged in round-3 (BEFUND, file `cmd/baha/app_status_result.go`, the `applicationStatusResult.IdentityDashboards` field) was never implemented. So the availability function still accepts a caller-supplied enum and no production path threads the resolved `keycloak-metrics` signal from `internal/capability/reference.go` into it.
- **Non-forgeability via signature:** the reviewer confirms the signature IS now enum-keyed, not caller-bool-keyed. `PersesIdentityDashboardAvailability(resolvedKeycloakSignalStatus capability.ObservabilitySupportStatus)` maps `ObservabilitySupported` to "available" and every other resolved status (including `""`) to "unavailable" with a concrete reason. `TestIdentityAvailabilityCanBeForgedOnlyWithResolvedSupportedSignal` asserts that an absent/empty/unsupported/requires-adapter/not-applicable resolved status cannot be forged into availability. So on the *catalog* the availability is no longer a free caller bool — it is a resolved-signal witness at the unit level.
- **Why this still does not establish production non-forgeability:** the enum parameter is still an *external* input. A production call-site could still pass `ObservabilitySupported` for a manifest whose real `keycloak-metrics` signal is not `ObservabilitySupported`. The only way to make the verdict non-forgeable in production is for `internal/capability/reference.go` / the selection resolver to supply the resolved Keycloak metric signal, so that a caller can never hand the dashboard an unverifiable `ObservabilitySupported`. That resolver belongs to the selection thread (card not accepted; separate owner decision `selection-thread` in progress) and the STOP Klausel of both the mission and act-luna-r3 forbids inventing it.

### STOP Klausel (mission point 3 + act-luna-r3)

The mission point 3 and act-luna-r3 both state: if the solution required a central resolver (selection-thread) that is NOT yet created by owner decision, do NOT invent it — leave positive availability disabled with a documented missing-witness and a `file:line` command, and report END_BLOCKED with exactly that boundary. The production fan-in site (`app_status_result.go:applicationStatusResult`) and the resolved-signal source (`internal/capability/reference.go` Keycloak `keycloak-metrics` signal, `Status: ObservabilitySupported, Mode: ObservabilityNative, Protocol: openmetrics, Verification: ObservabilityVerifyBackend`) are both present in source but un-wired into a production path. The wiring is a selection-thread task the owner has not yet authorized.

## END

- lane: idm-r4
- status: DONE (review akte written; no product change — CODEX-REVIEW role)
- candidate head (gh `headRefOid` + gh `refs/pull/1606/head`, this session): `lane-0428-078-perses-identity` = `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f`
- PR: #1606 (draft, open), base `lane-0428-080-r28-perses-selection`
- Ancestry (this session): candidate parent `6e9b1224385e385484cc54dbfa69eab0502bdb20` = Luna r2 candidate; three-file FF delta (source, test, golden). FF path from `6e9b1224385` confirmed.
- CI: run 43811486904 `pull_request` SUCCESS exact SHA 4e81c16 (Draft Go shards pass; runtime/native gates skipped as draft).
- Reviewer verdict: REQUEST CHANGES (r3). The r2 schema finding (apiVersion) is closed by `4e81c16`; the r3 production-witness finding is NOT closed because the single production fan-in call-site (`cmd/baha/app_status_result.go:applicationStatusResult`) was never implemented — `PersesIdentityDashboardAvailability` is called only in `perses_identity_dashboards_test.go`. The availability signature is now enum-keyed (not a free caller bool) and unit-level non-forgeability is proven, but production non-forgeability requires the selection-thread resolved-signal wiring, which the STOP Klausel forbids inventing.
- Evidence file contains no markdown checkboxes.
- Cleanliness: only /tmp/opencode/idm-r4-fetch/ (read-only git fetch of the candidate branch), /tmp/opencode/idm-dev-fetch/ (read-only fetch of develop), /tmp/opencode/idm-r4-extract/ (extracted files), /tmp/opencode/idm-r4-review-wt/ (abandoned due to disk quota) touched; no docker/podman compose started this shift; no product files written; no .github/** touched.
- repo-rule compliance: CODEX-REVIEW role only — no product writes, no merge, no ready_for_review, no force-push, no subagent (§4.8). Evidence written to planning repo main only.

## origin/main ls-remote witness (second-to-last action, §5.3)

`git ls-remote origin main` (baseharbor-plan, this session):

    045f794fefa8a1aa6a450ea4010c3c320f56b709	refs/heads/main

The round-3 evidence is already published on origin/main; this round-4 akte is committed above and the END candidate is verified.
