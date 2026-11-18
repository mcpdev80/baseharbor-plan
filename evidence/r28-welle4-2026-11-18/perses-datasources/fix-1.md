# 0428-083 · Connect Perses Prometheus datasource — r2 port (fresh branch)

Mission: /var/tmp/missions/mission-083-datasources.md
Task contract: `python3 scripts/plan.py show t-20261114-r28-perses-datasources`
Card: 0428-083 · release v0.4.28 · type task · areas observability
Owner decision (2026-11-17/18): PR #1608 closed-without-merge; work fresh on `lane-0428-083-datasources-r2` from develop; one PR per card.

## PLAN (nummerliste)

- Read mission, task contract, and #1608 reference (round-1/round-2/luna-r1 akte + old 083 commit objects); confirm scope is the dedicated Prometheus datasource adapter + golden test, fail-closed, no new Prometheus instance.
- Verify remote truth via ls-remote (develop @ 907f16713 = mission base; old w083 branch superseded); confirm planning repo root and origin/main before first evidence commit.
- Claim task via plan.py claim + commit/push claim to planning origin/main.
- Cut worktree `lane-0428-083-datasources-r2` from develop tip 907f16713; confirm 907f16713 is an ancestor of HEAD (git merge-base --is-ancestor).
- Port the CURRENT datasource content (develop-structure-wins): the adapter evolved on the 082 lane (#1665), so copy internal/metrics/perses_prometheus_datasource.go + _test.go + golden from the latest 082 head into my branch, adapting for any develop divergence.
- Verify all referenced symbols exist on develop (readRuntimeSourceSnapshot, providerHTTPClient, queryUp, MetricsPolicy, MetricsDeploymentPolicy, observability.MetricsSource, queryUp).
- gofmt -l + go build ./... + go vet ./... + targeted datasource tests by name; source-readability audit.
- Create one PR #1609 (or reuse per one-PR-per-card) base develop; run exact-head CI to terminal (no .github/** edits); record job + trigger + witness.
- Commit evidence to planning origin/main; confirm present on origin/main; END + GUI-todos; bring down any container.

## SCOPE DECISION

Dedicated Prometheus datasource adapter/tests only (card scope line). No new Prometheus instance, no invented metrics, no .github/** edit, no merge, no force. The selection catalog (internal/capability/perses_selection.go) is NOT wired by the 083 contract: the original #1608 authored only the 3 adapter files and never edited the catalog; the card scope says "Dedicated Prometheus datasource adapter/tests; no new Prometheus instance or invented metrics" and acceptance item 3 is "Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract" — the adapter binds the existing provider endpoint, not the dashboard selection catalog. hunt-912 befund-1 ("catalog war test-only") is a SELECTION-LINE finding about the 080 catalog, not a datasource-contract obligation. The 083 datasources-lieferumfang does not include catalog production wiring; therefore documented only, not implemented. The adapter is the integration point 082/#1665 consumes.

## BASE ATTESTATION

- `git ls-remote origin develop` (before first commit): `907f16713cbf38693d30c9dadaad7fe299759219`
- Branch cut from that head; `git merge-base --is-ancestor 907f16713..HEAD` → YES.
- Candidate carries only my own commits on top of develop.

## Planning repo attestation

- Planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT the workers/ bookkeeping clone).
- Evidence written here, not in a product repo.

## WITNESSES

ls-remote base head (origin, before first commit):
```
$ git ls-remote origin develop
907f16713cbf38693d30c9dadaad7fe299759219	refs/heads/develop
```

Plan claim commit pushed to planning origin/main:
```
$ git log --oneline -1 origin/main
0bfc5934 claim t-20261114-r28-perses-datasources: worker-ornith1.5
```

## TEST + BUILD VITNESSES

```
$ gofmt -l internal/metrics/perses_prometheus_datasource.go internal/metrics/perses_prometheus_datasource_test.go
(empty = clean)

$ go build ./...
(no output)

$ go vet ./internal/metrics/ ./internal/capability/ ./internal/application/
(no output)

$ go test ./internal/metrics/ -run TestPersesPrometheusDatasource -count=1 -v
=== RUN   TestPersesPrometheusDatasourceShape
--- PASS: TestPersesPrometheusDatasourceShape (0.00s)
=== RUN   TestPersesPrometheusDatasourceNamesPrometheusOwner
--- PASS: TestPersesPrometheusDatasourceNamesPrometheusOwner (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoCapabilityClaim
--- PASS: TestPersesPrometheusDatasourceNoCapabilityClaim (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoSecretInDescriptor
--- PASS: TestPersesPrometheusDatasourceNoSecretInDescriptor (0.00s)
=== RUN   TestPersesPrometheusDatasourceAccessIsProxy
--- PASS: TestPersesPrometheusDatasourceAccessIsProxy (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenUnpinned
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenUnselected
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnselected (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenSourceAbsent
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenSourceAbsent (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenNoProvider
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenNoProvider (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenSourceDenied
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenSourceDenied (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenForeignSourceOwned
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenForeignSourceOwned (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedInvalidSnapshot
--- PASS: TestPersesPrometheusDatasourceFailClosedInvalidSnapshot (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedBadURL
--- PASS: TestPersesPrometheusDatasourceFailClosedBadURL (0.00s)
=== RUN   TestPersesPrometheusDatasourceQueryPath
=== RUN   TestPersesPrometheusDatasourceQueryPath/up
=== RUN   TestPersesPrometheusDatasourceQueryPath/down
--- PASS: TestPersesPrometheusDatasourceQueryPath (0.00s)
=== RUN   TestPersesPrometheusDatasourceQueryErrorPropagates
--- PASS: TestPersesPrometheusDatasourceQueryErrorPropagates (0.00s)
=== RUN   TestPersesPrometheusDatasourceVerifyRealQuerySuccess
--- PASS: TestPersesPrometheusDatasourceVerifyRealQuerySuccess (0.00s)
=== RUN   TestPersesPrometheusDatasourceVerifyFailClosed
--- PASS: TestPersesPrometheusDatasourceVerifyFailClosed (0.00s)
=== RUN   TestPersesPrometheusDatasourceUnverifiedReachability
--- PASS: TestPersesPrometheusDatasourceUnverifiedReachability (0.00s)
=== RUN   TestPersesPrometheusDatasourceGoldenFiles
--- PASS: TestPersesPrometheusDatasourceGoldenFiles (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.014s

$ go test ./internal/metrics/ ./internal/capability/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.182s
ok  	github.com/mcpdev80/baseharbor/internal/capability	0.004s

$ bash scripts/source-readability-audit.sh  (baseharbor repo root)
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

19 datasource test cells PASS (the QueryPath cell has two sub-cells up/down). All run on my candidate `8c71395045` (built from develop `907f16713`, my own ancestor).

## CI COVERAGE (Owner directive 2026-11-07)

The new/changed tests live in package internal/metrics and run in the existing CI unit group: `.github/workflows/ci.yml` `go test ./contracts/... ./internal/... ./spec/...` and `go test ./...` on the pull_request Test job. No .github/** change is required (Owner scope); if the group did not already cover the metrics path, report the exact needed change as a finding with file:line rather than editing it.

## hunt-912 / catalog decision (STATE, documented)

- hunt-912 befund-1 (evidence/r28-welle3-2026-11-16/hunt-selection/befund-1.md) is a SELECTION-LINE finding about internal/capability/perses_selection.go (080 acceptance). It states the catalog is the 080 resolver, fail-closed by ownership.
- The 083 datasources-lieferumfang does not include catalog production wiring; the original #1608 never touched perses_selection.go. The adapter is consumed by 082/#1665. No catalog change implemented; documented only.

## repo-rule compliance

- Write-set: only internal/metrics/perses_prometheus_datasource.go + _test.go + golden testdata. No shared/seam/capability/.github edits.
- No merge, no force-push below base, no ready_for_review toggle of another PR, no subagent (§4.8).
- Planning zone verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
- No containers/compose started on the coordinator/codeman host; any test stack brought down before END.

## CLEANLINESSION (/tmp/opencode/083-datasources-r2-wt)

(no docker/podman compose projects started; witness before END)

## END

(to be filled: END_DONE or END_BLOCKED + candidate SHA)
