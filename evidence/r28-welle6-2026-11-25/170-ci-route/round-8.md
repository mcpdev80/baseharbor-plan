# w137-0428-285-pr170-legb — #170 Leg-B supersession witness

**Lane:** w137-0428-285-pr170-legb (orchith)
**Task:** t-20261124-ci-operator-acceptance-nontty (#0428-285, closed)
**Mission:** queued AFTER #1812 scheduling. Leg-B supersession witness for demo PR #170.
**Date:** 2026-11-24

## PLAN

- Read mission, verify planning-remote, serialized window, exact develop tip, pin condition (#1830), demo PR #170 state, and the Leg-B dispatch authorization.
- Root-cause whether the authorized `pre-release.yml` `workflow_dispatch` with `ref=develop-tip`, `demo_ref` OMITTED, `only_gates=atomic,static,config-matrix` can actually execute the `Static · config-matrix` job for v0.4.28.
- Post a QUESTION to the Coordinator with the finding (no interactive dialog).

## Repo / remote attestation

- Planning repo remote (verified before first write): `https://github.com/mcpdev80/baseharbor-plan.git`
  - `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) / (push)`.

## Reality witnesses

- Exact develop tip (Core): `9d7e22902f368c78f489021432c8112eb54cb74e` (ls-remote `refs/heads/develop`).
- Pin condition: `8bfc76edd90bb54bbe12f31a2c200a1de67bd7b0` is an ancestor of `9d7e2290` (Core `>=8bfc76ed` satisfied). `git merge-base --is-ancestor` returned clean.
- Core PR #1830 (`docs(release): pin v0.4.28 to Demo PR 174`) state = **MERGED** at `8bfc76edd90bb54bbe12f31a2c200a1de67bd7b0` by `mcpdev80` (Marcel Pfingstgräf) 2026-11-24T21:05:45Z, base `develop`.
- Demo `docs/releases/v0.4.28.demo-ref` on develop tip `9d7e2290` = `b41127723e523134a1c14ee3c36cf133237162ce`.
- Demo PR #170 (`test(config-matrix): demo operator-allowlist root-name fix (0428-250)`) in `mcpdev80/baseharbor-demo`: state = **OPEN**, draft, head `0249c9f73c21f46ba532fddc94a764e772f69acf`, base `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`, lane `lane-0428-250-demo-operator-root`. Changed files: exactly one = `tests/config-matrix/run.sh` (+11/-12). (API `pulls/170/files`: `11/12 tests/config-matrix/run.sh`.)
- Serialized window: `gh run list --repo mcpdev80/baseharbor --workflow "Release · Pre-Release Validation" --status in_progress --status queued` => `[]` (no other validation run in progress).

## Root cause: the authorized Leg-B dispatch cannot run for v0.4.28

- The mission authorizes `only_gates=atomic,static,config-matrix`. The pre-release gate selector is `scripts/pre-release-check-plan.py` on `origin/develop`. It validates `selected ⊆ required`, where `required = [row.id for row in gates if tag in row.required_for]`.
- On `origin/develop` tip `9d7e2290`, the gates `required_for: v0.4.28` are **exactly two**: `atomic/static/mcp` and `atomic/static/ci-fast-check`. `atomic/static/config-matrix` is **not** in that set, so any `only_gates` containing `atomic/static/config-matrix` is rejected by the plan script with `selected checks must be unique exact required check IDs` (exit 2).
- Exact reproduction (`python3 scripts/pre-release-check-plan.py --tag v0.4.28 --only-gates "..."`, run from the `scripts/` dir with `release-requirements.json` beside it):
  - `--only-gates "atomic,static,config-matrix"` (mission's literal form) => `Pre-Release gate selection failed: selected checks must be unique exact required check IDs` (exit 2).
  - `--only-gates "atomic/static/config-matrix"` (exact check-id form) => same rejection (exit 2).
- `atomic/static/config-matrix` is `required_for: ['v0.4.22','v0.4.23','v0.4.24','v0.4.25','v0.4.26','v0.4.27']` — dropped after v0.4.27, never re-added to v0.4.28.
- Provenance (git on `origin/develop`):
  - `scripts/release-requirements.json` at v0.4.27 tag `6c40fab4` still lists `config-matrix` as `required_for ... 'v0.4.27'`.
  - Commit `8bf52f02` `ci: register v0.4.27 in the candidate gate catalog (release-requirements + pr-gate-map)` (#1812) is the catalog-registration change that moved the per-gate `required_for` lists; the v0.4.28 block (`for_release`-only gate = `atomic/static/ci-fast-check`) does not include `config-matrix`.
  - Subsequent commits (`fc3eecbf` #1793, `fdced23d` #1805) add `ci-fast-check` and PR-executed static gates but never add `config-matrix` back to v0.4.28.
- Consequence for the authorized dispatch:
  - With `only_gates` containing `config-matrix`, `source_prepare` (Pre-Release Validation) fails at `pre-release-check-plan.py` before any job is scheduled (exit 2) — a workflow-level failure, zero jobs.
  - With `only_gates` empty, `static_count` for v0.4.28 = `{mcp}` only; the `Static · config-matrix` job is never in the matrix (it is not `required_for` v0.4.28).
  - With `only_gates=atomic/static/mcp,atomic/static/ci-fast-check`, only those two gates run; `config-matrix` still never schedules.
- Therefore there is no authorized `only_gates` value that makes `Static · config-matrix` actually execute and pass on v0.4.28. The Leg-B supersession witness as written is not runnable against the current Core develop tip.

## #170 hunk status

- The only content of PR #170 is the `tests/config-matrix/run.sh` bootstrap-root change (round-7 documented the wrapper-rejection rationale; head `0249c9f7`, hunk NOT on pinned tip `b4112772`).
- The develop-tip `tests/config-matrix/run.sh` (pinned demo `b4112772`, no hunk) is the exact source the `config-matrix` gate would execute — but the gate does not run for v0.4.28.

## Disposition / proposal for close (no close action)

- #170 was a Demo-side fix gated on Core pin #1830 (#1830 merged, condition satisfied). The remaining blocker is a Core release-catalog decision, not Demo content: `atomic/static/config-matrix` is no longer a v0.4.28 required gate, so the Leg-B supersession dispatch cannot execute it.
- Proposed Owner decision (one of):
  - (A) Owner re-adds `atomic/static/config-matrix` to `required_for` v0.4.28 in `scripts/release-requirements.json` (owner-scope, shared planner file, coordinator/owner action) — then the Leg-B dispatch becomes runnable and I re-run it to green.
  - (B) Owner accepts that the Demo operator-allowlist root-name fix is no longer a v0.4.28 required gate and #170 is superseded by develop (documented, no run).
  - (C) Owner designates a different, existing v0.4.28 gate whose source IS the pinned demo tip to witness #170's behavior.
- Close boundary (per card handoff): #170 stays OPEN until an owner-visible confirmation line naming the supersession witness and disposition exists in the Kanban card. This note proposes that; no card edit, no PR edit, no dispatch made.

## END

- END_BLOCKED w137-0428-285-pr170-legb: Leg-B dispatch is not runnable for v0.4.28 because `atomic/static/config-matrix` was removed from the v0.4.28 required-gate catalog (only `atomic/static/mcp` + `atomic/static/ci-fast-check` are required_for v0.4.28). Root-caused in `pre-release-check-plan.py` validation + `release-requirements.json` provenance. QUESTION posted to Coordinator for Owner decision (re-add gate / accept superseded / alternate gate). No dispatch, no PR edit, no workflow change, no merge.
