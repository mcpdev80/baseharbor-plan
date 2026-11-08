# CODEX-REVIEW 0427-134 r2 — PR #1457

## PLAN

1. Verify the live PR head, develop base, candidate ancestry, exact diff, and hosted run.
2. Compare CA discovery, headless PKCE/code-file, callback behavior, and trust precedence with the r1 review recipe.
3. Verify the host-cleanup witness and keep the separate 0427-039 enrollment boundary explicit.
4. Record an actionable verdict, required regressions, CI result, and stop criterion.
5. Publish this review in the Planning Vault and verify its origin/main presence.

## Verdict

**ROLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1457:** OPEN, mergeable  
**Candidate head:** `09030b370c607a818a77cc128322c7b06fffd4f7`  
**develop base:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Hosted run:** `42455848388`, terminal failure on the exact candidate

The candidate now has its own correctly scoped PR and is ancestry-clean against current develop. The host-cleanup evidence is documented. However, the command-line headless path is not wired correctly, the CA and PKCE tests do not prove the combined production login path, and required hosted checks are red.

### 1. Candidate ownership and ancestry: PASS

Live refs identify PR #1457 head `09030b370c607a818a77cc128322c7b06fffd4f7` and `develop` `07ae6c3e91b081a189266ca4b162ba705d4aa78f`. `gh pr view` reports base `develop`, state OPEN, and mergeable. `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 09030b370c607a818a77cc128322c7b06fffd4f7` returned exit 0. `git log --oneline origin/develop..HEAD` contains only the CA/PKCE commit `09030b37`; there is no foreign candidate commit. The diff contains the 13 intended operator-auth, authentication-doc, and test files; it does not include the destroy/data-root files from the mis-scoped #1455 candidate.

### 2. Headless CLI flag is documented but rejected by the production command

`cmd/baha/operator_auth.go:218-224` handles `--no-browser` by appending it to the remaining arguments. The command then sends those arguments through `extractApplicationEnvironment` and rejects any remainder at `:32-37`. The `TrustOptions` passed to `operatorauth.Login` at `:65-68` contain only `ExplicitCaFile` and `AuthCodeFile`; they do not carry a no-browser option. In `internal/operatorauth/login.go:151-153`, browser launch is suppressed only by `BASEHARBOR_NO_BROWSER`. The English and German authentication docs present `--no-browser` as a working CLI flag and call the environment variable its alias. As implemented, the documented flag is not consumed or connected to browser suppression.

**Fix recipe:** In `cmd/baha/operator_auth.go:218-244`, parse `--no-browser` into an explicit boolean, remove it from generic argument parsing, and pass the option to the production login path. In `internal/operatorauth/login.go` (or an equivalent explicit option), use that value to suppress `openBrowser`; keep the environment alias if intended. Add a command-level regression that invokes `baha login ... --auth-code-file ... --no-browser`, verifies the command accepts the flag, and proves no browser opener is called. Stop if the documented invocation is still rejected or tries to launch a browser.

### 3. CA discovery and PKCE code-file tests exist, but do not prove the combined production path

`internal/operatorauth/trust_test.go:91-152` creates a TLS discovery endpoint signed by a managed test CA and calls `discoveryClient`, then performs a direct HTTP GET. It does not invoke `oidc.NewProvider` or production `Login`, so it does not prove that actual OIDC discovery through login uses the additive managed-CA roots.

`internal/operatorauth/login_headless_test.go:25-158` exercises production `Login` with a code file, verifies PKCE S256/state and persisted session, but injects `oidc.ClientContext(ctx, server.Client())` at `:103`, bypassing the managed-CA resolver. It configures `CallbackPort: 0` at `:106`, and does not assert a fixed callback listener or its printed callback URL. The test exercises the library `AuthCodeFile` option, not the advertised `baha login --no-browser` command path.

Source inspection confirms that `Login` calls `discoveryClient` before `oidc.NewProvider` (`internal/operatorauth/login.go:54-65`), and `ResolveTrustFile` orders explicit flag, environment, and state-dir default (`internal/operatorauth/trust.go:92-106`). The resolver's code order is correct, but current tests cover explicit-over-environment and helper-level TLS only; they do not cover the full OIDC login with the managed CA or environment-over-default precedence.

