---
id: t-20261125-hunt43-env-leak-disk
card_number: "0428-316"
card_short_title: "ambient runtime env boundary"
type: bug
areas: [runtime, security]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Prevent secret-bearing ambient process environment values from being expanded into Podman Quadlet service .env files or passed…
kanban_title: "0428-316 · ambient runtime env boundary"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/pull/134"
  - "https://github.com/mcpdev80/baseharbor-plan/blob/9cd7c3d0588a441330827b102de1aa0aecfa0477/evidence/2026-11-27/w331-0428-316-hunt43envleak/hunt43-env-leak-disk.md"
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md"
---

- [ ] t-20261125-hunt43-env-leak-disk · 0428-316 · Ambient runtime env boundary #task #release/v0-4-28 #status/planned #view/ready #area/runtime #area/security #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/pull/134), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/9cd7c3d0588a441330827b102de1aa0aecfa0477/evidence/2026-11-27/w331-0428-316-hunt43envleak/hunt43-env-leak-disk.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv43-config-injection/hv43-findings.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Prevent secret-bearing ambient process environment values from being expanded into Podman Quadlet service `.env` files or passed wholesale to Docker Compose. Preserve documented and explicitly configured runtime inputs while making unapproved inherited values unavailable to both runtime paths.

## Disposition and source

FUND-A (HIGH) and FUND-B (MEDIUM) from H-V43 are tracked together here because both arise from the same unfiltered ambient-environment inheritance, with separate Podman and Docker sinks and acceptance checks. The evidence extends the earlier H-V43 FUND-2/FUND-3 observations with the exact Podman plaintext file write and the Docker subprocess path.

FUND-C (LOW, `BASEHARBOR_RUNTIME_IMAGE` YAML injection) is not tracked by this card: the hunt documents an operator-supplied override but does not establish an untrusted source or privilege boundary. Its disposition is recorded in PR #134 and the hunt evidence.

## Scope

- In scope:
  - Podman Quadlet: bound values collected from `os.Environ()` and substituted by `quadletComposeEnvironment` / `expandQuadletComposeString` before `quadletRenderServiceEnvironment` writes service `.env` files.
  - Docker Compose: bound the ambient environment assembled by `mergeProcessEnvironment`, `commandEnvironment` and `runtimeCommandEnv` before invoking the Compose subprocess.
  - Define and document the explicitly supported environment inputs for both paths; preserve those values and project-level configuration that is intentionally supported.
  - Prevent arbitrary ambient secrets and unrelated inherited values from reaching generated service files or the Compose child/container environment.
- Out of scope:
  - `BASEHARBOR_RUNTIME_IMAGE` YAML-input validation (FUND-C; no tracking disposition).
  - Product consent, authentication or authorization behavior.
  - An unrelated environment-variable registry or broad configuration redesign.

## Acceptance

- Podman regression: set an ambient secret sentinel and render a Compose environment that references it; the resulting service `.env` and generated Quadlet files must not contain the secret. An explicitly supported non-secret input must still render as documented.
- Docker regression: set an ambient secret sentinel and invoke the existing Compose command-environment path; the unsupported value must not be inherited by the child or reach the container, while explicitly supported inputs remain available.
- Positive and negative tests cover both runtime paths independently; do not infer Docker behavior from Podman or vice versa. Keep current 0700 directory / 0600 file protections intact.
- The supported-input policy is explicit in code/tests and fails closed for unapproved ambient values; no diagnostic emits secret material.
- Documented/project-configured Compose behavior that is intentionally supported remains compatible. Any behavior change is covered by a focused regression.
- No consent/auth/authorization changes and no unrelated runtime redesign.

## Required checks

- Test binding: ordinary package-discovered Go tests for the modified runtime packages; register any tests requiring special fixtures with the existing package/gate equivalent in the same task.
- Exact test scenarios: Podman ambient-secret materialization regression; Docker ambient-environment inheritance regression; positive compatibility checks for each supported-input path.
- Hosted CI must execute the relevant Docker and rootless Podman/Quadlet gates on the exact final product head. Record test name/package, gate, trigger, run URL and result separately for each runtime. A skipped applicable gate is not evidence.
- Keep the selected-check route impact-based. If an existing path-to-gate mapping or required workflow route is missing, repair it within this task and coordinate its shared-file owner; do not introduce a new CI framework or a blanket matrix.

## Ownership and write set

- Podman runtime implementation and tests under `internal/providers/runtime/podman/`.
- Docker Compose environment assembly and tests under `internal/runtime/`.
- Existing test-to-gate mapping/selection needed for those source paths.
- No workflow-wide or unrelated authentication changes.

## Handoff

Disposition authored by Codex lane w267-0428-284-pridentity on 2026-11-26 from H-V43 evidence in PR #134. This card extends the existing H-V43 task 0428-316 for remediation of FUND-A/FUND-B; it does not mark the hunt or implementation accepted. FUND-C remains no-tracking unless later evidence establishes an untrusted input boundary.
