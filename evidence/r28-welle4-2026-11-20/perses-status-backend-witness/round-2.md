# 0428-142 r2 — real `unreachable` backend-witness emission

Korrekturrunde nach CODEX-REVIEW (note-142-fix.txt / review-1.md). PR #1702, head `6740299f91c040af7b1357d63be898eac57669f5`, base develop.

## PLAN

- Befund 1 (content): the backend-witness still derives every state from manifest flags; `unreachable` is declared (`app_status_result.go:64-65`) but never emitted. Derive per-backend state from a REAL resolved backend signal so `unreachable` is a genuine state, tested against a manifest that declares a signal but resolves unreachable.
- Befund 2 (records): locate the false `validate ...` claim in the akte, correct it with a witnessed source.
- Befund 3 (knowledge, not a bug): after merging #1702 to develop 40cb28c the four CLI shards stay red (0428-204). Do NOT touch cmd/baha/main.go, internal/operatorauth/**, or tests that 0428-204 occupies.

### Steps

- Fix witness test helper to add configureTestTarget(t) env setup so the witness path resolves (baseline repro).
- Implement unreachable emission: change persesBackendSignalWitnessFromManifest signature to (m, resolvedHostSignalStatus, PersesBackendSignalWitness), wire both call sites.
- Add a test asserting unreachable against a declared-but-unresolved manifest (not against a flag).
- Correct the false validate claim in the akte with a witnessed source.
- Gate: go test cmd/baha (Status|Witness|Perses) before/after + go test internal/metrics, go vet, go build.
- One PR push on lane-0428-142-statuswitness, watch hosted run to terminal, record run-id + conclusion.
- Publish evidence to baseharbor-plan origin/main, clean host, post END to coordinator.

## Repo-rule compliance

- Write-set: exactly the PR witness files (cmd/baha/app_status_result.go, cmd/baha/perses_lifecycle.go, cmd/baha/app_status_result_test.go, and the per-backend witness input from internal/metrics which is already in the PR). No new files beyond the PR's existing ones.
- No changes to cmd/baha/main.go, internal/operatorauth/**, internal/capability/perses.go, internal/serviceaccess/**, .github/**, scripts/**.
- No subagents; every step runs in this session.

## Cleanliness

- Host cleaned before END. My shift-started docker container `bh-docker-dev-edit-runtime-integration-dev-api-1` (up 17s, from the ORAS/runtime shard verification) was removed: `docker rm -f ...` -> `bh-docker-dev-edit-runtime-integration-dev-api-1`. Post-teardown ps-witness: only the 13-day pre-existing shared stack remains (`bh-docker-dev-shared-postgres-1`, `...-member-1-1`, `...-admin-1`, `bh-docker-dev-shared-openbao-admin-1`), none mine. No podman containers. No orphaned volumes of mine. No stray `baha` binary (git status clean).

## CI run watch (terminal, witnessed)

- PR #1702 head = `3f7600ded0d98902ec689543fa29ad4fdc0d3e6e` (pushed 6740299f9..3f7600ded to lane-0428-142-statuswitness; ls-remote proof: 3f7600d on both refs/heads/lane-0428-142-statuswitness and refs/pull/1702/head).
- Hosted run 44841239916 (pull_request, ci.yml, head 3f7600d): status `completed`, conclusion `failure` (updated 2026-11-21T00:11:13Z). The required aggregate `PR Selected Checks` = **success**.
- The only failing required jobs are the Go-unit DB shards `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,packages}`; the `owner` shard = success. The required aggregate is green.
- These shards run `bash scripts/pr-unit-database.sh <shard>` against an isolated PostgreSQL container. The failing Go tests are all host-environment failures, NOT a regression from this card:
  - `TestRuntimeUpRequiresORASBeforeCoreBootstrap` — "container runtime orchestration not found" / no ORAS on this host.
  - `TestSharedBackendReconcileRejectsSecondProcess` — second-process shared-owner lock needs a real runtime.
  - `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` — needs a real runtime.
  - `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` — "native Git archive failed: signal: killed" (host OOM kill at 60s).
- NOT a regression: on the PR head `6740299f9` WITHOUT my change, `bash scripts/pr-unit-database.sh cli-1` fails with the identical pair `TestRuntimeUpRequiresORASBeforeCoreBootstrap` + `TestSharedBackendReconcileRejectsSecondProcess`. My witness fix compiles clean (cli-0 = 434 passed / 13 intentional skips / 447 discovered) and the full witness/perses/status suite is green locally. These four also fail on clean develop (no real container runtime on this host).
- Per the scope split in the working note: these are a host-environment / runner-runtime STATE, not a content fix. I do not touch runner infrastructure or the container runtime, and I do not add a `.github/**` change to paper over a host gap. The required aggregate is green; P1 (real `unreachable` from a resolved signal) is implemented and green.

## END

- END_DONE w222-0428-142-witness: candidate SHA 3f7600ded0d98902ec689543fa29ad4fdc0d3e6e.
