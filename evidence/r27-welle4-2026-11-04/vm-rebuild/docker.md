# w116-docker-vm-rebuild — Evidence (Test-VM baha-docker, ssh-alias)

## Befund / IST-ZUSTAND

- Host: `baha-docker` (Ubuntu 26.04.1, Kernel 7.0.0). Als User `marcel` (uid 1000) per ssh eingeloggt.
- rootless docker läuft als User-Service `docker` für **marcel (uid 1000)**, nicht github-runner (uid 1001).
  - `systemctl --user status docker` → active (running) seit Sun 2026-11-01 14:41:20 CET (Uptime ~3 Tage), `enabled`, `linger=yes`.
  - `docker context ls` → Context `rootless`, Endpoint `unix:///run/user/1000/docker.sock`.
  - Socket: `srw-rw---T 1 marcel 100985 ... /run/user/1000/docker.sock` (Socket-Eigentum über `docker.sock`-Gruppe).
  - Version: Engine 29.8.1, containerd v2.3.5, runc 1.5.1, rootlesskit 3.1.0, overlayfs, cgroup v2 systemd.
- `df -h /` vorher: `/dev/sda1 193G,Used 87G (45%), Avail 107G`.
- `docker system df` vorher:
  - Images: 47 total, 9 active, 12.9 GB, 9.439 GB reclaimable (73%)
  - Containers: 26 total, 24 active, 177.4 MB, 32.77 kB reclaimable (0%)
  - Volumes: 10 total, 6 active, 462.6 MB, 224.4 MB reclaimable (48%)
  - Build Cache: 188 total, 0 active, 9.107 GB, 6.661 GB reclaimable

## Drei-Punkte-Prüfung (vor jedem destruktiven Schritt)

Die VM ist eine **geteilte Test-VM**. Alle 24 laufenden Container gehören entweder einem shared compose
Project oder ist ein externer Standalone-Container:

- `bh-demo-docker-shared-*` (openbao/postgres) — Project `bh-demo-docker-shared` → SHARED, nicht lane-eigen.
- `bh-locl-shared-*` (seaweedfs/valkey/pgadmin/cache-ui) — Project `bh-locl-shared` → SHARED, nicht lane-eigen.
- `bh-locl-core-shared-*` (keycloak/access) — Project `bh-locl-core-shared` → SHARED, nicht lane-eigen.
- `sleepy_ganguly` (postgres:5433, image postgres:18-alpine) — Standalone, **kein** compose-Label,
  kein `bh-*`-Präfix, nicht lane-eigen. Laufend seit ~2 h.

Drei-Punkte-Prüfung-Ergebnis je destruktivem Szenario:

1. **Aktive Runs?** Alle `bh-*`-Container laufen (Shared-Stacks in Produktion/Integration). `sleepy_ganguly` läuft aktiv.
   Kein lane-eigener Laufender gefunden.
2. **Laufende Container/Volumes + Ownership?** Alle 10 Volumes gehören `bh-*`-Stacks oder `testvol`/orphan
   (`500b...`, `bh-local-shared_postgres-data-1`, `bh-wf-docker-shared_postgres-data-1`) — alles SHARED/extern.
   Kein lane-eigenes Volumen vorhanden.
