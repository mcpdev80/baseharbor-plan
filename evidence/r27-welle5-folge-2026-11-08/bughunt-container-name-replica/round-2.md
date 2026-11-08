# 0427-128 r2 — gofmt correction on PR #1452

Lane: mission-128-r2.md (0427-128 r2 KORREKTURRUNDE, formal only)
Candidate: PR #1452 branch `bughunt/0427-128-container-name-replica`, head `978503376c34e447fc0f82451c35b43fb9fa8fd5`
Task: `t-20261108-bughunt-0427-container-name-replica` (card 0427-128)

## PLAN

1. Verify PR #1452 head and branch name via `gh pr view 1452`.
2. Use the existing 128-lane worktree `/tmp/opencode/0427-128-contname-wt` on the candidate branch (same chain, no new branch).
3. Ensure `internal/runtime/container_identity_test.go` is gofmt-clean; `gofmt -l` empty on all diff-touched files.
4. Drift check against current `origin/develop` head.
5. Push only if a correction commit is needed (normal follow-up, no rebase/force).
6. Observe the PR run to terminal state (self-run duty AGENTS 4.6).
7. Evidence in baseharbor-plan on origin/main, END post.

## Reality witnesses

Planning repo verification (before first evidence commit):
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)`

Remote refs fetched fresh via `git ls-remote` from the worktree's real product remote:

```text
978503376c34e447fc0f82451c35b43fb9fa8fd5	refs/heads/bughunt/0427-128-container-name-replica
e39b0004346cdfd082e34ba55d94d24757bbbd27	refs/heads/develop
```

`gh pr view 1452`: head `978503376…`, state OPEN, mergeable CLEAN/MERGEABLE.

- Base attestation: the chain descends from `develop` at `e39b0004346cdfd082e34ba55d94d24757bbbd27`; ancestry verified with `git merge-base --is-ancestor e39b00043 978503376` → OK. No second branch was created; work stays on the named candidate branch (AGENTS 3.8).
- Drift: `e39b00043` (current develop tip) is already merged into the branch at `c551fcd01`. No further merge needed.
- Diff files `git diff e39b00043...978503376 --name-only`:

```text
internal/runtime/container_identity.go
internal/runtime/container_identity_test.go
internal/runtime/service_stop.go
```

- Log line `git log --oneline origin/develop..HEAD`:

```text
978503376 style(runtime): gofmt container_identity_test.go
c551fcd01 Merge remote-tracking branch 'origin/develop' into bughunt/0427-128-container-name-replica
a96b4e218 fix(runtime): accept pinned container_name in quiesce identity check
```

## State at lane start (attribution)

The mission's required correction — the normal follow-up commit `978503376`
("style(runtime): gofmt container_identity_test.go", author identity
`0427-maintenance-r3`, timestamped before this session began) — had already
landed on the same candidate branch when this lane started. This lane therefore
performed full independent verification of the correction rather than creating a
duplicate commit or a competing candidate (one candidate per chain).
`978503376` is not this session's work; it is the chain's own follow-up.

## Format verification (bitwise, neutral path)

- Fetched the file blob for both heads via the GitHub API
  (`/repos/mcpdev80/baseharbor/contents/internal/runtime/container_identity_test.go?ref=<sha>`).
- `c551fcd01` blob: git object `673eb2a8e7d9ba2ea9478520de62e9b4a9ed6a88`, sha256 `f87b25f136fd7d4f…` → `gofmt -l` lists it (misaligned struct-literal fields, trailing blank line). This is the file act-1452-review.md flagged.
- `978503376` blob: git object `3d16979daf909046ad3c728d58216c325bf027ae`, sha256 `53abba123b01d4ab5e90f7094bf12ef592f34c9f611701d0bb9dedfae3f2dad7` → `gofmt -l` clean.
- Running `gofmt` on the exact `c551fcd01` content reproduces the `978503376` content byte-for-byte (identical sha256). The style commit touches ONLY `container_identity_test.go` (10 insertions / 11 deletions, whitespace only); `container_identity.go` and `service_stop.go` are untouched by it and remain gofmt-clean.
- Local checks on head: `go build ./...` OK; `go test ./internal/runtime/ -run 'Quiesce|Identity' -count=1` → ok (go1.26.8 host toolchain).

## Hosted CI (observed to terminal, AGENTS 4.6)

Exact head `978503376c34e447fc0f82451c35b43fb9fa8fd5`, run `42440204879` (started by the normal PR push; no manual rerun or dispatch). This session watched it from pending to the terminal state (`gh run watch`, then `gh run view` / `gh pr checks`):

```text
Workflow policy                pass
PR · Source format             pass   <- the gate that failed at c551fcd01
PR · Trusted Plan              pass
PR Selected Checks             pass   <- also failing in the review STATE, now pass
PR · Focused Python            pass
PR · Validation · cli-build    pass
PR · Validation · cli-guided-tests           pass
PR · Validation · cli-vet                    pass
PR · Validation · runtime-provider-package-tests pass
PR · Validation · source-contracts           pass
```

Unrelated matrix cells (Targeted HA docker/podman, validate, Release Source
Preflight, Demo Pin, Exact Candidate, Consumer Pins, Runner Interface, Public
Contracts, Selected Runtime, Native Keycloak/Core) report `skipping` for this
head, as expected for selected checks. Run conclusion: `success`.

The review's stop criterion (act-1452-review.md: terminal green `PR · Source
format` and `PR Selected Checks` on the exact new head) is met at `978503376`;
the suspended content review can resume against this head.

## CI pickup for tests

No new tests this round. `internal/runtime/container_identity_test.go` is
covered by GitHub CI through existing selection: the `source_format` job
(`PR · Source format`, `.github/workflows/ci.yml`, trigger: `pull_request`
against `develop`) runs `gofmt -l` over diff-touched `.go` files, and the Go
test group runs it inside `PR · Validation` jobs. No `.github/**` change needed.

## repo-rule compliance

- Scope: format-only per mission ("KEINE inhaltlichen aenderungen — nur format"). Zero product-repo edits and zero pushes by this session; verification of the existing chain follow-up.
- No `.github/**` edits; no reruns, no workflow_dispatch.
- No subagents (AGENTS 4.8); all steps in this session.
- No containers/compose projects started (no VM smoke named in this mission); nothing to bring down.
- Evidence lives only in baseharbor-plan (no `.evidence/`, no product-repo planning acts).
- Observation (left untouched, other lanes' work): uncommitted modification of `evidence/.../bughunt-test-bootstrap-leak/round-1.md` present in the shared planning checkout at lane start; untracked `conformance/provider/v1/testdata/external/go.sum` present in the shared product worktree.
- This file previously held a parallel r2 record from another session on the same mission; that content is preserved in this file's git history.

END_DONE mission-128-r2.md: verified; PR #1452 head 978503376c34e447fc0f82451c35b43fb9fa8fd5 gofmt-clean, `PR · Source format` + `PR Selected Checks` terminal green in run 42440204879; no duplicate commit by this lane (see attribution).
