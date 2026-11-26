# Lineage-audit akte — lane w268-0428-284-1842impl

**Card:** t-20261125-0428-284-1812 · **Product PR:** #1856
**Product branch:** `w268-0428-284-demo-pin-1812-clean` (base develop) · **Head:** `67457cdb3`
**This akte:** plan branch `w268-0428-284-1842impl-evidence` (commit `bf47bf3c2`), opened via `gh pr create`. **Not** pushed to plan main, **not** merged. Lane identity `w268-0428-284-1842impl`.

## Ruling (owner 2026-11-26 ~04:19Z, after Codex w267 REVIEW verdict HOLD)

`67457cdb3` is **superseded / frozen**. No more triggers, no merge, no close of
#1856; #1856 becomes the **lineage audit**. Run 45754203548 (started 04:16:53Z
on `67457cdb3`) is preserved as a CI event record and clears nothing. Do NOT
touch the product branch again — no commit, no comment-triggered event, no
close. Successor work is commissioned to a fresh lane precisely because the
checkout config that produced the five w198-attributed commits must not carry
over.

## (a) Commit-by-commit identity census of #1856

Five carried commits authored **and** committed as `w198-0428-284-demo-parser`
(stale worktree git config inherited from the #1842 lineage); tip `67457cdb3`
correctly this lane's own.

| commit | an | cn | payload |
|---|---|---|---|
| cc453c79b | w198-0428-284-demo-parser | w198-0428-284-demo-parser | clean reissue as PR #1856 (closed contaminated #1842); selector fix in pr-gate-plan.py (any active-release demo-ref → validator; v0.4.24-26 no-pin) |
| f5b86f477 | w198-0428-284-demo-parser | w198-0428-284-demo-parser | pr-check-runner.py: anonymous git transport for the pinned Demo SHA, fail-closed, transport stderr surfaced; test_pr_check_runner.py git-transport mock test |
| de26af2ec | w198-0428-284-demo-parser | w198-0428-284-demo-parser | ci.yml: run Demo Pin validator job when plan carries the validator |
| 5ae41085b | w198-0428-284-demo-parser | w198-0428-284-demo-parser | ci.yml: pr-diff.json source route for the Demo Pin REQUIRED trigger + test_pr_gate_coverage.py correction |
| **67457cdb3** | **w268-0428-284-1842impl** | **w268-0428-284-1842impl** | ci.yml: populate Demo Pin `demo_sha` from trusted var + anonymous git fallback (identity-fix proof commit) |

Cause: worktree `git config user.name` = `w211-0428-307-fallback`; the five
carried commits inherited `w198-0428-284-demo-parser` from the #1842 lineage.
Foreign-lane full identity is not admissible admission (w205 covers only
same-lane shortened forms). Green CI does not admit authorship. From
`67457cdb3` onward the lane uses its own full name per-command
(`git -c user.name=... -c user.email=...`); the inherited config was never
edited. No amend / rebase / force on the carried commits.

## (b) What the payload proved

- **Required-route fix works.** Run 45752147188 (run_attempt 1, terminal
  SUCCESS ~04:03:02Z): `PR · Demo Pin` (job 139682275264) EXECUTED and PASSED.
  Live log: `demo_sha="98e4d549c73fb099c780b5ae455da35a0ef68c71"` → 40-hex pass →
  clone `--filter=blob:none --no-checkout` → `fetch --depth=1 origin` →
  `checkout --detach` → rev-parse equality pass → `baseharbor-core.ref` present →
  HEAD at `98e4d54 fix(backup): preserve Loki host on recovery query (#168)` →
  artifact uploaded. Fail-closed checks intact.
- **Validator PASS with the correct pin.** The `demo-source-pin-validation`
  required-route path is reachable from this head's verify job; the validator
  `matched_tests=[5ca92a7cd2f746934890cfd7096a48068bdf218e]` line is emitted by
  `pr-check-runner.py execute --check demo-source-pin-validation` in the
  **validate** matrix job (ci.yml ~1372), driven by the base planner's matrix
  row — reachable once the selector fix lands in develop (base still develop
  here, so `validate` was skipped on this head).
- **Six-file write-set.** `.github/workflows/ci.yml`
  (source route + verify/demo_source demo_sha), `scripts/pr-check-runner.py`
  (anonymous git transport), `scripts/test_pr_check_runner.py` (git-transport
  mock), `scripts/test_pr_gate_coverage.py` (release-mismatch contract), plus
  `scripts/pr-gate-plan.py` (selector) and `docs/releases/v0.4.28.demo-ref`
  (pin relocation).
- **Pin relocation.** `docs/releases/v0.4.28.demo-ref`: `b41127723e523134a1c14ee3c36cf133237162ce`
  → `5ca92a7cd2f746934890cfd7096a48068bdf218e`; tag `v0.4.28` (was v0.4.27).

## (c) What Codex w267 held on (REVIEW / HOLD)

- **Unsafe `os.makedirs(exist_ok=True)` creation** inside the checkout
  (`scripts/pr-check-runner.py:495` running `git init -q _demo_repo` with
  cwd=<repository> and `:503` building `Path(repository)/'_demo_repo'`), i.e.
  the scratch demo repo is created INSIDE the checkout where the cleanup
  `rm -rf` (`scripts/ci-runtime-reset.sh:244`) can destroy it.
- **Foreign lineage** — the five w198-attributed commits on an otherwise-correct
  payload.

## (d) Run register

| run | head | role |
|---|---|---|
| 45752147188 | 67457cdb3 | SUCCESS — 40 jobs / 21 executed-success / 19 skipped / 0 failed; `PR · Demo Pin` (139682275264) EXECUTED + PASSED |
| 45754203548 | 67457cdb3 | CI event record only (started 04:16:53Z), clears nothing |
| 45750304453 | 5ae41085b | Audit only — `PR · Demo Pin` (139676294648) FAILED: `demo_sha=""` under `set -euo pipefail`; `PR Selected Checks` cascade |
| de26af2ec / cc453c79b / 5ae41085b runs | — | Audit only |

## Plan PR

Open via `gh pr create` from branch `w268-0428-284-1842impl-evidence`.

## Repo-rule compliance

- Git transport: anonymous `git ls-remote`/`git fetch` over public https; no
  cross-repo token. Fail-closed on non-40-hex, missing commit, or SHA mismatch.
- No check deleted or softened; no amend/rebase/force on carried commits.
- CI identity from `67457cdb3`: lane `w268-0428-284-1842impl` (per-command).
- Zero local test execution (CI is the test surface).
- Publish: own plan branch + `gh pr create`; never direct main, never merge.
