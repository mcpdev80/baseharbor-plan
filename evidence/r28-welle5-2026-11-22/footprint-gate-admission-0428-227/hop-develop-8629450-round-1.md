# 0428-227 footprint-gate-admission (PR 1753) hop — round-1 akte

Sitz `w21-pr1702-0428-142-compat`. Karte 0428-227, PR 1753, eigentuemers-Prio.
Dieser kandidat ist der SCHLUESSEL: PR 1762 und die data-capabilities-familie an seiner Zulassung haengen.

## PLAN

- Plan in board-file + ## PLAN in akte
- karte 0428-227 ueber scripts/plan.py claim (commit + push)
- ls-remote + attestation: develop 8629450e; PR 1753 head b86440c3 (re-hop), base develop 8629450e
- addiver hop: git merge --no-ff <develop-sha> (ziel-sha 8629450e unmittelbar vor merge); NO rebase/amend/force
- push normal; hosted run to terminal: run-id, failed-count, two data-capabilities native rows (docker + podman)
- STOP point: matrix RED on both engines at broker readiness => STOP (0428-237), no rerun, akte with two job-ids + dependency

## base attestation

- planning repo remote (evidence only): `origin https://github.com/mcpdev80/baseharbor-plan.git`
- develop: `8629450ef3c5198bb675331c12f56b2c9377aa1c` (confirmed via ls-remote, still head)
- PR 1753 head (final candidate): `b86440c389b6f8f82b0a3a1dce284d315b4531c7`
- PR 1753 base: develop `8629450e`, non-draft, unmerged (verified via API)
- additivity: branch base develop-content `52a3c5446f` IS ancestor of both branch tip `a40b767` and current develop `8629450e` (verified: YES). Merge parents of hop `b86440c3`: `a40b767` (prior branch head) + `8629450e` (current develop) — additive, no foreign head as parent.
- diff vs develop `8629450e..HEAD --name-only`: only the two PR content files `cmd/baha/ci_integration_operator_enabled.go` and `cmd/baha/ci_integration_operator_enabled_test.go` — no foreign content. The prior hop `a40b767` and final hop `b86440c3` are byte-identical on those two files (empty diff), so the only change since prior CI is the 29-develop-content merge.

## run:

- ONE hosted CI run, run-id `45008538769` (CI · PR #1753, event pull_request, run_number 7248)
- status completed, conclusion FAILURE
- failed-count: 2 (only 2 jobs failed across the whole matrix; all other jobs completed success or skipped)

## native:

The two data-capabilities native rows ran to terminal (completed/failure on BOTH engines, not skipped/queued):

- docker native data-capabilities: run 45008538769, job `137165488041`, `completed/failure`
- podman native data-capabilities: run 45008538769, job `137165488058`, `completed/failure`

Failure mode: identical to prior run 44994268323 on head a40b767 — `TestApplicationCapabilityLifecycleExistingCore/secrets` fails at the secure-runtime broker start on both engines, readiness 503 not_ready, timeout ~2m (docker) / ~5m (podman), mTLS identity fine beforehand. The candidate content is byte-identical to the prior hop, so this failure is the domain of the broker-readiness fix, not this additive hop.

## dependency:

- card 0428-237 (broker readiness fix) is the dependant trigger. This card's PR 1753 depends on 0428-237's develop head landing, then one additive hop and one exact hosted run. The hop is done; the exact run failed at broker readiness. Chain: 0428-237 -> 1753 -> 1762 -> 1723/1725/1761 (data-capabilities family gated on PR 1753 admission).

## repo-rule compliance

- write-set respected: only the two cmd/baha files carry PR content; the develop-content merge touched internal/metrics/testdata, internal/serviceaccess etc. but those are develop HEAD content (additive hop), not edits of internal/** product code by this lane beyond the standard merge. No .github/**, no scripts/** edits.
- no subagents; no merge/close/comment on the product PR; PR left non-draft.
- candidate on the single named branch lane-0428-227-footprint-gate-admission; no second candidate branch invented by this lane (the pre-existing surplus branch lane-0428-227-footprint-gate-admission-rh2 at 43d85d637a0 was left untouched per card note).

## cleanliness:

- no containers/networks/volumes/compose projects started (hosted CI only); worktree workers/0428-227-hop-wt detached at develop HEAD then checked out the PR branch for the hop. No orphaned test stack.

## END w21-pr1702-0428-142-compat BLOCKED

candidate ready for review is NOT reached: matrix RED on both native data-capabilities engines at broker readiness (0428-237). No rerun. Post END_BLOCKED with run-id 45008538769 + two job-ids (137165488041 docker, 137165488058 podman) and dependency 0428-237.
