---
id: t-20261108-bughunt-0427-target-env-ignored
card_number: "0427-124"
card_short_title: "target env has no effect"
type: bug
areas: [lifecycle,compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-124-target-env
kanban_status: closed
kanban_lane: closed
kanban_summary: "The production CLI target-selection slice is accepted on PR #1451. Greenfield core bootstrap and isolated-target ownership…"
kanban_title: "0427-124 · target env has no effect"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1443, mcpdev80/baseharbor#1451]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1451", "https://github.com/mcpdev80/baseharbor/commit/e39b0004346cdfd082e34ba55d94d24757bbbd27"]

---

## Outcome and acceptance

The production CLI target-selection slice is accepted on PR #1451. Greenfield core bootstrap and isolated-target ownership recovery are excluded from this slice by the coordinator decision and tracked in 0427-133 (`t-20261108-bughunt-0427-greenfield-isolation`), which depends on the access-wizard authority work.

- [x] t-20261108-bughunt-0427-target-env-ignored · 0427-124 · BASEHARBOR_TARGET wird ignoriert #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-124-target-env · **Priority:** high  
    **PR:** [baseharbor#1443](https://github.com/mcpdev80/baseharbor/pull/1443), [baseharbor#1451](https://github.com/mcpdev80/baseharbor/pull/1451)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1451), [proof 2](https://github.com/mcpdev80/baseharbor/commit/e39b0004346cdfd082e34ba55d94d24757bbbd27)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
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

Production command paths honour `BASEHARBOR_TARGET` (or an explicit equivalent) for target selection, and a regression proves the environment read on the production path. Isolated greenfield core bootstrap without touching shared-plane objects is a separate acceptance criterion owned by 0427-133.

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

### 2026-11-08 CODEX-MERGE #1451 scope decision

- Coordinator decision moves greenfield isolation/core bootstrap to follow-up 0427-133 (`t-20261108-bughunt-0427-greenfield-isolation`), dependent on access-wizard authority work. The target-selection slice is therefore independently acceptable without claiming a native greenfield bootstrap result.
- PR #1451 merged to `develop` as `e39b0004346cdfd082e34ba55d94d24757bbbd27`; exact-head CI run 42433354279 was successful before merge.
- Post-merge Runtime Docker Core run 42435313622 and Runtime Podman Core run 42435313588 both completed successfully on the merge SHA. Runtime-specific cells were skipped by their source-only impact selectors; these runs do not claim native Docker/Podman greenfield validation.

CODEX-MERGE #1451 e39b0004346cdfd082e34ba55d94d24757bbbd27; greenfield isolation moved to 0427-133 by coordinator decision; post-merge runtime Docker/Podman runs 42435313622 and 42435313588 success, source-only runtime cells skipped.
