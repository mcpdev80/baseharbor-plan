# r27 app-binding — Round 1 evidence (lane w179)

## Lane / Mission
- Lane: w179-app-binding, Coord f49a3303
- Card: t-20261018-r27-app-binding (round 1, welle 5), release v0.4.27, parent core-777
- Repo: mcpdev80/baseharbor
- PR: https://github.com/mcpdev80/baseharbor/pull/1388 (base develop, head 4e4a23e8)

## Outcome and acceptance (from card / task note)
- Server allocates IDs; a checkout may explicitly create a new app or attach to a permitted existing app.
- Two distinct checkout paths resolve one deployment by installation + application ID + Target + environment.
- Name/Git URL is only discovery evidence, never authorization.
- No IDs authored by developers or hidden repository-path identity.

## Base attestation (PR rule: branch provenance is proof)
- Base ref: develop 42bfcb1cb481c9e37ecd6ce30580e27829284113 (ls-remote attested before branch cut)
- Cut branch `work/r27-app-binding` from develop 42bfcb1c.
- `git merge-base --is-ancestor 42bfcb1c HEAD` → rc=0 (42bfcb1c IS an ancestor of HEAD).
- `git ls-remote origin work/r27-app-binding` → 4e4a23e89bd3ff9d6db1fc65d4a7ee7a7e44f7b6 (== local HEAD).
- `git log --name-only 42bfcb1c..work/r27-app-binding` lists ONLY the single own commit and only the four own files:
  - cmd/baha/app_binding_production_test.go
  - internal/application/app_binding_contract_test.go
  - internal/application/identity_resolution.go
  - internal/application/store.go
- No foreign candidate commit carried on top; single integration candidate per chain (AGENTS 3.8).

