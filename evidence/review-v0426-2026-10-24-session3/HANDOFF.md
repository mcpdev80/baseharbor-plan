# Independent v0.4.26 review and evidence handoff — session 3

Latest corrected-candidate decisions: [independent round2 review](ROUND2.md). Round1 details below remain historical and exact-head scoped.

Authority: Marcel's explicit 2026-10-24 assignment to independent review, evidence verification and coordinated planning. Session 1 owns all implementation/integration/merges; session 2 owns native acceptance and consumer freeze. This report changes neither product/CI code nor their ownership. No daemon, worker, native run, merge, tag, release or deployment was started. v0.4.27 is outside scope.

## Review decisions and immutable inputs

| Repository / PR | Reviewed head | API base at review | Technical decision |
| --- | --- | --- | --- |
| baseharbor #1064 | 54dfa458528e958be0ea3d8157a46bd501e76eb1 | 65aa063e90767c85af976081c100be1817370e67 | REQUEST_CHANGES: rejection fixtures and binding to rejected #1060 |
| baseharbor #1060 | 0f3bd169d4a02c5f019da822b4f45f66b972423e | 65aa063e90767c85af976081c100be1817370e67 | REQUEST_CHANGES: three independently reproduced defects |
| baseharbor #1056 | b0abe10526554960b827dd0f4a503a10cebff911 | 65aa063e90767c85af976081c100be1817370e67 | REQUEST_CHANGES: both prior findings reproduced |
| baseharbor #1052 | 9f715184af7b89ca3011aa4a0636c45138fe2c6b | a2abc17a8057ba972cb9ed481fad229fe9f12824 | PENDING: production diff inspected; complete source/test qualification waits on corrected #1060 and evidence |
| baseharbor #1046 | 1ec67f8d4b259d62bd108ee678f25c288b8b0564 | f39295680d41290fc505c0a8cc1769da51699293 | APPROVE source-only: six-file test diff inspected; integration/CI/native prerequisites remain open |
| baseharbor-demo #121 | f57c8b6e5ff39d0873df62b26272962765e88d6e | 82d042bc9b2393733858fd5fc9dd42a7f5491ea9 | REQUEST_CHANGES for evidence acceptance: relevant inputs differ from claimed passing run |
| baseharbor-console #9 | 6017de2845fa3e4e408c69038a0a5bdd7e82cad9 | e7d1e4a1d603158dece19bbc25a8e267d07cde5e | PENDING final repin/native receipt, no advance approval |
| baseharbor-node-connector #10 | e832d5651752121dea9484e18422d3e6459f9a72 | 7c7093d9671dfaa1aafeb92d62bbe9d074f9f47e | PENDING final repin/native receipt, no advance approval |

Repository names in this table are under `mcpdev80/`. The API-reported base on #1052/#1046 is recorded as returned, not silently substituted with develop. Any changed head/base/integration requires renewed qualification. These are technical decisions; **no formal GitHub pull-request review was submitted**. Findings were published as issue comments through @mcpdev80, the same account as PR author.

## #1064: exact bundle binding

Read the entire two-file diff (446 additions, one deletion), planner call path, diff resolver, trusted first-parent merge proof, new fixtures, trusted CI job logs and job states.

Verified the immutable R commit is `0f3bd169d4a02c5f019da822b4f45f66b972423e`, single parent `cb3a2bf7d73e21fae2ac80996cf3d5287ec0179f`. All four declared Git blob object IDs match R:

| Path | Git blob ID |
| --- | --- |
| .github/workflows/ci.yml | cf84de8ecf4ec89cd8b93c75a4e4bfe8b9e25c85 |
| scripts/pr-check-runner.py | 4ebe9499ebdda1194e829a9b2f36bfce93548213 |
| scripts/pr-gate-plan.py | 838fb3d68f730693d0617e930a545279a0f33be9 |
| scripts/test_pr_gate_plan.py | 25554d0a2231d236c6f3bb2774018db39ceeb5fc |

These are Git blob IDs, not raw SHA-256 digests. The full commit SHA also binds parent/tree. The planner re-derives the actual diff, compares all inputs, requires exact modified statuses and four paths, authenticated repository/develop, merge-base equality and clean first-parent target-forward merges. No candidate-supplied qualification record becomes authority in this new branch.

Reviewer created only local synthetic Git objects from actual R and policy candidate trees. `git merge-tree` succeeds with tree `ee549de2715adc8bb4f82d83879e7fd28f0b600d`; target-forward head `6526fdd6752e3c476d0e51c7e7068d8d0b5940e4` and integration `6ccb218b312f64bdd78aa49ac46a292e7359050c` were local simulations, **not GitHub integration or merge evidence**. Binding returns exactly pr-planner-tests, ci-policy, ci-executor-verifier-tests and ci-actionlint. Wrong repository, absent integration, changed status and forged merge-base reject. See [realgraph1064.log](realgraph1064.log).

