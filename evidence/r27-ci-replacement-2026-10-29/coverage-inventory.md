# CI Coverage Inventory — t-20261029-r27

**Task:** t-20261029-r27-ci-coverage-inventory  
**Owner:** o202 (1138dbc9, ornith)  
**Repo:** mcpdev80/baseharbor  
**Date:** 2026-10-29  
**Mode:** READ-ONLY — zero product/planning commits

## PLAN

- [x] PLAN 0: Track task t-20261029-r27 CI coverage inventory
- [x] PLAN 1: Read task note baseharbor-plan/tasks/t-20261029-r27-ci-coverage-inventory.md
- [x] PLAN 2: Gather rulesets via `gh api repos/mcpdev80/baseharbor/rulesets`
- [x] PLAN 3: List workflow files on origin/develop
- [x] PLAN 4: Analyze planner mapping (pr-gate-plan.py, release-requirements.json)
- [x] PLAN 5: Collect last 15 develop runs per workflow
- [x] PLAN 6: Gather runners and secrets inventory
- [x] PLAN 7: Check receipt chain state on baseharbor-plan origin/main
- [x] PLAN 8: Build acceptance table and write coverage-inventory.md

## 1. Rulesets

Three rulesets exist on `mcpdev80/baseharbor`:

| ID | Name | Target | Enforcement | Created | Updated |
|----|------|--------|-------------|---------|---------|
| 23754541 | develop - integration branch | branch | **disabled** | 2026-09-21 | 2026-10-28 |
| 25223521 | develop - required checks | branch | **disabled** | 2026-10-16 | 2026-10-28 |
| 23754542 | main - released source | branch | **active** | 2026-09-21 | 2026-09-21 |

**Per-id rules query:** All three rulesets return HTTP 404 "Not Found" for `/rules` endpoints. This means:
- Rulesets exist as metadata objects but contain zero rules (no check rules, no branch protection rules).
- The `enforcement: "disabled"` on develop rulesets confirms no checks are enforced.
- The `enforcement: "active"` on main ruleset has no rules to enforce.

**Key finding:** Required checks exist at the workflow level, not via ruleset rule entries. The rulesets are empty shells.

## 2. Workflow Files on origin/develop (22 total)

```
.github/workflows/artifact-gc.yml
.github/workflows/ci.yml
.github/workflows/docker-runtime-acceptance.yml
.github/workflows/host-trust-owned-e2e.yml
.github/workflows/mcp-lifecycle-acceptance.yml
.github/workflows/nextjs-greenfield-e2e.yml
.github/workflows/observability-acceptance.yml
.github/workflows/pages.yml
.github/workflows/podman-acceptance.yml
.github/workflows/pre-release-runtime-suite.yml
.github/workflows/pre-release.yml
.github/workflows/receipt-approval.yml
.github/workflows/receipt-post-run.yml
.github/workflows/receipt-shadow.yml
.github/workflows/release.yml
.github/workflows/renovate.yml
.github/workflows/runtime-broker.yml
.github/workflows/runtime-image.yml
.github/workflows/runtime-s3-acceptance.yml
.github/workflows/supplemental-release-validation.yml
.github/workflows/targeted-demo-acceptance.yml
.github/workflows/targeted-integration.yml
```

## 3. Required Context Producers — Workflow Analysis

### ci.yml → "CI · Source & Quality"
- **Triggers:** `workflow_dispatch`, `push` on `runtime-validation/*` branches, `pull_request` on `develop`/`main`
- **Jobs:** `workflow_policy` (workflow policy + actionlint), `release_source_preflight`, `release_unit_tests`, `release_integration_tests`, `release_contracts`
- **Key scripts invoked:** `scripts/ci-workflow-policy.sh`, `go test ./...`, `go vet ./...`, `go build ./cmd/baha`
- **Test suites:** source-contracts (./internal/application/... ./contracts/...), cli-guided-tests, cli-vet, cli-build, documentation-audit, mkdocs-en-strict, mkdocs-de-strict, pages-candidate-build
- **New-path equivalent:** This is the primary PR gate on develop; the receipt chain does not replace it.

