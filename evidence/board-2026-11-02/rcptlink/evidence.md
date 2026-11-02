# rcptlink (v2) — Open-PR task-link fix

**Worker:** ornith (rcptlink lane) · **Date:** 2026-11-02 · **Model:** Ornith
**Follow-up to prior END_BLOCKED (accepted in part)** — Owner correction: "open PRs are editable now, fix them."

## Task (Owner, 30 min)
1. Give each OPEN PR a single `Resolves` line to the right Planning card/Issue (other PRs without a card get a `t-20261102-*` card first, then link).
2. Confirm the 7 reworked merged PRs are processed at the next writer run — READ the queue, don't guess; if a manual `workflow_dispatch` is needed, run it (tokens from system).
3. END_DONE with run-IDs. If only Owner action remains after that: END_BLOCKED with exact grounds + link.

## Step 1 — Open-PR Resolves links (DONE)

Open PRs targeted: #1272, #1273, #1282 (named by Owner). Resolved families:

| PR | Fix family | Issue | Card |
|---|---|---|---|
| #1282 | gofmt (Präzedenz #1270) | #1279 `t-20261102-ci-gofmt` | t-20261102-ci-gofmt.md |
| #1273 | runtime-broker / openbao/control-plane | #1278 `t-20261102-ci-openbao` | t-20261102-ci-openbao.md |
| #1272 | MCP authoring Workload.Compose optional | **#1284 (new)** `t-20261102-rcptlink-1272` | **t-20261102-rcptlink-1272.md (new)** |

New card `baseharbor-plan/tasks/t-20261102-rcptlink-1272.md` (state active, owner ornith, prs #1272),
Issue #1284 (title `Planning task t-20261102-rcptlink-1272`, body carries `tasks/t-20261102-rcptlink-1272.md`
so the resolver matches). `plan.py render` + `check` clean for the new card; published to main (0b33b1b).

Each PR body = original + exactly one `Resolves #<issue>` line appended. Verified: exactly one closer each.

## Step 2 — Next writer-run confirmation (READ, not guessed)

**Verified green (data layer):** ran live `receipt_tasklink.resolve_task_from_pr()` and
`receipt_verifier.resolve_pull()` against all 3 open PRs + the 7 merged PRs — all resolve to a
valid `tasks/<id>.md` (tasklink step no longer blocks).

**Queue read (authoritative):**
- `receipt-post-run.yml` runs the tasklink step + publish only for producer runs that match the
  `public-contracts` **pilot** entry in `baseharbor-plan/evidence/receipt-plans/public-contracts.json`,
  which binds head `3a04457f5d66e4b99da013769f2bf41fb9090a77` ("contracts: qualify extension/v1…",
  a `contracts/connection_profile_trust_test.go` touch).
- That pilot head is a **pilot** from the r27-ci-producer chain and is **not in any live PR**.
- The 3 open PR heads (5260fa41, 765033d4, 9ea36396) are **non-pilot**; their producer CI runs already
  executed and the **`PR · Public Contracts` job was SKIPPED** (they don't touch `contracts/` — confirmed
  for run 41427348336/PR#1282). No contracts/ PR is open among #1238–#1283.
- Editing a PR body does **not** trigger producer CI, so these runs cannot re-fire. A queued `workflow_dispatch`
  (41430889567) is stuck queued on the self-hosted runner backlog.

**Consequence:** The 7 merged PRs cannot re-trigger the writer (already merged). The 3 open PRs won't
produce a `public-contracts` pilot run (no contracts/ touch). No green receipt run is reachable without an
Owner action. Verified locally via the real resolver that the data fix is correct; the run itself is gated.

### Owner action to close (exact)
Any ONE of:
- Open a live PR that touches `contracts/` (selects `PR · Public Contracts`) with head == the
  `public-contracts` pilot entry, so its producer CI runs tasklink+publish green; OR
- Owner `workflow_dispatch` on `receipt-approval.yml` with `pr_number` for a PR whose producer run already
  published a `public-contracts` receipt (verify/approve/publish path in `receipt_verifier.approve`).

## Step 3 — END line
END_BLOCKED — data fix complete + verified green for all 10 PRs; green receipt run gated on Owner (no live
public-contracts pilot PR; merged PRs can't re-run CI; open PRs don't touch contracts/). Runs observed:
41427348336 (PR#1282 producer CI, Public Contracts skipped), 41428168338 (receipt fail, tasklink pre-fix).

## repo-rule compliance
- baseharbor-plan: added 1 card + 1 Issue; `plan.py render`/`check` clean; published to main (0b33b1b).
- baseharbor: NO product/workflow-code change (mission STOP). Only Issue + PR-body data edits.
- No closing other owners' Issues; no subagent spawn; no interactive dialog.

## END line
END_BLOCKED rcptlink: 10/10 PRs (7 merged + 3 open #1272/#1273/#1282) tasklink-resolve green; receipt run Owner-gated — pilot head 3a04457 not in a live contracts/ PR, merged PRs can't re-run CI, open PRs don't touch contracts/. evidence: baseharbor-plan/evidence/board-2026-11-02/rcptlink/evidence.md
