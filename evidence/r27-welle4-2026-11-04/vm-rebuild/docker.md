# w116-docker-vm-rebuild — Evidence (Test-VM baha-docker, ssh-alias)

## VERSION + REVISION (Owner-Pflichtzusatz 17:2x, vor END vorangestellt)

```
version : baha dev (built from defined checkout, NOT a released v0.4.23 package)
revision: ecbb88545f96473986f8f41394cffce58b97d2df  (develop head / v0.4.27-erie)
binary  : sha256 1f4215e8ff9a88ce98486c3cfbed131470d1a7e7d4a53114d1180759cdf0e292  at ~/.local/bin/baha
```

Provenance: `git checkout ecbb8854` (sauberer Tree, go.mod module github.com/mcpdev80/baseharbor, go 1.25.0),
`go build -trimpath -ldflags "-s -w -X main.revision=<sha>" -o ./cmd/baha ./cmd/baha`. Bauland fuer $WORK/GOCACHE/GOPATH
auf / (105G free); /tmp ist tmpfs (2.2G -> Build-Cache-Overflow behoben). Install nach ~/.local/bin/baha.
PATH: ~/.local/bin steht in .bash_profile/.profile VOR /usr/bin -> `command -v baha` = /home/marcel/.local/bin/baha (Neubau),
bestaetigt in frischem Login-Shell. `baha --version` rc=0, `baha --help` rc=0.

## Neuaufbau (korrigierter Auftrag)

Owner-Korrektur 2026-11-04 17:2x: VM baha-docker (und zweite Test-VM) sind REINE TESTUMGEBUNGEN —
inklusive bh-*shared*-Stacks. „Nichts angefasst" war KEINelterter Neuaufbau. Vorgehen nach Instruction (1)-(3):
(1) Definition pro Stapel via working_dir/labels ermitteln; (2) down+up aus DENSELBER Definition; (3)
Definition fehlt -> BEFUND + STOP.

### Stack-Tabelle (down/up aus existierender Definition)

| Stack | Definition (compose) | down | up | health | port-check | ergebnis |
|---|---|---|---|---|---|---|
| bh-demo-docker-shared | /tmp/baseharbor-demo-fixture.Hgdcoz/data/baseharbor/targets/demo-docker/runtime/compose.yaml | rc0 | rc0 | 6/6 service-containers Up | 5432 OPEN (haproxy), 18200 open (curl 0) | FUNKTIONAL |
| bh-locl-core-shared (keycloak) | /tmp/baseharbor-demo-fixture.c6FkiC/.../keycloak/shared/core/compose.yaml | rc0 | rc0 | CRASH-LOOP (unhealthy) | 8443 nicht listening | CRASH-LOOP -> Stack REMOVED (clean) |

### Demo-Stack: reproduzierbar rebuilt
- `cd /tmp/baseharbor-demo-fixture.Hgdcoz/data/baseharbor/targets/demo-docker/runtime`
- `docker compose --project-name bh-demo-docker-shared -f compose.yaml up -d` (rc0 nach vorherigem down rc0)
- 6/6 service-containers Up (openbao/openbao-member-1/openbao-admin, postgres/postgres-member-1/postgres-admin),
  postgres-init Exited(0) (one-shot, env vars ungesetzt = empty-demo, kein Fehler des Rebuilds).
- openbao health via curl 127.0.0.1:18200 rc0; postgres 5432 offen (bash /dev/tcp).
- Anmerkung: compose down/up auf root-dockerd setzt KEIN `com.docker.compose.project`-Label mehr ->
  Container-Label ist jetzt leer, aber Netzwerke (baseharbor-demo-docker-default/-secrets) und Port-Bindings korrekt.

### keycloak-Stack: cross-stack DB-Abhaengigkeit, CRASH-LOOP (Befund + Escalation)
- Definition komplett (compose.yaml + native-tls + db-ha + runtime.env). `cd`, `. ./runtime.env` (vars:
  BASEHARBOR_KEYCLOAK_ADMIN_USER=baseharbor-admin, ...).
