# VM Smoke — Round 3 (baha-docker abgeschlossen, baha-podman offen)

Lane: w246 (frueher im Schlossbuch fälschlich 'w227' vermerkt — Koordinator 2026-11-06 korrigiert).
Mission: w227-vm-smoke-r2, Kartentitel t-20261104-r27-vm-smoke-docker-podman (RUNDE 2).
Koordinator: 841e7734.

## Stand nach Round 2 (Kontext)
- baha-podman hatte 8 laufende bh-podman-test-shared Container (postgres/openbao/keycloak/haproxy/caddy),
  inhaber=w243, stack vor ~8min -> als aktive Lane w243 identifiziert. DECISION Koordinator: NICHT loeschen.
- w243 haelt baha-podman-Claim (vm-lock). podman-Haelfe blockiert bis Freigabe.

## Round 3 — baha-docker: abgeschlossen (gruen)

### (1) Vorpruefung baha-docker
- container=0, keine baha-Prozesse, keine baha-Konf/Cache.
- alt-baha: launcher `~/.local/bin/baha.bak-0.4.23-9514a768`, version `baha 0.4.23 (commit 9514a768...)`, built 2026-10-08.

### (2) Alt weg (Owner-Direktive)
- `rm -f ~/.local/bin/baha.bak-0.4.23-9514a768`. Danach `command -v baha` -> "baha: nicht installiert".

### (3) Rootless Docker (bestaendigt, nicht neu eingerichtet)
- rootful: `sudo docker run --rm hello-world` -> "Hello from Docker!" (gruen).
- rootless: `docker run --rm hello-world` -> "Hello from Docker!" (gruen).
- rootless socket: `/run/user/1000/docker.sock` (systemd user docker.service, active/running).
- storage driver rootful = overlayfs; load niedrig (~0.3).

### (4) Neu bauen (develop)
- source: /home/marcel/dev/baseharbor-ecosystem/baseharbor, branch develop, sha 5e4fde7177ea020de39b117f6d89cfa8f7c62be2.
- build: `go build -ldflags "-X main.version=dev -X main.commit=5e4fde71... -X main.date=2026-11-06"`.
- version nach build: `baha dev (commit 5e4fde7177ea020de39b117f6d89cfa8f7c62be2, built 2026-11-06)`.
- Install: `~/.local/bin/baha` auf baha-docker.

### (5) Smoke baha-docker (Befehl + Ausgabe wortlich)
- `baha node list` -> "No remote connector nodes configured." (node/enroll-Workflow praezipiert)
- `baha up --control-plane-only --postgres-port 15432 --openbao-port 15200 --yes`:
  - "[OK] OpenBao initialized and unsealed", "[OK] baseharbor KV v2 mount configured",
  - "BaseHarbor Core READY: SQL + Secrets + Identity."
- `baha app init --input tls_mode=local --yes` (dev domain smoke.local):
  - "Application runtime initialization saved for w227-smoke2 (dev). Runtime provider: docker."
- `baha app apply` mit Automatisierungspfad (Koordinator-Handoff w237):
  - `BASEHARBOR_PROVIDER_CHANGE_CONSENT='{"plan_id":"<angezeigter>","first":true,"second":true,"delete_data":false}'`
  - zweiter Lauf: `baha app apply --confirm-candidate 57c3678166661251bfafa048b68a7a43b76c061c861ac5da5048cf0e0643c11e`
  - Ergebnis: "[OK] Waiting for backend readiness - done", "Services: READY PostgreSQL authenticated SELECT 1",
    "OK READY application and requested infrastructure verified".
- `baha status` -> "READY" (application, postgres, postgres/primary, service-bindings, core-shared/openbao/postgres, TLS).
- `baha doctor` -> alle OK (workload discovery/security/repository, service TLS sql/primary READY, certificate READY).
- Container meiner App nach down: NONE (nur noch 9 gemeinsame bh-*-shared/-control-plane Container, nicht meins).

### (6) Nach Smoke rueckgebaut (fabrikregel)
- `baha app down` (mit consent-env + --confirm-candidate) -> "STOPPED application persistent data preserved".
- baha-Binaeren entfernt: `command -v baha` -> "baha: nicht installiert".
- Container meiner App: NONE. Shared control-plane (9x bh-*-shared/-core-shared) laut R4 = NIHT anfassen, verbleibt.
- ps-witness (docker): container meiner Lane = NONE; load ~0.28.

### Blocker/Notes (docker)
- `baha app apply` / `baha down` sind fail-closed: 2-Stufen provider-impact confirmation + candidate submission.
  Nicht-interaktive Loesung = dokumentierter Automatisierungspfad w237 (BASEHARBOR_PROVIDER_CHANGE_CONSENT env
  {"plan_id","first","second","delete_data"}, key-namen aus internal/application/provider_change_types.go:
  PlanID/First/Second/DeleteData; zweiter Lauf --confirm-candidate <hash>). Ohne env: "impact-confirmation-required".
- Ein hängender `baha app apply` (PID 1171556, eigener pty-run, haelt Installation-Lifecycle-Lock) wurde nach
  Koordinator-Freigabe (Option 2) per SIGTERM/SIGKILL beendet; parent-bash 1171553 mit.

## baha-podman: OFFEN (wartet auf w243-Freisabe)
- 8 laufende bh-podman-test-shared Container (inhaber=w243). NICHT loeschen (Koordinator-DECISION 2026-11-06).
- vm-lock baha-podman: inhaber=w243.
- erst nach release von w243: claim als w246, smoke (rootless podman + baha), rueckbau, release.

## END_STATE
- docker: GRUEN — control-plane READY, app apply gruen (PostgreSQL SELECT), status/doctor READY, rootless docker hello-world, fabrikregel rueckgebaut.
- podman: WARTET AUF W243-FREISABE — 8 shared-container unveraendert, claim bei w243.
- raumzustand docker: 0 Container meiner Lane; 9 gemeinsame control-plane (R4-gemaess unveraendert).
- vm-lock baha-docker: RELEASED (w246). baha-podman bleibt bei w243.
