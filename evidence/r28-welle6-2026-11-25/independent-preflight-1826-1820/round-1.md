# Independent preflight for #1826 and #1820 (0428-279 / 0428-271)

READ-ONLY pre-CODEX preflight. No product writes, no CI, no reruns. Two INDEPENDENT candidates.

## Provenance
- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified via `git -C baseharbor-plan remote -v`)
- Product remote: `https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 remote; NOT the quarantined workers/checkout)
- develop HEAD (remote `git ls-remote`): `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` `fix(0428-249): build baha-ci-operator-testonly artifact with its build tag (#1825)`
- Worktree: /tmp/pf1826 (full clone, branch develop @ 46d3dccc)
- Hosted-only: no local go test/docker. Read-only source + diff scan.

---

## (a) #1826 / 0428-279  head `080ea830`

- PR #1826: `state=open, merged=False, base=develop, files=1`. Base `git merge-base --is-ancestor develop HEAD` = TRUE (fresh base).
- HEAD HEAD = `a4dffedb90fc92f3d7f6d15e2860cdb97c2f33a5` (PR rebased since `080ea830`). Single commit.
- `git ls-remote ... refs/pull/1826/head` = `a4dffedb...`.
- File changed vs develop: **exactly one** — `docs/releases/v0.4.28.demo-ref`:
  ```
  -c23bd9ac58919302ffad3a43f43afb1a34bfbc96
  +df4867c7540774eba8b8811cb64946b4adc0c8ab
  ```
- Byte-identical content check between the claimed head `080ea830` and live head `a4dffedb` for the changed file -> `diff` reported IDENTICAL. The live PR carries NO `cmd/baha/app_pull_render.go` and NO test file.
- CI (per handoff): earlier static FAIL was the dispatch demo_ref mismatch (`c23bd9ac` in the demo workflow vs `df4867c` expected). `df4867c` is the demo fix (#0428-279) that adds `baseharbor.app.pull` to the static/mcp contract. This is a docs/release-pin correctness fix, not a code defect. No new code defect found.

Verdict #1826: clean. The static FAIL was ONLY the dispatch demo_ref mismatch (c23bd9ac vs df4867c), now corrected. No code defect. Acceptable.

---

## (b) #1820 / 0428-271  head `28803d11`

- PR #1820: `state=open, merged=False, base=develop, files=6`. Base `git merge-base --is-ancestor develop HEAD` = TRUE (fresh base).
- HEAD HEAD = `28803d11027197e7734fb3ec94bef9b34e224b0d`. Base of 1820 = `05ef4853...` (ancestor of develop; NOT the #1824/0428-276 env_destroy base).
- `git ls-remote ... refs/pull/1820/head` = `28803d11...`.
- #1820's OWN diff vs its base `05ef4853` is exactly 2 files, 63 insertions:
  1. `cmd/baha/app_broker.go` `verifyRuntimeBrokerBuildIdentity` — adds a fail-closed commit-provenance check:
     ```go
     if expectedCommit != "" && actualCommit != "" && expectedCommit != actualCommit {
         return fmt.Errorf("%w: runtime build commit %s incompatible with CLI commit %s",
             errRuntimeBrokerIncompatible, actualCommit, expectedCommit)
     }
     ```
     (replaces the prior `_ = expectedCommit / _ = actualCommit` discard; dev/edge pair with an empty commit still stays lenient)
  2. `cmd/baha/app_broker_compat_test.go` — new `TestVerifyRuntimeBrokerBuildIdentityCommitMismatch` regression + expanded dev/edge cases (34 -> 83 lines).
- The other 4 files in the `files=6` diff vs develop (`env_destroy_integration_test.go`, `environment_destroy_scope.go`, `environment_destroy_scope_test.go`, `.github/workflows/pre-release.yml`) are the #1822 batch baseline (90086a1f) + #1824 (0428-276) env_destroy OwnerVerified removal, already in #1820's base. NOT part of #1820's own work.
- dev/edge + EMPTY-runtime-commit regression: CONFIRMED PRESENT. The test asserts `verifyRuntimeBrokerBuildIdentity("edge", "")` passes (empty runtime commit stays lenient for the dev/edge pair), and `verifyRuntimeBrokerBuildIdentity("dev", "")` with an empty CLI commit stays green. This is acceptance-criterion #2 for 0428-271 and the regression covers the exactly-empty case.
- `git log 05ef4853..origin/pr1820` lists ONLY #1820's four 0428-271 commits (no foreign commit). Base is fresh (05ef4853 is an ancestor of develop). No #1812/#1819 touched.

Verdict #1820: clean. Both regressions present (commit-mismatch fail-closed + dev/edge empty-commit). No code defect.

## repo-rule compliance
- Read-only scan only. No product files edited. No .github/** touched. No local test suite or docker executed. Subagents: none.
- Evidence lives in baseharbor-plan evidence/ (not in a product repo). Atomic commit + push.

END_STATUS
#1826 clean (demo_ref mismatch c23bd9ac->df4867c, no code defect). #1820 clean (both 0428-271 regressions present, fresh base, only own 0428-271 commits). Both ready for CODEX review.

END_DONE w82-0428-216-hv24actionability: independent preflight for #1826/#1820 done read-only; evidence SHA <pending>; no product writes/CI/subagents
