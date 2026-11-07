---
id: t-20261108-bughunt-0427-multitarget-ambiguity
card_number: "0427-126"
card_short_title: "init/status/doctor bei mehreren Targets"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "with a repository that has multiple deployment targets configured, baha app init / status / doctor fail with 'multiple deployment targets configured' and offer no selection remedy"
kanban_title: 0427-126 · init/status/doctor bei mehreren Targets
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/podman2.md]
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 podman2 hunt: brownfield repo; error text verbatim in the act; commands give no --target selection hint.

## Acceptance

the three commands either apply to all targets consistently or present an explicit selectable list with a deterministic default; error text names the remedy.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.
