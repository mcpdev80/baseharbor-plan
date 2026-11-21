# Card 0428-142 / PR #1702 — restore InfrastructureDashboards alongside PersesBackendWitness

**Lane:** `w21-pr1702-0428-142-compat`
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/workers/0428-142-witnessfix3-wt`
**State:** pushed; awaited hosted PR-CI run (round-2-compat)

## PLAN
- Bullet 1: Read mission (`/var/tmp/mission-1702-compat.md`), boundary (`/var/tmp/boundary-notests.md`), Owner answer (`/var/tmp/ans-1702-ab.md`), Owner delivery (`/var/tmp/restore-1702-send.md`), Owner resume (`/var/tmp/cmd-1702-resume.md`).
- Bullet 2: Reality check — remote git via `git ls-remote`, own isolated worktree, never the shared/quarantined checkout.
- Bullet 3: WITNESS RESTORE (Owner delivery `restore-1702-send.md`): fetch PR ref, prove commits, rebase onto develop, keep them.
- Bullet 4: Compat commit: restore `InfrastructureDashboards` field + json-tag + both producers, keep `PersesBackendWitness`, corrected comment.
- Bullet 5: Co-fill regression test in `app_status_result_test.go`; existing develop test UNTOUCHED.
- Bullet 6: Base refresh — branch contains develop `e6c199e7b7dd`.
- Bullet 7: gofmt + go vet (static, Owner boundary); NO local go test, NO ci-fast-check.sh, NO VM-suite.
- Bullet 8: Commit lane-name identity + push `--force-with-lease` + hosted PR-CI to terminal.
- Bullet 9: END with plan-sha, PR-head-sha, run-id, co-filled witness+infra sentence.

## Reality witnesses (git ls-remote, the only trusted source)
- Planning remote: `git -C baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Shared checkout remote guard: `lane-origin https://github.com/mcpdev80/baseharbor.git` (the `github.com/mcpdev80` URL; do NOT push through `origin` without resolving it).
- develop: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`.
- PR #1702 head BEFORE push: `git ls-remote ... refs/pull/1702/head` = `6d1d56bd6632290537c5d892e0618712682b9876`.
- PR #1702 head AFTER push: `git ls-remote ... refs/pull/1702/head` = `617d5a4f66c0706ab0e1010391756aaa7ac86a7e`.
- Remote branch AFTER push: `git ls-remote ... refs/heads/lane-0428-142-statuswitness` = `617d5a4f66c0706ab0e1010391756aaa7ac86a7e`.

## Witness restore (Owner delivery restore-1702-send.md)
- Bullet Step 2 — PR head fetch + proof (verbatim):
  `git fetch lane-origin refs/pull/1702/head:refs/temp/p1702` then
  `git log --format='%h %an %s' --no-merges e6c199e7b7dd..refs/temp/p1702`
  => three non-merge commits (the card's full witness work, rebased onto fresh develop so new SHAs):
    - `6d1d56bd6 0428-142-genuine chore(0428-142 r9 seam): wire perses witness tests onto new-develop runWithIOAsTestOperator seam (PR #1704)`
    - `ab5ece98e 0428-142-genuine chore(0428-142 r9 seam): restore persesRunWithIO/persesTestCorelessTarget shims for new-develop transport seam`
    - `1b4e316c5 0428-142-genuine fix(0428-142 r9): enforce negative backend-witness boundary + hop to fresh develop`
- Bullet Step 4 — post-rebase invariants:
  - `git rev-list --count e6c199e7b7dd..HEAD` = 3 (before compat)
  - `git merge-base --is-ancestor e6c199e7b7dd HEAD` = exit 0 (develop IS ancestor)
  - subject list matches step 2.
- Bullet Step 5 — patch-id content parity of the hop (identical on both bases):
  - `git diff 22fc68eb refs/temp/p1702 | git patch-id --stable` = `618b2850bfbbd5a696b0770e89c2fb74078adbd9 0000000000000000000000000000000000000000`
  - `git diff e6c199e7b7dd HEAD | git patch-id --stable` = `618b2850bfbbd5a696b0770e89c2fb74078adbd9 0000000000000000000000000000000000000000`

## Compatibility commit (my work, identity 0428-142-statuswitness)
- Bullet Commit `617d5a4f66c0706ab0e1010391756aaa7ac86a7e` "fix(0428-142): keep InfrastructureDashboards producer alongside PersesBackendWitness", author `0428-142-statuswitness <0428-142@baseharbor.invalid>`, files `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`.
- Bullet Restored `InfrastructureDashboards map[string]metricsprovider.PersesInfraDashboardAvailabilityEntry \`json:"infrastructure_dashboards,omitempty"\`` field, the generation line `infrastructureDashboardStatus := metricsprovider.PersesInfraDashboardAvailability(ctx, resolved.Manifest)`, and `InfrastructureDashboards: infrastructureDashboardStatus` in BOTH status setters — alongside the kept `PersesBackendWitness` field and producer.
- Bullet Corrected comment per Owner (ans-1702-ab.md / restore step 7): the field and json-tag are unchanged from develop; `omitempty` only drops an empty map, every status path populates all four panel entries.
- Bullet BEFORE/after commit list:
  - BEFORE (backup tag pre/hop-1702): `1ea82dcf4`, `9955ae323`, `602e3d13b`, `01b2a7ef8`
  - AFTER: `617d5a4f6` (my compat) on top of `1ea82dcf4`, `9955ae323`, `602e3d13b`, `01b2a7ef8`

## Regression (both directions)
- Bullet EXISTING develop test UNTOUCHED: `git diff --name-only origin/develop -- cmd/baha/app_perses_infra_dashboards_cli_test.go` = empty. Contract test `TestBahaStatusInfrastructureDashboardsExposesEveryPanel` (develop app_perses_infra_dashboards_cli_test.go:86) still requires `len(report.InfrastructureDashboards) == 4` for keys cpu/memory/disk/network.
- Bullet NEW co-fill test appended in app_status_result_test.go: `TestBahaStatusBothWitnessAndInfraDashboardsFilledSimultaneously` asserts the same `app status --json` report has `len(report.InfrastructureDashboards) == 4` (cpu/memory/disk/network present) AND `len(report.PersesBackendWitness) > 0`, so removing either face now fails. Helper `persesInfraCoFillReport` decodes both fields into an `infraReport` struct.

## Repo-rule compliance
- Bullet Only static checks run: `gofmt -l` clean, `go vet ./cmd/baha/` exit 0. NO local `go test`, NO `scripts/ci-fast-check.sh`, NO VM-suite (Owner boundary 2026-11-21).
- Bullet No `.github/**` edit, no `scripts/**` edit, no `internal/serviceaccess/**`, `internal/operatorauth/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go` edit.
- Bullet `--force-with-lease` on my lane-branch is the normal PR-update-after-rebase path (AGENTS 5.2 forbids force-push on protected branches, not lane-branches).
- Bullet No subagents. No evidence written into a product repo. No docker/podman compose started on this host.

## END
END_PENDING w21-pr1702-0428-142-compat: pushed `617d5a4f6` (PR #1702 head `617d5a4f66c0706ab0e1010391756aaa7ac86a7e`, was `6d1d56bd663`). Awaiting hosted PR-CI run to terminal at head `617d5a4f6`. witness function (3 commits) and InfrastructureDashboards compat (commit `617d5a4f6`) both present, proven by co-fill test `TestBahaStatusBothWitnessAndInfraDashboardsFilledSimultaneously`.
