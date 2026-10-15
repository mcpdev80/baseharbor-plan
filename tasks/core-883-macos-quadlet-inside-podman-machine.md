---
id: core-883
type: feature
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-820]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#883"]
source_updated: "2026-10-15T16:49:24Z"
labels: [kind/feature, area/runtime, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-883 · macOS: run Quadlet inside Podman Machine #task #release/v0-4-29 #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-820](core-820-linux-host-adapters-regressions.md)  
**Required by:** [core-822](core-822-macos-darwin-adapters.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#883](https://github.com/mcpdev80/baseharbor/issues/883)
<!-- /generated:links -->

## Goal

Podman Machine on macOS reuses the existing Podman Quadlet realization, executed inside the Podman Machine Linux VM (decision 2026-10-14). No second Podman realization: no Docker-compat shortcut, no `podman kube play`/compose variant. Consumed by core-822.

## Scope

- Flow: native `baha` renders the same Quadlet units as on Linux → executor `podman machine` (ssh) → Fedora CoreOS VM (`~/.config/containers/systemd/*.container`, `systemctl --user`/`journalctl --user`, rootless workloads). Quadlet/systemd is never claimed to run natively on Darwin.
- Problem: the provider calls host commands/filesystem directly (~40 `exec`/`os.*` call sites in ~13 files, mainly `quadlet_runtime.go` (19), `quadlet_project.go`, `quadlet_images.go`, `lifecycle.go`, `quadlet_resources.go`, `quadlet_systemctl.go`; `quadletUserUnitDir()` resolves a local path). On macOS `QuadletAvailable` is false, so `podman.New` returns `ErrRuntimeNotFound` (`internal/providers/runtime/podman/provider.go:51`) — a dead-end diagnostic for an installed Podman.
- Work: (1) narrow provider-internal executor seam (run a command, read/write/remove a unit file, resolve unit directory and `XDG_RUNTIME_DIR`) with `local` (today's Linux behavior, byte-for-byte) and `machine` (selected machine via `podman machine ssh <name>` or its ssh identity/port from `podman machine inspect`); not part of the Host Platform Contract, not generic remote exec, not exposed via MCP; bound to the explicitly selected machine/endpoint and verified owner; verify SSH identity/host boundary, unit-directory ownership and path mappings; no fallback to another machine, host daemon or unchecked SSH destination. (2) Machine discovery/selection: default or the Target's explicit machine; running/stopped; observed privilege plus positively verified VM execution/isolation (D1); never infer isolation from rootful status; systemd/Quadlet generator availability in the VM. (3) Path mapping: bind-mount sources must be visible in the VM (`$HOME` via virtiofs by default); other paths fail before mutation with a typed diagnostic naming the path and the `podman machine` volume remedy. (4) Ownership/evidence parity: labels, unit names, owned-resource removal, retirement, logs and explorer units as on Linux; never trust the macOS host for VM-side state. (5) Typed diagnostics instead of `ErrRuntimeNotFound`: Podman not installed, no machine, machine stopped, Quadlet unavailable in VM, path not shared — each with a next action.
- Out of scope: Quadlet/systemd in the Host Platform Contract; Podman Desktop APIs (plain `podman machine` only); Windows/WSL2 Podman Machine (core-821).

## Acceptance

- One Podman realization; the `machine` executor produces the same units and ownership as `local`.
- Linux Podman acceptance unchanged.
- Real macOS Podman Machine Dev Local journey passes on an exact SHA.
- Every Podman Machine failure mode is typed and actionable; no `ErrRuntimeNotFound` for an installed Podman.
- Endpoint/machine mismatch, unknown VM provenance, changed SSH/owner boundary and unauthorized host path/socket sharing are rejected with typed diagnostics under D1.

## Required checks

- Unit: fake executor conformance with identical rendered units and command sequences for `local` and `machine`.
- Linux: rootless Podman/Quadlet acceptance stays green.
- macOS: real Podman Machine Dev Local journey on the self-hosted runner (core-884): init/plan/up/status/doctor/logs/sql/cache/owned destroy plus negatives (stopped machine, unshared path, missing machine).

## Dependencies and file ownership

- Depends on core-820 (and the D1 review in core-819). Owns the executor seam inside `internal/providers/runtime/podman/`.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
