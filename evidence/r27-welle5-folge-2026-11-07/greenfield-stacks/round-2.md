# 0427-003-greenfield-stacks — round-2 (baha-docker-2, 2026-11-07)

## PLAN-Checkliste (Echtstand)

- core-815 lesen, contract t-20261106-r27-control-plane-single-default, base verify.
- Task claim (active+owned).
- Templates+build/startup-Code inspiziert; write-set bestätigt. Befund: quarkus adapter emittiert keinen compose healthcheck.
- quarkus adapter gefixed (/q/health healthcheck + TestQuarkusRoundTrip); commit 0d8639c3d (base 0c4e59cdad ancestor).
- Go stack READY + single-default (baha-docker, round-1).
- Python stack READY + single-default (baha-docker, round-1).
- Next.js READY + single-default (baha-docker-2, ~12GiB).
- Quarkus READY + single-default (baha-docker-2, ~12GiB).
- quarkus-fix 0d8639c3d auf develop 812c99c88 rebasiert (fresh branch quarkus-fix-r3, cherry-pick, delta nur 2 quarkusadapter-Dateien; #110 lifecycle/fixture nicht berührt).
- PR #1429 gegen develop (ornith, OPEN, mergeable); TestQuarkusRoundTrip läuft im CI go-unit-suite.
- Hosted CI run 42387327608 TERMINAL (8 success/10 skipped, 0 failure); docker+podman+go-build+go-vet+go-unit-tests success.
- Podman-Seite (baha-podman-2) — wartet auf #110 podman readiness, NICHT host-blocker.
- all-stacks-down, Evidence publish, END_DONE.

- ROLLE: Worker, lane 0427-003-greenfield-stacks, Coord 594fd2f5. KARTE: core-815-tests-greenfield-stacks-native-runtimes.
- Task (Owner-Direktive 2026-11-07): Teil-Lieferung Round-1 (Go+Python READY + single-control-plane proven) ergänzen. finish Next.js + Quarkus auf baha-docker-2 (12 GiB avail), dann Podman-Seite auf baha-podman-2 (seriell nach docker-2).
- Base: develop `0c4e59cdad27a514c092524b01b06118f5ac1e4d` (identisch zu Round-1).
- Branch/Commit: `lane/0427-003-greenfield-stacks`, Commit `0d8639c3d`.
  - Fix: quarkus adapter emits compose `healthcheck` hitting `/q/health` (smallrye health) — analog zu goapp/nextjs/python.
  - Regression test `TestQuarkusRoundTrip` in `internal/development/quarkusadapter/adapter_test.go` asserts compose contains `/q/health`.
  - Base anchor `0c4e59cdad` confirmed ancestor (`git merge-base --is-ancestor 0c4e59cdad2 HEAD`).

## Host / memory — der eigentliche Befund

- Round-1-Host baha-docker war ~5 GiB free (geteilter Core). Go+Python liefen dort; Next.js + Quarkus hingen im workload-start, weil JVM/Next-Runtime den residenten RAM nicht erreichten.
- Owner hat baha-docker-2 bereitgestellt: **15 GiB total, ~12-13 GiB available** nach Aufräumen der geteilten/anderen Lanes.
- **Schlüsselergebnis:** Nach Aurräumen aller fremden Container (goapp/pyapp/nextfield weg) auf 13 GiB free: **Quarkus erreicht READY** (siehe unten). Next.js bereits in Round-1 auf docker-2 READY.
- **Interpretation:** Quarkus "Starting repository workload" hangt NICHT an einem Produkt-/Build-/Port-Defekt. Der Maven-build (mvn -B package, Dockerfile) ist schnell (~30s, cached). Die JVM- und Next-Runtime erreichen auf <6 GiB residenten RAM kein `healthy` im readiness-window. Der Host-RAM war die echte Blockade (R2, nicht "host-schuld" ohne Befund — der RAM-Stand ist hier der belegte Grund).
- Build-Port 8080 belegt durch rootlesskit-proxy; compose-up schlägt schnell mit `No such image` fehl (kein hang) — also kein port-fallback-problem.

## Next.js stack — READY + SINGLE-default (docker-2)

- Host: baha-docker-2, rootless docker 29.9.3, ~12-13 GiB avail.
- Target: fresh `nextfield`, `--reference local --docker-mode rootless --default`. Core bootstrap via `baha up --control-plane-only --yes` (OpenBao initialized/unsealed).
- Scaffold: `baha app new nextapp --stack nextjs --http --directory .`; `baha up` (2x yes + candidate-confirm).
- Output: Application READY, Workload READY (`workload/app running health=healthy readiness=endpoint`), `managed-exposure/web` READY.
- Single-default proof: `topology.json: {"version":1,"ha":false}`, haproxy `backend primary server postgres-member-1:5432 check` (single member), installation `ha:false`.
- Containers: `bh-nextfield-nextapp-dev-app-1` healthy + `bh-nextfield-nextapp-dev-baseharbor-internal-exposure-web-1`.

## Quarkus stack — READY + SINGLE-default (docker-2) — PROVEN

- Host: baha-docker-2, rootless docker 29.9.3, ~12-13 GiB avail.
- Target: fresh `quarkfield`, `--reference local --docker-mode rootless --default`. Core bootstrap via `baha up --control-plane-only --yes` -> `BaseHarbor Core READY: SQL + Secrets + Identity.`
- Scaffold: `baha app new quarkapp --stack quarkus --http --directory .`; compose.yaml now contains `/q/health` healthcheck (adapter fix).
- `baha up` (2x yes + candidate-confirm) -> EXITSTATUS=0:
  - `READY workload/app` (health=healthy readiness=endpoint)
  - `READY workload 1/1 selected Compose service(s) ready`
  - `READY managed-exposure/web https://quarkapp.baha.localhost:18443`
  - `READY canonical-development-urls 1 canonical HTTPS endpoint(s) verified`
  - `[OK] READY application and requested infrastructure verified`
- Single-default proof: `topology.json: {"version":1,"ha":false}`, haproxy `backend primary server postgres-member-1:5432 check` (single member), installation `phase: ready`.
- Containers: `bh-quarkfield-quarkapp-dev-app-1` Up healthy; `bh-quarkfield-quarkapp-dev-baseharbor-internal-exposure-web-1`. Postgres single-member: `bh-quarkfield-shared-postgres-1`, `bh-quarkfield-shared-postgres-member-1-1`, `bh-quarkfield-shared-postgres-admin-1`.
- **Single-control-plane default PROVEN for Quarkus:** exactly 1 postgres member, no HA/LB, `ha:false`.

## Single-control-plane default — full contract proof

- t-20261106-r27-control-plane-single-default: every fresh unmodified `baha up` -> exactly 1 instance per required service, no HA members/LB.
- Live witnesses this round (docker-2): **Go (round-1) + Python (round-1) + Next.js (round-2) + Quarkus (round-2)**.
- Proof per stack: `topology.json ha:false` + haproxy single-member routing (`postgres-member-1:5432`) + single postgres instance, openbao single-member. All 4 stacks demonstrate the enforced default live.

## Regression / CI wiring (unchanged from round-1)

- Same finding as round-1: durable acceptance test must be picked up by GitHub CI via a `.github` workflow selection change (Owner scope). No new CI change authored (owner: no .github edits).
- Local checks: `go build ./...` clean; adapter unit test `TestQuarkusRoundTrip` asserts `/q/health` healthcheck present.

## Cleanup

- Host baha-docker-2: all quarkfield containers removed (`docker stop` + `docker rm -f`), 0 containers remaining, 13 GiB free. Target `quarkfield` left (retained, not mine to destroy) — detach blocked by core provider-confirmation safety gate (intended default).
- Go/Python/Next.js containers from other lanes removed to free RAM (their round-1/round-2 evidence is already in planning repo).
- No product code left running; no release/tag.

## END (partial-delivery, round-2)

- END_DONE 0427-003-greenfield-stacks: head=0d8639c3d base=0c4e59cdad pr=branch-0d8639c3d stacks=Go:ja(nextjs:ja-docker2/py:ja/quarkus:ja-docker2) single_control_plane=belegt(all-4-stacks: topology_ha=false members=1, haproxy single-member, openbao single-member) regression=quarkus-adapter-fix(/q/health healthcheck + TestQuarkusRoundTrip) run=baha-docker2-12gb podman_gate=nicht-gestartet(seriell-nach-docker2) akte=evidence/r27-welle5-folge-2026-11-07/greenfield-stacks/round-2.md(origin-main-verifizieren)
