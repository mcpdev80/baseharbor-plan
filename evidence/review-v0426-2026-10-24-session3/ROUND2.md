# Independent corrected-candidate review — round 2

Authority: Marcel's session3 assignment and explicit follow-up requesting review of corrected #1064/#1060, with standing authorization to publish Planning. Session1 retains all implementation/integration/merges; session2 owns native evidence/freeze. Reviewed the source handoff at Planning9c15cf5e8820d3d0b8f9fe58f2e6c54238f6674f and exact Git objects, not just reported test counts.

## Exact technical verdicts

All repositories are under mcpdev80. These are technical review decisions published as PR issue comments, **not formal GitHub pull-request reviews**. No product/CI implementation change, merge, native run, tag, release or deployment was performed by this reviewer. Old rejected heads remain rejected historically; new decisions cover only the specified source.

| Repository / PR | Full reviewed head | API base | GitHub integration | Verdict |
| --- | --- | --- | --- | --- |
| baseharbor #1064 | e7fe45ccb3c2103bb3b57ad3300892b932818934 | 65aa063e90767c85af976081c100be1817370e67 | 7e090b1553e80d8ca322430a469de385059a7050 | APPROVE exact policy source; mandatory CI verified green |
| baseharbor #1060 | db79f24a39ccc1a6f8f38a13d20dd18ab151abc2 | 65aa063e90767c85af976081c100be1817370e67 | 5424874e482d4b3640bad7a0c3ce849114651a65 | APPROVE corrected source delta; final integration qualification remains OPEN |
| baseharbor #1052 | 9f715184af7b89ca3011aa4a0636c45138fe2c6b | a2abc17a8057ba972cb9ed481fad229fe9f12824 | Not newly qualified on GitHub | APPROVE source/unit contract; current-base CI/native/integration conditions remain OPEN |

Verified trees: #1064 ead688ff2e5ebb660c369cd073e1dc268153d6d0; #1060 aaf2be84d53c8b8b320e14d3b73c7260c31b1fe1; #1052 593cfa4f9f113f86f067a5cfadc24535e1210e29. Repository working trees remained unchanged after review.

## #1064: prior findings resolved

Read entire net two-file diff and surrounding trusted record/resolver/merge proof. Removed both the inherited title/commit-message bootstrap fallback and the obsolete rejected-R hard-coded branch. The target register permits exactly the three modified CI scripts or those three plus modified ci.yml. Workflow inventory requires ci-actionlint. Exact authenticated repository/develop, full immutable source SHA, raw SHA256 blobs, statuses, complete mandatory check IDs, duplicate-key/anchor rejection and independent full diff/integration re-derivation remain required. Candidate-side records confer no authority; reviewed source can advance only through exact Git-computed first-parent merges of authenticated target ancestors.

The old false negatives were removed. Existing real-Git fixture now runs against both inventories, positively proving CRLF/raw hashes, retained three-file acceptance and real trusted forwards, and negatively exercising bad context, omitted/weakened/duplicate records, changed hashes/statuses/inventory, forged integration/trees, untrusted sideparents, copied trees and unreviewed follow-ups. Matching record shapes alone do not qualify a candidate; ancestry and reviewed blobs are checked independently.

Reviewer executed **complete planner suite115 PASS** with Python3.12/Go1.26.9, including actual registration shell/package checks that were unavailable during round1. The suite also executed existing utility sub-suites:8 typed-consent,7 GC and5 sandbox-reset regressions, all PASS. See [local execution log](r2-1064-planner.log). No duplicate CI run was launched.

