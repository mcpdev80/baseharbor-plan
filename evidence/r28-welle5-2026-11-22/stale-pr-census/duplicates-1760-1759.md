# CODEX-MERGE: duplicate PR census and closure

Role: CODEX-MERGE, close duplicates only; no merge of carrying PRs.

## PLAN

1. Verify Planning remote and exact PR heads/base.
2. Compare both duplicate file sets against carrying PRs and inspect four branch logs.
3. Close only strict-subset duplicates and capture close evidence, or report unique files.
4. Publish and remotely verify this evidence on Planning main.
5. Post per-PR verdict and evidence witness to the coordinator.

## Independent recalculation

Base fetched from the GitHub remote: develop `52a3c5446f41a1dd8678d99875e4cb1eee67874c`.
The exact refs were independently measured with `git ls-remote https://github.com/mcpdev80/baseharbor.git` and fetched to `refs/remotes/review/*` for the three-dot diffs and logs.

### PR #1760

Head: `5f6f3a98a66f2e18d8c76f68ab04dd7d285a276a`

Changed-file set from `develop...PR head` (4 paths):

```text
cmd/baha/app_apply.go
cmd/baha/app_workload_ports.go
cmd/baha/runtime.go
cmd/baha/workload_port_local_regression_test.go
```

### PR #1723

Head: `12a62523fc5f2259220aece4cc5619dcb8f4ae4d`

Changed-file set from `develop...PR head` (16 paths):

```text
cmd/baha/app_apply.go
cmd/baha/app_workload_ports.go
cmd/baha/application_provider_authorization.go
cmd/baha/commands.go
cmd/baha/env_destroy.go
cmd/baha/env_destroy_integration_test.go
cmd/baha/machine_coverage.go
cmd/baha/runtime.go
cmd/baha/workload_port_local_regression_test.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/application/provider_preferences.go
internal/deployment/environment_destroy_scope.go
internal/deployment/environment_destroy_scope_test.go
```

### PR #1759

Head: `22087745d27217bfe7b7bcbe66f36685cc9ba4ce`

Changed-file set from `develop...PR head` (3 paths):

```text
internal/application/shared_backends.go
internal/application/shared_backends_state.go
internal/application/shared_backends_state_version_test.go
```

### PR #1725

Head: `485103523b93d23877e2103974d7af22ef95f831`

Changed-file set from `develop...PR head` (19 paths):

```text
cmd/baha/app_apply.go
cmd/baha/app_workload_ports.go
cmd/baha/application_provider_authorization.go
cmd/baha/commands.go
cmd/baha/env_destroy.go
cmd/baha/env_destroy_integration_test.go
cmd/baha/machine_coverage.go
cmd/baha/runtime.go
cmd/baha/workload_port_local_regression_test.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/application/provider_preferences.go
internal/application/shared_backends.go
internal/application/shared_backends_state.go
internal/application/shared_backends_state_version_test.go
internal/deployment/environment_destroy_scope.go
internal/deployment/environment_destroy_scope_test.go
```

### Strict-subset results

- #1760 is a strict subset of #1723: 4/4 #1760 paths occur in #1723, zero paths exist only in #1760, and 12 paths exist only in #1723.
- #1759 is a strict subset of #1725: 3/3 #1759 paths occur in #1725, zero paths exist only in #1759, and 16 paths exist only in #1725.

Both subset conditions hold; closure was authorized by the mission. No merge, force push, or action on #1723/#1725 was performed.

## Branch logs

### `git log --oneline develop..PR #1760`

```text
5f6f3a98a hop PR 1723 to new develop 5ca8420c (0428-199 workloadport)
d7b4f1b3d hop PR 1723 to current develop 8b9a8f50645 (0428-199 workloadport)
8fe3c9bfb Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD
b9c2e483f hop develop 7d4351c6d645 into 0428-199 workloadport candidate (re-hop)
5c063c7f2 hop develop 42da7128e72 into 0428-199 workloadport candidate
71ac9ba51 Merge remote-tracking branch 'origin/develop' into codex/continue-0428-199
26755fc1e fix(0428-199): respect --workload-port on local apply/up path
```

### `git log --oneline develop..PR #1723`

