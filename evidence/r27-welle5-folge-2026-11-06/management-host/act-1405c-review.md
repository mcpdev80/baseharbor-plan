# CODEX-REVIEW 0427-036 / PR #1405 rereview

Role: CODEX-REVIEW. Candidate PR head: `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede`. Mission base: `develop` at `934be499b9d2d894f80889fc23cd811884c8aec4`.

## PLAN

1. Confirm the real planning repository and fresh remote develop/PR SHAs.
2. Inspect the exact serve.go candidate diff and verify both RuntimeAppName paths use the same non-nil context.
3. Review round-8 regression evidence and verify behavioral red/green witnesses.
4. Inspect exact-head run 42336074504 and check required cells.
5. Write a SHA-specific verdict, publish evidence, verify origin/main, and post END.

## Candidate and implementation review

Fresh first remote witness, from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1405/head`:

```text
934be499b9d2d894f80889fc23cd811884c8aec4\trefs/heads/develop
5b8d0f5745c55fd8be89d5dc53edb4e9b145eede\trefs/pull/1405/head
```

A second fresh witness confirmed `refs/heads/work/r27-management-host` and `refs/pull/1405/head` both point to `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede`. PR #1405 is OPEN, non-draft, targets `develop`, and is mergeable.

The exact `cmd/baha/serve.go` change initializes `startup := ctx` before the `RuntimeAppName == ""` branch (candidate lines 48–50), applies the connector target override to that context in the installation branch (lines 51–54), applies management-host attachment to that same context when attaching (lines 100–105), and passes it to `controlplaneruntime.Run` (line 110). For a valid non-nil CLI context there is no remaining nil path in either branch. No product changes were made during this review.

The new `TestServeStartUpPathNeverReceivesNilStartupContext` in `cmd/baha/serve_test.go:34-108` exercises `RuntimeAppName != ""`, reaches serve startup, and verifies shutdown after context cancellation. Round-8 evidence records behavior-red exit 1 on the no-fix head and green exit 0 on the fixed head; the failure is the nil-context panic in `controlplaneruntime/server_run.go:369`, not a compile failure. The exact-head CI package run independently confirms the test passes. The previously reviewed round-6/7 ownership red-first proof remains accepted and is not being requested again.

Round-8 evidence also contains a later remote witness of `5fc7e14a...`; the fresh live refs in this review show both source branch and PR head at `5b8d0f57...`, the mission SHA. The fresh live witness is used for this verdict.

## Candidate-base provenance finding

The fix commit `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede` has parent `0f08b877f4152c156b219ff6d13ab05ee6b082de`. The current fetched mission base `934be499b9d2d894f80889fc23cd811884c8aec4` is NOT an ancestor of the PR head: `git merge-base --is-ancestor 934be499... 5b8d0f57...` returned 1. The actual merge base is `dddf0d7823f6eec161ad518bbced626fa9efe52e`; the symmetric difference contains 62 base-only commits and 6 candidate-only commits. The source branch and PR head agree, but the PR update was made on the old `0f08b877` candidate without first incorporating the exact current `develop` head. This fails the required base-provenance/up-to-date gate.

The candidate-side log contains the management-host chain (`a87f83776`, `64d93e945`, `3a80ed040`, `5b8c54222`, `0f08b877f`) and the rereview fix `5b8d0f574`; no unrelated PR candidate is present. The issue is the missing current base ancestry, not an unrelated task commit.

## Exact-head CI

Run `42336074504` (`CI · PR #1405`) is terminal `success` at exact head `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede`.

- `PR · Validation · go-unit-tests` job `128293256158`: success. The candidate’s `scripts/pr-unit-database.sh` runs `go test ./... -count=1`; the log reports `ok github.com/mcpdev80/baseharbor/cmd/baha 393.083s`, so the regression is included.
- `go-build`, `go-vet`, `authority-package-tests`, source format, workflow policy, trusted plan, and `PR Selected Checks` succeeded.
- `Targeted HA · docker` job `128293220825` and `Targeted HA · podman` job `128293220641` were skipped. Their current workflow conditions are push-ref limited; this rereview does not treat those owner-scoped runtime cells as a defect in this task because the exact-head unit and focused package coverage passed.
- No check failed; no workflow rerun or dispatch was performed.

## Verdict and correction recipe

REJECT candidate `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede` on branch-provenance grounds. The startup fix and focused regression are correct, and the exact-head CI run is green, but the candidate does not contain its stated current base `934be499b`.

Correction recipe: update the existing branch `work/r27-management-host` by merging the exact current `develop` head `934be499b9d2d894f80889fc23cd811884c8aec4` into it; do not create a second branch. Before the next PR update, record the base SHA, verify it is an ancestor of the new candidate, and record `git log --oneline 934be499b..HEAD` showing only the management-host task chain plus its base-refresh merge. Run exact-head required CI to terminal and request CODEX-REVIEW on the resulting SHA. Stop until the current-base ancestry and exact-head evidence are verified.

## Repo-rule compliance

- Read-only product review: no product file edits, no branch update, no merge, no tests run locally, no workflow rerun/dispatch, no runner/VM/container work, and no subagents.
- Evidence is in the real `baseharbor-plan` repository. The existing unrelated untracked `evidence/r27-welle5-folge-2026-11-06/management-host/round-8-serve-startup.md` was left untouched.
- No markdown checkbox syntax appears in this file.

## END

END_DONE codex-1405-rereview-c: verdict=REJECT head=5b8d0f5745c55fd8be89d5dc53edb4e9b145eede startup=beid-pfade-nichtnil ok regression=ROT-ohne-fix/GRUEN-mit-fix ci=42336074504-success rezept=merge exact develop 934be499 into existing branch and rerun exact-head CI; stop until ancestry is verified.

## Planning repository and publication witness

Before this first evidence commit, `git remote -v` in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` returned:

```text
origin\thttps://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin\thttps://github.com/mcpdev80/baseharbor-plan.git (push)
```

Exact `git ls-remote origin refs/heads/main` output captured immediately before publishing this evidence:

```text
a18740ece17d7d68c4a13346e3cbe096aefb00b9	refs/heads/main
```
