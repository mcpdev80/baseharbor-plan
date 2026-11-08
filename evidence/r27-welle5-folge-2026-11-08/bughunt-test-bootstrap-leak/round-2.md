# Evidence: Bug t-20261108-bughunt-0427-test-bootstrap-leak (0427-127) — round 2

Shift r27-welle5-folge-2026-11-08. Lane mission `mission-127-r2.md`, candidate branch `work/0427-127-test-bootstrap-leak` (PR #1454), single candidate per chain (AGENTS 3.8).

## PLAN

- Read the full correction recipe `act-1454-review.md` from origin/main (4815359d lineage, fetched); confirm PR #1454 head f03b12bdd and develop base via ls-remote only.
- Set up worktree on the named candidate branch only; fetch develop AKTUELL (drift notice: 07ae6c3e9 access-wizard merge), merge, prove ancestry, run conflict check (orgconfig/accesswizard files touched by the merge; no conflict with my files).
- Recipe (1): bind cleanup to the package/singleton lifetime — TestMain-level teardown with durable marker fail-safe; remove first-*testing.T registration and the late-registration gap; setup capture becomes explicit failure.
- Recipe (2): wächter scoping to exactly this run's generated target/project namespaces plus explicitly derived shared subprojects; broad `bh-w169-*` filter removed; inventory errors stay fail-closed.
- Recipe (3): durable package-coverage tests (multi-caller cleanup, panic/setup-failure paths, watcher foreign-lane exclusion, fail-closed inventory).
- Recipe (4): CI routing OWN-BLOCK below; no workflow file touched, no rerun/dispatch triggered. IMPORTANT discovery: `cli-package-tests` on PRs is NOT a full package run — `scripts/validation-owner.sh` (cli-package-tests branch) executes selector groups (`^TestGuided`, named doctor tests, `./internal/application/...`, …) and none of them matches `^TestBootstrap…`. The new proofs therefore need an explicit selector entry to be CI-visible; see OWN-BLOCK item 2.
- Push follow-up commits to the named branch, observe CI terminal on the exact candidate (4.6), publish evidence, END.

## Base attestation

Planning repo (authoritative) — one-line witness as required:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
origin: https://github.com/mcpdev80/baseharbor-plan.git
```

(NOT the workers/baseharbor-plan directory; no evidence was committed to any product repo.)

Product repo remote truth measured via `git ls-remote` from the fresh worktree only:

```
$ git ls-remote origin refs/heads/develop refs/pull/1454/head
e39b0004346cdfd082e34ba55d94d24757bbbd27    refs/heads/develop      (initial; drift notice later)
f03b12bdd0b9549b9dd36dae2d947db322caac6e    refs/pull/1454/head
$ git ls-remote origin refs/heads/develop   (drift refresh per coordinator notice 2026-11-08)
07ae6c3e91b081a189266ca4b162ba705d4aa78f    refs/heads/develop
```

- Branch cut: the mission names the existing candidate branch; worktree HEAD started at its exact head `f03b12bdd` (its only non-develop commit; develop-at-cut ancestor was `e39b00043`).
- Drift-merge: `origin/develop@07ae6c3e9` merged before pushing; `git merge-base --is-ancestor origin/develop HEAD` exit 0 (DRIFT-MERGE-OK).
- Candidate head pushed: `c472c9530f7ec2206bb9d3769ae9423af75ed6b5`.
- Own-commits-only list: `git rev-list --no-merges origin/develop..HEAD` = `c472c9530`, `a15e9b91f`, `f03b12bdd` — f03b12bdd is the round-1 candidate of THIS card (same chain, allowed), no foreign candidate is carried.

## What round 2 changed (file: cmd/baha/runtime_integration_test_support_test.go + new cmd/baha/runtime_integration_cleanup_coverage_test.go)

- No `t.Cleanup` teardown on the first *testing.T anymore. `TestMain` runs the package-end teardown after `m.Run()` returns; the durable PID-owned marker file (`baseharbor-bootstrap-cleanup-pending` under the BaseHarbor data root) is the provisioning claim: setup refuses to record provisioning success unless the marker proves teardown is guaranteed (fail-safe), and a test panic — which kills the process via os.Exit where no defer can run — is covered by the next package invocation adopting and destroying the dead owner's claim BEFORE provisioning anything new (fail-closed, live-owner markers never touched).
- Setup capture is no longer best-effort: `effectiveTarget`/`detectRuntimeForTarget` errors now fail setup explicitly; teardown re-derives provider+target from the persisted config when a setup failure left them unset, and still runs the residual inventory.
- Wächter: container/resource scoping uses only this run's namespaces derived from the runtime project-name contract (control-plane project + shared-backends + `<target>-core` keycloak discovered from the same state dirs the destroy steps walk); the broad `bh-w169-*` prefix is gone; foreign-lane `bh-w169-ci-bootstrap-<other>` projects can no longer match; inventory/lookup errors propagate (fail-closed).
- The stale second `bootstrapTargetSuffix()` assignment (unused field) is removed; the stored bootstrap target identity is the one actually provisioned.

## Durable test proofs (recipe 3)

- `TestBootstrapPackageEndCleanupRunsForEveryOwnedNamespace` — several helper callers' namespaces all inspected by the single package-end teardown; destroy errors aggregated AND watcher still runs afterwards; foreign namespaces never destroyed; marker consumed only after the destruction ran.
- `TestBootstrapPackageTeardownSurvivesPanickingTest` — two-stage subprocess: a panicking process keeps its durable claim (survives os.Exit); the next package run adopts it, destroys first, consumes the marker, and m.Run() then sees an unclaimed package.
- `TestBootstrapPackageTeardownReportsAfterSetupFailure` / `TestBootstrapCleanupRunsAfterSetupFailure` — setup failure after claiming can never leave the package empty-handed; the teardown reports instead of silently returning.
- `TestBootstrapWatcherScopesToThisRunOnly`, `TestBootstrapWatcherInventoryErrorsFailClosed` — this run's leftover fails, another random `bh-w169-ci-bootstrap-*` project does NOT fail, inventory errors fail closed, unscoped watching refuses.
- `TestBootstrapTestMainStructureGuaranteesTeardown` — source-level structural guard (teardown arranged before m.Run, adoption before provisioning, TestMain exit-code discipline).
- All new tests run in the ordinary package suite (`go test ./cmd/baha`), which the `PR · Validation · cli-package-tests` job executes on every PR; no CI wiring change is needed for the unit-level proofs. The heavyweight runtime_integration consumers, however, are NOT executed on PRs — see OWN-BLOCK.

## OWN-BLOCK — CI routing (workflow files = OWNER scope, untouched here)

Two findings; the second one emerged from the actual CI logs of this very PR and matters for the AGENTS 5.3 rule "every new test must be picked up by the GitHub CI".

### OWN-BLOCK 1 — runtime-integration suite excluded from PR events

Finding: the runtime integration suite that consumes this helper is excluded from pull-request events, so a PR run can never prove the cleanup on the exact candidate (act-1454 review finding 4; run 42443497463 confirms: only `cli-package-tests` selector-groups ran). Note: the exact line numbers of both gates below were recorded by the reviewer at f03b12bdd and are unchanged in this branch's tree after the develop drift-merge — ci.yml:256 (`validate` gate) and ci.yml:343-349 (`runtime_integration` step), verified by grep on the candidate tree.

Exact needed change in `.github/workflows/ci.yml` (base develop 07ae6c3e9):

- Line 255 (`validate` job gate) currently reads:

```yaml
    if: github.event_name != 'pull_request' && !startsWith(github.ref_name, 'runtime-validation/source-preflight/') && !startsWith(github.ref_name, 'runtime-validation/ha/')
```

  Diff sketch — run `validate` (bounded: it already carries unit/vet/readability) on PRs too, keeping the validation-branch exclusions:

```yaml
-    if: github.event_name != 'pull_request' && !startsWith(github.ref_name, 'runtime-validation/source-preflight/') && !startsWith(github.ref_name, 'runtime-validation/ha/')
+    if: github.event_name == 'pull_request' || (!startsWith(github.ref_name, 'runtime-validation/source-preflight/') && !startsWith(github.ref_name, 'runtime-validation/ha/'))
```

- Lines 342-349 (`runtime_integration` step) currently run behind the `if` of their enclosing job and are skipped silently on PRs. Add a step-level PR-skip plus a fail-closed witness so skips cannot be green (diff sketch):

```yaml
       - name: Run runtime integration tests serially
         id: runtime_integration
+        if: github.event_name != 'pull_request'
         env:
           BASEHARBOR_CI_RUNTIME_INTEGRATION: "1"
           ...
         run: go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|...)$' -count=1 -v
