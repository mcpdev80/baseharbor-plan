---
id: core-818
title: Support host platforms
status: open
release: v0.4.29
parent: v0.4.29
sources: ["mcpdev80/baseharbor#818"]
---
# core-818 · Support host platforms

Source: [baseharbor#818](https://github.com/mcpdev80/baseharbor/issues/818). Release: [v0.4.29](../releases/v0.4.29.md) (authoritative scope and D1–D5). Child tasks: [views/epics.md](../views/epics.md). Final acceptance: v0.4.31 (#174).

## Goal

Define one small **Host Platform Contract** so BaseHarbor reasons about the machine/client platform without scattering Linux/Windows/macOS branches through Core, CLI, Runtime Providers or lifecycle code: BaseHarbor semantics → Host Platform Contract → Linux | Windows/WSL2 | macOS. It models only host concerns BaseHarbor genuinely needs; it is not a plugin framework.

## Why (current host assumptions)

`internal/hostresource/memory.go` reads `/proc/meminfo` and PSI; memory preflight tells users to check `/proc/meminfo`; guided backup/restore uses `/proc/self/fd/<fd>`; `internal/hosttrust` installs trust only on Linux; `baha update` self-updates Linux only; Podman Quadlet assumes `systemd --user` (a Runtime Provider concern); runtime discovery uses executable lookup; browser opening has Darwin/Windows branches; XDG/home/path assumptions need review; Docker Desktop / Podman Machine / WSL2 mean physical host capacity ≠ effective runtime capacity. Hotspots to inventory: `internal/hostresource/`, `cmd/baha/app_memory_preflight.go`, `cmd/baha/app_backup_restore_guided.go`, `internal/hosttrust/`, `internal/operatorauth/login.go`, `internal/health/doctor.go`, `cmd/baha/update.go`, `internal/runtime/stack.go`, `internal/deployment/target.go`, `internal/orgconfig/store.go`, `cmd/baha/path_prompt_linux.go`, `internal/providers/runtime/podman/`.

## Hard rules

- Portable Application Intent contains no host OS fields.
- Runtime Provider, Target Access Provider and Host Platform are separate axes.
- No `if GOOS == ...` branches in domain/lifecycle code.
- Linux runtime mechanics (Quadlet/systemd) stay inside the Podman Linux realization.
- Physical host resource values are not used when workloads run inside WSL2, Docker Desktop or Podman Machine with a smaller allocation.
- Unsupported host capabilities fail explicitly with typed actionable diagnostics.
- No support claim without matching evidence. Vocabulary: SUPPORTED, TESTED, PORTABILITY-VERIFIED, EXPERIMENTAL, UNSUPPORTED (align with the existing platform-support classification).

Platforms: Linux is the reference host, migrated without regression. **Windows in v0.4 = Linux `baha` inside real WSL2 only**; native Windows client ≠ WSL2 execution environment; Windows-runner checks are supplementary. macOS: native Darwin `baha` with VM-backed runtimes; effective resources come from the runtime VM.

## Order (macOS supplement 2026-10-14)

core-882 (ahead) → core-819 (+ D1/D2 review) → core-820 → (core-821 WSL2 ∥ core-822 macOS + core-883 Podman Machine) → core-823 (+ core-884 runtime lane) → core-817 audit. Follow-ups outside v0.4.29: core-885 signing/notarization, core-886 Keychain trust and macOS Dev Remote.

Notes from the supplement: macOS needs **both** Docker Desktop and Podman Machine on darwin/arm64 (the older "one reliable path" prioritization is extended); effective resource evidence moves to the runtime engine observation (D2) and is no longer a Host Platform capability; hosted macOS runners give native build/unit/conformance only, runtime E2E comes from core-884 (no nested virtualization on hosted Apple Silicon); macOS Dev Remote moves to core-886, WSL2 Dev Remote is unchanged.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).

## Testing strategy

Shared conformance with deterministic fake hosts (capability/error semantics, resource evidence classification, path/filesystem, trust results, secure ephemeral secrets, no-dead-end diagnostics, architecture guard). Linux: existing CI and Docker/Podman acceptance stay authoritative. Windows/WSL2: hosted Windows runner for native build/unit/conformance; real WSL2 acceptance needs a genuine WSL2 environment, never GOOS cross-compilation. macOS: hosted ARM64/Intel runners for native build/unit/conformance; full Docker Desktop/Podman Machine lifecycle needs real runtime evidence.

## Non-goals

No generic OS plugin ecosystem; no requirement that every Runtime Provider works on every host; no native Windows container claim; no macOS Docker Desktop/Podman Machine claim without runtime evidence; no Quadlet/systemd in the Host Platform Contract; no Application Contract changes for host portability.

## Acceptance

- Real host-dependent call sites are inventoried and classified.
- A minimal Host Platform Contract is documented and implemented.
- Linux behavior is routed through the contract with no regression.
- Windows native vs WSL2 semantics are explicit.
- macOS native host semantics are explicit.
- Effective runtime capacity is distinguished from physical host capacity.
- Trust/filesystem/secure-ephemeral/browser/terminal semantics have explicit capability behavior.
- Unsupported capabilities fail closed with actionable next steps.
- An architecture guard prevents new unapproved host-specific branching outside adapters.
- A shared conformance suite exists.
- The CI matrix records what is actually tested per platform.
- Platform support documentation matches evidence and does not overclaim.
- No portable Application Intent or provider contract needs host-specific fields.

Evidence rule: Linux SUPPORTED while real runtime gates stay green; native Windows outside v0.4 (Windows-runner checks confer no support); WSL2 TESTED/SUPPORTED only after real WSL2 execution; macOS PORTABILITY-VERIFIED from real Darwin CI, full runtime support only after Docker Desktop/Podman Machine E2E. The superseded v0.4.25 assignment text of the source is historical.
