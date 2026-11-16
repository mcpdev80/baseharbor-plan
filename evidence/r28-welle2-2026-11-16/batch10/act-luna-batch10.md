# CODEX-REVIEW — Luna batch 10

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch10.md`; object 2 replaced per owner instruction: PR #1610 is closed; review PR #1645 at the supplied exact head. The local mission text is otherwise unchanged.

**Session identity:** assigned as CODEX-REVIEW (Luna). The runtime does not expose an independently verifiable provider-side model identity to this review; no model alias is asserted.

| PR | Exact head | Exact-head `pull_request` run | Verdict |
|---|---|---|---|
| #1614 | `80d4df52e913e4472334a5f257fe868d26d5976e` | `43840657678`, attempt 2, SUCCESS | APPROVE CONTENT; prior exact-head CI hold resolved |
| #1645 | `c781eb86fc996493bf5e0ee807913e81a51c3ab4` | `43874313785`, SUCCESS (26 success / 13 skipped / 0 failed jobs) | REQUEST CHANGES: PR combines the open 0428-075 seam with 0428-091 Tempo work and targets `develop` |

## #1614 — `t-20261114-r28-cli2-app-status`

Live PR #1614 is open and draft, based on `lane-0428-059-cli2-source-model` at `818d572b982a69e2caebd5474a4ba270ed21fd41`; head remains the reviewed `80d4df52e913e4472334a5f257fe868d26d5976e`. Run `43840657678` is a `pull_request` run on that exact head, completed SUCCESS on attempt 2. The `PR · Draft Go · cli-1` job completed SUCCESS; its log reports 413 passed, 10 intentionally skipped, 423 discovered. The successful exact-head run resolves batch9's red-run hold.

I inspected the production row-building paths at this exact checkout/head. `collectSourceModelComponents` passes `retainedPlacementClassifier(resolved.DeploymentRecord)` into `declaredVersionServices`; aggregate `componentRowsForRecord` does the same using the retained record. `app version` consumes the shared status collector. The classifier reads the record's persisted `backend_placements`, classifies shared PostgreSQL/Valkey from that deployment's retained placement, and does not mutate process-global environment. The prior r2 placement-wiring finding is therefore addressed in production code. The successful cli-1 rerun also removes the only batch9 blocker; no unrelated fix is proposed for the formerly red core assertions.

**Verdict: APPROVE CONTENT** for exact head `80d4df52e913e4472334a5f257fe868d26d5976e`. This review does not accept dependencies or authorize merge. Evidence includes `evidence/r28-welle1-2026-11-15/cli2-app-status/round-2.md`, `round-3.md`, batch9's review act, live PR metadata, exact-head run/job/log, and the production source at the exact head. No local product tests were run.

## #1645 — `t-20261114-r28-perses-tempo-source`

Live PR #1645 is open and draft, base `develop` at `fae335a3ec1ed93663e4971cbf71f157f1c07174`, exact head `c781eb86fc996493bf5e0ee807913e81a51c3ab4`. Run `43874313785` is a completed `pull_request` run on that exact SHA; 26 jobs succeeded, 13 were skipped, and none failed, including `PR Selected Checks` SUCCESS. This establishes the requested CI result for the current head.

The Tempo correction delta from the prior reviewed head `601f3c3af26a7aec00551f8d37899c30918b9939` is limited to two commits: the eight pinned upstream witness files changed from `.go` to `.go.txt`, embed/witness paths and `perses-pin.json` paths follow those renames, and the witness map was gofmt-aligned. The prior round-4 changes supply the native pinned-model witness, native datasource/query envelopes, and production validation of both resources; round-5 records the CI selector root cause and content-preserving renames. I found no new Tempo behavior regression in that delta.

**Blocking finding — PR scope/base includes another open card.** The current PR base is `develop`, while PR #1575 for `t-20261114-r28-perses-contract-seam` remains OPEN at `lane-0428-075-perses-seam` head `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`. The #1645 head contains that seam's commit history (including the merge of `66ff93d1c`) plus the Tempo commits. The live PR diff against `develop` therefore includes the seam's manifest, capability, documentation, and management-UI changes alongside the Tempo datasource. This is a two-card PR and breaks the one-PR-per-card and stacked-base rules; the seam dependency is not merged/accepted.

**Verdict: REQUEST CHANGES for PR #1645 as currently based. Recipe:** retarget the replacement PR to `lane-0428-075-perses-seam` at its current head, preserving the exact Tempo head and the separate #1575 PR. Recheck the complete PR diff and obtain a fresh exact-head `pull_request` run after changing the base; retain draft state. Stop if the base lane has advanced and requires an explicit content rebase. No product code correction is indicated by the Tempo-only two-commit delta. No GitHub metadata was changed by this review.

The exact-head `pull_request` run is a CI witness, not dependency acceptance or merge approval. No local product tests were run. The #1575 seam remains a separate review/merge prerequisite.

## repo-rule compliance

- Read-only product review; no product files, PR metadata, review state, CI, or release state changed.
- No merge, PR approval mutation, or task-state change.
- Evidence is planning-only and does not mark either task accepted.
- Turn-start flags recorded for coordinator disposition: worker pool 0/4 with existing `NO_ELIGIBLE_WORK` holds; 36 open PRs; dev-host R1 alarm reports 6 `bh-*` containers.
