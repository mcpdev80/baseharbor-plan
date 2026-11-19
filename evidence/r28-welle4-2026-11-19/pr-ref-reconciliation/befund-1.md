# PR-Reference Reconciliation — mission `pr-ref-reconciliation` (card 0428-140)

Date: 2026-11-19
Lane: pr-ref-reconciliation. Read-only reconciliation of PR references for cards in
`review` whose PR link runs empty, per audit finding 0428-139 findings 3 and 5.

## PLAN

1. Preparation: `git -C baseharbor fetch origin --prune` (main clone, read-only); `baseharbor-plan pull --rebase origin main`; record `origin/main` HEAD witness.
2. Per card (0428-079/#1603, 0428-091/#1610, 0428-085/#1619, 0428-082/#1665):
   - PR truth via `gh api pulls/<n>`.
   - Branch existence via `git ls-remote origin refs/heads/<head.ref>`.
   - Successor search via PR page listing on `head.ref`, commit search on `origin/develop` for the task id, and `pr-body` reference scan.
   - Last terminal Actions run on the exact head sha (via `head_sha`-filtered run listing) + executed-cell count.
   - If no successor: state that explicitly.
3. #1665 (0428-082): `merge-base --is-ancestor <#1684 head> <#1665 head>` and `merge-tree --write-tree origin/develop <#1665 head>` + `^CONFLICT` count; evaluate what a retarget onto `lane-0428-083-datasources-r2` would mean (conflict count against that head).
4. Per-card EMPTFEHLUNG for the coordinator (coordinator changes board status, not this lane).
5. Host cleanliness before/after; commit only own file, pull --rebase, push, verify path on `origin/main`.

## Environment witnesses

- Planning repo (correct zone, per mission warning): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `https://github.com/mcpdev80/baseharbor-plan.git`). The workers/ bookkeeping copy `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` was NOT used for any planning act.
- Main clone: `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, remote `origin`/`lane-origin`/`upstream` all `https://github.com/mcpdev80/baseharbor.git`. The quarantined checkout `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was NOT cited for any remote truth; all remote facts came from `gh api` + `git ls-remote origin` against github.com.
- `origin/main` HEAD witness BEFORE fetch: `c000c5db2560c471fe84842136e03d6e54d96779` (unchanged after `fetch origin --prune`).
- `gh auth status`: logged in as `mcpdev80`, git protocol ssh, scopes gist/read:org/repo.
- No product repo edited, no PR touched, no `gh pr ready`, no comment, no merge, no rerun/dispatch, no card status change, no `.github/**` edit, no subagent (`AGENTS` 4.8). Scratch confined to the read-only git/`gh` path; no containers/compose started.

## Reconciliation table

