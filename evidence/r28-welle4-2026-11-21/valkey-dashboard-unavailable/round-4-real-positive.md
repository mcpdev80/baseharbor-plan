# round-4-real-positive: 0428-183 valkey dashboard unavailable-only + verified-panel gate

ROLLE: Worker. KARTE: t-20261120-r28-valkey-dashboard-unavailable-only (0428-183). PR #1714, branch `lane-0428-183-valkey-dashboard-gate`, base `develop`.

## CONTEXT (reviewer verdict, round 4)

A CODEX-REVIEW with REQUEST CHANGES produced this round. Verbatim critique:

1. POSITIVE CASE IS SYNTHETIC. The test `TestPersesValkeyDashboardVerifiedRealizesRealPanel` sets `capability.ObservabilitySupported` DIRECTLY as a value instead of running the real resolution. The real signals chain on develop delivers `ObservabilityUnsupported` with `ObservabilityVerifyNone` (`internal/capability/reference.go`, ValkeyIntegration metrics signal). Consequence: the verified panel path is UNREACHABLE in production, the test proves nothing about the production decision.

2. WHAT THE CASE STILL CARRIES (keep it): the `unavailable` rendering when NOT verified — file `internal/metrics/perses_dashboards_valkey.go` predicate + `up{job="baseharbor-providers", backend="valkey"}` panel-query (lines 225-245 predicate, 262-270 panel-query) + golden witness `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`.

## PLAN (numbered list)

- Step 1: reproduce the reviewer critique by running the real producer and confirming develop resolves Valkey metrics to ObservabilityUnsupported, not Supported.
- Step 2: confirm the current candidate's verified-branch tests set ObservabilitySupported directly (synthetic).
- Step 3: refactor `perses_dashboards_valkey.go` so the verified branch is driven by an injectable verification anchor (not the finished enum), so the panel code truly runs when a real verified signal exists.
- Step 4: rewrite the positive test to run the real producer, pin today's truth (unavailable-only with cited reason), and drive the verified-panel path via the injectable anchor.
- Step 5: mutations in both directions on the new candidate SHA; record file:line + failing line.
- Step 6: HOP to measured develop, rebase, prove ancestor + only-my-own-commits.
- Step 7: push to PR #1714 and prove delivery.
- Step 8: hosted run to terminal at the exact head (4.6).
- Step 9: write this akte, repo-rule compliance, cleanliness.

## STEP 1 - REPRODUCE THE CRITIQUE (real producer on develop)

Real producer on develop:

- `go test ./internal/metrics/ -run TestPersesValkeyDashboardProducerReadsReferenceCatalog` on the current candidate PASSes (the test asserts the producer does NOT resolve to Supported).
- Probe of the real producer value: `REAL PRODUCER RESOLVES: "unsupported"` and `REF CATALOG VALKEY METRICS: name=metrics status=unsupported verification=none`.
- Confirmed via `git show origin/pr1714:internal/capability/reference.go` (ValkeyIntegration metrics signal = `ObservabilityUnsupported`, `ObservabilityVerifyNone`).
- `internal/capability/integration_contract.go`: `ObservabilitySupported = "supported"`, `ObservabilityUnsupported = "unsupported"`, `ObservabilityVerifyNone = "none"`.

CONCLUSION: on the current develop, the real producer resolves Valkey metrics to `ObservabilityUnsupported` / `ObservabilityVerifyNone` — NOT Supported. The verified-panel path is genuinely unreachable today. The reviewer is correct: the candidate's `TestPersesValkeyDashboardVerifiedRealizesRealPanel` / `TestPersesValkeyDashboardVerifiedGolden` set `ObservabilitySupported` directly, bypassing the real producer and proving only a hypothetical path.

## STEP 2 - CONFIRM SYNTHETICITY OF CURRENT CANDIDATE

Current candidate (`0afcaf374225b206789770499a7aa3b55daf807d`) test `TestPersesValkeyDashboardVerifiedRealizesRealPanel` calls `PersesValkeyDashboardAvailability(capability.ObservabilitySupported)` — passing the finished enum directly, never the real producer. The three-state map `valkeyAvailabilityStatuses()["verified"]` = `capability.ObservabilitySupported` is a caller-set value, not a catalog-resolved one. Same for `TestPersesValkeyDashboardMutantPredicateRevertedIsolated` (`persesValkeyDashboardCatalogWithStatus(capability.ObservabilitySupported)`) and `TestPersesValkeyDashboardVerifiedGolden` (`persesValkeyDashboardCatalogWithStatus(capability.ObservabilitySupported)`).

## STEP 3 - REFACTOR (injectable verification anchor, not finished enum)

File: `internal/metrics/perses_dashboards_valkey.go` (write-set allowed). Changes:

