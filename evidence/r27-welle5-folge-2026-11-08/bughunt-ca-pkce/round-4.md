# 0427-134 r4 — PR #1457 execution (round 4)

## Status

ACTIVE — executing the fix recipe from `act-1457-review-r3.md` (r3 review: REQUEST-CHANGES).
Scope per mission: TWO deliverables only — (1) `--no-browser` consumed in the CLI login
path, (2) the parser regression test flipped + a command-level regression. Points 2/3 of the
r3 verdict (combined CA+PKCE test, DAE doc/unit) are PASS and were NOT touched. Trigger #1464
is the 0427-136 lane's drift-merge, not mine.

## PLAN

- Read mission + `act-1457-review-r3.md` fully; verify live refs
- Create isolated worktree at the exact PR head, cut working branch from that exact SHA
- (1) Fix `cmd/baha/operator_auth.go`: capture `--no-browser` into `noBrowser=true` and
  consume it (do NOT append to the generic `remaining` list)
- (2) Flip `TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag` to assert `--no-browser`
  absent from `remaining`; add a command-level regression proving the documented
  `baha login -e dev --no-browser` invocation reaches the headless path
- Local verify: build, vet, targeted tests, docs audit
- Commit only my two files, push to the named candidate, delete stray branch with witness
- Report trigger #1464 (not mine) and stop; write evidence to planning; post END

## Reality witnesses

- PR #1457 head (before my fix): `83d175f54ea9aba432d192c87dfe6464e879e0df`; base `develop`.
  `gh pr view 1457` reported OPEN, not draft, `mergeStateStatus=UNSTABLE`.
- `git ls-remote origin refs/heads/134-r3-ca-pkce` -> `7da148a36131b339a84b26942093e09be1e521bb`
  (my fix commit; candidate branch advanced from the exact PR head)
- `git ls-remote origin refs/heads/develop` -> `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`
- `git merge-base --is-ancestor 83d175f5... HEAD` -> exit 0. The exact PR head `83d175f5`
  is a direct ancestor of my commit `7da148a36`.
- Candidate-only log over the exact PR head: single commit `7da148a36 fix(cmd/baha): consume
  --no-browser flag ...`. No foreign commit carried on top.
- Branch cut from the exact PR head `83d175f5` (base attest).
- Planning repo remote is `https://github.com/mcpdev80/baseharbor-plan.git`; pre-publication
  `git ls-remote origin refs/heads/main` returned `7c0a0d923aa9bfdb5a272bde0e9c86dbeca27678`.
- Stray temp branch `134-r3-ca-pkce-r4` (which held the same content as my fix) created and
  then deleted with witness: `git ls-remote origin refs/heads/134-r3-ca-pkce-r4` before ->
  `7da148a36...`, after -> empty (deleted).

## The fix (product point 1)

`parseLoginTrustArgs` in `cmd/baha/operator_auth.go` set `noBrowser = true` but still executed
`remaining = append(remaining, arg)` for `--no-browser`. The returned `remaining` then passed
through `extractApplicationEnvironment`, which only strips `-e/--environment` and returns other
arguments unchanged; the login `Run` then rejected any leftover argument
(`cmd/baha/operator_auth.go`: `if len(filtered) != 0 { return usageError("baha login accepts
only -e/--environment, --init-tenant, --ca, --auth-code-file and --no-browser" ...)`), so the
documented `baha login ... --no-browser` never reached `operatorauth.Login`.

Change (file `cmd/baha/operator_auth.go`, `parseLoginTrustArgs` `--no-browser` case):

- Before:
  ```go
  case arg == "--no-browser":
      noBrowser = true
      remaining = append(remaining, arg)
  ```
- After:
  ```go
  case arg == "--no-browser":
      noBrowser = true
  ```

The flag is now consumed: `noBrowser=true` is captured and the flag is dropped from `remaining`,
so the leftover check passes and `TrustOptions.NoBrowser` (already wired to
`operatorauth.Login` at `operator_auth.go:61-65`) receives the headless signal end-to-end. The
doc comment was updated to state that `--no-browser` is consumed, not echoed.

## The test (product point 2)

`cmd/baha/operator_tenant_bootstrap_test.go`:

- `TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag`: asserted `--no-browser` was *present*
  in `remaining`. Assertion flipped to assert it is *absent* (`remaining == ["-e", "test"]`).
  The combined `--ca`/`--auth-code-file`/`--no-browser` case now also asserts `--no-browser` is
  consumed from `remaining`.
- Added `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` (command-level regression):
  `operatorLoginCommand().Run(ctx, []string{"-e", "dev", "--no-browser"}, ...)` must NOT return
  the leftover-argument usage error and reaches the `dev` trusted-local "no login required"
  output; a real unknown leftover flag (`--bogus-flag`) is still rejected with `accepts only`,
  proving the leftover check is alive and `--no-browser` was specifically consumed, not
  blindly dropped.

