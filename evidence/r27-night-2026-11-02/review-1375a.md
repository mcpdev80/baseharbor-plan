# CODEX-REVIEW — PR #1375 consent-abort

- Candidate: `c24a6c7c7777c216d75c0cb76591984910ca8390` (SHA exact)
- Base: `ecbb88545f96473986f8f41394cffce58b97d2df` (`develop`, confirmed with `ls-remote`)
- PR: OPEN, DRAFT, mergeable; diff has three files (+153/-0). No `.github` or specification files changed.
- Verdict: **REJECT**. No approval or merge.

## Seven SHA-exact probes

1. **Refused apply then actual `destroy` returns 0 — FAIL / not demonstrated.** I ran `go test ./cmd/baha -run '^TestW120' -count=1` against an archive of the exact candidate; it passed. But `TestW120RefusedApplyWritesNothingLeavesDestroyableState` only calls `resolveApplication(..., "destroy")` at `cmd/baha/w120_consent_abort_repro_test.go:62-70`. It never invokes `app destroy --yes`, the destroy lifecycle, or checks an exit code. This does not meet the card's destructive counterprobe. The lane's earlier slice also reports the red-first destroy failure, but is not green evidence for this candidate's actual teardown.

2. **Valid-consent follow-up reaches READY — FAIL / not demonstrated.** `TestW120ConsentedApplyPassesChokePointAfterRefusal` validates and persists an `applying` record at `w120_consent_abort_repro_test.go:98-110`; it does not execute apply, runtime realization, or assert READY. The contract requires the full follow-up apply without manual cleanup.

3. **Correct record-before-mutation point and unchanged consent semantics — PARTIAL.** `deployment_record.go:122-150` validates consent before `SaveDeploymentRecord`, and the tests reject a wrong digest without recording consent. But the candidate's executable code diff in this file is empty: the only change is a comment. `git diff ecbb8854..c24a6c7c -- cmd/baha/deployment_record.go` shows comments only, so the claimed fix was already present in the base. The missing-digest behavior is referenced by the helper test and existing sentinel; candidate tests do not add a distinct real-apply missing-digest regression.

4. **Rollback failure is typed and fail-closed — PASS as not applicable to the proposed rollback-free path; no rollback is introduced.** The implementation returns before saving on invalid consent, so it has no rollback operation whose failure could be swallowed. This does not compensate for probes 1-3: the submitted tests do not prove the required lifecycle outcomes.

5. **Scope / no generic evidence engine / no `.github` — PASS.** Changed paths are `cmd/baha/deployment_record.go` and two focused test files only. No generic evidence engine, CI surface, or `.github` file was added.

6. **Package tests, build, gofmt, vet — PARTIAL.** The two new `TestW120` tests passed on the exact archived SHA. `go build -buildvcs=false ./cmd/baha`, `go vet ./cmd/baha`, and `gofmt -l` on all three changed files passed. Full `go test ./cmd/baha -count=1` was started but interrupted after it remained silent; it is not reported as passing. The candidate's latest hosted run `41863532371` has `Workflow policy` and `PR · Source format` successful, while `PR Selected Checks` is **skipped** and 14 other jobs are skipped. Required product coverage is not terminal green.

7. **EN/DE specification — PASS; no spec files changed.** Existing EN/DE candidate-contract text already requires missing consent to fail without writing state (`docs/spec/candidate-contract-v1.md` and `docs/de/spec/candidate-contract-v1.md`). The proposed rollback-free behavior is consistent with that requirement; no spec update is needed for this implementation.

## REZEPT

- **File:** `baseharbor/cmd/baha/w120_consent_abort_repro_test.go`.
- **Change:** replace the resolver-only assertion with an isolated, executable lifecycle regression that refuses an apply for missing and wrong `--confirm-candidate`, invokes `app destroy --yes` on that same environment, and asserts rc=0. Then invoke apply with the correct canonical digest and assert the real lifecycle reaches READY without cleanup.
- **Test requirement:** red-first the destroy and READY paths against the prior failure, then pass `go test ./cmd/baha` (plus the card's required `internal/deployment` coverage), build, vet, and gofmt on the final SHA. Keep consent validation fail-closed and at the pre-write point; do not introduce rollback semantics or record invalid consent.
- **Stop criterion:** do not accept while either actual destroy rc=0 or consented follow-up READY lacks an executed regression, while the candidate has no functional product-code delta for this bug, or while required hosted checks are skipped/non-green. Re-review the new exact head after correction.

## Review boundary

Read-only candidate review. Exact PR head and `develop` were checked independently. The local full package run was interrupted and remains unverified. Hosted skipped jobs are not counted green. No merge performed.

END_DONE codex-r1375a: verdict=REJECT open=actual-destroy-rc0,follow-up-ready,functional-fix,full-package-test,hosted-gates | The candidate adds no executable fix over develop and its tests stop before the required destroy and READY outcomes.
