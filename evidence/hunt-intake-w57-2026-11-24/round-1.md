# w57-0428-266-huntintake — H-V25 findings F1-F9 intake (planning-only)

Lane: w57-0428-266-huntintake. Mission: turn the H-V25 bug-hunt findings F1-F9
(dossier `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`,
origin/main SHA adc07163d) into baseharbor-plan bug cards. No product-code changes.
Develop anchor verified: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
→ `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd` (matches the mission anchor).

## PLAN

1. Verify planning repo remote + fetch origin/main — DONE (witness below).
2. Read dossier round-1.md — DONE.
3. Inspect existing cards 0428-143/152/186/189-194 + next free numbers — DONE (143/152/186 all closed/accepted; 189-194 planned registry/consent cards, none matches a finding; next free numbers start at 0428-263; 263 was NOT free — it is this mission's lane number only; 263-262 highest used).
4. Verify each F1-F9 against cited code at develop 3ebfb90d — DONE (fresh read-only clone, per-finding notes below).
5. Dedup decisions (new card vs cross-ref into existing card) — DONE.
6. Write cards 0428-263..268 — DONE.
7. `python3 scripts/plan.py render && python3 scripts/plan.py check` — DONE (0 errors, 10 pre-existing warnings).
8. Commit + pull --rebase + push to main — see witness below.
9. Evidence persisted on origin/main before END — see witness below.

## Finding verification on develop 3ebfb90d (fresh clone, file:line re-measured)

- F1 REAL. `internal/metrics/perses_backend_status.go:49-60` documents the "real HTTP round trips" path then calls `BuildPersesInfraDashboardWithProbe` (line 81); `cmd/baha/app_status_result.go:306-307` names `VerifyPersesInfraDashboard` as the only probe that can promote to verified; `PersesInfraDashboardAvailability` uses it (`internal/metrics/perses_infra_dashboards.go:208`). Note: both paths DO run live HTTP through `httpClientSeriesProbe`/`querySeries` (`perses_infra_dashboards.go:119-121,630-633`); the defect is two coexisting named "real probe" definitions for one contract. → new card 0428-263.
- F2 REAL. All-missing divergence confirmed: `perses_backend_status.go:85-87` maps all-missing → `configured_unverified`; `perses_infra_dashboards.go:145-147` errors → all-unavailable entries. Both faces computed in one render (`app_status_result.go:314,:317`). → new card 0428-264 (depends on 263).
- F3 REAL. `reportPersesSurfaceStatus` gates with `authorizeApplicationOperation` (`cmd/baha/perses_lifecycle.go:351-358`); `collectApplicationStatusResult` (`cmd/baha/app_status_result.go:294-317`) runs `PersesBackendAnswersStatusNow` (line 314, HTTP at `perses_backend_status.go:52-60`) with no authorize/operatorauth gate on the path (grep: no `authorize*` in the status render path; `collectApplicationStatus` at `cmd/baha/app_observe.go:32` issues none). Contract text at `internal/capability/perses.go:213` requires the probe context. → new card 0428-266 (depends on 186 + 265 so it wraps the final wiring).
- F4+F5 REAL (one defect, two faces). Zero-value `metricsprovider.PersesBackendSignalWitness{}` at `cmd/baha/perses_lifecycle.go:366`, `cmd/baha/app_status_result.go:328` and `:436`; also internally at `internal/metrics/perses_dashboards_hosts.go:338,:612`. No production site sets any `Proven` field (fields at `perses_dashboards_hosts.go:546-555`). The "card 0428-143" deferral comment at `app_status_result.go:112-116` is stale: 0428-143 closed accepted as #1729 with different scope (Verification=none semantics — verified in its card). 0428-143 is CLOSED/accepted → cannot add new scope there; 0428-142 (witness shape, accepted #1702) is the true predecessor. → new card 0428-265 (one card for F4+F5, depends 142).
- F6 REAL (as edge-case, matches dossier severity). `deploymentApplied` = `ExistingRuntimeFiles(...) == nil` only (`cmd/baha/perses_lifecycle.go:343-346`); applied branch derives verdict manifest-only via `BuildPersesAlertEvaluator`. → intake into the alert-face card (with F7).
- F7 REAL. `VerifyPersesAlertEvaluatorHealth` (`internal/metrics/perses_prometheus_alerts.go:90`) has no caller outside its own file; `BuildPersesAlertEvaluator` always returns `configured_unverified` (`perses_prometheus_alerts.go:83`); consumer `persesAlertEvaluatorObservation` (`cmd/baha/perses_lifecycle.go:250-270`) calls only the builder. 0428-152 closed accepted (#1816) and its consumer landed — the missing piece is the health-probe wiring, i.e. 152's contract incomplete in practice. → new card 0428-268 combining F7 (probe wiring) + F6 (applied-face identity cross-check), depends 152.
- F8 REAL, but the dossier miscounts. `grep -rn 'PersesBackendAnswers' | grep -v StatusNow` on develop 3ebfb90d outside tests hits EXACTLY three comments: `internal/capability/perses.go:213`, `internal/capability/perses.go:252`, `internal/application/perses_lifecycle.go:162`. The dossier's 4th site, `internal/metrics/perses_backend_status.go:18`, names no symbol (it says "the production path runs real HTTP round trips") — dossier over-read. No new card: comment-only fix folded into 0428-267 acceptance item 2 (same file family as the F9 sweep).
- F9 REAL. Three shapes confirmed: `not_configured` (underscore, `internal/application/perses_lifecycle.go:166-171` via `capability.PersesStatusNow` `internal/capability/perses.go:265-283`); `not configured` (space, `cmd/baha/perses_lifecycle.go:234-235`); `not-configured` (hyphen) / `configured` / `unreachable` (`cmd/baha/app_status_result.go:76-80`). Spec `docs/spec/management-access-v1.md:43-58` pins the underscore pair normatively. → new card 0428-267 (with F8).

## Intake result (F → card)

- F1 → NEW 0428-263 `t-20261124-r28-perses-backend-status-real-probe` (depends 0428-186)
- F2 → NEW 0428-264 `t-20261124-r28-perses-two-status-faces-disagree` (depends 263)
- F3 → NEW 0428-266 `t-20261124-r28-app-status-unauthorized-live-probe` (depends 186, 265)
- F4 → NEW 0428-265 `t-20261124-r28-perses-witness-producer-cli` (depends 142) — shared with F5
- F5 → NEW 0428-265 (same card as F4; one producer closes both faces)
- F6 → NEW 0428-268 `t-20261124-r28-alert-evaluator-live-health-wiring` (depends 152) — shared with F7
- F7 → NEW 0428-268 (same card as F6; the 3-state alert face needs both the probe wiring and the runtime cross-check)
- F8 → intake into 0428-267 acceptance item 2 (comment-only sweep, no own card) — cross-referenced in 0428-263 "Related"
- F9 → NEW 0428-267 `t-20261124-r28-perses-state-spelling-drift` (depends 265, 263)

Dedup notes: 0428-143 (#1729), 0428-152 (#1816), 0428-186 (#1810) are all closed/accepted; per mission rule 2 they cannot absorb new scope, and their unlanded promises (witness producer, health-probe wiring, verified-source) get successor cards instead. 0428-189..194 (registry/consent surface) match none of F1-F9 (registry.go/consent were explicitly excluded from this hunt, dossier lines 140/146). No existing planned card covers F1-F9 (grep for probe/witness/spelling topics across all planned cards: only 0428-142/152/186/143, all closed).

## Remote witnesses

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Render/check before push: `python3 scripts/plan.py render && python3 scripts/plan.py check` →
`707 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings` (10 warnings pre-existing, unrelated t-20261*-r27 cards).

## repo-rule compliance

- baseharbor-plan AGENTS.md: claim-free planning publish (this lane publishes cards only), never mark accepted/qualified — all 6 new cards are `kanban_status: planned`, `owner: ""`, `resolution: ""`. render + check before push (0 errors). No checkboxes outside tasks/ (plan.py check_stray_checkboxes passes).
- No product-code changes: the baseharbor repo was read via a detached fresh clone in /tmp/opencode only (`--no-checkout`, then checkout of 3ebfb90d); no builds, no tests, no pushes, no PR.
- No subagents (AGENTS 4.8): every step executed in this session.
- Ops hazard (documented, not acted on): the coordinator cron `plan-sync.sh` (every 2 min, part of the 0428-246 lane's work set — NOT this lane's scope to fix) stashes and hard-resets any dirty baseharbor-plan checkout during a turn. This lane hit it twice (work recovered from the auto-stash `f569ff2ec`); final publication therefore runs render+check+commit+push atomically. Suggest the coordinator serialize plan-sync with publishing lanes or widen its grace.

## cleanliness

This lane started no containers/networks/volumes/compose projects (read-only + planning files). `docker ps -a` was not needed: nothing was created. Mirror at `/tmp/opencode/w57-0428-266-huntintake-wt` (blobless, detached HEAD 3ebfb90d) removed at END.
cleanliness: besenrein — nothing started or stopped by this lane on this host.

## Publication witness

Push: `35fd37ee6..177f7af4e  main -> main` to https://github.com/mcpdev80/baseharbor-plan.git
(`git ls-remote origin refs/heads/main` → `177f7af4ebd6f8913b990ef62038d699b35d5c64`).

`git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep -E 'hunt-intake-w57|20261124-r28'`:
```
evidence/hunt-intake-w57-2026-11-24/round-1.md
tasks/t-20261124-r28-alert-evaluator-live-health-wiring.md
tasks/t-20261124-r28-app-status-unauthorized-live-probe.md
tasks/t-20261124-r28-perses-backend-status-real-probe.md
tasks/t-20261124-r28-perses-state-spelling-drift.md
tasks/t-20261124-r28-perses-two-status-faces-disagree.md
tasks/t-20261124-r28-perses-witness-producer-cli.md
```

END_DONE w57-0428-266-huntintake: 6 new bug cards 0428-263..268 for F1-F9 (F5→265, F6→268, F8→267 cross-ref); render/check 0 errors; published to baseharbor-plan main.
