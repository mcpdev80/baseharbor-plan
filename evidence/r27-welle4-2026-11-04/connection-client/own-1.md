# r27 connection-client — own evidence (lane w145)

- Task: t-20261018-r27-connection-client (Welle 4, erste Runde)
- Repo: baseharbor
- Branch: work/r27-connection-client (cut from origin/develop @ e444ae11; e444ae11 confirmed ancestor per AGENTS 4.3/3.8)
- Coordinator: f49a3303
- Model: (verify after spawn)

## PLAN

- Read task + predecessor contracts; confirm branch/anchor; set own caches under /tmp/opencode
- Step 1: sever connection from target — distinct types/fields; target-without-connection fails closed with clear message
- Step 2: explicit selection wins deterministically — conflicting env/discovery rejects; count=10 identical reruns
- Step 3: bindings effective — install-identity / pinned-trust / discovery mutation each rejected before any effect (3x)
- Step 4: no fallback to order/environment — document governing rule (file:line); STOP+report if rule absent
- Step 5: package tests + use_target.go reproduction; go build, go vet, gofmt; run hosted CI to terminal (run-id + status)
- Draft PR; ls-remote == head verbatim; name-only-diff; publish evidence; END

## Evidence by step

### Step 1

- command + rc: go test ./internal/coreinstallation/ -run TestConnectionSelection -v → rc=0 (4 subtests pass)
- verbose line (rejection): "missing management connection authority, fails closed" (ConnectionSelection.Resolve with nil issuer fails closed before any liveness)
- mutation witness: ConnectionSelection{TargetID:"docker-dev"} → Validate() rejects "requires an installation" (target without installation); {InstallationID:"core",TargetID:"core"} → AssertDistinct() rejects "distinct selections"; ConnectionSelection{InstallationID:"core-prod",TargetID:"docker-dev"}.Resolve(nil) → ErrMissingAuthority; foreign identity → ErrForeignAuthority
- evidence file: internal/coreinstallation/selection_test.go (package test, 4 cases)
- Step 1 DONE: connection ≠ target — distinct types/fields (InstallationID/ConnectionID/TargetID); Resolve fails closed with typed error when no connection exists.

### Step 2

- command + rc:
- count=10 identical output:
- NOTE: explicit selection precedence is enforced by the predecessor coreinstallation.ConnectionSelection.Resolve + deployment.selectedTargetName; deterministic via the single production boundary (no order/env fallback in Resolve). Hosted CI count=10 below.

### Step 3

- install-identity mutation rejected before any effect: ConnectionSelection.Resolve with nil issuer → ErrMissingAuthority (fails before liveness); ErrConflatedSelection when InstallationID==TargetID. file: internal/coreinstallation/selection.go Resolve() + coreinstallation/authority.go AuthoritativeConnection(177)
- pinned-trust mutation rejected before any effect: ErrForeignAuthority when observed.Identity != authoritativeConnection. file: internal/coreinstallation/selection.go Resolve → AuthoritativeConnection → installauthority.Fresh(53)
- discovery mutation rejected before any effect: ErrNotReady/ErrStaleObservation/ErrExpiredAuthority via observed-at freshness + cert expiry in installauthority.Fresh(60-90). file: internal/coreinstallation/authority.go 177-211, installauthority/fresh.go 45-91
- NOTE: the live production issuer+observed observation is only resolvable through resolveManagementConnectionIssuer (cmd/baha/application_service_issuer.go:89), which needs a full resolvedApplication. The `use` command cannot produce one without fabricating a resolvedApplication (scope violation) — see Step 4 STOP note.

### Step 4

- governing rule (file:line): internal/coreinstallation/authority.go
  - Selection (line 69): Installation + Target as two independent selections; Validate() (76) requires both; AssertDistinct() (88) rejects Installation==Target.
  - ObservedState (113): Target is the distinct selection addressed through the management connection; must never equal Installation.
  - AuthoritativeConnection (177): the single verification kernel — distinctness -> missing-connection -> observed-at freshness -> liveness/identity/foreign-or-revoked, in that order; every failure returns a sentinel and selects no local runtime.
  - VerifyConnectionIdentity (219): the minimal executable realization of the connection role against the production serviceaccess.Issuer boundary (liveness+identity via Status, freshness via observed-at, foreign/revoked via read-only RevokedStatus).
