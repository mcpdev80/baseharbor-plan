# 0427-node-cli-r4 — authoritative enrollment/certificate state + production-path regressions

Lane: 0427-node-cli-r4 (b9097188, flash, fresh)
Card: t-20261018-r27-node-cli · Candidate chain: PR #1436 branch `work/r27-node-cli-r3` base head `eee54634a`
Review acted on: `evidence/r27-welle5-folge-2026-11-07/node-cli/act-1436-review.md` (CODEX-REVIEW r3 = REQUEST-CHANGES)
Disposition: STOPPED — Owner-STOP 2026-11-07, Owner + ChatGPT took the enrollment lifecycle over on this card.

## PLAN

1. Verify planning-repo toplevel and remote (wrong-zone check); read mission, card, r3 review artifact and r3 evidence — done.
2. Claim `t-20261018-r27-node-cli`: the card on origin/main is already `state: active` with `owner: lane-0427-039-node-cli-r4`, which is this lane. `plan.py claim` refuses an already-active task ("only planned, wait or blocked tasks can be claimed"), so no re-claim and no planning churn was needed. Done.
3. Cut an isolated worktree from PR#1436 head `eee54634a`, record the base attestation SHA, merge `origin/develop`, prove ancestry (rc0) — done, no merge commit needed (develop is already an ancestor).
4. Locate the authoritative certificate/enrollment expiry + revocation source in the connector/node-trust data path; cite file:line here — done (section below).
5. Derive PENDING/ENROLLED/EXPIRED/REVOKED from that source, fail-closed — done in production code.
6. Rewrite the regression tests so they call the real production path (connector/enrollment store -> classify -> CLI output), table-driven: enrolled, cert-expired -> EXPIRED, revoked -> REVOKED, none -> PENDING/fail-closed — done.
7. Mutation-check that each new test fails when the production derivation is broken — 6 of 9 caught, 3 gaps open at stop.
8. Local checks: `go test ./cmd/baha`, `go vet`, `go build`, `gofmt`; confirm the delta is only `node.go`/`node_read.go` + tests — done, all green.
9. Push the candidate to the branch named in the mission (exactly one candidate per chain) — pushed `a267ae031`; hosted pr-check not started before the stop.
10. Publish this evidence file to origin/main, verify presence with `git ls-tree`, then post END to `594fd2f5-4e80-43b6-9841-92879146a85e` — done as a STOPPED handoff.

## Planning repo verification (wrong-zone check)

Exact output, before the first evidence commit:

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan

Remote: `https://github.com/mcpdev80/baseharbor-plan.git`; local HEAD == `origin/main` == `ccd7b86cc12a7993f01d676a4f7ad1617c729a57` at turn start.
Note: an unrelated pre-existing working-tree modification to `node-cli/round-3.md` (from the r3 lane) was observed and left untouched and unstaged, as were a foreign new file `onboarding-wizard/round-3.md` and `tasks/t-20261105-r27-compose-host-isolation.md` that appeared in this shared checkout during the stop.

## Base attestation

- Exact remote refs (fetched, `git ls-remote origin`):
  - `eee54634a65eeab6f16205e91009ea0de9de91f2  refs/pull/1436/head` (the candidate base cut from)
  - `eee54634a65eeab6f16205e91009ea0de9de91f2  refs/heads/work/r27-node-cli-r3` (mission-named branch)
  - `0dc4c4d4f3e8c27bc9d48019d0b210807d45f951  refs/heads/work/r27-node-cli` (superseded r1/r2 branch, untouched)
  - `8a3f58da905fad52327d33466fde1d9568092519  refs/heads/develop`
