# r28-welle1 · cli2-env-delete (0428-055) — round 1

Task contract: baseharbor-plan/tasks/t-20261114-r28-cli2-env-delete.md
Card: 0428-055 · Env deletion lifecycle · release v0.4.28
Lane: 06e53598 (worker-ornith1.5-laptop)
Evidence location (ONLY): baseharbor-plan evidence above. No evidence in any product repo.

## Scope

Environment-scoped destruction with impact preview, one Keep-data (default)/Delete-data choice, explicit confirmation, auth/audit, preserve global apps, other environments, shared services and node hosts. Bounded slice of umbrella t-20261114-r28-cli-command-semantics. Write-set: env-delete domain/CLI files + dedicated tests. Consumes env-registry (b85efaf6) + env-policy (018b4e58) seams Read-only; no edits to wizard/secrets/registry internals, .github/**, commands.go generated index.

## PLAN

- Step 1: Establish base SHA and isolated worktree on cli2-env-policy-head; confirm build + existing env/deployment tests pass. DONE (re-attested to post-sync base e5ad8a68).
- Step 2: Define the environment-destroy domain seam (fail-closed ownership, per-(target,env) deployment inventory, association-aware member list, Keep/Delete data choice, audit). DONE: internal/deployment/environment_destroy_scope.go + 7 domain tests.
- Step 3: Wire the CLI leaf `baha env destroy [NAME] [--keep-data | --delete-data] [--yes]` on top of the impact preview + consent path; register a new top-level `env` group. DONE: cmd/baha/env_destroy.go + registered in commands.go:141.
- Step 4: Add dedicated tests (cross-env app protection, unknown ownership fail-closed, retain/recover, data-delete consent, partial failure/retry) routed into the existing CI group covering cmd/baha and internal/deployment. DONE: domain tests + 4 CLI integration tests.
- Step 5: Bundle, run focused local tests + vet + build, open a DRAFT PR, publish claim via plan.py, update evidence + board, post END with head SHA. PENDING.

## STATUS (progress)

- Steps 1-4 implemented and locally verified on the post-sync base.
- Full cmd/baha regression suite in progress (10m Go test timeout; other lanes share the runner).

## BASE ATTESTATION

- Old base (pre-sync): `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc  refs/heads/cli2-env-policy-head`
- New base AFTER develop-sync (coord, 2026-11-16): `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d  refs/heads/cli2-env-policy-head`
  - New head is `Merge remote-tracking branch 'origin/develop' into cli2-env-policy-head`.
  - Branch reset onto new base; work re-applied from stash; build + all env tests green on new base.
  - Consumed seams (ListDeployments, ListEnvironmentAssociations, GetEnvironment) unchanged by the sync diff; CollectableOrphans refactor is internal-only (not called by this slice).
- Final diff-witness in this file must be the post-sync base head above.

## DELIVERED CONTENT CONSUMED (Read-only, on base)

- env-policy 018b4e58: internal/serviceaccess/policy.go, internal/operatorauth/config.go, internal/application/workload_security.go — explicit trustedLocal policy, fail-closed default.
- env-registry b85efaf6: internal/deployment/environment_association.go (AssociationKindApp/Node, (kind,id) membership key, idempotent register/deregister, fail-closed foreign binding), environment_identity.go RenameEnvironment seam.
- Existing destroy contract: cmd/baha/app_lifecycle.go (appDestroyCommand, executeApplicationDestroyLifecycle, buildApplicationDestructionPlan, authorizeApplicationDestruction), cmd/baha/runtime_destroy_impact.go (runtimeDestroyImpact via coordinator), internal/deployment/deployment_list.go (ListDeployments / listDeploymentRecords with Environment field), internal/environment/environment.go (stable ID domain).

## OPEN DECISION (posted QUESTION to owner d4212c96)

Decision line (owner, 2026-11-16): OPTION A confirmed — top-level `baha env destroy`, matching brief taxonomy (app/env/target/context/platform/access/system) and the umbrella contract routing destroy to the env group. This is a documented owner scope decision under AGENTS 3.1 (design decision pre-resolved by the task/owner), not a worker-invention. Generated command-index (.github/** generated index + commands.go registration) stays reserved to the integration/CI owner: change reported as file:line finding, never self-edited.

## END

END lane DONE (pending)
