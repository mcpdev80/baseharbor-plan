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
- Grounding: planning-Remote (ls-remote origin/main) + Base-Attestation develop HEAD; Mission + Task-Note gelesen
- Code-Analyse: OIDC-Discoverypfad (operatorauth/login.go, auth/oidc.go), Bootstrap, CA-Ablage, node add Flow, CI-Job-Gruppe
- Implementieren CA-Trust: --ca Flag + BASEHARBOR_OPERATOR_OIDC_CA_FILE env; atomarer CA-Write beim Bootstrap in <state-dir>/trust/managed-operator-ca.pem; RootCAs-Pool (add-only); Fail-Text nennt Pfad
- Implementieren Headless-PKCE: fixed port (BASEHARBOR_OPERATOR_OIDC_CALLBACK_PORT) Ende-Ende; auth-URL + callback-URL drucken; --auth-code-file + --no-browser/--BASEHARBOR_NO_BROWSER; --init-tenant ohne Echttymilling
- Unit/Regression Tests (CI-Pflicht) für CA-Transport-Pool + headless callback completion
- Docs: documented headless flow (login + node add)
- Local checks: go test ./internal/operatorauth ./internal/auth ./cmd/baha; go vet; go build
- Evidence commit + push origin/main; ls-remote witness
- Cleanup: residuales managed core auf baha-podman-2 via PTY destroy; docker/podman ps-witness
- END an 594fd2f5-4e80-43b6-9841-92879146a85e posten

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

## END
_(to be filled: SHA + CI terminal + ls-remote + host cleanliness)_
