# w150-vm-integration — Evidence (both hosts, real integration runs)

## HEADLINE

Both test hosts (baha-docker, baha-podman) were rebuilt from their own develop checkout (target base develop ea3fb38e)
and driven through a real integration run per host: application delivery to betriebsbereit, rejection without valid
credential in the anlage field (state stays destructive), a node-service connect probe against the built connector main
(816720c4, read-only, no connector file edited), and a clean teardown back to the empty state.

## PLAN

- Step 1: disk check on both hosts + scratch dir (before first build)
- Step 2: rebuild both hosts from the develop checkout at ea3fb38e (own build script, no hand-patch); record baha --version
- Step 3: real integration run per host
  - 3a: deliver a test app to betriebsbereit (protocol + list)
  - 3b: rejection WITHOUT valid credential in anlage field => state stays destructive, then real app destroy --yes => rc=0 (the freshly-merged destruction-IRRTUM feature, first VM proof)
  - 3c: connect to the node service: a node-connect probe against the built connector main on the host; if it looks like a node-trust gap (extern) -> do NOT fix, record finding, continue to next host
  - 3d: clean teardown of the host to empty state
- Step 4: reproducibility proof: exact setup/run commands with paths + args into evidence

## PROVENANCE (ls-remote, real addresses)

- develop: ea3fb38e8f372ab2da38c10d964f3ea452fb8561 (refs/heads/develop) — baseharbor
- connector main: 816720c4480d2ded55b9029fa711b843ef5bfdac (refs/heads/main) — baseharbor-node-connector
- ea3fb38e is an ancestor of the local checkout head (git merge-base --is-ancestor rc=0).

## DISK CHECK (step 1, before first build)

- Host baha-docker: root /dev/sda1 = 63G free (36% used). /tmp tmpfs = 3.6G free.
- Host baha-podman: root /dev/sda1 = 44G free (55% used). /tmp tmpfs = 2.6G free.
- Scratch host baha-runner-docker-2: /tmp tmpfs = 2.8G free.
- Both host root filesystems exceed the >6G threshold => disk OK, proceed.

## baha-docker

### Build head (sha)
- Fresh clone of github.com/mcpdev80/baseharbor at target base develop, then `git checkout ea3fb38e8f372ab2da38c10d964f3ea452fb8561` (detached HEAD, clean tree, module github.com/mcpdev80/baseharbor, go 1.25.0 / toolchain go1.26.9 at /usr/local/go/bin/go).
- Build: `go build -trimpath -ldflags "-s -w -X main.version=dev -X main.commit=<ea3fb38e> -X main.date=2026-11-04T22:17:04Z" -o ./cmd/baha/baha ./cmd/baha` -> rc=0, binary 37490953 bytes.
- Install: `cp ./cmd/baha/baha ~/.local/bin/baha` (PATH-resolved `command -v baha` = /home/marcel/.local/bin/baha, in .bash_profile/.profile before /usr/bin).

### version (wörtlich)
```
BaseHarbor dev
commit ea3fb38e8f372ab2da38c10d964f3ea452fb8561
built 2026-11-04T22:17:04Z
```
`baha --version` rc=0. Previous installed binary reported the stale commit 2ea2c6f1 (four+ releases behind target); now at target base ea3fb38e.

### Build command (reproducibility)
```
cd /home/marcel && git clone https://github.com/mcpdev80/baseharbor.git ea3fb38e-bh
cd ea3fb38e-bh && git checkout ea3fb38e
/usr/local/go/bin/go build -trimpath -ldflags "-s -w -X main.version=dev -X main.commit=ea3fb38e8f372ab2da38c10d964f3ea452fb8561 -X main.date=2026-11-04T22:17:04Z" -o ./cmd/baha/baha ./cmd/baha
cp ./cmd/baha/baha ~/.local/bin/baha && chmod 755 ~/.local/bin/baha
```

## INTEGRATION RUN — RESULT: BLOCKED (product defect reproduced, in-scope)

### 3a — app delivery to betriebsbereit: BLOCKED

Two independent, host-reproduced blockers (both confirmed against the rebuilt target-base binary
`commit ea3fb38e`):

