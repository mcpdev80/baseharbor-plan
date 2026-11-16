# CODEX-REVIEW — Luna batch 16

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch16.md` · PR #1650, card 0428-078.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`).

## Candidate and current PR states

- Authenticated GitHub account: `mcpdev80`.
- PR #1650 is OPEN/DRAFT; base `lane-0428-080-r28-perses-selection` @ `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`; head `lane-0428-078-perses-identity-on-resolver` @ `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`.
- Exact-head run `43934658620` is `pull_request`, completed SUCCESS on the exact head. It has 6 successful draft jobs and 24 skipped jobs. The skipped jobs include `PR Selected Checks`, `PR · Go unit`, `PR · Native Keycloak/Core`, `PR · Public Contracts`, `PR · Exact Candidate`, and `PR · Selected Runtime`. The draft Go package/shard jobs did run; this is not full required-gate evidence.
- PR #1660 remains OPEN/DRAFT on `f709e14b58f55be9e6ef93323e31bb9166aa04e8`, base `develop` @ `13ffdd15d24fcfb4a379c834d25450ebb2737a6a`; it is not merged.
- No local product tests were run by this reviewer.

## Functional review

The production path in `cmd/baha/app_status_result.go` resolves Keycloak placement, calls `IdentitySelectionWitnessAt`, and sets `identity_dashboard_eligible` from `NonForgeableAvailable()`. The witness derives selection from the manifest, authorization from validated non-external provider placement, and metric presence/currentness from the observability registry entry matching provider `keycloak` and ID `keycloak-metrics`. It does not derive eligibility from a caller-supplied status.

The positive witness regression seeds a valid Keycloak metrics source in the registry and uses resolved BaseHarbor-owned placement. Negative regressions cover missing signal, unselected provider, and external placement. The 097 registration test separately invokes `registerKeycloakSignals`, lists the real registry, and verifies the exact native ID/protocol/path; its disabled-metrics case fails closed. The 080 non-forgeability regression remains unchanged in the current PR diff. These code paths are consistent, but the positive witness test and registrar test are separate tests; the round-4 end-to-end observation is reported in the worker akte and is not itself a CI test.

## Integration and evidence findings

### Duplicate 097 patch is not ancestry-equivalent

The current #1650 diff includes `internal/identityprovider/keycloak_realization.go` and `internal/identityprovider/keycloak_signal_registration_test.go`, the same two files changed by #1660. Their blob SHAs at #1650 head and #1660 head are identical. However, #1650's registration commit `325ab0d4` has parent `d94d477d`; the #1650 commit list contains neither #1660 commit `f709e14b` nor old head `972a78da`. This is patch equivalence, not shared commit ancestry. Thus integrating both PRs as currently presented is not automatically clean at the PR/change-set level: #1650 still carries 097-owned files in its diff. After the 097 patch is integrated into the target base, rebase/deduplicate #1650 and verify these two files disappear from its diff before any merge. Until then, the exact #1650 candidate is not a clean one-card integration candidate.

The initial `972a78da` head was replaced on the owned draft branch and is absent from the current PR commit list; its run `43933249045` is superseded. The exact current head has a new run, so the old run is not evidence. The non-fast-forward branch rewrite is a process deviation to record; the available evidence shows no remaining dependency on that abandoned head.

### CI evidence wording does not match GitHub

The round-4 akte says required jobs such as `PR · Go unit`, `PR · Native Keycloak/Core`, `PR · Public Contracts`, and `PR · Exact Candidate` executed and passed. GitHub reports those jobs as skipped in run `43934658620`. Correct the evidence record; do not use the skipped jobs as acceptance evidence. The exact-head SUCCESS is the draft workflow result, not proof those gates passed.

## Verdict

**REQUEST CHANGES / ACCEPTANCE HOLD** for PR #1650 at `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`. The resolver logic is consistent with the owner chain, and the 080 non-forgeability regression is intact. The candidate still carries the separate 097 registration patch without its commit ancestry, and its review akte overstates which exact-head CI jobs ran. Recipe: after 097 is integrated into the target base, rebase/deduplicate 078 so the two 097-owned files are no longer in #1650's diff; verify only 078-owned changes remain and preserve the 080 tests; correct the run evidence to distinguish six successful draft jobs from 24 skipped checks; then obtain the exact required checks for the post-rebase candidate. **078 is not acceptance-ready under frost yet.**

## repo-rule compliance and turn-start flags

- Read-only product review; no product code, PR state, CI, task state, or release state changed. No merge, approval, or GitHub review mutation.
- Turn-start flags forwarded to the coordinator: worker pool 0/4; `NO_ELIGIBLE_WORK` holds on ornith:1, ornith:2, laptop:1, laptop:2; 40 open PRs.
