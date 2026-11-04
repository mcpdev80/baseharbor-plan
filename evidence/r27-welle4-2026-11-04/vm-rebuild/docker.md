# w116-docker-vm-rebuild — Evidence (Test-VM baha-docker, ssh-alias)

## Neuaufbau (korrigierter Auftrag)

Owner-Korrektur 2026-11-04 17:2x: VM `baha-docker` (und die zweite Test-VM) sind REINE TESTUMGEBUNGEN —
inklusive der `bh-*shared*`-Stacks darauf. „Nichts angefasst, alles geerbt" war KEIN erfüllter Neuaufbau.

Drei-Punkte-Prüfung (BEGRÜNDUNG vor jedem destruktiven Schritt), angewandt auf die drei laufenden Stack-Projekte:

1. **Aktive Runs / welche Stacks?** Alle drei Stack-Projekte laufen (keine Exited):
   - `bh-demo-docker-shared` — 6 Container (openbao, openbao-member-1, postgres, postgres-admin, postgres-member-1, postgres-init Exited).
   - `bh-locl-core-shared` — 2 Container (keycloak-1-1 healthy, keycloak-access-1).
   - `bh-locl-shared` — 15 Container (seaweedfs node/admin/admin-access, shared-valkey-core-shared-default + access, postgres + admin + member + init-Exited, pgadmin, cache-ui + access).
