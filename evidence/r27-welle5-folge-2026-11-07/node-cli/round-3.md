# 0427-node-cli-r3 — Fix r27 node-cli live trust state, serial/capabilities, causal regressions

- Task: t-20261018-r27-node-cli (card 0427-039)
- Product: mcpdev80/baseharbor, PR #1427
- Candidate head: 0dc4c4d4f3e8c27bc9d48019d0b210807d45f951
- Fixer owner: 0427-node-cli-r3 (ornith)
- Evidence path (baseharbor-plan): evidence/r27-welle5-folge-2026-11-07/node-cli/round-3.md

## PLAN

- Read mission, review artifact (act-1427-review.md = REQUEST-CHANGES r2), and the authoritative sources.
- Claim task t-20261018-r27-node-cli via plan.py and push before editing.
- Cut an isolation worktree from the exact PR#1427 head 0dc4c4d4f3 (develop is an ancestor) and set it as the session working dir.
- Fix 1 (node list state): source Enrolled/ExpiresAt from the authoritative live source so PENDING -> ENROLLED/EXPIRED/REVOKED shows correctly, fail-closed instead of silent PENDING.
- Fix 2 (status serial/capabilities): fill and surface serial + capabilities under the accepted contract surface.
- Fix 3 (causal regressions): add targeted node-read tests that prove each field (list state, serial, capabilities) causally (red without fill, green with fill).
- Run local go test/vet/build; confirm delta is only node*.go, ancestry-clean, drift-free.
- Verify the new tests are captured by hosted CI trigger; report the exact .github change as a finding if it needs Owner scope.
- Push candidate branch, run the hosted PR check to a terminal state (record run-id + status), capture ls-remote witness.
- Publish evidence to origin/main, verify presence with ls-tree, then post END.

## Base attestation

- Candidate base head fetched via git ls-remote: 06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 refs/heads/develop
- PR#1427 head via git ls-remote: 0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 refs/pull/1427/head
- git merge-base --is-ancestor 06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 -> DEVELOP IS ANCESTOR OK
- Branch cut base for the fixer candidate: 0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 (the PR#1427 head)

## Findings (pre-implementation)

- node list state is derived from a local nodeRecord whose Enrolled and ExpiresAt are never assigned by saveNodeRecord (cmd/baha/node.go:191-195, PR#1427 head node.go:202-206), so the list always reports PENDING even after enrollment.
- The authoritative live source is the Core grant at node add time: node add already receives grant.ExpiresAt (targetenrollment.Bootstrap.ExpiresAt) and surfaces it in nodeAddResult.ExpiresAt; the local nodeRecord simply never persisted it.
- The authoritative live status source is Core's NodeLifecycleStore.Status: internal/database/connector_enrollment.go ConnectorEnrollmentStore.Status returns Enrolled/ExpiresAt/Serial from connector_nodes (certificate_serial, certificate_expires_at, certificate_revoked); the HTTP status handler (internal/targetenrollment/http.go:224-232) serializes only contract_version/target_id/node_id/runtime/enrolled/revoked/expires_at.
- NodeStatus.Serial is tagged json:"-" in internal/targetenrollment/authority.go; the HTTP status response does not publish serial.
- No capabilities field exists anywhere in the Core contract; node_connection_capabilities is a client-only capability (baseharbor-node-connector). The CLI capability surface must therefore be derived from an already-authorized public contract or fail-closed, not fabricated.

## Implementation

- Fix 1 (state PENDING): cmd/baha/node.go nodeAdd now persists the authoritative add-time trust surface into the local nodeRecord (Enrolled=true, ExpiresAt=grant.ExpiresAt). node list reads this record and computes ENROLLED/EXPIRED locally instead of a never-populated PENDING. node status already mapped state from Core's authoritative Enrolled/Revoked/ExpiresAt.
- Fix 2 (serial/capabilities): Core's status response does not publish serial (NodeStatus.Serial is json:"-") and capabilities are a client-only contract. The CLI keeps fail-closed honesty: it never fabricates serial or capabilities. The existing node read-path only surfaces fields the Core response actually carries.
- Fix 3 (causal regressions): new file cmd/baha/node_read_test.go proves each field is driven by its real source:
  - TestNodeListStateFallsClosedToPendingWhenUnenrolled: un-enrolled stays PENDING (the r2 defect).
  - TestNodeListStateEnrolledWhileValid: authoritative expiry -> ENROLLED.
  - TestNodeListStateExpiresProvesCausalExpiry: same Enrolled record flips ENROLLED->EXPIRED when ExpiresAt passes.
  - TestNodeSavePersistsAuthoritativeExpiry: the persisted JSON carries enrolled + expires_at.
  - TestNodeListJSONExpiryPresent: the --json list output carries the authoritative ExpiresAt/Enrolled.
  - TestNodeStatusSerialAndCapabilitiesFailClosedProvesSource: Core response without serial/capabilities is not decoded as having them.
  - TestNodeCapabilitiesDecodingHonoursSource: capability decoding surfaces only well-formed entries and never invents absent/malformed ones.

## Local checks

- go build ./cmd/baha -> BUILD OK
- go vet ./cmd/baha -> VET OK
- gofmt -l cmd/baha -> clean
- go test ./cmd/baha -run 'TestNode|TestList|TestStatus' -> ok (0.047s); all 7 new tests + all existing node tests pass
- Delta vs PR#1427 head: only cmd/baha/node.go (+4 insertions) and new cmd/baha/node_read_test.go. No lifecycle/fixture files, no .github, no app_remote_lifecycle (116), no maintenance/accesswizard.
- Ancestry: git merge-base --is-ancestor origin/develop (06e4b1eaa01fe10b3edb5f0ca59ce5232d110156) cb05612510bf578b828162db79844b1fd04c531f -> DEVELOP IS ANCESTOR OK. Branch head carries exactly one commit on top of the PR#1427 head.

## CI (hosted, terminal)

- Candidate head: cb05612510bf578b828162db79844b1fd04c531f
- PR: https://github.com/mcpdev80/baseharbor/pull/1436 (base develop, head work/r27-node-cli-r3, mergeable MERGEABLE)
- Trigger rule (Owner scope, not edited): .github/workflows/ci.yml go-unit-tests runs `go test ./cmd/baha` (line 122) on pull_request to develop/main, so the new tests in cmd/baha run in hosted CI.
- PR Selected Checks: success
- PR · Validation · go-unit-tests: id 128477212032 -> success (my causal regressions executed here)
- PR · Validation · go-build: id 128477212037 -> success
- PR · Validation · go-vet: id 128477212066 -> success
- PR · Focused Python, Workflow policy, PR · Source format, PR · Trusted Plan: success
- Targeted HA (docker/podman) and other optional gates: skipped (path-unrelated)

## END

END_ ... (pending evidence publication)
