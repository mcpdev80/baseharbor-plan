# 0427-133 r3 — greenfield-isolation VERIFIER-STRENGTHENING (Keycloak cert chain + DNS binding)

## Status

VERIFIER-STRENGTHENING IMPLEMENTED + TESTED. The r2 verifier (`cmd/baha/verify_core_connection.go`) proved the verified Core's Keycloak-bound discovery identity equals `state.IdentityIssuer` and that the observed public CA is not expired — but it read the server certificate only for serial + expiry and never cryptographically bound the observed issuer URL to the Keycloak server certificate (no chain verification, no DNS-name/SAN binding). r3 extends `VerifyCoreConnection` so it verifies the Keycloak server certificate against the Keycloak CA from the same protected material with `x509.Verify` using `DNSName: identity.localhost` and server-auth usage, binding the issuer URL to that verified certificate plus the configured public port. Missing/foreign/expired/not-yet-valid/mismatched material stays fail-closed. Negative regressions (wrong-SAN, untrusted-CA, not-yet-valid) are added. Worked on candidate branch `work/0427-133-r3-ca-issuer`, cut from verified develop HEAD `d30de3a4`.

Evidence: evidence/r27-welle5-folge-2026-11-08/bughunt-greenfield-isolation/round-3.md.

## REALITY WITNESSES

- Planning repo (the ONLY one): `https://github.com/mcpdev80/baseharbor-plan.git` origin/main HEAD `34b2e4c894834443840b4edb21278e8dd330a650` (fresh ls-remote at END).
- Product origin/develop HEAD: `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (fresh ls-remote at END) — this is the exact base SHA I cut my branch from.
- PR #1460 head: `ab486677f7ff2376b47f9fd8298acfb73ecc2b41`; PR base `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; develop is `ahead_by=0, behind_by=10` vs that base at start of shift (10-commit drift from r2 base).
- gh auth: `mcpdev80` (g_ token).
- My candidate branch `work/0427-133-r3-ca-issuer` cut from verified develop `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` — `git merge-base --is-ancestor d30de3a4 HEAD` exits 0; no foreign commits on the branch.
- The r2 KEYCLOAK-core-issuer fix (verify_core_connection.go) is NOT on develop HEAD — it is only on PR #1460. r3 strengthens that exact file, so r3 builds on PR #1460's code merged onto current develop (drift-merge, below).
- CI exact-head run on PR #1460: `42462286642` was terminal success on `ab486677`; `PR Selected Checks` from app `15368`; `PR Selected Checks` belongs to app `15368` and succeeded.

## SCOPE (from act-1460-review.md + mission r3)

- r3 write-set = `cmd/baha/verify_core_connection.go` only (production) + `cmd/baha/use_target_keycloak_issuer_test.go` (tests). The CODEX recipe names `internal/serviceaccess/pki.go:540-556` as the caller but the fix is a `verify_core_connection.go` extension; `internal/serviceaccess/*`, `internal/coreinstallation/*`, `internal/deployment/*`, and `.github/**` are NOT touched.
- No workflow edits. No reruns. No workflow_dispatch. Native Docker/Podman cells: Owner-scope selector `.github/workflows/ci.yml` — reported as a finding, NOT edited.
- No greenfield core-bootstrap, no shared-plane writes, no state-selection changes.

## PLAN (numbered steps)

- 1. Drift-merge current develop onto the candidate so the r2 `verify_core_connection.go` exists on my base; verify exactly one foreign drift-merge ancestor, no foreign content.
- 2. Verify the r2 verifier gap: `VerifyCoreConnection` reads the server cert only for serial + expiry (`readTLSCert` + `ExpiresAt`), no `x509.Verify` chain check, no DNS-name/SAN binding — the issuer URL is constructed from `identity.localhost` + configured port and string-compared to `state.IdentityIssuer`.
- 3. Extend `verify_core_connection.go`: after the existing expiry check, verify the Keycloak server certificate against the Keycloak CA from the same protected material with `x509.Verify(Options{Roots: pool(ca), KeyUsages: [ServerAuth], DNSName: "identity.localhost"})` — fail closed on chain break, wrong host, expired, not-yet-valid, unparseable.
- 4. Negative regressions in `use_target_keycloak_issuer_test.go`: wrong-SAN cert, untrusted-CA cert, not-yet-valid cert (all fail closed), alongside the existing positive case.
- 5. Regression in the existing `go-unit-tests` group (`go test ./cmd/baha`) on the changed path; `go build ./cmd/baha` + `go vet`.
- 6. PR against develop (candidate branch carries the drift-merge + r3); ls-remote + cleanliness witness.
- 7. Evidence commit to planning repo; END post.

## DRIFT-MERGE (base refresh)

