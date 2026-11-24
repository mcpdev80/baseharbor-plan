---
id: t-20261124-r28-release-candidate-testonly-binary
card_number: "0428-269"
card_short_title: "release ships no testonly"
type: task
areas: [ci, release, testing, platform]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Produce baha-ci-operator-testonly in the candidate artifact the pre-release runtime suite consumes, so a release runtime gate…"
kanban_title: 0428-269 · release ships no testonly
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-release-candidate-testonly-binary · The release candidate artifact never contains baha-ci-operator-testonly, so every release runtime gate fails its test -s under set -e. #task #release/v0-4-28 #status/planned #view/ready #area/ci #area/platform #area/release #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261122-runtime-image-registry-artifact-unknown](t-20261122-runtime-image-registry-artifact-unknown.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Produce `baha-ci-operator-testonly` in the candidate artifact the pre-release runtime suite consumes, so a release runtime gate can run the test-only operator instead of dying on the binary-presence check. Witnessed on develop 3ebfb90d (bughunt-hv26 F1):

- `.github/workflows/pre-release.yml:491-501` ("Build exact candidate binary") builds and uploads only `baha` into `pre-release-source-candidate`; the string `baha-ci-operator-testonly` occurs ZERO times in that file.
- The `runtime_candidate` job (`.github/workflows/pre-release.yml` ~575-636) re-downloads that source artifact, builds the runtime image and uploads `pre-release-runtime-candidate` — which therefore never carries the test-only binary.
- `.github/workflows/pre-release-runtime-suite.yml:315-318` does `testonly="$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly"`, then `test -s "$testonly"` under `set -euo pipefail` and `"$testonly" version | grep -F "$CANDIDATE_SHA"`. Every runtime-class gate dispatched with `candidate_artifact: pre-release-runtime-candidate` (pre-release.yml:716, 745, 794, 823) hits that line whenever `reuse_from` is empty.
- Contrast: the CI path builds the binary correctly once per PR head in `pr_candidate` (`.github/workflows/ci.yml:1141-1153`), including the same `version | grep -F "$GITHUB_SHA"` identity proof. So PR runtime gates get the operator and release runtime gates do not.

## Scope

- In scope: building `baha-ci-operator-testonly` in the release candidate path with the same flags and identity proof as `pr_candidate`, and placing it in the artifact the runtime gate consumes.
- Out of scope: changing gate semantics, the `test -s` contract itself, `reuse_from` behaviour, or a source-build fallback inside the gate (rejected earlier; the binary must come from the candidate artifact).

## Acceptance

1. A release run of `.github/workflows/pre-release.yml` puts `baha-ci-operator-testonly` into the artifact consumed at `pre-release-runtime-suite.yml:315`, and that binary answers `version` with the exact `CANDIDATE_SHA`.
2. At least one Docker and one rootless Podman runtime-class release gate execute to a terminal green with `reuse_from` empty, so `pre-release-runtime-suite.yml:316` is proven satisfied by a real run rather than by reused evidence.
3. The evidence names the workflow, job, tested head SHA and run URL that executed each gate (AGENTS 5.3).

## Dependencies and file ownership

- Owned files or areas: `.github/workflows/pre-release.yml`, and `.github/workflows/pre-release-runtime-suite.yml` only if the artifact contract moves. Both are Owner scope.
- Shared files: none. No product Go code, no `scripts/**` changes.

## Handoff

- OWNER SCOPE: the fix is a `.github/**` change; per CI policy (Owner directive 2026-11-19) a lane reports this need and the Owner implements it. This card exists so the need, the file:line and the acceptance proof are tracked instead of being rediscovered per release run.
- This is the pinned root cause of 0428-249 / baseharbor#1812 (light-gate failure): that card is blocked behind this one and rebases onto its outcome instead of widening its own PR.
- Source: bughunt-hv26 F1 dossier `evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (develop 3ebfb90d).
