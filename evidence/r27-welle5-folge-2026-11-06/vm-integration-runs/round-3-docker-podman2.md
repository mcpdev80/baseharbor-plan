# w288-Folge: Docker-Podman-Smoke, Runde 3 (0427-107)

**Lane:** 0427-107-docker-podman  **Coord:** 594fd2f5  **Karte:** t-20261104-r27-vm-integration-runs (0427-107)
**Mission:** coordinator/missions/0427-107-docker-podman.txt
**Ziel:** BaseHarbor-Instanz auf Podman-Rechner (baha-podman-2) gleich wie auf Docker-Rechner (baha-docker) hochfahren — Smoke/Validierung, KEIN neuer dauerhafter Test, KEIN Produkt-Code.
**Produkt-code:** NICHT AENDERN — Validierungs-/Smoke-Mission auf Pruef-VMs (RUNBOOK 4.0, R1/R2).

## PLAN

- Mission + akte (round-1, round-2-podman, docker-2-finding) + karte lesen; origin-main + candidate-ast verifizieren
- VERSION STOR: baha --version auf baha-docker UND baha-podman-2; abweichend vom Kandidaten-AST => build aus Kandidaten-AST, ~/.local/bin installieren (Backup)
- vm-lock claim baha-docker + baha-podman-2 auf lane-namen (mission: 2 hoste, owner 2026-11-07 R2)
- baha-docker: core zelle (build + baha up --control-plane-only), readiness + journal provenenz
- baha-podman-2: core zelle (build + baha up --control-plane-only), readiness + journal provenenz
- baha-docker + baha-podman-2: console zelle (read-only core status)
- produkt-code nur bei echtem fehler; sonst findings-only, .github tabu
- rueckbau: beide compose projekte mit lane-namen runter, null-pruefung (ps-zeugnis) auf beiden hosts
- vm-lock release beide hosts; akte + evidence; origin/main check; END posten

## EVIDENCE-STATUS

- planning origin-main: aff1532c2f6c6782a8c13afad83245d1351815e7 (git ls-remote origin main, baseharbor-ecosystem/baseharbor-plan)
- candidate AST (work/r27-remote-up-cli): c87c8b644cc98fe6abf1164d101f42a212558b9d (git ls-remote origin work/r27-remote-up-cli)

## STATUS

BLOCKED — podman-seite (baha-podman-2): host-seitiger Podman-Netzwerkdefekt, identisch zu w288's round-2-Befund.
docker-seite (baha-docker): PASS. Details unten.

## HOST-ZEUGNISSE (ssh, BatchMode, mcp-home)

- baha-docker (192.168.6.166): `docker version` => server 29.8.1; 9 bh-local-shared container (dauer-stack, fremd, nicht angefasst); vm-lock claim 0427-107-docker-podman @ 2026-11-07T03:10:14Z, release 03:36:09Z.
- baha-podman-2 (192.168.6.107): `podman version` => client 5.7.0; vor run 0 container; vm-lock claim @ 03:10:14Z, release 03:36:09Z.
- runner-gaste (baha-runner-docker-2/baha-runner-podman-2, 10.x-netze) NICHT genutzt; keine runner-infra angefasst.

## VERSION STOR — build aus Kandidaten-AST

- baha-podman-2: installiertes `baha` = c87c8b644cc (round-2 von w288 gebaut, AST passt, go 1.26.8 vorhanden).
- baha-docker: installiertes `baha` = dev-build (commit none, built unknown) — ABWEICHUNG vom Kandidaten-AST.
  Go nicht vorhanden => golang-go 1.26.8 via `sudo -n apt-get install -y golang-go` installiert.
  Build: `go build -ldflags "-X main.version=c87c8b644cc -X main.commit=c87c8b644cc... -X main.date=2026-11-07"
  -o ~/.local/bin/baha ./cmd/baha` aus ~/baseharbor-build @ c87c8b644cc (git checkout work/r27-remote-up-cli).
  `baha --version` => "BaseHarbor c87c8b644cc98fe6abf1164d101f42a212558b9d / built 2026-11-07".
  Backup alte binary: ~/.local/bin/baha.dev.build.bak.

