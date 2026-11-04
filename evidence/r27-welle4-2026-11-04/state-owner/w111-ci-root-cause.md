# CI root-cause analysis: PR #1347 red hosted checks (run 41831850228)

- Lane / role: w111-state-owner (coordinator f49a3303, CI field), root-cause + fix prep
- PR #1347 head: 03e4e01b217c433e7b199951b062f4c98f9c488f (branch work/r27-state-owner)
- Base: origin/develop bb9bc0ef (note: develop has since moved to 2a43984a, PG-isolierung)
- CI run: 41831850228 (CI · PR #1347, workflow_dispatch-ish pull_request run)
- Date: 2026-11-04

## 1. Which file, which path, who produces it (workflow-log proof)

The failing assertion in run 41831850228 (verbatim, both go-unit-tests job 126580873725 and wizard-app-edit-tests job 126580873935):

- app_edit_apply_test.go:1022: real Edit lifecycle did not converge: application machine: partial
- application preflight failed: managed service PKI preflight: stat /tmp/TestAppEditCommandCompleteProviderEditRunsRealLifecycle2350953225/001/state/targets/docker-dev/runtime/compose.yaml: no such file or directory

Path the managed-service PKI preflight expects a file:
- runtime/compose.yaml under the docker-dev Target runtime root = <BASEHARBOR_STATE_DIR>/targets/docker-dev/runtime/compose.yaml
- BASEHARBOR_STATE_DIR is set by the test to <t.TempDir()>/state, hence the .../001/state/targets/docker-dev/runtime/ prefix in the CI log.
- runtime.env lives beside it (same dir) and is read by the same provider.

Who is supposed to produce it in PRODUCTION (the path the preflight reads):
- existingTargetRuntimeFiles(ctx) [cmd/baha/target.go:580] -> targetRuntimeFiles -> bhruntime.ExistingFilesForProject(stateDir, project)
- ExistingFilesForProject [internal/runtime/stack.go:399] reads files.Compose = stateDir/compose.yaml AND files.Env = stateDir/runtime.env; both os.Stat must succeed or it returns an error.
- The production writer of those files is bhruntime.EnsureFilesForProjectAndResources [internal/runtime/stack.go:60], which os.MkdirAll(stateDir, 0700) then os.WriteFile(compose.yaml) [stack.go:104] and os.WriteFile(runtime.env) [stack.go:115]. A Core-backed deployment materializes runtime/compose.yaml + runtime.env into the owned Target root via this path; the read-only preflight callers never do.

Who produces it in the TEST:
- TestAppEditCommandCompleteProviderEditRunsRealLifecycle [cmd/baha/app_edit_apply_test.go:888] seeds a bare authoritative Core via registerInstallationForTarget (writes only installation.json), and writes compose.yaml into the REPO WORKTREE (t.Chdir(root); mustWriteWizardTestFile(root/compose.yaml)) as the wizard source. It never materializes runtime/compose.yaml into the Target runtime root.

## 2. Root cause (the divergence, not an environment flake)

The test's baseline manifest m is api-only (no SQL). Baseline executeApplicationApplyLifecycle has no managed service -> no managed-service PKI preflight -> it converges without runtime/compose.yaml (this is why the baseline passes on the shared runner).

The confirmed Edit adds the SQL instance (desired := application.WithSQLInstances(m, "default"), line 945). SQL makes the manifest request a managed service:

- application.HasManagedRuntimeServices(m) returns true when SQLInstanceNames(m) > 0 [internal/application/runtime_shape.go:HasManagedRuntimeServices]
- requiresManagedServiceIssuer(m) [cmd/baha/app_provider_preflight.go] then returns true -> the Edit preflight registers the "managed service PKI" check -> resolveApplicationServiceIssuer -> resolveApplicationCoreRuntime [cmd/baha/application_core_authority.go:85] -> existingTargetRuntimeFiles -> os.Stat(runtime/compose.yaml) -> file absent -> "managed service PKI preflight: ... compose.yaml: no such file or directory" -> Status:partial -> test fails at line 1022.

This is a real precondition gap, not a Docker-mode / runner-infra issue: the Edit's managed-service PKI preflight requires the owned Core runtime manifest to exist, and the test never materializes it. The fix must make the fixture self-endending: the test materializes runtime/compose.yaml (and runtime.env) into its own Target runtime root via the production EnsureFilesForProjectAndResources path, so the preflight finds the exact file it reads.

## 3. The fix (test-scope fixture only; no product, no .github)

Insert after the baseline lifecycle (after line 943) and before desired := WithSQLInstances (line 945):

- resolve the Target runtime root via targetRuntimeStateRoot(target)
- materialize the Core runtime with bhruntime.EnsureFilesForProjectAndResources(runtimeRoot, bhruntime.SharedProjectName(target.Name), bhruntime.SharedResourceProjectName(target.Name), bhruntime.Ports{Postgres: 15432, OpenBao: 18200}, false)
- t.Fatalf on either error (loud failure, never a silent pass)

This is a helper in test scope that ESTABLISHES the production precondition (an installed, owned Core) rather than hiding the failure: it is neither a skip clause nor a t.Setenv trick. It matches the established pattern in application_shared_sql_observation_test.go and application_runtime_retirement_verification_test.go, which both call EnsureFilesForProjectAndResources into the Target runtime root.

Local verification (no Docker needed for this path):
- Before the fixture: os.Stat(runtime/compose.yaml) fails with the exact CI error ".../targets/docker-dev/runtime/compose.yaml: no such file or directory".
- After the fixture: os.Stat(runtime/compose.yaml) and os.Stat(runtime/runtime.env) succeed; existingTargetRuntimeFiles(nil) succeeds. A focused probe (TestW111FixProbePKIPreflightFindsCompose) passed; doctor-boundary + TestAppEditCommandHydratesExactSourceAndNoCancelWrites pass (no regression). go build ./... and go vet ./cmd/baha/ clean.

## 4. Correctness / contra-probe (mission step 4)

The fix makes the test self-verifying in the reverse direction too: if runtime/compose.yaml is absent, the PKI preflight fails closed (that was the observed CI failure). A deliberately corrupted/absent compose.yaml in the fixture therefore still makes the Edit fail — the test is not silenced. (Full green requires a Docker daemon + verifiable postgres backend for the SQL resume; that execution convergence is gated by the hosted runtime matrix, not by this shared-runner PKI preflight.)

## 5. Scope statement

- Product code: UNCHANGED. This is a test-fixture precondition (materialize the owned Core runtime the test already assumes exists).
- .github / workflow: UNCHANGED. The shared-runner go-unit-tests job runs this test unconditionally (ci.yml `go-unit-tests) go test ./...`); the fix makes it pass there. No workflow change needed.
- Per mission step 5: because this fix needs NO workflow change, it does not require an Owner CI-field stop. The product ADR-0022 boundary is untouched.

## END

END_DONE w111-state-owner (coordinator CI field): root-cause-fixed compose.yaml-missing at managed-service PKI preflight; fix=test-scope Core-runtime fixture materialization (no product, no .github). CODEX-REVIEW ACCEPT. PR #1374 CLOSED (superseded, comment id 6634103570 with diff-beleg: commit 069b02b5 = only cmd/baha/app_edit_apply_test.go +18/0). Fix landed on PR #1347 (work/r27-state-owner), merged develop ecbb8854 (Vorfahr-pflicht) -> merge head fd4980a1, pushed, ls-remote==head fd4980a1. ROOT CAUSE FIXED but CI run 41854714268 shows failure MOVED from "compose.yaml: no such file or directory" to "OpenBao manager credentials are not configured" (app_edit_apply_test.go:1090) — deeper Core-bootstrap gap. STOP+MELDEN (directive 17:4x #4). CLEANUP per Owner 17:4x: .github ci.yml change unstaged+restored (belongs to Owner's 2a43984a PG-isolation, NOT my write-set); stray wt1347-fix worktree removed from ecosystem root and moved to /tmp/opencode/wt1347-fix (clean, fix intact, NOT pushed). No further push pending Owner. Evidence below.
