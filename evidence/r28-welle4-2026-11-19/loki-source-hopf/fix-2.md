# fix-2 — 0428-086 perses-loki-source: per-source Loki query selector (PR #1616)

- Card: t-20261114-r28-perses-loki-source (0428-086)
- PR: mcpdev80/baseharbor#1616
- Lane: lane-0428-086-perses-loki-source
- Date: 2026-11-19
- Role: worker (laptop, filling owner w086-0428-086-lokisource)
- Write-set (disjunkt, nur diese 4 Pfade): internal/logs/loki_datasource.go, internal/logs/loki_test.go, internal/logs/runtime_log_source_snapshot.go, internal/logs/testdata/perses-loki-datasource/loki.json

## 1. PLAN (numbered)

- 1) Reality witness: fetch origin --prune; develop HEAD = 1019190d (1598 merged), PR #1616 head = ed401f460 (behind), base = fac01c77. Planning repo /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan verified (origin/main baseharbor-plan.git).
- 2) Monotonic merge-hopf onto develop (no rebase/reset/force): git merge origin/develop. New head 94f4eb10. rc0: `git merge-base --is-ancestor origin/develop HEAD` = 0. rc1: `git merge-base --is-ancestor ed401f460 HEAD` = 0. merge-tree --write-tree origin/develop HEAD = 7f70f44b (0 conflict). diff --name-only origin/develop HEAD = 4 write-set files.
- 3) Multi-source query defect found by CODEX-REVIEW/abnahme (functional defect at prior head 7d6538b45). Fix in internal/logs/loki_datasource.go persesLokiDatasourceQuery: one queryStream call per authorized source, exactly one single-pair selector per call, no comma-listed or 'or'-composed selector.
- 4) Test in internal/logs/loki_test.go: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (records both per-source queries, asserts one valid single selector each, no duplicate label name, no 'or'), TestPersesLokiDatasourceMultiSourcePartialMatchability (one source verified => healthy), TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (no match => error). PKI helper materializeLokiServiceAccessPKI (throwaway self-signed CA + server leaf for localhost) + recordingQueryCaptureServer (HTTPS, records raw queries).
- 5) Focused checks: go build ./... PASS, go vet ./internal/logs PASS, go test ./internal/logs -count=1 PASS (all internal/logs green), bash scripts/ci-fast-check.sh PASS (275 tests, source readability PASS, workflow policy PASS), gofmt clean.
- 6) Commit 7042ee61 (write-set only), push draft=false. Exact-run 44557985875 terminal SUCCESS 13 success / 17 skipped at head 7042ee61. PR #1616 head = 7042ee61, base = 1019190d.
- 7) Evidence written from own /var/tmp clone; evidence path to origin/main; card stays active (owner sets review after terminal green).
- 8) Host cleanup: docker/podman ps before/after + 'cleanliness:' line.

## 2. The defect (old query build, wörtlich)

Three lines before the fix (internal/logs/loki_datasource.go, persesLokiDatasourceQuery):

    matchers := make([]string, 0, len(sources))
    for _, source := range sources {
        matchers = append(matchers, fmt.Sprintf(`baseharbor_application=%q,baseharbor_service=%q`, source.OwnerApplication, logServiceLabel(source)))
    }
    query := "{" + strings.Join(matchers, ",") + "}"
    return probe.queryStream(ctx, endpoint, query)

With two sources this produced one selector
`{baseharbor_application="a",baseharbor_service="s1",baseharbor_application="b",baseharbor_service="s2"}`
— duplicate `baseharbor_application` label names inside one selector.

## 3. Why comma-within-one-selector is wrong (LogQL source)

