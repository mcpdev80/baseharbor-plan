# w182-codex-1843-review — PR #1843

## PLAN

1. Refresh PR #1843 state, exact head/base, changed-file scope, and author identity against the task owner.
2. Review the docs-only corrections against the itemized H-V44 findings and verify destination paths.
3. Verify Hosted Actions run heads and terminal outcomes for the exact candidate.
4. Publish the SHA-specific CHANGES verdict and actionable remedy to plan evidence and PR comments.

## Review evidence

Planning repository remote witness before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

PR: [#1843](https://github.com/mcpdev80/baseharbor/pull/1843), state OPEN, non-draft, mergeState CLEAN. Exact PR API head `7e1fc3a57dcd615f9d286b67393cae9a02763c81`; base `develop` at `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`.

Identity check: plan task note `tasks/t-20261125-hunt44-doclink-repair-sweep.md` frontmatter owner is `w181-0428-doclink-sweep`. GitHub commit API reports the exact head commit author `.commit.author.name` as `w181-0428-doclink-sweep`. Identity matches. The commission/evidence label uses task identifier `t-20261127-hunt44-doclink-repair-sweep`, while the actual task note frontmatter ID is `t-20261125-hunt44-doclink-repair-sweep`.

Scope check: GitHub PR API lists 15 changed files, all under `docs/**`; no `.github/**`, code, or scripts. The changes replace six EN/DE plain-text management-access references with relative Markdown links; repair historical audit path annotations/current-state pointers; clarify the retired management-access-profiles path; and distinguish conformance identifiers from repository paths. Destination files for the canonical EN/DE spec, audit, reference, explanation, runtime-security, backup/restore, provider-conformance, and profile/harness targets exist in the exact head tree. The existing CI link-check remains an owner-scope finding as directed; no workflow/code change is requested here.

## Exact-head CI verification

Direct GitHub Actions API verification:

- Run `45609710215`: `completed / success`, exact head `7e1fc3a57dcd615f9d286b67393cae9a02763c81`. Executed `PR Selected Checks` (job `139190326815`), `documentation-audit` (job `139189900788`), `mkdocs-en-strict` (job `139189900927`), `mkdocs-de-strict` (job `139189900853`), and `pages-candidate-build` (job `139189900887`), all successful.
- Run `45609692069`: same exact head but `cancelled`; not qualifying evidence.
- Run `45608051338`: `completed / success`, but GitHub records head `9f7da6d420c1a9f35a83b1d1771956e4781ab667`, not the reviewed head. It does not count as exact-head evidence. Thus the current exact head has one successful full run ID, not two.

## Verdict: CHANGES

The independent scope review is clean, but acceptance is blocked by two contract/evidence gaps:

1. Mission/card require two full green Hosted CI runs on the exact candidate. Only `45609710215` is a successful run for `7e1fc3a5`; `45609692069` is cancelled. `45608051338` is green on a different head.
2. The task contract and handoff claim 40 repaired rows, but the itemized H-V44/source and repair inventories enumerate 38: F1 6 + F2 28 (2 current-pointer rows plus 26 annotations; the evidence heading says 25/23) + F3 2 + F4 2. The documented row inventory and claimed total need reconciliation before acceptance.

Actionable remedy: run a second full PR validation on the unchanged exact head through the supported Hosted CI route and preserve its distinct run ID and terminal `PR Selected Checks` success; do not count the cancelled run or the earlier `9f7da6d4` run. Reconcile the 40-row contract against the source inventory by identifying and repairing the two omitted rows within the docs-only scope, or have the task owner/coordinator correct the authoritative card and evidence count if the itemized 38-row inventory is complete. Hand the resulting exact candidate back for re-review. Stop condition: no merge until both conditions are evidenced.

PR comment posted: https://github.com/mcpdev80/baseharbor/pull/1843#issuecomment-7162105566. Final live API read still showed the PR OPEN on exact head `7e1fc3a57dcd615f9d286b67393cae9a02763c81`, mergeable state `clean`. No merge, PR-head change, CI rerun, workflow edit, or code edit was performed by this reviewer.
evidence/board-2026-11-27/w182-codex-1843-review.md