| Card | PR | state | draft | merged | merge_commit_sha | head_ref | head_sha | ls-remote head | base_ref | Successor PR | Successor state / head | Last terminal run on head | Executed cells | EMPTFEHLUNG |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0428-079 perses-messaging | #1603 | closed | true | false | null | `lane-0428-079-r28-perses-messaging` | `fed84349…` | REF-MISSING (branch deleted with closed PR) | develop | none | — | 43794628957 (pull_request) SUCCESS | 6/30 draft cells only (PR Selected Checks skipped) | Card points at a closed-without-merge PR whose head branch no longer exists. No deliverable for 0428-079 exists in develop (`internal/metrics/perses_messaging.go` absent). Recommendation: card should leave `review` (or be marked blocked/superseded pending a NEW delivery PR for the never-built native messaging dashboard), not be retargeted — nothing to retarget. |
| 0428-091 perses-tempo-source | #1610 | closed | true | false | `aa69064a…` | `w091-0428-091` | `d57ab527…` | present, equals head_sha | lane-0428-075-perses-seam | #1645 | open / draft / head `c781eb86…` (branch `w091-tempo-r5-fix`) | KEIN LAUF auf diesem kopf (`d57ab527…` never ran CI) | — (only a queued third-party `claude` suite) | #1610 is a closed draft; its work lives on in successor #1645 (`w091-tempo-r5-fix`), which renames the eight embedded Tempo witness files `.go` -> `.go.txt` to unblock the Draft Go package selector. #1645 has terminal SUCCESS on its head: runs 43876671426 and 43874313785 (pull_request, success). Recommendation: board PR-link for 0428-091 should be repointed to #1645 (open, draft, success on head). |
| 0428-085 perses-log-trace-dash | #1619 | closed | true | false | `b2515445…` | `lane-0428-085-perses-log-trace-dash` | `fbffb965…` | present, equals head_sha | `w091-0428-091` | none | — | 43796266469 (workflow_dispatch) FAILURE | dispatch only (2 cells) | #1619 closed (draft) via a single failed workflow_dispatch; no successor PR references 0428-085 and the deliverable is absent from develop (`internal/logs/perses_log_views.go` + `internal/traces/perses_trace_views.go` missing). Recommendation: card should leave `review` (or be blocked pending a new delivery PR); nothing to retarget. |
| 0428-082 perses-dashboards | #1665 | open | true | false | null | `lane-0428-082-perses-dashboards` | `e580d324…` | present, equals head_sha | `w083-perses-datasources` (the CLOSED-without-merge #1608 head) | #1684 | open / non-draft / head `ab693229…` (branch `lane-0428-083-datasources-r2`) | 43999100666 (workflow_dispatch) FAILURE | 2 cells, `validate` job failed — no successful terminal run on this head | #1665 (draft, base = closed #1608 branch `w083-perses-datasources` @ `ed55d893`) should base on the successor #1684 (`lane-0428-083-datasources-r2` @ `ab693229`, non-draft, terminal SUCCESS 44505333646 incl. `PR Selected Checks`). `merge-base --is-ancestor ab693229 e580d324` => rc=1 (successor head NOT carried in #1665). Retarget onto successor = 6 content conflicts (cmd/baha/app_status_result.go, internal/application/manifest_render.go, internal/application/manifest_test.go, internal/capability/perses.go add/add, internal/capability/perses_selection.go add/add, internal/metrics/perses_contract_test.go add/add). Recommendation: retarget #1665 base to `lane-0428-083-datasources-r2` (Owner/operator action, 6 conflicts to resolve), then mark ready for a terminal PR run. |

## Command witnesses (per step, exactly as run)

Preparation (step 1):

```
$ cd /home/marcel/dev/baseharbor-ecosystem
$ git rev-parse origin/main        # before fetch
c000c5db2560c471fe84842136e03d6e54d96779
$ git -C baseharbor fetch origin --prune
(no output — clean, no pruned heads)
$ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git pull --rebase origin main
From https://github.com/mcpdev80/baseharbor-plan
 * branch              main       -> FETCH_HEAD
Already up to date.
$ git rev-parse origin/main        # planning
7c6b9c4ccc48db43ab91c2b561465d33d9683b7f
```

PR truth (step 2), exactly as run:

```
$ gh api repos/mcpdev80/baseharbor/pulls/1603 --jq '{state, draft, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, merged, merge_commit_sha}'
{"state":"closed","draft":true,"head_ref":"lane-0428-079-r28-perses-messaging","head_sha":"fed843492482b26572f093049a28e8bdcd19f777","base_ref":"develop","merged":false,"merge_commit_sha":null}

$ gh api repos/mcpdev80/baseharbor/pulls/1610 --jq '{state, draft, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, merged, merge_commit_sha}'
{"state":"closed","draft":true,"head_ref":"w091-0428-091","head_sha":"d57ab527524048bddc0af7bb08009edbb4d32033","base_ref":"lane-0428-075-perses-seam","merged":false,"merge_commit_sha":"aa69064a04c9e4cf02173986791965f9075a9997"}

$ gh api repos/mcpdev80/baseharbor/pulls/1619 --jq '{state, draft, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, merged, merge_commit_sha}'
{"state":"closed","draft":true,"head_ref":"lane-0428-085-perses-log-trace-dash","head_sha":"fbffb965f72585b160d4fee7bcc6050287c10fc2","base_ref":"w091-0428-091","merged":false,"merge_commit_sha":"b2515445b4cb386f6cdf68ca1b956410b4efd61f"}

$ gh api repos/mcpdev80/baseharbor/pulls/1665 --jq '{state, draft, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, merged, merge_commit_sha}'
{"state":"open","draft":true,"head_ref":"lane-0428-082-perses-dashboards","head_sha":"e580d32414565442376f23ace9a4a2dd7ed03838","base_ref":"w083-perses-datasources","merged":false,"merge_commit_sha":null}

$ gh api repos/mcpdev80/baseharbor/pulls/1608 --jq '{state, draft, head_ref: .head.ref, head_sha, merged, merge_commit_sha}'
{"state":"closed","draft":false,"head_ref":"w083-perses-datasources","head_sha":null,"merged":false,"merge_commit_sha":null}

$ gh api repos/mcpdev80/baseharbor/pulls/1684 --jq '{state, draft, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, merged}'
{"state":"open","draft":false,"head_ref":"lane-0428-083-datasources-r2","head_sha":"ab6932296f1f24c2024810f10b155633d931f7d4","base_ref":"develop","merged":false}
```

