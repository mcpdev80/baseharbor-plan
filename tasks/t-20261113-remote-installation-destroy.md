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
kanban_status: active
kanban_lane: active
kanban_summary: baha destroy invoked on a developer workstation must permanently remove the BaseHarbor-owned installation reached through its…
kanban_title: 0427-188 · destroy remote Core
priority: "high"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-remote-installation-destroy · Lifecycle: destroy remote Core installations from the workstation #task #release/v0-4-27 #status/active #view/active #area/cli #area/lifecycle #area/runtime #kind/task
    <!-- generated:card -->
    **Owner:** cg-s3 (Codex) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** cg-s3 (Codex)  
**Priority:** high  
**PRs:** none  
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

- Current state: confirmed missing remote path at merged SHA `197ece9843e0563f75dd47adb8bed3a12089f973`; CLI `baha app destroy` routes remotely but installation-wide discovery calls native `detectRuntimeForTarget` and rejects remote Targets. VM inventory currently contains only `local/dev`; no `prod` deployment is registered. No live resources were removed.
- Product branch: `fix/remote-installation-destroy`, based on `develop` SHA `197ece9843e0563f75dd47adb8bed3a12089f973`.
- Required gates: exact remote HTTP journey selection in existing CLI checks; Docker and rootless Podman native destroy-retry gates for local parity. Record exact test -> gate -> trigger -> run/SHA before handoff.
