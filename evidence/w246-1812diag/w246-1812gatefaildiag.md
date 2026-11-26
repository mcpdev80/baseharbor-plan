# w246 — 1812 post-retry gate fail diagnosis

- Card: 0428-284 / '1812 post-retry gate fail'
- Shift: w246
- Type: READ-ONLY DIAGNOSIS — NO writes, NO pushes, NO CI triggers, NO plan commits
- Feeds: w200's #1812 routing finalization

## PLAN
- Attest planning-repo remote, confirm evidence lives only in baseharbor-plan
- ls-remote develop tip + gh pr view 1812 (head 0922888af8-era, base develop)
- Enumerate all pull_request runs on that head; failing run full jobs table + failing log lines
- Root-cause mapping: quote deciding config lines; classify (a)/(b)/(c)/combination
- Post-#1842 verdict: does CI-reload-only delta still hit this failure? yes/no + why
- Write akte; END_DONE

## Base attestation
- Planning repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (origin = https://github.com/mcpdev80/baseharbor-plan.git; verified NOT the workers/ subdir phantom-checkout). No plan commit made this shift.
- develop tip (git ls-remote, runtime): `ae70964d7b80b779822b76107b70ea76782f998e` refs/heads/develop
- PR #1812: head `0922888af8fd70be4049cec529c69aebc057a356`, base `fcd449117e189c555c7530b9527cd22d3f6f25ff`, OPEN, not draft. Base SHA IS an ancestor of develop (git merge-base --is-ancestor passed).
- #1812 head side commits: `0922888a` sync, `f166a49f` sync, `394559ec` re-admit, `eafd5e6d` sync, `10129196` drop release-requirements.json, `3859d466` release-requirements add v0.4.28 rows, `2ea41620` merge develop, `64d3dc0e` merge develop, `9140b2cb` fix(ci): re-load candidate image before runtime publish.

## (1) PR runs on the head
- gh api runs per_page=100, filtered to head `0922888af8`: exactly ONE pull_request run.
  - Run `45709326054` — status completed, conclusion SUCCESS, event pull_request, created 2026-11-25T21:59:41Z, attempt 1.
- The mission's "failing head" is the older sync `e21b5c528923ddd610b8c5e709ff0d61294c211e` (same branch era, pre-re-final-sync). Runs on it:
  - Run `44884894925` — failure, pull_request, created 2026-11-21T08:26:29Z, attempt 1.
  - Run `44850246247` — failure, pull_request, created 2026-11-21T01:27:06Z, attempt 1.

## (2) Failing run jobs table (run 44884894925)
| Job | status | conclusion |
| --- | --- | --- |
| Workflow policy | completed | success |
| PR · Native gate plan | completed | success |
| PR · Trusted Plan | completed | success |
| PR · Source format | completed | success |
| Targeted HA · podman | completed | skipped |
| PR · Exact full Pre-Release | completed | skipped |
| PR · Main release source | completed | skipped |
| PR · Draft Go (shards) | completed | skipped |
| PR · Main release Go (shards) | completed | skipped |
| Targeted HA · docker | completed | skipped |
| Release Source Preflight | completed | skipped |
| PR · Draft source and routing | completed | skipped |
| PR · Native · native/docker/greenfield | completed | success |
| PR · Native · native/podman/installation-destroy | completed | success |
| PR · Native · native/podman/second-target-conflict | completed | success |
| PR · Native · native/docker/onboarding | completed | success |
| validate | completed | skipped |
| PR · Focused Python | completed | success |
| PR · Native Keycloak/Core · podman | completed | **failure** |
| PR · Native Keycloak/Core · docker | completed | **failure** |
| PR · Validation · go-build | completed | success |
| PR · Validation · cli-gofmt | completed | success |
| PR · Go unit · cli-0 | completed | success |
| PR · Go unit · owner | completed | success |
| PR · Go unit · cli-1 | completed | **failure** |
| PR · Go unit · cli-2 | completed | **failure** |
| PR · Go unit · packages | completed | success |
| PR · Go unit · cli-3 | completed | **failure** |
| PR · Runner Interface | completed | skipped |

Decisive observation: the Native Keycloak/Core and Go-unit groups ran and FAILED with environment-bound errors — they were SELECTED and executed, not silently skipped. The HA/Pre-Release/Main-Go/Draft-Go groups were skipped only because the base workflow (HA `push` trigger; release matrix) does not fire on a normal PR push.

## (3) Failing step log lines (verbatim, fetched via jobs/<id>/logs)
- PR · Go unit · cli-1 (`[error]Process completed with exit code 1.`):
  - `cli-1 failed: (package), TestPersesStatusWitnessNeverClaimsHealthyFromManifestFlag, TestPersesStatusWitnessNotConfiguredWithoutObservabilityBackend`
  - `app_status_result_test.go:233: baha status --json failed: operator authentication needs interactive setup but input is not a terminal`
  - `app_status_result_test.go:183: baha status --json failed: operator authentication needs interactive setup but input is not a terminal`
- PR · Native Keycloak/Core · podman (`[error]Process completed with exit code 1.`):
  - `--- FAIL: TestControlPlaneSingleDefaultNativeRuntimeInCI (0.00s)`
  - `bootstrap trust-plane package teardown failed: bootstrap trust-plane teardown could not begin: bootstrap trust-plane teardown target "w169-ci-bootstrap-fbfe2ff3" is not configured`
  - `bootstrap trust-plane teardown left residual resources: wächter cannot inspect residuals: no runtime provider available for target "w169-ci-bootstrap-fbfe2ff3"`
- Same teardown error in the docker Keycloak/Core job (target `w169-ci-bootstrap-3724a9c1`).

## (4) Root-cause mapping (deciding lines, PR base tree @ fcd44911)
- ci.yml 447-467 (id `select`, job `pr_native_impact`): computes `required` from `git diff --name-only BASE_SHA..HEAD_SHA` against `scripts/pr-native-gate-plan.py` + `scripts/pr-gate-coverage.json`. On this PR the only content diff is `cmd/baha/perses_lifecycle.go`.
- resolve_native_checks (validate-pr-gate-coverage.py, resolve_native_checks): a native gate is selected only when a changed component's component-ID appears in the gate's `source_components`. `cmd/baha/perses_lifecycle.go` owns component `source.cmd_baha_perses_lifecycle_go` (surfaces `source.gate.atomic.docker.data.capabilities`, `source.gate.atomic.podman.data.capabilities`).
- `native/docker/data-capabilities` / `native/podman/data-capabilities` gate lists 20 `source_components`, all package-style IDs (`cmd.baha.main.go`, `source.cmd.baha.app.broker.diagnostics.test.go`, …). **None lists `source.cmd_baha_perses_lifecycle_go`.** Verified by running the real planner (`python3 scripts/pr-native-gate-plan.py`) against the changed path → output `{"include":[]}`, i.e. `required=false` for that path in isolation.
- However the coverage validator `validate()` at the same base returned `PR gate coverage catalog is valid` (no missing-required-gate error), because the gate owner surface `source.gate.atomic.docker.data.capabilities` IS covered and `atomic/docker/data-capabilities` is `required_for` `['v0.4.22'..'v0.4.27']` (NOT v0.4.28). So the catalog is schema-valid and required-gate-present, but the per-file routing simply never maps `perses_lifecycle.go` to a native check.
- Classification: **(c) missing catalog rows** — specifically the per-file-to-native-check mapping is incomplete. It is NOT (a): the demo pin `b411`/`5ca92a7cd` has zero bearing — no demo component appears in any `source_components` of any native check, and the runtime-image reload in 9140b2cb lives in `.github/workflows/pre-release-runtime-suite.yml` (a release-HA path), never in the PR native-gate route. It is NOT (b) a `pr-target-tip`/ValueError mechanism — no ValueError path is hit; the planner returns an empty matrix cleanly.

## (5) What actually failed vs. the "routing" framing
- The Go-unit failures (`operator authentication needs interactive setup but input is not a terminal`) and the Native Keycloak/Core failures (`teardown target ... is not configured / no runtime provider available`) are **test-environment / host-runtime limitations on the shared hosted runner** (no pty, no configured bootstrap target). These are genuine test failures, not CI routing omissions.
- The single PR-native-gate group that DID select (`native/docker/greenfield`, `native/podman/installation-destroy`, `native/docker/onboarding`, `native/podman/second-target-conflict`) all passed. No PR-native-gate group failed on a routing gap.
- Net: the observed "gate fail" is an environment-bound test failure in the runner, not a route that failed to fire.

## (6) Post-#1842 verdict
- Question: after #1842 merges (develop pin → 5ca92a7cd) and #1812 absorbs that tip as ONE normal merge commit, does the predicted delta (CI reload only, per w241) still hit this failure?
- Answer: **NO** for the observed failures, for two independent reasons:
  1. The observed Go-unit and Native Keycloak/Core failures are runner/environment limitations (no pty, no bootstrap target), independent of the demo pin and of #1842. They would recur on any PR touching these tests regardless of the merge. #1842 changing the demo pin does not change them.
  2. The CI-reload-only delta (w241) lives in the **release HA path** (`pre-release-runtime-suite.yml`), which is gated behind `push` / `runtime-validation/ha/` triggers and never runs on a normal PR push — so it cannot "hit" the PR gate-fail at all. The PR-native-gate route (`pr-native-gate-plan.py` + coverage catalog) is unaffected by a demo-pin bump.
- Caveat (real, non-blocking finding): the per-file native-gate mapping remains incomplete — `source.cmd_baha_perses_lifecycle_go` (and the whole `cmd/baha/perses_lifecycle.go` change) is never selected into any native check. That is a latent coverage gap, not the observed failure. It would only surface if a future run required `native/docker/data-capabilities` to include that path. Fix = add `source.cmd_baha_perses_lifecycle_go` (and the `internal/application/perses_lifecycle.go`, `internal/metrics/perses_backend_status.go`, `internal/metrics/perses_dashboard_provision.go` rows) to the `source_components` of both `native/docker/data-capabilities` and `native/podman/data-capabilities` in `scripts/pr-gate-coverage.json`. That is a coverage-catalog change inside this card's write-set (scripts/), so it is implementable here, not a .github/** finding.

## Evidence
- Runs list: gh api runs per_page=100 (full transcript saved under session shell output; run IDs quoted verbatim above).
- Jobs tables: gh api repos/mcpdev80/baseharbor/actions/runs/44884894925/jobs.
- Log lines: gh api jobs/136787993375|136787993300|136787993316/logs (verbatim quotes above).
- Config lines: fetched from PR base tree @ fcd44911 via `git show fcd44911:scripts/pr-native-gate-plan.py`, `validate-pr-gate-coverage.py`, `pr-gate-coverage.json`, `release-requirements.json`, `.github/workflows/ci.yml`; planner executed against the changed path → `{"include":[]}`.
- develop tip: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `ae70964d7b80b779822b76107b70ea76782f998e`.
- Base provenance: `git merge-base --is-ancestor fcd44911 origin/develop` → ancestor confirmed.

## Cleanliness
- No containers/compose projects started this shift (read-only diagnosis). `docker ps -a` not witnessable here; no daemon state touched.
- /tmp scratch clones (`/tmp/bh-src`, `/tmp/bh-1812`) and helper .py/.json removed after use.

## repo-rule compliance
- Read-only diagnosis. No product writes, no pushes, no CI triggers, no plan commits. Planning remote attested; evidence path written only into baseharbor-plan (planning repo), not any product repo.

END w246-0428-284-1812diag DONE — one-line verdict: 1812's post-retry gate fail is an environment-bound runner limitation (no pty / no bootstrap target), NOT a CI routing gap; the observed failures are NOT fixed by the #1842 demo-pin merge because they are pin-independent, and the CI-reload delta lives in the release-HA path that never runs on a PR push. Latent real finding (non-blocking): `cmd/baha/perses_lifecycle.go` is missing from `native/docker,podman/data-capabilities` source_components in the coverage catalog.
