# w182-codex-1844-review — PR #1844, card 0428-320

## PLAN

1. Refresh PR #1844 head/base/state and current `develop` tip.
2. Review the exact `STYLE_GUIDE`-only diff and verify owner identity.
3. Verify both full-green exact-head runs and active strict required-check policy.
4. Publish CHANGES review evidence and PR comment; await base refresh and re-review.

## Candidate and scope

Planning repository remote witness: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).

PR #1844 remains OPEN and non-draft at head `2c19c945786da8dd1065f96bfef33bf8fbbdf722`, based on develop `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`. Its current `mergeable_state` is `behind`. After PR #1843 merged normally as `384d857b556908e4377c6f26e81127c7d48fb838`, a fresh `git ls-remote` reports `develop` at `384d857b556908e4377c6f26e81127c7d48fb838`; the #1844 candidate branch and PR head still point to `2c19c945786da8dd1065f96bfef33bf8fbbdf722`.

Final PR diff is one file only: `docs/STYLE_GUIDE.md` (2 additions, 2 deletions). It states EN/DE parity is measured on mkdocs nav pages and that maintainer-facing `docs/internal/` audits are English-only, outside nav parity, with German pages linking to the canonical English audit. No code, `.github/**`, or consent surface changed. Candidate commit author is `w183-0428-320-0428-audits-enonly`, matching owner in `tasks/t-20261125-hunt44-audits-en-only-declaration.md`. Content and scope review pass for this exact head.

## Exact-head hosted CI

Direct GitHub API witnesses for head `2c19c945786da8dd1065f96bfef33bf8fbbdf722`:

- Run `45614592648`: completed/success; `PR Selected Checks` success, documentation audit, strict EN/DE mkdocs, and Pages candidate jobs successful.
- Run `45618011559`: completed/success; `PR Selected Checks` job `139218984612` success; documentation audit `139218534018`, strict EN `139218533605`, strict DE `139218533497`, and Pages candidate `139218533869` successful.
- Both are distinct run IDs on the same exact head. Cancelled run `45618000306` is excluded. The successful required check on this head is from GitHub Actions app ID 15368.

## Verdict: CHANGES — merge blocked by stale base

The exact-head scope and content review pass. The candidate cannot merge now because `develop` advanced after the runs and PR #1844 is `behind`. Active ruleset `25223521` requires `PR Selected Checks` from app 15368 with `strict_required_status_checks_policy: true`. The green runs are valid for the old base/head pair; they do not qualify the candidate after an integration refresh. No merge, rebase, push, rerun, or ruleset bypass was performed by this reviewer.

Actionable remedy: the owning worker should integrate current `origin/develop` into the existing PR branch with the normal merge transport, push the updated candidate, then produce two distinct full-green hosted runs on that new exact head (including successful `PR Selected Checks` and docs jobs). Return the final SHA for a fresh independent review. Stop condition: do not merge the old head or reuse these runs for a new head.

PR comment posted: https://github.com/mcpdev80/baseharbor/pull/1844#issuecomment-7163210524.
evidence/board-2026-11-27/w182-codex-1844-review.md
