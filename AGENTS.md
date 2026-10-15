# AGENTS.md

Entry point for local and cloud coding agents. This repository holds BaseHarbor **planning** only; product code, engineering rules and specifications live in the product repositories.

> Planning authority: task and release notes in this repository are authoritative once this activation commit reaches `main`. GitHub source issues retain discussion/history only. Read [migration/cutover-checklist.md](migration/cutover-checklist.md) for the activation record and outstanding operational cleanup.

## Load only what your task needs

Do not read the whole vault. For an assigned task:

1. `git pull`, then `python3 scripts/plan.py show <id>` — file path, derived state, dependency status.
2. Read that task note, its release note in `releases/`, and its epic in `epics/` if `parent` points to one. Follow links only as needed.
3. For product work, read the product repository's own entry points (for BaseHarbor: [AGENTS.md](https://github.com/mcpdev80/baseharbor/blob/develop/AGENTS.md) and [DEVELOPMENT_GUIDELINES](https://github.com/mcpdev80/baseharbor/blob/develop/docs/DEVELOPMENT_GUIDELINES.md)). This vault links to them; it does not duplicate them.

No task assigned? `python3 scripts/plan.py list --ready` shows candidates, but **ready is not assigned**: the Maintainer assigns work.

## CI execution discipline

For product work, follow the binding [BaseHarbor CI execution discipline](https://github.com/mcpdev80/baseharbor/blob/develop/AGENTS.md#ci-execution-discipline): batch and precheck coherent verification candidates, inspect results before another push, justify reruns, and select impact-based checks. Repeated avoidable CI cancellations and automatic full-release PR matrices violate this rule. Planning-only edits continue to use this repository's cheap validator.

## Rules

- One assigned task per session. Claim before editing anything ([ownership protocol](WORKFLOW.md#ownership-protocol)): `scripts/plan.py claim`, commit, push; on a rejected push, pull and re-check the claim. A local `owner` field is not a lock.
- Edit only your task's note in this repository; coordinate shared notes (releases, epics, roadmap) separately.
- Respect file ownership and dependencies stated in the task; a draft or partial PR is not a completed prerequisite.
- Hand off and stop: update the task's Handoff section, set `#status/review` with the PR, push. Do not start another task on your own; report blockers.
- Never mark a task accepted or a release qualified; only the Maintainer does, with evidence. Ticking a checkbox is not acceptance.
- No force-push; preserve others' commits. All maintained text, metadata and headings in English.
- After editing metadata run `python3 scripts/plan.py render` and `python3 scripts/plan.py check`; both must pass before you push.

Details: [WORKFLOW.md](WORKFLOW.md). Overview: [HOME.md](HOME.md).
