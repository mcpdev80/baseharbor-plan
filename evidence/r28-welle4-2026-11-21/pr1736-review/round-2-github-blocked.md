# PR #1736 - verdict booking when GitHub refuses the review (card 0428-055, Owner-held)

  - candidate: `a595472b77fb3620fac1dd457448211a86e3be24`, branch `codex/env-destroy-gate-routing`, base develop,
    Ready run `44928428184` = completed/success at this exact head (coordinator-measured, `ls-remote` equality for
    `refs/pull/1736/head` and the branch).
  - reviewer session `fecbada9` (CODEX-REVIEW), first pass recorded in `round-1.md` at plan SHA `f8cae90c63f1`:
    **APPROVE CONTENT with a pre-merge condition**.
  - second pass, confirmed against current source by the reviewer and re-measured by the coordinator:
      - `scripts/validate-pr-gate-coverage.py` validates `required_test_names` **syntactically only**;
      - `scripts/pre-release-integration.py` omits `TestEnvironmentDestroyNativeLifecycle` from `CHECKS`,
        `CORELESS_TEST_ANCHORS` and `CORELESS_SHARD_TESTS` (at the PR head the anchor list still names only
        `TestManagedRegisteredOTLPNativeConsumerHandoff`, line 76) - so both selected native gates can go green without
        executing the test the PR maps.
  - submission attempt: `REQUEST_CHANGES` at the exact head with an inline comment on `scripts/pr-gate-coverage.json:1475` was
    **rejected by GitHub because the same account authored the PR**. No comment exists on the PR and no code changed.
  - consequence, stated so no later reader mistakes an empty field for missing proof: `reviewDecision` stays empty for this PR
    for a structural reason. Per AGENTS 3.7/5.2 the authoritative verdict is this akte, not the GitHub review field.
  - disposition set by the coordinator: PR #1736 stays OPEN and draft; no CODEX-MERGE order. The only blocking item is the
    runner registration in `scripts/pre-release-integration.py` (Owner scope, requested three times, ledger rows 940/944c/947).
    #1627 must not be accepted as native proof before that catalog/shard entry exists.
