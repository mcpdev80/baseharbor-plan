# Round 6 — Decision B delivered (domain slice), CLI exposure reverted (scope)

- Shift: r28-welle1, 2026-11-15
- Worker lane: `lane-0428-uid-environment`
- Task / card: `t-20261114-r28-cli2-uid-environment` (0428-051), PR #1578, base `lane-0428-uid-app`
- r6 head: `756d21b783` (lane-0428-uid-environment), PR #1578 base `lane-0428-uid-app`
- Planning repo origin/main: `265f35ca53` (owner decision B DESIGN-RULING head)

## ZWECK

Owner decision B (card DESIGN-RULING 2026-11-15, plan-head 265f35ca): Environment-Identitaet wird EIGENE environment.json identity record pro target, KEIN Feld in deployment-state-records. UMSETZUNG: (1) Realitaetsabgleich; (2) envUid in own versioned identity-record unter target state-root; (3) r5-content zurueckbauen; (4) Tests (UID-Konvergenz, reuse, no-authored-leak, konflikt fail-closed); LIEFERUNG push + CI beobachten + akte + END. Kein merge (frost).

## REALITAETSABGLEICH

- Planning repo origin/main head `265f35ca53ef9e7fe0ef08c5de1583c0fa817260` (verified via ls-remote).
- PR #1578 head `f353d1f736`, base `lane-0428-uid-app`, DRAFT, OPEN.
- Decision B TEXT (card, plan-head 265f35ca): "Option B. Environment identity is a dedicated per-target identity record (environment.json), NOT a field inside existing deployment-state records. Storage: under the target's state root, one lean versioned record carrying the environment UID plus renameable metadata (name), generated idempotent under lock, reused on checkout, fail-closed on conflict. Deployment-state records stay unchanged."
- r5 state already IMPLEMENTED B exactly: UID in own per-(target,env) environment.json at targets/<target>/.baseharbor/environments/<env>/environment.json; deployment_store.go schema UNCHANGED (DeploymentRecord keyed by (target,app,env,deployment_id), untouched); app.id stays out.

## DIFF EXACTLY B (vs app-base 2bf0c9295)

- internal/deployment/environment_identity.go — own environment.json identity record (UID as field in own record, not deployment-state).
- internal/deployment/environment_identity_test.go — B-acceptance tests.
- internal/environment/environment.go — environment-domain package (NewID/Validate; UID system-generated, never authored).
- internal/environment/environment_test.go.
- deployment-store schema: UNCHANGED (no field folded into DeploymentRecord).
- NO reserved files touched: cmd/baha/commands.go, internal/machine contract registry, docs/cli/command-index.md, docs/de/cli/command-index.md.

## SCOPE DECISION: CLI exposure reverted (out of slice)

- r5/r6 added `baha target env [show|rename OLD NEW]` (cmd/baha/target.go + command_target_env.go + environment_identity_cli_test.go).
- r6 CI run 43707049604: the command broke 3 CI-GENERATED tests (command-index.md drift + unclassified product command `baha target env` in machine-coverage).
- Card explicitly RESERVES: `cmd/baha/commands.go`, shared machine registry, `.github/**`, release notes, generated indexes — for integration/CI owners. Editing them = scope violation.
- Decision B ACCEPTANCE is all DOMAIN-LEVEL (card acceptance: identity uniqueness, concurrent registration, rename stability, shared multiple apps/nodes, migration, no accidental recreation/cross-tenant mixing) — covered by internal/deployment + internal/environment tests. CLI exposure is NOT required for B and belongs to follow-up uid-target #1580 / integration.
- ACTION: reverted the CLI command and its CLI test; slice = environment-identity DOMAIN only. CONFIRMED no reserved files touched.

## TESTS (all green on r6 head 756d21b783)

- internal/deployment: ok (0.818s) — TestGetEnvironmentGeneratesOnceAndReuses, TestGetEnvironmentIsPerTargetIsolation, TestGetEnvironmentReusesOnBrownfield, TestGetEnvironmentConcurrentRegistrationIsAtomic, TestRenameRetainsIdentityIsThePersistedContract, TestRenameReopeningByNameIsIdempotent, TestRenameAcrossTargetsKeepsIsolation, TestReadEnvironmentRecordFailsClosedOnCorruptBinding, TestRenameRefusesExistingDestinationUID, TestRenameConvergesUnderContention, TestLegacyStateReuseViaGetEnvironment.
- internal/environment: ok (0.003s).
- 3 doc/coverage tests (TestHumanCommandIndexTracksExactCommandMetadata, TestMachineDocumentationTracksRegistryAndCommandTree, TestMachineCoverageCIRealTreeAndJSONClassification) AFTER CLI revert: ok (0.030s).
- go build ./...: exit 0. go vet ./internal/deployment/... ./internal/environment/...: exit 0.
- environment.json under BASEHARBOR_STATE_DIR (BF-01 isolation); app.id stays OUT.

## CI RUN (own-run duty) — run 43707049604, head 756d21b7

- Trigger: manual workflow_dispatch on refs/heads/lane-0428-uid-environment (Q-CIFIRE/Q-RUNTIME environment).
- validate job: unit tests (validate/13) = 0 failures.
- runtime-integration (validate/15, `Run runtime integration tests serially`) = FAILURE — PRE-EXISTING native runtime sandbox limitation (same as r3-run 43658208331 @ b71f64e19 and base-run 43659613732 @ 18b0ebc9d): ORAS required / postgres-analytics runs as root. NOT my defect.
- unit tests green, runtime-integration pre-existing sandbox fail => domain slice CI-clean.

## PROVENANCE

- r6 head `756d21b783` on refs/heads/lane-0428-uid-environment (ls-remote).
- PR #1578 base = lane-0428-uid-app (gh pr view), DRAFT, OPEN.
- app-base 2bf0c9295 (founder on develop). Decision B DESIGN-RULING plan-head 265f35ca53.
- CI run 43707049604 head 756d21b7 (manual workflow_dispatch).
- NO reserved files in r6 diff: git diff 2bf0c9295..756d21b783 --name-only = internal/deployment/environment_identity.go, internal/deployment/environment_identity_test.go, internal/environment/environment.go, internal/environment/environment_test.go.

## END

- END status: DONE. Decision B delivered as 4-file environment-identity DOMAIN slice (own environment.json per target, UID field in own record, deployment-schema unchanged, app.id out). All domain tests green. CLI exposure reverted (out of slice; no reserved-file edits). CI run 43707049604: unit tests 0 failures; runtime-integration = pre-existing sandbox fail.
- END lane: DONE.
- Compose cleanliness: no lane-0428 container/compose; CI + unit tests only.
- Next trigger: owner decision on CLI-exposure follow-up (uid-target #1580 / integration); no merge (frost).