- `persesValkeyDashboardCatalogWithStatus(status, verification)` now takes a SECOND parameter `verification capability.ObservabilityVerificationMode`. The verified-panel branch now requires `status == ObservabilitySupported && verification == ObservabilityVerifyBackend`. This is the real gate: supported AND backend-verified, never supported-alone.
- New `persesValkeyBackendVerified()` returns `capability.ObservabilityVerifyNone` — the real production backend-verification verdict (today none, because no verified signal exists). This is the injectable test anchor: a test drives the verified branch by supplying `ObservabilityVerifyBackend`, never by setting the supported enum alone.
- `persesValkeyDashboardCatalog()` now feeds `(persesValkeyResolvedSignalStatus(), persesValkeyBackendVerified())`.
- `PersesValkeyDashboardAvailability(status, verification)` takes both axes.
- New `PersesValkeyDashboardAvailabilityResolved()` = canonical production caller feeding both real producers — the CLI face wires exactly this, never a fabricated status.

## STEP 4 - REWRITTEN POSITIVE TESTS (real producer, pinned today's truth)

File: `internal/metrics/perses_dashboards_valkey_test.go` (write-set allowed).

- `TestPersesValkeyDashboardCatalogIsUnavailableOnly` now drives through the real producer + real verification (`persesValkeyResolvedSignalStatus()` = unsupported, `persesValkeyBackendVerified()` = none) and asserts exactly one entry, UNAVAILABLE, no fabricated panel, reason names "Valkey" + "ObservabilityUnsupported" + "no exporter". This is the real shipped truth, the positive witness.
- `TestPersesValkeyDashboardAvailabilityResolvedUnavailableToday` pins the production caller `PersesValkeyDashboardAvailabilityResolved()` to unavailable today.
- `TestPersesValkeyDashboardAvailabilityVerifiedGated` drives the verified branch via `ObservabilitySupported + ObservabilityVerifyBackend` (real anchor) -> available with datasource; and `ObservabilitySupported + ObservabilityVerifyNone` -> still unavailable (verified-only predicate).
- `TestPersesValkeyDashboardVerifiedRealizesRealPanel` / `VerifiedGolden` / `MutantPredicateRevertedIsolated` now use the injectable verification anchor instead of the finished enum.
- `keysOf` helper retained; `TestPersesValkeyDashboardThreeStates` replaced by the two-gated tests above (the three-state loop passed a bare status; the real two-axis gate supersedes it).

## STEP 5 - MUTATIONS (both directions, on new candidate)

New candidate SHA (local, before HOP): `6d85444f2` / rebased HEAD `bf251b2b083d39b26826732b9e79b790f7044936`.

MUTATION (i): predicate `unavailable` -> `ok`. Set `persesValkeyDashboardCatalogWithStatus` return to `Unavailable: false`, `Reason: ""` (the unavailable branch). Run:

```
go test ./internal/metrics/ -run "PersesValkey"
```

RESULT: 7 tests FAIL — `TestPersesValkeyDashboardCatalogIsUnavailableOnly`, `TestPersesValkeyDashboardAvailabilityResolvedUnavailableToday`, `TestPersesValkeyUnavailableMarshalsReason`, `TestPersesValkeyDashboardAvailabilityPinsReasons`, `TestPersesValkeyDashboardAvailabilityVerifiedGated`, `TestPersesValkeyDashboardMutantAvailabilityForcedIsolated`, `TestPersesValkeyDashboardGoldenFiles`. Failing line witness:

```
perses_dashboards_valkey_test.go:39: Valkey dashboard has no native metrics signal and must be marked unavailable (producer="unsupported" verification="none")
```

This is mutant A (a reverted predicate is not an independent witness -> isolated test). GATE IS REAL.

MUTATION (ii): verify-query removed. Replace the panel query `up{job="baseharbor-providers", backend="valkey"}` with an empty spec (query-less graph panel). Run:

```
go test ./internal/metrics/ -run "PersesValkey"
```

RESULT: `TestPersesValkeyDashboardVerifiedGolden` FAILS (golden file requires the real query in the panel). GATE IS REAL.

Both mutations restored clean (`diff internal/metrics/perses_dashboards_valkey.go /tmp/opencode/0428-183-tmp/valkey.go.bak` = IDENTICAL; query count = 2, `persesValkeyBackendVerified` count = 7).

## STEP 6 - HOP (measured develop) + REBASE + PROOF

Base attestation (ref cut from): `f5ce95afc` = `f5ce95afc1cfec053dd7717ed05e89bfe153535`. `git merge-base --is-ancestor f5ce95afc HEAD` = YES.

Fresh measured develop (git ls-remote):

- Before rebase: `22fc68ebc0655874bc3f6aa886ff356dcad79624` (as mission predicted).
- At rebase time: `e6c199e7b7dd7d076a776d11c3ba16f25e59c254` (develop advanced during the shift; measured fresh, not cited from memory).

Rebase: `git rebase origin/develop` -> success.

Hop proof:

