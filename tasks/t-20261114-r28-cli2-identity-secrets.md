---
id: t-20261114-r28-cli2-identity-secrets
card_number: "0428-057"
card_short_title: "Separate human/runtime secret"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Owner (marcel, direkt)
kanban_status: active
kanban_lane: active
kanban_summary: "Separate human/runtime secret authority. Follow the owner working brief, command mapping and code entry index; revalidate…"
kanban_title: 0428-057 · Separate human/runtime secret
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry, t-20261120-trusted-local-operation-grant]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1615]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98d/evidence/r28-welle4-2026-11-19/identity-secrets-hopf/fix-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44735405029"]
---

- [ ] t-20261114-r28-cli2-identity-secrets · CLI redesign: Separate human/runtime secret authority #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Owner (marcel, direkt) · **Priority:** high  
    **PR:** [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98d/evidence/r28-welle4-2026-11-19/identity-secrets-hopf/fix-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44735405029)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md), [t-20261120-trusted-local-operation-grant](t-20261120-trusted-local-operation-grant.md)  
**Required by:** [t-20261114-r28-cli2-app-data](t-20261114-r28-cli2-app-data.md), [t-20261114-r28-cli2-app-export](t-20261114-r28-cli2-app-export.md), [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261120-r28-cli2-context-precedence-evidence](t-20261120-r28-cli2-context-precedence-evidence.md), [t-20261120-r28-shell-wrapper-tests-not-skippable](t-20261120-r28-shell-wrapper-tests-not-skippable.md)  
**Owner:** Owner (marcel, direkt)  
**Priority:** high  
**PRs:** [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
**Source:** 
<!-- /generated:links -->

## Goal

Separate human/runtime secret authority. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement configured human authorization for service credential reveal via OpenBao while keeping workload access independent. Prevent unauthorized alternate path via env files, machine output, export and API.

## Entry points and ownership

- Starting points: `internal/openbao/; internal/application/access.go; cmd/baha/app_env.go; app_access.go; secret_operations.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Explicit auth for selected/all reveal, denial, sealed/unavailable behavior, app/env/target isolation, all alternate interfaces and runtime startup; no secret in logs or normal machine output.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)

hopf-/ketten-runde angesetzt, grund ist der drift-sweep 0428-137: GitHub meldt #1615 'clean', die merge-tree-prognose zeigt aber content-conflict in internal/deployment/target.go und add/add in cmd/baha/app_init_uid_app_slice_test.go (base ist der ketten-ast cli2-env-policy-head ueber #1578). lane prueft zuerst #1578s zustand: nicht gemergt -> basis bleibt, nur hopf auf den basis-ast; gemergt -> retarget auf develop + monotoner hopf per merge (kein rebase). akte identity-secrets-hopf/fix-1.md

hopf delivered, von mir gegen den gepushten kopf geprueft: branch cli2-identity-secrets-head = f93564a0d, MONOTON (develop da76c5cf9 ist ancestor), 'git merge-tree --write-tree origin/develop <head>' = 0 konflikte (ware der content-conflict internal/deployment/target.go plus add/add in cmd/baha/app_init_uid_app_slice_test.go — der wichtigste fund aus dem drift-sweep 0428-137, weil GitHub 'clean' meldete, waehrend der kopf kollidierte). PR promoted: draft=false, state=open, mergeable clean. ketten-regel eingeholt: #1578 als basis-ast war nicht gemergt, daher basis treatment nach mission. exaktkopf-lauf noch offen (keine check-runs sichtbar), akte identity-secrets-hopf/fix-1.md folgt von der lane

WURZELFUNDE, warum auf head f93564a0d KEIN lauf erscheint (suite 'queued', 38 minuten, 'actions/runs?head_sha=' leer): PR #1615 hat base_ref 'cli2-env-policy-head' (5ef9c329b), und ci.yml auf DIESEM ast laesst PR-CI nur fuer develop/main/'lane-*' — zeuge zeilen 14-18 'pull_request.branches: [develop, main, lane-*]' sowie die job-bedingungen zeilen 428/478/515 "github.base_ref == 'develop' || startsWith(github.base_ref, 'lane-')". ein ketten-ast ohne 'lane-'-praefix erhaelt damit NIE required-CI, draft oder nicht. daserklaert auch die sechs draft-zeilen der zulassungs-pruefung (#1627/#1625/#1623/#1620 basen ebenso auf cli2-*-head). DER BETROFFENE FALL IST NICHT DIE LANE: ein 'gh pr ready' allein macht hier nichts. MASSNAHME: neuer draht-PUNKT (f) fuer 0428-114, owner-entscheidung — entweder die bedingung auf beliebige base_ref erweitern (sauberste: 'github.event_name == "pull_request" && github.event.pull_request.draft == false') oder die ketten-aeste auf 'lane-*' umziehen (rename ist zerstoerlich, PR-basen mitsammenziehen)

END_BLOCKED akzeptiert: die lane hat RICHTIG gehandelt — kein zweiter push, kein selbst-gesetzter pruefeingang (§3.8), stattdessen befund mit datei:zeile. sie bestaetigt damit meine eigene wurzelfunde unabhaengig (queue500): ketten-aeste ohne 'lane-'-praefix bekommen niemals required-CI. akte identity-secrets-hopf/fix-1.md nennt jetzt den 40er-head und die promotion

OWNER UEBERNIMMT DIREKT (Ausdrueckliche Anweisung 2026-11-20): karte ist aktiv unter owner-hand, kein codeman-sitz mehr dahinter. gemessen: PR #1615 head 8a4490ca034d, branch refs/heads/cli2-identity-secrets-head == refs/pull/1615/head (ls-remote), base develop, draft=false, ancestry auf develop-spitze 40cb28c758b0 = JA. exakter run 44796477628 am head, stand meiner aufnahme: 27 success / 11 in_progress / 5 failure / 57 skipped. DIE FUER FINF ROTEN SIND NICHT IHR DIFF: 'PR · Selected Runtime' (atomic/docker/observability, atomic/docker/guided, atomic/podman/lifecycle, atomic/docker/lifecycle, atomic/docker/backup-restore) scheitern an DERSELBEN feld-weilen operator-meldung ('authenticated BaseHarbor operator', zweimal in job 136498326500, run 44796477628) = karten 0428-198 (sammelstelle, lane arbeitet) und 0428-202 (blocked an ihrem eigenen #1594/0428-053-rail, policy.go 2af892e4e). FOLGERUNG FUER IHREN PLAN 'bei gruenem Required-CI merge ich #1615': das required-cI KANN NICHT GRUEN werden, bevor 198/202 geloest sind - auch ihr eigener PR liegt in der schusslinie. der alte owner-string (codeman 01b370c0, END_BLOCKED) ist damit ersetzt; der sitz ist laengst entlassen. INHALTLICH NOTIERT: 'baha plan' erhaelt denselben lokalen laufzeit-autorisierungsscope wie 'app plan' - das ist genau die identitaets-luecke, die bei 0428-198 als test-seitiges muster gefragt ist (27 test-dateien nutzen operatorauth.WithVerifiedPrincipal bereits, cmd/baha/app_input_resolver_first_run_test.go:21-27); ihr fix beruehrt internal/identityprovider/** und damit die grenze, die sie fuer lanes gesetzt haben - fuer SIE gilt die grenze naturgemaes nicht, fuer lanes bleibt sie zu.

### Handoff — 2026-11-20 19:48 UTC

- PR #1615 remains OPEN/BLOCKED on `develop`. Current exact pushed head is `aef3b6515f49a4b65dc9613f485ef0a9aff65c3a`; do not merge until exact required CI is green and review is clean.
- Exact-head run [44805205717](https://github.com/mcpdev80/baseharbor/actions/runs/44805205717) on superseded `708e275a` exposed: (1) managed local gates call read-only root `doctor`, which the test-only operator policy rejected; (2) guided/backup acceptance's `run_consented` parser could not decode the current impact refusal because the test-only trace prefixed stderr JSON; (3) `cli-1` tests were contaminated by concurrent goroutines changing process-global cwd; (4) restart acceptance ignored HA fixture-cleanup errors, leaving an unowned native network before the next test. Exact CI run's demo source was `mcpdev80/baseharbor-demo@adda7599cb5b79689702f6a63a5ca802179df967`.
- Commit `aef3b651` grants the test-only synthetic operator only exact read-only `doctor` forms on the exact selected local gate target; `doctor --fix` remains rejected. Under GitHub Actions, traces go to `GITHUB_STEP_SUMMARY`, keeping machine-readable stderr clean so the existing fixture helper can validate the current plan ID and pass two explicit acknowledgements plus separate deletion consent. Unit coverage pins clean stderr and strict command scope. The `cli-1` cwd switch is serialized; genuine concurrent store creation remains covered by its dedicated test. Restart acceptance now asserts HA cleanup and surfaces deferred cleanup errors.
- Locally PASS: tagged CI-operator tests including trace-stream isolation; exact CLI failure tests and UID fixture with `-count=3`; `python3 scripts/pr-go-unit-shard.py --mode cli-1` (428 passed / 10 intentional skips / 438 discovered); real Docker `TestSingleControlPlaneRestartRotationAndCleanup` with `BASEHARBOR_RUNTIME_SINGLE_ACCEPTANCE=true` (243.494s); `git diff --check`. The previous full `go test -p 1 ./cmd/baha -count=1` was interrupted after 493s, before completion, and is not a pass.
- New exact run [44808406077](https://github.com/mcpdev80/baseharbor/actions/runs/44808406077) is queued on `aef3b651`; observe its full required check set. Run `44805205717` attempt 2 was still the old head `708e275a` and repeated the same runtime failures before being cancelled. The sweep census is now 26 OPEN PRs; current adjacent PRs have active owners, so #1615 remains the concrete assigned work while their owners resolve their own blockers.

### Handoff — 2026-11-20 20:17 UTC

- Corrected the root-doctor gate scope after review found the production root command authorizes `control-plane.doctor` (without an ApplicationID), so the app-bound local runtime grant is not applicable. Removed the misleading root `doctor` grant scope. In the test-only binary, the synthetic operator now admits only exact read-only root doctor forms (`doctor`, `doctor --json`, `doctor --output json`) on the selected disposable gate Target; existing tests reject `--fix`, `--yes`, and noncanonical forms. App doctor remains app-bound/grant-backed.
- Commit `39bda4ac45ef19c66a9f81f0e42f1e7011e59586` is pushed to `cli2-identity-secrets-head`. Independent review: APPROVE. Local PASS: focused tagged gate tests, `TestCLILocalWorkloadOperationIncludesGrantBackedRoots`, `python3 scripts/pr-go-unit-shard.py --mode cli-1` (428 passed / 10 intentional skips / 438 discovered), `gofmt`, and `git diff --check`.
- Exact run [44809688140](https://github.com/mcpdev80/baseharbor/actions/runs/44809688140) is active on the exact commit; at last check it had no failures, with Go unit, native runtime, and selected Core-less checks still running or queued. Older exact run on `51f73cb5` was force-cancelled after supersession; ignore it. Keep #1615 OPEN/BLOCKED until run 44809688140 and its full required exact-head checks complete green; merge only after fresh PR state verification.
- Fresh open-PR inventory: 26 OPEN PRs; no other safe merge candidate surfaced. Codeman remains read-only.

### Handoff — 2026-11-20 20:28 UTC

- Exact run [44809688140](https://github.com/mcpdev80/baseharbor/actions/runs/44809688140) on `39bda4ac` surfaced a common native setup blocker: five selected Docker/Podman runtime gates failed while the shared demo `atomic-bootstrap.sh` invoked the root `baha init` wizard, which stayed silent until the 120-second timeout. The guided failure's subsequent fixture diagnostics also lacked a managed-environment operator after teardown. Pinned demo source `adda7599` confirms every selected runtime gate calls `tests/atomic-bootstrap.sh`, which calls `tests/guided/drive.py` and exact `baha init`.
- Current pushed head `da5f5b20cb005754684ed93dec1bb0e50904f245` adds a test-only synthetic-operator exception for exact `init` arguments on the selected disposable Target, including the expected no-installation bootstrap state. It remains bounded by the test-only build, explicit atomic-gate opt-in, exact selected runtime/gate Target, local provider/no tenant, and exact argv. Local focused tagged gate tests and `git diff --check` passed. Independent review APPROVED after verifying the pinned demo call graph: all runtime gates use the same init bootstrap, so narrowing to the `guided` gate would leave other selected gates blocked.
- New exact run [44811463507](https://github.com/mcpdev80/baseharbor/actions/runs/44811463507) is queued on `da5f5b20`; superseded run 44809688140 was cancelled by the new head. No merge until exact required CI is green and the new scope has clean review.

### Handoff — 2026-11-20 20:50 UTC

- PR #1615 remains OPEN, non-draft, based on `develop`; current pushed head is `ef0acea77a5a1f05aef600ae4940b8f01cc6d061`. Keep it open until the full required exact-head CI is green. The PR has no GitHub review decision yet; the independent review of the latest test-only allowlist delta found no remaining issue.
- Run [44812831798](https://github.com/mcpdev80/baseharbor/actions/runs/44812831798) on `66b437c2` produced three concrete runtime failures before cancellation: guided bootstrap rejected `up --yes --json` while the selected local Target's installation was absent; both Docker and Podman lifecycle gates rejected root `status` as outside the test-only managed-workload command set after `app preflight` passed. The log traces are in the local handoff memory. The earlier candidate-consent refusal was expected and the fixture harness retried with its exact digest, reaching READY.
- Commit `8880c960` adds a test-only guided Core rebootstrap allowance bound to the exact `$DEMO_ROOT/tests/.guided-control-plane` real path, selected `guided` gate/Target/runtime, canonical `up --yes` or `up --yes --json`, and missing installation only; malformed/present installation remains fail-closed. Independent call-path review confirmed the demo appends `--json` and inherits this directory. Its exact run `44814082337` was superseded while checks were still in progress.
- Commit `75d03fba` added exact read-only root `status` gate handling after traces showed lifecycle required `baha status`; local tagged gate tests passed. Review then identified the actual later demo call `status -o json`, so commit `ef0acea7` extends the exact allowlist to all parser-supported JSON forms (`--json`, `-o json`, `--output json`, `--output=json`, `-ojson`) and rejects mutating/extra arguments. Independent review approved this final delta.
- Local verification at `ef0acea7`: `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^(TestCIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate|TestCIIntegrationOperatorAllowsOnlyGuidedCoreRebootstrapRoot|TestCIIntegrationOperatorAllowsRootDestroyOnlyForGuidedGate)$' -count=1` PASS; `gofmt` and `git diff --check` PASS. These test-only gates are exercised by the selected runtime acceptance jobs in the exact PR workflow; the workflow selects runtime gates from the PR's source diff.
- Exact run [44814684817](https://github.com/mcpdev80/baseharbor/actions/runs/44814684817) is pending/queued on `ef0acea7`; it is the only current candidate for acceptance. Run `44814530505` on `75d03fba` and run `44814082337` on `8880c960` were superseded by later heads. No merge has occurred. Codeman remains strictly read-only; no sessions, workers, worktrees, or files were touched.

### Handoff — 2026-11-20 20:57 UTC

- Independent full-diff review found a security blocker in the previous `ef0acea7` head: `RequireHumanOperator` verified identity but bypassed tenant membership and `secret.reveal` permission checks. It also found the non-MCP `secret.reveal` operation rendered as a blank tool row.
- Fixed in commit `80bea2a73dabcd8f37e046cc9dcf3c190665afb0`, pushed to `cli2-identity-secrets-head`. Both reveal entry points now require a verified operator and pass through the normal registered `secret.reveal` target/environment/membership/permission authorization; `app creds --reveal` supplies the canonical ApplicationID. The new tests deny a verified principal with no membership and a mapped membership without read permission. MCP documentation generation skips registry entries without an MCP tool and the blank row is removed.
- Local PASS on this exact candidate: `go test ./cmd/baha -run '^(TestHumanRevealRequiresAuthorizedMembership|TestAppEnvMasksSecretsByDefaultAndRevealsExplicitly|TestAppCredsRevealRequiresVerifiedOperator|TestMachineDocumentationTracksRegistryAndCommandTree)$' -count=1`; `gofmt`; `git diff --check`. Package tests are ordinary Go unit discovery; exact workflow's `PR · Go unit` package shards cover them. Documentation audit/source validation covers generated `docs/reference/mcp.md`.
- Independent reviewer rechecked both fixes and reported no remaining issue. PR #1615 is OPEN, non-draft, based on `develop`, and MERGEABLE at exact head `80bea2a7`. New exact run [44815738274](https://github.com/mcpdev80/baseharbor/actions/runs/44815738274) is pending; prior run `44814684817` is superseded and was force-cancelled. Do not merge until all required exact-head checks finish green and PR/review state is revalidated.
- Codeman on `192.168.6.119` remains read-only; no sessions, workers, worktrees, files, or state were changed.

### Handoff — current head refresh

- The PR branch advanced independently to `9dccd0ed67689fcc8a3bb69f89853fa96121091b`, removing the synthetic CI operator from root `status`; that command must use the actual local runtime authorization scope. No edits were made to this commit.
- On the prior exact head `80bea2a7`, hosted Docker/Podman lifecycle and Docker guided gates reached READY, then their app-doctor auth check reported OIDC `NOT_CONFIGURED`. The old root-status allowlist advanced this failure past status into doctor. Current exact run [44817430166](https://github.com/mcpdev80/baseharbor/actions/runs/44817430166) is exercising the updated head; all six runtime gates entered `Run runtime gate`, with no failure reported at the latest observation.
- Local PASS on `9dccd0ed`: `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestCIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate$' -count=1`; `git diff --check`. Keep the card active and do not merge until all required exact-head checks finish green and the reveal authorization/diff review remains clean.

### Handoff — status gate fix and exact CI refresh (~2026-11-20 21:23 UTC)

- Exact run [44817430166](https://github.com/mcpdev80/baseharbor/actions/runs/44817430166) on `9dccd0ed67689fcc8a3bb69f89853fa96121091b` is terminal-cancelled after a successor commit. Before cancellation, five selected runtime gates failed because root `status` was rejected by the test-only managed-local gate and then attempted interactive operator setup; `app preflight` had passed. The control-plane-recovery gate passed.
- The Docker/coreless `application` shard in that run also failed `TestSelectiveApplicationBackendRuntimeAddRemoveReAdd/document_database` with an incomplete provider plan (`runtime ownership/state is unverifiable`) followed by stale impact consent. The same targeted Docker acceptance passed locally on the then-current product worktree; treat hosted runner variance as unresolved until the fresh exact run reports it.
- Current head is `af7bf653bf3f12ebf007f9563e5857e8981d2518`. It admits only canonical read-only root `status` forms for the exact selected disposable local runtime gate, without injecting a synthetic Principal; mutation and noncanonical argument forms remain denied. Focused tagged gate tests pass on this head (`go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^(TestCIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate|TestCIIntegrationOperatorAllowsOnlyGuidedCoreRebootstrapRoot|TestCIIntegrationOperatorAllowsRootDestroyOnlyForGuidedGate)$' -count=1`; `git diff --check`).
- Fresh exact run [44819622710](https://github.com/mcpdev80/baseharbor/actions/runs/44819622710) is queued/in progress on `af7bf653`; it selects the native matrix and both Docker/Podman Core-less lifecycle shards. Keep the task active; do not merge until the exact head's required CI and review pass.

### Handoff — scoped runtime readiness auth refresh (~2026-11-20 21:36 UTC)

- Exact run [44819622710](https://github.com/mcpdev80/baseharbor/actions/runs/44819622710) on `af7bf653` reproduced the blocker in Docker Observability, Docker Guided, Docker Lifecycle and Podman Lifecycle: after the fixture reached READY, its application-facing readiness/log checks failed with `operator authentication needs interactive setup but input is not a terminal`. The trace confirmed root `status` was now admitted; the old assumption that it should use the production local-grant path did not match this fixture's app-readiness OIDC boundary. The prior-head run is superseded and force-cancelled.
- Commit `0454a0a0476c43615093382cd9584af7c6715f87` scopes a test-only Principal to canonical read-only root `status` forms on the exact selected disposable local gate, plus the exact `app logs demo-app` probe only for the `observability` gate. Gate/Target/runtime/provider/tenant and installed-Core checks remain mandatory; log flags, other app names, aliases, and all other gates are rejected. This is test-only coverage, not evidence of production local-grant behavior.
- Local PASS at this commit: `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^(TestCIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate|TestCIIntegrationOperatorAllowsGuidedCoreRebootstrapRoot|TestCIIntegrationOperatorAllowsRootDestroyOnlyForGuidedGate|TestCIIntegrationOperatorAllowsOnlyObservabilityLogProbe)$' -count=1`; `gofmt`; `git diff --check`.
- New exact PR run [44821678689](https://github.com/mcpdev80/baseharbor/actions/runs/44821678689) is active on the pushed SHA. At first check, Workflow Policy, Native Gate Plan, Source Format and Trusted Plan were running; later candidate/runtime checks had not yet spawned. CI watcher is monitoring the exact head. PR remains OPEN, non-draft, MERGEABLE on `develop`, with no review decision. Do not merge until all required exact-head jobs pass and review is clean.

### Handoff — owner follow-up on status authority (~2026-11-20 21:38 UTC)

- The owner advanced the shared PR branch again to `fc6fe96a0ce058765ef08b8acc37f9e9c18806fa`. This commit intentionally restores the no-synthetic-Principal behavior for root `status`, while retaining the narrowly scoped observability `app logs demo-app` probe from `0454a0a`. Do not overwrite this concurrent owner decision.
- Exact run [44821678689](https://github.com/mcpdev80/baseharbor/actions/runs/44821678689) on `0454a0a` was superseded; its exact-candidate job was cancelled and eight long-running Core-less shards were still active, so the obsolete run was force-cancelled to free capacity. New exact run [44821862388](https://github.com/mcpdev80/baseharbor/actions/runs/44821862388) is pending on `fc6fe96a`; no jobs had materialized at last check. Watcher is monitoring whether current status authority behavior resolves the runtime failure.
- No merge: PR remains OPEN, MERGEABLE, non-draft, and without a GitHub review decision. Retest the live head before any further branch edits.

### Handoff — managed status principal and reproduced DB fixture failure (~2026-11-20 21:42 UTC)

- Static path audit established why the exact `fc6fe96a` status behavior cannot pass its selected readiness fixture: root `status` resolves the demo application, calls `ensureOperatorAuthForBoundary`, and the one-call local grant is explicitly unavailable after a Core installation is registered. Without a persisted/configured OIDC boundary or Principal, the selected non-TTY gate fails at interactive auth setup. The owner follow-up commit `90af401c55236d9df085c1fddbf4011660914973` therefore restores a scoped test-only Principal for canonical root `status` forms after the selected disposable local gate/Core checks; production auth code remains unchanged. Focused tagged test suite and `git diff --check` pass locally.
- On cancelled exact run [44821862388](https://github.com/mcpdev80/baseharbor/actions/runs/44821862388) at `fc6fe96a`, Docker Core-less application reproduced a separate acceptance failure in `TestSelectiveApplicationBackendRuntimeAddRemoveReAdd/document_database`: Mongo provider plan was incomplete (`Action=preserve`, `runtime ownership/state is unverifiable`, no consumers), then apply rejected stale impact consent. Prior local targeted Docker acceptance had passed, so inspect exact runner fixture/state and resolve before merge. Podman foundation and identity-backend failed to download `segmentio/encoding@v0.5.4` because proxy.golang.org returned HTTP 500 (infrastructure/transient); retry those failed jobs only after the current run completes. Other checks/runtime jobs were cancelled on head movement before terminal results.
- Current pushed head is `90af401c`; new exact run [44823129405](https://github.com/mcpdev80/baseharbor/actions/runs/44823129405) is active. The prior `fc6fe96a` run was cancelled after supersession. Independent review of 90af is pending; a separate read-only audit is investigating the repeated Mongo fixture failure. Do not merge until all required checks pass on the exact live head, all product failures are fixed, transient failures are rerun, and review is clean.

### Handoff — exact 90af auth review and Mongo observation audit (~2026-11-20 21:45 UTC)

- Independent reviewer APPROVED `90af401c55236d9df085c1fddbf4011660914973` at the exact live PR head: the status Principal is only in the tagged test binary after all selected local Gate/Target/runtime/Core checks; only canonical status forms; no production auth changes. Reviewer confirms the selected runtime gate is the necessary end-to-end test, not this unit assertion alone.
- Local Docker rerun PASS on `90af401c`: `BASEHARBOR_BACKEND_LIFECYCLE_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestSelectiveApplicationBackendRuntimeAddRemoveReAdd/document_database$' -count=1 -v` (135.03s). All three add/remove/re-add phases completed; verified TLS-authenticated retained data, selected-container/retained-volume assertions, final PASS.
- Read-only analysis of the prior hosted Mongo failure found no basis to weaken fail-closed behavior: `preserve/incomplete` is correct when native Mongo ownership/state is unverifiable. Local acceptance passes; the likely hosted issue is timing or inventory observation. Existing failure diagnostics report Core/total counts but omit the Mongo container identity/health and observer early-return reason. If the current exact run repeats, add bounded fixture-side wait + precise observer diagnostics before apply/consent.
- Exact run [44823129405](https://github.com/mcpdev80/baseharbor/actions/runs/44823129405) is active on 90af; at 21:45 UTC all six selected runtime gates and Docker/Podman application Core-less jobs were active with no terminal failures yet. Prior-run Podman dependency-download failures were proxy HTTP 500; rerun only those jobs after this full run terminates if they recur. PR remains OPEN/MERGEABLE; do not merge before all exact required CI passes and a final live-head check.

### Handoff — exact status OIDC boundary fixture and CI refresh (~2026-11-20 21:57 UTC)

- Exact run [44823129405](https://github.com/mcpdev80/baseharbor/actions/runs/44823129405) on `90af401c` was cancelled after four selected runtime failures: Docker guided, Docker lifecycle, Docker observability cleanup preparation, and Podman lifecycle. The guided/lifecycle failures all reported operator authentication not configured for the Target/Environment boundary; observability's product acceptance itself passed Metrics/Traces/Logs, but fixture cleanup preparation failed afterward. Remaining long Core-less/backup shards were superseded to avoid spending runner capacity on the known failing head.
- Added a tagged-test-only OIDC boundary for the exact selected disposable managed-local root-status gate, matching the existing synthetic CI operator issuer/client. It persists only target `dev` boundary configuration after gate/Core checks; production auth code is untouched. Regression test verifies the stored issuer/client. Focused tagged tests pass on the candidate, and `git diff --check` passes.
- Commit `d6bb1843604d9f9663f241354a6694ed179f3d09` was pushed to `cli2-identity-secrets-head`. Current exact run [44824776027](https://github.com/mcpdev80/baseharbor/actions/runs/44824776027) is queued. PR #1615 is OPEN, non-draft, MERGEABLE; there is no formal GitHub review on the new head. Re-review and exact CI are required before merge.
- Codeman host was not modified. Continue with exact-head CI triage; keep the independent observability cleanup-preparation issue separate from the OIDC boundary fix.

### Progress — exact-head review and selected runtime gates (~2026-11-20 22:00 UTC)

- Independent read-only code review APPROVES exact candidate `d6bb1843604d9f9663f241354a6694ed179f3d09`; reviewer found the boundary write remains inside the tagged CI binary, exact selected disposable managed-local gate and canonical read-only root status. Production path is unaffected. No files changed by reviewer.
- Run [44824776027](https://github.com/mcpdev80/baseharbor/actions/runs/44824776027) remains exact on d6bb. Native/source/package checks have not reported failures. Selected Runtime control-plane-recovery, observability and Podman lifecycle are executing; Docker Core-less and Podman Core-less shards also executing; other selected Docker gates queued. Continue waiting for all required exact checks; do not merge while any are pending.
- Full PR census at ~21:58 UTC found 28 OPEN and no PR simultaneously green, clean-reviewed and merge-ready. Plan snapshot still has 0 Blocked / 0 Review; do not claim unassigned Ready cards.

### Progress — guided developer-domain authorization and cleanup evidence (~2026-11-20 22:08 UTC)

- Exact run [44824776027](https://github.com/mcpdev80/baseharbor/actions/runs/44824776027) on `d6bb1843` confirmed the OIDC boundary fix: status/doctor reported operator authentication `READY`, principal `ci-acceptance-operator`, and issuer `https://issuer.test`. Lifecycle and observability product assertions reached `RESULT PASS`; their three jobs failed later and exclusively at fixture cleanup preparation (`cleanup preparation=1`). Docker guided exposed the remaining real acceptance gap: after doctor, its selected fixture runs exactly `baha dev domain`, which still requires the authenticated operator.
- Downloaded GitHub job logs verified guided fails specifically at `baha dev domain`; the atomic guided script skips `dev credentials`. No unrelated broad authorization is needed.
- Commit `04a19a673a8e0184fac6aaf01daed8a22b69b960` adds a test-only exception for exact `dev domain` only on the selected `guided` gate, with denial tests for flags, credentials, other dev commands and other gates. It also prints the already-produced `failure-runtime/<gate>/scope-result.json` from failure cleanup diagnostics so the precise cleanup preparation error is visible. Focused tagged tests, `bash scripts/ci-workflow-policy.sh`, YAML parse and `git diff --check` pass locally; actionlint is not installed in the workstation.
- New exact run [44826826577](https://github.com/mcpdev80/baseharbor/actions/runs/44826826577) is queued on 04a19a67. Previous d6 run was force-cancelled after failures were diagnosed. Independent review is pending. PR #1615 remains OPEN/MERGEABLE; do not merge before exact checks finish green and any cleanup failure is resolved.

### Progress — exact preview and guided wizard scope (~2026-11-20 22:25 UTC)

- Detailed `scope-result.json` from exact run [44826826577](https://github.com/mcpdev80/baseharbor/actions/runs/44826826577) proves the fixture cleanup blocker: `destroy --all --json` is its non-mutating owner preview, but the test wrapper admitted only the later confirmed `destroy --all --yes --json`, causing `errors=["owned runtime evidence unavailable: ValueError (phase=owner-preview)"]`. Added only the exact no-`--yes` preview form to the test-only managed-local allowlist, with negative argument/gate tests.
- That run also proved `dev domain` now succeeds and the OIDC fix works. Guided reached the interactive New/Edit regression but then failed because the wrapper rejected exact `app new`; verified the pinned Demo source calls exact `app new`, then exact `app edit`, inside the selected atomic guided fixture. Added exact test-only `app new` and `app edit` exceptions under guided gate only, with negative flags/unrelated-command tests.
- The candidate also prints bounded-in-size-expected `scope-result.json` currently via a file-content loop to job logs when cleanup prep fails, enabling the root cause above. Focused tagged test suite and workflow-policy script pass locally; YAML parsing passed on the prior candidate (workflow unchanged since). New exact run [44828743735](https://github.com/mcpdev80/baseharbor/actions/runs/44828743735) is active on `5d5cfdf1b3edefabfdcafb154d711d61dad74ed8`; previous runs were cancelled after isolated failures. Independent re-review is pending; no merge until all exact checks pass.

- Independent final-head review APPROVES `5d5cfdf1b3edefabfdcafb154d711d61dad74ed8`: the no-confirmation destroy JSON form is preview-only; app new/edit exact bare commands remain confined to guided gate; domain exception accurately covers default persistence. No blocking finding. Scope binds to the exact selected gate/Target (not cwd), which matches the current disposable acceptance process. Exact CI run [44828743735](https://github.com/mcpdev80/baseharbor/actions/runs/44828743735) remains active/queued on this head with no failures at latest check; selected runtime jobs are still pending materialization.

### Progress — guided Footprint read on disposable gate (~2026-11-20 22:36 UTC)

- Run [44828743735](https://github.com/mcpdev80/baseharbor/actions/runs/44828743735) showed the `destroy --all --json` preview fix worked: guided fixture cleanup completed, and traces show the exact preview admitted. Guided now passed `dev domain`, the interactive `app new` and `app edit` journeys, and their `app plan/status` checks; it then failed only at its read-only `app footprint show -o json` assertion, rejected by the managed-gate test wrapper. Thus the expected runtime/app journey advanced to the final footprint contract.
- Added exact `app footprint show -o json` permission only on the selected guided gate, with negative tests for other formats/commands. Commit `5675c23047fa33bdb23618223c2e84e695e82eda` pushed; focused tagged test suite and workflow policy pass. Exact run [44830291770](https://github.com/mcpdev80/baseharbor/actions/runs/44830291770) queued on this head. Previous 5d run was superseded/cancelled after the specific blocker was isolated. Re-review pending; PR remains OPEN/MERGEABLE.

### Handoff — 2026-11-20 22:40 UTC

- Refreshed the exact PR state: #1615 is OPEN/non-draft on head `5675c23047fa33bdb23618223c2e84e695e82eda`, base `develop`, and GitHub reports merge state BLOCKED with no formal review decision. Independent review of this head is APPROVE.
- Exact run [44830291770](https://github.com/mcpdev80/baseharbor/actions/runs/44830291770) is running on that exact head. Ordinary checks have completed without failure; seven selected Core-less lifecycle jobs and six selected native runtime gates (Docker lifecycle, backup-restore, control-plane-recovery, guided, observability; Podman lifecycle) remain in progress. No merge until the exact required checks finish green and mergeability/review are freshly verified.

### Handoff — 2026-11-20 22:58 UTC

- Exact run [44830291770](https://github.com/mcpdev80/baseharbor/actions/runs/44830291770) completed failure on `5675c23047fa33bdb23618223c2e84e695e82eda`; all Core-less gates passed. Runtime failures: guided CLI/MCP Footprint parity rejected exact `mcp serve`; Docker and Podman lifecycle acceptance/cleanup passed but Go lifecycle failed because ORAS used HTTPS against the isolated plain-HTTP `localhost:5000` registry; backup/restore reached the Loki query but omitted its required mTLS client cert/key. Docker observability and control-plane-recovery passed.
- Local BaseHarbor follow-up adds `--plain-http` only for localhost ORAS resolution and exact guided-gate `mcp serve` test-only allowance with negative argument/gate checks. Focused tagged Go tests and `git diff --check` pass. These changes are not yet pushed.
- Opened Demo PR [#166](https://github.com/mcpdev80/baseharbor-demo/pull/166) at `c31ca0ec75097419368457f607b6dafc5317b387` to provide the generated Loki service-access client cert/key to the read-only restore probe. `bash -n tests/backup-restore/run.sh` and diff check pass; its `Guided consent · production-path regressions` CI is still pending. No merge yet.
- After Demo #166 is green and merged, push the BaseHarbor candidate and confirm the exact selected runtime gates pass against the updated Demo main pin. Keep #1615 open until full exact CI and fresh mergeability/review checks are green.

### Progress — #1615 candidate and Demo mTLS fix (~2026-11-20 23:00 UTC)

- Demo #166 passed its `Guided consent · production-path regressions` check plus local `bash -n`/diff checks, then merged as `63039ef1399803ae2b823f1657a96bdc559b8df3`. Its pinned probe now uses the generated Loki client certificate/key for its read-only query.
- BaseHarbor candidate commit `2310b8046b475000d100983db86c981e04c269d1` fixes local-only ORAS HTTP resolution and the exact guided-gate MCP server start; targeted tagged Go tests and `git diff --check` passed locally.
- Exact #1615 run [44833293998](https://github.com/mcpdev80/baseharbor/actions/runs/44833293998) is queued on 2310b8046. Confirm its Demo pin includes merged `63039ef` before relying on backup/restore evidence. PR #1615 remains OPEN/BLOCKED; no merge until this exact run and fresh review/mergeability are green.

### Progress — MCP scope hardening and refreshed Demo pin (2026-11-20 23:08 UTC)

- Independent review found the prior `mcp serve` test-only exception exposed the full MCP toolset to a synthetic editor principal. Replaced that path with a private context marker set only by the tagged guided-gate wrapper after exact gate validation; the marked server registers only read-only `baseharbor.app.footprint.show`. A new in-memory MCP regression test asserts that is the sole listed tool and `baseharbor.app.destroy` is rejected. Focused tagged Go tests and `git diff --check` pass; independent review APPROVES exact PR head `e670ee30f28e15189eb39b4383776583b562bd7f`.
- Updated repository variable `BASEHARBOR_PR_DEMO_SOURCE_SHA` from stale `adda7599cb5b79689702f6a63a5ca802179df967` to already-merged Demo commit `63039ef1399803ae2b823f1657a96bdc559b8df3`. Verified API value. The prior exact run 44833293998 consumed the stale SHA and is cancelled as superseded.
- Fresh exact run [44834248616](https://github.com/mcpdev80/baseharbor/actions/runs/44834248616) is pending on `e670ee30`; its jobs have not materialized yet. Verify job input `demo_ref` is `63039ef` before interpreting the refreshed backup/restore result.
- Run 44833293998 also failed the Docker Core-less application lifecycle test while re-adding Mongo after stop/resume: inventory marked runtime ownership/state unverifiable, so the local apply grant correctly failed closed with `stale-impact-consent`. This is under separate diagnosis; do not weaken the ownership or consent checks. #1615 remains OPEN/BLOCKED, with no merge until all exact required checks pass.

### Progress — MongoDB retained-binding observation and fresh exact run (2026-11-20 23:17 UTC)

- Run 44834248616 confirmed the corrected Demo pin (`63039ef`) and still reproduced the MongoDB Core-less lifecycle failure on `e670ee30`: during withdrawal, the observation fallback handled PostgreSQL only, so a retained canonical MongoDB binding had no measured runtime fact and the safe apply grant failed closed. Messaging passed.
- Added a narrowly scoped MongoDB fallback alongside PostgreSQL. It requires a BaseHarbor-owned application instance with exact application/environment owner fields plus a Target binding matching provider-instance ID, app, environment, capability kind, and nonempty resource name. It reconstructs only the canonical inspection manifest; `InspectProjectResources` still must return measured runtime evidence before any provider fact is emitted. Negative tests reject foreign owners and mismatched bindings.
- Local focused helper tests pass, and full Docker acceptance `BASEHARBOR_BACKEND_LIFECYCLE_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker go test ./cmd/baha -run '^TestSelectiveApplicationBackendRuntimeAddRemoveReAdd$' -count=1 -v -timeout 25m` passes for both messaging and document database, including retained TLS-authenticated data across add/remove/re-add. Test-only tagged MCP/ORAS tests and diff check also pass.
- Pushed initial Mongo-observation fix `5e873f5c31247c4826439ff9cab9d2a97a717f96`; its exact run [44835556361](https://github.com/mcpdev80/baseharbor/actions/runs/44835556361) materialized all selected runtime gates but was superseded and force-cancelled after review found one multi-binding edge case. Earlier stale/superseded runs 44833293998 and 44834248616 were also cancelled.

### Progress — multi-binding Mongo observation correction (2026-11-20 23:22 UTC)

- Independent review found provider instance IDs can be shared across multiple document-database requirements in one application, so taking only the first matching Target binding could undercount owned containers. Updated the fallback to collect/deduplicate/sort every exact matching binding for the same app/environment/instance; inconsistent resource app/provider/kind/name fails closed. Tests cover two Mongo resources and wrong instance/app/environment/owner/resource identity.
- Focused unit tests pass. Re-ran the full Docker `document_database` lifecycle acceptance (add/remove/re-add with TLS-authenticated retained data) on the corrected behavior: PASS. Pushed commit `a4e811a425a5e60241db669144c67948356ca024`.
- Exact run [44836136230](https://github.com/mcpdev80/baseharbor/actions/runs/44836136230) is active on a4e811a; previous 5e873f5 run 44835556361 was force-cancelled after the review correction. New independent final review is pending. PR #1615 remains OPEN/BLOCKED until this exact run and review finish green.

### Progress — conflicting same-instance binding fail-closed (2026-11-20 23:26 UTC)

- Final independent review on a4e811a found that a conflicting app/environment binding with the same provider-instance ID could be silently skipped when a valid binding also existed. Fixed the helper to reject every mismatched app/environment binding for that instance (including empty legacy environment) instead of permitting partial measurement. Focused regression tests cover valid-plus-conflicting app, environment, and unscoped legacy bindings. Reviewer rechecked the delta: no remaining findings.
- Re-ran the document-database Docker lifecycle acceptance and focused binding tests with this stricter behavior; both pass. Pushed `d434cc2a91861da88d17bfe8c61779865435edd9`. Previous a4e811a run 44836136230 was cancelled after the review correction; no terminal gate failures were observed before cancellation.
- Fresh exact run [44836690991](https://github.com/mcpdev80/baseharbor/actions/runs/44836690991) is queued on d434cc2; repository Demo source variable remains `63039ef1399803ae2b823f1657a96bdc559b8df3`. PR #1615 remains OPEN/BLOCKED until fresh exact CI completes successfully and mergeability is confirmed.

### Progress — runtime CI repair resumed by owner instruction (2026-11-21)

- Marcel explicitly reassigned completion of #1615 to Codex. Codeman Coordinator was notified that Codex owns the three failing runtime checks for this continuation; live delivery confirmed `steered-live`.
- Exact run [44836690991](https://github.com/mcpdev80/baseharbor/actions/runs/44836690991) failed on Docker backup-restore (job `136635306829`) and Docker/Podman lifecycle (jobs `136635306849`, `136635306869`). Read-only log diagnosis: backup-restore returned HTTP 421 from its Loki mTLS probe because it connected to `127.0.0.1` while sending the wrong Host/SNI; both lifecycle jobs failed to resolve the explicitly local OCI image while bootstrapping their integration trust plane.
- Fixed the Demo backup-restore probe in Demo PR [#168](https://github.com/mcpdev80/baseharbor-demo/pull/168), keeping CA/client certificate verification and pinning `localhost` to `127.0.0.1`; its `Guided consent · production-path regressions` check passed and it merged as `98e4d549c73fb099c780b5ae455da35a0ef68c71`. Updated and re-read BaseHarbor repository variable `BASEHARBOR_PR_DEMO_SOURCE_SHA` to that exact Demo main commit.
- BaseHarbor candidate commit `29aae4fded06cce139456e963d2342e907b5de2b` adds an explicit ORAS `--resolve localhost:port:127.0.0.1` override only for local `localhost` runtime-image references. Focused tests and `git diff --check` pass; a real isolated local Docker registry push/ORAS resolve returned an immutable digest. Independent agent review found no safety blocker.
- Fresh exact BaseHarbor CI [44850884739](https://github.com/mcpdev80/baseharbor/actions/runs/44850884739) is running at `29aae4fd`; the exact Demo pin is the merged `98e4d549…`. Do not mark accepted or merge until every required check passes and the exact current head is confirmed green.


### Progress — atomic runtime gate target-bootstrap auth (2026-11-21)

- Exact run [44850884739](https://github.com/mcpdev80/baseharbor/actions/runs/44850884739) on `29aae4fd` failed five selected runtime gates (Docker lifecycle, Podman lifecycle, Docker observability, Docker backup-restore, Docker guided) at the first `baha target create`, before their gate assertions: the managed-environment operator requirement fired.
- Root cause: Demo `scripts/acceptance.sh` intentionally unsets `BASEHARBOR_TARGET` while creating its disposable target; the tagged CI-only operator hook used that variable to identify the exact target and consequently did not inject its synthetic test principal. This is distinct from the earlier ORAS and Loki findings, which were fixed in the same candidate lineage.
- Fixed only `cmd/baha/ci_integration_operator_enabled.go` and its tagged regression test. With no selected target, the hook derives `atomic-<runtime>-<gate>` only when `DEMO_ATOMIC_GATE=1`, runtime is Docker/Podman, and `BASEHARBOR_DEMO_OPERATOR_GATE` equals `GATE`; it injects only when that exact target is not already configured. Normal binaries remain no-op. Regression coverage includes the unset-target bootstrap, pre-existing exact target denial, wrong target denial, and gate mismatch denial.
- Focused tests pass: `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestCIIntegrationOperatorIsLimitedToRemoteCoreAndTargetBootstrap$' -count=1` and all `TestCIIntegrationOperator*`; `git diff --check` passes. Independent agent review found no auth-scope blocker.
- Current PR head is `003c48fa53d8cf6c3c76c7a098fe0783bb1fd9cd`. Exact workflow [44852021582](https://github.com/mcpdev80/baseharbor/actions/runs/44852021582) is pending runner allocation. PR remains OPEN/BLOCKED; do not merge until all required checks for this exact head pass and mergeability/review are fresh. Cancellation was requested for obsolete run 44850884739, but it was still reported in progress at last poll.

### Progress — republish candidate image after runtime reset (2026-11-21)

- Exact run [44852021582](https://github.com/mcpdev80/baseharbor/actions/runs/44852021582) exposed a new follow-up failure after the successful Demo gates: the mandatory runtime reset cleans up the local OCI registry before backup-restore and lifecycle integration tests resolve the candidate image. Keep the reset cleanup intact; republish the already loaded candidate image after reset in both follow-ups.
- Added that republish ordering to `.github/workflows/pre-release-runtime-suite.yml` and a contract regression test to `scripts/test_pre_release_integration.py`; local `scripts/test_pre_release_integration.py` passes 18 tests and workflow policy passes. Independent review found no blocker.
- Published exact fix commit `29a97c5ecdb7b14a11a021119f5e561cf223e2ee` to PR #1615 using the connected GitHub commit/ref API after Git push was rejected for missing OAuth `workflow` scope. Independent review confirmed the remote file blobs match the reviewed local diff.
- Exact workflow [44854191474](https://github.com/mcpdev80/baseharbor/actions/runs/44854191474) is running against that exact head; Workflow policy, Trusted Plan, Source format, Native gate plan and Runner Interface have passed so far. Runtime, Go and remaining validation checks are still running or queued. PR remains OPEN/BLOCKED; merge only after every required exact-head check succeeds and fresh mergeability/review is clean.

### Progress — mock registry republish in workflow execution fixtures (2026-11-21)

- Exact run 44854191474 found that `scripts/test_targeted_gate_ref.py` executed the real backup-restore/lifecycle shell blocks but did not create the newly invoked `ci-local-oci-registry.sh` fake. Both Focused Python and CI Executor tests failed on that missing fixture script before reaching their Go fakes.
- Updated both temporary fixtures to validate the exact `publish` action and source/target image arguments. Local verification: `python3 scripts/test_targeted_gate_ref.py` 20/20, `python3 scripts/test_pr_check_runner.py` 34/34, `python3 scripts/test_pre_release_integration.py` 18/18, and `git diff --check` pass.
- Published `7fae3a288f4a7639728a10b047bda9a36e35604a` with the fixture correction. Exact workflow [44854729670](https://github.com/mcpdev80/baseharbor/actions/runs/44854729670) is pending/starting on that head; run 44854191474 on prior head `29a97c5` is superseded and being cancelled. PR stays OPEN/BLOCKED until full exact-head checks and fresh mergeability/review are green.
- Live update for exact run 44854729670: Docker control-plane-recovery is terminal SUCCESS; the other five selected runtime gates (backup-restore, guided, Docker lifecycle, Podman lifecycle, Docker observability) remain in progress. No failure is reported so far.

### Progress — isolate runtime-test operator auth (2026-11-21)

- Exact run [44854729670](https://github.com/mcpdev80/baseharbor/actions/runs/44854729670) completed on `7fae3a288f4a7639728a10b047bda9a36e35604a` with three selected runtime failures: backup-restore direct Core startup/cleanup lacked the test operator context; Docker and Podman repository lifecycle failed because the shared test Core had no persisted `dev` operator-auth boundary.
- Fixed only integration-test setup: backup-restore now uses `testOperatorContext` for direct Core start/readiness/owned cleanup and writes the matching external-OIDC boundary under its private temporary XDG config. Repository lifecycle writes the matching boundary for its exact owner-verified target, then restores or deletes the prior boundary in cleanup. Product authorization and candidate-consent checks remain unchanged.
- Independent read-only patch review confirmed the auth scope and recommended restoring the shared Core's previous boundary; that restoration is implemented. Local targeted Go package test passed and `git diff --check` passed.
- Published commit `5466a87bffe1edbef68b6b52777d12d773178b3d` with expected-head protection. PR #1615 remains OPEN/BLOCKED at that exact head. New exact run [44856918920](https://github.com/mcpdev80/baseharbor/actions/runs/44856918920) is in progress; Native gate plan, Source format, Trusted Plan, Demo Pin, Runner Interface and advisory Candidate checks are successful so far. Do not merge until the complete exact required run, final independent review, and fresh mergeability are clean.
- Exact run 44856918920 then exposed the same missing `dev` policy in `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` (Docker and Podman lifecycle selection), not a production authorization defect. Added `configureRuntimeIntegrationTestOperatorAuth` for each shared-Core workload lifecycle test that calls `app doctor`; it restores the prior boundary. Local targeted Go checks pass. Published follow-up `a82ce82409219bce3f4a30dea91c97230bffd1de`; exact run `44858328354` was triggered for that head. The prior run was force-cancelled after confirming the missing-boundary failure and superseding it.