P2: `scripts/test_pr_gate_plan.py:2902–3053` rejection fixtures do not patch the generated reviewed SHA/hash constants, so production R is absent and they pass for the wrong reason. Applying the same binding setup as the positive cases gives 13 passes / 2 failures: lines 2986 and 3029 manufacture valid integration trees/parents instead of their named invalid scenarios. The purported forward-chain positive duplicates direct-R; three-file Akte retention is described but not asserted. See [probe1064.py](probe1064.py) and [probe1064.log](probe1064.log). These two resolving valid integrations are not themselves a policy vulnerability.

The four-file SHA-bound R is also independently rejected below. Correcting R invalidates this binding: session 1 must adjust qualification through a newly reviewed exact candidate, never silently extend approval to a new head.

[CI run 40108385755](https://github.com/mcpdev80/baseharbor/actions/runs/40108385755) is green. Trusted Plan job120914758384 logs explicitly bind B=65aa063e90767c85af976081c100be1817370e67, H=54dfa458528e958be0ea3d8157a46bd501e76eb1, I=8abaa61683e2a2cb165f541d76f74346c29f948c. Final job120915093436 is successful. Artifact12565029718 has producer-reported ZIP digest57a71063b57536854f9cbeec18a477e93e21282019c2485495bc3129bfdbdd43; artifact contents were **not downloaded/independently authenticated**, so that digest is not a reviewer artifact verification.

Local full planner suite executed 116 tests, ending with one error and one failure from two existing registration subprocess checks because Go is absent from this environment. This is an environment limitation, not attributed to #1064 and not represented as PASS. Focused real-Git/probe checks above executed independently.

[Published technical comment](https://github.com/mcpdev80/baseharbor/pull/1064#issuecomment-6386325882).

## #1060: reported ACCEPT superseded by independent findings

Entire four-file net diff and relevant surrounding code inspected. [Current run40099514587](https://github.com/mcpdev80/baseharbor/actions/runs/40099514587) is failed; no rerun dispatched. Prior o139 ACCEPT was not available locally and is not adopted.

- P1 `scripts/pr-gate-plan.py:1217–1225`: all OpenBao production paths, including the intended bootstrap.go/bootstrap_test.go pair, remain unresolved. OPENBAO_CHECKS at299 is never required. Actual planner probe returns unresolved and only source-contracts. Landing this candidate alone cannot qualify #1052; missing exact reviewed-source/status qualification remains a real prerequisite. Do not fix by a generic production allowlist.
- P2 `scripts/pr-check-runner.py:69–72`: WIZARD_TEST_FAMILIES guard rejects openbao-package-tests before reaching its new branch. Actual call raises ValueError unsupported executable validation. Workflow at ci.yml:719 executes ordinary package tests instead of this strict discovery/RUN/PASS helper. Establish the actual route and its zero-test/skip rejection proof.
- P1 `scripts/pr-check-runner.py` removed the existing `$` suffix for wizard-core918-native-sql-safety-tests. Mocking only the Go process boundary, a suite containing four `<required-name>Replacement` tests is accepted although no exact required safety test exists. Restore the unrelated exact-name invariant.

[Executed probes/log](probe-followups.log); [published technical findings](https://github.com/mcpdev80/baseharbor/pull/1060#issuecomment-6386344700). Session 1 owns repair, exact qualification and fresh CI. No acceptance of future heads.

## #1056: explicit follow-up of F1/F2

Read both affected implementations and independently reproduced both prior defects on b0abe105. [CI40093488851](https://github.com/mcpdev80/baseharbor/actions/runs/40093488851) is green, but candidate remains rejected.

- P1 F1 `scripts/pr-gate-plan.py:746–806,1165–1168`: strict binding refusal falls back to bootstrap_eligible. In an isolated real Git repository, a base with the title and empty JSON record plus candidate adding internal/unreviewed/security.go with that title in its commit message resolves with zero gates and only the three CI checks. No exact reviewed SHA/blob/status authority was satisfied. Remove/narrow this generic fallback; strict refusal must remain closed. The same broad helper exists in the inherited develop source: do not interpret #1064's new branch as fixing it.
- P1 F2 `scripts/pr-check-runner.py:157–228`: three individually mutated #1050 pin payloads pass: cyclic core.consumes.connector, live-console console.origin.commit=f*40, console repository attacker/repo. The validator fails to check consumes DAG/equality, exact gate role repositories and origins. Canonical ecosystem graph/origin validation must reject these.

See [probe-followups.py](probe-followups.py), [log](probe-followups.log), [published findings](https://github.com/mcpdev80/baseharbor/pull/1056#issuecomment-6386345891). cmf12 and o135 Ops originals were unavailable; findings here are reviewer reproductions, not an assertion those files were read. Keep correction serialization behind #1060 and review R'→Q'→H' separately.

## #1052 / #1046

#1052 production diff inspected: bounded five-attempt, five-second-per-attempt unseal probes with caller-cancelled backoff; permanent-before-transient classification; inspect remains single-probe; post-unseal verification retries only supported transport failures. The full ~1,400-line added test diff and real native evidence are not qualified here. q123 is only reported ACCEPT, not independently read. Current [CI40099034364](https://github.com/mcpdev80/baseharbor/actions/runs/40099034364) failed. Complete source/test review and exact fresh CI follow corrected #1060. No acceptance.

#1046 complete six-file diff inspected: one shared 0700 TempDir helper and seven fixture substitutions across five test files. No production guard change, skip or permission-rejection relaxation in the diff. Technical source-only APPROVE for 1ec67f8d / f3929568; **no local Go tests executed**, since Go is absent. q118/cmf10 reported execution is not independently inspected. [CI40086275780](https://github.com/mcpdev80/baseharbor/actions/runs/40086275780) is failed. Current-base exact qualification, successful required checks and task-native acceptance remain mandatory; the task is not accepted here.

## Consumer evidence and freeze

Directly inspected actual immutable consumer blobs and net diffs. #121 contains Core pin1861ed07888a1ec22c218ca491d23ee54f48e261. Console #9 pins Core1861ed07 and Demo25c319697fd3d89d894943e0f44cd3d5dde8b198; Connector #10 pins those and Console69d1d14007fa43dc0c0457c3347280be7f802818. These are historical freeze references, not final Demo/Console merge commits. Pin-only diffs do not establish compatibility/native acceptance.

Read job states and complete logs of [Demo run39990941852](https://github.com/mcpdev80/baseharbor-demo/actions/runs/39990941852): Podman120542211968 and Docker120542212240 actually checkout Demo25c319697fd3d89d894943e0f44cd3d5dde8b198 and Core1861ed07888a1ec22c218ca491d23ee54f48e261; native Backup/Restore result PASS and cleanup complete are in the logs. Historical success is independently observed, not reviewer re-execution or proof of every required developer journey.

REQUEST_CHANGES for #121 evidence acceptance: entire tree is not identical to that historical run. `git diff 25c31969..f57c8b6e` changes two relevant files:

- `.github/workflows/v0424-targeted.yml`: candidate omits the archived cleanup-preparation/scope-result.json present in the passing workflow.
- `scripts/failure-runtime-diagnostics.sh`: candidate lacks passing commit's Podman cold-start allowance (90-second overall/60-second per-call versus candidate60/20).

Identical Core ref does not prove compatible cleanup/evidence inputs. Need session2's exact candidate native receipt or verifier-authenticated compatibility covering these files, actual scope/ownership/foreign preservation, origin run/attempt/artifact/digest and relevant newer failures. No artifact authentication or full cleanup/sentinel ownership qualification was completed here. [Published session2 handoff](https://github.com/mcpdev80/baseharbor-demo/pull/121#issuecomment-6386360796).

Freeze order remains Demo D → Console U repin → Connector K repin → #1050 reconcile. Connector#9 supersession is session1's operation, not executed here. Core C remains1861ed07888a1ec22c218ca491d23ee54f48e261 for the established W1 matrix; no substitution with moving develop and no v0.4.27 dependency introduced.

## Release dossier: current versus historical blockers

Read current AGENTS, development rules, WORKFLOW/RELEASE_WORKFLOW, core-923, prepare card, v0.4.26 release scope, canonical audit and readiness guide. Planning baseline78dc7b591c7bc9325a029bb422f74a8fb30f082a.

- Historical: #1047 and #1063 already integrated. Older #995/#990/#998/#1007, paused handover prose and prior head-specific failures must not be revived as current blockers without a current unmet contract. Historical evidence is retained.
- Current D/CI: #1064 rejection fixtures plus its rejected bound R; #1060 three findings; #1052 qualification and final native evidence.
- Current C2: #1056 F1/F2; serialized correction/record/integration still required.
- Current appid: #1046 exact current qualification/required checks plus native developer path; source-only approval does not close the task.
- Current freeze: #121 evidence compatibility / native acceptance; Console/Connector final dependency pins and actual issuer/auth/mTLS/lifecycle/cleanup receipts.
- Current #1050 head388967621c90750e59c5faab35344b46d4108fef: actual JSON read, historical C/D/U/K DAG and origins present but not final merged D/U/K. PR body still mentions #1055; that is fenced v0.4.27 and not permission to move Core C. Current integration chain must be reconciled explicitly.
- Current W1: requires actual frozen pins and verified targeted gate inputs/receipts, not the number of accepted cards. Independent developer path and full CLI/JSON/MCP/HTTP, Console auth and Connector mTLS acceptance remain unverified in this session.
- Current J: read-only hygiene history only; no cleanup performed or needed for this assignment.

On clean isolated product65aa063e90767c85af976081c100be1817370e67, executed `bash scripts/documentation-audit.sh`: PASS; EN/DE158 paired pages, DE technical integrity and41 human-guide/navigation pages. Inspected EN/DE v0.4.26 notes, both release indexes, CHANGELOG candidate section, canonical audit and Pages workflow/readiness inputs. Candidate notes remain explicitly unpublished and substantively aligned on New/Edit/Footprint/MCP, backup fixes, ownership/security and deferred Console scope. No final ecosystem-ready claim.

Strict MkDocs not executed: module/tool unavailable locally. Prior run40064756153 is reported green in planning, not independently artifact-verified here. Do not rerun it merely because unrelated CI files changed; prove unchanged complete doc/build inputs first, then reuse through the established verifier. Gate/pin/origin inputs also changed independently of documentation and require their own qualification.

Only docs/releases/v0.4.26.md exists as a release-specific artifact on the inspected product baseline: final v0.4.26.evidence-runs, v0.4.26.selected-gates.json, v0.4.26.consumer-pins.json and v0.4.26.demo-ref are not present. #1050 supplies proposed pins only. Their final values depend on freeze and reviewed CI. No final immutable ecosystem candidate, final gate inventory, authenticated origin bundle or independent developer-path receipt was supplied, so canonical readiness remains **NOT PROVEN**.

## Missing local Ops and boundaries

The codeman host `/home/marcel/dev/baseharbor-ecosystem` is not mounted here. Searches of available scratch files found no o139-review1060.md, codex-recipe-1060-qualification.md, q123 source acceptance, cmf12 original review, o135 design, q118/cmf10, f53/f54, q116 dispatch table or o120 dossier originals. Root-only coordinator-plan.md, ops/missions/*.txt and unpushed evidence/board-2026-10-24/*.md are unavailable. Published planning snapshots and PR bodies are available, but do not replace these originals. No reported ACCEPT/native receipt has been promoted to independently verified fact.

No destructive cleanup or worker start is authorized/needed. Existing inherited/untracked v0.4.27 material encountered in a scratch clone was preserved untouched and excluded from the clean docs audit. No v0.4.27 files/PRs are part of the planning write set.

## Reproduction and next trigger

The three reviewer scripts are evidence probes, not product fixes. From a separate scratch directory, provide exact checkouts named review-core (#1064 H), source1060 (R), source1056 (b0abe105), with the actual historical objects available. Run realgraph1064.py and probe-followups.py from their parent. probe1064.py intentionally returns two fixture failures after correctly binding the baseline; this demonstrates false original negatives. No native runtime is involved. Git commit IDs for newly synthesized fixtures depend on local author/time; trees and verdicts are the invariant.

Session1: address #1060 defects first without broadening source authority, then correct #1064 exact R and real rejection fixtures; serialized #1056 F1/F2 and appid qualification follow. Re-submit exact base/head/integration and focused results for independent review. Session2: supply candidate-bound compatible native/cleanup evidence, final acyclic pins and explicit provenance. This handoff grants no approval to those later heads.

Planning changes add only this session-owned evidence and clearly identified Handoff sections on existing prepare/core-923 cards. Original task owners, states and historical notes remain. Regular generator/render/check/tests and final remote validation are recorded in the accompanying verification receipt. No task or release is accepted by this report.

## Initial publication boundary (historical)

The evidence/planning bundle is saved in local commits only: ordinary push lacked credentials; automatic approval review blocked connector publication. No final remote planning SHA is claimed. Findings already published in the PR issue comments remain available to sessions1/2. See VERIFICATION.md for the precise blocker and local validation. Publication requires the Owner's explicit renewed approval requested because of the automatic rejection, followed by concurrency reconciliation and actual remote-SHA validation.

## Renewed publication authorization

Marcel explicitly approved publication of this reviewed Planning bundle in the follow-up message “ja ich gebe es frei”. The previous publication blocker above is historical. This publication preserves exact-head technical verdicts; it does not review or approve later product/consumer heads. Current Planning main is integrated before publication, normal render/check/tests run, and the actual remote commit is validated after the expected-SHA update. No product/CI change, merge, tag, release, deployment or native run is included.
