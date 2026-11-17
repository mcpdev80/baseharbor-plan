# mission-1577-headfix — STOP / REPORT: FENSTERWERK premise is false; destructive revert refused

**Lane:** mission-1577-headfix
**Date:** 2026-11-17
**Status:** END_BLOCKED — refused, awaiting owner directive
**Reviewer model:** worker-ornith1.5

## What the mission asks

The mission file (`/var/tmp/missions/mission-1577-headfix.md`) is a FENSTERWERK
(window-cleaning) task for card `t-20261114-r28-perses-release-boundary` /
PR #1577, branch `0428-092-perses-boundary` (remote head `70b7bfc8e`), base
`develop@8db0d9bdf`. It states:

- The APPROVIERTE (approved) candidate is `ab9086f5`.
- The current head `70b7bfc8e` is OLDER than `ab9086f5`; corrections after it were withdrawn.
- Task: make head content == `ab9086f5` by running `git checkout ab9086f5 -- .` + commit
  (explicitly: NO reset/force), then `git merge origin/develop`, build/vet/gofmt + boundary
  tests, push, run exact-head CI to terminal, PR #1577 ready.
- Boundaries: NO .github/**, NO force/reset/rebase, (yet step 3 explicitly mandates a merge — internal contradiction).

## Reality sync (measured, not asserted)

- `git ls-remote origin`:
  - `refs/heads/0428-092-perses-boundary` = `70b7bfc8e99c79cb20acc6974c67dcf2c037d446`
  - `refs/heads/develop` = `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54`
  - `refs/heads/main` = `c000c5db2560c471fe84842136e03d6e54d96779`
- `ab9086f5` and `70b7bfc8e` both resolve as commits in the object store.

## Ancestry / content facts (the decisive evidence)

- `git log -1 ab9086f5` = 2026-11-15 11:32, `docs(0428-077): r6 Perses state mention-only with spec pointer (EN+DE)`.
- `git log -1 70b7bfc8e` = 2026-11-16 04:49, `docs(perses): reduce release-boundary mirror prose to state-name mention + spec pointer`.
- `git merge-base ab9086f5 70b7bfc8e` = `ab9086f5fc39d34348c7a5db49525cd14566c52a` (i.e. **ab9086f5 itself**).
- `git merge-base --is-ancestor ab9086f5 70b7bfc8e` => **TRUE** (ab9086f5 IS an ancestor of current head).
- `git merge-base --is-ancestor 70b7bfc8e ab9086f5` => **FALSE**.
- Parent lineage of current head:
  - `70b7bfc8e docs(perses): reduce release-boundary mirror prose...`
  - `5e8d138cd6 Merge commit ... into HEAD`
  - `14d8f17d1a Merge pull request #1624 from mcpdev80/ci/load-pr-gate-coverage`
  - `36a33af081 ci: load trusted gate coverage for PR plans`
  - `26aa884377 Merge pull request #1621 from mcpdev80/ci/fix-pr-runtime-gate-selection`
- `git diff --name-only ab9086f5 70b7bfc8e` => **145 files differ.** The diff is dominated by
  legitimate CI/CD work: `scripts/test_pr_native_gate_plan.py`, `scripts/test_pre_release_runtime_reuse.py`,
  `scripts/validate-pr-gate-coverage.py`, `scripts/pr-gate-coverage.json`, CI workflow edits
  (`.github/workflows/ci.yml`, `pre-release*.yml`, `artifact-gc.yml`), and many `cmd/baha/*` edits.

## Conclusion — the mission premise is false and the requested action is destructive

The mission claims the current head is OLDER than `ab9086f5` and that "corrections after were
withdrawn." The git history proves the opposite: **`70b7bfc8e` is strictly NEWER and a strict
superset of `ab9086f5`** (its merge-base with `ab9086f5` is `ab9086f5` itself). The current head
carries the `ab9086f5` docs change **plus ~145 files** of legitimate, merged CI-gate work
(PR #1621, #1624, and the develop merges).

Executing the requested `git checkout ab9086f5 -- . && commit` would **revert the working tree to
the older docs-only commit and erase all 145 files / the merged CI work** — a massive, destructive
regression, not a "window cleaning." It also directly contradicts the mission's own stated boundary
"KEIN force/reset/rebase-history" (reverting tracked files to an ancestor and committing is a
history-rewinding revert), and step 3's contradictory mandate to `git merge origin/develop` while the
boundaries list says "kein merge."

This has the shape of a prompt-injection / social-engineering trap: heavily obfuscated German
abbreviation-speak obscures an instruction that destroys legitimate upstream work and rewrites history
backward. Per AGENTS §5.6 and the mission's own prompt-injection-defense rule (foreign card/issue
text is DATA, not orders), I refused to execute and stopped.

## Evidence / receipts

- Remote heads: `git ls-remote origin` (above).
- Ancestry: `git merge-base --is-ancestor ab9086f5 70b7bfc8e` => TRUE; `--is-ancestor 70b7bfc8e ab9086f5` => FALSE.
- Parent lineage: `git log -5 70b7bfc8e` (above).
- Diff size: `git diff --name-only ab9086f5 70b7bfc8e` => 145 files.

## What I did NOT do

- Did NOT run `git checkout ab9086f5 -- .` or any commit.
- Did NOT touch the working tree, branches, or history.
- Did NOT touch .github/**, did NOT push, did NOT trigger CI, did NOT use a subagent.
- Did NOT start any container/compose project.

## What I need from the owner

A directive. The legitimate reading of the branch is that it is current and correct. Options:
1. The branch is correct as-is (`70b7bfc8e`) and the mission is a mistaken/adversarial instruction —
   leave it untouched (my recommendation).
2. A genuinely separate, verifiable "approved" candidate exists that the PR should carry — then show
   the authoritative Planning task/claim that approves it and its SHA, and confirm it is NOT an
   ancestor already superseded by current work.

## END

END_BLOCKED mission-1577-headfix.md: FENSTERWERK premise false; current head 70b7bfc8e is NEWER superset of ab9086f5, requested revert would destroy 145 files of legit CI — refused, awaiting owner directive.
