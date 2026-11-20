# 0428-203 · Stale emitted target on Verification=none same-id switch — evidence (round 1)

- Card: t-20261120-verif-none-stale-target (0428-203)
- Lane: w205-0428-203-staletgt (session ornith)
- Release: v0.4.28
- Date: 2026-11-20
- Base lane: 0428-143 `lane-0428-143-verify-none` head 809a8196e1cf8b29d410c6a9bd07114d99c2dc10 (draft=false, base develop, ancestry on develop YES)
- develop head measured: 40cb28c758b02960356434b630086a341ebe1738

## PLAN

1. Reality check: confirm planning remote (baseharbor-plan = https://github.com/mcpdev80/baseharbor-plan.git) and product remote (lane-origin = https://github.com/mcpdev80/baseharbor.git, NOT a local fs path); measure base + develop heads via ls-remote.
2. Create detached worktree /var/tmp/w203b-wt from exact base lane head 809a8196e1cf, own branch lane-0428-203-stale-target, PR base = refs/heads/lane-0428-143-verify-none.
3. Reproduce the stale-target finding with witnesses BEFORE any edit: same-ID application source emits target under a verifying mode, switches to Verification=none, exported surface re-read.
4. Decide covered vs open; record verbatim exported surface.
5. Add exactly one contract sentence at integration_contract.go stating the retirement rule; no second site documents it.
6. Add CI-discovered regression test asserting through the real exported surface; verifier wait semantics unchanged.
7. gofmt + go vet clean; one squashed commit; focused go test both packages.
8. Draft PR base refs/heads/lane-0428-143-verify-none, draft=false with STACK line.
9. Hosted run at exact head observed to terminal state; run-id + conclusion per cell.
10. Publish evidence to baseharbor-plan main; verify origin/main presence; compose sweep; END.

## Repo rule compliance

- Read baseharbor/AGENTS.md; implemented inside the card write-set only: internal/metrics/prometheus_verify.go (read-only, wait semantics unchanged), internal/capability/integration_contract.go (one sentence) and their test files. No touched files: internal/serviceaccess/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identityprovider/**, internal/machine/**, internal/operatorauth/**, internal/metrics/perses_dashboards*, internal/metrics/prometheus_files.go (exported-target assembly read-only here), cmd/baha/app_status_result.go, internal/application/provider_registry.go, .github/**.
- No subagents (4.8); every step executed in this own session.

## Reality witnesses

- Planning repo remote: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push).
- Product remote resolved: lane-origin = https://github.com/mcpdev80/baseharbor.git; the shared checkout also carries origin/upstream pointing at the same github URL, used only the github.com/mcpdev80 remote.
- Base lane head (measured via ls-remote): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote lane-origin refs/heads/lane-0428-143-verify-none` -> 809a8196e1cf8b29d410c6a9bd07114d99c2dc10.
- develop head (measured via ls-remote): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote lane-origin refs/heads/develop` -> 40cb28c758b02960356434b630086a341ebe1738.
- Worktree /var/tmp/w203b-wt cut from 809a8196e1cf, detached HEAD then branch lane-0428-203-stale-target; `git merge-base --is-ancestor 809a8196e1cf HEAD` = YES; `git merge-base --is-ancestor 40cb28c758b0 HEAD` = YES (over the base lane).

## Fund held with witnesses (reproduce BEFORE change)

Card write-set witness: internal/capability/integration_contract.go:58 `ObservabilityVerifyNone ObservabilityVerificationMode = "none"`. The single contract site validating verification modes is integration_contract.go:240-248 (provider signal-liveness field only); it says nothing about retiring output emitted before a mode change. PR #1693 independent review (card-filed witness) reproduced a stale emitted target when a same-ID source switches from a verified mode to VerificationNone.

### Reproduction runs (verbatim), no edit before witness

Test harness: same-ID application-class source, file `application--alpha--dev--declared.json` emitted under Verification=backend-query, then same ID switched to Verification=none, exported TargetsDir re-read.

Run A (base lane head 809a8196e1cf, my worktree):
- `go test ./internal/metrics/ -run TestReproStaleTargetOnNoneSwitch -v`
- `repro_0428_203_test.go:60: verifying pass emitted targets: [application--alpha--dev--declared.json]`
- `repro_0428_203_test.go:94: none pass emitted targets: []`
- `repro_0428_203_test.go:99: OK: application target not present after switch to none`
- PASS

Run B (same-ID switch while a second app source stays verifying, `hasApplication` path):
- `go test ./internal/metrics/ -run TestReproStaleTargetNoneWithSecondSource -v`
- `repro_0428_203_test.go:153: OK: A retired with B present`
- PASS

Run C (develop head 40cb28c758b0, throwaway worktree /var/tmp/w203check-wt):
- `go test ./internal/metrics/ -run TestReproStaleTargetOnNoneSwitchDev -v`
- `repro_dev_0428_203_test.go:73: OK on develop: application target retired after switch to none`
- `repro_dev_0428_203_test.go:82: OK on develop: PruneApplicationTargets retires target when list empty`
- PASS

### Verdict: finding COVERED

The same-ID `Verification=none` switch retires the previously emitted target through the room-scoped sweep in internal/metrics/prometheus_files.go:129-144 (`application--*` files removed when `hasApplication`, which stays true while the source remains in the list) and full removal through PruneApplicationTargets. `prometheus_files.go` is byte-identical between 809a8196e1cf and 40cb28c758b0 (verified: `git diff 809a8196e1cf 40cb28c758b0 -- internal/metrics/prometheus_files.go` empty). The stale entry is therefore NOT reproducible on the current stand (predecessor 0428-143 carries the sweep fix; the earlier appKeep mechanism from 0428-123 r5 2efbf043a no longer exists). Per AGENTS 4.2 no fix is built for a problem the witness does not show.

Per the card acceptance field (authoritative scope) the lane still ships the additive defensive contract sentence and regression guard that the acceptance item enumerates, WITHOUT altering verifier wait semantics (acceptance #4) or touching any locked path.

## Acceptance mapping

1. Regression test (defensive, same-id switch to none asserts target absent through the real exported TargetsDir): added as TestVerifyApplicationSourceVerificationNoneRetiresPreviouslyEmitted in internal/metrics. Asserts via os.ReadDir(files.TargetsDir) + os.Stat of the emitted filename — the real exported surface, not an internal helper.
2. Contract sentence at exactly ONE place: internal/capability/integration_contract.go, appended to the ObservabilityVerifyNone const doc; no second file documents the retirement rule (verified integration_contract.go is the only contract site mentioning verification modes).
3. Test runs in GitHub CI: the `packages` shard (scripts/pr-go-unit-shard.py --mode packages runs `go test ./...` over every non-CLI package) auto-discovers every internal/metrics test; named shard = packages.
4. Verifier wait semantics unchanged: internal/metrics/prometheus_verify.go untouched in this change; the application-source loop skip 0428-143 set is preserved.
5. Hosted run at exact head observed to terminal state (4.6); cli-0..3 + PR Selected Checks and the packages internal/logs Loki-trio are the field-wide gates 0428-198/0428-202, named not fixed.

## CI — exact head, own terminal observation (4.6)

- PR: #1730, head c90a73ac8128bca974eb7383c341eb614a2a636a, base refs/heads/lane-0428-143-verify-none, draft=false, branch == refs/pull/1730/head.
- Run: GitHub Actions run #6826 (databaseId), URL https://github.com/mcpdev80/baseharbor/actions/runs/44812049031 (event `pull_request`).
- Head at run: `c90a73ac8128bca974eb7383c341eb614a2a636a` (verified via `gh run list --branch lane-0428-203-stale-target`).
- Run conclusion: **failure** (observed to terminal state, own terminal observation, AGENTS 4.6). Six red cells, all field-wide gates, none in this card's diff.

### Per-cell run-id + conclusion (run 6826 / 44812049031)

- `PR · Go unit · owner` (job 136551273575): SUCCESS.
- `PR · Validation · go-vet` (job 136551273396): SUCCESS; `PR · Validation · go-build` (job 136551272950): SUCCESS.
- `PR · Focused Python` (job 136551272894): SUCCESS; Workflow policy / Trusted Plan / Source format / Native gate plan: SUCCESS.
- `PR · Go unit · cli-0` (job 136551272955), `cli-1` (136551272991), `cli-2` (136551272990), `cli-3` (136551273050): **failure**, field-gate 0428-198 (locked to lane 0428-198, out of this card write-set). Root cause, literal line from cli-0 (job 136551272955):
  `main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.` — the authenticated-operator-on-managed-Target gate, pre-existing (fails identically on unmodified develop).
- `PR · Go unit · packages` (job 136551273116): **failure**, not my change. `internal/metrics` passes: `ok  github.com/mcpdev80/baseharbor/internal/metrics  1.604s` — my regression `TestVerifyApplicationSourceVerificationNoneRetiresPreviouslyEmitted` was auto-discovered by the packages shard and passes. The only three failing tests are `internal/logs`:
  - `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (loki_test.go:522),
  - `TestPersesLokiDatasourceMultiSourcePartialMatchability` (loki_test.go:586),
  - `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (loki_test.go:633)
  all failing with: `load Loki service access identity: stat .../providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory`. These are **0428-202** (Loki multi-source-consumer, root `2af892e4e` in `internal/serviceaccess/policy.go`); zero operator-auth lines in this job, so the cause is external. Confirmed pre-existing.

GATE-FAIL 0428-198 (field-wide, out of write-set): cli-0..3 + PR Selected Checks fail with `Managed-environment machine operations require an authenticated BaseHarbor operator` (root 2af892e4e in internal/serviceaccess/policy.go). Recorded run-id 6826 / run 44812049031, jobs 136551272955/136551272991/136551272990/136551273050.

0428-202 (field-wide, out of write-set): packages cell fails on the internal/logs Loki-trio — `TestPersesLokiDatasourceMultiSource*` (loki_test.go:522/586/633), job 136551273116, run 44812049031 — `client-cert.pem: no such file or directory`. Named, not fixed (locked internal/serviceaccess/**).

My regression test discovered by the `packages` shard (scripts/pr-go-unit-shard.py --mode packages runs `go test ./...` over every non-CLI package), ran and passed: `ok github.com/mcpdev80/baseharbor/internal/metrics 1.604s`.

BEWEISKETTE:
- `git ls-remote lane-origin refs/pull/1730/head` -> c90a73ac8128bca974eb7383c341eb614a2a636a (== head, delivery witness)
- `git ls-remote lane-origin refs/heads/lane-0428-203-stale-target` -> c90a73ac8128bca974eb7383c341eb614a2a636a
- `git merge-base --is-ancestor 809a8196e1cf c90a73ac8` = YES (stack on base lane)
- `git merge-base --is-ancestor 40cb28c758b0 c90a73ac8` = YES (over base lane)
- `git diff origin/lane-0428-143-verify-none...HEAD --name-only`:
  ```
  internal/capability/integration_contract.go
  internal/metrics/prometheus_verify_workload_only_test.go
  ```
- run-id 6826 / run 44812049031, head c90a73ac8, conclusion failure (field gates only).

## EVIDENCE PUBLICATION

- Pre-push origin/main check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep verif-none-stale-target`:

## END

END_DONE w205-0428-203-staletgt: PR #1730 head c90a73ac8128bca974eb7383c341eb614a2a636a base refs/heads/lane-0428-143-verify-none draft=false run 6826/44812049031 conclusion=failure (field gates only: cli-0..3 = 0428-198, packages internal/logs Loki-trio = 0428-202; internal/metrics ok in CI). Card set to wait by coordinator with 0428-198/0428-202 named. evidence=origin/main

## cleanliness:

- No docker/podman compose project started this session (in-process `go test` only).
- `docker ps -a` before/after: <witness>; `docker volume ls`: no 0428-203/lane-0428-203 volumes; no state dirs created under the worktree.
- Throwaway develop worktree /var/tmp/w203check-wt removed after verification.
- ambient-core/ foreign-cart images untouched. Broom-clean.
