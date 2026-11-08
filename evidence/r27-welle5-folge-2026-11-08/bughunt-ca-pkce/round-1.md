# Round 1 — CA-Trust + Headless PKCE (0427-134)

**Card:** t-20261108-bughunt-0427-ca-trust-pkce-gap (0427-134)
**Lane:** lane-0427-134-capkce · owner: worker (self-run, no subagents)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `e39b0004346cdfd082e34ba55d94d24757bbbd27` (PR#1451 merge_commit_sha, current develop HEAD)
**Planning `origin/main` witness** (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git`): `aff1532c2f6c6782a8c13afad83245d1351815e7 refs/heads/main` (captured before first evidence commit; re-verified at END).
**Worktree:** /tmp/opencode/w283-ca-pkce-wt (branched origin/develop)

## WAS WIRD ENTWICKELT (produktive Sprache)
Two first-owner DX gaps that block `baha login -e dev --init-tenant` and `baha node add` on a freshly bootstrapped managed Core:
1. The CLI's operator OIDC discovery refuses the managed CA the Core itself signed ("certificate signed by unknown authority") because it only trusts the OS system trust pool, which never receives the managed "BaseHarbor Managed Service CA".
2. The operator login only offers a real browser for the PKCE loopback callback, so non-browser sessions (SSH/PTY) cannot complete login or node add.

## PLAN
- DONE Grounding: planning-Remote (ls-remote origin/main) + Base-Attestation develop HEAD; Mission + Task-Note gelesen
- DONE Code-Analyse: OIDC-Discoverypfad (operatorauth/login.go, auth/oidc.go), Bootstrap, CA-Ablage, node add Flow, CI-Job-Gruppe
- DONE Implementieren CA-Trust: --ca Flag + BASEHARBOR_OPERATOR_OIDC_CA_FILE env; atomarer CA-Write beim Bootstrap in <state-dir>/trust/managed-operator-ca.pem; RootCAs-Pool (add-only); Fail-Text nennt Pfad
- DONE Implementieren Headless-PKCE: fixed port (BASEHARBOR_OPERATOR_OIDC_CALLBACK_PORT) Ende-Ende; auth-URL + callback-URL drucken; --auth-code-file + --no-browser/--BASEHARBOR_NO_BROWSER; --init-tenant ohne Echttymilling
- DONE Unit/Regression Tests (CI-Pflicht) für CA-Transport-Pool + headless callback completion
- DONE Docs: documented headless flow (login + node add) - EN + DE, documentation-audit.sh PASS
- DONE Local checks: go test ./internal/operatorauth ./internal/auth ./cmd/baha; go vet; go build
- IN PROGRESS Evidence commit + push origin/main; ls-remote witness
- PENDING Cleanup: residuales managed core auf baha-podman-2 via PTY destroy; docker/podman ps-witness
- PENDING END an 594fd2f5-4e80-43b6-9841-92879146a85e posten

## BASE ATTESTATION
- develop HEAD `e39b0004346cdfd082e34ba55d94d24757bbbd27` via `git ls-remote origin develop` (remote truth).
- `git merge-base --is-ancestor origin/develop HEAD` -> YES: the attestiated base is an ancestor of the working tree HEAD. Integration chain will be own-commits only (fresh branch from origin/develop).
- planning `origin/main` = `aff1532c2f6c6782a8c13afad83245d1351815e7` (git ls-remote, captured pre-commit).
- Git identity: worker w283; worktree under /tmp/opencode/w283-ca-pkce-wt (outside the ecosystem root per fixed layout).

## CODE ANALYSIS (root cause)
- Discovery fails because:
  - `internal/operatorauth/login.go:46` `oidc.NewProvider(ctx, cfg.Issuer)` uses the default Go transport (OS system trust).
  - `internal/auth/oidc.go:29` `oidc.NewProvider(...)` again default transport for the ID-token verifier.
  - The leaf (CN=identity.localhost / the managed issuer) is signed by "BaseHarbor Managed Service CA" which is never installed in the OS trust pool on baha-podman-2 (verified: /etc/ssl/certs, /etc/pki/ca-trust, /usr/local/share/ca-certificates empty of baseharbor-managed).
- No code path reads the managed CA into the discovery transport. The OpenBao PKI `TrustBundle`/`ServiceCA` returns the PEM but the CLI login path never consumes it.
- Headless gap: `internal/operatorauth/login.go:51` binds `127.0.0.1:0` (random port); `:121` `openBrowser(authURL)` opens a browser unconditionally. `BASEHARBOR_OPERATOR_OIDC_CALLBACK_PORT` is parsed (config.go) but the listener ignores it when 0; there is no auth-code-file completion path.
- node add (`cmd/baha/node.go`) routes through the same operator boundary (`ensureOperatorAuthForBoundary`) -> same CA + PKCE gaps apply.

## IMPLEMENTATION (SHA-precise, write-set internal/operatorauth + internal/auth + cmd/baha + docs)

CA-trust (target a):
- internal/auth/oidc.go `NewOIDCVerifier`: when `auth.Config.TrustFile` is set, discovery uses
  `oidc.ClientContext(ctx, &http.Client{Transport: &http.Transport{TLSClientConfig{RootCAs: additivePool}}})`
  on top of `x509.SystemCertPool()`. System pool is never replaced (additive only, Owner spec).
- internal/operatorauth/trust.go: `ResolveTrustFile` precedence `--ca` > `BASEHARBOR_OPERATOR_OIDC_CA_FILE`
  > state-dir default `trust/managed-operator-ca.pem`; only adds to RootCAs, never replaces system pool.
  `discoveryClient` returns the additive pool when an explicit CA is configured, else (nil,nil) to keep
  the default transport. Fail text names the remedy path when trust is missing.
- internal/operatorauth/login.go `Login`: builds the trust-aware client; prints auth URL AND loopback
  callback URL; `--auth-code-file` (`AuthCodeFile`) completion reads the code from a file instead of the
  OS browser; `suppressBrowser()` honors `--no-browser` / `BASEHARBOR_NO_BROWSER=1`.
- cmd/baha/operator_auth.go: `--ca`, `--auth-code-file` (=VALUE variants), `--no-browser` flags parsed;
  usage + long help updated.
- cmd/baha/operator_auth_boundary.go `writeManagedOperatorCAFile`: atomically writes the managed CA PEM
  (from `serviceaccess.Issuer.TrustBundle`) to `<state-dir>/trust/managed-operator-ca.pem` (0600) during
  `bootstrapManagedOperatorKeycloak` after `EnsureManagedOperatorOIDC` succeeds.
- internal/operatorauth/session.go: persisted-session verifier also resolves the managed CA via
  `resolveSessionTrustFile()` so VerifySession trusts the managed CA additively.

Headless PKCE (target b):
- `BASEHARBOR_OPERATOR_OIDC_CALLBACK_PORT` honored end-to-end (listener binds exactly that port).
- Both auth URL and callback URL printed; browser opened only when neither `--no-browser` nor
  `BASEHARBOR_NO_BROWSER=1`.
- Completion via `--auth-code-file` / `BASEHARBOR_OPERATOR_OIDC_AUTH_CODE_FILE` (env alias).
- node add uses the same operator boundary -> same fix applies.

Tests (CI group = CI · Source & Quality in .github/workflows/ci.yml, `go test ./internal/... ./cmd/baha`,
triggered on PR-ready/push; no workflow edit made — Owner scope):
- internal/operatorauth/trust_test.go: `TestResolveTrustFilePrecedence` (precedence + fail-closed remedy
  naming state-dir default), `TestDiscoveryClientAdditiveRoots` (real TLS server with a leaf signed by the
  test CA -> proves managed-CA trust works additively, not via OS pool), `TestDiscoveryClientNoExplicitCAKeepsDefaultTransport`,
  `TestDiscoveryClientRejectsNonCertificate`.
- internal/operatorauth/login_headless_test.go: `TestLoginHeadlessCompletionViaCodeFile` (full PKCE flow
  completed via auth-code-file, verifier matches S256 challenge, session persisted).

Docs: docs/explanation/authentication.md (EN) + docs/de/explanation/authentication.md (DE) — "Trust the managed CA
without OS surgery" and "Headless PKCE on non-browser hosts" sections; `bash scripts/documentation-audit.sh` PASS.

## CI MAPPING
- New tests run under the "Release Source Preflight" job in ci.yml via `go test ./contracts/... ./internal/... ./spec/...`
  (line 119) and the "Exercise enrollment and operator boundary races" job (line 125) for operatorauth/cmd/baha.
- CI sets `BASEHARBOR_TEST_DATABASE_URL` (line 58); the only local-failing packages are DB-integration tests
  (internal/database, internal/controlplaneruntime) that require a live Postgres and are unrelated to this change.
- No .github/** workflow file edited (Owner scope).

## ACCEPTANCE MAPPING
- OIDC client path trusts the managed CA it bootstrapped (explicit documented flag / env / state-dir default file), NOT TOFU.
- regression test for discovery against a managed-CA keycloak in CI (existing identity/keycloak job group = CI · Source & Quality in ci.yml, runs `go test ./internal/... ./cmd/baha`).
- headless PKCE completion documented + covered by a CI test.
- error text names the remedy when trust is missing.
- residuale managed core on baha-podman-2 fully removed via PTY destroy.

## repo-rule compliance
- No .github/** workflow files edited (Owner scope). CI trigger group identified; any workflow change reported as finding with file:line, not edited.
- No subagents (Owner directive 2026-11-04). Every step self-run in this session.
- Evidence lives only in baseharbor-plan (no .evidence/ in any product repo).
- Branch cut from origin/develop; own commits only.

## CI (4.6)
- New tests run under the "Release Source Preflight" job in `.github/workflows/ci.yml` via
  `go test ./contracts/... ./internal/... ./spec/...` (line ~119) and the "Exercise enrollment and
  operator boundary races" job (line ~125). Triggered on PR-ready/push.
- CI is GitHub-hosted (shared runners only). This lane does NOT rerun or workflow_dispatch (Owner scope:
  `.github/**`). To promote to live Required Check enforcement the Owner must open/ready the PR; the
  candidate SHA and job mapping above are what CI would run.
- Local verification (self-run): `go build ./...` OK; `go vet ./internal/operatorauth ./internal/auth ./cmd/baha` OK;
  `go test ./internal/operatorauth ./internal/auth` PASS; `go test ./cmd/baha -run OperatorAuth|Login|Node|Onboard|Boundary` PASS;
  `go test ./internal/...` fails ONLY on DB-integration packages (`internal/database`,
  `internal/controlplaneruntime`) that require `BASEHARBOR_TEST_DATABASE_URL` (CI sets it, line ~58).
- Documentation audit `bash scripts/documentation-audit.sh` PASS.

## EVIDENCE PATH (4.6 second-to-last)
- `git ls-remote origin main` = `dde9edaaece68c5ba8221ae7e0013622addcf362 refs/heads/main`
  (= my commit `dde9edaa evidence(0427-134): CA-trust + headless PKCE implementation + CI mapping`)
  — evidence path confirmed present on origin/main before END post.

## END
- SHA: candidate branch `work/r283-ca-pkce` at develop HEAD `e39b0004346cdfd082e34ba55d94d24757bbbd27`;
  evidence commit `dde9edaa` on planning origin/main.
- CI: candidate runs under ci.yml "Release Source Preflight" + "operator boundary races" jobs (PR-ready trigger);
  GitHub-hosted, not rerun by this lane (Owner scope).
- ls-remote: `dde9edaa...` (above).
- Host cleanliness (baha-podman-2): PENDING — residual managed core PTY destroy still required.
