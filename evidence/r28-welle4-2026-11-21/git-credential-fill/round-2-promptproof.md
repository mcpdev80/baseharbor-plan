# 0428-217 git credential fill bootstrap hang — round-2 evidence (prompt-path proof)

Lane: 0428-217-credfix2 (worker session, flash channel). Card:
`t-20261121-git-credential-fill-bootstrap-hang`. PR: #1742 (`w0428-217credfill`).
Correction round 2 against `evidence/r28-welle4-2026-11-21/git-credential-fill/review-1.md`
(BEFUND 1: witness must reproduce git's OWN prompt/askpass path, red-first;
BEFUND 2: app_update.go stdin lines need a focused regression or removal).

## Candidate and provenance

- Final candidate head: `719d28a888abf9dc2c7715fb002f1aa77fdf9708` (merge commit
  `Merge develop 4fa5293a4 into 0428-217 candidate (round-2 hop)` on top of
  round-1 `0df7efc00bb3` + round-2 commit `517d2a4e2`).
- Develop hop: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  measured `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9` (advanced again during
  this round; earlier coordinator snapshot 72ebc9d10ec2 is contained in it —
  `git merge-base --is-ancestor` after the merge: develop head is an ancestor of
  the candidate, so the hop is current).
- `git log --oneline origin/develop..HEAD` after hop:
  `517d2a4e2 test(0428-217): prove the credential-fill fix on git's own prompt path`
  and `0df7efc00 fix(0428-217): git credential fill must fail closed ...`
  (own commits only).
- `git diff origin/develop...HEAD --name-only`: cmd/baha/app_inspect_remote.go,
  cmd/baha/app_update.go, cmd/baha/app_update_gitstdin_test.go,
  internal/credential/native/{credfill_noninteractive_test.go,credfill_pty_linux_test.go,credfill_pty_stub_test.go,gitcredential.go,host.go}
  — exactly the write-set plus the new regression file (inside the write-set).
- Delivery witness: `git push --force-with-lease=w0428-217credfill:0df7efc00bb3... https://github.com/mcpdev80/baseharbor.git HEAD:refs/heads/w0428-217credfill`
  then `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w0428-217credfill refs/pull/1742/head`
  showed `719d28a888...` on the branch, and `gh pr view 1742` confirmed
  `head=719d28a888abf9dc2c7715fb002f1aa77fdf9708 draft=false merge=BEHIND`
  with `refs/pull/1742/head` at the same SHA.

## BEFUND 1 + M1: the test reproduces git's own prompt/askpass path

Key platform calibration (measured this round, needed to understand the design):

- Go's `os/exec` de-duplicates `cmd.Env` keeping the LAST copy of a duplicated
  key, so an in-process "sick" builder that reproduces round-1's append-only
  vector CANNOT make git consult the inherited prompt script through Go exec —
  the duplicate resolves to the appended `/bin/false` and the red arm goes green
  for the wrong reason (witnessed repeatedly, incl. `/proc/self/environ` reads
  showing one resolved copy).
- A RAW `execve` vector with duplicates intact (no Go de-duplication) resolves
  git's prompt lookups to the FIRST (inherited) copy: the round-1-shaped vector
  HANGS git on the waiting `GIT_ASKPASS` script (`rc=124` under `timeout`) and,
  with an answering prompt script, makes git fabricate a credential
  (`username=x password=x`, `rc=0`) behind the appended `GIT_TERMINAL_PROMPT=0`.
  This is the card's fail-open/hang, reproduced on git's real prompt path.
- `GIT_CREDENTIAL_HELPER` as environment override is NOT honored by this git
  (2.53) for helper selection (marker helper never executed); the helper comes
  from config. Production nonetheless strips+pins the key defensively — the
  strip set is a superset guarantee, harmless on platforms without the override.

Design (in `internal/credential/native/`):

- `host.go` keeps ONLY production code: `appendNonInteractiveEnv` strips every
  inherited prompt key (`promptEnvKeys()` incl. `GIT_CREDENTIAL_HELPER`) and
  appends the sentinels exactly once (`GIT_TERMINAL_PROMPT=0`,
  `SSH_ASKPASS=/bin/false`, `GCM_INTERACTIVE=never`,
  `GIT_CREDENTIAL_HELPER=/bin/false`, `GIT_ASKPASS=/bin/false`).
  `CredentialFillEnvSickForTest` (exported, test-use-only, documented)
  reproduces the round-1 establishment (pure append, round-1 order) so the M1
  witness runs the historical code shape, not a paraphrase.
- `TestRound1VectorKeepsPromptChannelOpen` (the M1 witness): builds the
  inherited-hostile base (waiting `GIT_ASKPASS` script recording each
  invocation, `GIT_TERMINAL_PROMPT=1`), runs it through
  `native.CredentialFillEnvSickForTest`, and `execve`s git via
  `syscall.ForkExec` — bypassing Go's de-duplication exactly as round-1
  production handed the vector to the OS. Assertion: the prompt script executed
  or the probe hung to the deadline. Measured: RED for round-1 code (git asked,
  `CALL1 Username for 'https://example.invalid':`), and it does not depend on
  any test-only hook in the fixed path.
