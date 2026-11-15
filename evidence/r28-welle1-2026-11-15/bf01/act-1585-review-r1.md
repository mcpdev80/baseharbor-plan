# PR #1585 Review R1 — BF-01 state-dir isolation

ROLE: CODEX-REVIEW. No merge; frost remains in force.

## PLAN

1. Verify the current PR #1585 head and base, refs, ancestry, candidate commit list, and exact-head CI run.
2. Compare access/init test changes and CI results; confirm no expectations were weakened.
3. Review the current two-root isolation test and production state-root, temporary-write, and target-registration paths.
4. Record the verdict and correction recipe, validate and publish this evidence, then post END.

## Review target and remote witnesses

The owner corrected the dispatch pin. I reviewed the current exact candidate `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0` against `develop` at `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.

Planning repository identity, verified before evidence publication:

```text
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Fresh product refs:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01-v2
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/pull/1585/head
```

Current PR metadata:

```json
{"baseRefName":"develop","headRefName":"lane-0428-fix-bf01-v2","headRefOid":"7bdeaa08499f4b3d8113d537a48e36d4f9881bf0","isDraft":true,"state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1585"}
```

PR #1584 is closed without merge at `f048627c14164cb4c0a147e997e80ac92d076668`; duplicate PR #1586 is closed at the reviewed `7bdeaa0` head. The two live branch names both resolve to the same current candidate. `develop` is an ancestor of the reviewed head. The complete log above base contains only this BF-01 chain:

```text
7bdeaa084 test(cli): mirror real organization-state placement in the BF-01 regression
8041a9f01 fix(cli): keep foreign organization defaults out of isolated state roots
f048627c1 fix(cli): state-root override owns target selection state
18c922e37 test(cli): add BF-01 state-dir target-selection isolation regression
```

## CI evidence

Exact run witness:

```json
{"conclusion":"success","databaseId":43685670514,"event":"pull_request","headSha":"7bdeaa08499f4b3d8113d537a48e36d4f9881bf0","status":"completed","workflowName":"CI · Source & Quality"}
```

Run `43685670514` completed successfully on the exact reviewed head. The `pull_request` trigger executed `PR · Draft Go · cli-0` through `cli-3` and `PR · Draft Go · packages`; all five jobs completed successfully. The shard logs report cli-0 `408 passed / 13 skipped / 421 discovered`, cli-1 `403 / 10 / 413`, cli-2 `408 / 19 / 427`, and cli-3 `394 / 15 / 409`; `internal/orgconfig` reports `ok`. Source and routing job `132725534769` also succeeded. The new test is in `cmd/baha`, covered by the CLI package shards on PR pushes. No workflow file was changed or rerun by this review.

## Review findings

No existing `TestAccessAssign*`, `TestAccessOffboard*`, or `TestGuidedInit*` test was changed. The only test-path delta against develop is the added `cmd/baha/target_selection_state_dir_isolation_test.go`; its 7bde amendment changes only that new fixture/assertion. The access/init green result is therefore not caused by weakened expectations.

The production diff keeps target selection under `BASEHARBOR_STATE_DIR/config/active-target`, filters active organization state whose source/cache is outside the selected root, and checks organization-default targets against the existing `deployment.Config.Targets` registry. It adds no second target-registration store and no production temporary-directory fallback/write. `t.TempDir()` is confined to test fixtures. No BF-03 temporary-persistence behavior was changed. `git diff --check` passed.

The new test does positively assert that A's persisted selection is absent from B and that switching B to `beta` leaves A's `alpha` selection intact. However, its central resolver assertion does not exercise the organization-default path or the new registration-boundary guard. At lines 57 and 84, B has two registered targets (`beta`, `gamma`), no persisted B selection, and no configured default. `effectiveTarget` calls `selectedTargetName` first; `cmd/baha/target_selection.go:92-97` returns “multiple deployment targets configured” before `cmd/baha/target.go:98` can call `resolveTargetWithOrganization`. The test at `target_selection_state_dir_isolation_test.go:84-90` accepts any error that omits `alpha`, so that unrelated ambiguity error satisfies it.

I ran the exact new test file against both the candidate and `develop` code. Both passed:

```text
Candidate 7bdeaa084, with its test file:
ok   github.com/mcpdev80/baseharbor/cmd/baha  0.026s

develop 0e9ccb582, with the same 7bdeaa084 test file:
ok   github.com/mcpdev80/baseharbor/cmd/baha  0.021s
```

The first local attempt did not reach test execution because inherited Go temp/cache paths were read-only. Re-running with `TMPDIR`, `GOTMPDIR`, and `GOCACHE` under `/tmp/opencode` produced the two results above. CI independently ran the same package on the candidate.

Thus the reported round-3 “red on base” claim is not reproduced: the current test passes unchanged against base. More importantly, the test does not distinguish the candidate's new guard from the pre-existing multiple-target selection error. This leaves the changed behavior without a discriminating regression assertion.

## Actionable correction

Keep the two-root persisted-selection assertions, but separately exercise the organization resolver without an earlier ambiguous-selection return. A focused same-package test can call `resolveTargetWithOrganization` with no explicit or user selection, a root-local organization default of `local`, and B registrations that omit `local`. Candidate code should reject that organization default at the state-root registration boundary; the base resolver would otherwise accept the built-in `local` fallback. Assert the specific boundary error (and the root-local valid-target case) so the test fails on base for the intended reason. Keep the test in `cmd/baha`; the existing `PR · Draft Go · cli-*` jobs selected by the `pull_request` trigger already cover it. Then update the exact-head CI receipt.

## repo-rule compliance

Read-only CODEX-REVIEW. Product source was not modified; the candidate and base test runs used separate worktrees under `/tmp/opencode`. No PR, workflow, or develop state was changed. Evidence is in the actual `baseharbor-plan` repository. No branch was created by this review, so a branch-cut attestation does not apply. No containers were started.

## Verdict

**REJECT** candidate `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0` for the non-discriminating BF-01 regression test described above. The code change is narrowly scoped and CI is green, but the added assertion passes on base and exits through the pre-existing ambiguity error before testing the new organization-default guard. Recipe: bypass that early selection error in a focused resolver test, assert the new registration-boundary result, and prove the test fails on base and passes on the candidate. No cherry-pick SHA is provided.

Planning validation is recorded after running `python3 scripts/plan.py check`; its result is `536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors, 12 warnings`.

END_DONE: Review complete, verdict REJECT on exact candidate `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0`; PR #1585 remains draft and unmerged.

Pre-push `git ls-remote origin refs/heads/main` output:

```text
8153a1de1f21a2d856fa0c67707f81380cbd73a9	refs/heads/main
```
