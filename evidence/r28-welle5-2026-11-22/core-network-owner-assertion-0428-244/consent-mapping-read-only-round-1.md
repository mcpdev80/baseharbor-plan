# 0428-227 consent-contract read-only mapping round 1

- READ-ONLY MAPPING fuer OWNER/CORE-ENTSCHEIDUNG. KEIN code-aenderung, KEIN push, KEINE guard-aenderung, KEIN commit/push/merge/kommentar, KEINE subagenten.
- sitz f0f6c8b4. KONTEXT: #1753 selected runtime (head 94b0fd63, run 45019340456) failt an 'app footprint show' / record-deployment MUTATION die --confirm-candidate verlangt (produkt: "Re-run with --confirm-candidate <64hex>").
- STATE (nur, keine aenderung): run 45019340456 conclusion=failure, head_sha=94b0fd63a4. Failure = repository-owned candidate apply ohne --confirm-candidate -> fail-closed refusal (record-deployment mutation).
- remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git (used github.com/mcpdev80 remote); no git write executed.

## PLAN

1. Establish reality (remote guard, #1753 run 45019340456 STATE). No git write.
2. Fact 1: how does the selected-data-capabilities block call 'app footprint show' / record-deployment, and how it differs from core-bootstrap. cmd/baha/app_capability_runtime_test.go selected block + coreBootstrapFixtureConsent definition.
3. Fact 2: does core-bootstrap already use the digest-retry (helper lines); what the helper does (bind digest to context).
4. Fact 3: if selected uses/could-use the same helper, would a pure-TEST digest-retry suffice, or does it touch guard logic (cmd/baha/app_candidate_consent.go digest-pattern / 'refusing to record')?
5. Fact 4: minimum change per option (A: test calls helper like core-bootstrap; B: gate-vertrag/triggerscript) with file:line.
6. Write akte (read-only), no git write beyond akte.

## helper + guard + selected-block (file:line)

- coreBootstrapFixtureConsent DEFINITION: cmd/baha/core_installation_runtime_test.go:642-660.
  - resolves the application, derives the CandidateSubmission via candidateSubmissionForResolvedApp(ctx, resolved) (cmd/baha/app_candidate_consent.go:106), and if submission.SourceRevision != "" binds the canonical digest to the CONTEXT via withCandidateConsentDigest(ctx, delivery.CandidateConsentDigest(submission)) (cmd/baha/app_candidate_consent.go:43-48). Then provider-change consent (withProviderChangeConsent). So the digest is carried on ctx through the apply lifecycle.
- SELECTED-DATA-CAPABILITIES BLOCK: cmd/baha/app_capability_runtime_test.go:129-137.
  - loops {{"app","apply","--skip-memory-preflight"}, {"app","status","--json"}, {"app","doctor","--json"}}. For the apply command it sets commandCtx = coreBootstrapFixtureConsent(t, ctx) (line 133) before runWithIO(commandCtx, command, ...). So the selected apply ALREADY routes through coreBootstrapFixtureConsent.
  - The "selected runtime" that #1753 runs is this app_capability_runtime_test.go flow (sql/secrets/sql-second/https kinds). It does NOT call 'app footprint show' directly here; the record-deployment mutation happens inside 'app apply' via recordDeploymentBeforeMutation.
- APPLY CHOKENOINT: cmd/baha/app_apply.go:192 -> recordDeploymentBeforeMutation(ctx, execution.resolved, "applying", candidateConsentOverride(ctx)).
  - rawCandidateConsent comes from candidateConsentOverride(ctx) (cmd/baha/app_candidate_consent.go:56-59): reads the context value stored by withCandidateConsentDigest. Empty override -> candidateConsentDigestFromError path / missingCandidateConsentError.
- GUARD LOGIC: cmd/baha/app_candidate_consent.go.
  - candidateConsentDigestPattern (digest-pattern): cmd/baha/app_candidate_consent.go:17 -> `(^|[[:space:]])--confirm-candidate[[:space:]]+([0-9a-f]{64})([[:space:]]|$)`.
  - candidateConsentDigestFromError parses the digest from a UsageError.Hint: cmd/baha/app_candidate_consent.go:22-32.
  - missingCandidateConsentError (the "refusing to record" message + "Re-run with --confirm-candidate <digest>" hint): cmd/baha/app_candidate_consent.go:152-157 (message line 154, hint line 155).
  - finalizeCandidateConsent (binds canonical digest, constant-time compare, digest mismatch -> errCandidateConsentDigestMismatch): cmd/baha/app_candidate_consent.go:159-182.
  - recordDeploymentBeforeMutation choke point: cmd/baha/deployment_record.go:400; repository-owned applying guard at :520-542 (finalizeCandidateConsent at :532; stale -> :539; consent==nil -> :543 fail-closed).
- digest hint string provenance (the "Re-run with --confirm-candidate <64hex>" product text): cmd/baha/app_candidate_consent.go:94 (prompt), :155 (missingCandidateConsentError hint); also cmd/baha/runtime.go:127 (usageError).

## Fact 2: does core-bootstrap already use the digest-retry?

YES. coreBootstrapFixtureConsent (cmd/baha/core_installation_runtime_test.go:642-660) binds the digest to the CONTEXT (withCandidateConsentDigest, cmd/baha/app_candidate_consent.go:43-48) whenever submission.SourceRevision != "". The apply path reads it via candidateConsentOverride(ctx) (cmd/baha/app_apply.go:192). So the core-bootstrap path does NOT need a CLI --confirm-candidate flag; the digest travels on ctx. The helper's retry semantics = the digest is recomputed from the CURRENT resolved application (candidateSubmissionForResolvedApp, cmd/baha/app_candidate_consent.go:106) on every call, so a fresh apply re-derives the current digest automatically. No separate "parse Re-run with --confirm-candidate" scan is needed for the ctx path — the digest is already bound.

Note: the ONLY place that PARSES "Re-run with --confirm-candidate <digest>" out of a printed hint is candidateConsentDigestFromError (cmd/baha/app_candidate_consent.go:22-32) — used when a UsageError is returned and the caller wants to auto-retry with the parsed digest (e.g. cmd/baha/app_coreless_runtime_test.go:153, cmd/baha/app_backup_runtime_fixture_test.go:615/648/707/754). That is the "digest-retry via helper" the 0428-236 card references.

## Fact 3: would a pure-TEST digest-retry suffice, or does it touch the guard?

- The selected-data-capabilities apply at cmd/baha/app_capability_runtime_test.go:133 ALREADY calls coreBootstrapFixtureConsent(t, ctx), which binds the digest to ctx. So for the sql/secrets/https kinds, the digest is ALREADY carried through the apply and finalizeCandidateConsent should succeed WITHOUT any guard change.
- The #1753 failure therefore indicates the digest binding is NOT reaching the apply for the specific kind/command that failed — most likely a path that does NOT go through coreBootstrapFixtureConsent (a direct 'app apply' / 'app footprint show' / record-deployment call without the helper), OR the digest was cleared between helper and apply (e.g. an intermediate command that re-resolves the app and the submission.SourceRevision became empty).
- A pure-TEST digest-retry (re-run the failing command with the digest from coreBootstrapFixtureConsent bound to ctx, or re-parse 'Re-run with --confirm-candidate <digest>' via candidateConsentDigestFromError and retry) touches NO guard logic: finalizeCandidateConsent / candidateConsentDigestPattern / 'refusing to record' stay untouched (cmd/baha/app_candidate_consent.go:17,152-157,159-182; cmd/baha/deployment_record.go:400,520-542). It is a test-only invocation fix.
- BUT: the digest is bound to the ctx by coreBootstrapFixtureConsent, which requires the app to have a repository SourceRevision (cmd/baha/core_installation_runtime_test.go:649). If the selected flow resolves an app with SourceRevision == "" (no repository candidate), the helper binds nothing and the apply fails closed by design — a pure test change cannot make that pass without also binding a digest, and the guard is CORRECT to refuse.

## option-A vs option-B (minimum change per option, file:line)

- OPTION A (test-only, test calls the helper like core-bootstrap):
  - Locate the failing apply/footprint-show/record-deployment invocation in the selected-data-capabilities block that runs WITHOUT coreBootstrapFixtureConsent (cmd/baha/app_capability_runtime_test.go, the selected kinds loop around lines 129-333). Ensure the digest is bound to the ctx for that invocation — either (i) wrap it in coreBootstrapFixtureConsent(t, ctx) like line 133 does, or (ii) capture the digest the helper computes (delivery.CandidateConsentDigest(submission), cmd/baha/app_candidate_consent.go:85,153) and bind it via withCandidateConsentDigest(ctx, digest) (cmd/baha/app_candidate_consent.go:43-48) before the apply.
  - Alternatively (if the failing path returns a UsageError carrying the hint): parse the digest with candidateConsentDigestFromError (cmd/baha/app_candidate_consent.go:22-32) and retry the apply with the parsed digest bound to ctx.
  - Minimum change: ONE test file (cmd/baha/app_capability_runtime_test.go), no guard change, no product change. Does NOT touch cmd/baha/app_candidate_consent.go (guard) — only consumes the existing helper/parse.
  - CONDITION: requires the resolved app to carry a repository SourceRevision so the helper actually binds a digest (cmd/baha/core_installation_runtime_test.go:649). If SourceRevision == "" the helper binds nothing and option A cannot succeed without a product change.
- OPTION B (gate-vertrag / triggerscript):
  - If the selected-data-capabilities test is a gate that must supply --confirm-candidate as a real CLI flag (not ctx), the minimum change is in the gate/trigger script that invokes the selected test or the apply: add `--confirm-candidate <digest>` to the 'app apply' call, where <digest> is the confirm-hash the product prints (cmd/baha/app_candidate_consent.go:94 prompt, :155 missingCandidateConsentError hint). This is a CI-gate/trigger-script change (Owner scope .github/**) — report as STATE with file:line, do not edit.
  - Alternatively, if the gate must set the digest on the environment, bind it via the same ctx helper before the apply in the gate harness (test-only, option A).

## conclusion (facts only, no decision)

- The selected-data-capabilities apply (cmd/baha/app_capability_runtime_test.go:133) ALREADY routes through coreBootstrapFixtureConsent, which binds the digest to ctx; the apply reads it via candidateConsentOverride(ctx) (cmd/baha/app_apply.go:192). The fail-closed guard (finalizeCandidateConsent, cmd/baha/app_candidate_consent.go:159-182; cmd/baha/deployment_record.go:520-542) is unchanged and correctly refuses without a matching digest.
- Option A (test-only) does not touch the guard; it requires the resolved app to carry a repository SourceRevision so the helper binds a digest (cmd/baha/core_installation_runtime_test.go:649). Option B is a CLI-flag / gate-trigger change (Owner scope).
- No change made. No guard, product, .github, or scripts touched.

## cleanliness

- READ-ONLY. No product code, no guard, no test code, no .github, no scripts changed.
- No git write executed (no commit/push/merge/comment). No git branch checked out for editing.
- No container/network/volume/state created. No docker/podman compose project started.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE
