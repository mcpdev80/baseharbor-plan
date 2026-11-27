# ROLLE: REVIEW — BaseHarbor Demo PR #183, correction round 2

Review date: 2026-11-27 04:58 UTC  
Reviewer lane: `w255-0428-251-demo170codex`  
Card: 0428-284  
Reviewed head: `2628f5abe7aab1d0c77c946b94b9f12583d352cd`  
PR base: `58ac70679efe5f7e95bd47d602841704fb9ffa67`

## PLAN

1. Compare the exact correction against the prior test_25 review recipe and inspect the full PR write set and commit identities.
2. Record the independent verdict, including whether the negative proof establishes that the final-drain increment is necessary.
3. Publish this evidence-only Akte to planning main.

## Identity admission

Card frontmatter owner, read from planning `origin/main` at base `bee977174d96720b8a309998419d1f6934424341`: `owner: w374-0428-284-demo183fix`.

Planning repository remote, verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

This review-evidence commit uses the executing reviewer lane identity `w255-0428-251-demo170codex`. Git user name: `w255-0428-251-demo170codex`. Git user email: `w255-0428-251-demo170codex@baseharbor.local`. Literal invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-284): demo PR 183 correction round 2'`. Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## Verdict

CHANGES. The new padding calculation now places the digest after offset 4096 and asserts that offset. The exactly-once assertion remains. However, the test does not establish that the digest-bearing chunk is consumed by `run_tty`'s final-drain branch after the child exits; `delay=0` and `final_delay=0` do not synchronize the child exit with the reader's next `select`/`poll` cycle. The negative proof is therefore conditional, not proven by this test: if the main loop reads the digest tail before process exit, removing the final-drain `bytes_read += len(chunk)` has no effect on this assertion.

## Findings

1. Pass, offset calculation: `tests/guided/test_consent_capture.py` at `test_25` sets `pad_len = 4096 + len(digest_line)`, appends the digest line after that prefix, assigns `digest_start_offset = pad_len`, and asserts `digest_start_offset >= 4096`. With `len(digest_line) == 134`, the asserted digest start offset is 4230. This corrects the previous offset error.

2. CHANGES, execution proof: the test still invokes the real `run_tty` path through `run_capture(..., capture=True)`, and the assertion still requires `transcript.count(digest) == 1`. The source-level negative argument is correct only if the digest is read in the final-drain loop: that loop appends the chunk and advances `bytes_read`, after which the log reconciliation starts at `log[bytes_read:]`. But no assertion or controlled schedule proves that this exact chunk was read after `proc.poll()` entered the final-drain branch. A >4096-byte blob and a digest offset do not prove the reader waited until child exit before reading the tail.

   Recipe: keep the computed offset assertion and exactly-once assertion. Add deterministic synchronization or instrumentation that proves the digest-bearing bytes are read by the final-drain branch after process exit, before reconciliation. The negative case must demonstrate that removing only the final-drain `bytes_read += len(chunk)` causes the same test to observe the digest twice and fail. Keep this test in the Hosted CI path; do not use a local test run as qualification evidence.

3. Pass, scope and fail-closed tests: the PR remains limited to `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. The exact comparison from `00b87bfc36cb3070bb7046f40d0df798f59ff4b1` to this head changes only `test_25`; tests 22 and 23 are unchanged. No product authentication or consent implementation is touched.

4. Pass, four-field commit identities and forward lineage. Every commit's author name/email and committer name/email match the same lane identity:

   - `83c80c917858e719118bd21e0183b4516959ac53`: `w366-0428-284-democonsent` / `w366-0428-284-democonsent@baseharbor.local` for both author and committer.
   - `1dfead1998254e124ff54a7678ab8ed388e3bee0`: `w373-0428-284-demo183fix` / `w373-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `442d8bb1c7b7d32bf8a54d2e266388f7012edaba`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `2628f5abe7aab1d0c77c946b94b9f12583d352cd`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.

## Hosted evidence state

The exact-head Actions query returned push run `45942636723`, completed failure for `.github/workflows/pr-config-matrix.yml`; it is not a pull_request validation. No successful exact-head Hosted run was found. This does not change the content verdict. Green exact-head Hosted evidence is still required before any product merge.

## Review boundary

This is a read-only review record. No product files were edited, no tests were run locally, and no product merge or push was performed.