- `TestGitCredentialFillIsNonInteractiveProvesTheFix` (the fixed arm through
  the production seam `GitCredentialSource.Resolve → ExecRunner.Invoke`): with
  the fix, git can reach no prompt channel, the script never runs, the probe
  fails closed with the host-named `ErrGitCredentialUnavailable` well inside
  the 15s deadline. GREEN.
- `TestExecRunnerEnvSentinelsWinInChildVector` pins the child's own
  `/proc/self/environ`: exactly one copy of each pinned key with the sentinel
  value, inherited `GIT_SSH_COMMAND` removed. GREEN.
- `TestGitCredentialFillIsNonInteractiveUnderControllingTerminal` (PTY witness,
  Linux, `credfill_pty_linux_test.go` + stub): the production runner starts git
  with a real controlling terminal (`pty.Open`, setsid + ctty), config helper
  reads the password from the terminal; with the fix the probe fails closed
  fast, and the hook-gate `ttyPromptBranchWasLive` proves the terminal branch
  actually ran. GREEN.
- Develop-baseline M1 (already recorded in round-1 evidence and re-confirmed):
  at develop `40cb28c75` (no `cmd.Env` at all), the same fixed-arm tests hang
  to the 20s deadline and FAIL. M1 therefore discriminates three ways: raw
  round-1 vector (this file), develop baseline, and PTY terminal path.

Local run at candidate `719d28a88` (after hop), named form:
`go test ./internal/credential/native/ -count=1` → `ok` (all witnesses incl.
the M1 red-vector witness green-as-red). Full-package suite output shows the
five credential-fill witnesses PASS (round-1 vector witness logs
`M1 red as required: round-1 vector reaches git's prompt path`).

## BEFUND 2: app_update.go :456/:515 kept, with focused regression

`cmd/baha/app_update_gitstdin_test.go::TestGitOutputUpdatePathNeverTakesControllingTerminal`:
drives the REAL update-path helpers `gitOutput`/`gitIsAncestor` over a temp
repository (init, commit, local fetch, ancestor checks) under a 10s deadline —
bounded failure, no hang — plus an AST-level pin (`pinHelperStdinContract`)
that fails if either helper stops assigning `cmd.Stdin` before starting its
git subprocess. Mutation probe: both `cmd.Stdin` lines commented out → test
FAILS naming both helpers ("must assign cmd.Stdin"); lines restored → PASS.
The two lines therefore stay, as the contract's alternative required a
regression of exactly this shape.

## CI pickup answer (where internal/credential/native runs)

Cell: `PR · Go unit · packages` (`.github/workflows/ci.yml:1185-1186`, matrix
shards built at `ci.yml:961-962` — full scope extends `cli-0..3` with
`packages` + `owner`). The shard executes
`scripts/pr-unit-database.sh:38-40 → python3 scripts/pr-go-unit-shard.py --mode packages`,
whose selection rule is `packages()` at `scripts/pr-go-unit-shard.py:117-134`:
`go list ./...` minus `./cmd/baha` — i.e. EVERY non-CLI package, so
`internal/credential/native` runs there unfiltered whenever the plan selects
full Go-unit scope. The new tests need no workflow change: no `.github/**` or
`scripts/**` edit is required for CI pickup.

## Hosted CI on the exact head (§4.6 own-run duty)

Run `44895100181` ("CI · PR #1742" / Source & Quality), headSha
`719d28a888abf9dc2c7715fb002f1aa77fdf9708`, observed by this lane from creation.

(RESULT AND PER-JOB FAIL-NAME COUNTS APPENDED BELOW BY THE LANE AFTER TERMINAL STATE.)

END-PENDING

## repo-rule compliance

- Write-set honored: only `internal/credential/native/{host.go,gitcredential.go,credfill_noninteractive_test.go}` (+ two new witness helpers in the same package), `cmd/baha/{app_inspect_remote.go,app_update.go}` and the new `cmd/baha/app_update_gitstdin_test.go`; no `.github/**`, no `scripts/**`, no other repos.
- `gofmt`/`go vet` clean; `bash scripts/ci-fast-check.sh` → 295 python tests OK, no candidate-added validation checks; `scripts/source-readability-audit.sh` all PASS; `scripts/documentation-audit.sh` PASS.
- No subagents used; single lane session; scratch `zz_*_test.go` calibration files deleted before commit (`git status` clean at commit).
- Named-form runs honored (`-skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` for cmd/baha). The access-wizard failures observed at 0df7efc00 are PRE-EXISTING at base (verified: identical failures via `git stash` at develop content) and belong to the w200/0428-200 trust-regression class, not this change.

## cleanliness

Before push and after all test runs on this host:
`docker ps -a` → header only, zero containers (docker daemon reachable, none
created; no test in this lane creates containers). No volumes/networks/state
directories owned by this lane; every witness ran inside `t.TempDir()`.
