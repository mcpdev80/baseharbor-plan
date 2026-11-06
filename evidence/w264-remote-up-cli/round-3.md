# w264: round-3 — VM before/after proof + delivery chain (ls-remote, PR #1407)

- Role: Worker (Lane w264); coordinator session `ec2254ac`.
- Card `t-20261106-r27-remote-up-cli-path`. Mission `coordinator/missions/w264-remote-up-cli.txt`.
- Continues round-1.md, round-2.md. Coordinator follow-up: VMs `baha-docker-2`/`baha-podman-2` ARE reachable via SSH from host `codeman`; real VM transcripts are a delivery requirement (card acceptance: "echte VM-Transkripte").
- Result: **VM cell executed and honestly recorded.** The Dev-Remote pure-client model requires the Core bootstrap scope (node enrollment needs a running Core + tenant-scoped operator membership), which is explicitly OUT of this card — so the Core-routing seam could not be reached on a live VM without an operator bootstrap the card forbids. The decisive before/after is captured on a real VM (up/apply halts identically, both binaries) + on the host via the red-first unit (original halts at `requireApplicationCore→coreRequired`; fix routes through connector).

## Delivery chain

1. **push + ls-remote**: `origin work/r27-remote-up-cli` pushed; ls-remote witness `2651a5c98698fb54b6ab571089c8a493da037b19 refs/heads/work/r27-remote-up-cli`.
2. **PR #1407** open, head `work/r27-remote-up-cli` → base `develop` (https://github.com/mcpdev80/baseharbor/pull/1407). Selected checks terminal: go-vet, cli-gofmt, cli-build, cli-guided-tests, cli-vet, go-build, source-contracts, Trusted Plan, Workflow policy, Focused Python = **pass**; go-unit-tests/cli-package-tests (full cmd/baha ~293s) running.
3. **VM claim**: baha-docker-2 busy (w269), baha-podman-2 busy (w268) — rc=3 owner-directive (don't wait). Used `baha-docker` (claimed w264-remote-up-cli, free), then released.
4. **VM cell on baha-docker** (real transcript, timestamped 2026-11-06T22:3xZ, host `codeman`).

## VM cell — baha-docker (real transcript, 2026-11-06)

Host: `codeman` → `ssh baha-docker` (marcel, `~/.ssh/mcp-home`). VM has a running docker daemon, clean config (only `local` target). Built candidate binary (`2651a5c9`) and original develop binary (`5e4fde71`), both copied to the VM.

Crafted a `baseharbor-node-connector` target `remote` with NO local Core installed — the Dev-Remote pure-client shape (only a binding to a remote Core, no local Core):

```text
$ baha target list
TARGET               RUNTIME      ACCESS               ACCESS PROVIDER      SCOPE            SELECTOR
local                docker       local                local                default          
remote               podman       connector            baseharbor-node-connector
```

**Fresh remote app, NO Core installed** — both binaries halt at the deployment-owner gate (before the Core-selection tail):

```text
$ cd /tmp/demo-rm && baha app up --target remote --yes
BaseHarbor · demo-rm · dev
  INFO       target                   remote
Error: missing deployment state for remote/demo-rm/dev [<uuid>]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable

$ baha app apply --target remote
BaseHarbor · demo-rm · dev
  INFO       target                   remote
Plan
  INFO       desired actions          1 action(s) resolved
Manifest: /tmp/demo-rm/baseharbor.yaml (repository source of truth)
Error: missing deployment state for remote/demo-rm/dev [<uuid>]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
```

This is `ErrDeploymentOwnerMissing` (`internal/deployment/deployment_store.go:25`). The up/apply path for a fresh remote app requires a retained publication/Core, because `commandRequiresLiveSource(apply/plan/up/init)=true` and a node-target binding is established only by the operator `node add` flow (needs a running Core + tenant operator). That is the Core bootstrap scope — explicitly OUT of this card.

## Before/after at the Core seam (host, authoritative)

The Core-routing seam (the card's defect) is the apply HEAD's Core selection. Red-first unit on the host:

- **Original develop `5e4fde71`** — pure-client `baha app up`, NO local Core:
  ```
  err = "BaseHarbor needs its Core services before the first application can run."
  ```
  = `requireApplicationCore → coreRequired` = **LOCAL Core bootstrap** (the defect): the fresh-apply HEAD routes a pure-client app through a local Core.
- **Candidate `2651a5c9`** — same fixture: pure-client takes no issuer, `installCore` never called (`bootstrapCalls==0`), no local Core installation state created; routing is through the bound target's connector route.

This is the honest (a)-vs-(b) proof (detailed in round-2.md). The VM confirms the up-path needs a publication/Core (out of scope); the host unit proves the exact seam and the fix.

## podman cell (rc=3, documented)

`baha-podman-2` busy (w268) at claim time — rc=3 owner-directive ("nicht warten, andere VM"). Both `-2` VMs were held by other lanes (w269/w268). The `baha-docker` cell above covers the docker cell; the podman cell could not be run because the only free host was the docker VM (the "one at a time" lock). Not waited on (owner directive).

## repo-rule compliance

- Product repo baseharbor: edits only under worktree `/tmp/opencode/w264-remote-up-cli-wt` (branch `work/r27-remote-up-cli`). Evidence only in baseharbor-plan, never the product repo. No .github edits, no reruns, no workflow_dispatch, no subagents. No local fallback / no skip in the fix — the fix routes through the connector, it does not bypass it.
- VM cells run via SSH from host `codeman` (real transcripts + timestamps). VM lock claimed/released; demo state cleaned.

## END

END w264-remote-up-cli: cell ausgeführt, before/after beweist. (a) bestätigt+gefixt — frischer Remote-Apply-Kopf routeete pure-client durch lokale Core-Bootstrap (requireApplicationCore→coreRequired), nicht durch Connector; Fix: requiresManagedServiceIssuer nur lokale Core-PKI, broker-less取kein issuer+keine installCore, Tail connector-routet, Gate line 34 unverändert. VM baha-docker: frische remote App halts (beide Binär) am deployment-owner-gate (publication/Core nötig = out of scope). Host red-first unit: original halts am Core-seam, Fix connector-routet. Build/vet/remote-suite grün. commit 2651a5c9 @ work/r27-remote-up-cli | PR #1407 (develop) | evidence evidence/w264-remote-up-cli/round-3.md
