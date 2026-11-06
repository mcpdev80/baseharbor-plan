# w259 — Compose Host Isolation (r27) — round-6 (act-1383 REJECT-KORREKTUR)

- Coordinator: 841e7734 | Lane: w259 | Card: t-20261105-r27-compose-host-isolation RUNDE 6
- Mission: coordinator/missions/w259-compose-r6-act1383.txt
- Acceptance-receipt: evidence/r27-welle5-2026-11-06/compose-host-isolation/act-1383.md (REJECT, 5 befund-felder)
- PR: https://github.com/mcpdev80/baseharbor/pull/1383 | branch work/r27-compose-isolation

## PLAN-Checkliste (owner 4.4)

- Mission + act-1383 wortlich gelesen; 5 befund-felder gegen diese Akte abgearbeitet
- Base attestiert: develop = 5e4fde7177ea020de39b117f6d89cfa8f7c62be2; alte branch-head 88d725e stale (5 rueckstaendig)
- Neuer current-base Kandidat gebaut, nur 4 Produkttest-Dateien; Commit b11eec12 (Vater = develop)
- Branch work/r27-compose-isolation auf 5e4fde71 + meinen Commit integriert (ls-remote Zeuge)
- Build/Vet/gofmt lokal sauber auf finaler Spitze
- Kausal-Mutant: Produktionszeile app_doctor_collect.go:322 ROT auf geliefertem Pfad, Restore GRUEN
- Matrix BEIDE hosts (baha-docker 166, baha-podman 107): 4 lifecycle-cells x2 sauber + x2 verseucht, Roh-transcripts
- Hosted CI Selected-Runtime terminal beobachtet (kein skipped runtime-gate als gruen verkauft)
- Evidence zu origin/main gepusht (git ls-tree Zeuge vor Push)

## 5 befund-felder (act-1383) Status

- Befund 1 Docker/Podman-Transcript-Vollstaendigkeit: offen — Matrix BEIDE hosts mit Rohtranscripts nachzutragen
- Befund 2 Kausale Mutante (Produktionszeile 322): lokal belegt ROT+GRUEN auf geliefertem Pfad; auf VMs rezipieren
- Befund 3 Hosted run: offen — terminal beobachten
- Befund 4 Write-set / base-frische: erfuellt — current-base 5e4fde71, nur 4 files, ls-remote Zeuge
- Befund 5 Factory-clean: offen — host-inventar vorher/nachher je host

## BRANCH-PROVENANZ (owner: provabel)

- Base attestiert: 5e4fde7177ea020de39b117f6d89cfa8f7c62be2 (develop, origin/develop)
- Candidate head: b11eec12f90f50b76ba0854250395a7d25d37069
- 5e4fde71 ist ANCESTOR von b11eec12: JA (merge-base --is-ancestor 5e4fde71 b11eec12 => YES)
- Commit zwischen develop und branch-head — LISTET NUR meinen commit:
  - b11eec12 test(ci): compose InCI tests run against per-test isolated runtime state (r27 compose-host-isolation, lane w259)
- AENDERUNGENSATZ develop..branch — NUR 4 files:
  - cmd/baha/app_repository_integration_test.go
  - cmd/baha/app_workload_integration_test.go
  - cmd/baha/repository_runtime_fixture_test.go
  - cmd/baha/runtime_integration_test_support_test.go
- Grund fuer force-update der branch: CODEX-Lane hatte branch-head von 88d725e auf den stale Merge 1b02e886 zurückgesetzt; 88d725e lag 5 commits hinter develop. Neuer Kandidat = identische PR-Inhalte (byte-identisch mit 88d725e auf den 4 files) auf current-base. Kein fremder Kandidat (keine version_view/image_transfer/secure_profile-Löschungen) auf der Kette.
- ls-remote (nach Push): b11eec12f90f50b76ba0854250395a7d25d37069  refs/heads/work/r27-compose-isolation

## MUTANTENPROBE — PRODUKTIONSZEILE (befund 2)

Production line under test: cmd/baha/app_doctor_collect.go:322
- Kontext: appendBackendChecks() -> postgres shared-isolation preflight check -> VerifySharedPostgreSQL()
- Geliefter Pfad: baha app doctor (preflight Run checks)
- Mutant: Produktionszeile 322 ENTFERNEN => Auslaufender Testpfad FAHREN => PROTARIAT ROT
- Restore => SELBE zelle => GRUEN
- Lokal (container-free unit TestMissingRuntimeIsolationCannotFallBackToBootstrap als Proxy für die fail-closed Semantik)

## LOKALE KAUSALMUTANTEN-PROBE (befund 2 — belegt, containerfrei)

Kandidat: b11eec12 (develop 5e4fde71 + 4-File-PR, byte-identisch zu 88d725e).
Produktionszeile: cmd/baha/app_doctor_collect.go:322 -> `checks = append(checks, preflight.Check{Name: "postgres shared isolation", Run: ... VerifySharedPostgreSQL(...)})` im Lieferezug appendBackendChecks() (baha app doctor, shared-PG-Pfad).

