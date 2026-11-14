# PR #1575 Review R3

## PLAN

1. Verify exact PR #1575 r3 candidate/base, ancestry, own-commit log, and specified hosted run.
2. Recheck the three r2 blocking regression cells and configured-versus-unverified status semantics; assess PR #1577 documentation consistency.
3. Check for documentation regressions and record SHA-specific verdict in planning evidence.
4. Validate and publish evidence to planning origin/main, verify remote presence, and post END.

## Review scope and provenance

Role: CODEX-REVIEW, correction round r3. No product files were modified and no merge, rerun, workflow dispatch, or container action was performed.

Planning repository verification before evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Product remote witness from a fresh clone at `/tmp/opencode/mission-rev1575-r3`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/pull/1575/head
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

PR #1575 is OPEN and DRAFT, base `develop`, candidate `c195a9a2049253accdf57a082e6eb33fc36ec7dd`. The fetched base head is `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`; `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c c195a9a2049253accdf57a082e6eb33fc36ec7dd` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..c195a9a2049253accdf57a082e6eb33fc36ec7dd` lists only this chain's commits:

```text
c195a9a test: exercise Perses status through the public CLI
dc670bfd fix: report selected Perses as configured but unverified
61f76fa feat: add fail-closed Perses management surface
```

The r3-only diff `dc670bfd..c195a9a` changes only `cmd/baha/app_perses_cli_test.go` (+345/-75). The complete candidate diff against `develop` is 14 files, 842 additions, 9 deletions; no `.github/**`, environment/target, or unrelated paths. `git diff --check` passed.

## Hosted run

Run `43647090290` completed with conclusion `success`, event `pull_request`, workflow `CI · Source & Quality`, and exact head SHA `c195a9a2049253accdf57a082e6eb33fc36ec7dd`. The four CLI shard log witnesses were:

```text
PASS cli-0: 411 passed / 13 intentionally skipped / 424 discovered; CLI inventory total=1675
PASS cli-1: 405 passed / 10 intentionally skipped / 415 discovered; CLI inventory total=1675
PASS cli-2: 407 passed / 19 intentionally skipped / 426 discovered; CLI inventory total=1675
PASS cli-3: 395 passed / 15 intentionally skipped / 410 discovered; CLI inventory total=1675
```

The candidate is draft, so draft-source and CLI/package checks ran successfully; remaining PR Selected Checks were skipped by draft selection. No failing check was observed. No rerun was triggered.

## Review findings

The three r2 CLI-test corrections are materially present. The revised tests invoke `baha status --json` and `baha app status --json` through `runWithIO`, decode the actual command output, and exercise the selected Perses configuration path. The previously inert unknown-owner coverage now exercises repository status, UUID status, and `show` command paths. The tests are picked up by the hosted `Draft Go` CLI shards in the pull-request event, as evidenced by the run above.

Blocking finding: status still does not satisfy the contract that configured declaration is distinct from runtime reachability explicitly reported as unverified. In `internal/capability/perses.go:126-168`, the surface records selected-and-pinned declaration as `Provisioned`, while reachability remains unverified. `internal/application/management_ui.go:401-412` builds the public status surface without exposing either field. `internal/metrics/management_ui.go:55-61,89-100` validates compiled release configuration and returns success without a runtime reachability observation. `cmd/baha/app_status_collect.go:357-367,450-472` consequently records a nil verifier result as a successful ready check, with a detail claiming the Prometheus management UI is reachable. `internal/application/status_result.go:29-36` maps that success to `ready` and `OK=true`. A declared pin can therefore be surfaced as reachable/ready without a runtime observation.

The added helper `assertPersesSurfaceUnverified` in `cmd/baha/app_perses_cli_test.go:85-103` only rejects ready/verified states among matching checks; it does not require a matching management-UI check or assert an explicit unverified observation with `OK=false`. The fixture does not start a workload, and the status collection may return early as stopped when no components are running (`cmd/baha/app_observe.go:57-61,577-585`; `cmd/baha/app_status_collect.go:122-148`). Thus an empty matching-check set passes vacuously and does not verify the runtime path that currently records readiness.

Required correction recipe: preserve the configured declaration independently; emit an explicit non-ready `unverified` reachability observation for Perses instead of a successful reachable check absent a runtime probe; add a public-CLI regression that reaches managed-service collection with a running/fake application and unavailable Perses health; assert exactly one management-UI observation, its unverified state and `OK=false`, and the intended aggregate non-ready result. Ensure that test remains selected in the existing CLI CI shards.

Cross-PR effect on #1577: WAITING. Its current release prose says a selected but unprovisioned Perses surface is unsupported, “never as configured,” and says no release reports Perses as provisioned when it is not provisioned. Those claims remain inconsistent with #1575's declaration-based `Provisioned` field. The #1577 wording must distinguish selected-and-pinned configuration from actual provisioning and runtime reachability; it should say authentication remains unsupported and runtime reachability remains unverified until actually observed. Keep #1577 draft pending that clarification and the #1575 correction. R3 changed no documentation, so it introduces no new documentation regression, but it does not resolve the existing cross-PR discrepancy.

## Verdict

REJECT candidate `c195a9a2049253accdf57a082e6eb33fc36ec7dd` for the blocking status-semantics and vacuous-regression-test finding above. R3 fixes the prior test-path gaps, but leaves the underlying false-ready behavior and does not prove an explicit unverified runtime status.

## repo-rule compliance

Evidence is in the actual planning repository, not the workers bookkeeping checkout. Product remote state was measured from a fresh clone and `git ls-remote`; the quarantined stale-ref checkout was not used. No workflow files were edited, no hosted run was triggered, no containers were started, and no product repository was modified. Planning validation: `python3 scripts/plan.py check` reported 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors and 10 existing dependency warnings.

Planning origin/main witness before evidence commit:

```text
9333e7815666c1b3ba738743adcf3ebb6a5f8ddc	refs/heads/main
```

## END DONE
