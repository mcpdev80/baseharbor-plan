---
id: t-20261022-r27-evidence-verifier
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-publisher, t-20261022-r27-evidence-resolver]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-verifier · evidence verifier #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task


# Evidence verifier: retained does not mean qualified

## Goal
Bind archived evidence to the exact current trusted plan, source/integration SHA, check requirements and accepted run identity without weakening existing finalcheck.

## Scope
- Verify checksums, authenticated provenance, run outcome, policy version and candidate binding against existing trusted authorities.
- Fail closed on absent evidence, changed source, missing mandatory checks, mismatched integration SHA, stale/invalid trust inputs or tampering.
- Independently review trust-affecting changes. Publisher author cannot self-qualify evidence.

## Acceptance
- Production-path negative regression matrix plus genuine accepted-path check.
- Final verifier accepts archived proof even when the source workflow artifact has expired, only if every current qualification predicate holds.
- No broad CI path exemptions, self-review or silent green reuse.
