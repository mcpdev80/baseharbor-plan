# Coordinator session-retention hygiene card

## PLAN

- 1. Inspect the two coordinator cleanup sources and verify the four named acceptance.json witness keys and timestamps.
- 2. Identify the next valid card identity and create one focused, unstarted hygiene task with source lines, remediation alternatives, and acceptance criteria.
- 3. Render and check the complete Plan repository; keep changes limited to the new card, generated views, and this akte.
- 4. Commit with the canonical lane identity, publish one Plan PR, and verify Hosted Plan validation on its exact head.
- 5. Merge the Plan PR normally after review and current-main ancestry proof; report the resulting main SHA.

## Visible commit identity and card owner

- New card owner frontmatter to be written verbatim: `owner: ""` (unassigned planned work).
- Commit `user.name`: `w255-0428-251-demo170codex`.
- Commit `user.email`: `w255-0428-251-demo170codex@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.
- Planning remote verified before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- Exact Plan main SHA fetched before branch creation: `12eda9e029e9055aea70208842eae66ba133e2b0`.

## Source and acceptance evidence

Source examined at `/home/marcel/dev/baseharbor-ecosystem/coordinator/scripts/release-lane.py` and `worker-cleanup.sh`:

- `release-lane.py:47-72` resolves by working directory, then falls back to root-session rows in that directory and a start-time/name heuristic; close candidates are rejected as ambiguous.
- `release-lane.py:89-95` reads watcher registration by exact `directory`; `release-lane.py:103-117` and `worker-cleanup.sh:76-88` use parent/session and exact lane inventory paths before calling the release script.
- `release-lane.py:212-226` returns PARTIAL on unresolved mapping; with `--run` it calls `release_pool(name)` and retains the session. The exact pending mapping is only persisted later at `release-lane.py:240-245`, after mapping succeeds. `worker-cleanup.sh:83-88` invokes that release path and stops on an incomplete release.
- `release-lane.py:262-275` clears pending state and writes the final receipt only after successful Codeman/OpenCode deletion; reservation release follows at lines 268-270.

Coordinator `board/acceptance.json` currently records these reproductions:

- `w401-session-retained`, timestamp `2026-11-27T19:08:09Z`: second cleanup was still PARTIAL, no spawn reference, reservation released, idle OpenCode session `2cd2e2d6` retained.
- `w402-cleanup-partial`, timestamp `2026-11-27T19:25:00Z`: same spawn-reference/session-mapping defect; reservation handled but session remained idle.
- `cleanup-defect-rootcause`, timestamp `2026-11-27T19:30:29Z`: lanes share `workers/.models/<channel>`, making directory-to-session mapping ambiguous; proposed remedies are per-lane working directory or persisted session-ID reference.
- `flash2-not-vacant`, timestamp `2026-11-27T19:44:38Z`: retained idle sessions still occupied seats although reservations were freed; pool hold confirmed the seat was not vacant.

The card uses next free number 0428-352, path `tasks/t-20261127-coord-session-retention.md`, title `Coordinator cleanup preserves session identity through PARTIAL retries`. It is planned and unassigned.

## Validation

- `card-status.py t-20261127-coord-session-retention planned --no-push` completed successfully against this isolated Plan clone using a temporary runtime config with `plan_repo` pointed at this clone.
- `python3 scripts/plan.py render && python3 scripts/plan.py check`: 785 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing accepted-dependency warnings.
- The renderer refreshed one older generated card preview in `tasks/t-20261125-hunt40-migration-marker-last.md`; its frontmatter and status are unchanged. The global render also regenerated release counts and views for the new planned card.
- This akte contains no Markdown checkbox lines.

## Branch provenance and commit receipt

- The branch was cut from Plan main `12eda9e029e9055aea70208842eae66ba133e2b0`; `git merge-base --is-ancestor 12eda9e029e9055aea70208842eae66ba133e2b0 HEAD` passed after the first commit.
- `git diff origin/main...HEAD --name-only`:

```text
evidence/2026-11-27/w255-coordinator-session-hygiene/akte.md
releases/v0.4.28.md
roadmap/cards.md
tasks/t-20261125-hunt40-migration-marker-last.md
tasks/t-20261127-coord-session-retention.md
views/kanban-dashboard.md
views/overview.md
views/ready.md
views/releases/v0.4.28.md
```

- `git log --oneline origin/main..HEAD`: `ad1e1db add coordinator session-retention hygiene card`.
- Commit `ad1e1db9669e7a7f953a5944dc2b86019833d369` author and committer are both `w255-0428-251-demo170codex`; pre-push author gate `git show -s --format=%an HEAD` printed `w255-0428-251-demo170codex`.
- END w255-0428-251-demo170codex DONE — card and evidence merged through the normal Plan PR path; exact resulting main SHA is reported in the coordinator END.
