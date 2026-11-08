# CODEX-REVIEW — 0427-133 R3 / PR #1460 candidate

## PLAN

1. Refresh the exact remote candidate, live PR #1460 head, and develop head.
2. Inspect the verifier and each negative test, confirming the tests call the production verifier and isolate the claimed failure mode.
3. Verify candidate ancestry, commit list, and write-set against its stated base.
4. Evaluate current hosted native-gate selection against task 0427-133 and the 0427-137 Owner/CI-owner rule, including the merged #1464 result.
5. Publish the SHA-specific verdict and actionable correction recipe to baseharbor-plan.

## Verdict

**ROLLE: REVIEW**
**URTEIL: KORREKTUR (REQUEST-CHANGES)**
**Requested candidate:** `work/0427-133-r3-ca-issuer` at `80895b67123c80d2b902e3f91a90d2d9e38547bd`

The production verifier implements the intended chain and DNS binding. The negative tests reach the production verifier, but the three fixtures do not isolate the named negative conditions; the untrusted-CA fixture in particular installs its allegedly untrusted CA as the verifier's trust root. The required native Docker/Podman greenfield acceptance is also still missing. The current live PR and develop refs have advanced beyond the SHAs stated in the request.

### 1. Production verifier and negative tests

`VerifyCoreConnection` in `cmd/baha/verify_core_connection.go` compares the observed Keycloak identity to the genuine installation identity, checks certificate expiry, and calls `verifyKeycloakServerCertificateChain`. That function reads the Keycloak CA and server leaf from the protected material and calls standard-library `x509.Verify` with that CA as the root, server-auth usage, and DNS name `identity.localhost` (`verify_core_connection.go:137-175`). The production caller `bindExplicitSelectionToConnection` invokes `VerifyCoreConnection` (`cmd/baha/use_target.go:113`). The three new tests call `bindExplicitSelectionToConnection`, so they do reach the production boundary rather than a stand-alone helper.

The fixture setup weakens the negative evidence:

- `TestBindExplicitSelectionFailsClosedOnWrongSAN` at `cmd/baha/use_target_keycloak_issuer_test.go:308-318` uses `selfSignedServerLeafForHost`. That helper explicitly creates a leaf under an unrelated self-signed CA (`use_target_keycloak_issuer_test.go:132-181`), while the original CA remains in the target material. The test therefore fails chain validation even if the DNS-name check is removed; it does not isolate wrong-SAN rejection.
- `TestBindExplicitSelectionFailsClosedOnUntrustedCA` at `use_target_keycloak_issuer_test.go:328-380` writes `otherCA` to `ca.pem` and signs the replacement, valid-host leaf with that same `otherCA`. Since `verifyKeycloakServerCertificateChain` loads `ca.pem` as its root, this leaf is trusted by the root the verifier is given. The fixture does not test an untrusted chain and, absent a different earlier rejection, should make the test's expected error assertion fail.
- `TestBindExplicitSelectionFailsClosedOnNotYetValid` at `use_target_keycloak_issuer_test.go:385-438` sets the CA `NotBefore` to `future - 24h` while `future` is 48 hours ahead. Thus the CA itself is also not yet valid; chain rejection does not prove that a future `NotBefore` on the leaf is enforced.

**Correction recipe:** keep the production verifier. Make each negative fixture independently valid except for its named condition. For wrong-SAN, issue an otherwise valid leaf with a wrong DNS SAN from the same currently valid CA retained at `ca.pem`. For untrusted-CA, leave the original valid CA at `ca.pem` and sign an otherwise valid `identity.localhost` server leaf with a different CA. For not-yet-valid, use a currently valid CA that signs a leaf whose only invalid property is a future `NotBefore`. Each test must continue to call `bindExplicitSelectionToConnection` and assert fail-closed. Keep a positive same-CA, correct-SAN, current-validity control.

**Stop criterion:** all three counterexamples fail through the production verifier for their unique claimed reason, the positive fixture passes, and the exact candidate's `go-unit-tests` run passes. A test that fails because of an unrelated chain or CA-time defect does not satisfy the named regression.

### 2. Candidate ancestry and write-set

The live branch `work/0427-133-r3-ca-issuer` is exactly `80895b67123c80d2b902e3f91a90d2d9e38547bd`. Its direct parent is `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`, the develop head named in the request at candidate creation. `git log --oneline d30de3a4..80895b671` lists only the single R3 commit; no extra commit is carried on that branch. Its diff against that stated base contains six files, all under `cmd/baha`; it contains no `.github/**` paths.

The live state has since moved: develop is now `cd494610c9327d122720e90851ce1f818e5d073e`, and PR #1460 is open at `b09db84a16cdec3e64a736a1e29c98d41d2a1ef6` on branch `work/r27-greenfield-isolation-r2`. The requested R3 candidate is not an ancestor of that PR head, and the live PR head is not an ancestor of R3. The mission's statement that the PR still points at `ab486677` is stale. The R3 branch is based on the former `d30de3a4` head, not the current `cd494610` head. Therefore the proposed mechanical fast-forward cannot be assumed from the current remote state. No PR update was performed.

