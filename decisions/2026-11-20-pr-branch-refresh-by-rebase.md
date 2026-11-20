---
id: 2026-11-20-pr-branch-refresh-by-rebase
status: accepted
sources: []
---

# Decision: refresh a PR branch by `rebase` onto develop

## Context

Throughout the v0.4.28 merge window the coordinator dispatched branch refreshes as a
two-parent merge commit (`git merge --no-ff origin/develop`) and called that move
"hopf" — a word invented for the purpose. The owner rejected both on 2026-11-20: the
method must be `rebase`, and the vocabulary must be ordinary German plus the
established English terms, not a private jargon.

The merge-commit form was never required by the ruleset. Measured on 2026-11-20: PRs
#1684, #1690 and #1650 all carry `base=develop`, and each `base_sha` is an ancestor of
the then-current develop tip, so no stacked chain forces a merge commit. Active rulesets
(`25223521` develop required checks, `23754542` main released source; `23754541` develop
integration disabled) protect `develop` and `main` only — lane branches are unprotected.

## Decision

1. A PR branch that has fallen behind develop is refreshed with `git rebase origin/develop`.
   The new head is linear, develop's tip becomes an ancestor of it, and required checks run
   on exactly that head — which is what acceptance needs.
2. Publishing the rebased branch uses `git push --force-with-lease origin <lane-branch>`.
   Force-pushing a lane branch is permitted. Force-pushing `develop` or `main`, disabling or
   bypassing a ruleset, and pushing without `--force-with-lease` remain prohibited.
3. A rebase must not change content. Proof in the lane's evidence: `git diff <old-head> <new-head>`
   shows only develop-side changes; no line of the PR's own files differs. If both sides changed
   the same place, the lane stops with `file:line` instead of choosing.
4. After the rebase, exactly one `pull_request` run at the new head, observed to a terminal
   state by the lane itself (§4.6). Merge follows in the same turn, because develop moves every
   few minutes during the window.
5. Exception, unchanged: a stacked lane whose contract declares a base card whose content is not
   yet merged rebases onto that base lane's branch (AGENTS.md §3.3.8, fan-in on the contract lane),
   never onto a parallel successor.
6. The word "hopf" is retired. Documents and evidence already written keep it as history; new
   dispatch texts, cards and reports say `rebase` (or "branch auf develop aktualisieren").

## Conflict recorded

`coordinator/AGENTS.md` §5.2 states "kein Force-Push oder Schutzregel-Bypass" without restricting
the sentence to protected branches. Read literally it would forbid the `--force-with-lease` push
that step 2 requires. This decision resolves the sentence as intended by the owner: it prohibits
force-push on `develop`/`main` (where protection exists) and any protection bypass. A one-word
clarification in §5.2 ("kein Force-Push auf geschützte Branches") is the owner's call and is
requested here rather than edited silently.
