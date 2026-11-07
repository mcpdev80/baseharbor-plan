
## RUNDE 0427 (fortgesetzt 2026-11-07, ~22:45Z) — Kontext-Sicherung AGENTS 5.5

### Branch / Git
- Branch: `task/r27-compose-host-isolation-wip` @ `3011102aa8dbef2814b6dd90d5f3841758471ec9` (WIP-committet, auf origin).
- Drift vs develop OK: `06e4b1eaa` ancestor, Delta = exakt 3 write-set-Dateien.
- Write-Set: cmd/baha/deployment_record.go, cmd/baha/repository_runtime_fixture_test.go, cmd/baha/runtime_integration_test_support_test.go.
- Produkt-CODE (nicht test) bei cmd/baha/app_core_requirement.go:204 uses ControlPlaneOnly:true; shared SQL nicht durch ControlPlaneOnly.

### ZELLEN / HOSTS
- baha-docker (rootless docker 29.8.1): Lock 0427-110. LÄUFT aktuell ein docker-lauf (detached setsid), NICHT unterbrechen.
- baha-podman: an 0427-116-r5 (erst nach Release / nach docker-release).
- Host war stark kontaminiert: 67 orphaned container, Mem available bis auf 518MB abgеfallen → rootless dockerd ist gecrasht (unix:///run/user/1000/docker.sock unavailable). Nach full-cleanup (alle bh-container/network/vol weg, ci-data dirs weg) → available 6039MB, daemon OK.
- ambient `local` Core wird NIEMALS gelöscht/beriesührt. Nur w169-/baseharbor-ci-Orphanate cleanup.

### TEST-ERGBNISSE (docker, clean host nach cleanup)
- `TestRepositoryWorkflowRealLifecycle` SCHEITERT persistent bei Zeile 107:
  "BaseHarbor runtime is not initialized: .../w169-repository-workflow-<suffix>-iso/runtime/compose.yaml: no such file or directory"
- Ursprünglicher Verdacht (Memory-Preflight) korrigiert: MEMORY-WAIVER (withMemoryPreflightOverride(ctx,true)) HAT GEWIRKT — memory preflight FAILED-Eintrag verschwindet.
- Der `recordDeploymentBeforeMutation:551` „panic"-trace ist FALSCH-VERDEUTET: kein echter crash. Marker zeigen:
  * r27-before-stack: before runtime.Stack ✓
  * r27-after-stack: after runtime.Stack n=2956 ✓
  * r27-save-ok: record saved state=applying ✓ (SaveDeploymentRecord SUCCESS)
  * r27-save-fail: (none)
  → Die `consent == nil`-branch (Zeile 549-553) läuft normal ab: runtime.Stack→Fprint(os.Stderr)→return errConsentRequiredForCandidateSubmission. Kein SIGSEGV (strace: keins), kein panic recover(), fatal error keins.
  → Der trace ist die FAIL-CLOSED stack-ausgabe des ersten applies (kein confirm-candidate), NICHT ein crash.
- PROBLEM: Erster apply druckt KEIN confirm-hash (promptConfirmCandidateSubmission / app_candidate_consent.go:53-70 liefert nichts → first apply ohne digest). runRepositoryFixtureApply kann deshalb keinen retry mit digest auslösen.
- Folge: apply landet im consent==nil pfad, gibt typed error zurück, aber runtime/compose.yaml wird NIEMAL geschrieben → isolate runtime fehlt → test misslingt Zeile 107.
- BEOBACHTET: target dir existiert, .installation.lock da, providers/shared-backends/core/*.lock da — aber runtime/compose.yaml fehlt. Deployment record saved state=applying (also write path läuft).

### OFFENE FRAGE / NÄCHSTER SCHRITT
- Muss geklärt werden: warum schreibt der apply (state=applying, saved) KEINE runtime/compose.yaml, obwohl consent==nil pfad normal durchläuft? Möglich: apply bricht BEVOR ensureTargetRuntimeFiles (runtime/compose.yaml write) ab, weil shared Core SQL readiness / identity endpoint nicht ready (früherer Keycloak readiness timeout nach 4m).
- Diagnose-Plan: marker in ensureTargetRuntimeFiles / startControlPlaneRuntime (app_apply_lifecycle converge), und marker in promptConfirmCandidateSubmission ob digest gedruckt. Prüfen ob first apply überhaupt bis materializeResolvedApplicationBroker / convergeApplicationRuntime kommt.
- Nach klarem PASS: other 3 tests (TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI, TestRepositoryComposeWorkloadOnlyLifecycleInCI, TestRepositoryBuildWorkloadRebuildsSourceChangesInCI) — shared-SQL volume check (sharedSQLOwnedVolumeName/Identity) betrifft alle 4.

### EVIDENCE-PFADE
- Produkt-WIP (branch): /tmp/0427-compose-wt (worktree aus base repo baseharbor recovered nach tmp-sweep).
- Evidence rounds: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-07/, r27-welle5-folge-2026-11-06/.
- Diagnose-logs auf host: /tmp/iso-run-*.log, /tmp/r27-*.txt, /tmp/consent-diag.txt, /tmp/r27-sigv.txt.
