# CODEX-REVIEW 0427-051 / PR #1418 rereview

Candidate: `a91debbb047d6ea7a0f258194c0a3474978687bd` against `develop`.

## PLAN

1. Confirm real planning checkout and fresh exact develop/PR remote SHAs.
2. Inspect exact candidate diff for exposure-only gateway, single Caddy owner, and absence of duplicate logic.
3. Review round-5 evidence and verify rotation/node-consumption regression witnesses.
4. Inspect exact-head run 4984, go-unit/release_source results, and owner-scoped skipped runtime cells.
5. Write the verdict, publish evidence on origin/main, verify it, and post END.

## Base and remote witnesses

The planning repository is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
Exact `git remote -v` output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Fresh planning remote witness before evidence publication:

```text
18e991930c87122279a8c06c08d31281d8187457	refs/heads/main
```

Planning checkout was `main...origin/main` at `18e991930c87122279a8c06c08d31281d8187457`. This review did not create a product branch or modify product files. Existing unrelated untracked evidence files were left untouched.

Fresh product `git ls-remote` witness:

```text
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
a91debbb047d6ea7a0f258194c0a3474978687bd	refs/pull/1418/head
```

Exact diff `934be499b9d2d894f80889fc23cd811884c8aec4...a91debbb047d6ea7a0f258194c0a3474978687bd` contains only `A internal/exposure/exposure_node_serving_test.go` (140 lines). The base is an ancestor of the candidate; merge-base equals the base. Candidate-only log:

```text
a91debbb0 test(exposure): route node-serving cert through caddy.go single owner (t-20261018-r27)
```

That is the sole commit in the base-to-candidate log. PR #1418 is open, ready (not draft), targets `develop`, and reports this exact head.

## Review

F1 and F2 are addressed without a second gateway implementation. The only candidate change is a test file. `TestExposureOnlyWorkloadGetsAServingGateway` at lines 24-55 constructs an exposure-only manifest with SQL/cache disabled, runs preflight and `ensureFiles`, and asserts a Caddy route is materialized under `providers/caddy/routes/public`. The existing `internal/exposure/caddy.go` remains the sole implementation: `ReconcileWorkloadTransport` calls `ensureFiles` at lines 287-315; `ensureFiles` builds route and certificate files at lines 400 onward; `composeYAML` mounts the existing provider routes into the application exposure network; `caddyfile` reverse-proxies to the workload service.

F3 has a behavioral rotation regression in `TestServingCertificateRotatesWithoutReBootstrap` at lines 63-129. It writes serving material A, confirms the route's served `cert.pem`, changes deployment TLS material to B, calls the file-producing `ensureFiles` reconciliation path, asserts `changed`, and verifies the exact served route file now contains B. It does not invoke a live container or HTTPS handshake; the mission expressly accepts `ReconcileWorkloadTransport/ensureFiles`, and the regression verifies the node-side served-file consumption path without provisioning again.

Round-5 evidence `evidence/r27-welle5-folge-2026-11-06/remote-material/round-5.md` was reviewed. Its pinned-lease resolution is consistent with the fresh PR ref and exact one-commit candidate observed above.

## CI witnesses

Run 4984 is GitHub Actions run `42338068531`, event `pull_request`, head `a91debbb047d6ea7a0f258194c0a3474978687bd`, terminal conclusion `success` (https://github.com/mcpdev80/baseharbor/actions/runs/42338068531). `PR · Validation · go-unit-tests` job `128299450590` succeeded; its log includes:

```text
ok   github.com/mcpdev80/baseharbor/internal/exposure 0.022s
```

The job invokes `scripts/pr-unit-database.sh`, whose `go test ./... -count=1` includes the exposure tests. `PR · Validation · go-build`, `go-vet`, `PR Selected Checks`, and source-format checks also succeeded.

`Release Source Preflight` (`128299403803`), `Targeted HA · docker` (`128299403752`) and `Targeted HA · podman` (`128299403330`) were skipped. These are owner-scoped workflow cells gated to push refs; no workflow edits or reruns were made. Per the mission, the skipped runtime cells do not invalidate this acceptance because exact-head pull-request Go unit CI ran the regressions.

## Verdict

`ACCEPT` — F1/F2 single-owner exposure serving is covered, F3 serving-certificate rotation through the accepted `ensureFiles` path is covered, and exact-head pull-request Go unit CI passed. No correction recipe is required. No merge was performed.

## repo-rule compliance

Read-only product review only; no product files or workflows were edited, no hosted workflow was triggered, and no test VM/container was started. Evidence is stored only in the real `baseharbor-plan` repository. Native todowrite was not exposed in this session; the required live board JSON was used.

## Publication

The planning repository remote was verified as `https://github.com/mcpdev80/baseharbor-plan.git`, the authoritative planning vault. This review evidence is committed and pushed directly to planning `origin/main` under the planning repository publication rules. The commit and remote tree witness are recorded below.

## repo-rule compliance

Read-only product review only; no product files or workflows were edited, no hosted workflow was triggered, and no test VM/container was started. Evidence is stored only in the real `baseharbor-plan` repository. Native todowrite was not exposed in this session; the required live board JSON was used.

END_DONE codex-1418-rereview-b: verdict ACCEPT; evidence published to baseharbor-plan origin/main; candidate a91debbb047d6ea7a0f258194c0a3474978687bd.

Remote origin/main tree witness after the first push (commit `b52115d569b92364c0853a260bb50be44f0e0754`):

```text
100644 blob b5eeb99694179c5ad921ed41ccc41b4a512871c1\tevidence/r27-welle5-folge-2026-11-06/remote-material/act-1418b-review.md
```
