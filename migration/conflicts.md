# Conflicts and open questions

Found while migrating. "Applied" says how the vault currently reads the sources; items marked **Maintainer decision** block the cutover until answered.

## Conflicting sources

| # | Topic | Sources | Applied | Needs |
| --- | --- | --- | --- | --- |
| C1 | Shared release PR / two sessions per release | Section "Binding PR workflow: one shared release PR, two sessions (2026-10-10)" in baseharbor#174, #874, #875, #876; "two sessions" in #777, #818–#823 | Superseded by #155/#427 (2026-10-15) and `DEVELOPMENT_GUIDELINES.md`: task PRs against develop from v0.4.26 ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md), accepted) | Remove/mark the outdated sections in the source issues before cutover (or accept that the snapshot keeps them as history) |
| C2 | "BaseHarbor Core = SQL + Secrets + Identity" | baseharbor#777 ("Core capability consistency"), #174 ("Core definition acceptance", "Managed-provider lifecycle truth") vs binding #872 correction in #155/#427 | Later #872 correction applied; placement-neutrality part kept ([decision](../decisions/2026-10-15-capability-footprint-supersedes-fixed-core.md), proposed) | **Maintainer decision:** confirm, or define the distinction between a management installation's fixed Core and application capabilities |
| C3 | #893 interface reference SHA | #888/#893/#896 body: PR #930 at `d56737bd…` is the reference; #896 comment: consumes `ca2653cb…` | Recorded both in [core-893-interface](../tasks/core-893-interface-agree-planning-execution-interface.md); not accepted | **Maintainer decision:** record the agreed interface SHA |
| C4 | #862 release | Title "[v0.4.x]", milestone v0.4.x; #155/#427 tables place #862 in v0.4.31 ("final completion belongs to #174") | `release: v0.4.31` (completion release); the note says gates start early and ratchet per release | Confirm |
| C5 | Historical release labels inside current scope | #821 "v0.4.25 mandatory WSL2 delivery acceptance"; #750/#751/#754/#766 "lands directly in active v0.4.21"; #174 v0.4.25 sections | Requirements kept, old version labels marked historical | — |

## Items without a release decision (release `triage`)

| Item | Source | Candidate | Needs |
| --- | --- | --- | --- |
| [console-1](../epics/console-1-console-product-plan.md) | baseharbor-console#1 (product plan) | v0.4.28 (Console) | **Maintainer decision** |
| [console-2](../tasks/console-2-live-core-adapter-workflow-proofs.md) | baseharbor-console#2 (v0.4.23 live integration, umbrella #571 closed) | v0.4.28 | **Maintainer decision**; also continue/close draft console#3 |
| [nc-3](../tasks/nc-3-core-enrollment-remote-runtime-acceptance.md) | baseharbor-node-connector#3 (v0.4.23 integration) | v0.4.27 work area 1 | **Maintainer decision**; also continue/close draft node-connector#4 |
| [demo-24](../tasks/demo-24-managed-exposure-https-default.md) | baseharbor-demo#24 (HTTPS by default via managed PKI) | Core part possibly v0.4.30 / core-902 | **Maintainer decision** (and whether a Core task is needed) |

## Missing or stale information

| # | Topic | Detail |
| --- | --- | --- |
| M1 | Branch cleanup record | [core-909](../tasks/core-909-maintenance-remove-superseded-branches.md): remote shows 8 branches (2026-10-15T20:35Z), so removal appears done, but the per-ref deletion record (original SHA + reason) is not documented. |
| M2 | Old fix branches | Branches named in core-750/751/752 no longer exist on the remote; they are only in the Maintainer's local mirror. |
| M3 | Stale PRs | baseharbor-demo #61, #62 (empty diff), #86, #104, #106 (v0.4.18/19 era) are referenced by no open item; console#3 and node-connector#4 are stale drafts. **Maintainer decision:** continue or close (not part of planning migration). |
| M4 | GitHub Projects | Not inspectable: token lacks `read:project`. Whether a Project exists and must be retired is unknown. |
| M5 | Native GitHub sub-issue / blocked-by links | Never set (noted in #873/#888). Not needed after cutover: dependencies live in `depends_on`. |
| M6 | Live changes after snapshot | PR #931 merged at 20:32Z (after the 20:18Z snapshot); `develop` moved to `bf69ad0a…`. Run `scripts/snapshot.py diff` and reconcile before cutover. |
| M7 | Docker Desktop licensing (core-884) | Decision not yet recorded in the source. |
