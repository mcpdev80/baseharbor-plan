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

## Update (later 2026-10-31): layout migration COMPLETE + #1225 native-run route active
- Container ~/dev/baseharbor-ecosystem de-git-ized to the agreed layout: five repos +
  coordinator/ + workers/ (own local git) + .tmp; governance docs AGENTS.md/RUNBOOK.md now in
  coordinator/ (durable) with root symlinks. Coordination tooling relocated to
  coordinator/scripts; cron relocated+disarmed (no git clean/reset; tmp-sweep/hygiene scoped to
  workers/worktrees + .tmp). 527 leaked full-clone scratch dirs (3 GB) purged. Loops verified
  against codeman 1.47: only idle/exit signals fire for opencode lanes (blocked/stop 400 -> the
  old watcher missed idle-awaiting lanes); replaced by watch.py (idle/exit+inbox -> events.log +
  tmux wake) and coord-tick.sh (idle keep-alive). Worker lifecycle = spawn->work->handoff->
  verification->acceptance->planning-publish->cleanup (worker-cleanup.sh).
- #1225 native-run qualification route (Owner decision) is being executed by worker lane o1240
  on develop cb6b7387; will report candidate SHA + authenticated self-hosted rootless run id.

## #1225 native-run route - status after o1240 round 1
Owner-chosen route (resolve executor coverage via an authenticated NATIVE RUN) is currently
UNIMPLEMENTED in the gate: pr-gate-plan.py resolves `.github/workflows/*` + `scripts/pr-*.py`
coverage only via pre-registered hardcoded SHA sets (no native-execution code path), and the
Targeted HA docker+podman jobs SKIPPED for candidate 1954a46 (PR #1236), proving nothing. This is
a genuine coverage gap, not a product regression. Correct action per CODEMAN-START 6.1(b) /
RUNBOOK 6.1: a bounded classifier extension (own small PR) that resolves those areas ONLY on
genuine executed rootless native jobs (docker AND podman green, fail-closed on skip/absent), with
cli_native_required set so they RUN not skip, plus tests. Candidate #1236 branch is the base.
Lane o1240 executing this now; no gate weakening, no register hack.

## o1240b (correction round) result: classifier fix WORKS; blocked on runner rootless infra
Lane implemented the native-EXECUTION qualifier in pr-gate-plan.py; on #1236 (head advanced to
776841be) the Targeted HA docker AND podman jobs now EXECUTE instead of skipping (PR run attempts
41194053/57/58). They FAIL because the self-hosted rootless runners cannot present a verified
rootless daemon session in the PR-HA context (docker/podman user-service, linger, socket ownership -
RUNBOOK 6.2). This is runner INFRASTRUCTURE state, not code and not a gate weakening.
Blocker owner: runner host rootless session. Next trigger: restore rootless (verify `docker info`/
`podman info` as github-runner on baha-runner-docker-2/podman-2), then re-run #1236; HA jobs should go
green and flip coverage to resolved. Lane released (result recorded). Wake+tick moved to cron (the
sleep-loop froze across a VM suspend and missed a finished worker for hours - fixed).
