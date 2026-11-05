# CODEX-REVIEW — PR #1383 (read-only)

Verdict: **REJECT** — exact PR head `9bf29c89846fcc8e672ace1905d99c0ff1176118`.

## Candidate identity, write set, and assertions

The PR is open, non-draft, based on `develop`; PR API head and `ls-remote refs/heads/work/r27-compose-isolation` both match `9bf29c89846fcc8e672ace1905d99c0ff1176118`. Current develop is `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`, a parent of the merge head. The exact diff against develop changes only `cmd/baha/repository_runtime_fixture_test.go`; no product source or `.github` path changes.

The lifecycle assertion-bearing test files are byte-identical between develop and the exact candidate: `cmd/baha/app_workload_integration_test.go` blob `34da220164c8b30392b850187da13c73c73f0705` and `cmd/baha/app_repository_integration_test.go` blob `836ca2dec721d2c31c962ff648dc7bf4e20f5cd7`. No assertion was removed or weakened. The changed file `repository_runtime_fixture_test.go` adds a `confirm-hash` extraction and a retry using that digest.

## Cell evidence

- **Consent cell:** the recorded no-consent baseline failed at `cmd/baha/deployment_record.go:140` with “candidate submission requires an explicit operator/automation consent (`--confirm-candidate`)” and printed a confirm hash. The clean-daemon fixed run `TestRepositoryComposeWorkloadOnlyLifecycleInCI` passed (155.87s). The fix binds that printed digest for one retry. The evidence run was on predecessor code head `5246bd9d`; that head's helper-file blob is identical to the helper blob at `9bf29c89`.
- **Polluted runtime cell:** the evidence records a live `local` Core on `baseharbor-local-default` causing the test to fail at `runtime_integration_test_support_test.go:55` with “existing native network lacks a protected Core or shared backend owner.” The same source says the fixture still calls `runWithIO` on the ambient daemon and has no daemon/socket/target isolation. Therefore polluted develop is red at the gate, but the candidate under the same pollution is also red; the consent retry does not clear this cell.
- The current exact-head PR run `41974796205` is terminal success and `PR Selected Checks` succeeded (GitHub Actions integration 15368), but its `validate`/runtime-integration job was skipped. The prior all-runtime-tests success `41970165123` is for head `5246bd9d`, not the exact merge head. Thus there is no exact-head green runtime result for the polluted cell.

## Isolierungsursache — offen

The cause is identified, but the requested per-test isolation is not implemented or proven. The fixture only supplies consent. It runs against whatever daemon is ambiently selected; local `ci-runtime-reset.sh` clears the shared daemon and can remove other lanes' resources, while the hosted runner's fresh daemon is an external job precondition. A fresh-runner pass does not show that a polluted host is isolated by the fixture. The lane's own final honesty section labels isolation “UNPROVEN by code.”

## Recipe

- **File:** `cmd/baha/repository_runtime_fixture_test.go` and the narrowly scoped runtime fixture it wraps.
- **Change:** give each lifecycle test its own daemon/socket or equivalent isolated runtime namespace, without resetting or deleting resources on a shared daemon. Keep the consent digest retry separate from runtime isolation.
- **Test requirement:** on the exact refreshed head, run the four required lifecycle tests twice against clean state and against a deliberately polluted shared state. Require the candidate to pass without touching the foreign Core/resources; retain the red-first no-consent failure and successful one-time digest retry. Confirm all existing assertions remain present.
- **Stop criterion:** if the candidate still fails at the ambient runtime gate, or isolation requires clearing shared daemon state, do not accept.

No PR, merge, comment, or card action was taken.