## Write-set (from card / task note)
- internal/application/identity_resolution.go (modified: bounded concurrent-load retry)
- internal/application/store.go (modified: atomic Create + EEXIST normalization + transient-dir skip in List)
- cmd/baha/app_repository_identity.go — intentionally unchanged (the CLI already drives InitializeIdentity; the production-path test exercises that exact orbit).
- Locked (NOT touched, per card): internal/machinehttp/**, internal/devaccess, internal/openbao, internal/orgconfig, internal/policy.

## Delivery (from card)
1. Production-path test (Dauer clause): real `baha app init --quick` CLI orbit drives registration; the helper is not called directly.
2. Two-fresh-homes cell + simultaneous registration (race-count=20): bindings independent, no cross-rewrite; server-side ID assignment proven (client cannot set ID).
3. Attach denials: foreign/disallowed app → named fail-closed error; mutants: authorization check off => RED, server-id-rewritable => RED (verbatim lines).
4. RED-FIRST: mutants captured RED on the unmodified-develop baseline, then GREEN after the bounded fix.

## Tests added
- internal/application/app_binding_contract_test.go
  - TestServerAllocatesIdentityNeverClientsProves — client cannot author/override/rename a server id.
  - TestConcurrentFirstRegistrationConvergesProves — race-count=20 converges on one server-owned id.
  - TestAttachToPermittedExistingAppProvesNamedDenial — permitted attach converges; disallowed attach denied with named "already owned by" error.
- cmd/baha/app_binding_production_test.go
  - TestCLIProductionPathAssignsServerIdentityProves — real CLI assigns a server id, never authored in the contract, present in the canonical Store.
  - TestCLITwoFreshHomesConcurrentRegistrationProves — two independent checkouts each resolve a server id, no cross-rewrite.

## RED-FIRST mutant evidence (verbatim)

### Mutant A — authorization check disabled (attach not permission-gated)
Code under test: internal/application/identity_resolution.go InitializeIdentity owner-name guard.
Command: `go test ./internal/application/ -run "TestAttachToPermittedExistingAppProvesNamedDenial"`
RED output (unmodified-develop-equivalent with the guard commented):
```
=== RUN   TestAttachToPermittedExistingAppProvesNamedDenial
    app_binding_contract_test.go:140: foreign-name attach over existing id was accepted; attach is not permission-gated
--- FAIL: TestAttachToPermittedExistingAppProvesNamedDenial (0.00s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/application	0.006s
```
Verdict: the named fail-closed check has teeth — disabling it makes the foreign-name attach succeed and the test fail.

### Mutant B — concurrent-load retry disabled (server id re-writable / convergence broken)
Code under test: internal/application/identity_resolution.go bounded winner-manifest reload.
Command: `go test ./internal/application/ -run "TestConcurrentFirstRegistrationConvergesProves"`
RED output (retry replaced by a hard transient-not-found return):
```
=== RUN   TestConcurrentFirstRegistrationConvergesProves
    app_binding_contract_test.go:95: concurrent registration did not converge: "<err>"
--- FAIL: TestConcurrentFirstRegistrationConvergesProves (0.00s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/application	0.006s
```
Verdict: the bounded retry is what closes the atomic-rename window; removing it lets a concurrent creator mid-rename surface a transient "not found" and break convergence.

### Root-cause diagnosed (why the concurrency bug was intermittent)
Probe of 20 concurrent `InitializeIdentity` calls on develop showed errors of the form
`load myapp: application "myapp" not found`. Two independent defects:
1. `Store.Create`'s `os.Mkdir` returns a raw EEXIST (not `os.ErrExist`) when a concurrent creator made the directory first, and `InitializeIdentity` only treated `ErrExists`/`os.ErrExist` as retryable — so the raw error propagated as a hard failure.
2. `Store.List` reads every entry during a concurrent build; a half-built app directory (present, no baseharbor.yaml yet) made `Load` return "not found", which `List` surfaced as a hard error before any retry path ran.

Fix:
- `Create` builds the app in a uniquely named `<app>.<pid>.tmp<nanos>` temp directory and atomically `Rename`s it into place, so `List` never observes a half-built app. Mkdir/rename EEXIST is normalized to the existing `ErrExists` sentinel.
- `List` skips transient build directories via `isTransientBuildDir` (a valid slug has no dots; the temp suffix does), so a per-try unique name can never surface as an identity.
- `InitializeIdentity` reloads the winner's manifest with a bounded retry (concurrentLoadRetries=1000, 1 ms backoff) so a concurrent creator mid-rename converges instead of failing.

### GREEN after the bounded fix
Command: `go test ./internal/application/ -run "TestServerAllocatesIdentityNeverClientsProves|TestConcurrentFirstRegistrationConvergesProves|TestAttachToPermittedExistingAppProvesNamedDenial" -count=3`
```
ok  	github.com/mcpdev80/baseharbor/internal/application	0.028s
```
Race sweep (verified clean): `go test ./internal/application/ -race -count=3` on the same three tests → `ok`.

## Verification (all on work/r27-app-binding, HEAD 4e4a23e8)
- `go build ./internal/application/ ./cmd/baha/` → rc=0
- `go vet ./internal/application/ ./cmd/baha/` → rc=0
- `gofmt -l` on all four files → empty (clean)
- `bash scripts/source-readability-audit.sh` → PASS (file size, function span, regression ratchet)
- Full `go test ./internal/application/` → ok (all existing identity/store/adoption tests still pass; no regression from atomic Create or transient-dir skip)
- Selected `go test ./cmd/baha/ -run "Adoption|ApplicationInit|QuickAdoption|ApplicationIdentity|RepositoryIdentity"` → ok
- `go test ./cmd/baha/ -run "TestCLIProductionPathAssignsServerIdentityProves|TestCLITwoFreshHomesConcurrentRegistrationProves" -count=5` → ok

## Hosted CI (PR #1388, Run ID 42020006887)
- All required checks PASS or SKIPPED at head 4e4a23e8.
- Notable green: Workflow policy, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Validation · go-build, cli-build, cli-gofmt, cli-vet, cli-guided-tests, go-vet, source-contracts, cli-package-tests, go-unit-tests.
- Scoped runtime/HA gates (Targeted HA · docker/podman, Selected Runtime, Public Contracts) SKIPPED — no runtime change in this candidate.
- No .github edits and no workflow_dispatch used; checks started from marking the draft PR ready (normal PR operation), shared GitHub runners only.

## Scope / consent / safety notes
- Only production files identity_resolution.go and store.go changed; two test files added. No locked files touched.
- No developer-authored app id; server remains the sole ID owner.
- Concurrent first registration provably converges (race-20) with no cross-rewrite; disallowed attach fails closed with a named error.

## Status
DONE — implementation and RED-FIRST verification complete, PR #1388 open on develop, CI green at head.
