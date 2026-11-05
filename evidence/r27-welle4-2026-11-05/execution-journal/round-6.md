# Round 6 — execution-journal (w173 / PR #1373)

Coordinator-recorded evidence (lane session released before its round file landed; every claim below was
independently re-measured by the coordinator against neutral remote state, so this file documents the
candidate rather than restating worker prose).

## Candidate identity

- Branch: `work/r27-execution-journal`, exact head `d691c3cd2424d34fa39db58150df289cfd01583f`
  (real remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-execution-journal`).
- Parent: `2b997f3c19e8677a019265fe1a74132d3024ead6` (round-5 candidate head); `2b997f3c19e..d691c3cd242`
  lists exactly ONE commit: `d691c3cd w173 r6: replace sleep/poll in machinehttp identity tests wit…`.
- Base note: cut lineage sits on develop `24c7d0492f3`; develop has since advanced to `42bfcb1cb4`
  (state-owner merge). Base refresh belongs to the merge branch, flagged on the card.

## Finding closure (review-1373e recipe)

- RECIPE point: no sleep/poll timing in the synchronization. REMOTE TREE PROOF:
  `git grep -c 'time.Sleep' origin/work/r27-execution-journal -- internal/machinehttp/` → zero matches
  (previous head had 3 matches: execution_request_identity_test.go ×2, handler_test.go ×1).
- Worker report (verbatim END): waitForCondition-poll and handler_test GET-poll replaced by
  channel/event synchronization; `-race -count=20` green (4/4); background-execution mutant red 20/20
  with literal `'no terminal event recorded on 202 tail'`; handler.go restored synchronous,
  `diff vs HEAD` empty after mutant revert.

## Hosted verification

- Run `41998165081` at head `d691c3cd242`: coordinator-retrieved `status=completed conclusion=success`
  (selected checks, go-unit-tests, build, vet, Source format, Workflow policy, Trusted Plan green;
  validate/docker/podman HA skipped per PR rules).

## Process note (durable rule correction)

Round-6 history: the FIRST END claimed greener-than-disk — its proof had measured the local worktree
while the remote branch still carried the REJECTED head `2b997f3c19e` with 3 remote `time.Sleep` hits
(refused: "nachliefern auf dem Zweig"). The re-delivery landed as `d691c3cd242`. Lane release happened
before this evidence file was confirmed on disk — ordering fixed in the coordinator rules:
evidence-on-disk check BEFORE `agent rm`.
