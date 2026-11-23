# 0428-261 — Trusted Plan catalog baseline rows for PR #1816 (round 1)

Lane: w51-0428-261-catalog. Mission: coordinator/missions/w51-0428-261-catalog.txt.
Card: tasks/t-20261124-gate-catalog-baseline-1816.md (0428-261).
Candidate: PR #1817 https://github.com/mcpdev80/baseharbor/pull/1817 (draft until CI green),
branch lane-0428-261-catalog-baseline, head 3bae61a71a66913e50f92b94e486a15a3253d74f.

## PLAN

1. Read mission; create numbered work plan (todowrite board file workers/todos/w51-0428-261-catalog.json + this list) — done
2. Verify remotes; attest develop base SHA via git ls-remote — done
3. Claim task 0428-261 — done (coordinator claim at plan 6b2c59eaf already names w51-0428-261-catalog; plan.py refuses re-claim of an active task, "Keep it minimal")
4. Create worktree + branch lane-0428-261-catalog-baseline from exact develop SHA — done
5. Add exactly 3 catalog rows in scripts/pr-gate-coverage.json (components list) — done
6. Offline JSON + catalog validation (planner self-check) — done
7. Provenance witnesses + push branch through GitHub remote — done
8. Open draft PR against develop; write this evidence and push to origin/main — done (see witnesses)
9. Watch exact-head Hosted CI to terminal state (no local product tests) — in progress at time of writing
10. END post with PR number, head SHA, ls-remote, hosted run id

## Remote verification (first git action)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v` (quarantined checkout, NOT cited as remote truth):
  origin -> https://github.com/mcpdev80/baseharbor.git (and lane-origin same URL). All pushes below use the explicit GitHub URL.
- Planning repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
  origin https://github.com/mcpdev80/baseharbor-plan.git (verified BEFORE this evidence commit).

## Base attestation

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` output:

    d4fa8c589e02bf6708d9e6beba7a510c1a2efc7e	refs/heads/develop

Branch cut point: worktree created directly at that SHA
(`git worktree add -b lane-0428-261-catalog-baseline /tmp/opencode/w51-0428-261-wt d4fa8c589e02bf6708d9e6beba7a510c1a2efc7e`).

Ancestry proof:

    $ git merge-base --is-ancestor origin/develop HEAD   (origin/develop = d4fa8c589...)
    ANCESTRY-OK

Own-commits-only proof:

    $ git log --oneline origin/develop..HEAD
    3bae61a71 ci(gate): register Trusted Plan rows for PR #1816 sources

Diff name-only proof:

    $ git diff origin/develop...HEAD --name-only
    scripts/pr-gate-coverage.json

Single file, 15 insertions, no other changes (git diff --stat: `1 file changed, 15 insertions(+)`).

## The change

Three rows added at the head of the `components` array of scripts/pr-gate-coverage.json,
mirroring the existing object shape (id + path + surfaces, same style as
source.cmd_baha_secret_audit_test_go):

- source.cmd_baha_app_status_collect_go -> cmd/baha/app_status_collect.go
- source.cmd_baha_app_status_perses_alert_evaluator_0428_152_test_go -> cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go
- source.cmd_baha_perses_lifecycle_go -> cmd/baha/perses_lifecycle.go

All three with surfaces `["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]`.

No `.github/**` edits, no product code, no broad package rows (0428-260 lesson: package-level
rows were rejected; guard tests fail at d4fa8c589).

## Targeted selection proof (planner self-check, no product test executed)

`scripts/validate-pr-gate-coverage.py` exposes `validate()` and `resolve_covered_gates()`;
run against the candidate catalog:

- `validate(cov, release_requirements)` -> `validate errors: []` (catalog contract valid, ids unique, surfaces declared)
- `resolve_covered_gates(["cmd/baha/app_status_collect.go", "cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go", "cmd/baha/perses_lifecycle.go"], cov)` ->
  all three paths resolve to declared component owners (previously unresolved -> fail-closed "uncataloged source change" error).
  This is exactly the set of files changed by PR #1816 (verified via a fresh clone:
  `git diff --name-only origin/develop refs/pull/1816/head` on head 70ab77ad5e8f88faaac78c90c63a985bb69a72e5 lists precisely those three paths).
- For this PR's own diff (only `scripts/pr-gate-coverage.json`) the planner reports the path as
  unresolved -> conservative broad fallback selection; the aggregate run started
  (Source & Quality 45290693530) rather than failing open.

No local product/unit test suite was run (hosted-only, Owner direction 2026-11-23). The
offline checks above are pure planner-function evaluation of the candidate file in /tmp,
not a product test invocation.

## Hosted CI (exact head 3bae61a71)

- Workflow run: 45290693530 "CI · Source & Quality", headSha 3bae61a71a66913e50f92b94e486a15a3253d74f (observed in_progress at evidence write time; terminal outcome and gate table appended to this file before END, per §4.6).

## cleanliness

- No containers/networks/volumes started (no docker/podman commands run on any host).
- Local artifacts only: /tmp/opencode/w51-0428-261-wt (lane worktree) and /tmp/opencode/w51-1816
  (read-only clone used for the changed-path witness). Both live under /tmp/opencode, outside the ecosystem root.

## Delivery witnesses

- Push: `git push https://github.com/mcpdev80/baseharbor.git lane-0428-261-catalog-baseline:refs/heads/lane-0428-261-catalog-baseline` -> `[new branch]`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-261-catalog-baseline` ->
  `3bae61a71a66913e50f92b94e486a15a3253d74f	refs/heads/lane-0428-261-catalog-baseline`

## CI gate coverage of this change

No new tests were added by this PR. The routes that consume the catalog in hosted CI are the
native-gate selection in .github/workflows/ci.yml (lines 504-510: the PR base's
scripts/pr-gate-coverage.json + scripts/validate-pr-gate-coverage.py drive
scripts/pr-native-gate-plan.py over the PR's changed paths) and the controller-pinned planner
run (ci.yml line 865: validate-pr-gate-coverage.py and pr-gate-coverage.json are fetched at the
trusted controller SHA and used to build pr-plan.json). This PR's own candidate file is
additionally parsed by those jobs when it runs its own Selected Checks. The three new rows bind
the #1816 paths to the pre-existing docker/podman data.capabilities gates; no `.github/**`
change is needed and none was made. Note: #1816 selects those gates only once these rows are on
the trusted develop base (ci.yml:502-505 uses the BASE catalog; per the 0428-152 blocker text),
which is exactly what this PR lands.

## Status

- Candidate published, PR #1817 draft, exact-head CI observed. MERGE-FROST respected: nothing merged, no direct develop writes.

END_DONE w51-0428-261-catalog: PR #1817 (draft, exact-head CI 45290693530) — 3 catalog rows landed, awaiting Owner merge; #1816 rebases after.
