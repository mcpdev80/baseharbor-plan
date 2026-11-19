# 0428-088 · Perses runtime · host witness 1 (exact-head runtime proof)

Mission: mission-088-host-witness.md · Card: t-20261114-r28-perses-runtime · PR #1592
Branch: lane-0428-088-perses-runtime
Date: 2026-11-19

## What this file proves

A host-local runtime witness for `TestPersesRuntimeSmokeDockerIsolated` at the exact
candidate head, per the acceptance recipe (precedent 088-r3). The hosted CI cell for this
test has no trigger wiring (documented Owner finding, captured in 0428-114); this file
provides the exact-head host witness.

## Heads

- Candidate branch `lane-0428-088-perses-runtime` remote HEAD:
  `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`
  Witness: `git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor ls-remote origin refs/heads/lane-0428-088-perses-runtime`
  -> `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9	refs/heads/lane-0428-088-perses-runtime`
- `develop` remote HEAD: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
  Witness: `git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor ls-remote origin refs/heads/develop`
  -> `da76c5cf9c963207038d5599bd130b89ecb1e8a4	refs/heads/develop`
- Candidate head contains develop at `21161b101` (PR #1694) via the r4 second hopf; `da76c5cf9`
  (PR #1696, 0428-126) is NOT an ancestor of `76331c7d8`.
- Base attestation: the r4-1 dossier records the merge base as `21161b101f66a47fb1a253ae17e87fe82567ba4d`
  (develop content that this head carries). This lane made no product changes: the checkout is
  `git clone` of the remote branch at the exact SHA (detached HEAD), no new commits.

## Worktrees

Two isolated clones under `/var/tmp` (mission: tmp `/var/tmp`). Provenance rule: every test
run is preceded by its `git rev-parse HEAD` and `git status --porcelain` witness.

- Candidate: `/var/tmp/mission-088-wt`
  `git clone --branch lane-0428-088-perses-runtime https://github.com/mcpdev80/baseharbor /var/tmp/mission-088-wt`
  then `git checkout 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9` (checkout the exact SHA, no alias).
  Before run 1: `git rev-parse HEAD` -> `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`,
  `git status --porcelain` -> empty (0 lines).
- Develop comparison: `/var/tmp/mission-088-develop`
  `git clone --branch develop https://github.com/mcpdev80/baseharbor /var/tmp/mission-088-develop`
  Before run 2 (develop head): `git rev-parse HEAD` -> `da76c5cf9c963207038d5599bd130b89ecb1e8a4`,
  `git status --porcelain` -> empty (0 lines).
  `git checkout lane-0428-088-perses-runtime` (the remote-tracking branch created by the
  clone, fast-forward to the same candidate head).
  Before run 3 (same head, different worktree): `git rev-parse HEAD` ->
  `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`, `git status --porcelain` -> empty (0 lines).

## Environment

The run happened on the host this session runs on (`linux/amd64`, rootless Docker).
Docker is reachable (`/usr/bin/docker`); pre-existing shared containers `bh-local-shared-*`
belong to other lanes and are not touched. The mission's "baha-docker-umbauung wie im
088-r3-praezedenz" applies only if an image/container path is needed; here the Perses image
`docker.io/persesdev/perses:v0.55.1` is pulled by the test from the network. No custom
images were built and no `ambient-core/` images were touched.

Host `docker version` witness (full):

```
Client: Docker Engine - Community
 Version:           29.9.3
 API version:       1.56
 Go version:        go1.26.10
 Git commit:        5457199
 Built:             Tue Nov  3 21:42:07 2026
 OS/Arch:           linux/amd64
 Context:           rootless

Server: Docker Engine - Community
 Engine:
  Version:          29.8.1
  API version:      1.56 (minimum version 1.40)
  Go version:       go1.26.8
  Git commit:       464cd50
```

## Commands and outputs (verbatim)

### Run 1 — candidate head `76331c7d8` (worktree: mission-088-wt)

Before the test: `cd /var/tmp/mission-088-wt && git rev-parse HEAD` ->
`76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`; `git status --porcelain` -> empty.

Command:

```
cd /var/tmp/mission-088-wt && BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v
```

Full output:

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (19.32s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	19.326s
```

### Run 2 — develop head `da76c5cf9` (worktree: mission-088-develop)

Before the test: `cd /var/tmp/mission-088-develop && git rev-parse HEAD` ->
`da76c5cf9c963207038d5599bd130b89ecb1e8a4`; `git status --porcelain` -> empty.

Command:

```
cd /var/tmp/mission-088-develop && BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v
```

Full output:

```
testing: warning: no tests to run
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	0.005s [no tests to run]
```

This proves the test function is head-dependent: `TestPersesRuntimeSmokeDockerIsolated`
exists only in the `lane-0428-088-perses-runtime` branch and is not present on `develop`
(`git show origin/develop:internal/application/perses_runtime_test.go` -> path does not exist).

### Run 3 — cross-check on candidate head `76331c7d8` (different worktree)

To verify the PASS is not a fluke of one worktree, the same test was run at the same head
in the second worktree (after `git checkout lane-0428-088-perses-runtime` in mission-088-develop).

Before the test: `cd /var/tmp/mission-088-develop && git rev-parse HEAD` ->
`76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`; `git status --porcelain` -> empty.

Command:

```
cd /var/tmp/mission-088-develop && BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v
```

Full output:

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (11.80s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	11.810s
```

### Run 4 — recomputation at candidate head `76331c7d8` (worktree: mission-088-wt, final)

Run after all provenance/annotation edits, to prove the recorded PASS is reproducible.

Before the test: `cd /var/tmp/mission-088-wt && git rev-parse HEAD` ->
`76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`; `git status --porcelain` -> empty.

Command:

```
cd /var/tmp/mission-088-wt && BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v
```

Full output:

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (25.99s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	25.991s
```

### Run 5 — post-hopf recomputation at candidate head `76331c7d8` (mission-088-wt)

Final recomputation after all planning-repo hops, same command and worktree as run 4.

Before the test: `cd /var/tmp/mission-088-wt && git rev-parse HEAD` ->
`76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`; `git status --porcelain` -> empty.

Command:

```
cd /var/tmp/mission-088-wt && BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v
```

Full output:

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (14.50s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	14.510s
```

### Run 6 — final confirmation (both worktrees, candidate head `76331c7d8`)

Run immediately before the END post, once in each worktree, same command.

`cd /var/tmp/mission-088-wt` (HEAD `76331c7d8`, porcelain empty):

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (7.57s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	7.579s
```

`cd /var/tmp/mission-088-develop` (HEAD `76331c7d8`, porcelain empty):

```
=== RUN   TestPersesRuntimeSmokeDockerIsolated
--- PASS: TestPersesRuntimeSmokeDockerIsolated (7.34s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/application	7.348s
```

Afterwards `/var/tmp/mission-088-develop` was switched back to `develop`
(`da76c5cf9`) so both worktrees' on-disk heads match the recorded witness runs.

## Container/network witness

Before run 1:

```
$ docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
CONTAINER ID   NAMES                                 STATUS
de665349790f   bh-local-shared-openbao-1             Created
f821395e1f09   bh-local-shared-openbao-member-1-1    Created
828d8f4579d1   bh-local-shared-postgres-init-1       Exited (1) 2 days ago
2531cbd8df86   bh-local-shared-postgres-1            Up 2 days
4e4e8006c43f   bh-local-shared-openbao-admin-1       Up 2 days
52047404d2d4   bh-local-shared-postgres-admin-1      Up 2 days
d86c9d69f729   bh-local-shared-postgres-member-1-1   Up 2 days

$ docker network ls
NETWORK ID     NAME                       DRIVER    SCOPE
520134fdd9f3   baseharbor-local-default   bridge    local
8452917e1c81   baseharbor-local-secrets   bridge    local
1d699428d131   bridge                     bridge    local
f34ac3c2e551   host                       host      local
08570460291d   none                       null      local
```

After all runs (final cleanup, second-to-last action):

```
$ docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
CONTAINER ID   NAMES                                 STATUS
de665349790f   bh-local-shared-openbao-1             Created
f821395e1f09   bh-local-shared-openbao-member-1-1    Created
828d8f4579d1   bh-local-shared-postgres-init-1       Exited (1) 2 days ago
2531cbd8df86   bh-local-shared-postgres-1            Up 2 days
4e4e8006c43f   bh-local-shared-openbao-admin-1       Up 2 days
52047404d2d4   bh-local-shared-postgres-admin-1      Up 2 days
d86c9d69f729   bh-local-shared-postgres-member-1-1   Up 2 days

$ docker network ls
NETWORK ID     NAME                       DRIVER    SCOPE
520134fdd9f3   baseharbor-local-default   bridge    local
8452917e1c81   baseharbor-local-secrets   bridge    local
1d699428d131   bridge                     bridge    local
f34ac3c2e551   host                       host      local
08570460291d   none                       null      local
```

No perses container/network/volume remains. The `perses-runtime-smoke` compose project was
brought down by the test's own `t.Cleanup` (`DestroyProject`).

cleanliness: no orphaned perses artifacts; ambient `bh-local-shared-*` containers left
untouched (not this lane's projects).

## PLAN

1. Read mission instructions and establish current repo state — done.
2. Fetch exact candidate head for lane-0428-088-perses-runtime (`76331c7d8`) and isolated
   worktrees under `/var/tmp` — done.
3. Run `TestPersesRuntimeSmokeDockerIsolated` on the candidate head with full logs and
   timing — done (PASS six runs at the exact head; terminal runs 7.57s and 7.34s).
4. Run the same command on develop head `da76c5cf9` for comparison — done
   ("no tests to run": the test file is absent on develop).
5. Compose evidence `witness-1.md` with required metadata, commit and push to
   origin/main in baseharbor-plan — done.
6. Report END to coordinator session — final action.

## Verdict

- Candidate `76331c7d8` PASS six times across both worktrees: 19.32s (run 1), 11.80s
  (run 3), 25.99s (run 4), 14.50s (run 5), 7.57s and 7.34s (run 6, both worktrees).
  Every PASS line is quoted verbatim in the Run sections above.
- Develop `da76c5cf9`: `no tests to run` (the test is head-dependent: it does not exist on develop).
- Hosted zelle nicht gemappt -> owner-befund 0428-114: no workflow file sets
  `BASEHARBOR_PERSES_RUNTIME_SMOKE` and `scripts/pr-gate-coverage.json` registers no perses
  runtime gate; durable CI wiring is an Owner decision tracked in 0428-114. Precedent 088-r3
  accepted this host-local fallback for exactly this case.

## Timing and timestamps

All runs on 2026-11-19. Times are Go test elapsed seconds as reported in the PASS line.

| Run | Worktree | Head | Time |
| --- | --- | --- | --- |
| 1 | mission-088-wt | `76331c7d8` | 19.32s |
| 2 | mission-088-develop | `da76c5cf9` | n/a (no tests) |
| 3 | mission-088-develop (checkout of candidate) | `76331c7d8` | 11.80s |
| 4 | mission-088-wt (recomputation) | `76331c7d8` | 25.99s |
| 5 | mission-088-wt (post-rebase recomputation) | `76331c7d8` | 14.50s |
| 6a | mission-088-wt (final confirmation) | `76331c7d8` | 7.57s |
| 6b | mission-088-develop (final confirmation) | `76331c7d8` | 7.34s |

## Revision labels

- mission revision: mission-088-host-witness.md (2026-11-19)
- head tested: `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9` (r4 second hopf)
- develop compared: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- precedent: `r3-1.md`, `r4-1.md`

## END

END_DONE mission-088-host-witness.md: host witness `TestPersesRuntimeSmokeDockerIsolated`
PASS six times at exact candidate head `76331c7d8` on the session host (terminal
confirmation run 6: 7.57s in mission-088-wt, 7.34s in mission-088-develop); develop
`da76c5cf9` reports "no tests to run" (head-dependent: the test file does not exist on
develop); no product change, no PR; host-local fallback per 088-r3 precedent with the
missing hosted wire as Owner finding 0428-114.

## Evidence on origin/main before END (second-to-last action)

```
$ git ls-remote origin refs/heads/main
c35d447e02ac2e46c96f819243a9200bd0e9416e	refs/heads/main
$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-19/perses-runtime/witness-1.md && echo PRESENT
PRESENT
$ git merge-base --is-ancestor 073e13e9 origin/main; echo $?
0
```

This lane's evidence commits on origin/main: `073e13e9` (initial witness, parent
`4ca4ab28`) through `c35d447e` (terminal: run 6 confirmations 7.57s / 7.34s, END restated).
Coordinator commits interleaved on the path (`779dd3c6`, `984055db`, gate-map intake) are
not this lane's and were preserved. `git log --oneline origin/main..HEAD` is empty after
the final push (nothing of this lane is unpushed).
