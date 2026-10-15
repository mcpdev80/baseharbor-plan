---
id: core-819
areas: [architecture]
type: architecture
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-882]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#819"]
source_updated: "2026-10-15T16:50:35Z"
labels: [kind/architecture, area/runtime, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-819 · Architecture: define the host interface and guard #task #release/v0-4-29 #status/planned #view/waiting #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-882](core-882-macos-fix-darwin-builds-build-vet.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-882](core-882-macos-fix-darwin-builds-build-vet.md)  
**Required by:** [core-820](core-820-linux-host-adapters-regressions.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#819](https://github.com/mcpdev80/baseharbor/issues/819)
<!-- /generated:links -->

## Goal

Inventory every real host-dependent call site and define the smallest Host Platform Contract that isolates platform mechanics from domain/lifecycle semantics. Owns the contract and seam, not platform feature completion.

## Scope

- Confirmed host assumptions: `internal/hostresource/memory.go` (`/proc/meminfo` + PSI); `cmd/baha/app_memory_preflight.go` (Linux remediation text); `cmd/baha/app_backup_restore_guided.go` (`/proc/self/fd/<fd>`); `internal/hosttrust/hosttrust.go` (auto trust only on Linux); `internal/operatorauth/login.go` (GOOS browser branch); `internal/health/doctor.go` (host OS and executable discovery); `cmd/baha/update.go` (Linux-only self-update); XDG/home conventions in runtime/deployment/orgconfig; Podman Quadlet `systemctl --user` (keep runtime-specific).
- Additional inventory (macOS supplement 2026-10-14):

| Call site | Host assumption | Proposed classification |
| --- | --- | --- |
| `cmd/baha/app_backup_restore_guided.go` | untagged `unix.MemfdCreate`, `TCGETS/TCSETS` → darwin does not compile | secure ephemeral material + terminal; fixed ahead in core-882 |
| `cmd/baha/tui_host_resources.go` | reads `/proc/meminfo`, `/proc/loadavg`, `/proc/pressure/memory` | presentation consumer of capacity evidence (D2) |
| `cmd/baha/human_open.go` | second GOOS browser-open switch | browser handoff; consolidate |
| `cmd/baha/control_plane_operations.go:148`, `internal/health/doctor.go:28` | report darwin/windows as `os` OK | identity/support level; no false green |
| `internal/runtime/terminal/process_other.go`, `internal/runtimeexplorer/terminal.go:59` | PTY "Linux only", `GOOS == "linux"` gate | terminal capability |
| `internal/runtime/docker_engine.go:51` | default `rootless`; Docker Desktop observed `rootful` | runtime engine observation (D1) |
| `internal/providers/runtime/podman/provider.go:51` | no host Quadlet → `ErrRuntimeNotFound` | Runtime Provider detail; core-883 |
| `internal/application/workload_security.go:308` | socket deny-list knows only Linux paths | runtime engine observation (engine-reported socket) |
| `internal/operatorauth/config.go:110` | sessions under `os.UserCacheDir()` while other state is XDG-style | filesystem/path policy |
| `cmd/baha/node.go:731` | `systemctl --user` for node install | Target/Node concern; typed unsupported off Linux |
| `.goreleaser.yaml`, `scripts/install.sh:27`, `release.yml:530` | linux-only artifacts, installer, attestation | distribution; core-822 |
| `internal/devgateway/gateway.go:504`, `render.go:63` | listen on `127.0.0.1` only, macOS resolves `*.localhost` to `::1` first | host networking; verify browser/curl path |

- Work: classify each call site (generic host semantic / Runtime Provider detail / Target Access / local presentation / portable stdlib needing no abstraction); define the minimum internal contract from demonstrated needs (candidates to evaluate: PlatformIdentity, HostResourceObservations, TrustStore, Filesystem, SecureEphemeralMaterial, BrowserOpen, TerminalCapabilities, ServiceCapabilities, RuntimeEnvironmentHints — prefer focused subinterfaces); deterministic fakes; architecture guard; typed capability/unsupported results with cause/remediation/next action.
- Contract review items before dependent implementation: **D1** and **D2** as defined in [v0.4.29](../releases/v0.4.29.md). Context/socket names are discovery hints, not proof of VM identity, ownership or safe file sharing. Host adapters supply host observations; the runtime/engine observer supplies selected runtime/VM evidence; admission consumes one resolved evidence model.
- Hard rules: no new Application Intent fields; no host OS names in portable contracts; no plugin framework; no duplicated Runtime Provider responsibilities; adapters may use GOOS/build tags internally, callers may not; unsupported is a typed result.

## Acceptance

- Inventory committed/documented.
- Every inventoried call site classified, including the additional rows.
- Minimum contract implemented.
- Fake platform test implementation exists.
- Architecture guard prevents new leakage, including direct `/proc` reads in `cmd/baha` presentation code and duplicate browser-open switches.
- No runtime/provider semantics were pulled into the host contract.
- Child Linux/Windows/macOS implementations can conform without changing portable semantics.
- D1 and D2 recorded in the pinned spec with review sign-off before core-820/core-822/core-883 depend on them.
- D1 rejects spoofed context names, mismatched endpoint/machine owners, unknown VM provenance and implicit rootful-host fallback.
- D2 distinguishes total/free/available/estimated memory and never promotes incomplete or stale runtime capacity to SAFE.

## Required checks

- Fake-platform conformance, architecture guard, unsupported-capability diagnostics, no-dead-end remediation tests, exact current Linux semantics captured before refactor.

## Dependencies and file ownership

- Depends on core-882. Owns the shared host interfaces; publishes the boundary before downstream work.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
