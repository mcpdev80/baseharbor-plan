# Coordination handoff - CI cutover + ecosystem layout (2026-10-31)

Durable record; local working evidence copies may be removed after this lands.

## v0.4.27 CI cutover state (against develop, current)
- develop advanced by two verified CI cutover fixes, each green under the new gate
  (PR Selected Checks + Trusted Plan = pass), Owner-delegated maintainer integration:
  - #1233 -> 9f08d3cd : receipt-post-run skips CLEAN for non-PR producer events
    (fixed live main failure, post-run writer Run 41160456127 "trusted-pr-plan missing").
  - #1235 -> cb6b7387 : producer-eligibility probe, fail-closed artifact ABSENCE vs ERROR,
    authenticated run->PR base.sha binding + drift watchdog (supersedes #1227/#1230).
- #1225 (core-750 resolver registration) = OPEN, BLOCKED. Its changes to ci.yml /
  scripts/pr-check-runner.py / pr-gate-plan.py are classified coverage-unresolved, and
  scripts/pr-gate-plan.py resolves that class ONLY via a hardcoded register entry OR a
  genuinely-EXECUTED native runtime gate for the exact candidate. Register-entry route
  rejected by Owner. Chosen route: one-time authenticated NATIVE RUN on the self-hosted
  rootless runners (baha-runner-docker-2 / baha-runner-podman-2, online) proving the
  changed ci.yml executes. Pending decision/evidence; no gate weakened, no skip counted
  as pass. #1234 (a rebase of #1225) was opened then closed as structurally unsatisfiable
  without that native qualification.

## Ecosystem layout migration (owner-approved 2026-10-31)
Container ~/dev/baseharbor-ecosystem is being converted from a baseharbor product checkout
(duplicating baseharbor/) into a plain folder holding the 5 repos + two self-protecting
local-git dirs: coordinator/ (durable tooling/state) and workers/ (ephemeral lane worktrees
on DISK). Binding operating model: spawn -> work -> handoff -> verification ->
coordinator-acceptance -> planning-publish -> cleanup. Durable truth = GitHub + this repo's
main; no second local durable copy. Coordinator tooling is immune to worker git-clean by
design. See coordinator/LAYOUT.md + MIGRATION.md.
