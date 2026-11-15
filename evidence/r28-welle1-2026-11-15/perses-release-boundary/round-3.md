# PR #1577 Release/Reference R3 (0428-077: how-to Perses prose + verified-health-probe alignment)

## PLAN

1. Read r3 akte (act-1577-review-r3.md): REJECT — two pure-doc findings on the already-corrected r2 head `e51911a5`.
2. Fix (1): the EN/DE observability HOW-TO still says `unsupported` in a Perses context (`docs/how-to/observability.md:32`, `docs/de/how-to/observability.md:28`) — align to the three states.
3. Fix (2): ensure all four release/reference passages positively tie `verified` to an actual Perses health-path probe.
4. Card branch `0428-092-perses-boundary`, PR #1577 draft, pull_request run on exact head terminal, round-3.md, END. No merge (frost).

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd`. Exact product `git ls-remote` witness:

```text
2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd	refs/pull/1577/head
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
```

The r2 head `e51911a5` is a direct ancestor: `git rev-list --count e51911a5..2c4ccc31` is `1` (fast-forward), and `0e9ccb58` is an ancestor of `2c4ccc31`. Fresh review clone `/tmp/opencode/w077-pr1577-review-r3-wt`; the pre-existing review worktree was not used for this edit.

## What r3 required and how it is satisfied

### Finding 3 — HOW-TO still says `unsupported`

`docs/how-to/observability.md:32` said an unprovisioned selected Perses surface is `unsupported`; the German `docs/de/how-to/observability.md:28` used the same `unsupported` value. Both are now `configured_unverified`, with the unselected/invalid-pin case reported as `not_configured` (fail-closed) and reachability stated unverified absent a real Perses health probe. `verified` is now positively reserved for an actual health-path observation in both languages.

`git diff --check` clean. The repository grep for `perses ... (unsupported|not supported)` across `docs --glob '*.md'` returns **no matches** — the stale Perses assertions are gone.

### Finding 2 — `verified` tied to an actual health probe

The four release/reference passages already positively state `verified` is reserved for a real Perses health-path probe; this r3 edit extends the same wording to the two HOW-TO files so every Perses passage in scope states it identically.

## Hosted run

Exact headed pull_request run on the corrected card head:

```
0428-077  run 43677090058  success  2c4ccc31  pull_request  CI · Source & Quality  (PR #1577)
```

No workflow dispatch was needed — the branch push ignited the run. No rerun or dispatch was initiated. No failing or cancelled check observed. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed, per mission scope.

## repo-rule compliance

Evidence is in the actual planning repository. Product remote state was measured from a fresh clone and `git ls-remote`. No product code, workflows, CI, containers, or VMs were changed beyond the two doc files on the card branch. PR #1577 was NOT merged (frost honoured). Both candidate heads sit exactly on `2c4ccc31`. No markdown checkbox lines in evidence.

## END DONE (0428-077)
