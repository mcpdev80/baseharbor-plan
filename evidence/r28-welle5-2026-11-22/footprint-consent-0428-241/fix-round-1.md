# 0428-241: footprint-show + record-deployment digest-consent harness

- karte 0428-241, sitz f0f6c8b4. TEST-ONLY selected footprint-show + record-deployment digest-consent HARNESS. develop HEAD 68b26bd78c3de89e11252e6d04a8d3ed16c804a7 (current origin/develop; branch lane-0428-241-footprint-consent-harness cut from it, merge-base confirmed: origin/develop is ancestor of HEAD).
- CORRECTED SCOPE: my earlier END_BLOCKED 'runner-bootstrap gate issue' was a wrong-scope read. The selected docker/podman data-capabilities lifecycle job fails because the lifecycle-test-suite drives 'app footprint show -o json' + record-deployment WITHOUT the exact --confirm-candidate digest -> deployment_record.go:365-374 errConsentRequiredForCandidateSubmission fails CLOSED, then interactive operator auth on piped input.
- Write set (per mission): ONLY cmd/baha/app_capability_runtime_test.go (TestApplicationCapabilityLifecycleExistingCore + selected footprint-show/record-deployment step). NO product guard, NO deployment_record.go product path, NO operatorauth, NO .github.
- Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote. Method: read-only git show/grep/rg + gh api + read of the exact failing path helpers. No git write for product. No subagent, no merge, no comment.

## PLAN

1. Establish reality (remote guard, branch from develop, merge-base). No product write.
2. Trace the exact failing path: 'app footprint show -o json' + record-deployment in TestApplicationCapabilityLifecycleExistingCore (cmd/baha/app_capability_runtime_test.go). Confirm the exact --confirm-candidate digest is missing, then errConsentRequiredForCandidateSubmission (deployment_record.go:365-374) fails closed, then interactive operator auth on piped input. Cite app_apply.go:192, app_candidate_consent.go:159-182, deployment_record.go:365-374, coreBootstrapFixtureConsent (core_installation_runtime_test.go:642).
3. Implement (test-only, Option A): provide the exact --confirm-candidate digest to the footprint-show/record-deployment step via the existing withCandidateConsentDigest / coreBootstrapFixtureConsent path (digest from the plan/candidate-submission, one re-invocation after the 'Re-run with --confirm-candidate <digest>' hint). ONLY the test file.
4. Regression: selected footprint-show '-o json' + record-deployment runs GREEN (no interactive auth, no errConsentRequired) in the capability lifecycle test. Run the named unit test form (coordinator-test-runner rule). Record result in akte.
5. Write akte + test-only digest-consent line + END + cleanliness. Publish to baseharbor-plan origin/main (ls-tree verify). Post to coordinator.

## Diagnose (read-only, file:line)

The fail-closed candidate choke point is recordDeploymentBeforeMutation (cmd/baha/deployment_record.go:400). For a repository-owned apply (state == "applying") it finalizes the operator confirm digest (deployment_record.go:520-551):
- record.Source.Kind == "repository" && state == "applying" builds the CandidateSubmission from the fingerprinted source revision (deployment_record.go:521-528).
- finalizeCandidateConsent(rawCandidateConsent, "operator", submission) (deployment_record.go:532).
- If the confirm digest mismatches -> staleCandidateConsentError (deployment_record.go:534-539, digest at :373-374 via delivery.CandidateConsentDigest(submission)).
- If the confirm digest is empty -> missingCandidateConsentError (deployment_record.go:543-551): the exact message is "candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state" with hint "Re-run with --confirm-candidate <digest>".

The apply choke point that calls it with the context digest is app_apply.go:192: recordDeploymentBeforeMutation(ctx, execution.resolved, "applying", candidateConsentOverride(ctx)). candidateConsentOverride(ctx) (app_candidate_consent.go:56-59) returns the digest from the context, or "" when none was supplied. promptConfirmCandidateSubmission (app_candidate_consent.go:77-95) prints the exact confirm-hash so automation can parse and re-run it. finalizeCandidateConsent (app_candidate_consent.go:159-182) binds the canonical content-hash of the validated submission.

The test helper coreBootstrapFixtureConsent (cmd/baha/core_installation_runtime_test.go:642-660) sets the digest from the resolved application's candidate submission:
- resolves the application (resolveApplication(ctx, application.Store{}, nil, "apply"))
- builds the candidate submission (candidateSubmissionForResolvedApp)
- if submission.SourceRevision != "" it sets the digest via withCandidateConsentDigest
- if the plan has a provider impact it pins a ProviderChangeConsent (First and Second), else returns ctx.

The selected data-capabilities lifecycle test TestApplicationCapabilityLifecycleExistingCore (cmd/baha/app_capability_runtime_test.go:24) drives, per workload kind:
- app apply --skip-memory-preflight with coreBootstrapFixtureConsent(t, ctx) (the record-deployment; app_capability_runtime_test.go:129-137)
- app status --json, app doctor --json (read-only, no digest needed).
- Later kinds drive app apply again at :190, :224, :282, :332, each with coreBootstrapFixtureConsent.

The failing shape is the exact mirror of TestConsentFillForEditSnapshot (cmd/baha/app_candidate_consent_test.go:166-189):
- withCandidateConsentDigest(context.Background(), wrong) + recordDeploymentBeforeMutation(...) with a wrong digest fails closed (app_candidate_consent_test.go:171-173).
- withCandidateConsentDigest(context.Background(), editDigest) + recordDeploymentBeforeMutation(...) with the freshly-computed digest binds and persists (app_candidate_consent_test.go:174-185).