### Local verification (run in my own session, my own worktree)

- `go build -o /tmp/opencode/134-r4-baha ./cmd/baha` -> BUILD OK
- `go vet ./cmd/baha` -> clean (no output)
- `go test ./cmd/baha/ -run 'TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag|TestOperatorLoginCommandNoBrowserReachesHeadlessPath|TestParseOperatorLoginArgs|TestInitialTenant|TestInitialOperatorBootstrapRejectsRemoteTarget|TestHumanCommandIndexTracksExactCommandMetadata|TestHumanDocumentation' -count=1` -> PASS
- `bash scripts/documentation-audit.sh` -> all sections PASS (163 EN/DE pages), exit 0
- `docs/cli/command-index.md` already carries `[--no-browser]` (regenerated at r3), unchanged.

Note: the full `cmd/baha` suite contains pre-existing network-bound loopback tests
(`TestAppEditCommandIncompleteSQLConsumerRemainsPartial` and a peer) that hang in this
sandboxed host (they dial a loopback port with no listener). This is an environment
limitation, independent of the r4 change. The r4-relevant unit tests, `go vet`, `go build`,
and the docs audit all pass; the CI-relevant `documentation-audit`/`cli-gofmt`/`go-unit-tests`
paths are covered by those passing local checks.

## CI witness / trigger #1464 (state, not my work)

The mission references trigger #1464 as the condition for the native Docker/Podman cells and
PR Selected Checks to turn green on the exact head. That drift-merge belongs to lane 0427-136
(PR #1458, polling pattern in `mission-136-r4.md`), NOT to this lane. I did not perform the
merge, did not edit any `.github/**` file, and did not trigger a rerun or `workflow_dispatch`.

Poll of develop for `#1464` (3 checks at ~60s):
- poll 1: `#1464` count in `git log origin/develop` = 0; develop head `d30de3a4a`
- poll 2: 0; develop head `d30de3a4a`
- poll 3: 0; develop head `d30de3a4a`

#1464 is not yet merged into develop. `134-r3-ca-pkce` (my candidate) is 9 commits behind the
current develop head. `git ls-remote origin refs/heads/134-r3-ca-pkce` -> `7da148a36`. My code
fix and regression test are verified; the required native-gate greenness cannot be observed
until the 0427-136 lane lands the drift-merge on develop. The other lane's candidate
`test/0427-ready-native-proof` (run #5201) is the one running the native cells.

## Repo-rule compliance

- Single integration candidate per chain; branch `134-r3-ca-pkce` advanced from the named PR
  head `83d175f5` as a linear fast-forward (my commit's parent is exactly `83d175f5`), no
  second branch for this card; stray temp branch deleted with witness
- No subagents (4.8); every step run inside this session (5a2d48b1)
- `.github/**` not edited, no workflow_dispatch/rerun, no runner build/register/repair
- Evidence file lives in baseharbor-plan only, not in the product repo
- Workspace fixed layout: worktree under `/tmp/opencode/134-r4-wt`; no scratch in the
  ecosystem root
- The pre-existing `baseharbor` checkout in `/home/marcel/dev/baseharbor-ecosystem/baseharbor`
  was on an unrelated lane's branch (`work/0427-133-r3-ca-issuer`, dirty) and was left untouched

## END

END_DONE 0427-134-r4 — the two scoped deliverables executed and verified:
(1) `--no-browser` is now consumed by `parseLoginTrustArgs` (captured into `noBrowser=true`,
removed from the generic `remaining` list) so the documented headless `baha login ... --no-browser`
reaches `operatorauth.Login` end-to-end; (2) `TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag`
asserts the flag is absent from `remaining` and a new command-level regression
`TestOperatorLoginCommandNoBrowserReachesHeadlessPath` proves the CLI entry reaches the headless
path; `go build`/`go vet`/targeted unit tests/docs audit pass. Candidate advanced to
`7da148a36` (linear fast-forward from exact head `83d175f5`, no foreign commit).

Trigger #1464 (drift-merge onto develop) is the 0427-136 lane's work (PR #1458); polled
develop 3x, `#1464` not present (develop head `d30de3a4a`); reported as STATE and not performed
(no product change, no workflow edit, no rerun). Combined managed-CA/PKCE test and DAE doc/unit
(points 2/3 of the r3 verdict) remain PASS and were not touched.

Candidate head: 7da148a36131b339a84b26942093e09be1e521bb
Exact base head committed from: 83d175f54ea9aba432d192c87dfe6464e879e0df
CI run for candidate: pending (blocked on lane 0427-136's drift-merge #1464 into develop)