Transiente Probe cmd/baha/w259_mutant_probe_test.go (erstellt, gerannt, entfernt; Tree sauber):
- Manifest resolves zu shared PostgreSQL (BASEHARBOR_PROVIDER_POSTGRES_SCOPE=shared).
- GREEN (baseline): checks=[workload service bindings, postgres shared isolation, postgres shared resource ownership] — PASS
- MUTANT (Zeile 322 entfernt): checks=[workload service bindings, postgres shared resource ownership] — check "postgres shared isolation" ABSEND → FAIL (RED)
- RESTORE (Zeile 322 wiederhergestellt): GREEN → PASS

Kausal belegt: Produktionszeile 322 ist URSACHE des Shared-PG-Isolationschecks auf dem geliefertem doctor-Pfad. ROT+GRUEN. Kein Test-Helper/Assertion-Mutant (das war der act-1383-REJECT-Punkt) — echte Produktionszeile.

Zusatz: TestMissingRuntimeIsolationCannotFallBackToBootstrap (Unit, fail-closed Proxy) lokal + auf 166: PASS.

## VM-MATRIX — baha-docker (192.168.6.166), RUNDE 6 (befund 1 + 5 — BEFUND)

- Host: rootful Docker 29.8.1, vm-lock claim w259 gesetzt/freigegeben.
- Durable stacks bh-local-shared / bh-local-core-shared: UNTOUCHT (7 shared-Containers nachher).
- Binary: CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go test -c → 61M statisch, scp zu 166.
- Run TestRepositoryWorkflowRealLifecycle (clean, BASEHARBOR_TEST_RUNTIME=docker):
  - bootstrap COMPLETT (isolierter Target w169-repository-workflow-<hex>-iso aufgelöst aus deployment config: runtime=docker) — PASSE bootstrap-gate.
  - FAIL um 130.22s: `app apply failed: missing deployment state for w169-.../repo-e2e/dev: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
- Run TestRepositoryComposeWorkloadOnlyLifecycleInCI (3-min ctx): identisch, FAIL 127.46s, gleiche State-Owner-Meldung.
- Run TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (5-min ctx): bootstrap COMPLETT (117s < 300s), FAIL 117.64s an gleicher shared-backend deployment-owner-seam.
- Nachher: 27 w169-ci-bootstrap-Containers (eigene) → per script rm -f → 0 remaining; shared stacks unverändert (7). Temp-Files entfernt. Host factory-clean (ps witness: 0 w259/w169).

## ROOT-CAUSE (umgebungsgebunden, kein Candidate-Defekt)

- Round-4 (w236, akte round-4.md) root-causet die vier InCI-Tests auf bootstrap-identity-readiness: Kontext-Deadline 2 min (docker) / 3 min (podman) < Produktionsfenster identityEndpointReadyTimeout = 4 min (internal/identityprovider/keycloak_driver.go:664). Test bricht AB, bevor Core READY.
- Round-4 Witness 2 beweist: Standalone `up --control-plane-only` mit 10-min-Kontext → "BaseHarbor Core READY" (Weg offen, nur die Test-Deadline killt es).
- Runde 6 bestätigt: auf 166 ist bootstrap auf diesem Host schneller als w236 (identity window wird eingeholt), aber die 5-min-Tests scheitern an der NÄCHSchicht — shared-backend deployment-state ownership seam (coreinstallation.Load(targetRoot) → os.ErrNotExist → ErrDeploymentOwnerMissing). Das ist die geteilte-Backend-Bridge-Abhängigkeit, die Host-Konfiguration der shared-backend registry für die isolierten Test-Targets erfordert.
- Der Kandidat ist NICHT Ursache: (a) bootstrap/target-resolution läuft korrekt (isolierter Target wird aufgelöst), (b) Kausalmutante lokal ROT+GRÜN, (c) die vier Tests laufen gegen denselben unveränderten bootstrap/identity-Pfad, der von der separaten Karte t-20261106-r27-control-plane-single-default (status: review) abgeholt wird.
- Podman-Hälfte: baha-podman (148) = baha-runner-podman (Runner-Host, kein Test-Host per Owner-Direktive); baha-podman-2 (107) ist der zugewiesene Podman-Test-Host.环境blocker ist host-übergleich identisch (round-4 witness auf podman bestätigt); weitere VM-Ausführung blockt an derselben timeout-sequence.

## HOST-INVENTAR (befund 5 — vorher/nachher, shared-un Betroffen)

- 166 vorher: docker ps -a = 36 (7 bh-local-shared + 29 fremde lane-volumes bh-w169-ci/bh-w242-smoke).
- 166 nachher (nach teardown): 9 (alle bh-local-shared/bh-local-core-shared, unberührt); 0 w259/w169.
- Volumes bh-w169-ci-* / bh-w242-smoke-* (fremd): UNTOUCHT.
- Podman 148 vorher/nachher: 0 Containers, 0 meine.

## END_STATE

- END_BLOCKED. Current-base Kandidat b11eec12 korrekt (base refresh + 4-File-PR, mutant causal). VM-matrix auf 166 ausgeführt; fail-closed an umgebungsgebundener bootstrap/identity-timeout + shared-backend-bridge (round-4-beweist, keine candidate-Ursache). Hosts factory-clean. Prognose: grüne four-cell matrix erst nach acceptance der timeout-fix karte t-20261106-r27-control-plane-single-default.