[CI40110621660](https://github.com/mcpdev80/baseharbor/actions/runs/40110621660): inspected jobs, all selected validations and required final job120921752898 successful. Trusted Plan120921382630 log explicitly binds the exact B/H/I in the table. Artifact contents were not independently downloaded in this round; no artifact-digest verification is claimed from job success alone.

No blocking finding remains on this exact policy source. [Published technical APPROVE](https://github.com/mcpdev80/baseharbor/pull/1064#issuecomment-6386652530). Session1 may evaluate its authorized integration using these exact inputs; this reviewer performed no merge.

## #1060: all three prior delta findings resolved

Read entire net four-file diff, planner call path, strict helper and actual workflow shell case plus new regressions.

- Planner binds exactly #1052 source9f715184af7b89ca3011aa4a0636c45138fe2c6b and two modified bootstrap paths. It independently re-derives actual diff/integration and proves clean target-forward ancestry. Other paths/statuses/contexts/follow-ups reject; no broad OpenBao exemption was introduced.
- OpenBao check is reachable. The actual workflow fetches BASE_SHA and extracts the trusted-base runner. The helper discovers once, requires all21 exact bootstrap unit test names, executes those families once and requires RUN/PASS for each; missing, skipped and failed work reject. Native opt-in tests keep separate runtime gates.
- Exact end-of-name matching is restored for existing core918 SQL safety families; replacement-suffixed tests cannot stand in for required tests.

Executed **six existing focused tests PASS** (OpenBaoExactRetryRouteTests and OpenBaoValidationTests). This includes the actual ci.yml shell fragment on a real temporary Git source/Go package, positive/missing/skipped cases, deterministic negative process-output matrix, restored SQL safety names and real-Git reviewed/forward/refusal cases. [Local execution log](r2-1060-targeted.log).

Independently ran the corrected helper from db79f24a against immutable #1052 source: **all21 exact required unit families PASS**, no native journey. [Execution summary](r2-1052-real-executor.log).

The separate [reviewer actual-object probe](r2-actual-source-probe.py) uses the real #1052 SHA and actual target65aa063e, without patching the reviewed anchor. Clean-forward simulation yields exactly source-contracts and openbao-package-tests, with only the two modified bootstrap paths. Missing/fake integration, wrong merge-base/status, extra path, wrong repository/branch and same-tree unreviewed linear follow-up all reject. [Results and synthetic IDs](r2-actual-source-probe.log). Synthetic commits/trees are local proof only, not GitHub merge or native evidence.

[CI40110759871](https://github.com/mcpdev80/baseharbor/actions/runs/40110759871): inspected successful component checks (focused Python, planner, policy, executor/verifier, actionlint). Trusted Plan120921794316 binds the exact B/H/I above. Final job120922163904 correctly reports:

> BLOCKED: coverage-unresolved: workflow execution/cleanup/evidence impact requires native qualification: .github/workflows/ci.yml; CI execution/evidence impact requires specific qualification: scripts/pr-check-runner.py

This is not green final qualification. No Required Check is waived. [Published technical delta APPROVE and conditions](https://github.com/mcpdev80/baseharbor/pull/1060#issuecomment-6386646293).

## #1052: actual source/unit contract independently qualified

Read bootstrap.go production net diff, added fixture implementations and error/order assertions, including permanent-before-transient admission, bounded five-attempt/five-second-per-attempt unseal probes, caller-cancelled backoff, unchanged nonretrying Inspect, invalid JSON refusal, zero writes after pre-probe failure, one write across post-probe transport retry and truthful direct per-member verification. Original unseal secret/ownership handling is not relaxed.

The actual corrected #1060 helper executed all21 mandatory unit tests on this exact immutable source. This upgrades round1's pending source/unit review; unavailable q123 was not used as substitute evidence. The real-object target-forward probe verifies the source-binding inputs.

Nonblocking evidence limits: TestUnsealRejectsUnknownBAOAddrDestination directly tests its fake destination parser, not a product validator. TestMemberPhaseSequenceIsEnforcedPerMember's description overstates omission/sequence checking; the primary convergence test separately asserts the actual ordered member sequence. These unit results do not establish native Podman/HA recovery. No extra tests or product fixes are requested merely to inflate counts.

[Published technical source/unit APPROVE](https://github.com/mcpdev80/baseharbor/pull/1052#issuecomment-6386647783). Fresh current-base qualification and green required CI remain mandatory after corrected target policy is integrated; actual native receipt remains with session2.

## Exact remaining integration conditions

1. #1064 exact policy is source-approved and mandatory CI green; all integration operations remain session1's assignment.
2. #1060 current db79f24a still inherits the broad bootstrap helper from its old base. The approved prerequisite #1064 removes it; source-delta approval never waives that dependency or approves the standalone inherited fallback.
3. Independently ran `git merge-tree --write-tree e7fe45cc... db79f24a...`: real conflict in scripts/test_pr_gate_plan.py, as reported by session1. Preserve both matrices when resolving. The conflicted synthetic tree is not accepted. A manually resolved result needs a **fresh exact-source review anchor**, not fabricated clean-merge evidence from this verdict.
4. Separately review/accept the target-side four-file SHA256 register for that final anchor, then genuine clean target-forward record merge and fresh mandatory PR CI. db79f24a itself is not automatically a valid final record anchor after manual conflict resolution.
5. #1052 then needs its actual new integration inputs/checks; #1056 remote b0abe105 remains rejected for old F1/F2. Local unpublished preparation is not reviewed/accepted here. #1046 and consumer/final pins/native journeys remain governed by their existing conditions.

The separately reported native run40110974339 is session2's receipt assignment; its status/evidence is not newly qualified by this policy review. No release or consumer freeze readiness is inferred. Core W1 anchor remains1861ed07888a1ec22c218ca491d23ee54f48e261; v0.4.27 remains untouched.

## Planning and publication verification

Own evidence files plus scoped round2 handoff sections only; original owners/status/dependencies and other sessions' material are preserved. Regular release-cycle generator, render/check and47 planning tests run before expected-parent non-force MCP publication. The actual published SHA is subsequently fetched into a clean worktree, its exact tree/parent checked, and generator/render/check/tests rerun. Final SHA/results are reported in the session response to avoid a self-referential receipt. Earlier round1 verdicts and initial publication difficulties remain historical in HANDOFF.md/VERIFICATION.md; this round's exact-head decisions supersede the corresponding old-head findings only.
