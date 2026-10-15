# Proposed entry-point updates in product repositories

**Prepared as draft PRs; not merged or activated.** Existing issue authority remains until the explicit planning-authority decision is accepted on `main`. No process rules are added to any product README. Line numbers refer to `mcpdev80/baseharbor` develop at `bf69ad0a37fcec12958992d4826e4f8d14c13ba6`.

## mcpdev80/baseharbor

| File | Current | Proposed |
| --- | --- | --- |
| `AGENTS.md:23` | "Planned work and release evidence: Roadmap, the task's issue/PR and latest comments, internal audits" | "Planned work: the task note in [baseharbor-plan](https://github.com/mcpdev80/baseharbor-plan) (start at its `AGENTS.md`); release evidence: the task's PR and [internal audits](https://github.com/mcpdev80/baseharbor/tree/develop/docs/internal)" |
| `CONTRIBUTING.md:22` | "Looking for something to work on? Open issues" | Link to `baseharbor-plan` views (ready tasks are assigned by the Maintainer); keep "open an issue" for bug reports/feature requests |
| `docs/DEVELOPMENT_GUIDELINES.md:113,119` and `docs/de/DEVELOPMENT_GUIDELINES.md:113,119` | "one assigned issue at a time per session", "start the next issue only after…" | "task" instead of "issue", plus one sentence: claim the task in baseharbor-plan before editing (link to its ownership protocol) |
| `docs/DEVELOPMENT_GUIDELINES.md:126` and DE counterpart | "GitHub Issues plan future work." | "baseharbor-plan plans future work." (EN/DE) |
| `docs/internal/pre-release-documentation-audit.md:37–48,106–107` | "Read the current roadmap issue…", "release-scoped issues", "EN/DE roadmap matches the current GitHub roadmap issue" | Read the release note in baseharbor-plan; "release-scoped tasks"; roadmap pages match `ROADMAP.md` there |
| `docs/roadmap.md:3` and `docs/de/roadmap.md` | "Detailed planning lives in GitHub Issues … issue #155 is the overarching roadmap" | "Detailed planning lives in baseharbor-plan; its ROADMAP.md is the overarching roadmap" (EN/DE parity; public docs, not process rules) |
| `.github/ISSUE_TEMPLATE/task.yml` | Task template for planning issues | Remove after cutover (tasks are created in baseharbor-plan); keep `bug_report.yml` and `feature_request.yml` for external intake |
| `.github/ISSUE_TEMPLATE/config.yml` | Contact links for security and docs | Add a link "Planning and roadmap → baseharbor-plan" |
| `.github/copilot-instructions.md` | Links to the guidelines | No change needed |
| `README.md` | — | No change (no process rules in the README) |

## mcpdev80/baseharbor-console

| File | Current | Proposed |
| --- | --- | --- |
| `CONTRIBUTING.md:14` | Points to Core issues #767–#770 (closed) | Point to baseharbor-plan for planned work |
| `.github/ISSUE_TEMPLATE/config.yml` | — | Add the planning link |

## mcpdev80/baseharbor-demo, mcpdev80/baseharbor-node-connector

No contributor/agent entry point exists. Proposal: none (the README stays free of process rules); optionally a one-line `CONTRIBUTING.md` linking BaseHarbor's contribution guide and baseharbor-plan.

## Prepared PRs and validation

- [baseharbor#937](https://github.com/mcpdev80/baseharbor/pull/937) — `92597de69aefa884a96bcdd6db8ed44a5d3ca9d0`.
- [baseharbor-console#5](https://github.com/mcpdev80/baseharbor-console/pull/5) — `51966e5de4edfb791da0126f9aa88a8077ca61a5`.
- [baseharbor-demo#114](https://github.com/mcpdev80/baseharbor-demo/pull/114) — `2574c958519a984fa9ddba4872d32d75e1f08c6a`.
- [baseharbor-node-connector#6](https://github.com/mcpdev80/baseharbor-node-connector/pull/6) — `e0d8e11b2e53e49d41c9c2dda75e8fad788eb538`.

BaseHarbor documentation audit passed locally: 156 EN/DE paired pages, structure, technical integrity, navigation, governance and internal evidence checks. Strict MkDocs EN and DE builds also passed locally at exact Core documentation commit `92597de69aefa884a96bcdd6db8ed44a5d3ca9d0`, using the repository-pinned documentation requirements. No Pages deployment or runtime suite was run. README files are unchanged. Core PR #937 shares development-guideline files with #895 / PR #933: integrate sequentially and retain both edits. Task-template removal is deliberately deferred until activation; removing intake before cutover would be premature.
