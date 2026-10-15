# CardBoard presentation work

Assigned directly by the Maintainer on 2026-10-16. Owner: Codex (planning presentation session).

Owned scope: CardBoard settings, scoped CSS, the existing plan renderer/validator and focused tests, generated card previews/readiness views, and concise vault usage documentation. Preserve other task owners, source metadata, acceptance and live handoffs. No product code, release qualification or task acceptance is part of this work.

Implementation uses an isolated checkout and a small PR. Derived previews and board grouping must be validated against canonical task notes; no second writable task-status authority.

## Handoff

- Implemented generated indented card previews (actual owner, optional priority, PR links, blocker and unfinished prerequisites), derived `#view/…` routing tags, a Next board and ready-task list, and a scoped compact CSS snippet. Canonical statuses, task ownership, acceptance and historical handoffs are preserved.
- `python3 -m unittest discover -s scripts/tests`: 32 PASS, including prerequisite acceptance vs mere PR presence, generated-preview/readiness tampering, status refresh, unset/invalid priority and text injection. `plan.py render` is idempotent; `plan.py check`: 0 errors, 4 existing dependency warnings.
- CardBoard 0.7.9 note parsing, settings schema and DOM/CSS selectors were inspected in the upstream source. A browser fixture was prepared but could not be rendered because the available Playwright browser download was invalid; no screenshot or native Obsidian UI validation is claimed.
- After pulling the shared configuration, reload CardBoard; enable `baseharbor-board` in Obsidian Settings → Appearance → CSS snippets. Theme/appearance preferences are intentionally left local. Run `render` after canonical edits; UI changes do not execute Python automatically and stale previews are rejected by the validator.
- Publish through the dedicated board-presentation PR; no product/runtime tests, task acceptance or release operation is part of this change.
