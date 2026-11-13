---
id: t-20261108-bughunt-0427-test-bootstrap-leak
card_number: "0427-127"
card_short_title: "test bootstrap leaks cores"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: cg-s3
kanban_status: closed
kanban_lane: closed
kanban_summary: "Runtime integration tests leave no residual bootstrap Core: after the test binary finishes, docker ps -a (and volumes/networks)…"
kanban_title: "0427-127 · test bootstrap leaks cores"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261108-bughunt-0427-target-env-ignored]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1454]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1454", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/22a3cb8a715f3a2063040ea3a3140c91d9e41ab6.json"]
---

- [x] t-20261108-bughunt-0427-test-bootstrap-leak · Bug Hunt v0.4.27: Test-Bootstrap leak't Cores #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** cg-s3 · **Priority:** normal  
    **PR:** [baseharbor#1454](https://github.com/mcpdev80/baseharbor/pull/1454)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1454), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/22a3cb8a715f3a2063040ea3a3140c91d9e41ab6.json)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261108-bughunt-0427-target-env-ignored](t-20261108-bughunt-0427-target-env-ignored.md)  
**Owner:** cg-s3  
**Priority:** normal  
**PRs:** [baseharbor#1454](https://github.com/mcpdev80/baseharbor/pull/1454)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Runtime integration tests leave no residual bootstrap Core: after the test binary finishes, `docker ps -a` (and volumes/networks) show zero `bh-w169-ci-bootstrap-*` objects created by that run, on both docker and podman cells.

## Problem (bug-hunt intake 2026-11-08, verified before carding)

Witnessed live on baha-docker 2026-11-08: three full Core stacks `bh-w169-ci-bootstrap-{2e0a4b61,d1dfaab2,afe2d8fa}-...` (keycloak/openbao/postgres sets) left `Up` by successive test runs of lane 0427-110-compose-native-acceptance. The prefix is hardcoded in `cmd/baha/runtime_integration_test_support_test.go:60` (`bootstrapTarget := "w169-ci-bootstrap-" + ...`); teardown does not destroy the bootstrap target (or fails silently), so every rerun leaks another isolated Core. "w169" is a stale wave label but the leak is current code.

## Acceptance

- Test teardown deterministically destroys the bootstrap Core (or t.Cleanup-registered full teardown on success AND failure paths).
- A CI-visible guard: a follow-up check step (same job) asserts zero leftover `bh-w169-ci-bootstrap-*` after the package finishes (CI-Aufnahmepflicht: runs in the existing go-integration job, no new engine).
- No behavior change for production destroy paths.

## Dependencies and file ownership

Depends on 0427-124 only if that fix changes target naming used by the helper; write-set: the test support file(s) under cmd/baha + one check step in the existing workflow that already runs the package.


## Audit 2026-11-08 — PR-Merge ist nicht Cleanup-Abnahme

- [#1454](https://github.com/mcpdev80/baseharbor/pull/1454) ist gemergt (`22a3cb8a715f3a2063040ea3a3140c91d9e41ab6`). Die Karte steht noch `review` und hat keine verlinkte Evidence in `evidence:`.
- Offener Akzeptanzbeleg ist der nachgelagerte Nachweis, dass nach den Docker- **und** Podman-Testpaketen keine `bh-w169-ci-bootstrap-*` Ressourcen verbleiben. Kein `closed` ohne diesen Cleanup-Beleg; Review-Owner-Eintrag bis Handover klaeren.


## Produkt-Code und CI — 2026-11-08

- `baseharbor/develop` `b73a13a9`: `cmd/baha/runtime_integration_test_support_test.go` hat `TestMain` mit Package-End-Teardown und langlebigem Cleanup-Marker; `runRuntimeIntegrationTestMain` uebernimmt nach Prozessabbruch verwaiste Marker, bricht bei fehlgeschlagener Adoption fail-closed ab und setzt einen Fehlercode, wenn Teardown scheitert. `destroyRuntimeIntegrationTrustPlane` entfernt Keycloak, Daten-Provider, Control Plane und prueft das Restinventar; eine Einzelschritt-Fehlfunktion verhindert die spaeteren Aufraeumversuche nicht.
- [PR #1454](https://github.com/mcpdev80/baseharbor/pull/1454) gemergt, exact-head [PR-CI #42464014150](https://github.com/mcpdev80/baseharbor/actions/runs/42464014150) terminal SUCCESS. **Code-Fix vorhanden.** CI-Erfolg allein ist jedoch keine hier eigens protokollierte Host-Nachmessung aller Docker-/Podman-Restobjekte nach dem Testpaket. Diese externe Restressourcen-Abnahme bleibt offen; deshalb Karte `review`, nicht voreilig `closed`.


## Full-card audit correction — 2026-11-13

0427-127 test-bootstrap cleanup remains open: record zero leftover containers, volumes, and networks after the Docker and Podman test packages. The merged implementation and earlier evidence are retained; no missing acceptance is inferred from a green unrelated workflow.

## 2026-11-13 Release qualification handoff

Core PR #1454 merged. Qualification only: attach actual post-test zero owned bootstrap container/volume/network inventory from Docker and rootless Podman. Do not re-implement teardown.

Existing implementation PRs have been retained; do not dispatch development Workers solely on this card. Attach current real checks/proofs and close only after exact-source Owner/Codex acceptance; an unrelated green selector is not native evidence.

## 2026-11-13 Maintainer acceptance — durable merge receipt

- Accepted on Marcel's clarification of the merge process: a successful merge is performed only after CI is green and all is well; the one receipt created for the merge is the durable proof of that state. Expired/deleted CI run records are not required as evidence.
- The receipt for PR #1454 is [`evidence/receipts/commits/22a3cb8a715f3a2063040ea3a3140c91d9e41ab6.json`](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/22a3cb8a715f3a2063040ea3a3140c91d9e41ab6.json), binding merge commit `22a3cb8a715f3a2063040ea3a3140c91d9e41ab6` to PR #1454. Per the Maintainer's process, this merge receipt is the acceptance proof for the cleanup fix and its CI checks.
- The earlier SSH access issue does not change this accepted merge evidence; no new runtime test was needed or started.

## 2026-11-13 cg-s3 qualification attempt

- Claimed as `cg-s3` and moved to active before qualification began. PR #1454 is merged; prior records contain Docker cleanup evidence, but the requested Docker and rootless Podman post-test inventories are not both present.
- Read-only SSH probes could not reach the designated hosts: aliases `baha-docker-2` and `baha-podman-2` fail DNS resolution; `192.168.6.205` rejects strict SSH because this machine has no trusted host key for it; `192.168.6.206` returns `No route to host`.
- No host key was accepted and no runtime test or resource mutation was started. Parked in `wait`; resume when routes are restored, Docker host identity is verified, and both native runtimes can be used for the exact-source cleanup proof.
