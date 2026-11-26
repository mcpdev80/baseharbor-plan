# 0428-065 export - rebase PR #1625 onto current develop

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). PR: #1625 (branch, base develop, DRAFT=true, head 010db47dae0).

## PLAN

1. Measure: git ls-remote develop + PR#1625 head; confirm develop newer; fetch both refs; git merge-base --is-ancestor develop head = NO. Record both lines verbatim in this file.
2. Resolve: rebase onto measured develop; resolve conflicts in cmd/baha/app_export*.go per contract. Develop-side auth/consent/fail-closed semantics win; no weakening, no consent-fading, no test-tweaking to go green. STOP + file:line on any write-set-tabu file.
3. Prove + run: merge-base --is-ancestor develop head = YES; rev-list --count head..develop = 0; git log -1 --format=%P = develop-sha; diff --name-only develop...head = exactly the write-set; git log --format=%an develop..head = exactly one identity; gh pr ready 1625; hosted run to terminal; report per-job conclusions; red REQUIRED that was green on old head = STOP + job-id + file:line.

## repo-rule compliance

- Single integration candidate: working on branch named in mission (#1625).
- Write-set respected: cmd/baha/app_export*/app_data*. Tabu untouched: internal/identityprovider/**, internal/serviceaccess/**, internal/operatorauth/**, internal/capability/perses_selection.go, internal/observability/registry.go, .github/**, scripts/**.
- Identity: dedicated worktree 0428-065-export-wt, git config user.name "0428-065-export" / user.email "0428-065@baseharbor.local".
- No subagents (4.8): all steps executed in this session.
- No git stash, no git add -A, no bare go test ./...

## cleanliness

- docker ps -a --filter name=bh- before: (none started this shift)
- docker ps -a --filter name=bh- after: (none started this shift)
- git worktree list after: 0428-065-export-wt (detached HEAD e6c199e7b, 2 feature commits on top)

---

## STEP 1 - MEASUREMENT (verbatim, as required)

git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop:
e6c199e7b7dd7d076a776d11c3ba16f25e59c254  refs/heads/develop

git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1625/head:
010db47dae0e0425f948914b3febc1ba86f41edc  refs/pull/1625/head

git merge-base --is-ancestor develop 010db47dae0e0425f948914b3febc1ba86f41edc => exit=1 (NO) -- PR #1625 head is out of date on develop (CONFLICTING, confirmed).

BASE ATTESTATION (SHA cut from): e6c199e7b7dd7d076a776d11c3ba16f25e59c254 (current develop head).

## STEP 2 - REBASE / CONFLICT RESOLUTION (in progress, then STOP)

Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/0428-065-export-wt (fresh, identity set).

Commits applied by cherry-pick:
- fbe703668 feat(0428-065): guided baha app export -- CONFLICT in cmd/baha/machine_coverage.go resolved.
- 010db47da fix app export managed secret selection and reveal -- no conflict.

Both commits landed on top of develop e6c199e7b. machine_coverage.go conflict resolved develop-side (authoritative): kept develop's richer cliPresentationCommands descriptions incl. the baha context command group; added exactly one "baha app export" line after the "baha app secure-profile export" line. gofmt-clean. Confirmed via diff against PR head that my resolution differs only by the develop-only context group (expected -- that group was added to develop after the PR was cut).

local_workload_authority.go in my worktree is byte-identical to develop (authoritative), confirming the rebase correctly took the develop side for the operator-path.

## STEP 3 - PROOF / TEST RUN: STOP

Build: go build -o ./baha-bin ./cmd/baha => exit 0 (57 MB binary).

Export test results on the new head (new develop base):
- TestAppExportCommandProducesCommand PASS
- TestAppExportManagedSecretsAuthorizedSelectionProducesEncryptedEntry PASS (uses a verified principal)
- TestAppExportManagedSecretBackendErrorsAreRedacted PASS (sub-checks)
- TestSecureProfileExport* all PASS
- FAIL (3):
  - TestAppExportCommandPathAssemblesProductionWiring -- "operator authentication needs interactive setup but input is not a terminal"
  - TestAppExportFailsClosedWithoutSelection -- same
  - TestAppExportManagedSecretWithoutOperatorFailsClosed -- same

### ROOT-CAUSE OF THE STOP (measured, not inferred)

- On the PR head's OWN tree (feature developed+tested there), these 3 tests PASS: go test -run 'TestAppExportFailsClosedWithoutSelection|TestAppExportCommandPathAssemblesProductionWiring|TestAppExportManagedSecretWithoutOperatorFailsClosed' => ok.
- On my rebase onto develop, they FAIL with "operator authentication needs interactive setup but input is not a terminal".
- The only develop-side change that breaks them is cmd/baha/local_workload_authority.go (the local-workload-authority verification path). Diff base 8963efd8a vs develop:
  - base form: authority := operatorauth.LocalRuntimeAuthority{}; returns via operatorauth.WithoutLocalRuntimeAuthority(withLocalInvocation(ctx, "")); local authority granted read-only and invocation-local with NO verified-runtime-engine requirement.
  - develop form: operatorauth.LocalOperationGrant; computes deployment.EnvironmentID(target, env) and calls operatorauth.CheckLocalRuntimeGrant(operationContract, environmentID, applicationID, check) where check runs validateTargetDockerBinding + provider.VerifyLocalRuntimeAuthority (podman) or a verified docker-engine check (localRuntimeEngine, requires engine.Verified && engine.DaemonID != "" && strings.HasPrefix(engine.Endpoint, "unix:///") and rootless/rootful mode).
- Empirical: verifiedLocalWorkloadAuthority(ctx, "app-export-ci", "dev") on the export test fixture returns (local=false, err=nil) -- the fixture target has provider docker but NO real daemon, so localRuntimeEngine is false, so local=false, so ensureOperatorAuthForBoundary (cmd/baha/operator_auth_boundary.go:67) proceeds past the local shortcut to the interactive-terminal branch (:117).
- The 3 failing tests rely on the local-workload-authority shortcut (no verified operator principal) to fail closed. That shortcut now requires a verified local runtime engine (develop #1717, internal/operatorauth/local_runtime.go CheckLocalRuntimeGrant). The feature itself is not broken for real users (verified daemon + dev env passes); only the no-daemon test fixtures trip the stricter contract.

### WHY THIS IS A STOP (mission rule, 0428-065 step 2)

- The blocker is the develop-side operator-auth verification contract (local_workload_authority.go / internal/operatorauth/**) -- AUTHORITATIVE develop-side contribution. The mission forbids weakening any berechtigung / consent / fail-closed-semantik. local_workload_authority.go is OUTSIDE the card's write-set (cmd/baha/app_export*/app_data*, machine_coverage.go).
- The mission forbids "keinen test 'anpassen', damit er gruen wird". The 3 failing tests encode the "without a verified operator, export fails closed" contract; changing their expectation or fixture to go green would weaken the fail-closed check or mask the develop-side contract change.
- The correct fix (carry the export feature's local-authority expectation into the new CheckLocalRuntimeGrant contract) is a develop-side operator-auth / identity-path change, which the mission routes to a separate card or to the owner -- NOT a self-help edit here.

### STOP DELIVERABLE

- file:line: the blocking contract change is cmd/baha/local_workload_authority.go:117-143 (develop CheckLocalRuntimeGrant + verified-runtime requirement) as reached via cmd/baha/operator_auth_boundary.go:56,62-67.
- The rebase is otherwise complete and correct; the only open item is this develop-side operator-auth contract incompatibility with the feature's no-daemon local-authority tests.

---

END_BLOCKED pr1625-0428-065-export: rebase to develop complete; develop-side operatorauth CheckLocalRuntimeGrant contract (cmd/baha/local_workload_authority.go:117-143 via operator_auth_boundary.go:56,62-67) makes the feature's 3 no-daemon local-authority tests fail; STOP per mission step 2 (no auth weakening, file outside write-set). Base: e6c199e7b7dd7d076a776d11c3ba16f25e59c254. Evidence: baseharbor-plan/evidence/r28-welle4-20261114/0428-065/round-rebase-1615.md (commit acfb8cd5b, unpushed).
