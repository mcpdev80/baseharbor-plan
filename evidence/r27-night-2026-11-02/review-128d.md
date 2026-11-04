# Review 128d — demo guided consent (round 4)

- Role: CODEX-REVIEW (no merge)
- PR: [#128](https://github.com/mcpdev80/baseharbor-demo/pull/128)
- Reviewed head: `061be773ddb7168aa2760afc9bb8cba18421fd93`
- Base `main`: `cd9176e0129f01270ca85fd6b29acf99404f6dcd`; remote branch refs match. `git diff --check` is clean.
- Candidate diff: exactly the requested three files (`tests/guided/drive.py`, `tests/guided/test_consent_capture.py`, `baseharbor-core.ref`). Review was read-only; preexisting untracked `.tools/` and `tests/guided/__pycache__/` were preserved.

## Technical findings

The regression imports the real module and uses `drive.up_rules` and `drive.run_guided_consent_flow`. The specified adversarial counter-probe fails: a nonzero first run containing both a valid 64-character confirm hash and the documented `Re-run with --confirm-candidate` text, followed by a foreign panic/error, is classified as `second_up`. I ran the production function against the candidate with `rc=3`; it invoked the second `up --confirm-candidate <hash>` and the fake core returned READY. In `run_guided_consent_flow`, the nonzero case only checks that the hash exists and `CANDIDATE_ABORT_ERROR` occurs somewhere in the transcript; it does not reject foreign error text. The permanent foreign-error tests omit the hash and documented prompt together, so they cannot catch this case. This violates the explicit fail-closed invariant.

The four other requested counter cases are represented in tests: rc=0 without READY, missing required completion, nonzero without hash, and nonzero hash with incomplete interactions. The documented positive consent->second-up->READY and regular READY paths are represented. However the tests’ interaction claim should be read narrowly: the sole non-optional `up_rules` entry is the READY completion rule; the ordinary interaction prompts are optional.

`ARTIFACT_DIR=/tmp/review-128d-discovery PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/guided -p 'test_*.py' -v` — 8 tests passed (17.559 s). `scripts/acceptance.sh` delegates the guided gate to `tests/guided/run.sh`; the repository workflow’s unittest command only discovers `tests/test_fixture_consent.py`, and its py_compile list compiles `drive.py` but not this new test. No normal top-level test-discovery reference to `test_consent_capture.py` was found. Thus the suite is discoverable with the documented explicit guided command, but it is not included in the workflow’s ordinary unittest command. The test module and drive module compile as imported by the passing discovery run.

## Verdict: REJECT

### REZEPT

- File: `baseharbor-demo/tests/guided/drive.py`, in `run_guided_consent_flow`: before the second run, classify the entire nonzero transcript as the documented candidate-consent abort, and fail closed if any foreign error/failure signature is present. Do not accept mere substring co-occurrence of a hash and consent hint. Preserve the regular rc=0 + READY requirement.
- File: `baseharbor-demo/tests/guided/test_consent_capture.py`: add a permanent production-path regression containing a valid hash, the exact documented consent prompt, and foreign error text in the same nonzero transcript; assert abort and no second invocation. Keep the existing positive consent and clean READY cases.
- Test wiring: include `python3 -m unittest discover -s tests/guided -p 'test_*.py'` in the normal demo guided gate (or the repository’s normal test workflow), and retain a bounded artifact directory for the run.
- Required recheck: rerun all four counter-probes, both positive paths, named guided discovery, and the normal demo test entry point at the corrected SHA. Stop/reject if the combined hash+foreign-error transcript can cause a second `up`, or if rc=0 without READY passes.

END_DONE codex-r128d: verdict=REJECT open=hash+foreign-error bypass; normal test workflow omits regression | The production flow launches the second up when a valid hash and consent hint coexist with a foreign error.
