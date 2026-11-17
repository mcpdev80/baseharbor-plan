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
or an alternative: merge `origin/develop` into the branch (fast-forward-free merge commit, ff push allowed) if a no-force path is preferred.

END_BLOCKED mission-097-rebase-develop.md: rebase clean onto develop@e6cce9c73 (candidate 34fb154b4, own commit only, local checks green) but push is non-fast-forward — force needed, STOP+QUESTION per mission gate.
