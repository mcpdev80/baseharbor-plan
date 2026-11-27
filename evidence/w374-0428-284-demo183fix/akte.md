# w374-0428-284-demo183fix — complete PTY final-drain exactly-once capture for PR #183

- card: 0428-284
- implementer (lane X): w374-0428-284-demo183fix
- repo: mcpdev80/baseharbor-demo
- PR: #183 (base develop), branch w366-0428-284-democonsent
- parent candidate (superseded, w373): PR #183 @ 83c80c917858e719118bd21e0183b4516959ac53
- candidate head: 00b87bfc36cb3070bb7046f40d0df798f59ff4b1
- date: 2026-11-27

## Visible Ansatz block (required before first commit)

- owner verbatim (from mission w374-0428-284-demo183fix.txt, card 0428-284): lane w374 = the transport/complete writer for PR #183; w373 is the superseded half-fix carrier.
- git user.name: `w374-0428-284-demo183fix`
- git user.email: `w374-0428-284-demo183fix@baseharbor.local`
- literal commit invocation: `git -c user.name=w374-0428-284-demo183fix -c user.email=w374-0428-284-demo183fix@baseharbor.local commit ...`
- pre-push `%an` gate line (satisfied): `git show -s --format='%an' HEAD` == `w374-0428-284-demo183fix` exactly.

## Base attestation

- demo remote (worktree `git remote -v`): demo -> https://github.com/mcpdev80/baseharbor-demo.git (the github.com/mcpdev80 remote; used for all demo push/fetch).
- PR #183 head BEFORE this lane: 83c80c917858e719118bd21e0183b4516959ac53 (w366-0428-284-democonsent, unqualified, buggy reconcile).
- w373 half-fix head: 1dfead1998254e124ff54a7678ab8ed388e3bee0 (parent carries the two runtime fixes: drive.py line 349 `bytes_read += len(chunk)` in the main read loop, line 411 in the final-drain loop, line 435 `os.fsync(log.fileno())` before reconcile).
- ancestry chain (linear, intended by owner): 83c80c917 -> 1dfead199 -> 442d8bb1c -> 00b87bfc3.
  - `git merge-base --is-ancestor 83c80c917 HEAD`: YES
  - `git merge-base --is-ancestor 1dfead199 HEAD`: YES
  - `git merge-base --is-ancestor 442d8bb1c HEAD`: YES
- `git log --oneline 83c80c917..HEAD`: 442d8bb1c (w374 runtime complete) + 00b87bfc3 (w374 test determinism) on top of the carried 1dfead199. My single authored commit in this shift that completes the review finding is 00b87bfc3.

## Repo-rule compliance

- Write-set: tests/guided/drive.py (w374 commit 442d8bb1c, the runtime completion) and tests/guided/test_consent_capture.py (w374 commit 00b87bfc3, this finding). No product-code delta, no product-auth/consent/authorization delta, no `.github/**` change, no CI change.
- Fail-closed consent tests 22/23: unchanged (verified: my diff touches only test_25).
- No subagents: every step executed inside session e6ca7696-b1f8-492d-b226-876b16925fc5 (lane w374). No local test execution (policy stop 2026-11-26): only `python3 -m py_compile`, `python3` byte-math simulation, `git diff --check`, `git ls-remote`.
- One integration candidate per chain: PR #183 only. The w373 branch w373-0428-284-demo183fix and its accidental PR #184 (now CLOSED) were not touched; PR #184 closure is the coordinator's task.
- Transport: `git fetch demo w366-0428-284-democonsent` -> `git merge --ff-only 1dfead199` (lineage 83c80c917->1dfead199 preserved, no rewrite, no cherry-pick) -> w374 commits on top -> `git push demo HEAD:w366-0428-284-democonsent`. No force, no amend, no new PR.
- No workflow_dispatch, no Hosted Run triggered by this lane (Owner launches on the new exact head).

## Finding -> Fix mapping