Per the LogQL documentation (https://grafana.com/docs/loki/latest/query/log_queries/) a log query has exactly one log stream selector, and a single selector forbids duplicate label names (the comma list is read as simultaneous, logical-AND matchers on the same labels). A selector that repeats `baseharbor_application` is therefore not a union of the two sources — it is a single AND query that a healthy Loki with several sources does not match. The per-backend backend-witness that card 0428-086 requires (availability per source, not a single global verdict) was returning a false down.

## 4. The new composition (query profile)

One queryStream call per authorized source, each carrying exactly one selector:

    matchedAny := false
    for _, source := range sources {
        query := fmt.Sprintf(`{baseharbor_application=%q,baseharbor_service=%q}`, source.OwnerApplication, logServiceLabel(source))
        matched, err := probe.queryStream(ctx, endpoint, query)
        if err != nil {
            return false, fmt.Errorf("perses Loki datasource query for source %s: %w", source.ID, err)
        }
        if matched {
            matchedAny = true
        }
    }
    return matchedAny, nil

Recorded query profile (multi-source test, two sources api + worker):
    {baseharbor_application="perses-loki-demo",baseharbor_service="api"}
    {baseharbor_application="perses-loki-demo",baseharbor_service="worker"}
Two calls, two different single-pair selectors, no duplicate label name in any selector, no 'or' between selectors.

Health policy per source: `verified` (true) only when a real matching stream is returned for that source; a probe error on any source is propagated, and a source that returns no matching stream is reported as unavailable for that source (matchedAny semantics). Partial availability (one source verified) is healthy; a total miss returns an error (fail-closed).

## 5. Test-id + gate

- Test id (all in internal/logs, package logs_test, runs in CI package/unit + go-vet + go-build):
    - TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource
    - TestPersesLokiDatasourceMultiSourcePartialMatchability
    - TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed
- Gate: CI `PR · Go unit · owner` / `PR · Go unit · packages` (package internal/logs) and `PR · Validation · go-vet` / `PR · Validation · go-build`. Trigger: PR Selected Checks on push of lane-0428-086-perses-loki-source.

## 6. Run receipt

- Run id: 44557985875 (CI · PR #1616)
- Terminal conclusion: success
- Head: 7042ee612430b472ba16cdaffbec0684e78686f6
- Composition: 13 successful non-skipped jobs, 17 skipped (wave-admission Pre-Release/HA gates). Successful: Workflow policy, PR · Native gate plan, PR · Source format, PR · Trusted Plan, PR · Validation · go-build, PR · Validation · go-vet, PR · Focused Python, PR · Go unit · cli-3, cli-0, cli-1, owner, cli-2, packages.
- PR Selected Checks (required): all pass at head 7042ee61.

### Why the previous runs do not count for this head

- Run 44548246953 was terminal SUCCESS but at head ed401f460 (pre-fix, behind develop). It never exercised the multi-source selector path: its tests seeded exactly one source and never asserted the composed query string. A green aggregate on an unchanged commit is not evidence for a case no test builds.
- Run 44052892273 (CODEX-REVIEW welle 4 ACCEPT) was at head 7d6538b45 (pre-fix). It accepted content at that head; it is not a receipt for the fix head 7042ee61.
- Per baseharbor/AGENTS.md minimal CI receipts: an unambiguous full selection already ran at the exact new head, so this run is the receipt; no evidence reuse across different SHAs.

## 7. repo-rule compliance

- Write-set: only internal/logs/loki_datasource.go + internal/logs/loki_test.go changed vs hopf base (runtime_log_source_snapshot.go + testdata unchanged from hopf). No cmd/baha, no docs/cli, no internal/metrics/perses_prometheus_datasource, no internal/machine/contract.go, no observability/registry.go, no cmd/baha/app_status_result.go.
- No .github/** edited, no scripts/** edited, no workflow_dispatch, no rerun triggered by me (CI started by the lane push).
- Branch provenance: 94f4eb10 (hopf) is a monotonic merge of origin/develop 1019190d; `git merge-base --is-ancestor origin/develop 7042ee61` = 0 and `git merge-base --is-ancestor ed401f460 7042ee61` = 0. No branch cut from another PR head.
- One integration candidate per chain: lane-0428-086-perses-loki-source only. No second branch.
- No merge by me. No subagents (§4.8). All steps in this own session.
- Evidence lives only in baseharbor-plan (this file), never in the product repo.
- Planning clone: /var/tmp/plan-086/clone against https://github.com/mcpdev80/baseharbor-plan.git; rebase origin/main 8e2d7041 (no force, no reset over foreign commits). Shared copy /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan: no git action.

## 8. Host cleanup (docker/podman)

- Before: no containers/networks/volumes started this lane (pure Go unit + CI; no compose/docker/podman test stack).
- After: ps-witness below.
- cleanliness: clean (no test containers/networks/volumes left by this lane)

docker ps -a 2>&1 | wc -l ; docker network ls 2>&1 | wc -l ; docker volume ls 2>&1 | wc -l

## END

END_BLOCKED mission-086-pr1616-laptop.md: functional defect (multi-source Loki selector) fixed at head 7042ee61, CI run 44557985875 terminal SUCCESS; evidence written, card left active for owner review-transition, END pending owner sign-off.
