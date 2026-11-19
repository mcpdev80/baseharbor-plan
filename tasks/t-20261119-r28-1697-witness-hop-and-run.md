---
id: t-20261119-r28-1697-witness-hop-and-run
kanban_title: 0428-153 · 1697 witness hop and run
card_number: "0428-153"
card_short_title: "1697 witness hop and run"
type: task
areas: [ci, docs, governance]
release: v0.4.28
version: ""
parent: ""
owner: Codex team (current thread)
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1697]
sources: []
source_note: "0428-144 implementation PR #1705 is already merged at 28fb427f057499efca705c1b7459e7653bd532a8; only its acceptance witness is outstanding. This witness-only card may run before 0428-144 acceptance because the hosted #1697 result is evidence needed for that acceptance."
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1705"
  - "https://github.com/mcpdev80/baseharbor/pull/1697"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-1697-witness-hop-and-run · nur zeuge produzieren, nichts annehmen #task #release/v0-4-28 #status/active #view/active #area/ci #area/docs #area/governance #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current thread)  
    **PR:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1705), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1697)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex team (current thread)  
**Priority:** not set  
**PRs:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
**Source:** 
<!-- /generated:links -->

## Goal

Fuer karte 0428-144 (PR #1705, merged = 28fb427f) einen gehosteten ZEUGEN produzieren, dass der documentation-audit den neuen docs/internal JSON-pfad tatsaechlich trifft. Der zeuge entsteht auf dem vorhandenen PR #1697 (karte 0428-131), weil dort genau die drei docs/internal/**/*.json-dateien geaendert werden. Diese karte nimmt dafuer NUR einen inhaltlichen stand auf den aktuellen develop und fuehrt einen terminalen exact-head-lauf. Sie UEBERNDERT nichts und MERGT nichts: weder #1697 noch #1705, kein accept, kein statuswechsel an einer anderen karte als dieser.

## Scope

- In scope: PR #1697, zweig wie im PR, drei dateien docs/internal/v0.4.25-destruction-workspace-checkpoint.json, docs/internal/v0.4.25-external-provider-delivery-source-evidence.json, docs/internal/v0.4.25-installation-destruction-runtime-evidence.json (gemessen: 'changed_files=3', base.ref=develop base.sha=1019190d8 = 190 koepfe alt, draft=false, merged=false, state=open, letzter pull_request-lauf am alten kopf 44478473607 success — der alte lauf zaehlt nicht).
- Ausdruecklich NICHT in scope: jede produkt-aenderung, jede aenderung an den drei JSON-inhalten, jede aenderung an scripts/pr-gate-plan.py (das ist 0428-144, gemergt), jede aenderung an .github/** oder scripts/test_pr_* (owner-scope), ein merge, ein rebase auf inhalt, ein accept von 0428-131 oder 0428-144.
- Wenn der hopf INHALTLICHE konflikte mit sich bringt: STOP + melde datei:zeile. Ein zeuge, der durch inhaltsumbau entsteht, ist kein zeuge.

## Acceptance

- Ein pull_request-lauf am NEUEN exakten kopf von #1697 ist TERMINAL, und in ihm ist der documentation-audit (DOC_CHECKS) fuer die drei docs/internal/**/*.json-dateien SICHTBAR ausgefuehrt — job-URL + die zeile, die die dateien nennt. SKIPPED gilt nicht als zeuge (§5.4).
- Der PR #1697 bleibt draft=false und UNMERGED; diese karte fuehrt keinen merge aus und aendert den status von 0428-131 oder 0428-144 nicht.
- Der zeuge wird in das evidence-verzeichnis von 0428-144 geschrieben (baseharbor-plan/evidence/r28-welle4-2026-11-19/prgate-docs-internal-json/witness-1.md): ls-remote-zeile von #1697's zweig, develop-zeitstempel, lauf-id, job-URL, die DOC_CHECKS-zeile wORTLICH, und die feststellung, ob der planner die dateien jetzt als audit-pfad erkennt (gemessen mit 'python3 scripts/pr-gate-plan.py ...').
- Eine zeile in den PR-koerper oder ein kommentar auf #1697, dass der lauf ein witness-lauf fuer 0428-144 ist und damit KEINE annahme von 0428-131 bedeutet (damit niemand spaeter 'gruen = fertig' daraus liest).

## Required checks

- **Modified features:** keine produkt-aenderung; pruefe nur, ob der hopf unveraendert bleibt ('git diff --name-only <kopf>..origin/develop' fuer die drei dateien muss leer sein).
- **CI integration:** EIN pull_request-lauf am exakten kopf bis terminal; die anderen zellen duerfen skipped sein — der documentation-audit NICHT.

## Ownership and dependency correction

The former dependency on 0428-144 represented an acceptance dependency, not an implementation prerequisite: #1705 already merged the selector fix. Requiring 0428-144 to be accepted first would create a cycle because this exact #1697 run is the evidence needed to accept 0428-144. The witness run does not accept or merge either product task.
