# Bug-Hunt 914 — auth/realization surf (Keycloak realization, enrollment/trust-plane, receipt/consent)

- Mission: `/var/tmp/missions/mission-hunt-authsurf.md` (HUNT-FREIGABE 2026-11-17)
- Scope: static read + unit-only tests. NO product changes. NO `.github/**`. NO containers on this host.
- Repo: baseharbor (product). Branch: `develop`. Base SHA: `907f16713cbf38693d30c9dadaad7fe299759219`
- Base attestation: `git merge-base --is-ancestor develop HEAD` -> OK. `origin/develop` == `907f16713` == HEAD, reachable in history.
- Read worktree: `/tmp/opencode/w914-authsurf-wt` (checked out on `develop` == `907f16713`)
- Host: this machine is the coordinator/codeman server (NOT a test host). No containers, no compose projects started.

## ## PLAN

- Read mission; confirm base SHA of develop and that it is an ancestor of my read worktree HEAD.
- Slice (a): trace every error path in the receipt/consent realization for swallowed errors / green returns on failure.
- Slice (b): trace the enrollment trust-plane state machine for half-finished states (consume-then-issuance-fail, renewal, overlap admission).
- Slice (c): doc-claim vs implementation consistency for Keycloak realization, trust-plane, receipt/consent.
- Reproduce the precedence bug as a unit-only test in the worktree (R1).
- Write befund-1.md with all slices, repro, cleanliness, END.
- Commit evidence to baseharbor-plan origin/main; verify with ls-remote.
- Cleanliness check; post END to coordinator.

## Befund 1 (heavy): receipt verification guard collapses to a single operand — actual disposition diffs are silenced

- File/line: `internal/application/provider_change_result.go:40-46`
- Severity: high — a real "actual-disposition-differs" outcome is mislabeled as "continuation-dependency-unverified", and the "actual-disposition-differs" branch becomes unreachable in the replacement path.
- The guard is `if continuationRequiresDependencyEvidence(imp) && len(imp.ContinuationDependencies) == 0 || !continuationDependencyOutcomesMatch(...)`. Go binds `&&` above `||`, so this is `(A && B) || C`.
- `continuationRequiresDependencyEvidence(imp)` (file `internal/application/provider_change_dependency_result.go:56-66`) returns true only when `imp.After != nil && imp.After.InstanceID != imp.InstanceID` (a replacement) OR a transition has dependencies. In a replacement, the planned `ContinuationDependencies` is always populated by `describeContinuationDependencies` at `internal/application/provider_change_plan.go:88` (a replacement without them would fail with `continuation-dependency-missing` at `provider_change_dependency_result.go:121`). So `len(imp.ContinuationDependencies) == 0` (operand B) is never true when A is true -> `(A && B)` is unsatisfiable.
- Result: the guard reduces to `!continuationDependencyOutcomesMatch(...)`, i.e. only the second operand fires. The first operand's intent ("treat continuation-dependency-unverified as distinct from actual-disposition-differs") is dead code.
- Repro: unit-only test in worktree `internal/application/zz_hunt_authsurf_repro_test.go`. With a verified replacement plan and an *applied* outcome that carries an **unplanned** continuation edge, `RecordProviderChangeResult` returns `status=failed` with `ErrorCode="continuation-dependency-unverified"` (the repro test asserts exactly this), not `actual-disposition-differs`.
- Impact: an `applied` execution whose actual realization differs from the approved one is reported under the wrong code. Callers that branch on the error code (retry/verification routing) cannot distinguish a genuinely stale continuation graph from a realized-but-different disposition.
- Existing coverage gap: `internal/application/provider_change_dependency_result_test.go` only drives the `continuation-dependency-unverified` code path via `ContinuationDependencies`; no test ever exercises `actual-disposition-differs`. `outcomeMatchesImpact` (`provider_change_result.go:153`) is only reached for the mismatch comparison, but the pre-check short-circuits first.
- NOTE: this is a befund for the Owner to triage. Per mission scope (R1, no product changes) this is NOT fixed here. A minimal fix would parenthesize the two operands as `A && (B || C)` or restructure, but that is an Owner decision and would require a new test for the `actual-disposition-differs` path.

