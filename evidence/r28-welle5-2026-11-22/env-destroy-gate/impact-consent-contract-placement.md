# Read-only placement review — card 0428-226 / impact consent after preview

## PLAN

1. Read the current 0428-226 task contract and inspect the current exact source refs without treating card text as authority to modify code.
2. Trace the provider-change rejection path, separating plan-ID validation from semantic provider-authority revalidation.
3. Locate where preview consent is issued and how stop/apply re-resolves target, deployment identity, mode, and retirement authority.
4. Give a file:line recommendation for binding preview consent while preserving stale protection; this is analysis only, not a verdict or implementation.
5. Publish this evidence to Planning origin/main, update the live board, and post END.

## Source and remote witnesses

The product remote was verified as `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push). Fresh `git ls-remote` gave develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`, #1627 `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`, #1736 `4c919fd61f3214fe435bafdc6281bf4bcb300022`, #1723 `5c063c7f278bfd92dcef9a0fabd3b6e6d1ddbe42`, and #1752 `5cb139a6e4e8987b9ef5ddf6398a8d13d1f97105`. `git rev-list --count` from #1627 b3 and #1736 4c to the fetched develop head is 8 for each. This is a read-only contract analysis; no verdict is issued on either stale PR head.

The Planning remote was verified as `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push). The 0428-226 card `t-20261122-impact-consent-after-preview-contract` is in `ready` state and asks for a single consent contract, exact current-target rejection coverage, and a passing exact-candidate Docker plus rootless Podman lifecycle run.

## Finding

The message text alone does not identify which comparison rejected the hosted request. `ProviderChangeError.Error()` prefixes every such code as `provider change` (`internal/application/provider_change_consent.go:46`); the same `stale-impact-consent` code can arise from PlanID equality, semantic authority comparison, or the stop-to-retirement binding. The prior artifact’s one-line error is therefore insufficient to conclude that the failing compare was or was not a plan hash.

The explicit provider-authority revalidation branch is `cmd/baha/application_provider_authorization.go:70-76`: after a `PlanID` difference it calls `application.ValidateProviderImpactRevalidation`. That helper (`internal/application/provider_consent_authority.go:707-725`) accepts equal IDs directly; when IDs differ, it compares the frozen `Authority` surfaces via `ConsentAuthority.Equivalent`, and rejects if they differ or either plan lacks the frozen surface. `Equivalent` preserves the security-sensitive target, confirmation/destructive flags, registry, required set, impact set, facts, consumers, and activity (`internal/application/provider_consent_authority.go:377-429`). This is the correct semantic comparison for benign digest churn while retaining fail-closed behavior for changed authority.

The current environment KEEP path has separate consent-binding checks. `applicationStopPlan` stores only `retirementPlanID` (`cmd/baha/application_stop_impact.go:19-25`), populated from the retirement impact’s `PlanID` (`:66-74`). Preview consent is read, emitted with the stop plan, validated, and then the stop plan is rebuilt at `authorizeApplicationStop` (`:177-217`); it rejects a changed scope `PlanID` at `:214-215`. The destroy apply calls that stop authorization and compares the stored retirement ID against the apply-time retirement `PlanID` at `cmd/baha/app_runtime_retirement.go:107-117`; after intent revalidation, it rebuilds retirement and compares IDs again at `:122-130`. Each branch can emit the same generic `provider change: stale-impact-consent` text.

Recommendation: the preview-to-apply bind point is the stop-plan reconstruction at `cmd/baha/application_stop_impact.go:210-215`, together with the stop/retirement cross-bind at `cmd/baha/app_runtime_retirement.go:112-117`. Have the preview contract retain the frozen retirement/provider authority surface, rather than only its `PlanID`, and revalidate it with the same semantic authority-equivalence rule at apply. Keep explicit stable identity checks for target, environment, deployment UUID, KEEP versus DELETE, stop mode, and the owner/retirement scope; any change to those must remain stale. The current `retirementPlanID`-only field at `application_stop_impact.go:25` is the information loss that prevents this path from using semantic revalidation. Add a deterministic negative assertion for target/deployment change as the card already requires. This identifies a sound placement; it is not a verdict, REQUEST CHANGES, or code change.

## repo-rule compliance

Read-only review of the owner-authorized 0428-226 question. No product edits, tests, hosted runs, workflow actions, PR comments, merges, or closes. The current #1627 review remains stopped with no verdict.

## cleanliness

Shell PID `1209996`: `docker ps -a` before and after returned the same eight pre-existing exited containers, with IDs `268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, and `9d3f1a2b1e0e`. No container or compose project was started or changed.

END_DONE codex-rev-1747: read-only 0428-226 placement recommendation published; provider semantic compare is application_provider_authorization.go:70-76 and preview bind belongs at application_stop_impact.go:210-215 with full authority retained.


## Planning remote tree witness

After `git -C baseharbor-plan fetch origin main`, `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/env-destroy-gate/impact-consent-contract-placement.md'` returned exactly:

`evidence/r28-welle5-2026-11-22/env-destroy-gate/impact-consent-contract-placement.md`


## PLAN — hold instruction follow-up

1. Read `/var/tmp/rev1723hold.g.md` and preserve its queue decision as the current instruction.
2. Keep #1723 out of review until the new external gate card 0428-227 delivers; do not issue a verdict, merge, or close.
3. Retain 0428-226 as the only permitted read-only fallback; its consent-placement analysis above is complete, with no additional product inspection or changes.
4. Record the mission-provided CI state and this hold in Planning evidence, update the board, and verify publication.

## Queue hold state

Mission `/var/tmp/rev1723hold.g.md` (SHA-256 prefix supplied there: `460b0408f370`) removes #1723 from this review queue. Mission-provided status: exact head `b9c2e483f8b` run `44963676934` completed with FAILURE; Docker guided job `137028211092` succeeded, while data-capabilities job `137028211165` and aggregate `137030140112` failed. The mission attributes the defect to `cmd/baha/ci_integration_operator_enabled.go:135`, with predicate at `:232-233` and fail-closed behavior at `:180`; it identifies new dep-free card 0428-227 for the fix. These are recorded as the supplied state, not as an independently reviewed verdict.

No action was taken on 0428-227. The only fallback task, 0428-226, remains a read-only placement recommendation above. No product source, tests, PR state, or CI were changed or triggered.

## cleanliness — hold follow-up

Shell PID `1243640`: `docker ps -a` before and after returned the same eight pre-existing exited containers (`268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`). No container or compose project was started or changed.

END_DONE codex-rev-1747: #1723 held outside review pending 0428-227; 0428-226 remains completed read-only analysis; no verdict, merge, close, product changes, or CI action.

Final pre-push tree command output:

evidence/r28-welle5-2026-11-22/env-destroy-gate/impact-consent-contract-placement.md
