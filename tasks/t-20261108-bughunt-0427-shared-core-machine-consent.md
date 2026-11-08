---
id: t-20261108-bughunt-0427-shared-core-machine-consent
card_number: "0427-123"
card_short_title: "Shared-Core Consent blockiert"
type: bug
areas: [lifecycle,dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "owner:chatgpt"
kanban_status: active
kanban_lane: active
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-123 · Shared-Core Consent blockiert"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [ ] t-20261108-bughunt-0427-shared-core-machine-consent · 0427-123 · App up/down haengt an machine-consent #task #release/v0-4-27 #status/active #view/active #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** owner:chatgpt · **Priority:** high  
    **In progress** · owner:chatgpt  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** owner:chatgpt  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 docker2 hunt: up/down on shared-core is not completable without machine-consent digest; down hangs after consent prompt. Related to (not identical with) 0427-120's --confirm-candidate flag.

## Acceptance

up/down complete through documented interactive flow without hanging; any required confirmation is explicit, single, and recoverable; stuck-state cleanup exists.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Übernahme (ChatGPT)

- Owner `owner:chatgpt`; `active`. Sicherheitsrelevanter Consent-Fluss: interaktiven App-Up/Down-Weg und die bestehende `ProviderChangeConsent`-Pruefung gegen die VM-Reproduktion untersuchen. Keine Abschwaechung der Freigabe- oder Datenloeschungs-Gates. Zuerst echter Negativ-/Positivtest, dann enger Produktfix.
