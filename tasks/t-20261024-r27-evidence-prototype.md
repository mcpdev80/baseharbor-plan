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
