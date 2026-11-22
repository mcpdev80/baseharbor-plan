# CODEX-REVIEW: PR #1627 exact-head review

Session marker: rev1627-20261122
Role: CODEX-REVIEW, read-only
Reviewed PR head: bfd01276ff2c1db005063c39390e03bd89cf80cd
Base: develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c
Exact hosted run: 44995034290

## PLAN

1. Poll remote PR #1627 until its head changes from 0768274c6f6 and the candidate is based on develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c; record whether the PR becomes CLEAN.
2. Observe the exact new-head hosted PR run to terminal and capture Selected Runtime, Native matrix, and selected integration job IDs.
3. Review the diff from develop and compare the approved head 0768274c6f6 for the stale-impact consent regression and requested PR behavior.
4. Verify changed paths and classify any skipped runtime/native matrices from the gate-plan output.
5. Publish this SHA-specific evidence and report the verdict to the coordinator.

## Verdict

REQUEST CHANGES

merge-empfehlung: Do not merge. Exact-head run 44995034290 failed the selected Docker and Podman application gates and terminal PR Selected Checks aggregate. The same test assertion failed on both runtimes. Correct/triage this failure and require a new terminal exact-head run before merge.

## Candidate and provenance

The live PR head changed from 0768274c6f692bc0779202a1b9dc1fb222fce2ef to bfd01276ff2c1db005063c39390e03bd89cf80cd. Remote witness at review completion:

```text
52a3c5446f41a1dd8678d99875e4cb1eee67874c refs/heads/develop
bfd01276ff2c1db005063c39390e03bd89cf80cd refs/pull/1627/head
```

GitHub compare develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c to candidate bfd01276ff2c1db005063c39390e03bd89cf80cd reported ahead 22, behind 0, merge base 52a3c5446f41a1dd8678d99875e4cb1eee67874c. The PR is OPEN and mergeStateStatus BLOCKED, so it did not reach CLEAN.

The candidate diff against develop contains these 12 paths:

- cmd/baha/application_provider_authorization.go
- cmd/baha/commands.go
- cmd/baha/env_destroy.go
- cmd/baha/env_destroy_integration_test.go
- cmd/baha/machine_coverage.go
- docs/cli/command-index.md
- docs/de/cli/command-index.md
- docs/de/reference/cli-machine-coverage.md
- docs/reference/cli-machine-coverage.md
- internal/application/provider_preferences.go
- internal/deployment/environment_destroy_scope.go
- internal/deployment/environment_destroy_scope_test.go

No `.github/**`, `scripts/**`, `internal/identity/**`, or `internal/serviceaccess/**` path is in the candidate diff against develop. Comparing old approved PR head 0768274c6f6 to bfd01276ff2 includes develop commits/merges and the final merge of 0768274c6f6; no new feature commit after 0768274c6f6 was introduced by the hop.

## Review notes

The provided review mission names card t-20261122-r28-source-pull-consent / 0428-061. GitHub PR #1627's title and body instead identify `0428-055: baha env destroy (env-scoped identity removal)`. I reviewed the actual candidate and its published PR scope; this card/PR mismatch remains a coordinator follow-up and is not silently treated as the same contract.

In the reviewed code, provider-impact consent revalidation retains the raw PlanID fast path and falls back to `ValidateProviderImpactRevalidation` for frozen authority equivalence; absent authority fails closed as stale consent. Manifest comparison canonicalizes the non-serialized nil-versus-empty provider-preferences projection. The environment-destroy CLI previews the scoped/preserved set, requires `--yes`, requires separate `--delete-data` consent for deletion, applies exact deployment UUIDs, verifies each lifecycle result, and removes the environment identity only after successful processing. This review did not identify a code finding before the required CI stop on the first failed selected gate.

## Exact-head CI evidence

Run 44995034290 tested bfd01276ff2c1db005063c39390e03bd89cf80cd and reached terminal `completed / failure` at 2026-11-22T06:59:39Z. There were 5 failed jobs; `PR Selected Checks` job 137127410987 failed. The two selected Core-less application jobs both executed `TestEnvironmentDestroyNativeLifecycle` and failed with the same log line:

- Docker job 137124194466, `PR · Selected Core-less · docker / PR selected · integration/docker/coreless-lifecycle · application`: `env_destroy_integration_test.go:136: KEEP must retain the stopped deployment owner: found=true state="runtime-retired" ready=false err=<nil>`.
- Podman job 137124193912, `PR · Selected Core-less · podman / PR selected · integration/podman/coreless-lifecycle · application`: `env_destroy_integration_test.go:136: KEEP must retain the stopped deployment owner: found=true state="runtime-retired" ready=false err=<nil>`.

The parent selected integration jobs also failed: Docker job 137127310612 and Podman job 137127206689. `PR Selected Checks` job 137127410987 completed failure after its `Require normal selected job results` step failed.

`PR · Native gate plan` job 137124127100 completed success. Its exact-head `pr-plan.json` reports `coverage_status=resolved`, `fallback_used=true`, `broad_required=false`, base/merge-base 52a3c5446f41a1dd8678d99875e4cb1eee67874c, and selected gates `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`. The aggregate exposed both integration matrix entries. It also reports `pr_native_impact.required=false` and `matrix={"include":[]}`, so the Native impact matrix length was zero. `PR · Native · ${{ matrix.id }}` job 137124158115 was skipped. `PR · Selected Runtime` job 137124193828 was skipped; the aggregate runtime matrix was the static `not-required` entry. The environment-destroy source is in the base gate catalog under both native Docker and Podman environment-destroy entries and its test source maps to both coreless lifecycle surfaces. The application components of those two selected gates did execute the test, and both failed as recorded above. Matrix-routing classification belongs with card 0428-235, not as a separate candidate defect.

No rerun or workflow modification was performed. No local tests were run.

## Repository and cleanliness

Planning repository remote witness from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Planning origin/main before publication: 76edabee02acdb22f94196722f37a6b37f0fbd95.

Coordinator-host container listing before review, shell PID 2986184: `docker ps -a` returned only the header and no containers.
Coordinator-host container listing after review, shell PID 3012886: `docker ps -a` returned only the header and no containers.

END_BLOCKED codex-rev2-1736: REQUEST CHANGES for exact head bfd01276ff2c1db005063c39390e03bd89cf80cd; exact run 44995034290 terminal failure, selected Docker and Podman application jobs failed the same native lifecycle assertion.
