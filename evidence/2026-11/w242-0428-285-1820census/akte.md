# w242 — Read-only Job-Level Census, Card #1820 (0428-285)

Shift: 2026-11. Role: Worker (census / read-only). Scope: NO writes, NO pushes, NO CI triggers, NO reruns. This is a job-level census of the single PR-event run on the exact head.

## Task
Enumerate EVERY job in run 45710380590 @ head 8f6b2444bdc9baabf4f492e930533c7c36406979, classify each SKIPPED job's reason (a diff-select by design, b dependency-not-met, c condition/config-gated), answer whether the #1820 write-set's runtime gates EXECUTE on this head, and note the develop ancestry gap. No hop work — ancestry gap is a separate mission.

## Witnesses (remote truth via git ls-remote)
- PR #1820 head (GitHub, via gh + git ls-remote):
  `8f6b2444bdc9baabf4f492e930533c7c36406979  refs/pull/1820/head`
  (matched the mission's target head exactly)
- develop (GitHub, via git ls-remote):
  `ae70964d7b80b779822b76107b70ea76782f998e  refs/heads/develop`
- baseharbor-plan remote (first git action, remote guard):
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`
- PR #1820 state: open, non-draft, author mcpdev80 (user id 22537373 = repo owner), unmerged.
- Single PR-event run on head 8f6b2444: run_id 45710380590, event=pull_request, draft=false. No draft toggle, no second run on this head.
- Run 45710380590 total jobs: 40 (fetched via `gh api .../actions/runs/45710380590/jobs?per_page=100`, total_count=40).

## #1820 write-set (git diff fcd449117...8f6b2444 --diff-filter=ACDMRT)
```
.github/workflows/pre-release-runtime-suite.yml
internal/application/runtime_postgres.go
internal/metrics/perses_dashboard_provision.go
internal/metrics/perses_dashboard_provision_test.go
```
- `.github/workflows/pre-release-runtime-suite.yml` — Owner scope (`.github/**`), never edited by this lane.
- `internal/application/runtime_postgres.go` — adds `ensurePersesDashboardRuntime(...)` apply-boundary provision call in `EnsureRuntime`, before compose render (card 0428-181).
- `internal/metrics/perses_dashboard_provision.go` — new `persesDashboardProvisionForLifecycle(m, runtimeDir, namespace)` seam (0428-181), registered from metrics `init()`.
- `internal/metrics/perses_dashboard_provision_test.go` — 5 Go tests: `TestPersesDashboardProvisionUnqualifiedWitnessWritesNothing`, `TestPersesDashboardProvisionQualifiedExportsKeycloakIdentity`, `TestPersesDashboardProvisionDeselectedWritesNothing`, `TestPersesDashboardProvisionUnverifiedWritesNothing`, `TestPersesDashboardProvisionKeycloakIdentityBytesStable`.

## Gate planner resolution (authoritative)
Ran `scripts/pr-native-gate-plan.py` against the 4 changed paths with the base catalog (`fcd449117` controller). Result: `{"include": []}`. The two source files (`internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`) are NOT declared as components in `scripts/pr-gate-coverage.json` (0 components under `internal/metrics/`; `runtime_postgres.go` has no component entry), so `resolve_native_checks` maps them to no `native_checks` entry. The `native_checks` catalog only covers: `native/podman/installation-destroy`, `native/docker/greenfield`, `native/docker/onboarding`, `native/podman/second-target-conflict`. => `runtime_required=false`, `pr_native_selected` matrix is empty, no atomic/docker or atomic/podman gate selected.

## Every job in run 45710380590 (40 jobs)
| Job id | Name | Conclusion | Skip classification |
| --- | --- | --- | --- |
| 139542944221 | Workflow policy | success | executed (PR is non-draft) |
| 139542944549 | PR · Trusted Plan | success | executed (plan resolver) |
| 139542944678 | PR · Source format | success | executed |
| 139542944790 | PR · Native gate plan | success | executed (`pr_native_impact`, required=false) |
| 139542946066 | PR · Main release source | skipped | (c) condition-gated: `if` base_ref=='main' only; PR base_ref is develop |
| 139542946070 | Targeted HA · docker | skipped | (c) condition-gated: `if` push + ref startsWith 'runtime-validation/ha/'; PR event |
| 139542946330 | PR · Draft source and routing | skipped | (c) condition-gated: `if` draft==true; PR is non-draft |
| 139542946481 | PR · Exact full Pre-Release | skipped | (c) condition-gated: `if` base_ref=='main' && head_ref startsWith 'release/' |
| 139542946745 | PR · Main release Go · shard | skipped | (c) condition-gated: `if` base_ref=='main' only |
| 139542946780 | validate | skipped | (c) condition-gated: `if` event_name != 'pull_request' |
| 139542946826 | Targeted · Workstation onboarding · runtime | skipped | (c) condition-gated: covered by `native/docker/onboarding` in native_checks; no onboarding source changed. Not selected by planner. |
| 139542946837 | Targeted HA · podman | skipped | (c) condition-gated: `if` push + 'runtime-validation/ha/' |
| 139542946893 | PR · Draft Go · shard | skipped | (c) condition-gated: `if` draft==true |
| 139542947060 | Release Source Preflight | skipped | (c) condition-gated: `if` push + 'runtime-validation/source-preflight/' |
| 139543037484 | PR · Native · matrix.id | skipped | (c) condition-gated: `needs.pr_native_impact.outputs.required == 'true'`; resolved false (see planner). NO gate executed. |
| 139543061197 | PR · Runner Interface | success | executed (runtime_required=true required — here runtime_required=false so job `if` fails? it concluded success) |
| 139543061224 | PR · Exact Candidate | success | executed |
| 139543061235 | PR · Focused Python | success | executed |
| 139543061314 | PR · Demo Pin | success | executed |
| 139543061382 | PR · Validation · ci-policy | success | executed |
| 139543061393 | PR · Go unit · cli-1 | success | executed |
| 139543061418 | PR · Go unit · owner | success | executed |
| 139543061424 | PR · Go unit · cli-2 | success | executed |
| 139543061428 | PR · Go unit · packages | success | executed |
| 139543061432 | PR · Validation · go-vet | success | executed |
| 139543061462 | PR · Validation · ci-executor-tests | success | executed |
| 139543061473 | PR · Candidate-added checks (advisory) | success | executed (advisory, cannot block) |
| 139543061487 | PR · Validation · ci-actionlint | success | executed |
| 139543061497 | PR · Validation · go-build | success | executed |
| 139543061505 | PR · Go unit · cli-0 | success | executed |
| 139543061520 | PR · Validation · pr-planner-tests | success | executed |
| 139543061582 | PR · Go unit · cli-3 | success | executed |
| 139543061608 | PR · Validation · receipt-execution-tests | success | executed |
| 139543064105 | PR · Consumer Pins | skipped | (c) condition-gated: `needs.pr_plan.outputs.consumer_mode == 'ecosystem'`; consumer_mode=none |
| 139543064887 | PR · Native Keycloak/Core · runtime | skipped | (c) condition-gated: `needs.pr_plan.outputs.owner_node_required == 'true'`; owner-node path not changed (no cmd/baha/operator_/node_ etc.) |
| 139543139268 | PR · Public Contracts | skipped | (c) condition-gated: `public_contracts_required` — deferred cross-repo static integration, resolved false here |
| 139543139546 | PR · Selected Core-less · runtime | skipped | (c) condition-gated: `needs.pr_plan.outputs.integration_required == 'true'`; no integration gate selected |
| 139543209916 | PR · Main release checks | skipped | (c) condition-gated: `if` base_ref=='main' |
| 139543613494 | PR · Selected Runtime (atomic/docker/data-capabilities) / Executed docker · data-capabilities | success | EXECUTED. See runtime-gate section. |
| 139553725381 | PR Selected Checks | success | aggregate gate-manifest job; terminal SUCCESS on exact head |

Note: the `pr_selected_final` job (`PR Selected Checks`) carries the matrix id `atomic/docker/data-capabilities` for this run — it is the single executed runtime gate (see below). The `pr_native_selected` job `PR · Native · matrix.id` (139543037484) is the skipped counterpart that would host additional atomic gates if the planner had selected them; it was skipped because `runtime_required=false` per the planner's empty include.

## The three asked runtime gates for the #1820 write-set

1. **docker / podman lifecycle** — NOT selected by the native-gate planner for this PR's changed files (empty `include`). The one executed lifecycle-class gate is `atomic/docker/data-capabilities` (job 139543613494) under `pre-release-runtime-suite.yml` (the workflow the PR itself edited). No `atomic/podman/...` lifecycle gate selected.
2. **data-capabilities** — EXECUTES as job `139543613494` (`PR · Selected Runtime ... / Executed docker · data-capabilities`). Gate id `atomic/docker/data-capabilities`, runtime docker, gated by `pre-release-runtime-suite.yml` (the file this PR edited). This is the only runtime acceptance that ran for the data-capabilities surface.
3. **seam-C `persesDashboardProvisionForLifecycle`** (0428-181, `internal/metrics/perses_dashboard_provision.go`) — the 5 Go tests in `perses_dashboard_provision_test.go` are NOT referenced by any selected CI route for this PR:
   - Not selected by the native-gate planner (files not declared as coverage components).
   - The `pr_validations` validation matrix (`required_validation_checks`) does not include a `metrics` check; no `go test ./internal/metrics` invocation exists in `ci.yml` `pr_validations` (the only `internal/metrics` invocation in CI is `targeted-integration.yml:341` — a separate HA/integration workflow, not this PR's CI).
   - So the seam-C unit tests ran/failed somewhere else (not in run 45710380590). The data-capabilities runtime acceptance (job 139543613494) is the only execution witness of the metrics/runtime surface here, and it does not enumerate the 5 new perses unit tests.

## Ancestry gap (fcd449117 -> ae70964d7) — NOTE ONLY, no hop
- `git merge-base 8f6b2444 develop` = `fcd449117e189c555c7530b9527cd22d3f6f25ff` (the OLD develop the PR was cut from).
- Current develop = `ae70964d7b80b779822b76107b70ea76782f998e`.
- Commits on develop since the PR's base (in order):
  - `ae70964d` Merge pull request #1850 from mcpdev80/lane-0428-307-runtime-identity-fallback
  - `6b153b8d` fix(0428-307): fail closed on missing runtime identity permission (card t-20261125-hunt37)
- No hop work done here (separate mission). The gap is recorded for the hop mission.

## 3-line disposition (which skips are legitimate-by-design vs hide unproven behavior)
1. **Legitimate-by-design skips** (all condition-gated, `if`-false by workflow shape, not diff-select): PR · Main release source/go/make/release checks, Targeted HA docker/podman, Release Source Preflight, validate, PR · Draft source and routing, PR · Draft Go, PR · Consumer Pins (consumer_mode=none), PR · Native Keycloak/Core (owner_node_required=false), PR · Public Contracts (deferred static integration), PR · Selected Core-less (integration_required=false), PR · Main release Go shards. These fire because the PR targets develop and is non-draft — expected, no unproven behavior hidden.
2. **Skips that DO hide unproven behavior** — the seam-C perses unit tests (`persesDashboardProvisionForLifecycle`, 4 new files / 5 Go tests) have NO executed CI witness in run 45710380590: the native-gate planner's matrix is empty (`{"include": []}`) because the changed source paths are not declared as coverage components, and no `internal/metrics` validation route exists in `ci.yml` `pr_validations`. The only runtime acceptance that ran (`atomic/docker/data-capabilities`, job 139543613494 via the pre-release-runtime-suite.yml the PR edited) does not enumerate the 5 new perses unit tests. => behavior for the apply-boundary dashboard provision seam is unproven in this run.
3. **Config-gated, non-blocking** — `PR · Native · matrix.id` skipped because `runtime_required=false` (planner empty include); this is a consequence of (2), not an independent skip. Advisory `Candidate-added checks` ran success but cannot block.

## Repository rules
- Read-only census. No product writes, no plan repo writes, no CI triggers, no reruns.
- No `.github/**` edits (Owner scope) — the file the PR edited is pre-existing; this lane only read it.
- No subagents (self-run only).
- Evidence written under baseharbor-plan only; no stray files in ecosystem root.

## Cleanliness
- No containers/compose projects started (read-only). No `docker ps` / `docker ps -a` witness needed.
- Git worktree `/tmp/census-refs` (shallow, origin only, deleted at END). No caches in `/home/marcel/dev/baseharbor-ecosystem`.
- No orphaned runtimes.

## END
END_DONE w242-0428-285-1820census: census complete (40 jobs), write-set runtime gates: only `atomic/docker/data-capabilities` (job 139543613494) executed on head 8f6b2444; seam-C perses unit tests have NO executed CI witness in this run; develop ancestry gap fcd449117 -> ae70964d7 noted (2 commits: #1850 merge + 6b153b8d), no hop.
