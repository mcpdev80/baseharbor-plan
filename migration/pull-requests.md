# Open pull requests at snapshot time

PRs stay in their code repositories; this list only records how they relate to planning. State as reconciled on 2026-10-15 ≈20:45Z; the machine-readable list is in [source-snapshot/inventory.json](source-snapshot/inventory.json).

| PR | State | Base ← head | Planning relation |
| --- | --- | --- | --- |
| [baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930) | draft | develop ← `work/v0.4.26-893-pr-check-enforcement` | core-893-interface / core-893 (session 1). Interface reference, **not** a qualified prerequisite. |
| [baseharbor#931](https://github.com/mcpdev80/baseharbor/pull/931) | **merged 2026-10-15T20:32Z** (`bf69ad0a…`) | develop ← `work/v0.4.26-900-safe-gc` | core-900 (session 2), now `review`. Merge is not acceptance: core-900 needs Maintainer acceptance and evidence. |
| [baseharbor#932](https://github.com/mcpdev80/baseharbor/pull/932) | ready for review | develop ← `work/v0.4.26-896-isolated-pr-runners` | core-896 (session 1), now `review`. |
| [baseharbor#934](https://github.com/mcpdev80/baseharbor/pull/934) | draft | develop ← `work/v0.4.26-910-read-context` | core-910 preparatory implementation (session 2); not to be integrated before the foundation. |
| [baseharbor#935](https://github.com/mcpdev80/baseharbor/pull/935) | draft | develop ← `task/752-reconcile-default-instances` | core-752 (pilot bug). |
| [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936) | draft, must not be merged | develop ← `runtime-validation/ci/934-guided-go-exact` | Temporary core-893 CI pilot for PR #934. |
| [baseharbor#933](https://github.com/mcpdev80/baseharbor/pull/933) | draft | develop ← `task/895-review-protection` | core-895: proposal payloads; activation waits for a qualified core-893 status check. |
| [baseharbor#616](https://github.com/mcpdev80/baseharbor/pull/616) | draft, conflicting | main ← `test/kubernetes-adoption-contract-demo` | Kubernetes pre-freeze architecture proof; must be explicitly resolved in [v0.4.31](../releases/v0.4.31.md). |
| [baseharbor-console#3](https://github.com/mcpdev80/baseharbor-console/pull/3) | draft, conflicting, last update 2026-10-08 | main ← `feature/v0.4.23-live-integration` | console-2 (triage). Stale against current Core; Maintainer decides continue/close. |
| [baseharbor-node-connector#4](https://github.com/mcpdev80/baseharbor-node-connector/pull/4) | draft, conflicting, last update 2026-10-08 | main ← `feature/v0.4.23-core-integration` | nc-3 (triage). Stale; Maintainer decides continue/close. |
| [baseharbor-demo#61](https://github.com/mcpdev80/baseharbor-demo/pull/61) | open, conflicting, 2026-09-30 | main ← `ci/v0418-pre-release-suites` | No open planning item. v0.4.18 era; superseded by #62? Maintainer decides. |
| [baseharbor-demo#62](https://github.com/mcpdev80/baseharbor-demo/pull/62) | open, mergeable, **empty diff**, 2026-09-30 | main ← `ci/v0418-pre-release-suites-v2` | No open planning item. Zero changed files: likely obsolete. |
| [baseharbor-demo#86](https://github.com/mcpdev80/baseharbor-demo/pull/86) | open, conflicting, 2026-10-01 | main ← `fix/v0419-shell-ux-static` | No open planning item (v0.4.19 era). |
| [baseharbor-demo#104](https://github.com/mcpdev80/baseharbor-demo/pull/104) | open, conflicting, 2026-10-02 | main ← `fix/v0419-final-gate-convergence` | No open planning item (v0.4.19 era). |
| [baseharbor-demo#106](https://github.com/mcpdev80/baseharbor-demo/pull/106) | open, mergeable, 2026-10-02 | main ← `fix/v0419-recovery-exposure-contract` | No open planning item (v0.4.19 era). |

The five Demo PRs belong to published v0.4.18/v0.4.19 work and are not referenced by any open issue. They are listed in [conflicts.md](conflicts.md) for a Maintainer decision; this migration does not close them.
