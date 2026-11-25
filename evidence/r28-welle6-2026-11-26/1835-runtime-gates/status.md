# PR #1835 runtime gate batch status

Status: **held for the corrected exact head from w157**. No Docker or Podman pair is qualifying yet. The owner directed that the pairs not be run further on `55d17d437cfced7ec648aa42c14cc529963b68b6` because PR #1835 is receiving a correction to the shared/foreign preservation assertion.

## Corrected-head qualification (w157 correction round + hop)

Candidate head advanced through w157's correction round (degenerate `plan.Providers.Impact` assertion removed; `scripts/pr-gate-coverage.json` wired the test into `native/docker/data-capabilities` + `native/podman/data-capabilities` via component `source.cmd_baha_installation_reset_preservation_test_go`, `runtime_specific: true`) and then a develop hop onto `2a141387d` (#1832 merged). Current PR #1835 head: `72fc60a923b7c9b91b803f469c8c5cf3572e0448`. Card 0428-287 product delta intact: `cmd/baha/application_destroy_authorization.go` (+30), `cmd/baha/installation_reset_preservation_test.go` (+201), `cmd/baha/w287_destroy_after_failed_apply_test.go` (+169) vs `origin/develop`.

### Red-first baseline proof (contract)
- Red baseline: base `55d17d437cfced7ec648aa42c14cc529963b68b6` (fix-absent) -> `ok github.com/mcpdev80/baseharbor/cmd/baha 0.008s [no tests to run]` (assertion absent on this base; test file introduced one commit later).
- Green candidate: `TestInstallationResetPreservesSharedForeignProvider (1.38s)` PASS on `72fc60a92` via `go test -run ... ./cmd/baha/`.

### Docker data-capabilities
- [45605189539](https://github.com/mcpdev80/baseharbor/actions/runs/45605189539) `success` on `40f72d101244783d141a87833fc19775020106cc` — full PR event, `atomic/docker/data-capabilities` (check 139123306347) green. Docker witness MET.

### Podman (required remaining witness) — diagnosed-blocked at operator auth
- [45611090994](https://github.com/mcpdev80/baseharbor/actions/runs/45611090994) `failure` on `72fc60a92`; [45611866489](https://github.com/mcpdev80/baseharbor/actions/runs/45611866489) `failure` on `72fc60a92`. Both fail at the podman-quadlet `baha doctor` probe with the operator-unauthenticated error:
  `2026-11-25T12:11:12.7977143Z   Managed-environment machine operations require an authenticated BaseHarbor operator.`
  `2026-11-25T12:11:12.8003049Z ##[error]Process completed with exit code 2.`
  Resolution hint in the log: `authenticate the BaseHarbor operator` / `Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.`
- Verdict: **diagnosed auth/setup gap** — the podman runner did not have a provisioned BaseHarbor operator (unauthenticated). This is NOT a pass and NOT yet proven to be a runner-provisioning gap: the resolution requires an authenticated operator, which this runner lacked. My card delta (destroy plan builder + preservation regression test) does not touch doctor/operator auth, so the failure is not a card-0428-287 semantic defect. The same probe passed on SUCCESS run `45608237959` on `2a141387d`. Other podman native gates skip on the head because they depend on the podman-quadlet job.
- No workaround applied: auth checks stay intact. Any test-only login/`baha login`/OIDC fixture decision is held for owner authorization (authorized lane/Codex), not hacked around.

## Requested source inputs

- Release tag: `v0.4.28`
- Candidate source SHA: `55d17d437cfced7ec648aa42c14cc529963b68b6`
- Demo pin: `b41127723e523134a1c14ee3c36cf133237162ce`; read from `origin/develop:docs/releases/v0.4.28.demo-ref` before dispatch and matched the supplied SHA.
- Docker selection: `atomic/docker/guided,atomic/docker/lifecycle`
- Podman selection: `atomic/podman/guided,atomic/podman/lifecycle`
- GitHub requires the dispatch event `ref` to be a branch or tag. The event was dispatched on `lane-0428-287-install-reset-recovery`, which resolved to the requested candidate SHA; the workflow input `ref` was the exact SHA above. The required `demo_ref` input was passed as the verified pin.

## Runs and gate proof

| Run | Head / selection | Terminal result | Per-gate execution | Disposition |
| --- | --- | --- | --- | --- |
| [45571397690](https://github.com/mcpdev80/baseharbor/actions/runs/45571397690) | `55d17d437cfced7ec648aa42c14cc529963b68b6`; Docker pair | `cancelled`; zero jobs | Neither gate ran | **Void; nonqualifying.** |
| [45572854473](https://github.com/mcpdev80/baseharbor/actions/runs/45572854473) | `55d17d437cfced7ec648aa42c14cc529963b68b6`; Docker pair | `cancelled` | The two selected Light matrix jobs were skipped; neither executed `Run runtime gate`. Two Go test shards (`cli-2`, `cli-3`) were cancelled. | **VOID — neither failure nor green; nonqualifying.** |
| [45570395768](https://github.com/mcpdev80/baseharbor/actions/runs/45570395768) | `f7540e591609e0db6453e9b690fbb5d6686448a2`; develop Leg-B Podman pair | `success` | `atomic/podman/guided`: `Run runtime gate` success; reuse steps skipped. `atomic/podman/lifecycle`: `Run runtime gate` success; reuse steps skipped. | Terminal watch satisfied, but wrong candidate SHA; **not evidence for PR #1835**. |
| [45571699415](https://github.com/mcpdev80/baseharbor/actions/runs/45571699415) | `a7b0a48048c11d20234160eede941532ddc33156`; queued validation push | `failure` in `Plan fail-closed reuse for runtime matrix gates` | No runtime jobs ran | Unrelated queue occupant; no gate evidence. |

## Cancellation diagnosis for void run 45571397690

The run record at `GET /repos/mcpdev80/baseharbor/actions/runs/45571397690` reports `conclusion=cancelled`, `actor=mcpdev80`, `triggering_actor=mcpdev80`, and no jobs from the run-attempt jobs endpoint. It does not expose a cancellation actor or reason. I issued no cancellation command for this run.

The workflow file at the exact candidate SHA contains a workflow concurrency group named `baseharbor-release-qualification` and `cancel-in-progress: false`. Run 45571699415 entered `pending` at 07:53:40 UTC; run 45571397690 was updated to `cancelled` at 07:53:42 UTC. This timing strongly suggests the earlier pending run was displaced by the newer pending run in the group’s single pending slot. This is an evidence-based diagnosis, not an explicit GitHub cancellation reason.

Run 45572854473 was a later redispatch after the queue cleared. On owner direction to hold for w157’s corrected head, I explicitly requested cancellation. Its run metadata exposes no cancel-actor field. Two Go test shards (`cli-2`, `cli-3`) were cut; the selected Light runtime matrix jobs were skipped, and no native Docker or Podman gate executed. This run is VOID and counts as neither failure nor green.

Run 45573394850 belongs to the #1833 lane per the owner and was not used as evidence for this batch.

## Next action

Wait for w157’s correction to produce the new exact PR head. Then dispatch Docker first and Podman second using that SHA as the workflow `ref` input, the verified `v0.4.28.demo-ref` pin, and the exact two gate IDs in each `ONLY_GATES` selection. Require top-level terminal results and per-gate `Run runtime gate` execution proof; reused-only results do not qualify.
