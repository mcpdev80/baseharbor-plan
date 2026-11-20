---
id: t-20261120-r28-packages-shard-develop-regression
card_number: "0428-202"
card_short_title: "packages shard red on develop"
type: bug
areas: [ci, observability]
release: v0.4.28
version: ""
parent: ""
owner: w202-0428-202-pkgshard
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-202 · packages shard red on develop
priority: ""
depends_on: [t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "Waiting for prerequisite 0428-057 / PR #1615 to merge with exact required CI green. The packages shard passed on its previous #1615 head, but the latest fix is now on 8880c9606a7662d0a7f6e5c077d6aa9223e431b7 and exact run 44814082337 is pending. Once #1615 is merged, hop #1714 onto current develop and rerun its exact packages shard to confirm Loki multi-source behavior on the new base. The earlier bisect finding remains recorded below; this is waiting for the owner rail's CI fix, not technically blocked."
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-r28-packages-shard-develop-regression · packages shard red on develop #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w202-0428-202-pkgshard  
    **Waiting:** Waiting for prerequisite 0428-057 / PR \#1615 to merge with exact required CI green. The packages shard passed on its previous \#1615 head, but the latest fix is now on 8880c9606a7662d0a7f6e5c077d6aa9223e431b7 and exact run 44814082337 is pe…  
    **Needs:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Owner:** w202-0428-202-pkgshard  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Finding (measured 2026-11-20, from a lane handoff, re-verified by the coordinator)

The `PR · Go unit · packages` shard is red for every PR that hops onto develop `40cb28c758b0`, and the failing
package is **not** the PR's own code:

- PR #1714 at head `5159192dadeec8335eb401c90fca6614e29048b0`, job `136433151042` (run `44778040176`):
  `--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (`loki_test.go:522` "health must pass
  for a healthy multi-source Loki: perses Loki datasource health client: …"),
  `--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability` (`loki_test.go:586`),
  `--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (`loki_test.go:633` "expected 2 per-source
  queries even on full miss, got 0") and `FAIL github.com/mcpdev80/baseharbor/internal/logs 0.124s`. The PR
  touches only `internal/metrics/**`, which is `ok` in the same log.
- The same PR at the previous base `f5ce95afce1c` had `PR · Go unit · packages` **success** (run `44755545566`),
  so the breakage entered between `f5ce95af` and `40cb28c`.
- Merged in exactly that window: `#1715` (0428-184), `#1716` (0428-182), `#1717` (0428-188), `#1594` (0428-053)
  plus the CI changes `#1721`/`#1722`. `internal/logs` itself last changed on Nov 19 in `c296086ca` (0428-086).
- Cross-check on an unrelated PR: #1645 at head `4abc25ab6772`, job of run `44731562217`, fails the same shard on
  a different package: `FAIL github.com/mcpdev80/baseharbor/internal/identityprovider` (owner field, #1650 - see
  stop rule below), with `internal/metrics` `ok` there.
- Why nobody saw it: develop push runs contain only `Runtime · Docker Core` / `Runtime · Podman Core` (runs
  `44769994971`, `44769994909` = success). The unit shards are PR-only, so a develop-side breakage is invisible
  until a PR hops onto it and pays for it.

## Acceptance

1. `PR · Go unit · packages` runs green at the exact head of any PR whose own diff is inside `internal/metrics` -
   i.e. the `internal/logs` multi-source Loki expectations are satisfied again on develop, with the behaviour, not
   the assertion, fixed.
2. The root cause is named by merge and file: which of `#1715`/`#1716`/`#1717`/`#1594` (or a CI routing change)
   made the per-source selector count become 0, proven by a bisect on develop with the test command and its
   output in the evidence file.
3. The blind spot itself gets a witness line in the evidence file (develop push workflow names vs the PR shard
   names). If closing it needs a `.github/**` change, that need is reported with file:line as a finding for the
   owner - not implemented here.
4. No test is deleted, skipped, or widened to make the shard pass. A green run without the assertion is a second
   defect.

## Boundaries and stops

- Start read-only: build the two revisions and run
  `go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource'` at `f5ce95afce1c` and at `40cb28c758b0`,
  then bisect the merge range.
- Allowed to write: `internal/logs/**` and the producer/selector code those tests exercise
  (`internal/observability/**` read-only first, see below).
- Locked: `internal/metrics/perses_dashboards_valkey.go` and its test (#1714, handoff candidate),
  `internal/observability/registry.go` (0428-078 owner takeover plus 0428-189..194),
  `internal/application/perses_runtime.go` and `internal/metrics/perses_prometheus_datasource.go` (#1684, live
  lane), `internal/identityprovider/**` + `internal/operatorauth/**` + `internal/machine/**` (#1650/#1594/#1615,
  owner is working there). If the root cause sits in a locked file: STOP and report the one line - the owner or
  the owning lane fixes it there.
- `internal/identityprovider` failures inside this shard are NOT this card's work: name them, prove they are a
  different package, and leave them to #1650.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.

ARBEITET JETZT, kante gegen session gemessen (w202-0428-202-pkgshard, laptop): ursache zuerst (bisect f5ce95afce1c -> 40cb28c758b0 mit 'go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource' an beiden enden), dann der kleinste fix am VERHALTEN, dann ein hosted run am exakten head mit 'PR · Go unit · packages' executed/success. die zwei nachmessungen, die den weg weisen: #1714 war am alten base f5ce95af GRUEN in diesem shard (run 44755545566), am neuen 40cb28c ROT an internal/logs (job 136433151042), und ein fremder PR (#1645, run 44731562217) faellt im selben shard an internal/identityprovider - das ist #1650/owner-feld, fuer diese karte nur zu benennen. develop-push faehrt das shard nicht (nur Runtime docker/podman, runs 44769994971/44769994909) - deshalb war der defekt unsichtbar.

DISPOSITION NACH MESSEN: die lane tat genau das richtige - im verschlossenen feld gestoppt + gemeldet statt still repariert. ihre zuordnung an #1684 habe ich NICHT uebernommen, weil die dateienliste von #1684 policy.go nicht fuehrt und der git-log 2af892e4e -> 018b4e58a zeigt, dass die stelle zum #1594/0428-053-rail des owners gehoert. sitz freigegeben, neu besetzt mit 0428-200 (konfliktfrei, andere dateien).
