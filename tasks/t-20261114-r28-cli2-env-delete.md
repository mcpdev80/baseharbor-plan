---
id: t-20261114-r28-cli2-env-delete
card_number: "0428-055"
card_short_title: "Env deletion lifecycle"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "Codex (Marcel assigned, wait sweep 2026-11-21)"
kanban_status: wait
kanban_lane: wait
kanban_summary: "Environment deletion lifecycle. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-055 · Env deletion lifecycle
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1627]
sources: []
blocker: ""
wait_reason: "Focused environment-destroy Go tests and vet pass on PR head 202b984e; exact-head Draft run 44852435311 completed FAILURE (CLI shards failed; native and selected checks were skipped because the PR is Draft). pr-gate-plan reports unresolved runtime/registration coverage. The native Docker attempt stopped at the existing missing-operator-auth gate before Environment-Destroy ran. #1615 is actively editing the exact selective-runtime test and shared pre-release runtime workflow needed for the native route; preserve that ownership. Resume after #1615’s shared auth/workflow change lands, then add/route the native assertion on disjoint files and run full exact-head CI."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1627", "https://github.com/mcpdev80/baseharbor/commit/202b984e2a103d713bb688eb0b8be52f1ddfa677", "https://github.com/mcpdev80/baseharbor/actions/runs/44852435311", "https://github.com/mcpdev80/baseharbor/pull/1615"]
---

