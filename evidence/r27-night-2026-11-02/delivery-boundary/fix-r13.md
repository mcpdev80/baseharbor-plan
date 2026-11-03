# w20-delivery-vanish evidence — PR #1333, t-20261018-r27-delivery-boundary

Lane: w20-delivery-vanish (Worker). Coordinator f49a3303.
Basis = mission base 0270e48069e743c96bf38b5e02d078709e2e78f1 (branch origin/work/r27-delivery-boundary). develop 9a57107f8b2b71011b66025efbb73b39ab1ff12f is Vorfahr (merge-base --is-ancestor rc=0).

## END line
END_DONE w20-delivery-vanish: head=87d1df12afcf397c82b89eb14fc07286369db2a3 vanish=e2e-seam doku=selection-mode | PR #1333 OPEN head=87d1df12; all substantive gates green; single PR·Selected Checks fail = pre-existing Node.js 20 deprecation (.github#93), not code-related.

## TASK (what was built, in product language)
1. End-to-end vanish regression: a nil preferences save against a previous record that vanishes between the one-writer guard read and the preferences-retention read fails closed (no silent drop of separately owned provider preferences), via a package-internal test seam so the real SaveDeploymentRecord path (not just loaders in isolation) is exercised, with a byte-stability proof.
2. One wording line each in EN + DE ADR 0022 so the one-writer refusal reads as a record-save check on recorded state with the owner following the normalized selection being saved (baseharbor for direct, external for delegated saves), not live reconciler detection.

## RESOLUTION OF INITIAL SCOPE CONFLICT (coordinator f49a3303 answered — merge, don't guess)
Initially my lane (work/r27-delivery-boundary @ bcc0eed2) lacked 0270e480's fix on a divergent branch. Per the owner's directive (1): `git merge --no-edit origin/work/r27-delivery-boundary` in the worktree after proving `merge-base --is-ancestor 0270e480… HEAD rc=0`. Merge succeeded (4780b42f), bringing in the fail-closed guard + 6 vanish tests. Then per (2) I checked what still diverged from the mission and applied the two missing pixels (seam + wording), below.

## PLAN (numbered)
1. Merge origin/work/r27-delivery-boundary (0270e480 ancestry proved rc=0).
2. Verify docs: EN+DE ADR 0022 first-consequences bullet. EN already = mission wording; DE still said the old "gilt als ungesetzt und folgt der Direktvorgabe" — replaced with mission B2 wording (selection-mode formel).
3. Code: add package-internal seam var testHookAfterGuardRead to deployment_store.go (after guard-read/previousExists+owner established, before retention-read, nil default, production path untouched).
4. Tests: rewrite TestRetentionVanishedRecordFailsClosed to the real SaveDeploymentRecord path using the seam to delete the record between the two reads; assert fail-closed + byte-stability (file stays ENOENT). Rewrote the comment to state it fails vs the pre-fix swallowing code.
5. Proof: against buggy base (seam call removed) the test FAILS ("nil save against vanished previous record must fail closed, got nil error"); with the fix it PASSES.
6. Local checks: go build ./... rc=0; go test ./internal/deployment ./internal/delivery green. Broader sweep: only internal/telemetry fails (OTLP TLS — pre-existing on clean base, unrelated).
7. Ancestry/merge-base proof (develop rc=0), write-set grep (0 .github changes), commit 87d1df12, push FF, ls-remote==head.
8. CI: all substantive gates green (delivery-package-tests, cli-build, cli-vet, cli-guided-tests, documentation-audit, mkdocs-en/de-strict, Trusted Plan, Workflow policy, Focused Python). Single PR·Selected Checks fail = pre-existing Node.js 20 deprecation (.github#93), confirmed identical on the 0270e480 run before my push.

## TEIL A — CODE SEAM
File: internal/deployment/deployment_store.go.
- New package-level var `testHookAfterGuardRead func()` (line ~29), nil default, production path untouched.
- Call added inside SaveDeploymentRecord immediately after refuseOneWriterMutation(guardRecord) and before validateRemoteProject(record) — i.e. exactly after the guard-read (previousExists + persisted owner established) and before the retention re-read. Style follows the cmd/baha observedAt seam.

## TEIL A — TEST (real SaveDeploymentRecord path)
File: internal/deployment/preferences_retention_test.go. TestRetentionVanishedRecordFailsClosed rewritten:
- Seeds a valid previous record (byteStabilityFixture), then anchors the seam to delete the on-disk record exactly once between the guard-read and the retention-read.
- Calls the REAL SaveDeploymentRecord(nilSave(id)); asserts a non-nil error (fail-closed) and that the file stays absent (os.Stat → ENOENT) — byte-proof, since the record was genuinely gone after the guard confirmed it existed.
- Proven to FAIL against the pre-fix code (swallowed ENOENT → nil error) and PASS with the fix.

## TEIL B — DOKU WORTLAUT (mission PUNKT 2, exact)
EN docs/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md:
- replaced "…, treated as unset and follows the `Selection.Normalize` direct default; …" with
  "…, treated as unset, and the owner then follows the normalized selection being saved (`baseharbor` for direct, `external` for delegated saves); …"
DE docs/de/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md:
- replaced "…gilt als ungesetzt und folgt der Direktvorgabe von `Selection.Normalize`…" with
  "…gilt als ungesetzt; der Besitzer folgt dann der normalisierten gespeicherten Selektion (`baseharbor` bei direktem, `external` bei delegiertem Speichern)…"

## REPO-RULE COMPLIANCE
- Isolated worktree at /tmp/opencode/w20-delivery-vanish-wt; changes only in the task write-set.
- Write-set: 4 files (2 docs, 1 .go, 1 _test.go). grep for .github = 0 changes.
- `git add <file>` only (never `git add -A`). FF push (0270e480..87d1df12), no force.
- No other generic test engine; seam follows existing observedAt style.
- No secrets logged.

## CI
Pushed 87d1df12 → work/r27-delivery-boundary. PR #1333 OPEN, head 87d1df12afcf397c82b89eb14fc07286369db2a3, ls-remote==head.
Green: delivery-package-tests, cli-build, cli-vet, cli-guided-tests, documentation-audit, mkdocs-en-strict, mkdocs-de-strict, Focused Python, Trusted Plan, Workflow policy.
One gate `PR · Selected Checks` = failure: `.github#93` "Process completed with exit code 1" — pre-existing Node.js 20 deprecation (forced to Node 24). Confirmed identical on the 0270e480 run (07:22) before my push. Not code-related.

## STOP
Seam on real SaveDeploymentRecord path + byte-stability; EN/DE wording = mission-exact selection-mode formel. All task points covered. END lane DONE.

