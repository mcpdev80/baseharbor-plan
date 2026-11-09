---
id: t-20261023-appid-test-env-dep
card_number: "0427-072"
card_short_title: "external Prov registry test"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle3 (lane w38)
kanban_lane: closed
kanban_summary: "TestExternalProviderRemoval (and any provider-registry ownership checks) pass or fail based on the code's ownership logic alone…"
kanban_status: closed
kanban_title: "0427-072 · external Prov registry test"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1351"]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1351b.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1351a.md"]
---

- [x] t-20261023-appid-test-env-dep · Defect: external provider registry test unverifiable-ownership outside CI runners #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle3 (lane w38)  
    **PR:** [baseharbor#1351](https://github.com/mcpdev80/baseharbor/pull/1351)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1351b.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1351a.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle3 (lane w38)  
**Priority:** not set  
**PRs:** [baseharbor#1351](https://github.com/mcpdev80/baseharbor/pull/1351)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestExternalProviderRemoval*` (and any provider-registry ownership checks) pass or fail based on the code's
ownership logic alone — identical results in a local isolated run (TMPDIR/XDG under /tmp/opencode) and on a
hosted runner — with no reliance on CI-runner ambient state. Documented failure `provider-registry-ownership-unverifiable`
must only occur for genuinely unverifiable state, never because the environment lacks a runner hint.

## Scope

- In scope: test fixtures/helpers in `internal/**` and `internal/testsupport/**` that seed provider-registry
  ownership state; deterministic setup/teardown independent of ambient env.
- Out of scope: `.github/**` and `scripts/**` (Owner's CI territory); product runtime behavior changes; the
  app.id parser fixture (t-20261020) and the CI-planner lane (#1047).

## Acceptance

- `TMPDIR=/tmp/opencode go test ./cmd/baha -run 'TestExternalProviderRemoval' -count=1` passes locally with
  no CI-only skips; the same command passes on the hosted PR run of the same head.
- No test asserts via ambient CI markers; ownership state is seeded by fixtures explicitly.
- Evidence file lists local run output and the hosted run id/url for the identical head.
- Reviews' repeated note "pre-existing env fail, equal on clean develop" is resolved: clean develop run of
  the fixed test is green.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- 2026-10-24 (o113): resolution documented here only; the schema forbids a free-text resolution on a non-checked card. State remains waiting — external provider-registry test is unverifiable outside CI runners, depends on unaccepted v0.4.27 release-start updates.

### Coordinator scope clarification (2026-11-03, review-1351a)

The ownership-seeding fixture lives in cmd/baha test files; touching TEST files under cmd/baha/ is
within this card's scope (no non-test cmd files, no .github/scripts). Recorded so scope checks
judge the candidate against the real defect location.
