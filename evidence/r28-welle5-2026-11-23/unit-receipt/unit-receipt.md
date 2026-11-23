# unit-receipt for #1725 shared_backends_test.go TestSharedBackendState*

## PLAN
1. plan.py claim (central, push).
2. QUELLENSTUDIUM read-only: which trusted-base loader (ci.yml) + planner determine the unit-shard selection.
3. MINIMAL scripts-only fix: correct the mapping so deltas on shared_backends*.go pull the unit tests.
4. regression if the loader has a test script.
5. EIN PR (develop base, ls-remote), EIN pull_request-run terminal: exec-receipt = the four test names named in the hosted log + UNIT_SCOPE != none. No merge.
6. Akte evidence/r28-welle5-2026-11-23/unit-receipt/.

## BASE ATTESTATION
- develop: git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop = b517b279c9533669c104dc6429c0a1934c508716
- Remote guard: git remote -v shows https://github.com/mcpdev80/baseharbor.git; all reads via that URL.
- Card: t-20261123-shared-backends-unit-receipt. First free seat.
- #1725 hop head: 3f334347580f1fcbf14182bfc521ec688a0b55b2.

## QUELLENSTUDIUM (read-only)
- Unit-shard selection is decided in ci.yml `unit_split` step (Run only required Go tests into mandatory parallel shards): unit_scope = 'full' only if 'go-unit-tests' in requested_validation_checks; else 'cli' if 'cli-package-tests'; else 'none'.
- go-unit-tests = {'id':'go-unit-tests','command':'go test ./... -count=1'} (CONSERVATIVE_CHECKS, pr-gate-plan.py:1727). CI_CHECKS does NOT include go-unit-tests.
- source-contracts = {'id':'source-contracts','command':'go test ./internal/application/... ./contracts/...'} (CODE_CHECKS, pr-gate-plan.py:69-72). ci.yml:1311-1312 runs it.
- shared_backends*.go already has an explicit handler in pr-gate-plan.py:1461 (unchanged on develop): `elif path.startswith('internal/application/shared_backends')` -> area='application-shared-provider-resolution'; require(CODE_CHECKS); selected.add('atomic/podman/lifecycle').
- require(CODE_CHECKS) adds source-contracts to required_validation_checks. So the four TestSharedBackendState* run via 'go test ./internal/application/...' in the PR · Validation · source-contracts job.

## FINDING: exec-receipt already exists (durable)
- Run 45136441345 (PR #1725 hop 3f33434758): PR · Validation · source-contracts job 137563847502 ran 'go test ./internal/application/... ./contracts/...' -> 'ok github.com/mcpdev80/baseharbor/internal/application 4.572s' (log 2026-11-23T08:11:11.8642681Z).
- The four TestSharedBackendState* PASS locally (named form):
  TestSharedBackendStateVersionMismatchNamesVersions PASS
  TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption PASS
  TestSharedBackendStateLoadReportsVersionReason PASS
  TestSharedBackendStateCorrectVersionStillLoads PASS
- The handler is identical between develop and the current branch (diff only a comment-line offset).

## OWNER/COORDINATOR ENTSCHEID (2026-11-23, coordinator via 9142ab1f)
- Decision: Option (1). The four tests ARE executed (package `go test ./internal/application` in source-contracts, job 137563847502, run 45136441345 'ok ... 4.572s'). The reviewer-verdict coverage gap is a RECEIPT-SICHTBARKEITSproblem (visibility), not a deckungsproblem (coverage).
- Option (2) planner-edit (unit_scope=full, broad `go test ./...`) ABGELEHNT — violates kleinsten ausreichenden diff; pr-gate-plan.py is a shared base planner file.
- No code change needed. Card closed with the witnesses below.

## EVIDENCE (durable exec-receipt)
- Route (pr-gate-plan.py:1461, text): `elif path.startswith('internal/application/shared_backends') or path.startswith('internal/application/shared_backend_dependency') or 'shared_backend' in path and path.endswith('.go'):` -> area='application-shared-provider-resolution'; `require(CODE_CHECKS)`; `selected.add('atomic/podman/lifecycle')`. `CODE_CHECKS` = `{'id':'source-contracts','command':'go test ./internal/application/... ./contracts/...'}` (pr-gate-plan.py:69-72). ci.yml:1311-1312 runs source-contracts.
- Exact package receipt: run 45136441345, job 137563847502 ('PR · Validation · source-contracts', success), log line 2026-11-23T08:11:11.8642681Z: `ok  	github.com/mcpdev80/baseharbor/internal/application	4.572s`.
- The four are named within that package at these definitions in internal/application/shared_backends_test.go:
  - line 286: TestSharedBackendStateVersionMismatchNamesVersions
  - line 316: TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption
  - line 337: TestSharedBackendStateLoadReportsVersionReason
  - line 367: TestSharedBackendStateCorrectVersionStillLoads
- Local named verification (named form per test runner rule): `go test ./internal/application/ -run 'TestSharedBackendState(VersionMismatchNamesVersions|VersionMismatchIsDistinguishableFromCorruption|LoadReportsVersionReason|CorrectVersionStillLoads)' -v` -> four PASS, `ok .../internal/application 0.005s`.

## OPTIONAL NULL-CHANGE (offered, not required)
- None required. A `-v` on the source-contracts command would make the four names visible in that log, but that is a `.github`/workflow edit (Owner scope) and is not required by the contract.

## WITNESSES
- pr-gate-plan.py:1461 handler (diff vs develop: comment only)
- Run 45136441345 job 137563847502 log: 'ok .../internal/application 4.572s'
- Local: go test ./internal/application/ -run 'TestSharedBackendState(...)' -v -> four PASS

## CLEANLINESS
- docker ps -a pre: empty
- docker ps -a post: empty (no containers started; read-only source study + named go test only)

END_DONE w078-pr1650-0428-078-reloc: #1725 unit-receipt DONE (no code change). Durable exec-receipt: four TestSharedBackendState* execute in source-contracts job 137563847502 (run 45136441345, 'ok .../internal/application 4.572s'); named at shared_backends_test.go:286/316/337/367. Coordinator decided Option 1 (coverage exists; only visibility gap). No .github, no consent, no merge.
