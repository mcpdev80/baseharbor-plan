---
id: t-20261125-hunt43-docker-path-config
card_number: "0428-317"
card_short_title: "Docker env scope"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-317 · Docker env scope
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
superseded_by: t-20261125-hunt43-env-leak-disk
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md"]
---

- [x] t-20261125-hunt43-docker-path-config · 0428 hunt H-V43: hunt43-docker-path-config #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

### Disposition: SUPERSEDED by 0428-316

The Docker Compose ambient-environment finding is the same root cause as the Podman/Quadlet finding: the selected application runtime inherits the host process environment for Compose interpolation. Fold both adapters into one security task so they share one explicit project-environment contract and independent Docker/Podman regressions.

### Evidence

- Docker Compose environment merge: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/compose_files.go#L276-L302
- Runtime command environment: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/docker_engine.go#L284-L315
- H-V43 finding: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md
