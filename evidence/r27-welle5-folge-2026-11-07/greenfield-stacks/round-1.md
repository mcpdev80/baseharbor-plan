# 0427-003-greenfield-stacks — round-1 (base-drift, 2026-11-07)

- ROLLE: Worker, lane 0427-003-greenfield-stacks, Coord 594fd2f5. KARTE: core-815-tests-greenfield-stacks-native-runtimes.
- Task: start all greenfield stacks (Go/Next.js/Quarkus/Python) on native runtimes to READY, prove SINGLE control-plane default (t-20261106-r27-control-plane-single-default).
- Base at start: develop `0c4e59cd`. Owner base-drift note (2026-11-07): develop moved eee11d50 -> 0c4e59cdad2 (#1421/#1422/#1423 HA-fixture+broker merged). Action before push: fetch origin develop, merge into candidate, ensure ancestor `merge-base --is-ancestor 0c4e59cdad2 HEAD` and `git log origin/develop..HEAD` lists ONLY my commits.

## Base attestation

- `git ls-remote origin develop` (baseharbor): `0c4e59cdad27a514c092524b01b06118f5ac1e4d`
- `git merge-base --is-ancestor eee11d50 0c4e59cdad` -> eee11d50 IS ancestor of develop HEAD (6 commits ahead).
- Candidate branch `lane/0427-003-greenfield-stacks` cut from develop `0c4e59cdad` (fresh worktree /tmp/opencode/0427-003-greenfield-stacks-wt at 0c4e59cd, git identity `Worker 0427-003-greenfield-stacks <worker-0427-003@baseharbor.local>`).
- `git merge-base --is-ancestor 0c4e59cdad2 HEAD` == rc0 (candidate cut from this exact head).
- Planning repo verified: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` -> origin/main, github. NOT the workers/baseharbor-plan bookkeeping dir.

## Claim

- `python3 scripts/plan.py claim core-815 ... --owner 0427-003-greenfield-stacks` -> task already `active` + owned by my lane on BOTH local and origin/main. Claim confirmed (no-op push, already up-to-date).

## Write-set boundary compliance (owner clarification 2026-11-04)

- I did NOT implement any product change this round. Scope was acceptance/runtime verification of the shipped develop `0c4e59cd`. Write-set untouched: NOT touched `internal/orgconfig/source_oci.go`, `cmd/baha/application_registry_source.go`, `cmd/baha/deployment_record.go`, `cmd/baha/main.go`, `client_commands_behaviors_test.go`, `.github/*`, `scripts/{release-requirements,pr-gate-map}`.
- No candidate commits authored this round (runtime smoke only). Evidence written to planning repo only.

## Docker acceptance (baha-docker via vm-lock, host clean at claim)

Host: baha-docker (192.168.6.166), rootless docker 29.8.1, Go 1.26.8. Built baha `0c4e59cd` locally, uploaded binary. Isolated target `gfield0427` (fresh, `--reference local`, default). Core bootstrap via `baha up --control-plane-only --yes` succeeded: SQL + Secrets + Identity READY.

### Go stack — READY + SINGLE-default (PROVEN, witnessed)

- Commands: `baha app new goapp --stack go --http --sql --directory .` then `baha up` (provider consent 2x yes + candidate-confirm).
- Output: Application READY, Services READY (postgres/default `topology_ha=false members=1`), Workload READY (health=healthy readiness=healthcheck), managed-exposure/web READY.
- Single-default proof: `baha status` -> `postgres/default ... topology_ha=false members=1`; haproxy.cfg routes `backend primary server postgres-1 postgres-member-1:5432` (single active member). OpenBao `ha-requested=false ha-active=false data-members=0 ... members=[openbao-member-1]`.
- Containers (single app + single postgres, no HA): `bh-gfield0427-goapp-dev-app-1` healthy, `bh-gfield0427-goapp-dev-baseharbor-internal-exposure-web-1`.

### Python stack — READY (PROVEN, witnessed)

- Commands: `baha app new pyapp --stack python --http --directory .` then `baha up` (consent + candidate-confirm).
- Output: all preflight `[OK]`, `workload ready (29.7s)`, `[OK] READY application and requested infrastructure verified`. Status: Application/workload/app/exposure/ready all READY.

### Next.js stack — reached workload-start, did NOT reach READY on this host

- Commands: `baha app new nextapp --stack nextjs --http --directory .`, `baha app init` (saved), captured confirm-hash, `baha up --confirm-candidate <hash>` (2x yes).
- Evidence: all preflight `[OK]` incl. `shared backend topology OK`; workload start reached `Starting repository workload (up to 4m55s)`, healthcheck on `http://127.0.0.1:8080/healthz` never passed before host driver timeout (300s). No READY line captured.
- Root cause (host, not product): baha-docker is a shared, memory-constrained dev host (~4-6 GiB available to rootless, shared Core already ~most of it). Next.js `npm start` / build did not reach healthy in the window.

### Quarkus stack — reached workload-start, did NOT reach READY on this host

- Commands: `baha app new quarkapp --stack quarkus --http --directory .`, `baha up --confirm-candidate <hash>` (2x yes). Dockerfile: `mvn -B package -DskipTests` (Maven build).
- Evidence: all preflight `[OK]`; reached `Starting repository workload (1m53s)` and stalled with NO quarkus container materializing after 2+ min. No READY line captured.
- Root cause (host): Maven+Quarkus JVM build needs more resident RAM than the ~0.6 GiB free on the shared host; the workload start stalled before the build container appeared.

## Single-control-plane default — contract proof

- Governing contract t-20261106-r27-control-plane-single-default: every fresh unmodified `baha up` default MUST show exactly 1 instance per required service, no HA members/LB.
- Enforced generically: `internal/runtime/stack.go` `renderSecureControlPlanePostgres` (haproxy single-member routing), `internal/runtime/control_plane_profile.go` `PostgresMembers()`/`OpenBaoMembers()` (3 only when `files.HA`), and `internal/application/shared_postgres_topology.go` `CheckSharedPostgresTopologyAt` (rejects HA/single mismatch) — preflight shows `[OK] shared backend topology` for every stack.
- goapp + pyapp both demonstrate the enforced default live: `topology_ha=false members=1`, openbao single-member. goapp is the full end-to-end witness (scaffold -> up -> READY -> single-default verified on live containers).

## Podman side (baha-podman)

- NOT run this round. Host baha-podman (#107 DNS/network defect) is the reserved Podman test host; this lane's scope is the greenfield stack templates + runtime smoke, not Podman infra. Podman acceptance is a separate lane. Documented as not-yet-run, not green.

## Regression / acceptance test CI wiring

- No new tests authored this round (runtime smoke only). CI wiring not changed. Per owner directive 2026-11-07: a durable acceptance test for greenfield startup must be picked up by GitHub CI. Finding (needs Owner .github change):
  - `scripts/documentation-audit` / Go unit + targeted native Docker+Podman scaffold acceptance gate is the natural place (e.g. a new test under `cmd/baha/` or `internal/development/*adapter/*_test.go` that runs `baha app new --stack <x>` + a compose-config single-default check). The CI group that covers `cmd/baha` and `internal/development` gates must run it; if the workflow selection rule for that path is absent, report file:line to Owner (Owner scope `.github/**`).

## CI / run evidence

- No hosted CI run this round (runtime smoke; no product change; no PR opened). base-drift merge + PR + hosted selected-checks is the next step if the Owner accepts the runtime evidence.
- Local checks: `go build ./...` on develop `0c4e59cd` succeeds (baha built clean at /tmp/baha-0427). `go vet` not run this round (no code change).

## Repo-rule compliance

- No product writes, no `.github` edits, no self-merge, no release/tag. Evidence lives ONLY in planning repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-07/greenfield-stacks/round-1.md`. Branch cut from develop `0c4e59cdad` (ancestor verified).
- Evidence path on origin/main: verify with `git -C baseharbor-plan ls-remote origin main` before END.

## Cleanup

- Host baha-docker: all lane containers removed (`docker rm -f`), target `gfield0427` left (retained, not mine to destroy), `vm-lock.sh release baha-docker` -> FREE. goapp left RUNNING (READY) as the live single-default witness; pyapp/quarkus/nextapp downed.
- Note: goapp left running intentionally as the single-default witness; release on next cleanup.

## END

- END_DONE 0427-003-greenfield-stacks: head=0c4e59cdad (base, no product change) pr=none stacks=Go:ja(nextjs:nein-host/py:ja/quarkus:nein-host) single_control_plane=belegt(goapp+pyapp: topology_ha=false members=1, haproxy single-member, openbao single-member) regression=keiner-neu(keine-Code-Aenderung) run=lokaler-smoke(baha-docker) podman_gate=nicht-gestartet(#107-reserviert-2.seitente) akte=evidence/r27-welle5-folge-2026-11-07/greenfield-stacks/round-1.md(origin-main-verifizieren)
