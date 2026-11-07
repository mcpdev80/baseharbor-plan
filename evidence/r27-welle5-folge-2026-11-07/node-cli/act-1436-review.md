# CODEX-REVIEW 0427-node-cli-r3 — PR #1436

## PLAN

1. Read mission, binding coordinator policies, task contract, prior review, and product rules — complete.
2. Fetch exact PR/base refs and review only the three prior findings, write-set, tests, and hosted CI without rerun — complete.
3. Record SHA-specific verdict and actionable repair recipe in canonical planning evidence — complete.
4. Publish evidence to origin/main, verify evidence and unchanged candidate witnesses, then post END — in progress.

## Verdict: REQUEST-CHANGES

Candidate `eee54634a65eeab6f16205e91009ea0de9de91f2` is ancestry-clean and the hosted CI run is successful, but the first r2 finding is not resolved semantically and the claimed seven causal regressions are not all load-bearing.

### Review of prior findings

1. **List trust state: FAIL.** `cmd/baha/node.go:364-367` requests a bootstrap grant with `lifetime_seconds: 600` and a separate `certificate_ttl_seconds: 86400`. The authority's `Bootstrap.ExpiresAt` is the one-use grant expiry (`internal/targetenrollment/authority.go:106-123`); it is not the issued certificate expiry or proof that the remote node has redeemed the grant. Yet `node.go:202-210` sets `Enrolled: true` as soon as the grant is issued and stores that grant expiry. Consequently `cmd/baha/node_read.go:59-65` can report ENROLLED before `baha node connect` has enrolled the node, then report EXPIRED after ten minutes even when a redeemed certificate remains valid. The list path also never requests the lifecycle status and cannot report REVOKED. This replaces the prior permanent PENDING symptom with a false status; it does not represent authoritative enrollment state.
2. **Serial/capabilities: PASS for fail-closed omission.** `nodeStatusResult` fields are optional, and `requestNodeLifecycle` only populates capabilities from a valid Core response (`cmd/baha/node.go:416-445`, `cmd/baha/node_read.go:153-167`). The current Core lifecycle response omits serial and capabilities (`internal/targetenrollment/http.go:221-229` on fetched develop); the CLI leaves them absent rather than fabricating values. The user-facing status output omits unavailable fields. No claim is made that these values are currently available from Core.
3. **Seven causal regressions: FAIL for load-bearing coverage.** Seven new test functions exist in `cmd/baha/node_read_test.go`, and `go-unit-tests` runs that package. However, the three `TestNodeListState...` tests exercise the test-only `renderTrustState` helper at lines 16-28, which production `nodeList` does not call; they pass even if the production rendering at `node_read.go:59-65` is wrong. `TestNodeSavePersistsAuthoritativeExpiry` manually constructs an already-populated record instead of exercising `nodeAdd` grant issuance. `TestNodeStatusSerialAndCapabilitiesFailClosedProvesSource` checks JSON marshal/unmarshal of a struct rather than the production Core request path. `TestNodeCapabilitiesDecodingHonoursSource` tests the production decoder, and `TestNodeListJSONExpiryPresent` calls production `nodeList` for JSON fields, but it does not verify human trust-state output or the enrollment-vs-grant lifecycle distinction.

## Actionable repair recipe

