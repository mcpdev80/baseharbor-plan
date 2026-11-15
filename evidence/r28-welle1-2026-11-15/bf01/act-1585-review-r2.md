# PR #1585 Review R2 — BF-01 state-dir and private organization store

ROLE: CODEX-REVIEW (no merge; frost).

## PLAN

1. Verify current PR #1585 refs, base develop, exact head e7501204caf27ece99636152220d389ad86374d4, exact-head run 43689640514, and candidate ancestry/log.
2. Inspect the BF-01 isolation regression and prove it fails on exact develop and passes on the exact branch, with both SHAs and command outputs; confirm it traverses the registration guard without an early-exit shortcut.
3. Review combined internal/orgconfig/store.go semantics from BF-01 and #1582, including world-writable guard and private fallback; run the requested throwaway vet and record its witness.
4. Read access/init test diffs and verify expectations remain intact and no second target truth source was introduced.
5. Write SHA-exact verdict and actionable recipe, run planning validation, publish evidence to origin/main, update the board, and post END.

## Review scope and provenance

The planning repository root was verified before the evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

The required pre-push remote-main witness was run with `git ls-remote origin refs/heads/main`; exact output:

```text
829867ec9ea6f556d56e705d6e329abbaa94a2a1	refs/heads/main
```

The product candidate was reviewed read-only at `e7501204caf27ece99636152220d389ad86374d4`. The exact remote witnesses were:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
e7501204caf27ece99636152220d389ad86374d4	refs/heads/lane-0428-fix-bf01-v2
e7501204caf27ece99636152220d389ad86374d4	refs/pull/1585/head
```

PR #1585 is open, draft, based on `develop`, and its head OID is `e7501204caf27ece99636152220d389ad86374d4`. The exact-head GitHub Actions run is `43689640514`, event `pull_request`, workflow `CI · Source & Quality`, terminal status `completed`, conclusion `success`, head SHA `e7501204caf27ece99636152220d389ad86374d4`.

Candidate ancestry and own-commit log:

```text
git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c e7501204caf27ece99636152220d389ad86374d4 => exit 0
git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..e7501204caf27ece99636152220d389ad86374d4
e7501204 fix(cli): state-root-owned target selection chain (BF-01, red-tightened)
7bdeaa08 test(cli): mirror real organization-state placement in the BF-01 regression
8041a9f0 fix(cli): keep foreign organization defaults out of isolated state roots
f048627c fix(cli): state-root override owns target selection state
18c922e3 test(cli): add BF-01 state-dir target-selection isolation regression
```

The log contains only the five PR #1585 commits above. No PR #1582 head is in this candidate ancestry. The remote `refs/pull/1582/head` remains `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`.

## CI witnesses

Run `43689640514` completed successfully on the exact candidate. Its CLI shard jobs reported:

```text
PR · Draft Go · cli-0: success; PASS cli-0: 408 passed / 13 intentionally skipped / 421 discovered; CLI inventory total=1670
PR · Draft Go · cli-1: success; 403 passed / 10 intentionally skipped / 413 discovered
PR · Draft Go · cli-2: success; 408 passed / 19 intentionally skipped / 427 discovered
PR · Draft Go · cli-3: success; 394 passed / 15 intentionally skipped / 409 discovered
```

Source/routing and packages jobs also succeeded. Docker, Podman, validate and other PR-policy-inapplicable gates were skipped; they are not claimed as passing. The CI summary does not expose a test-name-specific result for the BF-01 regression, so this run is not proof of the requested exact-test red/green pair.

## Findings

### F1 — #1582 private-store guard is absent from the combined candidate

At the reviewed SHA, `internal/orgconfig/store.go:18-30` selects config roots from `BASEHARBOR_STATE_DIR`, XDG or home, and `internal/orgconfig/store.go:191-221` writes the active state. The file has no definitions or references for `worldWritableCheckOptOutEnv`, `privateFallbackPath`, or `isWorldWritableCandidate`; repository search in `internal/orgconfig` found no matches. The required #1582 world-writable check and private fallback semantics are therefore not combined with BF-01 state-root isolation.

The required throwaway combined-vet check was run with the current #1582 `internal/orgconfig/orgconfig_test.go` overlaid onto an isolated scratch worktree at the reviewed BF-01 SHA. Command:

```text
TMPDIR=<isolated tmp> GOTMPDIR=<isolated tmp> GOCACHE=<isolated cache> go vet -p 1 ./internal/orgconfig
```

Observed failure:

```text
vet: internal/orgconfig/orgconfig_test.go:69:11: undefined: worldWritableCheckOptOutEnv
```

This overlay was confined to `/tmp/opencode`; neither the candidate nor a product checkout was modified. **Blocking.** Recipe: combine the #1582 world-writable guard, opt-out variable and private fallback path with BF-01’s isolated root selection in the single organization store; preserve explicit `BASEHARBOR_STATE_DIR` ownership and add/run the #1582 regression tests. Then rerun `go vet ./internal/orgconfig` and the relevant CLI package CI on the resulting candidate SHA. Do not add a second store or change workflow files.

### F2 — BF-01 target resolver introduces a second, environment-blind source of truth

`internal/orgconfig/store.go:164-183` implements `OrganizationTargetSelection`, preferring the organization default and otherwise selecting the first target after sorting all environment names. It has no environment argument. `cmd/baha/target_state_layout.go:56-60` uses that helper for the isolated-root organization selection. The existing canonical resolver `internal/orgconfig/effective.go:43-79` selects the active environment (default `dev`) and applies that environment’s target, while `cmd/baha/target.go:179-192` resolves the active repository/context environment. Thus an isolated root with distinct `dev` and `prod` targets can select the lexicographically first environment’s target instead of the active environment’s effective target. This is a second target-selection truth source and can select the wrong deployment.

**Blocking.** Recipe: route the state-root-owned organization selection through the canonical effective resolver with `organizationEnvironment(ctx)` and preserve state-root provenance/ownership checks. Add a regression with distinct targets in two environments and assert the active environment wins; include it in the existing CLI package test discovery and its GitHub CI group. Do not edit `.github/**`; if CI selection does not cover the test, report the required workflow change separately to the Owner.

### F3 — Required fail-first red/green evidence is not established

The test body in `cmd/baha/target_selection_state_dir_isolation_test.go` now models root-local organization state: its later case writes the B root-local default `beta` and expects it to resolve. On source inspection, develop’s legacy selection path can return the multiple-target conflict before consulting this organization default, while the candidate’s isolated-root branch consults it. This is a plausible red-on-develop path, not an observed test result.

Three local attempts could not execute the test because this host hit a disk quota at link time. The final observed error was `link: mapping output file failed: disk quota exceeded`; earlier compilation also emitted `disk quota exceeded`. The command chain stopped on that error, so the develop-side test was not run and no local green output exists. The successful exact-head CLI shard summary above does not identify this test by name. Therefore the contract’s required exact-SHA fail-first output pair is absent. **Blocking evidence gap.** Recipe: on a runner with sufficient disk, run the exact test against `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` with the regression file applied as a test-only overlay and against `e7501204caf27ece99636152220d389ad86374d4`; record both command output and verify the base failure is specifically the root-local organization-default assertion. A future new regression must remain discovered by the relevant GitHub CI package/shard.

## Access/init test review and source inventory

The candidate changes only one test file: `cmd/baha/target_selection_state_dir_isolation_test.go`. No existing access/init test file is changed, removed, skipped, or weakened in the PR diff. The new test adds state-root isolation cases and preserves positive expectations for root-local selection. The candidate also changes `cmd/baha/target.go`, `cmd/baha/target_selection.go`, `cmd/baha/target_state_layout.go`, `internal/deployment/target.go`, and `internal/orgconfig/store.go`; there is no second organization store file. F2 is a duplicate selection algorithm within the same store/resolver architecture, rather than a second persisted store.

## Validation and repository-rule compliance

Planning validation on the isolated planning worktree:

```text
python3 scripts/plan.py check
536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors, 12 warnings
```

The 12 warnings concern pre-existing accepted/active cards with dependencies not accepted; this evidence-only update did not edit task metadata. No product code, product test, `.github/**` workflow, runner, VM or compose project was modified or started. No PR comment, rerun, dispatch, merge, bypass or cherry-pick was performed. The product review worktrees and throwaway vet overlay are under `/tmp/opencode`.

The mission named `bf01` rounds 1–4. On the fetched planning `origin/main`, `evidence/r28-welle1-2026-11-15/bf01/` contains `round-1.md`, `round-2.md`, and `round-3.md`; no `round-4.md` exists at that remote path. The prior round-2 finding about missing #1582 symbols is reproduced at the current candidate SHA by F1 above.

## Verdict

**REJECT** `e7501204caf27ece99636152220d389ad86374d4`.

Blocking reasons: F1, the required #1582 private-store/world-writable semantics are missing and combined vet fails; F2, isolated-root selection bypasses the active-environment resolver; F3, exact-SHA fail-first evidence remains unproven because the local link hit disk quota and the successful CI summary is not test-name-specific. There is no cherry-pick SHA line because the candidate is not approved.

## END DONE

END_DONE mission-rev1585-r2.md: REJECT — combined private-store guard missing, environment selection duplicated, fail-first pair unproven; candidate e7501204caf27ece99636152220d389ad86374d4
