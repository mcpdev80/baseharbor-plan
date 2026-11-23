# 0428-201/#1725: test-relocalisation into base-cataloged sibling

- karte 0428-201/#1725, sitz f0f6c8b4. TEST-RELOCALISATION (owner-route, makes base-ingress need disappear): regression lines moved from the PR-NEW file into the already base-cataloged internal/application/shared_backends_test.go.
- NO subagent, NO .github touch, NO product-logic edit, NO merge.
- CI run 45088370048 @ a84a3ebc5 = FULL SUCCESS, zero failures. Trusted Plan GREEN.

## PLAN

1. hold PR-head (#1725): gh pr/ls-remote. numstat vs develop before.
2. VERSCHIEBEN: move 108-line regression test from internal/application/shared_backends_state_version_test.go INTO internal/application/shared_backends_test.go (package beibehalten, imports zusammenfuehren, test-names unchanged). LOESCHEN now-empty new file. REMOVE new-file catalog entry -> catalog BYTE-IDENTICAL to develop (diff EMPTY; sibling already base-registered).
3. HOPPEN onto origin/develop c6a7138ce: git merge --no-ff (KEIN force/rebase/amend). go vet + package test local (named run form).
4. push bereinigter head + ls-remote refs/pull/1725/head witness. PR open/ready. KEIN merge.
5. EXACT hosted bis terminal: TP now GREEN (no uncataloged source, only base-owned shared_backends_test.go touched). head + run-id + catalog==develop + gates.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop): c6a7138ce2bf7de88f45f2a68e5168c835601a16
- #1725 branch: w201-0428-201-statever (base develop, state OPEN, not draft)
- to-be-deleted file: internal/application/shared_backends_state_version_test.go (was 108 lines)
- target sibling (base-cataloged): internal/application/shared_backends_test.go (was 276 lines -> 376 after relocation)
- new head: a84a3ebc5df09cbd72523543636459b9b22376df (git log --oneline origin/develop..HEAD = ONLY my relocation commit on top of the additive c6a7138ce merge)
- PR #1725: base develop, head w201-0428-201-statever, ls-remote refs/pull/1725/head = a84a3ebc5

## What PR #1725 changed vs develop (numstat, before and after relocation)

Before relocation (e6907e591):
- 32 0 internal/application/shared_backends.go (pre-existing product logic)
- 1 1 internal/application/shared_backends_state.go (pre-existing product logic)
- 108 0 internal/application/shared_backends_state_version_test.go (PR-new file + regression test)
- catalog had a 7-line addition for source.internal.application.shared.backends.state.version.test.go (the uncataloged-source trigger)

After relocation (a84a3ebc5):
- 32 0 internal/application/shared_backends.go (unchanged)
- 1 1 internal/application/shared_backends_state.go (unchanged)
- 100 0 internal/application/shared_backends_test.go (relocated regression test appended to the base-cataloged sibling; imports: added errors + strconv; path/filepath + os already present; test-names unchanged)
- internal/application/shared_backends_state_version_test.go DELETED
- catalog diff vs develop == LEER (byte-identical; 218 components, release v0.4.27) — the new-file catalog entry removed, catalog reset to origin/develop

## Why this resolves the #1753/#1765/#1725 class at the source

