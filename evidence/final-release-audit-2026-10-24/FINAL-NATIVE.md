# Final exact-source native Go Docker acceptance

Independent reviewer: `/root/final_audit`. Technical verdict: **APPROVE** for this exact native proof and the appid card's final-develop lifecycle requirement. This is not full release approval or a formal GitHub review.

## Immutable identity and authenticated artifact

- Core: `3e27497b4ef7b567858ba646bc3071bee37d19bd`.
- Git tree: `8dce77b34ad51f8762c6bd6f6c809e54e73fdfd3`, independently equal to the remote Git commit tree.
- Workflow run: [40128173805](https://github.com/mcpdev80/baseharbor/actions/runs/40128173805), attempt 1, completed/success.
- Actual job: [120973982875](https://github.com/mcpdev80/baseharbor/actions/runs/40128173805/job/120973982875), completed/success.
- Artifact: `12574701602`, `docker-runtime-evidence-40128173805-1`.
- ZIP SHA256: `d0599384b87d6533da3394e909838f2f04338e668a8d8f048f1467e0ab7954a8`. Independent download hash equals GitHub's artifact digest.
- Toolchain: `go version go1.26.9 linux/amd64`.
- Host/container binary SHA256 equality: `caa45ed0b7f5b5359008b327c78d07bc43f82be0e7ffc1f08bcf6b76b3201daf`.
- Native validation binary reports `version=dev` and the exact Core commit, as intended for this test build. Release binary versioning remains a later publication check.

## Actual test and cleanup verification

Parsed every event in all four retained JSONL files. Each of the exact eight mandatory families and its Go package has PASS; there are no fail/skip events.

| Exact test family | PASS seconds |
| --- | ---: |
| TestManagedLokiIngestsRealComposeWorkloadLogs | 48.21 |
| TestRepositoryWorkflowRealLifecycle | 102.82 |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | 62.53 |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | 54.23 |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | 77.06 |
| TestMultiInstanceComposeLifecycleInCI | 4.54 |
| TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile | 255.93 |
| TestManagedTempoReceivesVerificationTraceThroughCollector | 18.08 |

Actual job logs record final isolated runtime cleanup complete at **20:17:51 UTC on 2026-10-24** and the strict eight-family verifier success at **20:17:52 UTC**. Runtime setup, exact source/image identity, engine preflight, detection, all test stages, cleanup, receipt generation and upload are successful. Provider-HA and MCP-edit sibling jobs are intentionally outside this existing route; their skipped states are not used as proofs.

The previously verified intermediate run `40117855934` remains historical and is not substituted for this final R run.

## Acceptance consequence

The existing appid fixture task's explicit final-develop `TestRepositoryWorkflowRealLifecycle` requirement now has actual exact-source native PASS, along with the other seven existing mandatory families and cleanup. Root can record Owner-authorized task acceptance with this evidence. Core-923, final consumer freeze, the required 65-gate authenticated approval, qualified promotion and publication retain their own requirements.
