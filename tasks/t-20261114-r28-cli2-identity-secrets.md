---
id: t-20261114-r28-cli2-identity-secrets
card_number: "0428-057"
card_short_title: "Separate human/runtime secret"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-057 (codeman 01b370c0, END_BLOCKED, sitz wird entlassen)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "Separate human/runtime secret authority. Follow the owner working brief, command mapping and code entry index; revalidate…"
kanban_title: 0428-057 · Separate human/runtime secret
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1615]
sources: []
blocker: "Der Trigger-Blocker ist behoben, aber der exakte PR-Head-Lauf 44735405029 auf ca930ce63c4ff080a736c6e3439dc1d87d017e0c ist rot: vier CLI-Go-Shards und ausgewählte/native Jobs scheitern am fehlenden Trusted-Local authority proof bzw. unkonfigurierten Runtime-Fixtures. Der Parent #1594 ist Draft und stale/conflicted; erst 0428-053 sicher end-to-end korrigieren, Parent aktualisieren, diesen Stack synchronisieren und neue exakte CI + Review bestehen lassen. Kein Promote/Merge vor grünen Checks."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98d/evidence/r28-welle4-2026-11-19/identity-secrets-hopf/fix-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44735405029"]
---

- [ ] t-20261114-r28-cli2-identity-secrets · CLI redesign: Separate human/runtime secret authority #task #release/v0-4-28 #status/blocked #view/blocked #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** 0428-057 (codeman 01b370c0, END\_BLOCKED, sitz wird entlassen) · **Priority:** high  
    **PR:** [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
    **Blocker:** Der Trigger-Blocker ist behoben, aber der exakte PR-Head-Lauf 44735405029 auf ca930ce63c4ff080a736c6e3439dc1d87d017e0c ist rot: vier CLI-Go-Shards und ausgewählte/native Jobs scheitern am fehlenden Trusted-Local authority proof bzw. unkonf…  
    **Needs:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98d/evidence/r28-welle4-2026-11-19/identity-secrets-hopf/fix-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44735405029)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Required by:** [t-20261114-r28-cli2-app-data](t-20261114-r28-cli2-app-data.md), [t-20261114-r28-cli2-app-export](t-20261114-r28-cli2-app-export.md), [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md)  
**Owner:** 0428-057 (codeman 01b370c0, END_BLOCKED, sitz wird entlassen)  
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
