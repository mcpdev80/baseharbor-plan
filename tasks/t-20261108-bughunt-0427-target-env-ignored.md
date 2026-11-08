---
id: t-20261108-bughunt-0427-target-env-ignored
card_number: "0427-124"
card_short_title: "Target-ENV ohne Wirkung"
type: bug
areas: [lifecycle,compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-124-target-env
kanban_status: review
kanban_lane: review
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-124 · Target-ENV ohne Wirkung"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1443, mcpdev80/baseharbor#1451]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [ ] t-20261108-bughunt-0427-target-env-ignored · 0427-124 · BASEHARBOR_TARGET wird ignoriert #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-124-target-env · **Priority:** high  
    **PR:** [baseharbor#1443](https://github.com/mcpdev80/baseharbor/pull/1443), [baseharbor#1451](https://github.com/mcpdev80/baseharbor/pull/1451)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261108-bughunt-0427-test-bootstrap-leak](t-20261108-bughunt-0427-test-bootstrap-leak.md)  
**Owner:** lane-0427-124-target-env  
**Priority:** high  
**PRs:** [baseharbor#1443](https://github.com/mcpdev80/baseharbor/pull/1443), [baseharbor#1451](https://github.com/mcpdev80/baseharbor/pull/1451)  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-3 docker2 hunt: grep on develop 0fe53052 shows t.Setenv(BASEHARBOR_TARGET) only in *_test.go (app_backup_runtime_fixture_test.go:26 u.a.), no production os.Getenv read; core self-install for isolated targets missing.

## Acceptance

production command paths honour BASEHARBOR_TARGET (or an explicit equivalent) for target selection; an isolated greenfield run on docker-2 completes without touching shared-plane objects; regression proves the env read on the production path.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Übernahme (ChatGPT)

- Owner `owner:chatgpt`, `active` fuer gezielte Diagnose von `BASEHARBOR_TARGET` im echten Core-CLI-Startpfad; keine implizite Target-Umschaltung und keine fremden Ressourcen manipulieren.
- Ergebnis noch offen; Reproduktion und Regression vor Abschluss erforderlich.

## 2026-11-08 Produktionspfad-Diagnose (ChatGPT)

- [PR #1443](https://github.com/mcpdev80/baseharbor/pull/1443), Head `37019b5c1445dda0cc47204e334c734c1e61aff7`: Regression prueft `BASEHARBOR_TARGET` direkt in der produktiven `effectiveTarget()`-Aufloesung und ueber `baha target show --json`, jeweils gegen ein abweichendes persistiertes Target. Exakte CI ausstehend.
- Codeinspektion: `cmd/baha/target.go` liest die Variable; `deployment_record.go` benutzt sie ebenfalls bei der Boot-Target-Auswahl. Der auf der VM beobachtete `ErrDeploymentOwnerMissing` fuer einen isolierten Target **kann** aus der separaten Installationseigentuemer-Pruefung kommen; keine unsichere automatische Core-Ausleihe eingefuehrt.
- Noch offen: isolierter nativer Docker+Podman `baha up --control-plane-only` auf anderem Target ohne Zugriff auf fremde Ressourcen; Karte bleibt `active`.

### 2026-11-08 Repro-Praezisierung (ChatGPT)

Die VM-Akte `evidence/r27-welle5-folge-2026-11-07/vm-bughunt/docker2.md` weist `BASEHARBOR_TARGET=ghisolated baha status` mit `ErrDeploymentOwnerMissing` nach, aber **keinen** exakten `BASEHARBOR_TARGET=ghisolated baha up --control-plane-only`-Aufruf. Der spaetere `baha up`-Befehl ist ohne ENV-Prefix dokumentiert; daher ist ein Rueckfall auf den gespeicherten/default Target fuer diesen Aufruf kein Beweis fuer ignorierte ENV. Es sind zwei getrennte Fragen: (1) Target-Aufloesung auf produktivem CLI-Pfad (PR #1443), (2) eigenstaendige Core-Installation/Owner-Recovery des isolierten Targets (weiter offen). Keine Fail-Closed-Aufweichung, keine fremde Core-Autoritaet ausleihen. Karte bleibt aktiv bis zum nativen isolierten Up-/Destroy-Nachweis.

## 2026-11-08 Merge #1443 (ChatGPT)

- [PR #1443](https://github.com/mcpdev80/baseharbor/pull/1443) nach `develop` gemergt: `c27d259dfdd072533b115cf38c38a3f992082bb2`. Exact-head [CI #42430159943](https://github.com/mcpdev80/baseharbor/actions/runs/42430159943) `success`.
- Der bestehende produktive `BASEHARBOR_TARGET`-Auswahlpfad ist jetzt gegen persistierten Target-Override getestet. **Kein Beleg** fuer erfolgreichen isolierten Core-Up/Owner-Zyklus; Karte bleibt `active` bis nativer Docker/Podman-Betriebsnachweis vorliegt.
