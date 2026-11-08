# CODEX-REVIEW 0427-133 r2 — PR #1460

## PLAN

1. Resolve current PR #1460 head, base, develop head, compare, and exact-head hosted checks from GitHub.
2. Review the Keycloak-core-issuer fix and its fail-closed tests against the r1 finding.
3. Check isolation/status scope and verify whether the card's required native Docker and Podman evidence ran.
4. Record verdict, correction recipe, and stop criteria; publish this act to verified baseharbor-plan origin/main.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1460 head:** `ab486677f7ff2376b47f9fd8298acfb73ecc2b41`  
**PR state:** open, not draft; GitHub reports `MERGEABLE` / `CLEAN` against base SHA `07ae6c3e91b081a189266ca4b162ba705d4aa78f`.

### 1. R1 authority-resolution finding: improved, with a remaining verification gap

The changed production path no longer treats a local base CA or OpenBao service-PKI issuer as the Core's management identity. In `cmd/baha/use_target.go`, `bindExplicitSelectionToConnection` loads the genuine Core installation from the selected Target's runtime state, then calls `VerifyCoreConnection` against the plain target-state root where the real Keycloak issuer is materialized. `cmd/baha/target.go:280-288` calls this boundary before persisting explicit activation; the guided target activation also uses the same helper. The code rejects missing installation/issuer, mismatch with `state.IdentityIssuer`, and expired material before selection is persisted.

The new tests in `cmd/baha/use_target_keycloak_issuer_test.go` cover a matching Keycloak issuer, a port-derived identity mismatch, and missing issuer material. The exact-head hosted `PR · Validation · go-unit-tests` job runs the `cmd/baha` package and passed. These tests exercise the production binding helper, although they do not execute a full native Core bootstrap/activation command.

A remaining gap is that `VerifyCoreConnection` does not cryptographically bind the observed issuer URL to the Keycloak server certificate. At `cmd/baha/verify_core_connection.go:126-152`, it reads the port from `runtime.env`, sets the issuer to the constant hostname `identity.localhost` plus that port, and compares that constructed string to `state.IdentityIssuer`. It reads the server certificate only for serial and expiry. The called `serviceaccess.ExistingTLSMaterial` validation (`internal/serviceaccess/pki.go:540-556`) checks that the CA parses and is marked as a CA, the server certificate is unexpired, and its private key matches; it does not verify the certificate chain or `identity.localhost` SAN. The negative test changes the configured port, not the certificate identity or issuing CA. A wrong-host or untrusted certificate placed at the expected Keycloak material path is therefore not distinguished by this verifier.

**Correction recipe:** in `cmd/baha/verify_core_connection.go`, verify the Keycloak server certificate against the Keycloak CA from the same protected material using `x509.Verify` with `DNSName: identity.localhost` and server-auth usage, and bind the issuer URL to that verified certificate plus the configured public port. Keep missing, foreign, expired, not-yet-valid, and mismatched material fail-closed. Extend `cmd/baha/use_target_keycloak_issuer_test.go` with wrong-SAN, untrusted-CA, and not-yet-valid certificate cases, alongside the valid positive case. The existing `go-unit-tests` job is the required CI group for these tests on `pull_request`.

### 2. Isolation and status scope

The r1 evidence records the `BASEHARBOR_TARGET` isolated-target reproduction, no shared-plane mutation on the failed activation path, and the status/selection isolation claim. The r2 write-set is six `cmd/baha` files; it does not edit shared-plan, status-selection, or workflow code. The changed binding helper is read-only and activation persists the selected target only after the helper succeeds. I found no new shared-plane write in this r2 diff. This review treats the r1 isolation work as prior evidence, not as a newly executed native proof.

### 3. Required native acceptance evidence is missing

The task card `tasks/t-20261108-bughunt-0427-greenfield-isolation.md:45-53` requires an isolated `BASEHARBOR_TARGET` second-target flow through bootstrap, Core self-install, and status, with no shared-plane mutation, **proven by native Docker and Podman cells in CI**. The exact-head run `42462286642` is terminal success on `ab486677f7ff2376b47f9fd8298acfb73ecc2b41`; `PR Selected Checks` passed from GitHub Actions app `15368`, and the `go-unit-tests` job passed. But `PR · Native Keycloak/Core · <runtime>`, `Targeted HA · docker`, and `Targeted HA · podman` were all skipped. Round-2 evidence also explicitly says no Docker/Podman cell ran. Passing unit checks and the r1 diagnostic do not satisfy the card's native Docker-and-Podman acceptance clause.

**Correction recipe:** keep workflow files unchanged in this review. The owner-scope selector for `PR · Native Keycloak/Core · <runtime>` is `.github/workflows/ci.yml:943-946`; line 946 requires `needs.pr_plan.outputs.owner_node_required == 'true'`. Report to the Owner that this task's relevant target/use/activate paths need to select the required native Docker and Podman cells, or identify an existing CI group that already does so. Then run the card's isolated-target bootstrap, activation, and status checks in both native cells, recording that shared-plane state is unchanged and `BASEHARBOR_TARGET` remains honored. A local or VM-only run is not durable acceptance evidence.

### 4. Base freshness

The live `develop` ref is `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`, while the PR base snapshot and the successful run's tested base are `07ae6c3e91b081a189266ca4b162ba705d4aa78f`. Compare against current develop reports `ahead_by=1`, `behind_by=10`, `status=diverged`. No files under `cmd/baha/use_target`, `target`, `coreinstallation`, `keycloak`, or `deployment` changed in those ten intervening develop commits, but a current-base integration is still required before acceptance. Rebase/update the candidate to current develop; the resulting SHA needs a fresh run and review.

## Stop criterion

Do not approve until the Keycloak certificate chain and hostname are verified fail-closed, the card's isolated-target acceptance has actually run in native Docker and Podman CI cells, and the rebased final candidate has terminal green `go-unit-tests` and `PR Selected Checks` from app `15368`. Any changed candidate SHA requires fresh exact-head gates and review.

## Evidence witnesses

- PR #1460 is open, not draft, head `ab486677f7ff2376b47f9fd8298acfb73ecc2b41`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1460/head` returned:

```text
d30de3a4a176e073c8c1a9a0fc0b0ef06202b064\trefs/heads/develop
ab486677f7ff2376b47f9fd8298acfb73ecc2b41\trefs/pull/1460/head
```

- `gh run view 42462286642` confirms completed success on the exact candidate SHA. `PR Selected Checks` belongs to app `15368` and succeeded. Native Keycloak/Core and targeted Docker/Podman jobs were skipped.
- Planning repository remote is `https://github.com/mcpdev80/baseharbor-plan.git`; pre-publication `git ls-remote origin refs/heads/main` returned `96b54ce29660797351179ae6db86748328c1fb85`.
- No product files or workflows were modified and no tests or workflow runs were started by this review.

## END

END_BLOCKED 0427-133-review-r2 — KORREKTUR; Keycloak identity is assembled from runtime.env without certificate-chain/DNS verification; required native Docker and Podman cells were skipped; the PR base is ten commits behind current develop. Exact-head unit tests and `PR Selected Checks` passed but do not satisfy the remaining acceptance criteria.
