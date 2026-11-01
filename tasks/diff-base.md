---
id: diff-base
areas: [ci]
type: fix
release: backlog
version: ""
parent: ""
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [1251]
sources: ["mcpdev80/baseharbor#1240"]
source_updated: "2026-11-01T13:00:00Z"
labels: [kind/bug, area/ci, status/claimed]
blocker: ""
resolution: ""
evidence: ["baseharbor-plan/evidence/board-2026-11-01/diff-base/evidence.md"]
---

- [ ] diff-base · PR diff-base resolver: stale event-base + linear-rebase integration checks fixed, fail-closed preserved #task #fix #status/claimed #view/progress #area/ci
    <!-- generated:card -->
    **Owner:** unassigned
    <!-- /generated:card -->

<!-- generated:links -->
**State:** progress
**Release:** [backlog](../releases/backlog.md)
**PRs:** [baseharbor#1251](https://github.com/mcpdev80/baseharbor/pull/1251)
**Source:** [baseharbor#1240](https://github.com/mcpdev80/baseharbor/issues/1240)
<!-- /generated:links -->

## Problem

`PR Selected Checks` blocked with `integration_sha_mismatch` on every PR whose develop had moved forward (e.g. #1240). Two structural defects in `scripts/pr-diff-base.py` + the ci.yml Plan-job:

- **(a) Stale event base:** the Plan-job used `github.event.pull_request.base.sha` as `target_base`. GitHub rebuilds the merge-ref (`github.sha`) against the *current* develop. #1240 merge-ref `a84b71e2` parents = `[437358e4 (old develop), b8446716 (head)]`; event base.sha `cb6b738` is older, so the parent comparison always fails once develop moves on.
- **(b) Linear rebased head:** after a rebase, head is itself a descendant of develop; GitHub sets `github.sha == head` (no merge commit) → single parent → `integration_sha_mismatch` even when base ancestry is clean.

## Fix

Authoritative base is the target branch tip GitHub actually built the merge-ref against — not the stale event base.sha field. The resolver now self-determines the base from the merge-ref parents (no new CLI flag; `--base-tip` optional, default `None`):

- Merge-ref: base parent B is lineage-linked to the event base.sha (ancestor, equal, or a *descendant* = the stale-event case); only a divergent B fails closed.
- Linear: `github.sha == head`, single parent, ancestry check against the event base.sha.
- `integration_tree_mismatch` still enforced → fail-closed unchanged.
- **ci.yml reverted to develop exactly** (`git checkout origin/develop -- .github/workflows/ci.yml`): the runner executes the trusted *base* checkout (develop), so a ci.yml fix only takes effect *after* merge — a bootstrap paradox. The base-tip self-determination stays solely in `scripts/pr-diff-base.py`; ci.yml stays untouched. A later separate PR could re-add it if host rules ever allow PR-ci changes.

## Verification

- Local: `test_pr_diff_base.py` 17/17 OK (13 existing + 4 new: linear rebased resolves, develop-forward merge-ref resolves, third-parent rejects, wrong-head rejects); `test_pr_gate_plan.py` 5/5.
- Hosted CI, run `41311582975` (own run, Eigenes-Run-Pflicht): `PR · Trusted Plan` **pass** (7s), `PR Selected Checks` **success**, `ci-policy` pass, `ci-executor-verifier-tests` pass, `Workflow policy` pass. Zero failures. candidate SHA `40b2028f` / final `d56e9ddd`.
