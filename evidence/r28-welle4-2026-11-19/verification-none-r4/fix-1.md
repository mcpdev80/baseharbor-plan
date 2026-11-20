# 0428-124 r4 — verification-none composition state: P3 fix + P2 proof

Lane: x-124r4 (worker, correction round r4 after CODEX r3 REQUEST CHANGES on
8d55cc03e1503f9e2dd827b014bcfd0923c9dbde; verdict
evidence/r28-welle4-2026-11-19/codex-review-wave/1695-0428-124-r3.md).
Card: t-20261119-hunt-metrics-verification-none-blind. PR:
mcpdev80/baseharbor#1695, branch lane-0428-124-metrics-verification-none.
Candidate head: f64d30af92f6b894f17c8d98c6b4612b8fbc8b8e.

## PLAN

1. Read r3 verdict act; verify worktree, lane branch HEAD 8d55cc03, develop tip. Done: verdict read from origin/main; remote lane head observed 8d55cc03; develop observed b7cbc00f, then e20f6f6e.
2. Check whether m.Environment is set at prometheus_verify.go:166-172 (fix vs displacement decision). Done — set by construction (see "Punkt A" below). No STOP needed.
3. Punkt A: apply P3 fix + named regression tests. Done: m.Environment passed to ListMetrics; five registry-backed regressions in internal/metrics/composition_state_r4_test.go.
4. Punkt B: seed a real shared provider source with Verification=none in the CLI test; count one [STATE] line with the right reason; mutation proof that the gate is discriminating. Done; mutation NOT committed (witness below).
5. Develop moved past b7cbc00f0adf → monotonic merge-hop (--no-ff, two parents); ci-fast-check run before each push. Done.
6. Commit + push to the named lane branch (no second branch). Done.
7. Watch the pull_request run on the corrected head to terminal. Done: run 44659653714 (head e3bcee4a) completed/failure on `PR · Source format` (801-line readability limit carried in with develop by the hopf) → fix-forward f64d30af → run 44662316412 (head f64d30af) completed/success.
8. Evidence file committed and pushed to origin/main of baseharbor-plan before END. This file.
9. END post to coordinator. Final action.

## Realitätsabgleich / witnesses

Planning repo verification (mission-mandated one-liner):

    $ git -C /var/tmp/x-124r4-plan/plan remote -v | head -1
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)

