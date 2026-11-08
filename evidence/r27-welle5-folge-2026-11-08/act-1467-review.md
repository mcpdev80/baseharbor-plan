# CODEX-REVIEW 0427-154 — PR #1467

## PLAN

1. Read the 0427-154 acceptance and HD5 BF-1 evidence.
2. Verify the exact PR head, changed files, code paths, tests, ancestry/base comparison, and terminal hosted checks.
3. Record the verdict and a specific correction recipe in this review act.
4. Publish only this evidence file to baseharbor-plan origin/main and verify its remote tree entry.

## Review identity

- Role: REVIEW
- Card: 0427-154, `t-20261108-bughunt-openbao-stale-manager-cred`
- Candidate: PR #1467, head `2d929127c343094234f07581c9fdfa9083fdb224`
- Current base observed: `develop` at `f05d6ee2e596da73056dfd1bda64a79ebbfe6b92`
- PR state: open, non-draft, mergeable, `CLEAN`
- Exact-head hosted run: [42479206678](https://github.com/mcpdev80/baseharbor/actions/runs/42479206678), terminal `success`, event `pull_request`, head SHA exactly matches the candidate.
- Changed-file set: `internal/openbao/bootstrap.go`, `internal/openbao/bootstrap_test.go` only. This stays within the card's product write-set.
- Planning provenance before this evidence commit: `59ee497d5107d8078240418f01e6574fc90b7f20 refs/heads/main`.

## Findings

1. **KORREKTUR — acceptance requires a visible recovery notice, but the production path emits none.** The card and HD5 BF-1 require re-bootstrap “with clear notice.” In `internal/openbao/bootstrap.go:241-253`, the comment says the operator sees an informational note through diagnostics, but the implementation only removes the file and continues. The production caller `cmd/baha/openbao_operations.go:48-70` returns the bootstrap error/result and has no notice path. Thus the claim in the comment is not backed by an observable CLI result.

2. **KORREKTUR — the stale-file cleanup is fail-open on filesystem errors.** `internal/openbao/bootstrap.go:248-253` ignores `os.Remove(adminPath)` errors and continues to initialize. If removal fails, the stale credential remains while bootstrap proceeds; the cleanup step must either succeed or stop with a useful error.

3. **The initialized-server branch currently preserves fail-closed ordering, but its regression does not prove preservation of live credentials.** `Bootstrap` checks `state.Initialized` and returns `ErrAlreadyInitialized` at `internal/openbao/bootstrap.go:234-238`, before touching the admin file, so the present code does not overwrite credentials on this path. However, `TestBootstrapStillRejectsInitializedServerWithStaleCred` at `internal/openbao/bootstrap_test.go:1630-1658` does not compare the original credential bytes after the call, and `executor.initialized != true` is tautological because the fake starts initialized. The test would not catch a future destructive mutation before the refusal. This leaves the required stale+INIT counter-check under-asserted, even though the inspected current ordering is correct.

4. **Hosted CI coverage is present for the new regression.** The exact-head run's `PR · Validation · go-unit-tests` job (job `128727286571`) emitted `ok github.com/mcpdev80/baseharbor/internal/openbao 5.083s`, so `internal/openbao/bootstrap_test.go` ran in the CI unit-test group. The trigger was `pull_request`; the exact run and head are recorded above. `PR · Validation · openbao-package-tests`, `go-vet`, `go-build`, both native destroy-retry jobs, and `PR Selected Checks` also completed successfully. No workflow file was changed. The CI result does not address the missing notice, ignored remove error, or insufficient INIT preservation assertion.

5. **Diff and integration state.** The PR contains one candidate commit and only the two files listed above. Against the live base observed for this review, GitHub compare reported one commit ahead and 21 behind (`diverged`); GitHub nevertheless reports the PR `CLEAN` and `MERGEABLE`. This review does not approve a merge, and any later pushed/rebased SHA needs its own exact-head checks.

## Verdict

**KORREKTUR.** The current code correctly checks `Initialized` before cleanup, and the stale+uninitialized happy path is exercised in the bao package. The acceptance is not complete because there is no clear operator-visible notice, cleanup errors are ignored, and the INIT regression does not assert that the existing credential file remains byte-for-byte unchanged.

## Umsetzungsvorschlag

- `internal/openbao/bootstrap.go:241-255`: make stale-file recovery observable through a production return/result channel consumed by the CLI; do not rely on a comment or an unconnected diagnostics claim. Check and return any `os.Remove` error before initialization proceeds.
- `cmd/baha/openbao_operations.go:48-70` and its command output path: surface a clear one-time message that a stale manager credential was found on an uninitialized server and re-bootstrap is proceeding. Keep genuine initialized servers fail-closed.
- `internal/openbao/bootstrap_test.go:1584-1658`: in the uninitialized fixture, assert the notice is returned/emitted and that cleanup failure prevents the init operation. In the initialized fixture, save the original credential bytes and assert they are unchanged, assert `ErrAlreadyInitialized`, no executor initialization call, and no recovery file. Replace the tautological initialized-state assertion with a call-count/state-transition assertion.
- Required test: the focused `internal/openbao` tests pass with explicit notice, remove-failure, and stale+INIT byte-preservation assertions. The test must continue to run under `PR · Validation · go-unit-tests` on the next exact PR head; record that run's terminal status and output.
- Stop criterion: do not approve until the production CLI exposes the notice, cleanup failure is fail-closed, the INIT regression proves the old credential bytes survive unchanged, and the focused tests are green in the exact-head hosted unit-test job. Do not weaken `ErrAlreadyInitialized`.

## Repository-rule compliance

- Product review was read-only; no product files, branches, PR state, workflows, checks, or runner infrastructure were modified or triggered by this review.
- Evidence is stored only in baseharbor-plan. No compose project was started.
- `python3 scripts/plan.py check` on the fetched planning main reported 25 existing errors and 3 warnings, including stale generated views and lifecycle metadata in unrelated cards (`t-20261018-r27-connection-client`, `t-20261018-r27-protected-credentials`, `t-20261108-bughunt-list-target-failclosed`, `t-20261108-bughunt-quickinit-failure-explain`, and other generated views). I did not render or edit those unrelated files. The review act is being published as the specifically authorized evidence update only.

## END

END_DONE 0427-154-review: KORREKTUR for PR #1467 head `2d929127c343094234f07581c9fdfa9083fdb224`; the act is published on baseharbor-plan origin/main.
