# 0428-220 hottarget: target-hotfix-inspection-config-missing (round 2, port)

ROLE: Worker. CARD: t-20261121-target-hotfix-inspection-config-missing (0428-220).
BRANCH: lane-0428-220-hottarget. PR: one new PR against develop.

## PLAN

1. Reality check: verify planning remote, measure develop HEAD via ls-remote, confirm no foreign PR owns 0428-220, cut/confirm worktree from develop.
2. Port the fix: apply the content of commit 46017060d ("register target before selecting it") onto the current develop file cmd/baha/target_hotfix_test.go (map the change onto develop's current context, do NOT cherry-pick -- the 198-lane is ~197 commits behind develop).
3. Proof-of-port (the real value of this card): (i) after the hotfix path the configured target edge-a resolves (assert on target name), (ii) a genuinely unknown target still fails closed ("target ... is not configured"), (iii) mutation: restore the bad 't.Setenv("BASEHARBOR_TARGET","edge-a") before create' order -> the test must go RED.
4. One PR: branch lane-0428-220-hottarget vs develop; prove delivery with git ls-remote on the PR head.
5. End-SHA proof: merge-base --is-ancestor origin/develop HEAD = YES, rev-list --count head..develop = 0, git log --format=%an develop..HEAD = exactly one identity, diff --name-only = exactly cmd/baha/target_hotfix*.go. Terminal hosted cli-3 run at the exact head.
6. Evidence file round-2-port.md: three measurements, port diff, mutations, the run, PLAN list, repo-rule compliance, cleanliness.

## Reality check

- Planning repo remote (verified BEFORE any evidence commit): `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- develop HEAD: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`.
- `git diff e6c199e7b7dd 46017060d -- cmd/baha/target_hotfix_test.go` shows the fix mechanics (see Port section).
- No foreign PR owns 0428-220 (gh pr list --search 0428-220 empty).

## Port: commit 46017060d onto develop

- Commit 46017060d author Marcel Pfingstgräf, 2026-11-21 05:43, changes EXACTLY ONE file cmd/baha/target_hotfix_test.go (+7/-5 net).
- Mechanic: move `t.Setenv("BASEHARBOR_TARGET","edge-a")` from BEFORE createTarget to AFTER createTarget, and set it empty at the top, so the env points at the configured target only after registration.
- develop's current file at HEAD already differs from 46017060d's PARENT (develop uses withTargetOverride at the call site); porting 46017060d's INTENT onto develop means the test selects edge-a via env AFTER createTarget, and calls collectTargetInspection with context.Background() so resolution reads the env.

## DISPOSITION (coordinator call: read ans-220b.md, read (a) correct)

Owner answer ans-220b.md: my round-2 answer point (a) is correct; point (3) was wrong, remote-proven not from my text.
No PR, no port. Card to be set to `closed` / `resolution: dropped` by the coordinator (reason: the reported bug does not
exist on current develop; verdict run 44867319394 ran on a pre-fix head of the 198 stack, not on develop).

Literal proof (measured):
  - `git show e6c199e7b7dd:cmd/baha/target_hotfix_test.go` line 203:
      result, err := collectTargetInspection(withTargetOverride(ctx, "edge-a"))
  - `git show 46017060d:cmd/baha/target_hotfix_test.go` line 16:
      t.Setenv("BASEHARBOR_TARGET", "")
  - Conclusion: the `withTargetOverride` form is exactly what 46017060d~1 named; 46017060d itself sets
    `t.Setenv("BASEHARBOR_TARGET", "")` (line 16). 46017060d is a different, OLDER branch of the same fix, NOT the
    missing precursor on develop. Reading (a) is correct.

Green on develop (local only, NOT durable evidence per 5.3):
  - All target/create cases green on develop in 9.65s (local host, single test 0.049s). A local pass is enough for the
    disposition decision, NOT for a hand-off acceptance.

The actual remainder we both care about:
  - The reported failure is red ONLY on the 198 stack. PRs on that stack (all OPEN, MERGEABLE as measured now):
      PR 1737  state OPEN   mergeable MERGEABLE
      PR 1740  state OPEN   mergeable MERGEABLE
      PR 1741  state OPEN   mergeable MERGEABLE
  - To be entered into the 198-stack inquiry to the owner by the coordinator.

## Querbehauptung (cross-reference 0428-223)

- 0428-223 class: umgebung, message `target "<name>" is not configured`, root since 80961866f.
- THIS card's fix is a TEST-ORDERING fix (env set after registration), NOT a change to the deployment.ErrConfigMissing resolution path. It does not repair the 0428-223 umgebung class.
- clears 0428-223 class: nein.

## Repo-rule compliance

- Write-set: ONLY cmd/baha/target_hotfix*.go (per contract).
- TABU untouched: .github/**, scripts/**, internal/identityprovider/**, internal/serviceaccess/**, internal/operatorauth/**, internal/capability/perses_selection.go, internal/observability/registry.go.
- No bare go test ./... or go test ./cmd/baha/ on this host. Targeted -run with skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication".
- No merge, no second PR, no subagents (4.8), no git add -A, no workflow_dispatch/rerun.
- .github/** not touched; no CI file changed (Owner scope).

## Cleanliness

- docker test run: none.
- git worktree: lane-0428-220-hottarget-wt at develop e6c199e7b7dd.
- No containers/networks/volumes left behind.

## END lane-0428-220-hottarget DONE

## Status

- DONE. Disposition: card dropped by coordinator (read (a) confirmed). No PR, no product change, no merge.
- Evidence committed to baseharbor-plan origin/main as 407be025b (cherry-picked from local 0f699c0ec onto remote tip 9d561928 to bypass other lanes' rebase conflicts on card/view files). ls-tree on origin/main confirms both target-hotfix-inspection/round-1.md and round-2-port.md present.
