---
id: core-822
areas: [platform]
type: feature
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-820, core-883, core-884, t-20261017-release-0-4-29-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#822"]
source_updated: "2026-10-15T16:50:17Z"
labels: [kind/feature, area/runtime, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-822 · macOS: implement and qualify Darwin adapters #task #release/v0-4-29 #status/planned #view/waiting #board/planned #area/platform #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [core-820](core-820-linux-host-adapters-regressions.md), [core-883](core-883-macos-quadlet-inside-podman-machine.md), [core-884](core-884-tests-macos-runtime-real-mac.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-820](core-820-linux-host-adapters-regressions.md), [core-883](core-883-macos-quadlet-inside-podman-machine.md), [core-884](core-884-tests-macos-runtime-real-mac.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
**Required by:** [core-823](core-823-tests-platform-conformance-support.md), [t-20261017-release-0-4-29-prepare](t-20261017-release-0-4-29-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#822](https://github.com/mcpdev80/baseharbor/issues/822)
<!-- /generated:links -->

## Goal

Implement and qualify the native macOS/Darwin Host Platform adapter and the macOS Dev Local journey without claiming runtime support that is not proven.

## Scope

- Architecture: macOS host runs native `baha`; Docker Desktop / Podman Machine run a Linux VM with the workloads. Physical Mac capacity and effective VM capacity are different sources.
- Native Darwin semantics: identity, state/config/data paths, filesystem permissions, browser opening (reuse the contract), trust/keychain capability, secure ephemeral material, terminal/PTY, runtime discovery, self-update selection.
- Runtime VM semantics: preflight uses effective VM allocation; binary presence does not imply lifecycle support; host trust ≠ runtime/workload trust; unavailable VM information fails explicitly instead of using total Mac RAM.
- Release scope: full Dev Local on darwin/arm64 with **both** Docker Desktop and Podman Machine (runtime qualification via core-884, independent walkthrough); darwin/amd64 artifacts/build/native conformance only; manual trust export/instructions and read-only verification in scope; automatic Keychain trust and macOS Dev Remote deferred to core-886, signing/notarization to core-885; hosted Darwin tests prove host behavior, core-884 proves container lifecycle, core-823 tracks the four lanes; D1/D2 extensions need core-819 review; same canonical commands/wizard, optional Dev Local login, ownership and TLS checks; failures name the engine/VM, missing capability and the user action; docs explain VM sizing, file sharing, manual trust and current support.
- Work packages: (1) build — core-882; (2) distribution — `darwin/arm64` and `darwin/amd64` in `.goreleaser.yaml`, `scripts/install.sh` accepts `Darwin`, `cmd/baha/update.go:179` allows darwin, `release.yml` attestation covers `baseharbor_darwin_*`, checksums include darwin; no notarization (D5), verify ad-hoc signing per architecture, installer/update integrity and clean-Mac quarantine/Gatekeeper behavior; (3) Docker Desktop engine (D1) — context/socket only as discovery hints, positively bind endpoint to its running owned VM, report privilege and VM isolation separately, keep explicit rootful-host opt-in, socket deny-list (`internal/application/workload_security.go:308`) covers engine-reported sockets; (4) capacity (D2) — engine-reported VM capacity replaces `hostresource.ReadLinux()` on darwin (`cmd/baha/app_memory_preflight.go:79`) and the direct `/proc` reads in `cmd/baha/tui_host_resources.go`; results carry source, freshness, limits and quality; remediation names the VM setting (Docker Desktop resources, `podman machine set --memory`); (5) Podman Machine — core-883; (6) PTY — darwin `internal/runtime/terminal` and removal of the `GOOS == "linux"` gate in `internal/runtimeexplorer/terminal.go:59`; (7) paths — one documented macOS policy, recommended: keep the XDG-style layout and move outliers (`internal/operatorauth/config.go:110` → `os.UserCacheDir()`, backup default path) onto it; (8) file sharing — verify repository and bind-mount sources are shared into the VM before mutation, else a typed diagnostic naming path and setting; (9) browser/networking — consolidate the two GOOS browser switches (`cmd/baha/human_open.go`, `internal/operatorauth/login.go`); audit macOS IPv6-first resolution against the IPv4-only gateway and prove browser/curl reachability; (10) honest identity — `internal/health/doctor.go:28` and `cmd/baha/control_plane_operations.go:148` report the evidence-based support level; `baha node install` on darwin returns typed unsupported (`cmd/baha/node.go:731`); (11) arm64 stack lane in core-823 (spot check 2026-10-14: `spilo-18:4.1-p2`, `openbao:2.7.1`, `etcd:v3.7.2`, `baseharbor-runtime:edge` publish linux/arm64); (12) EN/DE docs — macOS getting-started for both engines, VM sizing, file sharing, manual trust, support matrix rows.

## Acceptance

- `install.sh` installs and `baha update` updates darwin/arm64 and darwin/amd64 from published, checksummed and attested artifacts.
- Docker Desktop is classified `vm-isolated` and runs the Dev Local journey without manual mode flags.
- Podman Machine runs the Dev Local journey through core-883.
- Both journeys pass on darwin/arm64 on one exact SHA via the self-hosted runner (core-884), including negatives: stopped VM, VM memory below the plan, unshared path, missing runtime/machine.
- Browser and `curl` reach `https://*.baha.localhost` on macOS; manual trust steps documented and trust status reported read-only.
- Doctor/control-plane output shows the evidence-based macOS support level.
- VM identification/access/ownership and file-sharing negatives satisfy D1; incomplete memory estimates never establish SAFE under D2.
- Independent macOS Dev Local walkthrough passes using EN/DE public guidance.

## Required checks

- Hosted macOS native build/test and contract conformance on ARM64 and Intel where practical; real runtime journeys on core-884.

## Dependencies and file ownership

- Depends on core-820, core-883 and core-884 (D1/D2 review in core-819). Owns Darwin adapters, distribution changes and macOS docs.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
