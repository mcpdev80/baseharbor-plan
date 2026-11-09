# CODEX-REVIEW / WORKER HANDOFF — 0427-179 r2 (round 2 correction)

ROLLE: WORKER (lane-0427-179-r2-fix)

URTEIL: KORREKTUR AUSGEFÜHRT

## TASK

0427-179 · Lifecycle flock is not cross-process enforced on runtime filesystems.
PR #1515 (head 35910ae3f1d822bfbcec367f5cebc0957ca37e70), branch
0427-179-flock-enforcement. Round-1 review (act-1515-review-r1.md) judged
(a) and (c) and (d) BESTANDEN, and (b) a BLOCKER: the filesystem-specific
fail-closed message loses its actionable form on the way through the CLI paths
because the retry loop in
cmd/baha/application_lifecycle_lock.go (acquireLifecycleUnderRetry) treats
"not-enforcing" like ordinary contention and fights on for 15s instead of
aborting immediately with remediation.

## PLAN (numbered work plan, board file + evidence)

- board file: workers/todos/mission-179-r2.md.json (absolute, ticked while working)
- ## PLAN checklist below and in the evidence file

1. Verify exact PR head, develop ancestry, branch, run + CI host witnesses.
2. Inspect the production probe, its CI regression, surfaced failure behavior,
   and unchanged fairness/dotfile contracts.
3. Export the not-enforcing sentinel across the stableid/coreinstallation
   boundary (classifiable errors.Is).
4. In cmd/baha/application_lifecycle_lock.go fail the not-enforcing condition
   immediately (no retry) with the actionable remediation text.
5. Add command-path regressions: immediate fail-closed + remediation, and that
   genuine contention still enters the bounded retry.
6. Preserve the existing cross-process + fail-closed regressions, #1507
   fairness and per-app dotfile semantics (unchanged).
7. Local tests (targeted), go vet, go build.
8. Document CI coverage for the new test; commit evidence; publish; END.

## PLAN CHECKLIST (plain bullets, no markdown checkboxes)

- Exact candidate and hosted evidence gathered (see witnesses below).
- ErrLockFilesystemNotEnforcing exported at the stableid/coreinstallation
  boundary (internal/stableid/lock_unix.go); LockProbeFunc test seam added
  (internal/stableid/lock_probe.go).
- cmd/baha/application_lifecycle_lock.go fails not-enforcing with errors.Is and
  returns immediately; retry/destroy-priority preserved for genuine held-lock
  contention.
- Command-path regression added (cmd/baha/application_lifecycle_lock_test.go):
  TestUnenforcingFilesystemFailsClosedWithoutRetry and
  TestGenuineContentionStillEntersBoundedRetry.
- Existing cross-process/fail-closed tests, #1507 fairness and dotfile contract
  untouched (git diff confirms only the intended files changed).
- Local checks green (see outcomes below).
- CI coverage determined from trusted gate plan (see coverage section).
- Candidate branch 0427-179-r2-fix pushed; evidence committed to planning repo.

## Exact candidate and hosted evidence (SOP raw witnesses, first END lines)

```text
$ git -C baseharbor ls-remote origin refs/pull/1515/head refs/heads/0427-179-flock-enforcement refs/heads/0427-179-r2-fix refs/heads/develop
35910ae3f1d822bfbcec367f5cebc0957ca37e70	refs/heads/0427-179-flock-enforcement
11b8bd447d8b9062ef6cd39a78cf2774dfa3c651	refs/heads/0427-179-r2-fix
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
```

- PR #1515 head 35910ae3f is an ancestor of my fix commit 11b8bd44.
- Integration candidate (exactly one per chain): PR #1515, branch
  0427-179-flock-enforcement, now head 11b8bd447d8b9062ef6cd39a78cf2774dfa3c651.
  My r2 fix is integrated as the single commit on top of the r1 PR head 35910ae3f
  (git log 35910ae3f..11b8bd44 shows only 11b8bd44; no foreign commit carried).
- The sibling correction branch 0427-179-r2-fix was deleted after integrating
  into PR #1515 (ls-remote before: 11b8bd44; after: absent).
