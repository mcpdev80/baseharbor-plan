# 0427-119 — OCI pull error propagation (verify, round 1)

Lane: `lane-0427-119-oci-pull-error` (session 27494182, laptop). Card `t-20261107-oci-pull-error-propagation`, release `v0.4.27`.

Purpose of this round: verify that the already-merged PR #1434 actually satisfies the card's acceptance criteria, and record the process state for an Owner decision.

## FINDING: task is already CLOSED with truthful acceptance

The card is in state `accepted` / `kanban_status: closed`, set by Owner commit `f78bb724c91ab8a7bd8d04b0086e60c8c9497434` ("accept 0427-119 against merged PR 1434 and exact CI"). The card was **not** `active` when this lane started — the code is already integrated. No worker implementation, claim, or second candidate is in scope here.

Verified remote truth (via `git ls-remote` + GitHub API on `mcpdev80/baseharbor`, not the quarantined workers checkout):

- PR `mcpdev80/baseharbor#1434` `fix/0427-119-oci-pull-errors`, head `4808a20e1308758a5b1df02ec602bb33a6250f3e`, base `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- `git merge-base --is-ancestor 4808a20e 8a3f58da` → **YES**. PR head is an ancestor of develop → PR is merged.
- Merge commit `8a3f58da905fad52327d33466fde1d9568092519` (Merge PR #1434 from `fix/0427-119-oci-pull-errors`), merged by Owner, `2026-11-07T17:38:12Z`.
- Base `06e4b1eaa` is the exact SHA the mission required as basis; nothing on develop after the merge commit.

## Candidate SHA lineage (proof)

```
git merge-base --is-ancestor 4808a20e... 8a3f58da...  # YES (PR head is ancestor of develop HEAD 8a3f58da)
```

- `06e4b1ea` — required basis / PR base (equals mission base `06e4b1eaa`).
- `4808a20e` — PR #1434 head (candidate), ancestor of develop.
- `8a3f58da` — merge commit into `develop` (terminal candidate).

Only these commits sit between base and merge:

```
72613860 fix(oci): classify native pull errors without leaking stderr
ccb17409 refactor(oci): expose shared redacted native-tool classifier
bbb388d2 test(oci): assert pull missing-tool identity and stderr redaction
4808a20e style(oci): gofmt regression test struct fields
```

No foreign candidate carried on top. The integration candidate for this chain is `8a3f58da`.

## Acceptance criteria — all satisfied by the exact merged code (`8a3f58da`)

1. Same classifier as `oras resolve`: `cmd/baha/application_registry_source.go` `pullResolvedRuntimeImage` now calls `orgconfig.ClassifyNativeToolFailure("oras", err)` — the same helper `Resolve` uses. Shared classifier, not a divergent inline check.
2. Missing-binary identity preserved through the chain: `ErrRegistryNativeToolMissing = fmt.Errorf("%w: %w: ... 'oras' is not installed ...", ErrRegistrySourceUnavailable, exec.ErrNotFound)` → `errors.Is(err, exec.ErrNotFound)` holds.
3. Other pull failures not misclassified: `ClassifyNativeToolFailure` returns `ErrNativeToolNotFound` only via `IsNativeToolNotFound(err)`; otherwise a redacted generic-unavailable error. Test asserts `errors.Is(err, exec.ErrNotFound)` is **false** for a registry auth error and a non-zero-exit error.
4. No sensitive output leaked: test injects `secret = "very-sensitive-registry-token"` into registry/auth and exit-7 failures and asserts `strings.Contains(err.Error(), secret)` is false; the classifier returns only a sanitized class, never raw stderr.
5. One targeted regression test on the real pull path: `cmd/baha/application_registry_pull_error_test.go::TestApplicationRegistrySourcePullErrorClassification`, exercising the real `pullResolvedRuntimeImage` with a fake `RuntimeProvider` (no live runtime).

Write-set of the PR (exactly the mission's allowed files; no `.github/**`, no security-contract change):

```
cmd/baha/application_registry_pull_error_test.go   (new)
cmd/baha/application_registry_source.go            (+10 / -1)
internal/orgconfig/source_oci.go                   (+6)
```

## Evidence execution (CI)

Hosted run `42396424816` ("CI · PR #1434") — conclusion **success** (terminal), head_sha `4808a20e`, event `pull_request`:

```
Job                              | status   | conclusion
---------------------------------|----------|-----------
PR · Selected Checks             | completed| success
PR · Validation · go-unit-tests  | completed| success
PR · Validation · go-build       | completed| success
PR · Validation · go-vet         | completed| success
PR · Focused Python              | completed| success
PR · Source format               | completed| success
PR · Trusted Plan                | completed| success
Workflow policy                  | completed| success
Targeted HA · podman             | completed| skipped   (normal path selection, not required for pure error-classification change)
Targeted HA · docker             | completed| skipped
PR · Exact Candidate             | completed| skipped
PR · Consumer Pins               | completed| skipped
```

`go-unit-tests` runs the complete `cmd/baha` suite (which includes `TestApplicationRegistrySourcePullErrorClassification`) plus `internal/orgconfig`. No new CI trigger is required: the new test is covered by the existing `go test ./cmd/baha` / `./internal/orgconfig` unit checks that already ran and passed on the exact candidate. No `.github/**` change.

## Process observation (non-blocking, for the Owner)

- The PR was merged and the card accepted with **zero CODEX-REVIEW** (0 reviews, 0 review comments on #1434). This is a process deviation from the task's required-checks protocol (a CODEX-REVIEW verdict is the normal acceptance artifact). The Owner accepted against a verified SHA lineage + a terminal green CI run, which is a legitimate alternative acceptance path per §5.2; the card's `resolution: accepted` + HTTPS evidence (`#1434`, CI `42396424816`) is truthful and complete.
- This lane is a **verification/hygiene** lane only. It made no product change, opened no second candidate, and changed no `.github/**`.

## Repo-rule compliance

- Remote truth measured only via `git ls-remote` + GitHub API against `mcpdev80/baseharbor`; the quarantined workers checkout was never cited.
- No product-repo writes, no second candidate, no `.github/**` touch, no security-contract diff.
- No subagents (§4.8). Every step run in this session.

## END

Lane ended. Task already Owner-closed with truthful acceptance; no worker implementation or claim possible (card is at `accepted`, not `active`). Reporting the merged candidate and the zero-review process observation for the Owner.

## PLAN

- Read mission + card contract word-for-word; identify exact scope.
- Measure remote truth via `git ls-remote` + GitHub API; confirm PR #1434 state.
- Confirm PR #1434 merged into develop (base `06e4b1eaa`, head `4808a20e`), terminal CI `42396424816` success.
- Verify all 5 acceptance criteria against the exact merged develop code.
- Document the merged SHA lineage (ancestor proof) and write-set.
- Note the zero-CODEX-REVIEW process observation as an Owner decision item.
- Report to Owner; no further action required unless Owner asks for a follow-up.

## Status

END_BLOCKED — task already Owner-closed with truthful acceptance (merged candidate `8a3f58da`). No worker work remains. Reporting merged candidate and the zero-review process observation for the Owner.
