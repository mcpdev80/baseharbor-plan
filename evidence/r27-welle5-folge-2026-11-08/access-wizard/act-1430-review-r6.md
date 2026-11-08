# CODEX-REVIEW — 0427-013 access-wizard r6 — PR #1430

## PLAN

1. Refresh exact PR/develop refs, verify hosted checks and read the published r5/r6 evidence.
2. Review the R6 persistence change and CLI regressions against the R5 finding; check cancellation and offboarding behavior from the prior rounds.
3. Reproduce the two regression tests against the pre-fix revision and the exact R6 candidate; probe owner-key collision behavior in an isolated fresh clone.
4. Record the SHA-specific verdict and correction recipe; publish this act in baseharbor-plan and verify candidate immutability.

## Review verdict: KORREKTUR

Reviewed candidate: PR #1430 head `9dd2f779fa2445257d4f7f3c99a43b1245493818`; exact base/develop head `e39b0004346cdfd082e34ba55d94d24757bbbd27`. Live GitHub API reports OPEN and MERGEABLE. `git ls-remote` returned the same develop and PR-head SHAs. `git merge-base --is-ancestor e39b0004346cdfd082e34ba55d94d24757bbbd27 9dd2f779fa2445257d4f7f3c99a43b1245493818` returned 0. The candidate's three-dot diff against develop has no `.github/**` paths.

Hosted PR run `42438784031` is terminal `completed/success` on the exact candidate SHA. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `wizard-registration-tests`, `PR Selected Checks`, and documentation jobs passed. Unrelated runtime/consumer cells were skipped. The PR remains read-only and unchanged by this review.

## Finding — foreign-owner collision still overwrites the foreign record

The R5 defect is fixed for foreign rows whose profile key differs from the active owner's rows. `PersistActive` now carries foreign-owner values from the loaded map and merges the manager snapshot (`internal/orgconfig/profiles.go:621-646`). The R6 CLI tests prove assign and offboard preserve a distinct foreign profile (`cmd/baha/access_wizard_persistence_test.go:409-454`).

However, the map key is `ProfileKey(name, target)`, and the profile contract defines identity as `(Name, Target)` (`internal/orgconfig/profiles.go:99-115,259`). `LoadProfiles` deliberately skips a foreign owner's row (`:348-363`). If an active-owner assignment creates the same `(Name, Target)` pair as a stored foreign row, the manager does not load that row, but the later snapshot loop writes the active profile to the same key and overwrites the foreign value (`PersistActive`, lines 635-645). Thus the comment that every foreign-owner row is preserved is not true for key collisions.

I reproduced this in the fresh candidate clone without changing the PR: I changed only the temporary regression fixture's foreign profile from `(foreign, prod)` to `(alice, dev)`, matching the CLI assignment's identity, and ran `go test ./cmd/baha -run '^TestAccessAssignPreservesForeignOwnerProfile$' -count=1`. It failed with `got {Name:alice Target:dev ... Owner:persist-acme ...} want {Name:alice Target:dev ... Owner:other-installation ...}`. The candidate currently reports the assignment as successful while replacing the foreign record.

## R6 regression evidence and prior findings

I independently applied the R6-only test-file diff to a temporary worktree at pre-fix candidate `bd5f2f10838eeadb89bc121a3719427b2bc6c005` and ran:

```text
go test ./cmd/baha -run '^TestAccess(Assign|Offboard)PreservesForeignOwnerProfile$' -count=1
```

Both new CLI regressions failed on that pre-fix revision: assign reported `foreign-owner profile "foreign" on "prod" must survive the write`; offboard reported the same. The same command on exact R6 candidate `9dd2f779fa2445257d4f7f3c99a43b1245493818` passed (`ok github.com/mcpdev80/baseharbor/cmd/baha`). This confirms the distinct-key regression is red without the fix and green with it.

The R6 fix commit `1c76570ae663586484ccadc963c7b4c4e73901f2` changes only `internal/orgconfig/profiles.go` and adds the two CLI regressions in `cmd/baha/access_wizard_persistence_test.go`; it does not change the cancellation controller or offboarding authority paths. The exact-head hosted Go unit job passed, and the r3 cancellation and r4 fail-closed tests remain part of that Go test suite. I found no R6-delta regression to those earlier findings.

The round-6 note claims a local 16/16 identical failure-list comparison for the environment-rotated broad test, but the published note contains no raw paired outputs or named sample rows. I cannot independently verify that count from the published artifact. This diagnostic claim does not override the green hosted run and is not the basis of the code finding above.

## Correction recipe

- File: `internal/orgconfig/profiles.go:629-646`. Before merging manager snapshots, detect when a snapshot's `(Name, Target)` key is occupied by a non-empty foreign `Owner`; fail closed rather than replace that row. The current contract treats `(Name, Target)` as identity, so do not silently allow owner collisions. If multi-owner duplicate identities are intended, change the persistent key schema and all readers/writers consistently instead of overwriting.
- File: `cmd/baha/access_wizard_persistence_test.go`. Add a production CLI regression with a foreign profile whose exact `(Name, Target)` matches the requested active-owner assignment. Require a clear denial, no success output, byte-identical active-state bytes, and the foreign profile's full definition unchanged. Add the corresponding offboard collision assertion if the public path can reach it; it must also fail closed without mutation.
- Test requirement: retain the distinct-key assign/offboard regressions; run the focused `internal/orgconfig`, `internal/accesswizard`, and `cmd/baha` tests. The new test is in `cmd/baha` and must remain selected by hosted `PR · Validation · go-unit-tests`; require terminal green `PR Selected Checks` on the corrected exact head.
- Stop criterion: no successful assign or offboard may overwrite/delete a foreign-owner row, including a same-key collision; all intended owner-local mutations and cancel/fail-closed behavior pass, with exact-head hosted checks green.
- Evidence follow-up: if the local 16/16 rotation comparison is used to classify environment-only failures, attach a small paired before/after output sample and command/test names so the equality can be audited.

## Evidence provenance

- Round-6 evidence fetched from planning `origin/main`: `100644 blob e5e6e2aadc943178a1ebfd70ee8d28fbac5054e0 evidence/r27-welle5-folge-2026-11-08/access-wizard/round-6.md`.
- R5 act fetched from planning `origin/main`: `100644 blob eeda9bb6106a9536adf9f2067ce5489f3fa95442 evidence/r27-welle5-folge-2026-11-08/access-wizard/act-1430-review-r5.md`.
- Canonical planning root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `origin` fetch and push URL: `https://github.com/mcpdev80/baseharbor-plan.git`. The fresh planning clone used for publication started at `fecf6dbeeffada1332567f9875e91b85da389fcf`.
- Candidate read-only verification at end: PR head remains `9dd2f779fa2445257d4f7f3c99a43b1245493818`; develop remains `e39b0004346cdfd082e34ba55d94d24757bbbd27`.

END_DONE 0427-access-wizard-review-r6: KORREKTUR; distinct-key owner merge passes, but same-key foreign-owner overwrite remains on candidate `9dd2f779fa2445257d4f7f3c99a43b1245493818`.
