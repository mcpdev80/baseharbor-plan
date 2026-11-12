---
id: t-20261113-r28-console-api-contracts
card_number: "0428-009"
card_short_title: "Align Console Core decoders"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Align existing typed Core discovery/read-model decoders against the actual released 0.4.27 Core schema. ONLY update w"
kanban_title: "0428-009 · Align Console Core decoders"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-api-contracts · Align Console Core decoders #task #release/v0-4-28 #status/planned #area/console #kind/task

## Goal

Align existing typed Core discovery/read-model decoders against the actual released 0.4.27 Core schema. ONLY update wire decode/contract fixtures as necessary. Do not touch UI pages or change Core semantics. If Core operation missing, raise separate issue and stop that operation.

## Acceptance

One pinned Core commit, canonical schema/golden parity, valid and invalid decode cases and no fixture fallback; exact HEAD + check/trigger proof.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory.
- **Exclusive write ownership:** contracts/core-machine/v1/** and src/lib/baseharbor/{discovery,machine-wire,read-models}.ts as verified; worker must claim exact files before edit. No other shared session files or CI YAML.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

npm contract/architecture tests and canonical source-lock verification; negative unknown/malformed and cross-target responses.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Verified code entry points and no-guess rule (2026-11-13)

Current Console files: `src/lib/baseharbor/client.ts` already pins HTTPS/Core origin and bearer, `src/lib/baseharbor/read-models.ts` already contains `LiveCoreAdapter`, `src/components/live/live-core-view.tsx` already executes live apps/Targets/workspaces/runtime. Core source: `docs/spec/machine-http-v1.md`, `internal/machine/contract.go`, `cmd/baha/machine_http_operations.go`. Identify only exact mismatches and pin canonical source artifacts; do not rewrite working adapter or invent API routes.

Before coding, confirm files against exact current develop/main HEAD and actual named CI. If source differs, stop and hand one precise diff to Coordinator; no guessed endpoint or promise of success.
