# Gatewatch w103 — hosted CI observation (read-only)

- Lane: w103 (Worker, BEOBACHTUNG, no code)
- Coordinator: f49a3303
- Repo watched: mcpdev80/baseharbor
- Evidence role: watch hosted PR check runs to terminal per PR, record one TABLE line per PR, classify failures (PRODUCT / FLAKY / INFRA) using green-branch references (last green 1357/1362). No rerun, no commit, no PR command — read-only only.
- Started: 2026-11-04 (local)

## PLAN

- Verify gh auth context (repo = mcpdev80/baseharbor)
- For each PR (1354, 1363, 1369, 1355, 1362) find hosted check runs at the given head SHA and watch to terminal (no pending/queued)
- Record per PR: pr, head10, pass, fail, skipping, fail-check names (one TABLE line)
- For failures: extract exact FAIL lines from job log (gh api /actions/jobs/<id>/logs | grep FAIL), note if same spot also falls on green branches (1357/1362), classify PRODUCT/FLAKY/INFRA with one-sentence reason
- Write evidence table + witnesses to baseharbor-plan/evidence/r27-welle3-2026-11-03/gatewatch-1.md
- Post END to f49a3303

## PR inventory (from mission)

- 1354 = 5a5f1b38
- 1363 = d68251ee
- 1369 = bfaddb37
- 1355 = bed00516
- 1362 = 0958107f (old, already terminal — quick re-check it stays terminal)

## TABLE (terminal state, verified 2026-11-04, repo mcpdev80/baseharbor)

| PR | head10 | pass | fail | skipping | fail-checks |
| --- | --- | --- | --- | --- | --- |
| 1354 | 5a5f1b38f5 | 18 | 0 | 10 | none |
| 1363 | d68251ee00 | 2 | 0 | 14 | none |
| 1369 | bfaddb37f4 | 2 | 0 | 14 | none |
| 1355 | bed005160a | 22 | 0 | 10 | none (was 2 pending, waited to terminal) |
| 1362 | 0958107fb8 | 8 | 0 | 10 | none |

## Witnesses

- Overall run conclusion = `success` for every PR via `gh api repos/mcpdev80/baseharbor/actions/runs/<id> --jq '.conclusion'`:
  - 1354 run 41820069131 -> success
  - 1363 run 41820413065 -> success
  - 1369 run 41820625996 -> success
  - 1355 run 41822138124 -> success (waited for pending go-unit-tests job 126547721707 + cli-package-tests job 126547721705 to pass)
  - 1362 run 41815956903 -> success
- Per-PR `gh pr checks` status tally (grep of pass/skipping/pending/queued/failure): zero pending, queued, failure or timed_out across all five PRs.
- Head SHAs match mission exactly: 1354=5a5f1b38, 1363=d68251ee, 1369=bfaddb37, 1355=bed00516, 1362=0958107f.
- Classification: N/A — no failures to classify (PRODUCT/FLAKY/INFRA). No rerun, no commit, no PR command executed — read-only only.
- Green-branch reference (1357/1362): not needed, no failures present.

## End state

- END lane w103-gatewatch: DONE — gruene=5/5 | n/5 rote_mit_klassifikation=keine | alle 5 PRs terminal (gh run conclusion=success), 0 pending/queued/failure, SHAs match Mission; nothing to classify.
