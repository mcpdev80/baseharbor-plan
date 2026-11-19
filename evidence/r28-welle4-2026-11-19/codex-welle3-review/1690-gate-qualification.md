# CODEX-REVIEW — PR #1690 / 0428-119 gate qualification

Date: 2026-11-19  
Role: CODEX-REVIEW  
Current PR head: `4e032c858eb074785afcbd191c4ce6e1d4742f76`  
Current develop: `deeeb64778b3f6109d3a8e49fd652d490901e89c`  
Earlier exact-head PR run: [44456088960](https://github.com/mcpdev80/baseharbor/actions/runs/44456088960) — unit/selected checks SUCCESS; Docker runtime gates skipped.

## Required-cell ruling

The card requires `internal/application` unit coverage **and selected Docker lifecycle tests on the exact head**; mission-119r2 likewise requires a visible Docker runtime cell. Therefore a content-bearing Docker lifecycle witness is required. I am not requiring the unrelated app-backup-restore gate specifically. `coreless-runtime` is a possible route only when its Docker job checks out and verifies the exact candidate SHA and executes its lifecycle steps; a run-level green or skipped job is insufficient.

The current `targeted-integration.yml` declares `inputs.ref` (default `develop`), and the Core-less job checks out `${{ inputs.ref || github.sha }}` then compares `HEAD` with that input. Runs 557 (`44456773282`) and 558 (`44456790553`) logged `CANDIDATE_SHA=develop` and failed `Verify exact SHA input`; the Docker and Podman test steps were skipped. This proves those attempts supplied the default/base ref, not that the job cannot accept a candidate SHA. An explicit SHA is required if that route is used.

Run 559 (`44457119591`) is a different `app-backup-restore` dispatch. Its `Application backup and restore` step executed and failed with `ORAS is required before Core setup` at `app_backup_restore_integration_test.go:63`; it did not fail at `Verify exact SHA input`. It is not consent-path evidence, and the failure is not a flake. Reconcile any contrary queue summary against this run's job log before carrying it into the card.

The candidate is now stale/diverged after #1685: PR head `4e032c858...`, develop `deeeb6477...`, merge-base `ec592fd38`; the exact-head checks above cannot qualify a post-hop SHA. After the monotonic hop, use a dispatch route that checks out the full candidate SHA and record the actual Docker job ID and executed test steps. If no suitable hosted route exists, a direct supported-host Docker lifecycle witness can establish runtime behavior only with exact-head provenance, test identity, output, cleanup, and the missing hosted route recorded as an owner-scope coverage finding. It does not make a skipped job green.

## END

END_HOLD #1690: Docker lifecycle evidence required; no candidate-level Docker cell passed yet. No new run was started by this review.