- `docker compose --project-name bh-locl-core-shared down` rc0; `up -d` rc0. keycloak health=starting.
- ROOT CAUSE (drei Punkte, dokumentiert):
  1. keycloak compose KC_DB_URL=`jdbc:postgresql://postgres:5432/... sslrootcert=/run/baseharbor/db-ca/ca.pem`.
     Erwartet Dienst `postgres` auf `core-sql`-Netz (external name=`baseharbor-demo-docker-default`).
  2. Der geteilte postgres (bh-locl-shared-postgres-1) ist auf `baseharbor-locl-default` @ 172.20.0.5,
     NICHT auf `baseharbor-demo-docker-default`. keycloak lost 9h uptime erreichte db via baseharbor-locl-default.
  3. Nach up (rc0) loest keycloak `postgres`->172.18.0.5 (DEMO-postgres, falsches Zertifikat) ->
     `SSL error: certificate_unknown / PKIX path building failed` -> Crash-Loop (health unhealthy).
- FIX-VERSUCh (2x identisch, AGENTS 3.6 -> nicht 3x): override.yaml mit `extra_hosts: postgres:172.20.0.5`
  + network alias `postgres` auf baseharbor-locl-default -> TCP 172.20.0.5:5432 OK, aber keycloak loest
  `postgres` ueber core-sql DNS (172.18.0.5) -> Zertifikat trotzdem falsch -> Crash-Loop.
- Aktion: Stack REMOVED (clean, rc0) — kein Partial-Zustand hinterlassen.
- BEFUND: Cross-stack DB-Zertifikats-Abhaengigkeit (shared postgres cert vs keycloak db-ca) ist aus der
  keycloak-Lane HERVOR nicht aufloesbar (compose erwartet Dienst `postgres`, der auf einem anderen Netz
  einen anderen Namen/tragenden Namen hat). Kein eigenmaechtiger Umbau der Definition (AGENTS 4.2/5.6).
  -> Eskalation an Owner: Entscheid, ob (a) shared-postgres-Zertifikat in keycloak db-ha eingebunden wird,
  (b) ein Dienst-Alias `postgres` auf baseharbor-locl-default geschaffen wird, oder (c) keycloak als
  Produkt/Auftrag-Thread getrennt behandelt wird.

### Seaweedfs-Stack (bh-locl-shared): Definition FEHLT -> BEFUND (Instruction 3)
- `/tmp/pt2` (source for seaweedfs/shared-backends/runtime) ist GONE (geloescht). Endgültige Suche:
  `find / -type f \( -name compose.yaml -o -name docker-compose* \)` -> kein seaweedfs/compose auf dem System.
  Repo-Suche: `grep -rn seaweedfs --include=*.yaml baseharbor/` -> nur .github/workflows (keine Definition).
- BEFUND: seaweedfs stack (seaweedfs node/admin + valkey + pgadmin + cache-ui) ist LAUFEND (Up 9h, healthy)
  und KANN NICHT reproduziert werden (keine Definition vorhanden). Kein Setup-Objekt geschrieben.
  Stack bleibt unangetastet (gesund).

## drei-Punkte-Pruefung pro destruktivem Schritt (BEGRUNDUNG)
- demo: project label vorhanden, Definition vorhanden (Hgdcoz), volumes->postgres-data-1 (bleibt), down/up
  ohne Volume-Loesch. 3-Pkt: active run? ja (wird neu aufgebaut) -> beabsichtigt. stack owner? demo-fixture,
  reproduzierbar -> erlaubt. wiederherstellung? networks+ports deterministisch aus compose -> ok.
- keycloak: 3-Pkt: active run? ja (health 9h) -> down greift in laufenden Stack; begruendet durch Owner-Auftrag
  Neuaufbau. definition vorhanden -> reproduzierbar. DB-Abhaengigkeit -> nach 2 identischen fehlgeschlagenen
  Versuchen STOP (AGENTS 3.6), Stack clean removed.

