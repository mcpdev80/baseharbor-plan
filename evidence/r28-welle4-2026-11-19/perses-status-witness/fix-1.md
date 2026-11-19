# 0428-142 — perses status backend-witness — evidence

Card: t-20261119-r28-perses-status-backend-witness
CardNumber: 0428-142
Release: v0.4.28
Worker: laptop-142-statuswitness
Date: 2026-11-19

## HEAD

Commit: 317b730a98b5feea59eb2f1c3152aff676aa1bb2
Branch: lane-0428-142-statuswitness
PR: https://github.com/mcpdev80/baseharbor/pull/1702 (OPEN, not draft, base develop, MERGEABLE)

### Branch provenance (proof)

- Branch cut from develop HEAD at cut time: 7ee6f817dbff5a238bbc651315d6d76b3819fc91
- `git merge-base --is-ancestor origin/develop HEAD` => 0 (develop IS an ancestor of the commit)
- `git log --oneline origin/develop..HEAD` lists ONLY 317b730a (my own commit; no foreign candidate carried on top)
- Base at push: develop 7ee6f817. develop later moved (unrelated): 7ee6f817 -> 558dc42d (PR #1701 0428-079 messaging, internal/metrics/perses_dashboards_messaging.go) -> 223cb97a (docs 0428-148, docs-only). None touch cmd/baha/* or CI. Candidate stays MERGEABLE.

## PLAN

- Reality: fetch develop, verify planning remote (origin/main), cut branch from develop (ancestor verified), claim card.
- Audit data path; record befund-1.md.
- Scope decision (Owner 2026-11-19): both faces, manifest-only witness; three states configured / not-configured / unreachable; Loki/Tempo Verification=none is 0428-143 (file:line); write-set = perses_lifecycle.go + app_status_result.go (+ tests).
- Implement manifest-only per-signal witness in cmd/baha/app_status_result.go + wire perses_lifecycle.go perses status output + JSON.
- Write tests: 2 x 3 (configured / not-configured / logs-absent / never-healthy / human-vs-machine drift) for BOTH faces.
- Verify CI PR Go unit shard selects cmd/baha (ci.yml:125 runs `go test ./cmd/baha`), focused build/vet/test, ci-fast-check.sh.
- Push branch; open draft=false PR (base develop); one exact-head CI run to terminal; verify required aggregate green (skipped != pass).
- Evidence file; move card to review; host cleanup; END.

## repo-rule compliance

- Write-set confined to card/Owner-authorized files: cmd/baha/app_status_result.go, cmd/baha/perses_lifecycle.go, cmd/baha/app_status_result_test.go. No forbidden files touched (internal/capability/perses.go, cmd/baha/machine_coverage.go, internal/serviceaccess/**, internal/metrics/*.go, .github/**, scripts/**).
- No subagents (§4.8): every step executed in this session.
- No merge, no .github/** or scripts/** edits.
- Manifest-only witness; never emits healthy/verified from a manifest flag. Real backend probe cited (reference.go:133-134, :147-148) as 0428-143, not implemented.
- Planning writes made from the /var/tmp clone against https://github.com/mcpdev80/baseharbor-plan.git (fetch + rebase origin/main first), NOT the shared checkout.
- Host hygiene: no containers/compose/volumes started on this host; host besenrein.

## Acceptance point-by-point

### AC1 — perses status names, per observability signal, one of the three states with a source-id

Implementation: cmd/baha/app_status_result.go adds field `PersesBackendWitness []persesBackendSignalVerdict` to the status JSON; the three-state `persesBackendSignal` vocabulary (`not-configured`/`configured`/`unreachable`) and `persesBackendSignalWitnessFromManifest(m)`. cmd/baha/perses_lifecycle.go adds `persesStatusResult.BackendWitness` (JSON) and `renderPersesBackendWitness` (human output: `  <backend> [<source-id>]: <state>`).

Acceptance point -> file:zeile -> test -> run:

- Prometheus/Loki/Tempo per-backend witness declared from manifest flags.
  app_status_result.go:persesBackendSignalWitnessFromManifest; perses_lifecycle.go:reportPersesSurfaceStatus.
  Test: TestPersesStatusWitnessConfiguredForAllSelectedSignals (app_status_result_test.go:54) — asserts prometheus/loki/tempo all "configured" with non-empty SourceID. CI run #6637 job `PR · Go unit · cli-1` SUCCESS.
- Fail-closed without observability backend.
  Test: TestPersesStatusWitnessNotConfiguredWithoutObservabilityBackend (app_status_result_test.go:97). CI run #6637 cli-1 SUCCESS.
- Loki answers from its own logs collection, does not inherit Prometheus.
  Test: TestPersesStatusWitnessLogsAbsentMarksLokiNotConfigured (app_status_result_test.go:111). CI run #6637 cli-1 SUCCESS.

### AC2 — one unit test per state, in cmd/baha, run in the PR Go unit shard

- Test file: cmd/baha/app_status_result_test.go (5 tests, one per state per face, distinct names):
  TestPersesStatusWitnessConfiguredForAllSelectedSignals
  TestPersesStatusWitnessNotConfiguredWithoutObservabilityBackend
  TestPersesStatusWitnessLogsAbsentMarksLokiNotConfigured
  TestPersesStatusWitnessNeverClaimsHealthyFromManifestFlag
  TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends
- Shard selection proof: .github/workflows/ci.yml:125 `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` (PR Go unit). The ci.yml workflow has no `paths` filter, so any cmd/baha change triggers it. CI run #6637 executed `PR · Go unit · cli-1` (the ./cmd/baha shard) SUCCESS — measured, not felt.

### AC3 — human output and machine output (cli-machine-coverage / app status JSON) show the same state, no drift

- Shared witness function `persesBackendSignalWitnessFromManifest` feeds BOTH the machine `perses_backend_witness` JSON (app status) and the human `perses status` output.
- Test: TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends (app_status_result_test.go:151) runs `baha status --json` (machine) and `baha app perses status` (human) in the same repo and asserts every machine backend appears in the human output. CI run #6637 cli-1 SUCCESS.

## Hopf (merge develop 223cb97a into branch; commit witness)

Branch after hopf: lane-0428-142-statuswitness = e22f6795c9298b079072ee740c77d0d2a314643c
ls-remote: `git ls-remote https://github.com/mcpdev80/baseharbor.git
refs/heads/lane-0428-142-statuswitness` => e22f6795c9298b079072ee740c77d0d2a314643c
(refs/heads/lane-0428-142-statuswitness).

Hopf was a monotonic merge-hopf, NOT a rebase/reset/force-of-content:
- cut branch from develop 223cb97a, merged origin/develop into it, then carried my
  exact 3 candidate files (byte-identical to 317b730a, diff-verified) as one commit.
- `git merge-base --is-ancestor origin/develop <new head>` => 0 (develop IS ancestor of new head).
- `git merge-tree --write-tree origin/develop <new head>` => 0 conflicts (disjoint write-sets:
  develop hopf is squash of docs-only 0428-148 + PR #1701 messaging; mine touches only cmd/baha/*).
- `git log --oneline origin/develop..HEAD` lists ONLY e22f6795 (my candidate; no foreign candidate carried on top).
- New exact-head CI run triggered by the synchronize: #6641 (runs/44600570152), watched to terminal.

## CI run witness (exact head, terminal state)

- Run #6637 (old head 317b730a): https://github.com/mcpdev80/baseharbor/actions/runs/44594170799 — completed/success.
- Run #6641 (new head e22f6795, after hopf): https://github.com/mcpdev80/baseharbor/actions/runs/44600570152 — completed/success.
- Required shards (measured, not skipped), identical on both runs:
  - PR · Go unit · cli-1 (go test ./cmd/baha): SUCCESS
  - PR · Go unit · packages / cli-0 / cli-2 / cli-3 / owner: SUCCESS
  - PR · Validation · cli-gofmt / go-vet / go-build: SUCCESS
  - PR Selected Checks aggregate: SUCCESS (Require complete selected Go shard coverage, Require normal job results, Require selected native acceptance before merge)
- Skipped jobs (not required for a lane-branch draft PR; conservative broad fallback "No narrow mapping"): PR Main release source, PR Exact full Pre-Release, Draft source/routing, PR Draft Go/matrix, Targeted HA docker/podman, PR Native matrix, PR Main release checks, advisory/candidate-added/consumer-pins gates. Skipped != pass; the REQUIRED aggregate (PR Selected Checks) is SUCCESS on both #6637 and #6641.
- Base-distance rule: develop moved 7ee6f817 -> 558dc42d (PR #1701 messaging, internal/metrics/*) -> 223cb97a (docs-only 0428-148 squash). None touch cmd/baha/* or CI, so both runs are the exact-candidate proof. No contentually new run owed.

## Local verification (this host)

- `go build ./...` PASS; `go vet ./cmd/baha` PASS; `gofmt -l` clean on changed files.
- Focused tests PASS: `go test ./cmd/baha -run "TestPersesStatusWitness|^TestPerses|^TestBahaStatus"` ok.
- CI fast check PASS: `bash scripts/ci-fast-check.sh` EXIT=0 (gofmt, source readability, workflow policy, actionlint, 280-test validation run ok).
- Full `go test ./cmd/baha` on this host has PRE-EXISTING environmental failures (privileged system-backend / ORAS / git-candidate setup) proven identical on clean origin/develop 7ee6f817 in an isolated worktree (FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle, TestPrepareStagedCoreGitCandidatePinsCanonicalApplication, TestRuntimeUpRequiresORASBeforeCoreBootstrap, hosttrust runMaybePrivileged parallel interaction) — NOT caused by this card. CI runs on a hosted runner with the full toolchain and passes.

## Host hygiene

- No containers, compose projects, or volumes started on this host. No baha-docker/baha-podman test hosts used. No foreign perses/proto-perses/deny-perses/bh-local-shared objects touched. Host besenrein.

## Handoff (newest first)

- 2026-11-19: candidate 317b730a on lane-0428-142-statuswitness, PR #1702 (draft=false, base develop, MERGEABLE); CI #6637 required-aggregate SUCCESS; evidence on origin/main. Card moved to review. No merge by the lane (Owner/Maintainer merge).

## End

END_DONE mission-142-statuswitness.md: hopf done — branch lane-0428-142-statuswitness = e22f6795 (ls-remote: e22f6795c9298b079072ee740c77d0d2a314643c), candidate carried on develop 223cb97a (is-ancestor=0, merge-tree 0 conflicts, only my commit on branch). New exact-head CI #6641 completed/success. PR #1702 open/draft=false/base develop/mergeable. Evidence fix-1 on origin/main. Card -> review. No conflicts.
