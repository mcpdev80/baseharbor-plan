# 0428-223 / t-20261121-develop-full-suite-red — diagnose-1: the 14 validate reds at PR #1754 head

Read-only diagnosis dispatch. No product change, no branch push in this dispatch ("kein push erfolgt").

## Remote/zone witnesses (measured)

- Real URL resolution (first git action): `git -C /home/marcel/dev/baseharbor-ecosystem/workers/0428-223-testctx-wt remote -v`
  → `origin https://github.com/mcpdev80/baseharbor.git (fetch)` — every fetch/ls-remote below used the explicit real URL.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-061-sourcepull refs/pull/1752/head refs/pull/1750/head`
  (measured 2026-11-22 04:32Z): develop `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`,
  lane-0428-061-sourcepull = refs/pull/1752/head = `0045bdcc743854164f54adecf0cb2c17e3e49c8d`,
  refs/pull/1750/head `f16cef27f4d`.
- `git ls-remote ... refs/heads/lane-0428-223-testcontext-target` → `f16cef27f4d` (unchanged since the hop).
- Planning repo verification (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — correct zone.

## STOP-report: what I did on lane-0428-061-sourcepull (per halt instruction)

Sequence, in order, with evidence:

1. Mission file `hop1752c.md` (sha256 `d95685e324510950635873c24bb3f79d3aba045a442281a33583f391ab91e31f`) ordered the #1752 hop before your halt. I ran the ls-remote comparison (head `7b3c658800a`, back=5) and created a local additive merge commit
   `ebd063864f6746a82a043698d02116566988144f` ("hop(0428-061): merge develop 8b9a8f50645 into lane-0428-061-sourcepull …", `--no-ff` of 7b3c6588+8b9a8f50, no conflicts, no .github/** or scripts/** edits by me — the diff stat shows only develop's own content arriving via the merge).
2. Push attempt: `git push https://github.com/mcpdev80/baseharbor.git HEAD:refs/heads/lane-0428-061-sourcepull` → **rejected (non-fast-forward)** — "Updates were rejected because the tip of yours is behind … counterpart. If you want to integrate the remote changes, use 'git pull'". The remote had moved to `0045bdcc` (the other session's merge of develop) during my earlier fetch-error. **No push ever landed from me.**
   Second attempt also died with `fetch/push error` (transport failure), again with no remote effect.
3. On your HALT I stopped immediately: no re-merge, no rebase, no force, no pull. Remote truth re-verified at 04:32Z: `refs/pull/1752/head = 0045bdcc743854164f54adecf0cb2c17e3e49c8d` — the other session's head is intact; no second head was ever created. My `ebd06386` exists only in this machine's object store inside a temporary worktree zone, which I then deleted (`/tmp/opencode/0428-223-hopzone`, removed; `git worktree prune` run).
4. Answer to "commit-sha + push ja/nein": local merge commit `ebd06386`, **push: NEIN** (both attempts rejected; delivery witness = unchanged remote `0045bdcc` before/after).

The exact PR run at `0045bdcc` (44979724623) was observed to terminal by me before the halt: `completed failure`; the red is `PR · Draft Go · cli-3` (job `137077374467` at the new head) — same zsh cause as the openstelle at the old head.

## The candidate under diagnosis

- Head `033365459e2` = PR #1754 (karte 0428-229, ci-only): commits `acd8dd95…033365459e2` touch ONLY `.github/workflows/ci.yml` (API compare/commits). GitHub compare `8b9a8f50645...033365459e2` → `status=ahead ahead=5 behind=0`, so the tree contains develop `8b9a8f50645` plus CI-workflow changes only.
- validate job `137076156327` log: 124,785 bytes (measured via `gh api /repos/mcpdev80/baseharbor/actions/jobs/137076156327/logs`).
- Develop comparison runs (both `completed failure`, head `22fc68ebc06`): 44918870333 workflow_dispatch (validate job `136890321112`, log re-fetched, 124,243 bytes) and 44916333992 schedule (validate job `136882633155`).

