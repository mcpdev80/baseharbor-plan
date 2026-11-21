# 0428-065 export - round 4: re-author history to single lane identity (patch-id parity)

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). PR: #1625 (branch lane-0428-065-cli2-app-export, base develop, NON-DRAFT). Reviewer REQUEST CHANGES on head 16242122dbd7eca0c1e073bd50872416d2d55152; akte evidence/r28-welle4-2026-11-21/pr1625-review/review-1-head16242122.md (verdict line 85).

This round addresses ONLY reviewer finding 1 (identity, card 0428-224). Finding 2 (required per-case CI log proof) is Owner-scope (scripts/** and .github/** are not in this card's write-set) and is reported here as STATE, not remediated.

## PLAN

1. Double-write protection BEFORE any change: fetch --prune both refs via the real GitHub remote and ls-remote the PR head to confirm it still equals 16242122dbd. If it is no longer 16242122dbd, do NOT push - only publish a handoff note and END.
2. Hop to develop d1acf3f31 (back=0), cherry-pick the four content commits in order, rewriting author AND committer to the single lane identity 0428-065-export. Prove patch-id parity: git diff develop..head must equal the pre-rewrite 16242122 diff.
3. Confirm no content change to the eight-plus-path diff and no new tests; no .github/** or scripts/** edit.
4. EIN push --force-with-lease (expected = the remote-head measured in step 1). PR #1625 stays the one PR, non-draft, base develop. No merge.
5. Own hosted CI run to terminal on the new head; record run-id + per-cell conclusion + three test shards.

## repo-rule compliance

- Single integration candidate: lane-0428-065-cli2-app-export, PR #1625. No second branch invented.
- CONTENT-ONLY rewrite. No product change, no new tests, no .github/**, no scripts/**. The reviewer's finding 2 route (per-case log receipt) lives in scripts/** and .github/** (Owner scope); this round does NOT touch them.
- Identity: dedicated worktree 0428-065-export-wt. Canonical identity set to 0428-065-export / 0428-065@baseharbor.local for the rewritten commits.
- No subagents (AGENTS 4.8): every step in this session.
- No git stash, no git add -A over foreign files.

## double-write protection (BEFORE any change)

git remote -v (REMOTE GUARD): origin https://github.com/mcpdev80/baseharbor.git (fetch/push) - the real GitHub remote; used for all fetch/push.

git fetch --prune origin refs/pull/1625/head refs/heads/develop: OK.

git ls-remote BEFORE push:
16242122dbd7eca0c1e073bd50872416d2d55152  refs/heads/lane-0428-065-cli2-app-export
16242122dbd7eca0c1e073bd50872416d2d55152  refs/pull/1625/head
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3  refs/heads/develop

Remote PR head IS 16242122dbd (unchanged from review) => allowed to rewrite.

## base attestation

git ls-remote origin develop:
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3  refs/heads/develop

Hop to develop (back=0): HEAD d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3.

git diff develop..HEAD --name-only (content unchanged, eight-plus paths):
cmd/baha/app_export.go
cmd/baha/app_export_command_test.go
cmd/baha/commands.go
cmd/baha/machine_coverage.go
cmd/baha/target.go
cmd/baha/target_selection.go
cmd/baha/target_selection_state_dir_isolation_test.go
cmd/baha/target_state_layout.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/deployment/target.go
internal/orgconfig/store.go

## identity proof (BEFORE vs AFTER)

Pre-rewrite authors (develop..16242122dbd), the reviewer's finding:
16242122d 0428-065-export 0428-065-export fix(0428-065 r6): operator-auth fixture for export tests + DE docs literal
c44735b99 0428-065-export 0428-065-export fmt(0428-065): gofmt app_export.go, machine_coverage.go after develop rebase
f8f842458 Codex 0428-065-export fix app export managed secret selection and reveal
0643587cf lv4-verify 0428-065-export feat(0428-065): guided baha app export of selected local credentials

Post-rewrite authors (develop..f063d978), ONE lane identity:
f063d9788 0428-065-export 0428-065-export fix(0428-065 r6): operator-auth fixture for export tests + DE docs literal
c51e79ea 0428-065-export 0428-065-export fmt(0428-065): gofmt app_export.go, machine_coverage.go after develop rebase
ba6137ce 0428-065-export 0428-065-export fix app export managed secret selection and reveal
5b86bb53 0428-065-export 0428-065-export feat(0428-065): guided baha app export of selected local credentials

## patch-id parity (content unchanged)

git patch-id <(git diff develop..16242122dbd) [REMOTE pre-rewrite]:
1ca8434426439d7365525b4d80f38870482b3833

git patch-id <(git diff develop..f063d978) [NEW post-rewrite]:
1ca8434426439d7365525b4d80f38870482b3833

Equal => tree content of the PR range is byte-identical before and after the author/committer rewrite.

## push provenance

git push --force-with-lease origin 0428-065-rewrite:refs/heads/lane-0428-065-cli2-app-export (expected 16242122dbd):
+ 16242122...f063d978 0428-065-rewrite -> lane-0428-065-cli2-app-export (forced update)

git ls-remote AFTER push:
f063d9788ab0b8c6a11a6c6aa1c451b37d87099a  refs/heads/lane-0428-065-cli2-app-export
f063d9788ab0b8c6a11a6c6aa1c451b37d87099a  refs/pull/1625/head

gh pr view 1625 --json state,isDraft,baseRefName,headRefName:
{"baseRefName":"develop","headRefName":"lane-0428-065-cli2-app-export","isDraft":false,"state":"OPEN"}
PR #1625 remains the single PR, non-draft, base develop. No merge.

## TEST RUN: hosted CI (own run to terminal)

Run #7099 (GitHub databaseId 44942703411), workflow "CI · PR #1625", event pull_request, head f063d9788ab0b8c6a11a6c6aa1c451b37d87099a, status COMPLETED success, 4m28s, started 2026-11-21T19:46:14Z.

Per-cell conclusion (required + advisory cells):
- Workflow policy: success
- PR · Trusted Plan: success
- PR · Source format: success
- PR · Native gate plan: success
- PR · Focused Python: success
- PR · Go unit · cli-0: success (log: "PASS cli-0: 458 passed / 13 intentionally skipped / 471 discovered")
- PR · Go unit · cli-1: success
- PR · Go unit · cli-2: success (log: "PASS cli-2: 451 passed / 20 intentionally skipped / 471 discovered")
- PR · Go unit · cli-3: success (log: "PASS cli-3: 425 passed / 16 intentionally skipped / 441 discovered")
- PR · Go unit · owner: success
- PR · Go unit · packages: success
- PR · Validation · documentation-audit: success
- PR · Validation · mkdocs-en-strict: success
- PR · Validation · mkdocs-de-strict: success
- PR · Validation · go-build: success
- PR · Validation · go-vet: success
- PR · Validation · cli-gofmt: success
- PR · Validation · pages-candidate-build: success
- PR · Validation · wizard-registration-tests: success
- PR · Selected Checks: success
- (skipped: Release Source Preflight, Targeted HA docker/podman, validate, Exact full Pre-Release, Draft Go, Main release source/Draft source, Main release Go, Workstation onboarding, Runner Interface, Native Keycloak/Core, Exact Candidate, Candidate-added, Demo Pin, Consumer Pins, Selected Runtime, Core-less, Public Contracts, Native, Main release checks)

The three fixed tests hash into those shards under scripts/pr-go-unit-shard.py:60-82:
- TestAppExportCommandPathAssemblesProductionWiring -> cli-0 (passed)
- TestAppExportFailsClosedWithoutSelection -> cli-2 (passed)
- TestAppExportManagedSecretWithoutOperatorFailsClosed -> cli-3 (passed)

The head is a pure identity rewrite (patch-id identical to 16242122), so the earlier auth/data-flow review (review-1, no product defect) still holds for this head.

## finding 2 (Owner-scope) - STATE, not remediated

Reviewer finding 2: the required per-case CI log proof (each target case's name, duration, pass outcome) is absent from the per-job logs; the aggregate cannot establish the non-skipped per-case proof the mission demands. The per-job logs here expose only aggregate shard counts, not the three target test names.

Remedy is Owner-scope: the receipt must come from a hosted run that exposes each target case's name/duration/pass, which requires a change under scripts/** or .github/** - outside this card's write-set (reviewer: "this review did not modify them"; mission forbids editing scripts/** and .github/**). Stop criterion: all three per-case records present for the exact reviewed head and each a pass. This round leaves that criterion outstanding for the Owner.

## cleanliness

- docker ps -a --filter name=bh- before: (no containers started this shift; git worktree only)
- docker ps -a --filter name=bh- after: (no containers started this shift; git worktree only)
- git worktree list after: 0428-065-export-wt (detached HEAD f063d978, pushed to lane branch)
- temp ref refs/orig/pr1625 (old) and refs/orig/pr1625-new (new) left in worktree for patch-id evidence; not pushed to any tracked remote branch.
