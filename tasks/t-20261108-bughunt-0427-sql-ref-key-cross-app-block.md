---
id: t-20261108-bughunt-0427-sql-ref-key-cross-app-block
card_number: "0427-121"
card_short_title: "phantom SQL key blocks down"
type: bug
areas: [lifecycle, sql]
release: v0.4.27
version: ""
parent: v0.4.27
owner: coord-board
kanban_status: wait
kanban_lane: wait
kanban_summary: "An application whose recorded intent carries the malformed SQL instance-reference key \"/\" can no longer block baha app down of a…"
kanban_title: "0427-121 · phantom SQL key blocks down"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1447, mcpdev80/baseharbor#1450]
sources: []
blocker: ""
wait_reason: "Native Docker/Podman two-app stop-plan regression passed; full CLI app up/down E2E awaits operator-OIDC availability and verified end-to-end execution."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/8f8be71df2d73846d2cfed275cf6dfbf28ded89f"]
---

- [ ] t-20261108-bughunt-0427-sql-ref-key-cross-app-block · Bug Hunt v0.4.27: Phantom-SQL-Referenz-Key blockiert app down #task #release/v0-4-27 #status/wait #view/wait #area/lifecycle #area/sql #kind/bug
    <!-- generated:card -->
    **Owner:** coord-board · **Priority:** high  
    **PR:** [baseharbor#1447](https://github.com/mcpdev80/baseharbor/pull/1447), [baseharbor#1450](https://github.com/mcpdev80/baseharbor/pull/1450)  
    **Waiting:** Native Docker/Podman two-app stop-plan regression passed; full CLI app up/down E2E awaits operator-OIDC availability and verified end-to-end execution.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/8f8be71df2d73846d2cfed275cf6dfbf28ded89f)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-board  
