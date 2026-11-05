# CODEX-REVIEW — PR #1382, Runde 2

**Verdikt: REJECT.** The isolated missing-`runtime.env` destroy cells now pass, but the owner check sits in `stopRepositoryWorkload`, a shared utility reached by backup and TLS-update paths as well as destruction. In those non-destroy operations a missing owner file returns `(false, nil)`, so callers can proceed as if the workload were already stopped. The exact-head required checks also ended red.

## Candidate and gates

- `mcpdev80/baseharbor` PR #1382 is OPEN, READY, base `develop`.
- Exact head: `3691173821384d028f33d81cc2c54a991d639f12`; parent/base: `512dcd721ac3fb739bfd4cb0b990fd68d6794762`.
- `git ls-remote origin refs/heads/develop refs/heads/work/r27-destroy-aborted-apply` returned those exact SHAs.
- Name-only diff: `cmd/baha/app_workload.go`, `cmd/baha/w154_destroy_aborted_apply_test.go`, `cmd/baha/w154_gegenprobe_test.go`, `cmd/baha/w154_runtime_dir_present_envmissing_test.go`, `internal/application/runtime_owner_write.go`. No `.github/` or `AGENTS.md` changes.
- Exact-head run `41945163860` is terminal `completed/failure`; `PR Selected Checks` failed. `PR · Source format`, `PR · Validation · cli-gofmt`, `cli-package-tests`, and `go-unit-tests` failed. Build, vet, guided tests, source contracts, focused Python and trusted plan passed; unrelated candidate/runtime/consumer/release jobs were skipped.
- The format failures name `cmd/baha/w154_runtime_dir_present_envmissing_test.go`. `TestAppEditCommandChecksGoSourceFormat` independently failed at `app_edit_apply_test.go:1076` with `unformatted command sources: w154_runtime_dir_present_envmissing_test.go`; both package and Go unit jobs include that failure. Line 20 of the new test has `//_authorization.go` where gofmt requires `// _authorization.go`.

## Call-site-only check and operational consequence

The new production API `application.VerifyRuntimeFileOwner` has one production call site: `cmd/baha/app_workload.go:640`, inside `stopRepositoryWorkload`. The test calls it at `w154_runtime_dir_present_envmissing_test.go:76`. The API itself is therefore not called directly from the shared runtime reader or writer.

However, `stopRepositoryWorkload` is a shared stop operation, not a destroy-only helper. Its call sites include:

- `cmd/baha/app_destroy_lifecycle.go:329` and `cmd/baha/app_runtime_retirement.go:138` — application destruction/retirement;
- `cmd/baha/runtime_destroy_all.go:468` — full destroy;
- `cmd/baha/app_backup_restore.go:122` — backup writer quiescence; also restore reset at `:544` and restore recovery/error cleanup at `:369`, `:378`, `:498`;
- `cmd/baha/app_tls.go:251` — TLS certificate update/rotation;
- `cmd/baha/app_mcp_lifecycle_acceptance_test.go:122` and `cmd/baha/app_workload_stop_test.go:180` — tests.

`VerifyRuntimeFileOwner` delegates to `existingPrivateRuntimeOwner`; a missing file yields `(false, nil)`. The new branch at `app_workload.go:640-644` then returns `(false, nil)` before inspecting runtime resources. At `app_backup_restore.go:120-137`, a false workload-stopped result does not abort backup; archive capture continues. Thus a running workload whose runtime env/owner file is absent can remain live while backup proceeds, without being recorded for restart. TLS update similarly uses the false result to skip workload restart and reports that no restart was required (`app_tls.go:256-271`). The new CLI regression constructs an absent env and checks destroy's return, but it does not prove there are no live owned containers for these other callers. The direct helper is confined to one function, but the effects are not confined to destroy/retire.

The existing `writePrivateRuntimeOwnerFile` remains on the normal runtime writer path through `internal/application/runtime_contract.go:699`; `existingPrivateRuntimeOwner` also remains used by that writer and by `telemetry_authorization.go` / `telemetry_projection_owner.go`. The new API did not alter those callers, but its containing stop helper is shared as listed above.

## Independent probes

- **Unmaterialized runtime directory, develop:** I copied the two candidate W154 regression files into a detached worktree at develop `512dcd721ac3fb739bfd4cb0b990fd68d6794762` without product changes. The focused test command failed both W154 tests. The literal destroy failure was `read application runtime environment: open .../state/demo/runtime/runtime.env: no such file or directory` (exit 1).
- **Runtime directory present, env absent, develop:** I copied the new test into the detached develop worktree and adapted only its precondition assertion to avoid calling the candidate-only API. The actual CLI destroy still failed with the same literal missing-`runtime.env` error (exit 1).
- **Candidate:** `go test ./cmd/baha -run 'TestW154(DestroyAfterProviderChangeAbortReturnsZero|GegenProbeAbortedApplyRecoversOnSecondRun|RetireWhenRuntimeDirPresentButRuntimeEnvMissing)|TestW138DestroyAfterRefusedApplyReturnsZero' -count=1` passed on the exact candidate worktree (`ok .../cmd/baha 13.968s`). This covers the original aborted-apply cell, the directory-present/env-missing cell, fresh-apply re-resolution, and the #1375 never-delivered cell.
- **Healthy stop cell:** `go test ./cmd/baha -run '^TestGuidedRepositoryWorkloadBackupStopPreservesCanonicalBackendAndOtherTargetOwners$' -count=1` passed on the candidate (`ok .../cmd/baha 0.030s`), including selected owned workload stop modes with an owned runtime env.
- These focused tests use isolated repository/target state and no external product deployment. Their passing result establishes the CLI decisions under those fixtures; it does not negate the shared-caller risk above.

## REZEPT

- **Files:** `cmd/baha/app_workload.go`; `internal/application/runtime_owner_write.go` only if the API must be reshaped; add/extend tests in `cmd/baha`.
- **Change:** Keep the missing-owner success behavior specific to the authorized destroy/retirement path. Restore strict failure in shared `stopRepositoryWorkload`, or split a destroy-only helper so backup, restore, TLS update, and ordinary stop paths do not infer “no workload” solely from a missing owner file. Before destroy returns success, retain an ownership/resource inventory proof that no owned runtime remains; do not turn uncertainty about a live workload into a no-op.
- **Test requirement:** Keep both W154 sick-state regressions red on develop and green on the final candidate; retain W138 never-delivered and normal healthy apply/destroy coverage. Add a mutation fixture with a running owned workload and missing `runtime.env`: backup must not capture while it is still running, TLS update must not report a no-op success, and destroy must retire only after its ownership/resource check. Run gofmt, source-format/readability, package tests, Go unit tests, build/vet and obtain a new terminally successful `PR Selected Checks` for the final exact head.
- **Stop criterion:** REJECT until the new missing-owner behavior is unreachable from backup/TLS/restore/ordinary stop callers or those callers fail closed and the running-workload mutation proves it. Also stop while any applicable required gate is red/nonterminal; no rerun or bypass is authorized by this review.

## END

END_DONE codex-r1382b: verdict=REJECT aufrufer=nicht nur destroy; backup/TLS/restore teilen den stop-pfad lauf=41945163860 failure | Die zwei kranken Zellen und die gesunde Backup-Stop-Probe bestehen im fokussierten Lauf, aber fehlender Runtime-Eigentümer lässt gemeinsam genutzte Backup-/TLS-Stopps fälschlich als erledigt weiterlaufen; Gates sind terminal rot.
