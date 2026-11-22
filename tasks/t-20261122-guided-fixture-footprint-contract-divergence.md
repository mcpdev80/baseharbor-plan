---
id: t-20261122-guided-fixture-footprint-contract-divergence
card_number: "0428-241"
card_short_title: "guided fixture drift"
type: bug
areas: [testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord (wartet auf freien sitz)
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-241 · guided fixture drift
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor#1753]
sources: []
blocker: ""
wait_reason: "zugewiesener sitz 03c7350a ist der dokumentierte null-liefer-sitz (rotation = owner-directive ausstehend); die abweichung wartet auf den ersten echt freien arbeitssitz"
resolution: ""
evidence: []
---

- [ ] t-20261122-guided-fixture-footprint-contract-divergence · Selected data-capabilities: native CLI JSON/MCP footprint contracts differ from demo tests/guided/new_edit.py:63 #task #release/v0-4-28 #status/wait #view/wait #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** coord (wartet auf freien sitz) · **Priority:** high  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
    **Waiting:** zugewiesener sitz 03c7350a ist der dokumentierte null-liefer-sitz (rotation = owner-directive ausstehend); die abweichung wartet auf den ersten echt freien arbeitssitz  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coord (wartet auf freien sitz)  
**Priority:** high  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
**Source:** 
<!-- /generated:links -->

## Found by the exact-head CI of PR 1753 (card 0428-227), 2026-11-22

Measured in the selected Docker data-capabilities job 137165839346 of run 45008538769 (terminal FAILURE, head b86440c389b
on develop 8629450ef3c): `app footprint show -o json` IS admitted (the ci-operator log shows the admitted command), yet the
gate still fails with eight `--confirm-candidate` refusals and a contract note that the actual native CLI JSON/MCP footprint
output differs from `tests/guided/new_edit.py:63` in the demo repository.

## Acceptance

1. One canonical footprint contract: the guided demo fixture and the native CLI JSON/MCP output agree on the same fields, or
   the fixture asserts the native output through the shared contract helper (no duplicated expectations).
2. The selected data-capabilities gate for this path runs green with the consent digest supplied by the test harness, and
   the refusal text is proven to be harness behavior, not product behavior.
3. If the fix must touch `cmd/baha/**` product code, that belongs to card 0428-227; this card covers the fixture/contract
   side only.

## Boundaries

baseharbor-demo `tests/guided/new_edit.py` plus the footprint contract assertions in baseharbor `cmd/baha/app_footprint*`
test files. Reserved paths (`.github/**`, `scripts/**`) are excluded.

SITZ BESETZT (03c7350a). Die selected-seite der #1753-rotung hat jetzt eine EIGENE lane: der fixture-/contract-vergleich zwischen 'app footprint show -o json' und baseharbor-demo tests/guided/new_edit.py:63 (job 137165839346: confirm-candidate=8, not_ready=0, unhealthy=0 = reine consent-/fixture-ursache). Auftrag an 03c7350a: abweichung Feld fuer Feld benennen, fix auf der FIXTURE-seite (geteilter contract-helper statt doppelter erwartungen); falls cmd/baha/** produktcode noetig, an 0428-227 rueckmelden statt selbst zu aendern.

SITZ-VORBEHALT, KEIN DOPDEL-VERSAND: dieser auftrag wurde ZWEI mal an 03c7350a zugestellt (rc 0, 'sent'), aber die session liefert nicht (bleibt idle ohne todos) - es ist der dokumentierte NULL-LIEFER-SITZ, dessen rotation an einen owner-directive-wert des eigentuemers gebunden ist, den ich nicht habe. Ich stelle NICHT nochmal ins Leere zu. Die abweichung bleibt gut belegt (selected docker 137165839346: confirm-candidate=8, not_ready=0, unhealthy=0 vs new_edit.py:63) und wartet auf den ERSTEN echt freien arbeitssitz (frei werdend aus den read-only hunts von f0f6c8b4/ffe7611b oder nach #1753-fix auf 0847d100). Kein inhaltlicher blockierer, nur ein kaputter sitz.