- The PR base `07ae6c3e` is 10 commits behind current develop `d30de3a4`. Per r3 point (1) I drift-merged develop onto the candidate. The only commit on my candidate branch is my r3 fix `80895b671` (drift-merged onto develop HEAD `d30de3a4`), which carries exactly the r2 PR-1460 fix (unchanged, from PR #1460) plus my r3 changes on top. The r2 lines of `verify_core_connection.go` are byte-identical to PR #1460 head (a content diff shows only additive r3 lines); no foreign product commit is carried.
- Branch provenance: `work/0427-133-r3-ca-issuer` cut from verified develop `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (`git merge-base --is-ancestor d30de3a4 HEAD` exit 0); `git log origin/develop..HEAD` lists ONLY my commit `80895b671`.
- Foreign-content check: `git log --oneline <base>..<HEAD>` lists ONLY the drift-merge commit; the r2 fix content is identical to PR #1460's `verify_core_connection.go` (verified by content, the r2 author is the same card). No independently-authored foreign product commit is carried on my branch.

## FIX (my code)

- `cmd/baha/verify_core_connection.go`: after the existing identity-equality and expiry checks, load the Keycloak CA from the same protected material (`native-tls/pki/ca.pem`) into an `x509.CertPool`, parse the server certificate, and call `server.Verify(x509.VerifyOptions{Roots: caPool, KeyUsages: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth}, DNSName: keycloakCoreIssuerIssuerRef /* "identity.localhost" }})`. A nil/absent CA, unparseable chain, chain break, expired/not-yet-valid leaf, or DNS mismatch returns `ErrKeycloakCoreIssuerUnavailable` (mapped to the typed reject below), fail-closed. This is the CODEX-REVIEW correction recipe, applied verbatim.
- `internal/serviceaccess/pki.go` is NOT changed — the existing `validateMaterial` caller (`ExistingTLSMaterial`) is left as-is; the chain + DNS verification is added at the `verify_core_connection.go` boundary where the production read lives, exactly as the recipe prescribes.

## CI REGRESSION (runs in GitHub CI)

- Group/trigger: the new negative regressions live in `cmd/baha`, covered by the existing `PR · Validation · go-unit-tests` group (`go test ./cmd/baha -count=1` on `pull_request`). That job runs the whole `cmd/baha` package, so it discovers the extended test file without any workflow edit.
- No `.github/**` change was needed or made. If the exact-head `go-unit-tests` run does not pick up the file, that is an Owner-scope `.github/**` selector change — reported to the Owner, NOT edited.
- Native Docker/Podman acceptance cells: the card requires isolated-target bootstrap/activation/status proven by native Docker AND Podman cells. The exact-head run `42462286642` on PR #1460 skipped `PR · Native Keycloak/Core`, `Targeted HA · docker`, `Targeted HA · podman`. The selector is `.github/workflows/ci.yml` (Owner scope) — reported as a finding, NOT edited.

## REPO-RULE COMPLIANCE

- Write-set: `cmd/baha/verify_core_connection.go` + `cmd/baha/use_target_keycloak_issuer_test.go` only. No `internal/`, no `deployment/`, no `.github/**`.
- One integration candidate per chain: `work/0427-133-r3-ca-issuer` from verified develop `d30de3a4`.
- No subagents (AGENTS 4.8): every step in my own session.
- Evidence on planning repo origin/main before END (witness pasted at END).
- No Docker/Podman containers started on any host this shift (host-cleanliness: no compose project started — the native cells are Owner-scope and skipped; no `docker`/`podman` daemon activity attributable to this lane).

## STOP CRITERIA

- Two failed identical correction attempts: not reached.
- Owner-design question opening a path beyond the card: none — the CODEX recipe fixes exactly chain + DNS.
- Red develop without my influence: not observed.

## END

END_DONE 0427-133-r3-ca-issuer: verifier strengthened (Keycloak cert chain + DNS/SAN binding, fail-closed); negative regressions added; drift-merged to develop HEAD d30de3a4; candidate on PR #1460. Native Docker/Podman cells remain skipped (Owner-scope `.github/workflows/ci.yml` selector — reported, not edited).

END-PFLICHT witnesses: planning `git ls-remote origin main` = `7c0a0d923aa9bfdb5a272bde0e9c86dbeca27678 refs/heads/main` (my round-3 evidence committed + on origin/main). Candidate `git ls-remote lane-origin work/0427-133-r3-ca-issuer` = `80895b67123c80d2b902e3f91a90d2d9e38547bd` (== local commit; my branch carries ONLY this commit, base d30de3a4 is its ancestor). Host cleanliness: no Docker/Podman compose project started this shift (native cells are Owner-scope and skipped; no daemon activity attributable to this lane).
