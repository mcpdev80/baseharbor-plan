---
id: t-20261125-hunt47-config-mutation-migration-parity
card_number: "0428-349"
card_short_title: "migrate UIDs on mutation path"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "Read and mutation flows observe the same post-migration config, so a legacy file cannot produce a UID-collision surprise only on…"
kanban_title: 0428-349 · migrate UIDs on mutation path
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/config_mutation.go
---

- [ ] t-20261125-hunt47-config-mutation-migration-parity · 0428 hunt H-V47: config read path migrates TargetUIDs, mutation path does not (asymmetric UID handling) #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/config_mutation.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

Read and mutation flows observe the same post-migration config, so a legacy file cannot produce a UID-collision surprise only on the mutation side.

## Scope

- In scope:
  - `internal/deployment/config_mutation.go:20-40` `LoadConfigForMutation` → raw `decodeConfig` (no migration), versus `internal/deployment/target.go:249-252` `LoadConfig` → `migrateAndPersistTargetUIDs` (`target.go:263-278`, pure migrator `MigrateLegacyTargetUIDs` at target_id.go:80).
  - Run the pure migration inside the mutation read (and persist through the existing CAS owner), or make the collision check (`ResolveTargetUIDs`, target_id.go:161) authoritative in both paths.
  - The version-gate message half of BF-47-7 lives in 0428-345 (intake note: both paths die equally hard at `decodeConfig` on `version != 1` — confirmed; only the migration asymmetry is this card).
- Out of scope:
  - Config version-gate wording/forward-compat (0428-345).

## Acceptance

- Given a legacy config with two names for one Core installation (empty TargetUIDs), every entry point (target list AND any LoadConfigForMutation caller, e.g. target create/delete/policy) refuses with the SAME collision error — no entry point proceeds as if the UIDs were distinct.
- Legacy empty-UID configs observe identical `cfg.Targets[x].TargetUID` values in read and mutation paths (assert directly; the migration itself is idempotent and CAS-pure per target_id.go:35-114).

## Required checks

- **Modified features:** `internal/deployment/target_id_test.go` suite (collision/idempotence cases) and the cmd/baha config tests (`config_mutation_test.go`) stay green; extend with the mutation-path parity case.
- **New tests:** `TestLoadConfigForMutationMatchesReadPathUIDs` (package internal/deployment); auto-discovered unit lane.
- **CI integration and mapping:** no `.github/**` change.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `internal/deployment/config_mutation.go`, `target_id.go` (call-site only), `target.go` (save seams).
- Shared files: none.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-7 PARTIALLY LIVE — intake verification: (a) the akte's "read-only commands mutate config.yaml" is by DESIGN and documented (target.go:86 "such a definition migrates idempotently on read"; `MigrateLegacyTargetUIDs` fills ONLY empty UIDs, target_id.go:80 — no surprise edits to user content); (b) the akte's version-2-config "status surfaces it read-only" expectation is wrong — every command, read included, fails at the same gate (probe-confirmed). The LIVE residue is the read/mutation migration asymmetry above → this card. The version-gate half → 0428-345.
- Current state, branch, PR and evidence links. Newest first.
