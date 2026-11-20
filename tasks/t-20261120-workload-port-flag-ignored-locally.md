---
id: t-20261120-workload-port-flag-ignored-locally
card_number: "0428-199"
card_short_title: "workload-port ignored locally"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w199-0428-199-workloadport
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-199 · workload-port ignored locally
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1723]
sources: []
blocker: ""
wait_reason: "INHALT GELIEFERT, PFLICHTCHECK KANN NICHT DURCHLAUFEN - darum wait, nicht review (dasselbe muster wie 0428-183, damit das board nicht zwei arten fuer einen zustand zeigt): PR #1723, head 26755fc1edfb, parent EXAKT develop 40cb28c758b0, branch == refs/pull/1723/head gemessen, draft=false, 4 dateien; die sieben eigenen workload-port-tests BESTEHEN, der cli-shard-lauf 44788134959 faellt an der vorbestehenden operator-/OIDC-meldung (main_test.go:60). abhaengigkeiten: 0428-198 (sammelstelle, lane arbeitet) und 0428-202 (policy-rail, blocked an 0428-053/#1594 des owners). akte evidence/r28-welle4-2026-11-20/workload-port-local/round-1.md (51 zeilen, 0 checkboxen, gate-zaehler 3, cleanliness). TRIGGER FÜR DIE NÄCHSTE KANTE: ein grüner prueflauf am exakten head, nachdem der gate repariert ist - dann review, dann CODEX-MERGE."
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-workload-port-flag-ignored-locally · workload-port ignored locally #task #release/v0-4-28 #status/wait #view/wait #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w199-0428-199-workloadport  
    **PR:** [baseharbor#1723](https://github.com/mcpdev80/baseharbor/pull/1723)  
    **Waiting:** INHALT GELIEFERT, PFLICHTCHECK KANN NICHT DURCHLAUFEN - darum wait, nicht review (dasselbe muster wie 0428-183, damit das board nicht zwei arten fuer einen zustand zeigt): PR \#1723, head 26755fc1edfb, parent EXAKT develop 40cb28c758b0, bra…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w199-0428-199-workloadport  
**Priority:** not set  
**PRs:** [baseharbor#1723](https://github.com/mcpdev80/baseharbor/pull/1723)  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-V21 (2026-11-20, develop `40cb28c758b0`)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md`, slice "shipped surface".

The usage and long text of `baha app apply` and `baha up` document `--workload-port NAME=PORT` as a persistent
host-port selector for that deployment (`cmd/baha/app_apply.go:42-43`). The flag is only parsed on the remote
management path: `cmd/baha/management_remote_mutation.go:204-210` (`extractRemoteWorkloadPorts`) feeds
`management_http_executor_lifecycle.go:153` (`withRequestedWorkloadPorts`). The local repository path
(`app_input_resolver.go`, `cmd/baha/runtime.go:78` `parseRuntimeUpOptions`,
`resolveApplicationEnvironment`) never sees it.

Measured with the shipped binary built from develop `40cb28c`:

- `baha app apply --workload-port web=9090` -> `Error: baha app apply accepts at most one NAME`
- `baha up --workload-port web=9090` -> `Error: unknown option --workload-port` (exit 2)

So a documented option is either rejected or silently unread on the path most users take.

## Acceptance

1. `--workload-port NAME=PORT` is accepted by `baha app apply` and `baha up` on the **local** path and reaches the
   deployment the same way the remote path delivers it, or the documentation stops promising it. Silent drop is
   not an option either way.
2. A regression test drives the real local apply/up command surface (not the resolver function alone) and fails
   when the flag is ignored, with a distinct failing test per command.
3. One hosted run at the exact head shows the cli shard that owns these files executed (not skipped), 0 failure.
   Run id in the evidence file. If that shard fails with the operator/OIDC message, that is the gate defect
   `0428-198`: record it and report, do not fight it.

## Boundaries and stops

- Allowed to write: `cmd/baha/app_apply.go`, `cmd/baha/runtime.go`, `cmd/baha/app_input_resolver.go` and their
  test files, plus the shared option parsing they call.
- Locked (other owners): `cmd/baha/context_terminal*.go` (#1718, in merge), `internal/observability/registry.go`
  (0428-078 plus 0428-189..194), `internal/metrics/**` (#1714), `internal/serviceaccess/**` and
  `internal/application/perses_runtime.go` (#1684), `internal/identityprovider/**` and
  `internal/operatorauth/**` (#1650, owner), `internal/machine/**` (#1594/#1615 owner stack).
  Needing one of them: stop and report the single line (AGENTS 4.3).
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.

ARBEITET JETZT, kante gegen session gemessen (w199-0428-199-workloadport, ornith, worktree aus develop 40cb28c758b0): der dokumentierte '--workload-port NAME=PORT' soll auf dem LOKALEN apply/up-pfad dasselbe tun wie auf dem remote-pfad, oder die dokumentation darf ihn nicht mehr versprechen - stiller verlust ist in beide richtungen der fehler. regression pro kommando durch die echte kommando-oberflaeche. der beweis kommt durch das kleinste passende gate, weil die cli-shards seit #1594 am kaputten pruefeingang haengen (0428-198, andere lane).