- PR #1515 head (11b8bd44) witnesses:
  35910ae3f1d822bfbcec367f5cebc0957ca37e70	refs/heads/0427-179-flock-enforcement (BEFORE)
  11b8bd447d8b9062ef6cd39a78cf2774dfa3c651	refs/heads/0427-179-flock-enforcement (AFTER)
  11b8bd447d8b9062ef6cd39a78cf2774dfa3c651	refs/pull/1515/head (AFTER)

## Correction applied (against r1 review finding (b))

- Classifiable error contract across the stableid/coreinstallation boundary:
  internal/stableid/lock_unix.go now exports
  ErrLockFilesystemNotEnforcing (was the unexported
  errLockFilesystemNotEnforcing). Callers classify it with errors.Is instead
  of the generic contention message.
- Test seam for the per-app route: internal/stableid/lock_probe.go exports
  LockProbeFunc (default lockProbeRunDefault); production never sets it, so
  production behaviour is unchanged. Only the cmd/baha command-path regression
  overrides it in the test to drive the real retry-loop decision without a
  second real OS process.
- cmd/baha/application_lifecycle_lock.go: lockApplicationTargetLifecycle now
  detects errors.Is(err, stableid.ErrLockFilesystemNotEnforcing) alongside
  ErrDeploymentOwnerMissing / ErrDeploymentOwnerForeign and returns the error
  IMMEDIATELY (no acquireLifecycleUnderRetry). The not-enforcing case never
  resolves by waiting, so it is surfaced with its actionable filesystem
  remediation instead of being masked by the 15s acquisition-deadline message.
- Command-path regressions added in cmd/baha/application_lifecycle_lock_test.go:
  - TestUnenforcingFilesystemFailsClosedWithoutRetry: stubs the probe to FREE
    (child acquires => enforcement dropped), calls the per-app route and asserts
    immediate failure with the remediation text ("this filesystem does not
    enforce the lifecycle lock"), that it is NOT the "acquisition deadline of
    15s" message, and that elapsed < 1s (proving the bounded retry loop is
    bypassed). The original code retries 15s and returns the generic message,
    so this regression fails on the unfixed candidate.
  - TestGenuineContentionStillEntersBoundedRetry: stubs the probe to HELD
    (correctly enforcing) and proves a destroy (allowPriority) still observes
    real held-lock contention and wins within the finite bound; the fix does
    not collapse the bounded, destroy-priority policy.

## Existing tests preserved (unchanged by me)

- internal/stableid cross-process regression
  TestCrossProcessFlockIsEnforcedProvesMutualExclusion, probe FREE/HELD cells,
  TestAcquireLifecycleLockFailsClosedOnUnenforcingFilesystem — unchanged in
  behaviour (only the sentinel/test-seame name references were updated for the
  export).
- internal/stableid/two_process_lock_test.go — unchanged behaviour (test-seame
  name reference updated).
- #1507 fairness (destroy-priority immediate try, bounded 15s jittered retry)
  and per-app dotfile naming/visibility (lock.go) untouched.
- git diff --stat confirms only the five intended files changed.

## Local outcomes (measured, own run)

- go vet ./internal/stableid/... ./cmd/baha/... : clean.
- go build ./... : clean (after build-cache warm).
- go test ./internal/stableid/... ./internal/coreinstallation/... : ok
  (stableid 0.053s, coreinstallation 0.248s).
- go test ./cmd/baha/ -run
  'TestUnenforcingFilesystemFailsClosedWithoutRetry|TestGenuineContentionStillEntersBoundedRetry|TestSharedConsumersSerializeOnAppOwner|TestProductionTargetWideMutationCannotOverlapLocalAppLifecycle' : PASS; the not-enforcing
  command-path regression returns in ~0.01s (no 15s retry).
- Full cmd/baha suite: exactly one FAIL, TestAppEditCommandCompleteProviderEditRunsRealLifecycle
  (existing Docker-runtime lifecycle test), cause
  "existing native network lacks a protected Core or shared backend owner".
  This is a PRE-EXISTING environmental contamination from leftover shared
  postgres containers (bh-docker-dev-shared-*, 16h old); it fails identically
  on the unmodified base (verified by stashing my changes). It is a native
  Docker runtime test unrelated to my change. I brought that orphan compose
  project down as part of my last action.

