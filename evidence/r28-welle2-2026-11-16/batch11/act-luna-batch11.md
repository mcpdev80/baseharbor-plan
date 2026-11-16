# CODEX-REVIEW — Luna batch 11

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch11.md` · final review of the prior #1645 content hold against the schema-validation, query-validator, and base-stacking recipes.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`). `HORDE_WORKER_TOKEN` was unset.

## Candidate and exact-head CI

- Repository/account: `mcpdev80/baseharbor`, authenticated login verified as `mcpdev80`.
- PR #1645 is OPEN and DRAFT; base `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; head branch `w091-tempo-r5-fix` @ `c781eb86fc996493bf5e0ee807913e81a51c3ab4`.
- The current GitHub diff contains 21 files, all Tempo adapter, contract, witness, test, fixture, or test-support files. The #1575 seam PR remains OPEN at the exact base head, so the stack is separated one PR per card. No code or PR metadata changed during this review.
- Exact-head run `43876671426` is a completed `pull_request` run on `c781eb86fc996493bf5e0ee807913e81a51c3ab4`, conclusion SUCCESS. `PR · Draft source and routing` and Draft Go `packages`, `cli-0`, `cli-1`, `cli-2`, and `cli-3` succeeded. `PR Selected Checks`, `PR · Selected Runtime`, and native runtime jobs were skipped because the PR remains a draft. Thus the requested exact-head draft checks are green; those skipped gates remain a merge hold. The earlier run on the old `develop` base does not replace this post-retarget run.
- Worker evidence `evidence/r28-welle2-2026-11-16/perses-tempo-source/retarget-round-1.md` reports `go build ./...` success and focused Perses/Tempo tests passing. This reviewer did not rerun local product tests.

## Revalidation against prior recipes

### Pinned schema validation

At the exact head, `perses_tempo_contract.go` ties the mirrored model to the committed upstream source and sample witnesses. The validation rejects an `apiVersion` field because the pinned REST Datasource model has no such field. `BuildPersesTempoDatasourceWithProbe` validates the emitted resource with `ValidatePersesTempoResource` before returning it. The witness and tamper tests exercise drift and non-native resource rejection. This addresses the prior r3 schema-witness finding.

### Production TraceQuery validation and observation

The same production builder calls `ValidatePersesTempoTraceQuery` on the emitted query. `TestPersesTempoDatasourceBuilderValidatesBothResources` checks both validators; `TestPersesTempoDatasourceValidateRejectsNonNativeResource` exercises schema deviations; `TestPersesTempoDatasourceRealTraceQueryAnswers` exercises the query path and observed-answer behavior. The implementation uses the authorized Tempo service-access client and keeps health unverified unless a real TraceQL response is observed. This addresses the prior query-validator requirement.

### Base stacking

Live PR metadata now targets the exact still-open seam branch at `66ff93d1`; the head is unchanged. The current PR diff no longer includes the 0428-075 contract-seam changes, resolving batch10's one-PR-per-card finding. The seam remains a separate prerequisite and is not accepted or merged by this review.

## Verdict

**APPROVE CONTENT** for PR #1645 at exact head `c781eb86fc996493bf5e0ee807913e81a51c3ab4`, against base `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`.

No blocking content finding remains from the prior schema, query-validation, or base-stacking recipes. This is not task acceptance or merge authorization. Keep the PR draft; the required `PR Selected Checks` and native/runtime gates are skipped in the current run, and the #1575 dependency remains open. Recheck those gates and dependency state before any merge decision.

Non-blocking note: the comment above `TestPersesTempoDatasourceNativeResourceShape` still describes an `apiVersion` envelope, while the test and implementation correctly require its absence. Correct that stale comment in an ordinary content update; it does not change this verdict.

## repo-rule compliance and turn-start flags

- Read-only product review; no product files, PR state, CI, task state, or release state changed.
- No merge and no GitHub review mutation. No local product tests were run.
- Turn-start coordinator flags forwarded for disposition: laptop:1 `WORKER-SEAT-UNJUSTIFIED`; missing GUI TODO file `workers/todos/0428-080-.json`; 36 open PRs; other worker seats remain held/underfilled per the reported `NO_ELIGIBLE_WORK` evidence.
