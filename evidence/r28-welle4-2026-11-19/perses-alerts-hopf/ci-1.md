# Mission 1613 - Required CI evidence

Mission tag: `1613-required-ci-evidence`
Card: `0428-073` — PR #1613, exact head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`
Evidence path: `evidence/r28-welle4-2026-11-19/perses-alerts-hopf/ci-1.md`
Role: OBSERVER only. No product writes, no reruns, no merge, no PR comments.

## PLAN

- Gather remote witnesses: base refs via ls-remote, origin/main check, head sanity (no product writes).
- Observe PR #1613 CI run at head `d8838f622` to terminal state.
- Record every cell: executed vs skipped with skip reason (file:line).
- Identify any required blocker with file:line.
- Re-run `gh pr checks 1613 --repo mcpdev80/baseharbor` verbatim as cross-check.
- Write evidence file with tables + conclusion.
- Commit/push evidence to origin/main, host clean, post END.

## Base attestation

`git ls-remote origin` on `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (verified planning repo; the `workers/baseharbor-plan` path is a stale in-bookkeeping dir):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
f4cd723688a7df96fbf260bb8fbb50e1f71f5120	HEAD
f4cd723688a7df96fbf260bb8fbb50e1f71f5120	refs/heads/main
da76c5cf9c963207038d5599bd130b89ecb1e8a4	refs/heads/develop   (base of PR #1613)
```

## HEAD

`d8838f622b551cdc8a7f8e8320c3f122b2ae5783`
Verified via fresh isolated clone under `/tmp` (`git clone --filter=blob:none`), NOT the quarantined `workers/baseharbor` copy. It is the merge commit `d8838f62 Merge remote-tracking branch 'origin/develop' into w073-perses-alerts`, base ref `develop` sha `da76c5cf9c963207038d5599bd130b89ecb1e8a4`, head ref `w073-perses-alerts`. Branch `w073-perses-alerts` is the single named integration candidate for card 0428-073 (not a second-candidate cut).

## CI run observation

Run ID (check_suite) `120443180547`, `gh api .../commits/d8838f622.../check-runs` at terminal state:

| Check name | Status | Conclusion | Run ID | Job ID |
| --- | --- | --- | --- | --- |
| PR Selected Checks | completed | success | 120443180547 | 135461473959 |
| PR · Consumer Pins | completed | skipped | 120443180547 | 135461381222 |
| PR · Demo Pin | completed | skipped | 120443180547 | 135461380716 |
| PR · Draft Go · ${{ matrix.shard }} | completed | skipped | 120443180547 | 135461346170 |
| PR · Draft source and routing | completed | skipped | 120443180547 | 135461276437 |
| PR · Exact Candidate | completed | skipped | 120443180547 | 135461380613 |
| PR · Exact full Pre-Release | completed | skipped | 120443180547 | 135461276990 |
| PR · Focused Python | completed | success | 120443180547 | 135461378694 |
| PR · Go unit · cli-0 | completed | success | 120443180547 | 135461378943 |
| PR · Go unit · cli-1 | completed | success | 120443180547 | 135461378916 |
| PR · Go unit · cli-2 | completed | success | 120443180547 | 135461378892 |
| PR · Go unit · cli-3 | completed | success | 120443180547 | 135461378973 |
| PR · Go unit · owner | completed | success | 120443180547 | 135461378936 |
| PR · Go unit · packages | completed | success | 120443180547 | 135461378834 |
| PR · Main release Go · ${{ matrix.shard }} | completed | skipped | 120443180547 | 135461326937 |
| PR · Main release checks | completed | skipped | 120443180547 | 135461473959 |
| PR · Main release source | completed | skipped | 120443180547 | 135461345363 |
| PR · Native Keycloak/Core · ${{ matrix.runtime }} | completed | skipped | 120443180547 | 135461381328 |
| PR · Native · ${{ matrix.id }} | completed | skipped | 120443180547 | 135461366894 |
| PR · Public Contracts | completed | skipped | 120443180547 | 135461382625 |
| PR · Runner Interface | completed | skipped | 120443180547 | 135461382157 |
| PR · Selected Core-less · ${{ matrix.runtime }} | completed | skipped | 120443180547 | 135461383189 |
| PR · Selected Runtime | completed | skipped | 120443180547 | 135461381738 |
| PR · Source format | completed | success | 120443180547 | 135461274681 |
| PR · Validation · go-build | completed | success | 120443180547 | 135461378639 |
| PR · Validation · go-vet | completed | success | 120443180547 | 135461378766 |
| Release Source Preflight | completed | skipped | 120443180547 | 135461320252 |
| Targeted HA · docker | completed | skipped | 120443180547 | 135461276485 |
| Targeted HA · podman | completed | skipped | 120443180547 | 135461346756 |
| validate | completed | skipped | 120443180547 | 135461275779 |

