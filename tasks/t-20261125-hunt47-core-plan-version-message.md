---
id: t-20261125-hunt47-core-plan-version-message
card_number: "0428-348"
card_short_title: "provider version message"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "The Core update plan tells the truth about why a provider transition is unsupported: unknown ≠ downgrade, and a suffix that…"
kanban_title: 0428-348 · provider version message
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/coreupdate/plan.go
---

- [ ] t-20261125-hunt47-core-plan-version-message · 0428 hunt H-V47: uncomparable prerelease suffix + downgrade-mislabeling in coreupdate version classification #task #release/v0-4-28 #status/planned #view/ready #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/coreupdate/plan.go)  
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

The Core update plan tells the truth about why a provider transition is unsupported: unknown ≠ downgrade, and a suffix that carries no comparison meaning does not veto an otherwise strictly-newer numeric upgrade.

## Scope

- In scope:
  - `internal/coreupdate/plan.go:76-119` `compareProviderVersions`: its parser rejects every non-numeric component (e.g. `26.8.0-rc1`) with "unverifiable provider version", but the comparison loop never uses prerelease ordering — contrast the package's OWN contract `providerupgrade.ParseVersion` (internal/providerupgrade/version.go:15-35), which strips `-`/`+` suffixes and parses 2-3 numeric segments; the two parsers in one repo disagree about `26.8.0-rc1` (plan.go: unverifiable, version.go: equals 26.8.0 — the akte's example `26.8.0-rc1 > 26.8.0` "no precedence" is WRONG: plan.go never compares them, it errors). Reconcile on the documented `ParseVersion` semantics (or document the stricter rule where it is actually needed).
  - `plan.go:161-163` + `providerDowngrade` (`:177-180`): when the installed version fails to parse, the classification says "Core provider downgrade or unverifiable version" (the downgrade word applies to a strictly-newer-target case where nothing was downgraded). Split the two cases in the Reason string; the fail-closed Unsupported classification itself stays (guard comment plan.go:74-75 is correct policy).
  - `ha_spilo_compose.go:30` mirrors the same "unknown, major-changing or downgraded" conflation — same treatment.
- Out of scope:
  - Any change to what is admitted (still fail-closed); the `written_by`/message-direction surface (0428-345/347).

## Acceptance

- `TestProviderVersionComparisonFailsClosed` (internal/coreupdate/plan_test.go:105) is extended in place (intake note: it already pins `{"26.8.0-rc1","26.8.0", true}` — keep that outcome, fix only the message and the parser contract).
- Classification tests name the three directions distinctly: verified downgrade, verified upgrade, unverifiable version — table-driven, no real runtime.
- The providerupgrade version-parse contract is referenced (file:line) in the plan.go comment so the parsers cannot drift again.

## Required checks

- **Modified features:** internal/coreupdate plan tests (auto-discovered unit lane).
- **New tests:** the direction table above.
- **CI integration and mapping:** no `.github/**` change.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `internal/coreupdate/plan.go`, `ha_spilo_compose.go`, their tests.
- Shared files: none.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-6 LIVE with two intake corrections: (1) the message conflation is confirmed by direct `Build` probe (installed `17.9-aarch64`, target `18.1` → Unsupported "Core provider downgrade or unverifiable version" — an actually-newer target reported as a downgrade); (2) the akte's cross-parser example is wrong — `26.8.0-rc1` vs `26.8.0` never reaches comparison (parse error), while `providerupgrade.ParseVersion` accepts it as 26.8.0; the real defect is two contradictory parsers in one repository.
- Current state, branch, PR and evidence links. Newest first.
