# w121 — Podman-VM `baha-podman`: Bestand + reproduzierbarer Neuaufbau + VERSION-Korrektur

Lane w121 (Worker), Coord f49a3303. Host: `baha-podman` (ssh-alias `baha-podman`, rootless Podman).
Review-Typ: Betriebs-/Smoke-Auftrag, kein Produktcode, keine Produkt-Änderung. Ziel: neuaufbau der compose-/setup-definierten Stapel, VERSION-Korrektur baha von 0.4.23 (9514a768be) auf Quellbau develop (ecbb8854), Funktionsnachweis, lane-eigene Aufräumsphase.

## PLAN-Checkliste
- 1) BESTAND: podman ps -a, podman system df, df -h /, baha --version + Dreipunkte-Prüfung
- 2) NEUAUFBAU compose-/setup-definierten Stapel über Definition (broker erst Logs/Ursache, dann rebuild)
- 3) VERSION KORRIGIEREN: setup-skript auf Quellbau ecbb8854 umstellen, diff + beleg
- 4) FUNKTIONSBEWEIS pro runtime: rc=0 belege (run true, port-mapping, build/image)
- 5) AUFRÄUMPHASE: lane-eigene weg; END mit podman ps -a nachher + df + Anzahl + versionszeile

## 3. VERSION KORRIGIEREN — SOURCE BUILD (ecbb8854) — durchgefuehrt

