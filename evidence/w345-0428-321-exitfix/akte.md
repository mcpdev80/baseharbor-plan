# w345-0428-321-exitfix: 0428-321 correction round

## visible ansatz block (recorded at correction-round start; candidate committed after)

- card frontmatter owner (fetched from origin/main at runtime): `w345-0428-321-exitfix` (card t-20261125-hunt45-exit-code-taxonomy-docs; card_number 0428-321; kanban_status active). Coordinator correction block: "321 sits in REVIEW; correction round; do not commit as-is; steer 2/3 pending disposition."
- git user.name I use: w345-0428-321-exitfix
- git user.email I use: w345-0428-321-exitfix@baseharbor.local
- commit invocation (literal, per-command, on the pinned worktree):
  `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix -c user.name=w345-0428-321-exitfix -c user.email=w345-0428-321-exitfix@baseharbor.local commit -m "..."`
- pre-push admission gate (literal): `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix show -s --format=%an HEAD` must equal `w345-0428-321-exitfix` exactly; on mismatch STOP + report (no silent amend).
- worktree identity gate (pinned): `git var GIT_AUTHOR_IDENT` / `GIT_COMMITTER_IDENT` show w345-0428-321-exitfix; bare git config FORBIDDEN.

## base attestation

- baseharbor product remote (worktree, github.com/mcpdev80 confirmed): origin https://github.com/mcpdev80/baseharbor.git
- base ref cut from: cdb6e4d977d903ebbb6198b9b001403aba07868d (PR #1866 head, verified via `git ls-remote origin refs/pull/1866/head` and `gh pr view 1866`).
- `git merge-base --is-ancestor origin/develop HEAD`: develop is ancestor of cdb6e4d97.
- `git log --oneline origin/develop..HEAD` lists only w334/w345 commits (cdb6e4d97 + my 33754a9a0); no foreign candidate carried on top.
- PR #1866 head after my FF push: 33754a9a0b3462892d837574dfc09ab7da11a486 (ls-remote + gh api witness).

## END_DONE


## visible ansatz block

- card frontmatter owner (fetched from origin/main at runtime): owner EMPTY (`t-20261125-hunt45-exit-code-taxonomy-docs` frontmatter `owner:` blank; coordinator assigned owner w345-0428-321-exitfix via kanban_status=active on plan main; provenance in commit messages).
- git user.name I use: w345-0428-321-exitfix
- git user.email I use: w345-0428-321-exitfix@baseharbor.local
- commit invocation (literal, per-command, explicit --repo on the pinned worktree):
  `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix -c user.name=w345-0428-321-exitfix -c user.email=w345-0428-321-exitfix@baseharbor.local commit -m "..."`
- pre-push admission gate (literal): `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix show -s --format=%an HEAD` must equal `w345-0428-321-exitfix` exactly; on mismatch STOP + report.

## gate: git var before first commit

- `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix var GIT_AUTHOR_IDENT` = `w345-0428-321-exitfix <w345-0428-321-exitfix@baseharbor.local> ...`
- `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix var GIT_COMMITTER_IDENT` = `w345-0428-321-exitfix <w345-0428-321-exitfix@baseharbor.local> ...`
- identity pinned by the worktree; git config read via `--repo` on the pinned path; bare `git config` FORBIDDEN.

## base attestation

- baseharbor-plan remote (pulled before first commit): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => origin https://github.com/mcpdev80/baseharbor.git
- baseharbor product remote (worktree): `git -C /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w345-0428-321-exitfix remote -v` => origin https://github.com/mcpdev80/baseharbor.git (single github.com/mcpdev80 remote; no local-fs 'origin').
- base ref SHA cut from (ls-remote): develop = see live output below; cdb6e4d97 is a descendant of develop.
- `git -C ... merge-base --is-ancestor origin/develop HEAD` => YES (develop is ancestor of the PR head).
- `git -C ... log --oneline origin/develop..HEAD` lists only the existing single commit cdb6e4d97 (0428-321) — my new commit will be the only new entry.

## candidate / PR

- PR #1866 = 0428-321 head `cdb6e4d977d903ebbb6198b9b001403aba07868d` (ls-remote witness: same as worktree head).
- PR state at dispatch: OPEN, isDraft=false.
- Transport: `git push origin HEAD:w334-0428-321-exitcodedocs` (ordinary fast-forward; PR #1866 stays, no retarget). Prior lanes w334 (released) and w342 (retracted) — I am the implementing lane w345.

## PLAN

- Read mission w345-0428-321-exitfix + card; verify worktree identity + github remote
- Paste git var gate + visible ansatz block before first commit
- Convert tautology TestExitCodeTaxonomyLocked (cli_test.go:79-92) into a real passthrough test (assert ExitCode==child status across documented codes) plus a real SIGINT/SIGTERM->130/143 mapping test via main-level contract, not local map-key checks; zero behavior change
- Harden exit_code_taxonomy_audit.py: reject undocumented codes including 256; distinguish child-status passthrough range (1-255) from named top-level taxonomy values
- Precheck format/vet/build only (NO local test execution); prove 0428-322 untouched
- Push to PR branch under w345 identity; ancestry + commit-identity gate
- Trigger Hosted CI on exact head (draft toggle per doctrine); watch terminal run; capture FULL40+ run ids
- PR head comment, evidence, END_DONE, cleanliness (docker ps witness), publish

## repo-rule compliance

- Product repo only: internal/cli/cli_test.go (test) + scripts/exit_code_taxonomy_audit.py (audit row already wired in documentation-audit.sh:262). Docs (cli.md, errors.md) already honest; not rewritten.
- 0428-322 (cmd/baha/app_exec.go, internal/cli/cli.go ExitCode/WithExitCode behavior) untouched: zero exit-code behavior change. Only test + audit script.
- No .github/** edits, no workflow_dispatch, no reruns by hand. Draft toggle done via gh api gh ready (allowed: PR state, not CI infra).
- No subagents. No local test execution (only go vet/build prechecks). No direct main writes. Evidence lives in baseharbor-plan only.

## cleanliness

- docker ps -a BEFORE: (none started this shift)
- docker ps -a AFTER: (none to tear down)

## HOLD / BLOCKER (02:5xZ, coordinator) -> RESOLVED via steer 5/6/7

- RESOLVED. w267 chose route (a): move signal->exit helper into already-catalogued internal/cli/cli.go, regression test in already-catalogued internal/cli/cli_test.go, main.go calls the helper on the SIGTERM path, no pr-gate-coverage.json row.
- steer-6 catalog gate (job 140156134115) rejected head 6609608f5 for an uncataloged cmd/baha/main_test.go edit. Fixed: moved the passthrough coverage entirely into internal/cli/cli_test.go (drives the same main-level contract entry cli.ResolveSignalExitCode) and reverted cmd/baha/main_test.go to develop's version. PR diff now touches only catalogued files: cmd/baha/main.go, internal/cli/cli.go, internal/cli/cli_test.go, scripts/exit_code_taxonomy_audit.py.
- steer-7: head 03354deb876bae74272c1691537169792322288d had two attempt-1 pull_request runs; watched both. Run 45895462941 ended CANCELLED (cancel-in-progress group, ci.yml W33). Run 45895504172 (run_number 7916) is COMPLETED SUCCESS on the exact head with all required checks green.
- Zero behavior change: main.go:61-63 context.Canceled->130 shortcut intact; no rewiring; w267 bar honored. No behavior delta required for the 143 mapping.
- No merge. PR #1866 stays OPEN. Independent w255 review only after this END + green checks.

## END_DONE

- Card: 0428-321 (t-20261125-hunt45-exit-code-taxonomy-docs). Owner w345-0428-321-exitfix. Coordinator re-lane from w334, owner order 23:2xZ.
- Candidate head (PR #1866, exact): 03354deb876bae74272c1691537169792322288d (ls-remote + gh api witness; PR #1866 head on origin/main).
- Ancestry: git merge-base --is-ancestor origin/develop HEAD = true; git log --oneline origin/develop..HEAD lists only w334/w345 commits (cdb6e4d97 -> 33754a9a0 -> c0c39f3b9 -> 6609608f5 -> 03354deb8), no foreign candidate carried on top.
- Commits (all author+comitter w345-0428-321-exitfix):
  - 33754a9a0 drive signal->exit mapping through main-level contract entry
  - c0c39f3b9 gofmt cli_test + cover main_test.go in pr-gate-coverage (later reverted for steer-6)
  - 6609608f5 move signal->exit helper into catalogued cli.go (steer-5 route a)
  - 03354deb8 move passthrough coverage into catalogued cli_test.go (steer-6, revert main_test.go)
- Hosted CI evidence (exact head, FULL40):
  - Run 45895504172 (run_number 7916, event pull_request, head 03354deb8): COMPLETED SUCCESS.
  - Required checks green: PR.Trusted Plan, PR.Native gate plan, PR.Source format, Workflow policy, PR.Native native/podman/data-capabilities (success), PR.Native native/docker/data-capabilities (success), Go unit cli-1/cli-2/cli-3 (success), Go unit packages/owner (success), Validation go-vet/documentation-audit/ci-policy/mkdocs-de-strict (success). PR · Candidate-added checks (advisory) success. All release/pre-release jobs skipped (not a release PR).
  - No cancelled job on the qualifying run. Run 45895462941 (same head) ended CANCELLED (cancel-in-progress) and is NOT used as evidence.
- Gate route: signal->exit mapping lives in internal/cli/cli.go (SignalExitCode/ResolveSignalExitCode) and is exercised by TestSignalExitCodeMapsToDocumentedContracts in internal/cli/cli_test.go; CI coverage flows through the already-catalogued cli package (go vet, Go unit cli-1/2/3, documentation-audit). No same-PR pr-gate-coverage.json row (route a); catalog stays on develop.
- Behavior unchanged: main.go context.Canceled->130 shortcut (main.go:61-63) intact; signal handler calls cli.ResolveSignalExitCode on its SIGTERM exit path; 0428-322 (app_exec.go, cli.go ExitCode/WithExitCode) untouched.
- PR: #1866 OPEN at head 03354deb876bae74272c1691537169792322288d. No third run triggered. No merge.
- Evidence on origin/main (verified): ls-tree -r --name-only origin/main | grep w345-0428-321-exitfix/akte.md.

## cleanliness

- docker ps -a BEFORE: (none started this shift)
- docker ps -a AFTER: (none to tear down)
- Host runs only go vet/build prechecks; no go test, no containers. CI runs on GitHub shared runners.
