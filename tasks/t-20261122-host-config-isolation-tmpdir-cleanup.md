---
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/workload-port-0428-199/hop-develop-c463edf8-w17235.md", "https://github.com/mcpdev80/baseharbor/pull/1762", "https://github.com/mcpdev80/baseharbor/actions/runs/45001383922", "https://github.com/mcpdev80/baseharbor/commit/cace61802dcd34e59e4e7edebfd67f57dd3b07ad"]
id: t-20261122-host-config-isolation-tmpdir-cleanup
card_number: "0428-233"
card_short_title: "host config isolation tmpdir"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Owner (#1762 owner-merge) / Coordinator
tags: [#task, #release/v0.4-28]
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-233 · host config isolation tmpdir
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1725, mcpdev80/baseharbor#1762]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
---

- [x] t-20261122-host-config-isolation-tmpdir-cleanup · CLI: release the per-test host config isolation directory #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Owner (\#1762 owner-merge) / Coordinator  
    **PR:** [baseharbor#1725](https://github.com/mcpdev80/baseharbor/pull/1725), [baseharbor#1762](https://github.com/mcpdev80/baseharbor/pull/1762)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/workload-port-0428-199/hop-develop-c463edf8-w17235.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1762), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45001383922), [proof 4](https://github.com/mcpdev80/baseharbor/commit/cace61802dcd34e59e4e7edebfd67f57dd3b07ad)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Owner (#1762 owner-merge) / Coordinator  
**Priority:** not set  
**PRs:** [baseharbor#1725](https://github.com/mcpdev80/baseharbor/pull/1725), [baseharbor#1762](https://github.com/mcpdev80/baseharbor/pull/1762)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Why this card exists

Independent review of PR #1750 at exact head `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99` found a real cleanup
omission: `cmd/baha/test_operator_context_test.go:112-121` creates the per-test host configuration isolation
directory (`hostConfigIsolationDir`) without registering a removal, so every data-capabilities test that takes the
operator path leaves a directory behind under the system temporary root. It does not fail a gate and it does not
mask the 14-test root cause that card 0428-223 fixes, which is why it was not folded into that PR.

## Contract

- Give the isolation directory a lifecycle: create it under the test's own `t.TempDir()` root, or register
  `t.Cleanup` for the directory it creates today. Either shape is acceptable; the observable requirement is that a
  run of `TestOperatorContext*` leaves no new entry in the temporary root.
- Keep the operator selection behaviour of card 0428-223 unchanged; this is a lifecycle change only.
- The regression must be hosted: a gate that executes the affected `cmd/baha` test sources has to select the test
  after card 0428-228 lands its mapping, so the leak cannot return silently.

Abgesetzt auf den freien sitz: mission sha 15d11b3ec9a9, lifecycle-festigung der hostConfigIsolationDir in cmd/baha/test_operator_context_test.go:112-121, regression im gehosteten data-capabilities-gate (beide engines) nach PR 1755/1756.

inhaltsteil ist auf der lane fertig gemeldet (tmpdir-freigabe im host-config-isolation-test); PR steht noch aus, weil derselbe sitz zuerst den PR-1645-hop ausfuehrt. Kein merge, keine abnahme: es fehlt der gehostete beleg am eigenen head.

 Review-des-eigentmers ist umgesetzt: neuer head 6937d0609c7 auf lane-0428-233-tmpdir-cleanup (ls-remote belegt). Der beleg-test faehrt hostConfigIsolationDir jetzt in einem verschachtelten t.Run und prft die abwesenheit des verzeichnisses NACH rueckkehr des t.Run - das beweist das registrierte Cleanup; das manuelle os.RemoveAll ist weg. Exact run 45001093525 war in_progress, der neue run wird abgewartet. Korrektur zu meiner eigenen hinweis zuvor: die karte hatte doch einen PR (#1762), die aussage 'kein PR' galt dem stand vor ihrem push.

URSACHE KORRIGIERT, drei messungen statt einer vermutung: die nativen reihen in 45001383922 (docker 137144959891, podman 137144959836) scheitern an der ABWEISUNG von 'baha app footprint show -o json' (command-not-in-managed-workload-set / operator-auth-pfad); der 'missing --confirm-candidate'-verweis (cmd/baha/app_candidate_consent.go:148-158, errConsentRequiredForCandidateSubmission als *cli.UsageError, exit 2) erscheint nur DOWNSTREAM im halb abgebrochenen test. Meine broker-503-lesart fuer DIESEN kandidat war FALSCH und ist zurueckgezogen; fuer PR 1761 gilt sie weiter (von mir selbst gemessen: broker readiness timeout 2m03s in TestApplicationCapabilityLifecycleExistingCore/secrets). EIGENTUER-ENTSCHEID uebernommen: beide commits bleiben (adccce73 cleanup + 6937d060 assertion), endgueltiger diff = eine datei, kein rebase/amend/force. HALTEAUFTRAG an die lane: kein hop, kein durchgang bis 1753 gemergt ist; dann ein additiver hop auf die dann aktuelle develop-spitze und EIN durchgang mit den zwei nativen job-ids als zeugen. Erste/simple merge-ziel ist 1762 in genau dieser reihenfolge.

URSACHE KORRIGIERT, drei messungen statt einer vermutung: die nativen reihen in 45001383922 (docker 137144959891, podman 137144959836) scheitern an der ABWEISUNG von 'baha app footprint show -o json' (command-not-in-managed-workload-set / operator-auth-pfad); der 'missing --confirm-candidate'-verweis (cmd/baha/app_candidate_consent.go:148-158, usageError exit 2) erscheint nur DOWNSTREAM im halb abgebrochenen test. Meine broker-503-lesart fuer DIESEN kandidat war falsch und ist zurueckgezogen; fuer PR 1761 gilt sie weiter (selbst gemessen: broker readiness timeout 2m03s in TestApplicationCapabilityLifecycleExistingCore/secrets). EIGENTUEMER-ENTSCHEID uebernommen: beide commits bleiben (adccce73 cleanup + 6937d060 assertion), endgueltiger diff eine datei, kein rebase/amend/force. HALTEAUFTRAG an die lane: kein hop, kein durchgang bis PR 1753 gemergt ist; dann ein additiver hop auf die dann aktuelle develop-spitze und EIN durchgang mit den zwei nativen job-ids als zeugen. 1762 ist damit das erste simple merge-ziel in genau dieser reihenfolge.

0428-233 CLOSED: #1762 von owner gemergt als cace61802 ('test: prove host config tempdir cleanup'), exact-head run 45077628402 SUCCESS am head 3fe0754a5 (ls-remote+run fernbelegt; owner update-branch, gemergt 23:5x). Die im feld mitgefuehrte #1725 ist PR der karte 0428-201 (dort separat verfolgt, kein einfluss auf diesen abschluss). develop=cace61802.
