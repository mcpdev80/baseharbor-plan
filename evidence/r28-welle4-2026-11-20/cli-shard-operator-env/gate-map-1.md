# Coordinator evidence — PR-Gate collapse after develop `40cb28c758b0` (gate-map 1)

Written by the coordinator (no product change, no PR). Purpose: one durable, reproducible map of which hosted
checks fail, so no lane and no reviewer has to re-derive it and nobody attributes it to a candidate diff.

## How it was measured

1. `gh api repos/mcpdev80/baseharbor/commits/26755fc1edfb/check-runs?per_page=100` — all checks at the head of
   PR #1723 (card 0428-199, own diff = 4 files in `cmd/baha/`).
2. `gh api repos/mcpdev80/baseharbor/actions/runs/44788134959/jobs` and, per failed job,
   `gh api repos/mcpdev80/baseharbor/actions/jobs/<id>/logs`, grepped for
   `([a-z0-9_]+_test\.go):(\d+): ` plus the strings `authenticated BaseHarbor operator` / `operator OIDC`.
3. Cross-checked against `gh api repos/mcpdev80/baseharbor/commits/40cb28c758b0/check-runs` (develop push state)
   and the earlier PR runs `44774783515` (#1718), `44778040176` (#1714), `44731562217` (#1645).

## Result

- Ancestry is clean: `git ls-remote` shows `refs/heads/lane-0428-199-workloadport` == `refs/pull/1723/head` ==
  `26755fc1edfb`, whose only parent is `40cb28c758b0` (`refs/heads/develop`). So the failures below are not base
  drift.
- Failing checks at that head: `PR Selected Checks`, `PR · Go unit · cli-0..cli-3`, `PR · Go unit · packages`,
  `PR · Selected Runtime (atomic/docker/guided, docker, guided)` and
  `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)`.
- The message is identical everywhere: `Managed-environment machine operations require an authenticated
  BaseHarbor operator` (plus `operator OIDC configuration` in `app_secrets_shared_runtime_test.go:44`).
- Packages reported in the logs: `cmd/baha` and `internal/logs`.

## Distinct failure sites (job, file:line, occurrences in the log)

| shard | site | x |
| --- | --- | --- |
| cli-0 | `perses_lifecycle_transport_test.go:87` | 9 |
| cli-0 | `application_restore_external_identity_test.go:87` | 8 |
| cli-1 | `application_restore_registered_receiver_test.go:98` | 8 |
| cli-2 | `bugs_858_860_regression_test.go:305` | 6 |
| cli-2 | `app_restore_fresh_identity_test.go:186` | 6 |
| cli-0 | `application_restore_external_receiver_test.go:40` | 5 |
| cli-2 | `bugs_858_860_regression_test.go:101` | 3 |
| cli-3 | `perses_lifecycle_transport_test.go:168` | 3 |
| cli-0 | `application_destroy_authorization_test.go:103` | 2 |
| cli-0 | `core_installation_test.go:75` | 2 |
| cli-0 | `perses_lifecycle_transport_test.go:133` | 2 |
| cli-1 | `application_provider_authorization_test.go:278` | 2 |
| cli-2 | `app_application_backend_runtime_test.go:55` | 2 |
| cli-3 | `trust_status_regression_test.go:36` | 2 |

Same class in the packages shard: `app_workspace_bootstrap_test.go:87`,
`app_workspace_source_model_test.go:480`, `app_workspace_wizard_test.go:71` (all `cmd/baha`), and
`loki_test.go:522/:586/:633` in `internal/logs` (carried separately as card 0428-202).

## Independent witnesses that this is not a candidate defect

- PR #1718 (card 0428-178, content **APPROVED**, one test file): `ce5aa9633630` fails `cli-0..3` +
  `PR Selected Checks`; the same content passed `PR · Go unit · cli-2` executed/success at base `f5ce95afce1c`
  (run `44759243414`).
- PR #1714 (card 0428-183): `5159192dadee` fails `cli-0..3` **and** `packages`; `internal/metrics` is `ok` in the
  same log.
- PR #1645 (card 0428-091 family): run `44731562217` fails `packages` on `internal/identityprovider` (field of
  #1650, owned by the owner).
- PR #1615 (owned by the owner): head `a0f57fef91c9` shows failures in `PR · Selected Runtime` and
  `PR · Selected Core-less` cells as well.
- Lane 199 states verbatim in its transcript: "this is the pre-existing 0428-198 gate defect, NOT caused by my
  change".

## Blind spot that let this reach the field

`gh api "repos/mcpdev80/baseharbor/actions/runs?event=push&per_page=6"` returns only
`Runtime · Docker Core · develop` and `Runtime · Podman Core · develop` (runs `44769994971`, `44769994909`, both
success). The `Go unit` shards exist on the pull_request path only, so a develop-side breakage is invisible until
the next PR hops onto it and pays for it. Closing that gap needs a `.github/**` change and is therefore reported
here rather than implemented (owner scope, AGENTS 3.8).

## Consequence for the window

Until either a test-side operator identity exists again or the owner decides the environment/rollback question,
**no** PR in v0.4.28 can show a green prescribed check at an exact head. The coordinator therefore (a) orders the
lanes to stop re-running the matrix, (b) keeps such cards in `wait` with the dependency named, and (c) does not
order CODEX-REVIEW on candidates whose mandatory gate cannot pass.
