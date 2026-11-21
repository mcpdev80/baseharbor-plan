# Owner exception, commit identity for PR #1596 (card 0428-224) - recorded by coordinator

ROLE: coordinator record, read-only measurement. No product or workflow change.

## Decision

Card `0428-224` requires exactly one identity per candidate. The Owner offered two routes on 2026-11-21 22:2xZ:
a documented Owner exception, or authorized history normalization followed by fresh exact-head CI and review.
The coordinator records the **documented Owner exception** for this candidate only, and gives the reason.

## Witness (measured, not reported)

- `refs/pull/1596/head` = `c27158567c0ebc370fc6c97390a561846305738f`, base `develop` = `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, back=0, ahead=3, merge-commits 0.
- `git log --format='%h %an %cn' refs/heads/develop..refs/pull/1596/head` shows authors `welle2-056`, `mcpdev80`,
  `Marcel Pfingstgräf` with a single committer; the mixed authorship comes from Owner-side hops of this branch, not from
  several lanes writing the same candidate.
- Independent review `evidence/r28-welle4-2026-11-21/org-env-reconciliation/review-1-headc2715856.md`
  (plan commit `Verdict: REQUEST CHANGES`) found **no implementation finding**: the `EnvironmentIdentity.Authoritative`
  input boolean is ignored on the production path, so there is no behavioural exposure, and the Owner withdrew the
  earlier no-production-caller observation as unestablished without task-contract context.
- Exact hosted CI at the same head: run `44945468909`, completed/success, 14 jobs, 0 failures.

## Reason for choosing the exception over normalization

Rebasing three commits for zero content change would trigger another full matrix for this PR (AGENTS 5.4: no
needless CI, no green-reckoning), while the defect the identity rule guards against - an unattributable or
foreign-authored change riding along - is already answered by the reviewer's finding of no implementation issue.

## Scope and expiry of this exception

Applies to candidate `c27158567c0` of PR #1596 only. It is not a change to card `0428-224`: any future candidate of
this card that carries more than one author **and** any content finding, or whose branch is lane-owned rather than
Owner-owned, still requires normalization. Card `0428-056` and card `0428-224` reference this file.
