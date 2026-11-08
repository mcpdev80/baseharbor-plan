---
id: t-20261108-bughunt-0427-appinit-owner-seam
card_number: "0427-136"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w136-appinit-r2
kanban_status: active
kanban_lane: active
kanban_summary: baha target create --reference local + baha app init --quick completes the native acceptance bootstrap path (documented flow…
kanban_title: "0427-136 · app init Owner-Naht regression"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-ci-lanes]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md"]
---
- [ ] t-20261108-bughunt-0427-appinit-owner-seam · Bug Hunt v0.4.27: app init Owner-Naht regression #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w136-appinit-r2 · **Priority:** normal  
    **PR:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md)  
**Owner:** lane-w136-appinit-r2  
**Priority:** normal  
**PRs:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
`baha target create --reference local` + `baha app init --quick` completes the native acceptance bootstrap path (documented flow incl. genuine Core bootstrap, e.g. baha up --control-plane-only) without ErrDeploymentOwnerMissing on the real-instance lifecycle; the #1347 owner enforcement keeps working for paths that genuinely require an owner (fix location decided 2026-11-08: the native acceptance harness must run the documented bootstrap so a genuine owner exists; product consent semantics unchanged (core_required without --yes stays, #1347 enforcement intact)). Regression runs in the CI-selected native/validate group it belongs to (test->check->trigger named).

## Problem (Fund aus 0427-132 r3, round-3.md — origin/main 48980d11)
`app init --quick` bricht in zeile 43 des native-acceptanz tests mit ErrDeploymentOwnerMissing bevor destroy/retry-Phasen erreicht werden. Ursache: #1347 (commit 42bfcb1c) macht VerifyDeploymentOwner Pflicht in der init-Naht ohne owner-establishment für reference-local targets. Reproduktion dreifach identisch: PR #1453 head 7557a0b1d, develop 07ae6c3e9, CI run 42434076648 (develop 1fe57f250) — v0.4.25 (bad37ce6) besteht.

## Acceptance
- Native acceptanz-pfad (target create --reference local + app init --quick) gruen auf aktuellem develop + PR #1453 head; #1347 enforcement bleibt intakt (kein revert der owner-pruefung, fix am seam); develop-zellen 'Native single-default Docker/Podman' wieder gruen.

## Dependencies and file ownership
Blocks completion evidence of 0427-132 (native acceptance). Write-set: cmd/baha app init seam + internal/deployment owner establishment; KEIN anrühren von runtime_destroy_all.go (#1453 domain) ohne drift-merge.
