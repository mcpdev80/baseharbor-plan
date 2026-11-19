# CODEX-REVIEW — PR #1613 / 0428-073 alert evaluator contract

Date: 2026-11-19  
Role: CODEX-REVIEW  
PR head: `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`  
Develop: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`  
Exact-head run: [44495425072](https://github.com/mcpdev80/baseharbor/actions/runs/44495425072)  
Hop evidence: [fix-1.md](../perses-alerts-hopf/fix-1.md)

## Verified

- PR #1613 is OPEN, ready (not draft), and CLEAN at exact head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`; remote `develop` is `da76c5cf9`, an ancestor of the candidate.
- Run `44495425072` is terminal SUCCESS on the same exact head. Selected checks passed: PR Selected Checks, trusted plan, native gate plan, source format, workflow policy, go-build, go-vet, focused Python, six Go unit shards, runner interface, demo pin, exact candidate, and selected runtime jobs. Nineteen unrelated runtime/HA/release jobs were skipped by routing.
- The hop dossier documents the four content-preserving conflict resolutions and ancestry from the old candidate head `470735c1d`.
- The Planning task note declares `depends_on: t-20261114-r28-perses-datasources`; that card is still `review` and depends on `t-20261114-r28-perses-runtime`, which is also still `review`. The prerequisite chain is not yet accepted.

## Blocking finding

The PR does not deliver the task's required real alert rule evaluation or persistence. `PersesAlertEvaluator` contains only metadata (`Kind`, `Name`, evaluator/owner strings, and `RecipientValidated`); it carries no rule expression or persisted rule object. `BuildPersesAlertEvaluator` delegates to `persesAlertEvaluatorFromRelease`, which calls `persesAlertRealEvaluatorContractPresent()`. That function unconditionally returns `false`, so every selected/pinned candidate fails closed and no alert rule can ever be built. `VerifyPersesAlertEvaluatorHealth` has no execution or persistence path either. All added tests assert those failures.

The task contract asks for one real rule based on confirmed metrics with execution and negative tests, using an existing supported Prometheus contract or an Owner-approved alternative. The PR's finding that no evaluator/recipient currently exists explains the fail-closed behavior but does not meet that implementation requirement. No Owner approval to replace the task outcome with an unavailable-only contract is present in the reviewed card/evidence.

## Recipe

Implement the smallest supported Prometheus rule and persistence path, grounded in a confirmed metric, with an execution witness and negative/ownership tests; or obtain and record explicit Owner approval to revise the task to an unavailable-only contract before acceptance. Preserve fail-closed selection, ownership, recipient, and secret handling. Re-run exact-head required checks after any change.

## Verdict

**REQUEST CHANGES.** The candidate is correctly hopped and its exact-head checks are green, but the task's core evaluator/rule/persistence outcome is absent. No merge performed. The prerequisite chain also remains unaccepted, so #1613 is not merge-ready independently of this content finding.

## CI cost note

Run `44495425072` completed from 09:19:57Z to 09:25:04Z (5m07s wall time). Selected checks passed; runner-minute billing is not exposed in the run summary. No tests were run by this reviewer.

## END

END_REQUEST_CHANGES: #1613 / head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783` / run `44495425072` SUCCESS / real rule+execution+persistence or explicit Owner-approved scope revision / no merge.
