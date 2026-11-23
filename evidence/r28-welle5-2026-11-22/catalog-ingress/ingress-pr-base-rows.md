# catalog-ingress PR #1790: register existing-path sources in base catalog (solve #1753/#1765/#1725 class)

- karte t-20261123-catalog-ingress-develop-prereqs, sitz f0f6c8b4. DEVELOP-ONLY KATALOG-INGRESS-PR (base-precedence test-erzwungen; DIE loesung fuer #1753/#1765/#1725-class).
- #1725 head-edit bleibt unangetastet (wirkungslos, spaeter harmless redundant, KEIN revert-noetig, KEIN dritter #1725-cycle).
- NUR scripts/pr-gate-coverage.json; KEIN product-code, KEIN .github. NO subagent.

## PLAN

1. FRISCHE branch/worktree lane-0428-ingress-catalog from origin/develop ef73b50b. git remote guard first. Confirm develop HEAD ef73b50b (ls-remote).
2. VIER EINTRAEGE (components-rows, mustergetreu internal.operatorauth.test.operator.go):
   - a) internal/operatorauth/local_runtime.go, runtime_specific true, surfaces = both atomic docker+podman data.capabilities
   - b) internal/operatorauth/local_runtime_test.go, same form
   - c) cmd/baha/control_plane_single_native_ci_test.go, same form
   - d) KEIN package-root-entry (owner-schienenroute 2026-11-23: #1725 fold into cataloged shared_backends_test.go -> base-ingress nur die drei component-rows)
   Pure additions, release stays v0.4.27, no existing entry changed.
3. LOKAL BELEGEN vor push: validate-pr-gate-coverage.py + test_pr_native_gate_plan.py (13) + test_pr_gate_coverage.py (41). ALLE gruen.
4. PR #1790: base develop, title 'ci(0428-ingress): register existing-path sources + internal/application package-root in base catalog', body mit verweis on karte + blocked PRs #1753/#1765/#1725. PR NOT draft. ls-remote witness. KEIN merge.
5. EXACT hosted: TP MUST green (catalog-only diff, no product source). run-id + gates.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop): ef73b50b6aee3dea8d4badf347c264daefa3d064
- new branch: lane-0428-ingress-catalog (worktree detached HEAD ef73b50b -> commit b103495b6)
- new head: b103495b6ee53ee61b4f9d4ddd85400ca12b2367 (git log --oneline ef73b50b..HEAD = ONLY my commit)
- PR #1790: base develop, head lane-0428-ingress-catalog, state OPEN, isDraft false
- only file changed vs develop: scripts/pr-gate-coverage.json (27 insertions, 0 deletions)

## Catalog entries added (mustergetreu internal.operatorauth.test.operator.go)

- internal/operatorauth/local_runtime.go -> id internal.operatorauth.local_runtime.go, runtime_specific true, surfaces [source.gate.atomic.docker.data.capabilities, source.gate.atomic.podman.data.capabilities]
- internal/operatorauth/local_runtime_test.go -> id internal.operatorauth.local_runtime_test.go, same form
- cmd/baha/control_plane_single_native_ci_test.go -> id cmd.baha.control_plane_single_native_ci_test.go, same form
- release field stays v0.4.27. No existing catalog entry changed (pure additions).
- All three source paths exist on develop (git cat-file -e origin/develop:path = EXISTS for all three).

## Local verification (pre-push)

- validate-pr-gate-coverage.py: "PR gate coverage catalog is valid" (exit 0)
- scripts/test_pr_native_gate_plan.py: 13 tests OK (exit 0)
- scripts/test_pr_gate_coverage.py: 41 tests OK (exit 0)
- ci-fast-check.sh: PASS (exit 0)

## EXACT hosted — CI run 45086017941 @ b103495b6

- FULL GREEN, zero failures, PR Selected Checks = success.
- Key gates:
  - PR · Trusted Plan: success (catalog-only diff, no product source — exactly the mission requirement)
  - PR · PR Selected Checks: success
  - PR · Validation · receipt-execution-tests, pr-planner-tests, ci-policy, ci-executor-tests: success
  - PR · Source format: success
  - PR · Native gate plan: success
  - PR · Focused Python: success
  - PR · Candidate-added checks (advisory): success
- Skipped (not run by this PR): validate, Workstation onboarding, Targeted HA docker/podman, Release Source Preflight, Selected Runtime, Selected Core-less, Runner Interface, Public Contracts, Native ${{ matrix.id }}, Native Keycloak/Core, Main release source/checks/Go, Go unit shards, Exact full Pre-Release, Exact Candidate, Draft source/Go, Demo Pin, Consumer Pins.
- No failures.

## Why this resolves #1753/#1765/#1725 class

- Base-precedence is now test-enforced (Trusted Plan reads the catalog from the trusted base ef73b50b, not PR head). These three sources already exist on develop but had no declared runtime-gate owner, so the fail-loud guardian blocked PRs in the class. Adding base catalog rows admits the sources without any product-code change — the systemic fix.
- #1725 head-edit (e6907e591, discarded in the previous turn per owner BEFEHL-KORREKTUR) remains untouched; this ingress PR is a separate develop-only PR and does not touch the #1725 branch.

## Melden

- PR: #1790 (base develop, head lane-0428-ingress-catalog, OPEN, not draft)
- head: b103495b6
- CI run: 45086017941 (FULL GREEN, TP green)
- catalog diff vs develop: 3 new component-rows, release v0.4.27

## END

END_DONE w27-pr1627-0428-061-pull: catalog-ingress PR #1790 DONE. base develop + head lane-0428-ingress-catalog + commit b103495b6. 3 catalog component-rows added (internal/operatorauth/local_runtime.go, local_runtime_test.go, cmd/baha/control_plane_single_native_ci_test.go) — mustergetreu internal.operatorauth.test.operator.go, runtime_specific true, both atomic docker+podman data.capabilities. Pure additions (27 insertions/0 deletions), release stays v0.4.27, no existing entry changed. No package-root entry (#1725 folds into cataloged shared_backends_test.go per owner-schienenroute). Local pre-push: validate-pr-gate-coverage.py valid, test_pr_native_gate_plan.py 13 OK, test_pr_gate_coverage.py 41 OK, ci-fast-check PASS. PR #1790 OPEN, not draft, base develop, body references karte t-20261123-catalog-ingress-develop-prereqs + blocked PRs #1753/#1765/#1725. CI 45086017941 @ b103495b6 = FULL GREEN, zero failures: Trusted Plan GREEN (catalog-only diff, no product source), PR Selected Checks GREEN, receipt-execution/pr-planner/ci-policy/ci-executor tests + Source format + Native gate plan + Focused Python green. #1725 head-edit untouched. No merge. Evidence on origin/main. cleanliness: catalog-only edit, docker ps -a clean (no containers started locally).
