---
id: t-20261022-r27-evidence-publisher
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md"]
---

- [ ] t-20261022-r27-evidence-publisher · evidence publisher #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **PR:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->


# Evidence publisher: archive actual proof in baseharbor-plan

## Goal
Publish required, sanitized evidence payloads and a checksummed manifest to evidence/<release>/<candidate-id>/<run-id>/ in baseharbor-plan. GitHub Actions links alone are not evidence retention.

## Scope
- Reuse existing trusted CI inputs and artifact producers; upload only bounded required proof after completion, not every verbose log.
- Never overwrite an existing evidence ID; reject collisions and conflicting hashes. Publish manifest only when all payloads are present; use a dedicated branch/PR or collision-safe integration rather than force pushes.
- Preserve concurrent plan edits, avoid direct worker writes to protected main, use least-privilege short-lived credentials and scrub secrets before any commit.
- Keep run failures and upload failures distinguishable; failure to archive cannot masquerade as a qualified retained proof.

## Acceptance
- Real production-path tests for parallel writers, retry/idempotency, partial upload, duplicate ID, secret redaction and branch/run deletion simulation.
- Exact SHA, digest and trusted-run provenance preserved. Cheap targeted CI before independent review.
- No unrelated CI trust policy changes, no full release matrix.

## Mandatory zero-touch integration
- CI generates the manifest and sanitized required artifacts automatically on the ordinary human/agent/contributor PR path; no manual preparation or copying is allowed.
- Trusted post-run publisher handles fork PRs without exposing planning write tokens to untrusted code.
- On successful archival, automatically associate the immutable evidence reference with its task and PR via conflict-safe planning updates. Retrying after concurrent edits must preserve other authors' changes.
- Missing archive or linking reports an actionable status and fails closed for gates requiring retained evidence.
> Pre-research evidence retained (o64/o66/o68, console-2 PR #8, nc-3 PR pending): v0.4.26 ist noch nicht geschlossen (D2/W1/verify pending) => Release-27-Arbeit formal zurueck auf waiting, Outcome-Referenzen bleiben verlinkt.
