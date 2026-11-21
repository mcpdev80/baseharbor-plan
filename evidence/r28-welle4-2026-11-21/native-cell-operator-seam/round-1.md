# 0428-209 native cell operator seam — exact-head evidence

- PR: [#1740](https://github.com/mcpdev80/baseharbor/pull/1740)
- Branch: `lane-0428-209-native-cell-operator-seam`
- Exact candidate SHA: `0ffe093357d9f7fb52f5e7542f4ade41e48fab1b`
- Trigger: `pull_request` update to #1740, stacked on `lane-0428-198-cli-shard-operator-env`
- Run: [44868911131](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131)

## Test to gate mapping

| Exact test | Mapped check | Job | Result |
| --- | --- | --- | --- |
| `cmd/baha::TestControlPlaneSingleDefaultNativeRuntimeInCI` | `PR · Native Keycloak/Core · docker` | [136738825463](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131/job/136738825463) | PASS; log contains `--- PASS: TestControlPlaneSingleDefaultNativeRuntimeInCI (58.91s)` |
| `cmd/baha::TestControlPlaneSingleDefaultNativeRuntimeInCI` | `PR · Native Keycloak/Core · podman` | [136738825465](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131/job/136738825465) | PASS; log contains `--- PASS: TestControlPlaneSingleDefaultNativeRuntimeInCI (56.97s)` |

The regression assertion verifies `effectiveTarget` resolves the registered bootstrap Target only after selecting it, and that the selected runtime matches the native Docker/Podman cell. Target creation continues to use the shared `runWithIO` seam; no private auth stamp or production enforcement change was added.

## Full PR result and limitation

Run 44868911131 is terminal `failure` for the overall PR. `PR · Go unit · cli-0` fails `TestAppListAllTargetsWorksAfterInstallationDestroy` (`app_list_all_targets_test.go:26`), which is the separate 0428-210/#1739 defect. `PR Selected Checks` therefore fails. This card's native test binding is proven on the exact SHA, but #1740 is not mergeable until the stacked PR's required checks are green.

## Local verification

`go test ./cmd/baha -run '^TestControlPlaneSingleDefaultNativeRuntimeInCI$' -count=1` passes in the local environment by taking the documented skip path when native opt-in is absent. Hosted Docker and Podman results above are the live runtime evidence.
