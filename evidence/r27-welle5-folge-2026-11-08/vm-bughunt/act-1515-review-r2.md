# CODEX-REVIEW 0427-179 r2 — PR #1515

ROLLE: REVIEW

URTEIL: APPROVE

## PLAN

1. Verify the live PR head, branch-list run, exact SHA and develop ancestry.
2. Check all four r1 correction criteria against the r2 diff, tests and hosted execution.
3. Publish the exact-head verdict with raw remote witnesses.

## Exact candidate and hosted evidence

- PR #1515, branch `0427-179-flock-enforcement`, head `11b8bd447d8b9062ef6cd39a78cf2774dfa3c651`.
- Develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor; `develop...head` = `0 2`.
- Run 42633885783 is terminal `completed/success` on the exact head. `PR Selected Checks`, `go-unit-tests`, and `authority-package-tests` succeeded. The command-path regression in `cmd/baha` is included in the passing Go package suite.
- Reviewed the r2 product commit `11b8bd447` and round-2 evidence commits `23482fb4` and `54eedeb0`; round-2 evidence is `evidence/bughunt-flock-enforcement-cells/round-2.md`.

## Review against act-1515-review-r1

1. **Classifiable error across the lock boundary — PASS.** `internal/stableid/lock_unix.go` exports `ErrLockFilesystemNotEnforcing`. `coreinstallation`'s lock wrappers preserve the error, and `cmd/baha` classifies the propagated error with `errors.Is`.
2. **Immediate fail-closed in the per-app CLI lock path — PASS.** `lockApplicationTargetLifecycle` returns the not-enforcing sentinel directly before the bounded retry path. The error text retains the actionable local-filesystem remediation and says not to remove the lock file.
3. **Injected command-path regression — PASS.** `TestUnenforcingFilesystemFailsClosedWithoutRetry` injects a FREE probe through the production per-app lock route, asserts the remediation text, rejects the 15-second deadline message, and requires completion in under one second. `TestGenuineContentionStillEntersBoundedRetry` separately protects retries for actual contention.
4. **Probe, process regression and fairness — PASS.** The production cross-process probe remains active. `TestCrossProcessFlockIsEnforcedProvesMutualExclusion` still uses a second OS process. The r2 delta changes the test seam/sentinel names without weakening the contention assertion. The `#1507` destroy-priority and bounded retry logic, plus the per-app dotfile contract, remain unchanged; the new contention test exercises the preserved policy.

No blocking finding remains against the r1 recipe. This is a CODEX review verdict only; no GitHub approval or merge was performed.

## Repo-rule compliance

Product repository and GitHub were read-only. No local product tests, reruns, approval or merge were performed. The exact candidate was inspected through a fetched review ref.

Planning validation note: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed rendering but check reports three pre-existing errors in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md` (invalid decision status and two issue-inventory references). No unrelated decision was changed; this evidence is published per the explicit review instruction.

## SOP raw witnesses

```text
$ git -C baseharbor ls-remote origin refs/pull/1515/head refs/heads/0427-179-flock-enforcement refs/heads/develop
11b8bd447d8b9062ef6cd39a78cf2774dfa3c651	refs/heads/0427-179-flock-enforcement
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
11b8bd447d8b9062ef6cd39a78cf2774dfa3c651	refs/pull/1515/head

$ gh pr view 1515 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-179-flock-enforcement","headRefOid":"11b8bd447d8b9062ef6cd39a78cf2774dfa3c651","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1515"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-179-flock-enforcement --limit 8
completed	success	CI · PR #1515	CI · Source & Quality	0427-179-flock-enforcement	pull_request	42633885783	9m42s	2026-11-09T14:21:32Z

$ gh run view 42633885783 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"11b8bd447d8b9062ef6cd39a78cf2774dfa3c651","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42633885783"}
```

END_DONE 0427-179-r2-review: APPROVE PR #1515 at 11b8bd447; all four r1 criteria pass on the exact head and run 42633885783 is terminal success.
