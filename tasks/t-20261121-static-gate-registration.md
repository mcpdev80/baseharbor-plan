---
depends_on: [t-20261122-gate-catalog-missing-app-broker-component]
id: t-20261121-static-gate-registration
card_number: "0428-208"
card_short_title: "0428-208 static gate"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: ffe7611b (owner-delegierter release-only katalog-fix auf #1746, target cace61802) / Coordinator
kanban_status: active
kanban_lane: active
kanban_summary: Run the existing scripts/ci-fast-check.sh as its own static gate in the v0.4.28 Pre-Release Suite. Preserve every existing…
kanban_title: 0428-208 · 0428-208 static gate
priority: high
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1746, mcpdev80/baseharbor#1771, mcpdev80/baseharbor#1774, mcpdev80/baseharbor#1782, mcpdev80/baseharbor#1761]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44997978036", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/gate-census-1746.md"]
---

- [ ] t-20261121-static-gate-registration · 0428-208 wire `scripts/ci-fast-check.sh` as a standalone v0.4.28 Release Suite gate #task #release/v0-4-28 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ffe7611b (owner-delegierter release-only katalog-fix auf \#1746, target cace61802) / Coordinator · **Priority:** high  
    **PR:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774), [baseharbor#1782](https://github.com/mcpdev80/baseharbor/pull/1782), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44997978036), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/gate-census-1746.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-gate-catalog-missing-app-broker-component](t-20261122-gate-catalog-missing-app-broker-component.md)  
**Owner:** ffe7611b (owner-delegierter release-only katalog-fix auf #1746, target cace61802) / Coordinator  
**Priority:** high  
**PRs:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774), [baseharbor#1782](https://github.com/mcpdev80/baseharbor/pull/1782), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
**Source:** 
<!-- /generated:links -->

## Goal

Run the existing `scripts/ci-fast-check.sh` as its own static gate in the v0.4.28 Pre-Release Suite. Preserve every existing Release Suite gate selection, keep the normal CI workflow unchanged, and make an uncatalogued gate fail with its exact ID and one clear repair action.

## Owner scope authorization

Owner 2026-11-21: zweckgebundene Freigabe für pre-release-runtime-suite.yml und seine Dispatch-Verkabelung für 0428-205. Alle anderen .github-Änderungen bleiben gesperrt und dürfen nur über eine neue Owner-Freigabe erfolgen.

## Scope

- In scope: the `atomic/static/ci-fast-check` catalog entry; planner selection and static executor dispatch; the `pre-release-runtime-suite.yml` setup, catalog validation and dispatch case; reuse fingerprint mapping for the gate's source and selector tests; focused regression coverage.
- Out of scope: every other `.github` file, especially `.github/workflows/ci.yml`; any new PR-CI route or second test list; unrelated gate or release changes.
- `ci-fast-check` executes `scripts/ci-fast-check.sh` directly. Its existing test command remains the only list of checks for this gate.

## Acceptance

1. One PR contains the catalog, dispatch and two proofs. The Coordinator and Release Owner confirm the bounded scope and results in that PR.
2. Positive proof: the existing static Release Suite jobs and the new standalone gate run on the same exact candidate; all selected jobs pass and the previous matrix selection remains intact.
3. Negative proof: an intentionally uncatalogued static gate exits nonzero, identifies its exact catalog ID, and gives the direct registration action.
4. The new gate is selected only by the Release Suite. `.github/workflows/ci.yml` is unchanged, and feature PRs do not execute `ci-fast-check` through the normal CI path.
5. 0428-205 stays blocked until the two proofs are demonstrated live. Do not mark it accepted from catalog or card state alone.

## Test binding

| Attribute | Value |
| --- | --- |
| Gate | `atomic/static/ci-fast-check` |
| Executed source | `bash scripts/ci-fast-check.sh` |
| Trigger | v0.4.28 Pre-Release Suite static gate matrix |
| Negative case | `atomic/static/test-uncatalogued` in an isolated catalog fixture; selection exits nonzero with actionable ID |

## Stop and report

- Do not change `.github/workflows/ci.yml` or any other `.github` file.
- Do not merge unless both requested proofs and both PR confirmations are present.
- 0428-205 remains blocked pending the live gate demonstration.

## Handoff

- Candidate branch: `lane-0428-208-static-release-gate`; PR [#1746](https://github.com/mcpdev80/baseharbor/pull/1746).
- Candidate head after hop to current develop: `0a710235a4134ed45b53303a8faad44cbf4119d5`.
- Local exact workflow-policy comparison passed; `bash scripts/ci-fast-check.sh` passed (307 tests); uncatalogued-gate negative case exits nonzero and prints its ID plus the repair action.
- Coordinator scope confirmation is recorded in [PR comment](https://github.com/mcpdev80/baseharbor/pull/1746#issuecomment-7060850641). Exact-head PR run `44891832834` is pending. Hosted positive Release Suite proof and Release Owner confirmation remain pending. The exact v0.4.28 Demo pin file is absent on current `develop`; no older pin was substituted.

Owner hat 0428-208 selbst umgesetzt als PR #1746 (head a1e95e7ebc5d, base develop, 9 dateien, ci.yml NICHT im diff). Von mir gemessen am head: release-requirements.json traegt genau eine zeile atomic/static/ci-fast-check mit required_for v0.4.28, jobs static_gates, dependencies core, und die releases-liste enthaelt v0.4.28. Der withdrawn kandidat fab709a45 (required_for leer) bleibt unveroeffentlicht. Scope- und plan-bestaetigung als kommentar auf dem PR hinterlegt. Offen: head ist kein nachkomme von develop, der exakt-current-base aggregate braucht einen hop.

review -> wait: two foreign prerequisites (0428-223 operator-auth, 0428-225 mcp contract) proven from the failing run's own logs

Der gueltige statische nachweis ist gefuehrt und FEHLGESCHLAGEN: run 44987381250 (workflow ref lane-0428-208-static-release-gate, head eb2e471a8fd, ls-remote bewiesen) fuehrt ALLE sechs statischen gates aus, kein skip: agent 137102052113 SUCCESS, ci-fast-check 137102089845 SUCCESS, init 137102052110 FAILURE, config-matrix 137102052148 FAILURE, mcp 137102052168 FAILURE, shell-ux 137102052189 FAILURE. Die vier failures sind zwei bekannte, messbare ursachen: MCP contract mismatch (unexpected baseharbor.app.perses.disable/enable/remove/status, karte 0428-232, produktseite internal/machine/contract.go:205-208) und 'Managed-environment machine operations require an authenticated BaseHarbor operator' in init/config-matrix/shell-ux (karte 0428-231, operator-auth-helper). Der vorherige run 44986797647 war mit ref=develop angestossen und zaehlt nicht als beleg (akte static-suite-1746-valid-run.md, plan 036aa0175).

ihr hop ist gelandet: head e455302f1a8 auf base 52a3c5446f4, exact run 44997978036 SUCCESS/0 failed, coreless-lifecycle aggregate docker 137136393453 und podman 137136509792 SUCCESS. 'Exact full Pre-Release' ist SKIPPED und mergeable_state BEHIND, weil develop schon acc34323968 ist. Die vier 'require an authenticated BaseHarbor operator'-zellen haengen am helper (PR 1761, noch DRAFT). Rechenreihenfolge nach vorgabe des owners: 1761 hop -> ready -> review -> merge, dann 1746 hop und der exakte static-beweis.

hop ist gelandet und der exact run 44997978036 ist SUCCESS/0 failed (100 jobs, 32 success, 68 skipped) am head e455302f1a8. Die vier directive-gates (init, config-matrix, shell-ux, mcp) erscheinen nicht mehr als eigene jobs, weil die CI-matrix umgebaut ist - kein required check ist rot. 'PR . Selected Runtime' 137133121874 und 'PR . Native matrix' 137133096184 sind SKIPPED: base-zeiger-verzug (ci.yml:495, karte 0428-235), kein kandidatfehler und auch nicht der helper-blocker. RUECKSTAND: develop ist acc34323968, dieser head zeigt auf 52a3c5446f4, also ist vor der abnahme ein weiterer hop noetig - nach dem 1761-merge, damit der helper in der base liegt und die statischen zellen ihn ziehen koennen. Zusatz: die karte 0428-233 (tmpdir) hat KEINEN PR und ihre position liegt unveraendert in develop (cmd/baha/test_operator_context_test.go:112-116) - der Auftrag dafuer ist jetzt erneut bei ihrer lane, mit zustands-zeile zuerst.

CENSUS IST DA und faellt in die mittelste kategori (b): die vier gates init/config-matrix/shell-ux/mcp sind WEITER HINTERLEGT - scripts/release-requirements.json :13-29 fuehrt sie, das gehostete job-muster 'Static . matrix.gate' existiert - aber sie liefen an diesem kandidat NICHT als exact-head-pruefung, und zwar aus zwei gruenden: (1) der diff traegt keine quelle, die auf einen der vier gates gemappt ist (kein source-component im diff), (2) der planned von seinem alt-base 52a3c5446f4, develop ist acc34323968 (0428-235). Damit ist meine vorige formulierung 'kein required check rot, alles gut' ZU LANG: die deckung ist echt, aber der exact-head-beleg fehlt, solange der base-zeiger nicht h uepft. Ein eigener befund im census: eine source-registration-luecke auf .github/workflows/pre-release.yml (owner-scope) - ich trage sie als zeile in 0428-235 nach. Naechster schritt: ein weiterer hop auf develop nach dem 1761-merge, dann sind die vier gates am exact head sichtbar.

GRUND KORRIGIERT, MESSE STATT ERINNERUNG: mein bisheriger wart-grund ('wartet auf den helper aus PR 1761') ist WIDERLEGT - das diff von PR 1746 gegen develop 8629450ef3c beruehrt KEIN operatorauth-symbol (suche im diff: operatorauth / test_operator / RequireAuthenticatedOperator = keine treffer) und hat NULL pfade in cmd/baha, internal/capability oder internal/controlplaneruntime. Der diff besteht aus .github/workflows/pre-release.yml, .github/workflows/pre-release-runtime-suite.yml, CHANGELOG.md, docs/releases/v0.4.28.demo-ref und neun dateien in scripts/ (pr-gate-plan.py, pre-release-check-plan.py, pre-release-runtime-impact.json, release-requirements.json, ci-fast-check.sh, drei test_*.py). rueckstand nur 29 commits, 12 dateien. DAMIT: kein broker-bezug, kein helper-bezug - aber der diff liegtkomplett in RESERVIERTEN gebieten, die keine lane aendern darf. Abgabe-entscheidung ist ihre: entweder sie ziehen den hop selbst, oder sie geben eine benannte lane mit ausdruecklicher ausnahme fuers .github/-und scripts/-gebiet. Der previous exact durchgang 44997978036 war SUCCESS/0 failed am head e455302f1a8 (base damals 52a3c5446f4).

ROLLE KLARGESTELLT: diese karte bleibt der ZENSUS-verweis auf die gate-deckung von PR 1746 (verdict (b), akte gate-census-1746.md, plan 03e506a81). INTEGRATION und hop laufen ueber karte 0428-205 auf der lane ffe7611b - beide eroeffnen denselben PR, aber nur 0428-205 fuehrt ihn. Mein bisheriger wart-grund 'wartet auf den helper aus PR 1761' ist WIDERLEGT: der diff hat keinen verweis auf operatorauth/test_operator und keine broker-pfade (gemessen). Neuer grund: reservierte gebiete (scripts/** und .github/**), deren korrektur innerhalb der 205-vollmacht ist aktiv, plus der fisch-einschraenkungs-punkt des eigentuemers.

PROMOTED per owner-delegation: die freigegebene katalog-release-only korrektur (ledger 1291 rezept) wird von sitz ffe auf branch lane-0428-208-static-release-gate (head 208ee7607) ausgefuehrt. .github-bestand des PRs bleibt owner-eigentumunangetastet; kein PR-CI-neu-route. PR-aggregat muss nach fix weg-gruen; full release gate bleibt owner-aktion.
