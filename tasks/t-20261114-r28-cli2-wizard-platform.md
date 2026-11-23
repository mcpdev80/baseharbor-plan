---
id: t-20261114-r28-cli2-wizard-platform
card_number: "0428-067"
card_short_title: "Platform and access wizards"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (stop-anweisung: kein retry) / Coordinator
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "Platform and access wizards. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-067 · Platform and access wizards
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-env-policy]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1620]
sources: []
blocker: "trusted BASE c6a7138 lacks owners fuer cmd/baha/app_access.go + app_access_test.go (PR touches beide, same-PR edit wirkt nicht  base-precedence). naechster trigger: merge der karte t-20261123-catalog-ingress-app-access (owner-abgestimmte surfaces: beide atomic data-caps, analog app_env_test.go + target_runtime_access_provider_test.go), dann EIN re-hop/re-run #1620. Kein retry bis dahin, kein force-merge, validation bleibt. depends_on gesetzt."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1620", "https://github.com/mcpdev80/baseharbor/actions/runs/44849270489", "https://github.com/mcpdev80/baseharbor/commit/28cb907dc0a678d1b5326df5203741c70cf84978"]
---

- [ ] t-20261114-r28-cli2-wizard-platform · CLI redesign: Platform and access wizards #task #release/v0-4-28 #status/blocked #view/blocked #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (stop-anweisung: kein retry) / Coordinator · **Priority:** high  
    **PR:** [baseharbor#1620](https://github.com/mcpdev80/baseharbor/pull/1620)  
    **Blocker:** trusted BASE c6a7138 lacks owners fuer cmd/baha/app\_access.go + app\_access\_test.go (PR touches beide, same-PR edit wirkt nicht base-precedence). naechster trigger: merge der karte t-20261123-catalog-ingress-app-access (owner-abgestimmte su…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1620), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44849270489), [proof 3](https://github.com/mcpdev80/baseharbor/commit/28cb907dc0a678d1b5326df5203741c70cf84978)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** b90e4ba1 (stop-anweisung: kein retry) / Coordinator  
**Priority:** high  
**PRs:** [baseharbor#1620](https://github.com/mcpdev80/baseharbor/pull/1620)  
**Source:** 
<!-- /generated:links -->

## Goal

Platform and access wizards. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement guided local/remote/organization/access/provider paths in assigned adapter files; keep device enrollment and user login separate and no local remote fallback.

## Entry points and ownership

- Starting points: `cmd/baha/onboarding*.go; access_wizard_command.go; provider_external.go adapters only; no archived Node Connector implementation`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No new Node Connector functionality, public repository implementation or Connector-based release qualification.

## Acceptance

User guided across empty/missing/ambiguous contexts; trust and destructive consent explicit; permissions and failure recovery; archived external repos not changed.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only review: [PR #1620 / 0428-067](../evidence/r28-welle4-2026-11-19/codex-review-wave/1620-0428-067-independent-review.md). Current PR head `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` has no checks and remains a Draft on `cli2-env-policy-head`; audit-write failure does not prevent the secret reveal, which conflicts with the stated fail-closed intent.

## Handoff

## Handoff — 2026-11-21

- Resumed after 0428-053 / #1594 merged. Confirmed PR base develop at `40cb28c758b02960356434b630086a341ebe1738`; source diff is limited to `cmd/baha/app_access.go` and its dedicated test file. Local focused reveal tests and `go vet ./cmd/baha` pass on the final PR head `28cb907dc0a678d1b5326df5203741c70cf84978`; source-readability check passes.
- Exact ready run [44849270489](https://github.com/mcpdev80/baseharbor/actions/runs/44849270489) on `28cb907d` completed FAILURE. Workflow policy, Trusted Plan, source format, build, vet and focused Python pass. All four CLI Go shards fail on managed-operator authorization/runtime test setup; the packages shard fails the existing Loki multi-source cases. `PR Selected Checks` consequently fails. The two reveal tests are scoped to a verified operator principal and passed locally; no green required full run is claimed.
- The prior exact run `44848273028` on `fcba5d25` rejected the stale integration base; it was corrected by the monotone merge of current develop plus commit `28cb907d`. No history was rewritten. The current branch is Ready and exact CI is now using the corrected ancestry.
- No merge. Resume when the shared CLI/operator-context + runtime shard issues and Loki fixture issue pass (`0428-204/#1615`, `0428-215`, `0428-202/#1732`), then rebase/hop if develop advances and rerun all exact required checks.


Implemented and pushed as `fcba5d25ce8ba644709e362b6fd2a1f048ca767a` to the existing #1620 branch from exact parent head `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d`. `app creds --reveal` now returns an error and emits no password/URI if `recordConnectionRevealAudit` fails. Added `TestAppCredsRevealFailsClosedWhenAuditWriteFails`, which makes the target audit path unusable and verifies no credential output; existing successful reveal-and-audit regression remains covered.

At candidate `fcba5d25`: focused `go test ./cmd/baha -run '^TestAppCredsReveal(FailsClosedWhenAuditWriteFails|WritesPerRevealAuditEvent)$' -count=1` passed; `go vet ./cmd/baha` passed; `git diff --check` passed. Full `go test ./cmd/baha -count=1` failed after 440.825s, without a reveal-test failure. Environment-dependent failures report activated target `dev-docker-1` missing in `TestDeterministicInitDoesNotPersistUnneededSourceSelection`, `TestDeterministicInitPersistsAmbiguousSourceSelectionPositive`, `TestGuidedInitQuickDoesNotPromoteHeuristicSecrets`, `TestGuidedInitInteractiveCanAcceptDetectedDefaults`, `TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds`, `TestGuidedInitExplicitFlagsKeepDeterministicPath`, `TestQuickInitPreservesWorkloadOnlyRepository`, `TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent`, `TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload`, `TestGuidedInitDeterministicPositionalEnvironmentAliases` (`-e` and `--environment`), `TestAppDownRejectsUnknownOptionsBeforeRuntime`, `TestRuntimeUpRequiresORASBeforeCoreBootstrap`, `TestInitializeRepositoryManifestForUpQuickCreatesDetectedContract`, and `TestCoreHAInventoryRejectsImageDriftAndMissingPeers`. `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` separately failed because host memory headroom was tight. These unrelated package-wide failures are not a green result.

PR #1620 remains OPEN+DRAFT on base `cli2-env-policy-head`; `gh run list --branch w067-cli2-wizard-platform` shows no run on the new exact head (only stale November runs). In `.github/workflows/ci.yml`, PR triggers and selected jobs qualify `develop`/`lane-*` bases, not this base. A `workflow_dispatch` run would not execute the PR-selected exact-head jobs. Await an approved stack/CI-routing action from the Coordinator/CI owner, then keep this Draft until its qualifying ready exact-head run is terminal. No workflow/shared-file edits, no PR promotion, merge, or acceptance performed.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befund (independent review 1620): cmd/baha/app_access.go, --reveal-Zweig: scheitert recordConnectionRevealAudit, wird der Fehler nur nach errOut geschrieben und das SECRET TROTZDEM ausgegeben — ein nicht geschriebenes Audit muss die Ausgabe blockieren (fail-closed).
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).

vorhop im fenster: keine PR-neuen quellen, kein katalog-touch (present belegt); alter run 44849270489 failure auf altem base-stand, neuer exact-head run nach push steht aus (b90e mission laeuft).
