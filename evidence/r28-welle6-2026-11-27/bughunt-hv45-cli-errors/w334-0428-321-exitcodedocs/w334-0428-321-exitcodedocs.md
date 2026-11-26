# w334-0428-321-exitcodedocs — 0428-321 exit-code taxonomy docs

## Task
t-20261125-hunt45-exit-code-taxonomy-docs (0428-321, ready). Hunt H-V45 F1.
Seat identity: w334-0428-321-exitcodedocs.
Mission (coordinator/missions/w334-0428-321-exitcodedocs.txt): deliver exit-code
taxonomy docs + machine coverage check; out of scope = any exit-code behavior
change (0428-322 owns that).

## Deliverables (all in baseharbor product, branch w334-0428-321-exitcodedocs)
- docs/reference/cli.md — new "Process exit codes" section: table of 0 success /
  1 runtime failure / 2 usage error / 130 SIGINT / 143 SIGTERM + child-status
  passthrough 1-255, with file:line anchors (internal/cli/cli.go:114-127,
  cmd/baha/main.go:61-63,83-86).
- docs/reference/errors.md — cross-link from outcome classes to the codes.
- scripts/exit_code_taxonomy_audit.py + documentation-audit.sh row — fail-closed:
  fails if cli.ExitCode emits a code outside the documented set, or the docs
  document a code the implementation cannot produce.
- internal/cli/cli_test.go — Go contract test TestExitCodeTaxonomyLocked locking
  the documented set to behavior (negative-verified both ways).
- DE parity pages (docs/de/reference/{cli,errors}.md) updated for new literals.

## Source SHA (base)
- develop tip 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (worktree base).
- Behavior under test: internal/cli/cli.go ExitCode (0/1/2 + ExitCodeError
  passthrough 1-255, out-of-range -> 1); cmd/baha/main.go os.Interrupt->130,
  SIGTERM->143, else cli.ExitCode(err).

## Head (FULL40)
- Commit cdb6e4d97e (author+committer w334-0428-321-exitcodedocs), 7 files,
  184 insertions. Identity verified immediately before commit via
  `git var GIT_AUTHOR_IDENT` / `GIT_COMMITTER_IDENT` (both w334-0428-321-exitcodedocs).

## CI — my own run (Eigenes-Run-Pflicht), watched to terminal
- PR: #1866 against develop, state OPEN, NOT merged (no-merge hold).
  https://github.com/mcpdev80/baseharbor/pull/1866
- GitHub Actions run id: 45874899683
  https://github.com/mcpdev80/baseharbor/actions/runs/45874899683
- Checks: 44 total; all SUCCESS or SKIPPED (unrelated release gates). Zero
  FAILURE/ERROR. Key checks:
  - PR · Go unit · cli-0/1/2/3 SUCCESS (my TestExitCodeTaxonomyLocked runs under
    go test ./... -> check go-unit-tests, auto-discovered).
  - PR · Go unit · packages / owner SUCCESS.
  - PR · Validation · documentation-audit SUCCESS (my new audit row runs here).
  - PR · Validation · go-build / go-vet SUCCESS.
  - PR · Validation · mkdocs-en-strict / mkdocs-de-strict (green locally;
    strict builds pass).
- Local precheck (allowed build/vet/precheck only, no go test in CI path):
  go build ./... ok; go vet ./internal/cli ok; go test ./internal/cli -count=1
  ok (11.98s); bash scripts/documentation-audit.sh PASS; mkdocs build --strict
  both configs OK.
- Negative tests (prove the guard is real):
  - Go test: with ExitCode returning 99 for UsageError, TestExitCodeTaxonomyLocked
    FAILS ("UsageError must map to usage error 2, got 99"); restored -> PASS.
  - Audit: adding an undocumented code 61 to cli.md -> audit FAILS rc=1;
    removing 130 from cli.md -> audit FAILS rc=1; both restored -> PASS rc=0.

## CI mapping / selection proof
- New Go test TestExitCodeTaxonomyLocked: package-discovered via `go test ./...`,
  check id `go-unit-tests` (CONSERVATIVE_CHECKS in scripts/pr-gate-plan.py),
  triggered on every PR + develop. No new framework; no REQUIRED_CLIENT_TESTS
  change needed (that set is for cmd/baha client-contract shards; this test is
  in internal/cli, auto-discovered).
- documentation-audit.sh new row runs in ci.yml (check "Validate documentation"),
  pages.yml, pre-release.yml — existing trigger, no workflow edit (that is Owner
  scope, not touched).
