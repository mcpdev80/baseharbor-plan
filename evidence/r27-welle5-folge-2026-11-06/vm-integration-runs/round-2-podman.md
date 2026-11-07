# w288-pr1407-vm-matrix-podman — Evidence (round 2, podman-side of the matrix)

**Lane:** w288-pr1407-vm-matrix-podman  **Coord:** a4573079  **Karte:** t-20261104-r27-vm-integration-runs
**Mission:** w288-pr1407-vm-matrix-podman.txt (Ziel: BaseHarbor auf Podman-Rechner igual wie auf Docker-Rechner hochfahren)
**Produkt-code:** NICHT AENDERN — Validierungs-/Smoke-Mission auf Pruef-VMs (RUNBOOK 4.0)

## PLAN

- VERSION STOR: baha --version auf jedem genutzten Host nachweisen; bei Abweichung vom Kandidaten-AST aus Quelle neu bauen + ~/.local/bin installieren (Backup alte Binary)
- vm-lock claim <host> w288-pr1407-vm-matrix-podman; containerzahl + last vor und nach jedem Schritt pruefen + rueckbau
- core zelle auf podman: build aus Kandidaten-AST, `baha up --control-plane-only`, `baha doctor`, ausstieg + journal-zeile
- console zelle auf podman: befehl + pass/fail + version + transcript
- demo zelle auf podman: build + run; r27-w150-demo-repo + provisioniertes managed backend (sql/redis/s3) pruefen
- connector zelle auf podman: SINGLE-HOST-moeglichkeit pruefen; TWO-HOST-rest als echten blocker mit gruende melden
- null-pruefung am ende: podman ps -a frei von lane-eigenen namen + df-zeile
- vm-lock release <host> + rueckbau dokumentieren

## STATUS

BLOCKED — host-seitiger Podman-Netzwerkdefekt auf baha-podman-2. Core kann auf keinem Podman-Host konvergieren. Details unten. Keine Stop-Kriterium (1)/(2)/(3) erreicht: Build war moeglich, nur ein Host noetig gewesen, kein root/rechte-Blocker.

## OWNER-KLARIERUNG (a4573079, 05:0xZ + 05:2xZ — als REGEL gebucht)

- Zwei-Rechner-Regel ist KEINE Freigabe/Ausnahme, sondern REGEL (RUNBOOK R2, Owner-Satz 05:2xZ):
  wenn ein Nachweis mehrere Maschinen braucht, werden mehrere gestellt. Nachweis = podman<->docker-2
  connector-flow => BEIDE hosts halten (claim beider, release beerst nach Rueckbau-null-pruefung).
- Demo-Ablagefach + managed backend (sql/redis/s3) auf baha-docker-2 einzurichten UND demo-zelle fahrbar
  zu machen ist Teil dieses Auftrags (keine separate provisioning-lane mehr).
- Hosts seit 01:05Z unbelegt; claims laufen auf den LANENAMEN der Lane (w288-pr1407-vm-matrix-podman).

## VERSION STOR — ERFOLGT (BUILD)

