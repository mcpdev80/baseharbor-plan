# PR #1579 Review R2

## PLAN

1. Verify exact PR #1579 r2 head/base ancestry, own-commit log, live PR state, and specified hosted run.
2. Review the getwd/chdir leak fix against c0664c8e4 and inspect the task evidence for any round-2 record.
3. Recheck app.id exclusion, UID stability/fail-closed behavior, genuine CLI tests, and the r1 STATE finding at exact SHA 2bf0c929.
4. Record the SHA-specific verdict and correction recipe, validate and publish evidence to origin/main, verify remote presence, and post END.

## Candidate and provenance

Role: CODEX-REVIEW, no merge. Fresh product clone `/tmp/opencode/mission-rev1579-r2-wt`; live remote witness:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
2bf0c929506a5b0e64b7359a6fc8711ab3f48526	refs/pull/1579/head
```

PR #1579 is OPEN and DRAFT, base `develop`, branch `lane-0428-uid-app`, exact candidate `2bf0c929506a5b0e64b7359a6fc8711ab3f48526`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 2bf0c929506a5b0e64b7359a6fc8711ab3f48526` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..2bf0c929506a5b0e64b7359a6fc8711ab3f48526` contains only the lane's two commits:

```text
2bf0c929 cmd/baha: fix CWD state leak in concurrent uid-app test
c0664c8e cmd/baha: bounded uid-app identity-stability regression slice (0428-050)
```

R2 changes only `cmd/baha/app_init_uid_app_slice_test.go` (16 additions, 3 deletions). `git diff --check` is clean. No product implementation or `.github/**` path changed.

## Exact hosted run and prior STATE

Run `43651708694` is terminal `completed/success`, event `pull_request`, workflow `CI · Source & Quality`, exact head `2bf0c929506a5b0e64b7359a6fc8711ab3f48526`. The formerly failing job `PR · Draft Go · cli-1` is now `success`; its log says `PASS cli-1: 406 passed / 10 intentionally skipped / 416 discovered; CLI inventory total=1673`. CLI shards 0, 2, 3, packages, and draft source/routing also passed. The remaining jobs were skipped under draft selection.

R1's STATE was `PR · Draft Go · cli-1` failure on `c0664c8e4`; exact failure line was `app_new_wizard_test.go:605: getwd: no such file or directory`. This failure is resolved on the exact r2 SHA and is no longer a blocking CI STATE. No rerun or workflow dispatch was initiated for this review.

The mission-listed round-2 task evidence file is absent on planning main: `git ls-tree origin/main evidence/cli-redesign-20261114/cli2-uid-app/round-2.md` returned no entry. The round-1 evidence exists at `evidence/cli-redesign-20261114/cli2-uid-app/round-1.md` and contains the owner's Option B decision, r2 diagnosis, fix description, and hosted-run handoff.

## Review findings

### app.id remains outside authored `baseharbor.yaml` — satisfied

The owner-confirmed Option B and normative contract keep the system-owned application ID out of developer-authored manifests. `TestUIDAppSliceFirstCreateThenCheckoutReuseIdentityNoAuthoredLeak` asserts both the parsed authored ID is empty and the manifest bytes do not contain the allocated ID (`cmd/baha/app_init_uid_app_slice_test.go:57-68`). `TestUIDAppSliceNoIDLeakIntoNormalMachineOutput` checks the routine CLI summary and authored manifest bytes (`:260-293`). The candidate changes tests only and does not alter the production authoring behavior.

### Stable reuse and fail-closed behavior — present in the candidate's coverage

The new real CLI cases cover first creation/repeat reuse, old canonical-store adoption, one canonical owner under concurrent creation, and no normal-output leakage (`cmd/baha/app_init_uid_app_slice_test.go:27-113,132-181,183-258,260-295`). Existing contract tests reject ambiguous, invalid, or missing registered identity and reject replacing an existing owner (`internal/application/v0425_contract_test.go:103-161`). Existing CLI retained-identity cases include conflicting owners (`cmd/baha/app_init_retained_identity_test.go:17-70`). These paths are in the passing Go package/CLI coverage on the exact run.

### Genuine CLI cells — satisfied, with one concurrency-test flaw below

The added cases call `runWithIO` for production `baha app init --quick --no-input`; setup uses canonical stores and manifests as fixtures, not an internal function in place of the command. This is genuine CLI-entry coverage for the requested app identity behavior.

### getwd/chdir leak correction — original cross-test leak addressed, concurrent CWD race remains blocking

The r2 diff adds a stable `home := t.TempDir()` plus outer `t.Cleanup` that first moves the process out of a potentially deleted race directory and then restores the original CWD (`cmd/baha/app_init_uid_app_slice_test.go:193-203`). The temp root is removed before this cleanup due LIFO cleanup ordering; moving to `home` before restoring `prev` makes the post-test CWD valid. Each racer also explicitly calls `os.Chdir(prev)` after `runWithIO` (`:220-230`). This is a real cleanup change, not merely relying on one green rerun, and it explains why the formerly failing `cli-1` shard is green on r2.

However, each goroutine still calls process-global `os.Getwd` / `os.Chdir(root)` / `os.Chdir(prev)` around its CLI run (`:218-230`). One racer can restore the original CWD while another's `runWithIO` is still resolving the repository, so concurrent commands may run from different directories. The test then counts only successful racers and fails only if there are zero (`:234-242`); it accepts arbitrary failures among the other racers and never compares each CLI outcome or identity. It can pass with one racer succeeding while others fail because the CWD changed. The test therefore remains nondeterministic and does not prove that concurrent CLI creates converge.

### Correction recipe

Set the working directory once on the test goroutine before starting racers, then restore it once from `t.Cleanup` after all racers finish; remove all per-racer `os.Chdir` calls. If each CLI invocation must use an independent CWD, run separate test processes with an explicit `Cmd.Dir` rather than changing the Go test process CWD. Strengthen assertions so each racer returns only an expected create/reuse outcome and all successful outcomes resolve to the same canonical ID; do not treat arbitrary command failures as convergence. Keep the `app.id` omission and fail-closed identity assertions intact, then obtain a new exact-head hosted run.

## Verdict

REJECT exact candidate `2bf0c929506a5b0e64b7359a6fc8711ab3f48526`. The r1 `cli-1` failure is resolved and the owner-approved Option B identity contract is preserved. The remaining blocking issue is the concurrent real-CLI test's process-global CWD race and weak success-count assertion; it can still pass despite racers executing from the wrong directory or failing. PR #1579 remains DRAFT. No PR, workflow, CI, or product source action was taken.

## repo-rule compliance

Planning repository verification before this evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

The exact candidate was read from a fresh clone; the quarantined stale-ref checkout was not used. No local tests, containers, reruns, workflow dispatch, merges, PR updates, or product edits were performed. Planning validation and the exact `origin/main` witness are recorded below.

## END DONE

Exact `origin/main` witness required before publication:

```text
90ca09118a658d9bc0ba46c0ebdfcae2cb5afb28	refs/heads/main
```
