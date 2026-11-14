# PR #1580 Review R1

## PLAN

1. Read task contract and verify exact PR #1580 candidate, base, provenance, and hosted run.
2. Review target UID generation/migration, collisions, data and ownership boundaries, ID roles, CLI-entry tests, and changed paths.
3. Record exact-SHA verdict and actionable correction recipe in planning evidence.
4. Validate and publish evidence to planning origin/main, verify remote presence, and post END.

ROLLE: CODEX-REVIEW. Read-only review; no merge.

## Candidate and provenance

- PR #1580 is OPEN/DRAFT, base `develop`, head branch `lane-0428-uid-target`, candidate `ebeafa56a2d14d962603cbc649e4764628104417`.
- Exact `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1580/head` output:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
ebeafa56a2d14d962603cbc649e4764628104417	refs/pull/1580/head
```

- `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c ebeafa56a2d14d962603cbc649e4764628104417`: exit 0.
- `git log --format='%H %an <%ae> %s' 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..ebeafa56a2d14d962603cbc649e4764628104417` lists only the task commit: `ebeafa56a2d14d962603cbc649e4764628104417 lane-0428-uid-target <dev@pfingstgraef.eu> feat(r28): stable target UID without runtime-ownership change (0428-052)`.
- Fresh clone `/tmp/opencode/mission-rev1580-review` was checked out detached at the exact candidate. The diff is seven files, all target-related: `internal/deployment/target_id.go`, its tests, target config/recovery, and the `cmd/baha` target creation/list paths and dedicated tests. No application or environment paths are changed. No on-disk Target data path is relocated by this diff; state remains name-keyed. `git diff --check` is clean.
- Planning task `t-20261114-r28-cli2-uid-target` is in review and depends on accepted `t-20261114-r28-cli2-contract`. Contract §6 defines Target identity as a Core-side UUID, separate from workstation alias and deployment IDs. Owner instruction for this review additionally requires it remain separate from the `TenantID` ownership binding.

## Review findings

BLOCKER — Existing target definitions are not migrated on read or persisted idempotently. `TargetDefinition` says an empty UID marks a pre-identity target that “migrates idempotently on read” (`internal/deployment/target.go:52-60`), but `Config.ResolveTarget` copies `target.TargetUID` directly into `ResolvedTarget.UID` (`target.go:347-384`), and `baha target list` copies the field directly (`cmd/baha/target.go:219-243`). Both return an empty UID for legacy config. `MigrateTargetUID` is called only by the new-target create path (`cmd/baha/target_mutation.go:97-113`); it returns a generated value without persisting a legacy definition. `ResolveTargetUIDs` also generates temporary values for empty definitions, but does not update or save the config. Repeated resolution of the same legacy definition therefore does not yield a stable persisted UID.

BLOCKER — The tests do not enter through the real CLI command. `cmd/baha/target_uid_cli_test.go:22-28,64-65,94-105` calls `createTargetDefinition` directly with `machineTargetCreateInput`; it does not execute the `baha target create` command parser/dispatch path. Its “idempotent retry” passes an explicit UID into the helper, while the user-facing create command does not accept a UID option. The collision case likewise tests the helper directly. This does not satisfy the mission's “real CLI entry, no helper trick” criterion.

PASS — The UID is generated as UUIDv4, stored in `TargetDefinition.TargetUID` (`yaml:"target-uid"`, `json:"target_uid"`), and surfaced separately as `ResolvedTarget.UID`/target-list `uid`. `TenantID` remains a separate `tenant-id` / `tenant_id` field and remains the field used by the existing ownership path; the mutation builds both fields separately (`cmd/baha/target_mutation.go:111-118`). Deployment IDs are not changed or reused. Target names remain config keys and resolution selectors. The changed paths stay within the target owner's slice; no app/environment files were changed.

GAP — Rename preservation is plausible when a TargetDefinition is moved under a new config key because the UID is a field on the definition and state paths stay name-keyed, but no rename operation or regression test in this diff proves it. Likewise, type tags separate UID from TenantID and deployment IDs, but there is no serialization-level test asserting the three distinct roles survive config/recovery/list round trips. These should be covered with the migration and CLI regression work before acceptance.

Correction recipe: implement the legacy name-to-UID migration at the config resolution/persistence seam. Generate only for missing UIDs, validate the full post-migration config for collisions, then atomically persist the same UID while leaving target names and data directories unchanged. Preserve `TenantID` and deployment IDs as separate values and paths. Add tests that invoke the actual `baha target` command with a legacy config, resolve/list twice and verify the same UID persists, rename the config entry and verify UID retention without moving data, and submit a colliding UID through the actual CLI to verify fail-closed behavior and no partial write. Assert serialized config/recovery/list fields maintain the UID/TenantID/deployment-ID separation. Keep the PR draft until those tests pass in the normal CI group.

## Hosted run

- Run `43647367175` completed with conclusion `success` on exact candidate `ebeafa56a2d14d962603cbc649e4764628104417`, event `pull_request`, workflow `CI · Source & Quality`.
- All active jobs passed: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages`.
- `PR Selected Checks`, workflow policy, source format, validation, and other non-draft/native jobs were skipped under draft selection. This is a successful terminal draft run; skipped checks are not reported as passing.
- CI selection was verified read-only in `.github/workflows/ci.yml`: `pull_request` includes `develop` (`:12-16`); draft Go shards run for draft PRs (`:1400-1405`); changed Go package selection feeds the CLI shards and package test group (`:1435-1487`). `scripts/pr-go-unit-shard.py:28-40,64-115` discovers and executes the actual `cmd/baha` test inventory. The PR run passed CLI shard summaries: cli-0 409 passed, cli-1 403, cli-2 407, cli-3 396; package group ran `go test -p 1` for `./internal/deployment`, which passed. The three new CLI-package test names hash to cli-0 (`TestCreateTargetPersistsStableUID`) and cli-3 (`TestCreateTargetUIDIdempotentOnRetry`, `TestCreateTargetRejectsUIDCollisionByName`); they are present in the shard inventory. This confirms CI picks up the tests despite the helper-level nature of their assertions.
- No workflow change, rerun, or workflow dispatch was made.

## Repo-rule compliance

- Evidence repository root verified before this evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (`git rev-parse --show-toplevel`).
- Planning repo was fast-forward refreshed before evidence recording; exact evidence base SHA: `ceb9b9cb4c7d43ab7c245b5e0b8eec568114a5b5`.
- Exact `git ls-remote origin main` output immediately before evidence publication:

```text
ceb9b9cb4c7d43ab7c245b5e0b8eec568114a5b5	refs/heads/main
```

- Only this review evidence file is intended for the planning commit. No product or workflow files were modified.
- `python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 10 pre-existing dependency warnings.

## Verdict

REJECT PR #1580 at `ebeafa56a2d14d962603cbc649e4764628104417` for the missing persisted legacy-target migration and tests that bypass the real CLI entry point. The generated UID field is distinct in code from TenantID and deployment identities, target names remain addressable, and no target data paths move; rename and serialized-role regression coverage remain missing. No merge.

END DONE — PR #1580 rejected; review evidence to be published on planning origin/main.
