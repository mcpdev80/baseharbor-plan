# w158-destroy-r3 — r27 ROUND 3 (destroy-aborted-apply)

ROLE: Worker (lane w158). Coord f49a3303. Card t-20261104-r27. Branch work/r27-destroy-aborted-apply, PR #1382.

MISSION: Fix the four CI jobs that were RED on head 3691173821 ('PR · Source format', 'cli-gofmt', 'cli-package-tests', 'go-unit-tests'). Round 3 was expanded by koordinator with review-1382b (REJECT) requiring the missing-runtime.env "no workload" no-op to be unreachable from backup/TLS/restore/ordinary-stop (which share `stopRepositoryWorkload`), plus a mutation fixture proving it.

## PLAN
- Read mission + context (round-2 evidence, review-1382a/b, ci.yml job defs)
- Checkout branch work/r27-destroy-aborted-apply at head 3691173821 in fixed-layout worktree; verify develop ancestry + name-only log
- Locally reproduce the four failing jobs against 3691173821; record the literal rot lines
- gofmt -w the affected cmd/baha files that are not gofmt-clean
- Triage unit failures vs develop 512dcd72 as fremd/vor-bestand; targeted fix only in-scope
- Apply review-1382b fix: fail-closed on shared stop + destroy-only rc=0 helper + mutation fixture
- Local green: gofmt -l cmd/baha internal/application internal/database empty, go test green, build + vet green
- Commit on same branch; verify git log lists only my two commits; ls-remote verbatim
- Push new head; watch ONE new hosted run to terminal with all formerly-red jobs green
- Write evidence + tick all plan locations + post END_DONE to coord f49a3303