- `git merge-base --is-ancestor origin/develop HEAD` = YES (develop `e6c199e7` IS an ancestor of HEAD).
- Commits on top of develop (only my branch's own):
  - `120765aec fix(0428-183): verified Valkey dashboard carries a real query and contracts 0428-182` (prior worker session, original PR #1714 content)
  - `dc643aec2 fix(0428-183): valkey dashboard availability verified-gated` (prior worker session, original PR #1714 content)
  - `bf251b2b0 fix(0428-183 r4): drive valkey verified panel through injectable verification anchor, not finished enum` (MINE, round 4, lane identity below)
- `git log --format=%an origin/develop..HEAD` uniq = `0428-183-realpos` (my round-4 commit) and `worker` (the 2 prior commits — a different earlier session's identity, not mine to rewrite; they are the original PR #1714 content I rebased onto, not rewrote).
- `git diff origin/<base>...HEAD --name-only` at my commit = `internal/metrics/perses_dashboards_valkey.go`, `internal/metrics/perses_dashboards_valkey_test.go`, `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`, `internal/metrics/testdata/perses-valkey/valkey-targets.json` (write-set).

Single integration candidate per chain: I kept `lane-0428-183-valkey-dashboard-gate` the entire shift. The remote branch tip had a prior rebased commit `0afcaf374` (my own earlier round-4 content on an older develop) — my rebased HEAD is a strict superset of it on the newest develop, integrated by one force-push (documented below), NOT a second branch.

## STEP 7 - PUSH + DELIVERY PROOF

Push: `git push --force-with-lease origin lane-0428-183-valkey-dashboard-gate` -> `+ 0afcaf374...bf251b2b0 ... (forced update)`.

Delivery proof (git ls-remote, own persistent zone):

```
git ls-remote origin refs/pull/1714/head -> bf251b2b083d39b26826732b9e79b790f7044936
git ls-remote origin refs/heads/lane-0428-183-valkey-dashboard-gate -> bf251b2b083d39b26826732b9e79b790f7044936
```

PR #1714 head = my HEAD `bf251b2b0`. Delivered.

## STEP 8 - HOSTED RUN TO TERMINAL (4.6)

Run ID: `44920689363`, headSha `bf251b2b083d39b26826732b9e79b790f7044936`, event `pull_request`, base `develop`. Confirmed `gh api .../runs/44920689363 --jq '.head_sha,.event'` = `bf251b2b0` / `pull_request`.

Per-job conclusions (gh api jobs):

- success (executed): `PR · Go unit · cli-0` (3m41s), `cli-1` (2m44s), `cli-2` (2m40s, was pending at first read -> terminal success), `cli-3` (2m40s), `Go unit · owner` (1m50s), `packages` (1m56s), `Validation · go-build` (1m2s), `go-vet` (1m10s), `Focused Python` (38s), `Trusted Plan` (9s), `Source format` (20s), `Workflow policy` (23s), `Native gate plan` (7s).
- skipped (advisory / not triggered by this change path, NOT a pass/fail): all release, pre-release, Native Keycloak/Core, Native, Runner Interface, Consumer Pins, Demo Pin, Exact Candidate, Exact full Pre-Release, Draft Go, Targeted HA podman/docker, Workstation onboarding, Public Contracts. No red anywhere.

No red => no `gh run view --job <id> --log` needed.

## repo-rule compliance

Write-set (mission TABOO respected):

- EDITED: `internal/metrics/perses_dashboards_valkey.go`, `internal/metrics/perses_dashboards_valkey_test.go`, `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`, `internal/metrics/testdata/perses-valkey/valkey-targets.json`.
- NOT TOUCHED (TABOO): `internal/capability/perses_selection.go`, `internal/observability/registry.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`, `.github/**`, `scripts/**`.
- No `.github/**` edit, no workflow_dispatch, no rerun I did not trigger on my own head.
- No second branch (one integration candidate per chain).
- Identity in my round-4 commit: `0428-183-realpos <0428-183@baseharbor.local>`. Prior 2 commits carry an earlier session's `worker` identity (original PR #1714 content, not rewritten).
- Build: `go build -o ./bin-baha ./cmd/baha` succeeds (disk-backed GOCACHE). `go vet ./internal/metrics/` clean. Candidate-added checks (`bash scripts/ci-fast-check.sh`) = 295 tests OK (first run had 1 disk-quota discovery error, retryped clean on disk-backed TMPDIR).
- Evidence files live ONLY in baseharbor-plan (this akte); no `.evidence/` directory in the product repo.
- No compose/container started (no docker/podman on this host).

## cleanliness

- No docker/podman containers or compose projects started this shift. `docker ps -a` witness: n/a (host is the coordinator/codeman server; test hosts are named SSH hosts only).
- Scratch zone: `/var/tmp/0428-183-build/` (GOCACHE + GOTMPDIR, disk-backed to avoid /tmp tmpfs quota). No stray files in `/home/marcel/dev/baseharbor-ecosystem/`.
- `diff internal/metrics/perses_dashboards_valkey.go /tmp/opencode/0428-183-tmp/valkey.go.bak` after mutations = IDENTICAL (clean restore).
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/0428-183-valkey-wt` (my lane-named worktree, right place).

## END

Lane `0428-183-realpos` DONE. Candidate `bf251b2b083d39b26826732b9e79b790f7044936` on PR #1714, base develop, all executed required hosted jobs success, mutations proven both directions, hop proven, delivery proven. Awaiting coordinator END verification / CODEX-REVIEW.
