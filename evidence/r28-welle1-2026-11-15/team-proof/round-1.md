# t-20261018-r27-team-proof (0427-059) — round-1 evidence

## Plan (numbered, no markdown checkboxes)

1. Read mission + plan task, claim the task, push claim to origin/main.
2. Reality check: ls-remote develop, identify the real baseharbor checkout (NOT the quarantined workers/baseharbor), claim baha-docker test host via vm-lock.sh, verify Docker reachable.
3. Study the app attach/identity/revision contract on develop to scope the two-client fixture.
4. Build a bounded two-client Docker integration on baha-docker: two state-roots, one Core in a docker network, app IDs converge, revision-equal after A's change, same-deployment race, stale-negative.
5. Run the integration end-to-end and capture command-output witnesses (test scripts only under evidence/.../scripts/).
6. CI-uptake check: regression Go-test vs pure validity-evidence; wire into existing selected-check group or report an exact .github finding (Owner scope, do not edit).
7. Cleanup: bring down compose/container projects, ps-witness empty, cleanliness line.
8. Write this evidence, publish to origin/main, post the END line.

## Context

Acceptance card 0427-059 (release v0.4.28). Two isolated homes/checkouts attach ONE app on a Docker VM: A changes, B sees identical app IDs and the current revision; race on the same deployment/shared provider converges; stale/foreign identities rejected. Demo tests/team-authority fixture is the bounded write reservation for this slice (product changes only if a real deficit is visible).

## Base attestation

- baseharbor-plan origin/main before first evidence commit: 457ed060a3073486878541b13349cddb60f26044 (claim committed here).
- baseharbor develop (real target): 0e9ccb582f5bdcdc74049bbe3996263cdce6500c.
- Branch cut from: develop at 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (ancestor of first commit; will be shown).
- baha-docker test host (192.168.6.166 = baha-runner-docker) claimed for mission-059-teamproof; Docker server 29.8.1 reachable.

## Repo-rule compliance

- Planning evidence written ONLY under baseharbor-plan/evidence/... ; no evidence dir or writes in the product repo.
- No .github/** edited, no workflow_dispatch/rerun (Owner scope).
- No subagents (§4.8); every step run in session 55b459ac.
- Product baseharbor edited only if a real deficit is visible; otherwise demo test-authority fixture only.
- No container/compose started on the coordinator/codeman host; all runtime tests on baha-docker only.
