# Evidence: t-20261018-r27-local-registry — Round 1, Welle 5

- Lane: w224 (coord-welle5), Model: Ornith-Laptop, Coord: 841e7734
- Repo: mcpdev80/baseharbor
- Card file: coordinator/missions/w224-local-registry.txt
- Task contract: baseharbor-plan/tasks/t-20261018-r27-local-registry.md
- Outcome: for topologies that actually need a shared endpoint, explicitly opt into one existing OCI Distribution-compatible registry implementation; unreachable endpoint => explicit error, never a silent fallback.

## PLAN

- Read mission w224-local-registry.txt fully and the task contract
- Establish develop baseline (fail-closed, byte-for-byte) and build+test green
- Owner scope decision: env-gated opt-in (BASEHARBOR_ORG_OCI_ENABLED default OFF)
- Cut fresh branch work/r27-local-registry from origin/develop (base SHA proven as ancestor)
- Implement opt-in in internal/orgconfig only (write-set sacred, no app_broker)
- Negative/positive cells: no-optin==today baseline, opt-in uses shared endpoint, unreachable fails closed (no silent fallback), 1395c trap guard
- Local gates: race-20, build/vet/gofmt, observe hosted TERMINAL at head myself
- PR against develop, draft->ready myself, no .github/ / no workflow_dispatch
- ls-remote head==branch literal name-only; evidence to origin/main (ls-tree) before END
- END to coordinator 841e7734; any compose down (ps-witness)

## Owner / scope decision

- 2026-11-06 KOORD option1 (env-gated opt-in) confirmed by Owner: (a) card demands a REAL opt-in, the tests-only variant undersells the card text; (b) predecessor card registry-access 1395c solved the same fail with the ENV mechanism (BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE precedent) — consistency beats taste, and that same mechanism is already accepted. Write-set stays internal/orgconfig only; orgconfig files remain sacred; no cmd/baha/app_broker* touch. Decision line recorded here.

## Base attestation

- Base ref: origin/develop
- Base SHA cut from: ea656d1fcfce9ee14145a8dfaffb9e993fd29497
- This SHA must be an ancestor of my first commit (proven via git merge-base --is-ancestor in akte).

## Deliverables mapping

- (1) ohne konfiguration bleibt verhalten EXAKT wie heute: default ENV OFF => byte-for-byte identical cell vs develop-baseline
- (2) mit opt-in: pull-pfad nutzt den geteilten endpoint: ENV ON => resolveOCI uses configured shared endpoint cell
- (3) unreicherbarer endpoint => expliziter fehler, KEIN stiller fallback: fail-closed unreachable cell; 1395c trap (mutable fallback on denied) proven RED mutant
- (4) red-first auf develop: baseline red before change, green after

## Gates status

- race-20: pending
- build/vet/gofmt: pending
- hosted TERMINAL at head: pending (observed by me, RUN-ID recorded)
- PR vs develop draft->ready: pending
- ls-remote head==branch literal: pending
- evidence to origin/main (ls-tree) before END: pending

## END payload

- END an 841e7734: "END_DONE w224-local-registry: head=<sha10> ohne-optin=<baseline-zelle> mit-optin=<zelle> unreachable=<kein-fallback+mutante> redfirst=<belegt> lauf=<id TERMINAL> lsremote=<sha10> | <Satz>"

## Lane status

- active (in progress)

## CI observation (observed by me, run 42183319266)

- Head watched at head: PR #1401 vs origin/develop, run 42183319266, head sha e520ed6096d7dc47ae3e2e7d004bf15483b0e56a
- Green gates at head: PR Trusted Plan=success, Workflow policy=success, Source format=success, go-vet=success, Focused Python=success, go-build=success, and my package:
  - `ok  github.com/mcpdev80/baseharbor/internal/orgconfig  0.117s` (hosted CI log, run 42183319266)
- My cells pass locally with Owner-required race: `go test -race -count=10 ./internal/orgconfig/...` = ok (TMPDIR=/dev/shm; the race build exceeds the /tmp/opencode tmpfs quota)
- Red at head is FOREIGN and out of scope:
  - Verbatim CI log line (run 42183319266, job PR · Validation · go-unit-tests):
    `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.01s)`
    `    source_snapshot_test.go:309: change-during-read MutationAcked never fired on the mutated path within the local bound`
    `FAIL  github.com/mcpdev80/baseharbor/internal/development  7.528s`
  - Package: `internal/development` (round-7/8 snapshot flake work on develop HEAD, commits d0e0bdc6/667b0b0d/02988718 — a DIFFERENT lane, NOT my card)
  - My additive diff carries ONLY orgconfig files (name-only vs my commit parent e520ed60~1):
    internal/orgconfig/orgconfig_test.go, internal/orgconfig/source.go, internal/orgconfig/source_oci.go, internal/orgconfig/source_oci_test.go
  - `internal/development/source_snapshot.go` is unchanged from origin/develop (foreign to my card; forbidden cross-read); working tree == develop HEAD there

## Decision note (Owner 2026-11-06)

- KOORD variante 2: my write-set (orgconfig) is green, proven by me. The red is ANKANNED FOREIGN (a different lane's round-7/8 snapshot flake) and already has its own running fix — round-8 CI is executing on the same commit (d0e0bdc6) as a separate lane. I must NOT touch `internal/development`.
- Decision line KOORDvariante2:Owner KOORD 2026-11-06 variante 2 (PR offen lassen, session beim Landing freigeben, neuanlauf beim naechsten Trigger gegen refreshes develop-kopf), praeszedenz w207/w211 (identischer fall, identische anwort).
- Action: PR #1401 stays OPEN vs the current develop HEAD. Session will be freed at the landing event (round-8 lands), not by me — the card note carries the trigger. After round-8 lands, ONE green run at the current head with the next trigger.

## Next trigger

- Wait for the foreign round-8 CI to land on develop; then re-run CI at the current develop head with PR #1401 and record the green result before END.

## Branch head witness

- Branch: work/r27-local-registry
- Branch head (local + remote ls-remote, real): e520ed6096d7dc47ae3e2e7d004bf15483b0e56a
- Base origin/develop ea656d1fcfce9ee14145a8dfaffb9e993fd29497 is an ancestor (git merge-base --is-ancestor rc=0)
- PR #1401 against develop, READY, head e520ed6096, no foreign commit carried in (git log shows only my commit on top of the develop base)

