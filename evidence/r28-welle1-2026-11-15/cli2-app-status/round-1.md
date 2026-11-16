# round-1 — 0428-062 cli2-app-status: unify app status + versions over the source-model read view

Card: t-20261114-r28-cli2-app-status (0428-062)
Mission: /tmp/opencode/mission-welle2-062.md
Lane: lane-0428-062-cli2-app-status (flash worker session w062)
Claim: published on planning origin/main as 10d3f501 before any code change (AGENTS 4.3), owner "w062-cli2-app-status".

## PLAN
1. Task-Vertrag lesen (plan.py show, card note, mission); Claim publizieren und pushen. Done (10d3f501).
2. Basis verifizieren: ls-remote lane-0428-059-cli2-source-model = eda0cd61cc182d071657ac64848cf5cb306e30be (= refs/pull/1595/head); Worktree /tmp/opencode/w062/wt von diesem Head; develop 0e9ccb582 ist Ancestor der Basis (merge-base --is-ancestor exit 0). Done, witnesses below.
3. Unified view in cmd/baha/app_versions_view.go: ein Collector/Renderer, der die wanted/applied/observed-Zellen aus dem gelieferten machinereadmodels.ReleaseViewFromRecord und die Komponenten-/Quellzeilen aus dem gelieferten portablen source model (0428-059) + den deklarierten Backend-Identitäten bildet. Done.
4. app status integriert die Versions-Sektion in CLI-Human, -o json und MCP/HTTP (teilen collectApplicationStatusResult); app version und app versions konsumieren denselben Collector. Done.
5. -c/--component Parser + fail-closed Selektion, --all-targets erhalten. Done.
6. Read-model additive erweitern (ComponentVersion source/source_type/source_identity/sub_path, ViewStages.AnyRecorded) und Schema mit dem Repo-Generator regenerieren; Doku EN/DE aktualisiert. Done.
7. Targeted + full-package Tests, Audits; base-parity Fehlschläge gegen pristine Basis belegt. Done, results below.
8. Commit (ein own commit), Push, ls-remote witness, draft PR #1614 base lane-0428-059-cli2-source-model; keine merges, kein ready_for_review, kein .github/**. Done.
9. Akte hier, Push auf origin/main, Endbericht an d4212c96. In progress (this file).

## BASE ATTESTATION
Authoritative planning repo (wrong-zone witness, mandated):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

