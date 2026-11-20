---
id: t-20261114-r28-cli2-env-registry
card_number: "0428-054"
card_short_title: "Implement Env registry"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex-open-pr-sweep-054
kanban_status: closed
kanban_lane: closed
kanban_summary: "Implement environment registry. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-054 · Implement Env registry
priority: high
depends_on: [t-20261114-r28-cli2-uid-environment, t-20261114-r28-cli2-uid-target]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1591]
sources: []
blocker: ""
wait_reason: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1591", "https://github.com/mcpdev80/baseharbor/actions/runs/44652673886", "https://github.com/mcpdev80/baseharbor/commit/83b19dce24eed2f837dd2dda7d56222d20a7da32"]
---

- [x] t-20261114-r28-cli2-env-registry · CLI redesign: Implement environment registry #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-054 · **Priority:** high  
    **PR:** [baseharbor#1591](https://github.com/mcpdev80/baseharbor/pull/1591)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1591), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44652673886), [proof 3](https://github.com/mcpdev80/baseharbor/commit/83b19dce24eed2f837dd2dda7d56222d20a7da32)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md), [t-20261114-r28-cli2-uid-target](t-20261114-r28-cli2-uid-target.md)  
**Required by:** [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-context-shell](t-20261114-r28-cli2-context-shell.md), [t-20261114-r28-cli2-env-delete](t-20261114-r28-cli2-env-delete.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md), [t-20261114-r28-cli2-org-env](t-20261114-r28-cli2-org-env.md)  
**Owner:** codex-open-pr-sweep-054  
**Priority:** high  
**PRs:** [baseharbor#1591](https://github.com/mcpdev80/baseharbor/pull/1591)  
**Source:** 
<!-- /generated:links -->

## Goal

Implement environment registry. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## DESIGN-RULING (owner decision 2026-11-15)

Option B: app/target/node association is stored inside the existing per-Target environment state record (`environment.json`, per owner uid-env decision). No new registry package (C rejected: second source of truth); config/definition-layer-only (A) not chosen. CLI wiring is NOT part of this card — it belongs to 0428-053 (cmd/baha/commands* write set). Migration idempotent, collision fail-closed.

## Scope

Provide authoritative Core registry and app/target/node association for shared environments per accepted contract; do not infer matching from names; preserve organization source-vs-runtime authority.

## Entry points and ownership

- Starting points: `new internal environment registry files; dedicated machine-domain adapters (registration coordinated)`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Create/select/list/update shared environment, app association, multiple nodes, duplicate/conflict/permission and Core restart persistence; CLI/HTTP integration coordinated.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff (2026-11-20)

- Candidate: PR #1591, branch `lane-0428-env-registry`, exact head `bb5ea39fab4523bf876342764fb8f5d22fce30ff`, base `develop` at `b7cbc00f0adfa36945d6f7af8098d88096276c4f`; PR is OPEN + Ready and reports CLEAN after exact-head checks. The Maintainer promoted it after reviewing the focused fix and successful Draft run. The branch was advanced monotonically from verified old head `08fc5ad310e181394f6cef51d91ba8df42b2b446` and includes current develop as a merge parent. PR diff stays scoped to the three registry files.
- Reproduced defect on old exact head `08fc5ad3`: `TestDeregisterEnvironmentAssociationRejectsEnvironmentPathTraversal` failed because calling `DeregistrationEnvironmentAssociation("target-a", "other/../prod", AssociationKindApp, "app-1")` removed the real `prod` binding. Fix: validate the logical environment name via the existing `environment.ValidateName` before resolving the state path. Regression passes and invalid path selectors now fail before touching sibling records.
- Test -> check -> trigger -> result: `TestDeregisterEnvironmentAssociationRejectsEnvironmentPathTraversal` and package coverage in `go test ./internal/deployment ./internal/environment -count=1` -> normal Go package test discovery -> PR synchronize and `ready_for_review` workflows -> Draft run [44649695031](https://github.com/mcpdev80/baseharbor/actions/runs/44649695031) SUCCESS for source/routing and Draft Go, followed by Ready exact-head run [44650304561](https://github.com/mcpdev80/baseharbor/actions/runs/44650304561) SUCCESS. Ready run passed workflow policy, Trusted Plan, source format, native gate plan, focused Python, go-vet, go-build, deployment-package-tests, PR Selected Checks, all Go unit shards (owner, packages, cli-0..3). `go vet ./internal/deployment ./internal/environment` and `git diff --check` also PASS locally at `bb5ea39`.
- Ready-run native/runtime, release, and unrelated integration jobs were skipped by the impact plan; `PR · Native gate plan` and `PR Selected Checks` passed. The selector-path validation is a filesystem-input safety fix with no runtime lifecycle change, so no native runtime witness was selected. No Codeman worker overlapped the files at pre-edit check (host reported zero active sessions); no Codeman configuration/session was changed.
- Dependency path: both card dependencies 0428-051/#1578 and 0428-052/#1580 are accepted; #1578 is merged. Downstream #1594 is OPEN Draft at head `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`, based on `lane-0428-env-registry` (now bb5ea39); it needs its own monotone hop and exact checks after this card is accepted. #1615 remains OPEN Ready at `f93564a0d707983bfe6a8b59375c1c1c914d7827`, based on `cli2-env-policy-head`; it then needs a hop after #1594. Neither downstream PR was edited.
- At this handoff point, review decision was blank and no merge had been performed; this was superseded by the Owner acceptance below. Sequence #1594's exact checks before #1615's refresh; a successful #1591 run does not itself accept its dependents.

## Follow-up review fixes and current exact-head evidence (2026-11-20)

- Independent review of `bb5ea39` found that `RenameEnvironment` dropped `Associations`, and that a crash after destination installation left a stale source that same-identity retry did not remove. Fixed both, merging source/destination memberships on retry and retaining the canonical identity. Regressions `TestRenamePreservesEnvironmentAssociations` and `TestRenameRetryCleansSourceAfterInterruptedInstall` reproduce the prior failures and now pass.
- Follow-up review caught `RenameEnvironment` exceeding the 200-line source-readability limit; extracted install/reconciliation into `installRenamedEnvironmentIdentity`. A further race audit found a mismatched destination binding could otherwise reach `os.Rename`; the helper now fails closed and `TestInstallRenameRefusesMismatchedDestination` verifies foreign destination bytes and the source are preserved.
- At the time of this evidence update, PR #1591 head was `2922f5ed9c411eec28bbfe2ea90f2b27c8f3055e`, based on develop `6b8188df26a1e263750379a8c5e8255ee4ef740c` after a monotone merge of #1693's develop advance. It was OPEN + Ready and CLEAN; it has since merged as recorded below. The PR diff also carried the develop merge's metrics changes, which were not edited in this task.
- Test -> check -> trigger -> result: the three rename regressions plus `go test ./internal/deployment ./internal/environment -count=1`, `go vet ./internal/deployment ./internal/environment`, `git diff --check`, and `bash scripts/source-readability-audit.sh` passed locally. Exact Ready run [44652673886](https://github.com/mcpdev80/baseharbor/actions/runs/44652673886) passed workflow policy, source format/readability, native gate plan, Trusted Plan, focused Python, go-build, go-vet, deployment-package-tests, PR Selected Checks, and Go unit shards (owner, packages, cli-0..3). Native/runtime, release, and unrelated integration jobs were impact-skipped by the trusted plan.
- Codeman was freshly checked read-only before the develop hop: no active sessions; worker file changes were inspected read-only and did not overlap the environment identity files. No Codeman changes were made.

## Owner acceptance and merge (2026-11-20)

- Owner-delegated Maintainer acceptance: PR #1591 merged to `develop` at `83b19dce24eed2f837dd2dda7d56222d20a7da32` after exact Ready run [44652673886](https://github.com/mcpdev80/baseharbor/actions/runs/44652673886) passed and the exact head received a clean code review. Rename now preserves associations, retries reconcile interrupted installation, and mismatched destination bindings fail closed.
- The registry persistence test reloads the JSON through the storage API in the same process; it does not restart a Core process. CLI/HTTP integration is explicitly coordinated with 0428-053. This merge accepts the bounded registry/storage slice; do not represent this as full process-restart or CLI/HTTP evidence. Those integration checks remain required in the downstream lane.
