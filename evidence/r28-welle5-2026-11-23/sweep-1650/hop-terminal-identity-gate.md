# #1650 hop terminal + identity-gate classification

**Card:** 0428-078 (lane `w078-pr1650-0428-078-reloc`)
**PR:** #1650 `fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in`
**Date:** 2026-11-23
**Author:** w078 worker

## Hop onto current develop

**Candidate SHA:** `cf43c6e89aae8a8f1c489f9aa074c22f70ef4682`
**Parents:** `61fd56204` (merge) — which is `22a76d68` (PR #1650 head) + `f3d847874` (current develop tip)

- `git merge-base --is-ancestor f3d847874 HEAD` → YES (additive, current develop tip)
- `git merge-base --is-ancestor 22a76d68 HEAD` → YES (carries PR #1650 content)
- Pushed to backing branch `lane-0428-078-perses-identity-on-resolver` (was `22a76d68`, now `cf43c6e89`)
- ls-remote witness: `cf43c6e89... refs/pull/1650/head`

### NET diff vs develop f3d847874 = only 1650's own identity-witness paths

```
internal/identityprovider/keycloak_files.go
internal/identityprovider/keycloak_realization.go
internal/metrics/perses_dashboards_test.go
internal/metrics/realization.go
```

- `app_status_result_test.go` byte-identical to develop (identity-field resolution took develop's version)
- `scripts/pr-gate-coverage.json` byte-equal with develop (0 changed lines)
- `.github/**` untouched (not in NET diff)

### Resolution of the one conflict

The additive `--no-ff` merge onto `f3d847874` produced ONE conflict in
`cmd/baha/app_status_result.go`: #1650 added `IdentityDashboardEligible`; the
0428-062 app_status rework (already in develop) replaced it with the `Versions`
dimension. Resolution = take develop's version (the identity field is superseded
by the Versions dimension, wired via `internal/capability/perses_selection`
`TestEligibleForIdentityDashboardEligibleWithGlobalWitness`). The companion
`app_status_result_test.go` was taken to develop's version (it no longer asserts
the removed field). This is a supersession resolution, not a scope change: 1650's
goal (derive identity-keycloak dashboard availability only from real evidence) is
already live in develop via the perses_selection gate.

### Build / vet / tests on cf43c6e89

- `go build ./...` → 0
- `go vet ./cmd/baha/ ./internal/metrics/ ./internal/identityprovider/` → 0
- `go test ./internal/metrics/` (perses_dashboards + identity) → ok
- `go test ./cmd/baha/` (app_status + identity gate + perses) → ok (7.26s)
- CI `Validation · identity-provider-package-tests` → SUCCESS (code-level proof)

## CI run 45195781651 — terminal FAILURE, classification (b) environmental

**Run ID:** 45195781651
**Head:** cf43c6e89
**BASE_SHA (trusted-plan):** `f3d84787462f324a6311e2e95928441c64a09296` (current develop tip) — trusted-plan SUCCESS
**Job id for failing gate:** 137766841830
**Gate log:** `/tmp/identity1650.log` (313964 bytes, job logs API)

### Job matrix (run 45195781651)

| Job | Conclusion |
| --- | --- |
| PR · Trusted Plan | success (BASE_SHA == f3d847874) |
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

### Identity gate failure evidence (verbatim, from job log 137766841830)

```
Managed Identity             PASS
OIDC Discovery               PASS
demo-identity                FAIL
RESULT                       FAIL
```

Root cause lines (job log, timestamps 2026-11-23T14:39:03–14:42:06):

```
14:39:00  confirmations_required: 2
14:39:03  Error: record deployment before mutation: candidate submission
          requires an explicit operator/automation consent
          (--confirm-candidate); refusing to record deployment state
14:39:03  Re-run with --confirm-candidate
          35625563bdaa377a9c3e3281a8bef9060596d10d62d45cb82ed19cc929c5db61
          to acknowledge this exact submission.
14:41:47  identity workload binding verification failed
14:42:06  demo-identity                FAIL
14:42:06  RESULT                       FAIL
14:43:29  [ci-operator-testonly] decision=managed-local-gate
          command="up --confirm-candidate 35625563..."
          target="atomic-docker-identity" runtime="docker" access="local"
```

The gate execs into `demo-app` to verify `OIDC_ISSUER` / `OIDC_CLIENT_ID` /
`SERVICE_BINDING_ROOT/identity/*` files, but the managed-local-gate `up` step
refuses to record deployment state without an explicit per-submission
`--confirm-candidate <hash>` that a fresh CI branch run cannot auto-provide. The
`Managed Identity` and `OIDC Discovery` checks both PASS; only the `demo-identity`
workload-binding confirmation fails on the consent wall.

### Classification: (b) environmental, not (a) code fix, not (c) flake

- **Not (a):** My NET diff is 4 additive identity-witness files.
  `keycloak_realization.go` adds only a public `RegisterKeycloakMetricsSignalsAt`
  wrapper around the unchanged `registerKeycloakSignals()`. The code-level gate
  `Validation · identity-provider-package-tests` PASSES. The runtime failure is in
  the demo workload confirmation, which my code cannot affect.
- **Not (c):** The gate ran to completion (exit 41), deterministic consent-wall
  failure — not a crash, timeout, or transient.
- **Is (b):** Same pattern as 1623-coreless: the gate requires prior
  deployment-state consent (`--confirm-candidate <hash>`) that the CI harness on
  a fresh branch does not carry. Environmental / harness-level.

## FOLLOW-UP: candidate advanced to 8a53ff543 (owner-lane push)

The candidate head advanced from `cf43c6e89` to `8a53ff543` via a later push by
another lane. The `cf43c6e89` → `8a53ff543` delta carries `.github/workflows`
changes (pre-release-runtime-suite.yml, pre-release.yml), script updates
(pr-check-runner.py, validate-pr-gate-coverage.py, etc.), `CHANGELOG.md`,
`docs/releases/v0.4.28.demo-ref`, and `cmd/baha/app_new_wizard.go` + its test.
These are owner-lane / CI-harness changes, NOT #1650 code — the identity-witness
content from my hop is preserved in `8a53ff543` (confirmed:
`git diff cf43c6e89..8a53ff543` shows NO change to `keycloak_realization.go`,
`keycloak_files.go`, `perses_dashboards_test.go`, or `realization.go`).

The identity-gate consent-wall failure is **unchanged** on `8a53ff543`: run
`45202734176` (BASE_SHA `7e09afc38`) shows `Managed Identity` PASS, `OIDC
Discovery` PASS, `demo-identity` FAIL on the same `--confirm-candidate` consent
wall. All other gates (Go units, docker/podman data-capabilities, docker/
observability, `Validation · identity-provider-package-tests`) PASS.

## Action

Per coord triage (2026-11-23): for classification (b) → akte-zeugnis + QUESTION
to owner. NO code fix, NO gate-drop, NO skip-hiding. The candidate `8a53ff543`
is otherwise clean (all non-identity gates pass, BASE_SHA == current develop tip
`7e09afc38`, build/vet/tests green). The identity-gate consent wall is an
owner/harness decision point.

## END

- **hop head:** `cf43c6e89aae8a8f1c489f9aa074c22f70ef4682` (parents `22a76d68` + `f3d847874`, additive `--no-ff` hop onto current develop tip)
- **candidate advanced to:** `8a53ff5437624fa8ed48cb5d79acac24fb42228f` (owner-lane push; carries `.github/workflows` + script updates + `app_new_wizard.go`; #1650 identity-witness content preserved unchanged)
- **run:** `45202734176` — terminal FAILURE, BASE_SHA `7e09afc382c21dda6cc2b741a4ef4e4ada173d80` (current develop tip, trusted-plan SUCCESS)
- **klassifikation:** identity-gate failure = **(b) environmental** (1623-coreless pattern: per-submission `--confirm-candidate` consent CI cannot auto-provide). NOT (a) code fix — `keycloak_realization.go` change is purely additive `RegisterKeycloakMetricsSignalsAt` wrapper, code gate `Validation · identity-provider-package-tests` PASSES. NOT (c) flake — deterministic exit 41.
- **candidate clean:** all non-identity gates pass (Go units, docker/podman data-capabilities, docker/observability), build/vet/tests green
- **no merge, .github untouched by #1650** (NET diff vs develop = 4 1650 identity-witness files only)
- **change line cf43c6e89 → 8a53ff543:** candidate head advanced via owner-lane push carrying `.github/workflows` (pre-release suites), script updates, `app_new_wizard.go` + test — #1650 identity-witness content unchanged
- **evidence on origin/main:** `a485e76e0` (`evidence/r28-welle5-2026-11-23/sweep-1650/hop-terminal-identity-gate.md`)
- **board on origin/main:** `c178412b` (`todos/w078-pr1650-0428-078-reloc.json`)
- **cleanliness:** `docker ps -a` = no containers (CI ran on GitHub runners, not local)

### QUESTION to coordinator (Owner)

The identity-gate failure on `cf43c6e89` is environmental (consent wall), not a
code defect. Decision needed: (1) is the `--confirm-candidate` harness a CI
configuration issue to fix at Owner level, or (2) does the candidate need to be
carried on a branch that already has deployment-state consent? NO code change
suggested — the identity provider package tests pass and the runtime failure is
in the demo workload confirmation step.
