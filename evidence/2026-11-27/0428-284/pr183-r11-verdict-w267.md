# PR #183 r11 exact-head review — w267

## PLAN

1. Refresh the Plan and product refs; read W392's r11 evidence and confirm task ownership.
2. Verify PR #183's exact head, base ancestry, changed paths, and hosted run receipt.
3. Compare the exact diff with the outstanding r10 findings and record a SHA-specific independent verdict.
4. Merge and close out 0428-284 only if the exact candidate passes; otherwise record precise correction recipes.
5. Defer the #1881, #1882, and #1884 content-only reviews until #183 passes, as requested.

## Review identity and scope

Canonical lane: w267-0428-284-pridentity.
Task owner fetched from Plan origin/main: `owner: w267-0428-284-pridentity`.
Plan origin/main at review: `3dcd373ecb49a4bfa244c930010c4fdc4cbbfee7`.
No candidate commit was created; no commit invocation or push was performed.

Review role: REVIEW. Candidate: `mcpdev80/baseharbor-demo` PR #183, branch `w366-0428-284-democonsent`, base `develop`.
Exact head: `e3ae7008b938ea58f0f4285da68f121ba60a22c9`.
Fetched base: `58ac70679efe5f7e95bd47d602841704fb9ffa67`.
`git merge-base --is-ancestor 58ac70679efe5f7e95bd47d602841704fb9ffa67 e3ae7008b938ea58f0f4285da68f121ba60a22c9`: passed.
Changed paths: `tests/guided/drive.py`; `tests/guided/test_consent_capture.py`.
`git diff --check`: passed.

W392 r11 source evidence: `/home/marcel/dev/baseharbor-ecosystem/coordinator/evidence-staging/2026-11-27/pr183-r11-w392.md`.
SHA-256: `c833f2e5f37b2c39c6e04a4b0610ebf386e79b355df539f526b53f758ce4d8bb`.

Hosted receipt: run `46045731548`, event `workflow_dispatch`, terminal `completed/success`, exact head `e3ae7008b938ea58f0f4285da68f121ba60a22c9`, branch `w366-0428-284-democonsent`; URL: https://github.com/mcpdev80/baseharbor-demo/actions/runs/46045731548 . This satisfies the r11 card-specific mission qualification. Push run `46045710620` had zero jobs and is not a test receipt. No local tests were run during this review.

## Verdict: CHANGES — do not merge

Finding 1 — production reachability of the reconciliation suffix is not demonstrated. In `tests/guided/drive.py:283-298`, the helper's contract says the log may contain bytes not appended to `capture_buffer`; `:286-290` says both the select loop and final-drain loop write and capture the same read chunks, while `:482-483` advances `bytes_read` for the same final-drain chunk and `:509-529` reconciles only after those reads. The r11 explanation at `:300-310` acknowledges that the main path is empty-by-construction and relies on a separately fabricated suffix. `tests/guided/test_consent_capture.py:1082-1129` writes that suffix directly to a temporary file and proves the helper's append-once/idempotent behavior, but never drives `run_tty` through a state that produces a non-empty reconciliation suffix. Thus the helper invariant is tested, but the claimed production defect/fix is not connected to an observed production call path.

Correction recipe: either document this strictly as a defensive helper contract and remove claims that current Core/PTY behavior produces a log-only tail, or introduce a deterministic test seam in `run_tty` that causes the authoritative log to contain a byte suffix absent from the captured prefix, then assert the real call path reconciles it exactly once and idempotently. Preserve consent/auth behavior.

Finding 2 — the final-drain hook observation is not asserted. In `tests/guided/test_consent_capture.py` the test installs `drive._run_tty_final_drain_hook` and appends observed chunks to `drained["final_drain_chunks"]` (around `:933-936`). The test then asserts transcript digest count and log equivalence, but never reads/asserts that list. The supposed hook-deactivation negative control described around `:990-1023` is not implemented: those transcript/log assertions do not depend on the hook, and the helper-only test at `:1043-1077` is independent of the hook. The test therefore passes even if the hook is never called, contrary to the r11 claim that hook observation and its negative control are asserted.

Correction recipe: assert a specific sentinel or digest-bearing chunk was recorded in `drained["final_drain_chunks"]` on the invocation under test, and add a real negative control proving a wrong/deactivated hook causes that assertion to fail. If the current single-PTY behavior cannot put the relevant digest in the final-drain branch, make the test observe a deterministic final-drain sentinel and keep the digest/capture invariant separate; do not describe transcript equality as hook evidence.

The exact-head hosted run is green, but the two independent static findings remain. PR #183 remains open; card 0428-284 is not closed out. The requested #1881, #1882, and #1884 reviews are deferred until the #183 corrections pass.

END_BLOCKED w267-0428-284-pridentity: PR #183 r11 exact head e3ae7008b938ea58f0f4285da68f121ba60a22c9 has two CHANGES findings; no merge.

## Final remote witness

`git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/pull/183/head refs/heads/develop` returned:

```text
e3ae7008b938ea58f0f4285da68f121ba60a22c9	refs/pull/183/head
58ac70679efe5f7e95bd47d602841704fb9ffa67	refs/heads/develop
```

Final PR API state: `OPEN`, `isDraft=false`, base `develop`, head `e3ae7008b938ea58f0f4285da68f121ba60a22c9`, merge state `CLEAN`. The successful hosted receipt remains run `46045731548` on that exact head.
