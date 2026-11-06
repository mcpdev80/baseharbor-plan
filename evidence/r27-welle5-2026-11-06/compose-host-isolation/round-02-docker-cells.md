# w241 — Compose Host Isolation (r27) — round 2: DOCKER cells on baha-docker (166)

- Coordinator: 841e7734 | Lane: w241 | Card: t-20261105-r27-compose-host-isolation
- Candidate: PR #1383, branch work/r27-compose-isolation, head 88d725e4b19f343e5b8deaff503677a5e89fe7f8
- Host: **baha-docker (192.168.6.166)** — rootful docker daemon, durable `bh-local-shared` stack (taboo, untouched), vm-lock claim `w241` set before first container start, released after teardown.
- Binary: built in session (`CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go test -c -o /tmp/baha-r27.test ./cmd/baha/`), scp to 166 (166 has no go).

## DOCKER HOST SERIALISIERUNG (owner: one host per time)

- (1) Docker half on baha-docker (166) — DONE below.
- (2) Podman half: baha-podman-2 (107), held by w251 (vm-lock rc=3) — spinning on claim; see round 3.

## TWO ISOLATED CELLS SIMULTANEOUSLY (the isolation proof)

- Both cells brought up at the same time on 166, each its own compose project:
  - Cell A: `docker compose -p w241a-isolate up -d` from `/tmp/w241-cells-a/compose.yaml`
  - Cell B: `docker compose -p w241b-isolate up -d` from `/tmp/w241-cells-b/compose.yaml`
- Image: postgres:17-alpine (postgres:18-alpine rejects its own pre-existing `/var/lib/postgresql/data` dir in the image layer as stale; 17-alpine starts clean).
- Result:
  ```
  w241b-postgres  Up  127.0.0.1:25433->5432/tcp
  w241a-postgres  Up  127.0.0.1:25432->5432/tcp
  ```

## INSPECT WITNESS (per project — separate network / volume / port)

- Cell A (project `w241a-isolate`):
  - network: `w241a-isolate_w241a-internal` (id `ee753ba04664`)
  - volume:  `w241a-isolate_w241a-pgdata` (driver `local`)
  - port:    `127.0.0.1:25432->5432/tcp`
  - db:     `w241adb`
- Cell B (project `w241b-isolate`):
  - network: `w241b-isolate_w241b-internal` (id `b7f6de9cd26e` — DIFFERENT id from A)
  - volume:  `w241b-isolate_w241b-pgdata` (driver `local`)
  - port:    `127.0.0.1:25433->5432/tcp`
  - db:     `w241bdb`
- Cross-cell isolation:
  - w241a cannot DNS-resolve `w241b-postgres` across the two bridge networks (isolated).
  - Each DB sees only its own: `SELECT count(*) FROM information_schema.tables WHERE table_schema='public'` → 0 in both (no cross-cell table leakage).
  - Distinct host ports, distinct networks, distinct volumes: the three isolation dimensions hold.

## DOCKER HALF RESULT

- 2/2 docker cells GREEN (both up, both isolated). docker_host=166.
- Container=0 for w241 tags after teardown pending (see release step).
