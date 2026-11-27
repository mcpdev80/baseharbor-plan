# Combined exact review: w362 0428-249 edit set

Verdict: CHANGES

Review target: product candidate range `6ab5310d17358bc0f4c86ef09bea476b82517e3e..0b343af5ea895d23cbe808fda50a66d550552bc6`. It consists of workflow commit `8c83c7091479ab4001a1fc178f96dae788264eac` and fixture commit `0b343af5ea895d23cbe808fda50a66d550552bc6`. The diff changes exactly `.github/workflows/supplemental-release-validation.yml`, `.github/workflows/targeted-demo-acceptance.yml`, `.github/workflows/targeted-integration.yml`, `scripts/test_ci_check_routes.py`, and `scripts/test_pr_selected_runtime_matrix.py`; no product implementation or other test file is changed.

Authorization checked: `b45cc52f2f09079e0be0dc4dbb8615d16fbcd09d`, `evidence/2026-11-27/0428-249/four-class-fix-disposition.md`, authorizes narrow fixture/assertion changes only in the two named test files for stale workflow-shape expectations. The accepted workflow scope is in `evidence/2026-11-27/0428-249/workflow-integrity-review.md:89-98` and `qualification-workflow-integrity.md:9-15, 87-100, 160, 226-240` (ACCEPT basis `0637bc3c0`).

## Combined-diff review

The two fixture files make narrow, purpose-bound adjustments and retain the behavioral checks:

- The two Podman route cases no longer require the shared `resolve_candidate` prerequisite to have an `if:` predicate; the helper skips only that resolver and still evaluates routed gate jobs, including the existing positive and negative push/dispatch cases (`scripts/test_pr_selected_runtime_matrix.py:222-263`).
- The Coreless aggregator assertion now requires both `resolve_candidate` and `pr_selected_coreless_lifecycle_shards`, while retaining the shard-result assertion (`scripts/test_pr_selected_runtime_matrix.py:86-96`).
- The concurrency fixture checks the run-unique orchestrator and evidence-job keys containing the resolver SHA plus gate/runtime identity, and checks Docker/Podman distinction (`scripts/test_pr_selected_runtime_matrix.py:119-148`).
- Docker and Podman route assertions now expect checkout of `needs.resolve_candidate.outputs.candidate_sha`, replacing the stale raw-input checkout expectation (`scripts/test_ci_check_routes.py:124-139`).

The policy/actionlint failures on prior head `6ab5310d1` were the undefined `matrix.runtime`, `matrix.group`, and `matrix.gate` contexts in `targeted-integration.yml` at lines 636, 1170, and 1286. Commit `8c83c7091` replaces those expressions; the fixture commit does not touch workflow files. The owner audit's note that those earlier workflow-ruling points were already in `6ab5310d1` is recorded, but the object diff and run logs show the undefined matrix expressions on that exact head, so the replacements are assessed against the ACCEPT contract here.

The combined candidate still falls short of the accepted concurrency-key contract. The accepted pattern requires a resolved candidate SHA, gate/runtime identity, and run ID, without a raw ref key. Current workflow lines leave these gaps:

- `.github/workflows/targeted-integration.yml:636` and `:1286` include gate identity but omit runtime identity.
- `.github/workflows/targeted-integration.yml:1170` includes `github.ref_name` in the evidence concurrency key; that is a mutable ref key, not the resolved gate identity.
- `.github/workflows/targeted-demo-acceptance.yml:248` keys `reference_journey` by resolved SHA and gate name but omits `needs.resolve.outputs.runtime`.

All newly added workflow concurrency blocks use `cancel-in-progress: false`. The workflow diff adds no triggers, permissions, secrets, caching, product paths, or test paths beyond the two authorized test fixtures.

## Required forward corrections

1. In `targeted-integration.yml:636`, include `inputs.runtime` with the resolved SHA, `inputs.gate`, and run ID.
2. In `targeted-integration.yml:1170`, remove `github.ref_name`; use the fixed `v0421_ha` job/gate identity with resolved SHA, `matrix.runtime`, and run ID.
3. In `targeted-integration.yml:1286`, include `inputs.runtime` with resolved SHA, `inputs.gate`, and run ID.
4. In `targeted-demo-acceptance.yml:248`, include the resolved runtime output in the `reference_journey` key.
5. Add fixture assertions for those runtime dimensions and the absence of raw-ref concurrency keys; then run fresh Hosted validation on the final exact head. The prior run `45931118156` was on `6ab5310d1` and is not qualification for `0b343af5e`.

#1812 remains unqualified and must not merge. Its qualification follows the owner sequence only after Demo #183 is merged and its source pin is advanced; no test run on the present review range establishes that qualification.

## Publication provenance

Executing reviewer and commit identity: `w255-0428-251-demo170codex` <`w255-0428-251-demo170codex@baseharbor.local`>. Planning base: live `origin/main` `ef0bcfbcf55ad0e0aaaa552c3f2b42d9f72dc6f8`. Commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`. Pre-push identity gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.
