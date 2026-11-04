# Review 128c — demo guided consent

- Role: CODEX-REVIEW (no merge)
- PR: [#128](https://github.com/mcpdev80/baseharbor-demo/pull/128)
- Reviewed head: `e453e2a19a30ba9ffec787e6ffbf981c665cc225`
- Base: `main` = `cd9176e0129f01270ca85fd6b29acf99404f6dcd`
- Remote: PR OPEN, non-draft, mergeable; remote branch refs match these SHAs. `git diff --check` is clean.
- Test discovery: `ARTIFACT_DIR=/tmp/review-128c-e4532a-artifacts-2026-11-04a PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/guided -p test_consent_capture.py -v` — 7 tests passed.

## Technical findings

The test file passes but its `complete_rules()` and `TWO_PROMPT_RULES` are not production `drive.up_rules`. The production rule set includes mandatory `READY` (`drive.py`, `up_rules`). The capture validator checks every non-optional rule before recognizing a non-zero consent abort. A real documented first-run consent abort does not reach READY, so it is rejected as missing `READY\s*$` before the caller can read the hash or perform the intended second `up`. Independent PTY probes using fresh copies of production `up_rules` confirmed:

- (a) rc=0 without READY: ABORT (missing mandatory READY).
- (b) missing required interaction: ABORT (mandatory prompt coverage).
- (c) nonzero + hash + foreign error, without READY: ABORT (missing mandatory READY; no return to caller).
- (d) nonzero + hash + incomplete interactions: ABORT (missing mandatory READY).
- Positive documented consent abort + interactions, without READY: ABORT (missing mandatory READY); second `up` is unreachable.
- Regular success with READY: the permanent test passes; the production rule set accepts the READY completion path.

The positive test does two independent `run_capture` calls and checks the text/hash itself. It never calls the production guided-flow caller or its feature probe/second-run branch. Cases (a), (c) and (d) also use custom rule sets that omit mandatory production READY. Thus the passing suite does not establish those production paths. The candidate’s core pin is `488a39e6f67ecbc733dc6acdee2443b36db4717c`; comparison with BaseHarbor `develop` at `f8ef4255592fcb1502fa54187c0965b9d00f118c` reports `diverged` (ahead 6, behind 18; merge base `2cadfcee8161ec087b6f50d80fb41428d414f9df`), so the pin is neither an ancestor nor a descendant of that develop head.

## Verdict: REJECT

### REZEPT

- File: `baseharbor-demo/tests/guided/drive.py` — change capture validation so a nonzero exit is allowed only after all required interaction prompts (excluding the completion marker) were answered and the exact documented candidate-consent abort was observed; keep READY mandatory for rc=0.
- File: `baseharbor-demo/tests/guided/test_consent_capture.py` — exercise the real `up_rules` and production decision path, including a documented abort followed by the actual second-run decision, and the four required counter-probes. Assert that foreign errors never reach a second run.
- Pin: update `baseharbor-demo/baseharbor-core.ref` to a commit on the required `develop` ancestry, or document and satisfy the task contract’s intended pin relation.
- Required recheck: named unittest discovery for this file, plus the focused guided acceptance test required by the task note; verify each counter-probe and both success paths at the corrected candidate SHA.
- Stop criterion: reject again if a foreign error can invoke a second `up`, an ordinary rc=0 path can pass without READY, or the documented consent abort cannot reach the second run and READY.

No files in the candidate repository were changed. Local untracked files observed in its worktree were left untouched.
