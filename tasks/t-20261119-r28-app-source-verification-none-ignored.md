---
id: t-20261119-r28-app-source-verification-none-ignored
kanban_title: 0428-143 · Verification=none is ignored
card_number: "0428-143"
type: bug
areas: [metrics, observability]
release: v0.4.28
version: ""
parent: ""
owner: w203-0428-143-vernone
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/blob/fac01c77276ca2bf1e20cd0b7334bda5dd43e353/internal/metrics/prometheus_verify.go"
resolution: ""
created: 2026-11-19
card_short_title: Verification=none is ignored
---

- [ ] t-20261119-r28-app-source-verification-none-ignored · Verifier: Verification=none is ignored for application-class metrics sources #task #release/v0-4-28 #status/active #view/active #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w203-0428-143-vernone  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/fac01c77276ca2bf1e20cd0b7334bda5dd43e353/internal/metrics/prometheus_verify.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w203-0428-143-vernone  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this exists

0428-123 (metrics registration load-bearing) reviewed the app-class append path on develop and the
reviewer reported an asymmetry in the verifier. The coordinator re-read the code on develop and
confirmed it. No lane claim is involved; the finding predates 0428-123.

## Witnessed code state (develop fac01c77276ca2bf1e20cd0b7334bda5dd43e353)

- `internal/metrics/prometheus_verify.go:153` - app sources are listed with the environment threaded
  through: `applicationSources, err = observability.ListApplicationMetrics(placement, allowedApplications, m.Environment)`
- `internal/metrics/prometheus_verify.go:174` - application loop: `for _, source := range applicationSources {`
  followed by `waitForMetricsSource(ctx, client, endpoint, query, source.ID, "application", queryProvider)`.
  This loop has **no** `if source.Verification == capability.ObservabilityVerifyNone { continue }` guard.
- `internal/metrics/prometheus_verify.go:185` - provider loop **does** carry exactly that guard.
- `internal/capability/integration_contract.go:37` defines `ObservabilityVerificationMode` and its modes.

## Consequence

`ListApplicationMetrics` returns all app-class sources for the placement. A source whose `Verification`
mode is `none` is excluded from exported `ListMetrics` output, yet `verifyProviderSourcesAt` still
waits for it as a required `up` sample. So `Verification=none` does not mean "no verification" for
application-class sources, while it does for provider-class sources.

## Owner decision (2026-11-20)

**Option A selected: uniform semantics.** `Verification=none` means no verifier assertion
for every source class. For metrics, it also means the exporter emits no scrape target.
This avoids timing out on a source the exporter intentionally omitted and removes the
undocumented provider/application asymmetry. Option B (documented asymmetry) is declined.

The application-source verifier guard and regression are prepared on an isolated local
follow-up based on #1693's current head. The contract comment is in
`internal/capability/integration_contract.go`; no remote branch has been updated yet.

- Option A - uniform semantics: `Verification=none` means no verification everywhere; the application
  loop gets the same guard plus a regression test seeding an app-class source with `Verification=none`.
- Option B - documented asymmetry: app-class sources are always load-bearing; the contract text states
  that `Verification` is not a verifier switch for app sources, so nobody reads it as one again.

## Acceptance

- A CI-executed regression test in the package that owns the verifier proves the chosen semantics for
  an application-class source with `Verification=none` (test ID mapped to its gate per the CI intake rule).
- The contract text states the semantics in one place; no silent behaviour change.

The earlier narrowing found that #1693's exporter routing makes the missing application
guard observable: an app source with mode `none` is not exported, but the verifier would
still wait for it. The selected semantics above make the application guard part of the
same contract, not a separate policy.

Independent review of PR #1693 also reproduced a stale emitted target after a same-ID source switches to `VerificationNone` (see [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-independent-review.md)).

## Handoff

Local follow-up commit `82722617` is based on exact #1693 head `270a0de6`. It adds the
application-source `VerificationNone` skip, a regression in
`TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata`, and the contract
comment. `go test ./internal/capability ./internal/metrics -count=1`,
`go vet ./internal/capability ./internal/metrics`, and `git diff --check` pass locally.
The normal `PR · Go unit · packages` shard auto-discovers the test. This commit is not
pushed because #1693 had just been handed off and the Codeman Coordinator is busy; a new
exact-head run must execute after integration. Current follow-up worktree:
`/var/tmp/baseharbor-sweep-1693-hop`, branch `codex/0428-123-verify-none-hop`.


## 2026-11-20 parent PR merged

PR #1693 merged on 2026-11-20 (`head=6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b`, merge commit `6b8188df26a1e263750379a8c5e8255ee4ef740c`); current develop is `36d075fad77fa61ac8c153e979855546589b32c2`. The previous wait reason targeted the old #1693 head. Updated the wait reason to require reconciling the prepared follow-up onto current develop after Coordinator handoff, creating/updating its PR, and running exact-head CI. This task remains Wait; no acceptance claim is made for the follow-up.

ARBEITET JETZT, kante gegen session gemessen (w203-0428-143-vernone, 6d078b3c, ornith, worktree aus develop 40cb28c758b0). GRUND FUER DIE KOMMISSIONIERUNG: Ihre Owner-Entscheidung (option A, einheitliche semantik) ist UMSETZBAR ohne den feld-gate und ohne eine fremde lane - und der auf der karte genannte lokale follow-up 82722617 mit worktree /var/tmp/baseharbor-sweep-1693-hop und branch codex/0428-123-verify-none-hop ist auf DIESEM host nicht mehr vorhanden (gemessen: 'git cat-file -t 82722617' ohne ausgabe, 'ls -d' fehlt, branch nicht in 'git branch -a'). darum NEU-IMPLEMENTIERUNG auf develop statt portieren - das aendert nichts an der entscheidung, nur am weg. UMFANG: dieselbe 'ObservabilityVerifyNone'-wache in die anwendungs-schleife von internal/metrics/prometheus_verify.go, die die provider-schleife schon hat; contract-satz an GENAU EINER stelle (internal/capability/integration_contract.go, definitionsort :37); regression im paket des verifiers, die die CI ausfuehrt (§5.3) und deren aufnahme in den 'PR · Go unit · packages'-shard am laufenden bestaetigt wird, nicht am glauben. DER ZWEITE BEFUND DER KARTE (stale emitted target, wenn eine quelle mit gleichem id auf VerificationNone wechselt) IST NICHT ihr auftrag: falls offen, in der akte als 'offener fund, file:line' notieren + mir melden, ich giess ihn in eine eigene karte (fund->karten-pflicht liegt bei mir, §3.3.5). keine neue konfiguration, kein framework, kein umbau drumherum (§4.2). gateway-faelle = feld-gate 198/202. sitz: ornith, konfliktfrei zu w202 (andere dateien derselben pakete nur bei prometheus_files.go vs prometheus_verify.go - disjunktion gemessen an den karten-write-sets).
