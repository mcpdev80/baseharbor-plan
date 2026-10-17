---
id: core-820
areas: [platform]
type: feature
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-819, t-20261017-release-0-4-29-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#820"]
source_updated: "2026-10-15T16:50:29Z"
labels: [kind/feature, area/runtime, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-820 · Linux: integrate host adapters and verify regressions #task #release/v0-4-29 #status/planned #view/waiting #board/planned #area/platform #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [core-819](core-819-architecture-host-interface-guard.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-819](core-819-architecture-host-interface-guard.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
**Required by:** [core-821](core-821-wsl2-host-behavior-windows-boundaries.md), [core-822](core-822-macos-darwin-adapters.md), [core-883](core-883-macos-quadlet-inside-podman-machine.md), [t-20261017-release-0-4-29-prepare](t-20261017-release-0-4-29-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#820](https://github.com/mcpdev80/baseharbor/issues/820)
<!-- /generated:links -->

## Goal

Move current Linux host behavior behind the Host Platform Contract; Linux stays the fully qualified reference with no regression.

## Scope

- Preserve: effective memory evidence from `/proc/meminfo`; PSI where available; Linux CA trust-store integration; XDG/home state/config/data; Docker/Podman discovery; browser/client behavior; secure ephemeral secret handling; existing Docker and rootless Podman acceptance.
- Boundary: Quadlet/systemd stays a Podman Linux Runtime Provider realization; `systemd`, `systemctl`, Quadlet are not mandatory contract concepts (a narrowly justified service-facility capability is allowed if generic code truly needs it).
- Refactor targets: `internal/hostresource/`, `internal/hosttrust/`, `internal/health/doctor.go`, `internal/operatorauth/login.go`, state/path callers, secure ephemeral password-file path, update packaging/capability classification.
- macOS supplement (2026-10-14): **D2** — Linux keeps `/proc/meminfo` + PSI, available-memory evidence and cgroup limits, cross-checks the selected engine/VM, reconciles sources from the same environment; total is not available; the constraining budget governs; incomplete/stale/contradictory evidence never yields SAFE; preserve qualified native behavior. **D1** — native Linux `rootless`/`rootful` behavior and error texts unchanged; `vm-isolated` never inferred for a native Linux daemon. **D3** — the `local` executor (core-883) is byte-for-byte equivalent to today's Quadlet command and file sequence. **core-882** — Linux `memfd` + `/proc/self/fd` handoff and `TCGETS/TCSETS` unchanged after the build-tag split.

## Acceptance

- Linux host-dependent generic behavior routes through the contract.
- No regression in current Linux CLI/Core workflows.
- Docker acceptance remains green.
- Rootless Podman acceptance remains green, with the `local` executor from core-883.
- Linux-specific remediation stays actionable but does not leak into generic errors.
- Quadlet/systemd stays isolated to the Podman Linux realization.
- Linux remains SUPPORTED only with existing real runtime evidence.
- Linux capacity decisions unchanged on native engines; engine cross-check covered by unit fixtures.
- `vm-isolated` is never reported for native Linux daemons.
- Partial container-only usage, VM overhead, cgroup limits, stale/contradictory sources and physical-host/runtime mismatches have negative evidence tests.

## Required checks

- Unit/conformance against the Linux adapter; hostresource, trust, path/XDG and secret-safe ephemeral-file tests; existing Docker and rootless Podman/Quadlet acceptance; pre-release regression evidence.

## Dependencies and file ownership

- Depends on core-819. Owns the Linux adapters.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