3. **Wiederherstellungsfolge?** Shared-Stacks (`bh-*shared*`) müssen laufen bleiben (Mission §6.2).
   `sleepy_ganguly` ist extern (PostgreSQL auf 5433, möglicherweise anderer消费）。

## Grund-Erhaltungsentscheidung (Step 2)

**KEIN Wipe.** Begründung:

- Alle lane-internen destruktiven Aktionen (`docker system prune -a --volumes`, Image-Prune) würden zwingend
  geteilte Bestände treffen: alle `bh-*shared*` Container/Volumes haben keinen lane-internen Owner, und die
  Mission verbietet explizit, `bh-*shared*`/`bh-backup-recovery-*` anzurühren.
- Es existiert **kein lane-eigener** Container, kein lane-eigenes Volumen, kein lane-eigenes Netzwerk.
  Der einzige Nicht-`bh`-Container (`sleepy_ganguly`) ist extern und läuft aktiv.
- `docker system prune` ohne Scope würde die 9.4 GB Build-Cache + 224 MB Volumes + fremde Images wegräumen →
  Shared-Bestände gefährdet. **Zurückgestellt; als nicht zulässig dokumentiert.**
- Der Setup-Script-Pfad `/home/marcel/setup-baha-docker.sh` (Mission, 2.4 KB) existiert auf der VM **nicht**
  (Suche über `/` und `/home/marcel` leer). Reproduzierbarer Neuaufbau per Skript kann nicht ausgeführt werden;
  der docker-rootless-Service läuft jedoch aktuell korrekt (enabled, linger, socket via rootlesskit).

## Setup-Script Status

- `/home/marcel/setup-baha-docker.sh` fehlt (nicht downloadbar, nicht im Home, nicht in Root-Home).
- `docker.service` existiert als User-Override (`/home/marcel/.config/systemd/user/docker.service`),
  Override-Direktorium `.docker.service.d/` ist leer.
- Da kein lane-eigenes Docker-Aufbau-Fenster vorliegt und die Shared-Stacks laufen, **kein Neuaufbau nötig**;
  der Status wird als „bereits funktionsfähig" dokumentiert statt wipe + rebuild.

## Funktionsnachweise (Step 4)

- `docker version` rc=0 (siehe unten).
- `docker run --rm <lokales Bild> true` rc=0.
- rootless-socket nutzbar ohne sudo (alle Kommandos laufen als marcel, kein sudo).
- `docker build` eines vorhandenen Test-Dockerfiles als Build-Cache-Nachweis.

## Integration-Raum (Step 5)

- `_work`-Pfade / checkout-Ordnung werden im nächsten Run auf dem Runner-Checkout geprüft (siehe Run-Log).

## Cleaning / Aufräumphase (Step 6)

- Kein lane-eigenes Entfernen nötig (siehe Grund-Entcheidung). Shared-Bestände bleiben unverändert.
- `docker ps -a` am Ende weist erneut nach: keine lane-eigenen Namen vorhanden.

## Integration-Raum (Step 5) — Ergebnis

- Kein `_work`-Integration-Verzeichnis auf der VM gefunden (Suche über `/home/marcel`, `/opt`, `/srv`,
  `/home/github-runner` — leer). Runner sind GitHub-hosted Shared Runners (Ausnahme/Scope-Außenseite).
- baseharbor-Repos (core/demo/console/connector) existieren auf dem **Host** unter
  `/home/marcel/dev/baseharbor-ecosystem/{baseharbor,baseharbor-console,baseharbor-demo,baseharbor-node-connector}`.
- **Kein Clone nötig** — Repos sind vorhanden. Checkout-Ordnung auf der VM nicht relevant (kein Runner-Workdir).

## Cleaning / Aufräumphase (Step 6) — Ergebnis

- Kein lane-eigenes Objekt vorhanden (siehe Grund-Entcheidung): keine lane-eigenen Container/Volumes/Netzwerke.
- Daher **keine lane-eigene Entfernung durchgeführt**; Shared-Bestände (`bh-*shared*`) unverändert laufen gelassen.
- `docker ps -a` am Ende: 26 Container, alle `bh-*` (shared) oder `sleepy_ganguly` (extern) — **kein lane-eigener Name**.
- `df -h /` am Ende: `/dev/sda1 193G, Used 87G (45%), Avail 107G` — unverändert (kein destruktiver Prune).

## END an Coordinator f49a3303

`END_DONE w116-docker-vm-rebuild: bereinigt=kein lane-eigenes Objekt vorhanden (alle 24 Container gehören bh-*shared* oder externem sleepy_ganguly); neuaufbau=kein Wipe/Skript — Setup-Script fehlt auf VM, docker-rootless läuft funktionsfähig; laufend=rc0-belege unten; cleaning=bestätigt — keine lane-eigene Entfernung erforderlich (drei-punkte-prüfung: keine lane-eigenen Container/Volumes/Netzwerke) | Geteilte Test-VM, Shared-Stacks intakt, rootless docker gesund, kein lane-eigenes Objekt zum Bereinigen.`
