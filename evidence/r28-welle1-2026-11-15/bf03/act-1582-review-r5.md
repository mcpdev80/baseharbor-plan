# PR #1582 Review R5 — BF-03 source-and-target removal

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base refs, candidate ancestry/log, metadata, and exact-head run 43683234849.
2. Inspect diff `312933dc..756b2be7` and confirm it contains only the required source-and-target-removal regression.
3. Check that the test preserves the tombstone and asserts not-configured without re-adoption, and that the full-suite run is green.
4. Write APPROVE or REJECT with exact witnesses and cherry-pick SHA if approved, validate and publish evidence on `origin/main`, then post END.

## Candidate, ancestry, and exact delta

PR #1582 is OPEN and DRAFT, base `develop`, branch `lane-0428-fix-bf03`, exact head `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`. Direct product remote witness (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
756b2be7eb2ee2e0671de6cf2e7862395e3881fc	refs/heads/lane-0428-fix-bf03
756b2be7eb2ee2e0671de6cf2e7862395e3881fc	refs/pull/1582/head
```

`gh pr view 1582 --repo mcpdev80/baseharbor --json number,state,isDraft,baseRefName,headRefName,headRefOid,url`:

```json
{"baseRefName":"develop","headRefName":"lane-0428-fix-bf03","headRefOid":"756b2be7eb2ee2e0671de6cf2e7862395e3881fc","isDraft":true,"number":1582,"state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1582"}
```

The exact fetched base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). The log since r4 contains only the requested test commit:

```text
756b2be7eb2ee2e0671de6cf2e7862395e3881fc test(orgconfig): add source-and-target-both-removed migration regression (R4)
```

`git diff --stat 312933dc497aaac92dfb55a1a50d911583f500f7..756b2be7eb2ee2e0671de6cf2e7862395e3881fc` reports only `internal/orgconfig/orgconfig_test.go`, 81 insertions. No other file or prior r1/r2/r3/r4 content drifted. `git diff --check` passed.

## Regression review

`internal/orgconfig/orgconfig_test.go:598-677` adds `TestWorldWritableMigrationFrozenWhenSourceAndTargetBothRemoved`. It seeds and adopts the legacy selection, verifies the private `active.frozen.tombstone` exists, removes both canonical `active.json` and the legacy source, and asserts `LoadActive` returns `ErrNotConfigured` (therefore no successful re-adoption and no decode/EOF error). This is the distinct both-removed case requested in r4. The retained-source companion test remains in place and proves that the marker prevents re-adoption even when a legacy source still exists. Together, the tests cover both the exact deleted-source/deleted-target state and the marker's blocking behavior.

## Exact-head CI run

`gh run view 43683234849 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName`:

```json
{"conclusion":"success","databaseId":43683234849,"event":"pull_request","headSha":"756b2be7eb2ee2e0671de6cf2e7862395e3881fc","status":"completed","workflowName":"CI · Source & Quality"}
```

The full Go test coverage in this run was green: all four `PR · Draft Go · cli-*` shard jobs and `PR · Draft Go · packages` succeeded. Their exact shard outputs were:

```text
2026-11-15T06:00:50.7591410Z PASS cli-0: 408 passed / 13 intentionally skipped / 421 discovered; CLI inventory total=1669
2026-11-15T05:58:52.5814222Z PASS cli-1: 403 passed / 10 intentionally skipped / 413 discovered; CLI inventory total=1669
2026-11-15T06:01:49.4658117Z PASS cli-2: 407 passed / 19 intentionally skipped / 426 discovered; CLI inventory total=1669
2026-11-15T05:59:53.9278594Z PASS cli-3: 394 passed / 15 intentionally skipped / 409 discovered; CLI inventory total=1669
2026-11-15T05:59:27.4198055Z ok   github.com/mcpdev80/baseharbor/internal/orgconfig 0.099s
```

The new `internal/orgconfig` test ran under the `PR · Draft Go · packages` job on the `pull_request` trigger. The `validate` and PR Selected Checks jobs were skipped for this Draft PR event; no failing check was observed. No workflow rerun or dispatch was initiated. No local tests were run for this read-only review.

## Verdict and handoff

Verdict: APPROVE at `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`. The r4 finding is resolved by exactly one new test, its package ran green on the exact head, and the requested delta contains no unrelated changes.

Cherry-pick SHA for the merge queue: `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`.

## repo-rule compliance

Read-only review in a fresh clone at the exact PR head. No product files, `.github/**` files, PR metadata, tests, containers, or VMs were changed or run. No merge or cherry-pick was performed; the frost hold remains. Evidence is stored only in the actual `baseharbor-plan` repository.

END mission-rev1582-r5.md DONE — APPROVE #1582 at `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`; the distinct both-removed regression is present and the package/full Go shard jobs passed on the exact head.

## Planning repository and validation

Before this evidence commit, `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed: 536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors and 12 dependency warnings. `git diff --check` passed. This evidence contains no Markdown checkbox lines.

Planning origin/main witness immediately before evidence push (`git ls-remote origin refs/heads/main`):

```text
32311418d224c5eeec65a7ce949b2f311885451a	refs/heads/main
```
