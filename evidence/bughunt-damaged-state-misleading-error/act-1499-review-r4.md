# CODEX-REVIEW 0427-159 r4 — PR #1499

## PLAN

1. Verify the live PR head, develop base, ancestry, changed paths, and exact-head hosted run.
2. Check the real damaged-state ownership path and each r3 finding F1–F4 against candidate source and regression tests.
3. Distinguish executed native cells from skipped cells and record the exact hosted status.
4. Publish this SHA-specific verdict and post the review result.

## Verdict

**ROLLE: REVIEW — KORREKTUR; approval withheld.** The candidate closes F3: a registry-listing orphan without a retained owner is returned as an unknown-owner conflict, and a new production-path regression proves it is not attributed to the requested app. F2's malformed-directory filter is implemented, but the test does not prove the valid-UUID damage case or the record/directory identity-mismatch boundary requested in the prior recipe. F1 is not established: the claimed owned-app registry regression is absent, while the extant registry test fabricates a damaged error, fills its identity, and calls enrichment directly. The real ownerless registry path deliberately returns before network inspection. F4's new tests are routed through hosted Go jobs, but that does not provide regression coverage for F1 or the missing F2 boundary.

### Exact candidate and ancestry

- Repository: `mcpdev80/baseharbor`; PR #1499 is open at head `43fab0e5737f6e1bc587f8783467bed0ecb01db2`, base `develop` at `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- `git ls-remote` confirmed develop `b3a8042d18ea60f162a32a51df34a499cad6a237` and PR head `43fab0e5737f6e1bc587f8783467bed0ecb01db2`. `merge-base --is-ancestor develop head` returned 0.
- `develop..head` contains only this chain's three commits: `61f69c20`, `79f1a8f1`, `43fab0e5`; no foreign commit is carried. The PR reports mergeable.
- The 13 changed paths are under `cmd/baha`, `internal/application`, `internal/deployment`, and `internal/runtime`; no `.github/**` path changed.

### F1 — Registry record-plus-network proof remains incomplete

`cmd/baha/app_context.go:223-243` now recognizes ownerless registry damage and returns it as unknown owner without inspecting or attributing the requested app's network. This is the correct F3 safety rule. It also means the real missing-record registry path cannot produce the previous record-plus-network diagnosis unless an independently trusted identity source establishes which app owns that record.

The only registry-named F1 test, `TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent` at `cmd/baha/app_lifecycle_damaged_state_test.go:329-396`, constructs a synthetic `DamagedDeploymentError`, manually adds the requested app's identity, and calls `EnrichNetworkForOwnIdentity`; it does not call `FindDeployment` or `resolvedRepositoryApplication`. The production-path foreign-orphan test at lines 398-473 verifies that requested-app attribution is withheld, but there is no `TestRegistryOwnedAppReportsExactNetwork` in the candidate despite round-4 claiming one. The older `TestUpFailsClosedNamingRecordAndNetworkAbsent` at lines 221-327 checks only whether the error string contains `network`; its temporary directory is itself created beneath a test name containing “NetworkAbsent,” so that substring is not a reliable diagnostic assertion.

**Disposition:** F1 is not proven on the production path. Keep F3's no-false-attribution behavior. If no trusted identity can bind a deleted-record directory to an app, report it as unknown-owner and do not claim the requested app's network is part of that orphan. Separately, retain an owned-app production-path case where ownership is established from a surviving authoritative source and assert the exact absent network name/state. If such a source cannot exist for the deleted-record case, document the acceptance boundary and ensure the user-facing unknown-owner message is the intended diagnosis.

**Correction recipe:** In `cmd/baha/app_context.go:223-243` and `cmd/baha/app_lifecycle_damaged_state_test.go:329-396`, preserve the ownerless early return. Add a real `resolvedRepositoryApplication`/`FindDeployment` regression for an owned damaged deployment only if a trusted retained identity can establish ownership; assert the exact `NetworkName` and absent state, not a generic substring. For an ownerless UUID directory, assert `Application == "unknown"`, no requested-app identity, and no requested-app network claim. Remove or strengthen the synthetic-only F1 test so it cannot be mistaken for production-path evidence. Stop when the two ownership cases are distinct and the message matches the contract without false attribution.

