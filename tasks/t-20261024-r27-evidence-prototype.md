---
id: t-20261024-r27-evidence-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1048]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-r27-evidence-prototype · CI: isolated evidence archive security prototype #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->

# CI: isolated evidence archive security prototype

## Goal
Prepare and harden the draft evidence transport and advisory coverage code without granting qualification or changing the running v0.4.26 release.

## Scope
- Keep staging publisher, resolver and advisory signed receipt verification isolated in draft [PR #1048](https://github.com/mcpdev80/baseharbor/pull/1048).
- Ensure manifest and payload type checking, digest binding, path safety, create-only publication and negative tests.
- Do not replace existing trusted GitHub run, job or artifact provenance verification.
- Do not merge, change production workflows or Rulesets, or activate any v0.4.27 CI behavior while v0.4.26 is running.

## Acceptance
- Focused negative tests and independent review for artifact replay, foreign run/job, stale source/policy/integration, missing checks, symlink/concurrent-writer escapes and manifest collisions.
- Prototype handoff includes exact commit, reproducible test outputs and unresolved limitations.
- This prototype is not acceptance of [publisher](t-20261022-r27-evidence-publisher.md), [resolver](t-20261022-r27-evidence-resolver.md), or [verifier](t-20261022-r27-evidence-verifier.md).

## Dependencies and file ownership
Formal release-start update and evidence-contract dependencies remain unaccepted. The active card records only isolated security preparation and does not claim those formal tasks.

## Handoff
- 2026-10-24: draft PR #1048, isolated preparation underway, not independently qualified.
- GitHub Actions run [40040221997](https://github.com/mcpdev80/baseharbor/actions/runs/40040221997) has completed: Workflow policy, Trusted Plan, Focused Python and selected validations succeeded, but required **PR Selected Checks failed** at `Enforce every required check (unqualified runtime remains blocked)`. Treat as a genuine unresolved trusted coverage blocker; do not override it or count the prototype as accepted.
- Recent head after further changes is different from this run SHA, so the run is **not evidence for the current head**.

- Hugging Face executed focused evidence unit suite on draft PR #1048 head `b51f74b5eed4acf31a7602c9bb7f9892a488d6b7`: [68/68 PASS](https://huggingface.co/jobs/ThunderHawk1080/6adbf7351e112550ce7da8e7). First run revealed an invalid negative-case test expectation (caller default expected artifact was bound); fixed the fixture to explicitly pass `artifact_digest=None`, reran green. Independent provenance, race hardening, and trusted required-check qualification remain open.

- 2026-10-24: resolver now opens the entire archive directory chain with descriptor-relative `O_DIRECTORY|O_NOFOLLOW`, and reads manifest and payload via verified directory descriptors; mitigates symlink-component replacement between path inspection and reading. Added symlink-root and ancestor negatives. Exact isolated draft PR #1048 head `a56eba0de71ec9f209e89696500b0457ce521111`: [70/70 evidence unit tests PASS on Hugging Face](https://huggingface.co/jobs/ThunderHawk1080/6adc4e9a1e112550ce7dd7e7). Publisher still uses path-based operations and needs equivalent race hardening and independent provenance qualification; no activation or merge.

- 2026-10-24: publisher hardened with descriptor-relative `mkdir`/`open`/create-only `O_EXCL|O_NOFOLLOW` directory traversal, plus fail-closed collision checks on existing manifests and payloads; three root/ancestor/payload-directory symlink regressions added. PR #1048 exact prototype head `c1dca79776330cb3ceeae9582021dca92dc2033b`: [73/73 unit tests PASS in HF](https://huggingface.co/jobs/ThunderHawk1080/6adc507b046eb82b1ecdaec4). No authorization to merge/activate, and independent origin/provenance validation remains open.

- Planning audit performed on Hugging Face: [plan check → render → check](https://huggingface.co/jobs/ThunderHawk1080/6adc508f1e112550ce7dd8e0), 321 tasks / 7 epics / 13 releases, **0 errors**, 5 expected active-dependency warnings. This verified a temporary clean checkout; generated render outputs have not been published back to GitHub by this test.

- 2026-10-24: publisher failure handling hardened to avoid unlink-by-name after a write/fsync exception (a concurrently replaced directory entry must not be deleted). Added durability-failure regression verifying no committed manifest on incomplete staging. PR #1048 exact head `6a1005455ecd706ab4e3483eb0eef7a285e2cd85`: [74/74 evidence tests PASS on Hugging Face](https://huggingface.co/jobs/ThunderHawk1080/6adc56371e112550ce7ddb3a). Still prototype-only: no trusted issuer, no release promotion.

- 2026-10-24: `r27_verified_coverage.verify` now validates all caller-supplied expected scope fields (stage, exact commit SHA, policy digest, gate, artifact digest) before record comparison; negatives for non-string/unhashable and invalid types. PR #1048 exact head `5ab9b1094a1b936a735a3e75a89f0bbec09eda26`: [75/75 isolated HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc5cb8046eb82b1ecdb1e7). Trust issuer and production integration still pending; no merge or rollout.

- 2026-10-24: resolver rejects JSON's nonstandard `NaN`, `Infinity`, `-Infinity` constants in archive manifest (Python decoder otherwise permits them by default), including matching manifest digest; added regression cases. PR #1048 head `3f78bfeaf87aaebd68242d2dc7d29ac3f554f4e4`, [76/76 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc5fc7046eb82b1ecdb24d). No trusted provenance/issuer qualification or mainline merge.

- 2026-10-24: signed gate receipt parser now rejects nonstandard JSON `NaN`, `Infinity`, `-Infinity` at the decoder boundary with `EVIDENCE_SCHEMA`, rather than later identity validation. Regression for all three constants. Isolated PR #1048 head `d349cec01747a6a5ad2d9f44cf49b5d6d129506e`: [77/77 targeted HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc62b0046eb82b1ecdb30b). This does not qualify the trusted issuer or integrate into production CI.

- 2026-10-24: both signed gate-evidence (`r27_verified_coverage.py`) and compact offline receipt (`r27_evidence_receipt.py`) now reject nonstandard JSON NaN/Infinity/-Infinity during decoding, each backed by explicit parser-boundary regressions. Draft PR #1048 head `6e8e6a447ee2eb7bde6d3db2096b371ef6d21056`: [78/78 evidence tests PASS via Hugging Face](https://huggingface.co/jobs/ThunderHawk1080/6adc62d4046eb82b1ecdb318). Independent CI origin and trusted issuance remain unimplemented; not yet eligible for reuse/promotion.

- 2026-10-24: added isolated `r27_github_origin.py` pure validation seam for exact GitHub run ID/attempt/head SHA/repository/workflow/job ID/name/status/conclusion, failing closed on mismatches, duplicates, skipped/failed jobs; intentionally **does not fetch authenticated API data or issue signatures**. Four test methods include negative matrices. Draft PR #1048 exact head `e01fe1b257edcd90295a98f48bdc6202d505a1e6`: [82/82 combined HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6308046eb82b1ecdb327). Remaining: authenticated GitHub API owner, pagination, independent policy selection, issuer binding, integration/required-check acceptance; no promotion or mainline activation.

- 2026-10-24: independently reproduced malformed GitHub run repository response causing `AttributeError` and boolean `max_jobs=True` incorrectly accepted. Built both fixes plus regression cases in a temporary Hugging Face container; [85/85 tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc64381e112550ce7ddf62). Published code+tests as **one single branch update**, PR #1048 candidate `e0656eda8a4abe5d0e2c097fde30ffaf957ad46a`, avoiding per-file `synchronize` events. This is a validated prototype, not trusted issuance or CI activation.

- 2026-10-24: added isolated `r27_github_fetch.py` trusted-transport injection seam for exact run and attempt-specific paginated job results, with fail-closed handling of partial inventory, network exceptions and wrong run identity. Not an authenticated transport implementation or trusted issuer. Combined prototype [89/89 HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc64fa046eb82b1ecdb392), published as **single branch ref update** to draft PR #1048 head `f070005bef200c5cf82b44dee99880ba896b109b`; no v0.4.26 or `develop` changes.

- 2026-10-24: isolated `r27_github_transport.py` adds bounded, token-authenticated HTTPS GitHub REST GET (fixed API host and scoped run/jobs endpoints, 15s timeout, 4 MiB response limit, generic errors without credential leakage) plus mock transport regressions. [93/93 combined HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc65d51e112550ce7de00b); PR #1048 one bundled head update `0f1c18be7639d944f77f4341e73d733a65f9c574`. Transport is not yet wired to trusted CI issuer/policy and must not authorize promotion or trigger v0.4.26 CI rollout.

- 2026-10-24: bundled `fetch_authenticated_origin` integration connects scoped bearer-token GitHub REST transport to the exact-run/attempt job origin checker, with missing-token regression. Draft PR #1048 candidate `f11c9a432292ffa346b43c160d869f58894f9c02`, [94/94 HF regression tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc67471e112550ce7de0be), published via one branch update. This does not yet provide a trusted issuer, policy enforcement, or production rollout.

- 2026-10-24: trust-boundary hardening on isolated GitHub API transport: rejects HTTP redirects (prevents forwarding bearer credentials), duplicate JSON keys and nonfinite JSON constants before origin validation. PR #1048 exact candidate `d8acb5749cad430627fcbd6bf57a6102d73f5abc`, [96/96 focused HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc68b3046eb82b1ecdb462); one bundled GitHub branch update. Trusted policy/issuer integration and production end-to-end qualification still pending. No v0.4.26 CI activation.

- 2026-10-24: GitHub origin verification now binds a successful run to the expected workflow triggering event (`pull_request` default; explicit `push` or `workflow_dispatch`), preventing reuse of a successful run under the wrong event. Real GitHub API sample confirmed event/run/job metadata fields; [97/97 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6952046eb82b1ecdb476). Draft PR #1048 candidate `b14a1f43c5e613bd393861479d2b9f2c1c39fcb6` published in one branch ref update; still no issuer authorization or v0.4.26 CI rollout.

- 2026-10-24: isolated GitHub origin fetch now rejects path-unsafe repository identifiers and malformed/inconsistent first API job inventory pages without unnecessary retry calls. [99/99 HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6a55046eb82b1ecdb49c) on complete candidate before one branch update to draft PR #1048 `fddd2c06924d94f2d4b2e971109d2889a2151e89`. Authenticated origin remains a prerequisite only; policy-authorized issuer and end-to-end CI acceptance are pending. No impact on v0.4.26.

- 2026-10-24: exact-attempt GitHub job fetch now fail-closes immediately if API `total_count` drifts between pages, with targeted two-page regression and no extra third request. [100/100 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6b231e112550ce7de1a6), draft PR #1048 candidate `17635a4b63820fb1f368c6c04c3e686bd1e76648` published in one branch ref update. Trusted policy/issuer integration remains outstanding; no release CI activation.

- 2026-10-24: new isolated `r27_origin_bound_coverage.py` correlates exact-scope MAC-verified receipts with authenticated GitHub run/job origin and trusted-caller gate-to-workflow/job mapping. Includes pass/pending/bad-signature/failing-origin/missing-policy regressions and forwards exact expected workflow event through `r27_github_fetch.py`. [105/105 isolated HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6c0b046eb82b1ecdb4f5); draft PR #1048 candidate `35146264f0aabf3486c2f9bd10bf4a853c24c1f3` published with one ref update. Advisory only: trusted CI policy owner, issuer authorization, integration and required-check qualification remain open; no v0.4.26 impact.

- 2026-10-24: origin-bound coverage now preflights **every required gate's** trusted job/workflow mapping before making any authenticated GitHub API calls, including gates whose receipts are still pending; malformed/incomplete policy fails closed with a regression matrix. [106/106 HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6cd1046eb82b1ecdb510). Draft PR #1048 updated in one branch push to `40ef549d22ccaa7ca422bbe6b99cee495e416628`. No trusted issuer/production promotion and no v0.4.26 changes.

- 2026-10-24: tightened gate-to-job policy mapping to a single safe workflow filename and bounded job name; traversal, nested pseudo-paths and newline job identities rejected before API fetch. Draft PR #1048 head `34e5dd5499118fd65151f78d0c081c5354c24702`, [107/107 full isolated HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6dd41e112550ce7de29e). No trust issuer/promotion authority; no v0.4.26 changes.

- 2026-10-24: isolated gate-origin policy entrypoint now validates the `required` gate collection before set conversion, preventing uncontrolled exceptions and API activity on malformed caller types. Draft PR #1048 candidate `1636046019f677286617ce50db5579b58cabf96b`, [108/108 full focused HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6def046eb82b1ecdb546), one bundled branch update. Trusted issuer/production integration pending; do not activate v0.4.27 CI on develop before v0.4.26 is complete.

- 2026-10-24: removed redundant required-gate type check and added early fail-closed detection for duplicate required gate identities in origin-bound trusted-policy inputs, so no ambiguous gate list can qualify or trigger API calls. Draft PR #1048 head `9a84bd8ff4937a1c8dc3fffe9d10041f7f5fb976`, [109/109 HF regression tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc6ec81e112550ce7de2ba); one bundled branch ref update. Trusted issuer and full CI integration remain pending.

- 2026-10-24: added isolated gate receipt issuer `r27_verified_issuer.py` requiring an authenticated, exact GitHub job-success origin match before HMAC signing; explicit fail-closed checks for missing job, origin mismatch and malformed scopes. Draft PR #1048 exact head `db04636ff4495cafc0f7e06257d93ae3c3003ac0`, [113/113 tests PASS on published SHA](https://huggingface.co/jobs/ThunderHawk1080/6adc7474046eb82b1ecdb69a), one bundled branch ref update. **Not production trusted**: caller-provided gate-to-job policy, signing-key custody, issuer isolation and promotion authorization still require independent trusted CI integration; no activation before v0.4.26 release.

- 2026-10-24: isolated signed Evidence issuer now refuses issuance unless the caller provides an exact gate-to-workflow/job policy mapping matching the requested job, before GitHub API access. Mock negative cases cover missing, incomplete and mismatched mappings. PR #1048 head `b32c7b6c9e6a49f0e9440e03827619894b78f172`; [114/114 HF isolated tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc7518046eb82b1ecdb6d1). Mapping still caller-provided rather than a signed independent policy authority; not qualified for CI activation, no changes to v0.4.26.

- 2026-10-24: issuer now recomputes canonical SHA-256 of the complete gate-to-job mapping and requires exact equality with the signed `policy_digest` before authenticated GitHub fetch or MAC issuance. Modifying even another gate invalidates the digest. [115/115 HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc7780046eb82b1ecdb795); one bundled draft PR #1048 update `d6348a4be2d7deeba47c1c55fbcdd8c8e4321dc2`. WARNING: mapping source remains caller-provided, not independently authorized; signer key custody and CI isolation/promotion still unimplemented. v0.4.26/develop untouched.

- 2026-10-24: issuer now requires an independently supplied pinned policy digest, in addition to recomputing the full gate-job mapping digest; missing, malformed, or mismatching pins fail before any authenticated origin call or HMAC. Draft PR #1048 `2a1be246ab54caabdbcf95e607827fc641b97bf2`; [116/116 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc784a1e112550ce7de62a), one candidate ref update. Critical: trusted CI still must source the pinned digest from independently protected configuration; caller argument alone does not establish the trust boundary. No activation/merge, v0.4.26 unaffected.

- 2026-10-24: isolated issuer now enforces stage-specific GitHub event scope before authenticated job lookup: PR→pull_request, integration→push, release→workflow_dispatch. Wrong stage/event pairs fail closed; [117/117 HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc79911e112550ce7de6ff). Draft PR #1048 candidate `2e06005f5b2a1cb45351e4f98917dbf174cc973a` published in a single ref update. Still requires an independently protected policy source and signing key custody before production; no v0.4.26 CI changes.

- 2026-10-24: isolated issuer now checks full gate-policy mapping schema and safe exact workflow/job identifiers across **all gates**, including unrelated ones, before evidence signing or GitHub API requests; hash equality alone is insufficient. [118/118 HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc79f7046eb82b1ecdb8a3); draft PR #1048 head `6b6ec0c0ee8b0107c3d44d00b9260bdbfb9801a4`, one batched branch update. Trusted policy source and key custody not yet integrated; v0.4.26/develop untouched.

- 2026-10-24: isolated evidence issuer now fails closed by default unless the trusted executor explicitly sets `BASEHARBOR_TRUSTED_ISSUER=enabled`; test setup remains scoped and verifies disabled mode makes no GitHub API calls. [119/119 isolated HF regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc7a68046eb82b1ecdb8cb). Draft PR #1048 `0621ee47f8115cd4811837675c23fe83617595f4`, single batched ref update. **Security note:** environment flag alone is not an authentication boundary; protected CI runner, secret key custody, independent trusted policy source and promotion checks remain required. No change to v0.4.26/develop.

- 2026-10-24: issuer/coverage consistency: origin-bound verifier now requires an independently pinned complete-policy digest and enforces stage-to-GitHub-event mapping before API lookup, matching isolated issuer preconditions. [122/122 tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc8008046eb82b1ecdbaa4), PR #1048 candidate `40ac8a5e3c36bc6143f3c0710f652cbb7ef16aa2`. This is not an independent trusted policy authority: CI must supply the digest from protected configuration; secret custody and end-to-end qualification remain open. No release activation or merge.

- 2026-10-24: added isolated `r27_trusted_policy.py` canonical policy-bytes loader verifying an exact SHA256 digest before parsing, refusing missing pin, altered content, noncanonical JSON and excessive input. [126/126 isolated regressions PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc8138046eb82b1ecdbb01), PR #1048 head `d79db0c4ddbe5775b672a265bacaa2527120ca69`. This is a preparatory loader only: digest and bytes MUST come from independently protected CI configuration; operational wiring, key custody, and required-check E2E remain unimplemented. Draft, no merge or v0.4.26 activation.

- 2026-10-24: added `issue_with_pinned_policy` prototype wrapper: load canonical digest-matched policy bytes and derive job name/workflow from that mapping, refusing caller-supplied mapping/digest/job overrides before calling issuer. [128/128 isolated regression tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc82c0046eb82b1ecdbb62); draft PR #1048 `7f648163842ec424a09f5ab10aad0ab556821154`. The protected source is still a caller-provided input to this prototype API; protected runner injection and key custody are required before production. v0.4.26/develop untouched.

- 2026-10-24: policy-loader integration guard now validates all gate mapping entries before returning a pinned policy to the issuer (safe gate names, exact job names, contained workflow paths, no extra fields). [129/129 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc83e41e112550ce7deb7c), draft PR #1048 `a08cda603bb4b0b5354f38e1141df53e008d6717`; single feature-branch update. Still needs genuinely protected digest source, issuer key isolation and independent E2E/required-check qualification; no v0.4.26/develop changes.

- 2026-10-24: reject duplicate JSON keys at any nesting level in pinned policy loader (gate or job property) before canonical/schema validation, with explicit fail-closed error. [130/130 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc896d046eb82b1ecdbd56). Draft PR #1048 head `1a16ea7f1289d73530fe6b968ab3c743a316d148`. This resolves ambiguity only, not protected-source trust: immutable protected CI policy retrieval, signing key custody, and mandatory E2E qualification remain open. No develop merge or v0.4.26 activation.

- 2026-10-24: isolated #1048 policy loader now has bounded direct file-reading prototype with absolute-path requirement, O_NOFOLLOW on final component, regular-file and size checks, plus explicit symlink and valid file tests. [132/132 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc92ac1e112550ce7df2d2), feature head `684bcc78b0ce2a8675edd3e1aa99f409fa8c0cf0` (code and test commits). **Not production trust:** ancestor path components, owner/permissions, protected executor origin and digest custody remain unverified; this reader is not yet wired as production issuer entrypoint. No merge or v0.4.26 CI activation.

- 2026-10-24: protected policy reader now traverses each path component using directory file descriptors and `O_DIRECTORY|O_NOFOLLOW`, rejects `.` and `..` components, and opens the final file relative to the verified directory descriptor. Symlink-ancestor and traversal regressions added; [134/134 isolated HF tests PASS](https://huggingface.co/jobs/ThunderHawk1080/6adc96ca046eb82b1ecdc2b0). Draft PR #1048 exact head `1b600e2b6a34a0174159ae2c8276f53cf625a87c`. Protected ownership and permissions, trusted digest injection, signer secret isolation and CI E2E remain open; do not promote/merge or alter v0.4.26.
