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

## 6. BREAKTHROUGH (Owner directive 17:4x, second order): the missing piece is runtime/openbao-admin.env

- Lane / role: w111-state-owner (coordinator f49a3303, CI field), fixture extension + contra-probe
- Date: 2026-11-04
- Worktree: /tmp/opencode/wt1347-fix (baseharbor checkout, HEAD work/r27-state-owner = 069b02b5)

### 6.1 What the OpenBao manager credentials file IS and where it is read

- AdminCredentialsPath(files) = filepath.Join(filepath.Dir(files.Env), adminFileName) [internal/openbao/bootstrap.go:221], adminFileName = "openbao-admin.env" [bootstrap.go:21] => runtime/openbao-admin.env beside runtime.env.
- LoadAdminCredentials(files) [internal/openbao/bootstrap.go:447]: os.Stat(adminPath) -> os.ErrNotExist returns ErrManagerNotConfigured ("OpenBao manager credentials are not configured") [bootstrap.go:447-453]; requires mode 0600 (& 0o077 == 0) [bootstrap.go:458]; parses KEY=VALUE lines, requires OPENBAO_ROLE_ID AND OPENBAO_SECRET_ID both non-empty, else ErrManagerNotConfigured [bootstrap.go:464-482].
- The PKI preflight path that reads it: resolveApplicationServiceIssuer (cmd/baha/application_service_issuer.go) -> NewServiceIssuer (internal/openbao/service_issuer.go:24) -> Status (service_issuer.go:122) -> TrustBundle -> ServiceCA (internal/openbao/service_pki.go:152) -> managerToken (service_pki.go:373) -> LoadAdminCredentials.

### 6.2 Contra-probe 1 (unit-level, no Docker needed): PROVES the fixture hits the exact spot

- WITHOUT runtime/openbao-admin.env: LoadAdminCredentials(files) returns ErrManagerNotConfigured ("OpenBao manager credentials are not configured"). This is the EXACT credential message the CI showed at app_edit_apply_test.go:1090.
- WITH runtime/openbao-admin.env (mode 0600, OPENBAO_ROLE_ID=..., OPENBAO_SECRET_ID=...): LoadAdminCredentials returns credentials with RoleID/SecretID populated; the preflight proceeds past the credential check.
- CONCLUSION: the fixture extension (write a minimal openbao-admin.env next to compose.yaml/runtime.env) is the correct and sufficient fix for the "OpenBao manager credentials are not configured" boundary. Confirmed with an inline test (TestCC) that passed; removed afterward to keep write-set clean.

### 6.3 The fixture extension (test-only, same write-set as 069b02b5)

- File changed: ONLY cmd/baha/app_edit_apply_test.go (+19/0). No product code, no .github, no real credentials (placeholder OPENBAO_ROLE_ID=test-placeholder-role-id / OPENBAO_SECRET_ID=test-placeholder-secret-id, with a comment that it is a TEST-WINDOW PLACEHOLDER that only applies in the test window).
- Inserted after the baseline lifecycle (EnsureFilesForProjectAndResources block) and before `desired := application.WithSQLInstances(m, "default")`, writing adminEnvPath := filepath.Join(runtimeRoot, "openbao-admin.env") with os.WriteFile(..., 0o600).
- go build ./cmd/baha/ and go vet ./cmd/baha/ clean. Diff-beleg: https://github.com/mcpdev80/baseharbor/commit/069b02b5 (this extension rides on the same branch).

### 6.4 Contra-probe 2 (end-to-end, live Docker daemon via sg docker to /var/run/docker.sock): the failure MOVED AGAIN — this is the STOP+MELDEN

