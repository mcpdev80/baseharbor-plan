# round-6-redfirst — management-host (w289-0427-036-redfirst)

Lane: w289-0427-036-redfirst. Coord: a4573079. Evidence-only correction round to CODEX-REJECT act-1405a.
No product code changed. No `.github/**` touched (Owner scope). No containers on this host (codeman server).

## PLAN

- 1) Remote reality: ls-remote develop + work/r27-management-host, verify both SHAs
- 2) Isolated detached worktree on the sick SHA 64d93e94, candidate untouched
- 3) Behavioral red test: public-API test that USES the bootstrap-ownership bridge and FAILS behaviorally on sick
- 4) Same test on candidate 0f08b877 => GREEN (candidate-green witness)
- 5) Mutation harness (mutation_mgmt_host.sh) on candidate: L0 GREEN / L1 RED / L2 GREEN, L0==L2
- 6) CI capture for the new Go regression (job + trigger file:line)
- 7) Evidence written HERE (baseharbor-plan), git add <file> only, push to origin/main
- 8) worktree cleanup (no corpse), END to a4573079

## BASE ATTESTATION (branch provenance is proof)

- Candidate head: `0f08b877f4152c156b219ff6d13ab05ee6b082de` (ls-remote witness below).
- Sick (named bad) commit: `64d93e945aed892d2457bf94ab360cc11cc1567a`.
- sick IS an ancestor of candidate: `git merge-base --is-ancestor 64d93e94 0f08b877` => rc=0 (single integration candidate per chain, AGENTS 3.8).
- Candidate head commit `0f08b877` = "Merge develop dddf0d7823f into work/r27-management-host (basis-auffischung r5)"; its parent chain is
  `0f08b877 -> 5b8c5422 -> 3a80ed04 -> 64d93e94 -> a87f8377 -> 5e4fde71 (develop) -> ...` (round-5 provenance). No foreign candidate carried.
- develop tip at time of this run: `934be499b9d2d894f80889fc23cd811884c8aec4` (ls-remote fresh). Mission basis was `dddf0d7823f6`; develop moved forward after spawn. The red/green mass-giving SHAs remain `64d93e94` (sick) and `0f08b877` (candidate).

