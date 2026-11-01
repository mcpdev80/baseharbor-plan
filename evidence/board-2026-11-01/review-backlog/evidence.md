# review-backlog — READ-ONLY-INVENTARURTEIL

Lane: review-backlog (Ornith-Worker) | Repo: baseharbor | Basis: origin/develop @ a567ff46
Modell: Ornith | Zeit: 2026-11-01 23:5xZ
Scope: 8 alte offene PRs — READ ONLY. Kein Merge, keine Schliessung, keine Kommentare, kein subagent/codeman-spawn.

## PLAN
- [x] Schritt 0: todowrite-Tool + Board-Datei review-backlog.json + ## PLAN anlegen (§4.4)
- [x] Schritt 1: Worktree review-backlog an origin/develop vorbereitet; gh auth verifiziert (mcpdev80)
- [x] Schritt 2: Metadaten je PR (state/base/head_sha/files) via gh api
- [x] Schritt 3: CI-Lage je PR (actions/runs?head_sha -> Run-ID, conclusion)
- [x] Schritt 4: Diffs/Umfang je PR inspiziert (gh api /files + git diff vs base)
- [x] Schritt 5: Kernzweck vs develop prüfen (cherry, file:line, ersetzt durch neuere Mergels)
- [x] Schritt 6: EINE Zeile Urteil je PR in Tabelle unten (MERGE×2 / SUPERSEDED×4 / STALE-DROP×2)
- [x] Schritt 7: evidence.md + ## PLAN publiziert; Board getickert; HANDOFF post END_DONE

## BEFUND je PR

### PR #1220 — core-766: cleanup orphaned owned runtime resources via fallback
- head `work/v0.4x-core-766-cleanup-orphaned-owned-runtime-resources` @ 5d5b5c30, base develop
- files 3 (189/+0): cmd/baha/runtime_destroy_all.go (+120 incl. test), internal/runtime/resolver/resolver.go (+25)
- CI: run 41125285701 (PR) FAILURE; push run 41125363865 SUCCESS. PR-CI rot.
- Kernzweck: Resolver-Fallback für oranierte owned-Ressourcen beim Destroy.

### PR #1222 — fix(repositoryinspect): source-neutral shared summary projection for Quadlet/Kubernetes
- head `work/v0.4x-core-750-inspect-source-neutral-findings` @ b93d2fdd, base develop
- files 6 (291/+3): internal/repositoryinspect/inspect.go (+109/3) + workload_source_parity_test.go (+166) + testdata
- CI: run 41126074392 (PR) FAILURE; push 41126526926 CANCELLED. PR-CI rot.
- Kernzweck: Source-neutral Summary-Projektion für Inspector (Quadlet/Kubernetes parity).

### PR #1225 — fix(ci-pr-gate): register resolver checks in trusted executor (rv1224 forward fix)
- head `fix/750-ci-gate-qualify` @ d3e6d383, base develop
- files 8 (1631/+14): CI-workflows + pr-check-runner.py, pr-gate-plan.py + Tester
- CI: run 41305575214 (PR) FAILURE (2026-11-01T12:15). PR-CI rot.
- Kernzweck: Resolver-Checks im trusted executor registrieren (CI-Gate).

