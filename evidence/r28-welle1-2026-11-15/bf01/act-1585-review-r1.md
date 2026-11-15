# PR #1585 Review R1 — BF-01 state-dir honoring

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1585 head/base refs, ancestry and single-candidate log, metadata, prior PR #1584 closure, and exact-head run 43684179345.
2. Compare the access/init test diff with `develop` to ensure green results come from correct state-dir honoring, not weakened expectations.
3. Verify positive two-state-dir isolation, no temp-write regression per BF-03, and no duplicate registration.
4. Write verdict and actionable recipe with exact witnesses and cherry-pick SHA if approved, validate and publish evidence on `origin/main`, then post END.

## Review evidence

Requested review target: PR #1585, base `develop` at `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, head `8041a9f0119e390e03533082da05f9d62bdcc7e1`, branch `lane-0428-fix-bf01-v2`.

Planning repository identity, verified before evidence commit:
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

Exact refs observed at initial review:
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-fix-bf01-v2 refs/pull/1584/head refs/pull/1585/head`

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
8041a9f0119e390e03533082da05f9d62bdcc7e1	refs/heads/lane-0428-fix-bf01-v2
f048627c14164cb4c0a147e997e80ac92d076668	refs/pull/1584/head
8041a9f0119e390e03533082da05f9d62bdcc7e1	refs/pull/1585/head
```

Exact metadata observed at initial review:

```json
{"baseRefName":"develop","headRefName":"lane-0428-fix-bf01-v2","headRefOid":"8041a9f0119e390e03533082da05f9d62bdcc7e1","isDraft":true,"number":1585,"state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1585"}
{"baseRefName":"develop","closedAt":"2026-11-15T06:21:32Z","headRefName":"lane-0428-fix-bf01","headRefOid":"f048627c14164cb4c0a147e997e80ac92d076668","isDraft":true,"number":1584,"state":"CLOSED","url":"https://github.com/mcpdev80/baseharbor/pull/1584"}
```

Exact requested run witness:

```json
{"conclusion":"success","databaseId":43684179345,"event":"pull_request","headSha":"8041a9f0119e390e03533082da05f9d62bdcc7e1","status":"completed","workflowName":"CI · Source & Quality"}
```

The exact requested head is an ancestor of base `develop`. `git log --oneline develop..8041a9f0119e390e03533082da05f9d62bdcc7e1` listed only the three BF-01 chain commits: `8041a9f0` (organization-default registration boundary), `f048627c` (state-root target selection), and `18c922e3` (isolation regression). The predecessor PR #1584 is closed without merge. The source/test diff against develop changed no existing access/init tests: the only test-path change is the added `cmd/baha/target_selection_state_dir_isolation_test.go` (164 lines). `git diff --check` passed.

The exact-head CI jobs observed completed successfully: Go CLI shards cli-0 through cli-3, packages, and source/routing. The logs report `PASS cli-0: 408 passed / 13 intentionally skipped / 421 discovered`, `PASS cli-1: 403 passed / 10 intentionally skipped / 413 discovered`, `PASS cli-2: 408 passed / 19 intentionally skipped / 427 discovered`, and `PASS cli-3: 394 passed / 15 intentionally skipped / 409 discovered`; `internal/orgconfig` package log is `ok`. The failed run on the closed predecessor is historical and is not the exact-head run requested here.

Code review at the requested SHA found target selection rooted under `BASEHARBOR_STATE_DIR/config/active-target` through `TargetSelectionRoot`, with XDG/user config precedence only when the override is absent. Organization active state is rejected under an isolated root unless its resolution or cache reference belongs to that root. The added regression gives A and B separate roots, checks A's persisted selection is absent in B, checks B fails closed without naming A's target, then activates B and confirms A remains selected when returning to A. No existing expectations were weakened. The production diff adds no temporary-directory fallback/write path and does not introduce a second target-registration source; the registration check reads the existing `deployment.Config.Targets` map. Temporary directories are used only by the test fixture.

## State change during review

Before this evidence was finalized, a fresh remote read showed the exact PR branch had advanced beyond the mission target. Latest witnesses:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01-v2
f048627c14164cb4c0a147e997e80ac92d076668	refs/pull/1584/head
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/pull/1585/head
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/pull/1586/head
```

Current PR #1585 metadata is `{"baseRefName":"develop","headRefName":"lane-0428-fix-bf01-v2","headRefOid":"7bdeaa08499f4b3d8113d537a48e36d4f9881bf0","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1585"}`. Run `43685670514` is for that new head and is currently `in_progress`; no workflow was triggered by this review. Since the task contract pins the reviewed SHA to `8041a9f...`, this is a scope change. I am withholding APPROVE/REJECT and requesting direction on whether to review the new exact head `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0` after its run becomes terminal.

No product files, PR state, or workflow files were modified. No tests were run locally.

## repo-rule compliance

Read-only CODEX-REVIEW. Fresh product clone under `/tmp/opencode/w1585-pr1585-review-r1-wt`; no product writes. No workflow edits, reruns, or dispatches. Evidence is in the planning repository only. Existing unrelated modification `evidence/r28-welle1-2026-11-15/bf01/round-1.md` was preserved.

## Verdict

QUESTION: target PR moved from the mission-pinned SHA while this review was in progress. No verdict is issued against the stale SHA and no cherry-pick receipt is provided pending confirmation of the new target.

END BLOCKED

Planning validation: `python3 scripts/plan.py check` completed with `536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors, 12 warnings`. Warnings are the existing accepted/dependency and active/dependency notices printed by the validator.

Publication preflight, exact `git ls-remote origin refs/heads/main` output:

```text
0d117bd3fec101300c674437c9fcaf108ab5e2be	refs/heads/main
```

The planning repository root was verified above. This review did not create a branch, so no branch-cut base attestation applies.