```text
12a62523f Merge commit 'b2d9aeb446f1360f03e6f8a8c416b315e833a729' into HEAD
bfd01276f Merge commit '0768274c6f692bc0779202a1b9dc1fb222fce2ef' into HEAD
b2d9aeb44 Merge commit 'c463edf87ee' into lane-0428-199-workloadport
0768274c6 fix(app): tolerate nil-vs-empty providerPreferences in revalidate
d7b4f1b3d hop PR 1723 to current develop 8b9a8f50645 (0428-199 workloadport)
2f0f80786 Merge commit '8b9a8f50645db1dbaad4a5e1f2140930436d3ea7' into HEAD
8fe3c9bfb Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD
b9c2e483f hop develop 7d4351c6d645 into 0428-199 workloadport candidate (re-hop)
b3b0c2c9e test: prepare consent through destroy resolver
5c063c7f2 hop develop 42da7128e72 into 0428-199 workloadport candidate
38be89aa4 test: bind env destroy consent to stop plan
ac05cc4ef test: authenticate env destroy native fixture
62dd38f9b Merge develop 42da7128 into env destroy PR
8de37f58c ci: validate env destroy against coreless gates
d0616fc20 docs: retain env destroy rows in German coverage
5dd34a375 hop(0428-055): merge develop 513488eeb6d into cli2-env-delete for PR #1627
71ac9ba51 Merge remote-tracking branch 'origin/develop' into codex/continue-0428-199
e24bd481e docs: sync environment destroy command indexes
3d8aff0da test: fix native env destroy test imports
81aa4ca81 fix: process selected environment deployments independently
dff06723e Merge remote-tracking branch 'origin/develop' into cli2-env-delete
202b984e2 revert(test): preserve active 1615 runtime test ownership
cf82fe45a test(cli): cover environment destroy on native runtime
bb0424daa Merge current develop into 0428-055
e4777ac5d fix(cli): emit one confirmed environment destroy result
26755fc1e fix(0428-199): respect --workload-port on local apply/up path
96deb1f15 fix(cli): destroy environment scoped deployments safely
49e164ccb Merge commit '5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3' into cli2-env-delete
92cd73c43 Merge branch 'cli2-env-policy-head' into cli2-env-delete (base-heal r2)
c69d3fb6c cli2: add baha env destroy (env-scoped identity removal)
```

### `git log --oneline develop..PR #1759`

```text
22087745d hop PR 1725 to new develop 5ca8420c (0428-201 statever)
27e509757 hop PR 1725 to current develop 8b9a8f50645 (0428-201 statever)
1ec67313c Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD
0208f7259 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
cfd8851f7 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
b10cf253b Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
334588ee3 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
733decc09 Merge branch 'develop' of github.com:mcpdev80/baseharbor into codex/0428-201-refresh
48a4c476f Merge branch 'develop' of github.com:mcpdev80/baseharbor into codex/0428-201-refresh
9e3a0b25e Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
9bf4a72f7 0428-201: name shared backend state version mismatch
```

### `git log --oneline develop..PR #1725`