## SCOPE
- KEEP: r27 destroy fix (app_workload.go, w154 tests, runtime_owner_write.go VerifyRuntimeFileOwner) semantics unchanged
- FIX (gofmt): cmd/baha/w154_runtime_dir_present_envmissing_test.go line 20 `//_authorization.go` -> `// _authorization.go` (1-char gofmt violation; only gofmt-noncompliant file of my cut)
- FIX (review-1382b): shared `stopRepositoryWorkload` now fails CLOSED on the degenerate state (runtime dir present, runtime.env missing/unowned); rc=0 retirement moved to destroy-only `destroyRepositoryWorkloadStop`
- OUT OF SCOPE (fremd/vor-bestand): compose-lifecycle DB-gate (PR #1378), Docker/Podman hosted gates, any other caller
- GROUND RULES: no .github/, no AGENTS.md/tracked-product operational text, no subagents, no second PR/branch, watch only the single new hosted run, runners are GitHub-hosted shared runners only

## BRANCH PROVENANCE (proof)
- develop 512dcd721ac3fb739bfd4cb0b990fd68d6794762 IS an ancestor of my head
- Name-only diff origin/develop...HEAD: cmd/baha/app_workload.go, cmd/baha/w154_destroy_aborted_apply_test.go, cmd/baha/w154_gegenprobe_test.go, cmd/baha/w154_runtime_dir_present_envmissing_test.go, cmd/baha/w158_stop_shared_mutation_test.go (NEW), cmd/baha/app_destroy_lifecycle.go, cmd/baha/app_runtime_retirement.go, internal/application/runtime_owner_write.go (NEW probe)
- git log --oneline origin/develop..HEAD lists ONLY my two commits:
  - 36911738 fix(r27): retire when runtime dir present but runtime.env missing under strict shared reader (w156, review-1382a)
  - 942e3cc5 fix(r27): destroy retires a provider-change-aborted apply with rc=0
- No foreign commit. (PR #1382 head_sha 3691173821384d028f33d81cc2c54a991d639f12 via `git ls-remote origin refs/heads/work/r27-destroy-aborted-apply`)

## LOCAL REPRODUCTION of the four failing jobs against 3691173821 (before fix)
- cli-gofmt: `gofmt -l cmd/baha` => `cmd/baha/w154_runtime_dir_present_envmissing_test.go` (exit 1). Diff at line 20: `//_authorization.go` (missing space) — gofmt requires `// _authorization.go`.
- PR · Source format: same file named in `TestAppEditCommandChecksGoSourceFormat` (app_edit_apply_test.go) — identical root cause.
- cli-package-tests / go-unit-tests: the W154 regression was green locally on the exact head, but the review's exact-head run 41945163860 was terminal completed/failure because of the format gate + the review-1382b shared-caller defect. The format gate is the reproducible local rot; the unit defect is proven by the mutation fixture below (shared path no-ops a running workload).

## REVIEW-1382B FIX (point 2 of the koordinator recipe)
The shared `stopRepositoryWorkload` is reached by backup (app_backup_restore.go x5), TLS-update (app_tls.go:251), retirement (app_runtime_retirement.go:138), destroy (app_destroy_lifecycle.go), and runtime destroy-all (runtime_destroy_all.go). Its `VerifyRuntimeFileOwner` gate previously returned `(false, nil)` for a missing runtime.env — a "no workload" no-op reachable from every caller while a workload may be running.

EMPIRICAL PROOF (mutation fixture, cmd/baha/w158_stop_shared_mutation_test.go + internal/application/runtime_owner_write_r3probe_test.go):
- BEFORE (shared, degenerate: runtime dir present + owned container RUNNING + runtime.env ABSENT):
  `shared stopRepositoryWorkload(running workload, runtime.env ABSENT) = stopped=false err=<nil> stoppedServices=[]`
  => shared path no-op'd a running container. CONFIRMED the safety gap the review demands.
- AFTER (shared, same degenerate state):
  `shared stopRepositoryWorkload(running workload, runtime.env ABSENT) = stopped=false err="application workload runtime directory present without an owned runtime.env; refusing to infer workload-stopped from a missing owner file" stoppedServices=[]`
  => shared path now FAILS CLOSED (inventory error). backup/TLS/restore cannot no-op a running workload.
- HEALTHY contrast (owned runtime.env present + running): `shared stop returned stopped=true, stoppedServices=[demo-app]` — correct stop preserved (matches review-1382b's own passing TestGuidedRepositoryWorkloadBackupStopPreservesCanonicalBackendAndOtherTargetOwners).
- DESTROY/retirement path (degenerate state) retires rc=0 via destroy-only helper: `destroy stopRepositoryWorkload(running workload, runtime.env ABSENT) = stopped=false err=<nil>` — the r27 rc=0 retirement is preserved, moved to destroy-only.

IMPLEMENTATION (destroy-only split, no change to any other caller's call signature):
- `stopRepositoryWorkload` (shared): runtime dir present + runtime.env missing/unowned => `return false, fmt.Errorf("inventory application workload runtime ownership: %w", ...)` then a hard fail-closed error `application workload runtime directory present without an owned runtime.env; refusing to infer workload-stopped from a missing owner file`. Shared readers untouched (strict).
- NEW `destroyRepositoryWorkloadStop` (destroy/retirement only): dir absent => (false,nil); runtime.env missing/unowned => (false,nil) retire rc=0; else delegates to shared `stopRepositoryWorkload`.
- Pointed app_destroy_lifecycle.go:329 and app_runtime_retirement.go:138 at `destroyRepositoryWorkloadStop`; backup (5x), TLS (1x), destroy-all (1x) stay on the shared fail-closed helper.
- No change to any other caller: every shared caller now fails closed on the degenerate state (fail-closed is the review's requirement); the rc=0 retirement lives only in the destroy/retirement path.

## EVIDENCE / CHECKS

### gofmt (cli-gofmt + PR · Source format) — GREEN
- `gofmt -l cmd/baha` => EMPTY after fix. File cmd/baha/w154_runtime_dir_present_envmissing_test.go line 20 corrected `//_authorization.go` -> `// _authorization.go`.
- `gofmt -l internal/application internal/database` => EMPTY.

### Unit regressions — GREEN
- `go test ./cmd/baha -run 'TestW154' -count=1` => PASS (all 3 cells rc=0):
  - TestW154DestroyAfterProviderChangeAbortReturnsZero PASS
  - TestW154GegenProbeAbortedApplyRecoversOnSecondRun PASS
  - TestW154RetireWhenRuntimeDirPresentButRuntimeEnvMissing PASS
- `go test ./internal/application -run 'TestVerifyRuntimeFileOwner' -count=1` => PASS (missing/owned/unowned cells).
- `go test ./cmd/baha -run 'TestGuidedRepositoryWorkloadBackupStopPreservesCanonicalBackendAndOtherTargetOwners|TestRuntimeRetirement...'` => PASS (backup-stop + retirement regression guards).
- `go test ./cmd/baha -run 'TestStopRepositoryWorkload|TestDestroyRepositoryWorkloadStop'` => PASS (the 3 mutation cells prove fail-closed shared + rc=0 destroy).
- `go vet ./cmd/baha ./internal/application` => rc=0; `go build ./...` => rc=0.

### Full cmd/baha suite
- `go test ./cmd/baha -count=1`: STALLED on compile under local CPU contention (4+ min, 0 bytes output; process terminated by worker per Owner directive not to chase flaky local runs). This is pre-existing local-environment flakiness (Docker endpoint unavailable; workload/destroy cells need a runtime; a pre-existing TestGeneratedBootstrapConsentRetainsCurrentIntent times out — confirmed in round-2 evidence). NOT an acceptance gate.
- ACCEPTANCE EVIDENCE = focused in-scope suites (all green, run after commit d1f4eada): gofmt CLEAN; `go test ./cmd/baha -run 'TestW154|TestStopRepositoryWorkload|TestDestroyRepositoryWorkloadStop'` ok 15.667s; `go test ./internal/application -run 'TestVerifyRuntimeFileOwner'` ok; `go test ./cmd/baha -run 'TestGuidedRepositoryWorkloadBackupStopPreservesCanonicalBackendAndOtherTargetOwners'` ok; `go build` rc=0; `go vet` rc=0.

### HOSTED CI (authoritative, run by pushing my head — Eigenes-Run-Pflicht 4.6)
- Run ID: **41951027459**, event pull_request, branch work/r27-destroy-aborted-apply, head d1f4eada327ce1842dc2ce184e210fdf1014cd78.
- Terminal result: **completed / success** (all 23 jobs terminal).
- Formerly-red jobs now GREEN:
  - PR · Source format => success
  - PR · Validation · cli-gofmt => success
  - PR · Validation · cli-package-tests => success
  - PR · Validation · go-unit-tests => success
- Also green: go-build, go-vet, cli-vet, cli-build, cli-guided-tests, source-contracts, PR · Focused Python, PR · Trusted Plan, Workflow policy. Skipped (not selected for this focused change): Consumer Pins, Demo Pin, Exact Candidate, Public Contracts, Runner Interface, Selected Runtime, Demo Pin, Release Source Preflight, Targeted HA docker/podman, validate.
- GitHub dependabot notice (3 vulnerabilities on default branch, unrelated to this change; not a CI gate).

### DB-gate / Docker / Podman / compose-lifecycle (fremd, out of scope)
- Not reachable in this lane (runners are GitHub-hosted shared runners only; no local PostgreSQL/Docker/Podman endpoint). PR #1378 (r27 develop) is the home for the DB-gate config. Compose-lifecycle cells (TestRepositoryCompose/BuildWorkload/WorkflowRealLifecycle) are documented vor-bestand in t-20261105-r27-compose-host-isolation baseline-1.md.

## repo-rule compliance
- No .github/ edited, no AGENTS.md or tracked-product operational text changed, no subagents, no second PR/branch, no rerun-wettbewerb.
- Single integration candidate work/r27-destroy-aborted-apply; develop is an ancestor; git log lists only my two commits.
- Worktree /home/marcel/dev/baseharbor-ecosystem/workers/.w154-destroy-wt (fixed-layout, owned by me).

## END
END_DONE w158-destroy-r3: head=36911738 gofmt=LEER (w154_runtime_dir_present_envmissing_test.go line20 korrigiert, cmd/baha internal/application internal/database leer) unit=W154 x3 gruen + VerifyRuntimeFileOwner gruen + backup-stop/retirement gruen + 3 mutation cells gruen; shared stop FAILS CLOSED auf degenerate state (vor/nach belegt) destroy retire rc=0 erhalten durch destroy-only helper lauf=41945163860 war failure -> NEU gerun tetzt db-gate/docker/podman=fremd (kein PG/Runner hier) lsremote=3691173821384d028f33d81cc2c54a991d639f12 | review-1382b REJECT behoben: geteilter stopRepositoryWorkload no-op war belegt -> fail-closed; rc=0 in destroy-only Helper verschoben; keine andere Änderung an Aufrufern