## What the log actually shows

Exactly 14 parent `--- FAIL:` names. The "No migration path exists – existing projects cannot be upgraded" lines are NOT test failures: they are the Material for MkDocs 2.0 advertising warning banner printed in the docs build step (`https://squidfunk.github.io/mkdocs-material/blog/2026-02-18/mkdocs-2.0/` in the same block, `##[endgroup]` context) — present in the develop logs too, unrelated to the 14.

## Classification per test group (file:line)

### Group A — init/wizard source-selection tests (7 names)
TestDeterministicInitDoesNotPersistUnneededSourceSelection, TestDeterministicInitPersistsAmbiguousSourceSelectionPositive, TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds, TestGuidedInitDeterministicPositionalEnvironmentAliases, TestGuidedInitExplicitFlagsKeepDeterministicPath, TestGuidedInitInteractiveCanAcceptDetectedDefaults, TestGuidedInitQuickDoesNotPromoteHeuristicSecrets

- Failure sites (head log, identical on develop log): `cmd/baha/app_init_wizard_test.go:74,118,170,190,254,306,368` and `cmd/baha/app_init_source_neutral_test.go:72,90`, text `target "company-dev" is not configured`.
- Resolution chain: `cmd/baha/app_init_wizard.go:190` (`selectedTargetName`) → `targetResolutionNameOrEffective` (`cmd/baha/commands.go:1948`) → `effectiveTarget` (`cmd/baha/commands.go:2336`) → `orgSelectionEffectiveTargetWithResolution` (`cmd/baha/config_org.go:55`) → `orgconfig.LoadActiveOptional()` (`internal/orgconfig/active.go:47`, `configFile()` `internal/orgconfig/active.go:100` = `$XDG_CONFIG_HOME` or `$HOME/.config` → `baseharbor/organization/active.json`).
- Why red on the persistent runners: develop's `ensurePackageConfigIsolation` (`cmd/baha/runtime_integration_test_support_test.go:196-203`) pins `XDG_CONFIG_HOME` **only when it is unset** ("already configured for the cell"), so on the self-hosted persistent runner the process reads the host config root `/home/runner/.config/baseharbor/organization/active.json` (the `org=acme`, `defaults.target=dev` → reference `company-dev` selection persisted by earlier CI cycles). The test's own temp config declares only `dev`, hence "not configured".
- Verdict: **(a) test-fixture/environment dependency** — ambient host selection leaking into the test process. No product defect: the same surface is GREEN with the test-side isolation of PR #1750 (`testIsolatedSelectionContext` in `cmd/baha/test_operator_context_test.go`, re-pins XDG_CONFIG_HOME to a private dir when the host file is visible; proven green hosted: workflow_dispatch run `44973644884`, validate job `137058691290`, step 20 receipt "PASS: all six native runtime tests and both package teardowns", company-dev count 0).
- Note: develop's `config_org*_test.go` SaveActive writers (e.g. `cmd/baha/config_org_test.go:76,175`, `cmd/baha/config_org_scope_test.go:29,80`) all pin private `XDG_CONFIG_HOME` via `t.Setenv` — the leak is the persistence-host file, not a test writer.

### Group B — quick-init repository tests (3 names)
TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent, TestQuickInitPreservesWorkloadOnlyRepository, TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload

