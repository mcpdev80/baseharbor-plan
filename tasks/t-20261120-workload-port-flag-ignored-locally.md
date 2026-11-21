---
id: t-20261120-workload-port-flag-ignored-locally
card_number: "0428-199"
card_short_title: "workload-port ignored locally"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w1625-pr1723-0428-199-workloadport
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-199 · workload-port ignored locally
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1723]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44788134959"]
created: 2026-11-20
---

- [ ] t-20261120-workload-port-flag-ignored-locally · workload-port ignored locally #task #release/v0-4-28 #status/review #view/review #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w1625-pr1723-0428-199-workloadport  
    **PR:** [baseharbor#1723](https://github.com/mcpdev80/baseharbor/pull/1723)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44788134959)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w1625-pr1723-0428-199-workloadport  
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


## Codex closeout continuation — 2026-11-21

- Took over this started wait card under the Owner's instruction to complete every wait card except #1615. PR #1723 remains OPEN, non-draft, based on `develop`, exact head `26755fc1edfbde534986b501197a92f38842a0c1`; the current `develop` head is `40cb28c758b02960356434b630086a341ebe1738` and is an ancestor of the PR head.
- On that exact PR head, `go test ./cmd/baha -run '^(TestParseRuntimeUpOptions|TestExtractLocalWorkloadPorts|TestAppApplyRunAcceptsWorkloadPort|TestUpRunAcceptsWorkloadPort)$' -count=1` passed (`ok .../cmd/baha 0.009s`). The two distinct command-surface regressions are present and executed: `TestAppApplyRunAcceptsWorkloadPort` and `TestUpRunAcceptsWorkloadPort`. Source trace confirms `app apply` and `up` attach the parsed map to context and the existing deployment path persists and applies it.
- The exact hosted run [44788134959](https://github.com/mcpdev80/baseharbor/actions/runs/44788134959) is terminal FAILURE on the same head. All four owning CLI shards executed and failed on the shared operator gate; the verbatim representative failure is `main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.` The card's own regressions pass locally; exact hosted success, fresh current-head CI, and merge remain outstanding behind 0428-198/#1726 and its active 0428-204 entry-point prerequisite. No PR base or other owner's work was changed.

222

ab heute von einer FRISCHEN Lane uebernommen (sitz ornith 2/2, session ffe7611b, lane-name-Regel erfuellt; die alte Lane pr1625-0428-065-export ist nach gelieferter H-V21-Akte und abgelieferter PR-census-triage freigegeben). Grund fuer die Lane: das census-triage hat gezeigt, dass PR #1723 nicht in develop enthalten ist (back=21 front=2, mergeable=MERGEABLE, mergeStateStatus=BEHIND) - kein superseded-Fall, also hop-noetig und danach ordinary merge. Auftrag erteilt (mission sha256 6c9d783517f7): fetch + reset --hard FETCH_HEAD vor jeder Aenderung (Lehre aus dem heutigen false-contamination-Befund), additiver merge-commit hop auf develop 42da7128e72, rev-list --count HEAD..42da7128e72 = 0, author==committer==0428-199-workloadport, dann der exakte head run selbst bis terminal plus der NAME des CI-jobs, der cmd/baha/workload_port_local_regression_test.go ausfuehrt (nicht skipped); findet sich kein job, ist das ein Befund mit file:line an mich, .github/scripts bleiben gesperrt. Akte: evidence/r28-welle5-2026-11-22/workload-port-hop/hop-develop-42da7128.md.

kandidat ist EXAKT und VOLLSTAENDIG GEGENUEBER develop: head 5c063c7f278 (additiver merge-commit hop, parents 71ac9ba51b7 + 42da7128e72, back=0 gemessen, akte evidence/r28-welle5-2026-11-22/workload-port-hop/hop-develop-42da7128.md). der exakte run 44961493271 ist completed/failure, und die zwei failed jobs sind NICHT der inhalt dieser karte: job 137021826770 'PR · Selected Runtime (atomic/docker/data-capabilities) / Executed docker · data-capabilities' bricht mit '::error::candidate ref is not a branch/tag; resolve to a ref or a full commit SHA before the gate checkout' plus 'Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate…)', job 137023663943 'PR Selected Checks' faellt daraufhin. VON MIR GEGENPRUEFT als VORBESTEHEND: der alte run 44934975722 auf 71ac9ba51b7 faellt auf denselben jobs 136939892711 und 136941785609 mit derselben ::error-zeile (18:21Z) - der hop hat nichts veraendert, und das diff-touches-liste dieser karte beruehrt die consent-/footprint-pfade nicht. IHR EIGENER NACHWEIS: die cli-3-shard hat workload_port_local_regression_test.go ausgefuehrt (CI-Aufnahmepflicht erfuellt), go unit/build/vet/gofmt gruen. DER AEUSSERE DEFEKT ist auf karte 0428-226 (t-20261122-impact-consent-after-preview-contract) gegossen, zusammen mit dem consent-falle aus #1627; .github/scripts bleiben owner-scope, keine ausnahme erteilt.
