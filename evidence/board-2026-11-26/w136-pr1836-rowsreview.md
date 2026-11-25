# w136 Codex review queue — 2026-11-26

## PLAN

1. Review #175 exact head, base, card ownership, diff scope, and CI history — complete.
2. Run the demo guided-consent Hosted workflow twice on the exact #175 head and verify execution — complete.
3. Report the #175 verdict and record merge blockers — complete; CHANGES, no ready or merge.
4. Keep #1835 gate batches parked for w157's corrected head; retain void-run classifications — complete.
5. Wait for w162 to hand off the new #1832 hop head, then re-review only after exact-head CI evidence is complete — pending.

## #175 review — CHANGES

PR: https://github.com/mcpdev80/baseharbor-demo/pull/175
Head: `9dc5f7afbb19c3f9ece6d15edd5d5320bf602ea0`
Base: `b41127723e523134a1c14ee3c36cf133237162ce`

The diff is limited to `tests/fixture-consent.py` and `tests/test_fixture_consent.py`. There is no product consent/auth change. The fixture recognizes the `v1` / `internal_error` shape and the documented immutability phrases, but checks them with substring membership rather than exact `error.message` equality. The evidence contract describes an exact-message match. Fix-forward recipe: compare `error.message` to the full documented message and add negative tests for extra prefix/suffix text, then rerun Hosted CI on the resulting exact head.

The required identity pre-check returned `.commit.author.name = Flash`; the card lane in the authoritative w152 evidence is `w152-0428-249-demo-reconsent-fix`. These strings are not equal. Owner policy makes this head ineligible to merge until the admission rail is fixed forward. Recipe: add a new identity-only commit with author name/email set to the owning lane, preserve history, do not rewrite, and rerun both same-head Hosted qualifications after the final commit.

The PR was a draft targeting `develop`; the active guided-consent workflow listens to PRs targeting `main`, so no PR check runs existed on the draft head. The same workflow's `workflow_dispatch` was run twice on the exact branch/head. Both runs executed the `Run local fixture and real guided decision-path regressions` step and ended success:

- Run [45590658205](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45590658205) — `workflow_dispatch`, head `9dc5f7af...`, terminal success, test step success.
- Run [45590834599](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45590834599) — `workflow_dispatch`, same head, terminal success, test step success.

Verdict: **CHANGES**. Do not mark ready or merge until both the author-lane identity and exact-message finding are corrected. No code was changed by the reviewer.

## #1835 runtime gate disposition

Parked for w157's corrected exact head. Run 45571397690 remains void (zero jobs); run 45572854473 remains void (two Go shards cut, no selected native runtime gate executed). Both count as neither green nor failure.

## #1832 next review

Wait for w162's handoff of the new hop head. The prior `cee9ff8a` single green is history only; the final head needs two full same-head green runs and an identity check before the same-session review resumes.

## #175 re-review — head 49328fbc (2026-11-27)

PR: https://github.com/mcpdev80/baseharbor-demo/pull/175
Head: `49328fbc8047f4997545dcb1ba9a3e68d1e42bed`
Base: `develop` @ `b41127723e523134a1c14ee3c36cf133237162ce`

Ownership was transferred for card 0428-249 to `w170-0428-249-demo-pr175-fixup` in the coordinator mission and w170 evidence. `gh api repos/mcpdev80/baseharbor-demo/commits/49328fbc... --jq '.commit.author.name'` returned `w170-0428-249-demo-pr175-fixup`, an exact match. PR head is unchanged; it remains a draft and mergeable/clean. Demo main is `df4867c7540774eba8b8811cb64946b4adc0c8ab`, distinct from base develop, so the owner-approved workflow-dispatch qualification path applies.

Both exact-head qualification runs passed and executed `Run local fixture and real guided decision-path regressions`:

- [45593701391](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45593701391) — terminal success, head `49328fbc...`, test step success.
- [45593726801](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45593726801) — terminal success, same head, test step success.

Scope remains exactly two files, `tests/fixture-consent.py` and `tests/test_fixture_consent.py`; the identity fixup commit changes no tree content. No product consent/auth delta was found.

**Remaining review finding:** `tests/fixture-consent.py:75-76` checks whether two phrases occur anywhere in `error.message`; it does not require the full documented immutability message. A prefix, suffix, or inserted text can therefore still be accepted as a successful no-op when the contract is `v1` and code is `internal_error`. This contradicts the helper's “only the exact documented immutability message” statement at lines 68-69 and the test's `accepts_only_documented_message` contract at `tests/test_fixture_consent.py:406` (the current negative cases at lines 409-416 do not cover near-matches).

Fix-forward recipe: compare the complete `error.message` to the documented full string; add negative cases with extra prefix, suffix, and inserted text; then run the hosted guided-consent workflow twice on the resulting exact head. Do not rewrite history.

Verdict: **CHANGES; no ready transition and no merge.** The head fails the exact-message acceptance requirement despite correct identity, test-only scope, and two green runs. No product code was changed by the reviewer.

## #175 re-review and merge witness — final head 1a3c055c

The exact-message finding from the previous review is resolved on final PR head `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`. `tests/fixture-consent.py` now requires exact equality with the full documented immutability message, and `tests/test_fixture_consent.py` rejects prefix, suffix, and inserted-text near-misses. The diff remains limited to these two test files; no product consent/auth change. Exact identity check: author name `w170-0428-249-demo-pr175-fixup` equals the transferred card owner lane.

Two terminal same-head Hosted runs executed `Run local fixture and real guided decision-path regressions` and succeeded: [45598194194](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45598194194) and [45598209141](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45598209141). PR base `develop` was current at `b41127723e523134a1c14ee3c36cf133237162ce`; demo `main` remained at `df4867c7540774eba8b8811cb64946b4adc0c8ab`, so the documented workflow-dispatch qualification path applied.

PR #175 was marked ready and merged with the normal merge method using expected head `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`.

- Merge commit: `486c48be56f996fe976e0881a63e64bb7de92eb2`
- Current demo `develop` tip: `486c48be56f996fe976e0881a63e64bb7de92eb2`
- GitHub merge witness: https://github.com/mcpdev80/baseharbor-demo/pull/175#issuecomment-7160252828

Review verdict: **ACCEPTED**. The merge is ready for the coordinator-owned demo pin bump and #1812 requalification.
