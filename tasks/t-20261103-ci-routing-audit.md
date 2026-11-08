---
id: t-20261103-ci-routing-audit
card_number: "0427-101"
card_short_title: "conservative routing, ready-PR"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (CI routing audit 2026-11-03)"
kanban_lane: closed
kanban_summary: "Owner requests the JSON parser fix and a complete audit of all existing CI mappings, including current open PRs. Normal tests…"
kanban_status: closed
kanban_title: "0427-101 · conservative routing, ready-PR"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1349, mcpdev80/baseharbor#1350]
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/pull/1349, https://github.com/mcpdev80/baseharbor/pull/1350]
---

- [x] t-20261103-ci-routing-audit · CI: conservative routing, ready-PR cadence and reliable test execution #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI routing audit 2026-11-03) · **Priority:** critical  
    **PR:** [baseharbor#1349](https://github.com/mcpdev80/baseharbor/pull/1349), [baseharbor#1350](https://github.com/mcpdev80/baseharbor/pull/1350)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1349), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1350)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Owner:** Codex (CI routing audit 2026-11-03)  
**Priority:** critical  
**PRs:** [baseharbor#1349](https://github.com/mcpdev80/baseharbor/pull/1349), [baseharbor#1350](https://github.com/mcpdev80/baseharbor/pull/1350)  
**Source:** 
<!-- /generated:links -->

## Goal

Owner requests the JSON parser fix and a complete audit of all existing CI mappings, including current open PRs. Normal tests and the two-field commit receipt remain; no evidence/approval architecture is added.

## Scope and ownership

- Own scripts/pr-gate-plan.py, scripts/pr-check-runner.py, their focused tests, .github/workflows/ci.yml and a compact source-routing inventory/check.
- Parser lane owns runner and runner tests; coordinator owns planner/workflow; audit lane reads all mappings and inventories declared checks, workflow executors, test families and native gates.
- Preserve active Codeman product claims, their source branches and unpublished work. Product failures in State Owner remain with the product owner.
- Deployment routing must execute its package/consumer tests and actual Docker/Podman lifecycle where production ownership/state behavior is affected. Unknown valid paths must execute conservative Go unit/vet/build checks and applicable Docker/Podman lifecycle tests instead of blocking solely on a missing mapping. Invalid source/diff/catalog data still fails.

- Owner additionally requests cheap Draft-PR checks, selected checks on ready PRs and later pushes, no ordinary branch-push CI, and no duplicate develop-push suite after merge. Explicit validation branches/manual runs stay available.

## Acceptance

Go tool diagnostics cannot crash JSON parsing or hide failing tests. Every declared normal check and selected native gate has a real workflow executor. All explicit path mappings and required test families are inspected; missing/unimplemented routes are repaired or reported explicitly. Current open PR diffs are evaluated with the resulting policy. Focused local checks and normal hosted CI pass before merge. Rulesets remain off; no release/tag.

## Handoff

Resumed on explicit Owner instruction to publish and continue fixing CI. Claimed after reading current remote instructions and active product claims. Baseline develop 9a57107f; #1348 currently exposes JSONDecodeError, #1333 unknown deployment paths, #1347 actual owner-binding failures, #1334 old pre-migration CI result. No product implementation is taken over.

## Integrated CI correction

- Owner-authorized acceptance: PR #1349 merged to develop as a717c5f1412d5f8d02c68188204d3b891e1c7149. Exact candidate acebb12b07bdbb1a4ac98a25f440a0a7f59dac39 passed normal hosted run 41610825296, including every required validation and PR Selected Checks. This is not an independent review.
- Go JSON parsing separates stdout/stderr and retains real failures. Added Deployment/Broker package checks, recursive Runtime coverage, concrete Authority/ServiceIssuer bridge routes and execution for changed recovery/backup fixtures.
- Valid unknown paths select full Go tests/vet/build plus applicable Docker/Podman lifecycles. Invalid source/diff/path/catalog data still fails. No gate manifests, completed-run verification or receipt approval chain was added.
- Draft PRs run policy plus changed-Go formatting/readability. Ready PRs and their updates run selected checks. Ordinary branch pushes and develop merges do not start duplicate Source & Quality suites; explicit validation branches/manual validation remain.
- First candidate exposed pre-existing formatting debt in unchanged nonce_crypto_test.go. The follow-up scopes gofmt to changed Go files and has a real Git/gofmt regression proving unchanged debt does not block, changed bad formatting does fail and invalid diff references fail. It does not disable or autoformat product tests.
- Local validation: 237 combined regressions passed before the final small formatting correction; 10 relevant routing/fallback regressions and all-workflow actionlint passed after it. Hosted final run passed all normal selected checks. EN/DE audit/readability and local Go vet/build passed; worktree builds use -buildvcs=false. Broad local Go test attempt found the existing Docker-dependent real-lifecycle test; Docker is absent locally, so that attempt is not reported as green.
- The automatic writer created evidence/receipts/commits/a717c5f1412d5f8d02c68188204d3b891e1c7149.json with exactly commit and pull_request=1349. No duplicate Source & Quality run was launched for the merge SHA.
- Inventory reviewed all 51 normal check IDs, all PR-selectable gates, all 65 release checks and 1,992 tracked-path projections (699 targeted, 1,293 conservative fallback). Selection coverage is not product test success. All four fresh product PR projections resolve without gaps.
- Product sources remain unchanged by this repair. One tree-identical CI replan commit per open PR preserves each existing tree and uses expected-head leases: #1334 1d7dfd58, #1333 051b4035, #1348 6779d2cc, #1347 20f32c8f. New normal results are pending. Old #1348 failure is JSONDecodeError; old #1333/#1334 are missing mappings; #1347 additionally has real authoritative-installation-owner fixture/runtime failures and remains with its product owner.
- Automatic merge review initially rejected #1349 using stale queued status. Fresh exact-SHA check/run/job reads proved all required work successful; the ordinary expected-head merge then succeeded. No protection was bypassed.
- Rulesets remain off. No release/tag or product promotion to main was performed. Original unrelated worktree edits remain preserved.

## Final CI handoff

- CI correction accepted under Owner delegation. Follow-up #1350 merged as e90d7436c3353f85583d8fb4c385a0ba16783fc5 after exact candidate 39ac97f03fbc489b81b9349c6681d2739dcac632 passed hosted run 41611998033 and its final required check. Its two-field receipt is present. An older PR's event base can lag the actual integration parent; formatting now uses the authenticated candidate parents, with real Git/gofmt regression coverage for stale-base and linear inputs.
- Actual changed-file formatting errors were repaired mechanically in #1333 (f5183ded4b9b306ca4228a527e0c954556705d01; two Deployment test files) and #1348 (17aa2872ce9e5d7deaf620c9f6144cccc7d6ce5d; two Authority test files). Only gofmt whitespace/import ordering changed. Current Deployment and Authority package tests passed locally. Expected-head updates preserved concurrent product ownership.
- #1333's previous run 41611348234 passed both Docker and Podman lifecycle; only source formatting failed. New exact-candidate run 41612357682 has source formatting green and remaining runtime work in progress at handoff. No product acceptance or native-result reuse is claimed.
- #1334 was replanned with tree-identical head 7c4834bf7c545e453f37bebbbf20987577ec5889 after #1350. Run 41612448396 has source formatting green and remaining normal checks in progress at handoff.
- #1348 and #1347 were converted to Draft by the concurrent product sessions. Their current cheap Draft checks pass; required full product checks remain unqualified. The previous ready #1348 run was cancelled, not accepted. No Draft was marked ready and no product PR was merged by this CI task.
- The complete fresh PR projections have no unresolved mappings. Normal check outcomes remain authoritative; the CI fix does not accept unfinished product contracts or resolve the State Owner's actual ownership defects. No new active CI failure is known at this handoff, but pending product runs must still be inspected before product acceptance.
