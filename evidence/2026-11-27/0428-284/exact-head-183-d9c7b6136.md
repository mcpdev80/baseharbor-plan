# ROLLE: REVIEW — BaseHarbor Demo PR #183, correction round 3

Review date: 2026-11-27 05:09 UTC  
Reviewer lane: `w255-0428-251-demo170codex`  
Card: 0428-284  
Reviewed head: `d9c7b61361d158f7e62d04abda04811d138baf8d`  
PR base: `58ac70679efe5f7e95bd47d602841704fb9ffa67`

## PLAN

1. Verify the exact correction against the prior review recipe: counter scope, `run_tty` signature/callers, test assertions, negative proof, scope, tests 22/23, and all commit identities.
2. Record the independent verdict and any remaining forward correction recipe.
3. Publish this evidence-only Akte to planning main.

## Identity admission

Card frontmatter owner, read from planning `origin/main` at base `4c6ddb18fe517607f2a848f8ceef9b17e0317726`: `owner: w374-0428-284-demo183fix`.

Planning repository remote, verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

This review-evidence commit uses the executing reviewer lane identity `w255-0428-251-demo170codex`. Git user name: `w255-0428-251-demo170codex`. Git user email: `w255-0428-251-demo170codex@baseharbor.local`. Literal invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-284): demo PR 183 correction round 3'`. Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## Verdict

CHANGES. The test now computes and asserts digest start offset 4230, preserves the exactly-once assertion, and checks that the final-drain branch read at least one chunk. However, the instrumentation itself has a Python scoping error: `run_tty` assigns to `FINAL_DRAIN_CHUNKS` with `+= 1` at `tests/guided/drive.py:422`, but the function has no `global FINAL_DRAIN_CHUNKS` declaration. Python therefore treats the name as local and attempts to read it before local assignment. Any final-drain chunk raises `UnboundLocalError`, and test_25 cannot produce the claimed branch count.

## Findings

1. CHANGES: `tests/guided/drive.py:27` defines the module-level counter; `run_tty` begins at line 299. The only increment is line 422, inside the final-drain loop, and a source search finds no `global FINAL_DRAIN_CHUNKS` declaration in `run_tty`. Because the augmented assignment makes the name local to the function, the increment raises `UnboundLocalError` whenever a final-drain chunk is processed. This also breaks any other `run_tty` caller that reaches that branch, regardless of `capture` mode.

   Recipe: declare `global FINAL_DRAIN_CHUNKS` in `run_tty` before the increment, or use another counter mechanism that does not change the `(rc, buffer)` return signature. Keep the increment only in the final-drain loop. Then the real-path test must complete and assert the counter is at least one after the run.

2. Pass, review recipe coverage after the scope fix: `test_25` sets `pad_len = 4096 + len(digest_line)` and asserts `digest_start_offset >= 4096` at `tests/guided/test_consent_capture.py:766–775`; with the 134-byte line the start offset is 4230. It calls `run_capture`, which invokes the real `drive.run_tty` path, resets `drive.FINAL_DRAIN_CHUNKS`, asserts the counter is at least one after the run, and retains `transcript.count(digest) == 1` at lines 788–815. Since the digest is the fake Core's final emitted output and the final-drain loop reads until empty, once the counter works this fixture's remaining tail includes the digest; removing the final-drain `bytes_read += len(chunk)` leaves the digest in `capture_buffer` and makes reconciliation append it a second time. The static negative reasoning is valid for this exercised branch.

3. Pass, scope and fail-closed coverage: the PR write set remains exactly `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. The exact comparison from `2628f5abe7aab1d0c77c946b94b9f12583d352cd` to this head adds the counter and test assertions; tests 22 and 23 are unchanged. No product authentication or consent implementation is touched. The `run_tty` function signature and callers remain unchanged in the diff.

4. Pass, four-field identities and linear lineage. Each commit has matching author and committer name/email:

   - `83c80c917858e719118bd21e0183b4516959ac53`: `w366-0428-284-democonsent` / `w366-0428-284-democonsent@baseharbor.local` for both author and committer.
   - `1dfead1998254e124ff54a7678ab8ed388e3bee0`: `w373-0428-284-demo183fix` / `w373-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `442d8bb1c7b7d32bf8a54d2e266388f7012edaba`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `2628f5abe7aab1d0c77c946b94b9f12583d352cd`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.
   - `d9c7b61361d158f7e62d04abda04811d138baf8d`: `w374-0428-284-demo183fix` / `w374-0428-284-demo183fix@baseharbor.local` for both author and committer.

## Hosted evidence state

The exact-head Actions query returned push run `45943809749`, completed failure for `.github/workflows/pr-config-matrix.yml`; it is not a pull_request validation. No successful exact-head Hosted run was found. This does not change the content verdict. Green exact-head Hosted evidence remains required before any product merge.

## Review boundary

This is a read-only review record. No product files were edited, no tests were run locally, and no product merge or push was performed.
