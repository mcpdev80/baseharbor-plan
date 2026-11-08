# CODEX-REVIEW — 0427-013 access-wizard r7 — PR #1430

## PLAN

1. Refresh exact PR/develop refs and verify the candidate diff against the r6-reviewed head.
2. Inspect the same-key persistence guard and production CLI assign/offboard regressions.
3. Verify distinct-key coverage, prior cancellation/offboarding findings, and exact-head hosted CI.
4. Audit the paired before/after sample required by the r6 review.
5. Publish this SHA-specific verdict and correction recipe in baseharbor-plan.

## Candidate and hosted evidence

- PR #1430 is OPEN/MERGEABLE on exact head `931b43677bad186c73480f5923d4cf7716585ca9`, confirmed by `gh pr view` and `git ls-remote refs/pull/1430/head`.
- Base `develop` is `e39b0004346cdfd082e34ba55d94d24757bbbd27`; it is an ancestor of the candidate (`git merge-base --is-ancestor` exit 0).
- Delta from the r6-reviewed head `9dd2f779fa2445257d4f7f3c99a43b1245493818` is four files: `internal/orgconfig/profiles.go`, `internal/accesswizard/controller.go`, `cmd/baha/access_wizard_command.go`, and `cmd/baha/access_wizard_persistence_test.go`.
- Hosted run `42445068559` is terminal success on the exact candidate SHA. `PR · Validation · go-unit-tests` and `PR Selected Checks` passed. The job log reports `ok github.com/mcpdev80/baseharbor/cmd/baha`; this package contains the new CLI regressions and existing distinct-key and cancellation/offboarding tests. Unrelated runtime/Pin jobs were skipped.

## Review result

**REQUEST-CHANGES — evidence-only correction.** The r7 code delta resolves the r6 same-key overwrite finding and its production CLI regression tests are sound. The required r6 paired-sample artifact is not fully present in the published Round-7 evidence: it includes the BEFORE test-name sample, but the AFTER section only says it contains “dieselben 14 Zeilen” and that the diff is empty. The named raw AFTER file is under an ephemeral `/tmp/opencode/...` path, not in the planning evidence, so the paired sample cannot be audited from the published record.

## Findings

### Same-key assignment fails closed

`internal/orgconfig/profiles.go:660-689` checks the loaded state before saving. If a snapshot key is occupied by a non-empty different owner, `PersistActive` returns `ErrOwnerCollision` before `SaveActive`. The assign CLI catches that error, records it on the controller, and returns denial (`cmd/baha/access_wizard_command.go:80-89`); `Controller.Run` presents the collision reason and returns the error (`internal/accesswizard/controller.go:217-231`). `TestAccessAssignSameKeyForeignOwnerFailsClosed` uses the exact `alice@prod` key, requires a collision report and error, compares the full active-state bytes before/after, and checks the foreign row (`cmd/baha/access_wizard_persistence_test.go:466-503`). This closes the r6 silent overwrite.

### Same-key offboard fails before persistence

`TestAccessOffboardSameKeyForeignOwnerFailsClosed` selects `bob` on both `dev` and `prod`, with an owned `bob@dev` row and a foreign-owned `bob@prod` row. The production route rejects the unavailable owned `prod` row before `CommitActive`, then compares the full file bytes and checks both the foreign row and owned `dev` row remain (`cmd/baha/access_wizard_persistence_test.go:505-539`). The CLI now reports the denial cause through `NoteCommitError` (`cmd/baha/access_wizard_command.go:129-159`). This preserves batch atomicity and does not silently overwrite or delete the foreign row.

### Distinct-key and earlier findings

The r7 delta retains the r6 distinct-key assign/offboard regressions. The new `PersistActive` unit test also exercises a distinct-key merge and a revoke of the owner's `bob@dev` while preserving the foreign `bob@prod` row (`cmd/baha/access_wizard_persistence_test.go:576-654`). The controller delta only adds reporting for a denied persistence/authority callback; pre-confirmation cancellation remains on the existing early-return path. The exact-head Go unit job passed, including package `cmd/baha`, and the published r7 evidence records the focused `internal/orgconfig`, `internal/accesswizard`, and CLI checks green. I found no regression to the r3 cancellation or r4 fail-closed findings.

### Paired sample is not auditable in the published evidence

Round 7 names the command `go test ./cmd/baha/ -count=1`, lists the BEFORE sample, and then asserts that AFTER had the same 14 rows and the diff was empty. It does not include the AFTER rows or a durable artifact containing the raw pair. The referenced `/tmp/opencode/w013-r7-after-set.txt` is not part of origin/main. Also, the displayed bare per-test names do not match the ordinary output format of a successful non-verbose `go test` invocation, so the evidence should state the exact extraction command that produced them.

This is the sole outstanding review item. The sample gap does not invalidate the code review or the exact-head hosted CI result, but it leaves the explicitly requested r6 environment-rotation comparison unverifiable from the published record.

## Correction recipe

- File: `evidence/r27-welle5-folge-2026-11-08/access-wizard/round-7.md`. Add a small durable paired sample with the same representative rows shown for BEFORE and AFTER, and the exact command/extraction used to produce those rows. Include the comparison result and keep any raw artifact under this evidence directory rather than an ephemeral `/tmp/opencode` path.
- Test requirement: no product test rerun is needed for this evidence-only correction; the existing exact-head CI run `42445068559` remains valid for candidate `931b43677bad186c73480f5923d4cf7716585ca9`. Do not change product source or `.github/**` to repair this documentation gap.
- Stop criterion: accept this review only after the published round-7 record contains a directly comparable before/after sample and identifies the command that generated it. The code-level same-key, distinct-key, cancellation/offboarding, and hosted unit checks are otherwise satisfactory on this SHA.

## Evidence provenance and repo-rule compliance

- Planning source `round-7.md` is on planning `origin/main` as blob `17adad98c65cd5d4eac7db5d3679e7851cbfab66`; r6 act is blob `4dd5d1ef9d6b78a1eb34bdb8188fd633b2d36f84`.
- Product source was reviewed from a fresh clone; PR #1430 remained at `931b43677bad186c73480f5923d4cf7716585ca9` during review.
- No product files, workflows, or CI runs were changed or triggered by this review. This evidence is planning-only and contains no Markdown checkbox task lines.

END_DONE 0427-access-wizard-review-r7: REQUEST-CHANGES, evidence-only paired-sample correction; candidate `931b43677bad186c73480f5923d4cf7716585ca9`.
