# 0428-155 — coordinator/ tooling defects (coord tooling fix)

ROLE: worker, ONLY coordinator/. No product code, no baseharbor/, no baseharbor-plan content except this akte.
MISSION: /var/tmp/x-155.txt (KARTE t-20261119-coord-tooling-defects).
DATE: 2026-11-20 (shift started 2026-11-19 23:xxZ).

## PLAN

1. Read mission, confirm scope = coordinator/ only.
2. Reality check: planning repo = baseharbor-plan (origin/main 6968e55b), baseharbor develop HEAD 4b3a3559, branch lane-0428-155 cut from origin/develop (develop is ancestor).
3. DEFECT 1 card-status.py owner-field clear.
4. DEFECT 2 release-lane.py spawn-reference mapping + pool-leak guard.
5. DEFECT 3 dispatch-lane.sh board-name from lane not payload.
6. DEFECT 4 vm-audit.sh holder/dauer exclusion.
7. DEFECT 5 workspace-hygiene.sh cron run + report.
8. Regression unit tests (python3, no product).
9. Local checks: py_compile, bash -n, tests.
10. Commit test file in coordinator repo, write akte, post END_DONE.

## repo-rule compliance

- ONLY coordinator/ edited (product boundary honored; baseharbor/ untouched, baseharbor-plan/ touched only for this akte).
- No .github/** edits, no CI changes, no subagents, no git in workers/baseharbor-plan.
- Branch provenance: base 4b3a3559070e9b81b1886a357f6a46bc6dfce790 (origin/develop), `git merge-base --is-ancestor origin/develop HEAD` returns 0.
- No containers/compose started (host is coordinator/codeman server, not a test host); cleanliness: temp files in /tmp and /var/tmp only, no leftovers.

## DEFECT 1 — coordinator/scripts/card-status.py

BEFORE (line 75): `if a.owner: head = set_field(...)` AND line 124 validation `if a.status == "active" and not field(head, "owner"):`.
AFTER (line 75): `if a.owner is not None:` with a comment distinguishing None from "".
AFTER (line ~124 validation): active-owner check uses `not re.search(r"(?m)^owner:\s*$", head)` so an explicitly-set (empty) owner counts as present; `owner:` line is now written (and `active` passes) instead of silently left stale.

Measured regression (before fix): `--owner ""` left owner = some-owner; after fix, owner field is `owner: ` (present, empty) and check passes. No-`--owner` keeps the existing value.

REGRESSION TEST: `coordinator/tests/test_coord_tooling_fixes.py::Defect1OwnerClear` (2 cases: `--owner ""` clears; omitting it keeps the value).
HANDS: `python3 -m unittest tests.test_coord_tooling_fixes` -> 6 tests OK.

## DEFECT 2 — coordinator/scripts/release-lane.py

BEFORE (line 49): `if ranked[0][0] > 10*60*1000: raise LookupError("no OpenCode session near this Codeman session's start")` — the OpenCode session was inferred from the START CLOCK. Older lanes failed every release with `HOLD ... session/OpenCode release incomplete` even though the acceptance archive was accepted.
AFTER: `open_sessions()` first calls `_resolve_by_reference(directory)` (new helper). It reads the OpenCode id from (1) the spawn registry `watcher-state.json` registered entry, (2) `codeman agent list` `claudeSessionId` of the child whose `parentSessionId` is this Coordinator, or (3) the OpenCode DB row whose `parent_id` == coordinator and directory == lane working dir. Only if NO reference is readable does it fall back to the clock heuristic, with a loud `WARN: ... fell back to start-time heuristic ... guessed` to stderr.

ADDITIONAL FINDING (same file): a failed assignment previously left the lane entry occupying a seat. `open_sessions()` failure now calls `release_pool(lane name)` for THIS lane's reservation only, leaving foreign entries untouched (§5.6).

REGRESSION TEST: `test_reference_beats_clock` (stale createdAt still maps by registry ref) and `test_failed_assignment_frees_own_pool` (only own pool reservation freed).
HANDS: `python3 -m unittest tests.test_coord_tooling_fixes` -> OK. Verified release-lane.py --help and a HOLD path run cleanly (no crash).

## DEFECT 3 — coordinator/scripts/dispatch-lane.sh

BEFORE (line 12): `lane=$(basename "$pf" .txt)` — board name derived from the PAYLOAD filename.
AFTER (line ~13): `lane="${LANE:-}"` (caller-supplied canonical lane name from spawn-lane.sh), fall back to a stable slug of the payload path only when LANE is unset. Board path is `workers/todos/<lane>.json`, per lane.

REGRESSION TEST: `test_board_from_lane_env_not_payload` — payload `/var/tmp/x-155.txt` with `LANE=w083-0428-083-pr1684-datasources-r3` yields the lane name, not `x-155`.

## DEFECT 4 — coordinator/scripts/vm-audit.sh

BEFORE (line 19): `bh=$(docker ps --format '{{.Names}}' 2>/dev/null | grep -c '^bh-')` — counted EVERY bh-* container incl.dauer/shared stacks and holder-owned containers -> false ALARM.
AFTER: counts only lane-owned bh-* containers — excludes `shared` names and names currently held in the lock book (`vm-lock.sh status` holders). The counted line is now named in the output (`[gezählt: ...]`), so a reader sees exactly what was counted.

REGRESSION TEST: `test_counts_only_lane_owned` — `bh-worker` (held) excluded, `bh-lane001` (lane-owned) counted.

## DEFECT 5 — coordinator/scripts/workspace-hygiene.sh

NOT wired into cron. Verified before the run: 5 live worker sessions (w083, w119, w155, w150, w157); every worktree is either < 24h old or has uncommitted changes, so the script prunes nothing. Ran once:

    bash coordinator/scripts/workspace-hygiene.sh 1440

BEFORE: `/` = 176G/193G (92%), workers/ = 36445 MB, worktrees = 55.
AFTER: `/` = 176G/193G (92%), worktrees = 55, live lane `lane-0428-155-coord-tooling` worktree intact (ls-remote witness: `git -C baseharbor worktree list | grep lane-0428-155`).

No orphan/foreign worktree found among the unreferenced set; nothing was removed. The script is safe to schedule.

CRON PROPOSAL (NOT installed — Owner decision per §5.3/mission):

    0 */6 * * * bash /home/marcel/dev/baseharbor-ecosystem/coordinator/scripts/workspace-hygiene.sh 720 >> /home/marcel/dev/baseharbor-ecosystem/coordinator/logs/workspace-hygiene.log 2>&1

