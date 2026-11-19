---
id: t-20261118-enrollment-two-phase-boundary-doc
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w99-0428-115 r5 (codeman baf201fd)
kanban_status: closed
card_number: 0428-115
card_short_title: document the enrollment
kanban_title: 0428-115 · document the enrollment
prs: [mcpdev80/baseharbor#1685]
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1685", "https://github.com/mcpdev80/baseharbor/actions/runs/44408281995", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44446194802", "https://github.com/mcpdev80/baseharbor/actions/runs/44457842661", "https://github.com/mcpdev80/baseharbor/actions/runs/44460025899", "https://github.com/mcpdev80/baseharbor/commit/deeeb64778b3f6109d3a8e49fd652d490901e89c", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685-final.md"]
blocker: ""
resolution: accepted

---
# t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary

- [x] t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w99-0428-115 r5 (codeman baf201fd)  
    **PR:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1685), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44408281995), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44446194802), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44457842661), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/44460025899), [proof 8](https://github.com/mcpdev80/baseharbor/commit/deeeb64778b3f6109d3a8e49fd652d490901e89c), [proof 9](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685-final.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w99-0428-115 r5 (codeman baf201fd)  
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

r4-lane dispatched (freie 088er-spur uebernommen): zwei sprach-punkte gem. comment 6999389290, kein inhalt

r4 END akzeptiert: 'verpflichtet' durch 'eigene Transaktion abgeschlossen' ersetzt (commit-semantik korrekt), guard-satz direkt; head bb685c2dc monoton (ec592fd385 ancestor), run 44457842661 SUCCESS terminal + PR Selected Checks, akte fix-3.md (3f57ae39). vierte rueckweisung abgearbeitet — Routing an CODEX final

Re-reviewed exact head bb685c2d; corrected commit wording now reads clearly, but EN/DE guard descriptions are asymmetric because DE omits the consumed-grant predicate in RecordIssued. Exact-head run 44457842661 terminal success. Review comment 6999847636; no merge pending narrow DE correction and refreshed exact-head evidence.

r5 dispatched: DE-absatz nennt nur einen der beiden identity-schreib-schutze (serial-is-null) — consumed_at IS NOT NULL fehlt gegen EN (comment 6999847636, korrigierter end-text). eine stelle, kein inhaltsschritt. head bb685c2dc anerkannt bis darauf

r5 END akzeptiert: DE nennt jetzt beide identity-write guards (consumed_at IS NOT NULL wortgetreu nach EN), head 50f87cfb8 (ec592fd385 ancestor, ohne hopf/force), docs-check + run 44460025899 TERMINAL SUCCESS, akte fix-4.md (853f5f0f). Ready fuer CODEX-REVIEW final

CODEX-REVIEW ACCEPT at 50f87cfb8dd6e87913044f96cc0204af1423b61c; merged normally as deeeb64778b3f6109d3a8e49fd652d490901e89c. Exact-head CI 44460025899 SUCCESS; docs checks, selected unit jobs, native Keycloak/Core Docker+Podman, and PR Selected Checks pass. Develop ec592fd38 was an ancestor; no force or protection bypass.
