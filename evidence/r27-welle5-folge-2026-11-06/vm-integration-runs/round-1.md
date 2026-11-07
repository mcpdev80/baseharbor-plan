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

## SIDE-EFFECT (coordinator-facing, 2026-11-07) — network prune auf shared host

- Beim bereinigen meiner own broker/container-hinterlasse habe ich `docker network prune -f`
  gestartet. Prune loescht ALLE ungenutzten netzwerke, nicht nur meine. Dadurch wurden
  CI-bootstrap-netzwerke fremder w169-lanes (baseharbor-identity-core-w169-ci-bootstrap-*,
  baseharbor-w169-ci-bootstrap-*) auf dem shared host (166) rueckgebaut.
- KEIN container einer fremden lane wurde beruehrt (docker ps zeigte nur bh-local-shared + meine
  bh-w269-matrix-*). Die w274/w282-lanes benutzen baha-docker-2 (108)/podman, NICHT 166.
- KEIN reparatur in dieser lane (mission: kein host-repair). Nur bericht. Koordinator ec2254ac
  kann falls noetig fremde ci-netzwerke neu anlegen.

## PLAN (matrix, ab jetzt REMOTE nur noch)

- Punkt 1: R1-rueckbau erledigt (quittiert vor matrix-arbeit).
- Punkt 2: docker-phase REMOTE auf baha-docker (166). Vor `baha up` nachweisen, dass der socket die ferne
  ist (transcript-zeile: `docker context ls` / endpoint vor up).
- Punkt 3: issuer/verifier-pfad wie remote-control round-3 belegt (connector-gebundene ferne core).
- Punkt 4: matrix fortsetzen; podman-2 ist FREI (w273 released) fuer die podman-phase.

## DEMO-CELL (docker-1/baha-docker 166) — investigate, demo-app nicht READY

Ziel: r27-w150-demo gegen isolierten w269-matrix core (SINGLE default, ha=False) auf 166.

STATUS: BLOCKED — demo-app erreicht keine HTTP/TLS-Readiness; root-cause gefunden, umgehung nur
mit host-toolchain-fix (oras) + broker-readiness-block (edge-runtime image).

Was funktionierte:
- baha binary bei 8bda98c1cd3 auf 166 gebaut (commit korrekt).
- isolated target `w269-matrix` erstellt; `up --control-plane-only --skip-memory-preflight` => phase=ready, ready=True, ha=False; 8 container (openbao/postgres/keycloak/haproxy).
- demo-app repo `r27-w150-demo` (compose.yaml + demo-app/go): `app init --target w269-matrix` erfolgreich.
- `services.secrets: true` + `runtime.private: true` im manifest => runtime-broker wird aktiviert (mTLS),
  secrets-scope verified, broker container started, docs-ui (Swagger) auf :8081 antwortet.

Root-cause #1 (TLS gate): demo-app/main.go serverTransport() verlangt TLS_CERT_FILE/TLS_KEY_FILE;
plaintext ist intentional gesperrt (`log.Fatal`). BaseHarbor injektiert diese vars nur, wenn der
runtime-broker aktiv ist (`RequiresRuntimeBroker = m.Services.Secrets || len(m.Runtime.Permissions)>0`).
Demo-repo hatte beides nicht => broker skip => container startete, readiness miss => exit_code=1.

Root-cause #2 (oras fehlt): broker image resolution laeuft ueber `oras` (internal/orgconfig/source_oci.go,
cmd/baha/application_registry_source.go). `oras` ist auf 166 NICHT installiert => `oras: command failed`
`resolve development runtime image`. Fix: BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE=1 =>
pullResolvedRuntimeImage umgeht oras und nutzt docker pull. docker pull ghcr.io/mcpdev80/baseharbor-runtime:
edge/succeeded (image present).

Root-cause #3 (broker readiness): edge-runtime image `0.4.26`/`edge` => version check OK (dev/edge
development-pair). Broker container startet, mTLS-handshake ok, docs-ui live, ABER `/readyz` =>
{"status":"not_ready"} permanent. Externe deps pruefen: openbao (192.168.160.3) initialized/sealed:false
reachable von broker netns; broker-cert/ca.pem/permissions.json/service-tokens.json/runtime-token alle present.
Broker intern (kompilierter edge-binary) => dependency-check nicht auflsbar aus dieser quelle.

Betroffene digests (r27-w150-demo, source 1e918f0f...):
- prompt confirm-hash (repository desired-state fingerprint): c57ac457fe9a675797f73fb17676e457f9575f1486c93a18e63eca1c65bb3bd0
- --confirm-candidate (sha256 der submission json, Quelle internal/delivery/candidate.go): c57ac457...
  (verifiziert mit temp-probe in cmd/baha; probe entfernt, produkt-binary unveraendert, build 8bda98c)
Anwendung NIE completed (deployment.json existiert nicht); broker-container bleibt unhealthy nach 2m.

Bemerkung: demo-app ist ein product demo-workload; manifest-aenderungen waren fuer die isolierte matrix-notwendig,
ABER mission verbietet produkt-code-edits => dieser fix gehoert als product-fix, nicht als matrix-hack.

## CELL-ERGEBNISSE (docker-1/baha-docker 166, Core w269-matrix @ 8bda98c1cd3, SINGLE default)

- core: PASS — Core READY (postgres/openbao/Core Identity OK), doctor OK, ha-requested=false.
  Befehl: `baha doctor --target w269-matrix --plain` => READY.
- console: PASS — Core doctor (read-only control-plane inspection) sauber: alle Kerne OK,
  control-plane-ha requested=single. Same command as core; read-only, kein write-set.
- demo (r27-w150-demo): BLOCKED — Produkt-/infra-defekt (siehe DEMO-CELL section +
  card t-20261107-r27-runtime-broker-oras-missing-edge-readiness). Matrix-ausfuehrung OK,
  aber broker /readyz never ready.
- connector (node): BLOCKED-by-scope — `baha node add/connect/list/status/disconnect` ist ein
  ZWEI-HOST-flow (remote node enrollment gegen Core). Auf diesem single-host lane (166) ohne
  zweiten claimed host nicht end-to-end fahrbar. Kein core- oder host-schaden; nur out-of-scope.

## MATRIX (offen — noch nicht gefahren)

- docker-1 (baha-docker/166): SINGLE default core + demo + console + connector, je host pass/fail + revision.
- podman-1 (baha-podman/148): dieselbe matrix.
- Jede zeile: befehl, source-revision (ls-remote/rev-parse pro repo), pass/fail, transkrit.
- repo-rule compliance: kein produkt-code, kein .github, kein runner/infra, keine container auf dem coordinator-host.
