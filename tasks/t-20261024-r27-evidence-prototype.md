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
