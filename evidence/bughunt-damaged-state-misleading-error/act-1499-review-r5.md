# CODEX-REVIEW 0427-159 r5 — PR #1499

ROLLE: REVIEW
URTEIL: korrektur

## PLAN

1. Fetch the live PR head and develop head; verify exact ancestry and candidate-only commit range.
2. Inspect the two F1 outcomes and the F2 malformed/mismatch boundaries in the production resolver and regression tests.
3. Run the four targeted regressions locally, then verify the exact-head hosted jobs, trigger, and skipped-cell state.
4. Publish this SHA-specific verdict in the canonical planning evidence repository.

## Exact candidate

Repository: `mcpdev80/baseharbor`; PR #1499; task 0427-159.

- PR head: `794ffe435e14276a88d918fd9cc5029ae1f6afc7`.
- Live develop head: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 794ffe435e14276a88d918fd9cc5029ae1f6afc7`: exit 0.
- `git log --oneline b3a8042d18ea60f162a32a51df34a499cad6a237..794ffe435e14276a88d918fd9cc5029ae1f6afc7`: four commits, all on the 0427-159 chain (`61f69c20`, `79f1a8f1`, `43fab0e5`, `794ffe43`); no foreign commit.
- PR is open and mergeable. Product diff contains no `.github/**` paths.

## Verdict and findings

**KORREKTUR; approval withheld.** F2's two requested boundaries are now covered by concrete tests. F1 still does not establish an ownership binding for the “owned app” half, and the ownerless regression does not assert the exact promised unknown-owner result.

### F1 — attribution can still be invented by the repository fallback

The new `TestRegistryOwnedAppReportsExactNetwork` at `cmd/baha/app_lifecycle_damaged_state_test.go:412-473` does call the production `resolvedRepositoryApplication` resolver. However, its damaged directory is named `damaged-owned`, not a canonical deployment UUID (`:436-440`). The registry listing deliberately discards that entry at `internal/deployment/deployment_list.go:71-83`. The resolver then reaches its second, target-wide scan at `cmd/baha/app_context.go:265-300`; that scan returns the first damaged directory and labels it with the current manifest's identity (`:284-300`). The fixture seeds only a Core Target owner and an arbitrary `application.env` (`X=Y`); neither binds this directory to `owned-app`. Its fake network inspector returns absent, so the test proves the resolver can attach the requested app's network to an otherwise unidentified directory, not that this is the directory for that app.

The guard for registry errors at `cmd/baha/app_context.go:223-243` correctly changes an ownerless listing error to `Application = "unknown"` and clears the requested app identity. But a malformed directory bypasses that guard because listing drops it before returning an error, then the repository namespace scan assigns it to the request. This leaves the false-attribution path open through a second resolution path.

`TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` at `cmd/baha/app_lifecycle_damaged_state_test.go:489-553` exercises the real resolver with a canonical UUID orphan, but only asserts that `Application` is not `requested-app`, `ApplicationID` is not the request ID, and network state is not `Absent`. It does not assert `Application == "unknown"`, blank environment, blank `NetworkName`, or record-only error text. The production code sets the unknown identity at `app_context.go:237-242`, but this regression does not lock the full contract.

### F2 — boundary tests are materially complete

`internal/deployment/deployment_list.go:71-83` validates the canonical deployment ID before any damaged-state classification. `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` at `internal/deployment/damaged_namespace_network_test.go:190-263` seeds a genuine UUIDv4 damaged directory and a malformed damaged directory, asserts the valid UUID remains visible as damaged, and asserts the malformed name is neither surfaced nor returned as a record.

`TestListDeploymentRecordsDiscardsRecordDirectoryMismatch` at `internal/deployment/damaged_namespace_network_test.go:269-337` uses two valid UUIDv4 identities, puts one ID in the other ID's directory, and asserts the record is not accepted, is not reclassified as an orphan, and produces the storage-path mismatch warning. The production check is `internal/deployment/deployment_store.go:569-570`.

### Local and hosted verification

The four targeted tests were run against this exact worktree and passed:

```text
go test ./cmd/baha -run '^(TestRegistryOwnedAppReportsExactNetwork|TestRegistryForeignOrphanNoFalseAttributionToRequestedApp)$' -count=1
ok   github.com/mcpdev80/baseharbor/cmd/baha 0.009s

go test ./internal/deployment -run '^(TestListDeploymentRecordsDiscardsMalformedDirectoryNames|TestListDeploymentRecordsDiscardsRecordDirectoryMismatch)$' -count=1
ok   github.com/mcpdev80/baseharbor/internal/deployment 0.007s
```

Hosted run `42559458982` is terminal `completed/success` on the exact PR head `794ffe435e14276a88d918fd9cc5029ae1f6afc7` (`pull_request`). It reports 14 successful jobs and 12 skipped jobs, with no failure or pending job. `PR Selected Checks` passed (job `128975784564`); `PR · Validation · go-unit-tests` passed (job `128972510666`); `PR · Validation · deployment-package-tests` passed (job `128972510485`). The trigger is `pull_request` for `develop`/`main`, `.github/workflows/ci.yml:12-16`. `go-unit-tests` invokes `scripts/pr-unit-database.sh` (`ci.yml:915`), which runs `go test ./... -count=1` (`scripts/pr-unit-database.sh:33`). `deployment-package-tests` is dispatched at `ci.yml:964-970` and maps to `go test ./internal/deployment/... -count=1` through `scripts/pr-check-runner.py:170-175`.

The Native Keycloak/Core job was skipped, as were Targeted HA Docker and Podman; these are not green native executions. Native destroy-retry Docker and Podman did execute and pass (jobs `128972485289` and `128972485210`). The skips are reported as skips, not counted as passes. No workflow was edited or rerun.

## Actionable correction recipe

- In `cmd/baha/app_context.go:265-300`, do not bind a target-wide orphan to the current repository manifest solely because the repository resolver has a manifest. Require an authenticated retained identity that associates the damaged directory with that application. If no such source survives deletion of `deployment.json`, return the explicit unknown-owner, record-only error and move the app-specific network claim to a follow-up contract that adds a durable ownership binding.
- In `cmd/baha/app_lifecycle_damaged_state_test.go:412-473`, replace the malformed `damaged-owned` fixture with a case where the trusted ownership source is explicitly present and read by production code. If this path has no trusted source, change it to assert unknown owner and no network attribution. Add a regression where a malformed foreign orphan coexists with a different repository manifest; it must not acquire that app's identity or network.
- Strengthen `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` at `cmd/baha/app_lifecycle_damaged_state_test.go:541-553` to assert exact `Application == "unknown"`, empty `ApplicationID` and `Environment`, no `NetworkName`, no network state, and a record-only error message.
- Keep the two F2 tests and their hosted routing. Stop when both orphan cases are exercised through the production resolver, an unbound directory cannot receive the requesting app's identity/network, a trusted binding is required for the owned case, and the exact-head hosted selected checks remain successful.

## repo-rule compliance

- Product candidate was read-only; no product files or PR refs were changed.
- Evidence is in canonical `baseharbor-plan`, whose origin is `https://github.com/mcpdev80/baseharbor-plan.git`.
- No `.github/**` edits, CI reruns, or workflow dispatches were made.

END_DONE 0427-159-r5-review: KORREKTUR PR #1499 head 794ffe435; F2 covered, F1 still permits request-manifest attribution of an unbound orphan; exact run 42559458982 success with native Keycloak/Core skipped.
