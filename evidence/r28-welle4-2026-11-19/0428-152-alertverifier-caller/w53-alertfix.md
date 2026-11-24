# 0428-152 · alert-verifier caller wiring — w53-alertfix

Lane: w53-0428-152-alertfix (flash seat, rotated from stalled w52)
Card: t-20261119-r28-perses-alert-verifier-caller-wiring
PR: https://github.com/mcpdev80/baseharbor/pull/1816 (base develop, OPEN, not merged — Merge-Frost)
Branch: lane-0428-152-alertverifier-caller
Prior head: b21d144e2c482304d24bed1e30529e315251a878 (mission text)
Remote branch head at start: 916dccc856ae33fa2927ae27f1ec55014a293068

## PLAN

1. Read mission file and register plan in board JSON and evidence — done
2. Verify remotes and claim task via scripts/plan.py claim in baseharbor-plan — claim already published (card active, owner w53-0428-152-alertfix, db5aaec34)
3. Inspect branch lane-0428-152-alertverifier-caller and create worktree — done
4. FIX 1: make alert-evaluator state derivation return not configured / configured_unverified / unavailable distinct states in cmd/baha/perses_lifecycle.go — present at remote head 916dccc85
5. FIX 2: seed authenticated operator context in TestPersesAlertEvaluatorObservationPersesStatusSurface via runWithIOAsTestOperator / testOperatorContext — present at remote head 916dccc85
6. Commit, prove branch provenance, push new head and update PR #1816 — no new commit needed (remote head already contains both fixes)
7. Write evidence file in baseharbor-plan and push to origin/main — this file
8. Monitor exact-head Hosted CI to terminal and post END — pending

## Planning repo witness (before first evidence commit)

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

## Base attestation and branch provenance

    $ git remote -v            # first git action in the worktree
    lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
    lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
    origin       https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
    origin       https://github.com/mcpdev80/baseharbor.git (push)
    upstream     https://github.com/mcpdev80/baseharbor.git (fetch)
    upstream     https://github.com/mcpdev80/baseharbor.git (push)

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-152-alertverifier-caller
    6df6807e7651b38fc142559ea9780238264b6d8f  refs/heads/develop
    916dccc856ae33fa2927ae27f1ec55014a293068  refs/heads/lane-0428-152-alertverifier-caller

Branch checked out from exactly 916dccc856ae33fa2927ae27f1ec55014a293068.

    $ git merge-base --is-ancestor lane-origin/develop HEAD && echo ANCESTOR_OK
    ANCESTOR_OK

    $ git diff lane-origin/develop...HEAD --name-only
    cmd/baha/app_status_collect.go
    cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go
    cmd/baha/perses_lifecycle.go

    $ git log --oneline lane-origin/develop..HEAD
    916dccc85 0428-152: keep the evaluator 'not configured' until a deployment wires it
    b21d144e2 0428-152: drop the self-cataloging from this PR
    5301e8c8b 0428-152: use the underscore component ids the validator requires
    817775471 0428-152: map the three catalog rows to the data.capabilities surfaces
    caee5b546 0428-152: register gate coverage for the consumer files
    999f58d62 0428-152: resolve the perses status seam by application name
    ea75397c4 0428-152: add the alert-evaluator consumer to 'baha app perses status'
    47eed06f3 0428-152: assert the consumer on the production collection path
    8b691cb65 0428-152: tolerate the absent observation on non-applied command faces
    227725a0d 0428-152: run the alert-evaluator consumer on the applied status face
    bdb4274d8 0428-152: wire the Perses alert-evaluator verifier into 'baha app perses status'

All commits are this card's own (11 commits on branch, no foreign candidate). The remote branch head 916dccc85 already contains the two fixes named in the mission:
- FIX 1: cmd/baha/perses_lifecycle.go adds persesAlertEvaluatorObservationWithApplication(m, applied) and deploymentApplied(resolved) and uses them in reportPersesSurfaceStatus; cmd/baha/app_status_collect.go collectPersesAlertEvaluatorObservation also uses the applied-aware helper.
- FIX 2: cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go TestPersesAlertEvaluatorObservationPersesStatusSurface wraps ctx with testOperatorContext(ctx) before the direct seam call and calls runWithIOAsTestOperator for the command face.

Therefore no new commit is created; the candidate is the remote head 916dccc85.

## What was implemented

See fix-1.md for the original implementation. The w52/w53 correction adds the three-state machine on the perses status surface and the test-operator seeding.

## Tests and CI route

The tests live in cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go and are picked up by the Hosted PR Go-unit shard through `go test ./cmd/baha` in scripts/pr-unit-database.sh. No new test was added; existing tests were corrected in-place.

## Hosted CI (self-run duty §4.6)

- Prior run 45294765410 (head b21d144e) failed cli-0 and cli-2.
- Run 45298447080 (exact head 916dccc85): cli-1 failed because the unselected
  manifest-only case received the generic not-applied detail instead of the
  verifier's "Perses is not selected" reason.
- Head 4bfa655ef pinned the manifest-only cases to the applied face.
- Head a80dd26aa routes the unselected not-configured state THROUGH the verifier
  so the fail-closed reason is preserved verbatim, and restores the
  `persesAlertEvaluatorStatusObservation` helper for the manifest-only cases.
  Exact-head Hosted CI run — pending.

## cleanliness

- No containers, networks, volumes or compose projects started by this lane on the coordinator host or any SSH host.
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/w53-0428-152-alertfix-wt
- The prior w41 worktree was removed and the branch checked out here; no second branch exists.

## repo-rule compliance

- Write set: cmd/baha/app_status_collect.go, cmd/baha/perses_lifecycle.go, cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go only.
- scripts/** and .github/** untouched.
- No local product test suite executed; verification is exact-head Hosted CI only.
- No subagents.
- No merge (Merge-Frost); PR #1816 open at 916dccc85.
