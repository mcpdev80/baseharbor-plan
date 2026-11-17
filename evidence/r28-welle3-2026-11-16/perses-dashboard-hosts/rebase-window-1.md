# mission-1602-hopf — perses-dashboard-hosts sweep / rebase-window-1 (0428-077, PR #1602)

Card: `t-20261114-r28-perses-dashboard-hosts` (0428-077), PR #1602.
Candidate head (acceptance SHA): `1f7b5eee92fb142ba94776fce6738df32c5aab7a`
(branch `lane-0428-077-r28-perses-dashboard-hosts` == PR #1602 head).
Base: `develop` @ `4094448543359a13ba312119304f1f70d3bc40a9`.

## STOP — plain `git merge origin/develop` conflicts (31 markers / 8 files)

The mission's step 2 (`git merge origin/develop`, normal, conflict = STOP + recipe)
hits a hard STOP. A plain merge does NOT resolve. This lane stopped, left the
branch at its original head `1f7b5eee`, and did not commit, push, toggle the PR,
or touch `.github/**`.

## Zone witness (wrong-zone check)

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
    https://github.com/mcpdev80/baseharbor-plan

(Planner repo confirmed = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan,
not workers/baseharbor-plan.)

## Reality sync (first action)

Remote truth via `git ls-remote` (2026-11-17):

    4094448543359a13ba312119304f1f70d3bc40a9  refs/heads/develop
    1f7b5eee92fb142ba94776fce6738df32c5aab7a  refs/pull/1602/head
    1f7b5eee92fb142ba94776fce6738df32c5aab7a  refs/heads/lane-0428-077-r28-perses-dashboard-hosts

`develop` == the mission's base `409444854` (unchanged since the mission was
written). Branch head == PR #1602 head == candidate acceptance SHA.

## Base attestation

- Branch cut from: `origin/lane-0428-077-r28-perses-dashboard-hosts`
  @ `1f7b5eee92fb142ba94776fce6738df32c5aab7a`.
- Merge-base of branch and develop: `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`.
- `git merge-base --is-ancestor 1f7b5eee HEAD` (branch head == HEAD, untouched)
  → true. Only this lane's own candidate commits sit on the ref; no foreign
  candidate carried on top.

## Why the plain merge conflicts (root cause)

Candidate `1f7b5eee` is the **sweeper** that wires the new develop-introduced
Perses selection into the host dashboard. It was authored against a `develop`
that did NOT yet contain **#1590 "Select compatible Perses" (`40944485`)**, which
is now the `develop` head.

- `internal/capability/perses_selection.go`: develop adds the authoritative
  `IdentitySelectionWitness` (11 occurrences:
  `SelectionConfirmed / MetricPresent / MetricCurrent / TargetAuthorized /
  Available` + `NewIdentitySelectionWitness` + reworked
  `FilterEligibleDashboards(catalog, witness IdentitySelectionWitness, ...)`).
  The candidate has ZERO occurrences of `IdentitySelectionWitness`.
- `cmd/baha/app_status_result.go`: the candidate adds
  `HostContainersDashboards map[string]metricsprovider.PersesHostDashboardAvailabilityEntry`
  (field + two initializations) — develop does NOT have this field. develop
  #1590 restructured the surrounding function, so the two edit regions overlap.

Both sides edit the same line ranges of the same files → the 8 add/add and
content conflicts below. The sweeper cannot be merged onto #1590 without
re-binding its fan-in to the new `IdentitySelectionWitness` API.

