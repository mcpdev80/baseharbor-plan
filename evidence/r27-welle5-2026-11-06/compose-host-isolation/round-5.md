# w241 — Compose Host Isolation (r27) — round-5 combined

- Coordinator: 841e7734 | Lane: w241 | Card: t-20261105-r27-compose-host-isolation
- Candidate: PR #1383, branch work/r27-compose-isolation, head **88d725e4b19f343e5b8deaff503677a5e89fe7f8**
- PR: https://github.com/mcpdev80/baseharbor/pull/1383 (open, base develop, no review yet)

## PLAN-Checkliste (owner 4.4)

- Mission read; PR #1383 / branch head 88d725e verified via ls-remote + GitHub API
- InCI isolation scope isolated (3 files; unrelated removals are branch-history, not this lane's write-set)
- Local build + vet clean; testbinary built for VM copy (no go on VMs)
- Causal mutant probe: baseline GREEN, fail-closed removed RED (guard is causal)
- Docker half on baha-docker (166): 2/2 isolated cells, torn down, factory-clean
- Podman half on baha-podman-2 (107): 2/2 isolated cells, torn down, factory-clean
- Evidence written, committed to origin/main, pushed

## ISOLATIONSZELLEN — HOST-SERIELL (owner: one host per time)

### (1) DOCKER — baha-docker (192.168.6.166)

- vm-lock claim `w241` set before first container start; released after teardown.
- Durable `bh-local-shared` stack (taboo) untouched.
- Binary built in session (`CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go test -c -o /tmp/baha-r27.test ./cmd/baha/`), scp to 166 (166 no go).
- Two isolated compose projects brought up **simultaneously**:
  - `docker compose -p w241a-isolate up -d` (cell A)
  - `docker compose -p w241b-isolate up -d` (cell B)
- Image: postgres:17-alpine (18-alpine rejects its own pre-existing data dir as stale).
- Inspect witness (per project — separate network / volume / port):
  | cell | project | network | volume | host port | db |
  |------|---------|---------|--------|-----------|-----|
  | A | w241a-isolate | w241a-isolate_w241a-internal (id ee753ba0) | w241a-isolate_w241a-pgdata (local) | 127.0.0.1:25432->5432 | w241adb |
  | B | w241b-isolate | w241b-isolate_w241b-internal (id b7f6de9c) | w241b-isolate_w241b-pgdata (local) | 127.0.0.1:25433->5432 | w241bdb |
- Cross-cell isolation: w241a cannot DNS-resolve w241b; each DB sees only its own (table count 0 in both); distinct networks/volumes/ports.
- Result: **2/2 GREEN**. Torn down: 0 w241 containers (ps witness), volumes removed, /tmp/w241* removed, lock released.
- Full transcript: evidence/r27-welle5-2026-11-06/compose-host-isolation/round-02-docker-cells.md

### (2) PODMAN — baha-podman-2 (192.168.6.107)

- Claimed after w251 ENDed (107 was empty); vm-lock `w241` set before first start; released after teardown.
- Did NOT touch 148/w243 (owner: no silent move without coordination).
- Two isolated compose projects brought up **simultaneously**:
  - `podman compose -p w241ap up -d` (cell A)
  - `podman compose -p w241bp up -d` (cell B)
- Image: docker.io/library/postgres:17-alpine (podman needs full reference; short name fails).
- Inspect witness (per project — separate network / volume / port):
  | cell | project | network | volume | host port | db |
  |------|---------|---------|--------|-----------|-----|
  | A | w241ap | w241ap_w241a-internal (id e42c6439) | w241ap_w241apgdata (local) | 127.0.0.1:26432->5432 | w241adb |
  | B | w241bp | w241bp_w241b-internal (id c7489bae) | w241bp_w241bpgdata (local) | 127.0.0.1:26433->5432 | w241bdb |
- Cross-cell isolation: distinct network IDs (A≠B), distinct host ports, distinct volumes; w241apost does not DNS-resolve from w241bpost; distinct DBs.
- Result: **2/2 GREEN**. Torn down: 0 w241 containers (ps witness), volumes/networks removed, /tmp/w241* removed, lock released.
- Full transcript: evidence/r27-welle5-2026-11-06/compose-host-isolation/round-03-podman-cells.md

## MUTANTENPROBE (owner: causal, no hand-helpers)

- Guard under test: r27 InCI isolation fail-closed assertion — an unconfigured sentinel target must FAIL `cfg.ResolveTarget`. Dropping it → unconfigured target silently resolves to bootstrap default → isolation leak.
- Probe file cmd/baha/w241_mutant_probe_test.go (transient, created/run/removed; tree clean, HEAD 88d725e).
- Results:
  - Baseline (guard present): `PASS` (GREEN)
  - Mutant (fail-closed assertion removed): `FAIL` — `guard error still present; mutant must silence it` (RED)
- Conclusion: the isolation guard is **causal** — removing the fail-closed check flips the cell GREEN→RED. Non-causal earlier mutant (existence-check only) stayed GREEN and was discarded (owner precedent managed-users act-1397b). No hand-written workaround.
- Full transcript: evidence/r27-welle5-2026-11-06/compose-host-isolation/round-04-mutant.md

## EVIDENCE on origin/main (owner: ls-tree before push)

- Path: evidence/r27-welle5-2026-11-06/compose-host-isolation/round-0{1,2,3,4}-*.md + round-5.md
- Committed on a fresh worktree cut from origin/main, pushed to origin/main.

## REVERSE-CHECKS

- No subagents (owner 2026-11-04): every step run in this session.
- No second PR / no root-checkout / no .github change (mutant only ever a transient probe file, never committed).
- Containers never on the coordinator/session host; only on 166 (docker) and 107 (podman), both brought down to 0 w241 by this lane.
- Caches under /tmp/opencode/w241* only.

## END_STATE

- Both halves green in one round. docker_host=166 (2/2), podman_host=107 (2/2).
- Factory-clean on both hosts (ps witness, locks released, bh-*-shared untouched where present).
- Mutant ROT+GRÜN belegt (causal).
