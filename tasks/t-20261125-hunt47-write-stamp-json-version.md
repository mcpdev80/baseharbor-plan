---
id: t-20261125-hunt47-write-stamp-json-version
card_number: "0428-347"
card_short_title: "stamp writer release in state"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: planned
kanban_summary: "Version-gate diagnostics can name the release that wrote the state, and self-update candidate verification reads a machine…"
kanban_title: 0428-347 · stamp writer release in state
priority: low
depends_on: [t-20261125-hunt47-version-gate-error-surface]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/update_mutation.go
---

- [ ] t-20261125-hunt47-write-stamp-json-version · 0428 hunt H-V47: state files carry no writer-release stamp and self-update verification binds the human `baha version` format #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Waiting for prerequisites**  
    **Needs:** [t-20261125-hunt47-version-gate-error-surface](t-20261125-hunt47-version-gate-error-surface.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/update_mutation.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261125-hunt47-version-gate-error-surface](t-20261125-hunt47-version-gate-error-surface.md)  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

Version-gate diagnostics can name the release that wrote the state, and self-update candidate verification reads a machine contract instead of human text.

## Scope

- In scope:
  - A `written_by` release field (or reuse of an existing digest-bearing structure) on the versioned state writers: `internal/deployment/target.go:19` (config), `deployment_store.go:19` (record), `internal/capability/registry.go:16`, `internal/hosttrust/hosttrust.go:20`, `internal/externalprovider/store.go:16`, `internal/runtime/control_plane_credentials.go:132-155`, `internal/application/{backup,update,recovery}_metadata.go`, `internal/devgateway/gateway.go:23`, `internal/exposure/caddy.go:25`, `internal/serviceaccess/pki.go:525`. Intake witness: `git grep -l written_by` hits ONLY `cmd/baha/agent.go` (the agent report struct), never a state writer.
  - Version-gate errors (0428-345's surface) include the stamp when present.
  - Machine-readable version: keep `baha version -o json` ("version": version at cmd/baha/commands.go:200), retarget `verifyCandidateVersion` (cmd/baha/update_mutation.go:289-301, string-matches `"baha <target> "`) at the JSON output of the candidate (`<candidate> version -o json`), and pin the two human formats (`BaseHarbor %s` at main.go:139 vs `baha %s (commit…)` at commands.go:205) with a contract test so future humanization cannot silently break every self-update.
- Out of scope:
  - Direction/next-action wording of the gates themselves (0428-345 — dependency).

## Acceptance

- State writers persist the release identity they were written by; loaders surface it in mismatch diagnostics (no behavior change for matching versions).
- `verifyCandidateVersion` no longer parses human prose; a renamed/embellished `baha version` human line keeps self-update working (regression test with a candidate script printing a different human line but valid JSON).
- No format break for existing files: unknown/missing stamp loads as "unrecorded" (forward-compatible `omitempty`).

## Required checks

- **Modified features:** save/load round-trip suites in internal/deployment, internal/capability and the metadata packages; update_mutation tests (the `baha 0.2.0 (commit old…)` fixtures in cmd/baha/update_mutation_test.go adapt to the JSON contract).
- **New tests:** writer-stamp round-trip + version-contract test (packages above); auto-discovered unit lane.
- **CI integration and mapping:** no `.github/**` change; package selection via existing pr-gate-plan mapping.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: the writer sites above + `cmd/baha/update_mutation.go` (verification) + `cmd/baha/commands.go` (contract test).
- Shared files: gate message helpers from 0428-345 (depends edge pins the order).

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-8 LIVE at intake with the corrected premise note: the two human formats ALREADY differ (main.go:139 vs commands.go:205) and `verifyCandidateVersion` matches the commands.go form — today consistent; the brittleness and the missing writer stamp are the defect. All file:line cites re-verified at 99d9ddebc.
- Current state, branch, PR and evidence links. Newest first.