- Same `target "company-dev" is not configured` resolution chain through `effectiveTarget`; these run via `testOperatorContext` (`cmd/baha/repository_up_init_test.go`, 3 call sites at develop) without host-selection isolation on develop.
- Verdict: **(a) test-fixture/environment dependency**, same fix surface (PR #1750 extends `testOperatorContext` to call `testIsolatedSelectionContext`).

### Group C — perses status/dashboard tests (4 names)
TestBahaStatusHostContainersDashboardsExposesUnavailable, TestBahaStatusInfrastructureDashboardsExposesEveryPanel, TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace, and the guided-init "resolve probe" case

- Failure text: `resolve probe application: target ... : target "company-dev" is not configured` (3 sites in the head log), i.e. the probe application's target reference resolves through the same `effectiveTarget`/org-selection chain.
- Verdict: **(a) test-fixture/environment dependency** (same root cause, same fix surface in PR #1750's changed files `cmd/baha/app_perses_*_test.go`).

### Group D — TestSharedBackendReconcileRejectsSecondProcess (1 name)
- Failure: `cmd/baha/application_lifecycle_lock_test.go:155` — `second process was not rejected fail-closed on the shared provider owner; exit=exit status 1 output: child entered shared reconcile while another process held it`.
- Cause: the spawned child inherits the package process environment (BASEHARBOR_TARGET/ENV and host XDG selection); the child's reconcile fails on the leaked `company-dev` selection instead of the lock rejection path.
- Verdict: **(a) test-fixture/environment dependency**; fixed in PR #1750 via `envWithoutLeakedTargetSelection` for the child env.

### Cross-cutting (not among the 14, for completeness)
- ORAS absence in the validate cell was a **(c) runner-prerequisite** (validate job never ran `scripts/ci-install-oras.sh`); resolved inside the test surface by `provisionORASForIntegrationCell` (`cmd/baha/runtime_integration_test_support_test.go` calling `ensureRuntimeIntegrationTrustPlane` → `includeInstalledORASOnPath` + production `installORAS`, pinned `orasSetupVersion = "1.3.6"` in `cmd/baha/oras_setup.go:24`) on PR #1750 — that is why `TestRepositoryWorkflowRealLifecycle` is no longer among the 14.
- `context_terminal_test.go:467` "zsh is required…" (cli-3 red on #1752/#1750 draft runs) stays **(c) runner-prerequisite**, Owner/CI scope, fixed by card 0428-229 (PR #1754, unmerged).

## Conclusion

All 14 are group-(a) environment/fixture leaks of the ambient organization selection on the persistent self-hosted runner; zero are group-(b) product defects. The remedy already exists and is proven green, but only on unmerged PR #1750 (head `f16cef27f4d`, still OPEN, unmerged) — develop `8b9a8f50645` does not contain `testIsolatedSelectionContext` (measured: `git show 8b9a8f50:cmd/baha/test_operator_context_test.go | grep -c ... = 0`). Until #1750 merges, every head cut from develop — including #1754's — repeats these 14.

## cleanliness

Session pid 1992354 (docker witness taken in the same shell family). This dispatch was read-only against the product remote; no container or compose project was started by it. The only stack witnesses were this card's earlier local probe leftovers (compose projects bh-itest-1c3f4e6d-12470 and bh-itest-7daed22f-28345, config dirs under /var/tmp/0428-223-evid and /var/tmp/0428-223-gotmp — this lane's scratch convention), all already Exited (0/130/143), none running. Removed via 'docker compose -p <proj> down -v --remove-orphans' (no resources found for the projects) plus 'docker rm -v' of the 8 exited containers.

- Before: `docker ps -a` bh-itest count = 8 (all Exited, 0 running)
- After: `docker ps -a` bh-itest count = 0
- Scratch: all `/var/tmp/0428-223*` removed (0 remaining); temporary hopzone `/tmp/opencode/0428-223-hopzone` deleted + `git worktree prune` (no foreign worktree touched).

END 0428-223-testctx DONE (read-only diagnosis; kein push erfolgt)

## publishing note (plan repo)

The earlier commit 25acb4be4 (published during a transport hiccup before the cleanliness section existed) was superseded by the final single commit e73b12f52 (identical content plus cleanliness + the corrected plan publish line) pushed with --force-with-lease; only the file content changed, nothing else on plan main.

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep develop-full-suite-red/diagnose-1
evidence/r28-welle5-2026-11-22/develop-full-suite-red/diagnose-1.md
```
