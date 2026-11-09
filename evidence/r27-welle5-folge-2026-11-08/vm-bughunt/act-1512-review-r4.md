# CODEX-REVIEW 0427-175 r4 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## Exact candidate and hosted run

The live remote head is `a6afd633ce38a4cedfb74bc71d6703d3df56312b`, the same candidate reviewed in r3. The reported `6b1a4120a` is not the PR head visible from `origin` and is not reviewed here.

Raw witnesses:

```text
$ git ls-remote origin refs/pull/1512/head
a6afd633ce38a4cedfb74bc71d6703d3df56312b	refs/pull/1512/head

$ gh pr view 1512 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url
{"baseRefName":"develop","headRefName":"0427-175-initlock","headRefOid":"a6afd633ce38a4cedfb74bc71d6703d3df56312b","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1512"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-175-initlock --limit 1
completed	success	CI · PR #1512	CI · Source & Quality	0427-175-initlock	pull_request	42606542313	11m59s	2026-11-09T11:08:11Z

$ gh run view 42606542313 --repo mcpdev80/baseharbor --json databaseId,headSha,status,conclusion,url
{"conclusion":"success","databaseId":42606542313,"headSha":"a6afd633ce38a4cedfb74bc71d6703d3df56312b","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42606542313"}
```

Run `42606542313` is terminal `completed/success` on the exact live head. `PR Selected Checks`, unit/package checks, build, vet, format, docs validation and native destroy-retry Docker/Podman succeeded; unrelated native/keycloak/runtime cells were skipped, not passed.

## Review against `act-1512-review-r3.md`

The live candidate remains the r3 candidate, so all three blocking findings remain:

1. **UUID destroy path is not implemented.** `cmd/baha/app_lifecycle.go:329-348` accepts `--yes` and `--full-reset` and rejects `--uuid` as an unknown option. `cmd/baha/app_destroy_lifecycle.go:51-66` forwards only the positional name into resolution. The documented `baha app destroy --uuid <id> --full-reset` recovery command cannot execute.
2. **No production CLI twin-removal regression exists.** `TestPoisonedTargetRemainsReachableByUUID` in `cmd/baha/app_registry_poison_recovery_test.go:151-200` resolves `status --uuid`; it never calls destroy and explicitly returns success when it receives `ErrRegistryConflict` (`:185-195`). It does not prove one twin is removed while the other remains.
3. **The process concurrency assert remains loose.** `TestConcurrentInitAcrossRealProcessesIsSerializedOrRefused` at `cmd/baha/app_init_concurrent_race_test.go:141-175` discards `childErr` and does not prove the child reached the registration seam. A child that exits before attempting registration can pass based on the parent's sole record.

## Correction recipe and stop criteria

- Implement `--uuid` selection in the real destroy CLI path and carry that exact deployment identity through resolution, authorization, preflight and mutation. If the safe path cannot be implemented, remove the unsupported recovery command from the conflict guidance.
- Add a poisoned-registry CLI regression invoking `baha app destroy --uuid <selected-id> --full-reset`; assert the selected twin is removed, the other twin remains byte-identical, and the registry becomes healthy. Invalid or omitted UUIDs must fail closed. A conflict error must fail this recovery test.
- Tighten the real-process race regression: assert the child reached the registration seam, require the expected duplicate/busy refusal or explicitly verified convergence, and fail on every unrelated child exit. Preserve the incomplete/interrupted registration boundary test required by r3.
- Stop until these regressions and implementation changes land and required checks are terminal-success on the resulting exact remote HEAD. No merge or approval was performed.

## Repo-rule compliance

- Product source and GitHub were read-only; no tests, reruns, workflow dispatches, approvals, or merges were performed.
- No `.github/**` files were changed.

END_DONE 0427-175-r4-review: KORREKTUR PR #1512 live head a6afd633ce38a4cedfb74bc71d6703d3df56312b; run 42606542313 succeeded on that exact SHA, but the UUID destroy route, twin-removal CLI regression and asserted process contender outcome are still missing.
