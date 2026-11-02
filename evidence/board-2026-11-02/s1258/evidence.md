# s1258 R2 Evidence — Rebase PR #1258 onto develop 9a93865a + qualify

## PLAN

1. [DONE] REBASE branch work/gh-hosted-sweep (735acd95) onto develop 9a93865a, resolve conflicts in-content (preserve hosted migration + all native tests/Required Checks, no gate-weakening) -> head 8c323acd, 13 commits, 0 self-hosted, build OK
2. [DONE] Push via git push --force-with-lease + ls-remote Gegencheck (remote now 8c323acd)
3. [DONE] VERIFY: git grep -nE 'runs-on:.*self-hosted' -- .github/workflows = 0 in all workflows; list runs-on per workflow as hosted proof
4. [DONE] QUALIFY: CI Source & Quality + actionlint + affected native gates on new rebase SHA (run 41464906073)
5. [DONE] Watch all dispatched hosted runs to terminal color (Run-IDs); PR Selected Checks blocked-on-1286-A (coverage-unresolved) -> END_CODE_READY, NOT bypassed

## repo-rule compliance

- Write-set respected: ONLY rebase of #1258 branch work/gh-hosted-sweep onto develop. No product edits, no pr-gate-plan.py/Register, no receipt_verifier, no #1273. No force on develop/main. NO MERGE by me.
- No gate-weakening: all 13 #1258 commits preserved verbatim; all native tests pass locally; all Required Checks green.
- Rebase was clean (no conflicts): develop 9a93865a already contained the shared_backends + podman_doctor_checks.go fixes that resolve the earlier native test regressions.

## REBASE

- Source: work/gh-hosted-sweep @ 735acd95, target: develop 9a93865a
- rebased head: **8c323acd23977f48bb930efa3b1bd6f01dd5dd73** (13 commits, clean rebase, no conflicts)
- build: `go build ./...` OK
- native tests (were failing pre-rebase) now PASS on merged tree:
  - `go test ./cmd/baha/ -run 'TestMCPAuthoringAssignsCanonicalIdentityWithoutClientID|TestAppEditCommandIncompleteSQLConsumerRemainsPartial|TestMCPGenericClientRealApplicationLifecycle'` -> ok 7.4s
- push: `git push --force-with-lease origin work/gh-hosted-sweep` -> + 735acd95...8c323acd
- ls-remote Gegencheck (§6.5): `git ls-remote https://github.com/mcpdev80/baseharbor work/gh-hosted-sweep` -> 8c323acd23977f48bb930efa3b1bd6f01dd5dd73 ; gh API `.head.sha` -> 8c323acd (confirmed)

## VERIFY — self-hosted=0 in all 7 workflows (hosted proof)

`git grep -nE 'runs-on:.*self-hosted' -- .github/workflows` -> exit=1 (0 matches)

runs-on per workflow @ 8c323acd:
- ci.yml: ubuntu-latest x13, ubuntu-26.04 x1  (all hosted)
- mcp-lifecycle-acceptance.yml: ubuntu-26.04 x1, ubuntu-latest x1
- nextjs-greenfield-e2e.yml: ubuntu-latest x1
- observability-acceptance.yml: ubuntu-26.04 x1, ubuntu-latest x1
- podman-acceptance.yml: ubuntu-26.04 x1
- runtime-broker.yml: ubuntu-latest x2
- runtime-s3-acceptance.yml: ubuntu-latest x1

## QUALIFY — run 41464906073 (rebase SHA 8c323acd)

Individual Required Checks (all terminal, all GREEN):
- Workflow policy: success
- PR · Trusted Plan: success
- PR · Exact Candidate: success
- PR · Runner Interface: success
- PR · Validation · source-contracts: success
- PR · Validation · cli-gofmt: success
- PR · Focused Python: success
- PR · Validation · pr-planner-tests: success
- PR · Validation · receipt-execution-tests: success
- PR · Validation · cli-build: success
- PR · Validation · cli-guided-tests: success
- PR · Validation · cli-vet: success
- PR · Validation · ci-policy: success
- PR · Validation · ci-executor-verifier-tests: success
- PR · Validation · ci-actionlint: success
- PR · Validation · wizard-app-edit-tests: success
- PR · Selected Runtime (docker / lifecycle): success  (native docker gate green)
- PR · Selected Runtime (podman / lifecycle): success  (native podman gate green)

## ci.yml Bootstrap Block — blocked-on-1286-PR-A (NOT bypassed, documented per mission)

- Gate: **PR Selected Checks** -> FAIL (exit 1). All underlying jobs pass.
- Exact classifier output (job 125346481687, run 41464906073):
  `BLOCKED: coverage-unresolved: workflow execution/cleanup/evidence impact requires native qualification: .github/workflows/ci.yml; ...; CLI execution/evidence impact requires specific qualification: scripts/ci-core-rootless-runtime.sh`
- Root cause: the develop classifier (same bootstrap as #1286 PR-A) reports coverage unresolved for the 7 changed workflows + scripts/ci-core-rootless-runtime.sh because they need native qualification that is gated behind #1286. This is the known boundary the mission named.
- Per mission: NOT bypassed, NOT edited. ci.yml and all workflows untouched.
- Resolution path (Owner/Coordinator): #1286 PR-A qualifies the ci.yml classifier bootstrap; then integrate #1258 in correct order.

## END_CODE_READY

Rebase complete and verified (8c323acd, 0 self-hosted, all native tests pass). All individual Required Checks + native docker/podman lifecycle gates green on the new SHA. PR Selected Checks blocked-on-1286-A (ci.yml coverage-unresolved, file: line = the classifier block in job 125346481687). No product changes made; no merge done. Ready for controlled integration by the Coordinator.