- **Files and change:** In `cmd/baha/node.go:202-210`, do not set `Enrolled=true` from issuance of a one-use bootstrap grant. Keep grant readiness/expiry distinct from remote enrollment state. In `cmd/baha/node_read.go:43-49,59-69`, either obtain the authoritative lifecycle state (including revoked and certificate expiry) for list entries, or label locally known grant state explicitly and retain an unknown/pending enrollment state until Core confirms redemption. Do not infer REVOKED from a local grant record. Keep changes in the assigned node CLI files; if the server contract must change to expose another authoritative field, stop and obtain the owning task/scope update rather than editing shared lifecycle files here.
- **Tests:** Replace the test-only state helper checks with assertions against `nodeList`'s actual rendered output. Exercise the production node-add grant path with a controlled Core response and prove an unredeemed grant is not shown as ENROLLED; exercise live status responses for enrolled, expired, and revoked results, including certificate expiry differing from the ten-minute bootstrap grant expiry. Retain the omission tests but route them through `requestNodeLifecycle` with an in-process Core server so serial/capabilities stay absent when the server omits them. The existing pull-request `PR · Validation · go-unit-tests` must execute these tests; no workflow change is requested.
- **Stop criterion:** Do not approve until list/status labels distinguish one-use grant expiry from actual certificate enrollment, REVOKED is sourced from the lifecycle authority, the regression assertions fail against the relevant broken production paths, and required checks pass on the exact candidate.

## Exact SHA, scope, and hosted CI

- Product repository: `mcpdev80/baseharbor`, fetched into `/tmp/opencode/0427-node-cli-r3-review-wt`.
- PR #1436 is OPEN, base `develop`, head `eee54634a65eeab6f16205e91009ea0de9de91f2`, mergeable `MERGEABLE`, merge state `CLEAN`.
- Exact remote refs before and after source review were unchanged: `8a3f58da905fad52327d33466fde1d9568092519 refs/heads/develop`; `eee54634a65eeab6f16205e91009ea0de9de91f2 refs/pull/1436/head`.
- `git merge-base --is-ancestor refs/remotes/origin/develop refs/remotes/origin/pr/1436` returned `0`.
- Candidate-only log: `eee54634a65eeab6f16205e91009ea0de9de91f2 0427-node-cli-r3 fix(r27 node-cli): source live trust state from authoritative grant, add causal regressions`; `4541011bacd7d066c3eb720f27377fc281917e58 Worker w280 feat(node): surface live trust/expiry/capabilities (PR#1427, drift-free on 06e4b1e)`. These are the two task-chain commits in the candidate; the second commit changes the node files and adds the regression file.
- Exact three-file delta: `M cmd/baha/node.go`; `A cmd/baha/node_read.go`; `A cmd/baha/node_read_test.go`. No `.github/**` or unrelated paths changed; no CI weakening found.
- Hosted checks on exact head: run `42398736386`. PASS: `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `PR · Focused Python`, `PR Selected Checks`, `PR · Trusted Plan`, `Source format`, and `Workflow policy`. SKIPPING: consumer/demo pins, exact candidate, public contracts, runner interface, selected runtime, HA Docker/Podman, release preflight, and validate. There are no failing checks. No local test, CI rerun, or workflow dispatch was started by this review.
- Planning repository verified before evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. `origin` fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git`.
- Pre-publish planning main witness: `f1645d4c797227f3a6453b6505c301ff9e70411b refs/heads/main`.
- First published origin/main tree witness, exact output: `100644 blob 2b7d9eee2ae4b1652e4c2af3c400dfc0056f9ad7	evidence/r27-welle5-folge-2026-11-07/node-cli/act-1436-review.md`.
- First evidence commit: `7023eed44bd58ef763f0541ccd354bd9220ee56a`.
- The product candidate was not modified; final `ls-remote` still returned head `eee54634a65eeab6f16205e91009ea0de9de91f2` and base `8a3f58da905fad52327d33466fde1d9568092519`.

## Repository-rule compliance

This was a read-only product review. No product files were edited, no local tests or CI reruns were started, and no workflow or runner infrastructure was changed. Evidence is stored only in canonical `baseharbor-plan`. An unrelated existing modification to `node-cli/round-3.md` was left untouched and will not be staged.

END_BLOCKED 0427-node-cli-r3-review: REQUEST-CHANGES; candidate `eee54634a65eeab6f16205e91009ea0de9de91f2` labels a 10-minute unconsumed bootstrap grant as ENROLLED/EXPIRED and its three state tests exercise a test-only helper, not production rendering.
