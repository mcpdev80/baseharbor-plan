# CODEX-REVIEW + MERGE — PR #1575 / 0428-075

**Review date:** 2026-11-17 06:29 UTC  
**Reviewer:** Codex, session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`  
**Candidate:** `9fc771859415fa44145720ff5079851943b2c020`  
**PR:** `https://github.com/mcpdev80/baseharbor/pull/1575`

## PLAN

1. Refresh develop, branch, PR head/base, CI and review threads — done.
2. Compare the reviewed correction against the Hopf-4 candidate and inspect the corrected code/tests — done.
3. Record the SHA-specific review verdict and merge disposition — done.

## Remote witnesses

Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git`:

```text
bcae1e8c1261c9e44db03fe285a5d090c532dfcd refs/heads/develop
9fc771859415fa44145720ff5079851943b2c020 refs/heads/lane-0428-075-perses-seam
9fc771859415fa44145720ff5079851943b2c020 refs/pull/1575/head
```

PR #1575 is OPEN, ready (not draft), base `develop` at `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`, exact head `9fc771859415fa44145720ff5079851943b2c020`, and GitHub reports `MERGEABLE` / `CLEAN`. `bcae1e8c` is carried by the Hopf-4 merge commit `f24041a6413497b5a47116f6c2faee41c35884d0`.

The delta after `f24041a6413497b5a47116f6c2faee41c35884d0` contains exactly two lane commits:

- `87b287259a1d6f13fa255877558a5d027078a0b1` — removes process history from comments while retaining technical justification.
- `9fc771859415fa44145720ff5079851943b2c020` — fail-closed validation, lossless valid serialization coverage, and three regression cases.

Changed files in that delta: `internal/application/manifest_render.go`, `internal/application/manifest_test.go`, `internal/application/manifest_validation.go`, `internal/capability/perses.go`, `internal/metrics/perses_contract_test.go`. No `.github/**` files changed.

## Review against the correction requirements

1. **Fail-closed selection:** `internal/application/manifest_validation.go:508-515` rejects `Perses=true` without `ObservabilityManagementUI` before the generic “management UI not selected” early return. The error identifies the required relationship; the invalid selection no longer silently returns nil.
2. **Lossless valid serialization:** `internal/application/manifest_render.go:106-111` emits the management UI block and Perses selection together. `internal/application/manifest_test.go:168-190` serializes and parses canonical YAML and asserts both flags survive. The serializer argument is equivalent to the guarding field and preserves the valid case.
3. **Three regression cases:** `internal/application/manifest_test.go:156-166` asserts `(perses=true, management_ui=false)` fails; `:168-190` asserts `(true,true)` round-trips; `:193-214` asserts `(false,false)` remains a valid baseline without an observability block. Existing assertions were not weakened in the reviewed delta.
4. **Comment cleanup:** the two comment-only edits remove process/history references while retaining the technical contract explanation.

## Exact-head CI and GitHub state

- Exact-head workflow run `44029539129`: `completed / success` on `9fc771859415fa44145720ff5079851943b2c020`.
- ci-cost-note: run 44029539129, runner-minutes approx 35 (sum of rounded durations for completed, non-skipped jobs in the run summary).
- Required `PR Selected Checks`: SUCCESS, GitHub Actions integration `15368`, exact candidate SHA. `gh pr checks --required` reports pass.
- `PR · Trusted Plan`, `PR · Native gate plan`, Go unit shards, `go-build`, `go-vet`, `Exact Candidate`, selected runtime Docker lifecycle, source-format, docs and pages checks all completed successfully. Native gates outside the selected runtime plan were skipped by selection; the selected Docker lifecycle gate ran and passed.
- PR review threads: zero unresolved.
- No GitHub review was posted; this account cannot formally review its own PR. Verdict is recorded here for the owner’s independent cross-check.

## Verdict and merge disposition

**CODEX-REVIEW: APPROVE** at exact head `9fc771859415fa44145720ff5079851943b2c020`. The corrected validation, valid serialization, and all three regression cases match the stated acceptance points; the exact-head checks and current merge state are clean.

**CODEX-MERGE: STOP — not executed.** `/home/marcel/.config/baseharbor-coordinator/COST_CONTROL.md` currently says “do not merge PRs” while the cost-allocation clarification is pending. That binding stop blocks the otherwise-ready squash merge. No PR mutation was performed. Resume the head-guarded squash merge only when that stop is cleared; recheck develop/head, required checks and ruleset immediately before it.

## repo-rule compliance

- Candidate inspection was read-only; no product file, PR, review, or branch was changed.
- No local test suite was run; hosted exact-head CI evidence was inspected.
- No merge, bypass, force-push, workflow dispatch, or subagent was used.

END: welle1f review complete; merge held by the binding cost stop.