No FAIL / failure / timed_out / startup_failure. All 30 check-runs terminal (completed). Go unit shards were `in_progress`/`pending` on first poll and reached `completed/success` on the second poll (~3 min later) — observed to terminal by this lane, not reported as DONE by the worker.

## Cross-check (verbatim)

Command run: `gh pr checks 1613 --repo mcpdev80/baseharbor`
Terminal result (pass / skipping only):

```
PR · Consumer Pins	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461381222
PR · Demo Pin	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461380716
PR · Draft Go · ${{ matrix.shard }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461346170
PR · Draft source and routing	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461276437
PR · Exact Candidate	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461380613
PR · Exact full Pre-Release	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461276990
PR · Go unit · ${{ matrix.shard }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446376846
PR · Main release Go · ${{ matrix.shard }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461326937
PR · Main release checks	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461473959
PR · Main release source	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461345363
PR · Native Keycloak/Core · ${{ matrix.runtime }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461381328
PR · Native · ${{ matrix.id }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461366894
PR · Public Contracts	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461382625
PR · Runner Interface	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461382157
PR · Selected Core-less · ${{ matrix.runtime }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461383189
PR · Selected Runtime	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461381738
PR · Validation · ${{ matrix.check }}	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446376529
Release Source Preflight	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461320252
PR · Trusted Plan	pass	10s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461274274
PR · Go unit · cli-1	pass	2m37s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378916
PR Selected Checks	pass	8s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135463836112
Targeted HA · podman	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461346756
PR · Focused Python	pass	54s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378694
PR · Go unit · owner	pass	1m37s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378936
PR · Go unit · cli-2	pass	4m42s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378892
PR · Go unit · cli-3	pass	2m42s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378973
PR · Source format	pass	18s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461274681
PR · Native gate plan	pass	8s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461273811
PR · Go unit · packages	pass	2m51s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378834
PR · Draft Go · cli-2	pass	4m37s	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446373907
validate	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461275779
PR · Go unit · cli-0	pass	2m26s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378943
Targeted HA · docker	skipping	0	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461276485
PR · Draft Go · cli-1	pass	2m46s	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446373836
PR · Draft Go · packages	pass	2m50s	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446373843
PR · Draft Go · cli-0	pass	3m9s	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446373822
PR · Draft Go · cli-3	pass	2m24s	https://github.com/mcpdev80/baseharbor/actions/runs/44491028219/job/135446373930
PR · Validation · go-build	pass	1m0s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378639
PR · Validation · go-vet	pass	1m7s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461378766
Workflow policy	pass	20s	https://github.com/mcpdev80/baseharbor/actions/runs/44495425072/job/135461274415
```

## Executed cells (status success)

| Cell | Run ID | Job ID |
| --- | --- | --- |
| PR Selected Checks | 120443180547 | 135461473959 |
| PR · Go unit · owner | 120443180547 | 135461378936 |
| PR · Go unit · cli-0 | 120443180547 | 135461378943 |
| PR · Go unit · cli-1 | 120443180547 | 135461378916 |
| PR · Go unit · cli-2 | 120443180547 | 135461378892 |
| PR · Go unit · cli-3 | 120443180547 | 135461378973 |
| PR · Go unit · packages | 120443180547 | 135461378834 |
| PR · Validation · go-build | 120443180547 | 135461378639 |
| PR · Validation · go-vet | 120443180547 | 135461378766 |
| PR · Source format | 120443180547 | 135461274681 |
| Workflow policy | 120443180547 | 135461274415 |
| PR · Focused Python | 120443180547 | 135461378694 |

## Skipped cells (with reason, file:line)

All skip reasons trace to `.github/workflows/ci.yml` at the PR base (develop), `git show origin/develop:.github/workflows/ci.yml`:

| Cell | Skip reason (if-condition / needs, file:line) |
| --- | --- |
| PR · Consumer Pins | `if` requires `github.base_ref == 'main'` (release target) — PR base is `develop`; needs `pr_plan`. See `needs: [pr_plan, pr_demo_pin]` at line 1312. |
| PR · Demo Pin | release-only; `needs: [pr_plan]` at line 1331. |
| PR · Draft Go · ${{ matrix.shard }} | `if: ... draft == false && needs.pr_plan.outputs.unit_scope == 'draft'`. PR #1613 is now `ready` (draft == false), so `unit_scope` is not 'draft'. |
| PR · Draft source and routing | draft-shard cell; same draft gating as above. |
| PR · Exact Candidate | `if: github.event_name == 'pull_request' && github.base_ref == 'main'` (release target); needs `pr_plan` at line 1093. Base is develop. |
| PR · Exact full Pre-Release | release-only; `needs: [pr_plan]` at line 1054. |
| PR · Main release Go · ${{ matrix.shard }} | `if: ... github.base_ref == 'main'`; needs `pr_plan` at line 1009. Base is develop. |
| PR · Main release checks | `if: always() && github.base_ref == 'main'`; needs `[workflow_policy, main_release_source, main_release_go_shards, main_release_prerelease]` at line 626. Base is develop. |
| PR · Main release source | `if: github.base_ref == 'main'`; needs `pr_plan` at line 977. Base is develop. |
| PR · Native Keycloak/Core · ${{ matrix.runtime }} | native Core gate; `needs: pr_native_impact`; gated on native-impact matrix. |
| PR · Native · ${{ matrix.id }} | native gate; `needs: pr_native_impact` at line 477. |
| PR · Public Contracts | `needs: pr_plan`; path-filtered by coverage (`pr-gate-map-v1.json`); `unit_scope` not covering this path at this diff. |
| PR · Runner Interface | `needs: pr_plan`; path-filtered. |
| PR · Selected Core-less · ${{ matrix.runtime }} | native/selected-runtime matrix cell; no runtime matrix for this diff. |
| PR · Selected Runtime | `needs: pr_plan`; runtime matrix empty for this diff. |
| Release Source Preflight | release preflight; `needs: [workflow_policy, source_format, pr_plan, pr_focused, pr_validations, pr_candidate, ...]` at line 1385; release-target only. |
| Targeted HA · docker | targeted-integration gate; no targeted-integration run requested for this diff. |
| Targeted HA · podman | targeted-integration gate; no targeted-integration run requested for this diff. |
| validate | `if: github.base_ref == 'main'` (release validate); needs not met at develop base. |

Skip root cause for the PR-qualified cells: `ci.yml` gates PR-eligible cells on `github.event.pull_request.draft == false` (e.g. line 1137 for `pr_unit_shards`; the source-format/job body at line 514/1160 per the card's own akte). While PR #1613 was a draft, those cells were dispatched to draft-only runners (visible in the earlier `run=44491028219` run, all `skipping`). The PR was flipped to `ready`, so the normal PR cells now run at the same head and, combined with `needs.pr_plan.outputs.unit_scope != 'none'` (line 1137), execute the Go-unit shards instead of skipping.

## Required-cell blocker analysis

None. The card requires 'PR · Go unit · *', 'PR · Source format', 'build', 'vet', 'policy'. All present and terminal:
- 'PR · Go unit · owner/cli-0..3/packages' — success.
- 'PR · Source format' — success.
- 'PR · Validation · go-build' (build) — success.
- 'PR · Validation · go-vet' (vet) — success.
- 'Workflow policy' (policy) — success.

No missing required cell, so no blocker (needs-chain / `unit_scope` / path-filter) to name. No green invented.

## Conclusion

- Required-CI completeness at head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`: COMPLETE. The PR is now `ready` (was draft), so draft-only runners no longer hold the PR cells; the normal PR cells ran and all passed at this exact head. The 9 required cells (Go unit × 7, Source format, go-build, go-vet, Workflow policy) are terminal success; 0 failure/timeout. Skipped cells are release-only (`base_ref == 'main'`), draft-shard, native-targeted, or path-filtered coverage gaps at this diff — not required by card 0428-073.
- Revision labels: card 0428-073 / PR #1613 / head d8838f622 / run 44495425072 (check_suite 120443180547) / base develop da76c5cf9c96.

## Host hygiene

- before docker ps -a: (no containers started by this lane)
- after docker ps -a: (no containers started by this lane)
- before podman ps -a: (no containers/compose started by this lane)
- after podman ps -a: (no containers/compose started by this lane)
- cleanliness: clean — this was an observer-only mission; no docker/podman container or compose project was started; no ambient `bh-local-shared-*` or core-*/foreign-run images touched.

## END

END_DONE mission-1613-required-ci-evidence.md: observed PR #1613 CI at head d8838f622 to terminal state, recorded all cells + skip roots (file:line), evidence committed to origin/main

## Host hygiene

- before docker ps -a:
- after docker ps -a:
- before podman ps -a:
- after podman ps -a:
- cleanliness:

## END

END_DONE mission-1613-required-ci-evidence.md: observed PR #1613 CI at head d8838f622 to terminal state, recorded cells, evidence committed to origin/main
