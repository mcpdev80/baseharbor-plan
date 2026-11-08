---
id: t-20261108-bughunt-second-target-shares-core
card_number: "0427-163"
card_short_title: "Second same-host target silent"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w163b-sharedgate2
kanban_status: active
kanban_lane: active
kanban_summary: "Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for…"
kanban_title: 0427-163 · Second same-host target silent
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1487]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-second-target-shares-core · Bug Hunt v0.4.27: Second target reuses Core #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w163b-sharedgate2 · **Priority:** normal  
    **PR:** [baseharbor#1487](https://github.com/mcpdev80/baseharbor/pull/1487)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w163b-sharedgate2  
**Priority:** normal  
**PRs:** [baseharbor#1487](https://github.com/mcpdev80/baseharbor/pull/1487)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for a second same-host target must refuse to silently join another target's Core and must name the owning target plus concrete options. Decision note in the card for owner if by-design; regression in the runtime group.

## Problem (source evidence in the dossier)
Creating a second podman target with the same local access reference and running up --control-plane-only connects to the already-running shared Core: same ports 15433/18201, same bh-<first>-shared-* containers/networks; the second target gets no state dir and status still reports the first target (BF-05, blocker candidate, architecture/hazard). The project name is keyed by target name but running discovery resolves to whichever Core is up. Sources: internal/runtime/project_names.go:7-9, cmd/baha/target.go:603-605.

## Acceptance
Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for a second same-host target must refuse to silently join another target's Core and must name the owning target plus concrete options. Decision note in the card for owner if by-design; regression in the runtime group.

## Dependencies and file ownership
None. Write-set: control-plane up / runtime project naming.

## Exact-head CI monitoring — 2026-11-08 (0427-163)

- [PR #1487](https://github.com/mcpdev80/baseharbor/pull/1487), head `a158f2b183db3ed2dcfd6dcbead378b626ae9a55`, [CI #42503466672](https://github.com/mcpdev80/baseharbor/actions/runs/42503466672). Source format failed on unformatted shared_core_conflict_test.go; aligned map/fixture formatting, then re-triggered CI. Card remains open until the required CI is terminal green.

## Source-format correction — 2026-11-08

- The initial source-format repair was still not gofmt-canonical in the map table; fixed the exact spacing, verified the formatting shape separately, and pushed PR #1487 head `9572bdb3ae83db6da6252fcdc4d865e0a9fbbf35`.
- Fresh exact-head CI: https://github.com/mcpdev80/baseharbor/actions/runs/42503646942. Do not mark accepted before terminal checks.

## Native two-Target acceptance added — 2026-11-08

- PR #1487 rebased on develop after #1457: exact head `5a0b66c7a2fe3756a7caa640e94b2ae4a04c45fd`.
- Added real `TestSecondSameHostCoreNativeConflictInCI`: first Target owns a running Core on the selected Docker/Podman engine; second distinct configured Target's `baha up --control-plane-only --yes` must fail with typed owner conflict, first stays running, second never starts a Core.
- Wired into both `PR · Native destroy retry` matrix cells via `scripts/ci-native-installation-destroy.sh`; test must PASS once, not SKIP or synthetic success. Corrected engine-discovery errors to fail closed and stopped foreign Core resources to be ignored.
- Await exact-head native CI before merge and card acceptance.

## Owning Identity Core regression — 2026-11-08

- Additional review found that a Target's own `bh-<target>-core-shared` managed Identity project must be excluded from foreign-Core detection. Corrected on PR #1487 current head `3826acd9329832d907e717cbd97218740049f932` with `TestSharedCoreOwnerConflictIgnoresOwningIdentityCore`.
- Prior exact-head runs are historical only; new head must independently pass Go checks and actual Docker/Podman two-Target native CI before merge.

## Actual Docker two-Target proof — 2026-11-08

- [PR #1487 CI #42508772678](https://github.com/mcpdev80/baseharbor/actions/runs/42508772678) ran `TestSecondSameHostCoreNativeConflictInCI` against **actual Docker**: PASS (69.31s, exact head `3826acd9329832d907e717cbd97218740049f932`). Runtime log confirms the first live Core `w169-ci-bootstrap-8886576f` remained running and second distinct target `w169-second-target-conflict-6b91ea30-iso` was refused before a second Core started. The script's anti-skip verifier returned `PASS: two real Targets, one native engine, no silent Core reuse`.
- Podman and full Go unit/final PR gate still pending at this checkpoint; do not mark done or merge yet.

## Actual Podman two-Target proof — 2026-11-08

- Same exact-head [CI #42508772678](https://github.com/mcpdev80/baseharbor/actions/runs/42508772678): `TestSecondSameHostCoreNativeConflictInCI` **PASS on actual Podman** (66.84s), and anti-skip verifier `PASS: two real Targets, one native engine, no silent Core reuse`.
- First real Core `w169-ci-bootstrap-b2e0d3ca` remained running while second distinct Target `w169-second-target-conflict-d000e981-iso` was refused without a second Core. Combined Docker and Podman native proof passed at exact head; Go unit/final gate remained pending at the time of recording.
