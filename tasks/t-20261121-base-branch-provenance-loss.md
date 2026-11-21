
id: t-20261121-base-branch-provenance-loss
card_number: "0428-221"
card_short_title: "0428-221 base provenance loss"
type: bug
areas: [cli, ci]
release: "v0.4.28"
version: ""
parent: ""
owner: coordinator
kanban_status: planned
kanban_lane: planned
kanban_summary: "closed-unmerged lane branches lost content while cards recorded accepted; recover the content and add an ancestry witness"
kanban_title: 0428-221 · base provenance loss
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
created: "2026-11-21T09:34:20Z"
updated: "2026-11-21T09:34:20Z"

---

- [ ] t-20261121-base-branch-provenance-loss · 0428-221 base content of closed-unmerged lane branches must be recovered or the cards reopened, and the loss must be prevented by an ancestry check

## Found by the coordinator (2026-11-21, finding-to-card duty AGENTS 3.3.5)

Measured, not inferred: PR #1726 (cards 0428-198 and 0428-204) is CLOSED without merge (`mergedAt` null, `closedAt` 2026-11-21T09:09:20Z, `mergeable` CONFLICTING) while both cards sit `closed` with `resolution: accepted`. The lane head `e45430f2f1b7` carries 11 commits that are absent from develop (`rev-list --count develop..e45430f2f1b7` = 11, `merge-base --is-ancestor` NEIN for all eight sampled commits). Content proof: develop has 0 occurrences of `withoutOperatorAuthTestContext` in `cmd/baha/app_init_wizard.go`, the lane has 2. Four open PRs (#1737 #1738 #1740 #1741) declare that lane as `baseRefName`, so none of them can ever be green against develop, and the 0428-220 supersede I booked on witness `46017060d` had to be withdrawn.

## Acceptance

1. For every closed-unmerged lane branch of this window: either its content is re-landed onto develop (a commit whose tree contains the delta) or the cards that recorded `accepted` are reopened with a note naming the lost commits.
2. A machine check that fails when a card is `accepted`/`closed` while its PR has `mergedAt` null: the state transition must require remote merge witness, per AGENTS 5.2.
3. A machine check that reports, per open PR, whether `baseRefName` head is an ancestor of develop or a live lane (no silent stale-base ancestry).

## Boundaries

Card fields in `baseharbor-plan/tasks/**` plus the checks in `baseharbor-plan/scripts/**`. `.github/**` and `scripts/**` inside mcpdev80/baseharbor are owner scope: if a guard must live there, report file:line and stop.

## Verification

`git merge-base --is-ancestor` and `gh pr view --json mergedAt,mergeable` per PR are the witnesses; the hunt aktes `evidence/r28-welle4-2026-11-21/base-branch-liveness/` and `.../closed-unmerged-content-loss/` carry the inventories.