Product remote truth (NOT the quarantined workers checkout):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/lane-0428-059-cli2-source-model refs/heads/lane-0428-062-cli2-app-status
eda0cd61cc182d071657ac64848cf5cb306e30be	refs/heads/lane-0428-059-cli2-source-model
98877cc11c532a29973c2ac7535d99daa13ba5de	refs/heads/lane-0428-062-cli2-app-status
```

Base ref cut-from: refs/heads/lane-0428-059-cli2-source-model = eda0cd61cc182d071657ac64848cf5cb306e30be (mission STAPELREGEL; also refs/pull/1595/head). Ancestry: `git merge-base --is-ancestor eda0cd61c HEAD` → exit 0. `git log --oneline eda0cd61c..HEAD` shows exactly ONE commit: `98877cc11 cmd/baha: unify app status and versions over the source-model read view` — own commits only, no foreign candidate carried. develop 0e9ccb582 is an ancestor of the base.

PR content witness: `gh pr diff 1614 --name-only` == `git diff --name-only eda0cd61c..HEAD` (18 files, diff empty). Reserved-file witness:

```
git diff --name-only eda0cd61c..HEAD | grep -E '^\.github/|^cmd/baha/commands\.go$' || echo RESERVED-CLEAN
RESERVED-CLEAN
```

## CANDIDATE
- Branch: lane-0428-062-cli2-app-status @ 98877cc11c532a29973c2ac7535d99daa13ba5de (pushed; ls-remote above)
- PR: https://github.com/mcpdev80/baseharbor/pull/1614 (draft, base lane-0428-059-cli2-source-model, Titel enthält 0428-062)
- `gh pr view 1614 --json headRefOid,isDraft,baseRefName` → head 98877cc11c532a29973c2ac7535d99daa13ba5de, isDraft true, base lane-0428-059-cli2-source-model.

## WHAT CHANGED (candidate slice)
- cmd/baha/app_versions_view.go (new): the unified collector/renderer — collectAppStatusVersions derives the three separated cells through the delivered machinereadmodels.ReleaseViewFromRecord (persisted record authoritative); collectSourceModelComponents renders one row per declared identity (backend service instances + logical workload components) merged with the delivered portable source-model projections (LoadSourceModel/LoadWorkspaceMapping/ResolveWorkspace); explicit "unmapped" state + warning, never a status failure; partialWorkspaceResolution keeps declared identities when the developer-local checkout cannot be resolved; viewPlacementServices reads backend rows under the record-retained placement and restores the ambient environment afterwards; shared-placement backends stay omitted (base parity); pinned backend images come from the delivered runtime contract via pinnedRuntimeImage, with a separation regression against the shipped renderer sources.
- cmd/baha/app_observe.go, app_status_result.go, app_tls.go: status human/JSON/MCP faces consume the shared collector; the status machine result carries new fields versions (stages + components) and version_warnings.
- cmd/baha/app_version_view.go, app_versions_command.go: version and versions faces consume the same collector/renderer; the stages aggregate keeps per-application warnings and source state.
- internal/machinereadmodels/release.go: additive ComponentVersion fields Source/SourceType/SourceIdentity/SubPath and ViewStages.AnyRecorded; contracts/machine/v1/read-models.schema.json regenerated with the repo's own generator (`go run ./scripts/tools/machine-read-models -schema`).
- Docs: docs/cli/applications.md, docs/de/cli/applications.md, how-to local-remote-team-workflow EN/DE updated for the unified output; command-index files regenerated by BASEHARBOR_UPDATE_MACHINE_DOCS=1; literal tokens kept EN/DE-identical.
- Tests (new): app_status_versions_test.go, app_version_unified_test.go, app_versions_view_parity_test.go, app_versions_backend_test.go.

## ACCEPTANCE POINTS → TESTS + VERBATIM OUTPUT
All runs on candidate SHA 98877cc11, go build from go.mod toolchain, TMPDIR=/home/marcel/dev/baseharbor-ecosystem/workers/tmpcache/w062 (the /tmp usrquota artifact documented below).

### 1. Wanted/applied/observed machine fields preserved, never copied
Tests: TestStatusVersionsSectionRendersSeparatedCells, TestStatusVersionsUnknownDimensionIsUnclearNeverBlank, TestVersionViewThreeCellsAlwaysSeparated, TestVersionViewMissingDimensionIsUnclear, TestVersionViewDimensionIsolation, TestVersionViewJSONShapeSeparatesCells, TestStatusJSONCarriesVersionsSection, TestStagesViewMutationAgainstSeparationLine.

```
--- PASS: TestStatusVersionsSectionRendersSeparatedCells (0.00s)
--- PASS: TestStatusVersionsUnknownDimensionIsUnclearNeverBlank (0.00s)
--- PASS: TestVersionViewThreeCellsAlwaysSeparated (0.00s)
--- PASS: TestVersionViewMissingDimensionIsUnclear (0.00s)
--- PASS: TestVersionViewDimensionIsolation (0.00s)
--- PASS: TestVersionViewJSONShapeSeparatesCells (0.00s)
--- PASS: TestStatusJSONCarriesVersionsSection (0.00s)
--- PASS: TestStagesViewMutationAgainstSeparationLine (0.00s)
```

### 2. Unknown Git / image digest stays explicit unknown (no invented fields)
Tests: TestStatusVersionsUnknownDimensionIsUnclearNeverBlank (above), TestVersionViewWarningsRenderExplicitlyWithoutInference path inside TestVersionViewComponentColumnsShowSourceProvenance (app_versions_view_parity_test.go + app_version_unified_test.go), TestVersionSectionCarriesNoSecrets.

```
--- PASS: TestVersionSectionCarriesNoSecrets (0.00s)
--- PASS: TestAppVersionUnifiedRowsAndSelectorCallable (0.94s)
```
The callable test asserts an application-owned workload image is never invented (`Image != ""` fails; observation says "logical workload component"), i.e. no parallel truth.

### 3. Source provenance rows from the delivered source model; unmapped explicit, never a failure
Tests: TestVersionsComponentRowsProjectSourceModel, TestVersionsUnresolvableSourceModelIsExplicitNotFailure, TestStatusAndVersionsComponentRowsAreOneView, TestVersionViewComponentColumnsShowSourceProvenance.

```
--- PASS: TestVersionsComponentRowsProjectSourceModel (0.00s)
--- PASS: TestVersionsUnresolvableSourceModelIsExplicitNotFailure (0.00s)
--- PASS: TestStatusAndVersionsComponentRowsAreOneView (0.00s)
```

### 4. -c filter on status/version/versions, fail-closed; --all-targets preserved
Tests: TestComponentSelectorParsesAndFilters, TestAppVersionUnifiedRowsAndSelectorCallable, TestAppVersionsCommandUnifiedRowsCallable, TestAppVersionsCommandCallable (base-preserved), TestVersionsAggregateUnifiedRowsCallable path.

```
--- PASS: TestComponentSelectorParsesAndFilters (0.00s)
--- PASS: TestAppVersionsCommandUnifiedRowsCallable (0.50s)
--- PASS: TestAppVersionsCommandCallable (0.47s)
--- PASS: TestAppVersionCommandCallable (0.59s)
```

### 5. Backend rows: delivered pin, observed image only from inspection, record placement over ambient policy
Tests: TestVersionViewBackendRowsUseRecordPlacement (3 subtests), TestUnifiedViewPinnedImagesMatchRenderers, TestStatusSharedProviderBackendsAreNotDeploymentComponents, TestStatusBackendRowsKeepPinnedImageAndUnmappedSource.

```
--- PASS: TestVersionViewBackendRowsUseRecordPlacement (0.00s)
    --- PASS: TestVersionViewBackendRowsUseRecordPlacement/a_retained_application_placement_wins_over_the_shared_default (0.00s)
    --- PASS: TestVersionViewBackendRowsUseRecordPlacement/a_retained_shared_placement_stays_without_a_backend_row (0.00s)
    --- PASS: TestVersionViewBackendRowsUseRecordPlacement/without_a_retained_placement_the_ambient_policy_stands (0.00s)