**Priority:** high  
**PRs:** [baseharbor#1447](https://github.com/mcpdev80/baseharbor/pull/1447), [baseharbor#1450](https://github.com/mcpdev80/baseharbor/pull/1450)  
**Source:** 
<!-- /generated:links -->

## Goal

An application whose recorded intent carries the malformed SQL instance-reference key `"/"` can no longer block `baha app down` of a different, unrelated application on the same target; either the bad key is never written, or stop/impact resolution tolerates unresolvable foreign-app references.

## Scope

- In scope:
  - Fix generation of `Services.SQLInstanceReferences` in the init/apply intent path so map keys are provider instance IDs, never `"/"` or a filesystem path (observed record: `SQLInstanceReferences: { "/": { "providerId": "postgresql/shared/environment-dev-91df0423" } }`).
  - Harden `internal/application/footprint.go` (`include()` / `indexResolutionInstances`, ~168-176) and the stop consumer union in `cmd/baha/application_stop_impact.go`: a dependency reference that resolves to no registry instance must fail closed only for the owning application, not silently poison every other app's stop on the target.
- Out of scope: registry schema migration of already-written bad records (beyond detection/warning), destroy inventory (0427-122).

## Acceptance

- `baha app down` for application A succeeds while application B exists in `configured` state with a `"/"`-keyed reference (or such a record cannot be produced at all — test proves the init path writes valid keys only).
- A unit test reproduces the phantom-key record shape and asserts the old failure (`provider resolution missing-dependency for /`) no longer blocks the foreign app's stop.
- Repro from the hunt: second app with `services.sql.enabled: true` → `baha up` refused at impact stage leaves the configured record → `app down` in the first repo fails with the quoted error.

## Required checks

- New/changed: `internal/application` footprint resolution tests (missing-dependency isolation for foreign consumers), `cmd/baha` init intent test asserting `SQLInstanceReferences` keys match provider instance IDs.
- Gate: existing package CI checks on both packages; develop rootless-Docker acceptance covers the two-app stop journey.
- Prove positive selection via touched paths; no new CI lane.

## Dependencies and file ownership

- Owned files or areas: `internal/application/footprint.go`, `cmd/baha/application_stop_impact.go`, init/apply intent writer.
- Shared files: provider-registry format docs if validation rules change — coordinate.

## Handoff

- Source: bug-hunt session 2026-11-07, 0.4.23-develop (8a3f58da9), Docker 29.6.0 rootless.
- Report: `~/dev/Tests/Baha-Bug-03-cross-app-down-missing-dependency.md` with full error text, deployment.json excerpt, registry dump; reproduced 1x end-to-end (causality registry↔intent proven; independent second run outstanding).
- Note: manual workaround during the hunt was deleting the phantom deployment record; stop-path cross-app coupling was observed in the same run.

## 2026-11-08 Takeover (ChatGPT)

- Owner `owner:chatgpt`, Lane `active`: SQL phantom-key causality (Writer + foreign-app stop footprint) check against current `develop` sources, create a reliable isolation regression and a targeted product fix. Do not globally suppress foreign app references.

## 2026-11-08 Ursachenpruefung (ChatGPT)

- The JSON name `SQLInstanceReferences` reported on 0.4.23-develop does **no longer** appear in the current `baseharbor/develop` code (GitHub source search 0 hits). The current source describes `Services.SQLInstances` as well as shared `ResolveFootprint`/`ResolveProviderPlan` routines. The error may persist in already-persisted records, but it is not cleanly patchable on the historical name alone.
- `cmd/baha/application_provider_plan.go` validates all foreign retained intents; `internal/application/provider_retained_intents.go` and `footprint.go` reject unresolvable dependencies. **Do not** generally skip foreign defective intents, otherwise shared-provider removal would be possible without a consumer proof.
- Next required evidence: current two-app reproduction including unchanged `deployment.json`, `provider-registry.json` and target CLI errors, then only fix the original writer edge or verifiable foreign-app isolation. Card `active`; no fix/PASS claimed.

### 2026-11-08 Writer-Grenze verifiziert (ChatGPT)

- Aktuelle `internal/application/manifest_validation.go` validiert bereits jede mit `SQLInstanceNames` deklarierte Instanz ueber `validateSlug("SQL instance name", name)`; der Name `/` ist kein gueltiger Slug und darf bei `ValidateIntent` nicht als neuer authored SQL-Instanzname durchgehen. Die alte `SQLInstanceReferences`-Struktur existiert aktuell nicht mehr im Produkt-Quellbaum. Der gemeldete `"/"`-Key stammt wahrscheinlich aus einem alten/persistierten Intent oder einer anderen Projektion, nicht automatisch aus dem aktuellen Authoring-Writer.
- **Kein Codefix ohne Repro:** bereits gespeicherte Records muessen auf Owner, Provider-Instanz und Abhaengigkeiten untersucht werden; shared-last-consumer-Sicherheit bleibt fail-closed, wenn die Zuordnung unbekannt ist.

## 2026-11-08 SQL-Phantom-Guard (ChatGPT)

- [PR #1447](https://github.com/mcpdev80/baseharbor/pull/1447), head `44cb45784774656fb75aaa32c6510dbb3c362c41`: current portable-intent test rejects SQL instance key `/` fail-closed and checks valid `primary` roundtrip. Exact PR CI open.
- The old registry/deployment projection `SQLInstanceReferences` no longer appears in the current source. **This test alone does not fix a historical defective foreign-app record**; hence the card stays `active`; two-app repro and owner-safe cleanup required.

## 2026-11-08 Merge #1447 (ChatGPT)

- [PR #1447](https://github.com/mcpdev80/baseharbor/pull/1447) erfolgreich nach `develop` gemergt, Merge-SHA `ffa83e78f9d4df43e9ca7b0e40792509c9f5c129`. Exact-head [CI #42432320249](https://github.com/mcpdev80/baseharbor/actions/runs/42432320249) terminal `success`, **8 PASS, 0 FAIL, 0 pending**.
- Validiert neue SQL-Instanzschluessel gegen ungueltiges `/`, aber **alte Deployment-Record-Referenzen und fremde konfigurierte Apps noch nicht im Zwei-App-E2E rehabilitiert**. Deshalb `active` und kein gesicherter Produkt-Fix fuer das urspruengliche Fehlerbild behauptet.

## 2026-11-08 Zwei-App-Legacy-Record-Regression (ChatGPT)

- [PR #1450](https://github.com/mcpdev80/baseharbor/pull/1450), Head `90ef32f158ab7afa1fef0d914f9529cd773f2a91`: tatsaechlicher `buildApplicationStopPlan`-Pfad fuer App A, waehrend App B SQL anfordert und im gespeicherten `deployment.json` das alte `SQLInstanceReferences:{"/":...}` enthaelt. Prueft, dass fremder historischer Record den aktuellen Stop-Plan nicht blockiert und nicht geschrieben wird. **Keine CI-PASS-Behauptung vor exaktem Run**; danach nativer Docker/Podman-Stop noch erforderlich. Karte bleibt `active`.


## Handoff 2026-11-08 (duplikat-hinweis)
- Neue Funde im Bug-Hunt 2026-11-08: linkding (Baha-Bug-01), ghost/status (Baha-Bug-04/05), gsmoke (Baha-Bug-06/07), ghostapp (Baha-Bug-05/07/08/09).
- Ghost status/source MISSING (Baha-Bug-05): symptom overlaps with this card (discovery on missing source). Card stays active; new reports document the phenomenon without a separate card.

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `"owner:chatgpt"` auf `coordinator`. Board-Spalte `wait` (Abhaengigkeit / ausstehende native Abnahme; **kein** technischer `blocked`-Alarm).
- PR #1450 merged 8f8be71; native two-app Docker/Podman stop/down and legacy SQL reference safety still need exact SHA PASS.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.

### 2026-11-08 Develop-Merge #1450

- [PR #1450](https://github.com/mcpdev80/baseharbor/pull/1450) nach `develop` gemergt, **SHA `8f8be71df2d73846d2cfed275cf6dfbf28ded89f`**, exact-head [PR-CI #42433085133](https://github.com/mcpdev80/baseharbor/actions/runs/42433085133) terminal `success` (10 PASS). Zwei-App-Regression prueft historischen SQL-`/`-Key im App-B-Record gegen Stop-Plan fuer A ohne Fremd-Record-Mutation.
- **Nativer Zwei-App-Stop/Down auf Docker/Podman noch offen.** Keine stillschweigende Provider-Referenz-Loeschung; an Coordinator uebergeben.

## 2026-11-08 Blocker classification audit

- Changed `blocked` to `wait`: old frontmatter asserted native two-app acceptance was **never** executed, contradicted by [round-1 evidence](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-sql-ref-key/round-1.md). Both Docker and Podman ran real CLI stop-impact *resolver-layer* tests and passed, with legacy phantom-key deployment record preserved unmodified. These were Go test invocations on native hosts, **not** full containerized two-app `baha up`→`baha app down` CLI lifecycle acceptance.
- Complete CLI journey stopped at the operator-OIDC authentication precondition; do not claim runtime E2E PASS. Await a functioning operator login / native CLI E2E with the two-app reproduction. Existing merged #1447/#1450 safety guards and regressions stay intact; coordinator retains task ownership.
