---
id: t-20261120-r28-packages-shard-develop-regression
card_number: "0428-202"
card_short_title: "packages shard red on develop"
type: bug
areas: [ci, observability]
release: v0.4.28
version: ""
parent: ""
owner: w207-0428-202-lokifix
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-202 · packages shard red on develop
priority: ""
depends_on: [t-20261114-r28-cli2-env-policy]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1732]
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/packages-shard-develop-regression/round-2.md", "https://github.com/mcpdev80/baseharbor/pull/1734"]
created: 2026-11-20
superseded_by: t-20261121-loki-verify-probe

---

- [x] t-20261120-r28-packages-shard-develop-regression · packages shard red on develop #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w207-0428-202-lokifix  
    **PR:** [baseharbor#1732](https://github.com/mcpdev80/baseharbor/pull/1732)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/packages-shard-develop-regression/round-2.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1734)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md)  
**Required by:** [t-20261120-r28-valkey-dashboard-unavailable-only](t-20261120-r28-valkey-dashboard-unavailable-only.md)  
**Owner:** w207-0428-202-lokifix  
**Priority:** not set  
**PRs:** [baseharbor#1732](https://github.com/mcpdev80/baseharbor/pull/1732)  
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

URSACHE GEFUNDEN, UND SIE IST NICHT DER OWNER-RAIL: DIE packages-ZELLE FAELLT, WEIL EIN TEST-FIXTURE DAS CLIENT-PAR NICHT SCHREIBT. MESSEN (read-only, develop 40cb28c758b0 + job 136526893242 des runs 44805066271): woertlich 'load Loki service access identity: stat /tmp/<test>/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory', an genau drei tests (internal/logs/loki_test.go:522 / 586 / 633, familie TestPersesLokiDatasourceMultiSource). der helper materializeLokiServiceAccessPKI (internal/logs/loki_test.go:434) schreibt ca.pem + server-cert.pem + server-key.pem, ABER KEIN client-cert.pem; die consumer-seite lokiDatasourceHTTPClient (internal/logs/loki_datasource.go:394-401) verlangt ueber serviceaccess.ExistingTLSMaterial genau diese datei, und das producer-layout internal/serviceaccess/pki.go:485 benennt 'client-cert.pem'. serviceaccess.Resolve laeuft durch (sonst kaeme ein anderer fehler) - also ist 2af892e4e ('fail closed without explicit environment policy') HIER NICHT die ursache, und die owner-entscheidung, die ich als blocker bat, ist NICHT noetig. SITZ: w207-0428-202-lokifix (ornith), schreib-umfang internal/logs/*_test.go, internal/serviceaccess/** verschlossen. beweis-pflicht: kleinster gate 'go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource' vorher/nachher + ein terminaler hosted run am exakten head.

TIP-BELEG VON SITZ w210 (read-only, akte evidence/r28-welle4-2026-11-20/bare-develop-gate/round-1.md, plan-main 446e5f29): am nackten develop 40cb28c758b02960356434b630086a341ebe1738 sind die Loki-MultiSource-zellen ROT, woertlich 'stat .../service-access/pki/client-cert.pem: no such file or directory' (internal/logs/loki_test.go:522/:586); am stand 96f2ae11a sind sie GRUEN; valkey-/tempo-zellen sind KEINE tip-regression. LESART: der fixture half bisher, weil die consumer-seite das client-material nicht verlangte; seit #1594/policy.go (2af892e4e) verlangt sie es. DARUM bleibt die entscheidungsfrage am owner, aber der einzige weg innerhalb eines erlaubten write-sets ist der test-seitige. AUFTRAG AN w207: ihren helper-diff AUF DEN TIP setzen (worktree auf 40cb28c758b0 + diff on top) und den kleinen gate dort fahren: gruen = kandidat, rot = STOP + MELDEN (policy-seite = owner-rail, kein griff). SITZ w210 ist nach akzeptierter akte freigegeben (cleanup hielt, weil ihr status beim freigabe-versuch noch busy war - naechster tick).

ABGELIEFERT UND VON MIR GEMESSEN: PR #1732 head bddb27e6251e, base develop 40cb28c758b0, draft=false, 1 datei (internal/logs/loki_test.go), branch == refs/pull/1732/head. 'PR · Go unit · packages' = SUCCESS am exakten head (job 136574098983, run 44818799733) - die Loki-MultiSource-zellen sind damit auch am develop-tip behoben, der fixture schreibt jetzt das fehlende mTLS client-paar. cli-0..3 bleiben failure = feld-gate 0428-198 (nicht ihr scope, rail ist verschlossen). DARUM wait statt review: eine required-zelle fehlt noch, und sie haengt an genau einem anderen fall. TRIGGER FUER DIE naechste KANTE: 0428-198 gruen im feld -> dann ist dieser kandidat mit einem laufenden exact-head-CI abnehmbar.

SUPERSEDED BY 0428-212 (read-only comparison by w231, akte evidence/r28-welle4-2026-11-21/1732-vs-1734-supersede/round-1.md, plan main be9321bf). MEASURED BY COORDINATOR, not only by the lane: both PRs touch exactly one file, internal/logs/loki_test.go (#1732 +32/-0, #1734 +299/-109); #1732 head bddb27e62 is NOT an ancestor of #1734 head 75770bd2d, so the supersession is content-based; the same three client-cert fixture sites appear in both (1732 :554/:621/:665 = 1734 :671/:751/:813) and #1734 carries materializeLokiServiceAccessPKI plus named subtests materializedPKIFailsClosed*; packages is green at both exact heads. No open PR bases on lane-0428-202-lokifix, so closing #1732 breaks no stack (Owner-Direktive 2026-10-28: superseded PR closed after proof, without merge). This card's analysis of which sites and which gate is what made #1734 possible.
