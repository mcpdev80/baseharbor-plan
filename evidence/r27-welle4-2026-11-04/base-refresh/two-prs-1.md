# Base refresh: PRs #1369 and #1362

Mission: `coordinator/missions/cx02-base-refresh-two.txt` (ROLLE=CODEX-WORKER).

Freshly fetched `origin/develop` before merging: `ecbb88545f96473986f8f41394cffce58b97d2df`.
Both incoming branches were at the mission-specified old SHAs. `git merge-tree --write-tree` found no conflicts for either branch. Each `git merge --no-edit origin/develop` completed with exit code 0; no manual conflict resolution was needed. No product logic or tests were edited by this refresh.

## Branch and gate results

| PR / branch | Old SHA | New SHA | Merge RC | Conflicts | GitHub-hosted gate result |
| --- | --- | --- | --- | --- | --- |
| #1369 `work/w92-team-auth-claim-mapping` (still DRAFT) | `689689e3abdaf1bc14ef81aa601d69f40595e185` | `815fdfb709c7abe82f2ba77b85bdc8ddf2381c76` | 0 | none | Run [41861398529](https://github.com/mcpdev80/baseharbor/actions/runs/41861398529) terminal success. Source format and workflow policy passed. All test/validation jobs and `PR Selected Checks` skipped because `.github/workflows/ci.yml` gates PR tests on `github.event.pull_request.draft == false` (line 431 for `PR · Trusted Plan`; line 933 for `PR Selected Checks`). No test ran for this draft PR; changing draft state is forbidden by this mission. |
| #1362 `work/r27-native-auth` (still READY/open) | `a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c` | `9faf95f331e38dcc800bbfeb394e69ff618ed2d1` | 0 | none | Run [41861405497](https://github.com/mcpdev80/baseharbor/actions/runs/41861405497) observed. Trusted Plan, Source format, Workflow policy, `go-build`, `go-vet`, and Focused Python passed. `go-unit-tests` failed at `internal/database/identity_tenant_resolver_integration_test.go:101` and `internal/database/tenant_integration_test.go:87`; exact failure: `failed to connect to user=baseharbor_resolver_ci/runtime_ci database=baseharbor_test: 127.0.0.1:5432: dial tcp 127.0.0.1:5432: connect: connection refused`. The existing `scripts/pr-unit-database.sh` publishes PostgreSQL on `127.0.0.1:5433` and sets `BASEHARBOR_TEST_DATABASE_URL` to port 5433. The two tests therefore did not use that fixture. No fix or rerun was made. `PR Selected Checks` was still queued at last observation (job 126688353262, queued since 2026-11-04 15:55:30Z); its terminal result is pending GitHub runner assignment. |

Other CI jobs marked skipped on #1362 included Targeted HA Docker/Podman, validate, Release Source Preflight, Consumer Pins, Runner Interface, Demo Pin, Exact Candidate, Selected Runtime, and Public Contracts. These gates were not required by the selected plan; they are recorded as skipped, not passed.

## Literal remote-head verification

Command:

```text
git -C baseharbor ls-remote origin refs/heads/work/w92-team-auth-claim-mapping
```

Output:

```text
815fdfb709c7abe82f2ba77b85bdc8ddf2381c76	refs/heads/work/w92-team-auth-claim-mapping
```

Command:

```text
git -C baseharbor ls-remote origin refs/heads/work/r27-native-auth
```

Output:

```text
9faf95f331e38dcc800bbfeb394e69ff618ed2d1	refs/heads/work/r27-native-auth
```

Also verified remote `develop` remained `ecbb88545f96473986f8f41394cffce58b97d2df`. PR #1369 remained open/DRAFT; PR #1362 remained open/READY. No PR approval, merge, workflow dispatch, rerun, or PR status change was performed.