```text
485103523 Merge commit 'dd4e826f6c87c838950927a664f145ddc9a3b314' into HEAD
12a62523f Merge commit 'b2d9aeb446f1360f03e6f8a8c416b315e833a729' into HEAD
bfd01276f Merge commit '0768274c6f692bc0779202a1b9dc1fb222fce2ef' into HEAD
dd4e826f6 Merge commit 'c463edf87ee' into w201-0428-201-statever
b2d9aeb44 Merge commit 'c463edf87ee' into lane-0428-199-workloadport
0768274c6 fix(app): tolerate nil-vs-empty providerPreferences in revalidate
27e509757 hop PR 1725 to current develop 8b9a8f50645 (0428-201 statever)
d7b4f1b3d hop PR 1723 to current develop 8b9a8f50645 (0428-199 workloadport)
2f0f80786 Merge commit '8b9a8f50645db1dbaad4a5e1f2140930436d3ea7' into HEAD
1ec67313c Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD
8fe3c9bfb Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD
b9c2e483f hop develop 7d4351c6d645 into 0428-199 workloadport candidate (re-hop)
b3b0c2c9e test: prepare consent through destroy resolver
5c063c7f2 hop develop 42da7128e72 into 0428-199 workloadport candidate
38be89aa4 test: bind env destroy consent to stop plan
ac05cc4ef test: authenticate env destroy native fixture
62dd38f9b Merge develop 42da7128 into env destroy PR
8de37f58c ci: validate env destroy against coreless gates
d0616fc20 docs: retain env destroy rows in German coverage
5dd34a375 hop(0428-055): merge develop 513488eeb6d into cli2-env-delete for PR #1627
0208f7259 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
71ac9ba51 Merge remote-tracking branch 'origin/develop' into codex/continue-0428-199
e24bd481e docs: sync environment destroy command indexes
3d8aff0da test: fix native env destroy test imports
81aa4ca81 fix: process selected environment deployments independently
dff06723e Merge remote-tracking branch 'origin/develop' into cli2-env-delete
cfd8851f7 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
b10cf253b Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
334588ee3 Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
733decc09 Merge branch 'develop' of github.com:mcpdev80/baseharbor into codex/0428-201-refresh
48a4c476f Merge branch 'develop' of github.com:mcpdev80/baseharbor into codex/0428-201-refresh
9e3a0b25e Merge remote-tracking branch 'origin/develop' into codex/0428-201-refresh
202b984e2 revert(test): preserve active 1615 runtime test ownership
cf82fe45a test(cli): cover environment destroy on native runtime
bb0424daa Merge current develop into 0428-055
e4777ac5d fix(cli): emit one confirmed environment destroy result
9bf4a72f7 0428-201: name shared backend state version mismatch
26755fc1e fix(0428-199): respect --workload-port on local apply/up path
96deb1f15 fix(cli): destroy environment scoped deployments safely
49e164ccb Merge commit '5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3' into cli2-env-delete
92cd73c43 Merge branch 'cli2-env-policy-head' into cli2-env-delete (base-heal r2)
c69d3fb6c cli2: add baha env destroy (env-scoped identity removal)
```

## Closure certificates

PR #1760 was closed at 2026-11-22T07:08:19Z, state CLOSED, mergedAt null, head `5f6f3a98a66f2e18d8c76f68ab04dd7d285a276a`. Closing comment ID 7075734770 (2026-11-22T07:08:18Z): “Closing as a duplicate hop of #1723. Recomputed against develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c: #1760 changes 4 files and all 4 are present in #1723's 16-file diff. #1723 remains open; no merge or force action taken.”

PR #1759 was closed at 2026-11-22T07:08:21Z, state CLOSED, mergedAt null, head `22087745d27217bfe7b7bcbe66f36685cc9ba4ce`. Closing comment ID 7075735109 (2026-11-22T07:08:20Z): “Closing as a duplicate hop of #1725. Recomputed against develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c: #1759 changes 3 files and all 3 are present in #1725's 19-file diff. #1725 remains open; no merge or force action taken.”

Carrying PRs remain open at the measured heads: #1723 `12a62523fc5f2259220aece4cc5619dcb8f4ae4d`; #1725 `485103523b93d23877e2103974d7af22ef95f831`.

Exact `git ls-remote` witness after closure:

```text
12a62523fc5f2259220aece4cc5619dcb8f4ae4d refs/pull/1723/head
485103523b93d23877e2103974d7af22ef95f831 refs/pull/1725/head
22087745d27217bfe7b7bcbe66f36685cc9ba4ce refs/pull/1759/head
5f6f3a98a66f2e18d8c76f68ab04dd7d285a276a refs/pull/1760/head
```

## Planning publication and cleanliness

Planning repository `git remote -v`, verified before publication:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

No Docker or Podman commands or compose projects were started. No product files were changed.

Exact `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep ...` output after first publication:

```text
evidence/r28-welle5-2026-11-22/stale-pr-census/duplicates-1760-1759.md
```

First publication commit: f6bb18e2e1416aca2f48e569e7528576da0c8d37.

END_DONE codex-rev2-1736: closed duplicate PRs #1760 and #1759; #1723/#1725 remain open; reviewed heads 5f6f3a98a66f2e18d8c76f68ab04dd7d285a276a and 22087745d27217bfe7b7bcbe66f36685cc9ba4ce.
