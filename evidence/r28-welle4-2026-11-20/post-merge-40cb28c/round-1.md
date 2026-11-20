# Post-merge acceptance audit, develop head 40cb28c

lane 0428-197 (w197-0428-197-postmerge). Reine Befundung, KEINE Produktänderung, KEIN PR, KEIN Board-Edit. Ziel: je einer der heutigen develop-Merge feststellen, ob JEDE Akzeptanzzeile eine Stelle im Code hat und ob ein echter Gegen-Check besteht.

## PLAN

1. develop-head verifizieren via `git ls-remote` (real github remote).
2. Für jeden der fünf Merge den gemergten Commit in develop finden und als ancestor von develop beweisen.
3. Akzeptanzzeile der Karte lesen (`python3 baseharbor-plan/scripts/plan.py show <id>` bzw. tasks/*.md).
4. Im gemergten Diff prüfen, ob jede Akzeptanzzeile eine Stelle im Code hat (datei:zeile).
5. Einen echten Gegen-Check fahren: Go-Test oder Planner-Python für den gemergten Stand.
6. Für #1721/#1722 prüfen, ob die neue Auswahlregel die vier Feld-PRs (#1714 #1718 #1684 #1645) weiterhin trifft; roten checks ursachenbezogen zuordnen.
7. Befunde dokumentieren, evidence auf origin/main pushen, cleanliness bestätigen.

## base-attestation

- planning-repo remote (evidenz): `origin	https://github.com/mcpdev80/baseharbor-plan.git`
- develop head: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `40cb28c758b02960356434b630086a341ebe1738`
- Alle fünf merges sind ancestor von develop (real github ls-remote / git merge-base):
  - #1715 squash `2f81fa21d` OK
  - #1716 `f5ce95afc` OK
  - #1717 `3653369a` (base develop) OK
  - #1721 `17b9d1b0` OK
  - #1722 `a61905f5` OK
- PR-name-only diffs (commit-vs-parent):
  - #1715: internal/application/shared_backends_resources_runtime.go, internal/application/shared_backends_resources_runtime_test.go, internal/observability/registry.go
  - #1716: internal/capability/integration_contract_test.go, internal/capability/reference.go
  - #1717: cmd/baha/local_workload_authority.go, cmd/baha/mcp.go, cmd/baha/operator_auth_status.go, internal/operatorauth/authorization.go, internal/operatorauth/local_runtime.go + tests, scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py
  - #1721: scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py
  - #1722: scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py

## merge-verdicts

### #1715 (0428-184) shared destroy ohne registry-cleanup — ERFUELLET
- Merge in develop: squash `2f81fa21d` (ancestor von develop bewiesen). Card-Akte listet Head `c1485721f130`, der NICHT ancestor von develop ist (veraltet / nie merge); der merge-Committer ist `2f81fa21d`.
- Akzeptanz: (1) destroy entfernt exakt die vom Owner owned registry-row + re-registration mit neuem Owner gelingt; (2) regression rot bei Löschzeile + FOREIGN-owner-Eintrag bleibt erhalten (kein cross-tenant wipe); (3) CI-job im packages-shard.
- Stelle im Code: internal/observability/registry.go `func PruneOwnedPlatformSources(provider, class, scope, boundary, missing) error` (+29/-0); Aufruf in internal/application/shared_backends_resources_runtime.go `destroyAllSharedBackendsAt` für PostgreSQL + Valkey (`environment:<env>` SharingBoundary).
- Gegen-Check (ausgeführt): `go test ./internal/application/ -run TestSharedDestroyRemovesOwnedPlatformSources` => PASS; `go test ./internal/observability/` => ok; `go test ./internal/capability/` => ok. Der test registriert postgres+valkey durch den produktiven RegisterProviderSignals-Pfad, prüft owned-Entfernung + re-registration für beide provider + foreign-(other-env)-Erhaltung.
- Rote runtime-zelle (`PR · Selected Runtime (atomic/podman/data-capabilities)`) stammt aus karte 0428-187 (consent-gate-stall), nicht aus diesem diff (kein wizard/consent geändert).

### #1716 (0428-182) postgres/valkey-metrik unsupported — ERFUELLET
- Merge in develop: `f5ce95afc` (ancestor bewiesen).
- Stelle im Code: internal/capability/reference.go postgres & valkey metrics Signal Status ObservabilityUnsupported, Mode/Protocol entfernt; internal/capability/integration_contract_test.go `TestPostgreSQLAndValkeyMetricsAreNotRequiresAdapter` + `TestPostgreSQLAndValkeyMetricsWithoutProducerFailCatalog`.
- Gegen-Check (ausgeführt): `go test ./internal/capability/` => ok. Metrik-Signale jetzt Status ObservabilityUnsupported, Mode/Protocol leer, Verification=VerifyNone, Collectable()==false — akzeptanzgerefte Aussage deckt sich.
- Scope nur internal/capability/**; adapter-wiring (#1684 #1645) out-of-scope, wie karte und diff behaupten.

### #1717 (0428-188) opaque single-use local operation grants — ERFUELLET
- Merge in develop: `3653369a` (base develop, ancestor bewiesen); card-evidence listet run 44758114769.
- Stelle im Code: internal/operatorauth/authorization.go + internal/operatorauth/local_runtime.go (grant-typ, single-use nonce); tests internal/operatorauth/local_runtime_test.go; scripts/pr-gate-plan.py + scripts/test_pr_gate_plan.py (gate-map).
- Gegen-Check (ausgeführt): `go test ./internal/operatorauth/ -run Grant` => PASS. Räume `TestLocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse` (operation/target/environment/application/management/tenant/missing) + `TestCheckLocalRuntimeGrantFailsClosedAndUsesMonotonicNonce` (unknown-operation/invalid-env/invalid-app/runtime-check-failed/missing-check). Replay-case + monotone nonce abgedeckt; nonce schützt nur versehlichen same-process-wiederverbrauch, nicht hostile local user — karte deckt sich.

### #1721 (0428-180/ci) cli2 stacked PR base im planner — ERFUELLET
- Merge in develop: `17b9d1b0` (ancestor bewiesen).
- Stelle im Code: scripts/pr-gate-plan.py `supported_pr_target_branch` akzeptiert jetzt `cli2-*` (len>5) zusätzlich zu lane-/develop; scripts/test_pr_gate_plan.py `test_stacked_cli_runner_context_resolves` (GITHUB_BASE_REF=cli2-env-policy-head => resolved).
- Gegen-Check (ausgeführt): `python3 scripts/test_pr_gate_plan.py` => 160 tests OK, inkl. `test_stacked_cli_runner_context_resolves` ok.
- Feld-PR-Check (#1714 #1718 #1684 #1645): alle vier base_ref=develop (GitHub API, heads 18e84809634e/aa3c9d2a5b79/43d3a8dc0c6c/4abc25ab6772). Regel widened base_ref von lane-* auf cli2-*; ein develop-base kann dadurch nicht ausgeschlossen werden => KEIN fund durch #1721.

### #1722 (0428-*) ci serviceaccess policy tests eng geführt — ERFUELLET
- Merge in develop: `a61905f5` (ancestor bewiesen).
- Stelle im Code: scripts/pr-gate-plan.py `SERVICEACCESS_POLICY_FILES` (policy.go, policy_explicit_test.go, policy_test.go) + new branch `targeted_plan`; scripts/test_pr_gate_plan.py `test_serviceaccess_policy_files_skip_unrelated_cli_runtime_tests`.
- Gegen-Check (ausgeführt): `python3 scripts/test_pr_gate_plan.py` => 160 tests OK, inkl. `test_serviceaccess_policy_files_skip_unrelated_cli_runtime_tests` ok.
- Feld-PR-Check: #1714 (3 files, internal/metrics/*), #1718 (1 file, cmd/baha/context_terminal_test.go), #1684 (18 files), #1645 (34 files, internal/capability+metrics/*) — keine ändert internal/serviceaccess/policy*. => #1722 routet keine der vier als serviceaccess-policy-area (normale authority-package/source-contracts-area) => KEIN fund durch #1722.
- Rote runtime-zellen an #1714/#1718 gehören zur `PR · Selected Runtime (atomic/podman/data-capabilities)`-zelle (consent-gate-stall, karte 0428-187, run 44743111417 job 136312259900; base-drift außerhalb des repositories, owner pin auf adda7599cb5b79689702f6a63a5ca802179df967 gehoben).

## funde

Kein produktfund. Die fünf merges sind inhaltlich erfüllt, durch Go-/python-tests gegen den gemergten develop-head verifiziert, und die neuen ci-auswahlregeln (#1721 cli2-base, #1722 narrow serviceaccess-routing) schließen keine der vier feld-prs (#1714 #1718 #1684 #1645, alle base=develop) aus. Die roten runtime-zellen sind dem bekannten karte-0428-187-consent-gate-stall zugeordnet.

## befundlos (durch dopplungsausschluss gesperrt)

registry.go (0428-189..194), grant/consent/rollback-desk (H-V18), unsupported/metrik-desk (H-V19), stille-erfolg-desk (H-V20, befundlos). Hier wurde bewusst nichts erneut gemeldet.

## repo-rule compliance

- KEINE subagenten (4.8): jeder schritt in dieser session.
- KEIN git add -A: nur evidence-datei geschrieben, read-only gegen baseharbor.
- KEIN push auf produkt-branches: baseharbor unverändert (worktree read-only).
- LESEN而非 ändern: #1650 #1615 #1594 sowie lane-0428-179-shell-wrapper-cells nicht berührt.
- KEIN .github/** edit, KEIN rerun/workflow_dispatch.
- WORKSPACE: alles unter /tmp/opencode/w197-0428-197-postmerge-wt/; nichts im ecosystem root angefasst.

## cleanliness

- vorher: keine container/volumes/state-verzeichnisse dieser lane eröffnet (keine docker/podman-runs in diesem shift).
- nachher: `docker ps -a` => leer; kein ambient-core-bild fremder karren berührt.
- cleanliness: OK
