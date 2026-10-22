---
id: t-20261022-r27-evidence-publisher
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-plan]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

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
