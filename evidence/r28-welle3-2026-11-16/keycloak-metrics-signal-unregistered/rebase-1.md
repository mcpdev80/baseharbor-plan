# mission-097-rebase-develop — PR #1660 rebase onto develop (FENSTERWERK)

- Lane: flash, card t-20261116-keycloak-metrics-signal-unregistered / 0428-097
- Mission: /var/tmp/missions/mission-097-rebase-develop.md
- Repository: baseharbor, branch `lane-0428-097-keycloak-signal`, worktree `/var/tmp/w097/wt`
- Result: **END_BLOCKED** at step (3) — push requires force; mission says STOP+QUESTION.

## Planning-repo zone witness (wrong-zone check)

```
$ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan && git remote -v | head -2
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Step 1 — fresh sync + ls-remote witnesses (first action)

```
$ git ls-remote origin refs/heads/develop
e6cce9c73b8edddeff98fa858e83e4b08e8836ef  refs/heads/develop
$ git ls-remote origin refs/heads/lane-0428-097-keycloak-signal
f709e14b58f55be9e6ef93323e31bb9166aa04e8  refs/heads/lane-0428-097-keycloak-signal
$ git rev-parse origin/develop origin/lane-0428-097-keycloak-signal   # after fetch
e6cce9c73b8edddeff98fa858e83e4b08e8836ef
f709e14b58f55be9e6ef93323e31bb9166aa04e8
```

Local branch head == remote head (f709e14b5…) verified before rebase. Old base of the branch:
`14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` (merge-base with old develop), as the mission stated.

## Step 2 — rebase onto origin/develop

```
$ git rebase origin/develop
Rebasing (1/1) Successfully rebased and updated refs/heads/lane-0428-097-keycloak-signal.
```

- No conflicts. The branch carried exactly ONE own commit (`f709e14b5 fix(0428-097): register keycloak-metrics native observability signal`)
  on top of develop@14d8f17d; after rebase the log against develop lists ONLY this commit (rewritten as `34fb154b4`).
- Base attestation: cut/rebased onto `origin/develop` = `e6cce9c73b8edddeff98fa858e83e4b08e8836ef`;
  `git merge-base --is-ancestor origin/develop HEAD` → true.
- `git log --oneline origin/develop..HEAD`:
  `34fb154b4 fix(0428-097): register keycloak-metrics native observability signal` (own commit only).
- Diff vs develop: `internal/identityprovider/keycloak_realization.go` (+54), `internal/identityprovider/keycloak_signal_registration_test.go` (+112). Nothing else.
- Candidate SHA after rebase: `34fb154b4c4ece80f97d266d93d528b68f93e576`.

Local verification (in worktree, TMPDIR=/var/tmp/w097/tmp):
- `go build ./...` — clean.
- `go test ./internal/identityprovider/ -run 'SignalRegistration' -count=1` → `ok github.com/mcpdev80/baseharbor/internal/identityprovider 0.005s`.
  (First attempt under default /tmp failed only with "disk quota exceeded" on temp files — environment, not code.)
- `go vet ./internal/identityprovider/` — clean.

## Step 3 — push with explicit refspec — BLOCKED

```
$ git push origin lane-0428-097-keycloak-signal:refs/heads/lane-0428-097-keycloak-signal
 ! [rejected]  lane-0428-097-keycloak-signal -> lane-0428-097-keycloak-signal (non-fast-forward)