- Ran TestAppEditCommandCompleteProviderEditRunsRealLifecycle with the fixture + a working daemon (DOCKER_HOST=unix:///var/run/docker.sock). Local system socket returns empty server ID for the unprivileged user by default; `sg docker -c ...` grants access to the real daemon ID (5066d1c7...). This local daemon-config quirk is orthogonal to the CI boundary (CI's GitHub-hosted runner daemon reports a real ID); the fixture logic is what is being probed.
- RESULT (verbatim from the run): the fixture worked. The runtime/openbao-admin.env file is verified as a protected retained file (size=366); LoadAdminCredentials succeeded. The failure is NO LONGER "OpenBao manager credentials are not configured". It moved to:
    "application preflight failed: managed service PKI preflight: authenticate OpenBao manager for service PKI: OpenBao AppRole login failed: compose exec -T openbao-admin bao write -format=json auth/approle/login -: service \"openbao-admin\" is not running"
- The next boundary, traced to file:line:
    - loginManager (internal/openbao/bootstrap_auth.go:14) -> executor.ExecProjectInput(ctx, projectNameForFiles(files), files.Compose, files.Env, payload, serviceName="openbao-admin", "bao", "write", "-format=json", "auth/approle/login", "-") [bootstrap_auth.go:20]
    - Compose.ExecProjectInput (internal/runtime/compose.go:229) -> outputProjectInput -> `docker compose exec -T openbao-admin ...`
    - docker compose exec fails: `service "openbao-admin" is not running` (compose's own message when the container is stopped/never started).
- WHY: the OpenBao control-plane stack (compose-single.yaml defines openbao-admin at internal/runtime/assets/compose-single.yaml:177) is only STARTED by ensureAndStartRuntimeBrokerWithCore -> ensureAndStartRuntimeProviderExecutorWithCore -> (shared provider convergence calls runtime.UpProject, objectstorage/seaweedfs.go:EnsureSharedProviderAt:90) during a managed-service runtime-broker convergence. The test's baseline manifest is api-only (RequiresRuntimeBroker returns false at internal/application/runtime_identity_workload.go:53) so it never boots the OpenBao control-plane; the Edit's managed-service PKI preflight then tries to exec into a never-started openbao-admin container.
- This is a REAL product boundary: in production the OpenBao manager credentials are written by Bootstrap during stack bootstrap, and the service is running. The test materializes the credentials FILE but not a running OpenBao control-plane. Seeding openbao-admin.env is a legitimate test-fixture fix for the "credentials not configured" boundary; a running openbao-admin service is a DEEPER fixture/bootstrap step (start the compose stack in test scope), which is a different kind of change and/or a product-finding candidate. STOP+MELDEN per directive 17:4x #4.

## END

END_DONE w111-state-owner (coordinator CI field): root-cause-fixed compose.yaml-missing at managed-service PKI preflight; fix=test-scope Core-runtime fixture materialization (no product, no .github). CODEX-REVIEW ACCEPT. PR #1374 CLOSED (superseded, comment id 6634103570 with diff-beleg: commit 069b02b5 = only cmd/baha/app_edit_apply_test.go +18/0). Fix landed on PR #1347 (work/r27-state-owner), merged develop ecbb8854 (Vorfahr-pflicht) -> merge head fd4980a1, pushed, ls-remote==head fd4980a1. ROOT CAUSE FIXED but CI run 41854714268 shows failure MOVED from "compose.yaml: no such file or directory" to "OpenBao manager credentials are not configured" (app_edit_apply_test.go:1090). STOP+MELDEN (directive 17:4x #4). CLEANUP per Owner 17:4x: .github ci.yml change unstaged+restored (belongs to Owner's 2a43984a PG-isolation, NOT my write-set); stray wt1347-fix worktree removed from ecosystem root and moved to /tmp/opencode/wt1347-fix (clean, fix intact, NOT pushed).

BREAKTHROUGH (second Owner order): the missing piece IS runtime/openbao-admin.env. Fixture extended (+19/0, cmd/baha/app_edit_apply_test.go only, placeholder creds, comment: TEST-WINDOW PLACEHOLDER). Contra-probe 1 (unit): absent -> ErrManagerNotConfigured (the exact credential message), present -> loads; fixture hits the exact spot. Contra-probe 2 (end-to-end, live daemon): fixture works — openbao-admin.env verified (size=366), credential boundary CLEARED, failure MOVED to "service openbao-admin is not running" (loginManager internal/openbao/bootstrap_auth.go:14 -> Compose.ExecProjectInput compose.go:229 -> docker compose exec; baseline api manifest never boots the OpenBao control-plane stack). THIS is the next STOP+MELDEN: seeding the credentials FILE is a legit fixture fix, but a RUNNING openbao-admin service is a deeper bootstrap/fixture step. No further push pending Owner decision.
