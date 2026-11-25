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
