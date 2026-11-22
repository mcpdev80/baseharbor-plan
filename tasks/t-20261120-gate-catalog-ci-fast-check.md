---
id: t-20261120-gate-catalog-ci-fast-check
card_number: "0428-205"
card_short_title: "Gate catalog: ci-fast-check"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: owner (resolves) / coord
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "Register scripts/ci-fast-check.sh as a real v0.4.28 Pre-Release static gate, with the full catalog/dispatcher wiring and…"
kanban_title: "0428-205 · Gate catalog: ci-fast-check"
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1746, mcpdev80/baseharbor#1761, mcpdev80/baseharbor#1771, mcpdev80/baseharbor#1774]
sources: []
blocker: "#1746 head 887058a6 terminal cancelled 34 fails. Wurzeln sauber getrennt: (i) operator-auth fixture (authenticated BaseHarbor operator) fehlt in core-bootstrap 137227219764/735 + config-matrix/init/shell-ux + reference journeys -> 0428-231/#1771 BREITER pruefen (nicht nur target.create). (ii) ci-fast-check 137227411383 = katalog A fehlt -> #1774 (b90e4ba1 ergaenzt A+C). (iii) mcp perses 'unexpected' = H-V29: KEIN baseharbor-code-defect, RELEASE-VERSION-SKEW (bild vor contract-ops gebaut) -> bild-pin/release-ordnung, nicht code. (iv) light-runtime blob/manifest unknown = eigenes bild-artefakt/registry 0428-249 (nicht auth). (v) target.create = 0428-247 owner/core. Requalifikation erst wenn A+247+237+249+operatorauth(231) adressiert. NICHT qualifiziert."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44943804395", "https://github.com/mcpdev80/baseharbor/actions/runs/44944570763", "https://github.com/mcpdev80/baseharbor/pull/1746"]
---

- [ ] t-20261120-gate-catalog-ci-fast-check · 0428-205 · Wire ci-fast-check into the release gate catalog #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** owner (resolves) / coord · **Priority:** normal  
    **PR:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774)  
    **Blocker:** \#1746 head 887058a6 terminal cancelled 34 fails. Wurzeln sauber getrennt: (i) operator-auth fixture (authenticated BaseHarbor operator) fehlt in core-bootstrap 137227219764/735 + config-matrix/init/shell-ux + reference journeys -\> 0428-231…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44943804395), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44944570763), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1746)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** owner (resolves) / coord  
**Priority:** normal  
**PRs:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-21

Eigentümer-Entscheidung 2026-11-21: Umfang von 0428-208 zweckgebunden erweitert auf den echten Pre-Release-Dispatcher `.github/workflows/pre-release-runtime-suite.yml:264-270` plus die zugehörige Dispatch-Verkabelung; keine anderen .github-Dateien. Vollständige Registrierung behalten (Katalog-Eintrag + Workflow-Eintrag + Gate-Nachweis im selben PR). Umsetzung läuft unter PR #1746; der veraltete Verweis auf den lokalen Kandidaten fa b709a45 ist zu streichen. Zusätzlich freigegeben: ein einzelner zsh-Installationsschritt in pre-release.yml, zweckgebunden für #1746, keine Ausweitung auf den normalen CI-Pfad.

The authorization is retained here as the decision record. The canonical `blocker` field is empty while the card is waiting, as required by the planning schema.

## Goal

Register `scripts/ci-fast-check.sh` as a real v0.4.28 Pre-Release static gate, with the full catalog/dispatcher wiring and exact-head proof in PR #1746.

## Scope

- The catalog entry and its associated dispatch wiring in `.github/workflows/pre-release-runtime-suite.yml`.
- The single zsh installation step in `.github/workflows/pre-release.yml`, solely for PR #1746 and its existing cli-3 source test.
- No change to `.github/workflows/ci.yml` and no other `.github` file.
- Use `scripts/ci-fast-check.sh` as the gate's source of test selection; do not add a second test list.

