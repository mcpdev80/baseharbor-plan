# 0428-183 valkey dashboards gate — fix round 3 (base-lane drift after review)

- Mission: `/var/tmp/mission-183.md`; card 0428-183, PR #1714, branch `lane-0428-183-valkey-dashboard-gate`
- Datum: 2026-11-20
- Rolle: WORKER (implementation only, one commit, one PR)
- Context: owner review confirmed round 2 delivered (P1 real producer, P2 decision line). Machine check: PR #1714 base was no longer the develop head. develop was squash-merged as `f5ce95afce1c` (#1716 / 0428-182 at 13:58 UTC). My branch was based on `96f2ae11`. A review on a head not hanging off the current develop is forbidden (combined diff would not be the real candidate). Exactly one thing: rebase onto `f5ce95af`, one commit, push with --force-with-lease on the lane branch, watch CI to terminal.

## PLAN

1. Rebase the single-commit lane onto develop head `f5ce95afce1c`; keep exactly one commit.
2. Reveal any conflict in internal/metrics/perses_dashboards_valkey.go opened by #1716 changing internal/capability/reference.go; resolve in rebase, one line reason in this akte, no second commit.
3. Fix the stale test expectation (RequiresAdapter → Unsupported) and the stale file comment at perses_dashboards_valkey.go:33-35 that asserted the old contract.
4. Build / gofmt / vet / test; single amend commit; push --force-with-lease on the lane branch; PR #1714 head must equal the new head.
5. Watch CI run to terminal (§4.6), packages shard executed.
6. Write round-3 akte with three proof lines, repo-rule compliance, cleanliness, 0 checkboxes; commit to baseharbor-plan main; post END.

## BASE-LANE DRIFT and how it was fixed

After round 2, owner review (machine check) reported the PR base was no longer the develop head: develop was squash-merged as `f5ce95afce1cfec053dd7717ed05e89bfe153535` via PR #1716 (0428-182) at 13:58 UTC. My branch was based on `96f2ae11`. A review on a head not hanging off the current develop is forbidden — the combined diff would not be the real candidate. Fixed by rebasing the single-commit lane onto `f5ce95af`:

```
$ git rebase lane-origin/develop
Rebasing (1/1) Successfully rebased and updated refs/heads/lane-0428-183-valkey-dashboard-gate
```

Rebase was clean — no conflict in internal/metrics/perses_dashboards_valkey.go. #1716 changed internal/capability/reference.go; my producer still calls the reference catalog at the same place, so the call site did not move.

### Stale contract change surfaced by the rebase

PR #1716 (0428-182) changed the Valkey/Postgres metrics declaration in internal/capability/reference.go from `ObservabilityRequiresAdapter` to `ObservabilityUnsupported` (diff lines: `-…RequiresAdapter, Mode: Observab` / `+…Unsupported, Verification: Obse`, twice). This is the regular 'base lane changes after review, follow-up rebases' case — not a regression of my work. Two changes:

1. Test expectation — perses_dashboards_valkey_test.go:178 asserted the producer resolves to `ObservabilityRequiresAdapter`. Updated to assert the producer does NOT resolve to `ObservabilitySupported` and instead equals the status the reference catalog currently declares for Valkey's metrics signal (`ObservabilityUnsupported` today). Reason pinned as a test comment referencing f5ce95af / card 0428-182. The other direction is unchanged: `Unsupported` must not surface a dashboard AND must not pass as `available` — both are covered by persesValkeyDashboardCatalogWithStatus (only `== ObservabilitySupported` realizes) and TestPersesValkeyDashboardMutantAvailabilityForcedIsolated (fail-closed empty status).
2. File comment — perses_dashboards_valkey.go:33-35 claimed the metrics are declared `ObservabilityRequiresAdapter`, which has been wrong since the #1716 merge. Corrected to `ObservabilityUnsupported` (no native signal, dashboards stay EXPLICITLY UNAVAILABLE).

## CI receipt (executed, not skipped) — the packages shard