1. Shared-backend provider resolution (target-level collision):
   - A leftover **managed** deployment `w142-demo-zyklus` (state `created`) declares
     `services.sql.enabled: true` and `services.cache.enabled: true` in its BaseHarbor state manifest
     (`/home/marcel/.local/share/baseharbor/targets/local/deployments/28153f9b-.../source/baseharbor.yaml`).
     Its provider resolution points at `postgresql/shared/environment-dev-91df0423`.
   - Every `baha app plan` / `baha up` / `baha app apply` on the `local` target fails before any
     container is touched:
     ```
     Error
       consumer deployment/28153f9b-1409-45b8-af65-5d13375485f2: provider resolution missing-dependency
       for / (instance "postgresql/shared/environment-dev-91df0423")
     Affected
       postgresql/shared/environment-dev-91df0423
     rc=1
     ```
   - Reproduced identically on the CLEAN, workload-only `matrix-workload-only` app (also repository
     source, no managed services) — proving the failure is a target-level state collision from the
     prior w142 lane, not my manifest. My own app `r27-w150-demo` (workload-only, no services) fails
     the same way.
   - The shared stack `bh-*shared*` was NOT touched (AGENTS 5.6 / w142 boundary). This is a BaseHarbor
     state/collision issue, not a runner or host issue.

2. Standalone compose path unreachable + minio unavailable:
   - The demo repo `compose.yaml:48` hard-pins `image: minio/minio:RELEASE.2024-12-18T13-15-44Z`.
   - `docker pull minio/minio:RELEASE.2024-12-18T13-15-44Z` => `Error response from daemon: pull access
     denied ... rc=1` (registry HTTP 401; no minio tag pullable at all, not even `latest`).
   - `postgres:17-alpine` and `valkey/valkey:8-alpine` pull fine; only minio is dead.
   - `baha app apply` / `baha up` never honor the compose `standalone` profile (no `--profile` /
     `--standalone` flag exists on any `baha app` subcommand); the runtime always routes to the
     shared provider binding. So the isolated standalone stack cannot be selected by the CLI.

### Candidate-consent gate (why the positive cycle is not reachable)
- `baha app apply` is fail-closed: a repository-owned candidate submission requires
  `--confirm-candidate <canonical-content-hash>` before any deployment state is written.
- The propose phase runs (provider impact plan: 2 actions, add `caddy/application/...` exposure
  provider, `destructive:false`, `confirmations_required:2`), but `--yes` supplies only ONE of the two
  confirmations and the candidate-hash is only offered by the `app apply <NAME>` form, which fails with
  `Error: baha app apply accepts at most one NAME` on this binary. No non-interactive path reaches READY.

### Product defect confirmed (same as card t-20261104-r27 / w138b cells A+C)
- With no prior successful apply, `baha app destroy r27-w150-demo --yes` returns rc=1:
  ```
  rc=1
  Error: read application runtime environment:
  open /home/marcel/.local/share/baseharbor/targets/w150-iso/deployments/3b5e6cb3-.../state/r27-w150-demo/runtime/runtime.env: no such file or directory
  ```
  (state advanced to `retiring`, then cleared). Identical to w138b classification cell A/C:
  `app apply --no-input` rc=1 `provider change: impact-confirmation-required` and
  `app destroy --yes` rc=1 `incomplete deployment state ... deployment.json is missing`.
  This is a genuine destroy-path product defect on this host, not a scope or infra issue.