- Base SHA cut from: `eee54634a65eeab6f16205e91009ea0de9de91f2` (PR#1436 head).
- Worktree: `/tmp/opencode/0427-node-cli-r4-wt`, local staging branch `work/r27-node-cli-r4-wt`; the final push went to the ONE mission-named candidate branch `work/r27-node-cli-r3` (no second remote candidate created; the staging branch was never pushed).
- Ancestry rc0: `git merge-base --is-ancestor origin/develop eee54634a` -> rc 0 (develop `8a3f58da9` is an ancestor of the base); `git merge --no-edit origin/develop` -> "Already up to date". Merge-base is exactly `8a3f58da9`.
- After the commit: `git merge-base --is-ancestor eee54634a a267ae031` -> rc 0, so the base is an ancestor of the first (only) new commit.
- Candidate-only log `git log --oneline origin/develop..a267ae031` lists exactly two task-chain commits plus this lane's `a267ae031 wip(r27 node-cli r4)`: no foreign candidate is carried on top.

## Authoritative source for enrollment/certificate state

Grep/read of the connector + node-trust data path (all file:line at base `eee54634a`):

- The REAL enrollment record is the Core (server-side) `connector_nodes` row, written only at
  redemption and revoked only by disconnect:
  - `internal/database/migrations/0005_connector_enrollment.sql:1-10` — `connector_nodes` columns
    `certificate_serial`, `certificate_expires_at` (NULL = never issued; the CHECK binds serial and
    expiry together), plus `certificate_revoked` added by
    `internal/database/migrations/0006_connector_certificate_admission.sql`.
  - `internal/database/connector_enrollment.go:100-103` (`RecordIssued`) — the certificate serial and
    the issued certificate's NotAfter are written ONLY after the one-use grant was CONSUMED and the CSR
    signed; a grant that was merely created never touches this row.
  - `internal/database/connector_enrollment.go:172-173` and `:236-238` (`RevokeCertificate`,
    `RevokeCurrent`) — revocation is a server-side boolean on that same row, never a local file fact.
  - `internal/database/connector_enrollment.go:183-214` (`ConnectorEnrollmentStore.Status`) — the
    authoritative classifier: `Enrolled` is derived from `certificate_serial IS NOT NULL AND
    certificate_expires_at IS NOT NULL`, `ExpiresAt` is `certificate_expires_at` (the certificate
    NotAfter), and `Revoked` is `certificate_revoked`. Missing/ambiguous rows return
    `targetenrollment.ErrDenied` (fail-closed), never a guess.
  - `internal/targetenrollment/authority.go:64-74` (`NodeLifecycleStore`, `NodeStatus`) and
    `:194-200` (`Authority.Status`) — the contract surface the CLI must consume.
- What is NOT authoritative for enrollment: the one-use bootstrap grant. `Grant.ExpiresAt` is
  `time.Now()+lifetime` with lifetime capped at 10 minutes
  (`internal/targetenrollment/authority.go:106-123`, enforced at `:107`) and is also what
  `Bootstrap.ExpiresAt` returns to the CLI (`internal/targetenrollment/http.go:151-156`). The r3
  candidate persisted exactly that value (`cmd/baha/node.go:202-210`) and classified from it
  (`cmd/baha/node_read.go:59-69`) — the review finding is confirmed by the source.
- Reachable authority from the CLI within the assigned write set: the operator-authenticated
  lifecycle endpoint `POST /api/v1/connectors/status` (`internal/targetenrollment/http.go:24`,
  routed at `:92`, handler `:166-229`) backed by the same `ConnectorEnrollmentStore.Status`
  (`internal/controlplaneruntime/server_run.go:307,316` wires the production handler to the
  PostgreSQL store). `node list` therefore reads the certificate/enrollment lifecycle from Core
  instead of from grant or local-file truth.
- `revoked` and `expires_at` (certificate) on that endpoint are already the certificate lifecycle,
  not the grant: grant expiry never reaches the status response.

## STATUS (Owner-STOP 2026-11-07, controlled handoff)

Owner took the task over with ChatGPT. Work stopped in a controlled state; this section is the
authoritative handoff. Nothing after this point was changed or pushed by this lane.

### Finished

1. Authoritative source determined and cited above. The real enrollment/certificate lifecycle lives
   in the Core `connector_nodes` row (serial + `certificate_expires_at` + `certificate_revoked`),
   written only on redemption by `RecordIssued` and flipped only by `RevokeCurrent`; the CLI-reachable
   authority is the operator-authenticated `POST /api/v1/connectors/status`
   (`internal/targetenrollment/http.go:166-229`) over `ConnectorEnrollmentStore.Status`
   (`internal/database/connector_enrollment.go:183-214`). Grant expiry is provably not that source
   (`internal/targetenrollment/authority.go:106-123`).
2. Finding 1 fixed in production code. `classifyNodeTrust` (new, in `cmd/baha/node.go`) is the single
   rule shared by `node list` and `node status`; the grant-derived `Enrolled`/`ExpiresAt` fields are
   gone from `nodeRecord`, replaced by `grant_expires_at` registration metadata that no label or
   displayed expiry can follow. `node list` now performs the lifecycle read per node and fails closed
   to PENDING (with an explicit `Authority` reason line in the table) when the record, session or
   authority is unavailable. `REVOKED` comes only from the authority. `requestNodeLifecycle`
   additionally pins `runtime` in the identity confirmation and refuses `enrolled` without a
   certificate expiry.
3. Finding 2 fixed: `cmd/baha/node_read_test.go` rewritten to drive the real production path. The
   fixture mounts the actual Core enrollment handler (`targetenrollment.NewHTTP` + `New`) over TLS
   behind a real `serviceaccess.LocalIssuer`, then a test obtains a grant through
   `requestNodeAuthorization` (the exact call `baha node add` makes), redeems it through
   `Authority.Enroll` (the connector's exchange) and revokes through `Authority.Disconnect` (the
   revocation owner). State is asserted only from `nodeList`/`nodeStatus` output — the test-only
   `renderTrustState` helper is deleted. Table-driven: enrolled, certificate-expired -> EXPIRED,
   revoked -> REVOKED, unredeemed/none -> PENDING, plus authority-unavailable, missing-session,
   legacy-record, serial/capability-omission and unconfirmed-identity cases.
4. Local checks green: `gofmt -l cmd/baha` clean, `go vet ./cmd/baha` clean, `go build ./cmd/baha`
   OK, `go test ./cmd/baha -run TestNode -count=1` -> ok (all node tests including the rewritten
   regressions and their subtests). Delta is only `cmd/baha/node.go`, `cmd/baha/node_read.go`,
   `cmd/baha/node_read_test.go` — no `.github/**`, no other card's files.
5. Mutation harness recorded 6 of 9 mutations CAUGHT (grant-expiry state, local-state REVOKED,
   unconfirmed ENROLLED, status ignores revocation/expiry, classifier without EXPIRED, node-add
   claims enrollment), the script is `/tmp/opencode/0427-node-cli-r4-mutations.sh`.

### Open at stop (the next steps that would have been taken)

1. Three of nine mutation checks were MISSED, so those assertions are not yet load-bearing; the
   regressions must be extended until all nine are caught:
   - M7 dropping the lifecycle identity confirmation (`result.TargetID/NodeID/Runtime` guard in
     `cmd/baha/node_read.go`) still passed `TestNodeStatusUnconfirmedCoreIdentityFailsClosed` — that
     test fails earlier (missing record), so it never reaches the identity guard. Needs a case where
     Core answers for a different identity.
   - M8 dropping the `enrolled && expires_at.IsZero()` guard still passed — no test yet returns that
     shape from the authority.
   - M9 displaying `record.GrantExpiresAt` instead of `status.ExpiresAt` in the list still passed,
     because in that subtest the grant metadata and the certificate expiry were never set apart.
2. No hosted CI run was started for the r4 SHA (self-run duty not discharged): the pushed candidate
   `a267ae031` has no PR check result recorded. Per the scope split, `.github/**` is Owner scope and
   no rerun/dispatch was triggered by this lane.
3. Not verified: whether the widened `requestNodeAuthorization` signature (explicit grant/certificate
   lifetimes instead of the hardcoded 600/86400 literals) and the 24h `certificate_ttl_seconds`
   remain acceptable to other consumers. Only `node.go` calls it in this tree.

### Last SHA and ancestry

- Candidate branch (mission-named, single candidate): `work/r27-node-cli-r3`, PR #1436, head now
  `a267ae031affaa63b244faed11d16fd475023c2a`.
- Push was a plain fast-forward from the base `eee54634a` (remote BEFORE
  `eee54634a65eeab6f16205e91009ea0de9de91f2`, AFTER `a267ae031affaa63b244faed11d16fd475023c2a`); no
  force-push, no history rewrite, nothing half-finished deleted.
- Re-verified at the stop: `git ls-remote origin refs/heads/work/r27-node-cli-r3` ==
  `a267ae031affaa63b244faed11d16fd475023c2a` == local HEAD, and the worktree reports no uncommitted
  changes: the entire working state is on the remote branch.

### Ownership note at stop

- The card already names this lane (`owner: lane-0427-039-node-cli-r4`, `kanban_status: active` on
  origin/main), so no claim publishing was needed; `plan.py claim` refuses an already-active task.
  No other card's note was touched.

## Status

- STOPPED (Owner-STOP 2026-11-07). Candidate pushed to the mission-named branch; both review findings
  fixed in production code with green local checks; 3 of 9 mutation gaps and the hosted CI run open.
  Owner + ChatGPT continue on the enrollment lifecycle (cards #1435/#1436).

END_STOPPED 0427-node-cli-r4: candidate pushed to work/r27-node-cli-r3 @ a267ae031 (PR#1436); both review findings fixed in production code, 11 rewritten production-path regressions green locally, 3 of 9 mutation checks still missed and no hosted CI run started.
