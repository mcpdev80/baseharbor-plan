---
id: core-895
areas: [workflow]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: mcpdev80
depends_on: [core-893]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#933"]
sources: ["mcpdev80/baseharbor#895"]
source_updated: "2026-10-15T19:46:16Z"
labels: [area/dx]
blocker: "Both develop rulesets are active and independently read back; real positive/negative merge-enforcement pilots (including approval dismissal and bypass-free red-check blocking) remain unqualified."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/933", "https://github.com/mcpdev80/baseharbor/commit/e8b021fe63c61abc0990a560e5f2915bb70c2c13"]
---

- [ ] core-895 · Reviews: require maintainer approval for develop #task #release/v0-4-26 #status/blocked #view/blocked #area/workflow #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** not set  
    **PR:** [baseharbor#933](https://github.com/mcpdev80/baseharbor/pull/933)  
    **Blocker:** Both develop rulesets are active and independently read back; real positive/negative merge-enforcement pilots (including approval dismissal and bypass-free red-check blocking) remain unqualified.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/933), [proof 2](https://github.com/mcpdev80/baseharbor/commit/e8b021fe63c61abc0990a560e5f2915bb70c2c13)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md)  
**Required by:** [core-390](core-390-architecture-service-contracts-provider-catalog.md), [core-750](core-750-inspect-source-neutral-findings.md), [core-751](core-751-inspect-no-false-positives-comments-text.md), [core-752](core-752-inspect-reconcile-default-instances.md), [core-754](core-754-mcp-classify-expected-preconditions.md), [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Owner:** mcpdev80  
**Priority:** not set  
**PRs:** [baseharbor#933](https://github.com/mcpdev80/baseharbor/pull/933)  
**Source:** [baseharbor#895](https://github.com/mcpdev80/baseharbor/issues/895)
<!-- /generated:links -->

## Goal

PRs from other contributors need Maintainer approval; the Maintainer's own PRs remain possible under the documented solo exception.

## Scope

- In scope: rulesets/CODEOWNERS for develop as far as GitHub actually supports them; short central documentation of the rule and its limits.
- Out of scope: claiming a bypass restricted to own PRs without proof.

## Acceptance

- Read current rules/permissions; configure required PRs, @mcpdev80 code-owner review and dismissal of stale approvals as far as actually supported.
- Own PRs may merge without a second review; required green checks stay mandatory; no direct push.
- Bypass technically narrow and separate from CI protection where possible.
- The rule is documented briefly and centrally, naming GitHub's limits and the remaining Maintainer compromise.

## Required checks

- Foreign PR without/with approval, new commit, own PR and a red required check; qualify without a production merge. **Required check names must exist before activation.**

## Dependencies and file ownership

- Satisfied: #890 (closed). Requires a qualified #893 status check (core-893). Order fixed by the [2026-10-15 dependency correction](../epics/core-888-development-and-ci.md#binding-dependency-correction--2026-10-15).

## Handoff

- 2026-10-16 enforcement pilots (NO MERGES): disposable positive [PR #951](https://github.com/mcpdev80/baseharbor/pull/951), head `ffb5b44773788571347676b88c80e98d6f5053a6`, completed [Actions 38869158632](https://github.com/mcpdev80/baseharbor/actions/runs/38869158632) with genuine `PR Selected Checks=SUCCESS` (job `116869300935`) and required documentation validations; disposable negative [PR #952](https://github.com/mcpdev80/baseharbor/pull/952), head `860e83f1aef00e5b0bc4efd19bf980ca33165346`, completed [Actions 38869163429](https://github.com/mcpdev80/baseharbor/actions/runs/38869163429) with genuine `PR Selected Checks=FAILURE` (job `116869036764`) for deliberately unresolved root-file impact. Both were CLOSED without merge and remain inspectable. No runtime gate or release matrix was run.
- Limits: `mergeable=true` in PR metadata means conflict-free, NOT actual ruleset authorization; neither actual Maintainer merge admission after green checks nor bypass-free merge denial was exercised because merging these disposable PRs was expressly prohibited and the connector offers no merge dry-run. No distinct authenticated real contributor identity was available; foreign approval, CODEOWNERS enforcement, last-push approval and stale-approval dismissal cannot be honestly claimed proven. The two live ruleset configurations remain documented above from independent read-back; they were not changed or reactivated. Therefore **core-895 remains blocked, not accepted**, pending admissible direct protection enforcement evidence. Planning render/check still needs a verified execution before treating this note as validated.



- 2026-10-16 live activation, explicitly authorized by Marcel and applied through his authenticated gh CLI: review ruleset `23754541` and separate CI ruleset `25223521` are ACTIVE for `refs/heads/develop`. Independent GitHub API read-back confirmed one required approval, code-owner review, stale-review dismissal, last-push approval and preservation of `require_extra_approval_for_unattributed_changes: true`. Review-only User `22537373` bypass is `pull_request` (`current_user_can_bypass: pull_requests_only`). CI requires `PR Selected Checks` from integration `15368` with strict up-to-date checks, empty bypass actors and `current_user_can_bypass: never`. Sources: [review ruleset](https://github.com/mcpdev80/baseharbor/rules/23754541), [CI ruleset](https://github.com/mcpdev80/baseharbor/rules/25223521). Activation and write compatibility are now proven; real allow/deny enforcement pilots are NOT yet proven. The task remains open until those acceptance checks pass. This supersedes the former authorization blocker. No product merge or release was performed during activation.

- 2026-10-16 Maintainer-authorized closeout: Proposal PR #933 accepted and squash-merged into develop as `e8b021fe63c61abc0990a560e5f2915bb70c2c13`. Independent integration-tree review passed the complete documentation audit (156 EN/DE paired pages), proposal JSON invariants, separate bypass-free CI payload and CODEOWNERS checks. This is proposal acceptance only: no ruleset was written and live enforcement is not qualified. core-893 is now accepted. Keep this task OPEN until the separately authorized activation and all live enforcement checks succeed.

- Live migration review: PR #933 head `fefcdeeae0bf928b72018b9eb38b8758cdec0657`; draft/preparatory work remains unaccepted. The current PR head supersedes older SHA assertions in its body. Preserve the existing owner, branch and PR.

- Assigned to mcpdev80. Draft PR #933 ("propose maintainer review protection payloads"), head `2b6e0fcf14` at snapshot time — a proposal while core-893 is not qualified; activation must wait.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
