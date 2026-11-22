---
id: t-20261120-gate-catalog-ci-fast-check
card_number: "0428-205"
card_short_title: "Gate catalog: ci-fast-check"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: 0428-223-testctx
kanban_status: wait
kanban_lane: wait
kanban_summary: "Register scripts/ci-fast-check.sh as a real v0.4.28 Pre-Release static gate, with the full catalog/dispatcher wiring and…"
kanban_title: "0428-205 · Gate catalog: ci-fast-check"
priority: normal
depends_on: [t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1746]
sources: []
blocker: ""
wait_reason: "kopf exakt (48f0cb1e44d, ahead=5 behind=0) und PR-CI 44973953752 completed/success. der vom PR-koerper verlangte zielgerichtete volle static-lauf ist angestossen: workflow_dispatch auf 'Release . Pre-Release Validation' (workflow 362658451), run 44975747939 in_progress am exakten head, only_gates = atomic/static/agent, atomic/static/ci-fast-check, atomic/static/config-matrix, atomic/static/init, atomic/static/lifecycle, atomic/static/mcp, atomic/static/shell-ux; tag=v0.4.28, ref=48f0cb1e44d…, demo_ref=5d1cf312e18d06915db35c340bebe4e3d4f39d45. der pin kommt aus docs/releases/v0.4.28.demo-ref DES kandidaten, die gate-ids aus scripts/release-requirements.json - keine lane hat ihren pruefeingang selbst gesetzt (AGENTS 3.8). vorher: 44944570763 war am ALTEN head 9ddcde356e9 rot. offen: terminales resultat von 44975747939, Release-Owner-Bestaetigung, unabhaengiges verdict"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44943804395", "https://github.com/mcpdev80/baseharbor/actions/runs/44944570763", "https://github.com/mcpdev80/baseharbor/pull/1746"]
---

- [ ] t-20261120-gate-catalog-ci-fast-check · 0428-205 · Wire ci-fast-check into the release gate catalog #task #release/v0-4-28 #status/wait #view/wait #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-223-testctx · **Priority:** normal  
    **PR:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746)  
    **Waiting:** kopf exakt (48f0cb1e44d, ahead=5 behind=0) und PR-CI 44973953752 completed/success. der vom PR-koerper verlangte zielgerichtete volle static-lauf ist angestossen: workflow\_dispatch auf 'Release . Pre-Release Validation' (workflow 362658451…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44943804395), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44944570763), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1746)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Owner:** 0428-223-testctx  
**Priority:** normal  
**PRs:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746)  
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