--- PASS: TestUnifiedViewPinnedImagesMatchRenderers (0.00s)
--- PASS: TestStatusSharedProviderBackendsAreNotDeploymentComponents (0.00s)
--- SKIP: TestStatusBackendRowsKeepPinnedImageAndUnmappedSource (0.00s)
```
The SKIP is deliberate base parity (mission line 3): on this host the ambient organization config resolves the SQL placement to shared, and the delivered skip-semantics at eda0cd61 omit shared-placement backends from declared rows; the equivalent behavior is pinned deterministically by the two sibling tests above. On CI (no ambient orgconfig) the same code path yields the dedicated rows; TestStatusSharedProviderBackendsAreNotDeploymentComponents asserts the shared side stays row-free.

### 6. CLI/JSON/MCP parity — one collector behind all faces
Tests: TestStatusJSONCarriesVersionsSection (JSON == same stages/components), TestAppVersionsCommandUnifiedRowsCallable, plus the MCP/HTTP executors unchanged in call path (mcp_tools.go and machine_http_executor_read.go both consume collectApplicationStatusResult / collectMachineApplicationVersions — witnessed by grep of the candidate diff: neither file needed a change because both already route through the shared collector).
Secret guard: TestVersionSectionCarriesNoSecrets PASS (see 2).

## RESULT (broader gates at candidate SHA)
- Focused: `go test ./cmd/baha -count=1` with the acceptance run-list above → ok (18 PASS + 1 parity SKIP, verbatim above).
- `go test ./cmd/baha -run 'TestStatus|TestVersion|TestComponent|TestAppVersion|TestUnified|TestManifest|TestRender|TestHumanCommand|TestMachineCoverage|TestDoctor' -count=1` → `ok github.com/mcpdev80/baseharbor/cmd/baha 8.751s`.
- Full package `go test ./cmd/baha -count=1 -timeout 25m` at 98877cc11: exactly 3 FAILs, each reproduced identically at pristine base eda0cd61 in a detached worktree (base-parity, environment-bound, not candidate content):
  - `--- FAIL: TestNonTTYBackupDefaultUsesProtectedExternalArchive (0.51s)` — `app_backup_non_tty_test.go:36: default backup destination resolves inside the Git worktree; configure XDG_DATA_HOME outside the repository or choose a safe --output` (base run: same line, 0.63s)
  - `--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (3.70s)` — `app_edit_apply_test.go:957: start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner` (base run: same line, 13.35s)
  - `--- FAIL: TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (60.12s)` — `management_core_git_candidate_test.go:49: stage pinned Core candidate: native Git archive failed: signal: killed` (60 s kill; base run identical, 60.06s)
  - Mission-named base signatures 'ORAS is required before Core setup' (repository integration) and 'runs as root' (runtime_multi) are the same base-inherited native-runtime prerequisites; not fixable in this lane, not touched by this diff.
- `go test ./contracts/... ./internal/machinereadmodels/... ./internal/development/... -count=1`: contracts + machinereadmodels all ok; internal/development fails only TestStagePinnedGitTreeExportsCommitNotDirtyWorktree (60.09 s git-archive kill; same at base, same artifact class).
- `go build ./...` rc=0, `go vet ./...` rc=0, `gofmt -l` empty.
- `bash scripts/documentation-audit.sh` rc=0 (all PASS lines); `bash scripts/source-readability-audit.sh` rc=0 (Go file size / function span / regression ratchet PASS).

## TESTS → CI → TRIGGER
- Every new test is an ordinary `go test` test in cmd/baha (plus machinereadmodels schema coverage in ./contracts), executed by the existing validate job's `go test ./...` step whenever CI runs on this branch — no .github/** change needed for the tests themselves (AGENTS 5.3 CI-Aufnahmepflicht satisfied without Owner-scope workflow edits).
- Trigger state (observed, no dispatch by this lane per mission): PR #1614's base is a lane branch; the repo's pull_request trigger filters branches [develop, main], so a stacked PR gets no hosted run by itself (same finding as the 0428-059 akte). Exact-head CI runs are dispatched by the coordinator after END; the three base-parity failures above will also appear on any exact-head run of base or candidate and are environment/runtime-prerequisite failures, documented here in advance.

## Environment caveat (documented, not a candidate defect)
- Host /tmp is a usrquota tmpfs near its limit; without an explicit TMPDIR the disk-heavy tests fail with quota/killed artifacts. All runs above used TMPDIR on the disk-backed workers/tmpcache volume. The git-archive 60 s kills and the isolated-Core/backup failures reproduce unchanged at pristine base eda0cd61 (commands shown in RESULT), so they are not caused by this slice.

## repo-rule compliance
- Plan → preflight → apply → verify untouched: this slice is read-only surface work; no lifecycle mutation changed.
- Runtime, capability and delivery stay separate; CLI, JSON and MCP share one domain collector (the card's core demand). No invented fields: every machine addition maps to a dimension the delivered read model or source model already records; unrecorded dimensions stay explicit unknown/UNCLEAR.
- Ownership and secret protection: TestVersionSectionCarriesNoSecrets PASS; placement env overrides are process-scoped and restored by viewPlacementServices.
- Generated files regenerated via repo-owned generators only (machine-read-models -schema, BASEHARBOR_UPDATE_MACHINE_DOCS=1); commands.go and .github/** untouched (RESERVED-CLEAN witness).
- No subagents used (AGENTS 4.8); single candidate branch as named in the mission; no merge, no ready_for_review, no tag, no release.

## Cleanliness
- `docker ps --format '{{.Names}}'` at END: empty — this lane started no containers/compose/networks/volumes.
- Scratch state lives only in /tmp/opencode/w062/ (worktree wt; basewt detached base-comparison worktree — removed and pruned after the parity runs) and workers/tmpcache/w062* (test TMPDIR, logs excerpts). No writes to /home/marcel/dev/baseharbor-ecosystem/baseharbor main checkout, none to the quarantined workers checkout, none outside these zones.

## Handoff
- Branch: lane-0428-062-cli2-app-status (from eda0cd61c). PR #1614 draft, base lane-0428-059-cli2-source-model. Merge sequencing belongs to the stack integration (059 first), not to this lane.
- Shared-file note: contracts/machine/v1/read-models.schema.json and docs/*/cli/command-index.md are generator-owned; on stack integration re-run both generators on the combined tree.
- Remaining gaps: none known against the card acceptance list; the ambient-orgconfig placement caveat (point 5 SKIP) is base behavior, not a card gap.

## END
END_DONE mission-welle2-062.md: 0428-062 unified app status/versions over the delivered source-model read view — branch lane-0428-062-cli2-app-status, candidate SHA 98877cc11c532a29973c2ac7535d99daa13ba5de, draft PR https://github.com/mcpdev80/baseharbor/pull/1614 (base lane-0428-059-cli2-source-model), no merge, no .github/** change; base-parity failures documented above.

## Second-to-last action witness (mandated origin/main presence check)
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/cli2-app-status
evidence/r28-welle1-2026-11-15/cli2-app-status/round-1.md
```