- Kandidaten-AST (PR #1407): `work/r27-remote-up-cli` = c87c8b644cc98fe6abf1164d101f42a212558b9d
  (ls-remote, Quelle baseharbor/origin). develop = 3fa6f7b0d0ba01943501627e4c5d811cc7bee848.
  (Mission nannte develop dddf0d7823f; real 3fa6f7b — remote-nur via git ls-remote, Quarantane-Checkout
  workers/baseharbor NICHT zitiert.)
- Host baha-podman-2 (192.168.6.107, 0 container, FREE): installiertes `baha` = commit ed98ed1d7
  (baha --version). ABWEICHUNG: ed98ed1d7 != c87c8b644cc. VERSIONSTOR => Build aus Kandidaten-AST.
- Go-Toolchain auf Hosts NICHT vorhanden => golang-go 1.26.8 aus apt installiert.
- Build: `go build -ldflags "-X main.version=c87c8b644cc -X main.commit=<sha> -X main.date=2026-11-07"
  -o ~/.local/bin/baha ./cmd/baha` aus ~/baseharbor-build @ c87c8b644cc.
  `baha --version` => "BaseHarbor c87c8b644cc98fe6abf1164d101f42a212558b9d / built 2026-11-07".
- Backups: ~/.local/bin/baha.bak.ed98ed1d7, ~/.local/bin/baha.c87c.prebuild.

## CORE-ZELLE: BEFUND — Podman-Netzwerkdefekt auf baha-podman-2 (HOST-INFRASTRUKTUR)

Was gefahren wurde (beobachtet, kein Produkt-Change):
- `baha target list` => w268 = podman-runtime (clean, keine Installation). w268 als Ziel gewaehlt.
- `baha up --control-plane-only` => Core kommt hoch: postgres/openbao/admin/member-1/pg-init +
  keycloak-quadlet-units. installation.json: erst phase=sql_failed, kurz auf phase=sql, dann
  rueckfaellig auf sql_failed, ready=False, alle capabilities=False.
- `baha doctor --plain` => os/podman/quadlet/selected-runtime OK; postgres=openbao FAILED "TLS material
  is unavailable"; control-plane-ha FAILED "open .../providers/keycloak/shared/core/runtime.env: no such
  file or directory".
- baha doctor --fix --yes => "context deadline exceeded" (kann auf diesem Host nicht konvergieren).
- postgres-init log (wiederholt): `psql: error: connection to server at "postgres" (10.89.0.13), port
  5432 failed: timeout expired / server closed the connection unexpectedly`.

Ursachen-Analyse (auf baha-podman-2, 192.168.6.107):
1. `up` startete mit HA-Standard => postgres hinter haproxy-proxy; member-1:5432.
2. `bh-w268-shared-postgres-init` kann postgres-proxy:5432 nicht erreichen ("server closed the
   connection unexpectedly"). member-1 intern: pg_isready OK, aber vom proxy/kontainer aus UNREACHABLE.
3. Port-8200-Konflikt waehrend Retry-Sturm ("rootlessport listen tcp 127.0.0.1:8200: bind: address
   already in use") — behoben, als Ports frei waren, blieb aber sql_failed.
4. **Entscheidender Beweis** (podman net routing test, frische alpine-container auf
   baseharbor-w268-default): DNS loest rx auf (10.89.0.9), aber `nc -z rx 5432` => NOT-REACHABLE.
   Zwei BRANDNEUE container auf dem gleichen netz koennen sich untereinander NICHT erreichen.
5. Memory sauber: 6.5 GiB avail, kein OOM (dmesg leer). => kein Ressource-Problem, sondern Routing.

Schlussfolgerung: Der `baseharbor-w268-default` container-network auf baha-podman-2 ist defekt
(kein container-zu-container-routing). Der Core kann seine Backends nicht erreichen => Core
konvergiert nicht => matrix kann auf diesem host NICHT gruen gefahren werden. Das ist ein
HOST-INFRASTRUKTUR-DEFECT, kein Produkt-defekt und keine lane-repareatur (RUNBOOK 4.0).

Was versucht wurde (alle sauber rueckgebaut, 0 meine container/volumes/netze rueckstand):
- HA-install (default), non-HA-install (--ha weggelassen, target-dir vorher puriert) => beide sql_failed.
- doctor --fix --yes => context deadline.
- Volliges purge meiner w268/baseharbor units, container, volumes, netze => CLEAN (mine=0).

## STOP-KRITERIUM-PRUEFUNG

- (1) host-version passt nicht + neu bauen unmoeglich? => BAU WAR MOEGLICH (go 1.26.8 + net). Nicht ausgelost.
- (2) beide podman-hosts gleichzeitig belegt? => baha-podman-2 war frei. (baha-podman/148: 16 shared
  w169-container, nur leslich; lock-regel haelt mich an w268-host.) Nicht ausgelost.
- (3) blocker/root/rechte? => NETZWERKDEFECT IST host-infrastructure, kein lane-repareatur. Als BLOCKED
  gemeldet, nicht als (3)-stop, weil infra-repair dem owner/host-ops gehoert.

## NEXTER TRIGGER

- Owner soll host-ops anstoessen (podman network routing auf baha-podman-2 pruefen) ODER andere freie
  podman-maschine stellen. Sobald routing funktioniert: core-zelle erneut fahren (erwartet: sql+identity
  green), dann console/demo/connector.

## repo-rule compliance

- Kein produkt-code veraendert. Kein .github veraendert. Kein runner/infra angefasst.
- Kein container auf dem coordinator/host der session (build+install nur auf 192.168.6.107).
- w169 ci-bootstrap stack auf baha-podman (148) UNVERAENDERT.
- Alle lane-eigenen container/volumes/netze auf baha-podman-2 rueckgebaut (0 rueststand).
- vm-lock baha-podman-2 besteht; RELEASE + null-pruefung noch aus (siehe unten offensch).
