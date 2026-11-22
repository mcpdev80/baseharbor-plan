# 0428-076 / #1597 stale-base hop — akte

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 (perses company-dev fixture) — #1597 stale-base refresh
candidate SHA: ff3a1ad789a192cac5d6afed757348df68983266
PR branch: perses-dashboard-databases-lane
PR #1597: https://github.com/mcpdev80/baseharbor/pull/1597 (OPEN, not draft)
base develop SHA: b27b2ebedb7da10690fb83c24a9f763ee16d7468
CI run: #7325 (https://github.com/mcpdev80/baseharbor/actions/runs/45054008345)

## PLAN

1. Read mission m_0847_1597hop.md.g; verify real remote, PR #1597 head, develop b27b2ebe; confirm PR branch.
2. Additively hop perses PR branch 211a6d57a onto origin/develop b27b2ebe (git merge --no-ff --allow-unrelated-histories; second parent = develop HEAD, no force/rebase/amend).
3. Resolve merge conflicts correctly (ours for perses test, develop for scripts/* catalog).
4. Confirm diff vs develop is PURE #1597 perses content only.
5. Run the two named perses dashboard tests with the sanctioned skip pattern.
6. Push hop to perses PR branch; run hosted PR CI; verify Trusted Plan green.
7. Publish akte to baseharbor-plan origin/main, then post END.

## Base attestation

- Real remote verified: `origin` = `https://github.com/mcpdev80/baseharbor.git`, `lane-origin` = `https://github.com/mcpdev80/baseharbor.git` (both github.com/mcpdev80, per REMOTE GUARD).
- PR #1597 head before hop (ls-remote): 211a6d57a8974026a4bf61b6eed5477d3b707fbe
- develop head (ls-remote): b27b2ebedb7da10690fb83c24a9f763ee16d7468
- PR branch name: perses-dashboard-databases-lane
- #1779 commit: 3939aa5ea (catalog the #1597 perses dashboards cluster on observability surfaces). Confirmed ancestor of origin/develop, NOT ancestor of 211a6d57a (stale base).

## What the hop proves

- PR #1597 head 211a6d57a was STALE: it predated #1779 (perses cluster catalog), so the trusted-planner guardian aborted 'PR Trusted Plan' fail-loud on uncataloged perses product-sources.
- The earlier hop f4f6e8fea landed detached on lane-0428-076-hop1597 and did NOT reach the PR branch (head kept pointing at 211a6d57a). This hop fixes that on the correct PR branch.
- Hop ff3a1ad78 parents: parent1 = 211a6d57a (our base), parent2 = b27b2ebe (develop HEAD). develop is an ancestor of ff3a1ad78. Additive, no force/rebase/amend.

## Diff vs develop (prove #1597 content only, no catalog edit by us)

`git diff --name-only origin/develop HEAD` lists ONLY:

- cmd/baha/app_perses_cli_test.go (perses tests, ours)
- cmd/baha/app_status_result.go (perses observability product)
- internal/metrics/perses_dashboards.go + _helpers + _test + _promql_test + _0428-076_native_test.go
- internal/metrics/testdata/perses-dashboards/*.json + perses-native/v0.55.1/*.json

scripts/* files match develop EXACTLY (I took develop's side; #1779 catalog entries are inherited, not authored by this lane). `git diff --name-only origin/develop -- scripts/` => empty.

## Test run (sanctioned skip pattern)

`go test ./cmd/baha/ -count=1 -run 'TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases|TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`

- TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases — PASS
- TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed — PASS

## company-dev target im test fixture bereitgestellt

company-dev war FEHLSPUR: die zwei perses dashboard tests derive their verdict from the RESOLVED MANIFEST signal (app_status_result.go: persesStatus = PersesStatusNow(ObservabilityManagementUI && Perses); databaseDashboards = PersesDashboardAvailability(resolved.Manifest)), nicht aus einer company-dev target config. Tests PASSen auf dem branch und auf dem deployten PR head. Kein produktseitiges target-registration zu konfigurieren (wuerde product/observability owner-decision sein); hier nicht noetig.

## Hosted PR CI (#7325) — PR Selected Checks: success

- PR · Trusted Plan: success (catalog geerbt, kein fail-loud mehr)
- PR · Go unit: cli-0, cli-1, cli-2, cli-3, owner, packages: success (includes the two perses dashboard tests)
- PR · Selected Runtime (atomic/docker/observability / docker · observability): success
- PR · Selected Runtime (atomic/podman/observability / podman · observability): success
- go-vet, go-build, cli-gofmt, Runner Interface, Demo Pin, Source format, Focused Python: success
- Skipped (advisory / not applicable to this PR): PR · Exact full Pre-Release, Main release checks, Consumer Pins, Candidate-added checks, Public Contracts, HA docker/podman — expected, not a defect.
- No shared-gate cells red: the perses observability runtime cells passed directly; no data-caps footprint/parity wait needed.

## END lane

END_DONE — hop ff3a1ad78 additively onto develop b27b2ebe, pushed to perses PR branch (remote head ff3a1ad78, ls-remote witness). PR #1597 head = new develop-based SHA (not 211a6d57a). CI #7325 green: Trusted Plan + Go unit + observability runtime cells. Two perses dashboard tests PASS. Akte published to baseharbor-plan origin/main.

## cleanliness

- Worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 (existing dedicated worktree, no scratch created in ecosystem root).
- No docker/podman compose projects started (unit-test-only CI verification; no containers).
- git ps -a witness: none started (no daemon contact).
