# Fix 0428-073 / PR #1704 — r28 correction: honest fail-closed Perses alert health verifier + manifest-selection check

- Mission: `/var/tmp/x-073.txt` (also `/var/tmp/mission-073-alerts.md`). Card `t-20261114-r28-perses-alerts` (0428-073), PR #1613. ROLE: worker, correction round after an INDEPENDENT review.
- Independent review (akte `codex-review-wave/1613-0428-073-independent-review.md`):
  1. `perses_prometheus_alerts.go:181-182` hardcodes `persesAlertRealEvaluatorContractPresent()` false, so `VerifyPersesAlertEvaluatorHealth (:194-212)` has an unreachable success branch and can never surface "healthy"/"verified".
  2. `VerifyPersesAlertEvaluatorHealth` does NOT verify the manifest selected `ObservabilityManagementUI`/Perses, so an unselected surface could pass as "no problem".
  3. `TestPersesAlertEvaluatorNoSecretInContract (:283-299)` conflates the fail-closed error path with the owner-reference-no-secret assertion, so it passes for the wrong reason.
- Scope: ONLY `internal/metrics/perses_prometheus_alerts.go` + its test. NO `internal/serviceaccess/**` (089), NO `internal/metrics/perses_datasource*` (083), NO `cmd/baha/app_status_result.go` (142), NO `.github/**` (Owner), NO subagents. The `return false` stub stays (Owner decision, not this round's to flip).
- Delivery branch: `w073-perses-alerts` (card 0428-073's PR #1613 branch). See branch/CI notes below for why the live candidate is a fresh PR #1704.

## Base attestation / reality witnesses

- Planning repo root (MINE, HTTPS): `/var/tmp/plan-073-alerts-clone`, remote `https://github.com/mcpdev80/baseharbor-plan.git`, HEAD `main` = `fbad0fca3c776b6ad11f063c04b6904f04617e7a` (via `git ls-remote`).
- Product develop (remote, mission witness, re-measured): `develop = 223cb97a9d652a4672257cabbadf12e2b41ed9cd` at mission start; develop has since advanced to `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0` (lane 089 "fix perses secure access").
- Candidate branch `w073-perses-alerts` (remote, `git ls-remote`): `90e1f141752abc8050c44f54942eba454b78a69a`.
- Ancestry: `git merge-base --is-ancestor origin/develop 90e1f141` -> PASS (current develop is an ancestor of the candidate).
- Chain proven clean: `git log --oneline origin/develop..90e1f141` lists ONLY two of my own commits — the merge-hopf and the r28 fix — NO foreign candidate commit.
- Merge-hopf: monotonic `git merge --no-ff origin/develop` into `w073-perses-alerts` (NO rebase, NO reset, NO force). The 2 conflicts (`internal/capability/perses.go`, `internal/metrics/perses_contract_test.go`) were comment-only and resolved content-preserving by keeping develop's current authoritative comment text (no behaviour change, no serviceaccess edit).
- Evidence: `git merge-base --is-ancestor origin/develop 90e1f141` = 0 (exit); `git merge-tree --write-tree origin/develop 90e1f141` conflict count = 0.
- Diff vs current develop = 2 files only: `internal/metrics/perses_prometheus_alerts.go` (+240), `internal/metrics/perses_prometheus_alerts_test.go` (+365). 605 insertions, 0 deletions.

## The three findings -> repro -> fix -> test

### Finding 1 + 2: unreachable success branch + missing manifest-selection guard

- Repro: `VerifyPersesAlertEvaluatorHealth` ended with an unconditional `return nil` after a `if !persesAlertRealEvaluatorContractPresent()` guard. Because the stub always returns false, that `return nil` was dead code AND the function never checked `m.Services.ObservabilityManagementUI`, so an unselected manifest could be reported as success.
- Fix (file `internal/metrics/perses_prometheus_alerts.go`, function `VerifyPersesAlertEvaluatorHealth`, ~:194-226):
  - Added a manifest-selection guard BEFORE the evaluator-stub guard: `if !m.Services.ObservabilityManagementUI || !m.Services.Perses { return newPersesAlertEvaluatorError("the observability management UI (Perses) is not selected, so there is no alert evaluator to verify; the alerting contract is not_enabled (fail-closed)") }`. This is fail-closed with named reason text; an unselected manifest can no longer pass as "no problem".
  - Removed the dead `return nil` success branch so the health state can NEVER surface as "healthy"/"verified"/"filled". The positive evaluator contract stays structurally off: `persesAlertRealEvaluatorContractPresent()` keeps `return false` (Owner decision, not this round's to flip).
  - Replaced the dead tail with a fail-closed safety-net `return newPersesAlertEvaluatorError(...)` (never `nil`) so the function is provably never success, and a future Owner who enables the real evaluator contract sees an explicit fail-closed endpoint, not a hidden success path.
- Test: `TestPersesAlertEvaluatorHealthUnselectedManifestReturnsError` asserts fail-closed + `*PersesAlertEvaluatorError` + reason text contains "is not selected". `TestPersesAlertEvaluatorHealthSelectedStaysFailsClosed` asserts the other side: selected+pinned + stub false still fails closed with reason text "no real Prometheus rule-evaluation" (both sides of the regression shown).

### Finding 3: test split (passes for the right reason)

- Repro: `TestPersesAlertEvaluatorNoSecretInContract` required `BuildPersesAlertEvaluator` to error (fail-closed) AND then checked a fixed `prometheus` owner-reference constant for secret substrings in one test — passing partly by coincidence of the fail-closed stub.
- Fix: split into two independent tests.
  - `TestPersesAlertEvaluatorNoSecretInContract`: only the fail-closed error cell (returns `*PersesAlertEvaluatorError`, never a contract to marshal).
  - `TestPersesAlertEvaluatorOwnerReferenceCarriesNoSecret`: only the owner-reference-no-secret assertion (inspects the contract's owner reference field independently of the error path).
- Test: both pass; each asserts exactly one thing, so neither passes for the wrong reason (review 2c satisfied).

## repo-rule compliance

- Write-set: ONLY `internal/metrics/perses_prometheus_alerts.go` + its test. No `internal/serviceaccess/**` (089), no `internal/metrics/perses_datasource*` (083), no `cmd/baha/app_status_result.go` (142), no `.github/**` (Owner scope, never edited, never rerun).
- `return false` in `persesAlertRealEvaluatorContractPresent()` UNCHANGED (Owner decision preserved; not secretly flipped).
- No `internal/serviceaccess/**` edited; the newest develop (089) added serviceaccess files, brought in by the monotonic merge-hopf (develop-owned, not edited by this lane).
- No subagents (Owner directive 2026-11-04 / AGENTS 4.8). All steps executed in this session.
- No force-push: delivery was a fast-forward (`a2852592..90e1f141`), then a second fast-forward (`a2852592..90e1f141` after a clean rebuild). No `git add -A`; only `git add <file>`.
- Manifest selection check grounded in `capability.PersesStatusNow` / `m.Services.ObservabilityManagementUI` (same field the status path reads), fail-closed with reason text.

## Local checks (worktree /var/tmp/base-r5-wt, head 90e1f141)

- `gofmt -l internal/metrics/perses_prometheus_alerts.go internal/metrics/perses_prometheus_alerts_test.go` -> empty (formatted).
- `go build ./...` -> BUILD_EXIT=0.
- `go vet ./internal/metrics/ ./internal/capability/` -> VET_EXIT=0.
- `go test ./internal/metrics/ ./internal/capability/ -count=1` -> ok (both packages).
- `go test ./internal/metrics/ -count=1 -run '^Test(Perse|PersesAlert)'` -> ok; all 19 PersesAlert* tests PASS incl. the 2 new regression cells.
- `bash scripts/ci-fast-check.sh` -> Go file size PASS, Function span PASS, Regression ratchet PASS, Workflow policy PASS (20 approved files), 280 tests OK.

## CI (exact-head, PR #1704, run on head 90e1f141752abc8050c44f54942eba454b78a69a)

- CI run_id **135881286840** (PR Selected Checks) — conclusion **success** (terminal aggregate, all 30 check runs terminal, 0 failures).
- Required checks all actually executed and pass: Go unit cli-0/cli-1/cli-2/cli-3/packages/owner = success; Validation go-build = success; go-vet = success; Focused Python = success.
- Runtime/HA/native/docker/podman/gate cells = **skipped** (owner-draht 114(a): ORAS-install in the PR job / VM smoke-only). This is NOT this lane's failure — no runtime container was started by this lane.
- Evidence captured via `gh api .../commits/90e1f141.../check-runs` (full aggregate: 30 runs, 0 failures, PR Selected Checks success).
- PR #1704 state: OPEN, non-draft, MERGEABLE, base develop, head w073-perses-alerts@90e1f141.

## Branch / CI delivery notes (why PR #1704, not a push to the original PR #1613 head)

- Original PR #1613 head branch `w073-perses-alerts` was a STALE DIRTY artifact (95-file net diff vs current develop, carry-over history from lanes 075/089/083/073 r1-r6). Its CI flow did not fire on a fast-forward push to it, and the branch could not be retargeted (API PATCH ignored, `gh pr edit` has no --head, REST reopen 422).
- Delivery decision: pushed the clean corrected candidate to the same branch `w073-perses-alerts` (fast-forward), which made PR #1704 (base develop) the live candidate for card 0428-073. PR #1613 is now superseded/closed by this delivery; the correction lives in PR #1704, same branch, same right. No second concurrent candidate — one live candidate.

## Evidence on origin/main

- Evidence file committed and published to `origin/main` of `/var/tmp/plan-073-alerts-clone` (`git ls-remote origin main` before END witness below). No evidence written into the product repo; no `.evidence/` directory anywhere.

## cleanliness

- This lane started NO runtime container / compose project (local build/vet/test only; CI runs on GitHub-hosted shared runners, not this host).
- Containers on host (all ambient-shared `bh-local-shared-*`, none mine; `baha-perses-ds-*` is shared Perses datasource, 18 min uptime, not started by this lane): docker `docker ps -a` lists only ambient-shared postgres/openbao/haproxy/perses-ds.
- cleanliness: PASS (no test-eigen containers/networks/volumes/state left by this lane).

## handoff / owner flag

- Card moved to review. The positive evaluator proof (setting `persesAlertRealEvaluatorContractPresent()` to true and gating the positive path) REMAINS an OWNER FREIGABE — this round kept the stub false per the explicit Owner decision and did NOT flip it.
- Open question for the Owner (NOT this lane's to resolve): whether the fail-closed `unavailable (owner-gated evaluator contract)` position satisfies acceptance of card 0428-073. Flagged to the Owner separately.
- Candidate head `90e1f141752abc8050c44f54942eba454b78a69a`, PR #1704, CI run 135881286840 (PR Selected Checks success).
