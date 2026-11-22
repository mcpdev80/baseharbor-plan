# 0428-076 / #1597 perses company-dev fixture — akte

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 (company-dev fixture) — #1597's own correction on develop
branch: lane-0428-076-hop1597
candidate: (to be set after first hop commit)
base develop SHA: b27b2ebedb7da10690fb83c24a9f763ee16d7468

## PLAN

1. Verify real remote (origin = github.com/mcpdev80), PR #1597 head 211a6d57a, develop b27b2ebe; confirm branch carries only our own hop commit.
2. Switch worktree to lane-0428-076-hop1597 and additively hop onto origin/develop b27b2ebe (git merge --no-ff; second parent = develop HEAD, no force/rebase).
3. Read app_perses_cli_test.go:500 and :557 to determine the exact required contract for the company-dev test target (fixture registration vs fail-closed assert).
4. Configure ONLY the test fixture / test-target registration so the two perses dashboard tests pass; STOP with file:line if a real product-target/observability contract is required.
5. Run the two named tests with the sanctioned skip pattern and record output.
6. Push to #1597 (keep open), run hosted PR CI, note shared-gate cells as waiting-shared-gate.
7. Publish akte to baseharbor-plan origin/main, then post END to 9142ab1f.

## Base attestation

- Real remote verified: `origin` = `https://github.com/mcpdev80/baseharbor.git`
- PR #1597 head (ls-remote): 211a6d57a8974026a4bf61b6eed5477d3b707fbe
- develop head (ls-remote): b27b2ebedb7da10690fb83c24a9f763ee16d7468
- `git merge-base --is-ancestor 211a6d57a origin/develop` => NO (not yet merged into develop)
- `git log --oneline origin/develop..lane-0428-076-hop1597` lists only our own hop commit (plus the carried develop history up to b27b2ebe). The single non-develop commit on top is our additive hop; base is b27b2ebe, which is an ancestor of the hop commit by construction.

## company-dev target im test fixture bereitgestellt — BEFUND (gap nicht reproduzierbar)

Ziel der karte: die zwei perses dashboard tests (TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases, TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed) so korrigieren, dass der test-pfad einen 'company-dev' target in der test-config hat.

BEFUND — die zwei tests schlagen NICHT fehl. Sie laufen grün auf dem branch UND auf dem deployten PR #1597 head (211a6d57a8974026a4bf61b6eed5477d3b707fbe):

- go test ./cmd/baha/ -count=1 -run 'TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases|TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" => PASS (beide zellen绿)
- identisch绿 auf /tmp/0428-076-prhead (remote refs/pull/1597/head) abgeprüft

URSACHE, warum kein company-dev target noetig ist:
- Die availability verdicts werden in cmd/baha/app_status_result.go aus resolved.Manifest abgeleitet: persesStatus := capability.PersesStatusNow(resolved.Manifest.Services.ObservabilityManagementUI && resolved.Manifest.Services.Perses); databaseDashboards := metricsprovider.PersesDashboardAvailability(resolved.Manifest). Die zwei dashboard tests asserten den database_dashboards face (postgresql/mongodb => unavailable, prometheus/loki/tempo => available), der aus dem RESOLVED MANIFEST SIGNAL kommt (observability selected + Perses pinned), NICHT aus einem company-dev target.
- Der perses probe path (resolveApplication + runPersesStatusCommand) loadet KEIN orgconfig/company-dev/organization.yaml. git grep -S "company-dev" -- cmd/baha/app_perses_cli_test.go => 0 matches in allen blobs des branches (git log --all). Die helper configureTestTarget registriert einen docker-dev target, wird aber von den zwei dashboard tests nicht aufgerufen.
- Die dashboard tests existieren erst seit commit 074678d14 (card 0428-076 REQUEST CHANGES fix); develop (b27b2ebe) kennt sie gar nicht. Der "gap" war also kein aktueller fail, sondern eine veraltete Annahme in der mission.

Scope: NUR test-datei + test-fixture. Kein product/observability/perses-code, kein .github, kein scripts/pr-gate-coverage.json. Die karte ist damit erledigt — es gab keine produktseitige target-registration zu konfigurieren (und ein company-dev target im perses-probe-pfad ware ein product/observability owner-decision, hier aber nicht noetig).

## END lane

END_DONE — karte erledigt. Branch lane-0428-076-hop1597 head f4f6e8fea (additive hop onto develop b27b2ebe). PR #1597 head unveraendert (211a6d57a, content identisch). Die zwei perses dashboard tests laufen绿, kein company-dev target noetig (verdict aus resolved Manifest, nicht aus target config). Hop push an remote branch zugestellt (ls-remote witness f4f6e8fea). CI fast check: alle kellen绿.
