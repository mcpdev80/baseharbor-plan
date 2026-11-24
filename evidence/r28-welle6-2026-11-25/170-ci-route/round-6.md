## PLAN

- #3.8 Befund for Owner CI review: hosted runs are being cancelled by the shared workflow-level concurrency group in `.github/workflows/pre-release.yml:6-8`.
- The group expression at line 7 uses the per-run `baseharbor-develop-${github.run_id}` value only when `inputs.develop_mode` is true; otherwise every run uses the constant `baseharbor-release-qualification`. `develop_mode` is not a `workflow_dispatch` input (lines 2149-2179); it exists only as a `workflow_call` input (lines 2185-2191). Thus independent workflow_dispatch runs from `develop` and feature lanes contend in the same group.
- `cancel-in-progress: false` at line 8 does not preserve multiple pending runs. GitHub's default concurrency queue is `single`: only one pending run is retained, and a newer run in the same group cancels/replaces the existing pending run. See [GitHub Actions concurrency documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).
- Observed sequence (all had zero jobs when checked):

  | Run | Created | Head branch / SHA | Terminal or observed state | Correlation |
  | --- | --- | --- | --- | --- |
  | [45444093143](https://github.com/mcpdev80/baseharbor/actions/runs/45444093143) | 17:02:39 UTC | `lane-0428-279-mcpcontract` / `25c9480c5d69ef4bd700175529c906426268b2cf` | cancelled 17:04:50 UTC | Replaced when the next same-group run arrived |
  | [45444503754](https://github.com/mcpdev80/baseharbor/actions/runs/45444503754) | 17:04:48 UTC | `develop` / `f14fb87c8f5afd91168e4f174d620c9f00e6341e` | cancelled 17:06:35 UTC | This lane's v0.4.28 / config-matrix dispatch; replaced when the next same-group run arrived |
  | [45444841904](https://github.com/mcpdev80/baseharbor/actions/runs/45444841904) | 17:06:33 UTC | `lane-0428-279-mcpcontract` / `25c9480c5d69ef4bd700175529c906426268b2cf` | pending at 17:06:35 UTC | Newer run occupying the pending slot |

- This timing matches the configured single-pending behavior and explains why run 45444503754 ended `cancelled` before creating jobs. It did not check out the demo repository and produced no config-matrix result; there is still no hosted acceptance evidence for #170.
- Disposition: #170 remains OPEN and draft. No PR changes or workflow changes were made. Further dispatches of `Release · Pre-Release Validation` are on HOLD until the Owner signals that the window is free; #1826 runs go first.
- Owner review note: isolate independent validation lanes or enable an appropriate queue in the workflow concurrency policy so pending CI candidates are not silently replaced. This is a finding/recommendation only, not an implementation authorization.

END_DONE w113b-r2 round-6: concurrency root cause documented for CI review; no dispatch; #170 remains open.
