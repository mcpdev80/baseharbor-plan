---
id: core-751
type: bug
release: v0.4.x
version: ""
parent: v0.4.x
owner: mcpdev80
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#751"]
source_updated: "2026-10-15T16:51:27Z"
labels: [kind/bug, area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-751 · Inspect: avoid false positives from comments and text #task #release/v0-4-x #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80  
**PRs:** none  
**Source:** [baseharbor#751](https://github.com/mcpdev80/baseharbor/issues/751)
<!-- /generated:links -->

## Goal

Capability import evidence comes only from real import/require/reference syntax, not from prose, comments, prompts, regexes or string literals.

## Scope

- Bug: `baha app inspect` reports `database.document` as `suggested` for `baseharbor-demo`, which uses no document database. Reproducer: demo commit `5e17de4dbf0050e7ab34398ac6e11fd8533f0365`, `tests/guided/drive.py` contains `Rule(r"MongoDB-compatible document database instances ...", ...)`; the detector scans every source file with raw substring matching (`if isSourceFile(base) && containsAny(lower, signals.imports)`), so the literal becomes false `EvidenceImport`. Still visible at `1b1ae323` in `internal/repositoryinspect/capability_detection_runtime.go`.
- Test/E2E harness source must not imply production capabilities merely because it contains provider/client names.

## Acceptance

- `MongoDB-compatible` prompt text does not suggest `database.document`.
- Real Python `import pymongo` / `from pymongo ...` is detected.
- Real Go imports such as mongo-driver/pgx remain detected.
- Real JS/TS import/require references remain detected.
- Comments and unrelated strings do not create import evidence.
- Existing dependency metadata detection remains unchanged.
- Source scanning remains bounded/read-only.
- The source's "integrate into the active v0.4.21 release line" item is historical; the fix lands as a normal task PR against develop.

## Required checks

- Focused repositoryinspect tests and `go vet`.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Related: core-750.

## Handoff

- Earlier fix branch `fix/751-capability-import-noise-v0421` `aabd82ff6cb7f6a55f33001638e51e53dfc7f2a8`. Branch hygiene (2026-10-15): divergent earlier fix branches were inventoried; neither full integration nor safe deletion was proven by ancestry. Compare useful changes against the current contract; no blanket merge/rebase. The remote branches were later removed in the [maintenance cleanup](core-909-maintenance-remove-superseded-branches.md); their original commits are preserved in the Maintainer's local mirror backup.
