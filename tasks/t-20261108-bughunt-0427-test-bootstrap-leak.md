---
id: t-20261108-bughunt-0427-test-bootstrap-leak
card_number: "0427-127"
card_short_title: "test bootstrap leaks cores"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: coord-board
kanban_status: wait
kanban_lane: wait
kanban_summary: "Runtime integration tests leave no residual bootstrap Core: after the test binary finishes, docker ps -a (and volumes/networks)…"
kanban_title: "0427-127 · test bootstrap leaks cores"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261108-bughunt-0427-target-env-ignored]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1454]
sources: []
blocker: ""
wait_reason: "PR #1454 implements teardown, but the card explicitly says post-test Docker/Podman inventory proving zero leftover bootstrap objects is not recorded."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1454"]
---

- [ ] t-20261108-bughunt-0427-test-bootstrap-leak · Bug Hunt v0.4.27: Test-Bootstrap leak't Cores #task #release/v0-4-27 #status/wait #view/wait #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** coord-board · **Priority:** normal  
    **PR:** [baseharbor#1454](https://github.com/mcpdev80/baseharbor/pull/1454)  
    **Waiting:** PR \#1454 implements teardown, but the card explicitly says post-test Docker/Podman inventory proving zero leftover bootstrap objects is not recorded.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1454)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261108-bughunt-0427-target-env-ignored](t-20261108-bughunt-0427-target-env-ignored.md)  
**Owner:** coord-board  
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
