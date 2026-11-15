# PLAN — t-20261114-r28-cli2-env-registry (0428-054)

## Work plan (numbered)

1. Confirm reality: git ls-remote for baseharbor (base `3a91e2a8` = `refs/heads/lane-0428-uid-target`) and baseharbor-plan (origin/main). Record witnesses.
2. Claim the task centrally (plan.py claim) before any change; push a claim witness.
3. Create branch from base `3a91e2a8` in my own worktree; attest base SHA is ancestor of first commit.
4. Read accepted domain seam at base HEAD: `internal/environment/environment.go`, `internal/deployment/environment_identity.go`; read uid-app `app.id` manifest pattern; map current app/target/node association surface.
5. Implement authoritative Core registry: app/target/node association for shared environments (create/select/list/update), preserving Core source-vs-runtime authority, no name-inferred matching, fail-closed on unknown ownership.
6. Add focused tests for acceptance criteria (duplicate/conflict/permission, Core restart persistence, multiple nodes, shared apps) mapped to an existing CI check + trigger.
7. Run go build / go vet / go test at candidate SHA; record actual results.
8. Draft PR, base = `lane-0428-uid-target` (retarget), show base head ancestor + log witness (only own commits).
9. Write full akte (result, repo-rule compliance, witnesses).
10. Push evidence to origin/main; run `git log` witness; post END.

## BASE ATTESTATION

- Base product ref: `3a91e2a8362bc8028c8f4a7ef278f8c9d96df823` = `refs/heads/lane-0428-uid-target` (kette-oberkopf / chain head).
- PR base = that same branch (`lane-0428-uid-target`), NOT develop; retarget the PR to it.
- Will show `3a91e2a8` is an ancestor of first commit, and `git log` lists only own commits.

## REALITY WITNESSES (git ls-remote)

- baseharbor develop: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- baseharbor main: aff1532c2f6c6782a8c13afad83245d1351815e7
- baseharbor lane-0428-uid-target: 3a91e2a8362bc8028c8f4a7ef278f8c9d96df823 (matches mission)
- baseharbor-plan origin/main: e00377d6 (HEAD at start of shift)

## STACKING CHAIN (confirmed via plan.py + PRs)

- uid-app (#1579): app.id in versioned baseharbor.yaml — predecessor
- uid-environment (#1578): internal/environment + internal/deployment env identity seam — at base HEAD
- uid-target (#1580): stable target UID — at base HEAD
- env-registry (mine): authoritative Core registry + app/target/node association for shared environments

## SCOPE / WRITE-SET (strict)

- Own: new Core registry slice + app/target/node association + dedicated tests.
- environment.json / identity paths: READ-ONLY, do not restructure.
- Reserved to others: cmd/baha/commands.go, shared parser/machine registry, .github/**, release notes, generated indexes.
- Frost: NO merge.

## STOP CRITERIA

- If app/target/node association semantics are undecided or would require editing reserved files (commands.go, .github/**), STOP and post QUESTION with findings + exact needed change (file:line).
