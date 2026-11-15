# act-1585-review-r3.md — PR #1585 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15.

## PLAN

1. Verify PR #1585 head/base refs, candidate log/ancestry, exact-head run 43692224878.
2. Review-r3 points: guard completeness (store.go world-writable guard set + app-lane), fail-first (red on base, green on branch, no early-exit shortcut), unchanged test family, no new truth source.
3. Write APPROVE/REJECT with exact witnesses, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1585 OPEN/DRAFT, branch `lane-0428-fix-bf01-v2`, base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, exact head `13e096fc66d90e20b8f262b7f58024790c62b0e5`. Product `git ls-remote`:

```text
13e096fc66d90e20b8f262b7f58024790c62b0e5	refs/pull/1585/head
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

Base `0e9ccb582` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). Base-to-head log from develop contains only the candidate's own commit:

```text
13e096fc66d90e20b8f262b7f58024790c62b0e5 fix(cli): root-local organization default must resolve through the root's own selection
```

No foreign commit carried on top of the base.

## Review points

1. Guard completeness — `internal/orgconfig/store.go` at `13e096fc6` carries the world-writable guard set (18 guard symbols present: `worldWritableCheckOptOutEnv`, `isWorldWritableCandidate`, `privateFallbackPath`, `StateRootSelected`, `selectsWithin`, and the BF-03 lineage symbols the #1582 tests reference). The #1582 world-writable selection guard is carried across the state-root chain per round-4.
2. Fail-first — red on base, green on branch. The regression `cmd/baha/target_selection_state_dir_isolation_test.go` drives the root-local resolver (parts 4, 6: fail-closed naming B's own registrations / a non-existent registration; no ambient shortcut). On base `0e9ccb582` the resolver answers B's target without a B-local selection; on `13e096fc6` it fails closed. The test path goes through `resolveTargetBelowStateRoot` / `StateRootSelected` — no early-exit shortcut remains.
3. Test family unchanged in scope — single new isolation test file added; no new truth source introduced (state root remains the single source via persisted `active-target` under the state root).
4. CI — exact-headed `pull_request` run 43692224878, head `13e096fc6`:

```json
{"conclusion":"success","databaseId":43692224878,"event":"pull_request","headSha":"13e096fc66d90e20b8f262b7f58024790c62b0e5","status":"completed","workflowName":"CI · Source & Quality"}
```

No rerun or workflow_dispatch initiated. No failing or cancelled check observed.

## Verdict

APPROVE #1585 at `13e096fc66d90e20b8f262b7f58024790c62b0e5`. Guard set carried through the state-root chain (no #1582 symbol dropped), fail-first proven (red on base, green on branch, no early-exit shortcut), test family in scope, CI success on exact head. No product code, workflow, CI, container or VM changed. PR #1585 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-rev1585-r3 DONE — APPROVE #1585 at 13e096fc66d90e20b8f262b7f58024790c62b0e5

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
5e91f65f518cfbd0da68c996c8069c7c8d9b8cd5	refs/heads/main
```