ls-remote witnesses (step 3):

```
$ git -C baseharbor ls-remote origin refs/heads/lane-0428-079-r28-perses-messaging
(empty)   -> REF-MISSING: branch deleted together with closed PR #1603

$ git -C baseharbor ls-remote origin refs/heads/w091-0428-091
d57ab527524048bddc0af7bb08009edbb4d32033	refs/heads/w091-0428-091
$ git -C baseharbor ls-remote origin refs/heads/lane-0428-085-perses-log-trace-dash
fbffb965f72585b160d4fee7bcc6050287c10fc2	refs/heads/lane-0428-085-perses-log-trace-dash
$ git -C baseharbor ls-remote origin refs/heads/lane-0428-082-perses-dashboards
e580d32414565442376f23ace9a4a2dd7ed03838	refs/heads/lane-0428-082-perses-dashboards
$ git -C baseharbor ls-remote origin refs/heads/w083-perses-datasources
ed55d893374b593a7a6032f0de496ca9920ad08d	refs/heads/w083-perses-datasources
$ git -C baseharbor ls-remote origin refs/heads/lane-0428-083-datasources-r2
ab6932296f1f24c2024810f10b155633d931f7d4	refs/heads/lane-0428-083-datasources-r2
```

Successor search (step 4):

```
$ gh api 'repos/mcpdev80/baseharbor/pulls?state=all&per_page=100' --jq '.[] | select(.head.ref | test("079|messaging";"i")) | {number,state,draft,head_ref}'
  (only #1603)  -> no live successor branch for 0428-079

$ gh api 'repos/mcpdev80/baseharbor/pulls?state=all&per_page=100' --jq '.[] | select(.head.ref | test("091|tempo-source";"i")) | {number,state,draft,head_ref}'
  {"draft":true,"head_ref":null,"number":1645,"state":"open"}
  {"draft":true,"head_ref":null,"number":1610,"state":"closed"}

$ gh api 'repos/mcpdev80/baseharbor/pulls?state=all&per_page=100' --jq '.[] | select(.head.ref | test("085|log-trace";"i")) | {number,state,draft,head_ref}'
  (only #1619)  -> no live successor for 0428-085

$ gh api repos/mcpdev80/baseharbor/pulls/1645 --jq '{state,draft,head_ref,head_sha,base_ref}'
{"state":"open","draft":true,"head_ref":"w091-tempo-r5-fix","head_sha":"c781eb86fc996493bf5e0ee807913e81a51c3ab4","base_ref":"develop"}
$ gh api repos/mcpdev80/baseharbor/pulls/1645 --jq .body | grep -a "0428-091"   # witness file rename of the #1610 Tempo source
  ...renames the eight embedded Perses Tempo upstream witness files...  (0428-091)  -> continuation of #1610

$ for p in $(gh api 'repos/mcpdev80/baseharbor/pulls?state=all&per_page=100' --jq '.[].number'); do
    gh api repos/mcpdev80/baseharbor/pulls/$p --jq '.body' | grep -q "0428-085" && echo "body refs 0428-085: $p"
  done
  only 1619 -> no successor PR references 0428-085

$ git -C baseharbor ls-tree origin/develop -- internal/logs/ internal/traces/ | grep -iE "perses|view"
  (empty) -> 0428-085 deliverable absent from develop
$ git -C baseharbor ls-tree origin/develop -- internal/metrics/ | grep -i mess
  (empty) -> 0428-079 deliverable absent from develop
```

