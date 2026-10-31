---
id: t-20261017-release-0-4-27-cleanup
type: maintenance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: cleanup
parent: v0.4.27
owner: ""
priority: high
depends_on: [t-20261017-release-0-4-26-verify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/q42-v27cleanup.md"]
---

- [ ] t-20261017-release-0-4-27-cleanup · v0.4.27 · Release start: reconcile old PRs, tasks and branches #task #release/v0-4-27 #status/planned #view/queued #area/release #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Later release** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/q42-v27cleanup.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-26-verify](t-20261017-release-0-4-26-verify.md)  
**Required by:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reconcile previous-release leftovers before new development.

## Scope and acceptance

- Read current remote PRs, task claims, branches, release evidence and running CI across BaseHarbor, Demo, Console, Connector and this plan repository.
- Close or supersede obsolete PRs/tasks only with an integration or explicit-obsolescence reference. Preserve genuinely active/future work and owner claims; no blanket deletion of unmerged code.
- Delete incorporated temporary branches. Preserve maintained tracks, immutable tags, approval/candidate refs and evidence still needed by release verifiers; apply existing artifact-GC retention rules.
- Publish a concise kept/removed/deferred inventory with reasons on planning main. No product changes, release or task acceptance is implied by cleanup.

## Required checks

Inspect actual remote state; verify required changes are incorporated before deletion. No runtime journey or full matrix for housekeeping.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#cleanup). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Live-Inventur erbracht, Branches sauber (0 >14 Tage). 5 "still-open-legit" alle merged, 2 stale-candidates bereits geschlossen. Neue offene PRs (#1227–#1232 CI-Kette, demo#120, console#8, nc#9) dokumentiert.

**Status: active → review.** Ein prüpbarer Cleanup-Kandidat mit Live-Evidence (GitHub-API, 2026-10-31, main = e1ef5ea) liegt an der Karte. **Annahme bleibt dem Maintainer vorbehalten** — nur dieser markiert eine Task `accepted` mit Evidence (AGENTS.md). Sobald cleanup `accepted`, wird `updates` (Gate) freigegeben und als erste Worker-Lane dispatched.

> Inventar-Deliverables liegen als https-Evidence an der Karte; ein PR existiert nicht (read-only Analyse). v0.4.26 ist veröffentlicht (v0.4.26-verify: published/superseded); die logische depends_on-Referenz bleibt bestehen.
>
> **Live-Gegenprüfung 2026-10-31 (GitHub API, main = e1ef5ea):**
> - baseharbor: 10 offene PRs (#1227–#1232 CI-Receipt-Kette, #1229, #1227–#1231; #1042 PR-closed aber merged).
> - demo: 1 offen (#120 v0.4.26 freeze-lift). console: 1 offen (#8 CI-Adapter-Proof). node-connector: 1 offen (#9 consumer-freeze).
> - Die 5 "still-open-legit" aus der q42-Evidence sind alle **merged** (baseharbor #1043/#1039/#1042, console#7, nc#8).
> - Die 2 stale-close-candidates (#3 console, #4 nc, vom 06.10.) sind **bereits geschlossen**.
> - Branches >14 Tage: 0 (unverändert).
> - Die neuen CI-PRs (#1227–#1232) gehören zum updates/prepare-Work, nicht zur Cleanup-Inventur.
> Inventur erbracht; Branches sauber; Kategorien validiert.

## Stand 2026-10-31
- **Inventur erbracht, Branches sauber.** GitHub-API-Gegenprüfung: 0 Branches >14 Tage.
- **5 "still-open-legit": alle merged** (baseharbor #1043/#1039/#1042, console#7, nc#8).
- **2 stale-close-candidates (#3 console, #4 nc) bereits geschlossen** — keine Aktion erforderlich.
- **Neue offene PRs** nach q42-Evidence: baseharbor #1227–#1232 (CI-Receipt-Kette), demo#120, console#8, nc#9. Gehören zum updates/prepare-Work.
- Cleanup-Kern erbracht; Branches bereinbar.