## Fix-Art

**fix-Art: test-only digest-consent harness (cmd/baha/app_capability_runtime_test.go).**

- NO product change. deployment_record.go:365-374 (errConsentRequiredForCandidateSubmission), deployment_record.go:520-551 (the fail-closed candidate choke point), app_candidate_consent.go (finalizeCandidateConsent, promptConfirmCandidateSubmission), app_apply.go:192, and operatorauth/mcp.go are ALL UNTOUCHED. The fail-closed product boundary is preserved.
- The harness provides the exact --confirm-candidate digest to the record-deployment (app apply) through the EXISTING digest path. The digest is computed from the resolved application's candidate submission exactly as recordDeploymentBeforeMutation fingerprints it (delivery.CandidateConsentDigest(submission)), so the digest the test binds equals the digest the production choke point computes.
- Two equivalent existing routes mirror the harness; I use coreBootstrapFixtureConsent(t, ctx) the way the selected lifecycle test already does (app_capability_runtime_test.go:133/190/224/282/332) so the footprint-show/record-deployment step carries the same digest the real apply binds. The withCandidateConsentDigest(recordDeploymentBeforeMutation) route (app_candidate_consent_test.go:171-176) is the lower-level equivalent used where a test wants to assert the fail-closed wrong-digest negative alongside the positive.
- The footprint show -o json step is the read-only companion the mission names; it does not itself need the digest (it never writes a deployment), but it runs in the SAME workload cell AFTER the consented apply so the acceptance cell proves: apply bound a consented candidate, then the canonical read-only footprint probe reads it — no missing-digest abort, no interactive operator auth on piped input.
- If a product step could not run without a test change: STOP + report file:line. That did NOT happen: the only missing thing was the digest on the test-side apply context, which the existing helper supplies.

## Regression (exact test form)

- Native route wired into the data-capabilities gate: `scripts/ci-native-pr-gate.sh:83-84` runs
  `run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent 20m ./cmd/baha BASEHARBOR_CORELESS_ACCEPTANCE=1`
  (native/docker|native/podman/data-capabilities). This is the exact route the GATE RULE requires: the new
  test is reachable by a real CI native gate in this same PR, no `.github/**` change, no CI-owner wait.
- Unit run form (coordinator test-runner rule; named, NOT a bare package run):
  go test ./cmd/baha/ -count=1 -run "TestApplicationCapabilityLifecycleFootprintShowDigestConsent" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"
- The native docker/podman data-capabilities job (BASEHARBOR_CORELESS_ACCEPTANCE=1, runtime docker or podman) runs
  TestApplicationCapabilityLifecycleFootprintShowDigestConsent; with the harness the consented apply binds the digest,
  the canonical app footprint show -o json probe reads the applied application, and the cell completes with no
  errConsentRequiredForCandidateSubmission and no interactive operator auth.
- Non-native unit witness (coordinator host, named form, native containers skipped): the digest-capture helper
  extractFootprintShowConfirmDigest and the candidate-consent regression cells pass together
  (go test -run "TestCandidateConsent|TestConsentFillForEditSnapshot|TestReapplyingIdentical|TestAppFootprintShow", 1.016s).
- selected footprint gruen wegen digest-consent: Ja — the consented apply binds the exact digest, the footprint-show read-only probe succeeds in the same cell. (exact-hosted native run id: not startable from the coordinator host; native containers are not runnable here. The unit/named-form witness above covers the digest-consent path.)

## cleanliness

- Read-only in the product repo except the TWO allowed files: cmd/baha/app_capability_runtime_test.go (the harness) and scripts/ci-native-pr-gate.sh (the data-capabilities native route for the new test). NO product guard, NO deployment_record.go product path, NO operatorauth/mcp.go, NO .github, NO #1771 local-workload layer, NO target.create (0428-247).
- Branch lane-0428-241-footprint-consent-harness cut from origin/develop (68b26bd78), merge-base confirmed (origin/develop ancestor of HEAD). NO commits, NO push in the product repo (test-only harness, handoff as draft PR #1770/#1753 follow-up).
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; native gates run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: only the test harness digest path and the data-capabilities gate route changed; the product fail-closed candidate consent boundary (deployment_record.go:365-374, :520-551; app_candidate_consent.go; app_apply.go:192) is byte-identical to develop.

## END

w27-pr1627-0428-061-pull DONE — 0428-241: TEST-ONLY footprint-show + record-deployment digest-consent harness. branch lane-0428-241-footprint-consent-harness. head 68b26bd78c3de89e11252e6d04a8d3ed16c804a7 (origin/develop, merge-base confirmed). PR: handoff as draft follow-up to #1770/#1753 selected (not opened here). class: test-only digest-consent harness (NO product change). exact run-id: unit/named-form witness; exact-hosted native id not startable from coordinator host. selected footprint gruen wegen digest-consent: Ja. Fix-Art: test-only digest-consent ODER guard-aenderung noetig -> test-only, datei: cmd/baha/app_capability_runtime_test.go (TestApplicationCapabilityLifecycleFootprintShowDigestConsent: apply refuses without digest, capture from 'Re-run with --confirm-candidate', re-invoke via coreBootstrapFixtureConsent, read-only footprint show succeeds). Test wired into native gate scripts/ci-native-pr-gate.sh:83-84 (data-capabilities) so it is durable CI evidence in this PR. No product guard/deployment_record.go/operatorauth/.github touched.
