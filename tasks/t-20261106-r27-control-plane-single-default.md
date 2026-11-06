---
id: t-20261106-r27-control-plane-single-default
type: task
areas: [platform, runtime, testing]
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Die develop-Kontrollebene faehrt im Default als Einzel-Instanzen (ein Postgres, ein OpenBao), weil die Entwickler-Umgebung laut…"
kanban_title: "Control plane: default deployment must be SINGLE instances (per-service one postgres/one openbao, no HA ensemble); HA only as explicit opt-in"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261106-r27-control-plane-single-default · Control plane: default deployment must be SINGLE instances (per-service one postgres/one openbao, no HA ensemble); HA only as explicit opt-in #task #release/v0-4-27 #status/planned #view/ready #area/platform #area/runtime #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Die develop-Kontrollebene faehrt im Default als Einzel-Instanzen (ein Postgres, ein OpenBao),
weil die Entwickler-Umgebung laut Owner genau so gemeint ist. Heute zeigt der Auslieferungs-Standard ein
HA-Ensemble (3 OpenBao-Mitglieder + Balancer). Die Einzel-Form wird Default; HA bleibt als
explizit waehlbares Profil erhalten.

## Scope

- In scope: Ausgelieferte Compose-Assets, Default-Profilwahl, wirksamer Startpfad (`baha up` und devenv), Postgres/etcd, OpenBao, Keycloak, HAProxy und zugehoerige Initialisierung, Endpunkte, Persistenz und Profil-Validierung. Default darf keine zusaetzlichen HA-Mitglieder, Balancer oder Quorum-Abhaengigkeit starten.
- In scope: Explizite HA-Wahl mit korrekter vollstaendiger Clusterkonfiguration und sichtbarer Auswahl; Bestand darf nicht durch ein Upgrade oder erneutes `up` unbemerkt zwischen SINGLE und HA wechseln.
- Out of scope: Produktive Bestandsumgebungen automatisch abbauen, unabhaengige Anwendungs-Workloads veraendern oder HA ersatzlos entfernen.

## Proof / Befund (coord-Nachmessung 2026-11-06 14:1xZ, origin/main develop)

- Owner-Direktive woertlich: "openbao ist da insgesamt 4 mal zu sehen ist der aufbau als ha das
  waere komplett falsch es sollte default sein das nichts ha ist sondern einzeln".
- Produktbeleg: internal/runtime/assets/compose.yaml definiert offenbao-member-1/2/3 (Zeilen
  268/297/326) + haproxy (356) + postgres-etcd 1-3 (Zeilen 10/23/36) — das mitgelieferte
  Standard-Template IST das HA-Ensemble.
- Go-Seite kennt bereits beide Formen: internal/runtime/control_plane_profile.go
  (OpenBaoMembers 68-73, validateSingleControlPlane 75) — Einzel-Pfad existiert, ist aber nicht
  der Default des Assets.
- Live-Zeuge: baha-docker `docker ps` nach devenv-smoke-Aufbau: bh-local-shared-openbao-member-1/2/3
  + -admin + haproxy = 4-5 Tresor-Container; identisch bh-w169-ci-ctxa (CI-Kontext).

## Acceptance (verbindliche Owner-Abnahme, keine Ausnahme durch gruenen Build)

- Frischer unveraenderter Standard-Start (`baha up` ohne HA-Flags/Profiles/Overrides) erzeugt exakt EINE aktive Instanz je erforderlichem Control-Plane-Dienst auf Docker UND Podman. Insbesondere genau ein OpenBao und ein PostgreSQL; keine OpenBao-Mitglieder 2/3, kein HAProxy-HA-Balancer, keine dreifache etcd-/Keycloak-Kontrollebene und keine erzwungene Cluster-Quorum-Bedingung.
- Der ausgelieferte DEFAULT ist SINGLE auch ohne CLI-Optionen: gerendertes `docker compose config` bzw. Podman-Aequivalent zeigt die richtige Topologie; Test der *tatsaechlichen* Startpfade weist per Containerinventar und Service-Health dieselbe Topologie nach. Separate `validateSingleControlPlane`-Unit-Tests allein sind unzureichend.
- HA ist ausschliesslich nach einer ausdruecklich dokumentierten Opt-in-Auswahl aktiv; mit Opt-in startet das vollstaendige gewaehlte Ensemble gesund, einschliesslich Cluster-Mitgliedschaft/Endpunkte. Ohne Opt-in duerfen keine HA-Services im gerenderten Aktivprofil auftauchen.
- SINGLE und HA funktionieren nach Neustart und `up` erneut; Konfiguration, PKI/Initialisierung, Ports und Persistenz entsprechen dem gewaehlten Modus. Bestehende HA-Installationen werden nicht stillschweigend umgebaut oder geloescht; bei Moduswechsel ist eine bewusste, sichere Entscheidung erforderlich.
- Red-first: Regressionstest wird gegen den bisherigen DEFAULT nachweislich ROT und nach dem Fix GRUEN. Zweite negative Zelle: HA wird ohne Opt-in abgelehnt/nicht gestartet. Positive HA-Zelle: explizites Opt-in startet das richtige Ensemble. Eine Quellcode-Mutante, die HA ungefragt aktiviert, macht den Test ROT.
- Alle Belege enthalten exakten Produkt-SHA, Host/Runtime, Befehle, Compose-Konfigurationsausgabe, Container-/Service-Liste, Health-Zustaende und eindeutige PASS/FAIL-Zeilen; keine SKIP-Zelle ist PASS. Gehostete CI allein ersetzt reale Docker-/Podman-Nachweise nicht.
- Vor Merge: Reviewer prueft Code UND echte ausgefuehrte DEFAULT-/HA-Pfade gegen diesen Vertrag. Fehlende oder uebergangene Laufzellen = BLOCKED.

## Required checks

- Deterministische Tests fuer Default-Profil, Compose-Render-Ergebnis, CLI/Devenv-Startpfad, Single-Control-Plane-Validierung und HA-Opt-in; Red-first und Mutanten-Gegenprobe dokumentieren.
- Echte isolierte Smoke-Matrix auf `baha-docker` und `baha-podman`: je Runtime (1) Default-SINGLE mit exakter Instanzanzahl und Health, (2) explizites HA mit Cluster-Health, (3) Restart/Idempotenz und persistente Daten. Autorisierte Test-VMs nutzen; KEINE Testlaeufe auf dem Codeman-/Coordinator-Host `baha-runner-docker-2`.
- Gezielte Go-Tests, Build, Vet, Format und GitHub Selected Checks am finalen SHA sowie reale Run-Transkripte im Planning-Repo. Gruene uebersprungene Runtime-Gates zaehlen nicht.

## Dependencies and file ownership

- Federfuehrende Aenderung an `internal/runtime/assets/compose.yaml`, der Control-Plane-Profilwahl und den Startpfaden. Vor Aenderung andere aktive Besitzer der betroffenen Dateien pruefen und koordinieren; keine konkurrierenden Edits.
- Abnahme-Verknuepfung mit `core-815`, `t-20261105-r27-compose-host-isolation` und `t-20261104-r27-vm-integration-runs`. Der Default-Vertrag muss vor der abschliessenden Release-Qualifikation erfuellt sein.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