Last terminal run on each head (step 4):

```
$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=fed843492482b26572f093049a28e8bdcd19f777" --jq '.workflow_runs[]|{id,name,event,status,conclusion,created_at}'
  43794628957  CI · PR #1603   pull_request  success  2026-11-16T02:51:09Z
  43796258280  CI · lane-0428-079…  workflow_dispatch  failure  2026-11-16T03:07:40Z
  -> last terminal: 43794628957 (success). Executed cells:
$ gh api "repos/mcpdev80/baseharbor/actions/runs/43794628957/jobs?per_page=100" --jq '[.jobs[]|select(.conclusion!="skipped")]|length'
  6   (Draft cells only; PR Selected Checks skipped)

$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=d57ab527524048bddc0af7bb08009edbb4d32033" --jq '.workflow_runs[]|{id,name,event,status,conclusion}'
  (empty) -> KEIN LAUF auf diesem kopf; only a queued third-party claude suite.

$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=c781eb86fc996493bf5e0ee807913e81a51c3ab4" --jq '.workflow_runs[]|{id,name,event,status,conclusion,created_at}'
  43876671426  CI · PR #1645  pull_request  success  2026-11-16T13:32:03Z
  43874313785  CI · PR #1645  pull_request  success  2026-11-16T13:17:11Z
  -> #1645 has terminal SUCCESS on its head.

$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=fbffb965f72585b160d4fee7bcc6050287c10fc2" --jq '.workflow_runs[]|{id,name,event,status,conclusion,created_at}'
  43796266469  CI · lane-0428-085…  workflow_dispatch  failure  2026-11-16T03:07:45Z
  -> only a failed dispatch; no successful PR run on this head.

$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=e580d32414565442376f23ace9a4a2dd7ed03838" --jq '.workflow_runs[]|{id,name,event,status,conclusion,created_at}'
  43999100666  CI · lane-0428-082…  workflow_dispatch  failure  2026-11-17T01:54:45Z
  -> only a failed dispatch; no successful PR run on this head.
$ gh api "repos/mcpdev80/baseharbor/actions/runs/43999100666/jobs?per_page=100" --jq '.jobs[]|select(.conclusion!="skipped")|{name,conclusion}'
  {"conclusion":"success","name":"Workflow policy"}
  {"conclusion":"failure","name":"validate"}   -> 2 executed cells, validate failed
```

#1665 / #1684 base reconciliation (step 5):

```
$ gh api repos/mcpdev80/baseharbor/pulls/1684 --jq '.body' | grep -aoE "#[0-9]{3,4}" | sort -u
  #1608
  #1665
  (PR body: "Consumed by 082/#1665 … 083 is the vorgelagert datasource contract for #1665. Supersedes the closed-without-merge PR #1608.")

$ G1684=$(gh api repos/mcpdev80/baseharbor/pulls/1684 --jq '.head.sha')   # ab6932296f1f24c2024810f10b155633d931f7d4
$ git -C baseharbor merge-base --is-ancestor "$G1684" e580d32414565442376f23ace9a4a2dd7ed03838; echo "rc=$?"
  rc=1   -> #1684 head is NOT an ancestor of #1665 head (successor not carried in #1665)

$ git -C baseharbor merge-tree --write-tree origin/develop e580d32414565442376f23ace9a4a2dd7ed03838 2>&1 | grep -c '^CONFLICT'
  6
$ git -C baseharbor merge-tree --write-tree origin/develop ab6932296f1f24c2024810f10b155633d931f7d4 2>&1 | grep -c '^CONFLICT'
  0   (successor head itself is clean on develop)

$ git -C baseharbor merge-tree --write-tree ab6932296f1f24c2024810f10b155633d931f7d4 e580d32414565442376f23ace9a4a2dd7ed03838 2>&1 | grep -A1 '^CONFLICT'
  CONFLICT (content): Merge conflict in cmd/baha/app_status_result.go
  Auto-merging internal/application/manifest_render.go
  CONFLICT (content): Merge conflict in internal/application/manifest_render.go
  Auto-merging internal/application/manifest_test.go
  CONFLICT (content): Merge conflict in internal/application/manifest_test.go
  Auto-merging internal/application/manifest_validation.go
  CONFLICT (add/add): Merge conflict in internal/capability/perses.go
  Auto-merging internal/capability/perses_selection.go
  CONFLICT (add/add): Merge conflict in internal/capability/perses_selection.go
  Auto-merging internal/metrics/perses_contract_test.go
  CONFLICT (add/add): Merge conflict in internal/metrics/perses_contract_test.go
  -> retarget #1665 onto lane-0428-083-datasources-r2 would surface 6 conflicts.
```