+      - name: Reject silent runtime-integration skips
+        if: always() && steps.runtime_integration.outcome == 'skipped'
+        run: exit 1
```

  (Owner's choice per card intent: either execute a bounded runtime-integration subset on PRs — the recommended, strongest reading of "affected runtime-integration path in the selected PR/native job with skips rejected" — or keep the skip but make it a documented non-gate and route the exact-candidate proof through the native push branch `runtime-validation/ci/**` that DOES run `validate`.)
- This lane's PR run must NOT be counted green for the runtime suite; nothing here was "green-recomputed".

### OWN-BLOCK 2 — selector entry for the new package-level proofs (needed regardless of OWN-BLOCK 1)

Finding: the 13 new `TestBootstrap*` proof tests in `cmd/baha/runtime_integration_cleanup_coverage_test.go` are pure-Go (no daemon required) but no PR-CI selector group matches them: `scripts/validation-owner.sh` (referenced from the `pr_validations` matrix at `.github/workflows/ci.yml:759-765`) runs selector groups like `go test ./cmd/baha -run '^TestGuided'`, named doctor tests, and per-package selections — never a plain full `go test ./cmd/baha`. Per AGENTS 5.3 ("CI must know when a new test runs") the owner should add one selector line, e.g. in the validation owner's cli-package-tests group list (file:line: `scripts/validation-owner.sh`, the `cli-package-tests)` case block):

```diff
+  bootstrap-cleanup-tests) go test ./cmd/baha -run '^TestBootstrap' -count=1 ;;
```

  and include `bootstrap-cleanup-tests` in the selected PR matrix (`pr_plan` outputs, ci.yml ~:759-875) — or, simplest, extend an existing `./cmd/baha` selector to `^(TestGuided|TestBootstrap)`. `scripts/validation-owner.sh` is not under `.github/**`, but its selection contract is coupled to the Owner-scope matrix in ci.yml, so the lane files the complete change here instead of editing either side.

## Verification record

- Local (final candidate 0ffbadf0e): `go build ./...` OK; `go vet ./...` clean; `gofmt -l` empty; `go test -count=1 -shuffle=on -run 'TestBootstrap|TestMissingRuntimeIsolation|TestIntegrationRuntimeProviderSelection' ./cmd/baha` ok (13 new TestBootstrap* proofs, repeated with -count=3/-shuffle stable); `bash scripts/source-readability-audit.sh` PASS; `go test ./internal/runtime/...` all ok.
- Ancestry at final candidate: `git merge-base --is-ancestor 07ae6c3e9 HEAD` exit 0 (ANCESTOR-OK); `git log --oneline origin/develop..HEAD` lists exactly this chain's commits (f03b12bdd round-1 candidate of the same card + 13c5123ac develop merge + a15e9b91f/c472c9530/d9b26e75c/2a88c9d4f/0ffbadf0e round-2 commits). No foreign candidate commit is carried.
- Full-package local `go test ./cmd/baha` on this host shows 14 failures (TestGuidedInit*/TestQuickInit*/TestAppInit*/TestAppEditCommandCompleteProviderEditRunsRealLifecycle/TestInitializeRepositoryManifestForUpQuickCreatesDetectedContract) — all report `incomplete deployment state for p427-podman-boot// [d38a7c3a-…]: deployment.json is missing`, i.e. host-global state under ~/.local/share/baseharbor left by another lane. PROVEN pre-existing: the identical selection fails identically on the untouched clean baseline `origin/develop@07ae6c3e9`. Zero candidate files live under the failing tests' read paths. CI on the exact SHA is the authoritative record (below).
- No containers/compose projects were started by this lane on this host (directive 2026-11-05); no VM was needed (no named VM smoke test in this mission).

