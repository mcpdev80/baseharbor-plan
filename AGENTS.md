# AGENTS.md

## Current controlled Codeman resumption — 2026-10-19

Marcel explicitly authorized making Codeman operational again after CI stabilization. The [controlled resumption decision](decisions/2026-10-19-ci-stabilization-controlled-resumption.md) supersedes the earlier infrastructure hold for the existing Flash/o1 core-921 binding assignment. Preserve and checkpoint o1's unpublished two-file work before normal integration; do not duplicate its implementation or take over its claim. The coordinator may continue that existing owner and assign subsequent genuinely ready work through the normal ownership protocol. Separate independent review and final Maintainer acceptance remain required.

Qwen's exact-SHA #995 native recovery/automatic-cleanup proof remains an independent external blocker, not a global Codeman pause. No release, native success, Required Check bypass or merge without fulfilled prerequisites is authorized. The bounded Codex #995 correction has been published and independently source-reviewed; do not repeat it. Historical hold and exception records remain in [the earlier decision](decisions/2026-10-19-ci-stabilization-codeman-hold.md).

## Earlier handover pause ended — historical decision

The 2026-10-18 handover pause ([decision](decisions/2026-10-18-horde-codex-handover-pause.md)) was explicitly lifted by Marcel on 2026-10-19 ([resumption decision](decisions/2026-10-19-pause-lifted-codeman-delegation.md)). Development, merges and native tests are resumed under the standing rules of the affected repositories. Existing claims, PRs, reviews and handoffs from the paused period remain published and protected; they are not available for silent takeover, and an existing PR is continued only with an explicit ownership release. Operational delegation runs through the Codeman/Ornith/Codex coordinator model of the ecosystem-root `AGENTS.md`; releases still require separate authorization.

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

- This is a live shared planning repository: publish planning updates directly to `main`, including claims, progress, blockers, handoffs and shared planning changes within the assigned scope. Do not create a planning branch or PR unless the Maintainer explicitly requests one. Product-code branching/review rules remain unchanged.
- Pull current `main` before editing. Before publishing, integrate concurrent changes, re-read affected notes, render and validate. Use a normal push or an expected-SHA update; on rejection repeat integration. Never overwrite another session or force-push.
- If a planning branch already exists, bring its still-relevant updates onto current `main` promptly after validation, preserve newer main content, then delete the obsolete remote branch. Publishing a handoff does not accept its product task. Do not leave completed planning branches behind.

- One assigned task per session. Claim before editing anything ([ownership protocol](WORKFLOW.md#ownership-protocol)): `scripts/plan.py claim`, commit, push; on a rejected push, pull and re-check the claim. A local `owner` field is not a lock.
- Edit only your task's note in this repository; coordinate shared notes (releases, epics, roadmap) separately.
- Respect file ownership and dependencies stated in the task; a draft or partial PR is not a completed prerequisite.
- Hand off and stop: update the task's Handoff section, set `#status/review` with the PR, push. Do not start another task on your own; report blockers.
- Never mark a task accepted or a release qualified; only the Maintainer does, with evidence. Ticking a checkbox is not acceptance.
- No force-push; preserve others' commits. All maintained text, metadata and headings in English.
- After editing metadata run `python3 scripts/plan.py render` and `python3 scripts/plan.py check`; both must pass before you push. This includes every claim, dependency acceptance, blocker update and handoff: publish the refreshed derived Ready cards and views with the task update, preserving concurrent changes.
- At Maintainer acceptance/assignment reviews, inspect the current release's ready queue and remaining prerequisite gaps. Keep independently executable task slices current so available work is visible in CardBoard Ready; do not invent readiness, weaken prerequisites or let implementation sessions start unassigned work. See [Ready queue maintenance](WORKFLOW.md) and the executable task rules.

Details: [WORKFLOW.md](WORKFLOW.md). Overview: [HOME.md](HOME.md).

## Recurring release cards

Every future concrete release needs the six [release lifecycle cards](RELEASE_WORKFLOW.md). The already-running v0.4.26 has only its four completion stages; do not recreate startup cards for it. On scheduling/changing scope run `python3 scripts/release_cycles.py sync`, then render/check and planning tests. Complete cleanup and applicable Renovate intake before new feature development. Readiness, complete pre-release authorization, promotion/tagging authorization and post-release verification are distinct. Preserve verifier-valid green evidence from partially failed runs; rerun only failed/affected coverage. Planning card creation authorizes none of those operations.
