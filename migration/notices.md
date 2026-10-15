# Proposed notices for migrated issues

Not posted. To be posted only after the Maintainer approves the cutover ([checklist](cutover-checklist.md)). One comment per migrated issue; the destination link comes from [manifest.json](manifest.json) (`destinations[0].path`).

## Task, epic, release and roadmap issues

> Planning for this issue has moved to **baseharbor-plan**: <https://github.com/mcpdev80/baseharbor-plan/blob/main/DESTINATION>.
> Scope, acceptance, dependencies, ownership and status are maintained there from now on; please do not update this issue body. Discussion and history here stay available. Code, PRs, reviews and evidence stay in this repository. Closing this issue records migration only; it does not mean the work was implemented, accepted or cancelled.

Then, per the approved option in the cutover checklist, either close the issue (reason "not planned", label `planning/moved`) or leave it open with that label.

## baseharbor#893 (split)

> Planning for this issue has moved to baseharbor-plan as two phases: the agreed interface (`tasks/core-893-interface-…`) and the final integration/acceptance (`tasks/core-893-ci-…`). …

## Triage items (console#1, console#2, node-connector#3, demo#24)

Link the migrated destination even when release triage remains open. An unresolved product release assignment is not a migration blocker.

## External tooling (baseharbor#889)

No notice; Renovate owns the issue. Listed in [external-tooling.md](external-tooling.md).

## Generic intake notice (pinned or in issue templates)

> BaseHarbor planning lives in [baseharbor-plan](https://github.com/mcpdev80/baseharbor-plan). Bug reports and feature requests are welcome here; the Maintainer triages them into planning tasks and links the task in a comment.
