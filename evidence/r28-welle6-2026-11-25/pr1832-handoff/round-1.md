# PR #1832 handoff — round 1

Snapshot: 2026-11-24 UTC. Planning card: `t-20261116-r28-bug-metrics-discovery` (0428-290).

## Product PR state

- PR: https://github.com/mcpdev80/baseharbor/pull/1832 — open, not merged.
- The red-first test-only head `a442738cb5600975662aed5440755a942b4bee3b` is **not** the current PR head. Run [45478910054](https://github.com/mcpdev80/baseharbor/actions/runs/45478910054) completed with failure on its `d0a6f370` base. Its CI failure classification is below.
- Actual current PR head is `7c40e3d08b5a77fd77ce553f2bcbd36b8f7b3ef9`. Develop base is `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`; the branch already contains normal merge commit `07355c3e78a1355a5af265c835b439fc44400db2` with that develop tip as its second parent. Develop integration is **done**, not pending. Do not force-push or reset the PR back to `a442738`.
- The current candidate contains metrics detection/mapping code and corrected tests, but is not safe to merge. No local tests were run (Hosted CI only).

## Red-first CI classification

Run `45478910054` / head `a442738cb5600975662aed5440755a942b4bee3b` reached terminal failure. `PR · Validation · cli-guided-tests`, job `138750850316`, executed `go test ./cmd/baha -run '^TestGuided'`.

- `TestGuidedQuickInitDoesNotTreatBrunoRequestAsMetricsSource` and `TestGuidedQuickInitBindsQuarkusMetricsServicePortAndPath` failed before detector assertions because `mustWriteWizardTestFile` used `os.WriteFile` without creating parent directories. The helper’s behavior exists on develop; these new nested fixtures exposed a test setup defect. The final candidate adds `os.MkdirAll(filepath.Dir(path), 0o700)` before writing.
- `TestGuidedAdoptionSummaryFullyPopulated` strengthened the old green `TestAdoptionSummaryFullyPopulated` from generic `/metrics` wording to a service/port/path assertion. The develop witness only asserted generic wording, a too-weak assertion. The Owner also flagged the mapping input as an unproven fixture precondition. The final candidate explicitly checks that the fixture contains `application -> api:8080/metrics` before checking the summary output.
- On the `a442738` red-first run, both Docker and Podman guided and data-capabilities native jobs passed (static gate jobs `138750795667`, `138750795733`, `138750795832`, `138750795867`; selected-runtime jobs `138751660202`, `138751660288`, `138751660327`, `138751660421`). These are old-base diagnostic evidence only, not candidate acceptance evidence.
- The `a442738` trusted plan selected `cli-build`, `cli-guided-tests`, `cli-vet`, `source-contracts` and the four Docker/Podman data-capabilities/guided runtime surfaces. The `^TestGuided` selection is confirmed in job `138750850316`.

## Current candidate blockers

- Run [45485601446](https://github.com/mcpdev80/baseharbor/actions/runs/45485601446) is active on head `7c40e3d08b5a77fd77ce553f2bcbd36b8f7b3ef9`. `PR · Trusted Plan`, job `138770012853`, failed closed: eight changed production sources are uncataloged, and the trusted plan requires adding them to `scripts/pr-gate-coverage.json` with Docker/Podman runtime surfaces. The other four native jobs were still active at handoff: `138770122813`, `138770122864`, `138770123134`, `138770123173`. Do not treat this run as green or push another candidate while it is active.
- The mission excludes `scripts/**`; do not bypass trusted CI. A scope decision is required before changing the source coverage catalog. Keep PR #1832 open until the gate can pass within an authorized scope.
- Independent review `/root/independent_metrics_review` reviewed the complete nine-file diff at head `7c40e3d08b5a77fd77ce553f2bcbd36b8f7b3ef9`, base `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`. Blocking finding: detector evidence stores only a repository-global endpoint path, then quick init pairs it with the sole workload service/port, without proving that the exporter belongs to that service/module. A lone unrelated Caddy workload can still be mapped to a Quarkus/Spring exporter path. Add source/build-context-to-service association or fail closed and require explicit confirmation; add an unrelated-workload/exporter-module regression. The review also noted Spring YAML list-form exposure is not parsed. Candidate is not merge-safe; re-review any changed exact head.

## Next steps for the worker

1. Wait for run `45485601446` to reach terminal and record every exact-head job result. Its trusted-plan failure remains blocking even if the native jobs pass.
2. Obtain the Owner’s scope decision for the required `scripts/pr-gate-coverage.json` catalog entries; do not edit excluded paths, suppress checks, or bypass CI without that authorization.
3. Resolve the independent review’s exporter-to-workload association finding. Fail closed and prompt for confirmation whenever the module/config evidence cannot be tied unambiguously to the selected service. Add a regression where the exporter module is separate from the only unrelated workload. Preserve the fixture parent-directory creation and explicit metrics-source fixture precondition, adjusting them if needed.
4. Integrate any newer `develop` tip with a normal merge before pushing. Keep the PR diff limited to the authorized scope and push coherent candidates only after the current run is terminal.
5. On the resulting exact head, prove the trusted selector runs the intended test (`^TestGuided`) and selects only applicable gates. Obtain two exact-head green IDs, including independent Docker and rootless Podman evidence, and verify `PR Selected Checks` from integration 15368. Hosted CI only; no local test execution.
6. Get an independent review of the complete final diff at the exact head, resolve findings, then follow the existing expected-HEAD squash merge gate. Only after verified merge should the worker accept/close 0428-290 and publish the final Planning evidence.

## Session stop

The assigned w122 session stops implementation at this handoff. It did not merge PR #1832 or accept/close the card.
