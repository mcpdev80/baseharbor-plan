# w117 — Podman-VM `baha-podman`: Bereinigung + reproduzierbarer Neuaufbau

Lane w117 (Worker), Coord f49a3303. Host: `baha-podman` (192.168.6.148, ssh-alias `baha-podman`, rootless Podman, User `marcel`, uid 1000).
Review-Typ: reiner Betriebs-/Smoke-Auftrag, kein Produktcode, keine Produkt-Änderung.

## PLAN-Checkliste
- 1) Ist-Befund (df, system df, ps, linger, podman info, broker namentlich)
- 2) Drei-Punkte-Prüfung vor destruktiven Schritten, wortlich in Evidence
- 3) UNHEALTHY Broker diagnostizieren + Entscheidung (Neuaufbau vs Blocker)
- 4) Reproduzierbarer Neuaufbau über setup-baha-podman.sh (rc=0)
- 5) Funktionsnachweis (rc=0 + Port-Mapping)
- 6) Aufräumphase (lane-eigen weg, Shared stehen, df/podman ps bestätigt)

## 1. Ist-Befund
- `df -h /` (Vorher): `/dev/sda1 96G 52G 45G 54% /`
- `podman system df` (Vorher): Images 10 (6 aktiv, 2.962 GB, 1.886 GB = 64% reclaimable); Containers 9 (9 aktiv, 177.1 MB); Local Volumes 1 (96.48 MB).
- `podman ps -a` (9 lane-sichtbare + Broker via systemd): alle `bh-backup-recovery-ci-*shared*`/`*-core-shared*` `Up 2 weeks`; ein Container `unhealthy`.
- linger: initial `Linger: no` → mit `loginctl enable-linger marcel` auf `yes` gesetzt (rc=0). User `github-runner` hat bereits linger.
- `podman info`: `rootless=true`, storage-driver `overlay`, rootlessNetworkCmd `pasta`.
- UNHEALTHY-Container namentlich: `bh-backup-recovery-ci-backup-cli-dev-broker` (Status `Up 2 weeks (unhealthy)`), Image `ghcr.io/mcpdev80/baseharbor-runtime:edge`.

## 2. Drei-Punkte-Prüfung (vor jedem destruktiven Schritt)
Punkt 1 — aktive Runs: alle 9 lane-sichtbaren Container sind `running`; die einzigen `running`-Container nach Projekt-Label aufgeteilt.
Punkt 2 — Shared vs lane-eigen (via Label `com.docker.compose.project`):
- KEEP (Shared): `bh-backup-recovery-ci-shared` (6 Cont.), `bh-backup-recovery-ci-core-shared` (2 Cont.), später auch `bh-podman-test-shared` (6) und `bh-podman-test-core-shared` (11).
- LANE-SPECIFIC (entfernen erlaubt): nur `bh-backup-recovery-ci-backup-cli-dev` (Broker, 1 Cont.).
- Volumes: alle `bh-*shared*`/`bh-podman-test-*shared*` — keine lane-eigene Volume. `bh-backup-recovery-ci-shared_postgres-data-1` bleibt stehen.
Punkt 3 — Wiederherstellungsfolge: Der Broker ist ein deployter Runtime-Service EXTERNER `backup-recovery-ci`-Deployment (siehe §3), nicht lokal wiederherstellbar. Shared-Stapel unangetastet, keine wiederherstellungsrelevanten lane-eigenen Volumes vorhanden.

