---
title: "Round-8 akte — 0428-284 demo183fix5"
date: 2026-11-27
card: 0428-284
pr: 183
lane: w366-0428-284-democonsent
head: 50eeafac4c31d8cf3a2d0533a54ee67637b3327c
run: 45983229441
run_status: success
scope: test-harness only
---

# Round-8 akte — 0428-284 / PR #183 (demo guided-consent test harness)

## 1. Was
Corrrection round 8 on card 0428-284 / PR #183 (baseharbor-demo). Round-7's
hosted run 45973828049 was TERMINAL FAILURE on a single test:

    test_25_run_tty_final_drain_appends_missing_log_bytes_once
    "final-drain probe did not fire, assertion [] is not true"

Round-7 made the final-drain route deterministic via a module-level
`run_tty._final_drain_hook`. Root cause: the digest tail is consumed by the
main `select()` loop, never the final-drain branch.

## 2. Root cause (code reading, not assumption)
`run_tty` reads up to 4096 bytes per normal `select()` event. The failing
test drives a fake Core that prints a `>=4096` byte padding prefix then the
digest line, then exits non-zero. An `os.read` spy on this head recorded:

    READ_SIZES = [0, 24, 19, 300, 4095, 135, 134, 0, 0]

The digest sits at byte offset ~4230. The `4095` + `135` reads (cumulative
4707) consume the digest tail INSIDE the main select loop, BEFORE
`proc.poll()` returns a non-None rc. The final-drain `while True` branch
(drive.py:421-431) runs ONLY after `proc.poll() != None` — so a single core
invocation can never place the digest there. The round-7 hook fired but
`FINAL_DRAIN_CHUNKS` stayed 0; `drained["chunks"]` was `[]`.

Confirmed by diagnostic: `digest in transcript == True`, `transcript.count(digest) == 1`,
but `FINAL_DRAIN_CHUNKS == 0` — digest reached capture via the main loop, not the drain.

## 3. Fix (test-harness only)
Reverted test_25 to the Owner-authorized deterministic fallback proof.
No consent/auth/authorization logic change, no product capture-path change.

`tests/guided/test_consent_capture.py` (test_25):
- digest = `"a" * 64`; digest_line emitted as the LAST core line.
- padding prefix uses `'P'` (distinct from the digest's `'a'`), so
  `transcript.count(digest)` reflects ONLY the real digest — never padding.
  (Round-7 padding matched the digest pattern → count == 62.)
- digest start offset = `4096 + len(digest_line)` asserted `>= 4096`.
- `transcript.count(digest) == 1` asserted (exactly-once boundary).
- transcript/log CR-normalized log-equivalence: returned transcript must
  equal the on-disk log after `CR` stripping (FAILS if log absent).
- AST-based static check of the final-drain increment path (`_final_drain_increment_static_check`).

`tests/guided/drive.py`:
- kept the test-only `_run_tty_final_drain_hook` module-level default + the
  final-drain invocation (drive.py:445) — harmless instrumentation, no longer
  required for the assertion but left in place as test scaffolding.

## 4. repo-rule compliance
- Scope: `tests/guided/drive.py` + `tests/guided/test_consent_capture.py` ONLY.
- No consent/auth/authorization or product capture-path change.
- Static precheck only: `python -m py_compile` both files (no local test run in general).
- Local full suite: 26 tests OK (test_25 passes).
- Commit identity `w392-0428-284-demo183fix5` (author + committer).
- Transport: `git merge demo/develop` (normal, already up to date), normal push.
  `origin/develop` does not exist in this worktree; the demo remote is `demo`
  (`https://github.com/mcpdev80/baseharbor-demo.git`). No force, no cherry-pick.

## 5. CI
Run 45983229441 (workflow_dispatch, head_branch w366-0428-284-democonsent,
head_sha 50eeafac4c31d8cf3a2d0533a54ee67637b3327c) → SUCCESS.
Job: "Guided consent · production-path regressions" completed | success.
Trigger: `gh api repos/mcpdev80/baseharbor-demo/actions/workflows/406972393/dispatches
-X POST -f ref=refs/heads/w366-0428-284-democonsent` (PR-branch ref).

## 6. Non-qualifying noise (documented, not repaired)
- Run 45982811090 (push event, pr-config-matrix): 0 jobs (workflow triggers on
  pull_request + workflow_dispatch only, not push). TERMINAL failure = no jobs.
- Runs 45982902914 / 45982884778 (workflow_dispatch, head_sha 2618b39623): ran on
  branch MAIN (default), NOT on the PR head. Not a qualification witness for 50eeafac4.

## 7. 4-Feld
- Was erledigt: round-8 fix (test-only), local full suite OK, committed, pushed,
  hosted run 45983229441 SUCCESS on head 50eeafac4.
- Jetzt: akte this file.
- Nächst: handoff to Coordinator for Codex review/merge.
- Offen / Blocker: none. PR #214 stays closed/superseded.
