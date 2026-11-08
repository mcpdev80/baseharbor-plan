# CODEX-REVIEW 0427-163 — PR #1487

## PLAN

1. Verify the live PR head, develop head, ancestry, and hosted run for the exact candidate.
2. Inspect the shared-Core detector, container inventory semantics, error path, tests, and CI selection at that SHA.
3. Record the verdict and a repair recipe in this planning evidence, then verify the published file and unchanged candidate head.

## ROLLE: REVIEW

## Verdict: KORREKTUR

Candidate reviewed: `9572bdb3ae83db6da6252fcdc4d865e0a9fbbf35`.

### Remote witnesses

- PR #1487 is OPEN, base `develop`, head `9572bdb3ae83db6da6252fcdc4d865e0a9fbbf35`, and GitHub reports `mergeStateStatus=CLEAN`.
- `git ls-remote` witnesses: develop `3187cea15728143146905c7238ad6e280ca11b3e`; PR head `9572bdb3ae83db6da6252fcdc4d865e0a9fbbf35`.
- The candidate's merge base with the current develop head is `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`; current develop `3187cea15728143146905c7238ad6e280ca11b3e` is not an ancestor of this candidate. The reported CLEAN state does not mean the candidate includes this newer develop head. Rebase and rerun the required checks before accepting the final candidate.
- Hosted run `42503646942` is terminal SUCCESS on the exact candidate SHA. `go-unit-tests` and `runtime-provider-package-tests` passed. The native Keycloak/Core jobs were skipped; they are not counted as executed evidence for this change.

### Findings

1. **Stopped foreign Core containers also trip the conflict gate.** In `internal/runtime/compose_resources.go:455-515`, `ListRuntimeContainers` enumerates with `container ls -aq`, so its result includes stopped containers; it also populates each result's `Running` field from inspected state. In `internal/runtime/shared_core_conflict.go:57-65`, the new detector filters only by project label and never checks `container.Running`. A stopped container labelled `bh-boot-shared` therefore blocks a new target as if the other target's Core were running. The added tests only pass `Running: true`, so they miss this case.
2. **The gate drops runtime-resolution errors.** `cmd/baha/runtime.go:274-285` converts every `detectRuntimeForTarget` error into “no live engine binding” and skips the gate. The detector can return errors for remote-target binding and target-engine validation/resolution (`cmd/baha/target.go:657-670`). A genuine absence of a local binding should be distinguishable from a failed inspection/validation; otherwise the conflict check is bypassed on an unknown state. The subsequent materialize path propagates errors from the container listing itself, which is good, but does not repair this earlier fail-open branch.
3. **Owner messaging and same-target exclusion are present.** `SharedCoreOwnerConflict.Error` names the observed owner and gives `baha use` / `baha up --target` choices (`internal/runtime/shared_core_conflict.go:35-40`). The exact own project is excluded at lines 62-64, and the test covers a running container from that same project. The gate is invoked before the existing-runtime selection/materialization in `cmd/baha/runtime.go:176-190`.
4. **The gate tests are in hosted CI.** The foreign-owner and same-owner tests are in `internal/runtime/shared_core_conflict_test.go`; run `42503646942` passed both the repository `go-unit-tests` and `runtime-provider-package-tests` groups. The CI selection maps `go-unit-tests` to `scripts/pr-unit-database.sh` and `runtime-provider-package-tests` to `go test ./internal/runtime/... ./internal/health ./internal/providers/runtime/podman` in `.github/workflows/ci.yml:915-945`. The CLI message test constructs the conflict value directly rather than invoking the production up entrypoint, so it proves formatting, not that the CLI reaches the gate.

### Umsetzbares Lösungsrezept

- **Datei:** `internal/runtime/shared_core_conflict.go`. Ignore containers whose `Running` field is false before classifying their project. Keep exact same-project exclusion.
- **Datei:** `cmd/baha/runtime.go` around `detectSharedCoreOwnerConflict`. Treat only an explicitly identified “no local engine binding” case as no conflict. Propagate engine resolution/validation/inspection errors so an unknown state cannot silently skip the guard.
- **Datei:** `internal/runtime/shared_core_conflict_test.go`. Add a stopped foreign Core case that returns no conflict, retain a running foreign Core case that names the owner, and retain the running same-target case that allows re-up. Add a detector/materialization-path regression proving runtime-resolution failure does not proceed as if conflict inspection succeeded. Keep the CLI assertion, and add an entrypoint-level regression if the existing test seam permits it.
- **CI requirement:** these Go tests must remain selected by the hosted `go-unit-tests` or `runtime-provider-package-tests` job on `pull_request`. Rebase onto the current develop head and inspect terminal results for the exact rebased SHA; do not count skipped native jobs as passes.
- **Stop criterion:** approve only when stopped foreign containers do not block, a running foreign Core blocks with its owner and recovery options, same-target re-up proceeds, detector uncertainty fails closed, and the named regressions pass in hosted CI on the exact rebased head.

## repo-rule compliance

Read-only review of the product candidate; no product files or CI workflows were changed. Evidence is stored in baseharbor-plan.

## END 0427-163 REVIEW

KORREKTUR — candidate `9572bdb3ae83db6da6252fcdc4d865e0a9fbbf35`; hosted run `42503646942` passed, but stopped-container filtering and fail-closed runtime-resolution handling need correction, then rebase and rerun against current develop.
