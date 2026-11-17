# CODEX-REVIEW — Luna batch21

Date: 2026-11-17. Role: CODEX-REVIEW (Luna). Read-only review; no merge.

## Candidate and exact-head witnesses

- PR #1676, card 0428-100: `ea7d0b2fde78f2fc6e7efc1bb9929b289dbe28cd`, base `develop`, OPEN, DRAFT (`isDraft=true` at review head).
- PR head and run head agree exactly. Pull request workflow run [44000884721](https://github.com/mcpdev80/baseharbor/actions/runs/44000884721) completed SUCCESS on that SHA.
- `PR Selected Checks` job 133766197763: SUCCESS. `PR · Go unit · packages` job 133764424914: SUCCESS. Build, vet, format/readability and workflow policy jobs also succeeded. Several non-selected/native/release jobs were skipped; this draft run does not establish their execution.
- Exact PR diff contains only `internal/metrics/prometheus_verify.go` and new `internal/metrics/prometheus_verify_workload_test.go`. None of the #1665 paths are touched (`app_status_result.go`, `perses_infra_dashboards*.go`, `perses_prometheus_datasource.go`).
- PR metadata was checked live under account `mcpdev80`; no GitHub review or merge action was taken.

## Verdict — #1676 / 0428-100: CHANGES REQUESTED

The candidate does not satisfy the mission's registration or deploy-path criteria. It adds an early return in `VerifyProviderSourcesAt` (lines 137–144), which accepts a workload-only manifest without registering any provider source or changing the real deploy path. The added tests call `VerifyProviderSourcesAt` directly with temp directories; they do not deploy the app, inspect the produced `runtime-sources.json`, or prove a source was registered. No negative service-app registration regression is added.

The round-1 evidence describes an empty-source guard as fail-closed, but the current develop implementation at the candidate's parent `e6cce9c73b8edddeff98fa858e83e4b08e8836ef` has `if err != nil || len(sources) == 0 { return err }`. When `ListMetrics` returns an empty slice and nil error, that branch returns nil. The candidate repeats the same behavior after its early return. Thus the empty-registry unit case does not demonstrate the claimed fail-closed deploy failure, and the review has no reproducible real deploy-path witness showing that this change fixes the reported issue.

### Required correction recipe

1. Reproduce the reported failure on the real deploy path at the exact current develop baseline. Capture the workload-only app input, deploy invocation, generated shared `runtime-sources.json`, and the verifier/downstream failure. If the verifier is not the failing component, correct the diagnosis and target the actual registration step.
2. Implement registration in that existing deploy/registration path. Do not treat missing registration as success by bypassing verification; preserve fail-closed behavior for genuinely missing required sources.
3. Add a regression that drives the real deploy path for a workload-only app, asserts the intended source appears in the generated shared runtime snapshot, and demonstrates positive verification. Add the mission-required service-app negative/compatibility assertion proving service cases still register as before. Keep tests in the existing CI-selected package/group and show the exact test IDs and selection trigger.
4. Stop and return for review if the real deploy reproducer does not show the claimed failure, if the needed source contract is unclear, or if the fix requires touching #1665-owned files. Keep #1665's paths untouched.

No further product tests were run during this read-only review; the recorded CI run is the worker's exact-head evidence. Re-review is required after a new exact head and corresponding CI run.

## Turn-start coordination flags

`python3 coordinator/scripts/basics-check.py` reported: worker pool 1/3 (ornith 1/2, flash 0/1); holds `ornith:2` and `flash:1` with reason `NO_ELIGIBLE_WORK`; idle lane `0428-100-` awaiting END/inbox handling; and 41 open PRs. These coordinator-owned flags are reported for follow-up; this review did not dispatch work or alter lanes.

## Review identity

Session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codex mode; displayed model `GPT-6-Luna` (Codeman screen identity); review time 2026-11-17 02:19 UTC. Review source was the live GitHub PR diff and exact-head workflow metadata plus the Planning task/evidence.

## END

END_DONE mission-luna-batch21 — #1676 CHANGES REQUESTED. The exact-head selected CI passed, but the candidate bypasses verification instead of registering a source through the real deploy path; the direct verifier tests do not cover deployment or service-app compatibility. No GitHub approval, product change, or merge.
