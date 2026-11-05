# CODEX-REVIEW — stage versions, PR #1391

- Review date: 2026-11-05
- Verdict: **REJECT** — the actual lifecycle path drops independent reference dimensions; the required mutation evidence is not demonstrated.
- Candidate: `13192efa5d5ce1d4a855a43ceb8e9000ded5188c`
- Base: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- PR #1391: open, head `13192efa5d5ce1d4a855a43ceb8e9000ded5188c`, branch `work/r27-stage-versions`.
- Remote witness: `git ls-remote origin refs/heads/work/r27-stage-versions` returned `13192efa5d5ce1d4a855a43ceb8e9000ded5188c` exactly.
- Hosted run: [42103327299](https://github.com/mcpdev80/baseharbor/actions/runs/42103327299) is terminal `completed / success` at the exact candidate SHA.
- Diff: five files (`cmd/baha/app.go`, `cmd/baha/deployment_record.go`, `internal/deployment/deployment_store.go`, `internal/deployment/stage_versions.go`, `internal/deployment/stage_versions_matrix_test.go`); no migration SQL changed or added.

## Criterion results

1. **Three-reference matrix / race-20 — not independently verified.** The matrix tests directly call `SetReference`, rather than exercising the production lifecycle writers. I attempted the mission's `go test -race -count=20` focused matrix command twice; both attempts failed before assertions because `provisionOwnerForTarget` reported `write authoritative installation: read-only file system` (first at `stage_versions_matrix_test.go:74`). The hosted run is green, but does not resolve the concrete lifecycle defect below.
2. **Real lifecycle assembly — read; fails.** `recordDeploymentBeforeMutation` constructs intended+applied, but `recordAppliedDeploymentObservation` (deployment_record.go:233-258) constructs a fresh `References` map containing only applied, dropping intended and prior observed. More directly, `recordObservedDeployment` (lines 291-302) copies applied's release into a new observed entry, replaces the entire map, then restores intended only. It therefore deletes the applied dimension on convergence. Subsequent `DeploymentRecord.Stale()` sees no applied dimension and returns nil (stage_versions.go:82-96), so stale detection can silently pass. The helper-only `TestLifecycleOrdering` (stage_versions_matrix_test.go:272-324) calls `SetReference` directly and does not traverse these production functions, so it cannot catch this loss.
3. **Mutants — 0/2 demonstrated.** `TestMutantMergeCellsRed` (matrix_test.go:159-180) invokes the unmutated `SetReference` and checks expected good behavior; it does not apply the merged-fields mutant or show the test turning red. `TestStaleDetectionCellRed` (lines 182-209) seeds a missing observed field and checks the current implementation; it does not disable observer tracking or show stale detection turning red. The names/comments are not mutation-run evidence.
4. **Migration/down-SQL — not applicable.** No migration file is present in the candidate diff, so no down-SQL derivation is required for this change.
5. **State-owner seam — unchanged; journal/store data structure is intentionally extended.** `internal/deployment/deployment_owner_binding_test.go` has the same blob on develop and candidate: `ad79874e573587f1e8d2e1eb1b5b0e5cdaa763a7`. `internal/deployment/deployment_store.go` differs (`develop 7d16d70eea102292e8ebc0f9ae007463f3c3f060`; candidate `dae2fa96967a4a7c6756f79c9f6b705911f1c7e3`) to persist the new references. No existing owner-binding behavior file is changed. The diff is name-only as listed above.

## Correction recipe

- Make each production lifecycle update load/preserve the existing reference map and update only its owned dimension. `recordObservedDeployment` must retain applied while writing observed; `recordAppliedDeploymentObservation` must retain intended and observed while advancing applied. Preserve required absent/partial-state semantics and ensure stale detection compares the actual retained applied/observed values.
- Replace helper-direct lifecycle assertions with tests that call the actual submit/apply/convergence recording functions (or a real application up/apply lifecycle fixture), checking all three values after each transition and after reopen.
- Execute each required mutant as an isolated mutation run: (a) merge two fields in production lifecycle recording and capture the exact isolation assertion turning red; (b) disable observed tracking and capture stale detection turning red. Record terminal output for each.
- Re-run the focused matrix/race-20 in a writable test environment and attach terminal output for the final SHA; the hosted run already provides a green CI record for this current SHA.

Read-only review only. No product files changed and no PR action performed.
