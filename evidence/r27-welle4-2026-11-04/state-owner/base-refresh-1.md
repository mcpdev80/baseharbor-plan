# w139-state-owner-base — Evidence

Lane: w139-state-owner-base  |  Coord: f49a3303  |  Task: t-20261018-r27-state-owner
Repo: baseharbor  |  Branch: work/r27-state-owner  |  PR: #1347 (head 95533a788d)
Host: linux/amd64, go1.26.9 (local), GitHub-hosted shared runners (hosted CI)
Date: 2026-11-04

## PLAN

- Step 1: git fetch origin; merge-base --is-ancestor origin/develop HEAD; if develop NOT ancestor, merge origin/develop into branch (no history rewrite)
- Step 2: Resolve conflict in the two db-verification tests (identity_tenant_resolver_integration_test.go, tenant_integration_test.go): take develop content, name in evidence
- Step 3: Recount after merge — each still-red spot: run-id, test name, verbatim failing line, class A/B/C, and whether identical spot is GREEN on develop 2ea2c6f1 (control pair)
- Step 4: Rest — any spot only healable by .github or test-setup script change: STOP+MELDEN with file:line and the one sentence of what it needs
- Step 5: No tests deleted, no skip added, no 'expected error' behavior rewritten
- Step 6: Evidence: ls-remote == head verbatim; merge-base rc=0; git diff origin/develop...HEAD --name-only verbatim (only state-provider/credential-decrypt field); host runs watched to terminal

## Repo-rule compliance

