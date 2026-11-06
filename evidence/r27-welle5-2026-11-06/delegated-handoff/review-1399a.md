# CODEX-REVIEW 1399a — delegated delivery handoff

- Review scope: owner message naming `coordinator/missions/codex-r1399a.txt`;
  that file was not present in the workspace. I used the explicit owner message,
  task card, and published round-1 evidence as the review inputs.
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1399, base `develop`
- Reviewed head: `88cee2b21d7fc91b602e370d448316d2cf8494ab`
- Base `develop`: `f01d2fbdea6b93af6e06ca6297d04065b6acf701`
- Review date: 2026-11-06
- Verdict: **REJECT**

## Candidate, scope, and dependencies

`git ls-remote origin` reported `88cee2b21d7fc91b602e370d448316d2cf8494ab`
for `refs/pull/1399/head` and `f01d2fbdea6b93af6e06ca6297d04065b6acf701` for
`refs/heads/develop`. `git merge-base --is-ancestor origin/develop
origin/pr/1399` returned 0. The PR API reported the same head, base `develop`,
and an open, mergeable PR.

The task card lists four dependencies; each was checked in Planning and has
`kanban_status: closed`:

- `t-20261017-release-0-4-27-updates`
- `t-20261018-r27-delivery-boundary`
- `t-20261018-r27-stage-versions`
- `t-20261022-r27-ci-delivery`

Name-only diff from `origin/develop` to the candidate:

- `internal/delivery/handoff.go`
- `internal/delivery/handoff_test.go`

This matches the card's reserved write paths. No product files were changed by
this review.

## Published evidence and gates

The round-1 evidence is published on `origin/main` at
`100644 blob c9c5a2af336b31cc02a3bf6b75bf04f62e461c3f`.
It records direct and delegated fixture matrices for promote/apply/repair/destroy,
foreign tracking metadata preservation, drift refusal, a source mutant that
drops the tracking clone, and its restored counterprobe. It also records local
race-20, build, vet, and formatting results.

I independently verified hosted run `42150874541`: terminal `completed /
success`, with `headSha` equal to the reviewed commit. `PR Selected Checks` is
terminal success. Workflow policy, trusted plan, source format, delivery-package
tests, CLI build, CLI guided tests, and CLI vet succeeded; path-inapplicable HA,
validate, release-preflight, public-contract, and selected-runtime jobs were
skipped.

## Blocking finding: external status can be asserted without proof or despite drift

The card requires `synced` and `healthy` to be displayed only with actual
external evidence and forbids false success claims. `DriftObservation` documents
that those flags must come from actual external evidence. The type defines a
`validate()` method requiring both digests and evidence, but that method is not
called by `HandOff` or request validation.

In `internal/delivery/handoff.go`, the delegated path only rejects a partial
digest/evidence tuple when the evidence string is empty. It then copies
`drift.Synced` and `drift.Healthy` into the output without validating their
provenance. Thus a zero-digest, empty-evidence observation with `Synced: true`
or `Healthy: true` is returned as an observed, successful handoff. Also, on a
drifted observation, lines 201–202 copy those flags through unchanged. The test
claims “a drifted resource never renders synced/healthy,” but its fixture leaves
both booleans false, so it does not exercise that case.

### Required correction recipe

Fail closed when either status flag is asserted without a complete external
observation (both desired and observed digests plus evidence). For a drifted
observation, do not render `synced` or `healthy` as true. Add negative cases for
status flags with no evidence and for mismatched digests with true status flags;
retain the in-sync evidence-backed positive case. Re-run the relevant delivery
package checks and hosted gates on the corrected exact head.

## Repository-rule compliance

Read-only review only: no PR mutation, merge, product edit, or test-source
change. The candidate identity and evidence references above are exact.

## Conclusion

The two-file scope, dependency state, tracking preservation, drift refusal, and
hosted checks are supported by evidence. However, delegated `synced`/`healthy`
flags are passed through without evidence validation and can remain true on a
drifted result, contrary to the task contract. **REJECT** until status rendering
is fail-closed and the missing negative cases are covered.
