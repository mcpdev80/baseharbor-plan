---
id: t-20261125-hunt47-destroystep-v1-warning-kind
card_number: "0428-353"
card_short_title: "name version kind destroy-all"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: planned
kanban_summary: "Every SKIPPED line of baha destroy --all states the true reason: missing record, unreadable/corrupt record, or version-gated…"
kanban_title: 0428-353 · name version kind destroy-all
priority: normal
depends_on: [t-20261125-hunt47-deployment-record-v1-wall]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/runtime_destroy_discovery.go
---

- [ ] t-20261125-hunt47-destroystep-v1-warning-kind · 0428 hunt H-V47: destroy --all renders version/corrupt deployment states with the wrong 'incomplete' text (data-ownership disclosure gap) #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261125-hunt47-deployment-record-v1-wall](t-20261125-hunt47-deployment-record-v1-wall.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/runtime_destroy_discovery.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261125-hunt47-deployment-record-v1-wall](t-20261125-hunt47-deployment-record-v1-wall.md)  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

Every SKIPPED line of `baha destroy --all` states the true reason: missing record, unreadable/corrupt record, or version-gated record — plus what happens to the data it owns.

## Scope

- In scope:
  - `cmd/baha/runtime_destroy_discovery.go:126-145`: `fullDestroyDeploymentWarnings` collapses ALL `DeploymentRecordStateError` kinds into the single "incomplete deployment state has no usable deployment.json…" detail. The text is written for the missing-damaged.json semantics (BF-46-3 era) but is applied to `deployable_version_mismatch` and `corrupt` too — both of which DO have a readable-on-disk deployment.json the binary simply refuses to load.
  - Name the kind, the found/supported version (`DeploymentRecordVersionMismatchVersions`), and the consequence ("its owned provider state under this Target is removed with the local BaseHarbor state") in the SKIPPED line; if that deployment's provider state cannot be accounted for, emit FAILED instead of SKIPPED so the data root is not removed silently.
- Out of scope:
  - The migrate/remove decision for v1 records themselves (0428-342 — this card only fixes the disclosure on the destroy-all path, regardless of that outcome); the volume-inventory heuristic gate (0428-330 BF-46-5 family).

## Acceptance

- The warning renderer distinguishes `missing` / `corrupt` / `deployable_version_mismatch` kinds; a version-mismatched deployment is never described as "no usable deployment.json".
- With a version-1 record on a Target, `baha destroy --all` output either names the kind+versions and the provider state it removes, or blocks with FAILED — never the current generic line + wholesale `os.RemoveAll(dataRoot)` (cmd/baha/runtime_destroy_all.go:602).
- Regression test asserts the kind-specific line (fixture via the existing `versionMismatchDeployment` helper, cmd/baha/w200_deployment_version_mismatch_test.go:19).

## Required checks

- **Modified features:** the destroy-all disclosure tests in `cmd/baha` stay green; `TestCountFullDestroyBlockersDistinguishesInformationalSkip` semantics preserved.
- **New tests:** named test `TestFullDestroyVersionMismatchNamesKind` (package cmd/baha, no real runtime; uses the existing dry-run/full-destroy test harnesses) — auto-discovered by the Go unit lane; SKIPPED-line assertions run without containers.
- **CI integration and mapping:** no `.github/**` change; cmd/baha changes select the Go unit lane via the existing pr-gate-plan mapping.
- **Mapping selection proof:** plan artifact shows unit selection for cmd/baha.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/runtime_destroy_discovery.go`, `runtime_destroy_all.go` (blocker semantics only).
- Shared files: `internal/deployment` warning-kind accessors from 0428-342; rebase on that card's landed shape.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-3 LIVE at intake with a corrected mechanism note: the intake probe shows destroy --all ABORTS with "Provider consumer inventory is incomplete or damaged" (strict `ListAllDeployments` fail-closed, runtime_destroy_all.go:140) BEFORE reaching the SKIPPED+RemoveAll path for most v1 states — the akte's "skips silently and deletes anyway" is reachable only on the best-effort display branch when a strict listing does not run (e.g. `installation_destroy_continuation.go:21` uses the same discovery, and a target whose owner check passes but record version gate fails produces kind=deployable_version_mismatch warnings rendered with the WRONG "incomplete/no usable deployment.json" text — confirmed by direct call probe of `fullDestroyDeploymentWarnings`). The disclosure defect is confirmed; the deletion-while-skipped path depends on 0428-342's outcome.
- Current state, branch, PR and evidence links. Newest first.