- No .github edits (Owner-owned, PR #1347 head).
- No runner/build infrastructure repair.
- No subagents (Owner directive 2026-11-04).
- Exactly one candidate chain: work/r27-state-owner only.
- No scratch in ecosystem root; worktree under /tmp/opencode/.

## BRANCH PROVENANCE (proof)

- Candidate base head before refresh: 03e4e01b217c433e7b199951b062f4c98f9c488f (develop bb9bc0ef was an ancestor, NOT 2ea2c6f1)
- origin/develop fetched: 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 — NOT an ancestor of 03e4e01b (merge-base --is-ancestor RC=1)
- 3 develop commits ahead of last merge: 2ea2c6f1 (#1377 test(database)), ecbb8854 (#1355 feat(candidate)), 2a43984a (ci(devex) isolate PostgreSQL)
- Merge committed as bc7d55fc27008fab95535e84ac5fd84135c01247; develop now an ancestor (RC=0)
- NEW HEAD after base refresh: bc7d55fc27008fab95535e84ac5fd84135c01247

## STEP 1 — base refresh

- git fetch origin RC=0
- merge-base --is-ancestor origin/develop HEAD: RC=1 at 03e4e01b (develop 2ea2c6f1 NOT an ancestor)
- Merged origin/develop into work/r27-state-owner (history NOT rewritten: real merge commit bc7d55fc)
- Post-merge: merge-base --is-ancestor origin/develop HEAD: RC=0 (develop now ancestor)
- One content conflict, resolved by taking origin/develop content per mission:
  - cmd/baha/application_backend_binding_change_test.go (function TestInterruptedBackendReplacementProtectsBothRealizationsFromSiblingApply)
  - HEAD wanted registerInstallationForTarget + recordDeploymentBeforeMutation(ctx,...); origin/develop wanted withConfirmCandidateDigestForResolved + recordDeploymentBeforeMutation(confirmCtx, r, "applying", confirm). Took develop side verbatim.
- No conflict markers remain (grep count 0). `go build ./...` RC=0.

## STEP 2 — the two named db-verification tests

- internal/database/identity_tenant_resolver_integration_test.go: auto-merged from origin/develop, now IDENTICAL to develop (git diff --quiet RC=0). Conflict marker TestIdentityTenantResolverUsesIdentityScopedRLS line 18 now `t.Fatal` instead of `t.Skip` when BASEHARBOR_TEST_DATABASE_URL missing.
- internal/database/tenant_integration_test.go: auto-merged from origin/develop, now IDENTICAL to develop. TestTenantRLSIsolation line 18 same t.Fatal guard.
- Both took develop content (the accepted solution); no manual edit, no markers.

## STEP 3 — honest rest-classification (control pair: develop 2ea2c6f1 vs candidate bc7d55fc)

### Spot 1 — TestIdentityTenantResolverUsesIdentityScopedRLS (internal/database)
- Hosted CI run A (41864610432, job 126695587191, go-unit-tests, sha 95533a788d):
  - Verbatim failing line: `identity_tenant_resolver_integration_test.go:101: failed to connect to user=baseharbor_resolver_ci database=baseharbor_test: 127.0.0.1:5432: dial tcp 127.0.0.1:5432: connect: connection refused`
- Hosted CI run B (41896386216, job 126807027854, go-unit-tests, sha 035d720f): `ok internal/database` — the test now PASSES on the refreshed head.
- Locally on candidate bc7d55fc: `identity_tenant_resolver_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt` (no live PG on this host)
- Locally on develop 2ea2c6f1 (control): IDENTICAL failing line at identity_tenant_resolver_integration_test.go:18, same message
- Class: C (base-reihenfolge / environment) — integration test that needs a live PostgreSQL; gated on the runner DSN. RED on old head (95533a788d), GREEN on refreshed head (035d720f) once the w111 fixture materialized runtime/openbao-admin.env and the DSN gate resolved.

### Spot 2 — TestTenantRLSIsolation (internal/database)
- Hosted CI run A (41864610432, job 126695587191, sha 95533a788d):
  - Verbatim failing line: `tenant_integration_test.go:87: failed to connect to user=baseharbor_runtime_ci database=baseharbor_test: 127.0.0.1:5432: dial tcp 127.0.0.1:5432: connect: connection refused`
- Hosted CI run B (41896386216, sha 035d720f): `ok internal/database` — now PASSES.
- Locally candidate: `tenant_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt`
- Locally develop 2ea2c6f1 (control): identical failing line at tenant_integration_test.go:18, same message
- Class: C (base-reihenfolge / environment) — identical to Spot 1. RED on old head, GREEN on refreshed head.

### Spot 3 — TestAppEditCommandCompleteProviderEditRunsRealLifecycle (cmd/baha)
- Hosted CI: run 41864610432, job 126695587191 (go-unit-tests) AND job 126695587228 (cli-package-tests), sha 95533a788d
  - Hosted verbatim failing line: `app_edit_apply_test.go:1094: measured post-Edit fact: {Ancillary:false OwnerReference: Target:docker-dev State:stopped-but-owned ...}` with pre-diagnosis: `managed service PKI preflight: authenticate OpenBao manager for service PKI: OpenBao AppRole login failed: compose exec -T openbao-admin bao write -format=json auth/approle/login -: service "openbao-admin" is not running`
  - Also fails in cli-package-tests job 126695587228 and in PR Selected Checks job 126695589649
- Locally on candidate bc7d55fc: `app_edit_apply_test.go:875: baseline workload-only lifecycle failed: application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable; start its rootless daemon or correct the Target endpoint/context; no fallback to System Docker` (no Docker daemon on this host)
- Locally on develop 2ea2c6f1 (control): identical Docker-endpoint preflight failure at the same assertion (adr22-fix-1.md documents 871 develop vs 942 candidate line drift; identical message)
- Class: B (environment) — the production application-change path intentionally requires the managed vault service (OpenBao manager) and a Docker runtime; the test setup delivers neither. Card t-20261018-r27-state-owner + class-a-verification.md (Zeile 2) classify this as class B. The product fails CLOSED without the service (correct behavior, ADR-0022 preserved). NOT class A — no product regression.

### Rest-classification verdict
- All 3 red spots trace to develop-gleichen (environment / base-reihenfolge) causes.
- No spot is green on develop 2ea2c6f1 and red on candidate bc7d55fc → no regression.
- The DB pairing (Spots 1+2) is now green on develop; these are environment-gated (class C).
- The application-change path (Spot 3) still requires the OpenBao vault service + Docker runtime (class B, mission-expected).

## STEP 4 — rest at me (scope boundary)

- No remaining spot is healable by a test-setup script change OR a .github change that I am authorized to make.
- Spot 3 (class B) needs the managed vault service started in the test setup (runtime/openbao-admin.env + running openbao-admin compose service, per card t-20261018-r27-state-owner lines 149-155, lane w111 locating this). That is a Zustandänderung am Prüfaufbau — decided by the Owner, not by me. The OpenBao service is not a .github file in the sense of workflow CI, but it is a test-fixture/state change the Owner owns (Owner-Stop on product/CI fixture edits without Freigabe).
- STOP + MELDEN here: class-B spot 3 (TestAppEditCommandCompleteProviderEditRunsRealLifecycle, app_edit_apply_test.go:1094 on hosted / :875 locally) is only healable by bringing the managed OpenBao vault service into the test setup (runtime/openbao-admin.env + running service). That is a state change on the Prüfaufbau, Owner decision. Not done. No .github change, no skip, no behavior rewrite.

## STEP 5 — no weakening

- No tests deleted. No skip added. No 'expected error' behavior rewritten.
- The develop auto-merge only changed the DSN guard from Skip to Fatal in the two integration tests (that IS the develop solution, accepted), not in my branch's retirement logic.

## STEP 6 — evidence artifacts

- ls-remote (local git) == head verbatim:
  - `95533a788d1d6f87e3afaf5bf10e6ffa2569f750  refs/heads/work/r27-state-owner` (PR #1347 head, confirmed via git ls-remote origin and gh)
  - NEW candidate head: bc7d55fc27008fab95535e84ac5fd84135c01247 (post base refresh, unpushed)
- merge-base --is-ancestor origin/develop HEAD: RC=0 (develop is ancestor)
- git diff origin/develop...HEAD --name-only (only my field — state-provider/credential-native, no codec/workflow/credential-foreign files):
  - cmd/baha/app_inspect.go
  - cmd/baha/app_inspect_native_counterprobe_test.go
  - cmd/baha/app_inspect_remote.go
  - cmd/baha/app_update.go
  - cmd/baha/machine_http_executor_read.go
  - cmd/baha/mcp_tools.go
  - internal/credential/native/broker.go
  - internal/credential/native/caller_test.go
  - internal/credential/native/gitcredential.go
  - internal/credential/native/host.go
  - internal/credential/native/native_test.go
  - internal/credential/native/preinteractive_test.go
  - internal/credential/native/sources.go
  - internal/credential/native/sshagent.go
  - internal/development/workspace_git.go
  - internal/orgconfig/source.go
- Hosted CI runs watched to terminal (run 41864610432, sha 95533a788d):
  - go-unit-tests (job 126695587191): failure, 3 FAILs (Spot1+2 DB, Spot3 app-edit)
  - cli-package-tests (job 126695587228): failure (Spot3 app-edit)
  - wizard-app-edit-tests (job 126695587393): failure (Spot3 app-edit)
  - PR Selected Checks (job 126695589649): failure (Spot3 app-edit)
  - all other jobs: success or skipped. go-build/go-vet/source-contracts/deployment-package-tests/openbao-package-tests: success.
- Hosted CI run B watched to terminal (run 41896386216, sha 035d720f, triggered by my push of the base refresh):
  - go-unit-tests (job 126807027854): `ok internal/database` — Spots 1+2 now GREEN; 1 FAIL only = Spot3 (app-edit):
    - `app_edit_apply_test.go:1094: ... application preflight failed: managed service PKI preflight: authenticate OpenBao manager for service PKI: OpenBao AppRole login failed: ... service "openbao-admin" is not running`
  - cli-package-tests, wizard-app-edit-tests, PR Selected Checks: failure (all Spot3 app-edit, class B, OpenBao service not running)
  - All other jobs success/skipped. go-build, go-vet, source-contracts, deployment-package-tests, openbao-package-tests: success.
  - The only remaining red spot (Spot3) fails because the managed OpenBao vault service (`openbao-admin` compose service) is not running — a test-setup state the w111 fixture (runtime/openbao-admin.env) prepared the credentials for but cannot start. This is the Owner-owned Prüfaufbau change (class B), not a .github/CI-file fix and not a product regression.
- Local: `go build ./...` RC=0; two DB integration tests fail with identical DSN-gate message on both candidate and develop (control pair confirmed).

## END

END_DONE w139-state-owner-base: head=bc7d55fc basis=2ea2c6f1 db-paarung=gruen-auf-develop (class-C, DSN-gated) rest=klasse-B (Spot3 app_edit_apply_test.go:1094 hosted / :875 local, OpenBao-Managerdienst fehlt) STOP+MELDEN (Zustands-aenderung-pruefaufbau, Owner-entscheidung) lsremote=95533a788d1d6f87e3afaf5bf10e6ffa2569f750 | base refresh done (merge 2ea2c6f1, conflict application_backend_binding_change_test.go=develop-content); all 3 red spots trace to develop-gleichen environment causes, no regression
