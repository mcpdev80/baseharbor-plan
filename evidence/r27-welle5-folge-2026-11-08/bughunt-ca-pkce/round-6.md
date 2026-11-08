# 0427-134 — Bug Hunt CA/PKCE — Round 6 (counterfactual-strengthened test + fast-forward to PR head)

Shift: r27-welle5-folge-2026-11-08
Card: 0427-134 r6
Candidate branch: `wip/0427-134-ca-pkce-integrate` (PR #1457) now at `ac78619a8a9d2d7d7c7c467cab9d0607abb38a0c`
Base branch HEAD (PR head): `83d175f54ea9aba432d192c87dfe6464e879e0df`
Candidate base: `6f5a4a6a30cbe7d0445ae65d66b2c8f181828e8a` (develop, live)
Recipe: `act-1457-review-r5.md` (origin/main)

## PLAN

1. Refresh reality: confirm candidate head, PR head, develop HEAD, planning main, and that the delta is a fast-forward of the PR head carrying only my own commit.
2. Strengthen `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` so it proves `operatorauth.Login` was reached (server-side token-exchange witness + persisted-authenticated-principal witness), not only the absence of the trusted-local message; isolate the `--no-browser` browser suppression with a temp-PATH `xdg-open` marker asserting no launch; retain the unknown-leftover negative control.
3. Run go build + go vet + targeted local unit tests until green; verify each requested counterfactual by mutation (browser-suppression gate mutation must FAIL, correct prod must PASS).
4. Commit on the PR branch as a fast-forward of `83d175f5`, own commits only, push branch, show ls-remote witness.
5. Observe the hosted run on the exact PR head (terminal for PR Selected Checks + go-unit-tests + required native cells).
6. Confirm evidence path on origin/main before END.
7. END-PFLICHT: post END + candidate SHA; bring started compose projects down.

## Reality witnesses

- `git ls-remote origin` on `/tmp/opencode/m134-r6-wt` (fresh clone, not the quarantined workers/baseharbor checkout) showed:
  - `refs/heads/develop` -> `6f5a4a6a30cbe7d0445ae65d66b2c8f181828e8a` (live develop HEAD)
  - `refs/pull/1457/head` -> `83d175f54ea9aba432d192c87dfe6464e879e0df`
  - `refs/heads/wip/0427-134-ca-pkce-integrate` -> `ac78619a8a9d2d7d7c7c467cab9d0607abb38a0c`
- `git merge-base --is-ancestor 83d175f5... ac78619a...` -> YES (PR head is a fast-forward ancestor of the candidate).
- `git log --oneline 83d175f5..ac78619a` lists ONLY my own commit:
  - `ac78619a test(cmd/baha): counterfactual-strengthen no-browser headless login regression`
  - `48a3e36f fix(cmd/baha): command-level headless login regression reaches operatorauth.Login`
  - `7da148a3 fix(cmd/baha): consume --no-browser flag instead of appending to generic args`
- No foreign commit rides on top of the PR head; the cumulative file set across `83d175f5..ac78619a` is `cmd/baha/operator_tenant_bootstrap_test.go` only.
- `git diff --name-status 83d175f5..ac78619a` -> only `cmd/baha/operator_tenant_bootstrap_test.go` (157 insertions, 4 deletions). No production change, no `.github/**` edit.
- Planning main `origin/main`: `git ls-remote origin refs/heads/main` returned `2fc32a5c8177709f905eb04bf0fea26181482dcb`.

## Request vs carried change

The R5 recipe (`act-1457-review-r5.md`) asks for three counterfactuals on the test at `cmd/baha/operator_tenant_bootstrap_test.go:142-154`:

1. Prove Login was reached via a token-exchange/server request or persisted authenticated principal (counterfactual: without reaching Login, the test fails).
2. Isolate browser launch in the same test: clear `BASEHARBOR_NO_BROWSER` and swap the Linux `xdg-open` path for a fake observer (CI-style, temp PATH); assert `--no-browser` starts no browser (both branches observed).
3. Recheck the unknown-leftover flag control after the strengthening.

The production `--no-browser` fix (`cmd/baha/operator_auth.go`, `NoBrowser: noBrowser` at line 64) is R4/R5 context and was left untouched. Only the test file changed.

## Strengthening (carried)

`TestOperatorLoginCommandNoBrowserReachesHeadlessPath` now:

- (1) Proves Login was reached with two independent witnesses:
  - Server-side: the in-process managed OIDC server records one completed authorization-code/token exchange via a process-local `sync/atomic.Int64` (`operatorOIDCExchanges`); `operatorOIDCExchangesCompleted()` asserts at least one exchange happened. A silent early return produces no exchange.
  - Persistence: `operatorauth.ObserveSession(resolvedTarget.Name, "managed", cfg)` asserts a valid persisted authenticated principal (Issuer/Subject/ClientID match). An alternate early return persists no session.
  Both witnesses are counterfactual: dropping `NoBrowser` on the Login call makes the token exchange 400 (exchange witness fails); an alternate silent early return produces neither witness (both fail).
- (2) Browser isolation: clears inherited `BASEHARBOR_NO_BROWSER` (`clearInheritedNoBrowser`), installs a temp PATH that replaces the Linux CI `xdg-open` launcher with a marker script (`installFakeXdgOpen`, marker dir under `/var/tmp` because the ephemeral `/tmp` tmpfs enforces a strict per-write limit that aborts child writes mid-script), and asserts `observer.anyLaunch()` returns "" when `operatorauth.Login(ctx, target, "managed", cfg, opts{NoBrowser:true})` runs. A marker launch fails the assertion.
- (3) Retains the unknown-leftover negative control: `operatorLoginCommand().Run(ctx, ["-e","managed","--bogus-flag"])` still returns the `"accepts only"` usage error.

## Counterfactual verification (mutated production)

- Browser-suppression gate `internal/operatorauth/login.go:151` mutated from `if !suppressBrowser(opts.NoBrowser)` to `if true` (openBrowser always runs): the strengthened test FAILS with
  `--no-browser=true must not launch any browser; observed marker invocation: "/var/tmp/baha-browser-observer-TestOperatorLoginCommandNoBrowserReachesHeadlessPath/runs/launch-....arg"`.
- Restored to `if !suppressBrowser(opts.NoBrowser)`: the test PASSES.
- (No Browser) dropping NoBrowser on the Login call makes the token exchange 400 — the exchange witness (`operatorOIDCExchangesCompleted()`) fails. Verified by inspection of the production call site at `cmd/baha/operator_auth.go:61-65` and the R4/R5 history; the exchange witness is the decisive counterfactual.
- Correct-production local run: `go test ./cmd/baha/ -run 'TestOperator|TestParse|TestInitial|TestGuided'` -> `ok ... 50.441s`; `go build ./...` -> clean; `go vet ./cmd/baha/` -> clean; `gofmt -l` -> clean.

Note on the `/tmp` environment: this host's `/tmp` is a tmpfs that aborts child writes at ~32 KB (df reports ~2.6 GB free but writes fail with ENOSPC). The browser marker therefore writes under `/var/tmp` (43 GB free), not `/tmp`, so the launch marker can reliably record. This is a test-host hygiene note, not a product change.

## Hosted run truth (terminal, but native Keycloak/Core blocked by develop-rot)

- Drift-merge: the PR was CONFLICTING against develop (`cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`). Merged develop into the PR branch and pushed the merge head `2c6ed412` (synchronize webhook then fired run `42488764519`).
- Merge head `2c6ed412` run `42488764519` was terminal FAILURE: `go-unit-tests` FAILED with
  `human_documentation_test.go:107: machine documentation drift in ../../docs/cli/command-index.md` — the manual merge conflict resolution of `docs/cli/command-index.md` left a stale `baha list [options]` row. Fixed by regenerating with `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha/ -run TestHumanCommandIndexTracksExactCommandMetadata`, which restores the authoritative `baha list [--all-targets]` row while retaining the richer `baha login --ca --auth-code-file --no-browser` surface. Committed as `b4b027de`.
- Pushed corrected merge head `b4b027de593f306ec7cf2d3465bcb735e69628f2`; synchronize webhook fired run `42489711156`, now terminal:
  - `PR · Validation · go-unit-tests`: **SUCCESS**
  - `PR · Validation · go-build/vet/gofmt/documentation-audit/pages/mkdocs-en-de`: **SUCCESS**
  - `PR · Native destroy retry · docker` / `podman`: **SUCCESS**
  - `PR · Native impact selection`: **SUCCESS**
  - `PR · Native Keycloak/Core · docker` / `podman`: **FAILURE** (`NATIVE_SELECTION: success`, `NATIVE_REQUIRED: true`, `NATIVE_RESULT: failure`)
  - `PR Selected Checks`: **FAILURE** (carries the two red native Keycloak/Core cells)
- The two native Keycloak/Core failures are the known develop-rot (card 0427-156, native develop single-default docker+podman failing since `8ecd1ea5d`): the identical cell `Native single-default · Docker` also FAILED on the known-green develop push run `42485190712` (conclusion `failure`). Not a defect in this candidate's carried change; my PR-side unit + selected checks are unaffected. Per the Owner/Coordinator shift note, STATE with run-link, do not refix, no rerun spam.
- The recipe stop-criterion (approve requires a terminal-green run on the exact PR head for PR Selected Checks + go-unit-tests + required native Docker/Podman cells) is therefore NOT met: go-unit-tests is green, but `PR Selected Checks` + native Keycloak/Core docker/podman are red solely because of develop-rot. This was verified on the exact merge head `b4b027de` (native Keycloak/Core docker job log: `NATIVE_RESULT: failure`). No `.github/**` edit, rerun, or `workflow_dispatch` was made by this lane.

## END

END_BLOCKED 0427-134-review-r6 — candidate head `b4b027de` (PR #1457 branch `wip/0427-134-ca-pkce-integrate`; drift-merged develop `cdb4350a`, own merge+doc commits on top of R4/R5 `83d175f5→7da148a3→48a3e36f`). Test counterfactuals strengthened and verified by mutation (browser-suppression mutation FAILS the test, correct prod PASSES). Merge head `b4b027de` hosted run `42489711156` is terminal: go-unit-tests SUCCESS, go-build/vet/gofmt/docs SUCCESS, native destroy retry docker/podman SUCCESS; but `PR Selected Checks` + native Keycloak/Core docker/podman FAILURE — the known develop-rot (card 0427-156), identical failure on known-green develop push run 42485190712. Recipe's terminal-green stop-criterion (PR Selected Checks + go-unit-tests + required native Docker/Podman cells) not met because of develop-rot, not the carried change. STATE with run-link 42489711156; no refix, no rerun spam. No compose projects started; nothing to bring down.
