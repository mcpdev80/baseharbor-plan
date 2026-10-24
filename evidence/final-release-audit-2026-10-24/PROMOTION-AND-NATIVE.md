# Promotion, native receipts and superseded preparation

Independent read-only follow-up by `/root/final_audit`, 2026-10-24. No product mutation, workflow start, merge or tag was performed. Coordinator publication is separate.

## Final source and consumer pin review

Final Core R is `3e27497b4ef7b567858ba646bc3071bee37d19bd`, following #1069 and #1070. Remote comparison from intermediate `64dbf1dfcb3397a14bdfc4f1e1d1f8203a936f5c` shows exactly nine maintained prose files; no Go, runtime, test, workflow, inventory, contract or verifier changes.

The final EN/DE backup sentence was independently approved after narrowing it to interrupted workload stop. The actual code recovers attempted owners through a fresh bounded context; no claim of universal recovery success is made. Final published note blobs are EN `57176aa88e789429dcc03f9043aa335c5aacc7e9` and DE `c84ee3153fbfd0ae443ecf81dbb8027e1c9552e4`.

Demo #121 exact source `a1051ec5f5c366cdfafe527298ac60e5db4f951c`, tree `a372d0f5c473de417006ff6924632f11589073c9`, parent `f90d06235322e06f1fb2e4e58f0907b3c492aa91`: independent source verdict **APPROVE**. Direct commit, contents and complete one-file remote comparison prove the sole change is `baseharbor-core.ref` from intermediate Core to final R. Pin blob `42fe65908c5bcaa8edb22e2ed60ede126c818e06` contains the exact R plus newline. Cleanup helper, tests, fixture and workflow bytes are preserved. This verdict is source-only and is not a native receipt or formal GitHub review.

## Verified intermediate native Go proof

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/40117855934
- Actual Docker job: `120942823518`, completed/success; cleanup and eight-family verifier completed/success.
- Source: `64dbf1dfcb3397a14bdfc4f1e1d1f8203a936f5c`; source tree: `32a0b03569124ad704dac656b99c90d736a82228`.
- Artifact: `12570252664`, `docker-runtime-evidence-40117855934-1`, SHA256 `603c73dbdc2c57955ec406183209e7648a0c53089b6a59f79832e79606a2ce48`.
- ZIP downloaded independently; its digest equals GitHub's authenticated artifact digest.
- Go 1.26.9; actual rootless Docker 28.0.4, API 1.48; binary metadata reports the same source commit. Actual cleanup log completes at 18:02:01 UTC.

All four JSONL files were parsed directly. Each required test and its package have PASS; there are zero fail/skip actions:

| Exact family | Seconds |
| --- | ---: |
| TestRepositoryWorkflowRealLifecycle | 101.90 |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | 64.49 |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | 55.65 |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | 79.79 |
| TestMultiInstanceComposeLifecycleInCI | 4.53 |
| TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile | 253.64 |
| TestManagedLokiIngestsRealComposeWorkloadLogs | 48.52 |
| TestManagedTempoReceivesVerificationTraceThroughCollector | 17.63 |

This is intermediate proof only. The appid card explicitly requires the final develop-head repository lifecycle. The final source's public-prose changes include README and five front-page/DE files which `metadata_path` does not exclude; v0.4.26 has none of v0.4.25's special native fingerprint exemptions. Do not silently relabel this source as final R. Existing final-R native Go run `40128173805` is in progress at the audit checkpoint, not PASS.

## Main-only history reconciled

Actual main `54acc4b66715681213788fdba395a569ddc95a1b` and current develop have 33 historical main-only commits, spanning release/handoff squashes through v0.4.25. Their apparent divergence contains **no unique current main content**:

- Main tree: `d0cbc26477f2f4645c933ab43e649cb67c411858`.
- Develop ancestor `33b7ca94b42cc45e908c0d964cfbe0cc8349f231` has that exact same tree.
- Actual `git diff --exit-code` between those commits passes with zero changed paths.
- That develop release ancestor is contained in the inspected develop line, from which final R follows.

Ordinary merge-tree preview does produce many historical content/add-add conflicts. Do not accept that synthetic conflicted tree or resolve it opportunistically. Historical #908 establishes the existing safe promotion pattern: promotion commit `33f11c719124d4dd6c4bf09877470c6a23056888` retained prior main and reviewed candidate parents while selecting the exact reviewed candidate tree; its successor `1ed6a057bc9e58c2d98277287aa723109318a8f6` preserved original evidence ancestry and exact final develop tree. GitHub then squashed the reviewed promotion PR into main.

