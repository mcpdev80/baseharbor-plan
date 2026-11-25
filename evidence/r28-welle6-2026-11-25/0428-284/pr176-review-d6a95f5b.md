# Independent review — BaseHarbor Demo PR #176

Date: 2026-11-25
Card: 0428-284 / `t-20261125-0428-284-1812-postretry-gate-failure`
PR: https://github.com/mcpdev80/baseharbor-demo/pull/176
Reviewed exact head: `d6a95f5bba31e77670eb791ad47cec34cf84217c`
PR base: Demo `main` at `df4867c7540774eba8b8811cb64946b4adc0c8ab`
Current card owner: `w198-0428-284-demo-parser`
Candidate commit author (`.commit.author.name`): `w198-0428-284-demo-parser` — exact match.
Verdict: **CHANGES; not merged.**

## Scope review

The PR changes nine Demo paths, all under `scripts/` or `tests/`: acceptance/report diagnostics, fixture-consent, shell test helpers/runners, the policy login test fixture and its README, and fixture tests. No product application/authentication implementation, consent contract, or `.github` workflow changes appear in the diff. The X.509 operator-login changes are test-only. `tests/policy/run.sh` blob `93e2b5578fabba4a775334fd3117bde214c6095b` and `tests/policy/operator-test-certificate.sh` blob `cf16216cfbd9ab9741430de5ee6c4f3189f9bc9d` are identical to Demo commit `b1e1a77bd0e2b0af7d9bf3cf9178be68cad0119f`; that earlier head has successful hosted runs [45455975242](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45455975242) and [45456155783](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45456155783). No w177 history was rewritten; the current candidate commit is additive and carries the w198 author identity.

The parser correctly handles the documented lowercase 64-hex digest form, and the JSON path still requires the exact version/code/refusal and next-step message. The plain-text path is weaker than that JSON path, however (see finding below). Therefore I cannot conclude that fixture enforcement is fully fail-closed yet.

## Exact-head hosted evidence

Run [45646543061](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45646543061) is the only `pull_request` run found for this head. It completed SUCCESS on exact head `d6a95f5b...`; job 139318953135, `Guided consent · production-path regressions`, executed `python3 -m unittest discover -s tests -p test_fixture_consent.py -v` and the guided test discovery. The exact run log shows all three new regressions passing:

- `test_fixture_retries_real_plain_text_refusal_with_extracted_digest`
- `test_fixture_real_plain_text_refusal_carries_digest_exactly_once`
- `test_fixture_real_plain_text_refusal_still_fails_closed_when_no_digest`

The job reports 27 fixture tests and 26 guided tests, both `OK`. The Owner's commission witnesses these three regressions were run red-first against the real plain-text shape before the implementation. No separate red-run ID was supplied; hosted acceptance evidence is the exact-head green run above.

## Finding — plain-text parser can accept unrelated/prefix text

At `tests/fixture-consent.py:74-80`, `candidate_digest_from_text` uses unanchored `re.search` for the confirmation sentence. `main()` calls it for any non-JSON command failure at lines 211-221. Unlike `candidate_confirmation()` at lines 33-54, the plain-text branch does not require the candidate-consent refusal marker. For example, stderr containing an unrelated error followed by `Re-run with --confirm-candidate <64hex> to acknowledge this exact submission.` currently yields a digest; `main()` then adds the consent flag and retries. The new no-digest regression does not exercise this prompt-like near-miss.

Required fix: accept the prompt only as a complete canonical line (allow the actual indentation/`Next:` wrapper) and require the documented candidate-consent refusal marker in the same stderr; if the real output repeats prompt lines, require all parsed digests to agree. Add negative regressions for an unrelated error plus a prompt-like sentence and for prefixed/suffixed near-matches; assert the fixture returns failure without retrying or adding `--confirm-candidate`. Keep both nested-boundary and exactly-once positive cases green.

## Distinct-run decision

A second identical run is **not required** for this card's current PR acceptance contract. The exact `pull_request` run executed the affected fixture suite and guided regressions; the two-run #175 precedent was explicitly mission-specific. Repeating the same run would add no new coverage. The downstream Docker/Podman Light gate qualification remains a separate #1812 requirement after the authorized pin hop.

## GitHub record

CHANGES verdict and fix recipe posted to PR comment: https://github.com/mcpdev80/baseharbor-demo/pull/176#issuecomment-7167259351

No merge was performed because the plain-text fixture can acknowledge a candidate from unbound error text. The reviewer is using the PR author's GitHub account, so the formal request-changes review API is unavailable; the comment is the posted verdict.
