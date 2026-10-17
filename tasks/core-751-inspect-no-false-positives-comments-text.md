---
id: core-751
areas: [inspect]
type: bug
release: v0.4.x
version: ""
parent: v0.4.x
owner: "mcpdev80 (core-751 inspect import detection)"
depends_on: [core-893, core-895, core-896, t-20261017-inspect-import-ci-coverage]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#984]
sources: ["mcpdev80/baseharbor#751"]
source_updated: "2026-10-15T16:51:27Z"
labels: [kind/bug, area/dx, area/compatibility]
blocker: "Trusted PR planner classifies capability_detection_runtime.go and import detection regression files as inspect-implementation-unresolved; required focused coverage is not independently qualified."
resolution: ""
evidence: []
---

- [ ] core-751 · Inspect: avoid false positives from comments and text #task #release/v0-4-x #status/blocked #view/blocked #area/inspect #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-751 inspect import detection)  
    **PR:** [baseharbor#984](https://github.com/mcpdev80/baseharbor/pull/984)  
    **Blocker:** Trusted PR planner classifies capability\_detection\_runtime.go and import detection regression files as inspect-implementation-unresolved; required focused coverage is not independently qualified.  
    **Needs:** [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md)  
**Owner:** mcpdev80 (core-751 inspect import detection)  
**Priority:** not set  
**PRs:** [baseharbor#984](https://github.com/mcpdev80/baseharbor/pull/984)  
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

- Candidate implementation and local/focused validation are expressly permitted while the CI prerequisite remains under independent review. The blocker prevents acceptance and merge, not code authoring or test execution. Immutable content qualification and authenticated green mandatory finalcheck are required before either acceptance or merge.

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Related: core-750.

## Handoff

- 2026-10-17 **IMPLEMENTATION HANDOFF — independent review pending**. Following assigned role transfer (review finding [6233783222](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233783222)), existing product [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) HEAD `94f83f5afec9a48e8d6b07628b7a244711df72a0` fixes regex literals after control-condition parentheses with a control-paren stack in `jsModuleTokens`, distinguishing if/while/for statement bodies from ordinary function calls, expression grouping and division. Same commit adds direct syntax and integrated `EvidenceImport` regressions for if/while/for, nested controls, division and genuine imports; prior regression cases remain. The implementation and test modifications were batched in one commit; local pre-push gofmt/tests/vet were not run in the connector-only environment, but exact hosted [CI 39032328199](https://github.com/mcpdev80/baseharbor/actions/runs/39032328199), attempt 1, reports all five selected Inspect checks **SUCCESS** (`inspect-gofmt`, `inspect-package-tests`, `inspect-vet`, `inspect-consumer-tests`, `inspect-consumer-build`). Required `PR Selected Checks` **FAILURE** solely `coverage-unresolved` for `internal/repositoryinspect/capability_detection_runtime.go` and `internal/repositoryinspect/capability_import_detection_test.go`; this is an independent source-qualification prerequisite, not a test pass. This session **implemented** the fix and must not approve/qualify its own product contents or alter policy [#983](https://github.com/mcpdev80/baseharbor/pull/983). Blocked task status and foreign planning metadata preserved. No merge.

- 2026-10-17 implementation handoff claim: following Maintainer reassignment, this session takes **implementation only** of review finding [6233783222](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233783222) on existing #984 at `4b7a0371dc6dada7eb283290d4ad9bac62efc018`. Preserve the existing owner and blocker; implement bounded control-flow regex lexical fix and tests, run five selected Inspect checks, and hand off a new immutable source head for a separate independent reviewer. This does **not** accept core-751 or authorize #983 changes or a merge.

- 2026-10-17 **revised independent review candidate**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact product HEAD `4b7a0371dc6dada7eb283290d4ad9bac62efc018`, base `d54ac358fb6a6b256164ac2689a33e981c013baa`. Addresses review [#6233499789](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233499789): JS/TS regex literals after `return`, `throw`, `case`, `yield` and grouped expressions no longer imply imports; member method `obj.require(...)` and optional member calls are excluded; bare CommonJS `require(...)` and dynamic `import(...)` remain recognized; Python comma-separated imports with aliases detect every module. Regression cases exercise both direct syntax recognition and actual `EvidenceImport`, including the original guided MongoDB prompt. The actual PR diff remains exactly `internal/repositoryinspect/capability_detection_runtime.go` (modified) plus `internal/repositoryinspect/capability_import_detection_test.go` (added); dependency metadata and bounded read-only scanning remain untouched. Exact [CI run 39030351947](https://github.com/mcpdev80/baseharbor/actions/runs/39030351947): `inspect-gofmt`, `inspect-vet`, `inspect-package-tests`, `inspect-consumer-tests`, `inspect-consumer-build` all **SUCCESS**. `PR Selected Checks` **FAILURE**, solely `coverage-unresolved` for those two unreviewed files; independent immutable source binding/acceptance is still required before merge. #983 remains unchanged. No self-qualification or merge.


- 2026-10-17 **complete candidate for independent content review**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact product HEAD `f6538550b026f99d83fdf811ac9243eaeb5195ff`, `develop` base `d54ac358fb6a6b256164ac2689a33e981c013baa`. Actual diff contains exactly `internal/repositoryinspect/capability_detection_runtime.go` (modified) and `internal/repositoryinspect/capability_import_detection_test.go` (added). Source evidence now derives from real Python import/from, Go parsed imports, and JS/TS import/from/require/dynamic-import syntax, excluding prompts, comments, strings and regex literals; package dependency metadata and bounded read-only scanner are unchanged. Isolated local syntax tests and `gofmt` passed, and [focused CI run 39029904829](https://github.com/mcpdev80/baseharbor/actions/runs/39029904829) confirms **SUCCESS** for `inspect-gofmt`, `inspect-vet`, `inspect-package-tests`, `inspect-consumer-tests`, `inspect-consumer-build`. The authoritative `PR Selected Checks` is **FAILURE** with `coverage-unresolved` for exactly these two files (final job `117388281945`), not a functional failure. This is a review candidate only; exact immutable source-content binding and independent coverage acceptance remain prerequisites to merge. No policy/workflow edits, no #983 merge and no core-894/core-918 changes.


- 2026-10-17 implementation candidate: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact SHA `4014057e4b0e1319bf3ea7e5bdee8d66cc7a956b`, base `d54ac358fb6a6b256164ac2689a33e981c013baa`, limited to `internal/repositoryinspect/capability_detection_runtime.go` and `capability_import_detection_test.go`. Python/Go/JS/TS syntax-aware detection plus positive/negative tests. Candidate creation explicitly authorized despite unresolved CI prerequisite; no merge/acceptance until immutable source binding and independently qualified mandatory checks. Existing task remains blocked, #983 remains under independent review. Run 39029266030 is the first targeted candidate CI.


- CI prerequisite: [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md) owns trusted import-detector qualification. core-751 remains blocked until its independent acceptance; no product import-detection code may claim resolved coverage before immutable reviewed-source qualification.


- CI precondition: `scripts/pr-gate-plan.py` recognizes only `reconcile.go` and `reconcile_default_instance_test.go` as trusted Inspect coverage; other `internal/repositoryinspect/*.go`, including the affected detector, resolve to `inspect-implementation-unresolved` despite selecting inspect package/vet/format and consumer checks. A dedicated trusted qualification is required before a normal green PR finalcheck. Source reproduction: `capability_detection_runtime.go::detectCapability` uses whole-file substring detection for imports, which matches the MongoDB demo harness prompt. No product changes or PR were created.


- 2026-10-17 claim: assigned core-751 exclusively. Trusted `develop` planner `scripts/pr-gate-plan.py` only resolves `internal/repositoryinspect/reconcile.go` and `reconcile_default_instance_test.go`; required import detector file `internal/repositoryinspect/capability_detection_runtime.go` and its regression tests are classified `inspect-implementation-unresolved` even when `inspect-package-tests`, `inspect-vet`, `inspect-gofmt` and the CLI inspect consumer checks are selected. This is a concrete pre-implementation coverage gap, not a permission to self-exempt. No unrelated sources or CI policy changes are authorized.


- Earlier fix branch `fix/751-capability-import-noise-v0421` `aabd82ff6cb7f6a55f33001638e51e53dfc7f2a8`. Branch hygiene (2026-10-15): divergent earlier fix branches were inventoried; neither full integration nor safe deletion was proven by ancestry. Compare useful changes against the current contract; no blanket merge/rebase. The remote branches were later removed in the [maintenance cleanup](core-909-maintenance-remove-superseded-branches.md); their original commits are preserved in the Maintainer's local mirror backup.
