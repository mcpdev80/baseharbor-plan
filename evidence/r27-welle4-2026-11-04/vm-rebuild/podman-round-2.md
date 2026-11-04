# w121 — Podman-VM `baha-podman`: Bestand + reproduzierbarer Neuaufbau + VERSION-Korrektur

Lane w121 (Worker), Coord f49a3303. Host: `baha-podman` (ssh-alias `baha-podman`, rootless Podman).
Review-Typ: Betriebs-/Smoke-Auftrag, kein Produktcode, keine Produkt-Änderung. Ziel: neuaufbau der compose-/setup-definierten Stapel, VERSION-Korrektur baha von 0.4.23 (9514a768be) auf Quellbau develop (ecbb8854), Funktionsnachweis, lane-eigene Aufräumsphase.

## PLAN-Checkliste
- 1) BESTAND: podman ps -a, podman system df, df -h /, baha --version + Dreipunkte-Prüfung
- 2) NEUAUFBAU compose-/setup-definierten Stapel über Definition (broker erst Logs/Ursache, dann rebuild)
- 3) VERSION KORRIGIEREN: setup-skript auf Quellbau ecbb8854 umstellen, diff + beleg
- 4) FUNKTIONSBEWEIS pro runtime: rc=0 belege (run true, port-mapping, build/image)
- 5) AUFRÄUMPHASE: lane-eigene weg; END mit podman ps -a nachher + df + Anzahl + versionszeile

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
