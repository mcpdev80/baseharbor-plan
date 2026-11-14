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

## PLAN (r2 review)

1. Verify the exact r2 candidate, retargeted app-branch base, ancestry, own-commit log, live PR state, and exact hosted run.
2. Review identity creation, lock behavior, legacy reuse, durable rename, CLI-entry coverage, identity-role separation, and path ownership against the contract.
3. Record a SHA-specific independent review verdict and actionable findings in the planning evidence.
4. Run planning validation, publish the updated evidence to origin/main, verify its remote presence, and post END.

## R2 review — candidate 7930095b

Review role: CODEX-REVIEW only; no merge. Exact requested candidate `7930095b04ae716fe2375ee8f6a578535990eec2`, branch `lane-0428-uid-environment`, PR #1578, OPEN/DRAFT. `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-uid-app refs/pull/1578/head refs/pull/1579/head` returned:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
2bf0c929506a5b0e64b7359a6fc8711ab3f48526	refs/heads/lane-0428-uid-app
7930095b04ae716fe2375ee8f6a578535990eec2	refs/pull/1578/head
2bf0c929506a5b0e64b7359a6fc8711ab3f48526	refs/pull/1579/head
```

The declared PR base is `lane-0428-uid-app` at `2bf0c929506a5b0e64b7359a6fc8711ab3f48526`. `git merge-base --is-ancestor 2bf0c929506a5b0e64b7359a6fc8711ab3f48526 7930095b04ae716fe2375ee8f6a578535990eec2` failed (exit 1); their merge-base is `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`. The candidate's log from develop lists only its two lane-owned commits, `670402fd` and `7930095b`. The app branch is PR #1579 head `2bf0c929`, OPEN/DRAFT; its active checks on run `43651708694` passed, but Planning still lists the uid-app dependency as not accepted.

Combined-chain inspection: the app branch contributes `cmd/baha/app_init_uid_app_slice_test.go`; #1578 contributes `cmd/baha/environment_identity_cli_test.go`, `internal/deployment/environment_identity.go` and its tests, and `internal/environment/environment.go` and its tests. A local merge-tree of the fetched app base and exact #1578 head completed without conflicts (tree `10f4fcd9e884315b19886b13d702fa74de0c5bd7`). The app base is nevertheless not an ancestor of #1578, so the candidate is not structurally based on the declared stack head. No files overlap between the two PR diffs.

### Criteria review

1. UUIDv4 generation is non-secret, and first use is idempotent under the shared target registry lock; the candidate has a 32-goroutine convergence test. The creation/locking portion is supported by source and tests.

2. Reopening a valid `environment.json` returns its stored identity. The brownfield test reopens a record created by this same new implementation; the combined diff has no migration from the pre-existing environment state to this newly introduced record. Card acceptance explicitly includes migration and reuse of historical identity, which remains unproven.

3. R2 adds persisted `RenameEnvironment` and a test reopening under the new name with the same UUID (`internal/deployment/environment_identity.go:246-383`; test `:216-274`). The seam-level rename behavior passes by inspection. The CLI test does not invoke rename through the CLI itself, as detailed below.

4. The added test calls `runWithIO` for `target show --json` (`cmd/baha/environment_identity_cli_test.go:61-83`), but the command itself does not call the environment identity seam. `GetEnvironment`, `RenameEnvironment`, and `EnvironmentID` are called directly by the test before or after the command (`:55-58,85-109,119-130`); source search finds no production caller of those methods. The CLI assertion checks target output and target state root, not an environment UID. This is a helper-path test wrapped around a real but unrelated CLI command, not a real CLI-entry regression for the UID feature. Blocking.

5. The candidate does keep `EnvironmentRecord.Identity` distinct from deployment IDs. However, the owner rule forbids a second registry: the implementation creates a new authoritative per-name file at `targets/<target>/.baseharbor/environments/<env>/environment.json` (`internal/deployment/environment_identity.go:41-63`) and tests that it is outside the deployment registry (`internal/deployment/environment_identity_test.go:136-156`). This is a separate environment identity store, not a UID attribute on the existing canonical `(target, environment)` state. Also, `readEnvironmentRecord(path)` validates that stored target/name are non-empty and syntactically valid but does not compare them with the requested target/name (`environment_identity.go:66-98,161-168`). A valid record copied under a different target or environment path can therefore return an identity bound to another environment, contrary to the role-separation and no-cross-tenant-mixing requirement. The current corrupt-binding test covers only an empty target (`environment_identity_test.go:332-350`), not a valid mismatched binding. Finally, `RenameEnvironment` writes the new path with `os.Rename` without first rejecting an existing destination record (`:341-375`). On systems where rename replaces an existing file, renaming one environment over an already registered name overwrites that environment's UID. There is no regression test for a conflicting destination. Blocking.

6. Hosted run `43647672376` is terminal `completed/success`, event `pull_request`, workflow `CI · Source & Quality`, exact head `7930095b04ae716fe2375ee8f6a578535990eec2`. Active jobs `PR · Draft source and routing`, `PR · Draft Go · cli-0/1/2/3`, and `PR · Draft Go · packages` passed; other jobs were skipped under draft selection. The run was created `2026-11-14T22:21:34Z`, before the retargeted PR update at `2026-11-14T23:08:58Z`; it proves the exact source SHA passed, not the combined app-base candidate. No rerun was requested or triggered.

7. The combined change paths are limited to the app UID test in the app lane and the environment package/seam plus dedicated tests in this lane. No application or target implementation paths and no `.github/**` paths changed. Path ownership is respected, although the active candidate still lacks the designated base ancestry.

### Required correction recipe

Keep one PR/branch and rebase that same candidate onto the exact current designated app-lane head under the stack directive. Store the environment UID as an attribute of the canonical existing `(target, environment)` state; do not introduce a second authoritative registry. On read, validate that stored target and name exactly match the requested binding/path and reject mismatches. Reject a rename when its destination already belongs to a different environment; never overwrite that record. Add a legacy-state migration/reuse fixture. Wire the identity operation into the relevant production CLI command and make the `runWithIO` regression assert UID creation, reopen and rename through that actual command path, without direct calls to the seam standing in for CLI behavior. Then obtain terminal CI for the exact candidate with the app base in place; the existing CI grouping is `PR · Draft Go · cli-0/1/2/3` and `PR · Draft Go · packages`, triggered by `pull_request`.

### Verdict

REJECT exact candidate `7930095b04ae716fe2375ee8f6a578535990eec2`. Blocking findings: separate identity store conflicts with the explicit no-second-registry design; target/name bindings are not checked against the requested path; rename can overwrite an existing destination UID; the alleged CLI regression never exercises the UID via the CLI; legacy-state migration/reuse is not demonstrated; and the candidate is not based on the current declared app-branch head. The exact-SHA hosted run passed, but it predates the retarget and does not cure these findings. PR #1578 remains DRAFT; no PR action was taken.

## R2 repo-rule compliance

Planning root verification before the R2 evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

The prior review worktree `/tmp/opencode/mission-rev1578-wt` already existed; it was not extended. This round used a fresh clone at `/tmp/opencode/mission-rev1578-r2-wt`. No product source was changed, no local tests or containers were run, and no workflow, rerun, dispatch, merge, or PR update was made. At initial inspection, `git status` showed `evidence/cli-redesign-20261114/cli2-uid-app/round-1.md` modified; it was never staged or edited by this review, and it was clean at final pre-publication status. Planning validation and the exact main witness are recorded below.

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` reported 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors and 12 warnings. The task-specific warnings are that this environment task is in review while its uid-app dependency is not accepted, and the dependent uid-target task is active although this task is not accepted. The mission-listed separate `cli2-uid-environment/round-2.md` file is absent on current planning main; the r2 correction report is embedded in the `Round-2 correction` section of `round-1.md`.

Planning `origin/main` exact `git ls-remote` witness before the R2 evidence commit:

```text
ee055ada1b2a7b670d0f50964bdaa0c9fb8a956a	refs/heads/main
```

## END DONE (r2 review)
