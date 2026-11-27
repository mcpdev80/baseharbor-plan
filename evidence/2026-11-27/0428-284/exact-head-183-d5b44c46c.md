# ROLLE: REVIEW — BaseHarbor Demo PR #183, correction round 4

Review date: 2026-11-27 05:21 UTC  
Reviewer lane: `w255-0428-251-demo170codex`  
Card: 0428-284  
Reviewed head: `d5b44c46c694c3099408939ec962cd723505003c`  
PR base: `58ac70679efe5f7e95bd47d602841704fb9ffa67`

## PLAN

1. Verify the exact round-4 diff against the prior review recipe, including counter scope, `run_tty` signature/callers, test assertions, negative proof, file scope, fail-closed tests and commit identities.
2. Record the independent verdict in this evidence-only Akte.
3. Publish this Akte on planning main.

## Identity admission

Card frontmatter owner, read from planning `origin/main` at base `6734964786aaf9f3b73908e439f72b516766c95a`: `owner: w374-0428-284-demo183fix`.

Planning repository remote, verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

This review-evidence commit uses the executing reviewer lane identity `w255-0428-251-demo170codex`. Git user name: `w255-0428-251-demo170codex`. Git user email: `w255-0428-251-demo170codex@baseharbor.local`. Literal invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-284): demo PR 183 correction round 4'`. Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## Verdict

ACCEPT. The round-4 change fixes the counter's function scope, confines its increment to the final-drain loop, preserves `run_tty`'s return signature, and makes test_25 check the drain count, offset and exactly-once result. The static negative proof follows from the tested drain path: without the final-drain byte-count increment, the reconciliation rereads and appends the same digest-bearing tail.

## Findings

1. Pass: `tests/guided/drive.py:311` declares `global FINAL_DRAIN_CHUNKS` inside `run_tty`. The module counter is defined at line 27. Its only increment is line 427, inside the final-drain `while True` after `proc.poll()` returns an exit status; the normal `select` loop has no increment. This addresses the prior Python local-binding defect.

2. Pass: the `run_tty(name, argv, rules, env=None, timeout=900, no_output_timeout=None, cwd=None, expected_returncodes=(0,), capture=False)` signature is unchanged at lines 299–300, and the diff requires no caller changes.

3. Pass: test_25 drives `run_capture`, which calls the real `drive.run_tty` path. It computes `pad_len = 4096 + len(digest_line)`, sets `digest_start_offset = pad_len`, asserts the offset is at least 4096, resets the counter, then asserts `FINAL_DRAIN_CHUNKS >= 1` and `transcript.count(digest) == 1`. The digest is the final fake-Core output; after process exit the final-drain loop reads until the PTY is empty. Thus the counter assertion records that this final-drain branch ran, while the digest is beyond one maximum-size normal read.

4. Pass, static negative proof: the final-drain path appends each chunk to `capture_buffer` and advances `bytes_read`; reconciliation then appends only `log[bytes_read:]`. Removing the final-drain `bytes_read += len(chunk)` leaves the digest-bearing drained bytes outside the offset, so reconciliation appends them again and the exactly-once assertion observes a count of two. No local test was run.

5. Pass: the PR write set remains exactly `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. The comparison from `2628f5abe7aab1d0c77c946b94b9f12583d352cd` to this head adds the counter scope/increment and test_25 checks; tests 22 and 23 are unchanged. No product authentication or consent implementation is touched.

6. Pass, four-field identities and forward lineage. Each commit's author and committer name/email match the same lane identity:

   - `83c80c917858e719118bd21e0183b4516959ac53`: `w366-0428-284-democonsent` / `w366-0428-284-democonsent@baseharbor.local` for both author and committer.
   - `1dfead1998254e124ff54a7678ab8ed388e3bee0`: `w373-0428-284-demo183fix` / `w373-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `442d8bb1c7b7d32bf8a54d2e266388f7012edaba`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `2628f5abe7aab1d0c77c946b94b9f12583d352cd`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `d9c7b61361d158f7e62d04abda04811d138baf8d`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `d5b44c46c694c3099408939ec962cd723505003c`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.

## Hosted evidence state

The exact-head Actions query returned push run `45945163691`, completed failure for `.github/workflows/pr-config-matrix.yml`; it is not a pull_request validation. No successful exact-head Hosted run was found. This content verdict does not qualify the PR for merge; green exact-head Hosted evidence remains required before any product merge.

## Review boundary

This is a read-only review record. No product files were edited, no tests were run locally, no product merge was performed and nothing was pushed to the demo repository.
