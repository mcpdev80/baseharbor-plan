# Independent Codex disposition — PR #1842 draft/skip qualification

- PR: https://github.com/mcpdev80/baseharbor/pull/1842
- Exact reviewed head: `317d2f2593336a4e4dddfa7f4d304bc034ee5515`
- Base: `develop` at `a87da7d179e08d43e8987885c38ab459ff1d887d`
- Commit author: `w177-0428-284-demo-pin-1812` (matches card lane)
- Exact diff: one line in `docs/releases/v0.4.28.demo-ref`, `b41127723e523134a1c14ee3c36cf133237162ce` -> `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`. This is not a change to `scripts/release-requirements.json`.

## Verdict: B — ready PR and required checks must execute

The draft-only success is insufficient for acceptance because the required PR planner and final selection check were skipped. Independent source inspection used `.github/workflows/ci.yml` from base `a87da7d179e08d43e8987885c38ab459ff1d887d`:

- `ci.yml:1502`: `PR Selected Checks` has `if: always() ... && github.event.pull_request.draft == false`. A draft cannot produce the final required selected-check result.
- `ci.yml:529`: the selected native job itself is conditioned on `draft == false` and `needs.pr_native_impact.outputs.required == 'true'`.
- `ci.yml:556`: this is `set -euo pipefail`, not a draft condition. The native gate command is at `ci.yml:558`, inside the job whose draft/impact condition is at line 529.
- `ci.yml:1080`: `PR · Demo Pin` is also conditioned on `draft == false`, and additionally requires runtime, integration, or public-contract selection.

The exact-head draft run [45603924448](https://github.com/mcpdev80/baseharbor/actions/runs/45603924448), attempts 1 and 2, ran only the draft source/routing and Go shards; `PR Selected Checks`, Trusted Plan, native impact/native jobs, and Demo Pin were skipped. The PR was subsequently marked ready; ready-head run [45606949460](https://github.com/mcpdev80/baseharbor/actions/runs/45606949460) was still in progress at disposition time and is not acceptance evidence yet.

## Native and pin-check selection finding

I independently ran the trusted-base diff/planner read-only against the exact base/head diff. `pr-native-gate-plan.py` returned `{"include":[]}`. `pr-gate-plan.py` returned `selected_gates: []`, `fallback_used: true`, and the normal broad `go test ./... -count=1`, `go vet ./...`, and `go build ./...` validations. Thus no native runtime gate is selected for this one-file documentation pin; after ready, native skip is valid only if the trusted impact planner reports this empty selection and `PR Selected Checks` validates the skip.

However, the dedicated pin-validation branch in trusted `scripts/pr-gate-plan.py` at base line 1182 recognizes only `docs/releases/v0.4.27.demo-ref`; this candidate changes `docs/releases/v0.4.28.demo-ref`. The exact-head planner consequently treated the path as unresolved and used broad Go fallback. `PR · Demo Pin` at `ci.yml:1080` is not selected by that planner result. Therefore the current workflow does not establish that this v0.4.28 pin itself was validated. Before acceptance, record independent exact-pin validation or add/fix trusted-base selection so the dedicated pin check runs; then require a successful exact-head `PR Selected Checks` result. Native jobs need not be forced if the validated trusted native planner continues to select none for the data-only path.

## Disposition

The ruling is **B**, not A. The PR is now ready and its selected-check run must finish successfully; draft runs do not count. **Acceptance and merge remain withheld** pending that terminal required-check result and evidence that the v0.4.28 Demo SHA pin was specifically validated. No repository source or workflow was changed by this reviewer.