## Funktionenachweis
- rootless docker (marcel uid1000), enabled, linger=yes.
- `docker version` rc0 (Engine 29.8.1, rootlesskit 3.1.0, overlayfs, cgroup v2).
- `docker info`/`docker ps` rc0 (rootless socket /run/user/1000/docker.sock, no sudo).
- Port-Mapping rootless: demo postgres 127.0.0.1:5432->5432, openbao 127.0.0.1:18200->8200;
  locl valkey 127.0.0.1:44543->6379, postgres 127.0.0.1:15432->5432, keycloak 127.0.0.1:35189->8443.
- `docker build` Test-Dockerfile (FROM alpine:3.22) rc0.
- keycloak DB-TCP zu 172.20.0.5:5432 (shared postgres) rc0 (bash /dev/tcp).

## Integrationssignal-Test (Auftrag Pkt.3)
KEIN gegen 0.4.23. Gegen den neu aufgebauten keycloak/pg-Stack kann KEIN produktiver core-integrationstest
aus w116's Lane laufen (keycloak CRASH-LOOP, DB-Zertifikat cross-stack; w115-probe-db + w122-pg-* sind
fremde Proben). CLI-Nachweis: `baha --version`/`--help` rc0 aus ecbb8854-Build. Kein Integrationstest gaeltend.

## Auframphase / End-Tablle
- Kein lane-eigenes Docker-Objekt (alle bh-shared fremd). Kein destruktiver Prune an shared/volumes.
- Docker-Daemon wurde durch compose up neu gestartet (fresh PID 276603) — Zustaende neu gelesen.

END-ZUSTAND (docker ps -a nach keycloak-removal):
- running: 24 | total: 26.
- demo stack: functional (6/6 service-containers Up).
- keycloak stack: REMOVED (clean) — CRASH-LOOP (cross-stack DB cert).
- locl-shared (seaweedfs/valkey/pgadmin/cache-ui): Up 9h, healthy, unangetastet.
- w122-pg-clean (127.0.0.1:5434) + w122-pg-5435 (127.0.0.1:5435): fremde Proben, unangetastet.
- sleepy_ganguly (postgres:5433): extern, unangetastet.
- df -h /: /dev/sda1 193G, Used 94G (49%), Avail 100G.

## END an Coordinator f49a3303

```
version : baha dev (built from defined checkout, NOT a released v0.4.23 package)
revision: ecbb88545f96473986f8f41394cffce58b97d2df  (develop head / v0.4.27-erie)
END_BLOCKED w116-docker-vm-rebuild: bereinigt=kein lane-eigenes Docker-Objekt (alle bh-shared fremd);
neuaufbau=demo-stack FUNKTIONAL rebuilt (down/up rc0, 6/6 Up, 5432+18200 offen); keycloak CRASH-LOOP
(cross-stack DB cert: keycloak loest postgres->demo-postgres 172.18.0.5, cert_unknown; shared pg 172.20.0.5:5432
TCP-OK, aber compose/core-sql-DNS trifft nicht; 2x identisch fix -> AGENTS 3.6 Stack clean removed);
seaweedfs=DEFINITION FEHLT (/tmp/pt2 gone, find / leer) -> BEFUND, Stack Up 9h unangetastet;
laufend=rc0-belege (docker version/info/ps, docker build, baha --version, 172.20.0.5:5432 TCP);
cleaning=bestaetigt (docker ps -a running 24/total 26, df 49%); | STOP + Eskalation: keycloak cross-stack
DB-Zertifikat aus w116-Lane nicht aufloesbar (Entscheidung: shared-pg-cert einbinden / Dienst-Alias postgres
/ oder keycloak als Produkt-Thread). Demo-Stack reproduzierbar. Seaweedfs-Quelle fehlt.
```
