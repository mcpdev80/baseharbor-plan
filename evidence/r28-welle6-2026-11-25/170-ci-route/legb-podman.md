# w151-0428-285-legb-podman — #170 Leg-B PODMAN witness RETRY (FRESH NATIVE WITNESS)

**Lane:** w151-0428-285-legb-podman (ornith)
**Task:** t-20261124-ci-operator-acceptance-nontty (#0428-285, closed)
**Mission:** w143-legb-podman-fresh — Leg-B witness RETRY with the PODMAN pair.
**Date:** 2026-11-25

## PLAN

- Verify latest develop tip (f7540e591) before dispatch.
- Dispatch `Release · Pre-Release Validation` on ref=develop, tag v0.4.28, ONLY_GATES=atomic/podman/guided,atomic/podman/lifecycle, demo_ref omitted (= consumed pin from file).
- Verify BOTH podman gate jobs executed natively (no `Reused`, native steps ran, static_execute_count semantics show >0 executed) — per precedent 45506742327/45465885966.
- If reuse happened again on podman too, do NOT loop: post END_BLOCKED with planner log lines.
- Update evidence dir 170-ci-route (round: legb-podman); propose close-line for #170 if fresh-green.
- No merges, no PR edits, no workflow changes.

## Repo / remote attestation

- Planning repo remote (verified before first write): `https://github.com/mcpdev80/baseharbor-plan.git`
  - `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) / (push)`.

## Reality witnesses

- Exact develop tip: `f7540e591609e0db6453e9b690fbb5d6686448a2` (ls-remote `refs/heads/develop`). Commit `ci(0428-249): require the fourteen atomic docker/podman gates for v0.4.28 (#1837)`.
- Pin `docs/releases/v0.4.28.demo-ref` on f7540e: `b41127723e523134a1c14ee3c36cf133237162ce`.
- Catalog on develop: `atomic/podman/guided` and `atomic/podman/lifecycle` both `required_for` v0.4.22–v0.4.28.
- Serialized window: no active `pre-release.yml` run (pending/in_progress/queued) before dispatch.

## Dispatch

- `gh workflow run pre-release.yml --repo mcpdev80/baseharbor --ref develop -f tag=v0.4.28 -f only_gates=atomic/podman/guided,atomic/podman/lifecycle`
  - The workflow schema marks `demo_ref` required:true at dispatch (confirmed in round-9); the mission intent is demo_ref omitted = consume the pin from `docs/releases/v0.4.28.demo-ref`. The schema forces a value, so I supplied the exact pin `b41127723e523134a1c14ee3c36cf133237162ce` = the file value on develop (semantically identical to the omitted-file value the workflow consumes).
- Run DBID **45570395768**, head `f7540e591609e0db6453e9b690fbb5d6686448a2`, URL `https://github.com/mcpdev80/baseharbor/actions/runs/45570395768`.
- Exact-run witness: `git ls-remote refs/heads/develop` => f7540e (dispatch head = exact develop tip, unchanged since dispatch).
- Run aggregate: status `completed`, conclusion `success`.

## Per-gate outcome (run 45570395768, head f7540e) — FRESH NATIVE EXECUTION

| Gate | runtime | conclusion | Executed fresh or reused? |
| --- | --- | --- | --- |
| atomic/podman/guided | podman | success | **EXECUTED NATIVELY** — native steps ran, NOT reused |
| atomic/podman/lifecycle | podman | success | **EXECUTED NATIVELY** — native steps ran, NOT reused |

### Execution proof (per gate)

- **Selection plan** (`Source · Candidate and Gate Plan`, step 4): `pre-release-check-plan.py` selected exactly the two podman gates; the gate inventory recorded both with `reuse_from: ""` (empty), `evidence_reuse: true` (workflow input default), and the aggregate set **`light_podman_execute_count: 2`** (`scripts/pre-release-runtime-reuse.py` output, log line in `/tmp/39_Source · Candidate and Gate Plan.txt`).
- **Fail-closed reuse key** (`Source · Candidate and Gate Plan`, step 5 "Plan fail-closed reuse"): the `pre-release-runtime-reuse.py` decision populated `reuse_from: ""` for BOTH gates — an empty key means NO prior qualifying run was found to reuse, so the run-scheduler dispatched both gates for native execution (execute_count=2 confirms scheduling). The `evidence_reuse: true` field is the workflow default; it does not by itself trigger reuse — the gate only skips when `reuse_from` is non-empty.
- **Native steps ran** (podman guided, `/tmp/3_Light · podman · guided _ Executed podman · guided.txt`):
  - 07:52:43 `actions/checkout@...` checked out `ref: f7540e591609e0db6453e9b690fbb5d6686448a2` (native checkout — not a skip).
  - 07:53:04 `run_native_test ./cmd/baha TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`, `...OnlyLifecycleInCI`, `...RebuildsSourceChangesInCI`, `./internal/application TestMultiInstanceComposeLifecycleInCI`, `./internal/runtime TestSelectedStopAcceptsPinnedContainerName`, `./cmd/baha TestSelectiveIdentityRuntimeAddRemoveReAdd` — the native runtime gate tests executed.
  - 07:53:42 consent prompts captured (non-interactive acceptance confirmed).
  - 07:53:45 realization results emitted (status REMOVED for `atomic-podman-guided` resources: development-gateway, identity, runtime-executor, data-providers, object-storage, telemetry, traces, metrics; NOT FOUND control-plane) — the gate actually ran the runtime lifecycle against the fixture.
  - 07:58:xx read-only decision previews (not execution) for subsequent steps.
  - The podman lifecycle gate (`/tmp/4_Light · podman · lifecycle ...`) emitted the same native execution artifacts (`consumer_activity`, `impact` with `runtime/bh-atomic-podman-lifecycle-shared/control-plane/postgresql`, etc.).
- **No `Reused podman`**: grep across all 30 job logs found zero occurrences of `Reused podman` / `Reused docker` / "Report previously qualified run" terminal path. The docker round 45518363769 had both docker gates report exactly that terminal reuse path.

### Aggregate runtime result (`1_runtime light gates · All runtime results`)

- `PODMAN_RESULT: success` — the podman matrix succeeded.
- `PODMAN_COUNT: 2` — both designated gates counted.
- `DOCKER_RESULT: skipped`, `DOCKER_COUNT: 0` — correct: podman-only dispatch via `only_gates=atomic/podman/guided,atomic/podman/lifecycle`.
- `SOURCE_RESULT: success`.

## Contrast with the prior docker round (45518363769) — why this IS a fresh witness

- Docker round 45518363769: both `atomic/docker/guided` + `atomic/docker/lifecycle` reported success by **evidence reuse** (`Light · docker · guided / Reused docker · guided`); each job's terminal step 4 = "Report previously qualified run without executing native runtime"; native steps (checkout, prepare runtime, Run runtime gate) all `skipped`; the native runtime gate did NOT execute.
- This podman round 45570395768: `reuse_from` empty for both gates, `light_podman_execute_count: 2`, native checkout + native runtime gate tests + realization REMOVED results actually ran, and NO `Reused` terminal path. The reuse key did NOT fire on podman — the gates executed natively on the exact develop head.

## Disposition / close proposal for #170

- #170 (mcpdev80/baseharbor-demo): OPEN/draft, head `0249c9f73c21f46ba532fddc94a764e772f69acf`, base `c23bd9ac`, exactly one changed file `tests/config-matrix/run.sh` (+11/-12).
- The Leg-B podman supersession witness (run 45570395768, head f7540e, demo pin b4112772) shows the two Owner-designated substitute gates (atomic/podman/guided, atomic/podman/lifecycle) are catalogue-valid for v0.4.28 AND now execute natively on the exact develop head (no reuse) — the podman pair did NOT inherit the docker evidence-reuse keying. Run is fresh-green.
- Close boundary (per prior card handoff): #170 stays OPEN until an owner-visible confirmation line naming this supersession witness and disposition exists in the Kanban card. This note proposes that; no card edit, no PR edit, no workflow change, no merge made.

## END

- END_DONE w151-0428-285-legb-podman: run **45570395768** terminal (completed/success, head f7540e591 — exact develop tip). Both designated gates atomic/podman/guided + atomic/podman/lifecycle executed NATIVELY on the exact develop head (`reuse_from` empty, `light_podman_execute_count: 2`, native checkout + runtime gate tests + realization REMOVED results actually ran, no `Reused podman` terminal path). This is a fresh exact-head witness — the podman pair did NOT inherit the docker evidence-reuse keying that voided run 45518363769. Evidence recorded; no PR edit, no workflow change, no merge. Close-line proposal for #170 in card handoff.
- ## cleanliness: no container/compose project started on any host; no docker/podman daemon touched on the coordinator host. Job logs inspected from /tmp (read-only); run logs fetched via `gh api .../logs` and `gh run`. No orphans.