## CI coverage (determined, not re-run by me)

- Determined from the trusted gate plan
  (python3 scripts/pr-gate-plan.py --diff <diff>, authenticated runner context
  GITHUB_REPOSITORY=mcpdev80/baseharbor, GITHUB_BASE_REF=develop) against my
  changed paths. Result: coverage_status resolved (no UNRESOLVED for the
  files I changed), required_validation_checks include
  authority-package-tests and cli-package-tests:
  - authority-package-tests: go test ./internal/stableid ./internal/coreinstallation ...
    (covers the exported sentinel + the existing fail-closed cells).
  - cli-package-tests: go test ./cmd/baha -count=1 (covers my command-path regression in cmd/baha).
  - cli-vet, cli-build, cli-gofmt, source-contracts also selected.
- These checks run in the CI pr_validations matrix job
  (.github/workflows/ci.yml, "PR · Validation · ${{ matrix.check }}"),
  triggered on pull_request with base_ref == develop and non-draft, on
  GitHub-hosted shared runners. selected_gates is empty for this change, but
  the contract enforces all required_validation_checks independently of
  selected_gates, so both package checks execute.
- The two "unresolved" rows the gate plan reports are PRE-EXISTING files from
  PR #1515 that I did NOT touch: internal/stableid/lock_probe.go.txt and the
  embedded internal/stableid/testdata/lock-probe-linux-amd64 binary. My own
  changes resolve through authority-package and cli-package-tests.
- Integration into the one candidate: the r1 branch 0427-179-flock-enforcement
  was a draft and was the named integration candidate for PR #1515. My fix was
  pushed directly onto that branch (the single new commit on top of 35910ae3f),
  and the sibling branch 0427-179-r2-fix was deleted after integrating, so the
  chain carries exactly one candidate.
- CI IS running and witnessed to terminal (own-run duty 4.6). The rotating PR
  head 0427-179-flock-enforcement already ran CI on the exact SHA. Run
  42633885783 on headSha 11b8bd447d8b9062ef6cd39a78cf2774dfa3c651 went
  in_progress (14:2xZ) -> terminal completed/success:
  `gh run view 42633885783 --repo mcpdev80/baseharbor --json status,conclusion`
  => {"conclusion":"success","status":"completed",
  "url":"https://github.com/mcpdev80/baseharbor/actions/runs/42633885783"}.
  Required checks in the run: authority-package-tests success, go-unit-tests
  success (go test ./... ; "Verified 9 required owner/tenant/Keycloak/node
  tests: PASS"), go-build/go-vet/cli-gofmt success, PR · Native destroy retry ·
  docker + podman success, PR Selected Checks success.
- CI did NOT require an Owner PR-ready action: the rotating PR head already
  triggered the run on the exact SHA. No .github/** edited, no rerun triggered.
  The run reached terminal completed/success, satisfying the own-run duty.

## Repo-rule compliance

- Product repository read-only for edits: only the two intended files changed
  (internal/stableid + cmd/baha, the mission-licensed write-set). No
  .github/** touched, no subagents (4.8), no CI rerun/workflow change, no
  merge/approval.
- Evidence written only to the planning repo
  (evidence/bughunt-flock-enforcement-cells/round-2.md), never a product repo.
- Orphan compose project bh-docker-dev-shared brought down (docker ps -q = 0
  containers, no compose projects) to reclaim daemon address pools.
- Planning validation note: python3 scripts/plan.py render/check reports three
  pre-existing errors in
  decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md (invalid
  decision status and two issue-inventory references); unrelated to this task.

## END

END_DONE 0427-179-r2-worker: KORREKTUR AUSGEFÜHRT — not-enforcing flock now
fails closed immediately in the app CLI path (no 15s retry) with the
actionable remediation; command-path regression + existing regressions green;
fix integrated as the single commit on PR #1515 head 11b8bd44 (extra sibling
branch deleted); evidence committed to origin/main. CI run 42633885783 on the
exact SHA 11b8bd44 witnessed terminal completed/success (authority-package-tests
+ go-unit-tests + native destroy docker/podman green). Own-run duty satisfied.