```

Connectivity checks:
- `git merge-base --is-ancestor e6cce9c73(… develop tip) HEAD` → true
- `git merge-base --is-ancestor f709e14b5(… remote branch tip) HEAD` → **false**

Explanation: the remote branch tip f709e14b5 is a rewrite-equivalent of the local commit after rebase
(same content diff vs develop: `git diff` between 34fb154b4 and f709e14b5 relative to their bases is identical),
so the rebased tip is NOT a descendant of the remote tip. A regular fast-forward push is therefore impossible;
publishing the rebased candidate requires `git push --force-with-lease`.

Mission GRENZEN say "KEIN force-push — wenn force noetig waere: STOP+QUESTION". Stopping here.

## State of things at stop

- Remote branch unchanged: `f709e14b58f55be9e6ef93323e31bb9166aa04e8` (post-push ls-remote witness).
- Local branch `lane-0428-097-keycloak-signal` holds the correct rebased candidate `34fb154b4` in worktree `/var/tmp/w097/wt`; it is preserved for the authorized push.
- PR #1660 untouched, still points at f709e14b5.
- No containers/VMs were started; nothing to bring down.
- No `.github/**` changes; no merge; no force-push; no subagents.

## Decision requested (QUESTION → coordinator)

Either authorize `git push --force-with-lease` of `34fb154b4` (content-identical rebase of the single commit onto develop@e6cce9c73, no foreign commits) — then I publish, observe the exact-head pull_request run to terminal success and finish —
or an alternative: merge `origin/develop` into the branch (merge commit, ff push allowed) if a no-force path is preferred.

## Step 3b — Owner answer: merge-path (no force), executed

Owner decision (2026-11-17): Option (b) — `git merge origin/develop` into the branch, normal merge-commit, no force.

- Pre-state witness: remote branch unchanged during the QUESTION window (`f709e14b5…` via ls-remote); local branch reset back to `f709e14b5` (unpublished rebase candidate `34fb154b4` discarded, reflog witness: `rebase (finish)` entry only).
- The plain merge auto-resolved in a way that mattered and was triaged before committing: develop carries `109d879f1 chore: remove historical root evidence notes` which deletes 24 historical `evidence*/…md` files from the repository tree; those files are still present in the branch tree (its base `14d8f17d` predates or bypasses that cleanup, e.g. via `5c6744dc6 merge: reconcile release v0.4.27 with main`). The auto-merge deletes them.
  - Decision: keep the develop-side deletion. Reasons: (1) dispatch rule "EVIDENCE FILES LIVE ONLY IN baseharbor-plan … no main-branch writes ever" — keeping them re-added to the PR tree would recreate exactly the violation develop cleaned up (PR diff vs develop showed +2013 lines of foreign evidence files when they were kept); (2) content safety: deletion is tree-only, blob history remains (`git log -- evidence-r27/cy1.md` still resolves); (3) owner goal "branch tree at current develop state" for the selected-checks selector is satisfied only when the tree equals develop + the two own files.
  - This is a tree-structural resolution (no product content conflicted); `--no-renames` merge; no content conflict in the two own files.
- Merge commit: `22bbec9f5dfbce4590139e14c3522cead4413b2e`.
  - `git log --oneline origin/develop..HEAD` → exactly 2 lines: `22bbec9f5 Merge origin/develop…` and `f709e14b5 fix(0428-097)…` (own commits/merge only, no foreign candidate).
  - `git diff --stat origin/develop..HEAD` → only `internal/identityprovider/keycloak_realization.go` (+54) and `internal/identityprovider/keycloak_signal_registration_test.go` (+112).
  - Ancestry: `origin/develop` (e6cce9c73) is an ancestor of HEAD; previous remote tip `f709e14b5` is an ancestor of HEAD → push is a true fast-forward.
- Local checks on merged tree: `go build ./...` clean; `go vet ./internal/identityprovider/` clean; `TMPDIR=/var/tmp/w097/tmp go test ./internal/identityprovider/ -run 'SignalRegistration' -count=1` → `ok … 0.006s`.
- Push (explicit refspec, no force): `f709e14b5..22bbec9f5  lane-0428-097-keycloak-signal -> lane-0428-097-keycloak-signal`; ls-remote witness after: `22bbec9f5dfbce4590139e14c3522cead4413b2e`.
- PR #1660: state OPEN, isDraft false, `headRefOid = 22bbec9f5dfbce4590139e14c3522cead4413b2e` (gh pr view witness).

## Step 4 — own hosted run observation (Eigenes-Run-Pflicht)

- pull_request run for exact head `22bbec9f5`: `44009183072` ("CI · PR #1660 · CI · Source & Quality", started 2026-11-17T03:17:46Z). Selection now maps real gates (PR · Validation · identity-provider-package-tests, cli-guided-tests, cli-vet, source-contracts, Exact Candidate; native matrix cells evaluate on current develop).
- Outcome (terminal): **SUCCESS**. `gh run view 44009183072 --json status,conclusion,headSha` →
  `{"conclusion":"success","headSha":"22bbec9f5dfbce4590139e14c3522cead4413b2e","status":"completed"}` (7m37s).
  Executed and passed: PR · Trusted Plan, Exact Candidate, Source format, Runner Interface, Demo Pin, Focused Python, Native gate plan,
  Validation (cli-build, cli-vet, cli-guided-tests, source-contracts, identity-provider-package-tests),
  Selected Runtime (atomic/docker/identity, docker, identity). The previously failing 'PR Selected Checks' gate now succeeds
  because the branch tree is at current develop; irrelevant matrices correctly skipped. No failure log lines.
- This pull_request run (44009183072) is the only hosted run the push triggered for head 22bbec9f5 (ls-remote/run-list witness below).

## Verification witnesses (as required by dispatch rules)

```
$ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan && git ls-remote origin HEAD
01285a93179270d0d5fe39e451e0bede287a58d7  HEAD        # evidence commit IS on origin/main
$ git ls-remote origin refs/heads/lane-0428-097-keycloak-signal   # final re-check from product repo
f709e14b58f55be9e6ef93323e31bb9166aa04e8  refs/heads/lane-0428-097-keycloak-signal   # unchanged, no force used
```

## State at END (after merge-path completion)

```
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-097-keycloak-signal   # from the product worktree
e6cce9c73b8edddeff98fa858e83e4b08e8836ef  refs/heads/develop
22bbec9f5dfbce4590139e14c3522cead4413b2e  refs/heads/lane-0428-097-keycloak-signal   # ff push, no force
$ gh run list --repo mcpdev80/baseharbor --commit 22bbec9f5dfbce4590139e14c3522cead4413b2e
completed  success  CI · PR #1660  CI · Source & Quality  lane-0428-097-keycloak-signal  pull_request  44009183072  7m37s
```

- PR #1660: OPEN, not draft, head = 22bbec9f5. Terminal SUCCESS observed on the exact head. No merge performed (owner/Codex scope).
- No containers or compose projects were started by this lane; nothing to tear down.

END_DONE mission-097-rebase-develop.md: merge-path executed, candidate 22bbec9f5 on PR #1660, own pull_request run 44009183072 terminal SUCCESS.

END_BLOCKED mission-097-rebase-develop.md: rebase clean onto develop@e6cce9c73 (candidate 34fb154b4, own commit only, local checks green) but push is non-fast-forward — force needed, STOP+QUESTION per mission gate.
