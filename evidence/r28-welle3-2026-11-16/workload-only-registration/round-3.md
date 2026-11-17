# Workload-only registration — R3

Date: 2026-11-17. Role: WORKER, owner-authorized Codex lane. Candidate PR #1676, card 0428-100.

## PLAN

 * [x] 1. Refresh PR #1676, remote branch, current develop, Planning task/claim and inspect repository rules.
 * [x] 2. Trace workload `RuntimeTarget(project, "workload")` through the actual Prometheus `provider-*.json` file_sd generation. It is copied verbatim and no Prometheus runtime-target resolver exists.
 * [ ] 3. STOP+QUESTION: target contract is not defined for a workload-only app with no declared metrics service/port or workload `/metrics` endpoint. Do not invent a target or weaken verification.
 * [ ] 4. Add integrated workload-only regression from deploy registration through `EnsureProviderFiles` snapshot and positive verification; add service-app compatibility via the real registration path.
 * [ ] 5. Run gofmt, affected package tests, build, vet, and inspect the complete diff against #1665 scope.
 * [ ] 6. Merge current develop into the PR lane without force, push with explicit refspec, and observe its own exact-head pull_request run to terminal success.
 * [ ] 7. Re-review the exact new head against the batch21/r3 recipes; merge only if all exact-head checks and review gates pass, then publish both role akten and END posts.

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

## Resume after coord update

- Coord directed the WORKER role to continue, publish a corrected candidate, observe a terminal exact-head run, and then END before opening a distinct REVIEW object. This resumes the same WORKER role; it does not answer the unresolved target-contract question below.
- The prior R2 akte says the URI registration was intended to satisfy `SignalSource.Validate` “without fabricating a scrape backend.” R3's explicit owner requirement now says the target must be scrapeable without weakening verification. Product code still writes this URI verbatim to Prometheus file_sd, and neither the card nor repository defines a workload metrics service/port/endpoint for the fixture. Thus the R2 logical registration cannot satisfy the new scrapeability requirement as implemented, and selecting a DNS alias/port would invent product behavior.
- STOP+QUESTION remains: what concrete workload service, port, and `/metrics` endpoint is the contract for this workload-only shape, or should this card's contract change to a non-scraped logical registration? Await this definition before product edits, tests, base merge, push, or CI.
- Coordinator reports planning render/check now pass (0 errors) and band published. This supersedes the previous note that those checks were blocked; no planning-blocker remains.
