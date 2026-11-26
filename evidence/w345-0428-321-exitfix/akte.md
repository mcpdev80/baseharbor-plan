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
- `git log --oneline origin/develop..HEAD` lists only w334/w345 commits (cdb6e4d97 + 33754a9a0 + c0c39f3b9); no foreign candidate carried on top.
- PR #1866 head after FF push: c0c39f3b9dada2b0671c14782b8d4ad98a4aa248 (ls-remote + gh api witness).

## END_DONE

## PLAN

- Read mission w345-0428-321-exitfix + card; verify worktree identity + github remote
- Paste git var gate + visible ansatz block before first commit
- TestExitCodeTaxonomyLocked (cli_test.go) asserts real WithExitCode->ExitCode passthrough across documented 1-255; TestSignalMapsToDocumentedExitCode drives ResolveSignalExitCode (main-level contract entry interruptibleProcessContext uses)
- Harden exit_code_taxonomy_audit.py: reject undocumented codes incl >255; fix PASSTHROUGH_UPPER_BOUND typo; drop duplicate __main__ block
- Precheck go vet ./cmd/baha/ and ./internal/cli/ (clean); audit green; prove 0428-322 untouched
- Committed 33754a9a0 then c0c39f3b9 under w345 identity; FF push; PR #1866 head = c0c39f3b9
- Hosted CI run 45886641732: Docker + rootless Podman data-capabilities PASSED on exact head; Go Selected Checks failed gofmt-only; corrected c0c39f3b9
- HOLD (02:5xZ): Trusted Plan reads catalog from trusted develop, same-PR coverage row cannot work (run 45888974142 confirms). w267 decision on route (a) helper-in-catalogued-cli.go vs (b) baseline pending. Keep worktree clean, lane open.

## repo-rule compliance

- Product repo only: internal/cli/cli_test.go (test) + scripts/exit_code_taxonomy_audit.py (audit row in documentation-audit.sh:262). Docs (cli.md, errors.md) not rewritten.
- 0428-322 (cmd/baha/app_exec.go, internal/cli/cli.go) untouched: zero exit-code behavior change.
- No .github/** edits, no workflow_dispatch, no reruns by hand. No subagents. No local test execution (go vet/build only). Evidence in baseharbor-plan only.

## cleanliness

- docker ps -a BEFORE: (none started this shift)
- docker ps -a AFTER: (none to tear down)
