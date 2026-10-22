---
id: t-20261022-r27-evidence-contract
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-plan]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-contract · evidence contract #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task


# Evidence contract: retained, source-bound, independent of CI runs

## Goal
Define the smallest durable evidence contract using the existing baseharbor-plan evidence/ tree. No new evidence server, CI platform, database or mandatory S3 service. A deleted feature branch, workflow run or expired artifact must not erase an already archived proof.

## Scope
- Specify unique run/candidate IDs, source and integration SHA, workflow identity, required check identity, attempt, timestamp, status, payload paths, SHA-256 checksums, trust/provenance and manifest schema.
- Distinguish archived existence from current candidate qualification. Preserve trusted planner/executor/finalcheck authorities; no green carryover on changed source or policy.
- Set append-only publication conventions, bounded sizes, redaction, access policy, retention, protected planning branch and independent backup limits. Ordinary Git history is not immutable WORM; no absolute deletion guarantee.
- Define independent publisher, resolver and verifier contracts with negative-case behavior. Existing evidence and concurrent planning writers must be preserved.
- Assign source ownership and independent CI/trust review; no product/runtime mutation.

## Acceptance
- Schema fixtures and validation cover wrong SHA, tampered payload, missing blob, stale attempt, wrong check identity and absent provenance.
- Reviewer accepts threat model and repository-size/secret-exposure bounds before publisher work.
- Planning generator/render/check passes; exact revision handoff recorded.

## Parallel ownership
Any qualified Codeman worker, ChatGPT/Codex session or external contributor may claim this task. Claims are per task/write set, not exclusive to Codeman. Separate reviewer for trust-sensitive changes.
