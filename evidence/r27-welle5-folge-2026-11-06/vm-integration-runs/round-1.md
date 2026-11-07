# w269-vm-integration-runs — Evidence (round 1)

**Lane:** w269-vm-integration-runs  **Coord:** ec2254ac  **Karte:** t-20261104-r27-vm-integration-runs
**Reihenfolge:** matrix-farben auf baha-docker (166) + baha-podman (148); docker-2 = BEFUND (eigene karte)
**Host:** baha-docker (baha-runner-docker, 192.168.6.166, vm-lock claim w269)

## R1-VORFALL (Koordinator-Host, 2026-11-06 ~22:1xZ)

- FEHLGRIFF: `baha up --control-plane-only` lief auf dem COORDINATOR-HOST ins LOKALE docker-socket
  (kein target-context auf die ferne host umgeschaltet). 9 `bh-local-*` container liefen seit ~22:1xZ.
- AKTION (coord ec2254ac, notes/w269-r1-cleanup.txt): 9 container stop+rm, private netzwerke/volumes
  rueckbauen, nur lane-eigene mittel, KEIN anfassen des dauer-stacks.
- ZEITACHSE:
  - ~22:00 claim baha-docker (166) auf w269.
  - ~22:1xZ `baha up --control-plane-only` auf dem coordinator-dev-host => container liefen lokal.
  - 23:1xZ vm-audit meldet 8+ bh-local-container auf dem coordinator-host.
  - rueckbau: stop (9) => rm --force (9) => network rm (2) => volume rm (1).
- KOMMANDO-ZEUGNIS (rueckbau-aequivalenz):
  - `docker stop bh-local-core-shared-keycloak-access-1 bh-local-core-shared-keycloak-1-1 bh-local-shared-openbao-1 bh-local-shared-openbao-member-1-1 bh-local-shared-postgres-init-1 bh-local-shared-postgres-1 bh-local-shared-postgres-member-1-1 bh-local-shared-postgres-admin-1 bh-local-shared-openbao-admin-1` (rc 0)
  - `docker rm --force <9 container>` (rc 0)
  - `docker network rm baseharbor-identity-core-local baseharbor-identity-core-local-internal` (rc 0)
  - `docker volume rm bh-local-shared_postgres-data-1` (rc 0)
- ZEUGE (docker ps = 0 bh-* lokal):
  - `docker ps -a --format "{{.Names}} {{.Status}}"` => LEER (0 zeilen).
  - `docker ps -a --filter "name=bh-local"` => 0.
  - `docker network ls --filter "name=baseharbor-identity-core-local"` => 0 netzwerke.
  - `docker volume ls | grep bh-local-shared_postgres-data-1` => 0.
- RESTE: kein bh-local container, keine private netzwerke von mir, kein private volume von mir.
  Dauer-stack des hosts (166) NICHT angefasst; auf dem coordinator-host selbst ist kein matrix-host.

## PLAN (matrix, ab jetzt REMOTE nur noch)

- Punkt 1: R1-rueckbau erledigt (quittiert vor matrix-arbeit).
- Punkt 2: docker-phase REMOTE auf baha-docker (166). Vor `baha up` nachweisen, dass der socket die ferne
  ist (transcript-zeile: `docker context ls` / endpoint vor up).
- Punkt 3: issuer/verifier-pfad wie remote-control round-3 belegt (connector-gebundene ferne core).
- Punkt 4: matrix fortsetzen; podman-2 ist FREI (w273 released) fuer die podman-phase.

## CELL-ERGEBNISSE (docker-2/baha-docker-2 205, Core w269-matrix @ 8bda98c1cd3, SINGLE default)

Zielhost der Mission ist baha-docker-2 (192.168.6.205, vm-lock claim w269, seit 2026-11-07T00:37Z).
166 (baha-docker) nur als isoliertes Testfeld genutzt; release+cleanup (0 meine container/volumes/
netzwerke); shared bh-local-shared (6 container) unveraendert.

- core: PASS — Core READY (postgres/openbao/Core Identity), doctor OK, single default (ha-requested=
  false). Befehl: `baha up --control-plane-only --skip-memory-preflight --target w269-matrix`;
  `baha doctor --target w269-matrix --plain` => READY. Ports auto auf 15436/18203 (5432/8200 belegt
  durch w169 ci-bootstrap); 8 core-container.
- console: PASS — Core status read-only: postgres/openbao READY, availability satisfied.
- demo (r27-w150-demo): BLOCKED-by-scope — das reale demo-repo ist auf 205 NICHT verfuegbar
  (/home/marcel/work/... existiert nicht hier). Rekonstruiertes demo-app gegen isolierten w269-matrix
  (kein managed backend sql/redis/s3 provisioniert) => workload start FAILED (backend hostnames
  unerreichbar). Same broker/readiness-defect wie 166 (host-unabhaengig, card
  t-20261107-r27-runtime-broker-oras-missing-edge-readiness).
- connector (node): BLOCKED-by-scope — `baha node add/connect/list/status/disconnect` = TWO-HOST-flow
  (remote node enrollment). Single-host lane (205) ohne zweiten host nicht end-to-end fahrbar.

## MATRIX (offen — noch nicht gefahren)

- docker-1 (baha-docker/166): SINGLE default core + demo + console + connector, je host pass/fail + revision.
- podman-1 (baha-podman/148): dieselbe matrix.
- Jede zeile: befehl, source-revision (ls-remote/rev-parse pro repo), pass/fail, transkrit.
- repo-rule compliance: kein produkt-code, kein .github, kein runner/infra, keine container auf dem coordinator-host.