After genuine final approval, use the same dedicated promotion-branch approach: first parent actual unchanged main, additional parent approved R, tree exactly R plus only existing allowed publication metadata. Open one promotion PR to main and preserve required checks. Do not move R, mix in later develop work, change executable bytes or broaden the handoff allowlist. Compare the actual promotion tree and resulting main against approved R using `release-handoff.py validate`. Preserve all prior history through main's first-parent lineage and explicit candidate ancestry on the promotion branch; record squash-policy effects truthfully.

## Superseded alternative PRs

Reviewed complete current PR diffs, not titles alone:

| PR / exact head | Actual scope | Disposition evidence |
| --- | --- | --- |
| #1054 / `4f294811d2e4c6ac1d6da5bb052cb04fba40064d` | Historical 72-line v0.4.26 consumer JSON plus three CI scripts/tests | JSON is the already superseded #1050 C/D/U/K snapshot. Original classifier/partial validator is replaced by accepted #1056 canonical validator and actual workflow path. |
| #1061 / `ae9afc8791325b11ad0011d3011514fd6e8af92a` | Three CI scripts/tests plus stale qualification record for `7a220d26` | Optional ecosystem shape checks and multi-record support are covered and strengthened by accepted #1056/#1064. Final actual source record is separately accepted #1066. |
| #1062 / `7b9fd4ae1447c47c6c7e21386f30715031ff9be0` | Same functional four-file bundle, with record for `9d1624e2` | PR body says docs-only, but actual merge-base diff includes the three CI files. Its old anchor is obsolete; no unique relevant implementation is missing. |

Current accepted implementation validates exact gates, source origins, canonical four-role consumes DAG, graph/gate equality, strict filenames, duplicate keys and symlinks. It extracts the runner and canonical sibling owners from the trusted target. The old nine pins tests were replaced by three real CLI/workflow tests with a stronger negative matrix; they were not all preserved by name. Three register tests are retained by exact name, with strict qualified multiple-entry support.

A bounded read-only projection of the original classifier cases against current source passed: canonical add selects only pins-data-validation and no native gate; modified pin, outside-directory pin and mixed unknown JSON remain unresolved. No persistent test or product change was added for this audit.

Recommendation: root may explicitly close #1054/#1061/#1062 as superseded preparation with their history/branches preserved. Do not merge their stale records or weaker validator. This is not a claim that each old test or old snapshot was accepted. v0.4.27 PRs remain untouched.

## Remaining scoped cards

Seven current v0.4.26 cards remain unfinished at this checkpoint: core-923, final appid native proof, complete defect audit, prepare, qualify, publish and verify. CI closeout and Q20 documentation are accepted. Real remaining preparation is final-R native proof, actual final D/U/K graph and joint browser/remote receipts, required W1/atomic-first evidence and complete dossier. Historical STOP paragraphs do not create a new stop under the Owner's current completion instruction.

The final publish card requires the actual main SHA, clean-state/repository/identity checks, tag-absence guards, exact annotated tag and tag-only push commands. Verify must remain pending while the user has not yet pushed the reserved tag; publication and post-release artifacts cannot be claimed before that action.

## Subsequent coordinator disposition

The coordinator closed #1054, #1061 and #1062 as superseded preparation, without merge. Original heads, bodies and branches were preserved; each body received an explicit Maintainer disposition. No v0.4.27 PR was changed. This operational result was independently re-read from current PR metadata.

Planning check after this audit's local evidence additions: 322 tasks, 7 epics, 13 releases, 15 decisions; zero errors and five existing warnings. Shared card ownership and state remain with root.

## Current protection and promotion CI

Independent read-only ruleset retrieval confirms main ruleset `23754542` targets only `refs/heads/main`, remains active, requires linear history and a pull request with squash as its only merge method. Required approving review count is zero; review-thread resolution remains required. Develop status ruleset `25223521` targets only `refs/heads/develop` and requires strict `PR Selected Checks` from integration `15368`.

The current CI workflow runs workflow policy and syntax for PRs to main, while trusted PR planning and selected-final jobs explicitly require base_ref develop. Therefore the main promotion PR is not blocked by an unmapped 191-file develop planner request. This is the actual unchanged protection/workflow configuration, not a bypass or ruleset edit. Complete authenticated approval and exact published-tree/handoff verification still apply.