**Fix recipe:** Extend the in-process OIDC fixture so the real `Login` call performs provider discovery, JWKS retrieval, and token exchange over TLS signed only by the managed CA, using `TrustOptions`/the bootstrap-written state-dir CA path rather than an injected `server.Client()`. Complete PKCE from the code file in the same test. Add a configured fixed callback-port case and assert both the bound redirect URI and printed callback URL. Add the CLI invocation test for `--no-browser` described above, and cover `flag > env > default` including environment-over-default. Stop until these regressions fail when the production login skips managed trust or headless handling and pass through the actual command/login path.

### 4. Hosted CI is not green on this candidate

Run `42455848388` is completed with failure on exact head `09030b370c607a818a77cc128322c7b06fffd4f7`. `PR · Validation · go-unit-tests` failed with:

```text
--- FAIL: TestHumanCommandIndexTracksExactCommandMetadata (0.00s)
    human_documentation_test.go:101: machine documentation drift in ../../docs/cli/command-index.md; regenerate from the registry/command tree
```

`PR Selected Checks` also failed with:

```text
BLOCKED: required job did not succeed: pr_validations
```

The same hosted `go-unit-tests` log reports `ok github.com/mcpdev80/baseharbor/internal/operatorauth 0.119s`; therefore the operatorauth package tests were selected and passed in this run. Build, vet, documentation audits/builds, source format, focused Python, and both `PR · Native Keycloak/Core · docker` and `· podman` passed. `validate`, Targeted HA Docker/Podman, and Release Source Preflight were skipped. No rerun or workflow dispatch was started by this review.

**Fix recipe:** Regenerate and commit `docs/cli/command-index.md` from the current command registry/tree so `TestHumanCommandIndexTracksExactCommandMetadata` passes. Then observe the required `go-unit-tests` and `PR Selected Checks` on the corrected exact candidate SHA. Do not treat the passing `internal/operatorauth` package or native runtime jobs as a substitute for the red required checks.

### 5. Scoped host-cleanup witness: documented

`evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/round-2.md`, section “BEFUND 4”, carries the `baha-podman-2` before/after record for the specifically owned `w0427-owner-missing` installation. Before cleanup it records 10 containers and the owned Core volume `bh-w0427-owner-missing-shared_postgres-data-1`; after cleanup it records zero `bh-w0427-*` containers, zero w0427 volumes, and zero w0427 networks. It also records that `podman-local2`, foreign/anonymous volumes, and the ambient `podman` network were left untouched. This satisfies the requested evidence check; this review did not repeat host operations.

### 6. 0427-039 enrollment remains a separate acceptance

As scoped in `evidence/r27-welle5-folge-2026-11-07/node-cli/act-1436-review.md`, CA-trust and operator login do not establish that a bootstrap grant was redeemed or that the authoritative Core enrollment lifecycle is correct. This candidate can unblock the login prerequisite, but this review does not accept or close 0427-039.

## SHA, scope, and run witnesses

- `git ls-remote origin refs/heads/develop refs/pull/1457/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` and `09030b370c607a818a77cc128322c7b06fffd4f7 refs/pull/1457/head`.
- `gh pr view 1457 --repo mcpdev80/baseharbor` reports OPEN, base `develop`, head `09030b370c607a818a77cc128322c7b06fffd4f7`, and mergeable.
- Ancestry check against the exact fetched develop SHA returned exit 0. The candidate-only log contains the single CA/PKCE commit `09030b37`.
- `gh run view 42455848388 --repo mcpdev80/baseharbor --json headSha,status,conclusion` returned `headSha=09030b370c607a818a77cc128322c7b06fffd4f7`, `status=completed`, `conclusion=failure`.
- The failed job was `PR · Validation · go-unit-tests` (`128654600487`); the failed aggregator was `PR Selected Checks` (`128656001892`). Exact failure lines are quoted above.
- Review-only: no product file changed, no test was run locally, no `.github/**` file was changed, and no CI rerun/dispatch or host cleanup was performed.

## Stop criterion

Do not approve until the no-browser command is parsed and used by the production login, the CA-signed discovery and PKCE code-file scenario is proven together through real `Login` without an injected HTTP transport, the fixed callback behavior is asserted, the `flag > env > default` tests cover their stated precedence, and the exact-candidate required `go-unit-tests` and `PR Selected Checks` are successful. Keep 0427-039's Core-authoritative enrollment lifecycle acceptance separate. The recorded host-cleanup witness is adequate and need not be repeated by this review.

## END

END_BLOCKED 0427-134-r2-review — KORREKTUR required; candidate `09030b370c607a818a77cc128322c7b06fffd4f7`; run `42455848388` failed.