## Befund 2 (medium): enrollment trust-plane — consume and issue are two transactions; consumed-but-unissued leaves a dead grant but no active identity

- File/line: `internal/targetenrollment/authority.go:148` (Consume) -> `:167` (RecordIssued). `internal/database/connector_enrollment.go:76` (Consume), `:109` (RecordIssued).
- The state machine: `Consume` marks a grant consumed (`consumed_at=clock_timestamp()`) in one tenant-local transaction and returns a certificate TTL (`connector_enrollment.go:81-97`). `RecordIssued` writes the concrete serial into `connector_nodes` in a *separate* transaction (`connector_enrollment.go:114-136`).
- Half-finished state: if `RecordIssued` fails (issuer outage, bad serial, expired) at `authority.go:167`, the returned error path revokes the freshly-signed certificate (`authority.go:168-171`) and reports `enrollment identity persistence failed; certificate admission is unavailable`. The grant stays consumed (one-use, cannot retry) and the node has no serial -> the node is in a dead "consumed, never enrolled" state that requires a fresh `Create` (initial enrollment) or a `CreateRenewal` (renewal) to resolve. This is a correct fail-closed edge (no active identity survives), but it is a state transition where a competing in-flight `Create` on the same node could otherwise have raced `RecordIssued`'s serial write.
- Guard: `Consume`'s `previous_certificate_serial` clause (`connector_enrollment.go:87-90`) already serializes renewal-after-renewal, and `RecordIssued` guards the initial-write with `certificate_serial IS NULL AND EXISTS(...consumed...)` plus `RowsAffected()==1` (`connector_enrollment.go:125-135`). So there is no double-admission; the half-finished edge is contained.
- This is a documentation/mental-model finding: the consume/issue boundary is a two-phase operation where a failure in phase 2 is correctly fail-closed but leaves a permanently-consumed one-use grant. Worth noting for operators, not a vulnerability.

## Befund 3 (low): doc claim "Keycloak reloads certificates every 30s" vs code `--https-certificates-reload-period=35s`

- File/line: doc claim vs `internal/identityprovider/keycloak_files.go:87` (`keycloakCertificateReloadPeriod = 35 * time.Second`) rendered into compose as `--https-certificates-reload-period=35s` at `keycloak_files.go:519` (member template).
- The code comment at `keycloak_files.go:86` documents the intent: "Keycloak requires a TLS reload interval strictly above 30 seconds." The compose emits 35s, consistent with the code and the comment.
- Status: after a precise re-read the only "30s" strings in the keycloak/identity/trust area are unrelated Caddy/HAProxy/PostgreSQL timeouts; there is no spec/doc line that states the Keycloak reload interval is exactly 30s. No mismatch found — recording the check performed so the (c) slice is evidenced. If a doc elsewhere states a 30s Keycloak reload cadence, it would contradict the code (35s) and should be corrected; the code is the authority here.

## repo-rule compliance

- R1: static read + unit-only tests only. No `.github/**` touched. No containers/compose started on this host. No product changes.
- Read worktree isolated under `/tmp/opencode/w914-authsurf-wt`; no scratch in the ecosystem root. Repro test lives in the worktree only and is NOT committed to the product branch (mission forbids product changes; the test is evidence of the befund, not a durable product test — it would need CI wiring under `.github/**` (Owner scope) to become durable).

## cleanliness

- No docker/podman containers, networks, volumes or compose projects started on this host.
- No compose project was launched in the read worktree; no daemon started here.
- "cleanliness: PASS"

## END

- mission-hunt-authsurf.md: DONE — befund-1.md written with all three slices and repro.
