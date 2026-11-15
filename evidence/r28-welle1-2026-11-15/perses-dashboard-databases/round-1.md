# r28 wave 1 — Perses database dashboards (card 0428-076)

Mission file: `/tmp/opencode/mission-welle2-076.md`
Card id: `t-20261114-r28-perses-dashboard-databases`
PR base (named by mission): `lane-0428-080-r28-perses-selection` = `85b4cbb598272e28944e48b6895ce8935031c9ba`

## Status

END_BLOCKED — cannot begin implementation. The whole prerequisite chain is
unresolved and the named base branch does not exist on the upstream remote.

## Reality witnesses (measured, not assumed)

- Planning repo origin HEAD: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git`
  - `08ac9c64739d7192b3d75aaf2a189826c5dc3692	HEAD`
  - `08ac9c64739d7192b3d75aaf2a189826c5dc3692	refs/heads/main`
  - No `refs/heads/lane-0428-080-r28-perses-selection` anywhere.
- Task state via `python3 scripts/plan.py show t-20261114-r28-perses-dashboard-databases`:
  - `state: waiting` → `depends on t-20261114-r28-perses-dashboard-selection: NOT accepted`
- Dependency chain:
  - `t-20261114-r28-perses-contract-seam` → state `wait` (blocked)
  - `t-20261114-r28-perses-dashboard-selection` → state `wait`, depends on
    `t-20261114-r28-perses-contract-seam` (NOT accepted); depends on
    `t-20261114-r28-perses-signal-inventory` (accepted)
  - My card depends on the selection (NOT accepted) → not claimable/active yet.

## Why implementation is blocked

1. The mission stacks my lane onto head `85b4cbb5...` of
   `lane-0428-080-r28-perses-selection`. That branch is not reachable:
   absent from the remote, absent from `origin/*`, and not present locally in
   the planning repo. I therefore cannot prove that SHA is an ancestor of any
   commit I would make (branch-provenance requirement), and I cannot build on
   the Perses-selection write-set this card is meant to extend.
2. The card is in `waiting`/`claimed`-ineligible state: its prerequisite is
   `NOT accepted`. Per the task contract and §5.1, a task may only move
   planned→claimed on a successful claim, and the claim is gated on the
   prerequisite being accepted. It is not.
3. The task's own "Verified starting points" note (static ref `cd77e20e` at
   Core `develop`) is a static reference, not a runtime proof; it cannot
   substitute for a live base branch or a resolved prerequisite.

## What I did NOT do (deliberate, per scope)

- Did not create a branch, commit, or push in the product repo or the planning
  repo. No second candidate invented.
- Did not edit any `.github/**` file.
- Did not start or leave any docker/podman compose project.
- Did not spawn a subagent.
- Did not move the card state (that is the coordinator/owner action when the
  prerequisite resolves).
- Did not park in an interactive question dialog — reported via QUESTION line
  and this END_BLOCKED post.

## Cleanliness

- No worktree created under `/home/marcel/dev/baseharbor-ecosystem` or
  `/tmp/opencode/welle2-076/`.
- No containers, networks, volumes, or compose projects started.
- No evidence or scratch files written outside this evidence file.

## Next trigger

When (a) the base branch
`lane-0428-080-r28-perses-selection` exists upstream at a concrete SHA that is
an ancestor of the working tree, and (b) `t-20261114-r28-perses-dashboard-
selection` transitions to `accepted` (so the prerequisite is met), then:
claim the card (`python3 scripts/plan.py claim` + push), cut my lane from that
proven base SHA (witnessed with `git ls-remote`), implement the PostgreSQL /
MongoDB panels within the bounded write-set, run the focused tests by name
through CI/native gates, publish a single draft PR titled with the card number,
archive evidence in this directory, and post END_DONE with the head SHA.