- Base-precedence is test-enforced (Trusted Plan reads the catalog from the trusted base, not PR head). The PR-new file internal/application/shared_backends_state_version_test.go had no base-catalog runtime-gate owner, so the fail-loud guardian blocked the PR.
- Instead of adding a base catalog row for the new file, the owner-route folds the 108-line regression test into the already base-cataloged sibling internal/application/shared_backends_test.go and deletes the new file. No uncataloged source remains; the catalog is byte-identical to develop. This makes the base-ingress need (#1790) disappear for #1725 without any catalog change.
- #1725's product logic (shared_backends.go, shared_backends_state.go) is unchanged by this relocation; the four relocated tests keep their original names.

## Local verification (post-relocation, pre-push)

- catalog vs develop: git diff origin/develop -- scripts/pr-gate-coverage.json == LEER (byte-identical)
- go vet ./internal/application/: OK (exit 0)
- relocated tests pass (named run form, per TEST RUNNER RULE):
  go test ./internal/application/ -count=1 -run 'TestSharedBackendStateVersionMismatchNamesVersions|TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption|TestSharedBackendStateLoadReportsVersionReason|TestSharedBackendStateCorrectVersionStillLoads' -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -> ok (exit 0)
- go vet clean on the whole package too.
- Note: the package has 3 pre-existing unrelated failures (TestSharedBackendResolvedConsumerConvergencePreservesDataAndCredentials, TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle, shared_backend_dependency_test.go) in test files I did NOT touch; they fail on the develop baseline too. They are provider-registry/backup-path and unrelated to this relocation.

## EXACT hosted — CI run 45088370048 @ a84a3ebc5

- FULL SUCCESS, zero failures (run conclusion = success).
- Key gates:
  - PR · Trusted Plan: SUCCESS (no uncataloged source — the fail-loud guardian now admits the relocated test; catalog byte-identical to develop) — exactly the mission requirement
  - PR · Selected Runtime (native Podman Quadlet data-capabilities): SUCCESS (full native lifecycle gate passes with the test relocated into the base-cataloged sibling)
  - PR · PR Selected Checks: SUCCESS
  - PR · Exact Candidate, Runner Interface, Native gate plan, Focused Python, Demo Pin, Validation · source-contracts, Source format: SUCCESS
- Skipped (not run by this PR): validate, Workstation onboarding, Targeted HA docker/podman, Release Source Preflight, Selected Core-less, Public Contracts, Native ${{ matrix.id }}, Native Keycloak/Core, Main release source/checks/Go, Go unit shards, Exact full Pre-Release, Draft source/routing/Go, Consumer Pins, Candidate-added checks (advisory).
- No failures.

## Melden

- PR: #1725 (base develop, head w201-0428-201-statever, OPEN, not draft)
- head: a84a3ebc5df09cbd72523543636459b9b22376df
- CI run: 45088370048 (FULL SUCCESS, Trusted Plan GREEN, native podman runtime GREEN)
- catalog diff vs develop: LEER (byte-identical), release v0.4.27
- new-file source deleted; only base-owned shared_backends_test.go touched by the relocation

## END

END_DONE w27-pr1627-0428-061-pull: 0428-201/#1725 reloc DONE. branch w201-0428-201-statever (base develop) head a84a3ebc5, ls-remote refs/pull/1725/head witness = a84a3ebc5. Relocated the 108-line regression test (4 TestSharedBackendState* functions + helper sharedBackendStateVersionString) from internal/application/shared_backends_state_version_test.go INTO the already base-cataloged sibling internal/application/shared_backends_test.go (package application, merged imports: added errors+strconv; test-names unchanged), then git rm the now-empty new file. Catalog reset to origin/develop -> BYTE-IDENTICAL (diff LEER, 218 components, release v0.4.27) — no new-file catalog entry, base-ingress need for #1725 disappears. additive hop onto develop c6a7138ce via git merge --no-ff (KEIN force/rebase/amend); go vet clean; relocated tests pass (named run form). PR #1725 OPEN/not draft, base develop. CI run 45088370048 @ a84a3ebc5 = FULL SUCCESS, zero failures: Trusted Plan GREEN (no uncataloged source), native Podman Selected Runtime GREEN, PR Selected Checks GREEN, runner interface/native gate plan/focused python/exact candidate/demo pin/source-contracts/sourcformat green. Product logic unchanged; the 3 unrelated pre-existing failures (provider-registry/backup) are in files I did not touch. No merge. Evidence on origin/main. cleanliness: catalog-only + test relocate, docker ps -a clean (no containers started locally; local pid $$).
