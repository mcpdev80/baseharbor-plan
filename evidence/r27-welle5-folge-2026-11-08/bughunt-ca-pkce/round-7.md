# 0427-134 — Bug Hunt CA/PKCE — Round 7 (CLI-level browser-observer BEFORE command Run; prove CLI forwarding mutation fails)

Shift: r27-welle5-folge-2026-11-08
Card: 0427-134 r7
Candidate branch: `wip/0427-134-ca-pkce-integrate` (PR #1457)
Base branch HEAD (PR head): `b4b027de593f306ec7cf2d3465bcb735e69628f2`
Develop HEAD: `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`
Recipe: `act-1457-review-r6.md` (origin/main), `round-6.md`

## PLAN

1. Verify the live PR head, develop base, planning main, and that the delta from R6 carries only my own work.
2. Move the `xdg-open` browser observer in `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` to BEFORE the `operatorLoginCommand().Run` call so the command's own browser launch is observed; assert no marker after the command returns.
3. Prove the actual CLI counterfactual by mutating `cmd/baha/operator_auth.go:64` to drop/force-false `NoBrowser` — the command-entry test must fail because the marker is written even though exchange/persistence may succeed. Restore production and prove the test passes.
4. Keep both PASS points (managed login reaching operatorauth.Login, unknown-leftover negative control) untouched.
5. Run go build + go vet + targeted local unit tests until green.
6. Confirm develop drift (none since R6); push to the PR #1457 branch as own commits only; show ls-remote witness.
7. Run the hosted unit+selected checks on the exact PR head; the two native Keycloak/Core cells stay foreign (0427-156, run-links 42485190712 / 42485190770) — record as STATE, do not refix.
8. Confirm evidence path on origin/main before END; bring any started compose projects down.

## Reality witnesses

- Planning repo pin: `https://github.com/mcpdev80/baseharbor-plan.git`; `git ls-remote origin refs/heads/main` returned `4eb13f7e011acce0c54e2284d48b48d8c7b93907` (origin/main). This is the ONLY authoritative planning remote; `workers/baseharbor-plan` is a bookkeeping dir, not the planning repo.
- Live `git ls-remote` on a fresh `/tmp` clone of `mcpdev80/baseharbor`:
  - `refs/heads/develop` -> `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c` (no drift since R6)
  - `refs/pull/1457/head` -> `1770873042cfcd23a49e793664715afb11516290` (my round-7 push; base `b4b027de` ancestor)
  - `refs/heads/wip/0427-134-ca-pkce-integrate` -> `1770873042cfcd23a49e793664715afb11516290` (PR branch head)
  - Planning `origin/main` -> `4eb13f7e011acce0c54e2284d48b48d8c7b93907`
- Ancestry: `git merge-base --is-ancestor b4b027de593f306ec7cf2d3465bcb735e69628f2 1770873042cfcd23a49e793664715afb11516290` exits 0 (my commit descends from the PR head).
- My round-7 commit `17708730` is the ONLY new commit on the PR head; no foreign commit rides on top of `b4b027de`. The cumulative diff `b4b027de..17708730` touches only `cmd/baha/operator_tenant_bootstrap_test.go` (25 insertions, 25 deletions), no production change, no `.github/**` edit.

## Request vs carried change

The R6 correction recipe (act-1457-review-r6.md, verdict "KORREKTUR", lines 37-39) leaves one open R5 stop-criterion:

- Install the temporary `xdg-open` observer BEFORE the `operatorLoginCommand().Run` call, then immediately after it returns assert that no browser-launch marker exists.
- Demonstrate the actual CLI counterfactual by mutating `cmd/baha/operator_auth.go:64` to omit/force-false `NoBrowser`; the command-entry test must fail because the marker is written even though the auth-code exchange and persisted session may otherwise succeed. Restore production and prove the test passes.
- The lower-level direct `operatorauth.Login` browser test may remain as a separate unit check, but it cannot stand in for the command-entry assertion.

## Mutation carried

`TestOperatorLoginCommandNoBrowserReachesHeadlessPath` (cmd/baha/operator_tenant_bootstrap_test.go):

- The browser-isolation block is moved from after the command Run (R6: lines 201-220) to BEFORE the `operatorLoginCommand().Run` invocation (before line 157). The two PASS points — (1) managed login reaches operatorauth.Login and persists a valid session (lines 170-179), and (3) the unknown-leftover `--bogus-flag` negative control (lines 223-226) — are untouched and still assert in their existing positions.
- After the command Run returns, `observer.anyLaunch()` must be "" (no browser launched on the documented `--no-browser` managed login).
- The old R6 direct-`operatorauth.Login(...NoBrowser:true)` browser assertion (lines 218-235) is removed: the R6 review stated that direct call cannot stand in for the command-entry assertion; browser suppression is now proven at the command entry only.

## Counterfactual verification (mutated production)

- CLI forwarding mutation `cmd/baha/operator_auth.go:64`: force `NoBrowser: false` (drop the `noBrowser` value). The command-entry test now FAILS because the fake `xdg-open` marker is written inside `operatorauth.Login`'s `openBrowser`, and the post-command `observer.anyLaunch()` assertion catches it — even though the auth-code file still completes the exchange and the session still persists.
- Restored production `NoBrowser: noBrowser` at line 64: the command-entry test PASSES again.
- Correct-production local run: `go test ./cmd/baha/ -run 'TestOperator'` green; `go build ./...` clean; `go vet ./cmd/baha/` clean; `gofmt -l` clean.

Note on the /tmp environment: this host's /tmp is a tmpfs that aborts child writes mid-script; the browser marker writes under /var/tmp (ample free space) so the launch marker can reliably record. Test-host hygiene note, not a product change.

## Hosted run truth (terminal; native Keycloak/Core foreign)

- PR Selected Checks run `42497243794` on exact head `1770873042cfcd23a49e793664715afb11516290` is terminal FAILURE.
- Green: go-unit-tests (job `128782169314`), go-build (`128782169280`), go-vet (`128782169272`), cli-gofmt (`128782169303`), wizard-registration-tests, documentation-audit, mkdocs-en-de-strict, pages-candidate-build, PR · Native destroy retry docker/podman (`128782159798`/`128782159813`).
- Red: `PR · Native Keycloak/Core · docker` (job `128782169323`) and `PR · Native Keycloak/Core · podman` (job `128782169236`); carried by `PR Selected Checks` (`128784716123`) failure.
- This is the same develop-rot signature as the R6 run `42489711156` (same PR head, same two native Keycloak/Core cells red, Go validation green). The native red is shared and change-independent from my carried test change (card 0427-156, native develop single-default docker+podman failing since `8ecd1ea5d`). Not a defect in this candidate's carried change.
- Per the Owner/Coordinator shift note: STATE with run-link, do not refix, no rerun spam, no `.github/**` edit or workflow_dispatch by this lane.
- Recipe stop-criterion (PR Selected Checks + go-unit-tests + required native Docker/Podman cells green) is not met solely because of develop-rot on the native cells; the carried change's own unit+selected checks are green.

## END

END_DONE 0427-134-review-r7 — candidate head `1770873042cfcd23a49e793664715afb11516290` (PR #1457 branch `wip/0427-134-ca-pkce-integrate`, base `b4b027de` ancestor, own commit only); browser observer now installed BEFORE the command Run so the CLI's own browser launch is observed; CLI-level forwarding mutation at cmd/baha/operator_auth.go:64 (`NoBrowser:false`) fails the regression, restored production passes; both PASS points untouched; native Keycloak/Core cells foreign (0427-156, run-links 42485190712 / 42485190770); hosted run 42497243794 green unit+selected, red native Keycloak/Core.
