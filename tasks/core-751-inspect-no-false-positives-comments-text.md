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
blocker: "Independent re-review 5558472659 reproduces seven failing lexical-boundary cases on fcf756e8 (Java comment/literal/whitespace and JS brace/interpolation handling); correct and re-review before source qualification."
resolution: ""
evidence: []
---

- [ ] core-751 · Inspect: avoid false positives from comments and text #task #release/v0-4-x #status/blocked #view/blocked #area/inspect #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-751 inspect import detection)  
    **PR:** [baseharbor#984](https://github.com/mcpdev80/baseharbor/pull/984)  
    **Blocker:** Independent re-review 5558472659 reproduces seven failing lexical-boundary cases on fcf756e8 (Java comment/literal/whitespace and JS brace/interpolation handling); correct and re-review before source qualification.  
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

- 2026-10-17 **Review 5558472659 corrected candidate**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) exact HEAD `c9dae941583cfbfa4bceaa73b37a78f2ffceb79c` extends existing bounded import detector with Java comments/text block/whitespace-aware import scanning, JS block versus object closing-brace classification, and lexical string/comment/regex-aware template interpolation bounds; all prior nine review cases and existing regression tests retained. New 10-case shared direct/EvidenceImport matrix covers seven new reproduced failures and negative controls. [Isolated HF Go preflight](https://huggingface.co/jobs/ThunderHawk1080/6ad395115ccb47ba0f7bb9d8): complete `go test ./internal/repositoryinspect -count=1`, `go vet ./internal/repositoryinspect`, `gofmt -l` all PASS. [Hosted run 39045575706](https://github.com/mcpdev80/baseharbor/actions/runs/39045575706) pending five Inspect checks and authenticated final check. No live tests, self-qualification or merge; #983/#989 unchanged. Independent re-review still required.


- 2026-10-17 **independent re-review: changes required**, source `fcf756e8bc33139d48f5195df57de1cc9e1ed987`, [review 5558472659](https://github.com/mcpdev80/baseharbor/pull/984#pullrequestreview-5558472659). All nine prior counterexamples now independently PASS, and the existing repositoryinspect package passes. Further executable lexical-boundary matrix reproduces seven failing cases in both the direct detector and actual EvidenceImport: Java block-comment/text-block false positives and tab-separated import false negative; JS object-expression division mistaken for regex; template interpolation terminated by braces inside strings, comments or regex. Java line-comment and template-prose controls pass; four JS examples syntax-checked with Node v24.19.0. Go 1.26.9, no live tests or product changes. Fix these three boundary classes together and preserve the corrected prior matrix; #983 source binding remains withheld. Five Inspect gates in CI 39043521651 pass, finalcheck remains unresolved; generic green tests do not override these functional findings.

- 2026-10-17 **complete CI handoff for independent re-review**: exact #984 HEAD `fcf756e8bc33139d48f5195df57de1cc9e1ed987`, [run 39043521651](https://github.com/mcpdev80/baseharbor/actions/runs/39043521651) five Inspect gates all **SUCCESS** (`inspect-gofmt`, `inspect-package-tests`, `inspect-consumer-tests`, `inspect-vet`, `inspect-consumer-build`), plus Trusted Plan, workflow policy and Focused Python SUCCESS; required `PR Selected Checks` **FAILURE** only for independently unresolved source coverage on the two changed repositoryinspect files. Independent review [5558337726](https://github.com/mcpdev80/baseharbor/pull/984#pullrequestreview-5558337726) must re-review/qualify; do not self-approve. [HF validation](https://huggingface.co/jobs/ThunderHawk1080/6ad38ede5ccb47ba0f7bb7b2) on Planning-main `dee3832d2053a3a47b3968b28a718d37f9bbafd6`: render stable, 243 tasks, 0 errors/warnings, 47 planning tests PASS. Task remains blocked for independent content review; no merge, native execution, or unrelated PR changes.


- 2026-10-17: Review [5558337726](https://github.com/mcpdev80/baseharbor/pull/984#pullrequestreview-5558337726) nine cases addressed in one candidate [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) `fcf756e8bc33139d48f5195df57de1cc9e1ed987` (source + direct/EvidenceImport regression matrix). Bounded JS regex/control-boundary, import declaration reset, division and executable template interpolation; Python semicolon/inline-suite/explicit continuation; Java import support preserved. [HF isolated Go preflight](https://huggingface.co/jobs/ThunderHawk1080/6ad38e65c662881452268d6d) verified format, complete repositoryinspect package tests and package vet PASS on the exact candidate. [Hosted CI 39043521651](https://github.com/mcpdev80/baseharbor/actions/runs/39043521651) selecting five Inspect checks: inspect-gofmt, inspect-package-tests, inspect-consumer-tests, inspect-vet, inspect-consumer-build; evaluate exact job results before independent re-review. No source self-qualification or merge. #983/#989 untouched.


- 2026-10-17 **independent content review: changes required**, product HEAD `aabc1347d10b54c10bb156ca9c42937f06f9ed5d`, [review 5558337726](https://github.com/mcpdev80/baseharbor/pull/984#pullrequestreview-5558337726). Reconstructed exact candidate from develop base and verified both changed Git blob IDs against GitHub. Go 1.26.9: all five existing added test functions PASS; nine independent cases FAIL in both the direct detector and actual `detectCapability`/`EvidenceImport` projection. Blocking classes: JS regex after statement blocks/newline-separated control headers and leaked import state; missed require calls in numeric division/template interpolation; missed Python semicolon/inline-suite/continued imports; existing .java source support silently loses real MongoDB imports. JS examples syntax-checked with Node v24.19.0 module parser; Python examples parsed by the standard AST parser. Full reproducers and actual outcomes are in the review. Fix related lexical boundaries together and retain positive/negative controls; no general language engine requested. No live tests, product/policy modifications, source approval or merge. #983 source binding remains withheld until a corrected candidate independently passes content review.

- 2026-10-17 **implementation handoff, source approval pending**: existing [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) exact HEAD `aabc1347d10b54c10bb156ca9c42937f06f9ed5d`. Reviewed lexical token loss in previous source: `&&` and `]` were discarded, enabling false import evidence from `const rx = ready && /import 'mongodb'/;` and `obj[require]('mongodb');`. Existing JS/TS lexer now retains operator and closing bracket tokens consistently and considers expression operators as regex-start contexts. Added table regressions for binary/ternary regex, computed/optional member calls, genuine static/dynamic imports and require, multiline declarations, and division; each case executes both direct detector and real `EvidenceImport` projection; prior tests retained. [Actions 39033901985](https://github.com/mcpdev80/baseharbor/actions/runs/39033901985), attempt 1, records **SUCCESS** for all five `inspect-gofmt`, `inspect-package-tests`, `inspect-vet`, `inspect-consumer-tests`, `inspect-consumer-build`. The authoritative `PR Selected Checks` **FAILURE** is solely `coverage-unresolved` for `capability_detection_runtime.go` and `capability_import_detection_test.go`. Independent content review and source binding remain necessary; **no** self-approval, policy #983 edit or merge. No local end-to-end checkout claim; Planning metadata/status unchanged.

- 2026-10-17 **verified focused implementation handoff**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact source `6da9b7b513e6c2e586238a653ff08001ee5b48d4`, [Actions 39033245952](https://github.com/mcpdev80/baseharbor/actions/runs/39033245952), attempt 1. All five `inspect-gofmt`, `inspect-package-tests`, `inspect-vet`, `inspect-consumer-tests` and `inspect-consumer-build` **SUCCESS**. Required `PR Selected Checks` **FAILURE**, solely source `coverage-unresolved` for detector and direct regression file; policy #983 remains unchanged and independently owned. This candidate includes shared static/dynamic-import/require matrix against direct detector and `EvidenceImport` (normal, multiline, interspersed comments, member exclusions), with previous fixtures preserved. First intermediate [39033174621](https://github.com/mcpdev80/baseharbor/actions/runs/39033174621) identified gofmt alignment issue subsequently corrected. Implementation complete for independent source review; no implementer content approval, source qualification or merge. Planning generated status/metadata unchanged; no local Planning `render/check` claimed.

- 2026-10-17 implementation continuation, **review pending**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) exact head `6da9b7b513e6c2e586238a653ff08001ee5b48d4` (substantive source `c8d37a4d782c1fe7e51f21cbb2111d201c3006cf` plus gofmt alignment). Module call token matching now ignores newlines between `import` / `require`, `(`, quoted argument and `)`; comments are excluded by lexer; member `.import()`/`.require()` are excluded, static imports/re-exports retained. Shared 15-case matrix runs both direct detector and real `EvidenceImport` projection, covering static/dynamic/require normal, multiline, comments, member calls plus re-export and optional-member negatives; prior tests retained. Initial [Actions 39033174621](https://github.com/mcpdev80/baseharbor/actions/runs/39033174621) showed `inspect-gofmt` failure, corrected by the second commit. New [Actions 39033245952](https://github.com/mcpdev80/baseharbor/actions/runs/39033245952) is pending; no green claim until all five checks complete. Source coverage qualification remains independent; #983 untouched, no merge or self-approval. The implementer did not execute local pre-push gofmt/tests/vet in this connector-only environment.

- 2026-10-17 completed focused CI evidence for implementation candidate `80cf1571e7c018651a7a8fb455e768812c7db0ce`: [Actions run 39032882080](https://github.com/mcpdev80/baseharbor/actions/runs/39032882080), attempt 1, shows `inspect-gofmt`, `inspect-package-tests`, `inspect-vet`, `inspect-consumer-tests` and `inspect-consumer-build` all **SUCCESS**. Authoritative `PR Selected Checks` **FAILURE** only on `coverage-unresolved` for `internal/repositoryinspect/capability_detection_runtime.go` and `internal/repositoryinspect/capability_import_detection_test.go`; no failed focused test. Implementation review candidate only, independently review exact new source and qualify coverage separately, no self-approval or merge.

- 2026-10-17 implementation continuation (no source approval): existing [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) source `80cf1571e7c018651a7a8fb455e768812c7db0ce` fixes regex-literal `else`/`do` statement starts while retaining newline-separated static `import`/`export ... from` declarations; newline alone no longer ends the static import state, and newlines are skipped when determining whether `/` begins a regexp without indiscriminately treating newline-division as regexp. Added direct and actual `EvidenceImport` positive/negative cases for `else`, newline-separated imports/re-exports, comments, division and real imports; existing tests retained. Same exact source is under focused [Actions 39032882080](https://github.com/mcpdev80/baseharbor/actions/runs/39032882080); do not assert all five green until jobs conclude. No local pre-push run claimed, no #983 edit, no merge or implementer self-approval; independent source review still required. Task owner/blocked state unchanged.

- 2026-10-17 **IMPLEMENTATION HANDOFF — independent review pending**. Following assigned role transfer (review finding [6233783222](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233783222)), existing product [PR #984](https://github.com/mcpdev80/baseharbor/pull/984) HEAD `94f83f5afec9a48e8d6b07628b7a244711df72a0` fixes regex literals after control-condition parentheses with a control-paren stack in `jsModuleTokens`, distinguishing if/while/for statement bodies from ordinary function calls, expression grouping and division. Same commit adds direct syntax and integrated `EvidenceImport` regressions for if/while/for, nested controls, division and genuine imports; prior regression cases remain. The implementation and test modifications were batched in one commit; local pre-push gofmt/tests/vet were not run in the connector-only environment, but exact hosted [CI 39032328199](https://github.com/mcpdev80/baseharbor/actions/runs/39032328199), attempt 1, reports all five selected Inspect checks **SUCCESS** (`inspect-gofmt`, `inspect-package-tests`, `inspect-vet`, `inspect-consumer-tests`, `inspect-consumer-build`). Required `PR Selected Checks` **FAILURE** solely `coverage-unresolved` for `internal/repositoryinspect/capability_detection_runtime.go` and `internal/repositoryinspect/capability_import_detection_test.go`; this is an independent source-qualification prerequisite, not a test pass. This session **implemented** the fix and must not approve/qualify its own product contents or alter policy [#983](https://github.com/mcpdev80/baseharbor/pull/983). Blocked task status and foreign planning metadata preserved. No merge.

- 2026-10-17 implementation handoff claim: following Maintainer reassignment, this session takes **implementation only** of review finding [6233783222](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233783222) on existing #984 at `4b7a0371dc6dada7eb283290d4ad9bac62efc018`. Preserve the existing owner and blocker; implement bounded control-flow regex lexical fix and tests, run five selected Inspect checks, and hand off a new immutable source head for a separate independent reviewer. This does **not** accept core-751 or authorize #983 changes or a merge.

- 2026-10-17 **revised independent review candidate**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact product HEAD `4b7a0371dc6dada7eb283290d4ad9bac62efc018`, base `d54ac358fb6a6b256164ac2689a33e981c013baa`. Addresses review [#6233499789](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233499789): JS/TS regex literals after `return`, `throw`, `case`, `yield` and grouped expressions no longer imply imports; member method `obj.require(...)` and optional member calls are excluded; bare CommonJS `require(...)` and dynamic `import(...)` remain recognized; Python comma-separated imports with aliases detect every module. Regression cases exercise both direct syntax recognition and actual `EvidenceImport`, including the original guided MongoDB prompt. The actual PR diff remains exactly `internal/repositoryinspect/capability_detection_runtime.go` (modified) plus `internal/repositoryinspect/capability_import_detection_test.go` (added); dependency metadata and bounded read-only scanning remain untouched. Exact [CI run 39030351947](https://github.com/mcpdev80/baseharbor/actions/runs/39030351947): `inspect-gofmt`, `inspect-vet`, `inspect-package-tests`, `inspect-consumer-tests`, `inspect-consumer-build` all **SUCCESS**. `PR Selected Checks` **FAILURE**, solely `coverage-unresolved` for those two unreviewed files; independent immutable source binding/acceptance is still required before merge. #983 remains unchanged. No self-qualification or merge.


- 2026-10-17 **complete candidate for independent content review**: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact product HEAD `f6538550b026f99d83fdf811ac9243eaeb5195ff`, `develop` base `d54ac358fb6a6b256164ac2689a33e981c013baa`. Actual diff contains exactly `internal/repositoryinspect/capability_detection_runtime.go` (modified) and `internal/repositoryinspect/capability_import_detection_test.go` (added). Source evidence now derives from real Python import/from, Go parsed imports, and JS/TS import/from/require/dynamic-import syntax, excluding prompts, comments, strings and regex literals; package dependency metadata and bounded read-only scanner are unchanged. Isolated local syntax tests and `gofmt` passed, and [focused CI run 39029904829](https://github.com/mcpdev80/baseharbor/actions/runs/39029904829) confirms **SUCCESS** for `inspect-gofmt`, `inspect-vet`, `inspect-package-tests`, `inspect-consumer-tests`, `inspect-consumer-build`. The authoritative `PR Selected Checks` is **FAILURE** with `coverage-unresolved` for exactly these two files (final job `117388281945`), not a functional failure. This is a review candidate only; exact immutable source-content binding and independent coverage acceptance remain prerequisites to merge. No policy/workflow edits, no #983 merge and no core-894/core-918 changes.


- 2026-10-17 implementation candidate: [PR #984](https://github.com/mcpdev80/baseharbor/pull/984), exact SHA `4014057e4b0e1319bf3ea7e5bdee8d66cc7a956b`, base `d54ac358fb6a6b256164ac2689a33e981c013baa`, limited to `internal/repositoryinspect/capability_detection_runtime.go` and `capability_import_detection_test.go`. Python/Go/JS/TS syntax-aware detection plus positive/negative tests. Candidate creation explicitly authorized despite unresolved CI prerequisite; no merge/acceptance until immutable source binding and independently qualified mandatory checks. Existing task remains blocked, #983 remains under independent review. Run 39029266030 is the first targeted candidate CI.


- CI prerequisite: [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md) owns trusted import-detector qualification. core-751 remains blocked until its independent acceptance; no product import-detection code may claim resolved coverage before immutable reviewed-source qualification.


- CI precondition: `scripts/pr-gate-plan.py` recognizes only `reconcile.go` and `reconcile_default_instance_test.go` as trusted Inspect coverage; other `internal/repositoryinspect/*.go`, including the affected detector, resolve to `inspect-implementation-unresolved` despite selecting inspect package/vet/format and consumer checks. A dedicated trusted qualification is required before a normal green PR finalcheck. Source reproduction: `capability_detection_runtime.go::detectCapability` uses whole-file substring detection for imports, which matches the MongoDB demo harness prompt. No product changes or PR were created.


- 2026-10-17 claim: assigned core-751 exclusively. Trusted `develop` planner `scripts/pr-gate-plan.py` only resolves `internal/repositoryinspect/reconcile.go` and `reconcile_default_instance_test.go`; required import detector file `internal/repositoryinspect/capability_detection_runtime.go` and its regression tests are classified `inspect-implementation-unresolved` even when `inspect-package-tests`, `inspect-vet`, `inspect-gofmt` and the CLI inspect consumer checks are selected. This is a concrete pre-implementation coverage gap, not a permission to self-exempt. No unrelated sources or CI policy changes are authorized.


- Earlier fix branch `fix/751-capability-import-noise-v0421` `aabd82ff6cb7f6a55f33001638e51e53dfc7f2a8`. Branch hygiene (2026-10-15): divergent earlier fix branches were inventoried; neither full integration nor safe deletion was proven by ancestry. Compare useful changes against the current contract; no blanket merge/rebase. The remote branches were later removed in the [maintenance cleanup](core-909-maintenance-remove-superseded-branches.md); their original commits are preserved in the Maintainer's local mirror backup.
