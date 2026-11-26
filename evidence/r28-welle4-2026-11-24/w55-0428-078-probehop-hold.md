# w55-0428-078-probehop: #1818 HOLD for owner — identity catalog producer is #1819 (unmerged dependency)

## Lane identity
- Card: 0428-078 (task t-20261114-r28-perses-dashboard-identity)
- PR: baseharbor#1818 · branch lane-0428-078-cf-fix
- Owner session: w55-0428-078-probehop
- PR #1650: superseded by #1818

## Base attestation
- My branch HEAD (ls-remote witness): 0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f refs/heads/lane-0428-078-cf-fix
- develop remote HEAD: 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd (remote HEAD moved 840c4a6b->cd2fcda->3ebfb90d during shift)
- Remote URLs (git remote -v): lane-origin + origin both ssh://git@github.com/mcpdev80/baseharbor.git (resolved, not a local path)

## Owner ruling (2026-11-24, authoritative)
persesDashboardCatalog / PersesDashboardAvailability / backendForKey INTENTIONALLY realize ONLY
observability backends (Prometheus/Loki/Tempo) and DELIBERATELY exclude identity. Do NOT add
keycloak-identity to persesDashboardCatalog, and do NOT modify backendForKey / PersesDashboardAvailability.
The existing TestPersesDashboardKeysMatchSelectionCatalogKeys deliberately SKIPS DashboardBackendIdentity —
this is the codebase's intended contract: identity dashboards are NOT in the observability catalog.

## The failing Go unit test
- Test: TestPersesKeycloakDashboardQueriesSelectRealProviderLabels
- File: internal/metrics/perses_dashboards_test.go:768
- Failure: reads `persesDashboardCatalog()["keycloak-identity"]` from the OBSERVABILITY catalog
  (internal/metrics/perses_dashboards.go), which by design has no keycloak-identity entry.
- My prior commit c85c38f8 added keycloak-identity to that catalog — this is the scope violation.
  Owner confirmed: #1818 head 20fc1cb7 is GREEN ONLY because its diff adds keycloak-identity to
  persesDashboardCatalog(). Owner is REOPENING #1818 (review -> active) for correction.
- I removed c85c38f8 (hard reset back to remote head 0f20a3b9). Working tree clean; catalog untouched.

## Where the identity dashboard is genuinely produced (traced)
- internal/metrics/perses_dashboards_keycloak.go: persesPanelKeycloak() panel SET (3 queries) exists
  but is ORPHANED — never assembled into a PersesDashboard, never referenced.
- internal/metrics/testdata/perses-dashboards/keycloak-identity.json: golden PersesDashboard exists.
- internal/capability/perses_selection.go: owns DashboardBackendIdentity + the keycloak-identity
  DashboardTemplate (lightweight struct, NO PersesDashboard resource) + eligibility logic.
- internal/metrics/perses_dashboards.go: persesDashboardCatalog() — observability catalog —
  deliberately excludes identity.

