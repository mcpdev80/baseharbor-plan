# PR #1578 Review R1

## PLAN

1. Verify task contract, ownership, exact candidate/base ancestry, own-commit log, PR state, and hosted run.
2. Review UID generation, idempotent/concurrent creation, legacy reuse, rename stability, CLI-entry tests, and role separation.
3. Record evidence-backed verdict and any actionable findings in the planning evidence file.
4. Run planning validation, publish evidence to origin/main, verify remote presence, and post END.

## Scope and remote state

Role: CODEX-REVIEW only; no merge. The reviewed object is the exact mission SHA `670402fdefc57440a144365fce672b909a661228`, parent `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, subject `feat(environment): durable non-secret env identity per (target,env)`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 670402fdefc57440a144365fce672b909a661228` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..670402fdefc57440a144365fce672b909a661228` lists only the one task commit:

```text
670402fd feat(environment): durable non-secret env identity per (target,env)
```

Product remote witness from fresh clone `/tmp/opencode/mission-rev1578-wt` and `git ls-remote`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
7930095b04ae716fe2375ee8f6a578535990eec2	refs/pull/1578/head
```

PR #1578 is OPEN and DRAFT on `develop`, branch `lane-0428-uid-environment`. The live head is now `7930095b04ae716fe2375ee8f6a578535990eec2`; it includes the requested SHA plus the later r2 correction. This verdict is SHA-scoped to `670402f`; it is not a review of live head `7930095b`. The planning task currently lists dependency `t-20261114-r28-cli2-uid-app` as NOT accepted. No status or dependency transition was performed.

The requested candidate changes exactly four files: `internal/deployment/environment_identity.go`, its test, `internal/environment/environment.go`, and its test. No application, CLI, target implementation, workflow or documentation paths are part of this commit.

## Hosted run

Specified GitHub Actions run `43644615047` is terminal `completed/success`, event `pull_request`, exact head `670402fdefc57440a144365fce672b909a661228`, workflow `CI · Source & Quality`. Active successful jobs: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `PR · Draft Go · packages`. Other jobs were skipped under draft selection. This establishes the requested run result for the requested SHA; it does not establish coverage of the absent CLI-path regression below.

## Findings against the mission criteria

1. **System-generated, non-secret UID and first-registration concurrency:** the domain package generates a UUIDv4 via `stableid` (`internal/environment/environment.go`). First-use registration uses the existing target-wide write lock and retries lock contention (`internal/deployment/environment_identity.go:119-130,141-190`); the goroutine test checks convergence for 32 callers (`internal/deployment/environment_identity_test.go:83-133`). This supports the creation/concurrency part of the criterion.

2. **Brownfield reuse:** the test named `TestGetEnvironmentReusesOnBrownfield` creates a new-format record and calls the same function again (`internal/deployment/environment_identity_test.go:55-81`). It does not model an existing legacy environment state or migration. The reader requires a valid `id` in `environment.json` (`environment_identity.go:59-73`), and no legacy-record migration is present in this diff. Reuse of a pre-existing UID in the actual older state format is therefore unproven and not implemented here.

3. **Rename stability:** the domain value's in-memory `Rename` preserves its ID (`internal/environment/environment.go`, test at `internal/environment/environment_test.go:75-92`), but the persistence seam has no rename operation. Storage is keyed by the environment name in the path (`environment_identity.go:34-56`); calling `GetEnvironment` under a new name allocates a new ID. The in-memory helper test does not establish durable rename stability. Blocking.

4. **Real CLI-entry tests:** this commit changes no `cmd/baha/**` file and contains no `runWithIO` or production-command test. All added tests call the domain or deployment helper directly. Blocking: the mission explicitly requires the real CLI entry point.

5. **Identity roles and no second registry:** the record has separate `Target`, `Name`, and `Identity` fields, and does not directly reuse a deployment ID. However, the implementation creates `targets/<target>/.baseharbor/environments/<env>/environment.json` outside the existing deployment namespace (`environment_identity.go:34-56`) and treats that new file as the durable source of truth. That conflicts with the mission's owner constraint that UID be an attribute of the existing `(target, environment)` state, with no second registry. Additionally, persistence serializes `Name: id` rather than the environment name at `environment_identity.go:80-86`; the returned record also sets `Name` to the ID (`:113-116`). This conflates the human-readable environment selector with its UID. Blocking.

6. **Hosted run:** satisfied for exact requested SHA, as recorded above.

7. **File ownership:** satisfied for this candidate diff. The only changed paths are the internal environment identity/domain implementation and its dedicated tests; there are no app/target CLI implementation files and no `.github/**` edits.

## Correction recipe

Persist the UID as a field of the canonical existing `(target, environment)` state rather than adding a second authoritative registry. Keep the environment name distinct from the UID in all serialized and returned records. Add a persistence-level rename operation that updates the selector while preserving the ID, and add a genuine legacy-state fixture/migration proving an existing ID is reused without regeneration. Add production CLI-entry regression tests that exercise create/reopen/rename from the public command path, then map those tests to the existing CLI Go CI shards. Preserve the target-wide lock path for concurrent first registration and prove the existing record is reused under contention.

## Verdict

REJECT `670402fdefc57440a144365fce672b909a661228` for blocking gaps in rename persistence, legacy reuse proof, real CLI-path coverage, the second-registry design, and name/UID serialization. The hosted run passed but does not waive these acceptance failures. The live PR head is `7930095b04ae716fe2375ee8f6a578535990eec2`; this report makes no assertion about that later candidate. PR remains draft; no CI rerun or PR operation was initiated.

## repo-rule compliance

The planning repository is the actual `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, verified before any evidence commit with:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Review source came from a fresh product clone and live GitHub refs, not the quarantined stale-ref checkout. This was read-only review work: no product changes, workflow changes, local tests, containers, run dispatch, rerun, merge, or PR update.

Planning validation: `python3 scripts/plan.py check` reported 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors and 12 warnings. The task-specific warnings are that `t-20261114-r28-cli2-uid-environment` is in review although `t-20261114-r28-cli2-uid-app` is not accepted, and its dependent `t-20261114-r28-cli2-uid-target` is active although this task is not accepted.

Planning `origin/main` exact `git ls-remote` witness immediately before the evidence commit:

```text
ad8123972f47b4111465522184d25a80958acc60	refs/heads/main
```

## END DONE
