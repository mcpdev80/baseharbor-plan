# w241 — Compose Host Isolation (r27) — round 3: PODMAN cells on baha-podman-2 (107)

- Coordinator: 841e7734 | Lane: w241 | Card: t-20261105-r27-compose-host-isolation
- Candidate: PR #1383, branch work/r27-compose-isolation, head 88d725e
- Host: **baha-podman-2 (192.168.6.107)** — Podman 5.7.0 + `podman compose` plugin. vm-lock claim `w241` set before first container start, released after teardown.
- Host serialisation: docker half on 166 done & torn down first; podman half on 107 after (one host per time).

## PODMAN HOST CLAIM TIMELINE

- Mission said podman-2 (107) held by w251 until END (rc=3 BUSY).
- Checked 107: initially the durable `bh-podman-local2-shared` stack was running (not mine).
- Later re-checked: w251 had ENDed, 107 was empty (no containers, no lock). vm-lock `w241` claimed, then released after teardown.
- Did NOT touch 148/w243 (owner: do not silently move without coordination).

## TWO ISOLATED CELLS SIMULTANEOUSLY (the isolation proof)

- Both cells brought up at the same time on 107:
  - Cell A: `podman compose -p w241ap up -d` from `/tmp/w241-cells-a/compose.yaml`
  - Cell B: `podman compose -p w241bp up -d` from `/tmp/w241-cells-b/compose.yaml`
- Image: `docker.io/library/postgres:17-alpine` (podman needs a full unqualified reference; short `postgres:17-alpine` fails with "no unqualified-search registries").
- Result:
  ```
  CONTAINER ID  IMAGE                                      STATUS       PORTS
  a3de1cd37839  docker.io/library/postgres:17-alpine       Up  ...    127.0.0.1:26433->5432/tcp  w241bpost
  42fc471b646a  docker.io/library/postgres:17-alpine       Up  ...    127.0.0.1:26432->5432/tcp  w241apost
  ```

## INSPECT WITNESS (per project — separate network / volume / port)

- Cell A (project `w241ap`):
  - network: `w241ap_w241a-internal` (id `e42c6439ccd9...`, bridge)
  - volume:  `w241ap_w241apgdata` (driver `local`)
  - port:    `127.0.0.1:26432->5432/tcp`
  - db:     `w241adb`
- Cell B (project `w241bp`):
  - network: `w241bp_w241b-internal` (id `c7489bae2d53...`, bridge — DIFFERENT id from A)
  - volume:  `w241bp_w241bpgdata` (driver `local`)
  - port:    `127.0.0.1:26433->5432/tcp`
  - db:     `w241bdb`
- Cross-cell isolation:
  - Distinct network IDs (A≠B), distinct host ports, distinct volumes.
  - w241apost does NOT DNS-resolve from w241bpost across the two bridge networks (isolated).
  - Distinct DBs: `SELECT current_database()` → `w241adb` / `w241bdb`.

## PODMAN HALF RESULT

- 2/2 podman cells GREEN (both up, both isolated). podman_host=107.
- Container=0 for w241 tags after teardown (ps witness empty), my volumes/networks removed, vm-lock released.
- Shared-stack note: by the time I claimed/released 107, w251 had already ENDed and the durable `bh-podman-local2-shared` stack was gone (released by w251's teardown, not mine). No foreign stack touched by this lane.
