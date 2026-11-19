---
id: t-20261118-enrollment-two-phase-boundary-doc
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: coord (reserviert)
kanban_status: blocked
card_number: 0428-115
card_short_title: document the enrollment
kanban_title: 0428-115 · document the enrollment
prs: [mcpdev80/baseharbor#1685]
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1685", "https://github.com/mcpdev80/baseharbor/actions/runs/44408281995", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44446194802"]
blocker: "sprach-korrektur r4 reserviert (comment 6999389290: 'Transaktionen verpflichtet werden' commit-semantik-verdreht + schlusssatz unrund). naechster trigger: erster END-freiraum im pool -> neue lane mit mission-r4-stufe"

---
# t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary

- [ ] t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** coord (reserviert)  
    **PR:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
    **Blocker:** sprach-korrektur r4 reserviert (comment 6999389290: 'Transaktionen verpflichtet werden' commit-semantik-verdreht + schlusssatz unrund). naechster trigger: erster END-freiraum im pool -\> neue lane mit mission-r4-stufe  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1685), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44408281995), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44446194802)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coord (reserviert)  
**Priority:** not set  
**PRs:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
**Source:** 
<!-- /generated:links -->

## Goal
Per hunt 914 Befund 2 (medium): `Consume` and `RecordIssued` are two transactions; if the issuer fails in between, the grant sits consumed-but-unissued (recovery relies on the `previous_certificate_serial` clause in connector_enrollment.go:87-90). The finding is a documentation/mental-model gap: make the two-phase boundary, its failure window, and the recovery path explicit in the enrollment docs and a targeted code comment at authority.go.

## Scope
- docs (enrollment/trust-plane section) + one code comment block. NO behavior change, no migration.

## Required checks
- docs build/link checks; no runtime gates.

## Dependencies and file ownership
- Source: hunt 914 Befund 2, evidence/r28-welle4-2026-11-18/hunt-authsurf/befund-1.md.

Codex review comment 6993699816 remains open: German wording translates one-use authorization Grant as Zuschuss/Leugnung/toter Zuschuss. English and Store comment reviewed as accurate; merge blocked on corrected DE text and current-base CI.

reviewer haelt #1685 bei 2039628b: comment 6993699816 gueltig (Grant->'Zuschuss', denial->'Leugnung' = sicherheitssemantik verkannt; Grant bleibt englischer Eigenname, denial='Verweigerung') + 20 commits rueckstaendig hinter develop 40b9901398. mission-115r2-wording-hopf.md RESERVIERT fuer ersten END-freiraum; kein merge vom stale head

r2/r3 END akzeptiert: head 3b9a3f78 mit develop ec532... ec592fd38 integration, hosted run 44446194802 SUCCESS (19 jobs, 0 failures), akte b0276598 (fresh-clone verifiziert). Wort-Geschichte: Zuschuss->Grant (Eigenname), Leugnung->Verweigerung, redundanter DE-absatz getilgt. Routing an CODEX-REVIEW (final)

CODEX-REVIEW REQUEST CHANGES at 3b9a3f78e7e91f1c9a58a564ecbc013540697481; DE two-phase paragraph still has grammatical/technical-wording defects and repeats denial cases. Narrow recipe and exact-head evidence: https://github.com/mcpdev80/baseharbor/pull/1685#issuecomment-6998325146 and evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md.

reviewer haelt bei 3b9a3f78e (comment 6998325146): DE-absatz ungrammatisch + denial-wiederholung + raw identifiers unformatiert. da die r2-lane bereits released war: neue r3-lane auf ersten freiraum dispatched (mission erweitert). kein merge

r3 END akzeptiert: DE-absatz einmal + code-formatierte identifiers, denial-liste getilgt, Grant als terminus behalten; head 711e04c3 (develop ec592fd38 ancestor), beide runs terminal gruen. SELBSTANGABE force-slip beim amend, Vorwaerts-umgekehrt mit ref-restore-protokoll in der akte — gemeldet statt versteckt, bewertet als geheilt. Routing an CODEX (comment 6998325146 abarbeiten)

Exact-head run 44454648646 is green, but semantic DE documentation blocker remains; do not merge until corrected and re-reviewed.

vierte rueckweisung (comment 6999389290): 'Transaktionen verpflichtet werden' = commit-semantik verdreht + unrunder schlusssatz, alles sonst gruen (run 44454648646 SUCCESS). r3-lane war released -> r4-stufe in mission geschrieben, neue lane auf ersten END-freiraum. kein merge
