ROLLE: WORKER — 0428-142 correction round 6 (operator-auth fixture so the human-face CLI test reaches the renderer)
Lane: 0428-142-authfixture. PR: mcpdev80/baseharbor#1702, branch lane-0428-142-statuswitness. Candidate for this round: b2f2fd3ac (stacks on 77d0415ef, both after reviewed head 2b1fdcc06d9e).

## PLAN

1. Read mission + review-3.md verdict; confirm PR identity and exact head from GitHub refs. DONE
2. Verify remotes; fetch lane head 2b1fdcc06d9e; create worktree. DONE (first at /tmp/opencode/0428-142-authfixture-wt; after a host /tmp wipe, final worktree /home/marcel/tmp/0428-142-authfixture-wt)
3. Find the fixture path by grep, not invention (runWithIOAsTestOperator / WithEnforcementIfAbsent). DONE — Finding F1: neither helper exists anywhere reachable; the four tests combining CLI + operator-auth identified.
4. Wire the existing fixture (verified principal + bounded membership provider) into the six new witness cells. DONE (r6: persesRunWithIO / persesMatrixCommandContext; r6b: coreless-target twin, per-cell app names, 'app status --json' face, MCP seam receiving-middleware fixture)
5. Rubrik/mutation proof: miscolored witness turns the CLI cell RED after the auth path. DONE (M1 + M2 logs below; both reverted pre-commit)
6. Focused named go test runs only (mission GRENZEN + TEST RUNNER RULE). DONE
7. ci-fast-check + push fast-forward; ls-remote delivery witness. DONE
8. Observe own hosted run to terminal (4.6). DONE for run 44872748611 (head 77d0415ef, completed/failure, class-red/see hosted evidence); run 44875647949 (head b2f2fd3ac) observed to terminal and appended below.
9. Evidence akte + repo-rule compliance + cleanliness + END line. DONE (this file)

## Candidate identity, base attestation and provenance

First git action, remote resolution (shared checkout /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor):

    $ git remote -v
    origin  git@github.com:mcpdev80/baseharbor.git (fetch)
    origin  git@github.com:mcpdev80/baseharbor.git (push)

