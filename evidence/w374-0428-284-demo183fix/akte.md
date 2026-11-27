# w374-0428-284-demo183fix — complete PTY final-drain exactly-once capture for PR #183

- card: 0428-284
- implementer (lane X): w374-0428-284-demo183fix
- repo: mcpdev80/baseharbor-demo
- PR: #183 (base develop), branch w366-0428-284-democonsent
- parent candidate (superseded, w373): PR #183 @ 83c80c917858e719118bd21e0183b4516959ac53
- candidate head: d5b44c46c694c3099408939ec962cd723505003c
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
- ancestry chain (linear, intended by owner): 83c80c917 -> 1dfead199 -> 442d8bb1c -> 00b87bfc3 -> 2628f5abe -> d9c7b6136 -> d5b44c46c.
- `git log --oneline 83c80c917..HEAD`: carried w373 half-fix 1dfead199 (runtime bytes_read + flush/fsync), w374 runtime completion 442d8bb1c, w374 test determinism 00b87bfc3, w374 digest-offset 2628f5abe, w374 branch-attribution d9c7b6136, w374 scoping-fix d5b44c46c.

## Repo-rule compliance

- Write-set: tests/guided/drive.py and tests/guided/test_consent_capture.py. No product-code delta, no product-auth/consent/authorization delta, no `.github/**` change, no CI change.
- Fail-closed consent tests 22/23: unchanged.
- No subagents: every step executed inside session e6ca7696-b1f8-492d-b226-876b16925fc5 (lane w374). No local test execution (policy stop 2026-11-26): only `python3 -m py_compile`, `python3` byte-math simulation, static bytecode scope check, `git diff --check`, `git ls-remote`.
- One integration candidate per chain: PR #183 only. The w373 branch w373-0428-284-demo183fix and its accidental PR #184 (now CLOSED) were not touched.
- Transport: `git fetch demo w366-0428-284-democonsent` -> `git merge --ff-only 1dfead199` (lineage 83c80c917->1dfead199 preserved, no rewrite, no cherry-pick) -> w374 commits on top -> `git push demo HEAD:w366-0428-284-democonsent`. No force, no amend, no new PR.
- No workflow_dispatch, no Hosted Run triggered by this lane (Owner launches on the new exact head).

## Finding -> Fix mapping

### Finding A (w255 HOLD / exact-head review 2026-11-27) — final-drain not flushed + not byte-tracked before reread (runtime)
- Source: `tests/guided/drive.py` run_tty final-drain block.
- Resolution: carried by w373's 1dfead199 (main-loop + final-drain `bytes_read += len(chunk)`, and `log.flush()` + `os.fsync(log.fileno())` before `reconcile_capture_from_log`). w374 commit 442d8bb1c completes the final-drain loop's `bytes_read` advance so the running total is correct across the drain.

### Finding B (exact-head review 2026-11-27 04:39Z) — test_25 not deterministic
- Source: `tests/guided/test_consent_capture.py` test_25_run_tty_final_drain_appends_missing_log_bytes_once.
- Problem (round-1): the fake core emitted only a < 4 KiB digest line with a 20ms idle gap; run_tty reads up to 4096 bytes per normal select() event, so the digest was consumed entirely by the main loop and the final-drain reconcile path was never exercised.
- Problem (round-2, 2628f5abe): pad = 4096 - len(digest_line) + 1 produced only 3963 bytes of prefix for the 134-byte digest line, placing the digest at offset 3963-4097, wholly BEFORE the 4096 boundary.
- Correction (round-2): pad_len = 4096 + len(digest_line); digest appended AFTER the prefix so digest_start_offset = 4230 >= 4096 (asserted, computed).
- Correction (round-3, d9c7b6136): added drive.FINAL_DRAIN_CHUNKS module counter (incremented once per chunk in the final-drain loop); test_25 asserts >= 1, proving the digest tail was read by the final-drain branch.
- Correction (round-4, d5b44c46c): Python scoping bug - the counter increment inside run_tty had no 'global' declaration, so the module counter never advanced. Fixed with 'global FINAL_DRAIN_CHUNKS' in run_tty; static bytecode check proves the name is global (in co_names, not in co_varnames[:nlocals]).
- Static negative proof: removing bytes_read += len(chunk) from the final-drain loop makes reconcile re-append the digest tail -> count(digest) == 2, so the test fails deterministically without that line.

## Test matrix 21-25

- test_21 first transcript captures documented digest + hint on immediate drain - present (unchanged)
- test_22 capture boundary still aborts on foreign error - present (unchanged, fail-closed)
- test_23 capture boundary aborts when digest absent - present (unchanged, fail-closed)
- test_24 reconcile appends unread log bytes (white-box helper guard) - present (unchanged)
- test_25 run_tty final-drain appends missing log bytes exactly once - MODIFIED this lane (deterministic > 4096 byte final tail, digest_start_offset >= 4096 asserted, FINAL_DRAIN_CHUNKS >= 1, count == 1)

## Run witnesses

- Parent candidate PR #183 @ 83c80c917: unqualified (buggy reconcile). No qualifying run.
- w373 half-fix PR #184 @ 1dfead199: CLOSED (accidental; coordinator closes by ancestry proof).
- PR #183 heads this lane moved through:
  - 00b87bfc36cb3070bb7046f40d0df798f59ff4b1 (w374 test determinism)
  - 2628f5abe7aab1d0c77c946b94b9f12583d352cd (w374 digest offset fix)
  - d9c7b61361d158f7e62d04abda04811d138baf8d (w374 branch attribution)
  - d5b44c46c694c3099408939ec962cd723505003c (w374 scoping fix - current)
- Delivery witness (two independent sources agree on the exact SHA):
  - `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/w366-0428-284-democonsent` => `d5b44c46c694c3099408939ec962cd723505003c`
  - `gh pr view 183 --repo mcpdev80/baseharbor-demo --json headRefOid` => `{"headRefName":"w366-0428-284-democonsent","headRefOid":"d5b44c46c694c3099408939ec962cd723505003c","state":"OPEN","isDraft":false}`
- Pre-push `%an` gate: `git show -s --format='%an' HEAD` == `w374-0428-284-demo183fix` exactly (all w374 commits).

## END

- status: END_DONE. PR #183 OPEN, non-draft, base develop, head d5b44c46c694c3099408939ec962cd723505003c (exact match via ls-remote + gh). All four review rounds addressed: runtime final-drain fix (carried from w373), deterministic test_25 (>4096 byte digest tail, digest_start_offset >= 4096 asserted), branch-attribution proof via FINAL_DRAIN_CHUNKS, and the Python scoping fix that makes the counter actually advance. No product/auth/consent delta; fail-closed consent tests 22/23 unchanged. Hosted Run pending: Owner launches on the new exact head (this lane triggered no workflow_dispatch / no rerun). Merge held pending green exact-head hosted evidence + exact-head review.
- NOTE for coordinator: PR #184 (w373 accidental) is still present as a CLOSED PR; close by ancestry proof per mission.

## Cleanliness

- docker/podman: none started this shift. No compose projects to bring down.
- worktree `workers/worktrees/w374-0428-284-demo183fix` kept (demo remote added for this push); `git status --short` empty after removing `tests/guided/__pycache__`.

## Cleanliness (append 2026-11-27 05:25Z)

- `rm -rf tests/guided/__pycache__` removed the only untracked dir (static-import side effect); `git status --short` == empty. No other paths touched; no demo push, no local test run.
