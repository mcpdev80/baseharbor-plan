# CODEX-REVIEW 0427-150 — PR #1490

## PLAN

1. Verify the current PR head, base, selected checks, and exact-head hosted run.
2. Trace stale provider preference recovery, genuinely missing-instance handling, regression coverage, and changed-file scope.
3. Verify and record the draft-job routing issue as an owner-scope STATE finding.
4. Publish a SHA-specific verdict and actionable disposition in planning evidence.

## ROLLE: REVIEW

## Verdict: APPROVE

### Candidate and hosted evidence

- PR #1490 is OPEN, READY, MERGEABLE; exact head `35e5496203dc75fe6ad3bd4d1b97a44e98308792`; PR base SHA `1773491877a32e0a90f3537735216a7ba01657fd` on `develop`. Live `develop` at review time: `7af8d440e9a4dd1b633fdc44e4093109fe44ae37`.
- Exact-head run `42511516539` completed SUCCESS with 15 successful jobs and zero failed jobs. `PR Selected Checks` passed. The selected validation jobs included `go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `wizard-app-edit-tests`, `wizard-controller-tests`, and `wizard-provider-choice-tests`; Native destroy retry Docker and Podman also passed. Nonselected jobs reported `skipped` and are not counted as passing evidence.
- The six regression tests in `cmd/baha/app_provider_stale_instance_test.go` are included in the successful `go-unit-tests` execution (`scripts/pr-unit-database.sh` runs `go test ./... -count=1`) and focused wizard groups. Run `42511516539` is the terminal run for the exact reviewed candidate.

### Review findings

1. **A stale but live provider instance is re-resolved on the edit path.** `cmd/baha/app_edit.go:70-94` restores each stored explicit preference through `selectStoredProviderPreference`. That first tries the accepted projection selector; if the projection lost the instance, it obtains the provider kind when uniquely resolvable, reads the live provider registry, widens only the local choice snapshot with the exact instance, and retries the same requirement/instance selection (`cmd/baha/app_edit.go:122-190`; `cmd/baha/app_provider_choice.go:49-109`). The domain preference resolver independently re-adopts the exact still-registered BaseHarbor instance with its live scope/ownership (`internal/application/provider_preferences.go:236-295, 334-361`). The production-wiring regression `TestAppEditCommandStalePreferenceReResolvesFromLiveRegistry` covers the state-only sibling case.
2. **A genuinely unavailable instance is not silently accepted.** The edit surface names the missing instance, Target, and explicit automatic re-resolution action, and resets only that one stale choice to automatic so the user can continue (`cmd/baha/app_edit.go:79-91`). The authoritative preference validation still rejects an unresolved explicit preference with an actionable “no longer registered” / automatic re-resolution error (`internal/application/provider_preferences.go:299-303`). `TestProviderGoneInstanceFailsClosedWithNextStep` verifies the authority rejection and no registry publication; `TestAppEditCommandStalePreferenceDegradesToAutomaticWithNotice` verifies the CLI notice and reachable edit flow. Cancellation is write-free (`TestAppEditCommandStalePreferenceCancelWritesNothing`). This is an explicit recovery prompt, not a silent binding change.
3. **Regression coverage is durable and CI-selected.** The six tests cover live canonical re-resolution, missing-instance rejection with next step, stale edit resolution, state-only sibling residue, visible fallback when the preference is gone, and cancel without writes. They live in `cmd/baha/app_provider_stale_instance_test.go`; the exact-head run passed `go-unit-tests` (`go test ./...`) and the focused wizard app-edit/controller/provider-choice validations. The tests are not VM-only.
4. **Scope and contract surface are appropriate.** The product diff is nine files confined to `cmd/baha` app-edit/provider-choice/controller code and `internal/application` provider-preference/registry code, including the new regression file. It does not change `internal/machine/**`, public contracts, `.github/**`, or unrelated destroy/registry behavior.
5. **STATE — draft-only CI routing defect, owner scope.** The historical draft run `42509459864` on prior candidate `8ce26c9831b9fcc7eb92a352f4cbdb2713eaa6ee` failed `PR · Draft focused checks`; its log includes `stat /home/runner/work/baseharbor/baseharbor/cmd/baha.test: directory not found`, followed by analogous `*.test` pseudo-package failures. In `scripts/pr-draft-go-packages.py:12-17`, `go list -test` rows use `owner or name` without excluding generated `.test` packages; `.github/workflows/ci.yml:1205-1218` then passes the resulting selections to `go test`. This is an owner-scope CI routing finding; this review made no workflow/script change and did not rerun that draft job. It does not invalidate the current ready-phase exact-head run: run `42511516539` selected `go-unit-tests` and `PR Selected Checks`, both PASS.

### Umsetzbares Lösungsrezept

- **Product files:** no correction requested for this candidate. Preserve the exact-instance live-registry re-resolution, the actionable missing-instance notice/authority rejection, and the write-free cancellation regression.
- **Owner-scope follow-up:** in `scripts/pr-draft-go-packages.py:12-17`, exclude synthetic test-binary rows (for example import paths ending `.test`) and keep only real Go package import paths before emitting the draft selection consumed at `.github/workflows/ci.yml:1216-1218`. Add/retain a selector regression asserting no `.test` pseudo-package is emitted. This review does not modify those owner-owned files.
- **Acceptance stop criterion:** the reviewed candidate is acceptable on the exact current head because required selected checks and all six Go regressions passed. The separate draft-routing STATE should be fixed by the owner before relying on draft-only checks for future candidates; never count the skipped draft job in the ready-phase run as green evidence.

## repo-rule compliance

Read-only review of product source and hosted evidence. No product or workflow files were changed, and no checks were dispatched or rerun.

## END 0427-150 REVIEW

APPROVE — `35e5496203dc75fe6ad3bd4d1b97a44e98308792`; exact-head run `42511516539` passed, including `PR Selected Checks`; draft selector issue recorded as owner-scope STATE.
