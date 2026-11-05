# CODEX-REVIEW — PR #1384, round 2 (read-only)

Verdict: **REJECT** — exact candidate `3bb95cc794a9c2aa167a149618065ec998e9d812`.

## Candidate identity and write set

PR #1384 is open and ready, base `develop`; the PR API head equals the requested SHA. `ls-remote` reports `develop=24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/access-profiles=3bb95cc794a9c2aa167a149618065ec998e9d812`; develop is an ancestor. The exact name-only diff is six files:

```
cmd/baha/policy.go
internal/orgconfig/profiles.go
internal/orgconfig/profiles_test.go
internal/policy/assignment.go
internal/policy/assignment_test.go
internal/policy/model.go
```

This matches the round-2 reservation. The membership/identity chain remains blob-identical across develop and candidate: `internal/operatorauth/authorization.go` `885c61e2c889f9c95d3a5e1dcf7d588347e2adfd`; `internal/identity/principal.go` `f4794f51d0d0ceabd5a0257afac45bc201b24d6a`; `internal/orgconfig/source.go` `188ba03990ac757b54c691c6871f764865cc88fb`; and `internal/orgconfig/store.go` `1ca330c8fece4e164819fb01d49a86d149389486`. `internal/policy/model.go` is intentionally changed to carry profile revision in a finding.

## Six cases and mutations

I ran `go test ./internal/orgconfig/... ./internal/policy/... -count=1` at the exact SHA; both packages passed. The six required cases are covered by these tests:

| Case | Test | Result |
| --- | --- | --- |
| Assignment | `TestResolveAssignsAllowProvesAssignmentAdapter` | pass |
| Revocation through adapter | `TestResolveRevokedViaAdapterFailsClosed` | pass |
| Ambiguous name | `TestAmbiguousNameFailsClosed` | pass |
| Stale revision | `TestUpdateBumpsRevisionProvesStaleDetection` | pass |
| Foreign tenant | `TestResolveForeignTenantFailsClosed` | pass |
| No rights escalation | `TestUpdateEscalationRejected` | pass |

I independently applied both requested counter-mutations in disposable worktree `/tmp/review1384b`, restoring each source file afterward:

- Disabled both revision guards in `Manager.Update`; `TestUpdateBumpsRevisionProvesStaleDetection` went **red** (rc 1: “stale revision (older than stored) must be rejected”).
- Disabled the operation-subset guard; `TestUpdateEscalationRejected` went **red** (rc 1: “edit adding admin to a read-only profile must be rejected”).

The worktree is clean after restoration. Additional boundary probe: `Manager.Update` documents that expected revision must equal the stored revision, but its implementation only rejects zero and values less than stored (`profiles.go:369-373`). An independently added temporary test confirmed that a future/mismatched revision is accepted. The guard must compare for equality to enforce the stated precondition.

## Production authority finding

The adapter itself is now dumb: `Adapter.Resolve` returns a `Finding`, and `ResolveFinding` folds it into `policy.Aggregate`. The identity/owner chain is unchanged as above. However, the production caller does not supply a profile assignment to that adapter. `cmd/baha/policy.go:170` constructs `orgconfig.NewManager(org)` with no profiles; repository-wide search finds no other production `NewManager`, `Create`, or `Revoke` call. At lines 174-175 it then asks for profile name `org` and fixed operation `OpRead`, and discards the returned error. An empty manager returns `ErrAssignmentUnknown`; the ignored error leaves a zero-value `Finding`, whose empty decision is ignored by `Aggregate` (which defaults to `Allow`). Thus the production path contributes no profile decision at all; the passing package tests exercise only in-memory managers populated in test code. The claimed adapter-to-aggregate production connection is nominal, not functional.

## CI record, including the foreign timing flake

The requested run `41981861515` is terminal overall **success** at the exact SHA. I inspected its jobs: only source-format and workflow-policy jobs passed; `PR Selected Checks` and the validations were **skipped**. The later run `41983173186` is terminal failure at the same SHA: `PR · Validation · go-unit-tests` failed in the unrelated `internal/development` test `TestSourceSnapshotDetectsChangeDuringRead` at `source_snapshot_test.go:224`, and `PR Selected Checks` consequently failed. The round evidence reports the same timing-sensitive failure once green and once red and identifies it with the separately carded snapshot-change-guard task. I do **not** attribute that failure to this PR's write set or use it as a product-code finding. I record that the claimed terminal-success run did not itself produce a successful Selected Checks job; this does not change the independent code findings above.

## Recipe

- **Files:** `cmd/baha/policy.go`, the profile source/manager path in `internal/orgconfig/profiles.go`, and their tests; `internal/orgconfig/profiles.go` revision guard/tests.
- **Change:** feed a real, owned profile assignment and the actual operation into the production adapter; do not create an empty manager, use the organization name as a profile name, hard-code `OpRead`, or discard resolution errors. Ensure unknown/revoked assignments produce an explicit fail-closed finding through `policy.Aggregate`, while mandatory denies still win. Require `expectedRevision == existing.Revision`.
- **Test requirement:** add a production-path test with a configured owned assignment that proves the adapter's finding reaches the aggregate; verify unknown/revoked assignment fails closed and mandatory deny remains; test zero, lower, equal, and future expected revisions; retain all six domain cases and both red-first mutations. At the corrected SHA, establish the applicable selected checks according to the separately recorded owner decision for the external snapshot timing failure.
- **Stop criterion:** the production path has no actual profile data/operation, silently drops an adapter error, permits a mismatched revision, or the escalation/revision mutants pass their original tests.

No PR, branch, or card action was taken. The later snapshot timing failure is acknowledged as a separately tracked foreign test flake, not a finding against this PR.