## Conflict set (measured, 8 files / 31 `<<<<<<<` markers)

    cmd/baha/app_status_result.go            content  4 markers  (struct field + 3 init regions overlap develop #1590)
    internal/application/manifest_render.go  content  1 marker
    internal/application/manifest_test.go    content  1 marker
    internal/capability/perses.go            add/add  2 markers (PersesStatus / ResolveHostDashboardSignalStatus edits)
    internal/capability/perses_selection.go  add/add  8 markers (candidate's new host-dashboard resolver vs develop's IdentitySelectionWitness)
    internal/capability/perses_selection_test.go add/add 8 markers
    internal/capability/perses_test.go       add/add  1 marker
    internal/metrics/perses_contract_test.go content  1 marker

Reproduced with a throwaway worktree branch
(`git checkout -B _v origin/lane-0428-077-r28-perses-dashboard-hosts && git
merge origin/develop`); aborted (`git merge --abort`) and the throwaway branch
deleted. Working tree and ref left clean at `1f7b5eee`. No merge was ever
committed.

## Recipe to unblock (Owner decision point — NOT executed by this lane)

A plain merge cannot resolve this (per AGENTS §5.2 no force, no self-merge
approval). The only viable reconciliation is a **rebase of the sweeper onto
develop** (`git rebase origin/develop`), then resolve the 8 files by binding the
host-dashboard fan-in to the develop-introduced `IdentitySelectionWitness`:

1. `cmd/baha/app_status_result.go` — keep the candidate's `HostContainersDashboards`
   field + both initializations (`app_status_result.go:39`, `:152`, `:255`);
   resolve the 3 surrounding hunks by adopting develop's #1590 function body
   around them.
2. `internal/capability/perses_selection.go` — adopt develop's `IdentitySelectionWitness`
   and the `FilterEligibleDashboards(catalog, witness IdentitySelectionWitness,
   backendSignals)` signature; the candidate's host-dashboard resolver must build
   its `IdentitySelectionWitness` from real evidence (real Keycloak metric present,
   pinned to `AcceptedPersesVersion`, identity selected, Target authorized) and
   never from a caller-supplied status boolean (owner decision 2026-11-16).
3. `perses_selection_test.go` / `perses_test.go` / `perses_contract_test.go` —
   rewrite the candidate's host-dashboard tests against the new witness-based
   API (positive: real signal + authorized Target; negative: no-signal /
   wrong-version / unauthorized / caller-supplied true; fail-closed default).
4. `manifest_render.go` / `manifest_test.go` / `perses.go` — resolve the small
   content/add-add hunks to take develop's `AcceptedPersesVersion`/three-state
   boundary (v0.55.1, #1577) together with the candidate's host-dashboard wiring.
5. Fast-forward the sweeper to the new head (own commits only), refspec-push with
   `--force-with-lease` only if the Owner authorizes the rebase (the mission
   forbids plain force; a rebase that lands on develop is a different operation
   and needs an explicit Owner go-ahead), re-open a clean mergeability, and
   re-run the CI run to terminal.

This is a scope decision — the mission mandates a plain merge and labels conflict
as STOP+recipe. This lane therefore did NOT rebase, commit, push, toggle, or run
CI. All 8 conflict regions and the exact resolve recipe are recorded above.

## Local verification

Not run — blocked by the STOP. No `go build / vet / gofmt / test` executed
against a merge candidate (there is none).

## Push / PR state

Not performed. PR #1602 state left exactly as found. No refspec-push, no
`--force`, no merge. (For the record, the current remote head of both
`refs/heads/lane-0428-077-r28-perses-dashboard-hosts` and `refs/pull/1602/head`
is still `1f7b5eee92fb142ba94776fce6738df32c5aab7a`.)

## CI / new tests / .github

None this shift. No `.github/**` file touched or triggered (the sweep candidate
carries develop's workflow state only after a rebase that this lane did NOT do).
No new test added, no `workflow_dispatch`/rerun.

## Scope compliance (GRENZEN)

- No `.github/**` edits, no `workflow_dispatch`, no reruns, no merge of the PR,
  no ready-for-review toggle.
- No force-push, no second candidate branch (single `lane-0428-077` ref only).
- No subagents (§4.8); every step executed in this session.
- Scratch confined to `/tmp`; no docker/podman/compose started on this host.
- No evidence written into a product repo; evidence lives only in
  baseharbor-plan (this file).

## Evidence provenance

- Evidence dossier committed + pushed to `origin/main` of baseharbor-plan (second
  to last action). Remote `main` head shown after push.

## END line

END_BLOCKED mission-1602-hopf.md: plain `git merge origin/develop` conflicts in 8 files / 31 markers vs #1590 (identity-selection-witness) rewrites of the same sweeper files. Branch left clean at `1f7b5eee92fb142ba94776fce6738df32c5aab7a` (== PR #1602 head); no commit, push, force, PR toggle, CI run, or `.github/**` change. Rebase recipe + exact resolve locations recorded above; Owner decision required to rebase the sweeper onto develop.
