---
id: t-20261108-bughunt-0427-sql-ref-key-cross-app-block
card_number: "0427-121"
card_short_title: "phantom SQL key blocks down"
type: bug
areas: [lifecycle, sql]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "owner:chatgpt"
kanban_status: active
kanban_lane: active
kanban_summary: "An application whose recorded intent carries the malformed SQL instance-reference key \"/\" can no longer block baha app down of a…"
kanban_title: 0427-121 · phantom SQL key blocks down
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1447]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-bughunt-0427-sql-ref-key-cross-app-block · Bug Hunt v0.4.27: Phantom-SQL-Referenz-Key blockiert app down #task #release/v0-4-27 #status/active #view/active #area/lifecycle #area/sql #kind/bug
    <!-- generated:card -->
    **Owner:** owner:chatgpt · **Priority:** high  
    **PR:** [baseharbor#1447](https://github.com/mcpdev80/baseharbor/pull/1447)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** owner:chatgpt  
**Priority:** high  
**PRs:** [baseharbor#1447](https://github.com/mcpdev80/baseharbor/pull/1447)  
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

## 2026-11-08 Übernahme (ChatGPT)

- Owner `owner:chatgpt`, Lane `active`: SQL-Phantom-Key-Kausalitaet (Writer + Fremd-App-Stop-Footprint) anhand aktueller `develop`-Quellen pruefen, sichere Isolationsregression und gezielten Produktfix erstellen. Fremde App-Referenzen nicht global unterdruecken.

## 2026-11-08 Ursachenpruefung (ChatGPT)

- Der auf 0.4.23-develop gemeldete JSON-Name `SQLInstanceReferences` kommt im aktuellen `baseharbor/develop`-Code **nicht mehr** vor (GitHub Source Search 0 Treffer). Die aktuelle Source beschreibt `Services.SQLInstances` sowie gemeinsame `ResolveFootprint`-/`ResolveProviderPlan`-Routen. Der Fehler kann weiter in bereits persistierten Records bestehen, ist aber nicht sauber allein am historischen Namen patchbar.
- `cmd/baha/application_provider_plan.go` validiert alle fremden retained Intents; `internal/application/provider_retained_intents.go` und `footprint.go` verweigern unaufloesbare Dependencies. **Nicht** allgemein fremde fehlerhafte Intents ueberspringen, da sonst Shared-Provider-Entfernung ohne Konsumentennachweis moeglich waere.
- Naechster notwendiger Beleg: aktuelle Zwei-App-Reproduktion einschliesslich unveraenderter `deployment.json`, `provider-registry.json` und Ziel-CLI-Fehler, dann nur die urspruengliche Writer-Kante oder verifizierbare Fremd-App-Isolation korrigieren. Karte `active`; kein Fix/PASS behauptet.

### 2026-11-08 Writer-Grenze verifiziert (ChatGPT)

- Aktuelle `internal/application/manifest_validation.go` validiert bereits jede mit `SQLInstanceNames` deklarierte Instanz ueber `validateSlug("SQL instance name", name)`; der Name `/` ist kein gueltiger Slug und darf bei `ValidateIntent` nicht als neuer authored SQL-Instanzname durchgehen. Die alte `SQLInstanceReferences`-Struktur existiert aktuell nicht mehr im Produkt-Quellbaum. Der gemeldete `"/"`-Key stammt wahrscheinlich aus einem alten/persistierten Intent oder einer anderen Projektion, nicht automatisch aus dem aktuellen Authoring-Writer.
- **Kein Codefix ohne Repro:** bereits gespeicherte Records muessen auf Owner, Provider-Instanz und Abhaengigkeiten untersucht werden; shared-last-consumer-Sicherheit bleibt fail-closed, wenn die Zuordnung unbekannt ist.

## 2026-11-08 SQL-Phantom-Guard (ChatGPT)

- [PR #1447](https://github.com/mcpdev80/baseharbor/pull/1447), Head `44cb45784774656fb75aaa32c6510dbb3c362c41`: aktueller Portable-Intent-Test weist SQL-Instanzschluessel `/` fail-closed ab und prueft gueltigen `primary`-Roundtrip. Exakte PR-CI offen.
- Die alte Registry-/Deployment-Projektion `SQLInstanceReferences` kommt in der aktuellen Source nicht mehr vor. **Dieser Test allein behebt keinen historischen fehlerhaften Fremd-App-Record**; daher Karte weiterhin `active`, Zwei-App-Repro und owner-sichere Bereinigung erforderlich.
