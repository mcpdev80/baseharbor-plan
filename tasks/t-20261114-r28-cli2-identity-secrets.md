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
**Required by:** [t-20261114-r28-cli2-app-data](t-20261114-r28-cli2-app-data.md), [t-20261114-r28-cli2-app-export](t-20261114-r28-cli2-app-export.md), [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md)  
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
