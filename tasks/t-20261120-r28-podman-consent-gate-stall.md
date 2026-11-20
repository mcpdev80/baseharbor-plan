---
id: t-20261120-r28-podman-consent-gate-stall
card_number: "0428-187"
card_short_title: "consent gate stalls cell"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w187-0428-187-consentgate
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-187 · consent gate stalls cell
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/consent-gate-stall/round-1.md"]
---

- [x] t-20261120-r28-podman-consent-gate-stall · The podman data-capabilities cell stalls the guided wizard at the candidate-consent step #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** w187-0428-187-consentgate  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/consent-gate-stall/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w187-0428-187-consentgate  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found in the PR #1715 run (2026-11-20, run 44743111417, job 136312259900)

The card under review (#1715, destroy-side registry cleanup) changed neither the wizard nor the consent path, but its
`PR · Selected Runtime (atomic/podman/data-capabilities)` cell is red. Log witnesses, verbatim from the job log:

```
13:25:24  Existing consent authority requires 2 confirmation(s)
13:27:13  Error: wizard cancelled without changes
13:36:01  Error: record deployment before mutation: candidate submission requires an explicit operator
13:36:01  RuntimeError: new-edit-new-sql-remove exceeded no-output timeout: elapsed=241s no-output=180
13:32:30  demo-data-capabilities       FAIL
```

The scenario reaches the candidate step, is told two confirmations are required, cancels, and the harness keeps waiting
until the 180-second no-output limit kills the cell. `PR Selected Checks` therefore aggregates red while every Go unit
shard is green. Whether the same stall reproduces on a clean develop head is NOT yet proven: the job only materialises in
PR-selected runs, so no develop push carries a comparable cell (measured: develop runs 44728573148 / 44726527868 list no
data-capabilities job).

## Acceptance

1. Reproduce the guided scenario `new-edit-new-sql-remove` on the current develop head, in the same cell
   (podman, data-capabilities). State in the evidence whether the stall predates this release.
2. Fix the fixture/flow so the consent path is satisfiable in CI: either the fixture supplies the second confirmation the
   product asks for, or the product stops asking twice where the flow can only answer once - one of the two, with the
   chosen side named at file:line.
3. Keep the fail-closed behaviour: never make the cell green by removing the consent requirement or by auto-approving a
   candidate submission in the runner (AGENTS 3.8: the check input must not be set by the party being checked).
4. Bound the wait: the scenario must finish inside the 180-second no-output window; a silent wizard must surface its
   prompt instead of hanging. Record the new duration in the evidence.

## Boundaries

scripts/ci-greenfield-apply.py, the guided-wizard command path in cmd/baha and the data-capabilities fixture. The
destroy-side files of 0428-184 (internal/application/shared_backends_resources_runtime.go, internal/observability/registry.go)
and the identity witness of 0428-078 are NOT part of this card. No .github/** (owner scope): if the workflow needs a
consent env, report the needed change as a finding with file:line instead of editing it (AGENTS 5.3).

gefunden im PR #1715, run 44743111417 job 136312259900: 'Existing consent authority requires 2 confirmation(s)' -> 'Error: wizard cancelled without changes' -> 'candidate submission requires an explicit operator' -> 'new-edit-new-sql-remove exceeded no-output timeout: elapsed=241s no-output=180' -> demo-data-capabilities FAIL. base-drift ist NICHT bewiesen: der job erscheint nur in PR-selected-laeufen, kein develop-push traegt ihn (gemessen runs 44728573148 / 44726527868 ohne diesen job).

ARBEITET JETZT: session 425eb851 (ornith-kanal, model worker-ornith1.5, spawn verifiziert), worktree aus develop f5ce95afce1c. auftrag: scenario new-edit-new-sql-remove in der podman data-capabilities-zelle reproduzieren, dann ENTSCHEIDEN welche seite fixt (fixture liefert die zweite bestaetigung ODER produkt verlangt nicht twice), kein auto-approve im runner (§3.8), dentro 180s no-output. schreibfeld: scripts/ci-greenfield-apply.py + guided-wizard in cmd/baha + fixture; die dateien von 0428-184 (#1715) und 0428-183 (#1714) sind in der mission ausdruecklich verschlossen.

BEFUNDOLOS fuer den core-pfad, von lane 425eb851 fern belegt: die zelle stallte am demo-seitigen matched-catalog (CurrentConsent auf baseharbor-demo pin f23b6e09), der den core-text 'Warning: confirm the displayed outcome without a working alternative.' (internal/application/provider_change_consent.go:37) nicht akzeptierte -> stufe 1/2 blieb ohne antwort -> no-output timeout. der owner hat den pin auf adda7599cb5b79689702f6a63a5ca802179df967 gehoben; run 44748241522 attempt 2 zeigt an #1715 0 failures. der core-text ist bereits feld-abgedeckt durch cmd/baha/provider_change_confirmation_test.go:81, kein produktaenderung noetig. karte wird DROPPED, nicht accepted: sie hat nichts geliefert ausser dem nachweis, dass die ursache ausserhalb dieses repositories lag.
