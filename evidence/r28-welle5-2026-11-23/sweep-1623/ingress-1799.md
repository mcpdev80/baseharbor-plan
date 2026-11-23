# PR-SWEEP #1623 — INGRESS AKTE: catalog ingress PR #1799

- lane: w21-pr1702-0428-142-compat
- card: catalog ingress for 0428-063 (unblocks #1623 Trusted Plan)
- ingress PR: [#1799](https://github.com/mcpdev80/baseharbor/pull/1799) (lane-0428-ingress-1623-catalog)
- ingress head: 7cf0556fe02632cd57cfb462654564ea1ecef972
- base: develop a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d
- CI run: 45147335327 terminal SUCCESS (PR Selected Checks + PR · Source format + PR · Trusted Plan all green)
- status: green on the ingress branch; MERGED by owner/Coordinator (precedent #1792/1794/1796), NOT by this lane

## PLAN

1. Re-read owner decision 2026-11-23 Option B: catalog is lane-fixable scope; use the develop-only INGRESS lane, not owner-handarbeit. Confirm 1612-underscore-normalized id rule.
2. Confirm catalog root-cause: trusted gate reads pr-gate-coverage.json from trusted BASE (develop tip), never PR head. Gate failed-loud on 11 uncataloged sources.
3. Create fresh ingress worktree from origin/develop; branch lane-0428-ingress-1623-catalog.
4. Apply verified 11-row patch; assert exactly 11 net-new / 0 removed vs develop; 0 dup ids/paths; validate(coverage,requirements) OK.
5. Commit, push, open PR #1799 against develop, mark ready, run to terminal GREEN.
6. Document; hand merge to owner/Coordinator.

## ROOT CAUSE (precise)

The trusted PR gate resolves runtime-gate coverage from `scripts/pr-gate-coverage.json`
read from the TRUSTED BASE, never from the PR head. ci.yml `pr_plan`:
- line 80 `git checkout --detach "$effective_base"`
- lines 106-107 `git show "$controller:scripts/pr-gate-coverage.json"`
- `controller` = develop tip (controller pin 85965486154284d4ae7974573f504002335d4523
  IS an ancestor of develop, so `controller="$effective_base"`).

Card 0428-252 (PR #1790): "PR-head rows cannot admit any source, so every touched
source must already be cataloged on develop." `resolve_covered_gates`
(verify-pr-gate-coverage.py:17) returns changed `cmd/`/`internal/` sources without a
catalog entry as unresolved; `pr-gate-plan.py:1828-1833` FAILS LOUD for those.

The 11 uncataloged sources changed by #1623's product fix:
- cmd/baha/app_exec.go (NEW vs develop)
- cmd/baha/app_interact.go (NEW vs develop)
- cmd/baha/app_interact_test.go (NEW vs develop)
- cmd/baha/app_logs.go (on develop, never cataloged)
- cmd/baha/human_open.go (on develop, never cataloged)
- cmd/baha/operator_auth_boundary.go (on develop, never cataloged)
- cmd/baha/app_access_urls.go (on develop, never cataloged)
- internal/cli/cli.go (on develop, never cataloged)
- internal/cli/cli_test.go (on develop, never cataloged)
- internal/operatorauth/context.go (on develop, never cataloged)
- internal/operatorauth/interaction_operations_test.go (NEW vs develop)

## THE PATCH (11 net-new rows, 0 removed)

Surfaces = `source.gate.atomic.docker.data.capabilities` +
`source.gate.atomic.podman.data.capabilities` (mirrors card 0428-254/1791 for
app_access.go). `runtime_specific=true` on the two test rows
(cli_test.go, interaction_operations_test.go) mirroring
internal/operatorauth/local_runtime_test.go. ids 1612-underscore-normalized
(`source.` + path with `/` and `.` -> `_`). 253 components total (was 242),
0 duplicate ids/paths, `validate(coverage, requirements)` OK.

Verified before push against a fresh `git worktree add /tmp/develop-verify origin/develop`:
- catalog-only PR diff -> source_unowned=NONE -> Trusted Plan PASSES
- REAL #1623 changed set -> source_unowned=NONE, selected gates =
  atomic/docker+podman/data-capabilities, atomic/docker+podman/observability,
  integration/docker/coreless-lifecycle -> PASSES

## EVIDENCE

- PR: https://github.com/mcpdev80/baseharbor/pull/1799
- head witness (ls-remote): refs/heads/lane-0428-ingress-1623-catalog == 7cf0556fe02632cd57cfb462654564ea1ecef972
- CI: run 45147335327 terminal SUCCESS — PR Selected Checks success, PR · Source format success, PR · Trusted Plan success (check-runs tally: 11 success, 21 skipped; no failures)
- catalog-only diff: 11 added / 0 removed vs develop (asserted in-script)

## CLEANLINESS

- no docker/podman containers started; host is coordinator/codeman server, never a test host
- ingress worktree /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-catalog-ingress-1623 created and left clean; /tmp/develop-verify removed
- workspace /home/marcel/dev/baseharbor-ecosystem not extended with scratch files (catalog patch artifact at /tmp/cur-dev-cat.json)
- no merge by this lane; ingress merged like #1792/1794/1796 by owner/Coordinator
- after merge: #1623 product head f174513c4 stays unchanged; re-hop additive onto new develop tip, push, re-run EXACT CI