## Dependency chain (baseharbor-plan evidence)
Task t-20261124-gate-catalog-baseline-1819 (card 0428-273) states the owner-ordered chain:

  1. 0428-273 (Owner/CI scope, scripts/** + gate catalog): add #1819 source rows to develop
     pr-gate-coverage.json (surfaces docker + podman) for:
       - internal/application/runtime_postgres.go
       - internal/metrics/perses_dashboard_provision.go
       - internal/metrics/perses_dashboard_provision_test.go
     develop head 69f76b94 currently FAILS Trusted Plan because these paths have no declared
     gate owner; every downstream Go/runtime job skips. 0428-273 is a SEPARATE baseline PR on
     develop (precedent #1817), NOT inside #1819.
  2. 0428-181 / #1819 (owner w54): the identity dashboard catalog producer
     internal/metrics/perses_dashboard_provision.go. Rebases onto the post-0428-273 develop head
     and reruns exact-head. Owner accept+merge.
  3. #1818 (me): depends on #1819. Once #1819 merges, #1818 dependency is satisfied -> Owner accept.

Proof #1819 is unmerged: `git show develop:internal/metrics/perses_dashboard_provision.go` -> path
does not exist on develop 3ebfb90d. `w54-0428-181-export` branch @ 69f76b94 is open/unmerged.

## Owner lean: FIX C (architecture decision pending owner)
Owner leans FIX C (vs A): the test should point at the 0428-181/#1819 identity producer seam and
consume it as a DEPENDENCY — no duplicated producer in #1818. This is an owner architecture decision
(single-source-of-truth: #1819 is the designated producer, but it is unmerged and catalog-blocked).

## Exact needed change (finding with file:line)
#1818 cannot complete its Go unit fix until the #1819 identity producer seam exists on develop.
That requires, out of my write-set:
- 0428-273 (scripts/pr-gate-coverage.json, Owner/CI scope): add the 3 catalog rows so develop's
  Trusted Plan stops skipping #1819's paths (file:line scripts/pr-gate-coverage.json, per task
  t-20261124-gate-catalog-baseline-1819).
- #1819 (w54, internal/metrics/perses_dashboard_provision.go + _test.go): merge onto develop.
Then #1818 consumes the seam (points the failing test at the #1819 producer, not the observability
catalog).

## Docker consent exit-41 (unchanged)
The pre-release docker identity acceptance (run 45307918949, job exit 41,
"record-deployment-before-mutation: candidate submission requires an explicit operator/automation
consent (--confirm-candidate)") requires an operator/automation consent I cannot self-grant. This
is an OWNER authorization. Consent validation must NOT be weakened. Left STOPPED pending owner;
do not re-add the consent grant or weaken the validation.

## CROSS-SESSION BRANCH CONTAMINATION (critical finding)
Remote branch lane-0428-078-cf-fix was FORCE-PUSHED from 0f20a3b9 to 20fc1cb7 during this shift.
20fc1cb7 is authored by w53-0428-152-alertfix (a DIFFERENT session), built on develop 3ebfb90d,
commit "fix(0428-078): wire keycloak identity dashboard into develop metrics catalog". It RE-INTRODUCES
the exact scope violation the owner forbids:
  - backendForKey gains `case "keycloak-identity": return capability.ProviderKeycloak`
  - perses_dashboards.go +26 (keycloak-identity re-added to the observability catalog)
  - adds cmd/baha/ci_integration_operator_enabled.go (+ its test) — a #1815 fixture, out of my scope
20fc1cb7 is GREEN ONLY because of that forbidden catalog edit (matches the owner's HOLD finding).
My local HEAD is 0f20a3b9 (clean, no catalog edit); my 0f20a3b9 is NOT an ancestor of 20fc1cb7 (they
diverged). I did NOT write 20fc1cb7 and do NOT preserve/build on it. This is a cross-session write onto
my branch head and should be reset to my clean lane head before any #1818 correction is built.

## Park state
- No new head pushed BY ME. My local HEAD @ clean 0f20a3b9. Working tree clean. Observability catalog
  untouched (no keycloak-identity entry added on my side).
- The remote branch now carries another session's violating 20fc1cb7; owner is REOPENING #1818
  (review -> active) to correct exactly that violation.
- HOLD pending owner A-vs-C decision. Do not touch the observability catalog. Do not build on 20fc1cb7.

## END
END_BLOCKED w55-0428-078-probehop: HOLD for owner per 2026-11-24 ruling. #1818 Go unit failure is an
external dependency: the identity dashboard catalog producer (#1819, internal/metrics/perses_dashboard_provision.go)
is unmerged (not on develop 3ebfb90d) and catalog-blocked (needs 0428-273 scripts/pr-gate-coverage.json
rows, Owner/CI scope). Owner leans FIX C (point test at #1819 seam, consume as dependency). Do NOT touch
the observability catalog. Docker consent exit-41 remains an OWNER authorization, left STOPPED. Ack 'holding for owner A-vs-C'.
