---
id: t-20261108-bughunt-0427-target-env-ignored
card_number: "0427-124"
card_short_title: "BASEHARBOR_TARGET wird ignoriert"
type: bug
areas: [lifecycle,compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "isolated target selection via BASEHARBOR_TARGET env is read only in TEST code; production up/use/status ignore it, so every up lands on the shared plane and isolation setups are not reproducible"
kanban_title: 0427-124 · BASEHARBOR_TARGET wird ignoriert
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

- [ ] t-20261108-bughunt-0427-target-env-ignored · 0427-124 · BASEHARBOR_TARGET wird ignoriert #task

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-3 docker2 hunt: grep on develop 0fe53052 shows t.Setenv(BASEHARBOR_TARGET) only in *_test.go (app_backup_runtime_fixture_test.go:26 u.a.), no production os.Getenv read; core self-install for isolated targets missing.

## Acceptance

production command paths honour BASEHARBOR_TARGET (or an explicit equivalent) for target selection; an isolated greenfield run on docker-2 completes without touching shared-plane objects; regression proves the env read on the production path.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.