### F2 — Shape gate implemented; boundary regression is incomplete

`internal/deployment/deployment_list.go:67-100` calls `ValidateDeploymentID` before `DamagedDirectoryState`, so malformed directory names are skipped before they can be advertised as deployment damage. The new `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` at `internal/deployment/damaged_namespace_network_test.go:179-224` creates a valid UUID directory and a malformed directory, but it only iterates warnings to ensure none are damaged. It does not assert that the valid UUID entry is flagged as damaged; its comment acknowledges no Core owner was seeded, so that entry is only incomplete. No candidate test targets a `deployment.json` identity that disagrees with its directory name (search of `internal/deployment/*test.go` found no such regression).

**Correction recipe:** Extend `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` to seed the required owner state and assert the valid UUID damaged entry remains surfaced while the malformed signature is discarded. Add a record/path mismatch fixture and assert it fails closed as an integrity mismatch without being reclassified as a damaged orphan or silently accepted. Stop when valid damaged, malformed, and mismatched identities have distinct asserted outcomes.

### F3 — Closed on the production path

`internal/deployment/deployment_list.go:71-100` returns a damaged listing error with target and deployment UUID but no app identity. `cmd/baha/app_context.go:223-243` detects that ownerless error, changes the visible application label to `unknown`, clears the app ID/environment, and returns without adding the requested app's network. `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` at `cmd/baha/app_lifecycle_damaged_state_test.go:398-473` seeds a valid-UUID foreign orphan and calls the real `resolvedRepositoryApplication` path for a different app whose network inspector reports absent; it verifies the request app identity/network are not attached. This meets the ownership-before-attribution correction for unknown-owner registry damage.

### F4 — CI routing is real, with coverage gaps above

The exact-head pull-request run executed and passed `PR · Validation · go-unit-tests` (job `128942112081`) and `deployment-package-tests` (`128942112137`), which cover the new `cmd/baha` and `internal/deployment` tests. No workflow change is requested. These jobs establish routing for the tests that exist; they do not substitute for the missing production-path F1 proof or the unasserted F2 valid/mismatched cases.

### Hosted state and native-cell truth

Run `42549625424` is terminal `completed/success` on the exact head `43fab0e5737f6e1bc587f8783467bed0ecb01db2` under `pull_request`. `PR Selected Checks` (`128945160097`) passed. Go unit, deployment-package, runtime-provider, build, vet, formatting, source-format, focused-Python, trusted-plan, and native-impact-selection jobs passed. Native destroy-retry Docker (`128942092360`) and Podman (`128942092295`) jobs executed and passed.

The `PR · Native Keycloak/Core · ${{ matrix.runtime }}` job (`128942113184`) was **skipped**, not executed. The run had zero failed jobs, but “26 jobs terminal” does not mean every native cell ran. This is an honest skipped state, not a green native Keycloak/Core result; it is not itself a source finding for this write-set.

## Stop criteria

- F1: distinct, production-path owned and ownerless cases; only a trusted owner may receive an app-specific network diagnosis, and the exact network must be asserted.
- F2: valid UUID damaged entry remains detectable; malformed names are discarded; record/directory mismatch is rejected and regression-tested.
- F3: retain the real foreign-orphan no-attribution regression.
- F4: required regression tests pass in the existing `go-unit-tests` and `deployment-package-tests` jobs on the exact candidate head.

## END

END_DONE 0427-159-r4-review: KORREKTUR — PR #1499 head `43fab0e5737f6e1bc587f8783467bed0ecb01db2`; F3 closed, F1 unproven on production path, F2 regression incomplete; exact-head run `42549625424` success with Native Keycloak/Core skipped; evidence publication SHA to follow.
