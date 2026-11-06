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

## MATRIX (offen — noch nicht gefahren)

- docker-1 (baha-docker/166): SINGLE default core + demo + console + connector, je host pass/fail + revision.
- podman-1 (baha-podman/148): dieselbe matrix.
- Jede zeile: befehl, source-revision (ls-remote/rev-parse pro repo), pass/fail, transkrit.
- repo-rule compliance: kein produkt-code, kein .github, kein runner/infra, keine container auf dem coordinator-host.
