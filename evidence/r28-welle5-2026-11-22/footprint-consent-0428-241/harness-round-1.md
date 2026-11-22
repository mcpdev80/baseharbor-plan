# 0428-241 — footprint-show / record-deployment digest-consent harness (round 1)

Card: 0428-241 (footprint-show digest consent harness).
Sitz: ffe7611b. Target branch base: develop HEAD `68b26bd78c3de89e11252e6d04a8d3ed16c804a7` (verified ancestor via `git merge-base --is-ancestor origin/develop HEAD` before first edit).

## PLAN

1. Establish reality (remote guard): both `origin` and `lane-origin` resolve to `https://github.com/mcpdev80/baseharbor.git`; branch `lane-0428-241-footprint-consent` clean at develop HEAD `68b26bd7`, no commits, no PR.
2. Read mission `/tmp/opencode/m_241b.md.g` (card 0428-241, test-only, develop 68b26bd7); confirm `/var/tmp/m/fix241b.md.g` is an unrelated card (0428-063) — ignored.
3. Trace product choke point: `recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:400-558`) requires the exact `--confirm-candidate` digest at state `applying`; empty → `errConsentRequiredForCandidateSubmission` (exit 2); wrong digest → `staleCandidateConsentError` (`deployment_record.go:539`). Digest derived from `repositoryDesiredStateFingerprint` via `candidateSubmissionForResolvedApp` (`app_candidate_consent.go:106-130`).
4. Identify the build breaker in the working-tree harness `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` (`cmd/baha/app_capability_runtime_test.go`): initial `go test` failed with `too many arguments in call to extractCandidateConfirmDigest have (*testing.T, string) want (string)`.
5. Apply the fix: the harness now parses the refusal transcript through a local helper `extractFootprintShowConfirmDigest(out string) string` (lines 428 + 458-473), matching the `(out string) string` signature used at `repository_runtime_fixture_test.go:41` and `app_coreless_runtime_test.go:152`. No product touch.
6. Verify build + vet: `go build ./cmd/baha/` OK, `go vet ./cmd/baha/` OK. The test self-skips unless `BASEHARBOR_CORELESS_ACCEPTANCE == "1"` (native-runtime test).
7. Audit CI reachability of the new test against the selected data-capabilities gate.
8. Decision: report CI wiring as an Owner `scripts/**` finding; stop and post END with the exact file:line needed.

## repo-rule compliance

- Test-only. Only `cmd/baha/app_capability_runtime_test.go` changed (working tree). No `internal/`, `.github/`, `scripts/`, `deployment_record.go` product path, `operatorauth`, `controlplane/`, `runtime/`, `app_broker.go` touched.
- Additive intent. No commit made yet — see blocked section.

## CI reachability audit (found, not fixed)

The new test `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` (self-skips unless `BASEHARBOR_CORELESS_ACCEPTANCE == "1"`) is selected by the `coreless-lifecycle`/`data-capabilities` native gates because `cmd/baha/app_capability_runtime_test.go` is a `source.cmd.baha.app.capability.runtime.test.go` component. But it is never EXECUTED by either runner:

- `scripts/ci-native-pr-gate.sh:80-83` — `native/docker/data-capabilities` runs only `run_exact_test TestApplicationCapabilityLifecycleExistingCore 20m` (hardcoded single test name). My test is not in the gate's run list, so the runner executes a zero-test `go test` pass → no evidence.
- `scripts/pre-release-integration.py:63-82` — `CORELESS_SHARD_TESTS['core-capability']` runs only `TestApplicationCapabilityLifecycleExistingCore`. `coreless_anchor_checks` (line 114) iterates `CORELESS_TEST_ANCHORS` by exact name; my test is absent.
- Coverage catalog `scripts/pr-gate-coverage.json` pins the component's `required_test_names` to exactly `["TestApplicationCapabilityLifecycleExistingCore"]`, and `scripts/test_pr_gate_coverage.py:236` (test_coreless_fixture_acceptance_files_are_anchored_to_both_integration_gates) asserts that pin. Adding my test would require editing the catalog + that test.

Both runners (`scripts/`) and the catalog are Owner scope (Owner directive: `.github/**` and CI routing are the Owner's; report a failing check as STATE with file:line and stop). Per the CI gate rule (2026-11-20) this is the single carve-out: the route change is outside this card's write-set.

## BLOCKED

CI wiring needed so the new digest-consent test actually RUNS (not a zero-test pass). Exact change required, Owner to implement (NOT in my write-set):

1. `scripts/ci-native-pr-gate.sh:80-83` — add `run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent 20m ./cmd/baha BASEHARBOR_CORELESS_ACCEPTANCE=1` to the `native/docker/data-capabilities` (and the `coreless-lifecycle`) gate, OR run the test via a new discrete gate entry.
2. `scripts/pre-release-integration.py:76-82` — add `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` to `CORELESS_SHARD_TESTS['core-capability']` (or `CORELESS_OPTIONAL_TESTS`) so the pre-release integration runner executes it.
3. Optionally extend `scripts/pr-gate-coverage.json` `required_test_names` and the asserting test `scripts/test_pr_gate_coverage.py:236` to cover the second anchor (must remain exactly-one per existing anchor contract).

Without (1) or (2), the selected `data-capabilities` job runs a zero-test `go test` on my file: the digest-consent fix is not durable evidence.

## Test-only digest-consent wired (app_capability_runtime_test.go), no product touch.

## Next

- After Owner wires the gate: run the new test on the named docker host (`go test ./cmd/baha/ -count=1 -run TestApplicationCapabilityLifecycleFootprintShowDigestConsent -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` under `BASEHARBOR_CORELESS_ACCEPTANCE=1`), additive commit, normal push, verify with `git ls-remote`, then re-post END with run-id.

## End state

- class: END_BLOCKED (CI wiring is Owner scope; build fix + digest wiring complete and verified)
- run-id: (none — test not yet executed; blocked on CI gate registration)
- branch: `lane-0428-241-footprint-consent` at develop HEAD `68b26bd7`
- cleanliness: working tree contains one uncommitted test-only edit (`M cmd/baha/app_capability_runtime_test.go`); no containers, compose projects, volumes, or state dirs started on the coordinator host.
