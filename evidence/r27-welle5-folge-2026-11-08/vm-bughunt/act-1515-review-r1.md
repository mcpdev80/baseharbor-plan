# CODEX-REVIEW 0427-179 r1 — PR #1515

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify the exact PR head, develop ancestry, branch run and H-P5 Finding 1.
2. Inspect the production probe, its CI regression, surfaced failure behavior, and unchanged fairness/dotfile contracts.
3. Record the verdict and raw remote evidence.

## Exact candidate and hosted evidence

- PR #1515, branch `0427-179-flock-enforcement`, head `35910ae3f1d822bfbcec367f5cebc0957ca37e70`.
- `develop` `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor; `develop...head` is `0 1`.
- Branch run 42624603781 is terminal `completed/success` on the exact head. `PR · Validation · go-unit-tests`, build, vet, authority-package-tests, and `PR Selected Checks` passed. Other impact groups were skipped and are not counted as passes.
- `go test ./...` in `go-unit-tests` includes `internal/stableid`; the new cross-process and fail-closed regressions were executed in that passing job.

## Review against hp5.md FINDING 1

### (a) Is flock enforcement actually checked?

Yes. `internal/stableid/lock_unix.go:lockNamed` first acquires the lock and then runs `lockProbeRun` against the same lock path. The probe is a separate OS process; it opens the lock and attempts `LOCK_EX|LOCK_NB`. If the child acquires it, production releases its own lock and returns `errLockFilesystemNotEnforcing`; probe errors also release and fail the acquire. This detects the hp5 overlayfs/kernel behavior instead of treating successful in-process flock contention as proof.

### (b) Is the failure message actionable to the caller?

**Blocking gap in the app CLI path.** The filesystem-specific error text itself gives useful remediation: move the state root to an enforcing local filesystem and do not remove the lock file. But `cmd/baha/application_lifecycle_lock.go:lockApplicationTargetLifecycle` routes every `AcquireAppLifecycleLock` error other than owner-missing/foreign into `acquireLifecycleUnderRetry`. The new `errLockFilesystemNotEnforcing` is therefore treated like ordinary lock contention. The command retries for up to 15 seconds and then returns the generic “Target application lifecycle is active” / acquisition-deadline message, hiding the actionable filesystem cause. The underlying acquire fails closed, but `up`/`apply` callers are misled about why and how to recover.

### (c) Does the cross-process regression prove contention and run in CI?

The regression `TestCrossProcessFlockIsEnforcedProvesMutualExclusion` starts a distinct OS process that attempts the production acquire while the first process holds the lock, and requires the second process to fail specifically with the lifecycle-held outcome. Separate contract tests exercise probe-FREE, probe-HELD, and production fail-closed behavior. The package is selected by the passing exact-head `go-unit-tests` job via `go test ./...`; these are CI-executed tests, not VM-only evidence.

### (d) Fairness and per-app dotfile behavior

No rollback found. The PR changes only `internal/stableid` lock implementation/probe/test files; it does not change `cmd/baha/application_lifecycle_lock.go` or the per-app acquisition policy. The `#1507` destroy-priority immediate try and bounded/jittered 15-second retry remain. `AcquireAppLifecycleLock` still creates the hidden per-app dotfile inside the shared brief lock section and removes it on unlock; target-wide scanning and per-app dotfile naming/visibility semantics remain in `lock.go`.

## Correction recipe and stop criterion

- Give the not-enforcing/probe-unavailable condition a classifiable error contract through the `stableid`/`coreinstallation` boundary. In `cmd/baha/application_lifecycle_lock.go`, propagate that condition immediately instead of retrying it as contention; preserve retries and destroy-priority behavior for genuine held-lock contention.
- Add a command-path regression that injects the not-enforcing acquire result through the per-app route and asserts immediate failure with the actionable filesystem remediation, without the 15-second contention fallback. Keep the existing two-process regression and CI selection.
- Stop review when the user-facing `up`/`apply` path retains the filesystem-specific fail-closed reason, and the exact-head required checks pass. Preserve the existing fairness and dotfile tests/contracts.

## Repo-rule compliance

Product repository and GitHub were read-only. No local product tests, reruns, approval, or merge were performed. The exact candidate was inspected through a fetched review ref.

Planning validation note: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed rendering but check reports three pre-existing errors in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md` (invalid decision status and two issue-inventory references). No unrelated decision data was changed. The requested review evidence is published as instructed.

## SOP raw witnesses

```text
$ git -C baseharbor ls-remote origin refs/pull/1515/head refs/heads/0427-179-flock-enforcement refs/heads/develop
35910ae3f1d822bfbcec367f5cebc0957ca37e70	refs/heads/0427-179-flock-enforcement
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
35910ae3f1d822bfbcec367f5cebc0957ca37e70	refs/pull/1515/head

$ gh pr view 1515 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-179-flock-enforcement","headRefOid":"35910ae3f1d822bfbcec367f5cebc0957ca37e70","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1515"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-179-flock-enforcement --limit 8
completed	success	CI · PR #1515	CI · Source & Quality	0427-179-flock-enforcement	pull_request	42624603781	11m16s	2026-11-09T13:20:25Z

$ gh run view 42624603781 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"35910ae3f1d822bfbcec367f5cebc0957ca37e70","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42624603781"}
```

END_DONE 0427-179-r1-review: KORREKTUR PR #1515 35910ae3f; flock is now probed cross-process and CI covers the regression, but app CLI retries the new filesystem-not-enforcing failure as ordinary contention and hides its actionable recovery message.