## Acceptance

- PR #1746 contains the full catalog entry, workflow entry, and gate proof together.
- Positive proof: the existing Release Suite jobs and the new gate run unchanged and pass on the same exact PR head.
- Negative proof: an intentionally uncatalogued test makes the gate exit nonzero on the PR candidate; the message names the missing catalog ID and the one corrective action.
- Coordinator and Release Owner confirmations are recorded on PR #1746.
- Keep this card in Wait until all acceptance evidence is present; do not mark it accepted based on the isolated gate result alone.

## Current handoff — 2026-11-22

- PR [#1746](https://github.com/mcpdev80/baseharbor/pull/1746), exact head `9ddcde356e9ed452ddbf00440ab8189add586d3e`.
- PR CI run [#44942308935](https://github.com/mcpdev80/baseharbor/actions/runs/44942308935): SUCCESS.
- New standalone `ci-fast-check` gate [#44943804395](https://github.com/mcpdev80/baseharbor/actions/runs/44943804395): SUCCESS on that exact head.
- Full Pre-Release run [#44944570763](https://github.com/mcpdev80/baseharbor/actions/runs/44944570763): FAILURE; existing static gates `shell-ux`, `init`, `config-matrix` and `mcp` failed. This does not satisfy the positive proof for the full suite.
- The uncatalogued-gate negative regression is part of `scripts/ci-fast-check.sh`; the exact-head Release Suite gate run #44943804395 executed that script successfully on this same candidate. The standalone run therefore covers the negative selector test at the current head; the full-suite positive proof remains incomplete.
- The local unpublished candidate `fab709a45` is withdrawn and is not an acceptance candidate.
- Scope review: the current `pre-release.yml` diff installs both `zsh` and `fish` in one cli-3 setup step. The Owner authorized a single zsh installation step; Coordinator must confirm that the fish addition is already covered by that authorization or narrow it before merge. `ci.yml` remains unchanged.

EIGENTUER-ENTSCHEID UMGESETZT: der additive hop/recheck ist aktiv auf einer worker-lane (ffe7611b, frei nach ihrem halte-auftrag zu 1762) INNERHALBST der bestehenden vollmacht, ohne neue .github-vollmacht. ABHAENGIGKEIT ERLEDIGT UND UMGEZOGEN, gemessen: die karte zeigte depends_on auf t-20261120-r28-cli-shard-operator-env (0428-198); 0428-198 ist closed/superseded durch t-20261121-develop-full-suite-red (0428-223), und 0428-223 ist closed mit resolution accepted. Ihre wart-war damit GEOEFFNET - depends_on steht jetzt auf der acceptierten karte (plan bf5403c6c). ZWEITER PUNKT, von ihm verlangt: in .github/workflows/pre-release.yml steht im diff 'sudo apt-get install --no-install-recommends -y zsh fish' plus zwei echo-zeilen; die karte deckt NUR EINEN zsh-schritt, fisch ist nicht genannt - die lane muss die zeile auf zsh einschraenken ODER mit datei:zeile eine bestehende autorisierung belegen, sonst nichts. rueckstand 29 commits, additiver hop auf develop 8629450ef3c, danach EIN durchgang mit den vier static-job-ids (config-matrix, shell-ux, mcp, init) als zeugen - skipped ist kein beleg. HINWEIS INTEGRATION: karte 0428-208 eroeffnet denselben PR 1746; 0428-205 ist die INTEGRATIONS-karte, 0428-208 bleibt der zensus-verweis (gate-deckung), damit niemand zwei schreiber annimmt.

cli-3-failure 45027607903 = workflow-ref-Fehler (main statt kandidat), nicht #1746. Berichtigter Durchgang 45028181619 (ref lane-0428-208, workflow-head 887058a6) aktiv. target.create auth weiterhin separater, ungeklaerter blocker.
