# Codeman: current CI work order

## Owner instruction — 2026-11-03

Remove the old evidence path completely from CI, Pre-Release and Release. Required tests execute normally and their job results determine success. No gate manifests, evidence collection/reverification/reuse, Actions run/job rechecking, receipt approval or shadow chain remains active. The only CI record is a small Planning file containing merge commit SHA and PR number.

Rulesets stay disabled until CI works. GitHub-hosted runners only; no jobs on the Owner's self-hosted machines. No release or tag is authorized. Preserve runtime isolation, actual assertions, failing/missing-job handling, source identity and immutable consumer pins. Build/image artifacts used by later jobs are normal inputs, not CI evidence.

## Assigned work and ownership

[CI simplification](../../tasks/t-20261103-ci-plain-checks.md) owns the replacement and coordinated workflow/script/documentation changes. Preserve all active product claims and unpublished work. Use disjoint file ownership and the existing Coordinator's small parallel iterations. Do not restore old mechanisms to satisfy historical task wording.

[Receipt source recovery](../../tasks/t-20261103-ci-receipt-source-recovery.md) fixed the productive default-branch writer; records for PRs 1341, 1342 and 1344 exist. The existing Planning credential worked. No speculative token replacement is required. Receipt retries use the existing merged-PR dispatch, without querying CI results.

The normal package-test routing correction for authority/stableid/serviceaccess remains a real test-selection requirement; coordinate its reserved files with CI simplification. Product owners retain their product files. A new CLI test must actually execute through the selected normal test job; formatting/build alone does not prove its assertions.

## Acceptance and release boundary

The replacement must retain required tests and reject failing, missing, cancelled or improperly skipped work through ordinary workflow dependencies. Validate the focused behavior and workflow syntax locally, then inspect the actual normal hosted result before integration. Planning render/check and current CardBoard views must be refreshed. Do not claim a successful workflow or completed task from a receipt file.

The four domain CI cards cover their actual accepted interfaces, not an additional evidence authority. Keep current dependencies and Ready work honest. Owner-delegated Maintainer authority applies within the assigned implementation; no independent review is claimed unless one occurred. No release, tag or ruleset activation is implied.

## Preserved history

The [previous work order](https://github.com/mcpdev80/baseharbor-plan/blob/6a687317d2540106a0ff790d78e5ea05ab84a178/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md), old V1 receipts, acceptance results and release records remain historical. Their live/approve/retained and manifest requirements are superseded, not current prerequisites. Draft PRs 1321, 1325 and 1328 describe earlier evidence controllers and must not be integrated as the current design.
