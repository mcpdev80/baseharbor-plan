# 0428-244 core-network owner assertion fix round 1

- karte 0428-244, sitz f0f6c8b4. Stale assertion in a test blocks PR #1765 natively.
- Test-only fix. NO product change, NO .github/scripts, NO subagent, NO merge/comment.
- develop snapshot base attestation: 8629450ef3c5198bb675331c12f56b2c9377aa1c (confirmed via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- remote guard: all remotes (origin, lane-origin, upstream) -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote
- git remote -v line: `origin	https://github.com/mcpdev80/baseharbor.git`

## PLAN

1. Establish reality: git remote guard, develop 8629450ef3c, failing test TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork at cmd/baha/operator_core_network_binding_native_test.go:86, current product diagnostic string source (file:line).
2. Fetch develop; create fresh branch lane-0428-244-core-network-owner-assertion from 8629450ef3c; confirm `git merge-base --is-ancestor origin/develop HEAD` TRUE.
3. Align stale assertion line 78 (+ fatal line 86 reference) to the current product diagnostic. Stable semantic core checked: unowned native network is refused AND not adopted as external (lines 88-89 unchanged). No product text change needed.
4. Regression via existing native Keycloak/Core shards only (no new CI job, no .github). Local named-form test (never bare `go test ./cmd/baha/`).
5. ONE additive commit, normal push, NEW PR #1767 for 0428-244 (one card = one PR). Verify delivery via ls-remote.
6. ONE run to terminal: native Keycloak/Core docker+podman job-ids GREEN.
7. Write akte + publish to baseharbor-plan origin/main; END + post to coordinator 9142ab1f.

## phrase-alt vs phrase-neu

- phrase-alt (stale, test line 78): `"existing native network lacks a protected Core or shared backend owner"`
- phrase-neu (current product diagnostic, cmd/baha/core_network_binding.go:71 and :73): `"existing native network has no verifiable protected Core or shared backend owner"` (+ actionable tail describing missing runtime inventory / canonical protected owner shape / next step `baha app start`)
- drift: the product went from a terse "lacks a protected Core or shared backend owner" to an actionable "has no verifiable protected Core or shared backend owner: ...". The fail-closed guard comment at core_network_binding.go:62-69 states the refusal (a matching native label without a protected owner must never be adopted) is UNCHANGED; only the message is now actionable. The test now asserts the current phrase; lines 88-89 (unowned net refused, `bound.DefaultNetworkExternal` must be false) are untouched.

## provenance

- fresh branch from develop 8629450ef3c; `git merge-base --is-ancestor origin/develop HEAD` = TRUE.
- `git log --oneline origin/develop..HEAD`: single own commit bfebc35ef (additive, no force/amend/rewrite, no foreign parent).
- `git diff origin/develop...HEAD --name-only` = exactly one file: cmd/baha/operator_core_network_binding_native_test.go.
- PR 1767: OPEN, baseRefName=develop, headRefName=lane-0428-244-core-network-owner-assertion, headRefOid=bfebc35ef46fa98e2ad726d8f603e3afad1f33a8. develop is an ancestor (ahead 1 / behind 0).
- delivery ls-remote: `bfebc35ef46fa98e2ad726d8f603e3afad1f33a8 refs/heads/lane-0428-244-core-network-owner-assertion`.

## regression (local, named form, coordinator host)

- `go test ./cmd/baha/ -count=1 -run TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> PASS (confirmed ran with -v; not skipped).
- sibling `go test ./cmd/baha/ -count=1 -run TestCoreDefaultNetworkBinding ...` (with the same skips) -> ok.
- NOTE: ran on coordinator host with the named -run + required skips; a bare `go test ./cmd/baha/` was NOT used (real lifecycle containers otherwise start; ambient bh-docker-dev-shared-* is missing here).

## hosted run (terminal status)

- run-id: 45020547837 (event=pull_request, head_sha=bfebc35ef, conclusion=SUCCESS).
- failures: 0 across all jobs in the run.
- native Keycloak/Core docker: SUCCESS, job-id 137202320393 (https://github.com/mcpdev80/baseharbor/actions/runs/45020547837/job/137202320393).
- native Keycloak/Core podman: SUCCESS, job-id 137202320476 (https://github.com/mcpdev80/baseharbor/actions/runs/45020547837/job/137202320476).
- These are the two native gates that previously failed on the stale phrase (podman 137197826980 + docker 137197826981 in run 45018856573); both now green on this PR.

## cleanliness

- Test-only change. No product code, no .github, no scripts touched.
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- Working-tree script modifications in the shared working dir (scripts/*.py) were NOT part of this commit; only the one test file was staged + committed.
- cleanliness: only the test file changed; clean.

## END

w27-pr1627-0428-061-pull DONE