Current coordinator cron (crontab -l): watch-keepalive (*), codex-ear (*), coord-tick-once (*/2), ci-watch (*/10), prune-watch (*/15), history-30min (*/30), tmp-sweep (30 * and RAM_GUARD */5). workspace-hygiene.sh is the only hygiene script absent from cron.

## CI coverage for these scripts (DEFECT 5 / §5.3 CI-aufnahmepflicht)

FINDING (needs Owner decision): the coordinator scripts are tracked in a LOCAL-ONLY git repo (coordinator/, `git remote -v` empty), NOT in any product repo (baseharbor/baseharbor-console/baseharbor-demo/baseharbor-node-connector/baseharbor-plan) and NOT in the baseharbor CI matrix (`.github/workflows/ci.yml` runs `go test ./contracts/... ./internal/... ./spec/...` + `go test ./cmd/baha`; no coordinator reference anywhere). Therefore NO GitHub CI job runs these tests today. The new `coordinator/tests/test_coord_tooling_fixes.py` runs under `python3 -m unittest tests.test_coord_tooling_fixes` locally and under `python3 -m unittest discover -s tests` if a coordinator CI group is later added. Per §5.3 CI-aufnahmepflicht, a test that only runs locally is not durable evidence; wiring the coordinator script tests into a CI group would require a change under `.github/**` (Owner scope). Reported as a finding; `.github/**` not edited.

## FOCUS checks

    python3 -m py_compile coordinator/scripts/*.py            -> ALL PY OK
    bash -n coordinator/scripts/*.sh                          -> ALL SH OK
    python3 -m unittest tests.test_coord_tooling_fixes        -> Ran 6 tests, OK

## git witnesses

    git ls-remote origin main            -> 6968e55b... (baseharbor-plan)
    git ls-remote origin develop (baseharbor) -> 4b3a3559070e9b81b1886a357f6a46bc6dfce790
    git merge-base --is-ancestor origin/develop HEAD -> 0 (develop is ancestor of lane-0428-155-coord-tooling)
    coordinator repo commit 7214078e00caa4c6113e1fc6b00f1ee9d08f71de: 0428-155 regression tests

## cleanliness: temp files in /tmp and /var/tmp only; no containers/compose/worktree leftovers; no product repo writes

END lane-0428-155-coord-tooling DONE
