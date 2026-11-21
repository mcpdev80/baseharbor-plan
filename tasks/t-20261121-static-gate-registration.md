---
id: t-20261121-static-gate-registration
card_number: "0428-208"
card_short_title: "0428-208 static gate"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: "Codex (Owner-directed, 2026-11-21)"
kanban_status: blocked
kanban_lane: blocked
kanban_summary: Run the existing scripts/ci-fast-check.sh as its own static gate in the v0.4.28 Pre-Release Suite. Preserve every existing…
kanban_title: 0428-208 · 0428-208 static gate
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1746"]
sources: []
blocker: "Owner 2026-11-21: zweckgebundene Freigabe für pre-release-runtime-suite.yml und seine Dispatch-Verkabelung für 0428-205. Alle anderen .github-Änderungen bleiben gesperrt und dürfen nur über eine neue Owner-Freigabe erfolgen. Hosted positive proof is blocked because docs/releases/v0.4.28.demo-ref is absent on develop; do not substitute the v0.4.27 pin."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-static-gate-registration · 0428-208 wire `scripts/ci-fast-check.sh` as a standalone v0.4.28 Release Suite gate #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner-directed, 2026-11-21) · **Priority:** high  
    **PR:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746)  
    **Blocker:** Owner 2026-11-21: zweckgebundene Freigabe für pre-release-runtime-suite.yml und seine Dispatch-Verkabelung für 0428-205. Alle anderen .github-Änderungen bleiben gesperrt und dürfen nur über eine neue Owner-Freigabe erfolgen. Hosted positiv…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (Owner-directed, 2026-11-21)  
**Priority:** high  
**PRs:** [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746)  
**Source:** 
<!-- /generated:links -->

## Goal

Run the existing `scripts/ci-fast-check.sh` as its own static gate in the v0.4.28 Pre-Release Suite. Preserve every existing Release Suite gate selection, keep the normal CI workflow unchanged, and make an uncatalogued gate fail with its exact ID and one clear repair action.

## Owner scope authorization

Owner 2026-11-21: zweckgebundene Freigabe für pre-release-runtime-suite.yml und seine Dispatch-Verkabelung für 0428-205. Alle anderen .github-Änderungen bleiben gesperrt und dürfen nur über eine neue Owner-Freigabe erfolgen.

## Scope

- In scope: the `atomic/static/ci-fast-check` catalog entry; planner selection and static executor dispatch; the `pre-release-runtime-suite.yml` setup, catalog validation and dispatch case; reuse fingerprint mapping for the gate's source and selector tests; focused regression coverage.
- Out of scope: every other `.github` file, especially `.github/workflows/ci.yml`; any new PR-CI route or second test list; unrelated gate or release changes.
- `ci-fast-check` executes `scripts/ci-fast-check.sh` directly. Its existing test command remains the only list of checks for this gate.

## Acceptance

1. One PR contains the catalog, dispatch and two proofs. The Coordinator and Release Owner confirm the bounded scope and results in that PR.
2. Positive proof: the existing static Release Suite jobs and the new standalone gate run on the same exact candidate; all selected jobs pass and the previous matrix selection remains intact.
3. Negative proof: an intentionally uncatalogued static gate exits nonzero, identifies its exact catalog ID, and gives the direct registration action.
4. The new gate is selected only by the Release Suite. `.github/workflows/ci.yml` is unchanged, and feature PRs do not execute `ci-fast-check` through the normal CI path.
5. 0428-205 stays blocked until the two proofs are demonstrated live. Do not mark it accepted from catalog or card state alone.

## Test binding

| Attribute | Value |
| --- | --- |
| Gate | `atomic/static/ci-fast-check` |
| Executed source | `bash scripts/ci-fast-check.sh` |
| Trigger | v0.4.28 Pre-Release Suite static gate matrix |
| Negative case | `atomic/static/test-uncatalogued` in an isolated catalog fixture; selection exits nonzero with actionable ID |

## Stop and report

- Do not change `.github/workflows/ci.yml` or any other `.github` file.
- Do not merge unless both requested proofs and both PR confirmations are present.
- 0428-205 remains blocked pending the live gate demonstration.

## Handoff

- Candidate branch: `lane-0428-208-static-release-gate`; PR [#1746](https://github.com/mcpdev80/baseharbor/pull/1746).
- Candidate head after hop to current develop: `0a710235a4134ed45b53303a8faad44cbf4119d5`.
- Local exact workflow-policy comparison passed; `bash scripts/ci-fast-check.sh` passed (307 tests); uncatalogued-gate negative case exits nonzero and prints its ID plus the repair action.
- Coordinator scope confirmation is recorded in [PR comment](https://github.com/mcpdev80/baseharbor/pull/1746#issuecomment-7060850641). Exact-head PR run `44891832834` is pending. Hosted positive Release Suite proof and Release Owner confirmation remain pending. The exact v0.4.28 Demo pin file is absent on current `develop`; no older pin was substituted.
