---
id: t-20261125-hunt47-version-gate-error-surface
card_number: "0428-351"
card_short_title: "version gate recovery text"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: Every exact-equality state version gate says which way the mismatch goes (state older than this binary / written by a newer…
kanban_title: 0428-351 · version gate recovery text
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/target.go
---

- [ ] t-20261125-hunt47-version-gate-error-surface · 0428 hunt H-V47: all state version gates emit directionless 'unsupported version' errors with no next-action; too-new config breaks unrelated surfaces #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/target.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261125-hunt47-write-stamp-json-version](t-20261125-hunt47-write-stamp-json-version.md)  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

Every exact-equality state version gate says which way the mismatch goes (state older than this binary / written by a newer BaseHarbor) and what to do next.

## Scope

- In scope:
  - The gate list (all emit bare `unsupported … version %d`): `internal/deployment/target.go:19` + `:331`/`:397` (config), `internal/capability/registry.go:16`/`:395`, `internal/hosttrust/hosttrust.go:20`/`:404`, `internal/externalprovider/store.go:16`/`:46`, `internal/runtime/control_plane_credentials.go:132-155`, `internal/application/backup_metadata.go:16`/`:48`, `internal/application/update_metadata.go:14`, `internal/application/recovery_metadata.go:16`, `internal/devgateway/gateway.go:23`/`:618`, `internal/exposure/caddy.go:25`/`:330`, `internal/serviceaccess/pki.go:525`. Model: the typed `SharedBackendStateVersionMismatch{Found, Expected}` (internal/application/shared_backends.go:19-37, shared_backends_state.go:31-33).
  - A numeric comparison carrying found vs supported through to the CLI error surface, with two messages: "written by an older BaseHarbor → see the upgrade notes" vs "written by a newer BaseHarbor → run the newer release (rollback is unsupported)".
  - Intake-confirmed hard case: with `version: 2` config.yaml, `baha status` in a repo prints `Error: inspect repository: repository inspection size limit exceeded: more than 67108864 bytes of relevant files` — the config wall degrades into a false repository verdict; status-family commands must surface the version error itself.
- Out of scope:
  - Actually implementing any v1→v2 migration (0428-341/342); self-update version-string coupling (0428-346).

## Acceptance

- A shared typed mismatch (or reused `SharedBackendStateVersionMismatch` pattern) powers all gates listed above; no gate prints a directionless message.
- Read-only commands with a newer-than-binary config print the version problem and next-action, never the repository-inspection error (status/plan/list/doctor exercised).
- Table-driven unit test names each gate and asserts found/supported + direction appear (packages `internal/deployment`, `internal/capability` + CLI translation case).

## Required checks

- **Modified features:** existing gate tests (e.g. provider_registry_test.go:73 asserts the version-99 refusal) update to the new message contract.
- **New tests:** `TestStateVersionGatesNameDirectionAndNextAction` (table across gates); auto-discovered unit lane.
- **CI integration and mapping:** no `.github/**` change; touched packages select the Go unit lane.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: the gate sites listed above + a small shared error helper.
- Shared files: the CLI translation in `cmd/baha/app_context.go` is also touched by 0428-342; land this card after that one or coordinate hunks.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-7 tail + BF-47-8 first half + BF-47-9 clustered into this one error-surface card at intake: all line numbers RE-MEASURED at 99d9ddebc and hold (the akte's own line cites matched); the rollback-direction refusal with zero guidance (BF-47-9) is the same code shape as the forward-compat wall (BF-47-7), so they get one card. Intake witnesses: version-2 config → `unsupported BaseHarbor config version 2` bare (target.go:331) AND, in a real repo, the misleading repository-inspection error above; the grep for `written_by|baseharbor_version|created_by` writers returns no production stamp site (BF-47-8 core) — the writer-stamp half is tracked in 0428-346.
- Current state, branch, PR and evidence links. Newest first.


## Recovery provenance

Restored from original carrier `a47da84b82f2fd10294c934944566d4d935c61a1`; original blob `1eb4938b2204b83ebdd760e9123d1aec618dbffa`. Its source card number `0428-345` collided with the live main allocation for `t-20261128-hunt48-refresh-public-api-ownership-map`. Reallocated to verified-free `0428-351` due to the double allocation in the force-regression window. Stable task ID remains `t-20261125-hunt47-version-gate-error-surface`; dependent task IDs and links are unchanged.
