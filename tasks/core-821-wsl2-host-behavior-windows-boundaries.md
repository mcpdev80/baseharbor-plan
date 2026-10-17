---
id: core-821
areas: [platform]
type: feature
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: [core-820, t-20261017-release-0-4-29-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#821"]
source_updated: "2026-10-15T16:50:23Z"
labels: [kind/feature, area/runtime, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-821 · WSL2: implement host behavior and Windows boundaries #task #release/v0-4-29 #status/planned #view/waiting #board/planned #area/platform #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [core-820](core-820-linux-host-adapters-regressions.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** [core-820](core-820-linux-host-adapters-regressions.md), [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
**Required by:** [core-823](core-823-tests-platform-conformance-support.md), [t-20261017-release-0-4-29-prepare](t-20261017-release-0-4-29-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#821](https://github.com/mcpdev80/baseharbor/issues/821)
<!-- /generated:links -->

## Goal

Implement Windows-side Host Platform semantics with native Windows client behavior explicitly separated from WSL2 Linux execution, and deliver a working WSL2 developer journey (Dev Local and Dev Remote).

## Scope

- v0.4 Windows scope: real WSL2 with Linux `baha`. Native Windows executable/host adapter and Windows containers are outside this release; build-only evidence is not runtime support. `GOOS=windows` and WSL2 are different platform conditions.
- Native Windows (evaluate where applicable, no runtime claim): identification, state/config/data dirs, path semantics, browser opening, terminal, trust store, secure ephemeral material, self-update packaging, runtime discovery.
- WSL2: identify explicitly while keeping Linux execution semantics; use effective WSL2/runtime capacity, not physical Windows RAM; classify Docker Desktop integration vs Linux-local Docker/Podman honestly; define trust boundary (Linux trust in WSL2 vs Windows browser/host trust); do not assume systemd unless enabled; keep path safety across Linux and mounted Windows paths; actionable diagnostics when Windows-side action is needed.
- Testing: Windows-hosted runners for native build, portable unit tests, contract conformance, path/state, injectable browser selection, isolated trust adapter tests, packaging/update selection. **A Windows runner passing unit tests is not WSL2 acceptance**: real WSL2 qualification needs an environment that actually provides WSL2 (dedicated/self-hosted if needed); record untested status rather than simulating evidence.
- The source labels the journey requirements "v0.4.25 mandatory WSL2 delivery acceptance (2026-10-09)"; the release label is historical, the requirements stand per [v0.4.29](../releases/v0.4.29.md).

## Acceptance

- Native Windows and WSL2 are distinct platform classifications.
- Native Windows contract conformance passes on Windows GitHub Actions.
- WSL2 detection and effective-resource semantics are covered by unit fixtures.
- Real WSL2 smoke evidence is required before WSL2 is marked TESTED/SUPPORTED.
- No native Windows runtime support is claimed without real runtime evidence.
- Failures tell the user whether the next action belongs inside WSL2 or on the Windows host.
- No Application/Runtime Provider contract changes are required.
- `baha` installation/update inside real WSL2; supported Docker Desktop WSL integration or WSL2-local Linux Docker/Podman.
- End-to-end disposable Dev Local repo init/plan/up/status/doctor/logs/sql/cache/destroy with clean owned-resource removal.
- Dev Remote enrollment/import and scoped Core mTLS on WSL2; host/browser trust separation and reconnection/rotation/offboarding.
- Real runtime VM memory/capacity detected; fails safely when capacity is insufficient.
- Negative tests for missing WSL distro/runtime, unavailable systemd, Windows-mounted repository paths, unsafe ownership and expired credentials.
- Runner evidence comes from actual WSL2 execution; native Windows CI or GOOS cross-compilation does not count.
- A Windows developer completes installation and first application startup from one short public getting-started guide.
- WSL2, the installed distribution and a usable Docker or Podman runtime are detected automatically; only non-inferable decisions are asked.
- Missing WSL2, stopped runtime, memory limits, Windows-mounted repository paths and browser/trust integration are explained with a concrete next action.
- Dev Local works without mandatory BaseHarbor login; Dev Remote uses one-time guided profile import/enrollment and reuses the established session.
- The same canonical commands and wizard behavior work as on Linux; non-interactive CLI/JSON/MCP semantics stay consistent.
- An independent Windows developer completes install, app init, up, status/logs, app sql/cache and owned destroy using only public documentation; avoidable prompts and friction are recorded.

## Required checks

- Windows-hosted native conformance; real WSL2 runtime lane; independent walkthrough.

## Dependencies and file ownership

- Depends on core-820 (the seam from core-819 must be stable). Runs in parallel with core-822/core-883. Owns the WSL2/Windows adapters.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