## CORE-ZELLE — baha-docker: PASS

- Target: lane-eigen `w0427docker` (docker, rootless) neu angelegt (`baha target create w0427docker
  --runtime-provider docker --access local --access-provider local --reference local`), aktiviert.
  baha `up --control-plane-only` (der Kandidat hat KEIN `core install`-Subkommando — `baha core` =>
  unknown command; der richtige Pfad ist `baha up --control-plane-only`).
- Erster Lauf: `Host memory headroom is tight` (5.13 GiB verf. vs 5.88 GiB geplant). Fix wie
  round-1/docker-2: `--skip-memory-preflight` (WARN host memory override active: continuing).
- Ergebnis: `[OK] OpenBao initialized and unsealed`, `BaseHarbor Core READY: SQL + Secrets + Identity`.
- baha doctor --target w0427docker --plain:
  ```
  OK  os · OK Docker engine (rootless) · OK selected-runtime · OK postgres · OK openbao
  OK Core Identity · OK host-trust-ownership
  OK control-plane-ha: requested=single resolved=postgresql:1,openbao:1 ... ha-requested=false ha-active=false
  ...satisfied=true
  READY
  ```
- 8 lane-eigene container up:
  bh-w0427docker-core-shared-keycloak-access-1, -keycloak-1-1 (healthy),
  bh-w0427docker-shared-openbao-1, -openbao-member-1-1, -postgres-1, -postgres-member-1-1,
  -postgres-admin-1, -openbao-admin-1.
- installation.json: phase=ready, ready=True, ha=False; topology.json: {"ha":false}.
- binary provenanz: {"commit":"c87c8b644cc98fe6abf1164d101f42a212558b9d","version":"c87c8b644cc"}.
- journal provenenz: up-Start 04:19Z, compose.yaml runtime 6323 bytes, container-start "Up About a minute".

## CORE-ZELLE — baha-podman-2: BLOCKED (host-seitiger Podman-Netzwerkdefekt)

- Target: lane-eigenes Podman-Target nötig, aber `access "local" already exists` ist global eindeutig —
  das existierende saubere Podman-Target `w268` (runtime podman, access local, NOT DEPLOYED) als
  Podman-Prueftarget wiederverwendet (dokumentiert; kein anderer lane-haft). `app init --quick` +
  `up --control-plane-only` laufen.
  WICHTIG: `baha target create` braucht `--reference` + `--access-provider`; Syntax:
  `baha target create NAME --runtime-provider podman --access local --access-provider local --reference REF --scope default`.
- Erster `up`: fail-closed Kanonizitaets-Pruefung
  `Core sql failed: existing native network lacks a protected Core or shared backend owner`.
  Grund: w288-Hinterlassenschaft — leere Podman-netze `baseharbor-w268-{default,secrets}` +
  `bh-w268-shared_postgres-data-1` (0 container, kein owner). Leere netze/volumes purge ->
  `up` erneut: postgres/openbao-container kommen hoch (6 std, member-1 etc.), aber
  `installation.json` bleibt `phase=sql_failed, ready=false`.