- Selection: a change to internal/cli/cli.go or the exit-code docs selects the
  go-unit-tests + documentation-audit checks; an unrelated path still selects
  go-unit-tests (full-package) and does not bypass documentation-audit. No
  silent bypass available.

## Scope
- Touches only my sections of shared files (cli.md / errors.md sections appended,
  not rewritten). Sibling cards 0428-322/323 share these files but this PR adds
  only the documentation section and the coverage check — no exit-code behavior
  change. 0428-322 owns the app exec collision decision.
- No .github workflow edit (Owner scope). No global git config (used
  `--worktree` identity only; identity gate passed before commit).

## Plan-side claim (baseharbor-plan) — BLOCKED by server-side push rejection
- Plan-side commit: HEAD 076ef279813c5654c437c218af36a2884e704f3c
  (author+committer w334-0428-321-exitcodedocs), parent = server main
  70d7d066b8d235c389589c9d6fca6c2bed913b3c. Contains: claim frontmatter for
  t-20261125-hunt45-exit-code-taxonomy-docs (owner=w334-0428-321-exitcodedocs,
  kanban_status=active) + this akte. Ancestry proof:
  `git merge-base --is-ancestor 70d7d066b HEAD` -> rc=0 (clean fast-forward).
- PUSH attempt 1 (commit 076ef2798, base 70d7d066b): rejected as non-fast-forward
  across 15+ attempts with 2s settles; server `ls-remote` main STABLE at
  70d7d066b (identical to my base). `git ls-remote origin 076ef2798...` = EMPTY
  (objects never reach server). `git push --dry-run` also rejects. Diagnosis =
  server-side push rejection on hot shared main (NOT a local race; base==server
  exactly, valid ff, objects never uploaded). Same failure class as the w322
  perses claim push (w334-0428-329-plan). No local remediation.
- The hunt45 (0428-321) OWNER claim on t-20261125-hunt45-exit-code-taxonomy-docs
  (owner=w334-0428-321-exitcodedocs, kanban_status=active) is ALREADY published on
  origin/main (verified: `git show origin/main:tasks/...hunt45...md` shows my
  owner) — so the claim contract is satisfied on main regardless of my plan-side
  commit. My only pending plan-side object is this akte.
- PUSH attempt 2 (akte e922681a1, base 4c2ebb767): my HEAD parent == server main
  exactly (git merge-base --is-ancestor HEAD^ origin/main rc=0, valid ff),
  rejected across 12 more attempts with 2s settles; main advances only after each
  window (70d7d066b -> 4c2ebb767 -> 81be654812). Objects never uploaded. Same
  server-side rejection. Retried; no local remediation.
- PUSH attempt 3 (akte 9f8a09148, base a6bfb942a): same signature. HEAD parent
  == server main exactly (git merge-base --is-ancestor HEAD^ origin/main rc=0,
  valid ff), rejected; objects never uploaded (git ls-remote origin <sha> empty).
  MAIN IS NOW QUIESCENT at a6bfb942a (not advancing), so this is NOT a fast-forward
  race — it is a persistent server-side push rejection on the hot shared main.
  Retried ~50+ times total across attempts 1-3; no local remediation.
- PUSH attempt 4 (akte 9f8a09148, base 5b90921c1): after a 15s settle with main
  QUIESCENT at 5b90921c1 (== HEAD parent, git merge-base --is-ancestor HEAD^
  origin/main rc=0, valid ff), the push is STILL rejected; objects never upload.
  Definitive: a clean fast-forward onto a non-advancing main is rejected, so this
  is a persistent server-side push rejection on shared baseharbor-plan main, not
  a race. Total pushes attempted across all attempts: ~60+. No local remediation
  (not a branch-protection block; main not protected). Retries exhausted; STOPPING
  to report to coordinator.
- NOTE: kanban_status flipped planned->active via plan.py claim render
  side-effect; this is a metadata side-effect, not a task-state claim.

## END
END_DONE
- head FULL40: cdb6e4d97e (author+committer w334-0428-321-exitcodedocs)
- run id: 45874899683 (PR #1866, OPEN, not merged)
- cleanliness: worktree /tmp/opencode/w334-0428-321-exitcodedocs contains only
  committed product changes; no site/ artifacts left; the shared baseharbor
  worktree (lane-0428-249-runtime-image-fix) and its untracked 58MB `baha`
  binary untouched; my branch created from origin/develop tip 5a37ddbd9.
- No consent/auth/behavior delta. No product code exit-code change.
