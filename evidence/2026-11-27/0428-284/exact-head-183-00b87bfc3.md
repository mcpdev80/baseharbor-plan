# ROLLE: REVIEW — BaseHarbor Demo PR #183

Review date: 2026-11-27 04:36 UTC  
Reviewer lane: `w255-0428-251-demo170codex`  
Card: 0428-284  
Reviewed head: `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`  
PR base: `58ac70679efe5f7e95bd47d602841704fb9ffa67`

## PLAN

1. Inspect the exact PR head, changed blobs, commit metadata, and Hosted-run state without modifying the product repository.
2. Record the independent review verdict and any forward correction recipe in this Akte.
3. Publish this evidence-only Akte through the planning repository's authorized publication path.

## Identity admission

Card frontmatter owner, read from planning `origin/main` at base `6d4e82c82`: `owner: w374-0428-284-demo183fix`.

This review-evidence commit uses the executing reviewer lane identity, `w255-0428-251-demo170codex`, rather than another lane's identity. Git user name: `w255-0428-251-demo170codex`. Git user email: `w255-0428-251-demo170codex@baseharbor.local`. Literal invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-284): demo PR 183 exact-head findings'`. Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## Verdict

CHANGES. The implementation corrections are present, and the change remains limited to `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. The deterministic final-drain regression does not place the digest in the final-drain tail, so its exactly-once assertion can pass without exercising the double-append defect.

## Findings

1. Pass: `tests/guided/drive.py:411` advances `bytes_read` for each final-drain chunk. Lines 434–438 flush and `fsync` the log before reconciling it. The reconciliation receives the advanced byte count, so bytes already captured by the drain are excluded from the reread append.

2. CHANGES: `tests/guided/test_consent_capture.py:749` sets `pad = 4096 - len(digest_line) + 1`. For the current 134-byte line, this yields a 3963-byte pad; the digest occupies offsets 3995–4058 and the complete 4097-byte blob leaves only its last byte beyond offset 4096. Thus the digest is wholly before the claimed boundary, despite the comment at lines 743–745. The assertion at lines 774–778 can pass while the final-drain digest is not duplicated, so this does not prove the previously identified double-append fails.

   Recipe: place the full digest after the first 4096 bytes (for example, use a padding prefix of at least 4096 bytes, then assert the digest start offset is at or beyond 4096). Make the test deterministically drive the real `run_tty` final-drain branch before that digest tail is read; retain the exactly-once assertion and add an assertion or controlled schedule proving that the tail was consumed by that branch. The regression must fail if final-drain `bytes_read += len(chunk)` is removed.

3. Pass: `run_capture` calls `drive.run_tty(..., capture=True)` at `tests/guided/test_consent_capture.py:108–120`; `test_25` uses that helper at lines 766–768, so it exercises the real `run_tty` path. Tests 22 and 23 are unchanged between `1dfead1998254e124ff54a7678ab8ed388e3bee0` and the reviewed head; the exact comparison changes only the `drive.py` final-drain correction and test 25. The PR file list contains only the two `tests/guided/*` paths; no product authentication or consent implementation is changed.

4. Pass: all four commits have matching author and committer names/emails, each using the executing lane identity for that commit:

   - `83c80c917858e719118bd21e0183b4516959ac53`: author and committer `w366-0428-284-democonsent <w366-0428-284-democonsent@baseharbor.local>`.
   - `1dfead1998254e124ff54a7678ab8ed388e3bee0`: author and committer `w373-0428-284-demo183fix <w373-0428-284-demo183fix@baseharbor.local>`.
   - `442d8bb1c7b7d32bf8a54d2e266388f7012edaba`: author and committer `w374-0428-284-demo183fix <w374-0428-284-demo183fix@baseharbor.local>`.
   - `00b87bfc36cb3070bb7046f40d0df798f59ff4b1`: author and committer `w374-0428-284-demo183fix <w374-0428-284-demo183fix@baseharbor.local>`.

## Hosted evidence state

The exact-head Actions query returned push run `45940231146`, completed failure for `.github/workflows/pr-config-matrix.yml`; `gh pr checks 183` reported no checks. No successful exact-head Hosted run was found. This does not change the content verdict; green exact-head Hosted evidence remains required before merge.

## Review boundary

This is a read-only review record. No product files were edited, no tests were run locally, and no merge or product push was performed.
