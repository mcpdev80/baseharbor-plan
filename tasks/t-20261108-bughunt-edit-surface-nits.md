---
id: t-20261108-bughunt-edit-surface-nits
card_number: "0427-151"
card_short_title: "Edit surface nits"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-edit-surface"
kanban_status: active
kanban_lane: active
kanban_summary: "Each of the four: documented decision + matching regression OR fix in the existing field; the message loop terminates after at…"
kanban_title: 0427-151 · Edit surface nits
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1479]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md"]
---
- [ ] t-20261108-bughunt-edit-surface-nits · Bug Hunt v0.4.27: Edit surface nits #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-edit-surface · **Priority:** normal  
    **PR:** [baseharbor#1479](https://github.com/mcpdev80/baseharbor/pull/1479)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-edit-surface  
**Priority:** normal  
**PRs:** [baseharbor#1479](https://github.com/mcpdev80/baseharbor/pull/1479)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Each of the four: documented decision + matching regression OR fix in the existing field; the message loop terminates after at most one pass.

## Problem (source evidence in the dossier)
Interactive help contradicts itself (piping works, help/--no-input claim a terminal is required, BF-04); app new --directory silently creates missing parents (BF-07); status/doctor print a Docker block on a podman-only target (BF-08); init on an existing manifest loops its message (BF-14). Source: hunt H-P3.

## Acceptance
Each of the four: documented decision + matching regression OR fix in the existing field; the message loop terminates after at most one pass.

## Dependencies and file ownership
None. Write-set: cmd/baha edit surface (help text, directory check, target block display, init manifest path).

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): four independent symptoms; fix commits must each cite their BF, split PRs if write-sets differ. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## Code- und PR-Übernahme — 2026-11-08

- Owner `chatgpt-r27-edit-surface`, Produkt-[PR #1479](https://github.com/mcpdev80/baseharbor/pull/1479) auf `develop` zur Bearbeitung BF-04/07/08/14.
- Vorhandener Manifest-Pfad wird in einem einzigen Runtime-Init-Zweig verarbeitet, Podman-Target zeigt keine Docker-Engine, fehlende Directory-Parents werden vor Mutation abgelehnt, non-interactive Hilfetext geklärt. Gezielte Regressionstests für alle vier Befunde ergänzt.
- Exact-head CI noch offen. Status `active`, kein Merge oder acceptance behauptet.
