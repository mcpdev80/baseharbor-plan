# Workload-only registration — R3

Date: 2026-11-17. Role: WORKER, owner-authorized Codex lane. Candidate PR #1676, card 0428-100.

## PLAN

 - 1. Refresh PR #1676, remote branch, current develop, Planning task/claim and inspect repository rules.
 - 2. Trace workload `RuntimeTarget(project, "workload")` through the actual Prometheus `provider-*.json` file_sd generation. It is copied verbatim and no Prometheus runtime-target resolver exists.
 - 3. Resolve target contract with the coordinator: retain the symbolic runtime identity in the shared snapshot, without a scrape target; exclude it from Prometheus file_sd and do not weaken verification for real scrape sources.
 - 4. Add integrated workload-only regression from deploy registration through `EnsureProviderFiles` snapshot and positive verification; add service-app compatibility via the real registration path.
 - 5. Run gofmt, affected package tests, build, vet, and inspect the complete diff against #1665 scope.
 - 6a. Merge current develop into the PR lane with an ordinary merge commit and push with explicit refspec (no force).
 - 6b. Exact-head pull_request run 44018836577 completed successfully on `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c`.
 - 7. Independent REVIEW role checked the exact new head against batch21/r3 recipes; verdict CHANGES REQUESTED on the unmet scrapeable-target contract. No merge; see `review-1.md` and review END post.

## Ownership and baseline

- `plan.py claim` was attempted and refused because the card is in `review`. Mission fallback `r3-owner: codex (parallel-autorisiert 2026-11-17T04:17Z)` is present locally in the task note.
- Planning `render` and `check` are currently blocked by two unrelated invalid `sources` metadata entries in other task notes; details will be recorded in the handoff if they remain unresolved. No other task note will be changed by this lane.
- Initial exact product head: `0b8cecb058efb7dc7678071a3113bc8786890d2d`; current develop before changes: `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54`.

## Runtime target finding and stop

- Product evidence at the candidate/develop code: `internal/application/runtime_observability.go:101-103` creates the workload metrics source with `Target: observability.RuntimeTarget(project, "workload")` and `Path: "/metrics"`; `internal/observability/registry.go:257-270` defines that as the literal `runtime://<project>/workload` identifier.
- `internal/metrics/prometheus_files.go:64-67` writes each provider source target unchanged as the sole `Targets` value in `provider--*.json`.
- `internal/metrics/prometheus_render.go:217-226` consumes `provider--*.json` with Prometheus `file_sd_configs`; its relabeling only maps `baseharbor_metrics_path` to `__metrics_path__`. Product-wide search found no resolver converting this `runtime://` URI into a scrapeable host:port.
- Existing scrapeable application target generation requires a declared service and port: `internal/metrics/runtime_source.go:136` and `internal/metrics/realization.go:158` use `MetricsTargetAliasFor(...)+":"+port`. The manifest's declared metrics requirement is the existing contract; this workload-only fixture explicitly has no metrics sources.
- `VerifyProviderSourcesAt`'s early return currently encodes workload-only/no-runtime-permission as “nothing to verify” (`internal/metrics/prometheus_verify.go`, candidate lines 140 onward); removing it and registering this logical URI would make the verifier fail against a non-scrapeable target. The task/card does not say what endpoint to scrape, and inventing a service, port, or exporter would change product contract. STOP+QUESTION to coordinator/owner: should workload-only registration represent a non-scraped logical source (and therefore remain outside `VerifyProviderSourcesAt`), or must the application declare/implement a real `/metrics` endpoint before registration? Please define the scrapeable target contract before R3 proceeds.
- No product files changed; no tests, merge, push, or CI run started. The existing branch remains at `0b8cecb058efb7dc7678071a3113bc8786890d2d`.
- The planning blockers were subsequently repaired and published by coord (`1f124360` fixes path-form `sources`; `d3aff342` neutralizes the 092 stop-report checkbox syntax). `plan.py show t-20261117-workload-only-metrics-source-unregistered` now succeeds and reports `active`. The card is locally clean at current `baseharbor-plan/main`.

## Resume after coord update (historical stop below is superseded)

- Superseded on 2026-11-17 by the coordinator R3 direction: workload-only registration is logical snapshot metadata; it must stay out of file_sd/network/query, while normal backend sources retain scrape verification.

- Coord directed the WORKER role to continue, publish a corrected candidate, observe a terminal exact-head run, and then END before opening a distinct REVIEW object. This resumes the same WORKER role; it does not answer the unresolved target-contract question below.
- The prior R2 akte says the URI registration was intended to satisfy `SignalSource.Validate` “without fabricating a scrape backend.” R3's explicit owner requirement now says the target must be scrapeable without weakening verification. Product code still writes this URI verbatim to Prometheus file_sd, and neither the card nor repository defines a workload metrics service/port/endpoint for the fixture. Thus the R2 logical registration cannot satisfy the new scrapeability requirement as implemented, and selecting a DNS alias/port would invent product behavior.
- Historical STOP+QUESTION (resolved as recorded above): the owner selected non-scraped logical registration. The following historical paragraph describes the state before that direction and is no longer current.
- Coordinator reports planning render/check now pass (0 errors) and band published. This supersedes the previous note that those checks were blocked; no planning-blocker remains.


## Codex R3 implementation and exact-head CI (2026-11-17)

The coordinator's R3 direction resolved the stop point: retain a workload-only runtime identity in the shared snapshot, but do not invent a scrape endpoint. This implementation uses `Verification: ObservabilityVerifyNone` for that symbolic source and excludes it from provider file_sd target generation, provider network projection, and provider scrape queries. Existing verifiable backend sources keep their current verification path. No `security.go` or `.github/**` files changed; approved batch19/20 behavior was not weakened.

The prior candidate test that manually called `observability.Update` was removed. New tests are external-package tests using the real sequence `application.EnsureRuntime -> metrics.EnsureProviderFiles -> read runtime-sources.json -> metrics.VerifyProviderSourcesAt`; the workload-only case asserts its exact owner/identity/symbolic target is present and no matching Prometheus file_sd target exists. The service-app compatibility case also uses this real path.

Candidate commit `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c` is PR #1676 head, following ordinary merge commit `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54` (current develop at rebase). Local exact-head checks passed: `go build ./cmd/baha`; `go vet ./internal/application ./internal/metrics`; `go test ./internal/application ./internal/metrics`; `git diff --check`.

Exact-head PR workflow: [run 44018836577](https://github.com/mcpdev80/baseharbor/actions/runs/44018836577). Run completed successfully at 2026-11-17T04:45:52Z. Workflow policy, native gate plan, trusted plan, source format, all selected Go unit shards (including `PR · Go unit · packages` and isolated non-root PostgreSQL), focused Python, `go-build`, and `go-vet` succeeded. Docker/Podman native gates were skipped by trusted impact selection for this metadata/target-projection change; no native gate was required by the selected plan. PR #1676 was OPEN and MERGEABLE at this exact head. Sequential CODEX-REVIEW completed with CHANGES REQUESTED; no merge. Review evidence: `review-1.md`; review END post is in `evidence/coord-memory/inbox/0428-100-r3-review-end.md`.

Plan renderer/validator now pass after coordinator repair: `python3 scripts/plan.py render && python3 scripts/plan.py check` => 542 tasks, 0 errors, 35 warnings. The 35 warnings are dependency-resolution warnings on existing accepted/review/active cards; no plan errors remain.
