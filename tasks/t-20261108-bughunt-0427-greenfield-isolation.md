---
id: t-20261108-bughunt-0427-greenfield-isolation
card_number: "0427-133"
card_short_title: "greenfield isolation open"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: owner-chatgpt-r27
kanban_status: active
kanban_lane: active
kanban_summary: "An isolated greenfield run (BASEHARBORTARGET-selected second target, docker-2 style) completes bootstrap + core self-install +…"
kanban_title: "0427-133 · greenfield isolation open"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-access-wizard]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1460, mcpdev80/baseharbor#1503]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/act-1451-review.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-greenfield-isolation/acceptance-gap-audit.md"]
---

- [ ] t-20261108-bughunt-0427-greenfield-isolation · Bug Hunt v0.4.27: Greenfield-Isolation offen #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** owner-chatgpt-r27 · **Priority:** normal  
    **PR:** [baseharbor#1460](https://github.com/mcpdev80/baseharbor/pull/1460), [baseharbor#1503](https://github.com/mcpdev80/baseharbor/pull/1503)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/act-1451-review.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-greenfield-isolation/acceptance-gap-audit.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md)  
**Owner:** owner-chatgpt-r27  
**Priority:** normal  
**PRs:** [baseharbor#1460](https://github.com/mcpdev80/baseharbor/pull/1460), [baseharbor#1503](https://github.com/mcpdev80/baseharbor/pull/1503)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

An isolated greenfield run (BASEHARBOR_TARGET-selected second target, docker-2 style) completes bootstrap + core self-install + status without creating or mutating shared-plane objects; proven by a native docker AND podman cell in CI.

## Problem (split decision 2026-11-08)

act-1451-review.md: the 0427-124 production reader merged, but use/activate resolves through the management-connection binding whose authority belongs to access-wizard (#1430) and onboarding (#1435); the review requires this clause as a separate task.

## Acceptance

- Documented deterministic flow for isolated targets (use/activate honours the selected target's own core bootstrap); regression in CI; no shared-plane writes when operating an isolated target.

## Dependencies and file ownership

Depends on access-wizard acceptance (#1430). Write-set: cmd/baha target/use/activate paths + internal/deployment target-state reader.


## Audit 2026-11-08 — PR geschlossen, Acceptance getrennt

- [#1460](https://github.com/mcpdev80/baseharbor/pull/1460) ist gemergt nach `develop` (`201735b03145ce036407a0272882ec184943cd6a`); die Keycloak-Core-Issuer-/Destroy-Retry-CI war gruenn.
- Fuer die hier geforderte **isolierte Greenfield-E2E-Kette** auf Docker und Podman fehlt in dieser Kartenpruefung ein separat ausgewiesener PASS-Nachweis. Daher `active` nicht allein aus dem PR-Merge in `closed` umschreiben. `pending-lane-*` ist kein bestaetigter aktiver Worker; diese Eigentuemer-Zuordnung ist im naechsten Owner-Abgleich aufzuklaeren.

## Native E2E acceptance follow-up — 2026-11-08

- Source and CI gap audited in [acceptance-gap-audit.md](../evidence/r27-welle5-folge-2026-11-08/bughunt-greenfield-isolation/acceptance-gap-audit.md). Docker/Podman currently prove destroy-retry and same-engine conflict, not the positive second-isolated-engine greenfield chain.
- A second Core on the same daemon is intentionally forbidden; acceptance needs a genuinely isolated endpoint and a cleanup claim for both runtimes. Do not weaken the ownership guard or treat the existing native conflict test as positive evidence.
- Card stays **active** pending an exact-SHA Docker and Podman positive Core bootstrap/use/activate/status and no-shared-plane-writes proof. No additional CI success is claimed.

## Proof-gate implementation — 2026-11-08

- [Draft PR #1503](https://github.com/mcpdev80/baseharbor/pull/1503) provides fail-closed JSON verification for the future named native greenfield test on both Docker and Podman; it checks exact SHA, named PASS, no SKIP/FAIL and package teardown. Includes isolated Python regression cases.
- The actual positive two-engine bootstrap/use/activate/status Go test, hosted execution and no-shared-plane-write witness are **not yet supplied**. PR is intentionally Draft and the card remains active. Do not merge or close on verifier-only evidence.

## Pause / wait — 2026-11-08

- Owner-Entscheidung: Diese bereits begonnene Karte wird vorerst pausiert, um parallele Target/Core-/CI-Integration zu vermeiden. Die zweite Session bearbeitet PR #1473 und CI #5341; der CI-Owner bleibt fuer Workflow-Auswahl verantwortlich.
- Dies ist eine **Ressourcen-/Koordinationspause**, keine nachgewiesene technische Dependency von 0427-133 auf #1473 und kein Blocker.
- PR #1503 bleibt Draft, wird nicht gemergt. Wiederaufnahme nach Abstimmung; danach fehlende native Isolation-Acceptance gezielt in bestehende CI aufnehmen.

## Integration follow-up 2026-11-09

Draft #1503's two fail-closed proof-verifier files were replayed on post-#1518 `develop` as `33c0e25eda3b1f17fa37600a8aad215806f2ef11`; focused draft CI completed successfully. The real positive native Docker+Podman Greenfield isolated-Core Go test and its hosted run remain unimplemented. Keep Draft and card open, no false E2E PASS.

## Reaktiviert 2026-11-09

#1503 besitzt jetzt den nativen Test `TestGreenfieldIsolatedCoreNativeInCI`, Docker-/Podman-Host-Jobs und einen SHA-genauen Zwei-Runtime-Verifier auf `d99fc7c7`. Full-CI laeuft; keine native PASS- oder Release-Abnahme behauptet. Die bisherige Pause ist beendet.

## 2026-11-09 – Greenfield-PR nach Credentials-Merge neu integriert

#1503 war auf altem `develop` gruen, wurde nach dem Merge von #1470 aber von der GitHub Merge-API mit Konflikt (HTTP 405) verweigert. Der reine Greenfield-PR wurde deshalb ohne neue Produktfunktionalitaet auf `develop` neu aufgebaut: SHA `4a99e8f39f0956f888149fc7190b0562810c768c`. Der einzige Workflow-Konflikt betraf die `needs`-Liste (`pr_unit_shards` aus neuerem develop plus eigener `pr_native_greenfield_proof`); beide erhalten. Ein erneuter exakter CI-Lauf #42702568290 ist erforderlich und bei der Abfrage noch in Arbeit. Nicht mergen oder als accepted markieren, bevor er erfolgreich abgeschlossen ist.

## Verified integration and remaining release proof — 2026-11-09

- [BaseHarbor PR #1503](https://github.com/mcpdev80/baseharbor/pull/1503) is now **merged** into `develop` at `78963050a66e8758569223d01967174abadbffc4` (2026-11-09 21:36 UTC), after exact-head [PR workflow #42702568290](https://github.com/mcpdev80/baseharbor/actions/runs/42702568290) succeeded. The PR contains the native Greenfield Go test and proof verifier and registers the Docker/Podman proof workflow steps in `.github/workflows/ci.yml`.
- **Do not mark native two-engine E2E accepted from that PR workflow alone:** its reported jobs did not include the newly introduced `pr_native_greenfield_proof` job, even though the workflow is now present on `develop`. A subsequent selected PR/native run must execute both real Docker/Podman Greenfield cells and the exact-SHA two-engine aggregate proof. The physical independent-workstation/Core/Connector/READY journey is also a separate release acceptance requirement.
- Preserve **active** until the actual selected native proof has been captured and reviewed, then move to review/closed with true HTTPS evidence. No early release/tag.