- [ ] t-20261114-r28-cli2-env-delete · CLI redesign: Environment deletion lifecycle #task #release/v0-4-28 #status/wait #view/wait #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel assigned, wait sweep 2026-11-21) · **Priority:** high  
    **PR:** [baseharbor#1627](https://github.com/mcpdev80/baseharbor/pull/1627)  
    **Waiting:** Focused environment-destroy Go tests and vet pass on PR head 202b984e; exact-head Draft run 44852435311 completed FAILURE (CLI shards failed; native and selected checks were skipped because the PR is Draft). pr-gate-plan reports unresolved…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1627), [proof 2](https://github.com/mcpdev80/baseharbor/commit/202b984e2a103d713bb688eb0b8be52f1ddfa677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44852435311), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1615)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Required by:** [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md), [t-20261114-r28-cli2-wizard-env](t-20261114-r28-cli2-wizard-env.md)  
**Owner:** Codex (Marcel assigned, wait sweep 2026-11-21)  
**Priority:** high  
**PRs:** [baseharbor#1627](https://github.com/mcpdev80/baseharbor/pull/1627)  
**Source:** 
<!-- /generated:links -->

## Goal

Environment deletion lifecycle. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement environment-scoped destruction with impact preview, one Keep data default/Delete data choice, explicit confirmation, auth/audit, preserve global apps, other environments, shared services and node hosts.

## Entry points and ownership

- Starting points: `new environment deletion domain files; cmd/baha/runtime_destroy_impact.go interfaces via coordinator`. Verify exact current lines before changing files.
- Own this slice and its dedicated tests. This card is explicitly assigned the minimal CI/gate routing changes required for its own lifecycle tests, including relevant workflow, selector/catalog and trigger updates when no suitable route exists. Coordinate shared edits with the CI owner and avoid concurrent writes. Other parser, machine registry, release-note and generated-index files remain reserved for their integration owners.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Test shared app cross-env protection, ownership unknown fail-closed, recoverability if retain claimed, data delete consent, partial failure and retry; real isolated runtime where required.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to a real CI check or native gate and its trigger. If no suitable route exists, add or extend the minimal gate, selector/catalog entry and trigger in this same card and PR; coordinate shared-file edits with the CI owner, but do not wait for a separate CI-owner task. Prove actual exact-head execution before acceptance. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only findings: [PR evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1627-0428-055-independent-review.md). Draft #1627 `49e164cc` has no exact-head checks and overstates destroy: identity-only deletion leaves deployments/runtime/data in place; `--delete-data` does not delete data.

## Handoff (2026-11-20)

- Candidate: PR #1627, branch `cli2-env-delete`, exact head `96deb1f1597d0d4a10d54421acc973053d27224a`, based on `cli2-env-policy-head`; PR is OPEN + Draft. The push was fast-forward from the verified previous remote head `49e164ccbd6552a98854ceceaabfafa748775ed1`.
- Scope changed only `cmd/baha/env_destroy.go` and `cmd/baha/env_destroy_integration_test.go`. KEEP stops only scoped deployments and retains persistent data/recovery/canonical UUID ownership. DELETE fully destroys each scoped deployment and removes environment identity only after successful verification. Failures retain environment identity for retry; sibling/shared resources are preserved; noninteractive DELETE requires separate `--confirm-delete-data` consent.
- Tests -> existing check -> trigger -> result at candidate source: `go test ./cmd/baha -run 'TestCLIEnvDestroy|TestEnvironmentDestroy' -count=1` -> normal Go package test discovery -> Go source PR workflow -> PASS locally. `go test ./internal/deployment -count=1` -> normal Go package test discovery -> Go source PR workflow -> PASS locally. `go vet ./cmd/baha ./internal/deployment` -> Go vet workflow -> Go source PR workflow -> PASS locally. `git diff --check` -> whitespace validation -> local candidate validation -> PASS. The broader `go test ./cmd/baha -count=1` was cancelled after an unrelated idle test hung for over four minutes; it is not a pass.
- Required gate mapping is incomplete: the current planner selects cli-unresolved-runtime-impact for cmd/baha/env_destroy.go, so no qualified native lifecycle check is selected. No isolated Docker/Podman witness has run. Gate routing and native runtime proof are unfinished work owned by this card, not a separate CI-owner prerequisite. The stacked base cli2-env-policy-head also needs an eligible exact-head route; after card dependencies are accepted, update the base and include any required minimal workflow/selector change in this same PR.
- Keep Draft and task in wait while the declared predecessor cards are unresolved. No merge or acceptance. When resumed, this card completes its own lifecycle behavior and missing gate route, obtains the isolated runtime witness and exact-head checks, then hands off to review.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befund (independent review 1627): die destroy-PREVIEW kuendigt an, scoped deployments wuerden entfernt; der bestaetigte pfad ruft nur deployment.DestroyEnvironmentIdentity(...) auf und loescht das nicht. Lifecycle-correctness-blocker: nur melden, was der apply-pfad wirklich tut, oder die loesch-semantik implementieren UND verifizieren.
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).

## Wait-sweep handoff — 2026-11-21

- Resumed from the dormant Draft #1627 after predecessors 0428-053/#1594 and 0428-054/#1591 were already accepted; claimed through plan main `d4f2866d`. Merged current develop `40cb28c758b02960356434b630086a341ebe1738` monotonically and pushed the latest isolated head `202b984e2a103d713bb688eb0b8be52f1ddfa677`. PR remains Draft.
- Fixed confirmed JSON behavior: confirmed `baha env destroy --json` now emits one result object instead of concatenating preview and result JSON; added a focused regression. Local `go test ./cmd/baha -run 'TestCLIEnvDestroy|TestEnvironmentDestroy' -count=1`, `go test ./internal/deployment -run 'TestCollectEnvironmentDestroyScope|TestDestroyEnvironmentIdentity' -count=1`, `go vet ./cmd/baha ./internal/deployment`, and `git diff --check` pass on the final source tree.
- Local native Docker attempt was stopped by the existing `Managed-environment machine operations require an authenticated BaseHarbor operator` failure during the shared setup, before the environment-destroy call. The same active PR #1615 edits `cmd/baha/app_identity_selective_runtime_test.go` and `.github/workflows/pre-release-runtime-suite.yml`; my temporary overlapping test edit was reverted in `202b984e` and is absent from the final tree. Do not edit #1615 or its current shared files.
- Exact Draft run [44852435311](https://github.com/mcpdev80/baseharbor/actions/runs/44852435311) is running reduced Draft checks only. Exact current-head `pr-gate-plan.py` is `coverage_status=unresolved`: `commands.go`/`machine_coverage.go` need bounded registration coverage, `env_destroy.go` needs qualified native coverage, and catalog components do not yet own the changed paths. Continue with disjoint planner/catalog paths while #1615 owns the runtime workflow; no Ready promotion or merge.
