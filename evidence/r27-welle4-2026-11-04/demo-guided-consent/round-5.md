# t-20261104-r27-demo-guided-consent — guided consent correction round 5 (w109-demo-r5)

- Task: t-20261104-r27-demo-guided-consent (baseharbor-demo)
- Worker: w109-demo-r5 (assigned worker; card claimed by prior worker, continued under same branch/PR)
- Coord: f49a3303
- Date: 2026-11-04
- Authority: mission coordinator/missions/w109-demo-r5.txt; review-128d.md (CODEX Luna, REJECT); baseharbor-demo/AGENTS.md (planning = baseharbor-plan), product/review/CI in the demo repo.
- Write scope: tests/guided/drive.py, tests/guided/test_consent_capture.py, tests/guided/run.sh only. baseharbor-core.ref NOT changed (pin was already current/serveable). No Core files. No new gate semantics.

## PLAN

- Read mission w109-demo-r5 + review-128d + both recipes + demo AGENTS.md + CI workflow + drive.py + tests/guided/run.sh
- BASE: verify demo main + baseharbor-core.ref are current (develop bb9bc0ef or Core-tag). core.ref = 488a39e6, commits API HTTP 200 (serveable), commit "fix(runtime): thread --confirm-candidate to apply path on 'baha up'". Demo main = cd9176e. Head of branch = 061be773, ls-remote == head.
- R1 red at head: reproduce the review-128d REZEPT #1 bypass directly against the production path.
- R1 fix drive.py run_guided_consent_flow: a non-zero exit is the documented between-state ONLY when the ENTIRE transcript carries the hash + documented prompt AND no foreign error/failure signature. Fail closed otherwise.
- R1 regression: permanent test_09 (hash + documented prompt + foreign panic => abort, no second up) + control test_10 (documented abort, no foreign => second_up stays green) + helper-coverage test_11. Keep the four known counter-probes unchanged.
- R2 discovery fix: wire unittest discover on tests/guided into the acceptance guided gate before the runtime-dependent happy path.
- Local verification: py_compile + bash -n + unittest discover green with named tests + direct probe.
- Commit to branch; push; ls-remote == head; watch PR #128 CI to terminal.
- Write evidence round-5.md; END to f49a3303.

## Repo-rule compliance

- Write scope honored exactly: only tests/guided/drive.py, tests/guided/test_consent_capture.py, tests/guided/run.sh changed. baseharbor-core.ref left at 488a39e6 (already current/serveable; a change was not required, and the mission forbids Core changes in this repo/lane). No Core files touched.
- Consent gate NOT weakened: fail-closed everywhere. Only the documented candidate-consent abort (hash + documented prompt + NO foreign signature) proceeds; a foreign error/failure signature in a non-zero transcript aborts with no second up. Normal rc=0 + READY path unchanged. No env-var auto-confirm. No --help grep probe.
- R2 wiring is additive: the guided gate now runs the fail-closed suite before the runtime-dependent happy path; the happy-path assertions are untouched. Bounded, writable ARTIFACT_DIR set for the harness (drive.run_tty logs there).
- CI authority: demo CI is push-triggered to release branches only (work/v0.4.24/25/26-ecosystem-release, v0424-targeted.yml), NOT main/feature branches — so PR #128 (feature branch w85-demo-guided-consent) reports "no checks" by configuration. This is the configured gate, not a defect. No hosted gate exists for this feature branch; the local py_compile + 11/11 named-test discovery run is the verification for this correction round.

## R1 — fail-closed foreign-error (red -> green)

- RED reproduced at head 061be773 against the PRODUCTION path run_guided_consent_flow: a non-zero transcript carrying a VALID 64-hex confirm-hash + the documented "Re-run with --confirm-candidate" prompt + a FOREIGN panic line ("core: panic: unknown error 0xdeadbeef") classified as outcome="second_up" and launched a second "up --confirm-candidate <digest>". The head code only checked that a hash exists and the documented prompt appears SOMEWHERE in the transcript; foreign error text was never rejected. This matches review-128d's finding that the permanent tests omit the hash + documented prompt together and therefore never catch the bypass.
- Root cause location: drive.py run_guided_consent_flow, the `if first_rc not in (0,):` branch (line 458) — the non-zero branch accepted a documented abort on mere substring co-occurrence of hash + prompt, ignoring any foreign signature. The docstring explicitly promises "Every non-zero exit other than the documented abort aborts the whole flow (fail-closed) — never a second run", so the head violated its own contract.
- Fix: introduced production helper find_foreign_error_signature(text) scanning for the Core's failure-only words (panic, Traceback, Error:, error, exception, failed, Fatal, fatal, unhandled, refused, denied). The documented abort prompt itself contains none of these words. run_guided_consent_flow now classifies the non-zero exit as the documented between-state ONLY when confirm_hash is present AND CANDIDATE_ABORT_ERROR is present AND foreign_signature is None; otherwise it aborts with no second up.
- Green: python3 -m unittest discover -s tests/guided -p "test_*.py" -v — 11 tests, all OK (25.4 s). Direct probe re-run after the fix: Scenario A (hash+doc+foreign) => outcome="abort", second_rc=None, second_argv=None; Scenario B (hash+doc, no foreign) => outcome="second_up", second_rc=0. Red is green; the documented positive path is preserved.
- New permanent regressions added to test_consent_capture.py:
  - test_09_hash_and_documented_prompt_with_foreign_error_aborts — the exact review-128d REZEPT #1 bypass: asserts outcome="abort", second_rc/second_argv None, foreign_error_second_up False.
  - test_10_documented_abort_without_foreign_signature_reaches_second_up — control that over-tightening the fail-closed check did not kill the genuine documented abort; asserts "second_up" still reachable. Regression guard against the R1 fix.
  - test_11_foreign_error_signature_detected_by_production_helper — asserts find_foreign_error_signature flags "panic"/"Traceback" and returns None for the documented abort prompt and for "READY".
