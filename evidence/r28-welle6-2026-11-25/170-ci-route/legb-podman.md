# w151-0428-285-legb-podman — #170 Leg-B PODMAN witness retry

**Lane:** w151-0428-285-legb-podman (ornith)
**Task:** t-20261124-ci-operator-acceptance-nontty (#0428-285, closed)
**Mission:** w143-legb-podman-fresh — Leg-B witness RETRY with the PODMAN pair.
**Date:** 2026-11-25

## PLAN

- Verify latest develop tip (f7540e591) before dispatch.
- Dispatch `Release · Pre-Release Validation` on ref=develop, tag v0.4.28, ONLY_GATES=atomic/podman/guided,atomic/podman/lifecycle, demo_ref omitted (= consumes pin from file).
- Verify BOTH podman gate jobs executed natively (no `Reused`, native steps ran, static_execute_count>0) — per precedent 45506742327/45465885966.
- If reuse happens again on podman too, do NOT loop: post END_BLOCKED with planner log lines proving the reuse keying — an owner qualification-policy finding.
- Update evidence dir 170-ci-route (round: legb-podman); propose close-line for #170 if fresh-green.
- No merges, no PR edits, no workflow changes.

## Repo / remote attestation

- Planning repo remote (verified before first write): `https://github.com/mcpdev80/baseharbor-plan.git`
  - `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) / (push)`.

## Reality witnesses

- Exact develop tip: `f7540e591609e0db6453e9b690fbb5d6686448a2` (ls-remote `refs/heads/develop`). Commit `ci(0428-249): require the fourteen atomic docker/podman gates for v0.4.28 (#1837)`.
- Pin `docs/releases/v0.4.28.demo-ref` on f7540e: `b41127723e523134a1c14ee3c36cf133237162ce`.
- Catalog on develop: `atomic/podman/guided` and `atomic/podman/lifecycle` both `required_for` v0.4.22–v0.4.28 (present for v0.4.28, not dropped).
- Serialized window: no active `pre-release.yml` run (pending/in_progress/queued) before dispatch.

## Dispatch

- `gh workflow run pre-release.yml --repo mcpdev80/baseharbor --ref develop -f tag=v0.4.28 -f only_gates=atomic/podman/guided,atomic/podman/lifecycle`
  - demo_ref omitted per mission so the workflow consumes the release pin from `docs/releases/v0.4.28.demo-ref`.

## Per-gate execution proof (target)

- Both `atomic/podman/guided` and `atomic/podman/lifecycle` must report native execution: step 4 "Report previously qualified run" must NOT be the terminal path, native steps (Checkout BaseHarbor candidate, Prepare verified rootless runtime, Run runtime gate) must be run, and static_execute_count semantics must show >0.
- A `Reused podman · …` conclusion with native steps skipped = evidence reuse = NOT a fresh witness = END_BLOCKED with planner log lines.

## END

- (pending — to be filled with run ID + per-gate execution proof)
