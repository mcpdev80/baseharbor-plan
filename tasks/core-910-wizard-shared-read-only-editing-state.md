---
id: core-910
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: mcpdev80 (session 2, preparatory implementation)
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#934"]
sources: ["mcpdev80/baseharbor#910"]
source_updated: "2026-10-15T20:29:55Z"
labels: [area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-910 · Wizard: provide shared read-only editing state #task #release/v0-4-26 #status/review

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Required by:** [core-911](core-911-app-edit-load-existing-selections.md), [core-912](core-912-wizard-needs-first-selection.md), [core-913](core-913-wizard-compatible-providers-same-view.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Owner:** mcpdev80 (session 2, preparatory implementation)  
**PRs:** [baseharbor#934](https://github.com/mcpdev80/baseharbor/pull/934)  
**Source:** [baseharbor#910](https://github.com/mcpdev80/baseharbor/issues/910)
<!-- /generated:links -->

## Goal

New/Edit and the machine adapters consume the same short-lived state from existing authorities. Lane: foundation.

## Scope

- In scope: existing development/application read paths; narrow new `guided_application` context files and focused tests.
- Out of scope: TUI files, command registry files.

## Acceptance

- Uses existing manifest/Target/binding/footprint/consequence types; no second resolver, no registry and no persisted wizard file.
- Provides inputs/outputs and compiling read-only adapters with fixtures for follow-up tasks; existing truth is not replaced by dummy/stub results.
- Portable capability intent, system-owned ID and Target-specific provider preference stay separate; a snapshot/plan revision is passed on verifiably.

## Required checks

- Package/contract tests: read-only, wrong Target, unknown inputs, no secrets in output. No containers.

## Dependencies and file ownership

- Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first. No other product task.
- Owns the new guided-application context files.

## Handoff

- 2026-10-15 — **Review handoff, preparatory implementation only.** Draft [baseharbor PR #934](https://github.com/mcpdev80/baseharbor/pull/934), verified immutable source `574488ba3ae9b3c07ac78e057f7abc5168d69e5a`. [GitHub Actions run 38813614933](https://github.com/mcpdev80/baseharbor/actions/runs/38813614933), **job `PR934 · Exact Guided Go`: SUCCESS**. Exact SHA assertion PASS; complete-file `gofmt` PASS; focused `TestGuided` PASS; `internal/application/... ./contracts/...` PASS; `go vet ./cmd/baha` PASS; `go build ./cmd/baha` PASS. Workflow policy PASS. **Separate general `validate` job FAILED**, so **the overall workflow is not green**; its diagnostic formatting output came from the pilot validation branch, not the immutable #934 checkout. The temporary [pilot PR #936](https://github.com/mcpdev80/baseharbor/pull/936) must not be merged. No release/runtime qualification or claim that core-893 selected-check enforcement is accepted. #934 remains Draft, awaiting Maintainer review and the remaining unqualified core-893 and core-895 prerequisites before integration/final acceptance; core-896 is qualified and merged through [PR #932](https://github.com/mcpdev80/baseharbor/pull/932) at `fb229964dd277700e1c7ec815db42fa19c3ba2bd`. No further product edits are authorized without concrete review findings.

- Live migration review: PR #934 head `03088e52f0b98b4106f703647ca02dae49f37e0e`; draft/preparatory work remains unaccepted. The current PR head supersedes older SHA assertions in its body. Preserve the existing owner, branch and PR.

- 2026-10-15T20:29Z (issue comment): session 2 resumes ownership for **preparatory implementation only**, superseding the read-only restriction; isolated draft PR #934 (head `ba3b3e1ef4` at check time) with two dedicated read-adapter files in `cmd/baha` and tests. Integration and final acceptance stay blocked on the qualified foundation (core-893, core-895, core-896). No TUI, CLI/MCP registration, lifecycle mutation or repositoryinspect changes. Draft PR #936 runs a temporary CI pilot on its source.
- 2026-10-15 comment: a session took #910 for **read-only preparation only** (inspect authorities, write an implementation proposal). No implementation or PR until the foundation is qualified and the Maintainer gives a new explicit assignment.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