## Provenance / branch attestation

- Branch cut base for this read-only lane: none cut — this lane made no product branch. Remote base attestations:
  - `origin/main` HEAD at start of work: `c000c5db2560c471fe84842136e03d6e54d96779` (verified via `git -C baseharbor rev-parse origin/main`); unchanged after `fetch origin --prune`.
  - All `head_sha` values compared against `git ls-remote origin refs/heads/<head.ref>`; every existing head equals its PR `.head.sha`.
  - `origin/main` (planning) at evidence commit: `7c6b9c4ccc48db43ab91c2b561465d33d9683b7f`.

## Delivery

- Evidence file: `evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md` (this lane's only added file).
- Commit: own file only (`git add evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md`), no `git add -A`, no checkout of foreign worktrees.
- Pre-push: `git pull --rebase origin main`; push `origin main`; verify path present on `origin/main` (see below).

## Cleanliness

- before docker ps -a: 8 containers (ambient shared: `bh-local-shared-openbao-*`, `bh-local-shared-postgres-*` etc., pre-existing, not this lane's).
- after docker ps -a: 8 containers, identical list (`docker ps -a --format '{{.Names}} {{.Status}}'`): bh-local-shared-openbao-1 Created, bh-local-shared-openbao-member-1-1 Created, bh-local-shared-postgres-init-1 Exited (1) 2 days ago, bh-local-shared-postgres-1 Up 2 days, bh-local-shared-openbao-admin-1 Up 2 days, bh-local-shared-postgres-admin-1 Up 2 days, bh-local-shared-postgres-member-1-1 Up 2 days.
- before/after podman ps -a: `podman: command not found` (0 podman state).
- This lane started NO container/network/volume/compose project (read-only `gh api`/git audit).
- cleanliness: clean — no docker/podman artifacts created by this lane; scratch confined to the read-only git/`gh` path.

## Scope compliance

- Read-only reconciliation per mission GRENZEN: no card status change, no `git checkout` in foreign worktrees, no PR comment, no retarget, no merge, no rerun/workflow_dispatch, no `.github/**` edit, no product repo writes, no subagents (`AGENTS` 4.8), isolated read-only git/`gh` path.
- Evidence lives only in baseharbor-plan (this file).

## Handoff

END_DONE mission-pr-ref-reconciliation.md: 4 cards reconciled — 0428-079/#1603 closed-without-merge, branch deleted, no successor, deliverable never built (leave review); 0428-091/#1610 closed draft, successor #1645 (w091-tempo-r5-fix @ c781eb86, open/draft, terminal SUCCESS 43876671426) → repoint PR-link; 0428-085/#1619 closed draft via failed dispatch, no successor, deliverable absent (leave review); 0428-082/#1665 draft base = closed #1608 branch, successor #1684 (lane-0428-083-datasources-r2 @ ab693229, non-draft, terminal SUCCESS 44505333646), retarget surfaces 6 conflicts (cmd/baha/app_status_result.go, manifest_render.go, manifest_test.go, capability/perses.go, capability/perses_selection.go, metrics/perses_contract_test.go) → retarget to successor then mark ready.

## Origin/main verification (pasted before push, per mission)

```
$ git push -q origin main && git fetch -q origin main
$ git ls-tree origin/main -- evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md
100644 blob 3082ff7f154d72112c18e614553fbf2b266db2e9	evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md
$ git log -1 --format='%H' origin/main
45155da0eee61ad88e2bf739282f0bccb2904fa0
```
