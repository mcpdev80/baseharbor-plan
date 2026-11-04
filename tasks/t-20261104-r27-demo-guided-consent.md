---
id: t-20261104-r27-demo-guided-consent
areas: [demo]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: w85-demo-consent
kanban_status: active
kanban_title: "Demo: guided up supplies candidate consent (feature-detected)"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-demo-guided-consent · Demo: guided up supplies candidate consent (feature-detected) #task #release/v0-4-27 #status/active #view/active #area/demo #kind/task
    <!-- generated:card -->
    **Owner:** w85-demo-consent · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** w85-demo-consent  
**Priority:** high  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

The guided happy path (`baha up` via tests/guided/drive.py) captures the printed confirm-hash and, when the Core binary supports `--confirm-candidate` (feature-detected, e.g. `up --help`), re-runs `up --confirm-candidate <digest>` so the candidate-consent contract completes in one guided flow. Without Core support the path must behave exactly as today (fail-closed refusal, no unknown-flag crash). Rationale: PR #1355's lifecycle gates stay red until this lands; the consent digest is per-command-path, so capture-then-supply is the only harness route (see candidate card consent note).

## Inputs and output

Input: candidate contract's consent surface (`baha up --confirm-candidate`, PR #1355 branch). Output: demo harness change plus executable proof both ways: with-support → READY; feature-detection-false → today's behavior unchanged.

## Dependencies and file ownership

baseharbor-demo tests/guided/drive.py and scripts/acceptance.sh only; no Core files; no new contract or gate semantics. Sequence note: safe to merge before or after PR #1355 thanks to feature detection.

## Required checks

Demo repo focused acceptance/guided tests per baseharbor-demo/AGENTS.md; one hosted core lifecycle smoke after both sides current.

## Standards boundary

No weakening of the consent gate; no env-var auto-confirm (rejected 2026-11-04: second consent surface would dilute the explicit-consent contract).

## Handoff

Raised 2026-11-04 by coordinator from lane w80 dialog 5 (demo location proven: scripts/acceptance.sh + tests/guided/drive.py live in baseharbor-demo; earlier core-side placement note corrected here).


## Review-Rueckruf 2026-11-04 (Luna review-128d, verdict REJECT)
- Gegenprobe hash-stimmig-plus-fremder-fehler loest im Produktionspfad trotzdem einen zweiten Lauf aus
  (fail-closed-Luecke).
- Der Dauer-Test laeuft in einem normalen Demo-Testlauf nicht mit (Entdeckungsproblem).
- Karte zurueck auf active; Korrekturrunde ist vorgemerkt (Mission w109-demo-r5), Lane folgt mit der ersten
  frei werdenden Pool-Kapazitaet. Kandidat bleibt PR #128 head 061be773 bis zum neuen Push.
