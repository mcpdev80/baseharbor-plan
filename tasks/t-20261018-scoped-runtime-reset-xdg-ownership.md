---
id: t-20261018-scoped-runtime-reset-xdg-ownership
type: bug
areas: [ci]
release: v0.4.26
parent: v0.4.26
owner: "mcpdev80 (scoped XDG reset review)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#993]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/993#pullrequestreview-5566047336", "https://github.com/mcpdev80/baseharbor/actions/runs/39185400529", "https://github.com/mcpdev80/baseharbor/commit/cf63ccfc822796b2c9e8fe0214026bfe06ebb3f3"]
---

- [x] t-20261018-scoped-runtime-reset-xdg-ownership · Scoped runtime reset must retain unrelated XDG state #task #release/v0-4-26 #status/closed #view/closed #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (scoped XDG reset review) · **Priority:** high  
    **PR:** [baseharbor#993](https://github.com/mcpdev80/baseharbor/pull/993)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (scoped XDG reset review)  
**Priority:** high  
**PRs:** [baseharbor#993](https://github.com/mcpdev80/baseharbor/pull/993)  
**Source:** 
<!-- /generated:links -->

## Goal

Fix [baseharbor#992](https://github.com/mcpdev80/baseharbor/issues/992) before v0.4.26 readiness. A resource-scoped `scripts/ci-runtime-reset.sh` call must never recursively delete shared or ownership-unknown BaseHarbor XDG state.

## Ownership and scope

- Product files: `scripts/ci-runtime-reset.sh` and one dedicated sandbox regression script. No changes to #991 or CI policy/executor.
- Preserve scoped resource filtering; never infer state ownership from an arbitrary substring scope.
- Ambiguous/shared XDG state is retained or blocked. Only explicitly proven isolated state may be removed when scoped.
- Preserve existing intentionally authorized full reset of the dedicated runner; never expand it to arbitrary environments.
- Shell fixtures use disposable HOME/XDG roots, a stub container engine and harmless systemctl. Test selected/foreign containers, networks, volumes, Quadlets, selected/foreign XDG state, unknown scope, isolated roots and dedicated full reset.
- No real containers, SSH, native hosts, credentials or private paths. Minimal appropriate CI; batch edits and independently review before merge.

## Handoff

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Existing ownership unchanged; no takeover. Candidate SHAs and prior handoffs preserved. Trusted gate reports `coverage-unresolved` (missing independent exact-bundle qualification); CI reruns, correction loops and merges are halted by Maintainer order. Independent local review state recorded in ecosystem `evidence/board-2026-10-19/` where a worker ran one.
- Worker o4 (19d72a4b) independently reviewed exact head `b981f3b60bebfaebf6eb7f2f467dfd06142c90fe` read-only: verdict APPROVE (test/scripts-only diff, guards intact; report evidence/board-2026-10-19/o4-993-review.md).
- 2026-10-18: Review 5562183275 P1 correction: test-only strict rm fixture now intercepts all deletions, permits removals only in disposable test root, records /tmp global targets without executing them and rejects other external paths. An independent outside-root sentinel is asserted intact after the actual unscoped script executes under fixture PATH; scoped state/resource assertions and dedicated full-reset contract retained. Corrected PR #993 head `b981f3b60bebfaebf6eb7f2f467dfd06142c90fe`; HF sandbox job `6ad488b6c6628814522722dd`: 5/5 tests PASS, bash -n, py_compile, diff check PASS. Independent content review and trusted coverage remain required; no native/live test or merge.


- 2026-10-18: Exact implementation candidate `85395ecb5ddabc8034bca67bbc91bd300e1c7970` in [Draft PR #993](https://github.com/mcpdev80/baseharbor/pull/993). Shared/unknown XDG state is retained for any scoped reset; selected runtime resources remain scoped. Dedicated unscoped reset remains unchanged. Isolated [HF job 6ad4055bc66288145226d33b](https://huggingface.co/jobs/ThunderHawk1080/6ad4055bc66288145226d33b) passed five executable sandbox tests, Bash syntax, Python compilation and diff check. Independent review required; no native test, self-approval or merge.


- 2026-10-18: Claim published before product implementation. Review issue #992 and product repository rules; state cleanup must fail closed for shared XDG roots. Release prepare depends on this task.

### 2026-10-19 — Maintainer acceptance after actual required sandbox execution

- Final #993 headdbf3ef7a92f795606e88545d883bb222253ce872 normally integrates current develop; both product/test blobs unchanged from fresh independently reviewed e6616b45. Review5566047336 and finite source/status qualification#1003, strict ancestry/tree proof retained.
- Actual CI39185400529 SUCCESS, including mandatory planner117846706353 executing all five named safe sandbox tests and all seven GC tests; Actionlint, policy, verifier, focused Python and PR Selected Checks117847006885 PASS. The unrelated absent consent-suite skip is not claimed as executed evidence.
- Regular protected squash mergecf63ccfc822796b2c9e8fe0214026bfe06ebb3f3. Maintainer accepted/closed, prior source history and ownership retained. No real runtime reset/native execution or global cleanup was performed by coordinator; all reset testing was sandboxed.
