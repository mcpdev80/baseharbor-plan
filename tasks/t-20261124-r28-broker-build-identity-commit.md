---
id: t-20261124-r28-broker-build-identity-commit
card_number: "0428-271"
card_short_title: "broker identity version-only"
type: bug
areas: [runtime, lifecycle, cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w60-0428-271-brokerid
kanban_status: review
kanban_lane: review
kanban_summary: The apply/verify readiness probe either proves the runtime broker is the exact candidate commit or surfaces the commit…
kanban_title: 0428-271 · broker identity version-only
priority: normal
depends_on: [t-20261124-gate-catalog-baseline-1820]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1820]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-24/broker-build-identity-w60/evidence.md
---

- [ ] t-20261124-r28-broker-build-identity-commit · verifyRuntimeBrokerBuildIdentity discards both commit SHAs, so a runtime broker at the wrong commit passes readiness whenever the semver matches. #task #release/v0-4-28 #status/review #view/review #area/cli #area/lifecycle #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** w60-0428-271-brokerid · **Priority:** normal  
    **PR:** [baseharbor#1820](https://github.com/mcpdev80/baseharbor/pull/1820)  
    **Needs:** [t-20261124-gate-catalog-baseline-1820](t-20261124-gate-catalog-baseline-1820.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-24/broker-build-identity-w60/evidence.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261124-gate-catalog-baseline-1820](t-20261124-gate-catalog-baseline-1820.md)  
**Owner:** w60-0428-271-brokerid  
**Priority:** normal  
**PRs:** [baseharbor#1820](https://github.com/mcpdev80/baseharbor/pull/1820)  
**Source:** 
<!-- /generated:links -->

## Goal

The apply/verify readiness probe either proves the runtime broker is the exact candidate commit or surfaces the commit divergence as a named condition instead of silently dropping it. Witnessed on develop 3ebfb90d (bughunt-hv26 F4):

- `cmd/baha/app_broker.go:652-672`, `verifyRuntimeBrokerBuildIdentity(actualVersion, actualCommit string)`: fails closed on an empty version (`:658-660`), enforces the version match with the `dev`/`edge` development-pair exception (`:661-666`), then discards provenance via `_ = expectedCommit` / `_ = actualCommit` (`:668-669`) under the comment "Commit SHAs are build provenance, not a runtime compatibility contract."
- Call sites: the readiness probe at `cmd/baha/app_broker.go:641` (`verifyRuntimeBrokerBuildIdentity(ready.Version, ready.Commit)`) inside `verifyRuntimeBrokerRunning` (`:192`), reached from the apply/verify loop.
- The candidate path pins provenance everywhere else: the CI candidate job builds the image with `BASEHARBOR_SOURCE_REF=$CANDIDATE_SHA`, and `pre-release-runtime-suite.yml:318` requires the candidate binary `version` to contain `$CANDIDATE_SHA`. So an image built from a different commit at the same semver is accepted by this probe.

## Acceptance

1. The commit comparison becomes a real check with an explicit, narrow contract rather than `_ = actualCommit`: at minimum the readiness path fails closed, or reports a distinct named incompatibility, when the CLI carries a non-development candidate commit and the broker reports a different non-empty commit; the single place that defines which combinations are legitimately allowed (patch/docs-only rebuilds, the `dev`/`edge` pair) is documented at that function.
2. One regression test per direction in `cmd/baha`: same version and same commit passes; same version with a different commit fails (or records divergence as designed); the `dev`/`edge` pair with an empty commit stays green. The different-commit test must be RED against the current discard-the-SHA behaviour.
3. The test is picked up by the CI group that covers `cmd/baha` ("PR · Go unit"); the evidence names job, trigger and run URL (AGENTS 5.3).

## Boundaries

`cmd/baha/app_broker.go` (identity function, its call site, its tests) and, if the contract needs it, the readiness field that carries `Commit`. No change to the version-compatibility rule itself, no image-build provenance machinery, no `.github/**` or `scripts/**` edits.

## Related

- bughunt-hv26 F4 rated this low/medium: a documented by-design weakening rather than a crash or false-green in the normal path. It is filed as a card so the provenance-strength decision is explicit instead of a discarded parameter.
- Source: bughunt-hv26 F4 dossier `evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (develop 3ebfb90d).

Dispatched w60 (ornith, dep-free). Fix verifyRuntimeBrokerBuildIdentity to prove exact candidate commit (currently drops both SHAs; wrong-commit broker passes on semver). Write-set disjoint check first; scripts/.github untouched (catalog owner-scope). Hosted, merge-frost. Card BLOCKED on 0428-274 catalog owner-baseline: the regression test file needs a coverage-catalog row (scripts/ = #1817 owner-scope); fix + regression + build/vet + PR #1820 (head f5e50f5a) complete. On 0428-274 landing: rebase fix/broker-build-identity onto develop, push, mark #1820 ready, re-run exact-head CI.

head 514084f3c up-to-date on develop 05ef48536, 19 PASS/0 FAIL, MERGEABLE; routed to CODEX-REVIEW+MERGE.
