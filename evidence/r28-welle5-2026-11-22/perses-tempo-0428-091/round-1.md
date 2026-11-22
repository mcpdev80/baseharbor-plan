# 0428-091 perses-tempo-source r5 fix — akte

Card `t-20261114-r28-perses-tempo-source`, PR #1645, branch `w091-tempo-r5-fix`. Owner root-cause order (read-only) adopted; two pre-change verifications, then the fix.

## PLAN

- [x] Record plan in board file + ## PLAN in akte
- [x] PRUEFPUNKT 1 (read-only): confirm policy.go position with datei:leile that EnvironmentPolicy{TrustedLocal:true} is the ONLY switch making AuthenticationRequired=false
- [x] PRUEFPUNKT 2: fix is test-only setup line Resolve -> ResolveWithPolicy(TrustedLocal:true) in perses_tempo_source_test.go
- [x] git merge --no-ff acc343239681 on branch (develop head)
- [x] push without force; hosted run to terminal: run-id, failed-count, packages-job-id
- [x] akte with two pruefpunkt sections; END + coordinator post

## Base attestation

- develop head (remote): `acc343239681feb235a33cf00c8ea754c537291f` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- Branch `w091-tempo-r5-fix` head after fix: `8bd165e1a00d25972b55e5b50787091f0aee8f0a` (committed by Marcel Pfingstgräf, "test: use explicit trusted-local policy in neutral gateway check")
- `git merge-base --is-ancestor acc343239681feb235a33cf00c8ea754c537291f HEAD` => develop IS an ancestor of branch head
- `git diff --name-only origin/develop...HEAD` lists only the PR's 35 files (perses_tempo_*.go, pki.go, gateway_reader/http_gateway/perses_compose_realization, issuer.go, tempo.go/tempo_ha.go + testdata). No foreign candidate carried on top.

## PRUEFPUNKT 1 (read-only, before any change) — VERDICT: position confirmed

`internal/serviceaccess/policy.go`, `ResolveWithPolicy` (lines 113-159). The switch:

```
149  switch {
150  case policy.TrustedLocal:
151      // Explicit policy declares this environment operator-trusted: service
152      // authentication stays optional, transport (TLS) remains mandatory.
153      p.AuthenticationRequired = false
154  default:
155      // Managed (or an explicitly untrusted environment): authentication is
156      // required so a name can never silently weaken guarantees...
158      p.AuthenticationRequired = true
159  }
```

- `EnvironmentPolicy{TrustedLocal:true}` is the ONLY switch that sets `AuthenticationRequired = false`. No other code path in `Resolve` / `ResolveWithPolicy` / the PKI material functions produces the same effect: the managed+MTLS `requireClient` path (`pki.go:158,217,305,323,492`) always enrolls a client pair; the dev name via the compatibility `Resolve(dev, cache, MTLS)` wrapper routes over `ResolveWithPolicy(..., EnvironmentPolicy{})` (empty policy => default branch => `AuthenticationRequired=true` => client pair minted).
- The test's own doc comment ("trusted dev / non-RequireClient") names `TrustedLocal:true` as the required authority; the test never supplied it. So the observed client pair for that input is correct production behavior (fail-closed managed) — the bug is the test setup, not the gateway.
- No other path yields `AuthenticationRequired=false` for this input. Position confirmed; fix stays on the test side.

## PRUEFPUNKT 2 (fix) — VERDICT: test-only setup line only

One-line change in `internal/metrics/perses_tempo_source_test.go:407`:

```
-   policy, err := serviceaccess.Resolve("dev", "cache", serviceaccess.AuthenticationMTLS)
+   policy, err := serviceaccess.ResolveWithPolicy("dev", "cache", serviceaccess.AuthenticationMTLS, serviceaccess.EnvironmentPolicy{TrustedLocal: true})
```

`policy.go`, the adapter files, and the adapter commit `4d73aa97` are UNTOUCHED. The gateway behavior stays policy-neutral: the shared-backend valkey TCP gateway now reconciles server-side material only (no client pair), matching the test's pinned contract. Verified: `go test ./internal/metrics/ ./internal/serviceaccess/ -count=1` => both pass (0.582s / 0.110s); `go build ./internal/metrics/ ./internal/serviceaccess/` clean; `go vet` clean. The two production `Resolve("dev", ...)` callers (`cmd/baha/serve_managed_tls.go:162`, `internal/devgateway/gateway.go:409`) keep the managed fail-closed default — unaffected.

## Hosted run (terminal)

- Run `45001605859`, head `8bd165e1` (branch `w091-tempo-r5-fix`), conclusion = **success**.
- Previously failing job `PR · Go unit · packages`: id `137127343932` FAILURE (run 44996055999, head 326ca900) => now id `137144258716` SUCCESS.
- All other Go unit jobs (cli-0/1/2/3, owner) SUCCESS. `PR · Native · ${{ matrix.id }}` SKIPPED (pre-planner develop — STATE finding, same as card 0428-237; not a defeat).
- No .github/** touched; no runner infra touched; no workflow rerun initiated by this lane — CI started from the branch push.

## Cleanliness

`git status` clean in `workers/0428-091-pr-tree` and `workers/0428-091-tempo-wt`; worktrees removed after END. No containers/networks/volumes created. `docker ps -a` (own pid): empty.

## END

`END_DONE w21-pr1702-0428-142-compat: PR1645/0428-091 r5 fix done — head 8bd165e1, run 45001605859 SUCCESS (was 44996055999 FAILURE), packages job 137144258716 success (was 137127343932), policy.go untouched, test-only ResolveWithPolicy(TrustedLocal:true); PRUEFPUNKT1 confirmed EnvironmentPolicy{TrustedLocal:true} is the only switch; PRUEFPUNKT2 test-only; PR draft->review pending CI gate`.
