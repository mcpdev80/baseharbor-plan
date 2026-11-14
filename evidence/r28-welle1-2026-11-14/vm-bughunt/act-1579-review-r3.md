# PR #1579 Review R3

## ROLE
CODEX-REVIEW. No merge. Same lane as r2/r1 (`lane-0428-uid-app`, PR #1579).

## Candidate and provenance

Fresh witness via `git ls-remote origin`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop  (base)
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/pull/1579/head
```

`git merge-base --is-ancestor 0e9ccb582 18b0ebc9d` succeeds; merge-base is `0e9ccb582`.
Only three lane commits between base and head:

```text
18b0ebc9d cmd/baha: fix concurrent uid-app test CWD race + strengthen convergence assert
2bf0c9295 cmd/baha: fix CWD state leak in concurrent uid-app test
c0664c8e4 cmd/baha: bounded uid-app identity-stability regression slice (0428-050)
```

PR #1579 is OPEN and DRAFT, base `develop`, branch `lane-0428-uid-app`. Exactly one file changed vs base: `cmd/baha/app_init_uid_app_slice_test.go`. No product source, no `.github/**`.

## r3 findings (from R2 verdict)

### Finding 1 — concurrent CLI CWD race (process-global `os.Chdir`) — RESOLVED
Before (r2 SHA `2bf0c9295`): each goroutine called `os.Getwd()` / `os.Chdir(root)` / `os.Chdir(prev)` around its `runWithIO`, so one racer restored the original CWD while another's `runWithIO` was still resolving the repository. Concurrent commands ran from different directories; a racer could resolve from a wrong or deleted path.

After (r3 SHA `18b0ebc9d`): working directory is set **once** with `os.Chdir(root)` before the racers start, and restored **once** from the existing `t.Cleanup` after all racers finish. All per-racer `os.Chdir` calls removed. The CWD is now process-global-consistent across the whole concurrent run. Verified: `go test ./cmd/baha/ -run TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner -count=5 -race` → clean; combined run with the four formerly-failing tests → clean.

### Finding 2 — convergence assertion too weak — RESOLVED
Before: the test counted only successes (`successes == 0`) and never compared each CLI outcome or the resolved identity. It could pass with one racer succeeding while others failed because the CWD changed — arbitrary command failures were treated as convergence.

After: each racer now returns only a valid create-or-reuse outcome and the canonical ID it resolved via `canonicalOwnerID`. All successful racers must resolve the **same** canonical ID (`oc.uid != converged` → `t.Fatalf`), and the surviving canonical store ID must equal the CLI-resolved ID. Arbitrary failures are no longer treated as convergence. The `app.id`-omission and fail-closed identity assertions are intact.

## Exact hosted run

Run `43654843802` → terminal `completed/success`, event `pull_request`, workflow `CI · Source & Quality`, exact head `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`.

Job results: `cli-0` pass, `cli-1` pass, `cli-3` pass, `packages` pass, `draft source and routing` pass. No `FAIL`/`UNSTABLE` in the run; other jobs `skip` under draft selection. This is the exact r3 head.

## Verdict

**ACCEPT** exact candidate `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`. The r1 `cli-1` getwd leak is resolved (r2), the concurrent CWD race is removed and the convergence assertion is now identity-precise (r3). Owner Option B (system-owned `app.id` out of authored `baseharbor.yaml`) and the stable/fail-closed identity contract are preserved. The remaining two r2 findings — the concurrent process-global CWD race and the weak success-count assertion — are both fixed, and the exact-head hosted run `43654843802` is terminal green.

Merge authority (CODEX-MERGE) remains available only to a separate merge session; the review lane performs no merge, no PR/CI/workflow action, no product edit, and no release/tag. PR #1579 stays DRAFT.

## END DONE

Exact `origin/main` witness required before publication (recorded by the publishing session):

```text
refs/heads/main
```