## ls-remote witnesses (fresh, this run)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git develop
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-management-host
0f08b877f4152c156b219ff6d13ab05ee6b082de	refs/heads/work/r27-management-host
```

## AUFGAB 1 — red-auf-dem-kranken-commit: genuine behavioral red (public API only)

CODEX act-1405a REJECT required: the exact test/command and LITERAL failing output on the named sick
SHA `64d93e94`, using the production ownership bridge — not a mutant-only summary, not a compile stub.

The r4 regression `TestManagementHostAttachContendedByBootstrapServer` references the r4 sentinel
`ErrManagementHostBootstrapContended`, which does NOT exist on the r3 sick stand (compile error, which is
NOT a behavioral red under RUNBOOK 5.6). To satisfy the verdict WITHOUT touching the public API, I carried
the exact production test into an isolated detached worktree on the sick SHA and asserted the required
BEHAVIOR through the public API only (`NewManagementHost`, `Verify`, `AcquireBootstrapLock` — all public on
r3, defined in `internal/coreinstallation/lifecycle_lock.go`):

File (sick worktree, test-only, no product change):
  internal/coreinstallation/management_host_behavioral_red_test.go
  - seeds a genuine installation with seedInstallation (public test helper),
  - acquires the atomic bootstrap lock on the valid root (simulates the round-3 serve path mid-bootstrap),
  - calls `host.Verify()` on the same valid root,
  - asserts the result is a CONTENDED REFUSAL (verr != nil); it does NOT reference any r4-only symbol.

SICK-SITZ (detached worktree, candidate untouched):
  git worktree add /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w289-sick 64d93e945aed892d2457bf94ab360cc11cc1567a

ROTE AUSGABE — sick 64d93e94 (r3), behavioral RED, exit=1:
  Kommando:
    go test ./internal/coreinstallation/ -run 'TestManagementHostAttachContendedByBootstrapServer_behavioral' -v
  Ergebnis:
    === RUN   TestManagementHostAttachContendedByBootstrapServer_behavioral
    management_host_behavioral_red_test.go:39: Verify on bootstrap-contended valid root on r3 sick = nil (want a contended refusal) — the bootstrap-lock ownership bridge is missing on the attach path
    --- FAIL: TestManagementHostAttachContendedByBootstrapServer_behavioral (0.00s)
    FAIL
    FAIL	github.com/mcpdev80/baseharbor/internal/coreinstallation	0.003s
    exit=1
Ursache (archaeologie, RUNBOOK 5.6): on r3 sick the production `ManagementHost.Verify()` on a VALID root
loads the installation and takes ONLY the kernel lifecycle lock (.installation.lock); it NEVER checks the
atomic bootstrap lock (.bootstrap.lock) on the attach path. With a bootstrap server still holding the
bootstrap lock, Verify() SUCCEEDS (verr==nil) -> two writers coexist. The behavioral assertion (verr != nil)
therefore FAILS on the sick SHA. This is the round-3 gap act-1405c item 1, shown literally on the named commit.

## AUFGAB 1 gegengeprobe — kandidat 0f08b877 GRUEN (behavioral)

SAME test (same inputs, same bootstrap-lock precondition) on the candidate:
  git worktree add /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w289-cand 0f08b877f4152c156b219ff6d13ab05ee6b082de
  go test ./internal/coreinstallation/ -run 'TestManagementHostAttachContendedByBootstrapServer_behavioral' -v
Ergebnis:
  === RUN   TestManagementHostAttachContendedByBootstrapServer_behavioral
  --- PASS: TestManagementHostAttachContendedByBootstrapServer_behavioral (0.00s)
  PASS
  ok  	github.com/mcpdev80/baseharbor/internal/coreinstallation	0.003s
  exit=0
On r4 the production Verify() bridges attach through AcquireBootstrapLock (management_host.go:185-188) and
fails closed with ErrManagementHostBootstrapContended -> the behavioral assertion passes. RED-on-sick /
GREEN-on-candidate, SAME test, SAME inputs.

## AUFGAB 2 — causal mutation on candidate (L0/L1/L2, verified this run)

Harness (already committed on origin/main of baseharbor-plan):
  evidence/r27-welle5-folge-2026-11-06/management-host/scripts/mutation_mgmt_host.sh
run against the detached candidate worktree at 0f08b877 (the script's required argument is the worktree path):
  bash mutation_mgmt_host.sh /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w289-cand
Ergebnis (literal, this run):
  === L0: before mutation (fix in place) ===
  hash: 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca
  L0 test: GREEN
  === L1: under mutation ===
  hash: 553dfa1f918a72125bb7e76b897cd15c446ca0ae62ca97dd94e6d4c951c606da
  L1 test: RED (mutation broke it - causal)
  === L2: after exact restoration ===
  hash: 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca
  L2 test: GREEN (restored)
  === SUMMARY ===
  L0 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca
  L1 553dfa1f918a72125bb7e76b897cd15c446ca0ae62ca97dd94e6d4c951c606da
  L2 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca
  RESTORED-EXACT: L0==L2
The mutation is a MINIMAL surgical edit of the NEW production line only (attach-path AcquireBootstrapLock
bridge, management_host.go:185-187 restored to round-3 gap). L0==L2 exact restoration confirmed. The
candidate working tree was restored to L0 after the run (no MUTATION marker remains; behavioral test still
GREEN after restore).

## AUFGAB 3 — CI capture for the new Go regression (AGENTS 5.3)

The new regressions are Go tests in internal/coreinstallation (management_host_test.go) and cmd/baha
(serve_command_integration_test.go). For PRs targeting develop:
  - .github/workflows/ci.yml:12-16 triggers on opened/synchronized/reopened/ready PR events (Owner scope,
    NOT edited; reported here as file:line per AGENTS 5.3).
  - ci.yml:763-769 runs the selected validation matrix; ci.yml:803-804 maps go-unit-tests to
    scripts/pr-unit-database.sh, whose `go test ./... -count=1` discovers both changed Go packages.
- Exact-head candidate run: PR #1405 head 0f08b877, hosted run 42322027058 reached terminal SUCCESS;
  PR · Validation · go-unit-tests and PR Selected Checks were success. Full run: 15 SUCCESS, 10 SKIPPED,
  0 FAIL (Docker/Podman HA skipped, not claimed). No .github/** edit, no workflow_dispatch/rerun.
- PR #1405 state: OPEN, head 0f08b877, mergeable, not draft.

## repo-rule compliance

- Write set: ONLY baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/management-host/round-6-redfirst.md.
  No product code changed; no .github/**. No .evidence/ in the product repo. No main-branch writes in the
  product repo. Evidence lives ONLY in baseharbor-plan.
- Isolated detached worktrees on the sick/candidate SHAs, candidate untouched (no foreign candidate carried).
- No subagents; every step executed in this session.
- No containers/compose started on this host (codeman server); no ssh VM smoke named by this mission.

## Nachweise (witnesses)

- ls-remote develop 934be499b9; ls-remote work/r27-management-host 0f08b877 (both fresh, this run).
- sick 64d93e94 IS ancestor of candidate 0f08b877 (git merge-base --is-ancestor rc=0).
- Behavioral RED on sick: exit=1, literal output above (management_host_behavioral_red_test.go:39).
- Behavioral GREEN on candidate: exit=0, PASS.
- Mutation L0=8422c938 GREEN / L1=553dfa1f RED / L2=8422c938 GREEN, RESTORED-EXACT L0==L2.
- CI run 42322027058 @ 0f08b877 => success (go-unit-tests success).

## Endstand

- Kein produktcode geaendert. PR #1407 (anderer zweig) nicht angefasst. .github/** nicht aendern.
- Akte hier geschrieben: baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/management-host/round-6-redfirst.md
- worktrees w289-sick + w289-can gelöst (worktree list: keine Leiche).

## End-line

END_DONE w289-0427-036-redfirst: sick=64d93e94 BEHAVIORAL-RED(exit=1 Verify==nil want contended mgmt_host_behavioral_red_test.go:39) cand=0f08b877 BEHAVIORAL-GREEN(exit=0) mutation=L0=8422c938/L1=553dfa1f/L2=8422c938 RESTORED-EXACT ci=go-unit-tests run42322027058 success akte=baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/management-host/round-6-redfirst.md ls-remote develop=934be499b9 work/r27-management-host=0f08b877
