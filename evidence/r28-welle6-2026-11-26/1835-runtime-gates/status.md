# PR #1835 runtime gate batch status

Status: **held for the corrected exact head from w157**. No Docker or Podman pair is qualifying yet. The owner directed that the pairs not be run further on `55d17d437cfced7ec648aa42c14cc529963b68b6` because PR #1835 is receiving a correction to the shared/foreign preservation assertion.

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