### Beleg: build aus definierter Revision
- Go 1.25.0 installiert unter `/tmp/opencode/w121/go/bin/go` (VM hatte kein go).
- Voll-Clone (shallow clone landet auf develop-HEAD 60e198fa, NICHT auf ecbb8854 — daher full clone noetig):
  `git clone https://github.com/mcpdev80/baseharbor /tmp/opencode/w121/bh-ecbb`
  `git -C /tmp/opencode/w121/bh-ecbb checkout ecbb88545f96473986f8f41394cffce58b97d2df`
  => HEAD is now at ecbb8854 feat(candidate): canonical source/image submission and explicit consent (#1355)
  `git rev-parse HEAD` => `ecbb88545f96473986f8f41394cffce58b97d2df` (wortlich belegt).
- Build: `go build -trimpath -ldflags "-s -w -X main.version=ecbb8854 -X main.commit=ecbb88545f96473986f8f41394cffce58b97d2df -X main.date=<now>" -o baha ./cmd/baha`
  => rc=0, sha256 `81b8aa25d4c4f7873b691fbd594655baf6070816221753064040a9159b285db8`.
- `baha --version` => `BaseHarbor ecbb8854` / `commit ecbb88545f96473986f8f41394cffce58b97d2df` / rc=0.

### setup-skript: release-from-network -> quellbau (DIFF)
Original `setup-baha-podman.sh` (v0.4.23, Network-Release aus `raw.githubusercontent.com/.../v0.4.23/scripts/install.sh`)
aufbewahrt als `setup-baha-podman.sh.orig`; neu: `setup-baha-podman-source.sh`.
Wesentliche Aenderung:
- `VERSION="${BAHA_VERSION:-v0.4.23}"` -> `SOURCE_REV="${BAHA_SOURCE_REV:-ecbb88545f96473986f8f41394cffce58b97d2df}"`.
- Network-Release-Install (`curl install.sh; baseharbor_${os}_${arch}.tar.gz` + checksum-verify) ersetzt durch:
  `git clone "$SOURCE_URL" && git checkout "$SOURCE_REV" && go build -trimpath -ldflags "... -X main.commit=$HEADREV" ./cmd/baha`.
- Build-Pfade/Cache unter `/tmp/opencode/w121` (GOPATH/GOCACHE), Go-Toolchain aus `BAHA_GO_BIN`.
- Diff des skripts liegt in der evidence (diff -u .orig ...-source.sh, siehe unten).

### INSTALL: neu installiert, CORE-BOOTSTRAP BLOCKIERT
- `install -m 0755 baha ~/.local/bin/baha` => PATH-Eintrag zeigt jetzt `ecbb8854` (korrigiert).
- Core-Bootstrap `up --control-plane-only --yes` fehlschlaeuft mit:
  `Error: Core sql failed: existing native network lacks a protected Core or shared backend owner`
  installation.json: `phase: sql_failed`, `ready: false`. doctor: `Core Identity FAILED` (postgres+openao READY).
- URSACHE: fehlgeschlagene w117-Installation hinterliess podman-test in sql_failed mit orphaned Networks
  (baseharbor-identity-core-podman-test, baseharbor-identity-core-podman-test-internal,
  baseharbor-podman-test-default, baseharbor-podman-test-secrets) und ohne verwertbare Deployment-Eigenuemer.
- CLI `destroy --delete-data --yes` => `Runtime mutation requires verified existing Target and deployment ownership`
  (keine Eigenuemer-Referenz in fehlgeschlagener Installation) => CLI-Weg blockiert.
- BEFUND: bekannter #826-HA-Topology-Punkt (v0.4.23) PLUS korrupter Zielzustand; aus der Lane-Her nicht sauber
  aufloesbar, ohne (a) manuelles Teardown der podman-test-spezifischen Container/Netze/State (OUT OF SCOPE: Gefahr
  fuer geteilte Infrastruktur, `podman system reset` nicht erlaubt) oder (b) Owner-Entscheidung zum Teardown-Mechanismus.

### TEARDOWN-VERSUCH UEBER DIE DEFINITION (Koord-Anwort 2026-11-04, VM-Feld ist Koord-Feld)
- Koord-Entscheidung: KEIN `baha destroy` (der blockierte destroy ist der Produktfehler #1375 consent-abort); Teardown
  ueber die compose-/setup-Definition; compose down haengt -> pods/container einzeln NACH drei-punkte-pruefung.
- BEFUND teardown: Der `podman-test`-Core ist in `sql_failed` OHNE deployte Container.
  - `podman ps -a` (alle): 25 Container, SAMTLICH `bh-*shared*` (7 Up 2 weeks, 14 Up 3 hours, 3 healthy, 1 healthy).
  - `com.baseharbor`-labeled Container: **0**; `com.baseharbor.runtime=podman-test`: **0**. => Core Identity NICHT deployed.
  - `compose down` aus `~/.local/share/baseharbor/targets/podman-test/runtime/compose.yaml`: keine podman-test-Container
    vorhanden -> nichts abzubrechen; die zugehoerigen Netze `baseharbor-podman-test-default/-secrets` und
    `baseharbor-identity-core-podman-test(-internal)` sind GEMEINSAM belegt:
    - `baseharbor-podman-test-default` belegt von: bh-podman-test-shared-{postgres,postgres-admin,postgres-member-1,openbao,openbao-admin,...} (Up 3h), bh-podman-test-core-shared-keycloak-*
    - `baseharbor-identity-core-podman-test` belegt von: bh-podman-test-core-shared-keycloak-access (Up 3h)
    => Netze NICHT entfernbar ohne shared-Stapel abzureissen (`podman network remove` -> OUT OF SCOPE).
  - Volumes: keine `podman-test`-volaten (alle `bh-podman-test-shared*`/`bh-podman-test-core-shared*` = extern).
- DREI-PUNKTE-PRUEFUNG: Punkt1 active run? Core NICHT am laufen (sql_failed), Shared-Stapel laufen (fremd).
  Punkt2 ownership? podman-test-Core ist Lane-Install, aber ohne deployte Objekte -> kein compose-down-Ziel.
  Punkt3 wiederherstellung? Netze geteilt -> Teardown haengt an shared-Referenz. => Compose-Definition-Teardown
  fuehrt NICHT zu einem laufenden podman-test-Stapel (kein Ziel).

### VERKNUEPFUNG auf consent-abort-Karte (t-20261104-r27-consent-abort, PR #1375) — echter Zusatzbeleg
- Der festgefahrene Zustand ist BELEG FUR den #826/ownership-Schutzfehler:
  - installation.json: `"phase":"sql_failed"`, `"ready":false`, installation_id `6e0e95cc-f0fb-4d21-a417-9f3968b61f72`.
  - destroy-Fehler WORTLICH: `Runtime mutation requires verified existing Target and deployment ownership.`
    `Inspect the protected owner and native resource before retrying; no ownership is inferred.`
  - Kein Ownership-Verweis vorhanden (0 `com.baseharbor`-Container) => der ownership-geschuetzte destroy blockiert.
  - status: `postgres READY, openbao READY, Core Identity FAILED` / `runtime is running but not ready`.
- Diese Kette belegt die akzeptanz-relevante Schutzluecke fuer #1375 (ownership-nicht-inferiert -> runtime-mutation blockiert).

### DIFF setup-baha-podman.sh.orig -> setup-baha-podman-source.sh (KERN)
```
-VERSION="${BAHA_VERSION:-v0.4.23}"
+# SOURCE_REV defines the build revision (was: released v0.4.23 network binary)
+SOURCE_REV="${BAHA_SOURCE_REV:-ecbb88545f96473986f8f41394cffce58b97d2df}"
...
-printf 'BaseHarbor release: %s\nTarget: %s\n' "$VERSION" "$TARGET"
-... install verified release ...
-INSTALLER="$(mktemp ...)"
-INSTALLER_BHA="$(curl -fsSL .../${VERSION}/scripts/install.sh ...)"
-... baseharbor_${os}_${arch}.tar.gz + checksum verify ...
+echo "[1/4] Fetching source at revision $SOURCE_REV ..."
+git clone "$SOURCE_URL" "$WORK"
+git -C "$WORK" checkout "$SOURCE_REV"
+HEADREV="$(git -C "$WORK" rev-parse HEAD)"
+[ "$HEADREV" = "$SOURCE_REV" ] || die "checkout $SOURCE_REV did not land on $HEADREV"
+echo "[2/4] Building baha from source ..."
+go -C "$WORK" build -trimpath \
+  -ldflags "-s -w -X main.version=$SOURCE_REV -X main.commit=$HEADREV -X main.date=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
+  -o "$WORK/baha" ./cmd/baha
+[ -x "$WORK/baha" ] || die 'baha build failed: binary missing'
+install -m 0755 "$WORK/baha" "$INSTALL_DIR/baha"
```
Original-Release-Install (curl v0.4.23 install.sh + tar.gz + sha256-verify) vollstaendig durch Quellbau ersetzt;
Skript original als `setup-baha-podman.sh.orig` bewahrt.

## 1. BESTAND (Ist-Befund) — baha-podman (hostname baha-runner-podman, marcel, rootless Podman)

### podman ps -a (Bestand, 2026-11-04)
Shared-Stapel (KEEP, nicht lane-eigen):
- bh-backup-recovery-ci-shared: 6 Cont (postgres-admin, openbao-admin, postgres-member-1, postgres(haproxy), openbao-member-1, openbao(haproxy)) — alle `Up 2 weeks`.
- bh-backup-recovery-ci-core-shared: keycloak-1 (`Up 2 weeks (healthy)`), keycloak-access (caddy) — `Up 2 weeks`.
- bh-podman-test-shared: 6 Cont — `Up 3 hours`.
- bh-podman-test-core-shared: keycloak-db, keycloak-access, keycloak-db-etcd-1/2/3, keycloak-db-member-1/2/3, keycloak-1/2/3 — `Up 2-3 hours`, keycloak-1/2/3 healthy.
- broker: NICHT vorhanden (`podman ps -a | grep broker` leer) — muss wieder hochgebracht werden.

### podman system df
- Images: 12 (9 aktiv, 3.432 GB, 65.06 MB reclaimable / 2%).
- Containers: 25 (25 aktiv, 709.4 MB).
- Local Volumes: 9 referenziert.

### df -h /
- `/dev/sda1 96G 54G 43G 56% /` (Vorher; ~43 GB frei).

### baha VERSION (BEFUND, zu korrigieren)
- `~/.local/bin/baha --version` => `BaseHarbor 0.4.23`, commit `9514a768be96ad4081185a670705e469f79ff854`, built `2026-10-08T07:56:32Z`. rc=0.
- PATH enthält `~/.local/bin` NICHT; `command -v baha` => not found in non-login shell.
- setup-skript: `/home/marcel/setup-baha-podman.sh` (2614 bytes, Oct 8 14:32) — meldet/ installiert v0.4.23.
- Kein sauberer `~/baseharbor`-Checkout vorhanden; es existiert nur `/home/marcel/baseharbor-cleanup-test`.

### Dreipunkte-Prüfung vor destruktiven Schritten
- Punkt 1 (aktive Runs): 25 Cont in 4 Shared-Stapel laufen (Up 2h–2w). Reine TESTUMGEBUNG, OWNER-Freigabe 2026-11-04 16:0x für vollständige Bereinigung + reproduzierbarer Neuaufbau ausdrücklich gewollt — Rebuild beabsichtigt, nicht zu vermeiden.
- Punkt 2 (Shared vs lane-eigen): Alle laufenden Stapel sind `bh-*shared*` / `bh-backup-recovery-ci-core-shared*` / `bh-podman-test-core-shared*` = fremd/Shared. Keine lane-eigenen Objekte identifizierbar. Lane-eigen ist nur das setup-skript + der Install-Pfad `~/.local/bin/baha`.
- Punkt 3 (Wiederherstellungsfolge): Stapel sind aus compose-/setup-Definition reproduzierbar (compose project-labels vorhanden). Der broker ist externer backup-recovery-ci-Deployments-Teil; ZustandTree fehlt (laut w117). Shared-Stapel werden über DENSELBER Definition neu aufgesetzt, Volumes bleiben erhalten.

## BEFUNDE (vorheriger OPS-Durchgang, w117/w116, als Ausgangslage)
- broker-container auf baha-podman NICHT MEHR VORHANDEN (podman ps -a | grep broker => leer); muss wieder hochgebracht werden
- frühere logs: exit 137 (SIGKILL, plausibel OOM: 7.9 GB gesamt, ~2.4 GB verfügbar) + TLS-Handshake OHNE clientzertifikat
- baha --version meldet weiter 0.4.23 (revision 9514a768be); auf baha-docker schon korrekt (ecbb8854-Quellbau)
