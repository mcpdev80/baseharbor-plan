# PR #1577 Release/Reference R2 (0428-077: branch correction on card PR #1577)

## PLAN

1. r1 (round-1.md) corrected #1577 EN/DE release/reference prose on a new branch `mission-1577-077` / draft PR #1583.
2. PR-rule check (owner stoss): one PR per card is owner rule. `e51911a5` landed on the wrong head branch, not the card's PR branch `0428-092-perses-boundary`. Correction: push `e51911a5` to the card branch and close the stray PR.
3. Verify ancestry, push, watch the card PR run to terminal, write round-2.md, END.

## Provenance

Fresh clone at `/tmp/opencode/mission-1575-r4`. Exact product witness from `git ls-remote origin`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

Card branch head (ls-remote witness):

```text
ls-remote origin refs/heads/0428-092-perses-boundary  -> e51911a5 (current)
ls-remote origin refs/pull/1577/head                   -> e51911a5 (current)
```

Ancestry witness:

```text
git merge-base --is-ancestor 29dba54dddb02f48568c571e9ce37f671d21e6aa e51911a5   -> yes
git rev-list --count 29dba54dd..e51911a5                                          -> 1 (fast-forward)
git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c e51911a5   -> yes
```

`e51911a5` is exactly one commit ahead of the pre-correction #1577 head `29dba54dd`; the correction is a fast-forward, no rebase.

## What was corrected

`e51911a5` (the r1 doc-only correction: EN/DE release/reference aligned to `not_configured` + `configured_unverified`, no `unsupported` left in any Perses context) was re-pointed from the stray draft head `mission-1577-077` / PR #1583 onto the card's canonical PR branch `0428-092-perses-boundary` / PR #1577, restoring the one-PR-per-card rule. The stray draft PR #1583 was closed.

## Hosted run

Exact headed pull_request run on the card branch:

```
0428-077  run 43671511011  success  e51911a5  pull_request  CI · Source & Quality  (PR #1577)
```

No workflow dispatch was needed — the branch push ignited the run. No rerun or dispatch was initiated. No failing or cancelled check observed. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed, per mission scope.

## repo-rule compliance

Evidence is in the actual planning repository. Product remote state was measured from a fresh clone and `git ls-remote`. No product code, workflows, CI, containers, or VMs were changed beyond the doc-only card branch. PR #1577 was NOT merged (frost honoured); the stray draft PR #1583 was closed to restore the one-PR-per-card rule. Both candidate heads sit exactly on `e51911a5`. No markdown checkbox lines in evidence.

## END DONE (0428-077)
