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

## END_STATE

- (noch offen — Matrix VMs + hosted CI + evidence-publish)