## 3. UNHEALTHY Broker-Stapel — Diagnose + Entscheidung
- Label/Stack: `com.docker.compose.project=bh-backup-recovery-ci-backup-cli-dev`, Service `broker`, Exec `serve`, User 65532, `ReadOnly=true`, DropCapability=all.
- HealthCheck: `curl --fail-with-body ... --resolve baseharbor-runtime:8443:127.0.0.1 --cacert .../ca.pem --cert .../probe-client-cert --key .../probe-client-key https://baseharbor-runtime:8443/readyz`, Interval/Timeout 5s, Retries 12, StartPeriod 2s.
- Manuelle Wiederholung des Healthchecks: HTTP 503 `{"status":"not_ready"}` (rc=22). Port 8081 (`runtime-docs`) antwortet 200. rootlessport-rooted, ContainerAlive (PID 1 `baha serve`).
- Abhängigkeit offen: `openbao` (10.89.1.3) und `baseharbor-runtime` (10.89.5.2) per DNS erreichbar; `NRestarts=0`, nie `healthy` laut Journal-Suchlauf.
- URSACHE: Der Broker-Mountpoint des Deployment-Zustands `/tmp/TestAppBackupRestoreCLIRealDisasterRecovery2077142923/001/platform-state/targets/backup-recovery-ci/deployments/fc61a279-8f20-4780-a5c3-735f6ec59498/state/backup-cli/runtime/bindings/...` EXISTIERT NICHT mehr (bereinigt). Der Container mountet diese Pfade weiterhin read-only; der `/readyz`-Probe fehlt die zugrunde liegende Deployment-Bindung → `not_ready`.
- Kein lokaler Rebuild: `find / -ipath '*backup-recovery-ci*'` (maxdepth 6) findet kein Deployment; `baha target list` zeigt nur `local` (docker); `baha deployment list` existiert nicht. Das owning Deployment ist auf dieser VM nicht präsent.
- ENTSCHEIDUNG: **BLOCKER**. Broker = externer `backup-recovery-ci`-Deployment, Setup-Skript baut nur Core (`--control-plane-only`, Target `podman-test`), nicht diesen backup-cli Runtime. Reif für Rebuild? NEIN. Grund: Deployment-ZustandTree fehlt, owning Deployment nicht auf der VM. Nächster Auslöser: Deployment `backup-recovery-ci` auf der VM erneut deployen (Owner-Bereich), dann Broker neu starten; danach Healthcheck wiederholen. Zustand bleibt `unhealthy` (bekannter Dauerpunkt, seit ~2 Wochen, laut Mission).

## 4. Reproduzierbarer Neuaufbau — setup-baha-podman.sh
- Skript gelesen: `/home/marcel/setup-baha-podman.sh`, 55 Zeilen, SHA256 `ce1a1b9c92b804e83feb28cd62aca06c02e6bae787bfad6c89f836ee7f8b2893`. Installiert `baha` v0.4.23, Target `podman-test` (runtime podman), bootstrapped Core `--control-plane-only --yes`.
- Integrität: unverändert (kein lokales Anpassen des Skripts notwendig; kein Diff nötig).
- Endpunkt-Check: `curl -I https://raw.githubusercontent.com/mcpdev80/baseharbor/v0.4.23/scripts/install.sh` → HTTP/2 200.
- Prerequisites vor Run: podman (rootless, ok), curl, tar, sha256sum, awk vorhanden; `baha` war ABSEITEND nicht auf PATH (wird im Skript installiert).
- Run: `( echo "y" | bash /home/marcel/setup-baha-podman.sh )` → **rc=0** (PIPESTATUS[0]=0).
- Ergebnis:
  - `Installed BaseHarbor to /home/marcel/.local/bin/baha` — `baha 0.4.23 (commit 9514a768...)`.
  - Target `podman-test` created (runtime podman, access podman-test-local, State `/home/marcel/.local/share/baseharbor/targets/podman-test`).
  - Control-plane runtime started: PostgreSQL `127.0.0.1:15433`, OpenBao `127.0.0.1:18200` (Host-Port-Kollisionen 5432/8200 → automatisch 15433/18200 gewählt).
  - OpenBao: `[OK] initialized and unsealed`, KV v2 mount, restricted manager AppRole, root token revoked.
  - `BaseHarbor Core READY: SQL + Secrets + Identity.` — `postgres READY`, `openbao READY`, `Core Identity READY`.
  - Applications: 0 registered deployment(s) (Core, keine Anwendung — entsprechend `--control-plane-only`).
- Memory-Hinweis (Skript): `Safety headroom TIGHT`, `available memory 5.32 GiB < planned estimate 5.88 GiB + safety margin` — Warnung ignoriert mit `--yes` (Bestandteil des Skript-Flows, kein Blocker).

