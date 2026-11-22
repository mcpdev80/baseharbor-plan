# 0428-076 / #1597 stale-base hop — akte (final)

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 (perses company-dev fixture) — #1597 stale-base refresh
candidate SHA: 98620890c90869438e7e84b1c311c696e1159ad6
PR branch: perses-dashboard-databases-lane
PR #1597: https://github.com/mcpdev80/baseharbor/pull/1597 (OPEN, not draft)
base develop SHA (final, fresh): 484c95fca938cb96736c4578906e6ea58bf043b8
#1779 commit: 3939aa5ea (perses cluster catalog) — ancestor of final head
CI run: #45057415763 (https://github.com/mcpdev80/baseharbor/actions/runs/45057415763)

## PLAN

1. Read mission m_0847_1597hop.md.g; verify real remote, PR #1597 head, develop; PR branch.
2. Additively hop perses PR branch onto develop (merge --no-ff --allow-unrelated-histories; 2nd parent = develop, no force/rebase/amend).
3. Resolve merge conflicts correctly (ours for perses test, develop for scripts/* catalog).
4. Diagnose + fix CI packages FAILURE (trailing-newline golden regression).
5. Integrate healthy remote head + re-hop on fresh develop for catalog coherence; single coherent candidate.
6. Push hop; run hosted PR CI; verify Trusted Plan + packages + observability cells green.
7. Publish akte to baseharbor-plan origin/main, then post END.

## Base attestation

- Real remote: `origin` = `https://github.com/mcpdev80/baseharbor.git`, `lane-origin` = same (both github.com/mcpdev80, per REMOTE GUARD).
- PR #1597 head before hop (ls-remote): 211a6d57a8974026a4bf61b6eed5477d3b707fbe
- develop head (ls-remote, final): 484c95fca938cb96736c4578906e6ea58bf043b8 (moved from b27b2ebe during the shift)
- PR branch name: perses-dashboard-databases-lane
- #1779 commit 3939aa5ea: confirmed ancestor of final head, NOT ancestor of 211a6d57a (stale base).

## What the hop proves

- PR #1597 head 211a6d57a was STALE (pre-#1779), so 'PR Trusted Plan' aborted fail-loud on uncataloged perses sources.
- The earlier hop f4f6e8fea landed detached on lane-0428-076-hop1597 and did NOT reach the PR branch. That detached branch was deleted (before/after ls-remote witness) per EXACTLY ONE CANDIDATE PER CHAIN.
- Final head 98620890c parents: parent1 = 993a57f2 (healthy remote head carrying the Loki/Tempo + golden fix), parent2 = 484c95fca (fresh develop). develop is an ancestor; #1779 is inherited. Additive, no force/rebase/amend.

## Diff vs develop (prove #1597 content only, no catalog edit by us)

`git diff --name-only origin/develop HEAD` lists ONLY:

- cmd/baha/app_perses_cli_test.go (perses tests, ours)
- cmd/baha/app_status_result.go (perses observability product)
- internal/metrics/perses_dashboards.go + _helpers + _test + _promql_test + _0428-076_native_test.go
- internal/metrics/testdata/perses-dashboards/*.json + perses-native/v0.55.1/*.json

scripts/* match develop EXACTLY (`git diff --name-only origin/develop -- scripts/` => empty). #1779 catalog is inherited, not authored by this lane.

## Multi-writer collision diagnosis (Owner directive 2026-11-04, self-run §4.8)

The PR branch for card 0428-076 was hit by a SECOND Codex session running concurrent fixes. Three follow-up commits landed on perses-dashboard-databases-lane:

- f5ccb343 "use emitted Loki and Tempo attributes": changed Loki/Tempo panel queries to `{baseharbor_source_class=...}` / `{resource.service.namespace=...}` but did NOT regenerate the 4 golden JSON files.
- 1d1bdf821 "match canonical TraceQL JSON encoding": touched tempo-traces JSON.
- 993a57f2 "preserve golden byte format": stripped the trailing newlines the prior commits had added, restoring byte-for-byte golden equality.

Two regressions the collision introduced, which this lane fixed/verified:
1. Dropped mcp.go gate.mcp catalog entry from scripts/pr-gate-coverage.json (reintroduces fail-loud). Restored from develop.
2. Added trailing newlines to 4 perses golden JSON files. persesPanelJSON emits no trailing newline, so byte-for-byte golden equality requires NO trailing newline. Stripped from loki-logs.json, tempo-traces.json, loki-app-errors.json, tempo-app-traces.json.

Hosted CI #7328 (on 993a57f2 before my re-hop) confirmed the f5ccb343/1d1bdf821 state FAILED: `TestPersesNativeShapeCanonicalValidator/loki-logs` + `/tempo-traces` and `TestPersesDashboardGoldenFiles` (packages package). Final head 98620890c is healthy because it carries 993a57f2's fix + catalog restoration + fresh-develop inheritance.

## company-dev target im test fixture bereitgestellt

company-dev war FEHLSPUR: die zwei perses dashboard tests derive their verdict from the RESOLVED MANIFEST signal (app_status_result.go: `PersesStatusNow(ObservabilityManagementUI && Perses)`; `PersesDashboardAvailability(resolved.Manifest)`) — nicht aus einer company-dev target config. Tests PASSen. Kein produktseitiges target-registration zu konfigurieren (wuerde product/observability owner-decision sein); hier nicht noetig.

## Test run (sanctioned skip pattern, local, head 98620890c)

- `go test ./cmd/baha/ -count=1 -run 'TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases|TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` => ok (both dashboard tests pass)
- `go test ./internal/metrics/ -count=1` => ok (packages test green after golden fix)
- `go build ./...` ok, `go vet ./cmd/baha/ ./internal/metrics/` ok
- ci-fast-check.sh: all policy gates PASS (Go file size, function span, regression ratchet, workflow policy 20 approved files)

## Hosted PR CI (#45057415763) — PR Selected Checks: success

- PR · Trusted Plan: success (catalog fully inherited, no fail-loud)
- PR · Go unit: cli-0, cli-1, cli-2, cli-3, owner, packages: success (includes the two perses dashboard tests)
- PR · Selected Runtime (atomic/docker/observability / docker · observability): success
- PR · Selected Runtime (atomic/podman/observability / podman · observability): success
- go-vet, go-build, cli-gofmt, Runner Interface, Demo Pin: success
- Skipped (advisory / not applicable): PR · Exact full Pre-Release, Main release checks, Consumer Pins, Candidate-added checks, Public Contracts, HA docker/podman — expected, not a defect.
- No shared-gate cells red: perses observability runtime cells passed directly; no data-caps footprint/parity wait needed.

## END lane

END_DONE — hop 98620890c additive on fresh develop 484c95fca, parent1 = healthy remote head 993a57f2. Pushed to perses PR branch (remote head 98620890c, ls-remote witness). PR #1597 head = 98620890c (not 211a6d57a). CI #45057415763 green: Trusted Plan + Go unit (all shards) + observability docker+podman cells. Two perses dashboard tests + packages package pass. Akte published to baseharbor-plan origin/main.

## cleanliness

- Worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 (existing dedicated worktree; no scratch created in ecosystem root).
- No docker/podman compose projects started (unit-test-only CI verification; no containers).
- git ps -a witness: none started (no daemon contact).
- Stray ./workworkers dir from a path typo was removed (cleanup witness in transcript).