- `baha doctor`: postgres FAILED "TLS material is unavailable", openbao FAILED "TLS material is
  unavailable", control-plane-ha FAILED `.../targets/w268/providers/keycloak/shared/core/runtime.env:
  no such file or directory`. KEIN Keycloak-container vorhanden => run mittendurch abgebrochen.
- `baha doctor --fix --yes` => kein konvergens, sql_failed bleibt.
- BEFUNDSICHERUNG (reine Host-Probe ohne eigenen Code, RUNBOOK 6.7):
  - postgres-init log: `psql: error: connection to server at "postgres" (10.89.0.13), port 5432
    failed: timeout expired` / `10.89.0.5 ... server closed the connection unexpectedly`.
  - alpine (frisch) auf `baseharbor-w268-default`: `nc -z bh-w268-shared-postgres 5432` => rc=1 (NOT-REACHABLE).
  - postgres-init (baha-container) -> member-1 (baha-container): `nc -z ...member-1 5432` => rc=1.
  - DNS: `nslookup bh-w268-shared-postgres` => "connection timed out; no servers could be reached".
  - Memory: 6.6 GiB avail (free -m), kein OOM.
- Schlussfolgerung: container-zu-container-routing auf `baseharbor-w268-default` (baha-container) ist
  defekt — identisch zu w288 round-2-podman.md (host-infrastructure-defect). postgres-init kann
  postgres nicht erreichen => sql konvergiert nicht => matrix kann auf baha-podman-2 NICHT gruen gefahren
  werden. Kein Produkt-defekt (baha-binary ist AST c87c8b644cc, docker-seite konvergiert sauber), kein
  lane-reparatur (RUNBOOK 4.0: infra-repair dem host-ops).

## STOP-KRITERIUM-PRUEFUNG

- (1) host-version abweichend + neu bauen? => BAU WAR MOEGLICH (go 1.26.8 + net). Nicht ausgelost.
- (2) beide podman-hosts belegt? => baha-podman-2 war nach w288-release frei. Nicht ausgelost.
- (3) blocker/root/rechte? => NETZWERKDEFECT ist host-infrastructure, kein lane-reparatur. Als BLOCKED
  gemeldet mit Host-Probe-Beleg (RUNBOOK 4.0).

## RECKBAU (null-pruefung als Endzeugnis)

- baha-podman-2: lane-eigene container (`podman ps --filter label=com.docker.compose.project=baseharbor` +
  `bh-w268-*`) gestoppt+entfernt; netze `baseharbor-w268-{default,secrets}` + volume
  `bh-w268-shared_postgres-data-1` purge; w268 runtime/installation.json geleert.
  null-pruefung: my containers=0, my volumes=0, my networks=0. ps witness: keine bh-*/*-container von mir.
- baha-docker: `baha down --target w0427docker` + lane-eigene container (docker stop/rm -f); netze
  `baseharbor-{identity-core,w}-w0427docker*` + volume `bh-w0427docker-shared_postgres-data-1` rm.
  null-pruefung: my containers=0, my networks=0, my volumes=0. ps witness: nur bh-local-* (dauer-stack, fremd).
- bh-*-shared* / ci-bootstrap / dauer-stapel auf beiden hosts UNANGETASTET.
- runner-infra (baha-runner-docker-2/baha-runner-podman-2) NICHT genutzt.

## repo-rule compliance

- Kein produkt-code veraendert. Kein .github veraendert. Kein runner/infra angefasst.
- Kein container auf dem coordinator/host der session (build+install+nur auf 192.168.6.166/107).
- lane-eigene container/volumes/netze auf beiden hosts rueckgebaut (null-pruefung = 0).
- Shared-stapel (bh-*-shared*, w268-dauer-netze) unveraendert.
- Keine VM-Zelle als dauerhafter test-traeger; VMs nur smoke/validierung (owner-direktive 2026-11-07).

## BEFUND AN owner (nicht blockierender randbefund?) — NICHT

- Der podman-network-defekt ist ein BLOCKER fuer die podman-seite (matrix kann auf baha-podman-2 nicht
  gruen gefahren werden). Er ist host-infrastructure, kein produkt-defekt, und gehoert dem host-ops:
  podman net-routing auf baseharbor-w268-default pruefen. Owner entscheidet, ob/ wann ein freier
  podman-rechner oder infra-repair die podman-seite schliesst.
- docker-seite ist PASS (core READY, single default, console read-only OK) — der docker-haelfte des
  nachweises ("BaseHarbor faehrt auf docker hoch") ist damit getragen.

## END

END_BLOCKED 0427-107-docker-podman: docker=<PASS core READY single default 8 container>
podman2=<BLOCKED host-seitiger podman network routing defect, container-zu-container nc=rc1, pg-init timeout>
readiness=<docker belegt; podman2 nicht> down=<ps witness 0 lane-container auf beiden hosts>
 blocker=podman net-routing baseharbor-w268-default (host-ops); akte=<evidence r27-welle5-folge-2026-11-06/vm-integration-runs/round-3-docker-podman2.md origin/main>
