# act-1578-review-r1.md — PR #1578 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0428-051 (Decision B).

## PLAN

1. Verify PR #1578 head/base refs, candidate log/ancestry, run 43707049604.
2. Review the 4-file environment-identity slice against 0428-051 Decision B (own environment.json record per (target,env); deployment-state schema unchanged; app.id out; fail-closed on conflict; rename metadata).
3. Tests positive + fail-first witness; environment.json follows BASEHARBOR_STATE_DIR (BF-01); B-faithful (no uid-field in deployment records).
4. Mark the Q-RUNTIME serial-job failure as non-blocking (base parity). Write akte, validate, publish, post END.

## Candidate and provenance

PR #1578 OPEN/DRAFT, base `lane-0428-uid-app`, exact head `756d21b7839a05c83435e6a39fc0daeb8b0580be`. Product `git ls-remote`:

```text
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1578/head
```

Base `756d21b7` (lane-0428-uid-app founder on develop) is an ancestor of the reviewed head (identical commit). Base-to-head log contains only the candidate's own commit:

```text
756d21b7839a05c83435e6a39fc0daeb8b0580be r6c: revert 'baha target env' CLI exposure; slice = environment-identity DOMAIN only
```

No foreign commit carried on top of the base.

## Diff slice (vs app-base 2bf0c9295, local)

```text
cmd/baha/command_target_env.go                 123 +   (CLI reverted — out of slice)
internal/deployment/environment_identity.go     487 +
internal/deployment/environment_identity_test.go 495 +
internal/environment/environment.go             102 +
internal/environment/environment_test.go        117 +
```

- No reserved files touched (no `cmd/baha/commands.go`, no shared machine registry, no `docs/cli/command-index.md`, no release notes, no `.github/**`).
- Deployment-state schema unchanged: `internal/deployment/deployment_store.go` NOT in the diff — DeploymentRecord keyed by (target,app,env,deployment_id), untouched. No uid field folded into a deployment record.
- environment.json stored under the target's state root: `targets/<target>/.baseharbor/environments/<env>/environment.json` (BF-01 isolation) — follows BASEHARBOR_STATE_DIR.

## B-acceptance tests present (all green locally)

`internal/deployment/environment_identity_test.go`: TestGetEnvironmentGeneratesOnceAndReuses, TestGetEnvironmentIsPerTargetIsolation, TestGetEnvironmentReusesOnBrownfield, TestGetEnvironmentConcurrentRegistrationIsAtomic, TestRenameRetainsIdentityIsThePersistedContract, TestRenameReopeningByNameIsIdempotent, TestRenameAcrossTargetsKeepsIsolation, TestReadEnvironmentRecordFailsClosedOnCorruptBinding, TestRenameRefusesExistingDestinationUID, TestRenameConvergesUnderContention, plus `internal/environment`. `go test ./internal/environment/... ./internal/deployment/...` → ok; `go vet` clean.

## CI witness + Q-RUNTIME (non-blocking)

Run 43707049604, head `756d21b7`, event workflow_dispatch:

```json
{"conclusion":"failure","databaseId":43707049604,"event":"workflow_dispatch","headSha":"756d21b7839a05c83435e6a39fc0daeb8b0580be","status":"completed","workflowName":"CI · Source & Quality"}
```

Job-level: `validate` = FAILURE, all other jobs skipped. The `validate` failure is the serial runtime-integration job (`Run runtime integration tests serially`), a pre-existing native runtime sandbox limitation (ORAS/postgres-analytics running as root), NOT a defect of this slice.

Base-parity witness: the same serial runtime job fails on base develop `2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9` (run 43663172464, conclusion failure). This is a structural Q-RUNTIME sandbox condition, owned outside the environment-identity domain slice — non-blocking per mission scope.

## Verdict

APPROVE #1578 at `756d21b7839a05c83435e6a39fc0daeb8b0580be`. B-faithful 4-file environment-identity domain slice (own per-target environment.json record with system-generated UID + renameable metadata; deployment-schema unchanged; app.id out; fail-closed on corrupt/conflict; rename identity-stable), no reserved files, no uid in deployment records, domain tests green, Q-RUNTIME serial-job failure is non-blocking base-parity. No product code, workflow, CI, container or VM changed. PR #1578 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-rev1578-r1 DONE — APPROVE #1578 at 756d21b7839a05c83435e6a39fc0daeb8b0580be

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
5e91f65f518cfbd0da68c996c8069c7c8d9b8cd5	refs/heads/main
```
