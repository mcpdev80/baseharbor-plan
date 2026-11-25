# w157 — END handoff for card 0428-287 / PR #1835

**Lane:** w157-0428-287-pr1835-preservation (seat released per owner; card continues in a FRESH lane per new-task=fresh-lane rule — I start nothing new).
**Exact head:** `72fc60a923b7c9b91b803f469c8c5cf3572e0448` (author `w157-0428-287-pr1835-preservation`, lane OK; develop-hopped onto `2a141387d` via #1832).
**PR #1835:** retargeted to `72fc60a92`; OPEN.

## Card 0428-287 product delta (intact on head)
- `cmd/baha/application_destroy_authorization.go` (+30) — w105 fix: incomplete-inventory recovery for stuck/failed-apply.
- `cmd/baha/installation_reset_preservation_test.go` (+201) — my regression (shared/foreign provider preserved on install reset; red-first).
- `cmd/baha/w287_destroy_after_failed_apply_test.go` (+169) — w105 regression.
- `scripts/pr-gate-coverage.json` — wired test into `native/docker/data-capabilities` + `native/podman/data-capabilities` (`source.cmd_baha_installation_reset_preservation_test_go`, `runtime_specific: true`); catalog valid; selector fires both on the head.

## Run IDs so far
- Docker: [45605189539](https://github.com/mcpdev80/baseharbor/actions/runs/45605189539) `success` on `40f72d101` — `atomic/docker/data-capabilities` green. Docker witness MET.
- Podman: [45611090994](https://github.com/mcpdev80/baseharbor/actions/runs/45611090994) `failure`, [45611866489](https://github.com/mcpdev80/baseharbor/actions/runs/45611866489) `failure`, both on `72fc60a92`.

## Podman verdict (diagnosed auth/setup gap, not a pass)
Both podman runs fail at the podman-quadlet `baha doctor` probe with the operator-unauthenticated error:
`2026-11-25T12:11:12.7977143Z   Managed-environment machine operations require an authenticated BaseHarbor operator.`
`2026-11-25T12:11:12.8003049Z ##[error]Process completed with exit code 2.`
Resolution hint in log: `authenticate the BaseHarbor operator` / `Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.`
Diagnosed-blocked: this podman runner lacked a provisioned BaseHarbor operator (unauthenticated). NOT a pass, NOT yet proven to be a runner-provisioning gap — resolution requires an authenticated operator. My card delta (destroy plan builder + preservation regression test) does not touch doctor/operator auth, so not a card-0428-287 semantic defect. Same probe passed on SUCCESS run `45608237959` on `2a141387d`. Auth checks left intact; no workaround; any test-only login/OIDC fixture decision held for owner authorization (authorized lane/Codex). Podman witness stays OPEN pending a podman runner with a provisioned operator. Other podman native gates skip because they depend on podman-quadlet.

## Red-first baseline proof (contract)
- Red baseline: base `55d17d437` -> `ok github.com/mcpdev80/baseharbor/cmd/baha 0.008s [no tests to run]` (assertion absent; test file introduced one commit later).
- Green candidate: `TestInstallationResetPreservesSharedForeignProvider (1.38s)` PASS on `72fc60a92`.

## What the FRESH lane must do (no merge on my part)
1. Obtain the required PODMAN witness on a provisioned podman runner (podman-quadlet passes doctor, then guided+lifecycle+data-capabilities to terminal). Docker already MET.
2. If develop moved again past `2a141387`, hop first (merge origin/develop + normal push, no force), re-qualify on the new exact head (two same-head full-green IDs), retarget PR #1835.
3. Full CI (PR event) terminal green on the final exact head + two same-head full greens.
4. Then HANDOFF for Codex review/merge (w136/w156 roster).

## Cleanliness
No lane-owned containers/networks/volumes/state-dir leftovers created by w157. Temporary git worktrees (base/candidate for red-first) removed; `git worktree prune` clean. Only artifacts: `/tmp/w157-*.sh`, `/tmp/w157-*.txt`, `/tmp/w157-*.json` (logs), `/tmp/w157-changed*.txt` (selector input). No `bh-*` stacks touched. Podman/docker runner state is the CI runner's, not w157-owned.
