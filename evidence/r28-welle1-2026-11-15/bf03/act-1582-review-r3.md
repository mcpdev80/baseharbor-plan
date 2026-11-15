# PR #1582 Review R3 — BF-03

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base ancestry, branch refs, task commits, metadata, and run 43675072219.
2. Review diff fa3190eb..8730e29a7 for foreign-target symlink rejection and unchanged target assertions.
3. Verify exact 0700 directory and 0600 file permission-bit assertions and tombstone prevents repeat adoption after source and target removal.
4. Check no regression from r1 userConfigDir storage, write verdict and recipe, validate and publish evidence on origin/main.

## Candidate and provenance

PR #1582 is OPEN and DRAFT, base `develop`, head branch `lane-0428-fix-bf03`, exact candidate `8730e29a76b8455c6ad3570efcb197771aaed82c`. Direct remote refs:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
8730e29a76b8455c6ad3570efcb197771aaed82c	refs/heads/lane-0428-fix-bf03
8730e29a76b8455c6ad3570efcb197771aaed82c	refs/pull/1582/head
```

The fetched exact base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the candidate. `git log --format='%H %s' 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..8730e29a76b8455c6ad3570efcb197771aaed82c` lists only this task's commits:

```text
8730e29a76b8455c6ad3570efcb197771aaed82c fix(BF-03): durably enforce one-time migration; positive symlink + exact-mode tests
fa3190ebc968b6b2776fc6128afcc1d257df422c fix(BF-03): one-time migrate persisted selection off world-writable /tmp
c678cdd0a7385504be76d4acf927e47080e3db81 chore(BF-03): gofmt internal/orgconfig after world-writable fix
829d75bc9e710daebee62ad16710dd468db1fe13 fix(BF-03): persist target selection in private user state (not world-writable /tmp)
```

Planning repository root witness (`git rev-parse --show-toplevel`):

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Planning remote witness immediately before publication (`git ls-remote origin refs/heads/main`):

```text
3b146818e9e8e2a6ea352a9b32a37a286bc4c7c7	refs/heads/main
```

The exact requested delta `fa3190eb..8730e29a` changes only `internal/orgconfig/store.go` and `internal/orgconfig/orgconfig_test.go`. `git diff --check` passes.

## Review findings

Verdict: REJECT due to the frozen-marker missing-state behavior and absence of the requested deleted-source/deleted-target regression.

1. The positive symlink test is present and checks the foreign target stays unchanged. `TestWorldWritableMigrationRejectsForeignSymlink` (`internal/orgconfig/orgconfig_test.go:429-512`) places a symlink at the legacy selection, requires `LoadActive` to fail, and compares the foreign file's bytes and mode before and after. The static path is rejected by `os.Lstat` and the symlink mode check (`internal/orgconfig/store.go:156-171`). A TOCTOU caveat remains: the code uses `os.ReadFile(legacyPath)` after `Lstat`, so a replaceable legacy path can be swapped for a symlink between the two calls. Keep the no-follow guarantee through opening the file and validating the opened descriptor if the threat model includes concurrent writers to a non-sticky world-writable directory.

2. Exact mode assertions are now present. `TestWorldWritableMigrationAdoptsOnceThenFreezes` requires the canonical file `Perm() == 0o600` and canonical organization directory `Perm() == 0o700` (`orgconfig_test.go:377-389`); it also checks the frozen source is `0o400` when it remains present. This resolves the r2 test gap.

3. The private marker prevents the legacy path from being read again, but the missing-canonical path returns the wrong result. After successful migration, if `active.json` is deleted while `active.frozen.tombstone` remains, `LoadActiveOptional` sees the canonical read as not-exist, skips adoption because `canonicalMigrationFrozen(canonical)` is true, then falls through to `decodeActive(data)` with nil data (`internal/orgconfig/store.go:254-279`). That produces a JSON EOF error rather than `(zero,false,nil)`, so `LoadActive` does not return `ErrNotConfigured`. The required test that removes source and target after adoption is also absent: the only migration tests in this package are the ordinary subsequent-write test and the foreign-symlink test (`git grep` shows no test removing the canonical and legacy files or exercising the retained-marker case). Recipe: when the marker is present and canonical state is missing, return the normal not-configured result without touching the legacy path; add the requested regression that deletes the legacy source and canonical active file but leaves the private marker, then verifies no re-adoption and `ErrNotConfigured` semantics.

4. No regression drift from r1's storage location change: `configRoot` still honors `BASEHARBOR_STATE_DIR` and otherwise uses `os.UserConfigDir()` (`internal/orgconfig/store.go:46-54`); world-writable resolved roots continue to select the private home fallback (`store.go:105-118`). The diff does not alter BF-01 target-selection CLI logic.

## CI and validation

The exact run witness from `gh run view 43675072219 --json databaseId,status,conclusion,event,headSha,workflowName` is:

```json
{"conclusion":"success","databaseId":43675072219,"event":"pull_request","headSha":"8730e29a76b8455c6ad3570efcb197771aaed82c","status":"completed","workflowName":"CI · Source & Quality"}
```

The round-4 handoff lists the `PR · Draft Go · packages` job successful on this exact head; `PR · Native impact selection` was skipped because the draft diff did not request native/runtime impact. This read-only review did not run local tests or trigger workflows. The CI success does not cover the missing retained-marker/deleted-state assertion because no such regression test is present in the candidate.

## repo-rule compliance

Read-only review in a fresh clone at the exact PR head. No product or workflow files, PR metadata, tests, containers, or VMs were changed or run. No merge or cherry-pick was performed. Evidence is stored only in the actual `baseharbor-plan` repository.

END mission-rev1582-r3.md DONE — REJECT; marker-state behavior and its required regression test remain open on candidate `8730e29a76b8455c6ad3570efcb197771aaed82c`.
