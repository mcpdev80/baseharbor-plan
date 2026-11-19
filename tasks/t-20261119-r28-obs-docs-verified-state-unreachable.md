---
id: t-20261119-r28-obs-docs-verified-state-unreachable
kanban_title: 0428-148 · docs verified-state fehlt
card_number: "0428-148"
card_short_title: "docs verified-state fehlt"
type: task
areas: [docs, observability]
release: v0.4.28
version: ""
parent: ""
owner: Codex team (current thread)
kanban_status: closed
kanban_lane: closed
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1703]
sources: []
source_note: "hunt 0428-147 (akte evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md, haupt d667cce4)"
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md", "https://github.com/mcpdev80/baseharbor/commit/223cb97a9d652a4672257cabbadf12e2b41ed9cd"]
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md"
  - "https://github.com/mcpdev80/baseharbor/commit/dd7deadc665f4bb8dc6ceddae94a2835635a3e75"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44594850148"
resolution: accepted
created: 2026-11-19
---

- [x] t-20261119-r28-obs-docs-verified-state-unreachable · doku verspricht perses-zustand 'verified' #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/docs #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current thread)  
    **PR:** [baseharbor#1703](https://github.com/mcpdev80/baseharbor/pull/1703)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/223cb97a9d652a4672257cabbadf12e2b41ed9cd), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md), [proof 4](https://github.com/mcpdev80/baseharbor/commit/dd7deadc665f4bb8dc6ceddae94a2835635a3e75), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44594850148)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex team (current thread)  
**Priority:** not set  
**PRs:** [baseharbor#1703](https://github.com/mcpdev80/baseharbor/pull/1703)  
**Source:** 
<!-- /generated:links -->

## Goal

Die observability-how-to fuehrt fuer 'perses status' einen zustand 'verified', den der status-pfad in diesem release nicht zurueckgeben kann. Fund aus einer echten runtime-zelle (baha-docker, develop 558dc42d0), nicht aus doku-lektuere. Ziel: die doku nennt nur zustaende, die der code erzeugen kann — oder der code erzeugt sie nachweislich.

## Scope

- In scope: `docs/how-to/observability.md` and `docs/de/how-to/observability.md`, plus the status path `cmd/baha app perses status` and its existing production-path tests.
- Zur einordnung: der wert 'verified' existiert im code an anderer stelle (cmd/baha/app_evidence.go:168/:178) fuer einen ANDEREN kontext — das ist nicht derselbe zustandsraum.
- Out of scope: die 'Verification=none'-vertragsfrage (karte 0428-143, beim owner). Hier geht es ausschliesslich um ein versprochenes ergebnis in der doku.

## Acceptance

- Jede in der doku genannte status-zeile ist im code erzielbar, mit bedingungen-satz.
- Eine regression belegt den gelieferten zustand am echten pfad; bleibt 'verified' in der doku, muss ein test den wert erzeugen.
- documentation-audit laeuft am exaktkopf; selektiert die zuordnung docs/** nicht, ist das der bekannte befuend zu scripts/pr-gate-plan.py (karte 0428-144, owner-scope) — dann in der akte belegen statt 'gruen' behaupten.

## Required checks

- **Modified features:** doku-check (documentation-audit) + die status-regression der observability-pfade.
- **CI integration:** the existing status regression is `cmd/baha::TestBahaStatusPersesConfiguredUnverifiedPositive` and `cmd/baha::TestBahaStatusPersesNotConfiguredWhenUnselected`; both run in package `cmd/baha` under the mapped Go unit gate. This card adds no new code test or CI mapping.

## Handoff

- PR [#1703](https://github.com/mcpdev80/baseharbor/pull/1703) is open and ready for review at exact head `dd7deadc665f4bb8dc6ceddae94a2835635a3e75` on current develop base `558dc42d0c8c9d798fcdf5938be2ea14e432b754`. EN/DE how-to now state that invalid/unavailable or unselected Perses is `not_configured`, selected Perses with valid pin is `configured_unverified`, and `verified` is unreachable without a health probe. Existing production-path tests pass with `go test ./cmd/baha -run 'TestBahaStatusPersesConfiguredUnverifiedPositive|TestBahaStatusPersesNotConfiguredWhenUnselected' -count=1`; `bash scripts/documentation-audit.sh`, `python3 scripts/documentation-language-audit.py`, `python3 scripts/check_docs_locale_parity.py`, and `git diff --check` also pass locally. Exact hosted run [44594850148](https://github.com/mcpdev80/baseharbor/actions/runs/44594850148) is still pending. Do not accept or merge until required selected checks complete at this head.

hunt-fund 0428-147 -> karte -> implemented von der ANDEREN WELT (claim a15d83f2, PR #1703, squash 223cb97a9 auf develop 223cb97a9, blob-identitaet 2/2 gegen head dd7deadc6). Inhalt gemessen: die doku nennt jetzt genau configured_unverified (selektiert, gueltiger pin) und not_configured (nicht selektiert / pin ungueltig / unavailable) und sagt ausd uecklich 'verified is not currently reachable' — deckt sich mit capability.PersesStatusNow (internal/capability/perses.go:245, selected bool) und den tests cmd/baha/app_perses_cli_test.go:434/:448. KEIN CODEX-URTEIL in unserer welt: merge durch die andere welt, base-distanz docs-only => keine meiner lanen schuldet neue laeufe. ZWEIFEL am owner: grenzfall 'board = codeman, merge = andere welt'.
