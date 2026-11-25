---
id: t-20261125-hunt43-env-leak-disk
card_number: "0428-316"
card_short_title: "scoped Compose environment"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Stop unrelated host-environment secrets from entering rendered application configuration through Compose interpolation on either…
kanban_title: 0428-316 · scoped Compose environment
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_project.go#L338-L403","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_render.go#L254-L275","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/command_env.go#L9-L23","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md"]
---

- [ ] t-20261125-hunt43-env-leak-disk · 0428 hunt H-V43: hunt43-env-leak-disk #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_project.go#L338-L403), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_render.go#L254-L275), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/command_env.go#L9-L23), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302), [proof 5](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Stop unrelated host-environment secrets from entering rendered application configuration through Compose interpolation on either runtime. Preserve only values intentionally supplied through the selected application's project-scoped environment inputs and required runtime-control variables.

## Scope

- In scope: Podman Quadlet interpolation and owner-only service .env generation; Docker Compose subprocess environment and interpolation; explicit project-scoped environment inputs; focused tests for both adapters.
- Out of scope: broad environment-variable registry documentation (0428-318), logging redaction outside these paths, unrelated runtime process environment changes, and new CI pipelines.

## Acceptance

- Do not seed Compose interpolation from the entire ambient os.Environ set. Pass only explicitly selected project environment inputs plus the minimum runtime-control variables required to invoke the chosen engine.
- An unrelated host secret sentinel cannot appear in a Quadlet service .env file or in Docker Compose's application-service environment, even when the host defines a variable with the same name.
- Explicitly selected project environment values still reach the intended service; do not silently discard declared application configuration.
- Keep generated Quadlet secret-bearing env files owner-only and never print their values in diagnostics.
- Add focused positive and negative tests for both Podman/Quadlet and Docker Compose. Bind them to existing runtime acceptance routes; no parallel pipeline.
- Document the new source and precedence of project environment values in the implementation handoff.

## Evidence

- Quadlet reads the ambient process environment and expands it into Compose data: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_project.go#L338-L403
- Rendered service environment is written into the project files: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/providers/runtime/podman/quadlet_render.go#L254-L275
- Docker runtime process environment and Compose overrides: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/command_env.go#L9-L23, https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302, https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315
- Original H-V43 findings and rationale: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md
