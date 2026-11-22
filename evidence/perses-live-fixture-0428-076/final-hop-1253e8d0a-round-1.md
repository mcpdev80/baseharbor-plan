# 0428-076 / #1597 final hop to develop 1253e8d0a — akte

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 (perses company-dev fixture) — #1597 final merge-ready hop
candidate SHA: 2184bc400995e6d06feb5845d6cdd1a457a73b76
PR branch: perses-dashboard-databases-lane
PR #1597: https://github.com/mcpdev80/baseharbor/pull/1597 (OPEN, not draft)
base develop SHA (final): 1253e8d0a78f3adad10d677992af7b8b6fb331cf (PR #1785 merged)
previous candidate: 98620890c90869438e7e84b1c311c696e1159ad6 (base 484c95fca)
CI run: #45059821333 (https://github.com/mcpdev80/baseharbor/actions/runs/45059821333)

## PLAN

1. Read mission m_0847_1597final.md.g; verify real remote, PR head, develop.
2. Additively hop candidate onto current develop 1253e8d0a (merge --no-ff; 2nd parent = develop, no force).
3. Verify diff vs develop = pure perses content; scripts match develop.
4. Run the two named perses dashboard tests + internal/metrics packages.
5. Push hop; run hosted rerun; verify TP + Go + observability green.
6. Publish akte to baseharbor-plan origin/main, then post END.

## Base attestation

- Real remote: `origin` = `https://github.com/mcpdev80/baseharbor.git`, `lane-origin` = same (both github.com/mcpdev80, per REMOTE GUARD).
- PR #1597 head before this hop (ls-remote): 98620890c90869438e7e84b1c311c696e1159ad6
- develop head (ls-remote, final): 1253e8d0a78f3adad10d677992af7b8b6fb331cf
- PR branch name: perses-dashboard-databases-lane
- #1785 (1253e8d0a): single commit, changed ONLY scripts/pr-gate-coverage.json (catalog rows). Independent of #1770/#1783 observability/footprint.

## What the hop proves

- develop moved from 484c95fca to 1253e8d0a (PR #1785 merged) while #1597 content stayed static.
- Final head 2184bc400 parents: parent1 = 98620890c (prior candidate), parent2 = 1253e8d0a (fresh develop). develop is an ancestor. Additive, no force/rebase/amend.
- #1597 is independent of #1785/#1770/#1783: pure perses/observability, no footprint data-caps cells, so one additive hop makes it merge-ready.

## Diff vs develop (prove #1597 content only)

`git diff --name-only 1253e8d0a HEAD` lists ONLY:

- cmd/baha/app_perses_cli_test.go (perses tests)
- cmd/baha/app_status_result.go (perses observability product)
- internal/metrics/perses_dashboards.go + _helpers + _test + _promql_test + _0428-076_native_test.go
- internal/metrics/testdata/perses-dashboards/*.json + perses-native/v0.55.1/*.json

scripts/* match develop EXACTLY (`git diff --name-only 1253e8d0a HEAD -- scripts/` => empty). #1785 catalog rows inherited.

## company-dev target im test fixture bereitgestellt

company-dev war FEHLSPUR: die zwei perses dashboard tests derive their verdict from the RESOLVED MANIFEST signal (app_status_result.go: `PersesStatusNow(ObservabilityManagementUI && Perses)`; `PersesDashboardAvailability(resolved.Manifest)`) — nicht aus einer company-dev target config. Tests PASSen.

## Test run (sanctioned skip pattern, local, head 2184bc400)

- `go test ./cmd/baha/ -count=1 -run 'TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases|TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` => ok (both dashboard tests pass)
- `go test ./internal/metrics/ -count=1` => ok (packages test green)
- `go build ./...` ok, `go vet ./cmd/baha/ ./internal/metrics/` ok

## Hosted PR CI (#45059821333) — PR Selected Checks: success

- PR · Trusted Plan: success (catalog fully inherited, incl. #1785 rows)
- PR · Go unit: cli-0, cli-1, cli-2, cli-3, owner, packages: success (includes the two perses dashboard tests)
- PR · Selected Runtime (atomic/docker/observability / docker · observability): success
- PR · Selected Runtime (atomic/podman/observability / podman · observability): success
- go-vet, go-build, cli-gofmt: success
- Skipped (advisory / not applicable): PR · Exact full Pre-Release, Main release checks, Consumer Pins, Candidate-added checks, Public Contracts, HA docker/podman — expected, not a defect.
- No shared-gate cells red: perses observability runtime cells passed directly; no data-caps footprint/parity wait needed.

## END lane

END_DONE — final hop 2184bc400 additive on develop 1253e8d0a, parent1 = prior candidate 98620890c. Pushed to perses PR branch (remote head 2184bc400, ls-remote witness). PR #1597 head = 2184bc400, OPEN, not draft. CI #45059821333 green: Trusted Plan + Go unit (all shards) + observability docker+podman cells. current-base 1253e8d0a: ja. #1597 merge-ready (independent of #1770/#1783). Akte published to baseharbor-plan origin/main. NO merge of mine (owner/Codex merge after review).

## cleanliness

- Worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 (existing dedicated worktree; no scratch created in ecosystem root).
- No docker/podman compose projects started (git hop + unit-test-only CI verification; no containers).
- git ps -a witness: none started (no daemon contact).
- No content edit, no product/.github/catalog change (git-only hop per mission).
