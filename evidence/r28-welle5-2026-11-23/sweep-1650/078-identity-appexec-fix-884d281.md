# 0428-078 identity-gate fix: admit canonical `app exec demo-app` fixture probe

**Card:** 0428-078 (lane `w078-pr1650-0428-078-reloc` / `lane-0428-078-perses-identity-on-resolver`)
**PR:** #1650 `fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in`
**Date:** 2026-11-24
**Author:** w078 worker

## Context (prior lane)

The previous lane proved the docker-identity gate failed on the `--confirm-candidate`
consent wall for the demo `up` step, then advanced. This lane re-measured the
current head and re-diagnosed the failing assertion. The gate execs into
`demo-app` with `baha app exec demo-app /bin/sh -ec '<verify OIDC bindings>'`
to confirm the managed workload's OIDC service bindings. That `app exec`
invocation fell through to the interactive OIDC operator-auth boundary because
`app.exec` is a registered (mutating-class) machine operation that the tagged
CI synthetic operator (`--tags baseharbor_ci_operator_testonly`) did not admit
on the identity/security gates. `Managed Identity` and `OIDC Discovery` PASS;
only the `demo-app` workload-binding probe hit the consent wall.

## Fix (write-set only)

Two files in my write-set; the admit is gate-scoped to the two consumer gates
and the exact canonical form, so fail-closed operator-auth stays intact
everywhere else.

- `cmd/baha/ci_integration_operator_enabled.go`:
  - admission: `!managedWorkload && (gate == "identity" || gate == "security") && ciIntegrationAppExecFixtureDemoApp(args)`
  - predicate `ciIntegrationAppExecFixtureDemoApp(args)`: admits `app exec demo-app <shell/cmd>` with a following shell/command token; rejects the empty form, a leading baha-level flag (a different component selector / `--cmd` / `--json`), and any form selecting a non-fixture component.
- `cmd/baha/ci_integration_operator_enabled_test.go`:
  - `TestCIIntegrationOperatorAdmitsFixtureAppExecOnlyOnConsumerGates` — positive admit on identity + security (docker), negative fail-closed on all other gates (observability, lifecycle, policy, connectivity, data-capabilities, guided) and on every non-canonical form.

## Hosted CI verification (exact head)

**Run id:** r7564 — databaseId `45283500012`
**Head:** `884d2818e`
**Candidate branch head on lane-origin:** `884d2818e7b1d3c03e0f87287c88b07592f8741`
**PR #1650 head on lane-origin:** `884d2818e7b1d3c03e0f87287c88b07592f8741`

- Run conclusion: **success**
- `PR · Selected Runtime (atomic/docker/identity, docker, identity) / Executed docker · identity` → **pass** (4m54s) — the gate that failed on the prior head now passes
- `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)` → pass
- `PR · Selected Runtime (atomic/docker/observability, docker, observability)` → pass
- `PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities)` → pass
- `PR · Selected Runtime (atomic/podman/observability, podman, observability)` → pass
- `PR · Validation · ci-integration-operator-seam-tests` → pass (the tagged test this fix adds, runs in Hosted CI)
- `PR · Validation · identity-provider-package-tests` → pass
- `PR · Trusted Plan` → success

## Attestation

- Remote HEAD (verified via `git ls-remote lane-origin refs/heads/lane-0428-078-perses-identity-on-resolver` and `refs/pull/1650/head`): `884d2818e7b1d3c03e0f87287c88b07592f8741`
- Merge-base vs develop `d4fa8c589e02bf6708d9e6beba7a510c1a2efc7e` = `d4fa8c589` (additive hop onto current develop; develop is an ancestor)
- My commit `884d2818e` touches ONLY the two write-set files above (verified via `git show --stat`)
- No `.github/**` edits, no merge to develop, no force-push, one branch

## Scope split note (per Owner 2026-11-04)

`.github/**` (CI workflow policy) belongs to the Owner. The identity gate ran
and passed under the current CI policy; no workflow change was needed or made.
If the identity admission had to live in the demo/acceptance fixture outside
this product write-set, this lane would have posted a QUESTION with the exact
file:line instead of reaching into another repo. The admit is in product code
(`ci_integration_operator_enabled.go`, CI-tagged testonly), inside the
operator-auth fail-closed seam.
