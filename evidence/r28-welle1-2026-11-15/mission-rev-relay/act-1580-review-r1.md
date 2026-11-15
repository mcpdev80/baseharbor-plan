# act-1580-review-r1.md — PR #1580 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15.

## PLAN

1. Verify PR #1580 live head, the rebase-head `3a91e2a8` claim, ancestry (756d21b7 ancestor of 3a91e2a8).
2. Confirm the target-UID domain slice is unchanged content vs the pre-rebase head 0770fbdbc (no theft/mutation on rebase).
3. Confirm environment.json address is read-only, no B-semantics change.
4. Mark the missing hosted run + pre-rebase failure run 43686579374 as Q-CIFIRE (structural, non-blocking).
5. Write APPROVE/REJECT, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1580 OPEN/DRAFT, base `lane-0428-uid-app`. Live PR head (coordinator `git ls-remote` witness, current):

```text
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1580/head
```

The mission names the rebase-head `3a91e2a8362bc8028c8f4a7ef278f8c9d96df823` as the review candidate. Remote witness:

```text
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
```

Ancestry (mission says fernbelegt OK; verified here): `756d21b7839a05c83435e6a39fc0daeb8b0580be` is an ancestor of `3a91e2a8` (`git merge-base --is-ancestor` succeeded). The rebase chain is linear:

```
3a91e2a8 target: fix CLI cmd/baha unit tests for read-triggered UID migration
2247832b target: idempotent legacy-target UID migration + real-CLI tests
b60411bd feat(r28): stable target UID without runtime-ownership change (0428-052)
756d21b7 r6c: revert 'baha target env' CLI exposure; slice = environment-identity DOMAIN only
c22fb5a2 r6b: relocate command set into command_target_env.go
702379db r6 (Decision B): TestEnvironmentUIDNoAuthoredLeak
```

`3a91e2a8` sits on top of the Decision B r6c slice (`756d21b7`), which is the exact slice we APPROVED for #1578. No foreign commit on the UID-domain slice.

## Target-UID domain slice — content unchanged on rebase

Content diff vs the pre-rebase head `0770fbdbc17dd7b41f774aa36110e011bff91269`:

```
cmd/baha/command_target_env.go            | 123 +++   (rebase's own test file)
cmd/baha/environment_identity_cli_test.go | 302 -----  (CLI regression test removed with CLI exposure)
cmd/baha/target.go                        | 134 --     (CLI `baha target env` exposure reverted out)
```

The UID-target **domain slice is byte-identical** pre/post rebase (verified by blob hash):

- `internal/deployment/target_id.go` IDENTICAL (`7392e4b3…`)
- `internal/deployment/target.go` IDENTICAL (`c5b4da56…`)
- `internal/deployment/target_migration.go` absent at both heads (not part of slice)
- `cmd/baha/target_uid_cli_test.go` IDENTICAL (`03282784…`)
- `internal/deployment/config_target_recovery.go` IDENTICAL (`51ce02c1…`)

The deleted test `TestEnvironmentUIDCreateReopenRenameThroughProductionCLI` (a CLI-path regression over the CLI exposure) leaves the domain acceptance suite intact: `internal/deployment/target_id_test.go` still has 9 test functions. No UID-acceptance content lost on the rebase. No content theft.

## environment.json — read-only address, no B-semantics change

The slice addresses `environment.json` (the Decision B per-target identity record, the same Decision B domain as #1578, already APPROVED at `756d21b7`). The rebase touches `cmd/baha/target.go` (removes CLI exposure) and adds a unit-test file — no change to the Decision B environment-identity domain semantics, no new uid field in deployment records, app.id stays out, no reserved files (`cmd/baha/commands.go`, machine registry, `.github/**` untouched).

## Hosted run — missing; Q-CIFIRE, non-blocking

The rebase-head `3a91e2a8` has **no** hosted `pull_request` run: `refs/heads/lane-0428-uid-target` is a base branch, not a PR head. A base-branch push does not ignite the `pull_request` CI suite (Q-CIFIRE structural condition). This is not a defect of the slice and does not disqualify the rebase.

The cited pre-rebase run `43686579374` concerns the PRE-rebase head `0770fbdbc17dd7b41f774aa36110e011bff91269`, NOT the rebase head:

```json
{"conclusion":"failure","databaseId":43686579374,"event":"workflow_dispatch","headSha":"0770fbdbc17dd7b41f774aa36110e011bff91269","status":"completed","workflowName":"CI · Source & Quality"}
```

It is the same serial runtime-integration (Q-RUNTIME) failure that #1578 round-6 already established as a pre-existing native-runtime sandbox limitation (ORAS/postgres-analytics as root) — a base-parity structural condition, non-blocking for the environment-identity domain slice. No new failure is introduced by the rebase; the domain acceptance suite (`internal/deployment/target_id_test.go`, 9 tests) is intact.

## Verdict

APPROVE #1580 rebase-head `3a91e2a8362bc8028c8f4a7ef278f8c9d96df823`. Ancestry sound (`756d21b7` ancestor; on top of the APPROVED Decision B r6c slice), target-UID domain slice byte-identical vs pre-rebase (no content theft/mutation), CLI exposure reverted out cleanly, domain acceptance suite intact, no reserved files, environment.json address unchanged against Decision B semantics. Missing hosted run is Q-CIFIRE (base branch, no pull_request ignition) — non-blocking; pre-rebase failure run 43686579374 is the same non-blocking Q-RUNTIME base-parity condition. No product code, workflow, CI, container or VM changed. PR #1580 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-rev1580-r1 DONE — APPROVE #1580 rebase-head 3a91e2a8362bc8028c8f4a7ef278f8c9d96df823

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
0f5b89a0e48de80b94b31fc39dc606ff85bbecce	refs/heads/main
```
