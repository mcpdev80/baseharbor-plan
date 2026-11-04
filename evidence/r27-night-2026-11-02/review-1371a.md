# Review 1371a — workstation enrollment production wiring

- Role: CODEX-REVIEW; no merge.
- PR: [#1371](https://github.com/mcpdev80/baseharbor/pull/1371), task `t-20261018-r27-device-enrollment`.
- Exact head: `fb701991750c02021d7b062448ad3cd13a7f18d2`; base `develop` = `f8ef4255592fcb1502fa54187c0965b9d00f118c`.
- Current PR: OPEN, READY, mergeable. `git ls-remote` confirmed both refs. `git diff --check` clean. Worktree retained pre-existing untracked `baha`; not modified.

## Six requested checks / counter-probes

1. **Management route registration and reachability — FAIL.** `server_run.go:259-260` registers the ProductionHandler at `/api/v1/workstations/bootstrap` and `/api/v1/workstations/enroll`. But `ProductionHandler.ServeHTTP` (`internal/workstationenrollment/http/production_handler.go:56-64`) dispatches only when `r.URL.Path` is exactly `/bootstrap` or `/enroll`. Go's `ServeMux` does not strip the matched prefix from `r.URL.Path`, so a request through either registered production route falls through to 404. Existing tests call the handler with `/bootstrap` and `/enroll`; they miss the mounted production paths. The new route is therefore present but not callable as wired.
2. **Foreign installation / request scope — PARTIAL.** The tenant ID is derived from `tenancy.FromContext`, so a request `installation_id` cannot select a foreign tenant; the tests cover this and unauthenticated callers fail closed. However `Resolve(ctx, req.Station)` takes `station` directly from the request and constructs the enrollment scope from it (`production_handler.go:114-119,159-168`); it checks syntax but does not consult a policy/ownership mapping for that station. The mission requires policy as scope source rather than request. A valid but unowned station label is not rejected by the resolver.
3. **Durable store / reopened process — NOT VERIFIED LOCALLY.** The PostgreSQL integration test creates a fresh pool after consuming and expects replay rejection, and covers registry fact fields. It was skipped locally because `BASEHARBOR_TEST_DATABASE_URL` is unset. No real reopened-store execution was observed in this review.
4. **One-use second use — PASS for authority path.** `TestSecondUseRejected` and `TestEnrollSecondUseRejected` passed; the database integration contains a second-consume assertion but was skipped locally.
5. **Foreign enrollment files / namespace — PASS.** The exact name-only diff contains no `internal/targetenrollment/**` files and no pre-existing registry file; it adds workstation-specific contract, handler, database tables/store and additive management wiring only.
6. **Package tests, build, gofmt/vet — PARTIAL.** `go test ./internal/workstationenrollment/... ./internal/database -count=1 -timeout 8m -v` passed unit/handler cases, with PostgreSQL integration cases skipped as above. `gofmt -l` on all changed Go files returned empty; targeted `go vet` passed. Local `go build ./...` could not complete because the repository requires Go 1.26.9 and the sandbox could not download/unpack the toolchain (first the system module cache was read-only; redirected cache then hit `/tmp` disk quota). Hosted run `41821686309` on this exact SHA reported `cli-build`, `go-build`, `cli-vet`, `go-vet`, source format and other selected checks passing; `go-unit-tests` was still pending when observed. `PR Selected Checks` from run `41821537494` was reported skipped, so hosted required selection is not demonstrated green.

## Additional production-path defect

`ProductionEnrollment` requires `RecordRegistryFact`, but `ServeEnroll` conditionally type-asserts that method and discards its error (`production_handler.go:138-142`). Thus even after fixing route dispatch, an enrollment can return HTTP 200 and a certificate while the durable registry fact was not written. The claimed registry ownership invariant is not fail-closed, and there is no regression for registry-write failure (the test mock has a `registryErr` field but no test uses it).

## Verdict: REJECT

### REZEPT

- `internal/workstationenrollment/http/production_handler.go`: route by suffix/submux or register the handler with a path-aware production router so the exact `/api/v1/workstations/{bootstrap,enroll}` requests reach their endpoint methods. Add a test that mounts the handler at the same paths as `registerOperatorAPI` and verifies bootstrap/enroll do not return 404.
- Replace `ScopeResolverFromContext`'s request-supplied station acceptance with an authenticated policy/ownership lookup for the station; keep installation derived from tenancy. Regression: valid-looking but unowned station and foreign installation both fail before store/issuer calls.
- Make registry fact persistence mandatory and propagate failure (fail closed); test the `registryErr` path and assert no success response when persistence fails.
- Run the PostgreSQL integration against a real test database, including fresh-pool replay and registry readback; observe terminal `go-unit-tests` and `PR Selected Checks` for this exact SHA.
- Recheck focused tests, `go build ./...`, `gofmt`, and `go vet` after corrections. Stop if a production route is still unreachable, an unowned request station creates scope, replay survives restart, or registry persistence errors still return success.

No candidate source was changed. Review only; no merge.
