---
id: t-20261108-bughunt-0427-shared-core-machine-consent
card_number: "0427-123"
card_short_title: "App up/down haengt an machine-consent"
type: bug
areas: [lifecycle,dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "baha app up/down against a shared Core require machine-executor confirmation (digest); plain PTY interaction does not satisfy it and down stalls mid-operation"
kanban_title: 0427-123 · App up/down haengt an machine-consent
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/vm-bughunt/docker2.md]
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 docker2 hunt: up/down on shared-core is not completable without machine-consent digest; down hangs after consent prompt. Related to (not identical with) 0427-120's --confirm-candidate flag.

## Acceptance

up/down complete through documented interactive flow without hanging; any required confirmation is explicit, single, and recoverable; stuck-state cleanup exists.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.