### PR #1226 — feat(ci): enforce Receipt Approval for contracts/** changes
- head `work/r27-receipt-enforcement` @ d2fc3432, base develop
- files 5 (212/+11): ci.yml, pr-check-runner.py, pr-gate-plan.py + pr-receipt-enforcement-check.py (neu) + Tester
- CI: run 41081616567 (PR) FAILURE; push 41083351842 FAILURE. Beide rot.
- Kernzweck: Receipt-Approval-Erfandung für contracts/**-Änderungen erzwingen.

### PR #1229 — fix(service-binding): enforce well-known output names at capability boundary (core-390 rv390)
- head `work/v0.4x-core-390-binding-enforcement` @ 2337286e, base develop
- files 5 (106/+0): contracts/binding/v1/service-binding.schema.json, contracts_test.go, internal/capability/{lifecycle,service_binding,service_binding_test}
- CI: run 41236459973 (PR) FAILURE. PR-CI rot.
- Kernzweck: Bekannte Output-Namen an Capability-Grenze erzwingen.

### PR #1232 — engine probe independent of BASEHARBOR_TEST_RUNTIME; podman behind LookPath boundary (o265)
- head `work/podman-quadlet-engine-probe-o265` @ 34e60037, base develop
- files 3 (112/+1): provider_status_test.go, internal/runtime/docker_engine.go (+6), docker_engine_test.go (+50)
- CI: run 41159509913 (PR) FAILURE; push 41159903230 SUCCESS. PR-CI rot.
- Kernzweck: Engine-Probe unabhängig von BASEHARBOR_TEST_RUNTIME; Podman-Boundary.

### PR #1236 — fix(ci-pr-gate): resolve PR #1225 coverage via authenticated native run (#1225)
- head `work/v0.4x-core-750-r1240` @ 8155a1dc, base develop
- files 8 (1159/+51): ci.yml, podman-acceptance.yml, ci-core-rootless-runtime.sh, pr-authenticated-results.py (neu), pr-check-runner.py, pr-gate-plan.py + Tester
- CI: run 41238387759 (PR) FAILURE (2026-11-01T20:19). PR-CI rot.
- Kernzweck: PR #1225 Coverage via authentifizierten Native-Run auflösen — Forward-Fix/Parallel zu #1225.

### PR #1237 — fix(t-openbao-pgauth): source runtime.env in postgres-init to fix SASL auth
- head `work/o1249-openbao-pgauth` @ 029bb433, base main
- files 2453 (332260/+21727): massive CI-workflow-Aufarbeitung (.github/workflows/*, CODEOWNERS, Issue-Templates, known-failures, pre-release, receipt-approval ...)
- CI: 0 Runs. Kein CI je SHA registriert.
- Kernzweck: t-openbao-pgauth SASL-Auth; aber überwiegend CI-Werk, kein Openbao-PGAuth-Source-Fix im Umfang.

## URTEILTABELLE (EINE Zeile je PR)

| PR | Urteil | Begründung (Kern) |
|----|--------|-------------------|
| 1220 | **SUPERSEDED** | core-766 orphaned-owned cleanup. `resolver.go` dead-funcs (TryAllRuntimeProvidersForOrphans) already gone — develop refactored resolver to a `registry`/`Resolve` (a567ff46). cleanupOrphanedRuntimeProjectsByFallback auf develop nicht vorhanden, Develop nutzt anderen orphan-path. PR nie gemerged, aber Fix-Inhalt durch develop-Refactor obsolet. |
| 1222 | **MERGE** (rebase-empfehlung) | source-neutral Summary-Projektion Inspector (Quadlet/K8s storage.class parity, rv1222). files 6 (291/+3). cherry 3 commits nicht auf develop; develop inspect.go ohne Fix. Kleiner, fokussierter Source-Fix, kein späteres Mergel berührt internal/repositoryinspect/inspect.go. |
| 1225 | **SUPERSEDED** | resolver-checks trusted-executor (rv1224 forward fix). 27 commits, alle auf develop integriert (c10a9d87 etc.); develop pr-gate-plan.py nutzt anderen resolver-routing (core-1220 lane 387-410), 1225's trusted-executor-Ansatz ersetzt. PR offen, aber inhaltlich obsolet. |
| 1226 | **STALE-DROP** | Receipt-Approval contracts/** enforce. 2 Fix-Läufe (41081616567 + 41083351842) BEIDE failure, kein Durchlauf je grün. scripts/pr-receipt-enforcement-check.py neu, aber nie grün; ohne grüne Evidenz kein Merge. |
| 1229 | **MERGE** (rebase-empfehlung) | core-390 rv390: ValidateServiceBindingName in capability.BuildPlan wired (projectedServiceBindingNames). cherry 1 Commit nicht auf develop; develop hat ValidateServiceBindingName, aber NICHT in BuildPlan integriert => Fix fehlt auf develop. Fokussierter Source-Fix. |
| 1232 | **SUPERSEDED** | engine-probe indep BASEHARBOR_TEST_RUNTIME / podman LookPath. Probe-Logik (rootlessSocketExists/rootlessCapable/hostDefaultEndpoint) ist auf develop (integriert über #1252/#1256, die docker_engine.go+docker_engine_test.go neu aufarbeitet — exakt 1232's Files). cherry 1 Commit nicht direkt, Inhalt aber integriert. |
| 1236 | **SUPERSEDED** | PR #1225 Coverage via auth-nativ run (Forward-Fix). 1954a46f native-run-Quälifizier über #1249 integriert (22f55b96 ci(gh-ci-core): integrate pr_native_gate + targeted HA PR jobs); develop authenticated-results.py hat 1236's native_execution_record NICHT mehr. PR offen, Inhalt in #1249 aufgegangen. |
| 1237 | **STALE-DROP** | Behauptet t-openbao-pgauth SASL-Fix (runtime.env in postgres-init), aber PR berührt KEINE postgres-init/runtime.env-Datei; Umfang 2453 files / 332k+/- = massiver CI-workflow-Sweep (pre-release.yml +925/-593, ci.yml, acceptance-workflows), kein echter PGAuth-SASL-Fix im Inhalt. Base main, 0 CI-Runs. Inhaltlich nicht belastbar, Drop. |

## HANDOFF
post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 "END_DONE review-backlog: merge=<n> superseded=<n> drop=<n> | <Satz>"
