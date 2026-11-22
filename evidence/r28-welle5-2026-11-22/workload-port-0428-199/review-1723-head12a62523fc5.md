# CODEX-REVIEW: PR #1723 exact-head review

## PLAN

1. Finish publishing and remotely verify the prior duplicate-closure evidence before its coordinator handoff.
2. Verify PR #1723 exact head/base and observe terminal run 44995050874; list failed job IDs and names.
3. Classify failures against card 0428-237 shared broker readiness versus candidate failures.
4. Review all 16 diff paths for local apply/up workload-port behavior and regression sensitivity; compare approved heads for additive develop-only changes and inspect scope.
5. Publish SHA-specific review evidence and post the coordinator verdict.

Role: CODEX-REVIEW, read-only; no merge, close, comment, tests, or subagents.

## Verdict

REQUEST CHANGES for exact head `12a62523fc5f2259220aece4cc5619dcb8f4ae4d`.

The workload-port implementation is wired through both local command routes. `cmd/baha/app_apply.go:57-61` strips the option and places its parsed map in context. `cmd/baha/runtime.go:51-56,151-188` parses both flag forms and sets that same context for `baha up`. `cmd/baha/app_workload_ports.go:53-90` validates and removes the option; `:351-360` and `:592-625` consume the request for conflict behavior and persisted selection. The app-input resolver calls this handling on the repository path at `cmd/baha/app_input_resolver.go:497,508,517`.

The regression file `cmd/baha/workload_port_local_regression_test.go:15-49` asserts both `up` parsing forms and malformed inputs; `:89-119` drives `app apply` and `up` command hooks and rejects their pre-patch unknown/extra-argument errors. These tests would fail without the parsing/command patch (the option is rejected or the new parsed field is absent). They primarily prove acceptance and routing, not that a real deployment persists the selected port; the existing workload-port unit coverage exercises the selection/persistence helpers. No tests were run in this read-only review.

### Exact-head hosted run

Run `44995050874` is terminal `completed/failure` on the exact head. Six jobs failed:

- `137125231606` — `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities`.
- `137125232518` — `PR · Selected Core-less · docker / PR selected · integration/docker/coreless-lifecycle · application`.
- `137125232793` — `PR · Selected Core-less · podman / PR selected · integration/podman/coreless-lifecycle · application`.
- `137128581738` — `PR · Selected Core-less · docker / PR selected · integration/docker/coreless-lifecycle`.
- `137128789901` — `PR · Selected Core-less · podman / PR selected · integration/podman/coreless-lifecycle`.
- `137128813911` — `PR Selected Checks`.

The Docker and Podman execution failures repeat the same candidate test assertion in `cmd/baha/env_destroy_integration_test.go:136`: `KEEP must retain the stopped deployment owner: found=true state="runtime-retired" ready=false err=<nil>`. The runtime-selected job reports `candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`. Its log says `runtime broker ready (15.3s)`; it does not show `TestApplicationCapabilityLifecycleExistingCore/secrets`, `starting secure runtime broker`, or readiness `503 not_ready`. The aggregate reports that `pr_runtime_selected` and `pr_selected_integration` did not succeed.

Therefore the failing jobs are not the shared 0428-237 broker-readiness blocker. The integration assertion is a candidate failure in the included environment-destroy changes; the runtime failure is a separate consent/gate failure in the exercised path. `Haelt die karte, nicht der kandidat` does not apply to this run.

### Additivity and scope

The exact comparison `52a3c5446f41a1dd8678d99875e4cb1eee67874c...12a62523fc5f2259220aece4cc5619dcb8f4ae4d` has 16 files. None is under `.github/**` or `scripts/**`, and no forbidden path appears in the name-only list.

The supplied approved head `40444b1b49d` could not be resolved: GitHub `GET /repos/mcpdev80/baseharbor/commits/40444b1b49d` returned HTTP 422, `No commit found for SHA`. The other supplied head resolves to `ce5cf8f30373e13c0d08092d84b24232e93a356a`; it is not an ancestor of this PR head (merge-base is `1ff16925c4e141d732459a34ddf0b7f49128a214`). The branch history also contains `0768274c6f692bc0779202a1b9dc1fb222fce2ef`, authored by `0428-061-sourcepull`, titled `fix(app): tolerate nil-vs-empty providerPreferences in revalidate`, which is not an ancestor of develop `52a3c5446f41a1dd8678d99875e4cb1eee67874c` and adds `cmd/baha/application_provider_authorization.go` and `internal/application/provider_preferences.go`. This is non-develop candidate content outside the workload-port card. Thus the develop-only additivity condition is not demonstrated and fails on the observable unrelated commit; the unresolved 404 head prevents the second requested comparison from being certified.

`git diff --name-only` against the exact develop base:

```text
cmd/baha/app_apply.go
cmd/baha/app_workload_ports.go
cmd/baha/application_provider_authorization.go
cmd/baha/commands.go
cmd/baha/env_destroy.go
cmd/baha/env_destroy_integration_test.go
cmd/baha/machine_coverage.go
cmd/baha/runtime.go
cmd/baha/workload_port_local_regression_test.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/application/provider_preferences.go
internal/deployment/environment_destroy_scope.go
internal/deployment/environment_destroy_scope_test.go
```

`merge-empfehlung:` Nicht mergen. Keep the candidate open until the unrelated `0768274` content is removed or explicitly authorized, the approved-head identity is corrected/proven, and the exact resulting head has successful required checks. The environment-destroy assertion and consent failure also need resolution before acceptance.

## Evidence and provenance

- Product remote: `origin https://github.com/mcpdev80/baseharbor.git` (fetch/push).
- Exact remote refs observed: develop `52a3c5446f41a1dd8678d99875e4cb1eee67874c`; PR #1723 head `12a62523fc5f2259220aece4cc5619dcb8f4ae4d`.
- `git merge-base --is-ancestor 52a3c5446f41a1dd8678d99875e4cb1eee67874c 12a62523fc5f2259220aece4cc5619dcb8f4ae4d` succeeded.
- `git diff 52a3c5446f41a1dd8678d99875e4cb1eee67874c...12a62523fc5f2259220aece4cc5619dcb8f4ae4d --name-only` is the 16-path list above.
- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)`.
- Prior duplicate-closure evidence was updated in the planning repository and appears in fetched `origin/main` at `evidence/r28-welle5-2026-11-22/stale-pr-census/duplicates-1760-1759.md`.
- Review evidence is published at `evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1723-head12a62523fc5.md`. The fetched `origin/main` tree witness is recorded below.

## repo-rule compliance

- Read-only CODEX-REVIEW; no product files changed, tests run, PR comments, merges, closes, or workflow reruns.
- No `.github/**` or `scripts/**` changes are present in this candidate diff.
- No Docker/Podman commands or compose projects were started.

## Cleanliness

- `docker ps -a` before/after was not run: this review did not invoke Docker or Podman and the review host is not a test VM.

END_BLOCKED codex-rev2-1736: REQUEST CHANGES for #1723 at 12a62523fc5f2259220aece4cc5619dcb8f4ae4d; six failed jobs are candidate/consent failures, not the 0428-237 broker 503; additivity fails due non-develop 0768274 and unresolved approved head 40444b1b49d.

Exact output of `git fetch origin main && git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1723-head12a62523fc5.md'`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1723-head12a62523fc5.md
```
