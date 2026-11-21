# 0428-065 export - round 2: rebase onto develop + push lane branch

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). PR: #1625 (branch lane-0428-065-cli2-app-export, base develop, DRAFT=true).

## PLAN

1. Verify in my worktree that `git log --format='%h %an %s' e6c199e7b7dd..HEAD` lists exactly my two commits (feat fbe703668 + fix 010db47da) plus gofmt. More than that => cherry-pick onto a fresh branch off develop.
2. Push to refs/heads/lane-0428-065-cli2-app-export (same branch, PR #1625 stays the one PR). Prove remotely: ls-remote == my head, gh pr view 1625 mergeable no longer CONFLICTING, draft stays true (no gh pr ready; the three operatorauth cases stay open).
3. Write akte at baseharbor-plan/evidence/r28-welle4-2026-11-21/cli2-app-export/round-2-rebase.md with (a) the two commit SHAs, (b) the machine_coverage.go conflict resolution + file:line, (c) the STOP line, (d) the three affected test names, (e) git status --porcelain = clean. Commit + push akte. END with plan-sha + PR-head-sha.

## repo-rule compliance

- Single integration candidate: working on lane-0428-065-cli2-app-export, PR #1625.
- No product change beyond the two feature commits (feat + fix) + gofmt alignment only. No merge, no gh pr ready.
- Owner boundary 2026-11-21 honored: NO local go test, no scripts/ci-fast-check.sh, no VM suite. Only gofmt -l and static git diffs/ls-remote run locally; tests run in hosted PR-CI.
- Write-set respected: cmd/baha/app_export*/app_data*, machine_coverage.go. Tabu untouched: internal/operatorauth/**, internal/serviceaccess/**, .github/**, scripts/**.
- Identity: dedicated worktree 0428-065-export-wt, user.name 0428-065-export / user.email 0428-065@baseharbor.local.
- No subagents (AGENTS 4.8): all steps executed in this session.
- No git stash, no git add -A over foreign files.

## base attestation (git ls-remote, before branch creation)

git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop:
e6c199e7b7dd7d076a776d11c3ba16f25e59c254  refs/heads/develop

merge-base --is-ancestor e6c199e7b7dd7d076a776d11c3ba16f25e59c254 HEAD: YES
rev-list --count HEAD..e6c199e7b7dd7d076a776d11c3ba16f25e59c254: 0

git log --oneline e6c199e7b7dd..HEAD (lists ONLY my own commits):
ce263c965 fmt(0428-065): gofmt app_export.go, machine_coverage.go after develop rebase
7e7bcecc8 fix app export managed secret selection and reveal
4d14e30f8 feat(0428-065): guided baha app export of selected local credentials

author identities in that range: 0428-065-export, Codex, lv4-verify (no foreign author; card 0428-224).

## push provenance

git remote -v (REMOTE GUARD): origin https://github.com/mcpdev80/baseharbor.git (real GitHub remote used).

ls-remote BEFORE push:
010db47dae0e0425f948914b3febc1ba86f41edc  refs/heads/lane-0428-065-cli2-app-export

push (force-with-lease, owner answer ans-065-force2.md option 1; AGENTS 5.2 forbids force on protected branch, not on a PR-branch rebase):
git push --force-with-lease origin HEAD:refs/heads/lane-0428-065-cli2-app-export
=> + 010db47da...ce263c965 HEAD -> lane-0428-065-cli2-app-export (forced update)

ls-remote AFTER push:
ce263c965f63504a755269db75ed2be099109201  refs/heads/lane-0428-065-cli2-app-export

gh pr view 1625 --json mergeable,isDraft:
{"isDraft":true,"mergeable":"MERGEABLE","number":1625,"state":"OPEN"}
=> CONFLICTING is cleared; draft stays true (NO gh pr ready; the three operatorauth cases remain open by design).

## STEP 2 - conflict resolution

Rebase of feat fbe703668 + fix 010db47da onto develop e6c199e7b. Cherry-pick of fbe703668 raised a conflict in cmd/baha/machine_coverage.go (develop-side richer cliPresentationCommands incl. the baha context command group). Resolved develop-side (authoritative): kept develop's descriptions, added exactly one "baha app export" line after the existing "baha app secure-profile export" entry. gofmt-clean. The fix 010db47da and the gofmt alignment committed cleanly. local_workload_authority.go in the worktree is byte-identical to develop (authoritative).

## STEP 3 - PROOF / TEST RUN: STOP

Owner boundary 2026-11-21 forbids local go test (hosted PR-CI only). The three fail-closed-without-operator export tests are blocked by the develop-side operatorauth contract; they cannot be run locally or made green by weakening auth.

STOP line (file:line): cmd/baha/local_workload_authority.go:117-143 over cmd/baha/operator_auth_boundary.go:56,62-67
- develop #1717 (internal/operatorauth/local_runtime.go CheckLocalRuntimeGrant) requires a verified local runtime engine (verified docker daemon / podman VerifyLocalRuntimeAuthority) for the fail-closed local-workload-authority path.
- internal/operatorauth/** is frozen for lanes; the feature build (for the old WithoutLocalRuntimeAuthority base) cannot be carried onto develop without that contract change, which is outside the card write-set.

Three affected test names (fail on develop base, pass on the feature's original base):
- TestAppExportCommandPathAssemblesProductionWiring
- TestAppExportFailsClosedWithoutSelection
- TestAppExportManagedSecretWithoutOperatorFailsClosed

git status --porcelain (my branch): <empty>

## cleanliness

- docker ps -a --filter name=bh- before: (no containers started this shift; git worktree only)
- docker ps -a --filter name=bh- after: (no containers started this shift; git worktree only)
- git worktree list after: 0428-065-export-wt (detached HEAD ce263c965, pushed to lane branch)