## 5. Funktionsnachweis
- `podman run --rm alpine true` → **rc=0** (rootless, kein sudo).
- Port-Mapping-Test (netavark `cannot assign requested address` gegenbeweis):
  - `podman run -d --name w117-pmp -p 127.0.0.1:54321:5432 alpine sleep 30` → **rc=0**.
  - `podman ps` → `w117-pmp Up 2 seconds 127.0.0.1:54321->5432/tcp`.
  - `podman inspect` → `HostPortBindings=[{127.0.0.1 54321}]`.
  - `podman rm -f w117-pmp` → **rc=0** (sauber removed).
- Netavark-Funktion belegt; die `cannot assign`-Klasse wurde NICHT reproduziert.

## 6. Aufrephase (Pflicht)
- Broker gestoppt: `systemctl --user stop ...-broker.service` → rc=0, `is-active` = inactive.
- Container entfernt: `podman rm -f bh-backup-recovery-ci-backup-cli-dev-broker` → **rc=0**.
- Verify: `podman ps -a --filter name=...-broker` → leer; `podman pod ls` → keine Pods; Service `inactive`/`generated`.
- Lane-eigene Container nach Projekt-Label-Scan: **NONE** — keine lane-eigenen Namen verbleiben.
- Shared-Stapel unverändert: `bh-backup-recovery-ci-shared` = 6 Cont. running, `bh-podman-test-core-shared` = 11 Cont. running (alle `Up`/`healthy`).
- `df -h /` (Nachher): `/dev/sda1 96G 53G 43G 56% /` (kleiner Anstieg durch temporäre Image-Pulls der Tests).
- `podman system df` (Nachher): Images 12 (9 aktiv, 3.432 GB, 65 MB reclaimable); Containers 25 (25 aktiv); Local Volumes 9 / 11 referenziert.

## Repo-Regelkonformität
- `.github/**` / Workflows: nicht bearbeitet, kein `workflow_dispatch`, kein Rerun. (Mission-Scope: Owner-Bereich.)
- Runner: nicht gebaut/registriert/repariert (GitHub shared runner).
- Proxmox / produktive Dienste: unangetastet.
- `podman system reset`: NIEMALS ausgeführt (Drei-Punkte-Prüfung nicht nötig, da kein Hänger; netavark funktioniert).
- Destruktive Eingriffe nur auf lane-eigene Container beschränkt; Shared-Stapel geschont.

## End-Zusammenfassung für f49a3303
bereinigt=JA (Broker lane-eigen gestopft+entfernt, keine lane-eigenen Namen/volumes verbleiben; Shared-Stapel stehen). neuaufbau=SKRIPT (`setup-baha-podman.sh` rc=0; baha 0.4.23, Target podman-test, Core SQL+Secrets+Identity READY). broker=BLOCKER (externer `backup-recovery-ci`-Deployment, ZustandTree fehlt, owning Deployment nicht auf VM; Rebuild erst nach neuem Deployment der `backup-recovery-ci`-Instanz möglich; Next-Trigger: Deployment erneut deployen → Broker neustarten → Healthcheck). laufend=rc0-belege vorhanden (`podman run --rm alpine true` rc=0; Port-Mapping `127.0.0.1:54321->5432/tcp` rc=0; Skript-Run rc=0). cleaning=BESTÄTIGT (`podman ps -a` lane-eigen leer, Shared-Stapel intakt, `df -h /` 56%). | Test-VM bereinigt und Core über Setup-Skript neu aufgebaut; einzig verbleibender `unhealthy` Broker ist externer Deployment-Blocker, dokumentiert mit Ursache und nächstem Auslöser.

## END
END_DONE w117-podman-vm-rebuild: bereinigt=ja neuaufbau=skript broker=blocker-text laufend=rc0-belege cleaning=bestaetigt | Test-VM bereinigt und Core über Setup-Skript neu aufgebaut (rc=0); einziger `unhealthy` Broker externer `backup-recovery-ci`-Deployment-Blocker, dokumentiert.
