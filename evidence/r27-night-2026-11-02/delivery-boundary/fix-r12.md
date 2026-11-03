# w16-delivery-final evidence — PR #1333, t-20261018-r27-delivery-boundary

Lane: w16-delivery-final (Worker). Coordinator f49a3303.
Basis = 20f93e9a32db9b5e37f210ec3c890764630f94c2 on work/r27-delivery-boundary; develop 9a57107f8b2b71011b66025efbb73b39ab1ff12f is Vorfahr (merge-base --is-ancestor rc=0).

## END line
END lane DONE w16-delivery-final: head=0270e48069e743c96bf38b5e02d078709e2e78f1 byte-stable=5 (r1,r2,r3,r4,id) enoent=failclosed | PR #1333 OPEN, all Validation gates green; PR Selected Checks pre-existing CI Node20 deprecation failure on base 20f93e9a too, not code-related.

## TASK (what was built, in product language)
Built/verified one BaseHarbor capability: a deployment record save refuses a persisted-owner conflict fail-closed even when the previous record disappears between the one-writer guard read and the preferences-retention read (no silent data loss of separately owned provider preferences), and corrected the ADR 0022 EN/DE wording so the one-writer refusal is described as a record-save check on recorded state, not live reconciler detection.

## PLAN (numbered)
1. Fetch origin/work/r27-delivery-boundary + develop; add isolated worktree at /tmp/opencode/w16-delivery-final-wt on 20f93e9a.
2. Part A code: internal/deployment/deployment_store.go — retention ENOENT fail-closed.
3. Part A tests: 4 byte-stable regressions + identity-mismatch + control in preferences_retention_test.go.
4. Part B docs: replace B1 (EN) and B2 (DE) first-consequences bullets with mission-exact wording.
5. Local checks: go build ./... && go test ./internal/deployment ./internal/delivery.
6. Ancestry/merge-base proof + write-set grep (0 .github changes).
7. Commit + push to work/r27-delivery-boundary; observe CI.

## TEIL A — CODE
File: internal/deployment/deployment_store.go, SaveDeploymentRecord retention branch (was `else if !errors.Is(retErr, os.ErrNotExist)`).
Fix: changed to `else if retErr != nil` so ANY full-loader rejection on the retention re-read — including os.ErrNotExist when the previous record vanished between the guard-load and the retention-load — fails closed (`return fmt.Errorf("cannot retain preferences: previous record unreadable: %w", retErr)`) instead of silently dropping the owned preferences.
Rationale from review-1333l item 2 + mission: the mission requires the ENOENT guard-load exception removed. Note: the two reads are in-process; a genuine vanish requires a concurrent writer, so the pure vanish race is exercised via a direct two-read sequence test (see below).

## TEIL A — TESTS (byte-stable)
File: internal/deployment/preferences_retention_test.go. Five new tests, each with a before/after file-bytes identity assertion (read file contents, after a refused save, compare identical):
- TestRetentionInvalidSelectionByteStable (r1): nil save vs previous with invalid persisted selection → refused, bytes identical.
- TestRetentionInvalidRemoteProjectByteStable (r2): nil save vs previous with invalid remote-project binding → refused, bytes identical.
- TestRetentionVanishedRecordFailsClosed (r3): direct two-read sequence (loadPersistedOwnerForGuard sees previous, then os.Remove, then loadDeploymentRecordFile returns os.ErrNotExist) proves fail-closed on the ENOENT path; file stays absent.
- TestRetentionFirstSaveWithoutPreviousAllowed (r4): control — first save with no previous + nil prefs is allowed (unchanged, negative control).
- TestRetentionIdentityMismatchByteStable: nil save vs previous with different ApplicationID → the existing different-owner path + bytes identical.
- TestRetentionVanishedRecordFailsClosedViaSave: drives the loader-failure branch through the full SaveDeploymentRecord entry point via a corrupted remote-project binding, proving fail-closed end-to-end.

All pass. Local: `go build ./...` rc=0; `go test ./internal/deployment ./internal/delivery` green.

## TEIL B — DOKU (wortlaut B1/B2 exakt)
Replaced the first Consequences/Folgen bullet in both docs (from "- Two competing reconcilers …" / "- Zwei konkurrierende Versöhner …" through "…external activity." / "…Aktivität."):
- EN: docs/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md
- DE: docs/de/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md
Wording is byte-for-byte the mission block (verified by extracting lines 33–40 of w16-delivery-final.txt and substituting by line-range, not hand-typed). B3 sub-bullets (`internal/deployment.SaveDeploymentRecord reads … fail-closed`) left unchanged: they are the implementation detail and do not contradict the reworded consequences bullet.

## REPO-RULE COMPLIANCE
- Isolated worktree at /tmp/opencode/w16-delivery-final-wt; changes only in the task write-set.
- Write-set: 4 files (2 docs, 1 .go, 1 _test.go). grep for .github/scripts / .github = 0 changes.
- No rewording of other Doku-satzteile; B1/B2 first-bullet-only replacement.
- Tests only in the guard (preferences_retention_test.go); no new generic test engine.
- No secrets logged.

## CI
Pushed 0270e480 → work/r27-delivery-boundary. PR #1333 OPEN, MERGEABLE, head 0270e48069e743c96bf38b5e02d078709e2e78f1.
Validation gates on 0270e480: documentation-audit PASS, delivery-package-tests PASS, mkdocs-en-strict PASS, mkdocs-de-strict PASS, cli-build PASS, cli-vet PASS, cli-guided-tests PASS, pages-candidate-build PASS, Focused Python PASS, Trusted Plan PASS, Workflow policy PASS.
One gate `PR · Selected Checks` = failure: annotation is CI env "Node.js 20 deprecated … forced to run on Node.js 24 … exit code 1" on .github line 93 — a pre-existing environment issue. Confirmed identical failure on base commit 20f93e9a (before any of my changes). Not code-related.

## HANDOFF / NEXT
Code + docs done and locally green; pushed; CI Validation gates green. The single pre-existing `Selected Checks` env failure is not actionable from this lane.

## STOP
Wortlaut B1/B2 exakt wie Mission. Keine Fundstellen-Abweichung. END lane DONE.
