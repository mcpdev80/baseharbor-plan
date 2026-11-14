---
id: t-20261113-remote-installation-destroy
card_number: "0427-188"
card_short_title: "destroy remote Core"
type: task
areas: [cli, lifecycle, runtime]
release: v0.4.27
version: ""
parent: ""
owner: cg-s3 (Codex)
kanban_status: closed
kanban_lane: closed
kanban_summary: baha destroy invoked on a developer workstation must permanently remove the BaseHarbor-owned installation reached through its…
kanban_title: 0427-188 · destroy remote Core
priority: "high"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1532]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/pull/1532, https://github.com/mcpdev80/baseharbor/commit/8c2595ae04fc6388d46593b1e725817518dee2e8, https://github.com/mcpdev80/baseharbor/actions/runs/43552949871]
---

- [x] t-20261113-remote-installation-destroy · Lifecycle: destroy remote Core installations from the workstation #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/cli #area/lifecycle #area/runtime #kind/task
    <!-- generated:card -->
    **Owner:** cg-s3 (Codex) · **Priority:** high  
    **PR:** [baseharbor#1532](https://github.com/mcpdev80/baseharbor/pull/1532)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1532), [proof 2](https://github.com/mcpdev80/baseharbor/commit/8c2595ae04fc6388d46593b1e725817518dee2e8), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/43552949871)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** cg-s3 (Codex)  
**Priority:** high  
**PRs:** [baseharbor#1532](https://github.com/mcpdev80/baseharbor/pull/1532)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha destroy` invoked on a developer workstation must permanently remove the BaseHarbor-owned installation reached through its authenticated Core Target, including applications, providers, Core runtime and local connection/trust state. It must retain explicit plan-bound consent, verify the remote cleanup, preserve application source repositories and foreign state, and continue to support local Targets.

## Scope

- In scope: workstation-side orchestration for configured authenticated Core Targets; remote authoritative inventory and execution; explicit current-plan consent; post-destroy verification and cleanup of workstation-owned target connection, hosts and CA state; local-target parity.
- Out of scope: `app destroy` semantics, remote Connector lifecycle, new runtime/provider support, unrelated install or release readiness work.

## Acceptance

- From the developer workstation, one selected remote Core Target can be fully inventoried, explicitly approved, destroyed and verified without running `baha` on the Core host.
- Remote failure, stale plan, missing authentication, unreachable Target or incomplete ownership inventory fails closed and preserves retry/ownership state; no local fallback or partial success claim.
- Remote full destroy removes the exact workstation-owned connection profile, managed hosts entries and verified CA trust only after Core cleanup succeeds; foreign host state and authored source repositories remain untouched.
- Local Docker and Podman full-destroy behavior remains supported and unchanged.
- A human-readable `local/prod` context is never inferred for a `dev`-only installation; default authorization context is `dev`, with an explicit selected environment required for another context.

## Required checks

- Add exact remote full-destroy CLI/Core HTTP journey tests for plan/consent, successful teardown, lost connection/retry and no-mutation failure, plus local Docker/Podman regressions.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha` full-destroy client orchestration and Core machine HTTP destroy execution; focused runtime/authorization tests; task handoff.
- Shared files: coordinate through the owning task.

## Handoff

- Product branch `fix/remote-installation-destroy` is at exact source SHA `b0c812fe106bf244ad6f07bac42ef4db3317d2cf`, based on `develop` `197ece9843e0563f75dd47adb8bed3a12089f973`. Draft PR [#1532](https://github.com/mcpdev80/baseharbor/pull/1532) is open.
- Local verification passed: `go test ./cmd/baha -run 'Test(RemoteInstallationDestroy|FullDestroy|InstallationDestroy|SecondSameHost)'`; `go test ./internal/machinehttp`; `go vet ./cmd/baha ./internal/machinehttp`; CLI build; `scripts/source-readability-audit.sh`; generated machine documentation test; EN/DE integrity and page parity; CI impact selector test.
- Exact test-to-CI routing: `cmd/baha` remote journey tests `TestRemoteInstallationDestroyReviewsAndExecutesExactPlan` and `TestRemoteInstallationDestroyRejectsStaleConsentBeforeMutation`, plus terminal/idempotency transport tests, run in existing Draft Go CLI shards; `internal/machinehttp` terminal receipt/idempotency tests run in the Draft Go packages lane. PR `b0c812fe` was selected by the Draft workflow; at handoff these jobs were queued/running, so no CI result is claimed yet.
- Local parity tests `TestFullDestroyRemovesOwnedLocalStateButPreservesSourceRepository`, `TestFullDestroyRemotePhaseExcludesOnlyRemoteTargetsAndKeepsLocalTarget`, and `TestFullDestroyRefusesMultipleRemoteCoresBeforeMutation` are included in the CLI package tests. `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and `TestSecondSameHostCoreNativeConflictInCI` are selected through `scripts/ci-single-default-impact.sh` and executed by the existing native installation-destroy gate on both Docker and rootless Podman. The impact-selector positive/negative proof passes locally. Draft policy currently skips those native gates; they must actually run on PR ready and pass before acceptance.
- **Maintainer acceptance (2026-11-14):** PR #1532 merged to `develop` as `8c2595ae04fc6388d46593b1e725817518dee2e8`. Exact PR candidate `57f7cbd0ec03fa3b68f41bc4de6aa98231e3d8a7` passed selected CI in run [43552949871](https://github.com/mcpdev80/baseharbor/actions/runs/43552949871): remote plan/consent and stale-consent no-mutation tests passed in the CLI shards; local installation-destroy retry passed on native Docker and rootless Podman; selected checks passed. Current candidate `develop` `65c88f3305b5d94535d37c12af49739f29fe8a07` contains merge commit `8c2595ae`. `remoteJourneyFixture` exercises the workstation CLI against the Core machine-HTTP journey fixture; native gates exercise local Docker/Podman cleanup. No live user workstation, VM, or Core was destroyed. This satisfies the task's required test and CI routes; it does not claim a separate live remote-VM teardown.

The Owner-authorized Maintainer accepts this task on the exact merged source and recorded results. This is not an independent review claim.
