# round-2 — 0428-062 cli2-app-status (correcture, luna-r1 REQUEST CHANGES)

- Card: t-20261114-r28-cli2-app-status (0428-062)
- Mission: /tmp/opencode/mission-status-r2.md
- Lane: lane-0428-062-cli2-app-status (worker session)
- Reviewer recipe: evidence/r28-welle1-2026-11-15/cli2-app-status/act-luna-r1.md (kopf 03e280800)
- Candidate chain: PR #1614, base lane-0428-059-cli2-source-model

## PLAN
- Verify remote head 03e280800 on origin/refs/heads/lane-0428-062-cli2-app-status (FF only, refspec-push, ls-remote witness).
- Read recipe: retained-placement helper is test-only + mutates global env; wire retained per-provider placement into the production row builders (cmd/baha/app_versions_view.go collectSourceModelComponents, cmd/baha/app_versions_command.go componentRowsForRecord, cmd/baha/app_version_view.go collectVersionComponents); make declaredVersionServices a pure function of manifest plus placement; drop os.Setenv helper.
- Correcture: change ONLY 062-eigene files; do not touch app-interact/#1623 or export/#1625 files (foreign, not run).
- Tests: exercise the real production builders/command with two records whose retained PostgreSQL/Valkey placement differs from ambient org/environment config; assert ownership rows + CLI/JSON/MCP consistency + no concurrent leakage; cover prod path so CI runs them.
- Commit ONE own commit on lane-0428-062-cli2-app-status (FF from 03e280800), push via refspec, ls-remote witness.
- Push evidence to origin/main (second-to-last action).
- END with head SHA. No .github/**, no merge, no ready_for_review, no force-push, no subagent.

## BASE ATTESTATION
Authoritative planning repo (wrong-zone witness):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```
Product remote truth (NOT the quarantined workers checkout):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/lane-0428-062-cli2-app-status
03e280800b53b43cd08d6c468c0be7b55d45b1a8	refs/heads/lane-0428-062-cli2-app-status
```
Base cut-from: 03e280800b53b43cd08d6c468c0be7b55d45b1a8 (verified origin head, FF from eda0cd61). Ancestry: `git merge-base --is-ancestor 03e280800 HEAD` -> exit 0 on first commit. Only own commits will appear in `git log --oneline 03e280800..HEAD`.

## RESULT

### Correcture
- `declaredVersionServices` now takes a pure `placementClassifier` (manifest + provider → shared?) instead of reading ambient policy directly; the ambient classifier is retained as the no-retained fallback. No `os.Setenv`/`os.Unsetenv` global env mutation remains anywhere in the version builders.
- `retainedPlacementClassifier(record)` resolves PostgreSQL/Valkey by the record's retained `backend_placements` projection (`record.Applied.GeneratedState`) WITHOUT touching process-global state; a record without retained placement keeps the ambient fallback.
- `collectSourceModelComponents` (status + versions) and `componentRowsForRecord` (`app versions`) thread the classifier; concurrent CLI/MCP requests can no longer leak each other's placement into the rows.

### Tests (production path, CI-covered)
- `TestStatusBackendRowsUseProductionBuilderRetainedPlacement` — the REAL production builder (`declaredVersionServices`) with two deployments whose retained PostgreSQL/Valkey placement differs, run concurrently: both application-scoped deployments keep their owned backend row, proving no cross-request placement leakage.
- `TestStatusBackendRowsReserveSharedRetainedPlacement` — a retained shared PostgreSQL must not render as an owned component row (no-invention boundary).
- `TestVersionViewBackendRowsUseRecordPlacement` — retained placement over ambient classification (SKIPs on this host where ambient resolves PostgreSQL to shared, base parity).

### Verification (candidate SHA 6377f1b22)
- `go build ./...` rc=0.
- `go vet ./cmd/baha/` rc=0.
- `gofmt -l` empty for all changed files.
- `go test ./contracts/... ./internal/machinereadmodels/... -count=1`: ok (all ok).
- `go test ./internal/application/ -count=1 -timeout 10m`: ok.
- `go test ./cmd/baha -run 'TestStatus|TestVersion|TestComponent|TestAppVersion|TestUnified|TestManifest|TestRender|TestHumanCommand|TestMachineCoverage|TestDoctor|TestAppVersions|TestProvider|TestPlacement|TestBackend|TestRelease|TestCommand' -count=1`: ok (2.907s).
- Focused production-builder run at 6377f1b22:

```
--- PASS: TestStatusVersionsSectionRendersSeparatedCells (0.00s)
--- PASS: TestAppVersionsCommandUnifiedRowsCallable (0.01s)
--- PASS: TestAppVersionUnifiedRowsAndSelectorCallable (0.60s)
--- SKIP: TestStatusBackendRowsKeepPinnedImageAndUnmappedSource (0.00s)
--- PASS: TestStatusSharedProviderBackendsAreNotDeploymentComponents (0.00s)
--- SKIP: TestVersionViewBackendRowsUseRecordPlacement (0.00s)
--- PASS: TestStatusBackendRowsUseProductionBuilderRetainedPlacement (0.00s)
--- PASS: TestStatusBackendRowsReserveSharedRetainedPlacement (0.00s)
--- PASS: TestUnifiedViewPinnedImagesMatchRenderers (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.682s
```

### CI → TRIGGER
- Every new/changed test is an ordinary `go test` test in cmd/baha, executed by the existing validate job's `go test ./...` whenever CI runs on this branch — no `.github/**` change needed for the tests themselves (AGENTS 5.3 CI-Aufnahmepflicht satisfied without Owner-scope workflow edits).
- Trigger state (observed, no dispatch by this lane per mission): PR #1614's base is a lane branch; the repo's `pull_request` trigger filters branches `[develop, main]`, so a stacked PR gets no hosted run by itself (same finding as the 0428-059 akte). Exact-head CI runs are dispatched by the coordinator after END; the base-parity SKIPs above will also appear on any exact-head run of base or candidate and are environment-bound (ambient orgconfig resolves PostgreSQL to shared here), documented here in advance.

### repo-rule compliance
- Plan -> preflight -> apply -> verify untouched (read-only surface). Runtime/capability/delivery separate. CLI/JSON/MCP share one collector. No invented fields. Owner/consent/secret protection intact.
- Only 062-eigene files touched; no reserved files (commands.go, .github/**); RESERVED-CLEAN witness below.

## CLEANLINESS
- docker ps --format '{{.Names}}' at END: empty — no containers/compose/networks/volumes started.

## HANDOFF
- Branch: lane-0428-062-cli2-app-status @ <head SHA after push> (FF from 03e280800). PR #1614 draft, base lane-0428-059-cli2-source-model. Merge sequencing belongs to the stack integration (059 first).
- Shared-file note: on stack integration re-run machine-read-models -schema and BASEHARBOR_UPDATE_MACHINE_DOCS=1.

## END
END_DONE mission-status-r2.md: 0428-062 luna-r1 correction — retained per-provider placement wired into production row builders (declaredVersionServices takes pure placementClassifier; retainedPlacementClassifier reads record retained backend_placements, no os.Setenv global-env mutation); branch lane-0428-062-cli2-app-status, candidate head 6377f1b2298f104d54b67236177a1d3c8c26b2d2 (FF from 03e280800, verified remote head), draft PR https://github.com/mcpdev80/baseharbor/pull/1614 (base lane-0428-059-cli2-source-model), no merge, no .github/** change.

## second-to-last witness (origin/main evidence presence)
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/cli2-app-status
evidence/r28-welle1-2026-11-15/cli2-app-status/act-luna-r1.md
evidence/r28-welle1-2026-11-15/cli2-app-status/round-1.md
evidence/r28-welle1-2026-11-15/cli2-app-status/round-2.md
```