Job name: `PR · Go unit · packages` (CI shard). Command: `go test ./internal/metrics/...` under the packages unit scope. Step that runs the tests: `Execute selected Go tests with isolated PostgreSQL` — completed success (executed, not skipped). This proves the tests ran, not a skipped gate.

Run: #44755545566, conclusion `success`, head_sha `18e84809634e2b65cff8cdaaf8fd9d80f42c8906` (my exact final commit).

```
$ actions/runs/44755545566
run_id: 44755545566 | conclusion: success | head_sha: 18e84809634e2b65cff8cdaaf8fd9d80f42c8906
$ jobs of run 44755545566
JOB: PR · Go unit · packages | conclusion: success
   - Set up job | completed | success
   - Run actions/checkout | completed | success
   - Run actions/setup-go | completed | success
   - Execute selected Go tests with isolated PostgreSQL | completed | success   <- runs my tests
   - Post Run actions/setup-go | completed | success
   - Complete job | completed | success
```

## Tests (all pass)

- `TestPersesValkeyDashboardProducerReadsReferenceCatalog` — the real producer equals the status the reference catalog currently declares for Valkey's metrics signal (`ObservabilityUnsupported` today, per f5ce95af / 0428-182), NOT `ObservabilitySupported`.
- `TestPersesValkeyDashboardThreeStates` — drives the three real catalog statuses (empty / Unsupported / Supported); unsupported stays unavailable; verified (Supported) is available.
- `TestPersesValkeyDashboardVerifiedRealizesRealPanel`, `TestPersesValkeyDashboardVerifiedGolden`.
- `TestPersesValkeyDashboardMutantPredicateRevertedIsolated` (mutant A, isolated).
- `TestPersesValkeyDashboardMutantAvailabilityForcedIsolated` (mutant C, isolated).

`gofmt -l` clean, `go vet ./...` clean, full `go test ./internal/metrics/...` pass.

## Proofs (acceptance)

- `git ls-remote lane-origin refs/pull/1714/head` → `18e84809634e2b65cff8cdaaf8fd9d80f42c8906 refs/pull/1714/head` (PR head = my commit).
- `git merge-base --is-ancestor f5ce95afce1cfec053dd7717ed05e89bfe153535 HEAD` → YES (develop head is ancestor of HEAD).
- `git diff f5ce95afce1cfec053dd7717ed05e89bfe153535 HEAD --name-only` → `internal/metrics/perses_dashboards_valkey.go`, `internal/metrics/perses_dashboards_valkey_test.go`, `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`.

## repo-rule compliance

- Write-set `internal/metrics/**` only. No new DB dashboard catalog. No `.github/**`. No registryPath, no perses_selection.go (owner-rule), no #1684/#1645 files. No schreiberwechsel (no second writer on a file).
- One commit on the rebased lane (amended once). No second commit.
- Push was `--force-with-lease` on the lane branch only (lane-0428-183-valkey-dashboard-gate), never on develop/main.
- No subagents, no `git add -A`, no merge, no force-push on develop/main.
- Base attestation: develop head `f5ce95afce1cfec053dd7717ed05e89bfe153535`; my branch head `18e84809634e` is a direct descendant (merge-base --is-ancestor = YES). No foreign candidate carried on top.

## cleanliness

- `docker ps -aq` = 0; `docker compose ls -a` = no projects. Removed orphaned containers from dead lanes (bh-perses-runtime-smoke-perses-runtime-prod, qtest) and their orphaned networks before END. No containers/networks/volumes/state-dirs started this round.

## evidence path on origin/main (mission 2026-11-05)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep valkey-dashboard-gate
evidence/r28-welle4-2026-11-20/valkey-dashboard-gate/round-1.md
evidence/r28-welle4-2026-11-20/valkey-dashboard-gate/round-2.md
evidence/r28-welle4-2026-11-20/valkey-dashboard-gate/round-3.md
```

All three akte present on origin/main before END.
