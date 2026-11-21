---
id: t-20261114-r28-cli2-app-export
card_number: "0428-065"
card_short_title: "App export and recovery UX"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: pr1625-0428-065-export (active)
kanban_status: review
kanban_lane: review
kanban_summary: "App export and recovery UX. Follow the owner working brief, command mapping and code entry index; revalidate current develop and…"
kanban_title: 0428-065 · App export and recovery UX
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1625]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor/commit/010db47dae0e0425f948914b3febc1ba86f41edc"
---

- [ ] t-20261114-r28-cli2-app-export · CLI redesign: App export and recovery UX #task #release/v0-4-28 #status/review #view/review #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** pr1625-0428-065-export (active) · **Priority:** high  
    **PR:** [baseharbor#1625](https://github.com/mcpdev80/baseharbor/pull/1625)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/010db47dae0e0425f948914b3febc1ba86f41edc)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** pr1625-0428-065-export (active)  
**Priority:** high  
**PRs:** [baseharbor#1625](https://github.com/mcpdev80/baseharbor/pull/1625)  
**Source:** 
<!-- /generated:links -->

## Goal

App export and recovery UX. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Provide guided encrypted app data export choosing eligible code/backups/secret/env/evidence, preserve backup/restore distinction and existing secure-profile export features.

## Entry points and ownership

- Starting points: `cmd/baha/app_backup_restore*.go; app_evidence.go; secure profile export implementation`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Selected scope only, encrypted archive, secrets consent, non-Git/OCI metadata, unavailable sources clearly reported; restore claims tested, no silent unsupported import.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only findings: [PR #1625 / 0428-065](../evidence/r28-welle4-2026-11-19/codex-review-wave/1625-0428-065-independent-review.md). Draft head `da7a4e62` has no exact-head checks; managed-secret export is unreachable/unimplemented, no positive authorized-path test exists, and authorization precedes interactive source selection.

## Handoff

2026-11-20 — implementation complete on the existing PR branch; no acceptance/merge yet.

- PR #1625 remains OPEN+DRAFT, based on `cli2-identity-secrets-head`. Remote branch advanced monotonically from exact reviewed head `da7a4e62cda17bcc167cd659c24f81bdff9f0d15` to `010db47dae0e0425f948914b3febc1ba86f41edc`; no force update. The live Codeman snapshot had no #1625 worker before the fast-forward.
- In `cmd/baha/app_export.go`, managed-secret discovery now authorizes `secret.list` and inspects metadata through the app's managed secret service; selected values use `GetMany` only after explicit `--include secrets/openbao` consent or interactive selection plus `RequireHumanOperator`. List/read backend details are redacted, and temporary value buffers are cleared after encryption or error.
- Tests added in `cmd/baha/app_export_command_test.go`: `TestAppExportManagedSecretsAuthorizedSelectionProducesEncryptedEntry` proves a verified operator can export/decrypt the selected managed secret while output and ciphertext do not expose it; `TestAppExportManagedSecretBackendErrorsAreRedacted` covers both list and read errors. Existing `TestAppExportManagedSecretWithoutOperatorFailsClosed` continues to prove denial.
- Exact candidate `010db47dae0e0425f948914b3febc1ba86f41edc`: `go test ./cmd/baha -run '^TestAppExport' -count=1` PASS; `go vet ./cmd/baha` PASS; `git diff --check` PASS. Test binding: normal package discovery; hosted trigger is the selected `PR · Go unit · cli-*` shard for `cmd/baha`, on a non-draft PR whose base is `develop` or `lane-*`.
- `go test ./cmd/baha -count=1` did not pass as a whole (510.671s). Reported failures included unrelated test setup/runtime cases such as a tight-host-memory preflight and tests resolving missing `dev-docker-1`; no failure named the app-export tests. This broad run is not acceptance evidence.
- `gh run list --commit 010db47dae0e0425f948914b3febc1ba86f41edc` returned no workflow runs. The current PR base `cli2-identity-secrets-head` is outside `.github/workflows/ci.yml`'s `pull_request.branches` allowlist (`develop`, `main`, `lane-*`); do not mark Ready or merge. Wait for #1615/0428-057, then hop onto an eligible base and require a fresh exact-head run.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befund (independent review 1625): cmd/baha/app_export.go:273-275 'managedSecretScopePresent' ist HARDCODED (false, nil), collectExportEntries (:279-298) behandelt den fall als leer — der ANGEKUENDIGTE managed-secret export ist nie verfuegbar. Entweder implementieren (mit positivem authorized-path-test) oder aus dem vertrag entfernen.
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).

## Implementation follow-up 2026-11-20

The managed-secret path is implemented and locally verified at commit [`010db47`](https://github.com/mcpdev80/baseharbor/commit/010db47dae0e0425f948914b3febc1ba86f41edc). Exact focused tests, package vet and diff check pass. The card is `wait` while #1615 remains blocked and the stacked base cannot trigger the required PR workflow; #1625 stays Draft. See the Handoff above for exact results and next trigger.

review -> active: round-2 verdict REQUEST CHANGES at f063d9788ab (akte review-2-headf063d978.md, zeile 14) - candidate-owned regression gap: TestAppExportManagedSecretWithoutOperatorFailsClosed does not assert secret-safe output nor the operator-auth denial as failure cause. Correction dispatched to the same session (mission m065rc2). Receipt-tooling gap recorded as owner-scope open item, non-blocking.

lane END delivered round 5: the managed-secret deny test now asserts the fixed operator-auth denial string plus secret-safe stdout/stderr and no artifact, with the fail-first proof recorded; exact CI run 44947499669 completed/success on head 01578b334fc. The second RC point (per-case CI receipt) stays an owner-scope open item and does not block the candidate (AGENTS 3.8). Next: hop onto develop 1080986fe73 (back=4), then full verdict on the hopped head, then ordinary merge.