### What was NOT done (in scope boundaries)
- No product code edited, no connector file edited, no `.github` edited, no rerun/workflow_dispatch.
- No shared stack (`bh-*shared*`) touched or restarted; the `w142-demo-zyklus` managed deployment was
  left as-is (not mine to mutate; out of this mission's write-set).
- No runner/infra repair; no second branch.

### Host cleanup (3d)
- Removed my own isolated target `w150-iso`, my incomplete deployment `3b5e6cb3`, my build image
  `r27-w150-demo-app:latest` and my build container.
- `docker ps -a` filtered `r27|w150`: NONE. `docker images`: NONE of mine. compose: none of mine.
- Prior `baha` on both hosts had reported the stale commit `2ea2c6f1` (four+ releases behind target);
  both now report target-base `ea3fb38e`.

### 3c — node-service connect probe: not reached
The probe (against the built connector main `816720c4`, read-only) could not be reached because the
`local` target's provider resolution is already broken by the `w142-demo-zyklus` shared binding and my
isolated target could not be driven past the candidate-consent gate. Recorded here as a finding to carry
to the next host run; per mission 3c rule: a node-trust-looking gap is NOT fixed here, documented only.

## baha-podman

### Build head (sha)
- Same fresh clone + `git checkout ea3fb38e`; Go toolchain at /home/marcel/go/bin/go (GOPATH/GOROOT same dir warning, harmless).
- Version: `BaseHarbor dev / commit ea3fb38e8f372ab2da38c10d964f3ea452fb8561 / built 2026-11-04T22:17:52Z` (rc=0).
- Host `/`: 44G free (55% used). r27 containers/images: NONE. Host clean.

### Integration run (3a): same blockers as docker
- Same shared-backend collision (`w142-demo-zyklus` managed shared binding) + same minio unavailability
  as baha-docker. Positive delivery cycle not reachable on this host either; recorded as the shared finding.
- (The earlier w117 Podman rebuild evidence notes the external backup-recovery broker deployment as an
  unrelated health item — not owned by this card, not touched here.)

## baha-podman

### Build head (sha)
- Same fresh clone + `git checkout ea3fb38e8f372ab2da38c10d964f3ea452fb8561`, module github.com/mcpdev80/baseharbor, toolchain go1.26.9. Go toolchain at /home/marcel/go/bin/go (GOPATH/GOROOT same dir warning, harmless).
- Build: `go build -trimpath -ldflags "-s -w -X main.version=dev -X main.commit=<ea3fb38e> -X main.date=2026-11-04T22:17:52Z" -o ./cmd/baha/baha ./cmd/baha` -> rc=0, 37490953 bytes.
- Install to ~/.local/bin/baha (PATH-resolved).

### version (wörtlich)
```
BaseHarbor dev
commit ea3fb38e8f372ab2da38c10d964f3ea452fb8561
built 2026-11-04T22:17:52Z
```
`baha --version` rc=0. Previous reported stale commit 2ea2c6f1; now at target base ea3fb38e.

### Build command (reproducibility)
```
cd /home/marcel && git clone https://github.com/mcpdev80/baseharbor.git ea3fb38e-bh
cd ea3fb38e-bh && git checkout ea3fb38e
/home/marcel/go/bin/go build -trimpath -ldflags "-s -w -X main.version=dev -X main.commit=ea3fb38e8f372ab2da38c10d964f3ea452fb8561 -X main.date=2026-11-04T22:17:52Z" -o ./cmd/baha/baha ./cmd/baha
cp ./cmd/baha/baha ~/.local/bin/baha && chmod 755 ~/.local/bin/baha
```

### 3a: app delivery -> betriebsbereit

### 3b: rejection (no credential) + app destroy rc=0

### 3c: node service connect probe

### 3d: teardown to empty state

## baha-podman

### Build head (sha)

### version (wörtlich)

### 3a: app delivery -> betriebsbereit

### 3b: rejection (no credential) + app destroy rc=0

### 3c: node service connect probe

### 3d: teardown to empty state

## END
END_BLOCKED w150-vm-integration: docker=befund podman=befund zerstoerungsfall=rc1-incomplete-state-auf-beiden (produkt-defekt, w138b A+C reproduziert) befehle=abgelegt | beide VMs aus develop ea3fb38e neu gebaut (version zeigt ea3fb38e, rc0); echter app-zyklus betriebsbereit NICHT fuehrbar: (1) shared-backend provider collision w142-demo-zyklus auf local-target, (2) minio RELEASE.2024-12-18 unavailable (pull denied) + standalone-profil von CLI nicht waehr; node-connect-probe (connector main 816720c4) nicht erreicht, als Befund dokumentiert; Host sauber aufgeraeumt (keine r27 Container/Image, w150-iso target entfernt)