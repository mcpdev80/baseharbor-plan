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
- connector zelle auf podman: SINGLE-HOST-moeglichkeit pruefen; TWO-HOST-rest als echter blocker mit gruende melden
- null-pruefung am ende: podman ps -a frei von lane-eigenen namen + df-zeile
- vm-lock release <host> + rueckbau dokumentieren

## STATUS

BLOCKED-on-version-build (kein Stop-Kriterium erreicht). Details unten.

## VERSION STOR (BEFUND / MASSNAHME)

- Kandidaten-AST (PR #1407): `work/r27-remote-up-cli` = **c87c8b644cc98fe6abf1164d101f42a212558b9d** (ls-remote, Quelle baseharbor/origin). develop = 3fa6f7b0d0ba01943501627e4c5d811cc7bee848.
  - (Mission nannte develop dddf0d7823f; real ist es 3fa6f7b — remote-nur via git ls-remote verifiziert, Quarantäne-Checkout workers/baseharbor NICHT zitiert.)
- Host baha-podman-2 (192.168.6.107, 0 container, FREE): installiertes `baha` = **commit ed98ed1d7** (`baha --version` => "BaseHarbor dev / commit ed98ed1d7 / built 2026-11-06).
  - ABWEICHUNG: ed98ed1d7 != c87c8b644cc. Ein Test gegen ed98ed1d7 zaehlt NICHT (VERSIONSTOR).
- Host baha-podman (192.168.6.148): 16 langlebige w169 ci-bootstrap container (shared, NICHT anfassen); nur Leszugriff moeglich.
- Go-Toolchain auf beiden Hosts NICHT vorhanden (kein `go`); cc/gcc/make + apt-get vorhanden; apt hat golang-go 1.26.8.
- Alte Binary gesichert: `~/.local/bin/baha.bak.ed98ed1d7` (Kopie, 51976552 bytes).
- Entscheidung: Build aus Kandidaten-AST c87c8b644cc auf baha-podman-2, Install nach ~/.local/bin. GO-Modul-Downloads aus dem Build heraus noetig (Netzwerk zu go.dev + github.com auf dem Host vorhanden, belegt).

## OWNER-KLARIERUNG (a4573079, 05:0xZ + 05:2xZ — GILFT, als REGEL gebucht)

- Zwei-Rechner-Regel ist KEINE Freigabe/Ausnahme, sondern REGEL (RUNBOOK R2, Owner-Satz 05:2xZ):
  wenn ein Nachweis mehrere Maschinen braucht, werden mehrere gestellt. Nachweis = podman<->docker-2
  connector-flow => BEIDE hosts halten (claim beider, release beider erst nach Rueckbau-null-pruefung).
- Demo-Ablagefach + managed backend (sql/redis/s3) auf baha-docker-2 einzurichten UND die demo-zelle
  fahrbar zu machen ist NICHT eine separate provisioning-lane mehr, sondern Teil dieses Auftrags.
- Hosts seit 01:05Z unbelegt; claims laufen auf den LANENAMEN der Lane (w288-pr1407-vm-matrix-podman).

## VERSION STOR — ERFOLGT (BUILD)

- baha auf baha-podman-2 neu baut aus Kandidaten-AST c87c8b644cc (go build -ldflags -X main.*).
  `baha --version` => "BaseHarbor c87c8b644cc98fe6abf1164d101f42a212558b9d / commit c87c8b644cc... / built 2026-11-07".
- Go 1.26.8 aus apt installiert (keine Toolchain vorhanden). Alte Binary gesichert als
  ~/.local/bin/baha.bak.ed98ed1d7; alte c87c-prebuild als ~/.local/bin/baha.c87c.prebuild.
- Build-Quelle: ~/baseharbor-build @ c87c8b644cc (Klon aus origin, nicht quarantiniert).

## STOP-KRITERIUM-PRUEFUNG

- (1) host-version passt nicht zum Kandidaten UND neu bauen moeglich? Build moeglich (apt go 1.26 + Netzwerk ok) => STOP nicht ausgelost, sondern BUILD ergriffen.
- (2) beide podman-hosts gleichzeitig belegt? NEIN — baha-podman-2 frei.
- (3) blocker/root/rechte? NEIN.

## repo-rule compliance

- Kein produkt-code veraendert. Kein .github veraendert. Kein runner/infra angefasst.
- Kein container auf dem coordinator/host der session (build+test nur auf 192.168.6.107).
- w169 ci-bootstrap stack auf baha-podman (148) UNVERAENDERT.