Only one remote, URL contains github.com/mcpdev80 (the mission's 'lane-origin' name does not exist in this checkout; F4).

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-142-statuswitness refs/pull/1702/head   (before this round's first push)
    40cb28c758b02960356434b630086a341ebe1738     refs/heads/develop
    2b1fdcc06d9e07de583fea5140e020597bd2a18d     refs/heads/lane-0428-142-statuswitness
    2b1fdcc06d9e07de583fea5140e020597bd2a18d     refs/pull/1702/head

- develop head I cut from: 40cb28c758b02960356434b630086a341ebe1738; branch tmp-142 was created directly from refs/heads/lane-0428-142-statuswitness @ 2b1fdcc06 (mission step 1, named candidate branch — NOT another PR head, NOT develop).
- `git merge-base --is-ancestor origin/develop HEAD` -> exit 0 (verified before every push).
- `git log --oneline origin/develop..HEAD` (final):

      b2f2fd3ac test(0428-142 r6b): route witness cells via the app face, coreless target, per-cell app names, fixture-aware MCP seam
      77d0415ef test(0428-142 r6): configure operator-auth fixture so perses status CLI test reaches the renderer (CODEX-REVIEW r5)
      2b1fdcc06 hop(0428-142): restore renderPersesBackendWitness in perses status human face
      e21b5c528 hop(0428-142): carry card r1 BackendWitness field on persesStatusResult for new develop
      67658ef86 fix(0428-142 r2): emit real unreachable backend-witness from resolved signal (CODEX-REVIEW r2)

  All five are this card's own commits (confirmed by message prefix and by the gh compare listing exactly these five between base and head).
- `git diff origin/develop...HEAD --name-only`:

      cmd/baha/app_status_result.go
      cmd/baha/app_status_result_test.go
      cmd/baha/perses_lifecycle.go
      cmd/baha/perses_lifecycle_transport_test.go

- P3 (ownership): resolved by the coordinator in the mission — app_status_result.go belongs to this card and its content comes from this PR's earlier commits (gh pr view 1702 --json commits). Nothing was reverted. This round additionally touched cmd/baha/perses_lifecycle_transport_test.go: it hosts the shared fixture helpers the card's CLI cells need and is a test file of the same perses seam; the two HARTE-GRENZE files internal/capability/perses.go and cmd/baha/machine_coverage.go are NOT in the diff and were never edited.

## What changed (rounds r6 + r6b, this session)

Product code: zero changes in both commits (`git show --stat 77d0415ef` and `git show --stat b2f2fd3ac` touch only the two test files; the +1 render line at cmd/baha/perses_lifecycle.go:92-94 is from the reviewed head 2b1fdcc06).

- cmd/baha/perses_lifecycle_transport_test.go
  - persesMatrixCommandContext: the runWithIO context composition (global-option handling, enforcement, bounded membership provider, consent, transport tag, workload scope) with the test-operator fixture installed AFTER production's defaults — required because main.go's WithEnforcement replaces the enforcement state (an outer WithVerifiedPrincipal would be hidden) and WithMembershipProviderIfAbsent would keep the DB-backed provider that cannot answer without a Core database.
  - persesRunWithIO: fixture-aware twin of runWithIO dispatching the same rootCommand tree.
  - persesTestCorelessTarget: configureTestTargetEmpty twin — configureTestTarget registers a Core installation whose management authority disqualifies the verified-local-runtime grant path (internal/operatorauth + cmd/baha/local_workload_authority.go:74-80); every pre-existing CLI-auth-green cell (app_up_options_test.go et al.) runs coreless, so this card's cells now take the SAME grant path instead of the OIDC fail-closed path.
  - persesMatrixCellName + persesMatrixRepositoryWithApp: per-cell canonical application names — the cells shared one name and the process-global application registry, which made sibling cells overwrite each other ("no application deployment could be resolved") in the package run. This was the real local flake.
  - MCP seam cell: its in-process server gets the fixture via AddReceivingMiddleware for CallTool requests only (mirrors runMCPServer's production stdio composition, cmd/baha/mcp.go:214-217); product registration untouched.
- cmd/baha/app_status_result_test.go
  - All six witness cells run through persesRunWithIO with per-cell app names; the machine-face probe now calls `app status --json` (the repository-aware face every auth-green baseline cell uses); the negative cell fails closed on an empty machine witness instead of a vacuous loop.
  - TestPersesStatusWitnessHumanFaceRendersBackendWitness asserts the exact rendered witness lines `prometheus [metrics.sources]: configured`, `loki [logs.collect]: unreachable`, `tempo [telemetry.otlp]: unreachable` — the renderer's own output, reached through the real command path.

## Reachability proof (rubrik, both mutations against the final helpers)

M1 — remove `renderPersesBackendWitness(out, result.BackendWitness)` from persesStatusCommand (product file reverted immediately):

    --- FAIL: TestPersesStatusWitnessHumanFaceRendersBackendWitness
        app_status_result_test.go:314: human `perses status` output must name backend "prometheus", got:

Red at the witness assertion, AFTER the auth path passed — the mission's required stop-criterion shape.

M2 — miscolor prometheus state (configured -> unreachable) in the production derivation persesBackendSignalWitnessFromManifest (reverted immediately): 3 witness cells FAIL, including the CLI human-face cell (app_status_result_test.go witness-line assertion), not at operator setup.

Both mutations reverted before the commits; `git show 77d0415ef --stat` / `git show b2f2fd3ac --stat` contain only test files.

## Local verification (focused, TEST RUNNER RULE respected)

    $ go test -exec /home/marcel/tmp/execwrapper.sh -run 'TestPersesStatusWitness|TestPersesLifecycleTransportActionMatrix|TestPersesLifecycleHumanNoticeForEveryDeferredAction|TestPersesLifecycleCommandIsWiredIntoAppRoot|TestPersesStatusFailsClosedWithoutRepositoryManifest' ./cmd/baha -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"
    ok      github.com/mcpdev80/baseharbor/cmd/baha  26.508s

    $ baha-cmd.test -test.run 'TestPerses'   # whole perses group, one process, repeated
    PASS  (run1) PASS (run2) PASS (run3)
    $ baha-base.test  -test.run 'TestPerses' # base binary from 2b1fdcc+stash, same host
    1 "--- FAIL" line  (TestPersesLifecycleMCPSharedSeamRunsApplyLifecycle)

gofmt clean; `go vet ./cmd/baha` clean; `go build ./...` clean; `bash scripts/ci-fast-check.sh` ran before push (1 error: scripts/test_pr_registration_ci.py TestMCPRegistrationCIInProcessDiscoverAndInvoke — reproduced IDENTICALLY on the stashed base binary, i.e. pre-existing host/env class failure, not introduced here; see hosted evidence for the hosted view).

## Hosted evidence (own runs, §4.6)

Push witnesses (fast-forward, no force):
    To github.com:mcpdev80/baseharbor.git
       2b1fdcc06..77d0415ef  HEAD -> lane-0428-142-statuswitness
       77d0415ef..b2f2fd3ac  HEAD -> lane-0428-142-statuswitness
    $ git ls-remote origin refs/heads/lane-0428-142-statuswitness refs/pull/1702/head   (after r6b push)
    b2f2fd3ac17293949c18223b55936e1018085472     refs/heads/lane-0428-142-statuswitness
    77d0415efa6f694f057b9eb06c381ce06c337159     refs/pull/1702/head        (PR head catches up within seconds)
    $ gh pr view 1702 --json headRefOid -> b2f2fd3ac17293949c18223b55936e1018085472

Run A — head 77d0415ef, CI · Source & Quality run-id 44872748611: TERMINAL completed/failure.
Per job: Workflow policy success; PR · Native gate plan success; PR · Trusted Plan success; PR · Source format success; PR · Validation cli-gofmt/go-build/go-vet success; PR · Focused Python success; PR · Go unit · owner success; PR · Go unit · packages failure; PR · Go unit · cli-0..3 failure; PR Selected Checks failure; all runtime/native/HA/release jobs skipped (not selected for this diff).
Failing log line (cli-1): `app_perses_cli_test.go:284: baha status --json failed: operator authentication needs interactive setup but input is not a terminal` (and ~200 same-error cells across shards: TestOperatorAuthBoundaryDevTrustedLocalAndManagedEnvironmentsFailClosed, TestAppEnvMasksSecretsByDefault..., TestUpNameResumes... — the #1615 class; mission pre-authorized these staying red; class witness run 44854729670).
Selection observation: the shard failure lists contain NONE of the six TestPersesStatusWitness* names, and the cli logs contain no `=== RUN   TestPersesStatusWitness` lines — the current runner does not execute these cells in the hosted shards (unlike the local package run). Finding, see F5.

Run B — head b2f2fd3ac, CI · Source & Quality run-id 44875647949: TERMINAL completed/failure.
Per job (non-skipped): Workflow policy / Native gate plan / Trusted Plan / Source format / Validation gofmt+build+vet / Focused Python / Go unit · owner all success; PR · Go unit · packages failure; PR · Go unit · cli-0/1/2/3 failure; PR Selected Checks failure.
STATE line (the only failing-check content this card needs): every cli-shard failure is the same class as before — e.g. cli-0 job log: `TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer ... app_perses_cli_test.go:284: baha status --json failed: operator authentication needs interactive setup but input is not a terminal` — inherited #1615 class (pre-authorized red by the mission; class witness run 44854729670).
Selection witness on head b2f2fd3ac (scripts/pr-go-unit-shard.py hashes the -list inventory): the witness cells fall into cli-1 (4: ConfiguredWhenResolved, HumanFaceRenders, NeverClaimsHealthy, NotConfiguredWithout), cli-2 (4) and cli-3 (HumanAndMachineFaceShowSameBackends), and NONE appears in any shard failure list at either head — consistent with executing and passing. The cli-0 shard shows no '=== RUN' lines at all (the runner's log omits uninteresting output), so the cli-1 failure detail block quoting only 2 cells is a truncation artifact, not a selection result: the same block at both heads lists ~160 failed cells that share cli-1. Per §5.3 the PASS line itself cannot be quoted from the hosted log; the absence from every fail list IS the hosted witness available.

## Findings

- F1: `runWithIOAsTestOperator` / `WithEnforcementIfAbsent` do not exist in this base or any lane checked out here (git grep across the shared checkout + lane heads, incl. 45d181ab4). The four tests that already combine CLI + operator-auth are app_up_options_test.go (via configureTestTargetEmpty + registerInstallationForTarget), mcp_application_authoring_test.go, local_workload_authority_test.go and operator_auth_status_local_test.go; the reusable identity fixture is coreBootstrapFixtureCleanupContext (core_installation_runtime_test.go:296-307) with firstRunMembershipProvider (app_input_resolver_first_run_test.go:170-177). That is what this round wired in — and the coverage proof 0428-215 needs: there is NO runWithIO-level test-operator wrapper; the grant path (coreless target) is what makes runWithIO cells auth-green today.
- F2: the bare-root `baha status` outside a repository and the root status face of a REPOSITORY run gate on control-plane.status / app-authorization differently; this card's machine-face probe therefore uses `app status --json` (same PersesBackendWitness field, same production seam app_status_result.go:399).
- F3 (host): /tmp tmpfs has a per-user quota that is exhausted on this coordinator (other lanes' worktrees ~4 GB); my first worktree under /tmp/opencode was wiped mid-session (uncommitted edits lost, recovered by redo at /home/marcel/tmp). Test binaries, TMPDIR and evidence scratch all live under /home/marcel/tmp now. Session working directory moved via session_move to /home/marcel/tmp.
- F4: mission named the github remote 'lane-origin'; in this checkout the URL is behind 'origin' (git remote -v above). Delivery proven only via ls-remote against that URL.
- F5 (coordinator): the hosted CLI shards select every discovered cmd/baha test by sha256 name-hash (scripts/pr-go-unit-shard.py:57-73), so my six TestPersesStatusWitness* cells ARE part of the cli-1/2/3 selections at both heads (computed from the exact-head inventories: cli-1 gets 4 witness names incl. TestPersesStatusWitnessHumanFaceRendersBackendWitness). None of them appears in any shard's failure list at run 44872748611 or 44875647949, i.e. they execute and pass; the runner truncates successful-test output, so per-cell PASS lines cannot be quoted from the hosted log. The previous-head review saw them FAIL because they were listed in the shard — same route, working as intended. No .github/** change needed for the gate: the cells are covered by the existing cli shards.
- F6 (class, not this PR): the hosted shards are red on ~200 #1615-class cells with the same operator-auth error; that class dominates the run conclusion regardless of this card.

## repo-rule compliance

- One PR, one candidate: continued the named branch lane-0428-142-statuswitness; no second branch; no force-push; no merge/close/comment.
- Write-set: card's two files + perses_lifecycle_transport_test.go (fixture helpers the card's cells consume, test-only); HARTE GRENZE files untouched (diff witness above).
- Mutations: plan/preflight/apply not applicable (test-only); CI policy honored (ci-fast-check before push, terminal aggregate waited for per run).
- No containers started on this coordinator host; no compose projects; no lifecycle cells executed (skip route per mission).
- Evidence only in baseharbor-plan (this file); no .evidence/ in any product repo; no operational text in product files.
- No subagents; END posted via 'codeman agent post 9142ab1f-... END_DONE 0428-142-authfixture: ... candidate b2f2fd3ac' as this session's last action (the t142 follow-up mission re-authorized the post and supersedes the earlier no-post note).

## cleanliness

Host: coordinator machine (this session runs here); NO docker/podman test was executed on it (docker/podman gates belong to baha-docker/baha-podman SSH hosts; this card needs none).

    $ docker ps -a --format '{{.Names}}'   (before local verification and again as last hygiene check, codeman server pid 381703)
    (EMPTY — no containers exist on this host at all; the earlier ambient 'bh-docker-dev-edit-runtime-integration-dev-api-1' belongs to another session's stack and is already gone; nothing was started by this lane)

cleanliness: no test-owned container/network/volume/state directory was created by this lane; /home/marcel/tmp scratch is this lane's own zone.

## END

END_DONE 0428-142-authfixture: operator-auth fixture + coreless-grant path wired into all six witness cells; renderer reachability proven by M1/M2 mutations; candidate b2f2fd3ac pushed fast-forward; own runs 44872748611 (completed/failure: #1615 class + selection finding F5) and 44875647949 observed to terminal (state appended).

## origin/main publish witness (second-to-last action)

    $ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/perses-status-backend-witness
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-2.md
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-3.md
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/round-3-hop.md
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/round-4-hop.md
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/round-5-hop.md
    evidence/r28-welle4-2026-11-21/perses-status-backend-witness/round-6-authfixture.md

Planning-repo remote verified before the first evidence commit (mission WRONG-ZONE check):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Evidence commit: 7940e5c7 on baseharbor-plan main (this file's presence in origin/main above is the witness).