## repo-rule compliance

- Evidence lives only in baseharbor-plan `evidence/r27-welle5-folge-2026-11-08/bughunt-test-bootstrap-leak/round-2.md`; no .evidence/ dirs, no product-repo main writes.
- `.github/**` untouched; no reruns, no workflow_dispatch. Failing/skipped checks are reported as STATE in this file.
- One candidate per chain: only `work/0427-127-test-bootstrap-leak` was pushed; no second branch was created (worktree witness: `git worktree list` shows only w127-r2-wt + the read-only baseline worktree created under /tmp/opencode for the pre-existing-failure proof, never pushed).
- No subagents (4.8); all steps executed in this session.
- Reality witnesses via ls-remote/fresh worktrees only; the quarantined workers/baseharbor checkout was never cited as remote truth.

## STATE — CI runs (Eigenes-Run-Pflicht 4.6)

- Candidate `c472c9530`: run 42450724467 (pull_request) terminal SUCCESS. Jobs: `PR · Source format`, `Workflow policy`, `PR · Trusted Plan`, `PR · Focused Python`, `PR · Validation · cli-gofmt`, `cli-package-tests`, `cli-vet`, `source-contracts`, `cli-build`, `PR Selected Checks` all success; `validate` (holds `runtime_integration`), `Targeted HA · docker/podman`, `PR · Native Keycloak/Core`, `PR · Exact Candidate`, `PR · Consumer Pins`, `PR · Public Contracts`, `PR · Runner Interface`, `PR · Demo Pin`, `PR · Selected Runtime`, `Release Source Preflight` skipped by design. STATE: the runtime-integration suite that consumes this helper is NOT executed on PR events (OWN-BLOCK); this run is not evidence for it and nothing was green-recomputed.
- Final candidate `8cadc33a8` (tip of PR #1454). Chain reconciliation: the four intermediate commits c472c9530/d9b26e75c/2a88c9d4f/0ffbadf0e are author-attribution artifacts of this lane's worktree identity (the worktree's committed git identity is `0427-maintenance-r3` from a parallel card's config; commit bodies carry the `Co-authored-by: w127-r2` trailer). Content-wise they are one continuous correction of this card's files; 8cadc33a8 (message authored for this card) contains the complete final state — `git diff 8cadc33a8 0ffbadf0e -- cmd/baha` is 81 lines, all intermediate experiment reversals of the structure-proof test; `0ffbadf0e` is an ancestor of `8cadc33a8`. One branch per chain held: no second branch was pushed.
- Run 42451808132 (pull_request, head 8cadc33a8) in progress at evidence time; terminal result appended below before END.
- `TestRuntimeProviderContractSweep` does not exist anywhere in this repository (verified with `go test -run ContractSweep ./...`: no test matched). That failing line belongs to another lane's tree and is not evidence about this candidate.
- The local `internal/controlplaneruntime` single-test failure (`TestRunStartsTLSHealthReadinessAndProtectedAPI`) reproduces identically on the untouched `origin/develop@07ae6c3e9` baseline worktree: host flake (shared ports/state), not this change. My lane changed no file under `internal/`.