### 3. Native Docker/Podman cells: Owner-owned routing gap, still no acceptance

Task `t-20261108-bughunt-0427-greenfield-isolation` explicitly requires the isolated `BASEHARBOR_TARGET` bootstrap, Core self-install, and status flow to be proven by native Docker **and** Podman CI cells. The 0427-137 task assigns `.github/**` selector changes to the CI owner and says a skipped, missing, or failed required acceptance is not PASS.

The owner boundary is legitimate: this review must not edit the workflow or trigger a rerun. It does not waive the card's native proof. PR #1464 is now merged as `cd494610c9327d122720e90851ce1f818e5d073e`; its exact run `42474092741` passed the destroy-retry Docker and Podman cells and `PR Selected Checks`, but `PR · Native Keycloak/Core` was skipped. On the current PR #1460 R2 head `b09db84a16cdec3e64a736a1e29c98d41d2a1ef6`, run `42474997328` is still in progress: `PR · Native Keycloak/Core` is skipped, both `PR · Native destroy retry` cells and `PR · Validation · go-unit-tests` remain in progress, and there is no terminal `PR Selected Checks` result at review time. The exact requested R3 candidate has no hosted run.

The current develop workflow gates `PR · Native Keycloak/Core` at `.github/workflows/ci.yml:1044` on `needs.pr_plan.outputs.owner_node_required == 'true'`. The observed skip after #1464 shows that the greenfield/use/activate source paths are not selecting this required native group. This is a CI-owner finding, not a legitimate acceptance substitute and not evidence of green checks.

**CI-owner action / recipe:** update the owner-controlled selector so the 0427-133 use/activate/Keycloak-verifier paths select both required native runtime cells, then observe the exact final PR candidate through terminal Docker and Podman acceptance and successful `PR Selected Checks`. Do not approve based on #1464's destroy-only native success or the R2 run's unit checks. This review made no workflow change and triggered no run.

### Stop criterion

Do not approve until the three negative tests isolate and pass their respective verifier conditions, the candidate is integrated onto the current PR/develop lineage without foreign scope, and the final exact PR SHA has terminal green required unit and native Docker/Podman acceptance plus `PR Selected Checks`. If selector ownership prevents the native cells from running, keep the card unaccepted and report the selector gap to the CI owner.

## Evidence witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git` returned:

```text
cd494610c9327d122720e90851ce1f818e5d073e	refs/heads/develop
80895b67123c80d2b902e3f91a90d2d9e38547bd	refs/heads/work/0427-133-r3-ca-issuer
b09db84a16cdec3e64a736a1e29c98d41d2a1ef6	refs/pull/1460/head
```

- `gh pr view 1460` reports OPEN, head `b09db84a16cdec3e64a736a1e29c98d41d2a1ef6`, branch `work/r27-greenfield-isolation-r2`, base `develop`, mergeable, state `UNSTABLE`.
- `git show 80895b671 --no-patch --pretty=raw` identifies direct parent `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`; `git log --oneline d30de3a4..80895b671` lists only `80895b671`.
- `git diff --name-status d30de3a4..80895b671` lists six `cmd/baha` files and no workflow or other repository paths.
- `gh run list --commit 80895b67123c80d2b902e3f91a90d2d9e38547bd` returned no runs.
- `gh run view 42474997328` reports an in-progress run on the different PR head `b09db84a16cdec3e64a736a1e29c98d41d2a1ef6`; its Native Keycloak/Core job is skipped, while go-unit-tests and both Native destroy retry cells are still in progress.
- `gh pr checks 1464` shows run `42474092741` with both Native destroy retry cells and `PR Selected Checks` passing; Native Keycloak/Core is skipped. PR #1464 merged as `cd494610c9327d122720e90851ce1f818e5d073e`.
- The planning repository is `/tmp/opencode/0427-133-review-plan-wt`, remote `https://github.com/mcpdev80/baseharbor-plan.git`. The verified remote was:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

- Pre-publication `git ls-remote origin refs/heads/main` returned:

```text
4c57f78fd20ec113df0673b3059b2804128079d7	refs/heads/main
```

- This was a read-only product review. No product file, PR, workflow, or candidate branch was changed; no tests, reruns, workflow dispatches, or VM/compose projects were started.

## END

END_BLOCKED 0427-133-review-r3 — KORREKTUR: production `x509.Verify` is present, but the wrong-SAN and future-validity fixtures are confounded and the alleged untrusted-CA test replaces the trust root with its signing CA. After #1464 merged, PR #1460 still skips Native Keycloak/Core; the exact R3 candidate has no hosted run and is not the current PR head.
