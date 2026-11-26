---
id: t-20261125-hunt47-recover-preflight-and-flag-route
card_number: "0428-355"
card_short_title: "gate update --recover path"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "baha update --recover --version VERSION --yes (docs/cli/core.md:153, docs/spec/core-provider-update-v1.md:34) actually…"
kanban_title: 0428-355 · gate update --recover path
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/update.go
---

- [ ] t-20261125-hunt47-recover-preflight-and-flag-route · 0428 hunt H-V47: the documented HA recovery verb is unreachable through the dispatcher and unguarded by catalog/journal preflight #task #release/v0-4-28 #status/planned #view/ready #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/update.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

`baha update --recover --version VERSION --yes` (docs/cli/core.md:153, docs/spec/core-provider-update-v1.md:34) actually dispatches, and refuses before any restore begins when the release has no embedded pin or the installation has no matching durable recovery journal.

## Scope

- In scope:
  - Flag routing: `extractGlobalOutputOptions` (cmd/baha/main.go:184-237) treats ANY `--version` token as the global version flag and strips it (main.go:135-141 fails with "--version cannot be combined with a command" when a command follows). Proven at intake for every ordering, including `update --yes --version 0.4.24` (the pattern docs/cli/core.md:86 itself instructs). Fix: treat `--version` as global only when it appears before the command word (or exclude the `update` subcommand's value position), and keep `baha --version` exact.
  - Recover preflight: `recoverNativeCoreHA` → `recoverOwnedCoreHA` (cmd/baha/update_ha_recovery_command.go:12-49, update_ha_cutover_native.go:472) never calls `coreupdate.LoadRelease` (internal/coreupdate/catalog.go:36-44; only v0.4.24 ships an embedded pin) nor requires a matching journal under `coreUpdateJournal(root, release, false)` before entering the destructive restore; contrast the forward path `preflightNativeCoreUpgrade` (cmd/baha/update_mutation.go:54-61). Add both checks with named refusal reasons.
- Out of scope:
  - Self-update verification coupling to `baha version` output (0428-346); Core provider migration execution (H-V47 rows BF-47-5/6 stay separate).

## Acceptance

- A CLI-dispatch test runs `runWithIO(..., "update", "--recover", "--version", "0.4.24", "--yes")` and asserts the recover branch is entered (fail-closed later, e.g. "HA recovery requires the matching, owned Core"), NOT the usage error; `baha --version` alone and `--version` before other commands keep printing the version only.
- With a release that has no embedded catalog pin, or with no durable journal/recovery point for that release, `recoverOwnedCoreHA` refuses with a named reason BEFORE any restore/displacement; unit test through the dispatch seam with a temp installation (no real runtime).
- docs/cli (EN+DE) and command-index stay truthful after the fix (documentation-audit clean).

## Required checks

- **Modified features:** cmd/baha update/flag tests (`TestParseSelfUpdateOptionsDefaultsToStable`, completion/`extractGlobalOutputOptions` cases in completion_test.go:85) extend, never regress.
- **New tests:** `TestUpdateRecoverRoutesPastGlobalVersionFlag` and `TestUpdateRecoverRefusesUnknownReleaseOrMissingJournal` (package cmd/baha; auto-discovered unit lane; no containers).
- **CI integration and mapping:** no `.github/**` change; cmd/baha selects the Go unit lane.
- **Mapping selection proof:** plan artifact shows unit-lane selection.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/main.go` (flag extraction), `cmd/baha/update.go`, `update_ha_recovery_command.go`, `update_ha_journal.go`, docs/cli/core + command-index wording.
- Shared files: `extractGlobalOutputOptions` is used by every command — the fix must keep global semantics for all non-`update` commands (regression list in the test).

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-4 LIVE and WIDENED at intake: the akte assumed the recover path is reachable and merely un-preflighted; the in-process dispatch probe at 99d9ddebc proved the documented command form NEVER reaches `recoverNativeCoreHA` at all — `main.go:136-137` errors first (witness in the akte intake line). The missing `LoadRelease`/journal preflight confirmed by reading `recoverNativeCoreHA` (no catalog load between lock acquisition and `recoverOwnedCoreHA`).
- Current state, branch, PR and evidence links. Newest first.
