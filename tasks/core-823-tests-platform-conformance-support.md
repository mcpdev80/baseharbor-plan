---
id: core-823
type: acceptance
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-821, core-822, core-884]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#823"]
source_updated: "2026-10-15T16:50:10Z"
labels: [kind/acceptance, area/runtime, area/evidence, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-823 · Tests: verify platform conformance and support #task #release/v0-4-29 #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-821](core-821-wsl2-host-behavior-windows-boundaries.md), [core-822](core-822-macos-darwin-adapters.md), [core-884](core-884-tests-macos-runtime-real-mac.md)  
**Required by:** [core-817](core-817-audit-host-portability-architecture.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#823](https://github.com/mcpdev80/baseharbor/issues/823)
<!-- /generated:links -->

## Goal

A reusable conformance suite, CI matrix and support/evidence rules keep platform claims aligned with what BaseHarbor actually tests.

## Scope

- Conformance matrix (refine from implementation evidence):

| Semantic | Linux | Windows native | WSL2 | macOS |
| --- | --- | --- | --- | --- |
| platform identity | real | real | detected | real |
| state/config paths | real | real | real fixture/acceptance | real |
| filesystem safety | real | real | real fixture/acceptance | real |
| effective resource evidence | real | host/client only | WSL2/runtime | runtime VM aware |
| trust operations | real | capability/backend | split host/WSL | Keychain/capability |
| browser handoff | real | real | explicit boundary | real |
| secure ephemeral material | real | real | real | real |
| runtime discovery | Docker/Podman | classified | real when available | classified |
| full runtime E2E | Docker/Podman | evidence required | evidence required | evidence required |

- CI: Linux reuses static/source, Docker and rootless Podman gates; native Windows hosted gate for build/unit/conformance; macOS hosted gates (ARM64 and Intel where appropriate); WSL2 never faked — document a dedicated/self-hosted lane and keep status below TESTED until it passes. Four distinct evidence lanes (D4): Darwin cross-build, native Darwin conformance, Linux/arm64 container stack, real macOS runtime (core-884).
- Architecture guard: generic/core packages gain no new direct `runtime.GOOS` policy branching, `/proc` dependencies, Linux trust commands, Windows/macOS system commands or platform-specific path constants outside approved adapters or justified runtime-provider directories.
- Support levels with evidence-backed transitions: SUPPORTED (full acceptance for the claimed use case), TESTED (real execution for a defined subset), PORTABILITY-VERIFIED (native contract/build/conformance without full lifecycle proof), EXPERIMENTAL, UNSUPPORTED.
- No dead ends: failures state what capability is unavailable, why on this platform/topology, and the safe next action (run inside WSL2, start Docker Desktop, allocate VM memory, install/export trust manually, choose a supported runtime, use a remote Target/Node Connector).

## Acceptance

- One shared conformance suite.
- Linux CI remains authoritative for Linux support.
- Windows native CI exists.
- macOS native CI exists.
- The WSL2 real-evidence requirement is explicit.
- The architecture guard blocks new host leakage.
- Docs/support matrix is generated or audited against CI evidence where practical.
- No platform is promoted beyond its evidence.
- Failures are typed and actionable.
- Release gates can select the relevant platform proofs without multiplying full pre-release runs unnecessarily.

## Required checks

- The suite itself; per-lane receipts with exact source, runner, engine and OS versions.

## Dependencies and file ownership

- Depends on core-821, core-822 and core-884. Owns the conformance suite, matrix and support-level rules.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
