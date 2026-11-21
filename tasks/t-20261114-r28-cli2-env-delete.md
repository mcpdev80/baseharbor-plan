---
id: t-20261114-r28-cli2-env-delete
card_number: "0428-055"
card_short_title: "Env deletion lifecycle"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex owner (combined validation ref)
kanban_status: wait
kanban_lane: wait
kanban_summary: "Environment deletion lifecycle. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-055 · Env deletion lifecycle
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1627, mcpdev80/baseharbor#1736]
sources: []
blocker: ""
wait_reason: "FIX IST GEPUSHT: exakter kopf jetzt ac05cc4efbc (beide refs, gemessen 04:0xZ), base develop 42da7128e72. der kandidat fuegt testOperatorContext fuer den lifecycle-kontext UND den cleanup ein - genau die stelle, an der ensureRepositoryDeploymentInputsForUp vorher 'requires authenticated BaseHarbor operator' meldete (test-fixture-defekt, nicht die funktion). der exakte hosted run 44958801932 steht auf pending (0 jobs), der mitlaufende 44958293233 ohne den fix bleibt aktiv und zaehlt NUR als diagnostik. WARTEGRUND: terminaler 44958801932 mit docker UND podman coreless-lifecycle-AUSFUEHRUNG im trusted plan; dann unabhaengiges verdict auf ac05cc4efbc inklusive der abhaengigkeits-erfuellung fuer #1736 (1e2ba9d5786 ist ancestor); dann ordinary merge in abhaengigkeits-reihenfolge (#1627 vor #1736). keine lane schreibt an diesem branch."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1627", "https://github.com/mcpdev80/baseharbor/commit/202b984e2a103d713bb688eb0b8be52f1ddfa677", "https://github.com/mcpdev80/baseharbor/actions/runs/44852435311", "https://github.com/mcpdev80/baseharbor/pull/1615", "https://github.com/mcpdev80/baseharbor/pull/1736", "https://github.com/mcpdev80/baseharbor/actions/runs/44859609354"]
---

- [ ] t-20261114-r28-cli2-env-delete · CLI redesign: Environment deletion lifecycle #task #release/v0-4-28 #status/wait #view/wait #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Codex owner (combined validation ref) · **Priority:** high  
    **PR:** [baseharbor#1627](https://github.com/mcpdev80/baseharbor/pull/1627), [baseharbor#1736](https://github.com/mcpdev80/baseharbor/pull/1736)  
    **Waiting:** FIX IST GEPUSHT: exakter kopf jetzt ac05cc4efbc (beide refs, gemessen 04:0xZ), base develop 42da7128e72. der kandidat fuegt testOperatorContext fuer den lifecycle-kontext UND den cleanup ein - genau die stelle, an der ensureRepositoryDeplo…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1627), [proof 2](https://github.com/mcpdev80/baseharbor/commit/202b984e2a103d713bb688eb0b8be52f1ddfa677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44852435311), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1615), [proof 5](https://github.com/mcpdev80/baseharbor/pull/1736), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44859609354)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Required by:** [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md), [t-20261114-r28-cli2-wizard-env](t-20261114-r28-cli2-wizard-env.md)  
**Owner:** Codex owner (combined validation ref)  
**Priority:** high  
**PRs:** [baseharbor#1627](https://github.com/mcpdev80/baseharbor/pull/1627), [baseharbor#1736](https://github.com/mcpdev80/baseharbor/pull/1736)  
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


## Wait-sweep progress — 2026-11-21 (trusted gate route)

- Revalidated that 0428-053/#1594 and 0428-054/#1591 are closed and #1627 is based on current develop `40cb28c758b02960356434b630086a341ebe1738`. Kept #1615 untouched.
- The trusted PR planner loads its gate policy from the PR base, so mappings added only inside #1627 cannot select its native runtime tests. Split the small trusted policy change into Draft PR #1736, head `8f11a34da52f7a7f81a48eaf8df75da6f0fc3f12`, to bind the implementation and exact test `TestEnvironmentDestroyNativeLifecycle` to existing Docker and Podman coreless lifecycle gates. Individual `commands.go`/`machine_coverage.go` changes remain unresolved without the companion implementation and native test.
- PR #1736 exact Draft run [44859609354](https://github.com/mcpdev80/baseharbor/actions/runs/44859609354) passed its Draft source/routing and Go-shard jobs; Ready-only planner, validation, and native jobs were skipped, so this is not full CI acceptance. Focused mapping suite (37 coverage tests), the two new planner cases, coverage catalog validation, Go unit/vet and generated CLI documentation checks pass locally.
- Local feature commit `f564c580c516139558faebc1038fba05766c3351` adds `TestEnvironmentDestroyNativeLifecycle`, registers it in both existing Docker and Podman coreless gates and the application shard, and regenerates the command indexes. This commit is not pushed; #1627 stays on its last hosted head until the trusted policy can be used. No local native runtime was run because the shared Docker host has active unrelated containers and Podman is unavailable. #1627 remains Draft and its implementation/test/docs changes remain local until the trusted mapping can be used.
- The full planner suite still reproduces the inherited operator-auth failure in `TestMCPRegistrationCIInProcessDiscoverAndInvoke` on current develop. Exact #1615 run `44858521941` was still in progress at last check; it remains owned by the other session.

review -> wait: RC besteht nur aus dem owner-scope receipt-punkt; branch bleibt beim owner

wait -> review: der einzige RC-punkt war der per-case-CI-receipt, der nach der loop-guard-regel als 'open item, owner-scope receipt-tooling' gefuehrt wird und den kandidaten nicht blockiert (rev-1736-r1). der owner hat 22:0xZ eine eigene source spot-check ohne substantiellen routing-befund geliefert (docker UND podman coreless gates fuer env destroy, full-bundle gating mit bewusst offenen registration-only-paden, native test in genau einer application-shard). zweiter durchgang ist dem reviewer zugestellt (sha256 33619fcda7c6, prioritaet 1).

APPROVE stands at head 10150ee7164 (akte 04eef2798 + e2f2aaf36, run 44940073029 = 22 success / 73 skipped). develop moved to 513488eeb6d, so the candidate is BEHIND and cannot merge on that head. Independent check by coordinator 23:4xZ: 'git worktree list' contains NO worktree for branch codex/env-destroy-gate-routing and no live session owns it, so the Owner performs a normal merge-commit hop of develop 513488eeb6d into the PR branch. After the hop: exact hosted CI must be green at the new head and a fresh independent review is required before the ordinary merge. Card stays review; nothing is accepted yet.

abhaengigkeit ausdrtuecklich festgehalten (korrektur der abnahme 00:3xZ): #1736 (head 1e2ba9d5786, exact CI run 44952497719 completed/success, 22 success / 73 skipped / 0 failed) ist NICHT mergebar, bevor #1627 mit named test registration und BOTH runtime-gate executions (docker UND podman) gelandet ist. #1627 head e24bd481 ist noch auf e6c199 aufgesetzt und sein bisheriger hosted run hat failures - die bedingung ist also NICHT erfuellt, die frische review an #1736 bleibt zurueckgehalten. w21 hoppt #1627 auf develop 513488eeb6d und nimmt den draft raus. die approve von 04eef2798 gilt nur auf dem ALTEN head 10150ee7164.
