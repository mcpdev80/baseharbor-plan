---
id: t-20261122-ci-operator-fixture-allowlist-gap
card_number: "0428-250"
card_short_title: "ci operator fixture allow-list"
type: bug
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0847d100 (baseharbor-demo fix - SESSION GONE)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-250 · ci operator fixture allow-list
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor-demo#170]
sources: []
blocker: "MIS-SCOPED PR: card is in Review on baseharbor-demo#170 but that PR only changes demo tests/config-matrix/run.sh and CANNOT fix the Core test-only operator fixture. The real #1812 blocker is in Core cmd/baha/ci_integration_operator_enabled.go (ciIntegrationManagedLocalGateReason :96 / predicate group :230-317): add allowlist branches for the 5 denied forms [config organization set, policy explain, app inspect ., target -o json, app list --all-targets] so the fixture stamps them instead of falling into noninteractive OIDC. Owner 0847d100 is GONE. Route the Core fixture change to an authorized owner/lane against baseharbor (NOT demo). Next trigger: authorized owner lands the Core fixture forms."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-ci-operator-fixture-allowlist-gap · Add the missing command forms to the test-only CI-operator fixture allow-list so static/core gates stamp the synthetic operator instead of failing closed #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** 0847d100 (baseharbor-demo fix - SESSION GONE) · **Priority:** high  
    **PR:** [baseharbor-demo#170](https://github.com/mcpdev80/baseharbor-demo/pull/170)  
    **Blocker:** MIS-SCOPED PR: card is in Review on baseharbor-demo\#170 but that PR only changes demo tests/config-matrix/run.sh and CANNOT fix the Core test-only operator fixture. The real \#1812 blocker is in Core cmd/baha/ci\_integration\_operator\_enabled…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0847d100 (baseharbor-demo fix - SESSION GONE)  
**Priority:** high  
**PRs:** [baseharbor-demo#170](https://github.com/mcpdev80/baseharbor-demo/pull/170)  
**Source:** 
<!-- /generated:links -->

## Found by H-V30 (f0f6c8b4) on develop 3cbb2bac

The 'authenticated BaseHarbor operator' needed by the static/core gates is a synthetic, test-only fixture present on develop via `cmd/baha/ci_integration_operator_enabled.go:24-119` (`withCIIntegrationOperator`, guarded by `DEMO_ATOMIC_GATE=1` + build tag `baseharbor_ci_operator_testonly`), stamped by `ciIntegrationOperatorContext` (:369-377, Subject `ci-acceptance-operator`, IssuerVerified true). The non-tagged build is a no-op (`ci_integration_operator_disabled.go:10`).

`ciIntegrationManagedLocalGateReason` (`:96-195`) builds an exact command-form allow-list (12 managedWorkload=true exceptions: read-only status :116, guided/observability/doctor :123-155, root-identity/init :161, local-core-bootstrap :304-352). A command form NOT in that allow-list (or a binary built without the tag) reaches `mcp.go:300/314-323` with no verified principal and fails closed with 'missing authenticated BaseHarbor operator'. The `coreinstallation.Load` check (:188-195) returns core-installation-not-loadable (:195), matching the atomic-podman-data-capabilities failure.

## Acceptance

1. Identify which failing command forms (init, up-as-bootstrap, config-matrix, reference-journey, shell-ux) are missing from the allow-list and add them to the TEST-ONLY fixture (`ci_integration_operator_enabled.go`), so the gate cells stamp the synthetic operator and proceed. Do NOT weaken production `operatorauth` / `mcp.go` boundary.
2. Confirm the affected pre-release/workflow invocations build with the `baseharbor_ci_operator_testonly` tag (if the gap is a missing build tag rather than an allow-list entry, report the exact place as a finding, do not fabricate).
3. Regression via existing static/CI cells; prove one previously-failing static cell now passes because the operator is stamped.

## Boundaries

cmd/baha test-only fixture file(s) with the build tag only. NOT operatorauth production code, NOT .github workflows (report any needed workflow tag/ordering as owner file:line, do not edit), NOT #1771 (local-workload layer), NOT target.create (247).

UMKLASSIFIZIERT (f0f6c8b4 H-V30): KEIN baseharbor allow-list gap. baseharbor ci_integration_operator_enabled.go ist bewusst eng+korrekt (:327-330 prefix baseharbor-core-bootstrap.*). Fix liegt in baseharbor-demo/tests/config-matrix/run.sh + reference-journey: temp-root prefix auf baseharbor-core-bootstrap.* + BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT exportieren (core-bootstrap.sh:9 muster). 0847d100 drauf. Entblockt #1746 static core-bootstrap/config-matrix/reference-journey/shell-ux zellen.

UMKLASSIFIZIERT (f0f6c8b4 H-V30): KEIN baseharbor allow-list gap. baseharbor ci_integration_operator_enabled.go:327-330 ist bewusst eng+korrekt (prefix baseharbor-core-bootstrap.*). Fix liegt in baseharbor-demo/tests/config-matrix/run.sh + reference-journey: temp-root prefix baseharbor-core-bootstrap.* + BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT exportieren (core-bootstrap.sh:9 muster). Entblockt #1746 static core-bootstrap/config-matrix/reference-journey/shell-ux. Repo: baseharbor-demo (nicht baseharbor).

UMKLASSIFIZIERT: baseharbor allow-list bewusst eng+korrekt; fix in baseharbor-demo tests/config-matrix + reference-journey (temp-root prefix baseharbor-core-bootstrap.* + BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT export). 0847d100 dispatched. Entblockt #1746 static core-bootstrap/ config-matrix/reference-journey/shell-ux zellen.

GELOEST in baseharbor-demo tests/config-matrix/run.sh (commit 0249c9f, demo PR #170 draft): temp-root basename baseharbor-core-bootstrap.XXXXXX (zeile 9) + BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT export vor core-up (core-bootstrap.sh:9 muster, bootstrap_root=matrix_root damit cwd==allowedRoot). Local docker smoke: baha up --yes allow-list + startet Core (PG/OpenBao) statt missing operator. baseharbor/.github/allow-list/guard unberuehrt. reference-journey/run.sh existiert nicht auf develop. Entblockt #1746 static core-bootstrap/config-matrix auth-zellen. Review auf baseharbor-demo CI + merge. Kein baseharbor aenderung.

RECONCILED (Owner sweep): #1812's 8 red light gates fail on the CORE test-only operator fixture allowlist cmd/baha/ci_integration_operator_enabled.go (ciIntegrationManagedLocalGateReason :96; predicate group :230-317), NOT on baseharbor-demo#170. The 5 forms ABSENT from Core allowlist (verified git grep on develop 5ab9fe4): config organization set, policy explain, app inspect ., target -o json, app list --all-targets -> fixture denies -> noninteractive OIDC. demo#170 is a separate demo-slice; it must NOT stand in for the Core fix. Required owner action: add these 5 predicate branches in the Core fixture. THIS (not #1812's workflow) is the last blocker to #1812 green.
