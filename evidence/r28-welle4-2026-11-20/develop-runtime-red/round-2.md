# round-2 — 0428-174 base refresh + reinlichkeit (before release)

**Card:** t-20261120-r28-develop-runtime-integration-red / **PR:** #1711 / **Lane:** lane-0428-174-develop-runtime-red
**Worker:** x-174f / **Date:** 2026-11-20
**State:** Base refreshed onto new develop 681700ca66f3, CI run 44708908050 success, cell clean. Card stays active for Owner abnahme after the rebase-run.

## 1. Pflicht 1 — base refresh (before release)

Owner measured PR #1711 against a stale base: develop had advanced past my
PR base `36d075fad77f` (PR #1709 merged). New develop head `681700ca66f3`.

Measured PR #1711 before refresh:
```
$ gh api repos/mcpdev80/baseharbor/pulls/1711 --jq '{base:.base.sha, mergeable:.mergeable, head:.head.sha}'
{"base":"36d075fad77fa61ac8c153e979855546589b32c2","head":"595fda6187f29342cab4526d8fce9b47667652f9","mergeable":true}
```

Refresh (baseharbor-plan decisions/2026-11-20-pr-branch-refresh-by-rebase.md):
```
$ git fetch lane-origin develop
$ git rebase 681700ca66f3           # unprotected branch lane-0428-174-develop-runtime-red
$ git push --force-with-lease lane-origin HEAD:refs/heads/lane-0428-174-develop-runtime-red
```

After refresh:
```
$ git log --oneline -2
0a3805fb5 fix(0428-174): verify postgres entrypoint drops privileges in multi-instance runtime gate
681700ca6 Merge pull request #1709 from mcpdev80/lane-0428-168-signal-id-migration
$ git merge-base --is-ancestor 681700ca66f3 HEAD
JA   <- 681700ca66f3 (new develop) is an ancestor of my head 0a3805fb5
```

Test file content is byte-identical to the pre-rebase head (the rebase only moved
the base forward; my single commit's diff is unchanged). `go build ./internal/application/` clean.

Proof lines (required):
```
$ git ls-remote lane-origin refs/heads/lane-0428-174-develop-runtime-red refs/pull/1711/head
0a3805fb56df01d09a6d3b3c578ca50317af04f3  refs/heads/lane-0428-174-develop-runtime-red
0a3805fb56df01d09a6d3b3c578ca50317af04f3  refs/pull/1711/head          (branch == PR head)

$ git merge-base --is-ancestor 681700ca66f3 HEAD
JA   <- new develop is an ancestor of my head
```

Observed rebase-run (Eigenes-Run-Pflicht §4.6):
```
CI run 44708908050  (commit 0a3805fb5, event pull_request)  ->  conclusion=success, 0 failed jobs
Gate "PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle" = success
https://github.com/mcpdev80/baseharbor/actions/runs/44708908050
```

No force-push to develop/main. No subagent (§4.8). No `.github/**`. No merge.

## 2. Pflicht 2 — reinlichkeit (cell cleanup, before seat freed)

`docker ps -aq` on the coordinator host = 0 (reported). The seat is on my
machine; measured there before freeing.

BEFORE (my machine, at end of work):
```
containers (all): 0
volumes: 5
networks: 3
```
`bash scripts/ci-runtime-reset.sh docker`:
```
runtime-reset] volumes: no BaseHarbor-owned targets
runtime-reset] state: full dedicated-runner cleanup
```

AFTER:
```
containers: 0
volumes: 5
networks: 3
```

Analysis of the remaining 5 unlabeled volumes (`7b957ba8…`, `87e1440c…`,
`backup-foreign-862f95bd-…-sentinel`, `d7916abb…`, `testvol`) and 3 unlabeled
networks: none carry a baseharbor / compose-project label
(`docker volume ls --format '{{.Labels}}' | grep baseharbor` = 0,
`docker network ls --format '{{.Labels}}' | grep baseharbor` = 0). They are
foreign/system leftovers, not from this lane (the multi-instance test tears its
project down via t.Cleanup/compose.DestroyProject, and this lane started no
container that outlived it). `ci-runtime-reset` reports no BaseHarbor-owned
targets. Foreign / ambient-core images deliberately untouched (owner directive).

`cleanliness: clean — no baseharbor-owned container/network/volume remains;
ci-runtime-reset confirms "no BaseHarbor-owned targets"; foreign unlabeled
volumes/networks left as-is; ambient-core/other-lane images untouched.`

## 3. END

END_DONE (pending Owner abnahme after rebase-run). Card stays active.
