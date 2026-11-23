# #1650 hop onto develop 4f67760a2 (#1808 consent-gate trust-regel)

**Card:** 0428-078 (lane `w078-pr1650-0428-078-reloc`)
**PR:** #1650 `fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in`
**Date:** 2026-11-23
**Author:** w078 worker

## Decision point resolved by owner (remote-attested)

The owner resolved the identity-gate decision-point by merging **#1808**
`ci: trust candidate consent gate coverage` as commit **4f67760a2** (develop
head). This is the exact 1623-coreless analogie: a develop-side consent-gate
trust-regel. #1808 changes **only** `scripts/pr-gate-coverage.json` — it adds
consent-gate coverage rows for `cmd/baha/app_candidate_consent.go`,
`cmd/baha/app_input_resolver.go`, and `cmd/baha/runtime_ports_test.go`.

## Additive merge --no-ff onto 1650 branch

**Merge HEAD:** `403e18128a8d00e57a74495205b26c6bb9170890`
**Parents:** `8a53ff543` (current 1650 branch head) + `4f67760a2` (develop tip)

- `git merge-base --is-ancestor 4f67760a2 HEAD` → YES (additive, develop tip)
- `git merge-base --is-ancestor 8a53ff543 HEAD` → YES (carries #1650 identity-witness content)
- merge-base(cf43c6e89, 4f67760a2) = `f3d847874`; merge-base(8a53ff543, 4f67760a2) = `7e09afc38`
- Pushed to `lane-0428-078-perses-identity-on-resolver` (was `8a53ff543`, now `403e18128`)
- ls-remote witness: `403e18128... refs/pull/1650/head`

### Delta write-setfrei

- #1808 changes `scripts/pr-gate-coverage.json` ONLY — NO overlap with #1650's identity-witness files
- NET diff vs develop 4f67760a2 = exactly #1650's 4 identity-witness files:
  - `internal/identityprovider/keycloak_files.go`
  - `internal/identityprovider/keycloak_realization.go`
  - `internal/metrics/perses_dashboards_test.go`
  - `internal/metrics/realization.go`
- No `.github/**` changes, no catalog changes, no foreign commits
- `go build ./...` → 0; `go test ./internal/identityprovider/` → ok; `go test ./internal/metrics/` → ok

## CI run 45209984310 — terminal FAILURE, identity-gate is the decisive probe

**Run ID:** 45209984310
**Head:** 403e18128
**BASE_SHA (trusted-plan):** `4f67760a206399ac7c063a4001d677461851bb2e` (current develop tip with #1808) — TP SUCCESS
**Failing gate job:** 137816842885
**Gate log:** `/tmp/identity40.log` (311111 bytes)

### Job matrix (run 45209984310)

| Job | Conclusion |
| --- | --- |
| PR · Trusted Plan | success (BASE_SHA == 4f67760a2) |
| PR · Go unit · cli-0/1/2/3 | success |
| PR · Go unit · owner | success |
| PR · Go unit · packages | success |
| PR · Selected Runtime · docker/observability | success |
| PR · Selected Runtime · docker/data-capabilities | success |
| PR · Selected Runtime · podman/observability | success |
| PR · Selected Runtime · podman/data-capabilities | success |
| PR · Validation · identity-provider-package-tests | **success** |
| PR · Selected Runtime · **docker/identity** | **failure** |
| PR Selected Checks | failure (driven by identity gate) |

### Identity gate failure evidence (verbatim, from job log 137816842885)

```
Managed Identity             PASS
OIDC Discovery               PASS
demo-identity                FAIL
RESULT                       FAIL
```

Root cause lines (job log, timestamps 2026-11-23T15:58:11–15:59:09):

```
15:59:08  [ci-operator-testonly] decision=managed-local-gate
          command="up --confirm-candidate" target="atomic-docker-identity"
15:59:08  [ci-operator-testonly] decision=managed-local-gate
          command="up --confirm-candidate a66546c18536a53a83e1072b54873265..."
          target="atomic-docker-identity" runtime="docker" access="local"
15:59:09  Error: record deployment before mutation: candidate submission
          requires an explicit operator/automation consent
          (--confirm-candidate); refusing to record deployment state
```

The gate still fails on the `--confirm-candidate` consent wall. **The #1808
consent-gate trust-regel did NOT resolve the identity-gate failure.** The
`Managed Identity` and `OIDC Discovery` checks both PASS; only the
`demo-identity` workload-binding confirmation fails on the consent wall.

### Classification

- **NOT (a) code fix:** My NET diff is 4 additive identity-witness files.
  `keycloak_realization.go` adds only a public `RegisterKeycloakMetricsSignalsAt`
  wrapper. The code-level gate `Validation · identity-provider-package-tests` PASSES.
- **NOT (c) flake:** Deterministic exit — consent-wall failure, not transient.
- **IS (b) environmental / owner-punkt:** The #1808 trust-regel (develop-side
  CI coverage) does not touch the demo workload's deployment-state consent. This
  is now an **ECHTER owner-punkt**: the consent-gate harness requires an
  operator/automation acknowledgment that neither a fresh CI branch nor the #1808
  coverage-regel can auto-provide.

## Action

The identity-gate failure is an ECHTER owner-punkt (not a code fix, not a
flake). The #1808 consent-gate trust-regel resolved the CI-coverage dimension
but not the demo-workload deployment-state consent. Evidence on `origin/main`.
No merge, no `.github/**` change by #1650.