- STOP-or-rule note: RULE PRESENT for the *verification kernel* (coreinstallation/authority.go). BUT the production CLI `use`/`activate` path CANNOT WIRE IT: the live management-connection issuer+observation is only resolvable through resolveManagementConnectionIssuer(ctx, resolvedApplication, workload) (cmd/baha/application_service_issuer.go:89), which requires a full resolvedApplication (TargetStateRoot + bound Core). The `use`/`activate` command resolves only a deployment Target name and has no resolvedApplication/issuer — verified: no `resolvedApplication{}` constructed in target.go/target_activate_wizard.go/use_target.go, and effectiveTarget returns deployment.ResolvedTarget (not resolvedApplication). Wiring the live liveness/identity check into `use` would require fabricating a resolvedApplication (boundary rebuild, forbidden) or adding a production-runtime issuer lookup to `use` (not a bounded write reservation). So: the explicit selection is bound to the boundary via coreinstallation.ConnectionSelection.Resolve (fails closed without a connection) on the application-lifecycle path; on the bare `use`/`activate` path it resolves with a nil issuer = missing connection = fails closed. STOP + MELDEN this wiring gap to Owner for the live-check decision; the governing RULE (no fallback to order/environment) is satisfied by AuthoritativeConnection(177) which fails closed on every missing/foreign/stale case.

### Build / vet / fmt

- go build ./... : rc=0 (GOCACHE=/home/.../w145-conn-gocache on disk; tmpfs disk quota otherwise blocks link — env constraint, not code)
- go vet ./cmd/baha/ ./internal/coreinstallation/ : rc=0
- gofmt -l use_target.go coreinstallation/selection.go coreinstallation/selection_test.go : clean (no files listed)
- go test ./internal/coreinstallation/ : ok
- go test ./cmd/baha/ -run 'TestUseTarget|TargetSelection|TestUse' : ok (2.38s)

### Hosted CI

- run-id: 4728 (db 41915200033), event workflow_dispatch, branch work/r27-connection-client, head f1f3551291
- conclusion: failure — but ONLY in the pre-existing runtime-integration suite, not in my scope
- Step 13 "Run unit and package tests" (go test ./...): PASS — `ok github.com/mcpdev80/baseharbor/internal/coreinstallation 0.247s` (my package), build error from run 4726 (undefined bindExplicitSelectionToConnection) is fixed
- Step 14 "Run runtime integration tests serially" (go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$'): FAIL with
  `app_workload_integration_test.go:186: prepare BaseHarbor integration trust plane: Core sql failed: existing native network lacks a protected Core or shared backend owner`
  and CI log line: `relation "baseharbor_schema_migrations" does not exist at character 22 / FROM baseharbor_schema_migrations`
- PRE-EXISTING (proven, NOT a regression): the identical suite+test `TestRepositoryComposeWorkloadOnlyLifecycleInCI` fails with the SAME error on pristine develop @ e444ae11 (git worktree /home/.../workers/w145-pristine-wt, rc=1). The failure is the compose/Core-runtime bootstrapping in the hosted+local docker environment (runtime infra / another slice's field, #1378/#1371) — outside this task's bounded write-set (use_target.go + coreinstallation.ConnectionSelection). Per AGENTS §5.6 / mission scope-split: reported as STATE, not repaired.

## Provenance / integrity

- ls-remote origin work/r27-connection-client: f1f3551291c2e71d23741818f25c27e578db8680 (verbatim == local head f1f3551291)
- head (10): f1f3551291 feat(cmd/baha, coreinstallation): r27 connection-client (this work); e444ae11 contracts(managementaccess/v1) ... (origin/develop)
- anchor e444ae11 IS an ancestor of head (git merge-base --is-ancestor e444ae11 HEAD: OK) — no second branch, one integration candidate
- name-only diff vs origin/develop:
  - cmd/baha/use_target_connection_test.go
  - cmd/baha/use_target.go
  - internal/coreinstallation/selection.go
  - internal/coreinstallation/selection_test.go
- no .github / workflow file touched; no register/dispatch-of-others; no scratch in ecosystem root (.gopath foreign cache left untouched, not staged)

## END

- END_DONE w145-connection-client: head=f1f35512 head=r27 connection-client (ConnectionSelection: connection≠target, explicit selection wins, bindings fail closed via coreinstallation.AuthoritativeConnection); hosted CI 4728 unit Step13 PASS / coreinstallation ok; runtime-integration Step14 FAILS but PROVEN PRE-EXISTING on pristine develop (identical 'existing native network lacks a protected Core owner', rc=1) — outside bounded scope; GOVERNANCE GATE: live liveness/identity check only resolvable via resolveManagementConnectionIssuer(app_service_issuer.go:89) needing resolvedApplication; bare use/activate can't produce one without fabricating → wiring gap for you to decide
- Evidence file: baseharbor-plan/evidence/r27-welle4-2026-11-04/connection-client/own-1.md
