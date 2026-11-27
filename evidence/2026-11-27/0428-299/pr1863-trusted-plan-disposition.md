# PR #1863 Trusted Plan failure — resolver disposition

**Role:** REVIEW / disposition only. No product, resolver, planner, workflow, or card content was changed.

## Exact witnesses

- Product PR #1863 is OPEN at head `4160d53f736b3c978b1df028ff90cd2b7d033d49`, base `develop`; live develop at the inspected run is `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`.
- The relayed run ID `4591177930` does not resolve as an Actions run. The API returns the matching exact-head pull_request run as `45913103879`, attempt 1, FAILURE: https://github.com/mcpdev80/baseharbor/actions/runs/45913103879.
- Its `PR · Trusted Plan` log reports the resolver inputs `BASE_SHA=c167fa5d`, `HEAD_SHA=4160d53f`, `INTEGRATION_SHA=cd70d5676dcac76ccaa41af93b1d3dea07001882`, then reaches the trusted `pr-gate-plan.py` invocation and fails with `invalid trusted PR gate coverage catalog`: uncataloged `internal/stableid/lock_probe.go` and `internal/stableid/lock_probe_platform_test.go`. The subsequent `PR Selected Checks` failure is downstream (`UNIT_SCOPE` unset and `UNIT_RESULT=skipped`). The failure is not reported at `pr-diff-base.py:186`.
- The integration object is `cd70d5676dcac76ccaa41af93b1d3dea07001882` with parents `c167fa5dd323ae0746385caa2bdb8364ec7ad03f` and `4160d53f736b3c978b1df028ff90cd2b7d033d49`.

## Neutral resolver calculation

I read `scripts/pr-diff-base.py` at the develop source used by the run. The relevant checks are lines 126–150 (resolve a two-parent integration and validate forward base lineage), 163–167 (compute clean merge), and 169–240 (require the exact PR head as a parent and compare the integration tree with the clean merge). The workflow supplies the event PR head separately from `github.sha` as the integration (`.github/workflows/ci.yml:807–846`).

Re-running only the resolver calculation with the exact logged inputs:

```text
python3 scripts/pr-diff-base.py --target-base c167fa5dd323ae0746385caa2bdb8364ec7ad03f \
  --head 4160d53f736b3c978b1df028ff90cd2b7d033d49 \
  --integration cd70d5676dcac76ccaa41af93b1d3dea07001882
```

returns `broad_required=false`, `reasons=[]`, `merge_base_sha=c167fa5dd323ae0746385caa2bdb8364ec7ad03f`, and the three expected changed paths. Thus the resolver accepts the exact integration shape that the failing run passed to it; the Trusted Plan failure occurs afterward at the catalog admission check.

## Classification and tracking disposition

This is **not a product defect**, **not an environmental failure**, and **not a defect in the observed resolver path**. The actual failure is the expected fail-closed **trusted-base catalog prerequisite**: a candidate-side catalog row cannot authorize its own changed source files before the row exists in develop.

No new card and no extension are needed for these stableid rows. Existing card **0428-359** (`tasks/t-20261126-trusted-catalog-baseline-recovery-manifest.md`) and open Plan PR **#136** already list both exact IDs and paths as part of the seven-row trusted baseline, with Docker and Podman `data.capabilities` surfaces and `runtime_specific: true`. PR #136 is OPEN at `fe586a8da1f4a3b64b69c39f02960666d4443bee`; its scope is the existing baseline. The resolver allegation receives **no separate tracking**.

The Explained-Set for the same trusted-catalog admission pattern is #1860, #1861, #1862, and #1863: each has its own source set, and the existing 0428-359 baseline covers those sets. This does not claim that their failures occurred in `pr-diff-base.py`; the inspected #1863 run specifically failed on the two stableid paths in the trusted catalog.