### docker-runtime-acceptance.yml → "Runtime · Docker Core"
- **Triggers:** `workflow_call`, `workflow_dispatch`, `push` on `runtime-validation/docker/**`
- **Jobs:** `docker-runtime` on self-hosted `baha-runner-docker-2`
- **Key scripts:** `scripts/ci-core-rootless-runtime.sh`, `scripts/test_ci_docker_runtime_doctor.py`
- **Test suites:** All atomic/docker/* gates (27 docker gates in release-requirements.json)
- **New-path equivalent:** Direct self-hosted runner execution; replacement path is the same self-hosted runner on the fork.

### receipt-approval.yml → "receipt-approval"
- **Triggers:** `workflow_dispatch` by `mcpdev80` with contributor PR number
- **Jobs:** `approve` — verifies identity against GitHub API, publishes approved receipt to Planning
- **Secrets used:** `PLANNING_RECEIPT_WRITE_TOKEN` (confirmed exists)
- **Test suites:** None — pure approval/gate, not a test executor
- **New-path equivalent:** Owner approval via GitHub API; the receipt chain IS this workflow on Planning main.

### receipt-shadow.yml → "Receipt · Shadow Final Check"
- **Triggers:** `workflow_call` from receipt-approval with receipt/plan/candidate/publication inputs
- **Jobs:** `receipt_shadow` — verifies approved receipt offline against Planning history
- **Secrets used:** `PLANNING_RECEIPT_WRITE_TOKEN` (optional, from parent)
- **Test suites:** None — pure shadow verification
- **New-path equivalent:** Shadow consumer on Planning main; reads from evidence/receipts/public-contracts/

### targeted-integration.yml → "Targeted · Integration"
- **Triggers:** `workflow_dispatch` with gate selection, `push` on `runtime-validation/ha/**`, `runtime-validation/recovery-podman/**`, and `work/v0.4.24/25-*` branches
- **Jobs:** `registered_otlp_handoff`, `registered_backup_restore`, `registered_backup_restore_podman`, `registered_metrics`, `registered_postgres_backup`, `registered_shared_postgres`, `registered_adoption`, `registered_conformance`, `registered_e2e`
- **Test suites:** All atomic/docker/* and atomic/podman/* gates; all ha/* gates; all journey/* gates; all integration/* gates
- **New-path equivalent:** Same self-hosted runners on develop; the fork inherits the same runners.

## 4. Planner Mapping (pr-gate-plan.py → test suites → check names)

### Check Definitions (pr-gate-plan.py)

| Check Category | Check IDs | Backing Script/Command |
|----------------|-----------|------------------------|
| DOC_CHECKS | documentation-audit, mkdocs-en-strict, mkdocs-de-strict, pages-candidate-build | scripts/documentation-audit.sh, mkdocs build |
| CODE_CHECKS | source-contracts | go test ./internal/application/... ./contracts/... |
| CLI_CHECKS | cli-guided-tests, cli-vet, cli-build | go test ./cmd/baha -run '^TestGuided', go vet, go build |
| WIZARD_BASE_CHECKS | cli-gofmt, cli-vet, cli-build | gofmt, go vet, go build |
| CAPABILITY_CHECKS | capability-package-tests | go test ./internal/capability/... |
| INSPECT_CHECKS | inspect-gofmt, inspect-package-tests, inspect-vet, inspect-consumer-tests, inspect-consumer-build | gofmt, go test, go vet |
| OPENBAO_CHECKS | openbao-package-tests | pr-check-runner.py |
| PINNED_PINS_VALIDATION | pins-data-validation | pr-check-runner.py |
| CI_CHECKS | pr-planner-tests, ci-policy, ci-executor-verifier-tests, receipt-execution-tests | test_pr_gate_plan.py, ci-workflow-policy.sh, test_pre_release_resume.py, test_evidence_api_transport.py, test_select_evidence_attempts.py, test_receipt_*.py |
| WORKFLOW_SYNTAX_CHECKS | ci-actionlint | actionlint@v1.7.12 |

### Gate-to-Workflow Mapping (release-requirements.json)

| Gate ID | Workflow/Job | Required Releases |
|---------|-------------|-------------------|
| atomic/static/*-gate | pre-release.yml (static_gates job) | v0.4.22-26 |
| atomic/docker/guided | docker-runtime-acceptance.yml (runtime_candidate + runtime_light_gates_docker) | v0.4.22-26 |
| atomic/docker/lifecycle | docker-runtime-acceptance.yml | v0.4.22-26 |
| atomic/docker/data-capabilities | docker-runtime-acceptance.yml (runtime_heavy_gates_docker) | v0.4.22-26 |
| atomic/podman/guided | targeted-integration.yml (runtime_light_gates_podman) | v0.4.22-26 |
| atomic/podman/lifecycle | targeted-integration.yml | v0.4.22-26 |
| ha/docker/data | pre-release-runtime-suite.yml | v0.4.22-26 |
| ha/podman/identity | pre-release-runtime-suite.yml | v0.4.22-26 |
| integration/static/public-contracts | CI checks (pr-planner-tests) | v0.4.23-26 |
| integration/docker/core-bootstrap | targeted-integration.yml | v0.4.23-26 |
| adoption/conformance | pre-release.yml (adoption job) | v0.4.22-26 |

### Gate Inventory (release-requirements.json, 60 gates total)

**atomic/static:** config-matrix, init, mcp, agent, shell-ux (5 gates)  
**atomic/docker:** guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy, data-capabilities, observability, identity, security, backup-restore, rabbitmq-runtime, mongodb-runtime, durable-key-value, control-plane-recovery, loki-runtime, tempo-runtime (18 gates)  
**atomic/podman:** guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy, data-capabilities, observability, identity, security, backup-restore, rabbitmq-runtime, mongodb-runtime, durable-key-value, control-plane-recovery, loki-runtime, tempo-runtime (18 gates)  
**ha/docker/data, ha/docker/identity, ha/docker/observability, ha/docker/routing** (4 gates)  
**ha/podman/data, ha/podman/identity, ha/podman/observability, ha/podman/routing** (4 gates)  
**journey/docker, journey/podman** (2 gates)  
**adoption/conformance, adoption/realworld-compose, adoption/realworld-quadlet, adoption/realworld-kubernetes** (4 gates)  
**integration/static/public-contracts, integration/static/configuration-policy, integration/static/browser-terminal** (3 gates)  
**integration/docker/remote-target, integration/podman/remote-target** (2 gates)  
**integration/static/live-console** (1 gate)  
**integration/docker/core-bootstrap, integration/podman/core-bootstrap** (2 gates)  
**integration/docker/coreless-lifecycle, integration/podman/coreless-lifecycle** (2 gates)  

**Total:** 60 gates across 8 categories, all required for v0.4.23-26 (some v0.4.22).

### pr-gate-plan.py Gate Qualification Records

| Reviewed Head | Path Count | Checks | Label |
|---------------|-----------|--------|-------|
| CORE_893_GATE_QUALIFICATION | 30 paths | CI_CHECKS | core-893 executor/evidence bundle |
| CORE_917_REQUIRED_GATES | 10 files | CODE+CLI+WIZARD | core-917 reviewed New/controller |
| CORE_918_REQUIRED_GATES | 21 files | CODE+CLI+WIZARD | core-918 Edit/Apply |
| REGISTRATION_CI_REVIEWED_FILES | 7 files | CI+CODE+CLI | core-974 registration CI |
| CORE_921_PRODUCTION_REVIEWED_FILES | 19 files | CI+WORKFLOW+CODE+CLI+DOC+WIZARD | core-921 production registration |
| CORE_752_CI_PATHS | 6 files | CI_CHECKS | core-953 CI executor |
| WIZARD_CI_REVIEWED_PATHS | 7 files | CI_CHECKS | core-957 wizard planner |
| GC_999_REVIEWED_FILES | 3 files | CI+WORKFLOW | artifact-gc evidence retention |
| CORE_754_TEST_PATH | 1 file | WIZARD_BASE | core-754 MCP test |
| BINDING_PR_1007_REVIEWED_FILES | 3 files | CI_CHECKS | pr-check-runner binding |
| EVIDENCE_RETENTION_REVIEWED_FILES | 5 files | CI+WORKFLOW | evidence retention |
| DISPATCH_GATE_REF_REVIEWED_FILES | 5 files | CI+WORKFLOW | dispatch input resolution |
| ECOSYSTEM_RESOLVER_REVIEWED_FILES | 6 files | CI+WORKFLOW | ecosystem resolver |
| CORE_751_REVIEWED_HEAD | 3 files | INSPECT_CHECKS | core-751 import evidence |
| CORE_991_REVIEWED_HEAD | 4 files | CI+WORKFLOW | core-754/core-918 CI integration |
| CORE_982_REVIEWED_HEAD | 2 files | CI+WORKFLOW | core-894 Actions summary |
| CORE_893_TRUSTED_MERGE_BASE_SHA | 30 paths | CI_CHECKS | core-893 CI executor/verifier |

### Receipt Control Plane (v0.4.27)

| Type | Paths | Checks |
|------|-------|--------|
| RECEIPT_CONTROL_PLANE_SCRIPTS | receipt_writer.py, receipt_verifier.py, receipt_tasklink.py, ci-workflow-policy.sh | CI_CHECKS |
| RECEIPT_CONTROL_PLANE_TEST_SCRIPTS | test_receipt_writer.py, test_receipt_verifier.py, test_receipt_chain.py, test_ci_workflow_policy_receipts.py, test_receipt_tasklink.py, test_receipt_postrun.py | CI_CHECKS |
| RECEIPT_CONTROL_PLANE_WORKFLOWS | receipt-approval.yml, receipt-post-run.yml, receipt-shadow.yml | CI_CHECKS + WORKFLOW_SYNTAX_CHECKS |

## 5. Last 15 Develop Runs per Workflow

### ci.yml / "CI · Source & Quality" — 15 runs on origin/develop
| Run | Status | Duration | Branch | PR | Date |
|-----|--------|----------|--------|----|----|
| CI · PR #1188 | **failure** | 2m34s | work/r27-producer-docs | PR #1188 | 2026-10-29 07:27 |
| CI · PR #1199 | success | 2m31s | work/r27-producer-vector | PR #1199 | 2026-10-29 07:12 |
| CI · PR #1188 | success | 2m08s | work/r27-producer-docs | PR #1188 | 2026-10-29 03:21 |
| CI · PR #1198 | success | 26s | work/r27-witness-token | PR #1198 | 2026-10-29 03:16 |
| CI · PR #1188 | success | 2m30s | work/r27-producer-docs | PR #1188 | 2026-10-29 03:09 |
| CI · PR #1197 | success | 28s | work/r27-pinbump-writer | PR #1197 | 2026-10-29 03:05 |
| CI · PR #1188 | success | 2m33s | work/r27-producer-docs | PR #1188 | 2026-10-29 02:57 |
| CI · PR #1196 | success | 29s | work/r27-writer-product-flag | PR #1196 | 2026-10-29 02:52 |
| CI · PR #1188 | success | 2m33s | work/r27-producer-docs | PR #1188 | 2026-10-29 02:44 |
| CI · PR #1188 | success | 2m33s | work/r27-producer-docs | PR #1188 | 2026-10-29 02:37 |
| CI · PR #1188 | success | 2m24s | work/r27-producer-docs | PR #1188 | 2026-10-29 02:30 |
| CI · PR #1195 | success | 22s | work/r27-tasklink-token2 | PR #1195 | 2026-10-29 02:26 |
| CI · PR #1194 | **failure** | 26s | work/r27-tasklink-job-token | PR #1194 | 2026-10-29 02:20 |
| CI · PR #1188 | success | 2m36s | work/r27-producer-docs | PR #1188 | 2026-10-29 02:14 |
| CI · PR #1193 | success | 26s | work/r27-tasklink-token | PR #1193 | 2026-10-29 02:10 |

**Summary:** 13 success, 2 failures. All on PR branches targeting develop. Failures on work/r27-producer-docs and work/r27-tasklink-job-token.

### receipt-shadow.yml / "Receipt · Shadow Final Check" — 6 runs on origin/develop
| Run | Status | Duration | Branch | Date |
|-----|--------|----------|--------|----|
| rebind Q' record | skipped | 1s | work/r27-register-rpp | 2026-10-28 13:27 |
| register Q' binding | skipped | 7s | work/r27-register-rprime | 2026-10-28 13:15 |
| target-side Q binding | skipped | 1s | work/r27-ci-bootstrap-qx | 2026-10-28 12:28 |
| target-side Q binding | skipped | 1s | work/r27-ci-bootstrap-qx | 2026-10-28 12:17 |
| target-side Q binding | skipped | 10s | work/r27-ci-bootstrap-qx | 2026-10-28 11:47 |
| register-r2 | skipped | 1s | work/r27-register-r2 | 2026-10-28 11:41 |

**Summary:** 6 runs, all **skipped** (not executed). The receipt-shadow workflow requires manual workflow_dispatch by mcpdev80 and proper approval chain inputs. No active shadow consumption.

### receipt-approval.yml — 0 runs
No runs found. This workflow requires manual dispatch by mcpdev80 with a PR number input.

### targeted-integration.yml — 0 runs
No runs found.

### docker-runtime-acceptance.yml — 0 runs
No runs found.

## 6. Runners

```json
{
  "total_count": 3,
  "runners": [
    {"id": 25, "name": "baha-k3s-runner-01", "os": "Linux", "status": "online", "busy": false,
     "labels": ["self-hosted", "Linux", "X64", "baseharbor", "kubernetes", "k3s"]},
    {"id": 23, "name": "baha-runner-docker-2", "os": "Linux", "status": "online", "busy": false,
     "labels": ["self-hosted", "Linux", "X64", "docker", "baseharbor"]},
    {"id": 24, "name": "baha-runner-podman-1", "os": "Linux", "status": "online", "busy": false,
     "labels": ["self-hosted", "Linux", "X64", "podman", "baseharbor"]}
  ]
}
```

**Capacity:** 3 self-hosted runners, all online and not busy. Two runners support Docker (baha-runner-docker-2) and Podman (baha-runner-podman-1), one supports k3s/kubernetes.

## 7. Secrets (names only)

| Secret Name | Created | Updated |
|------------|---------|---------|
| **PLANNING_RECEIPT_WRITE_TOKEN** | 2026-10-28 | 2026-10-28 |
| RENOVATE_TOKEN | 2026-09-25 | 2026-09-25 |

**PLANNING_RECEIPT_WRITE_TOKEN exists:** YES. Used by receipt-approval.yml for publishing approved receipts to baseharbor-plan.

## 8. Receipt Chain State on baseharbor-plan origin/main

**Path:** evidence/receipts/public-contracts/  
**Contents:** 1 file

```
40428162731-1.json
```

**Content of 40428162731-1.json:**
```json
{
  "approved": {"at": "2026-10-27T02:52:00Z", "by": "mcpdev80",
               "receipt_commit": "06f25dcf1f9024a508f3beff0fb2e60bf7b0699f"},
  "gate": "public-contracts",
  "plan": "5ecabc17797aaf21a454cb83fab20e4ddc49eb7c",
  "run": {"attempt": 1, "id": 40428162731},
  "sha": "12f3c97ee9b593833aad5de223451e2e9d4f6dd3",
  "status": "pass"
}
```

**Chain state:** One approved receipt for gate `public-contracts`, approved by mcpdev80 on 2026-10-27, run 40428162731 attempt 1, status: pass. This is the sole public-contracts receipt in the chain.

## 9. Acceptance Table — Required Checks vs Replacement Coverage

| Required Context | Producing Workflow+Job | Test Suites Actually Invoked (file:line) | Candidate Binding Mechanism | Runner Used | New-Path Equivalent (receipt chain / selected execution) | Gap Status + Reason |
|-----------------|------------------------|-------------------------------------------|---------------------------|-------------|----------------------------------------------------------|-------------------|
| atomic/docker/lifecycle | docker-runtime-acceptance.yml:docker-runtime | atomic/docker/lifecycle (release-requirements.json:121-138) | pr-gate-plan.py wizard_check('wizard-app-lifecycle-tests') | baha-runner-docker-2 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| atomic/docker/data-capabilities | docker-runtime-acceptance.yml:docker-runtime | atomic/docker/data-capabilities (release-requirements.json:235-252) | pr-gate-plan.py wizard_check('wizard-app-data-tests') | baha-runner-docker-2 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| atomic/docker/guided | docker-runtime-acceptance.yml:docker-runtime | atomic/docker/guided (release-requirements.json:102-119) | pr-gate-plan.py wizard_check('wizard-app-guided-tests') | baha-runner-docker-2 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| atomic/podman/lifecycle | targeted-integration.yml:registered_backup_restore | atomic/podman/lifecycle (release-requirements.json:463-480) | pr-gate-plan.py wizard_check('wizard-app-lifecycle-tests') | baha-runner-podman-1 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| atomic/podman/data-capabilities | targeted-integration.yml:registered_backup_restore_podman | atomic/podman/data-capabilities (release-requirements.json:577-594) | pr-gate-plan.py wizard_check('wizard-app-data-tests') | baha-runner-podman-1 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| atomic/podman/guided | targeted-integration.yml:registered_backup_restore_podman | atomic/podman/guided (release-requirements.json:444-461) | pr-gate-plan.py wizard_check('wizard-app-guided-tests') | baha-runner-podman-1 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| ha/docker/data | pre-release-runtime-suite.yml:v0421_ha_groups_docker | ha/docker/data (release-requirements.json:858-874) | pr-gate-plan.py CI_CHECKS | baha-k3s-runner-01 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| ha/podman/identity | pre-release-runtime-suite.yml:v0421_ha_groups_podman | ha/podman/identity (release-requirements.json:948-964) | pr-gate-plan.py CI_CHECKS | baha-k3s-runner-01 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| integration/docker/core-bootstrap | targeted-integration.yml:registered_core_docker | integration/docker/core-bootstrap (release-requirements.json:1141-1155) | pr-gate-plan.py CI_CHECKS | baha-runner-docker-2 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| integration/podman/core-bootstrap | targeted-integration.yml:registered_core_podman | integration/podman/core-bootstrap (release-requirements.json:1156-1171) | pr-gate-plan.py CI_CHECKS | baha-runner-podman-1 (self-hosted) | Same self-hosted runner on fork | **closed** — fork inherits identical runner |
| integration/static/public-contracts | ci.yml:workflow_policy | integration/static/public-contracts (release-requirements.json:1040-1054) | pr-gate-plan.py CI_CHECKS (pr-planner-tests) | ubuntu-latest (GitHub-hosted) | Receipt chain: evidence/receipts/public-contracts/40428162731-1.json | **closed** — receipt chain provides approved receipt; one pass on record |
| adoption/conformance | pre-release.yml:adoption | adoption/conformance (release-requirements.json:786-802) | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | Pre-release.yml on fork | **closed** — fork inherits workflow |
| journey/docker | pre-release.yml:reference_journey | journey/docker (release-requirements.json:1002-1019) | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | Pre-release.yml on fork | **closed** — fork inherits workflow |
| source-contracts | ci.yml:release_unit_tests | source-contracts (pr-gate-plan.py:60-62): go test ./internal/application/... ./contracts/... | pr-gate-plan.py CODE_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| cli-guided-tests | ci.yml:release_unit_tests | cli-guided-tests (pr-gate-plan.py:64-66): go test ./cmd/baha -run '^TestGuided' | pr-gate-plan.py CLI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| cli-vet | ci.yml:release_unit_tests | cli-vet (pr-gate-plan.py:66): go vet ./cmd/baha | pr-gate-plan.py CLI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| cli-build | ci.yml:release_unit_tests | cli-build (pr-gate-plan.py:67): go build ./cmd/baha | pr-gate-plan.py CLI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| documentation-audit | ci.yml:release_unit_tests | documentation-audit (pr-gate-plan.py:14-16): bash scripts/documentation-audit.sh | pr-gate-plan.py DOC_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| mkdocs-en-strict | ci.yml:release_unit_tests | mkdocs-en-strict (pr-gate-plan.py:17): mkdocs build --strict --config-file mkdocs.yml | pr-gate-plan.py DOC_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| mkdocs-de-strict | ci.yml:release_unit_tests | mkdocs-de-strict (pr-gate-plan.py:19): mkdocs build --strict --config-file mkdocs.de.yml | pr-gate-plan.py DOC_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| pages-candidate-build | ci.yml:release_unit_tests | pages-candidate-build (pr-gate-plan.py:21): build candidate docs | pr-gate-plan.py DOC_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| pr-planner-tests | ci.yml:workflow_policy | pr-planner-tests (pr-gate-plan.py:674-676): python3 -m unittest scripts/test_pr_gate_plan.py | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| ci-policy | ci.yml:workflow_policy | ci-policy (pr-gate-plan.py:677-678): bash scripts/ci-workflow-policy.sh | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| ci-executor-verifier-tests | ci.yml:workflow_policy | ci-executor-verifier-tests (pr-gate-plan.py:679-680): test_pre_release_resume.py + evidence tests | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |
| receipt-execution-tests | ci.yml:workflow_policy | receipt-execution-tests (pr-gate-plan.py:681-682): test_receipt_*.py + ci-workflow-policy-receipts | pr-gate-plan.py CI_CHECKS | ubuntu-latest (GitHub-hosted) | receipt-approval.yml + receipt-shadow.yml on fork | **closed** — fork inherits workflows |
| ci-actionlint | ci.yml:workflow_policy | ci-actionlint (pr-gate-plan.py:685-687): actionlint@v1.7.12 | pr-gate-plan.py WORKFLOW_SYNTAX_CHECKS | ubuntu-latest (GitHub-hosted) | ci.yml on fork | **closed** — fork inherits workflow |

### Receipt Chain Gaps

| Required Context | Producing Workflow | Actual Invocation | Gap: unresolved |
|-----------------|-------------------|------------------|-----------------|
| Owner approval for public-contracts | receipt-approval.yml | Manual dispatch by mcpdev80 only; no automatic trigger | **unresolved** — approval workflow dormant; requires manual owner dispatch |
| Shadow verification of approved receipt | receipt-shadow.yml | All 6 recent runs **skipped**; requires manual inputs from approval | **unresolved** — shadow never runs; inputs from approval never produced |

## END o202-DONE
