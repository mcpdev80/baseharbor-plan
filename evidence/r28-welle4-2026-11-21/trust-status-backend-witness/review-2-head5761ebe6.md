# CODEX-REVIEW — #1702 second pass

## PLAN
1. Verify the live remote PR head and exact run before assessing the candidate.
2. Inspect the corrected fail-first `t.Fatal` assertion and its Prometheus plus exact `unreachable` evidence.
3. Verify the fail-first red proof in the round-4 evidence and report what it establishes.
4. Verify author and committer identity on the current candidate; mark the e0613d99 review superseded.
5. Record exact-head CI, findings or verdict, repo compliance, and cleanliness in this evidence.
6. Render/check Planning, publish this evidence to origin/main, and verify the published path.

## Candidate and provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1702/head refs/heads/develop` returned `5761ebe6914abab0817b8f5f7a68fba64d0069b1 refs/pull/1702/head` and `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop`.
- PR #1702 is OPEN, non-draft, base `develop`, exact head `5761ebe6914abab0817b8f5f7a68fba64d0069b1`. GitHub compare reports `ahead_by=5`, `behind_by=0`, `merge_base=d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`; current base is an ancestor.
- `gh pr diff --name-only` lists `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_seam_restored_0428_142_test.go`, `cmd/baha/app_status_result_test.go`, `cmd/baha/app_status_result_witness_boundary_0428_142_test.go`, `cmd/baha/perses_lifecycle.go`, and `cmd/baha/perses_lifecycle_transport_test.go`. No `.github/**` or `scripts/**` path is in the candidate diff.
- GitHub metadata for all five commits shows `author == committer == 0428-142-statuswitness`; the stale mixed-author identities from `review-1-heade0613d99.md` do not remain.

## Corrected fail-first assertion

- At `cmd/baha/app_status_result_witness_boundary_0428_142_test.go:157-170`, `TestPersesStatusWitnessEmptyResolvedSignalNeverResolvedProves` now fails with `t.Fatalf` if the Prometheus verdict is absent (`:165-166`) or if its state is not exactly `persesBackendUnreachable` (`:168-170`).
- The production mapping at `cmd/baha/app_status_result.go:124-138` emits `configured` only for a supported signal with proven Prometheus provenance; the supported-but-empty-provenance case emits `unreachable`.
- The round-4 fail-first evidence at `round-4-failfirst.md` records the named wrong-value probe, exit 1, and observed `state="unreachable"` (`BEFUND 1 — FAIL-FIRST PROOF`); it also records the restored assertion and passing corrected test. This establishes the negative assertion is sensitive to a wrong verdict rather than only logging it.
- CI job `PR · Go unit · cli-2` (`136974362151`) completed successfully on this exact head. Its log says `PASS cli-2: 455 passed / 20 intentionally skipped / 475 discovered; CLI inventory total=1837`. The log is shard-aggregate output and does not emit an individual test-name duration; no per-case timing is claimed.

## Hosted checks

- Run `44946315002`, event `pull_request`, head `5761ebe6914abab0817b8f5f7a68fba64d0069b1`, completed/success. It had 15 successful jobs, 21 skipped jobs, and 0 failed jobs. Skipped jobs are not passes.
- Terminal `PR Selected Checks` job `136976006559` completed successfully. Selected Go unit cells `cli-0`, `cli-1`, `cli-2`, `cli-3`, `owner`, and `packages` completed successfully; `go-vet`, `go-build`, source formatting, trusted plan, native gate plan, and workflow policy also passed.
- The run's `trusted-pr-plan` artifact is `pr-plan.json`, SHA-256 `038404ec4bd611aba8eb71ad56f949f14dd929e041e09e3feb3c8ce8be5b5094`. It is resolved against the exact head and develop base; it records normal broad validation fallback for the affected CLI paths and selects unit, vet, and build checks. The skipped-runtime-gate and release cells remain uncounted.

## Previous verdict and review result

- `review-1-heade0613d99.md` remains as the historical REQUEST CHANGES witness for the superseded head `e0613d9950a8caf3805c60c29b563ba8273230c5`. It is superseded by this exact-head review; it has not been edited.
- The new candidate fixes the fail-first assertion and has a single author/committer identity. I found no new implementation issue at the corrected head.

## Verdict

APPROVE — PR #1702 at `5761ebe6914abab0817b8f5f7a68fba64d0069b1`.

No merge performed.

## repo-rule compliance

- Reviewer-only, read-only review from GitHub remote source. No product edits, product push, local test suite, workflow dispatch, or merge.
- No `.github/**` or `scripts/**` change was made. The fail-first transcript is cited as prior lane evidence, not represented as a test run by this reviewer.
- Planning evidence is isolated to this file in the verified Planning repository; no other untracked evidence was staged.

## cleanliness

- Before review, shell PID `4008870`; `docker ps -a` listed the eight pre-existing `bh-itest-*` containers recorded above, all exited.
- After review, shell PID `4008870`; the eight pre-existing `bh-itest-*` containers remain exited. No containers or compose projects were started, stopped, or changed.

## END codex-rev-1747 DONE

#1702 approved at exact head `5761ebe6914abab0817b8f5f7a68fba64d0069b1`; run `44946315002` completed successfully with 15 jobs successful, 21 skipped, and 0 failures; plan-sha `038404ec4bd611aba8eb71ad56f949f14dd929e041e09e3feb3c8ce8be5b5094`; fail-first and identity corrections confirmed.

## Planning publication witness

- Evidence commit `e0273b919` was pushed to Planning `origin/main`; `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `e0273b919198a7ad6d292a5ce2656b821e7d6e4b refs/heads/main`.
- Exact output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/trust-status-backend-witness/review-2-head5761ebe6.md`:

```text
evidence/r28-welle4-2026-11-21/trust-status-backend-witness/review-2-head5761ebe6.md
```
