---
id: t-20261119-r28-app-source-verification-none-ignored
kanban_title: 0428-143 · Verification=none is ignored
card_number: "0428-143"
type: bug
areas: [metrics, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: blocked
kanban_lane: blocked
blocker: "Pre-existing behaviour on develop, not introduced by 0428-123: the provider loop skips sources whose Verification mode is none, the application loop does not. Changing it alters the up-sample obligation for application-class sources, so it needs an explicit contract decision before any lane edits code. Witnesses in the note below. Next trigger: owner decision plus a free seat after #1693 and #1599"
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/blob/fac01c77276ca2bf1e20cd0b7334bda5dd43e353/internal/metrics/prometheus_verify.go"
resolution: ""
created: 2026-11-19
card_short_title: Verification=none is ignored
---

- [ ] t-20261119-r28-app-source-verification-none-ignored · Verifier: Verification=none is ignored for application-class metrics sources #task #release/v0-4-28 #status/blocked #view/blocked #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Blocker:** Pre-existing behaviour on develop, not introduced by 0428-123: the provider loop skips sources whose Verification mode is none, the application loop does not. Changing it alters the up-sample obligation for application-class sources, so it…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/fac01c77276ca2bf1e20cd0b7334bda5dd43e353/internal/metrics/prometheus_verify.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this exists

0428-123 (metrics registration load-bearing) reviewed the app-class append path on develop and the
reviewer reported an asymmetry in the verifier. The coordinator re-read the code on develop and
confirmed it. No lane claim is involved; the finding predates 0428-123.

## Witnessed code state (develop fac01c77276ca2bf1e20cd0b7334bda5dd43e353)

- `internal/metrics/prometheus_verify.go:153` - app sources are listed with the environment threaded
  through: `applicationSources, err = observability.ListApplicationMetrics(placement, allowedApplications, m.Environment)`
- `internal/metrics/prometheus_verify.go:174` - application loop: `for _, source := range applicationSources {`
  followed by `waitForMetricsSource(ctx, client, endpoint, query, source.ID, "application", queryProvider)`.
  This loop has **no** `if source.Verification == capability.ObservabilityVerifyNone { continue }` guard.
- `internal/metrics/prometheus_verify.go:185` - provider loop **does** carry exactly that guard.
- `internal/capability/integration_contract.go:37` defines `ObservabilityVerificationMode` and its modes.

## Consequence

`ListApplicationMetrics` returns all app-class sources for the placement. A source whose `Verification`
mode is `none` is excluded from exported `ListMetrics` output, yet `verifyProviderSourcesAt` still
waits for it as a required `up` sample. So `Verification=none` does not mean "no verification" for
application-class sources, while it does for provider-class sources.

## Decision needed before implementation

- Option A - uniform semantics: `Verification=none` means no verification everywhere; the application
  loop gets the same guard plus a regression test seeding an app-class source with `Verification=none`.
- Option B - documented asymmetry: app-class sources are always load-bearing; the contract text states
  that `Verification` is not a verifier switch for app sources, so nobody reads it as one again.

## Acceptance

- A CI-executed regression test in the package that owns the verifier proves the chosen semantics for
  an application-class source with `Verification=none` (test ID mapped to its gate per the CI intake rule).
- The contract text states the semantics in one place; no silent behaviour change.
