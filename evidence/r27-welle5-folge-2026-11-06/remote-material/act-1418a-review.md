# CODEX-REVIEW 0427-051 / PR #1418

Candidate head: `efb6c2d2cde4e4478bec55963f003fc4a860a88b`. Base: `develop` at `934be499b9d2d894f80889fc23cd811884c8aec4`.

## PLAN

1. Confirm task contract, planning repository remote, and exact remote candidate/base SHAs.
2. Review round 1–4 evidence and verify its ls-remote and run witnesses.
3. Inspect the exact candidate diff for the bounded PKI-to-managed-publication-to-node flow and rotation.
4. Inspect exact-head CI and determine which applicable job runs the new `internal/application` test.
5. Write a SHA-specific verdict and actionable correction recipe if rejected; publish evidence on origin/main and post END.

## Candidate and task contract

- The contract requires remote provider/exposure/TLS projections through existing provider owners, protected secrets, preserved receiver/consumer/rotation behavior, executable regressions, and no broad remote guard.
- The planning checkout was verified before this evidence commit. `git remote -v`:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

This is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, not the `workers/` phantom checkout.
- Fresh product remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1418/head`:

```text
934be499b9d2d894f80889fc23cd811884c8aec4\trefs/heads/develop
efb6c2d2cde4e4478bec55963f003fc4a860a88b\trefs/pull/1418/head
```

- PR #1418 is OPEN, ready (not draft), targets `develop`, is mergeable, and its head matches the mission SHA.
- Exact diff `934be499b9d2d894f80889fc23cd811884c8aec4...efb6c2d2cde4e4478bec55963f003fc4a860a88b`: exactly three files, all within `internal/application/`: `backend_tls.go`, `runtime_postgres.go`, and the new `remote_exposure_serving_test.go`; 335 insertions, no deletions. No broad remote guard or shared registry changes.
- `git merge-base --is-ancestor 934be499b9d2d894f80889fc23cd811884c8aec4 efb6c2d2cde4e4478bec55963f003fc4a860a88b` returned 0. `git log --oneline 934be499b9d2d894f80889fc23cd811884c8aec4...efb6c2d2cde4e4478bec55963f003fc4a860a88b` lists the feature commit `852e421c2` and the develop refresh merge `efb6c2d2c`; the refresh merge has develop `934be499b` as its second parent, matching the round-4 provenance account. No unrelated PR candidate is present.

## Round 1–4 evidence

Reviewed `evidence/r27-welle5-folge-2026-11-06/remote-material/round-1.md` through `round-4.md` on planning main. Round 4’s remote branch/head and PR-head witnesses match this review. Its latest ready-PR CI run is `42333649344`, terminal success at the candidate SHA; the earlier run `42333343404` was from before the PR was ready and had the unit matrix skipped. Round 4 correctly notes no product `.github/**` file was authored by the lane.

The round-4 CI claim that `go-unit-tests` covers `internal/application` is confirmed by the live run log: job `128285616669` executed `go test ./internal/application/... ./contracts/... -count=1`, and reported `ok github.com/mcpdev80/baseharbor/internal/application`.

## Exact-head CI and runtime cells

Run `42333649344` (`CI · PR #1418`) is terminal `success` for `efb6c2d2cde4e4478bec55963f003fc4a860a88b`. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, source format, and `PR Selected Checks` succeeded. The package command above executes the new `internal/application/remote_exposure_serving_test.go` tests; this is the CI cell that runs the Go tests.

The required runtime evidence is absent: `Targeted HA · docker` job `128285576276` and `Targeted HA · podman` job `128285576576` are both `skipped` on that exact-head run. In `.github/workflows/ci.yml`, the Docker job is restricted at line 176 to push events on `runtime-validation/ha/...` branches containing `/docker/` or `/both/`; Podman has the same restriction at line 218. Neither cell ran the new service under its runtime. Thus the unit test was not skipped, but the Docker+Podman node-consumption evidence requested by this mission is only skipped. No rerun or workflow dispatch was performed.

## Blocking findings

1. **Exposure-only workloads never get a gateway.** `RuntimeComposeYAMLForProject` returns `services: {}` at `internal/application/runtime_postgres.go:310-311` whenever `HasManagedRuntimeServices(m)` is false. That predicate covers PostgreSQL, Valkey, RabbitMQ, and MongoDB, but not exposures. A second early return at lines 323-324 also omits exposures when those backend lists are empty (including shared backends after they are removed from this Compose project). The gateway loop is later at lines 354-356. Therefore a valid explicit workload with an HTTP exposure and no application-scoped data provider cannot get the gateway. The new fixture avoids this by setting SQL true (`remote_exposure_serving_test.go:21-23`), so it does not catch the case.
2. **The generated gateway has no serving/proxy configuration.** `writeExposureGatewayComposeService` at `runtime_postgres.go:522-550` launches Caddy with `/etc/caddy/Caddyfile`, but mounts no Caddyfile and generates no site/proxy configuration. It also takes only the exposure name, while the existing exposure contract carries service, target port, and protocol (`internal/application/manifest.go:164-169`); those routing values never reach this service. The new positive test asserts only that cert/key mount strings appear (`remote_exposure_serving_test.go:64-75`), not that an HTTPS request reaches the declared workload.
3. **Rotation and runtime consumption lack behavioral coverage.** The new tests check certificate projection, key location/modes, missing issuer, no-exposure behavior, and that a leaf chains to a CA. There is no test that renews/rotates the exposure certificate and proves the running node gateway serves the replacement. The exact-head Docker and Podman cells that could exercise the generated Compose gateway are skipped.

## Verdict and correction recipe

REJECT candidate `efb6c2d2cde4e4478bec55963f003fc4a860a88b`.

Correction recipe:

- In `internal/application/runtime_postgres.go:310-324`, keep the early-return behavior only when there are neither managed backend services nor HTTP exposures. Ensure the later exposure loop runs for workload-only and shared-backend exposure manifests. Add a regression using an explicit workload and exposure with no SQL/Valkey/RabbitMQ/MongoDB provider; require its gateway service and serving material in the publication.
- In `internal/application/runtime_postgres.go:522-550`, generate and mount an exposure-specific Caddy configuration that uses the serving cert/key and routes to the declared service and target port. Add an end-to-end test that requests HTTPS through the generated node gateway and receives the workload response.
- Add a rotation regression that reconciles new PKI material, reloads/reconciles the node gateway without re-bootstrap, and proves the replacement certificate is served.
- Required CI wiring is Owner scope: `.github/workflows/ci.yml:171-176,213-218` currently limits both runtime cells to designated push refs, which is why they skip on this PR. Owner should add an applicable exact-candidate/PR selection for this exposure serving test path and run the new runtime regression on both Docker and Podman. Do not edit the workflow in this review. Stop until both runtime cells and the exact-head Go tests pass with exercised, non-skipped results and the functional review is repeated on the new SHA.

## Repo-rule compliance

- Read-only product review: no product files changed, no merge, no workflow rerun/dispatch, and no containers or VM smoke started.
- Evidence stays in the real `baseharbor-plan` repository. A pre-existing untracked `evidence/r27-welle5-folge-2026-11-06/management-host/round-8-serve-startup.md` was left untouched.
- No subagents were used. This evidence contains no markdown checkbox syntax.

## END

END_DONE codex-1418-review-a: verdict=REJECT head=efb6c2d2cde4e4478bec55963f003fc4a860a88b ci=42333649344-success; docker=128285576276-skipped podman=128285576576-skipped; required node-runtime proof absent. Recipe=runtime_postgres.go exposure-only gate plus generated Caddy routing/rotation tests; Owner CI wiring; stop until both runtime cells execute and pass.

## Planning publication witness

Exact `git ls-remote origin refs/heads/main` output captured immediately before publishing this evidence:

```text
c904c5bae912214ded05faf7a50c54468edd992e	refs/heads/main
```
