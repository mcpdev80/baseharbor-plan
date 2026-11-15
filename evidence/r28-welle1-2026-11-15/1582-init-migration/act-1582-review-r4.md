# PR #1582 Review R4 — initializer migration

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base refs, candidate ancestry/log, metadata, and exact-head run 43680953347.
2. Review the tombstone-without-active-file `not_configured` case and source/target-removal regression.
3. Verify all four init tests and r1/r2 drift freedom for `userConfigDir`, modes, and symlink behavior.
4. Write verdict and actionable recipe with exact witnesses, validate and publish evidence on `origin/main`, then post END.

## Candidate and provenance

PR #1582 is OPEN and DRAFT, base `develop`, branch `lane-0428-fix-bf03`, exact head `312933dc497aaac92dfb55a1a50d911583f500f7`. Direct product remote witness (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
312933dc497aaac92dfb55a1a50d911583f500f7	refs/heads/lane-0428-fix-bf03
312933dc497aaac92dfb55a1a50d911583f500f7	refs/pull/1582/head
```

`gh pr view 1582 --repo mcpdev80/baseharbor --json number,state,isDraft,baseRefName,headRefName,headRefOid,url`:

```json
{"baseRefName":"develop","headRefName":"lane-0428-fix-bf03","headRefOid":"312933dc497aaac92dfb55a1a50d911583f500f7","isDraft":true,"number":1582,"state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1582"}
```

The exact fetched base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the candidate (`git merge-base --is-ancestor` succeeded). The base-to-head log lists only this BF-03 task's six commits:

```text
312933dc497aaac92dfb55a1a50d911583f500f7 test(cmd/baha): isolate package config/data root to stop leaked selection
234f8306f69d83af8d2ea2537adfbacf1f830d92 fix(BF-03): not-configured when tombstone present but canonical missing; add source+target removal regression
8730e29a76b8455c6ad3570efcb197771aaed82c fix(BF-03): durably enforce one-time migration; positive symlink + exact-mode tests
fa3190ebc968b6b2776fc6128afcc1d257df422c fix(BF-03): one-time migrate persisted selection off world-writable /tmp
c678cdd0a7385504be76d4acf927e47080e3db81 chore(BF-03): gofmt internal/orgconfig after world-writable fix
829d75bc9e710daebee62ad16710dd468db1fe13 fix(BF-03): persist target selection in private user state (not world-writable /tmp)
```

On the delta from r3 `8730e29a76b8455c6ad3570efcb197771aaed82c` to this head, only `internal/orgconfig/store.go`, `internal/orgconfig/orgconfig_test.go`, and `cmd/baha/runtime_integration_test_support_test.go` change (180 insertions, 17 deletions). `git diff --check` from `develop` to the reviewed head passed.

## Exact-head run and four init tests

`gh run view 43680953347 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName`:

```json
{"conclusion":"success","databaseId":43680953347,"event":"pull_request","headSha":"312933dc497aaac92dfb55a1a50d911583f500f7","status":"completed","workflowName":"CI · Source & Quality"}
```

The four required tests are dynamically assigned by `scripts/pr-go-unit-shard.py` using the test-name SHA-256 shard key. Each is in a different CLI shard; the respective job logs in this same run say:

```text
Job 132711241298 — PASS cli-0: 408 passed / 13 intentionally skipped / 421 discovered; CLI inventory total=1669
Job 132711241374 — PASS cli-1: 403 passed / 10 intentionally skipped / 413 discovered; CLI inventory total=1669
Job 132711241274 — PASS cli-2: 407 passed / 19 intentionally skipped / 426 discovered; CLI inventory total=1669
Job 132711241242 — PASS cli-3: 394 passed / 15 intentionally skipped / 409 discovered; CLI inventory total=1669
```

Test-to-shard mapping from the checked-in selector:

```text
TestDeterministicInitDoesNotPersistUnneededSourceSelection — cli-0
TestDeterministicInitPersistsAmbiguousSourceSelectionPositive — cli-1
TestGuidedInitInteractiveCanAcceptDetectedDefaults — cli-2
TestGuidedInitQuickDoesNotPromoteHeuristicSecrets — cli-3
```

Each named test body has no skip path. The corresponding shard passed and the selector requires every discovered, non-skipped test in that shard to pass. Thus all four named tests passed within run `43680953347`. `validate` was skipped in this `pull_request` event; these tests were instead run by the four successful `PR · Draft Go · cli-*` jobs. No workflow rerun or dispatch was initiated.

## Findings and verdict

Verdict: REJECT at `312933dc497aaac92dfb55a1a50d911583f500f7` for one missing acceptance regression.

1. The tombstone/missing-active-file behavior is fixed and asserted. `internal/orgconfig/store.go:260-270` checks the durable marker before migration and returns the normal absent result; `LoadActive` wraps it as `ErrNotConfigured`. `internal/orgconfig/orgconfig_test.go:562-595` verifies the marker exists, removes the canonical `active.json`, and asserts `errors.Is(err, ErrNotConfigured)`, excluding a decode/EOF error.
2. The requested source-and-target-removal regression is not actually present. Although `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved` and its opening comment (`internal/orgconfig/orgconfig_test.go:514-520`) claim both files are removed, the test deliberately retains `legacyPath` (`:574-581`) and only calls `os.Remove(canon)` at `:582`. No other test removes the legacy source in this missing-target regression. This retained-source case is valuable and proves the marker blocks re-adoption; it does not satisfy the separate requested source-and-target-removal case as written in the r3 review recipe and r4 mission. Recipe: keep this stronger retained-source assertion, and add a distinct case that removes both `legacyPath` and canonical `canon` while preserving the private marker, then calls `LoadActive` and asserts `errors.Is(err, ErrNotConfigured)` with no decode error. The new `internal/orgconfig` test is covered by the existing `PR · Draft Go · packages` job for `pull_request` changes to this path; no workflow edit is needed.
3. The four init tests pass in the exact candidate run, as evidenced above.
4. Drift check passes: `configRoot` still honors `BASEHARBOR_STATE_DIR` and otherwise uses `os.UserConfigDir()` (`internal/orgconfig/store.go:46-54`); the private fallback remains rooted at the user home (`:93-118`). Exact `0600` canonical-file and `0700` directory assertions remain at `internal/orgconfig/orgconfig_test.go:377-390`; the foreign-symlink regression still asserts rejection and unchanged target bytes/mode at `:429-512`. The r4 delta does not change these mode or symlink checks.

## repo-rule compliance

Read-only review in a fresh clone at the exact PR head. No product files, `.github/**` files, PR metadata, tests, containers, or VMs were changed or run. No merge or cherry-pick was performed; the frost hold remains. Evidence is stored only in the actual `baseharbor-plan` repository.

END mission-rev1582-r4.md DONE — REJECT #1582 at `312933dc497aaac92dfb55a1a50d911583f500f7`; tombstone handling and four init tests pass, but the test named source-and-target removal retains the source.

## Planning repository and validation

Before this first evidence commit, `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed: 536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors and 12 dependency warnings. `git diff --check` passes, and this evidence contains no Markdown checkbox lines.

Planning origin/main witness immediately before evidence push (`git ls-remote origin refs/heads/main`):

```text
3f68f4188aac33c9afe0b3241f33ef292bfae186	refs/heads/main
```