- The four known counter-probes (test_01..test_05) and both documented positive paths (test_06, test_07) are kept UNCHANGED.

## R2 — discovery: the permanent test was never executed (found + fixed)

- Root cause: nothing in the demo acceptance flow invoked the fail-closed suite. scripts/acceptance.sh delegates the "guided" gate (tests/gates.json) to tests/guided/run.sh. tests/guided/run.sh invoked only drive.py and new_edit.py — never the production-path suite test_consent_capture.py, and never the new_edit_process_test.py / new_edit_helpers_test.py unittest modules. The repository workflow v0424-targeted.yml only runs `python3 -m unittest discover -s tests -p test_fixture_consent.py` (plus a py_compile of drive.py), so no unittest discovery ever reached tests/guided.
- Fix: tests/guided/run.sh now runs `python3 -m unittest discover -s tests/guided -p "test_*.py" -v` into a bounded ARTIFACT_DIR (guided-consent-discovery.txt) right after sourcing tests/lib.sh and before the runtime-dependent happy path, records a results.tsv PASS line, and fails the gate on non-zero. These regressions need no BaseHarbor runtime (they drive fake cores / pure helper imports), so placing them first is correct and does not disturb the happy path.
- Evidence of wiring: `bash -n tests/guided/run.sh` clean; py_compile of drive.py + test_consent_capture.py clean; the discover run completes 11/11 with named test cases (see R1 green).

## END

- lane: w109-demo-r5 | verdict: REJECT corrected — R1 fail-closed foreign-error now aborts (no second up, red->green), R2 discovery wired into the guided gate.
- R1: head 061be773 still PASSED the unit discovery (8/8) because the permanent tests never included the hash+doc+foreign combination; direct production-path probe reproduced the second_up bypass. Fixed by rejecting any foreign error/failure signature in a non-zero transcript; added permanent test_09 + control test_10 + helper test_11; keep four known counter-probes + both documented positive paths unchanged.
- R2: found the discovery gap (run.sh never invoked unittest discover on tests/guided; CI workflow only discovers test_fixture_consent.py). Wired discovery into guided/run.sh before the happy path with a bounded artifact dir + results.tsv recording.
- STOP-KRITERIUM satisfied: no second up on any foreign-error/non-abort non-zero transcript; rc=0 without READY still fails; documented abort without foreign signature still reaches second_up; 11/11 named discovery green.

## PR + status

- PR #128 (open, not draft, READY): https://github.com/mcpdev80/baseharbor-demo/pull/128
- Base: main (cd9176e0129f01270ca85fd6b29acf99404f6dcd)
- Head: w85-demo-guided-consent = 5b1f6e92cbb352551dbb3d928edb2b142ca90c8d
- ls-remote == head: verified (5b1f6e92cbb352551dbb3d928edb2b142ca90c8d)
- Files: tests/guided/drive.py, tests/guided/test_consent_capture.py, tests/guided/run.sh. baseharbor-core.ref unchanged (pin 488a39e6, serveable). No Core files.
- Commit/PR status: committed to branch, pushed, PR OPEN/READY/draft=false.
- CI: demo CI is push-triggered to release branches only (work/v0.4.24/25/26-ecosystem-release, v0424-targeted.yml), NOT main/feature branches. PR #128 (feature branch) reports "no checks" by configuration — the configured gate, not a defect. No hosted gate exists for this feature branch.
- Local verification: py_compile drive.py + test_consent_capture.py PASS; `bash -n tests/guided/run.sh` PASS; `python3 -m unittest discover -s tests/guided -p test_*.py -v` — 11/11 OK with named cases; direct production-path probe R1 red->green confirmed.
- core.ref BASE note: 488a39e6 is serveable (commits API HTTP 200); demo main = cd9176e. No bump required this round (mission scope forbids Core changes; the pin was already current).
