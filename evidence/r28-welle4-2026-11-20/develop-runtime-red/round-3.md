# round-3 — 0428-174 freeze after post-merge content movement

**Card:** t-20261120-r28-develop-runtime-integration-red / **PR:** #1711 / **Lane:** lane-0428-174-develop-runtime-red
**Worker:** x-174f / **Date:** 2026-11-20
**State:** FROZEN per Owner stop. PR #1711 already merged (09:50:00Z, merge commit dbe7fbc3905b). A second commit ccb630681 pushed at 10:39 moved the live head after the merge; CI at that exact head is green. Card at state: review, Owner queued the abnahme. No further product pushes.

## 0. What happened (measured, not guessed)

- PR #1711 head before my stop message: 0a3805fb56df (the refreshed base, CI 44708908050 success).
- A second commit `ccb630681c96c9e5e8ef6dd52aa1bb111ecd1fb1` "test: verify all postgres process UIDs are non-root" (author mcpdev80, 10:39:07) stacked on top of 0a3805fb and moved the live head to ccb630681.
- PR #1711 was merged at 2026-11-20T09:50:00Z by mcpdev80 (merge commit dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2) — so the merge happened before the 10:39 second push; my stop message's claim "head=0a3805fb==refs/pull/1711/head" no longer holds.
- The freeze rule applies: a head that changes during review voids a verdict. I am NOT pushing anything further and NOT re-requesting review while a movement is in flight.

## 1. Pflicht 1 — observe CI at the EXACT current head (ccb630681c96), not the old 44708908050

Observed run:
```
CI run 44712547340  (commit ccb630681c96, event pull_request)  ->  conclusion=success, 0 failed jobs
Gate "PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle" = success
https://github.com/mcpdev80/baseharbor/actions/runs/44712547340
```

## 2. Pflicht 2 — three proof lines at the same head

```
$ git ls-remote lane-origin refs/heads/lane-0428-174-develop-runtime-red refs/pull/1711/head
(no branch line — the named branch was removed; the live candidate is the PR ref)
ccb630681c96c9e5e8ef6dd52aa1bb111ecd1fb1  refs/pull/1711/head

$ git fetch lane-origin refs/pull/1711/head
$ git merge-base --is-ancestor 681700ca66f3 ccb630681c96c9e5e8ef6dd52aa1bb111ecd1fb1
JA   <- 681700ca66f3 (develop) is an ancestor of ccb630681c96

$ gh api repos/mcpdev80/baseharbor/pulls/1711 --jq '{head:.head.sha, base:.base.sha, state:.state}'
{"base":"681700ca66f3619998e24bbfd71bc86912cf38ec","head":"ccb630681c96c9e5e8ef6dd52aa1bb111ecd1fb1","state":"closed"}
```

Note: PR #1711 state=closed because it was merged (09:50:00Z). The live candidate ref for CI review is still refs/pull/1711/head = ccb630681c96, and CI at that head is green.

## 3. Pflicht 3 — reinlichkeit (cell cleanup, before seat freed)

`docker ps -aq` on coordinator host = 0. On my machine, `bash scripts/ci-runtime-reset.sh docker` reports "no BaseHarbor-owned targets".
```
containers: 0
volumes: 5   (unlabeled foreign/system leftovers: testvol, backup-foreign-…, 3 hashes — none baseharbor-owned)
networks: 3  (unlabeled foreign/system — none baseharbor-owned)
```
`docker volume ls --format '{{.Labels}}' | grep baseharbor` = 0, `docker network ls --format '{{.Labels}}' | grep baseharbor` = 0. Foreign / ambient-core images untouched (owner directive).
`cleanliness: clean — no baseharbor-owned container/network/volume remains; ci-runtime-reset confirms "no BaseHarbor-owned targets"; foreign unlabeled volumes/networks left as-is; ambient-core/other-lane images untouched.`

## 4. END

END_DONE (frozen per Owner). No further product push, no review re-request until the Owner releases the freeze. Card stays at state: review.
