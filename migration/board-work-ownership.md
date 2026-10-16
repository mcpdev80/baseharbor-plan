# CardBoard presentation work

Assigned directly by the Maintainer on 2026-10-16. Owner: Codex (planning presentation session).

Owned scope: CardBoard settings, scoped CSS, the existing plan renderer/validator and focused tests, generated card previews/readiness views, and concise vault usage documentation. Preserve other task owners, source metadata, acceptance and live handoffs. No product code, release qualification or task acceptance is part of this work.

Historical implementation used an isolated checkout and a small PR. The Maintainer superseded that convention on 2026-10-16: publish planning updates directly on `main`; branches/PRs require an explicit request. Derived previews and board grouping must be validated against canonical task notes; no second writable task-status authority.

## Handoff

- Implemented generated indented card previews (actual owner, optional priority, PR links, blocker and unfinished prerequisites), derived `#view/…` routing tags, a Next board and ready-task list, and a scoped compact CSS snippet. Canonical statuses, task ownership, acceptance and historical handoffs are preserved.
- `python3 -m unittest discover -s scripts/tests`: 32 PASS, including prerequisite acceptance vs mere PR presence, generated-preview/readiness tampering, status refresh, unset/invalid priority and text injection. `plan.py render` is idempotent; `plan.py check`: 0 errors, 4 existing dependency warnings.
- CardBoard 0.7.9 note parsing, settings schema and DOM/CSS selectors were inspected in the upstream source. A browser fixture was prepared but could not be rendered because the available Playwright browser download was invalid; no screenshot or native Obsidian UI validation is claimed.
- After pulling the shared configuration, reload CardBoard; enable `baseharbor-board` in Obsidian Settings → Appearance → CSS snippets. Theme/appearance preferences are intentionally left local. Run `render` after canonical edits; UI changes do not execute Python automatically and stale previews are rejected by the validator.
- [PR #4](https://github.com/mcpdev80/baseharbor-plan/pull/4) merged at `c653ed55ddc7fd6dd820e168eb1f3a3106a112d8`; its exact source `595ace1c6030f5e9c73f551a7a425106e62b72f4` passed the GitHub `Plan · validate` check. All 68 canonical task records were independently compared before publication: metadata, statuses, acceptance and historical handoffs are identical after removing generated presentation. No product/runtime qualification, task acceptance or release operation is claimed. Implementation handoff complete; the real Obsidian view still needs the local snippet enabled.

## Follow-up assignment

Maintainer assigned visible area/kind badges and a derived release-roadmap presentation on 2026-10-16. Owner: Codex (planning presentation session), implementation handed off. Scope extends this presentation task only: renderer, validator, focused tests, board settings, CSS and concise navigation; no changes to product task ownership, acceptance or release scope.

### Follow-up verification

Visible `area`/`kind` badges are derived from optional `areas` and existing `type`; all 69 existing notes received explicit topic metadata only. A generated Roadmap board provides one read-only release/series card with maintained release status, accepted task counts, blockers and scope/task links. No dates, qualification or acceptance are inferred. `plan.py check`: 0 errors, 4 existing prerequisite warnings. 37 unit tests pass, including topic tampering, invalid topics, roadmap edits, acceptance-vs-review and board schema. Rendering is idempotent. Other task fields, status and handoffs are unchanged. Native Obsidian verification remains with the local vault. Follow-up merged in [PR #5](https://github.com/mcpdev80/baseharbor-plan/pull/5) at `9e60e4f73620ae7f58a3593243973558a4a41b7a`. Exact source `36c0a3596ec66a698ddd2b66b4937955e7789423` passed GitHub `Plan · validate` and was independently fetched for 37 passing unit tests and the validator. Implementation handoff complete; actual local Obsidian UI remains to verify.

## Current-board correction

Assigned by Maintainer 2026-10-16; owner Codex (planning presentation session), implementation complete. Restore a visible Planned column covering every canonical planned task, keep readiness as card detail and in Next. Preserve all product task owners, prerequisites, acceptance and other sessions' handoffs.

Correction verified: Current has Planned/Active/Review/Blocked/Closed; every canonical planned card remains visible regardless of readiness, with explicit waiting/needs detail. Next still separates readiness. 38 unit tests pass; validator: zero errors, four existing dependency warnings. Canonical task records independently compared unchanged. No task or prerequisite is accepted by this presentation correction.

## Live planning publication correction

Maintainer directed immediate planning publication on `main` on 2026-10-16. AGENTS and WORKFLOW now require direct-main updates with concurrent-change preservation, rendering/validation and no force-push. Existing branch content must be integrated if still relevant, then the branch removed. Product task acceptance and product PR rules are unchanged.