### Finding A (w255 HOLD / exact-head review 2026-11-27) — final-drain not flushed + not byte-tracked before reread (runtime)
- Source: `tests/guided/drive.py` run_tty final-drain block.
- Resolution: carried by w373's 1dfead199 (main-loop + final-drain `bytes_read += len(chunk)`, and `log.flush()` + `os.fsync(log.fileno())` before `reconcile_capture_from_log`). w374 commit 442d8bb1c completes the final-drain loop's `bytes_read` advance so the running total is correct across the drain.

### Finding B (exact-head review 2026-11-27) — test_25 not deterministic
- Source: `tests/guided/test_consent_capture.py` test_25_run_tty_final_drain_appends_missing_log_bytes_once.
- Problem: the fake core emitted only a < 4 KiB digest line with a 20ms idle gap. `run_tty` reads up to 4096 bytes per normal `select()` event, so the digest was consumed entirely by the main loop and the final-drain reconcile path was never exercised — the regression passed even against the buggy code.
- Correction: emit a single final core line LARGER than one 4096-byte read. The core now writes a padding prefix (`P` * (4096 - len(digest_line) + 1)) followed by the digest line, so `final_blob` is 4097 bytes. With `delay=0` the digest tail (bytes past the first 4096) is read by the final-drain loop after process exit. The test asserts `transcript.count(digest) == 1` (exactly-once, via `str.count`, not `in`), which fails against the buggy helper (double-append => count 2) and passes with the fix. Empty capture_tail path is covered by the same helper path (test_24 white-box guard).
- Byte math witness (static, not a test run): digest_line_len=134, final_blob_len=4097, bytes in final drain = 1 (>0 => digest tail lands in the drain).

## Test matrix 21-25

- test_21 first transcript captures documented digest + hint on immediate drain — present (unchanged)
- test_22 capture boundary still aborts on foreign error — present (unchanged, fail-closed)
- test_23 capture boundary aborts when digest absent — present (unchanged, fail-closed)
- test_24 reconcile appends unread log bytes (white-box helper guard) — present (unchanged)
- test_25 run_tty final-drain appends missing log bytes exactly once — MODIFIED this lane to be deterministic (> 4096 byte final tail, count()==1)

## Run witnesses

- Parent candidate PR #183 @ 83c80c917: unqualified (buggy reconcile). No qualifying run.
- w373 half-fix PR #184 @ 1dfead199: CLOSED (accidental; coordinator closes by ancestry proof).
- PR #183 @ 00b87bfc36cb3070bb7046f40d0df798f59ff4b1 (this lane):
  - base develop => `pull_request` event fires under CI workflow. Hosted run to be launched by the Owner on this exact head.
  - Delivery witness (two independent sources agree on the exact SHA):
    - `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/w366-0428-284-democonsent` => `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`
    - `gh pr view 183 --repo mcpdev80/baseharbor-demo --json headRefOid` => `{"headRefName":"w366-0428-284-democonsent","headRefOid":"00b87bfc36cb3070bb7046f40d0df798f59ff4b1","state":"OPEN","isDraft":false}`
- Pre-push `%an` gate: `git show -s --format='%an' HEAD` == `w374-0428-284-demo183fix` exactly (both 442d8bb1c and 00b87bfc3).

## END

- status: END_DONE. PR #183 OPEN, non-draft, base develop, head 00b87bfc36cb3070bb7046f40d0df798f59ff4b1 (exact match via ls-remote + gh). Implementation + ancestry correct; test_25 now deterministic (exactly-once, > 4096 byte final tail, count()==1). No product/auth/consent delta; fail-closed consent tests 22/23 unchanged. Hosted Run pending: Owner launches on the new exact head (this lane triggered no workflow_dispatch / no rerun). Merge held pending green exact-head hosted evidence + exact-head review.
- NOTE for coordinator: PR #184 (w373 accidental) is still present as a CLOSED PR; close by ancestry proof per mission.

## Cleanliness

- docker/podman: none started this shift. No compose projects to bring down.
- worktree `workers/worktrees/w374-0428-284-demo183fix` kept (demo remote added for this push).
- plan evidence worktree `workers/worktrees/w374-0428-284-demo183fix-plan` will be removed after push.
