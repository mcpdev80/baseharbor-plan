# Final re-review and merge receipt — BaseHarbor Demo PR #176

Date: 2026-11-25
Card: 0428-284 / `t-20261125-0428-284-1812-postretry-gate-failure`
PR: https://github.com/mcpdev80/baseharbor-demo/pull/176
Reviewed head: `6371ca5542c4782ac458c196aef87511ea7f9999`
Base before merge: Demo `main` `df4867c7540774eba8b8811cb64946b4adc0c8ab`
Current card owner: `w198-0428-284-demo-parser`
HEAD `.commit.author.name`: `w198-0428-284-demo-parser` (exact match)
PR run: [45648782687](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45648782687), `pull_request`, exact-head SUCCESS.
Disposition: **ACCEPTED and MERGED.**

## Re-review findings

The earlier CHANGES finding on `d6a95f5b` is resolved. Relative to that reviewed head, the fix adds only `tests/fixture-consent.py` and `tests/test_fixture_consent.py`. The parser requires the candidate-consent marker, anchors the documented digest prompt, checks that repeated prompt digests agree, and keeps the JSON consent branch intact. The new unrelated-error and near-miss regressions are present; the earlier nested-boundary retry, exactly-once, and no-digest fail-closed positives remain.

Run 45648782687 executed `Guided consent · production-path regressions`: the fixture suite passed 29 tests and guided suite passed 26 tests. Those logs include the three original positive cases and the two new fail-closed tests. A second distinct PR run is not required for this card: this one exact-head pull-request run executed both affected suites; the #175 two-run instruction was mission-specific.

The full PR diff is confined to Demo scripts/tests and test fixtures. It changes no product authentication or consent semantics and no workflow files. Previously reviewed test-only operator-login fixture blobs match the hosted-tested #174 versions. The only additive source commit since the earlier review is `6371ca5`, authored by the current owner. Earlier Flash-authored `86afbb`/`9dc5f7` commits are historical and unchanged; no history rewrite occurred.

## Merge receipt

GitHub API now reports PR #176 `merged: true`, `merged_at: 2026-11-25T15:59:12Z`, and `merge_commit_sha: 6381a67f58e067358ef54dce7f4cff2106f8a623`. Demo `main` points to that SHA.

The first expected-head squash request returned HTTP 502. On refresh, the PR still reported open/unmerged, while `main` had advanced to `f10216f717810111502cd160fd6ab104f9fd7d35`, a same-tree squash commit of this PR. After verifying that state, the expected-head squash command was retried; GitHub then reported the PR merged with final receipt `6381a67f58e067358ef54dce7f4cff2106f8a623`. The final receipt commit has the same tree as `f10216f7` and its parent is `f10216f7`; no source-tree delta was introduced by the duplicate-tree receipt.

PR review/acceptance comment: https://github.com/mcpdev80/baseharbor-demo/pull/176#issuecomment-7167453934