This evidence is committed in /var/tmp/x-124r4-plan/plan (a /var/tmp clone
against https://github.com/mcpdev80/baseharbor-plan.git), NOT in the quarantined
workers/baseharbor-plan directory.

Product-repo remote truth (ls-remote, at work start):

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-124-metrics-verification-none
    b7cbc00f0adfa36945d6f7af8098d88096276c4f  refs/heads/develop
    8d55cc03e1503f9e2dd827b014bcfd0923c9dbde  refs/heads/lane-0428-124-metrics-verification-none

Base attestation: the r4 work started from the existing lane candidate
8d55cc03e1503f9e2dd827b014bcfd0923c9dbde (the r3 candidate reviewed by CODEX —
this is a correction round on the same chain, not a new branch). Develop tip had
moved from b7cbc00f0adf to e20f6f6e3b27fb7f5d5e88c9f3d0365de8c5aa03, so the
mandated monotonic merge-hop ran: `git merge --no-ff origin/develop` → fe83f8b7
(two parents: 8d55cc03 and e20f6f6e; no rebase, no reset, no force).

Provenance of the candidate head (the base develop e20f6f6e is an ancestor of
the pushed head; the log lists ONLY this chain's commits — no foreign candidate
on top):

    $ git merge-base --is-ancestor origin/develop HEAD   # at e20f6f6e
    ok
    $ git log --oneline origin/develop..HEAD
    f64d30af style(0428-124 r4): keep prometheus_files.go within the 800-line readability limit
    e3bcee4a fix(0428-124 r4): pass m.Environment to composition-state ListMetrics; seed real shared provider source in CLI dedupe test
    fe83f8b7 Merge origin/develop into lane-0428-124-metrics-verification-none (0428-124 r4 hopf)
    8d55cc03 fix(0428-124 r3): adapt ListMetrics call to develop's new env param
    0a64a2ed Merge origin/develop into lane-0428-124-metrics-verification-none (0428-124 r3 hopf)
    e288df14 fix(0428-124 r3): guard empty provider composition + dedupe [STATE] (CODEX #1695 findings 1+2)
    4f0d5e9f Merge commit 'da76c5cf...' into lane-0428-124-metrics-verification-none
    0a33fa0d fix(0428-124 r2): wire CompositionStateError into operator-facing metrics verify path
    cc25c17e fix(0428-124): metrics verification:none composition reports null effective target state

Push witnesses:

    To https://github.com/mcpdev80/baseharbor.git
       8d55cc03..e3bcee4a  lane-0428-124-metrics-verification-none -> lane-0428-124-metrics-verification-none
    To https://github.com/mcpdev80/baseharbor.git
       e3bcee4a..f64d30af  lane-0428-124-metrics-verification-none -> lane-0428-124-metrics-verification-none

Final candidate head: f64d30af92f6b894f17c8d98c6b4612b8fbc8b8e (ls-remote after
final push: f64d30af92f6b894f17c8d98c6b4612b8fbc8b8e).

## Punkt A — P3 (the real defect)

Verdict recipe applied literally: `ProviderSourcesCompositionState` in
internal/metrics/prometheus_verify.go now passes `m.Environment` to
`observability.ListMetrics` (was the empty string), so the composition-state
determination sees the same source set the verify path
(prometheus_verify.go:199-205) and the writer path
(prometheus_files.go EnsureProviderFilesWithRuntimeCAAt) already saw.

Fix-vs-displacement check the mission demanded BEFORE changing: m.Environment
IS set by construction on this call path. The only production caller is
cmd/baha/app_metrics.go:205, which passes `prepared.manifest` — the same
manifest object `verifyManagedMetricsAfterWorkload` hands to
VerifyProviderSourcesAt one call earlier. `prepared.manifest` comes from
`resolvedApplication.Manifest` (prepareManagedMetrics, app_metrics.go:35
`m := resolved.Manifest`), i.e. the loaded baseharbor.yaml manifest; the
manifest `Environment` field (internal/application/manifest.go:23) is a
required, validated manifest dimension (application.New(name, environment, …)
sets it and manifest validation rejects a missing environment). So this is a
correction, not a displacement. No STOP applies.

Named regression (the verdict's case — two provider sources with the same id in
DIFFERENT environments; the state must say what it should, neither "empty" nor
the sum): `TestCompositionStateTwoEnvironmentsSameVerificationNoneID`. The
observability registry keeps ONE record per (id, kind)
(observability.UpdateSignal drops same-id records before appending), so the
condition is realised by walking the same id through its two environment lives
(project token bh-local-twin-dev → bh-local-twin-staging): the dev caller first
sees its own null-target (Verification=none) composition — never the pre-fix
no-source collapse — and after the id moves, the dev caller sees fail-closed
no-source while the staging caller reports exactly its own single source.
Companions pin the rest of the recipe:

- `TestCompositionStateUsesManifestEnvironment` — current-environment
  backend-backed source reports one effective target; an off-environment
  caller still sees no-source (fail-closed filtering preserved).
- `TestCompositionStateBackendSourceReportsOneEffectiveTarget` — one effective
  target with an off-environment sibling registered (never the sum).
- `TestCompositionStateEmptyRegistryReportsNoSource` — truly empty registry
  reports the no-source state.
- `TestCompositionStateMatchesWriterSourceSet` — display and writer agree on
  one source set (the environment guard is real on both paths: an
  environment-ambiguous source is dropped by BOTH, fail closed).

All in internal/metrics/composition_state_r4_test.go (package metrics). CI
pickup: the gate plan selects `PR · Go unit · packages`, which runs the whole
`./internal/metrics` package on the pull_request trigger — runs 44659653714 and
44662316412 both recorded that job success, so every new test here is durably
CI-covered with no .github/scripts change.

RED-proof at the exact pre-fix code: with the fix reverted (git stash, tests
kept), these three fail with the "no provider metrics sources registered"
collapse: TestCompositionStateUsesManifestEnvironment,
TestCompositionStateTwoEnvironmentsSameVerificationNoneID,
TestCompositionStateBackendSourceReportsOneEffectiveTarget. After the fix:
`go test ./internal/metrics/ -count=1` → ok (full package green).

## Punkt B — P2 (the missing proof)

cmd/baha/app_metrics_composition_state_test.go rewritten per the verdict
recipe: the `r4SharedProviderSeam` helper seeds one REAL shared
platform-provider metrics source with Verification=none through the public
observability registry (observability.Update) and writes the shared
registrations.json, so the allowed-application set is shared by both paths;
verifyProviderSourcesAt therefore reaches its CompositionStateError branch and
ProviderSourcesCompositionState resolves the identical nonempty-all-none state
— both reasons live at once. `TestVerifyManagedMetricsDedupesProviderCompositionState`
counts exactly ONE `[STATE] metrics` line and requires it to name the RIGHT
reason ("null effective scrape targets", "Verification=none").
`TestVerifyManagedMetricsCompositionErrorBranchIsReached` pins that the fixture
genuinely reaches the compositionErr != nil branch (the r3 blind spot), and
`TestVerifyManagedMetricsProviderCompositionStateReasonIsUniqueLine` re-counts
from the line side. CI pickup: the `PR · Go unit · cli-*` shards run the
`cmd/baha` package on the pull_request trigger (both r4 runs recorded all four
cli shards success).

Smallest mutation proof (gate removed, NOT committed):

    $ sed -i 's/... compErr == nil && state != "" && compositionErr == nil {/... compErr == nil && state != "" {/' cmd/baha/app_metrics.go
    $ go test ./cmd/baha/ -run 'TestVerifyManagedMetricsDedupesProviderCompositionState|TestVerifyManagedMetricsProviderCompositionStateReasonIsUniqueLine' -count=1
    --- FAIL: TestVerifyManagedMetricsDedupesProviderCompositionState (0.00s)
        app_metrics_composition_state_test.go:140: expected exactly one [STATE] metrics line for an all-verification:none shared composition, got 2:
    --- FAIL: TestVerifyManagedMetricsProviderCompositionStateReasonIsUniqueLine (0.00s)
        app_metrics_composition_state_test.go:181: expected exactly one [STATE] metrics line, got 2:

The mutation was reverted from a byte-copy backup; `git diff --stat` before the
r4 fix commit showed only the intended files (app_metrics.go untouched in every
commit):

    $ git diff --stat
     cmd/baha/app_metrics_composition_state_test.go | 146 +++++++++++++++++++++++--
     internal/metrics/prometheus_verify.go          |   2 +-
     (+ new file internal/metrics/composition_state_r4_test.go)

After restore: `go test ./cmd/baha/ -run TestVerifyManagedMetrics -count=1` → ok.

## Checks and CI

- go build ./... → clean (before and after merge-hop). go vet ./cmd/baha/ ./internal/metrics/ → clean. gofmt -l cmd internal → empty.
- Full local package runs: internal/metrics ok; cmd/baha shows two failures (TestAppEditCommandCompleteProviderEditRunsRealLifecycle, TestPrepareStagedCoreGitCandidatePinsCanonicalApplication) that reproduce IDENTICALLY on the unmodified merge tree (git-stash witness) — pre-existing local-environment limitations (needs a protected Core docker network; native Git archive killed locally), not caused by this change; the exact-head PR CI ran those shards green (cli-0..3 success).
- scripts/ci-fast-check.sh → exit 1 before the first push: it flags internal/metrics/prometheus_files.go at 801 lines — that overflow arrived WITH develop via the hopf (base 755 lines + this chain's 46 lines from the r1-r3 guard/test additions). I ran it anyway and let CI confirm; CI said exactly the same (run 44659653714, `PR · Source format`).
- Run 44659653714 (pull_request, head e3bcee4a): completed/failure. Failing job STATE: `PR · Source format` → "source readability: internal/metrics/prometheus_files.go has 801 lines (limit: 800; baseline ratchet: 0)"; cascade `PR Selected Checks` → "BLOCKED: required job did not succeed: source_format". The other 13 selected jobs (Go unit packages + cli-0..3, owner, go-build/vet/gofmt, plans, policy, Focused Python) all success; 20 jobs skipped per the base plan.
- Fix-forward: f64d30af extracts the provider-security file list into a named providerSecurityFile type + providerSecurityFileCopies helper (behaviour identical; package green; file 795 lines; audit exit 0). No rebase, no force; monotonic on top of e3bcee4a.
- Run 44662316412 (pull_request, head f64d30af92f6b894f17c8d98c6b4612b8fbc8b8e): completed/success — TERMINAL on the exact current head. 15 jobs success (incl. `PR Selected Checks` pass and `PR · Source format`), 0 failure, 20 skipped (runtime/native/release cells, not applicable; skipped != pass per §5.4).
- No .github/workflows/ci.yml, planner, or scripts/test_pr_*/test_ci_* change since e20f6f6e relevant to this PR's routing, so no further base hop is forced: develop had meanwhile moved to ec02d5fa, but under the CI policy 2026-11-19 distance rule the green exact-head run 44662316412 stands (merge window will hop when required by acceptance).

## repo-rule compliance

- One candidate per chain: every r4 commit is on lane-0428-124-metrics-verification-none; no second branch existed; no force-push; merge-hop used --no-ff (two parents).
- Scope: no .github/** or scripts/ edits; no writes to cmd/baha/app_status_result.go or perses-identity-path files (0428-078 field untouched); no merges performed by this lane (auto_merge requested=false explicitly in the PR edit call; PR left open).
- The prometheus_files.go line-fix is the minimal edit that clears the required source-format check on the merged tree; it changes no semantics (pure extraction).
- No subagents used (§4.8); every step ran in this session.
- No VM, container, network or volume was created (all fixtures are temp-dir filesystem state).
- Base attestation + ancestry + log-line witnesses included above.
- Evidence lives only in baseharbor-plan (this file); nothing written to a product repo.

## cleanliness:

- No docker/podman compose project was ever started by this lane (ps-witness: no daemon involvement at all; every fixture is a t.TempDir() filesystem layout). Nothing to bring down.
- Lane artifacts: /tmp/opencode/124-composition-wiring-wt (product worktree, retained for the correction round), /var/tmp/x-124r4-plan/plan (planning clone), /var/tmp/x-124r4-r3verdict.md (verdict extract), /tmp/opencode/x124r4-runwatch*.log + /tmp/opencode/x124r4-app_metrics.go.bak (watch logs + mutation backup).

## END

END_DONE x-124r4: candidate f64d30af92f6b894f17c8d98c6b4612b8fbc8b8e on lane-0428-124-metrics-verification-none (PR #1695, open, unmerged); P3 fixed (m.Environment into composition-state ListMetrics) with the named twin regression, P2 proof wired (real shared verification:none source; mutation witness red at gate removal); run 44659653714 failed source-format at head e3bcee4a, fix-forward f64d30af, run 44662316412 completed/success terminal.
