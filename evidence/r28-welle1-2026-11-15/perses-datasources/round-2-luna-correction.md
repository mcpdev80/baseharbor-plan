# 0428-083 · Connect Perses Prometheus datasource — round-2 correction (luna-r1 findings)

Mission: /tmp/opencode/mission-fix-datasources.md
Card: t-20261114-r28-perses-datasources · PR #1608 · release v0.4.28 · areas observability
Verdict under correction: act-luna-r1.md = REQUEST CHANGES (candidate c77c76870dc0245d7f7e6be4caf13b562435dd6e).
Naming note: the existing round-2.md akte was the earlier gofmt-only round (01bc7d448); THIS akte is the luna-r1 correction round (mission named it round-2.md; recorded here as round-2-luna-correction.md to preserve the prior akte).

## PLAN (nummerliste)

1. Read mission + luna-r1 akte (act-luna-r1.md); confirmed defect: VerifyPersesPrometheusDatasourceHealth passed on pin validation alone; builder suppressed source/URL errors into empty-config datasource with nil error.
2. Verified remotes: ls-remote planning repo root = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (zone check); product refs: w083-perses-datasources @ c77c76870, base lane-0428-075-perses-seam @ 66ff93d1c, develop @ 14d8f17d1.
3. Worktree /tmp/opencode/mission-fix-datasources-wt cut AT c77c76870 (base attestation below).
4. Rewrote internal/metrics/perses_prometheus_datasource.go fail-closed per recipe (details below); fixed gofmt (the pre-existing file carried a duplicated comment block gofmt -w repaired; F-signature watch honored).
5. Replaced nil-on-pinned-only expectation; added cells: unselected, absent provider, absent sources, denied sources, foreign-owned source, invalid snapshot, bad URL, query error propagation, real query success (httptest incl. exact query, 401-denied, untrusted-CA), down-answer stays unverified; golden now carries the materialized endpoint config.
6. go build ./... + go vet ./... + go test ./internal/metrics/ ./internal/capability/ green; source-readability audit PASS; gofmt -l empty.
7. Commits pushed to branch w083-perses-datasources (PR #1608 stays draft, base seam unchanged). Provenance witnesses below.
8. Evidence akte committed + pushed to planning origin/main (this file); END post.

## FIX SUMMARY (vs recipe)

- File/change (internal/metrics/perses_prometheus_datasource.go):
  - persesPrometheusDatasourceURL's suppression ("if urlErr != nil { url, urlErr = "", nil }") removed; endpoint resolution is fail-closed (missing provider dir, missing/unmaterialized/invalid port propagate as errors).
  - Construction is tied to the selected/authorized manifest sources via the retained runtime snapshot (runtime-sources.json, validated against the provider placement): absent snapshot => "no materialized Prometheus sources"; policy-denied/foreign-owned sources => "no authorized Prometheus sources"; damaged snapshot => propagated authority error. No path returns a datasource with empty config and nil error anymore.
  - VerifyPersesPrometheusDatasourceHealth(ctx, m) now performs a REAL Prometheus query — max(up{baseharbor_provider=,baseharbor_source=} or ...) over the authorized sources — against the materialized management endpoint through the Prometheus service-access TLS client (providerHTTPClient: pinned CA, mTLS or dev basic auth; no secret in the descriptor). Pin validation alone can NEVER pass: unverified/unreachable/all-down state returns an error.
  - Reachability axis: "verified" only from a real probe result (BuildPersesPrometheusDatasourceWithProbe); the probe-less build stays "unverified". This replaces the old doc-claim "no probe exists here" with an actually-used query path (prometheus_verify.go queryUp) — the authorized existing health path, no invention: it is the same /api/v1/query path the provider verify lane uses.
- Tests: internal/metrics/perses_prometheus_datasource_test.go (19 PASS cells); golden testdata/perses-prometheus-datasource/prometheus.json now pins kind/name/default/config{url,access=proxy,authentication} — the emitted shape checked against the pinned Perses v0.55.1 native PrometheusDatasource fields the adapter uses.
- CI selection: package internal/metrics runs in the existing unit group (see CI section); no .github change.

## BASE ATTESTATION

- ls-remote (before first push): `c77c76870dc0245d7f7e6be4caf13b562435dd6e  refs/heads/w083-perses-datasources`
- Branch cut exactly at that head (git worktree add --detach c77c76870, then local branch); `git merge-base --is-ancestor c77c76870 HEAD` => YES.
- c77c76870 is the existing PR #1608 head (merge of seam 66ff93d1 + card commits); base lane-0428-075-perses-seam left unchanged, per mission.
- git log c77c76870..HEAD = ONLY my own commits (06ec8e24e fix + 11bdc332d comment-line cleanup; the intermediate push e6efd9cd4 was amended into 06ec8e24e before the final push — see push notes).

## WITNESSES

Push + head (origin, after push):
```
$ git ls-remote origin refs/heads/w083-perses-datasources
11bdc332d676b0f7bc696a5cbf04351b9927b35c	refs/heads/w083-perses-datasources
$ git log --oneline c77c76870dc0245d7f7e6be4caf13b562435dd6e..origin/w083-perses-datasources
11bdc332d docs(0428-083): drop duplicated comment line
06ec8e24e fix(0428-083): fail closed on missing/denied/invalid Prometheus sources; verify health by real query (luna-r1)
```
- No foreign commit in that range (both are this lane's own commits).
- No extra remote branch: `git ls-remote origin | grep mission-fix-ds-branch` => empty (local helper branch only; single candidate branch w083-perses-datasources per mission).
- Push note: the first push (e6efd9cd4) was replaced by its amended form 06ec8e24e via ONE --force-with-lease pinned to e6efd9cd4 (never below base c77c76870), then fast-forward 06ec8e24e..11bdc332d. Lease witness above.
- PR #1608 (gh): baseRefName lane-0428-075-perses-seam, headRefOid tracks branch, isDraft true, state OPEN (checked at head e6efd9cd4; branch head since advanced only by this lane's own commits).

## TEST + BUILD VITNESSES

```
$ gofmt -l internal/metrics/perses_prometheus_datasource.go internal/metrics/perses_prometheus_datasource_test.go
(empty = clean)
$ go build ./...        (no output)
$ go vet ./...          (no output)
$ go test ./internal/metrics/ -run TestPersesPrometheusDatasource -count=1 -v
--- PASS: TestPersesPrometheusDatasourceShape (0.00s)
--- PASS: TestPersesPrometheusDatasourceNamesPrometheusOwner (0.00s)
--- PASS: TestPersesPrometheusDatasourceNoCapabilityClaim (0.00s)
--- PASS: TestPersesPrometheusDatasourceNoSecretInDescriptor (0.00s)
--- PASS: TestPersesPrometheusDatasourceAccessIsProxy (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnpinned (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnselected (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenSourceAbsent (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenNoProvider (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenSourceDenied (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenForeignSourceOwned (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedInvalidSnapshot (0.00s)
--- PASS: TestPersesPrometheusDatasourceFailClosedBadURL (0.00s)
--- PASS: TestPersesPrometheusDatasourceQueryPath (0.00s) [up + down cells]
--- PASS: TestPersesPrometheusDatasourceQueryErrorPropagates (0.00s)
--- PASS: TestPersesPrometheusDatasourceVerifyRealQuerySuccess (0.00s)
--- PASS: TestPersesPrometheusDatasourceVerifyFailClosed (0.00s)
--- PASS: TestPersesPrometheusDatasourceUnverifiedReachability (0.00s)
--- PASS: TestPersesPrometheusDatasourceGoldenFiles (0.00s)
ok  github.com/mcpdev80/baseharbor/internal/metrics
$ go test ./internal/metrics/ ./internal/capability/ -count=1
ok  github.com/mcpdev80/baseharbor/internal/metrics
ok  github.com/mcpdev80/baseharbor/internal/capability
$ bash scripts/source-readability-audit.sh
... PASS (file size / function span / regression ratchet)
```

## CI COVERAGE (Owner directive 2026-11-07)

- All new/changed tests live in package internal/metrics; they run in the existing CI unit group: `.github/workflows/ci.yml:124` (`go test ./contracts/... ./internal/... ./spec/...`) on the `Test` job (pull_request, paths: '.github/**', '**.go', 'go.mod', 'go.sum', 'spec/**', 'contracts/**'). My changes touch only internal/**.go + internal/**.json testdata => trigger satisfied.
- Formatting signature (`Check formatting`, ci.yml:106 `gofmt -l cmd internal spec contracts`) is clean at head (witness above).
- No new test is VM-only or local-only; no .github/** edit was needed or made.

## SCOPE / STOP NOTES

- The runtime mTLS health path itself (service-access PKI) is exercised by the existing provider integration suite (prometheus_integration_test.go, build-gated); this lane added the httptest-backed query/TLS/auth-denied cells in the unit package instead of a VM run; the mission named no VM smoke test.
- No containers/compose started; nothing to bring down. Host-local: only worktree + caches under /tmp/opencode and ecosystem go-cache/work-gotmp (lane-named dirs).
- STOP criteria not hit: the authorized existing Prometheus query/health path (internal/metrics queryUp + providerHTTPClient) exists and is used; nothing was invented.

## repo-rule compliance

- Write-set: only internal/metrics/perses_prometheus_datasource.{go,_test.go} + its golden testdata. No shared/seam file edits; no .github/**; no merge / ready_for_review / force-push below base; PR #1608 stays draft.
- No subagents (§4.8); all work in this session.
- Planning zone verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## END LINE

END DONE mission-fix-datasources.md: 0428-083 luna-r1 correction — datasource construction fail-closed on missing/denied/invalid sources and bad endpoint (errors propagate, no empty-config nil-error path), health verify runs a real Prometheus up=1 query over the service-access client (pin validation alone never passes), golden pins the materialized config; 19 test cells PASS, gofmt/build/vet/readability clean; branch w083-perses-datasources head 11bdc332d676b0f7bc696a5cbf04351b9927b35c (own commits on c77c76870 only), PR #1608 draft, base seam unchanged.