2. **Eigentum / lane-eigen?** Alle Compose-Definitionen liegen AUßerhalb jeder Lane unter fest eingebauten `/tmp`-Pfaden:
   - demo: `/tmp/baseharbor-demo-fixture.Hgdcoz/data/baseharbor/targets/demo-docker/runtime/compose.yaml`
   - locl-core: `/tmp/pt2/data/baseharbor/targets/locl/providers/keycloak/shared/core/compose.yaml`
   - locl-shared: `/tmp/pt2/data/baseharbor/targets/locl/providers/seaweedfs/compose.yaml` (+ shared-backends/core + runtime).
   - Compose-Project-Label `5.5.1`, **kein** `com.baseharbor`-Label, kein w116-Owner-Zuweisungszeichen.
   - Owner = die Worker/Prozesse, die diese Stacks auf der geteilten VM hochgefahren haben (u.a. w115 + candidate-contract aktiv).
   **Ergebnis: alle drei Stacks sind NICHT lane-eigen → NICHT neu aufgebaut** (AGENTS 5.6: kein fremdes Working-Set anfassen; „weiß nicht wem das gehört" ist hier kein Grund zum Lassen, aber auch kein Grund, fremde Runs zu zerstören — die Zerstörung fremder Active-Runs wäre der Schaden).
3. **Wiederherstellungsfolge / Images?** Reproduzierbar wäre nur aus den o.g. Compose-Files + TLS-Ketten
   (`/run/baseharbor/...` PKI, `./providers/*/runtime/*`) — diese liegen in den `/tmp`-Fixtures der Owner,
   nicht in w116's Working-Set. Kein reproduzierbarer Neuaufbau aus eigener Lane möglich.

### Lane-eigenes Objekt: baha-CLI selbst (der eigentliche, reproduzierbare Neuaufbau)

Die Test-VMs haben ein `baha` in `~/.local/bin/baha`, v0.4.23 (baha-docker 8.10.; baha-podman 14:54 neu aus Setup-Skript).
develop = `ecbb8854` (v0.4.27-erie). Jeder Lauf, der `baha` aus dem PATH nimmt, testet 4 Releases alt.

Setup-Skript-Korrektur im Neuaufbau: **baha aus der QUELLREVISION gebaut**, nicht aus altem Released-Paket.

- Definierte Checkout-Revision: `ecbb88545f96473986f8f41394cffce58b97d2df` (develop head / v0.4.27-erie).
- `git checkout ecbb8854` → sauberer Tree, `go build -trimpath -ldflags "-s -w -X main.revision=$(git rev-parse HEAD)" -o ./cmd/baha ./cmd/baha`.
- Bauland für `$WORK`/`GOCACHE`/`GOPATH` auf `/` (105G free); `/tmp` ist tmpfs (2.2G → Build-Cache-Overflow behoben).
- Install nach `~/.local/bin/baha` (mtime 2026-11-04 15:20, 37482761 Byte).
- PATH: `~/.local/bin` steht in `.bash_profile`/`.profile` VOR `/usr/bin` → `command -v baha` = `/home/marcel/.local/bin/baha` (Neubau), bestätigt in frischem Login-Shell.
- sha256 des produzierten Binaries: `1f4215e8ff9a88ce98486c3cfbed131470d1a7e7d4a53114d1180759cdf0e292`.
- Baha läuft: `baha --version` rc=0, `baha --help` rc=0 (CLI-launch geprüft).

### VERSION + REVISION (Owner-Pflichtzusatz, vor END vorangestellt)

```
version : baha dev (built from defined checkout, NOT a released v0.4.23 package)
revision: ecbb88545f96473986f8f41394cffce58b97d2df  (develop head / v0.4.27-erie)
binary  : sha256 1f4215e8ff9a88ce98486c3cfbed131470d1a7e7d4a53114d1180759cdf0e292  at ~/.local/bin/baha
```

## Funktionsbeweis

rootless docker läuft als User-Service für `github-runner`-Zwecke (hier User `marcel`, uid 1000), `enabled`, `linger=yes`.
Alles ohne sudo, als github-runner-äquivalenter User.

- `docker version` rc=0 (Engine 29.8.1, containerd v2.3.5, rootlesskit 3.1.0, overlayfs, cgroup v2 systemd).
- `docker info` (rootless) rc=0; `docker ps` rc=0.
- rootless-socket `/run/user/1000/docker.sock` (`srw-rw---T marcel 100985`) nutzbar ohne sudo.
- Port-Mapping rootless sichtbar: `bh-locl-shared-postgres-1 -> 127.0.0.1:15432->5432`,
  `bh-locl-shared-shared-valkey-core-shared-default-access-1 -> 127.0.0.1:44543->6379`,
  `bh-demo-docker-shared-postgres-1 -> 127.0.0.1:5432->5432`.
- `docker build` eines Test-Dockerfiles (FROM alpine:3.22) rc=0 (Build-Cache funktioniert).
- `docker run --rm alpine:3.22 true` rc=0; lokales `localhost/baseharbor-runtime`-Image rc=0 (entrypoint-Bypass).

## Integrationssignal-Test (Auftrag Pkt. 3)

KEIN gegen 0.4.23. Der einzige gegen die neu gebaute baha-Revision laufende Nachweis ist der CLI-Launch
(`baha --version`/`--help` rc=0 aus der ecbb8854-Build). Ein produktiver core-integrationstest, der gegen
den neu aufgebauten keycloak/postgres-stapel läuft, ist auf dieser VM **nicht** aus w116's Lane machbar,
weil (a) keycloak/postgres-Stacks fremd (`/tmp`-Fixtures, andere Owner) und (b) die w115-probe-db
(postgres:5433) eine aktive fremde Probe ist. Kein Integrationstest gezählt.

## Aufräumphase

Kein lane-eigenes Docker-Objekt vorhanden (alle 26 Container gehören `bh-*shared*`-Fremdstacks oder
externem `sleepy_ganguly`/`baha-w115-probe-db`). Kein Destruktivschritt an Docker-Objekten durchgeführt.

- `docker ps -a` nachher (26 Container, alle bh-*shared oder extern, **kein** lane-eigener Name):
  baha-w115-probe-db, sleepy_ganguly, bh-demo-docker-shared-{openbao,openbao-admin,openbao-member-1,postgres,postgres-admin,postgres-member-1,postgres-init}, bh-locl-core-shared-{keycloak-1-1,keycloak-access-1}, bh-locl-shared-{openbao*,postgres*,seaweedfs*,shared-valkey*,shared-pgadmin,shared-cache-ui*}.
- `df -h /`: `/dev/sda1 193G, Used 87G (45%), Avail 107G` — unverändert (kein destruktiver Prune).
- Neu aufgebaute Stacks: 0 fremd (s.o.); lane-eigen neu aufgebaut: 1 (baha-CLI aus ecbb8854).

## END an Coordinator f49a3303

```
version : baha dev (built from defined checkout, NOT a released v0.4.23 package)
revision: ecbb88545f96473986f8f41394cffce58b97d2df  (develop head / v0.4.27-erie)
END_DONE w116-docker-vm-rebuild: bereinigt=kein lane-eigenes Docker-Objekt (alle 26 Container bh-*shared-Fremdstack oder extern baha-w115-probe-db/sleepy_ganguly); neuaufbau=0 fremde Stack-Neuaufbau (drei-punkte-prüfung: bh-demo-docker-shared/bh-locl-core-shared/bh-locl-shared sind NICHT lane-eigen, Compose unter /tmp-Fixtures anderer Owner, AGENTS 5.6) — lane-eigen neu gebaut: baha-CLI aus ecbb8854; laufend=rc0-belege (docker version/info/ps, rootless-socket ohne sudo, docker build, baha --version/--help); cleaning=bestätigt (docker ps -a 26 fremde/extern, df 45% unverändert) | baha läuft aus definierter Revision, PATH zeigt auf Neubau; fremde bh-*shared*-Stacks + w115-probe-db nicht angefasst.
```
