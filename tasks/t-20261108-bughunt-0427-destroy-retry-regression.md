---
id: t-20261108-bughunt-0427-destroy-retry-regression
card_number: "0427-132"
card_short_title: "#1448 breaks destroy retry"
type: bug
areas: [lifecycle]
release: v0.4.27
version: ""
parent: v0.4.27
owner: coord-board
kanban_status: closed
kanban_lane: closed
kanban_summary: "develop's Runtime Docker Core and Podman Core push runs are green again;…"
kanban_title: "0427-132 · #1448 breaks destroy retry"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1453]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/42434076648", "https://github.com/mcpdev80/baseharbor/actions/runs/42476195799"]
---

- [x] t-20261108-bughunt-0427-destroy-retry-regression · Bug Hunt v0.4.27: 1448 macht destroy-retry rot #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** coord-board · **Priority:** critical  
    **PR:** [baseharbor#1453](https://github.com/mcpdev80/baseharbor/pull/1453)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/42434076648), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42476195799)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-board  
**Priority:** critical  
**PRs:** [baseharbor#1453](https://github.com/mcpdev80/baseharbor/pull/1453)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

develop's Runtime Docker Core and Podman Core push runs are green again; TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry passes on the exact develop head.

## Problem (discovered via owner report 2026-11-08, verified against hosted logs)

Both develop push runs failed on commit 1fe57f25007413c710e049094c62bf71656b2aa2 (merge of #1448 "fix(destroy): scope blocking unknown runtime to legacy local target only"): `cmd/baha/installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry [uuid]`, deterministic (fails in 0.016 s, identical on docker and podman cells). Previous develop head 8f8be71df was green on the same workflow.

## Acceptance

- Either the scoping in the production destroy path preserves deployment-state visibility for the native-retry fixture (root-cause fix), or #1448 is reverted; regression stays in the existing native acceptance job; develop push cells green on exact head (witness: hosted run ids in the act/evidence).

## Dependencies and file ownership

Umbrella only; write-set cmd/baha/app_destroy_lifecycle.go scope branch + installation_destroy_native_test.go fixture expectations. Owner decision needed if the intent of #1448 conflicts with the fixture contract.


## Audit 2026-11-08 — Merge-/Abnahme-Abgleich

- PR [#1453](https://github.com/mcpdev80/baseharbor/pull/1453) ist gemergt (`d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`). Die anschliessende native Regression in PR [#1464](https://github.com/mcpdev80/baseharbor/pull/1464) hat Docker und Podman bestanden und wurde laut Owner-Integration gemergt (`cd494610`).
- `active` auf der Karte ist **kein offener PR #1453**. Die urspruengliche Acceptance verlangt zusaetzlich einen exakten `develop`-Push-Lauf fuer beide nativen Runtime-Zellen; dieser wurde in diesem Karten-Audit nicht gesondert verifiziert. Bis dahin keine automatische Schliessung, kein Re-Claim und keine neuen Testressourcen reservieren.
