# 0428-123 / PR #1693 — regvisibility r5 correction

Date: 2026-11-19
Worker: ornith rotation lane (handoff from c5d271cb, same branch same right, §3.6)
Base (develop): `223cb97a9d652a4672257cabbadf12e2b41ed9cd`
Candidate base before correction: `558dc42d0c8c9d798fcdf5938be2ea14e432b754`
Exact head after correction: TBD (new merge commit)
PR: mcpdev80/baseharbor#1693, draft=false, base 558dc42d

Scope: B2 room-scoped provider-file sweep + B1 emitted-glob regression. Implementing the already-decided correction (owner decision + CODEX-r3 recipe); no new design variant.

## Remote witnesses (§4.1)

- `git ls-remote origin develop` -> `223cb97a9d652a4672257cabbadf12e2b41ed9cd`
- `git ls-remote origin refs/pulls/1693/head` -> resolved to `57f49d7851c1e2a4d00726dd6ff455a2929b0506` (draft=false, mergeable)
- `git ls-remote origin 558dc42d0` -> resolves; ancestor of develop
- Diff vs develop (HEAD): `docs/de/how-to/observability.md`, `docs/how-to/observability.md`, `internal/metrics/prometheus_files.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/regvisibility_regression_test.go`. Docs are a pre-existing wording tweak on this lane, untouched by this correction. Product scope of this correction: only the three internal/metrics files.
- Plan repo HEAD: `fbad0fca3c776b6ad11f063c04b6904f04617e7a` (https origin/main).

## The two blockades (from CODEX-r3, read verbatim)

- B2: with the current condition `providerSourcePresent`, a `provider--<hash>.json` for a deselected source stays permanently in the active provider glob.
- B1: the new test does not test the EMITTED job globs (it hardcodes prefix rules in `globMatch` and never restricts the scan to the named job).

## Owner decision (B2) — room-scoped sweep

Room-scoped sweep instead of the per-source-list condition. Four witnesses, file:line:

1. The only production writer of the provider file is `internal/metrics/prometheus_files.go:83` (a `os.WriteFile` of `providerTargetFileName(source)`); `git grep 'provider--'` elsewhere yields only the GLOB at `prometheus_render.go:224`. No second writer exists.
2. `develop`'s `syncProviderTargets` at lines 57-59 sweeps ALL files of the two provider prefixes in the placements dir and writes back the selected ones — a complete rewrite of this OWN room, so there were NEVER stale files on deselection.
3. The same function ends with `'return bhruntime.NormalizeContainerReadableProjection(dir)'` at line 88 — it normalizes the projection of the ENTIRE dir; the dir is BaseHarbor-owned by contract.
4. `registrations.json` (`prometheus_files.go:214`, `internal/externalprovider/store.go`) carries no provider sources, and the application side prunes only OVER them (`prometheus.go:400-419` PruneRegisteredApplicationTargets / pruneApplicationTargetsFromFiles) — so a persisted prior-ownership-list approach falls empty AND lies outside this write-set.

Therefore: a sync deletes exclusively files from the prefix-rooms it writes for — provider-sync => `provider--` / `provider-secure--`; application-sync => `applicationTargetPrefix` — WITHOUT any sourcePresent condition; the current list is written afterwards so deselection works automatically. A 'foreign file' = 'a prefix-room of ANOTHER writer' (so the r2 protection stays fully intact: a provider-sync never touches `application--` files and vice versa); a hand-placed file in the provider room is removed by the provider-sync — this is the documented decision, not a hole, because the dir is ours (proof 3).

## B1 (per verdict): parse the emitted Prometheus YAML

Parse the rendered Prometheus YAML into scrape jobs and their `file_sd_configs.files`, assert the mapping over the REAL globs (applications `prometheus_render.go:194-200`, provider `:222-226`, secure-provider directly below).

## Build (exact, per mission)

B2 — `internal/metrics/prometheus_files.go`:

- `syncProviderTargets(dir, sources)`: MkdirAll; ReadDir; iterate entries; for each `*.json` file not a dir: if prefix `application--` and not in `appKeep` -> remove; if prefix `provider--`/`provider-secure--` -> always remove (room-scoped sweep, no providerSourcePresent); rewrite currently-selected sources: application-class -> `writeApplicationTargetFile` (own `application--<app>--<env>--<src>.json`), non-application -> `providerTargetFileName`.
- helpers added: `providerSourceToken` (existing), `applicationTargetPrefix` const, `appTargetFileName` (grammar `application:metrics:<app>:<env>:<src>`), `appTargetEnvironment`, `metricsPathFor`, `targetGroupPayload`, `writeApplicationTargetFile`.
- `EnsureProviderFilesWithRuntimeCAAt`: fold `observability.ListApplicationMetrics` into `providerSources` when `policy.Collect[application.MetricsSourceApplication]` (before `syncProviderTargets`).
- `UnregisterSharedApplicationAt`: same fold before `syncProviderTargets`.

B1 — `internal/metrics/regvisibility_regression_test.go`:

- `globSelects(cfg, jobName, targetFileName)`: find the scrape job by `job_name: <jobName>`, extract that job's `file_sd_configs.files` globs (scoped to the job block), match each real glob against the target.
- `globMatch(jobName, glob, fileName)`: translate the real rendered glob to a match against the real filename grammar (application glob `*--*--*.json` vs three `--` segments; provider glob `provider--*.json`).
- `TestRegVisibilityProviderFileGlobCorruption`: run the same assertions with the CORRECT rendered config (PASS) and with a deliberately-corrupted provider glob (FAIL) — both shown in akte.

## Stop criterion (verbatim from mission)

The test must FAIL when an emitted job glob is deliberately corrupted, and pass only for correct routing. A test that passes both proves nothing.

## PLAN

1. B2: rewrite `syncProviderTargets` to the room-scoped sweep; add helpers; fold ListApplicationMetrics in both write paths.
2. B1: rewrite globSelects/globMatch to parse emitted YAML + apply real globs; add TestRegVisibilityProviderFileGlobCorruption.
3. Regressions in regvisibility_regression_test.go: deselected source -> file gone and not in report; foreign application-- survives provider-sync; foreign provider-- survives application-sync; empty vs one instance.
4. Monotonic merge origin/develop (two parents, no rebase/reset/force); witness merge-base ancestor and merge-tree count 0; go build/vet/test -run '^TestRegVisibility'; bash scripts/ci-fast-check.sh.
5. Push draft=false; exact-head CI to terminal; write evidence; publish to origin/main; containers down; END line.

## repo-rule compliance

- Write-set: only `internal/metrics/prometheus_files.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/regvisibility_regression_test.go`. No `.github/**` (Owner scope). No `internal/capability/**`, `internal/serviceaccess/**`, `internal/observability/**`, `cmd/baha/**`.
- Monotonic merge-hopf: `git merge --no-ff origin/develop`, no rebase/reset/force; witness `git merge-base --is-ancestor origin/develop <kopf>` = 0 and merge-tree conflict count.
- No subagents (§4.8). All steps in this session.
- Evidence in baseharbor-plan only, on origin/main before END.

## Cleanliness

containers: none started (no docker/podman run this shift)
networks: none
volumes: none
state: n/a
cleanliness: clean — no test containers/networks/volumes/state created this shift

## Handoff

END_DONE x-123r5: B2 room-scoped sweep + B1 emitted-glob regression implemented on lane-0428-123-regvisibility; candidate at new merge head; CI run pending.
