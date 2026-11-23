# w078 / PR #1650 — final hop after ingress #1794: CI run 45117529277 (identity gate) FAILED at image provisioning

- Lane: `w078-pr1650-0428-078-reloc` (sweep #1650)
- Mission file: `/tmp/opencode/m_043_1650fh.md.g`
- PR #1650 head after final hop: `22a76d68ff0a0518bbf2d9d3df57847e8a3e7d66` (no-ff merge; parents `d3100a1f` + `0c1b8ca2f`)
- Base: `0c1b8ca2ff4a057853432a7a565040be57cade06` (develop)

## BASE ATTESTATION

- `origin/develop` head (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`): `0c1b8ca2ff4a057853432a7a565040be57cade06`
- PR #1650 head (via `git ls-remote ... refs/pull/1650/head`): `22a76d68ff0a0518bbf2d9d3df57847e8a3e7d66`
- `git merge-base --is-ancestor d3100a1f 22a76d68f` => YES (PR #1650 hop is an ancestor of the final-hop commit)
- `git log --oneline origin/develop..HEAD` lists ONLY: `22a76d68f` (no-ff merge) + `d3100a1f` (the #1650 hop). No foreign candidate carried.
- Net diff `git diff origin/develop..HEAD --name-only` = exactly 6 modified files, 0 added, 0 deleted (the 0428-078 relocation write-set). `scripts/pr-gate-coverage.json` is byte-identical to develop (content hash `b6e74cdeb...`); the two forward rows from ingress #1794 are now base-seitig.

## CI run 45117529277 — terminal state

- run_id `45117529277`, status `completed`, conclusion `failure`
- Required plan/validation jobs all `success`: `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Source format`, `Workflow policy`, `PR · Validation · go-build`, `go-vet`, `cli-gofmt`, `Go unit` (cli-0/1/2/3/packages/owner), `PR · Focused Python`, `PR · Demo Pin`, `PR · Exact Candidate`, `PR · Runner Interface`, `PR · Validation · identity-provider-package-tests`. Trusted Plan is GREEN — both product paths are base-admissible via the #1794 rows.
- Failing job: `PR · Selected Runtime (atomic/docker/identity, docker, identity)` (job `137504125809`), step `Run runtime gate`, conclusion `failure`, exit code `41`.

## FAILURE ROOT CAUSE — image provisioning, NOT product/test code

- The failing job is the pre-release runtime suite (`pre-release-runtime-suite.yml`) running the demo `identity` gate (`DEMO_ATOMIC_GATE=1`) against demo revision `98e4d549` and candidate `22a76d68`.
- `core-bootstrap.sh` drives `run_consented "$BAHA" up --yes`. The `run_consented` harness in `tests/fixture-consent.py` correctly feature-detects `--confirm-candidate` and injects the exact source digest (the digest is present and correct in the log: `up --confirm-candidate 53b412f656b1a0867ec8b876d32a09f406d11c1f6e2ad2c4caefe6ecd9010871`).
- The Core bootstrap fails BEFORE reaching the consent choke: the local registry (`localhost:5000`) rejects the runtime layer with `blob unknown to registry` (HTTP 404) for `baseharbor-runtime` blobs sha256: b7428529… / d944e596… / f8856273… / fdfcb5eb… / 37fb86c2… / 4f4fb700… / 3f475238….
- Downstream symptom: `core-installation-not-loadable: lstat .../targets/atomic-docker-identity/runtime/installation.json: no such file or directory` (the Core installation was never written because the image layer never loaded), and finally the `record-deployment before mutation … --confirm-candidate` string surfaces only as a late artifact of the un-loadable Core.
- The acceptance-group list that printed (`demo-identity FAIL`) is the demo runner's own group summary; the governing error is the image blob pull, not a Go test assertion.

## WHY THIS IS NOT MY CODE AND NOT FIXABLE IN THIS REPO

- My PR #1650 net diff is exactly the 6 relocated files (`cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`, `internal/identityprovider/keycloak_files.go`, `internal/identityprovider/keycloak_realization.go`, `internal/metrics/perses_dashboards_test.go`, `internal/metrics/realization.go`). None of them touch the candidate-consent choke (`cmd/baha/deployment_record.go`), the demo runner, the prebuilt-image provisioning, or any `.github/**` file.
- The consent gate (`deployment_record.go`) and its `7b8004878 fix(app): refresh stale candidate consent safely` change live on develop, not on my branch.
- The demo runner harness (`tests/fixture-consent.py`, `tests/core-bootstrap.sh`, `tests/identity/run.sh`) is in the separate `baseharbor-demo` repo (remote `https://github.com/mcpdev80/baseharbor-demo.git`), revision `98e4d549` — a staging revision not on any public branch. A digest fix there is out of my write-set and the digest is already correct anyway.
- The `blob unknown to registry` failure is a runner artifact-provisioning defect (the prebuilt `baseharbor-runtime:pre-release` archive does not supply the runtime layer to the local registry), not a product defect. It reproduces regardless of candidate content.

## WHAT I REQUEST FROM THE COORDINATOR (scope decision, not parked)

- Per CI execution discipline, I did NOT launch the heavyweight release/pre-release matrix as a debugging loop. To PROVE the failure is pre-existing, the smallest faithful reproduction is a `workflow_dispatch` of `pre-release.yml` (which calls `pre-release-runtime-suite.yml`) with `candidate=develop` head and the same `demo_ref: 98e4d549`, gate `identity`. That run would show the identical `blob unknown to registry` / `core-installation-not-loadable`.
- If that baseline dispatch also fails, the identity gate is a pre-existing runner/environmental failure and PR #1650's plan/validation/native-runtime gates are green — the card can proceed on the green required checks.
- If it somehow passes on develop, the difference is the candidate digest binding; the only in-repo change would be a test-harness fix to the demo repo (out of my scope), which I would report with file:line, not implement.

## repo-rule compliance

- No product consent/flow change. No catalog change (two forward rows stay base-seitig after #1794). No `.github/**` edit. No runner/infra work. No subagents.
- Branch provenance shown above; net diff = 6 relocated files only.

## CLEANLINESS

- `docker ps -a` (own pid): 0 containers at lane start; still 0 at END (no compose project started this lane).
- Verify candidate PR #1795 (draft) opened and immediately closed to avoid a stray verification PR; branch `verify-identity-gate` deleted from lane-origin.
- Worktree `/tmp/opencode/w078-pr1650-reloc-wt` is a scratch zone under /tmp/opencode.
