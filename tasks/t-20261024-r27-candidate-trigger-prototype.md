---
id: t-20261024-r27-candidate-trigger-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1055]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-r27-candidate-trigger-prototype · CI: explicit candidate trigger prototype #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
**Source:** 
<!-- /generated:links -->

# CI: explicit candidate trigger prototype

## Goal
Prepare explicit candidate-ready PR trigger with no per-commit PR CI, without activating it during v0.4.26.

## Scope
- Isolated design, review and regression preparation only on the existing draft PR.
- No merge to develop, no Ruleset or production workflow changes, no v0.4.26 interference.
- Do not treat prototype output as accepted trusted evidence.

## Acceptance
- Mock event and token paths, draft/stale guards, workflow-policy and actionlint; independent E2E qualification after v0.4.26.
- Final independent check and Owner-authorized rollout must follow v0.4.26 completion.

## Dependencies and file ownership
The v0.4.27 release-start updates remain unaccepted; this active status documents isolated work only, not production readiness. Existing PR #1055 remains draft. No ownership of other tasks or PRs is implied.

## Handoff
- 2026-10-24: isolated preparation in [PR #1055](https://github.com/mcpdev80/baseharbor/pull/1055); current status active, not qualified or mergeable by this card.
- Draft-label event security fix: all twelve candidate guards in `ci.yml` now require a non-draft PR for `labeled` events; the separate artifact-GC test guard also rejects draft label events. Static regression checks cover both workflow surfaces. Candidate source head: `a77371a20e6a1959c7fc0e9e0adc4ce3689c7c1b`.
- Missing: executable workflow-policy/Actionlint/selected checks on exact head; authenticated GitHub App/PAT event E2E and base-SHA/stale-head verification. Keep on draft feature branch; v0.4.26 release freeze is binding.

- 2026-10-24: label-delete HTTP 404 is no longer ignored by the candidate submitter: it now fails closed before POST rather than reporting a spurious dispatch. Regression added for GET/DELETE-only on failure. Draft PR #1055 current head `1089a169061fec0fdc49ecb2140dc0b1001cdd3c` (unqualified until targeted checks run).

- 2026-10-24: tightened re-label race guard: after DELETE, the second GET must show `ci:validate` absent; otherwise fail with an actionable error and perform no POST. Added a mocked GET/DELETE/GET negative regression. Candidate head `24934756677fd261580f2f37b11ad61197f4444d`, draft/unqualified. This protects against silently claiming CI dispatch when GitHub has not actually removed the label.

- Current draft PR #1055 head: `4a89d8115ee146675599ca31bd8a1ac8486a91a9`. Submission text distinguishes a label request from proven CI completion. Independent checks remain outstanding.

- Latest prototype head `13e6a649200b70330e1179cd882bcdcb4e355522`: candidate submitter now rechecks exact target base SHA after label preparation and fails closed on a changed base before POST; mocked regression and all relevant fixture shapes updated. Static source review only; independent tests and actual event delivery not yet qualified.

- 2026-10-24: candidate dispatch now re-fetches the PR after the label POST and verifies exact source/base SHAs, open/non-draft status, target branch, and the label's presence; regression matrix covers missing label, changed head, changed base and re-draft. Draft PR #1055 candidate `685ec3ab1a1f037f17f1d513fa41fd54cb017a59`. This confirms repository label state only, not a successful Actions run; independent exact-head tests pending.

- 2026-10-24: API rejection regression added for HTTP 403 on the actual `gh` wrapper. Draft PR #1055 head `c453be60a123227261344886c10e04883c85a874`. No accepted CI proof or workflow rollout yet.

- CI prototype guard-test audit: a test previously skipped every PR job because it searched only for `if:` conditions beginning with `github.event_name`, while production conditions begin with the candidate event matrix. This was corrected to enumerate all `pr_*` jobs, fail if the guard is missing, and check develop targeting and draft-label exclusion. Draft PR #1055 exact head `e21ee2b9c390eb20570e8939cfb0c2f3f56b8b36`. Unit tests still require execution and independent verification.

- 2026-10-24: targeted candidate test suite on Hugging Face CPU at exact PR #1055 head `8f40ce4f850c59048111d0c54a9a7276361e68cc`: **16/16 passed**, [run evidence](https://huggingface.co/jobs/ThunderHawk1080/6adbf6881e112550ce7da873). The initial run found and the subsequent commit fixed an actual test assertion indexing bug after the new readback GET. Wider planner suite requires Git/PyYAML/Go in the temporary runner; these are environment prerequisites, not candidate qualification. Native GitHub event delivery is still unverified.

- Hugging Face independent execution, exact PR #1055 commit `8f40ce4f850c59048111d0c54a9a7276361e68cc`: [candidate trigger 16/16 PASS](https://huggingface.co/jobs/ThunderHawk1080/6adbf6881e112550ce7da873); [trusted planner 95/95 PASS](https://huggingface.co/jobs/ThunderHawk1080/6adbf6ba1e112550ce7da896) with git, Go and pinned PyYAML available. No GitHub Actions event E2E proven; still draft/isolated.

- 2026-10-24: independently audited all 19 workflow files on isolated #1055 branch: only `ci.yml`, `artifact-gc.yml`, and legacy `host-trust-owned-e2e.yml` listen to PR events. The legacy listener targets `release/v0.4.24`, not `develop`; others are manual, reusable, push-on-special-branches, or release-only. Added fail-closed workflow PR-trigger inventory regression. Exact draft PR head `ecde3f9293cb08b7ef92c3c69c02ea85591e4839`: [17/17 candidate tests PASS via HF](https://huggingface.co/jobs/ThunderHawk1080/6adc50e1046eb82b1ecdaef4). No changes to mainline workflow activation.

- Independent Hugging Face actionlint run on exact PR #1055 draft head `ecde3f9293cb08b7ef92c3c69c02ea85591e4839` using `golang:1.25`, initialized temporary checkout, actionlint v1.7.12 with shellcheck disabled: [job completed without reported lint diagnostics](https://huggingface.co/jobs/ThunderHawk1080/6adc5118046eb82b1ecdaf0f). This is static workflow lint, not evidence of a real candidate-label event. Existing 17/17 candidate unit tests separately passed.
